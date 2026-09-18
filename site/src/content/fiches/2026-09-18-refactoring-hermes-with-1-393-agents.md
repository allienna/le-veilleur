---
title: "Refactoring Hermes with 1,393 agents"
date: 2026-09-18
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fnousresearch.com%2Frefactoring-hermes-with-1393-agents%3Futm_source=tldrdev/1/010001a0af146874-dc9a6ee3-a5dc-4222-8676-ccbdd199480a-000000/3h-TH5wWtHj1o4KIDGP8I_vjZACerPvUw9hCW5PHt4w=452"
keywords: ["agents IA", "refactoring", "Hermes", "Nous Research", "orchestration multi-agents", "dette technique"]
theme: "IA"
tone: "research"
used_in: ["2026-09-18"]
---

## Résumé
Nous Research raconte comment son agent open source Hermes a mené seul un refactoring massif d'une base de code Python de plus d'un million de lignes, en orchestrant 1 393 sous-agents sur environ dix-neuf heures actives de travail. L'opération a réduit le code source non-test de 34,4 %, pour un coût estimé à environ 19 300 $ (25 000 $ en comptant les sessions de suivi), contre une estimation de 150 000 $ à 1,8 million de dollars pour une équipe humaine sur une durée de deux mois à deux ans. L'agent s'appuie sur des compétences (« skills ») qu'il a lui-même accumulées au fil des sessions de travail avec l'auteur, ce qui lui a permis d'appliquer les standards et procédures maison à une opération de grande ampleur. L'article détaille l'architecture d'orchestration, les incidents rencontrés (expiration d'un jeton d'authentification, régressions détectées en revue), et quantifie les gains via des mesures avant/après et un test de recherche de symboles simulé.

## Points clés
- 1 393 sous-agents, jusqu'à 218 en parallèle, ont fait passer le code Python non-test de 1 063 826 à 698 363 lignes (-34,4 %) en environ 19 heures actives, avec un merge le 4 septembre après deux tours de revue communautaire.
- Coût du run principal : environ 19 300 $ de tokens (~25 000 $ tout compris), contre une estimation manuelle de 150 000 $ à 1,8 million de dollars pour une petite équipe.
- L'agent s'appuie sur une compétence baptisée `hermes-agent-dev`, constituée automatiquement à partir des corrections et procédures apprises pendant le travail quotidien avec l'auteur, puis diffusée à toute l'équipe d'ingénieurs.
- L'orchestrateur a réparti le dépôt en 36 groupes non chevauchants, chaque worker opérant dans son propre git worktree, avec des chaînes de délégation pouvant atteindre trois niveaux.
- Un incident (expiration d'un jeton d'authentification après une cinquantaine de minutes) a interrompu le run principal, mais les commits et les instructions de travail avaient survécu, permettant une reprise après diagnostic dans une session séparée.
- La revue humaine a détecté de vraies régressions — suppression de noms publics utilisés par des plugins externes, changement de comportement sur environ 65 sites via une réécriture automatique des appels `suppress()` — corrigées avant et après le merge.

## Analyse approfondie
**Refactoriser Hermes avec 1 393 agents** — sous-titre : comment tirer 1,8 million de dollars de valeur de 19 000 $ de tokens.

En résumé, selon l'auteur : l'agent Hermes a traité de façon autonome environ un million de lignes de nettoyage ingrat, libérant Teknium et le reste de l'équipe pour continuer à livrer des fonctionnalités aux utilisateurs.

L'équipe repoussait depuis longtemps un grand nettoyage de Hermes, leur agent open source, car cela aurait mobilisé des ingénieurs au détriment des fonctionnalités et des correctifs. En septembre, le dépôt dépassait le million de lignes de Python hors tests ; le seul fichier `gateway/run.py` en comptait 34 847. L'auteur voulait des fichiers plus petits, des fonctions d'aide partagées et moins de fonctions démesurées à parcourir en cas de bug.

Le 2 septembre, l'auteur a demandé à son agent Hermes habituel de s'occuper de ce nettoyage. Le run principal a duré environ dix-neuf heures actives et a mobilisé 1 393 sous-agents, avec un pic de 218 en fonctionnement simultané. Après un redémarrage, une session de continuation et deux tours de revue et de correctifs communautaires, la pull request a été fusionnée le 4 septembre. Elle a réduit le code source Python hors tests de 34,4 %.

Le coût modèle estimé était d'environ 19 300 $ pour le run principal, soit environ 25 000 $ en comptant les sessions complémentaires — hors temps de revue humaine. L'estimation interne pour réaliser ce travail manuellement se situait entre 150 000 $ et 1,8 million de dollars, pour une petite équipe travaillant de deux mois à deux ans. Un chantier que l'équipe ne pouvait pas justifier de caser au milieu du reste du planning.

L'auteur utilise Hermes Agent au quotidien pour développer Hermes Agent lui-même. Au fil des corrections de bugs et des revues de changements effectuées ensemble, Hermes enregistre ce qui a fonctionné et met à jour ses compétences lorsque l'auteur corrige son approche ou qu'il trouve la bonne méthode pour résoudre de nouveaux problèmes. Au moment de demander ce refactoring, l'agent avait déjà intégré les procédures et standards préférés de l'auteur, et pouvait les appliquer à un chantier bien plus vaste. La consigne donnée était, en substance : produire un ensemble massif de PR de simplification (ou une PR monolithique unique), faire chuter drastiquement le nombre de lignes de code (au moins 30 % au global), découper les « fichiers-dieux », unifier les fonctions d'aide réutilisables, réduire les chaînes de conditions en cascade, améliorer la lisibilité et l'élégance du code, retirer le code superflu — le tout sans attendre de validations intermédiaires et sans excuse, jusqu'à livrer une ou plusieurs PR complètes.

L'auteur a utilisé la commande `/goal`, qui donne à Hermes un objectif permanent et l'incite à poursuivre le travail au lieu de s'arrêter en cours de route.

### L'auto-amélioration (pour de vrai)
La compétence `hermes-agent-dev` de l'auteur est née de son travail quotidien sur le dépôt. Chaque fois qu'une procédure était mise au point, ou qu'une erreur était corrigée, Hermes le remarquait automatiquement et enregistrait la leçon réutilisable. Au fil du temps, l'agent a ainsi accumulé des instructions sur la préparation d'une PR, les raccourcis à éviter, et la façon de vérifier un changement. Ces compétences sont des documents Markdown lisibles, accompagnés au besoin de fichiers de référence et de scripts, que l'agent peut charger pour des tâches ultérieures. Hermes les rédige et les révise lui-même au fil de son travail.

La version actuelle de `hermes-agent-dev` contient par exemple cette instruction en cas d'échec d'un test : reproduire l'échec sur la branche `origin/main` dans un environnement propre, afin de déterminer s'il est préexistant. Autrement dit, faire tourner le test en échec sur le code non modifié pour établir si le changement en est la cause. Hermes a appliqué le même type de comparaison pendant le refactoring : il a établi une base de référence figée et a confronté les échecs à cette base au fur et à mesure qu'il intégrait les changements des différents workers.

L'auteur diffuse cette compétence à tous les ingénieurs de l'équipe. Ils peuvent l'installer dans leurs propres instances de Hermes, afin que leurs agents bénéficient des procédures et corrections mises au point lors des sessions de l'auteur, sans avoir à refaire ce travail eux-mêmes — et leurs agents peuvent ensuite continuer à faire évoluer la compétence à leur propre usage.

### Le déroulement du refactoring
L'orchestrateur a mesuré la base de code et l'a divisée en 36 groupes sans chevauchement. Il s'est appuyé sur l'objectif fixé par l'auteur et sur les consignes accumulées pour préparer des instructions de travail écrites, sans que l'auteur ait besoin de briefer chaque worker individuellement.

Les workers ont utilisé des git worktrees — des copies de travail séparées leur permettant de modifier le code sans écraser les fichiers des autres. Leurs instructions précisaient le code à simplifier, les interfaces à préserver, et les vérifications requises avant tout commit.

Certains workers ont eux-mêmes délégué une partie de leur mission. L'arborescence de délégation a atteint trois niveaux sous l'agent d'origine, celui-ci se consacrant à la coordination plutôt qu'à l'édition directe du code source : il rédigeait les instructions et les scripts, lisait les rapports des workers, intégrait les branches et exécutait les vérifications.

Hermes a coordonné l'ensemble des agents dans un seul processus Python, sur un poste de bureau équipé d'un processeur i7 et de 64 Go de RAM. Les outils tournaient dans des sous-processus locaux, tandis que l'inférence était assurée à distance par Claude Fable 5.1.

L'agent vérifiait des interfaces précises par rapport au code d'origine : le schéma JSON d'un outil devait par exemple rester identique, et la sortie de la commande `--help` d'un CLI pouvait être comparée octet par octet. Les workers devaient également committer après chaque étape validée.

Après environ cinquante minutes, le jeton d'authentification du fournisseur a expiré, provoquant des échecs en cascade qui ont interrompu le run. Les commits et les instructions des workers avaient toutefois survécu. L'auteur a utilisé une session Hermes distincte pour diagnostiquer la panne et préparer une passation, avant de la transmettre à la session reprise. Hermes a alors renvoyé les workers inspecter leurs changements sauvegardés, réparer les extractions inachevées, et poursuivre le travail.

Sur `gateway/run.py`, le plus gros fichier du dépôt, les workers ont séparé la distribution des messages, le streaming, le RPC et la gestion du cycle de vie en modules distincts. Ailleurs, ils ont regroupé des fonctions d'aide dupliquées et remplacé de longues chaînes de conditions `if/elif` basées sur des noms par des tables de dispatch.

Les relecteurs ont repéré des noms publics supprimés par les workers parce qu'ils n'avaient plus d'appelant dans le dépôt, alors même que des plugins externes pouvaient les importer. Une réécriture automatisée des appels `suppress()` a également modifié la gestion des exceptions sur une soixantaine de sites. Il s'agissait de véritables régressions que les tests existants n'avaient pas détectées. Elles ont été corrigées avant la fusion, au terme de deux tours de revue communautaire, puis d'autres correctifs ont suivi après le merge.

### Le code est-il devenu plus facile à manier ?
Les mesures avant/après de la PR montrent l'ampleur du changement :

| Indicateur | Avant | Après |
|---|---|---|
| Lignes de Python hors tests (tous répertoires) | 1 063 826 | 698 363 |
| Fichiers de plus de 5 000 lignes | 37 | 6 |
| Fonctions de plus de 300 lignes | 192 | 2 |
| Chaîne `if/elif` la plus longue | 92 branches | 9 |
| `gateway/run.py` | 34 847 lignes | 5 512 lignes |

Un code plus facile à parcourir pour un humain l'est-il aussi pour un agent ? Découper une fonction raccourcit sa définition, mais peut obliger l'agent à suivre des appels dans d'autres fichiers. Ce point a été testé en simulant la recherche des mêmes 4 000 symboles dans les deux versions du code. Chaque recherche cherchait la définition, lisait une fenêtre de 60 lignes, puis ne poursuivait dans des fenêtres de 2 000 lignes que si la définition dépassait cette taille.

Le nombre moyen de tokens renvoyés par recherche est passé de 2 218 à 993. Les recherches nécessitant une fenêtre de lecture supplémentaire sont passées de 628 à 184. Plusieurs fonctions qui nécessitaient auparavant la lecture de dizaines de milliers de tokens pouvaient désormais être lues en quelques milliers de tokens seulement.

Ces chiffres ne mesurent que le coût de la recherche ; l'équipe n'a pas évalué la capacité des agents à mener à bien des tâches d'ingénierie complètes. La recherche médiane renvoyait en réalité davantage de tokens : avec moins de commentaires et de docstrings, une fenêtre de lignes fixe contenait un code plus dense. La moyenne a baissé parce que les très grandes définitions sont devenues beaucoup plus petites.

D'autres coûts sont apparus. Le découpage des fichiers a augmenté le nombre de modules et de dépendances d'import, et certains points d'entrée ont mis plus de temps à s'importer. Le refactoring a rendu les éléments individuels plus lisibles sans pour autant résoudre tout le couplage qui existait entre eux. Six fichiers dépassaient encore les 5 000 lignes.

### Enseignements tirés
Faire tourner des centaines de workers a révélé des pistes d'amélioration pour Hermes lui-même. Par exemple, des workers travaillant dans des worktrees séparés avaient chacun lancé leur propre instance de Pyright, un serveur de langage Python — soit une trentaine de copies consommant environ 8,7 Go de mémoire. Un correctif ultérieur a permis aux worktrees de partager un seul serveur, avec une vérification en direct que les diagnostics remontaient bien pour chacun d'eux. L'équipe a également réduit la duplication des transports HTTP et corrigé des références qui maintenaient en mémoire des agents pourtant terminés.

Les instructions et vérifications données aux futurs workers ont été révisées. Le dépôt dispose désormais de consignes sur la taille des fichiers, la complexité des fonctions, et l'emplacement approprié pour tout nouveau comportement, réparties par domaine afin que chaque worker reçoive les règles pertinentes au bon moment. Une vérification a aussi été ajoutée pour signaler en revue toute suppression de nom public ou de test.

Les compétences Hermes de l'auteur ont été automatiquement enrichies des leçons tirées de ce refactoring, prêtes à être partagées avec le reste de l'équipe — le tout pour 1 % du coût et 1 % du temps qui avaient été estimés pour une réalisation manuelle.

L'auteur conclut que cet épisode illustre bien la façon dont Hermes démultiplie les capacités d'une équipe : travailler un problème avec Hermes, le laisser enregistrer ce qui a été appris, et rendre cette expérience disponible pour la tâche suivante et le prochain ingénieur. Au prochain grand refactoring, l'auteur et les ingénieurs utilisant la compétence mise à jour pourront repartir directement des leçons tirées de celui-ci.

## Pourquoi ça compte
Ce cas illustre concrètement comment l'orchestration de centaines d'agents IA en parallèle peut abattre, à moindre coût, un chantier de dette technique qu'aucune équipe humaine ne priorise jamais — avec des méthodes de vérification reproductibles (bases de référence figées, comparaisons octet par octet) qui rendent la démarche crédible au-delà du simple effet d'annonce.
