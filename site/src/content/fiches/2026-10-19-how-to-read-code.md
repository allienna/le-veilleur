---
title: "How to read code"
date: 2026-10-19
url: "https://programmingdigest.net/links/23483/8e384055-4ef6-4411-8656-1644e3ae163f/email"
keywords: ["lecture de code", "revue de code", "IA générative", "ingénierie logicielle", "diff", "LLM"]
theme: "Tech"
tone: "opinion"
used_in: ["2026-10-19"]
---

## Résumé
L'article défend l'idée que lire du code n'a rien à voir avec lire un texte en anglais : le code est fait pour être exécuté par une machine, se lit surtout sous forme de diffs plutôt que comme un produit fini, et sa complexité structurelle dépasse largement celle des textes les plus difficiles. L'auteur propose une méthode de lecture « en plusieurs passes » (structure globale, puis sous-structure, puis détails) plutôt qu'une lecture linéaire. Il conclut en réfutant l'idée que les LLM rendraient la lecture de code obsolète : d'après son expérience, le code généré par IA contient régulièrement des erreurs d'alignement avec les valeurs techniques de l'équipe, pas seulement des bugs, et doit donc toujours être relu attentivement par un humain.

## Points clés
- Le code diffère fondamentalement du texte en langue naturelle : son ordre est dicté par la machine (compilation, exécution), pas par la lisibilité humaine, et les dépendances peuvent s'étendre sur toute une base de code plutôt que sur un seul paragraphe.
- On lit le code presque toujours comme un diff (changement incrémental sur de l'existant), rarement comme une œuvre achevée — ce qui change complètement la façon d'en suivre le fil.
- La plupart des gens lisent mal le code : en le parcourant linéairement comme un livre, en se focalisant uniquement sur les lignes modifiées (en ratant l'impact sur le code non modifié), ou en abandonnant et en devinant.
- La technique recommandée, inspirée de la lecture des articles de mathématiques (« dyadic scanning »), consiste à faire plusieurs passes : d'abord repérer le chemin d'exécution principal (happy path) en suivant les appels de fonctions, puis affiner progressivement jusqu'aux détails, en traitant tout le reste comme une boîte noire.
- Une dernière lecture linéaire complète n'intervient qu'à la fin, une fois la structure comprise, pour repérer les détails inhabituels manqués lors des passes précédentes.
- Le code généré par IA doit toujours être relu : l'auteur y trouve régulièrement des erreurs non pas de bug mais d'alignement (l'IA fait ce qu'elle a cru bon de faire, mais pas ce qui correspond aux valeurs techniques de l'équipe) — illustré par un agent ayant transformé un petit changement en un diff de 3000 lignes pour « corriger » une race condition en réalité inoffensive.

## Analyse approfondie
**Pourquoi lire du code n'est pas comme lire un livre**

Tout le monde sait lire un livre : on commence à la première page, on lit chaque mot dans l'ordre, en s'arrêtant de temps en temps pour réfléchir, jusqu'à la dernière page. C'est ainsi qu'on lit un article de presse, un poème ou un e-mail. Pourquoi la lecture de code serait-elle différente ?

Le texte en anglais (ou dans toute langue naturelle) est conçu pour être lu dans l'ordre : il n'existe presque aucune contrainte sur l'ordre d'un texte, si ce n'est la façon dont l'auteur veut que le lecteur le parcoure. En écrivant un billet, on peut organiser ses idées dans l'ordre qu'on souhaite. Le code, à l'inverse, est conçu pour être *exécuté* par un ordinateur : son ordre est donc avant tout déterminé par des contraintes non humaines. On ne peut pas simplement déplacer une ligne de code au début d'un fichier ou d'une fonction parce qu'elle offrirait une meilleure introduction pour un lecteur humain — la contrainte principale reste que le code doit compiler (ou s'exécuter sans erreur de syntaxe), avant même d'être lisible.

La deuxième grande différence est que le texte en langue naturelle est toujours lu comme un produit final, alors que le code est le plus souvent lu sous forme de *diff*. Les ingénieurs passent la majeure partie de leur temps à lire des modifications subtiles apportées à du code existant, pas des programmes entièrement nouveaux. Imaginez si lire un article revenait à lire chaque brouillon successif dans l'ordre où il a été écrit, en consommant le texte phrase changée par phrase changée : il deviendrait facile de perdre le fil global.

La troisième raison — et l'auteur le dit en amoureux de la littérature et de la poésie — est que le code est structurellement bien plus complexe que les textes en langue naturelle. Même les livres réputés difficiles sont *syntaxiquement* plus simples que la plupart des programmes informatiques : par exemple, les dépendances grammaticales restent largement circonscrites à un seul paragraphe, alors que les dépendances dans le code peuvent s'étendre à l'ensemble de la base de code. La difficulté principale d'un roman tient à la compréhension des nuances de la nature humaine qui y sont discutées, pas à la fonction grammaticale de chaque mot. Les grandes bases de code sont aussi simplement plus longues : *Guerre et Paix* compte environ 600 000 mots, alors que la plupart des grandes bases de code modernes comptent autant de *lignes*.

Comme l'auteur l'a répété à plusieurs reprises, les grands programmes informatiques sont simplement trop complexes pour qu'une seule personne les comprenne entièrement. Lire du code dans un grand programme est donc un processus de *compromis* : il faut décider quelles parties comprendre en profondeur et lesquelles survoler, c'est-à-dire répartir une capacité mentale finie sur l'ensemble de la base de code.

**Pourquoi la plupart des gens lisent mal le code**

À cause de tout cela, la plupart des gens lisent très mal le code. Soit ils s'acharnent à le lire de bout en bout, comme un livre, et perdent le fil du flux d'exécution. Soit ils se contentent de lire le diff et passent à côté de l'importance des parties non modifiées. Soit ils sont simplement vaincus par la complexité, abandonnent et devinent ce que le code signifie. Comment faire mieux ?

Le meilleur article que l'auteur ait lu sur ce sujet porte en réalité sur la lecture des articles de mathématiques, qui ont une structure similaire. L'auteur de ce texte décrit une technique appelée « dyadic scanning » (balayage dyadique) : plutôt que de lire lentement et séquentiellement, on effectue plusieurs passes — d'abord pour cerner la structure globale, puis la sous-structure, puis enfin les détails.

Pour le code, cela signifie lire dans le désordre. L'auteur aime choisir un chemin important (par exemple le « happy path » de la fonctionnalité introduite dans le diff) et suivre quelles fonctions appellent quelles autres fonctions, juste pour avoir une idée du flux. Ce n'est qu'une fois cette vue d'ensemble acquise qu'il prête une attention minutieuse à ce que ces fonctions font réellement.

En général, il effectue plusieurs passes, chacune suivant un fil différent. Il prend une fonction ou une donnée et essaie de comprendre comment elle est utilisée, en élargissant vers plusieurs sites d'appel (y compris en dehors du diff) au fur et à mesure. Pour les petits diffs, il fait simplement un ctrl+F pour chercher le nom de la fonction et naviguer ; pour les diffs plus volumineux, il ouvre le code dans un éditeur et utilise le ctrl+clic pour naviguer plus facilement. Il s'efforce de rester impitoyablement concentré sur l'élément qu'il regarde à l'instant : tout le reste est traité comme une boîte noire.

Une fois convaincu de comprendre le diff, il s'assoit alors seulement pour le lire attentivement de bout en bout. Le but de cette lecture n'est pas tant d'en apprendre sur la structure — qu'il devrait déjà connaître à ce stade — que de repérer les éléments de code inhabituels qu'il n'aurait pas remarqués lors des passes précédentes effectuées dans le désordre. S'il repère quelque chose d'inhabituel, il recommence alors de nouvelles passes.

Cela peut sembler lent. Mais en réalité, chaque passe est très rapide, car il ne s'agit pas de décortiquer laborieusement chaque ligne de code.

**Les LLM ne dispensent pas de lire le code**

Beaucoup affirment aujourd'hui qu'il n'est plus nécessaire de lire le code : soit parce que les LLM produiraient désormais du code fiable et de haute qualité sans supervision, soit parce qu'on pourrait simplement demander à un LLM relecteur de lire le code à notre place. L'auteur juge ces deux idées fausses.

Évidemment, la qualité du code produit par une IA dépend du contexte. Comme évoqué dans un précédent billet intitulé *Pure and impure software engineering*, certains domaines du logiciel (jeux vidéo, bibliothèques, outils comme les bases de données) ont des standards, pratiques et valeurs d'ingénierie radicalement différents d'autres domaines (par exemple les systèmes distribués dans les grandes entreprises technologiques). Si l'on crée simplement un outil pour soi-même, on peut sans doute se dispenser de lire le code si on le souhaite. Mais après avoir lu beaucoup de code généré par IA cette année, l'auteur affirme qu'il faut absolument continuer à le lire.

Il trouve *régulièrement* des erreurs massives dans le code généré par IA. Ce ne sont pas des bugs — le code fait généralement ce que l'IA a voulu qu'il fasse — mais plutôt des problèmes d'alignement. Exemple récent : un petit changement destiné à faire transiter une valeur supplémentaire à travers du code existant s'est transformé en un diff complexe de trois mille lignes, parce que l'agent avait repéré une race condition et construit une mécanique complexe pour la « corriger ». En réalité, cette race condition était inoffensive par conception : deux éléments de données sans lien pouvaient se désynchroniser brièvement, sans aucun impact pour le client.

Les LLM peuvent-ils simplement lire le code à notre place ? Non, pour la même raison : même s'ils ne commettent aucune erreur, leurs valeurs techniques ne correspondront pas aux nôtres ni à celles de notre entreprise. On peut utiliser les LLM pour nous aider à lire du code, mais il faut alors relire et vérifier attentivement ce que produit le LLM, tout en continuant à lire soigneusement le code lui-même.

**Notes**
1. Dans la pratique, beaucoup de gens ne lisent pas réellement ainsi : il est courant de sauter des mots voire des paragraphes entiers par inattention, ou de lire un livre entier sans jamais prendre le temps d'y réfléchir. Mais en théorie, tout le monde s'accorde sur le fait que c'est ainsi qu'on devrait lire.
2. On peut bien sûr réorganiser certaines parties du code dans certains langages plus que d'autres, mais la contrainte *principale* reste l'ordinateur : il est plus important que le code compile (ou s'exécute sans erreur de syntaxe) que d'être lisible.
3. L'auteur ne veut pas minimiser l'importance de l'analyse syntaxique de la grande littérature, un exercice qu'il juge à la fois difficile et sous-estimé. Il cite en exemple la première scène d'*Hamlet*, où une phrase relativement courte exige un effort pour déterminer à quoi renvoient certains pronoms et relatifs — de même qu'une fonction peut avoir de nombreux appelants dispersés, une phrase d'un texte peut modifier le sens de nombreuses autres.
4. Dans un billet précédent, l'auteur avait identifié cela comme la principale erreur commise par la plupart des ingénieurs lors des revues de code.
5. Il s'agit ici d'un diff significatif, touchant quelques centaines de lignes ou plus. Les diffs triviaux peuvent, eux, être lus de bout en bout sans difficulté.

## Pourquoi ça compte
Ce billet apporte un cadre méthodologique utile pour la revue de code à l'ère des agents d'IA générative : il rappelle qu'un code généré rapidement n'élimine pas le besoin de relecture humaine experte, car les erreurs d'alignement avec les valeurs techniques d'une équipe sont aussi dangereuses que les bugs classiques.
