---
title: "How to make interactive charts you can email – Nicola Rennie"
date: 2026-11-04
url: "https://elink56e.dataelixir.com/ss/c/u001.j-XgCKvFNabSVzP6jGY2YRq6GH3Ac_M8jH19-63qhmHMklKUpJciSbqsARiea1z3TyV-rap682eyQ5ZNHVCyLtRu3xy-0b5Sefvs2xyj1XJfKKtepLjaumMQJ2NIy_rLJd6OhbDuCAJOSH1l_eSEb1LjktN5MjDrwHMFvSPGtmT9hpXBURd_rD1AOwqERbbrXAo-IQmHAxVpftrgQZnheG_toNxhseNImnz1jJdRP2g/4vf/9_2zRaPmRUOeF_YxJ4YDRg/h13/h001.mMvfSk_VPIqwyoH4fhM4dHQnOc7oJwCvMq7FjkO09hg"
authors: ["Nicola Rennie"]
keywords: ["ggiraph", "R", "graphiques interactifs", "ggplot2", "Quarto", "visualisation de données"]
theme: "Data"
tone: "tutorial"
used_in: ["2026-11-04"]
---

## Résumé
L'article explique comment créer des graphiques interactifs en R qui peuvent être partagés simplement par email, sans serveur ni dépendance externe. L'auteure part d'un graphique `ggplot2` statique et montre comment le rendre interactif avec le package `ggiraph`, en ajoutant des tooltips puis un menu déroulant piloté par un peu de JavaScript. La solution finale consiste à exporter le tout dans un document Quarto avec `embed-resources: true`, produisant un fichier HTML autonome contenant toutes les données, envoyable en pièce jointe et utilisable directement dans un navigateur.

## Points clés
- `ggiraph` permet de transformer des graphiques `ggplot2` en versions interactives en remplaçant les `geom_*()` par leurs équivalents `_interactive()`, puis en les enveloppant dans `girafe()`.
- Les tooltips s'ajoutent simplement via l'esthétique `tooltip`, et des interactions plus riches (ex. menu déroulant) passent par l'esthétique `data_id` combinée à un peu de JavaScript et CSS.
- L'auteure déconseille `ggplotly()` (package `plotly`) comme méthode de conversion, lui préférant `ggiraph`.
- La technique évite les problèmes classiques de partage (serveur Shiny requis, R à installer, JavaScript bloqué dans les emails) car toutes les données sont déjà intégrées et seul du CSS pilote l'affichage/masquage.
- Exporter le résultat dans un document Quarto avec l'option `embed-resources: true` produit un fichier `.html` autonome, envoyable par email et ouvrable dans n'importe quel navigateur.
- Le rendu du document peut être plus lent à générer, mais l'expérience utilisateur finale reste très réactive puisqu'aucune donnée n'est rechargée au changement de sélection.

## Analyse approfondie
```
library(ggplot2)
library(dplyr)
set.seed(20261027)
plot_data <- diamonds |>
  group_by(cut) |>
  slice_sample(n = 100) |>
  ungroup()
```
Je ne vais pas commencer par un long débat sur la question de savoir si vous devriez ajouter de l'interactivité à vos graphiques, car cela pourrait faire l'objet de plusieurs articles à lui seul. Mais je vous demanderai au moins de garder en tête que *ce n'est pas parce que vous pouvez le faire que vous devez le faire* !

Si l'interactivité est nécessaire, elle crée un problème supplémentaire : comment partager le graphique avec quelqu'un d'autre ? Vous ne pouvez plus simplement lui envoyer un fichier PNG ou un document Word contenant votre graphique. Il existe de nombreuses façons de créer des graphiques interactifs, via des outils comme Shiny en R ou Python, en utilisant ObservableJS dans des documents Quarto, ou en créant une application Javascript à partir de zéro. Cependant, chacune de ces approches a ses propres problèmes en matière de partage. Un tableau de bord interactif créé avec Shiny a besoin d'un serveur pour s'exécuter (même si Shinylive résout ce problème, cela peut être lent), ou bien il faut que la personne destinataire ait R installé pour l'exécuter localement. Les documents Quarto avec des graphiques ObservableJS intégrés peuvent s'exécuter entièrement dans le navigateur, mais si vous envoyez par email un fichier HTML contenant du JavaScript intégré, celui-ci ne s'exécutera pas. À la place du graphique, le destinataire obtiendra une erreur qui ressemble à peu près à ceci.

Bien que cela soit gênant, il s'agit en fait d'une fonctionnalité utile. Cela signifie que du JavaScript arbitraire ne peut pas simplement s'exécuter dans votre navigateur — et donc sur votre ordinateur — simplement parce que vous avez cliqué sur un fichier que quelqu'un vous a envoyé. Alors, est-il possible d'envoyer un graphique interactif à quelqu'un par email ? Oui, c'est possible. Et nous allons le construire en R.

## Commencer par un graphique statique

Commençons par récupérer des données que nous pourrons utiliser pour cet exemple. Nous allons ici utiliser le jeu de données `diamonds` fourni avec `ggplot2`. C'est un jeu de données assez long, avec environ 55 000 lignes. Uniquement pour accélérer un peu le rendu de cet article, je vais échantillonner un sous-ensemble de lignes afin de n'en garder que 500 à utiliser. Évidemment, ne faites pas ça avec vos propres données !

Jetons un œil à ce nuage de points plutôt générique, avec des points colorés selon la colonne `cut`. Au lieu de (ou en plus de) la couleur, nous pourrions utiliser l'interaction pour mettre en évidence les catégories de `cut`. Cela pourrait prendre la forme de tooltips (infobulles), d'une mise en surbrillance au survol, ou d'un menu déroulant.

```
ggplot(
  data = plot_data,
  mapping = aes(x = carat, y = price, colour = cut, shape = cut)
) +
  geom_point()
```
Commençons par déterminer comment transformer notre graphique `ggplot2` statique en un graphique interactif. Certains d'entre vous vont peut-être se tourner vers la fonction `ggplotly()` du package `plotly`, et je vous demanderais gentiment de la reposer. Charlotte Hadley explique pourquoi dans son article de blog. Il existe une bien meilleure façon de créer des graphiques interactifs.

## Des graphiques interactifs avec `ggiraph`

Le package `ggiraph` permet de créer des graphiques `ggplot` interactifs, et vous permet d'ajouter des tooltips, des effets de survol et des actions JavaScript aux graphiques.

Il y a deux étapes principales pour créer une version interactive de votre graphique `ggplot2` :

1. Remplacez vos appels `geom_` par la version `_interactive()` fournie par `ggiraph`. L'exemple ci-dessous utilise `geom_point_interactive()` à la place de `geom_point()`.

```
library(ggiraph)
g <- ggplot(
  data = plot_data,
  mapping = aes(x = carat, y = price, colour = cut, shape = cut)
) +
  geom_point_interactive()
```
2. Enveloppez le code de votre graphique dans la fonction `girafe()`, qui effectue tout le travail nécessaire pour le rendre interactif.

`girafe(ggobj = g)`
C'est le type de graphique interactif le plus simple que l'on puisse créer : la seule fonctionnalité supplémentaire est une barre d'outils en haut qui permet à l'utilisateur de télécharger plus facilement l'image. Vous voudrez probablement ajouter un peu plus que cela.

Si vous essayez de créer un graphique interactif et qu'il n'existe pas de `geom_*_interactive()` correspondant, il existe souvent des moyens de contourner ce problème. Vous pouvez voir un exemple de création de graphiques en essaim (beeswarm) interactifs dans cet article de blog.

### Ajouter des tooltips aux graphiques

La chose la plus simple à ajouter ensuite, ce sont des tooltips qui apparaissent lorsque l'utilisateur survole un point. Pour cela, on associe (map) une colonne des données à l'esthétique `tooltip` à l'intérieur de notre fonction geom interactive, tout comme on le ferait avec `fill` ou `colour`. Pour des tooltips plus complexes, vous pouvez ajouter du formatage HTML, ou combiner des colonnes avec du texte en utilisant `glue()`. Je conseillerais de faire cela lors de l'étape de préparation des données (data wrangling), plutôt que directement dans l'appel `aes()`. Dans l'exemple ci-dessous, nous associons la colonne `cut` au tooltip.

```
g <- ggplot(
  data = plot_data,
  mapping = aes(x = carat, y = price, colour = cut, shape = cut)
) +
  geom_point_interactive(
    mapping = aes(tooltip = cut)
  )
girafe(ggobj = g)
```
## Des graphiques interactifs plus complexes

Les tooltips sont une fonctionnalité interactive plutôt passive, et ce que l'on veut souvent réellement quand on parle de graphiques interactifs, c'est un moyen pour l'utilisateur de faire un choix et de le voir se refléter dans le graphique.

### Relier des menus déroulants à `ggiraph`

Il nous faut un moyen de relier les options de notre menu déroulant au graphique. Heureusement, `ggiraph` dispose déjà de cette fonctionnalité intégrée. Nous associons la colonne de nos données qui correspond aux *valeurs* du menu déroulant (pas aux noms) à l'esthétique `data_id`.

*Remarque : j'ai retiré ici les associations de couleur et de forme, car une seule catégorie sera affichée à la fois dans la version interactive que nous créons.*

```
g <- ggplot(
  data = plot_data,
  mapping = aes(x = carat, y = price)
) +
  geom_point_interactive(
    mapping = aes(
      tooltip = cut,
      data_id = cut
    )
  )
```
Pour garder un code propre et bien organisé, nous allons enregistrer notre graphique interactif dans un objet plutôt que de le rendre immédiatement.

`g_int <- girafe(ggobj = g)`
Nous pouvons ensuite le passer à `tagList()` du package `htmltools` pour les garder ensemble lors du rendu :

```
browsable(
  tagList(
    dropdown_html,
    g_int
  )
)
```
La fonction `browsable()` permet de faire en sorte que certains objets soient rendus comme du HTML par défaut lorsqu'ils sont affichés dans la console, plutôt que d'être simplement imprimés comme du texte HTML. Si vous effectuez le rendu uniquement dans un document Quarto, vous n'avez pas besoin d'utiliser `browsable()`, mais c'est utile pour le débogage lorsque vous travaillez de façon interactive dans une console.

### Ajouter des actions au menu déroulant

Pour l'instant, notre menu déroulant et notre graphique ne sont que partiellement liés. Si vous testez la version ci-dessus, vous remarquerez que rien ne se passe lorsque la sélection du menu déroulant change. Cela s'explique par le fait que nous n'avons écrit aucun code pour définir *ce qui* doit se passer quand le menu déroulant change.

Pour cela, nous allons ajouter un petit bout de Javascript dans nos éléments `browsable()`. Je commence par reconnaître que le code ci-dessous a l'air plutôt horrible. Le Javascript peut sembler assez intimidant, et l'écrire entièrement dans une seule chaîne de caractères n'est certainement pas la façon la plus conviviale de procéder. Mais allons-y tout de même…

Commençons par créer une fonction contenant une instruction `if`. Le code ci-dessous indique que si la valeur `cut` (associée via `data_id`) d'un point donné est égale à la valeur sélectionnée dans le menu déroulant, alors ce point doit être affiché. Sinon, il ne doit pas être affiché.

```
browsable(
  tagList(
    dropdown_html,
    g_int,
    tags$script(HTML("
      function filterByDropdown(selected) {
        document.querySelectorAll('[data-id]').forEach(el => {
          if (el.getAttribute('data-id') === selected) {
            el.setAttribute('style', 'display:block;');
          } else {
            el.setAttribute('style', 'display:none;');
          }
        });
      }
    "))
  )
)
```
Nous ajoutons ensuite un peu de Javascript supplémentaire qui indique au graphique de se mettre à jour et d'exécuter notre fonction contenant l'instruction `if` chaque fois que le menu déroulant est modifié pour sélectionner une valeur différente.

```
browsable(
  tagList(
    dropdown_html,
    g_int,
    tags$script(HTML("
      function filterByDropdown(selected) {
        document.querySelectorAll('[data-id]').forEach(el => {
          if (el.getAttribute('data-id') === selected) {
            el.setAttribute('style', 'display:block;');
          } else {
            el.setAttribute('style', 'display:none;');
          }
        });
      }
      document.getElementById('dropdown').addEventListener('change', function() {
        filterByDropdown(this.value);
      });
    "))
  )
)
```
Lorsque le graphique s'affiche pour la première fois sur la page, l'écouteur d'événement (event listener) ne reconnaît pas cela comme un *changement* du menu déroulant, si bien que tous les points sont rendus par défaut avant que l'instruction `if` ne s'exécute pour la première fois. Notre dernier petit bout de Javascript consiste à forcer l'exécution de notre instruction `if` avec la valeur par défaut initiale au chargement de la page.

```
browsable(
  tagList(
    dropdown_html,
    g_int,
    tags$script(HTML("
      function filterByDropdown(selected) {
        document.querySelectorAll('[data-id]').forEach(el => {
          if (el.getAttribute('data-id') === selected) {
            el.setAttribute('style', 'display:block;');
          } else {
            el.setAttribute('style', 'display:none;');
          }
        });
      }
      document.getElementById('dropdown').addEventListener('change', function() {
        filterByDropdown(this.value);
      });
      document.addEventListener('DOMContentLoaded', function() {
        const initialSelected = document.getElementById('dropdown').value;
        filterByDropdown(initialSelected);
      });
    "))
  )
)
```
Si vous souhaitez ajouter un peu de style à votre menu déroulant, par exemple pour définir une largeur minimale ou utiliser des couleurs différentes, vous pouvez ajouter du CSS qui cible soit tous les éléments `select`, soit spécifiquement votre menu `#dropdown`.

Et voilà, nous avons maintenant un graphique interactif pleinement fonctionnel, où les données affichées changent selon ce que l'utilisateur sélectionne dans le menu déroulant. Si vous créez des graphiques interactifs avec des outils comme Shiny depuis un certain temps, cela ne vous semblera peut-être pas extraordinaire. Cependant, la beauté de cette approche, c'est que vous n'avez pas à vous soucier du déploiement. La façon la plus simple de partager cela avec quelqu'un d'autre est de tout intégrer dans un document Quarto et de le lui envoyer par email. Pour vous assurer que tous les éléments nécessaires sont inclus dans la sortie HTML, définissez `embed-resources: true`.

```
---
format: 
  html: 
    embed-resources: true
---
```
Le résultat sera un fichier `.html`. Vous pouvez alors envoyer ce fichier en pièce jointe d'un email. Lorsque votre destinataire reçoit l'email, il peut télécharger la pièce jointe et double-cliquer sur celle-ci pour l'ouvrir dans un navigateur web. Il pourra alors interagir avec le graphique, exactement comme vous l'avez fait.

Cela fonctionne parce que notre graphique interactif initial contient en réalité toutes les données, et nous utilisons simplement du CSS pour définir quels éléments sont masqués ou affichés en fonction du menu déroulant. Un changement dans le menu déroulant ne nécessite donc pas de récupérer de nouvelles données, ni de reconstruire l'ensemble du graphique avec du Javascript. Cela peut parfois rendre le rendu du document Quarto un peu lent, mais l'expérience utilisateur est en général très réactive.

Vous trouverez ici un lien vers un document Quarto complet. Je recommande également de consulter le livre `ggiraph` pour davantage d'exemples des types d'interactivité que vous pouvez ajouter.

## Réutilisation

## Citation

```
@online{rennie2026,
  author = {Rennie, Nicola},
  title = {How to Make Interactive Charts You Can Email},
  date = {2026-10-27},
  url = {https://nrennie.rbind.io/blog/interactive-charts-ggiraph/},
  langid = {en}
}
```

## Pourquoi ça compte
Ce tutoriel apporte une solution concrète et peu coûteuse à un problème récurrent en data viz — le partage de graphiques interactifs sans infrastructure serveur — ce qui en fait une référence utile pour les équipes data qui communiquent par email ou rapports statiques avec des parties prenantes non techniques.
