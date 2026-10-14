---
title: "Social Graph Builder: Open-Source Map of How Engineers Collaborate | Unblocked"
date: 2026-10-14
url: "https://elinkc09.newsletter.manager.dev/ss/c/u001.eqcFzdcasjwIo5IEEZj2cBtajTrEBOSiykbD5ObqWDMMDnsZc4Jo7xobxXodqiNs3I6ByAUOHBMcX1ZPhOlPBnA382WDpfcMRMzXPNywh5p-Q4bENYEMw2PAxTOV7JFWEd5B1KCsvM_bgaQh2kCzK8XsH_S-asluP57vj0TtKWfS2bkUDcmozZhlXk0jAPurz8VbxcKL4IHQPciMJTAYNZJPylrkNQkzr1RDXLkcp5zYfCGY5osv3cC3p1Z60IPg6JfShSMIu9AShD3umhdd9ipyp8NTbbidwbk1YgmVQJg/4uu/NLnvxY0cSrivpEOaskP88w/h1/h001.UGv0WlSMbs5s2UsYQcBiQe6j5c5xFHwOHQoLOFRfHmc"
keywords: ["graphe de collaboration", "revue de code", "bus factor", "open source", "détection de communautés", "context engine"]
theme: "Leadership"
tone: "news"
used_in: ["2026-10-14"]
---

## Résumé
Unblocked publie en open source « Social Graph Builder », un outil en ligne de commande qui reconstruit un graphe pondéré de collaboration à partir de l'historique des pull requests GitHub, afin de révéler qui relit le code de qui, de détecter automatiquement les équipes, d'identifier les experts par zone de code et de signaler les silos de connaissance (bus factor). L'algorithme combine un amortissement logarithmique des interactions, une décroissance temporelle gaussienne, une détection de communautés de type Louvain bonifiée pour les revues mutuelles, ainsi qu'un score d'expertise fondé sur plusieurs signaux issus de `git log`. Le résultat est une visualisation HTML interactive (graphe, heat map, tableaux de pairs, cartes d'équipe, classement d'experts) utilisable de façon autonome. Chez Unblocked, cet outil constitue aussi une brique de leur « context engine », servant de signal de pertinence pour aider des agents IA à arbitrer entre des sources de documentation contradictoires.

## Points clés
- L'outil interroge l'API GraphQL de GitHub pour reconstruire, à partir des PR, un graphe pondéré des relations de revue de code.
- Il produit un fichier HTML unique offrant cinq vues : graphe interactif à disposition par forces, heat map relecteur/auteur, tableaux de pairs, cartes d'équipe (avec libellé généré par IA via Claude, optionnel) et classement d'experts avec badge de bus factor.
- L'algorithme repose sur quatre mécanismes : amortissement logarithmique des scores d'interaction, décroissance temporelle gaussienne (constante de 16 semaines), détection de communautés de Louvain avec bonus ×3 pour les relecteurs mutuels, et score d'expertise combinant lignes modifiées, nombre de commits, étendue des fichiers et récence.
- Unblocked présente ce graphe social comme un signal exploité en interne pour la « déconfliction » de sources contradictoires par des agents IA, en s'appuyant sur la proximité de collaboration et l'expertise réelle des personnes.
- L'installation se fait via `poetry` et PyInstaller ; un token GitHub est requis, une clé Anthropic est optionnelle, et les données sont mises en cache localement pour accélérer les exécutions suivantes.
- Le projet est disponible sur GitHub (`unblocked/engineering-social-graph`), avec algorithme documenté dans le README et contributions (issues, PR) bienvenues.

## Analyse approfondie
### Présentation
Unblocked met à disposition en open source Social Graph Builder, un outil en ligne de commande qui reconstruit un graphe pondéré de collaboration à partir de l'historique des pull requests GitHub. Pointé sur un dépôt, il identifie qui relit le code de qui, détecte les équipes à partir des schémas de revue, repère les experts de chaque zone du code et signale les silos de connaissance. Le résultat est une visualisation interactive consultable dans un navigateur. L'outil a été développé chez Unblocked comme composant de leur « context engine », mais se veut utile de façon autonome pour toute organisation.

### Le problème : personne ne sait précisément qui sait quoi
Dans une organisation, il existe presque toujours un répertoire de code que seule une personne a touché depuis des mois, sans que cela ait été une décision délibérée. Le « bus factor » (le risque de dépendre d'une seule personne) est alors de 1, et cela ne se révèle généralement qu'au moment où cette personne est absente pendant un incident.

Les organigrammes ne montrent que les lignes hiérarchiques : ils ne révèlent pas que deux ingénieurs d'équipes différentes se relisent mutuellement chaque semaine, que la « backend team » est en réalité composée de trois sous-groupes qui se chevauchent à peine, ou qu'un service critique repose sur un seul expert qui en a accumulé la responsabilité depuis 2024.

Cette information existe déjà — dans l'historique des PR, les fils de revue, les logs git — mais personne ne l'exploite systématiquement, car la reconstituer à la main est fastidieux, et l'image devient obsolète presque aussitôt qu'on la dresse.

### La solution : construire le graphe à partir des données déjà disponibles
Social Graph Builder récupère l'historique des PR via l'API GraphQL de GitHub, attribue un score à chaque interaction de revue, applique une décroissance temporelle pour privilégier les collaborations récentes, puis exécute un algorithme de détection de communautés pour identifier les véritables clusters d'équipe.

Le résultat est un unique fichier HTML comportant cinq vues :
- un graphe interactif à disposition dirigée par les forces, où les nœuds représentent les contributeurs (taille proportionnelle au volume de commits), les arêtes les relations de revue (pondérées par leur intensité), et où les clusters détectés sont entourés d'un cercle ; survoler met en évidence les connexions, cliquer affiche le détail ;
- une heat map croisant relecteurs et auteurs ;
- des tableaux de pairs avec le détail par personne et des barres d'intensité de collaboration ;
- des cartes d'équipe avec la composition détectée automatiquement et un libellé généré par IA (Claude, si une clé API est fournie, sinon un nom de répertoire par défaut) ;
- un classement des experts par zone de code, chacun assorti d'un badge de bus factor : propriétaire unique, à risque, partagé, ou bien couvert.

### Fonctionnement de l'algorithme
Trois idées structurent l'algorithme, bien que la logique s'articule en réalité autour de quatre mécanismes :
- **Score d'interaction avec amortissement logarithmique** : dix commentaires de revue sur une PR ne représentent pas dix fois l'engagement d'un seul commentaire, mais plutôt le double. Le calcul utilise une mise à l'échelle du type `1 + log₁₀(n)`, une approche sous-linéaire proche de celle de TF-IDF, afin que les commentateurs prolifiques ne dominent pas le graphe.
- **Décroissance temporelle gaussienne** : la contribution de chaque PR est pondérée par une fonction `exp(-t²/C²)` avec une constante de décroissance de 16 semaines. La courbe gaussienne maintient un plateau pour les derniers mois avant de décroître, ce qui permet de rester fortement connecté aux collaborateurs du dernier trimestre et pas seulement de la dernière semaine.
- **Détection d'équipe par algorithme de Louvain** : appliqué à une version non dirigée du graphe, avec un bonus de pondération ×3 (via moyenne géométrique) pour les relecteurs mutuels (A relit B et B relit A). Cela permet de distinguer nettement les coéquipiers, qui se relisent à parts à peu près égales, des relecteurs inter-équipes, dont la relation est le plus souvent unidirectionnelle.
- **Score d'expertise** : combine quatre signaux issus de `git log` — lignes modifiées (40 %), nombre de commits (30 %), étendue des fichiers touchés (20 %) et récence (10 %), tous pondérés par décroissance temporelle. Le bus factor correspond au nombre de contributeurs dont le score atteint au moins 20 % de celui du meilleur contributeur sur une zone donnée.

### Pourquoi Unblocked considère cela comme une « infrastructure de contexte »
Social Graph Builder fonctionne de façon autonome — on peut le cloner, l'exécuter et obtenir une image utile de son organisation sans s'intéresser au reste de l'écosystème Unblocked. Mais l'entreprise l'a conçu comme une brique de son « context engine », et c'est la raison de sa publication.

Le problème récurrent chez Unblocked : un agent doit répondre à une question du type « quelle est la bonne façon de gérer les feature flags dans ce service ? ». La documentation dit une chose, le code en fait une autre légèrement différente, et un fil Slack vieux de trois mois explique pourquoi le code a dévié. Un moteur de contexte doit alors déterminer quelle source privilégier — ou du moins signaler le désaccord avec assez de traçabilité pour qu'un humain puisse trancher. Unblocked appelle ce processus la « déconfliction ».

Le graphe social s'avère être un point d'appui utile dans ce processus : si la personne qui pose la question appartient à l'équipe paiements, et que les deux sources en désaccord ont été écrites par un ingénieur infrastructure et par le lead de l'équipe paiements, le graphe indique que ce dernier est un collaborateur plus proche de la personne, qu'il a déjà relu ses PR, et qu'il a une expertise directe sur la zone de code concernée. C'est un signal de pertinence : il ne règle pas le conflit automatiquement, mais donne au moteur une base pour classer quelle source importe le plus, pour cette personne, sur cette tâche précise.

Le même type de parcours dans le graphe aide à répondre à d'autres questions : qui devrait relire ce changement ? quelles conventions d'équipe s'appliquent ici ? la seule experte de cette zone a quitté l'entreprise il y a six mois — dans l'historique de revue de qui faut-il chercher pour reconstituer ce qu'elle savait ?

Unblocked utilise en interne le graphe social comme un signal parmi d'autres pour la synthèse et la déconfliction inter-systèmes. L'entreprise choisit de l'open-sourcer car les données de collaboration appartiennent à chacun, l'algorithme est documenté dans le README, et l'outil est utile de façon indépendante — mais, pour qui réfléchit à une infrastructure de contexte pour ses agents, il s'agit là d'une des pièces du puzzle.

### Démarrage rapide
L'installation se fait via `git clone` du dépôt `unblocked/engineering-social-graph`, puis `poetry install` et la construction d'un exécutable via PyInstaller. Il suffit ensuite de se placer dans un clone local d'un dépôt GitHub et de lancer `social-graph run` : l'outil récupère les PR, construit le graphe, détecte les équipes, calcule les scores d'expertise et ouvre la visualisation dans le navigateur. L'opération prend quelques minutes selon la taille du dépôt ; les données sont mises en cache (`~/.social-graph/cache.db`), ce qui rend les exécutions suivantes quasi instantanées.

Un token GitHub est nécessaire (`gh auth token` ou variable `GITHUB_TOKEN`). Une clé `ANTHROPIC_API_KEY` est optionnelle pour obtenir des libellés d'équipe générés par IA plutôt que par défaut sur les noms de répertoires.

Le pipeline peut être scindé en deux étapes : `social-graph build` pour la récupération et le calcul, puis `social-graph viz` pour le rendu à partir des données en cache, sans nouvel appel API.

### Appel à contribution
Unblocked invite la communauté à cloner l'outil, à le tester sur son propre dépôt, et à ouvrir des issues ou des PR sur le projet pour l'améliorer.

## Pourquoi ça compte
Ce projet illustre une tendance à utiliser les méta-données de collaboration (PR, revues, commits) comme signal de confiance pour des agents IA chargés d'arbitrer entre sources documentaires contradictoires, un sujet clé pour qui s'intéresse aux architectures de « context engine » pour l'IA en entreprise. C'est aussi un outil concret et immédiatement actionnable pour les équipes d'ingénierie souhaitant diagnostiquer leurs silos de connaissance et leur bus factor avant qu'un incident ne les révèle.
