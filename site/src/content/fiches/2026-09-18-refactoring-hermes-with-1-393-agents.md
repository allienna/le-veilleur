---
title: "Refactoring Hermes with 1,393 agents"
date: 2026-09-18
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fnousresearch.com%2Frefactoring-hermes-with-1393-agents%3Futm_source=tldrdev/1/010001a0af146874-dc9a6ee3-a5dc-4222-8676-ccbdd199480a-000000/3h-TH5wWtHj1o4KIDGP8I_vjZACerPvUw9hCW5PHt4w=452"
keywords: ["agents autonomes", "orchestration multi-agents", "refactoring", "Claude", "ingénierie logicielle", "Hermes"]
theme: "IA"
tone: "research"
used_in: ["2026-09-18"]
---

## Résumé
Nous Research a utilisé son agent autonome Hermes pour refactoriser plus d'un million de lignes de code Python en déployant 1 393 sous-agents sur une exécution de dix-neuf heures actives. Le résultat : une réduction de 34,4 % du code source hors tests, des fichiers géants découpés et une complexité cyclomatique fortement réduite, pour un coût d'environ 19 000 à 25 000 $, contre une estimation manuelle de 150 000 $ à 1,8 M$. L'agent s'appuie sur un système de compétences (« skills ») auto-améliorantes qui capitalisent au fil du temps les procédures et corrections apprises auprès de l'ingénieur. Des régressions réelles (suppression d'API publiques utilisées par des plugins externes, modification de la gestion des exceptions) ont toutefois été détectées lors de la revue humaine avant la fusion.

## Points clés
- Refactoring massif : 1 393 sous-agents (218 simultanés), 19 heures actives, réduction du code Python hors tests de 34,4 % (1 063 826 → 698 363 lignes).
- Coût : environ 19 000-25 000 $ en tokens, contre une estimation de 150 000 $ à 1,8 M$ pour un travail manuel équivalent.
- Architecture : un orchestrateur découpe la base de code en 36 groupes non chevauchants, les workers travaillent dans des git worktrees isolés, avec jusqu'à trois niveaux de sous-délégation.
- Système de compétences auto-apprenant (`hermes-agent-dev`) qui capitalise les corrections et procédures de l'ingénieur et se partage entre équipes.
- Gains mesurés pour la navigabilité du code par un agent : tokens moyens par recherche de symbole divisés par plus de deux (2 218 → 993).
- Limites observées : régressions réelles détectées en revue (API publiques supprimées mais utilisées par des plugins externes, changement de gestion des exceptions sur 65 sites), couplage inter-fichiers non résolu, six fichiers encore supérieurs à 5 000 lignes.

## Analyse approfondie
# Refactoring Hermes avec 1 393 agents

Ou : comment tirer 1,8 M$ de valeur de 19 000 $ de tokens

*TLDR : L'agent Hermes a labouré de façon autonome environ un million de lignes de nettoyage ingrat, libérant Teknium et son équipe pour continuer à livrer des fonctionnalités aux utilisateurs.*

Nous avions longtemps repoussé un nettoyage en profondeur de Hermes, notre agent open source, car cela signifiait détourner des ingénieurs des fonctionnalités et des corrections de bugs. En septembre, le dépôt comptait plus d'un million de lignes de Python hors tests. `gateway/run.py` à lui seul faisait 34 847 lignes. Je voulais des fichiers plus petits, des helpers partagés et moins de fonctions énormes à parcourir quand quelque chose cassait.

Le 2 septembre, j'ai demandé à mon agent Hermes habituel de faire le nettoyage. L'exécution principale a duré environ dix-neuf heures actives et a déployé 1 393 sous-agents, atteignant 218 en cours d'exécution simultanée. Après un redémarrage, une session de continuation, et deux tours de revue communautaire et de corrections, j'ai fusionné la PR le 4 septembre. Cela a réduit le code source Python hors tests de 34,4 %.

Le coût estimé du modèle était d'environ 19 300 $ pour l'exécution principale, soit environ 25 000 $ en incluant les sessions de suivi. Cela exclut le temps de revue humaine. Notre estimation approximative des effectifs pour faire ce travail manuellement était de 150 000 $ à 1,8 M$ pour une petite équipe travaillant pendant deux mois à deux ans. Nous ne pouvions pas justifier de le programmer parmi tout ce que nous devions livrer par ailleurs.

J'utilise Hermes Agent tous les jours pour développer Hermes Agent. Au fil de nos corrections de bugs et revues de changements ensemble, Hermes enregistre ce qui a fonctionné et met à jour ses compétences (skills) quand je corrige son approche ou quand il trouve la bonne voie pour résoudre de nouveaux problèmes. Au moment où j'ai demandé ce refactoring, il avait appris mes procédures et standards préférés et pouvait les appliquer à un travail bien plus vaste :

*Je veux un ensemble massif de PR de simplification. Ou une seule PR monolithique. Je veux que le nombre de lignes de code chute drastiquement. Minimum 30 % au global. Je veux que les fichiers géants soient découpés. Je veux une simplification sur tous les fronts. Je veux l'unification des helpers et méthodes réutilisables. Je veux moins de routage en if-if-if-if-if-else. Je veux plus de lisibilité du code. Je veux plus d'interprétabilité de la base de code et de la façon dont les éléments s'articulent entre eux. Je veux de l'élégance. Je veux que le code superflu et boursouflé soit nettoyé et supprimé. Je veux que tout soit fait entièrement. Pas d'excuses. Pas d'attente de mes décisions. Faites tout, et présentez-moi une PR ou un ensemble de PR une fois terminé.*

J'ai utilisé `/goal`, qui donne à Hermes un objectif permanent et l'incite à continuer alors qu'il se serait autrement arrêté.

## Auto-amélioration (pour de vrai)

Ma compétence `hermes-agent-dev` est née de mon travail quotidien sur le dépôt. Quand nous mettions au point une procédure ou que je corrigeais une erreur, Hermes le remarquait (automatiquement) et enregistrait la leçon réutilisable. Au fil du temps, il a accumulé des instructions sur la façon de préparer une PR, les raccourcis à éviter, et comment vérifier un changement. Les compétences (skills) sont des documents Markdown lisibles, avec des fichiers de référence et des scripts si nécessaire, que l'agent peut charger pour des tâches ultérieures. Hermes les écrit et les révise au fur et à mesure de son travail.

La version actuelle de `hermes-agent-dev` inclut cette instruction pour un test qui échoue :

*reproduire sur `origin/main` HEAD dans un environnement propre pour vérifier si c'est préexistant*

Autrement dit, exécuter le test qui échoue sur le code inchangé pour aider à déterminer si votre changement en est la cause. Hermes a utilisé le même type de comparaison durant le refactoring : il a établi une base de référence figée et a vérifié les échecs par rapport à celle-ci au fur et à mesure qu'il intégrait les changements des workers.

J'envoie cette compétence à tous nos ingénieurs. Ils peuvent l'installer dans leurs propres configurations Hermes, afin que leurs agents puissent utiliser les procédures et corrections développées dans mes sessions. Ils bénéficient de ce travail sans avoir à répéter les sessions eux-mêmes, et leurs agents peuvent adapter la compétence au fur et à mesure de leur utilisation.

## Exécuter le refactoring

L'orchestrateur a mesuré la base de code et l'a divisée en 36 groupes non chevauchants. Il a utilisé mon objectif et les directives accumulées pour préparer des consignes écrites, sans que j'aie à briefer chaque worker.

Les workers utilisaient des git worktrees, des copies de travail séparées où ils pouvaient effectuer des modifications sans écraser les fichiers des autres. Leurs consignes identifiaient le code à simplifier, les interfaces à préserver, et les vérifications requises avant de committer.

Certains workers ont eux-mêmes délégué des parties de leurs tâches. L'arborescence a atteint trois niveaux sous l'agent d'origine, lequel s'occupait de la coordination plutôt que de l'édition des fichiers source : il rédigeait les consignes et scripts, lisait les rapports des workers, intégrait les branches, et exécutait les vérifications.

Hermes a coordonné les agents dans un seul processus Python sur un poste de bureau i7 avec 64 Go de RAM. Leurs outils s'exécutaient dans des sous-processus locaux, tandis que Claude Fable 5.1 gérait l'inférence à distance.

L'agent vérifiait des interfaces spécifiques par rapport au code d'origine. Le schéma JSON d'un outil devait par exemple rester identique, et la sortie `--help` d'une commande CLI pouvait être comparée octet par octet. Les workers devaient aussi committer après chaque étape vérifiée.

Environ cinquante minutes après le début, le jeton d'authentification du fournisseur a expiré et les échecs qui en ont résulté ont tué l'exécution. Les commits et consignes des workers ont survécu. J'ai utilisé une session Hermes séparée pour diagnostiquer la panne et préparer une passation, que j'ai ensuite fournie à la session reprise. Hermes a renvoyé les workers inspecter leurs changements sauvegardés, réparer les extractions inachevées, et continuer.

Pour `gateway/run.py`, notre plus gros fichier, les workers ont séparé la répartition des messages (dispatch), le streaming, le RPC et la gestion du cycle de vie en modules distincts. Ailleurs, ils ont consolidé des helpers dupliqués et remplacé de longues chaînes `if/elif` basées sur des noms par des tables de dispatch.

Les relecteurs ont repéré des noms publics que les workers avaient supprimés parce qu'ils n'avaient aucun appelant à l'intérieur du dépôt, alors même que des plugins externes pouvaient les importer. Une réécriture automatisée des appels à `suppress()` a également modifié la gestion des exceptions sur environ 65 sites. Il s'agissait de véritables régressions que les tests existants n'avaient pas détectées. Nous les avons corrigées avant la fusion, au terme de deux tours de revue communautaire. D'autres corrections ont suivi après la fusion.

## Le code était-il plus facile à travailler ?

Les mesures avant/après de la PR ont montré à quel point le code avait changé :

| Métrique | Avant | Après |
|---|---|---|
| Lignes Python hors tests (tous répertoires) | 1 063 826 | 698 363 |
| Fichiers de plus de 5 000 lignes | 37 | 6 |
| Fonctions de plus de 300 lignes | 192 | 2 |
| Plus longue chaîne `if/elif` | 92 branches | 9 |
| `gateway/run.py` | 34 847 lignes | 5 512 |

Un code plus facile à parcourir pour les humains fonctionne-t-il aussi mieux pour les agents ? Diviser une fonction raccourcit sa définition, mais peut obliger l'agent à suivre les appels vers d'autres fichiers. Nous avons testé une partie de cette question en simulant des recherches des 4 000 mêmes symboles dans les deux versions. Chaque recherche cherchait la définition, lisait une fenêtre de 60 lignes, et ne se poursuivait dans des fenêtres de 2 000 lignes que si la définition dépassait cette taille.

Le nombre moyen de tokens renvoyés par recherche est passé de 2 218 à 993. Les recherches nécessitant une fenêtre de lecture supplémentaire sont passées de 628 à 184. Plusieurs fonctions qui nécessitaient auparavant de lire des dizaines de milliers de tokens pouvaient désormais être lues en quelques milliers.

Il s'agit là de coûts de recherche ; nous n'avons pas mesuré des agents accomplissant des tâches d'ingénierie complètes. La recherche médiane renvoyait en fait davantage de tokens : avec moins de commentaires et de docstrings, une fenêtre de lignes fixe contenait un code plus dense. La moyenne a baissé parce que les très grandes définitions sont devenues bien plus petites.

Il y avait d'autres coûts. Diviser les fichiers a augmenté le nombre de modules et les dépendances d'import, et certains points d'entrée mettaient plus de temps à s'importer. Le refactoring a rendu les éléments individuels plus faciles à lire sans résoudre tout le couplage qui existait entre eux. Six fichiers dépassaient encore 5 000 lignes.

Les données du benchmark incluent les résultats des recherches ainsi que les mesures de dépendances et d'exécution.

## Leçons apprises

Faire fonctionner des centaines de workers a révélé des opportunités d'amélioration pour Hermes lui-même. Par exemple, les workers dans des worktrees séparés avaient démarré environ trente copies de Pyright, un serveur de langage Python, consommant environ 8,7 Go. Un changement ultérieur a permis aux worktrees de partager un seul serveur, avec une vérification en direct que les diagnostics arrivaient bien de chacun d'eux. Nous avons aussi réduit la duplication des transports HTTP et corrigé des références qui gardaient en mémoire des agents pourtant terminés.

Nous avons modifié les instructions et vérifications que recevront les futurs workers. Le dépôt dispose désormais de directives sur la taille des fichiers, la complexité des fonctions, et l'endroit où doit aller le nouveau comportement, réparties par zone afin que les workers reçoivent les règles pertinentes au moment voulu. Nous avons aussi ajouté une vérification qui signale les noms publics supprimés et les tests à examiner.

Mes compétences Hermes ont été automatiquement mises à jour avec les leçons de ce refactoring, que je peux partager avec l'équipe. Le tout pour 1 % du coût et 1 % du temps que nous avions estimé nécessaires si nous avions tenté ce travail manuellement.

C'est un excellent exemple de la façon dont Hermes est un superpouvoir pour les équipes : travailler un problème avec Hermes, le laisser enregistrer ce qu'on a appris, et rendre cette expérience disponible pour la tâche suivante et le prochain ingénieur. La prochaine fois que nous nous attaquerons à un refactoring, mon Hermes et les ingénieurs utilisant la compétence mise à jour pourront repartir des leçons de celui-ci.

## Pourquoi ça compte
Ce cas illustre concrètement le passage à l'échelle de l'orchestration multi-agents autonome appliquée à une tâche d'ingénierie réelle, avec un ROI économique chiffré, tout en montrant que la supervision humaine reste indispensable pour détecter les régressions silencieuses que ces systèmes peuvent introduire.
