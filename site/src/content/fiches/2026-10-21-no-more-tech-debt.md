---
title: "No more tech debt"
date: 2026-10-21
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fswizec.com%2Fblog%2Fno-more-tech-debt%3Futm_source=tldrdev/1/010001a1590528e5-7bd99b87-b914-4994-a1b4-a75f54780554-000000/Up9tfxYPJgLGeA-zSBPhPFAhIeRf3OjFPEDAz7CGWFA=452"
authors: ["Swizec"]
keywords: ["dette technique", "migration de design system", "agents IA", "refactorisation", "Tailwind/ShadCN", "sentiers de désir"]
theme: "Leadership"
tone: "opinion"
used_in: ["2026-10-21"]
---

## Résumé
L'auteur (Swizec) raconte comment son équipe a, pour la première fois, mené à son terme une migration complète de design system, en partant d'un mélange hétérogène de Bootstrap, CSS fait main, styles générés par IA et composants React partiellement alignés sur la charte. La clé du succès a été de traiter la réécriture comme un investissement stratégique : poser d'abord des fondations propres (Tailwind, ShadCN/BaseUI, linters, documentation), laisser le système « mûrir » pendant un mois, puis lancer une migration massive accélérée par des agents IA (Claude) travaillant en longues sessions autonomes. Résultat concret : le nombre de fichiers important l'ancienne librairie JoyUI est passé de 592 à 146 en une semaine, via 45 pull requests sur 8 stacks techniques différentes. L'article conclut que les agents IA amplifient les patterns existants dans une base de code plutôt que de raisonner depuis les premiers principes, ce qui impose de ne laisser aucune trace de l'ancien système pour que les futurs agents (et développeurs) reproduisent uniquement les bons patterns.

## Points clés
- Une migration de code est par nature stratégique : elle ne crée pas de valeur directe, mais débloque des capacités futures.
- Les incohérences d'un design system ne sont pas une faute des développeurs produit mais le signe que les bons outils/composants manquaient (« sentiers de désir / desire paths »).
- La méthode gagnante : poser une base minimale et des garde-fous (Tailwind, ShadCN/BaseUI, fichier `DESIGN.md`, linters) avant de migrer en masse.
- Après la bascule initiale, laisser le système se stabiliser pendant plusieurs semaines (corrections, enrichissement de la librairie, ajustement des instructions) avant d'industrialiser.
- Les agents IA (Claude) ont permis une migration massive et rapide (592 → 146 fichiers en une semaine, 45 PR sur 8 stacks) en travaillant par petites tranches verticales, page par page, validées par des captures d'écran avant/après.
- Les agents amplifient les patterns déjà présents dans le code plutôt que d'en inventer de meilleurs ; il faut donc supprimer intégralement l'ancien système pour qu'ils ne reproduisent que les bonnes pratiques.

## Analyse approfondie
L'auteur ouvre son billet sur un constat rare dans sa carrière : la conclusion effective d'une migration de design system. Il formule une loi générale de la vie à grande échelle : une organisation est toujours en plein migration, en pleine réécriture, en plein constat que « ce code est franchement mauvais ». L'entreprise évolue en quelques mois et les systèmes construits deux ans plus tôt ne sont plus adaptés. La manière de gérer ces transitions fait toute la différence.

Il rappelle qu'une réécriture de code est toujours un choix stratégique : elle n'apporte presque aucune valeur immédiate, mais l'espoir est qu'elle débloque des capacités ultérieures. Dans son cas, la migration du design system a permis :
- d'unifier les styles entre différentes stacks techniques (React, HTMX, Jinja classique) ;
- de se débarrasser d'une librairie de composants désormais non maintenue (JoyUI) ;
- de construire une librairie de composants riche permettant à chacun de produire une interface soignée ;
- de nettoyer les anciennes erreurs accumulées ;
- d'appliquer de façon cohérente les leçons apprises ;
- d'adopter des technologies que les modèles de langage (LLM) maîtrisent mieux.

JoyUI reposait sur une approche CSS-in-JS compilée en CSS pur. L'équipe appréciait son ergonomie en React, mais l'outil restait malcommode dans les pages Jinja/HTMX plus traditionnelles — si bien qu'il n'y a jamais été réellement adopté là-bas.

Avec le temps, la base de code s'est transformée en un patchwork de Bootstrap, de CSS écrit à la main, de styles générés par IA (« AI vibed »), et de pages React suivant plus ou moins la charte. Il manquait constamment des composants de base solides, et personne n'avait le temps de les construire — si bien que même les interfaces censées suivre le design system paraissaient maladroites et incohérentes.

L'auteur insiste : les ingénieurs produit sont évalués sur les fonctionnalités livrées et la satisfaction client. Ils font de leur mieux pour respecter les conventions établies et garder un code propre, mais on ne peut pas attendre d'eux qu'ils fassent de grands détours pour « bien faire les choses » à tout prix. Si les raccourcis pris par les équipes (les « sentiers de désir ») dégradent la qualité du code, c'est la responsabilité de ceux qui conçoivent le système : un système se dégrade dès que le coût de le maintenir propre devient trop élevé.

Chaque composant bizarre, chaque page mal stylée, chaque convention appliquée de façon inégale est en réalité un signal : les outils adéquats n'étaient pas disponibles. Les ingénieurs ne pouvaient pas piocher des composants prêts à l'emploi, ne trouvaient pas les bonnes conventions à suivre, et devaient donc repartir des premiers principes au lieu de se concentrer sur leurs fonctionnalités. Résultat : chaque page et chaque composant semblait avoir été conçu par une personne différente — ce qui était littéralement le cas.

L'équipe a démarré par des étapes prudentes :
1. Une surcouche Tailwind personnalisée reprenant les couleurs de la marque ;
2. Une librairie de composants minimale basée sur ShadCN + BaseUI ;
3. Une configuration de base garantissant que les anciens et nouveaux composants puissent coexister sur une même page sans paraître affreux — un peu de maladresse est tolérable, l'horreur ne l'est pas ;
4. Un fichier `DESIGN.md` décrivant le chemin de migration ;
5. Quelques linters de base pour forcer l'usage du design system plutôt que des styles créés à partir de zéro.

L'équipe a ensuite lancé une migration « big bang », réécrivant en une seule grosse pull request l'ensemble des styles Jinja et HTMX. Cette PR a été fusionnée, suivie de deux jours de correction de petits bugs. Pour chaque bug corrigé, l'équipe évaluait si quelque chose manquait dans le design system ou dans la documentation, et mettait à jour en conséquence.

Le système a ensuite été laissé « mûrir ». Pendant environ un mois, les équipes ont enrichi la librairie de composants, corrigé des incohérences, affiné les instructions lorsque les agents IA faisaient des erreurs, mis à jour les linters pour détecter les problèmes courants, et continué à réécrire l'interface page par page.

Une fois que la requête type « Hey agent, réécris cette page en ShadCN, suis le nouveau design system, conserve toutes les fonctionnalités, et ajoute des captures d'écran avant/après dans la pull request » a commencé à produire des résultats régulièrement bons, l'équipe a de nouveau accéléré fortement.

À un moment, l'auteur a laissé Claude travailler en autonomie pendant six ou sept heures pour migrer plusieurs sections majeures du site. C'est cette période qui explique la **chute du nombre de fichiers important `@mui/joy`, de 592 à 146 en une semaine** mentionnée (et illustrée par une capture d'écran dans l'article d'origine). Au total, 45 pull requests ont été produites sur 8 stacks techniques différentes — une expérience que l'auteur qualifie de « glorieuse ». L'astuce consistait à demander systématiquement des captures d'écran avant/après pour permettre une comparaison visuelle, et à demander à Claude de migrer par « tranches verticales » : chaque pull request migrait une seule page et pouvait être fusionnée sans perturber le reste de l'équipe.

Il a ensuite fallu une semaine supplémentaire pour nettoyer les derniers fichiers récalcitrants, en traitant d'abord les cas à fort impact, puis en traquant les cas isolés restants.

L'objectif affiché était de « ne laisser aucune trace de l'ancien design system ». Cela peut sembler excessif, mais l'auteur le juge crucial dès lors que tout le monde utilise des agents IA pour écrire du code : les agents amplifient la base de code existante. Ils ne raisonnent pas depuis les premiers principes et appliquent mal de meilleurs patterns sans un encadrement humain important — en revanche, ils excellent dans des tâches du type « construis cette fonctionnalité en suivant les patterns de cette autre fonctionnalité existante ». Il faut donc s'assurer que tout est propre : supprimer l'ancien code, migrer l'intégralité du système. Ainsi, n'importe quel ingénieur peut construire une nouvelle fonctionnalité de qualité sans se soucier de savoir ce que cela implique techniquement — les agents, eux, « font juste bien les choses ».

L'article se termine sur la signature « ~Swizec », classé sous les catégories « Software Engineering » et « Teamwork ».

## Pourquoi ça compte
Ce témoignage illustre une tendance émergente en veille tech : les agents IA (type Claude) permettent désormais de mener à bien, en quelques semaines, des migrations de grande ampleur (design systems, dette technique) jugées auparavant interminables, à condition de poser d'abord des garde-fous clairs (conventions, linters, documentation) — un changement de paradigme pour la gestion de la dette technique en ingénierie logicielle.
