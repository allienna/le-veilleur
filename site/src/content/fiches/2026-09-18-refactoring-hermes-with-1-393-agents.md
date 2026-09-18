---
title: "Refactoring Hermes with 1,393 agents"
date: 2026-09-18
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fnousresearch.com%2Frefactoring-hermes-with-1393-agents%3Futm_source=tldrdev/1/010001a0af146874-dc9a6ee3-a5dc-4222-8676-ccbdd199480a-000000/3h-TH5wWtHj1o4KIDGP8I_vjZACerPvUw9hCW5PHt4w=452"
keywords: ["agents IA", "refactoring", "orchestration multi-agents", "Nous Research", "Hermes", "dette technique"]
theme: "IA"
tone: "research"
used_in: ["2026-09-18"]
---

## Résumé
Nous Research a chargé son agent Hermes d'orchestrer 1 393 sous-agents pour refactoriser en profondeur la base de code Python de Hermes Agent, un chantier repoussé de longue date faute de temps disponible. En environ 19 heures de calcul actif, réparties sur 218 agents simultanés au pic, le projet a réduit le code Python hors tests de 34,4 % (1 063 826 → 698 363 lignes), pour un coût estimé de 19 300 à 25 000 dollars en tokens — contre une estimation manuelle de 150 000 à 1,8 million de dollars pour une petite équipe travaillant de deux mois à deux ans. L'opération s'est appuyée sur une architecture orchestrateur/workers utilisant des git worktrees isolés, des vérifications d'interfaces strictes (schémas JSON, sorties CLI identiques), et sur des « skills » que Hermes avait accumulées et affinées au fil des sessions de travail quotidiennes avec son opérateur. L'article documente aussi les limites de l'exercice : régressions détectées en revue, incident d'infrastructure en cours de run, et mesures chiffrées de l'impact du refactoring sur la capacité des agents (et non seulement des humains) à naviguer dans le code.

## Points clés
- Échelle de l'opération : 1 393 sous-agents dispatchés, jusqu'à 218 en parallèle, run principal de ~19h, fusion de la PR le 4 septembre après deux tours de revue communautaire.
- Gains mesurés : -34,4 % de lignes de code Python hors tests ; le fichier `gateway/run.py` passe de 34 847 à 5 512 lignes ; les fonctions de plus de 300 lignes passent de 192 à seulement 2 ; la plus longue chaîne `if/elif` passe de 92 à 9 branches.
- Coût dérisoire comparé au travail humain : environ 19 000-25 000 $ de tokens contre une fourchette estimée de 150 000 $ à 1,8 M$ pour réaliser le même travail manuellement.
- Méthode d'orchestration : découpage du dépôt en 36 groupes non chevauchants, workers isolés via git worktrees, consignes écrites automatiquement à partir des standards appris par l'agent, vérifications d'interfaces avant chaque commit, et récupération après une panne d'authentification qui a interrompu le run à mi-parcours.
- Amélioration continue outillée : la « skill » interne `hermes-agent-dev`, enrichie automatiquement à chaque correction ou leçon apprise, a été redistribuée à toute l'équipe d'ingénieurs pour que leurs propres agents en bénéficient sans repasser par les mêmes sessions.
- Limites et effets de bord : des régressions réelles ont été repérées en revue (suppression de noms publics utilisés par des plugins externes, changement de comportement de `suppress()` sur une soixantaine de sites), l'import de certains modules a ralenti, et six fichiers dépassaient encore 5 000 lignes après coup.

## Analyse approfondie

### Le point de départ
Le dépôt de Hermes, l'agent open-source de Nous Research, avait dépassé le million de lignes de Python hors tests, avec des fichiers monstres comme `gateway/run.py` (près de 35 000 lignes). Le nettoyage était repoussé depuis longtemps car il aurait mobilisé des ingénieurs au détriment des fonctionnalités et des correctifs. Début septembre, l'auteur a confié cette tâche à son agent Hermes habituel plutôt qu'à des humains. Le run principal a duré environ 19 heures actives et déployé 1 393 sous-agents (218 en simultané au maximum) ; après un redémarrage, une session de continuation et deux tours de revue communautaire, la PR a été fusionnée le 4 septembre, réduisant le code source Python hors tests de 34,4 %. Le coût du run principal est estimé à environ 19 300 $, et à environ 25 000 $ en comptant les sessions de suivi (hors temps humain de revue) — à comparer à une estimation de 150 000 $ à 1,8 million de dollars pour une petite équipe humaine travaillant de deux mois à deux ans sur le même chantier, un budget que l'équipe ne pouvait de toute façon pas dégager.

### Une auto-amélioration continue, pas un coup ponctuel
L'agent utilise au quotidien une « skill » nommée `hermes-agent-dev`, construite progressivement : chaque fois qu'une procédure est mise au point ou qu'une erreur est corrigée en session, Hermes enregistre automatiquement la leçon réutilisable sous forme de documents Markdown, avec fichiers de référence et scripts si besoin. Au fil du temps, cette skill a accumulé des consignes sur la préparation des PR, les raccourcis à éviter, et la manière de vérifier un changement — par exemple la règle consistant à reproduire un échec sur la HEAD de `origin/main` en environnement propre pour savoir s'il est préexistant. C'est exactement cette logique de comparaison à une base de référence figée que l'agent a réutilisée pendant le refactoring pour valider les changements des workers. Cette skill est partagée avec toute l'équipe d'ingénierie, qui peut l'installer dans ses propres instances de Hermes et bénéficier des procédures et corrections développées par l'auteur sans avoir à refaire le travail — chaque agent pouvant ensuite continuer à faire évoluer la skill à son tour.

Pour lancer le chantier, l'auteur a formulé un objectif explicite et ambitieux — une simplification massive avec au minimum 30 % de réduction du nombre de lignes, la décomposition des fichiers monolithiques, l'unification des fonctions redondantes, la réduction des chaînes de conditions imbriquées, une meilleure lisibilité et interprétabilité du code, sans attendre de validations intermédiaires — via la commande `/goal`, qui fixe un objectif permanent et pousse l'agent à continuer de lui-même plutôt que de s'arrêter.

### Le déroulement du refactoring
L'orchestrateur a commencé par mesurer la base de code et la répartir en 36 groupes non chevauchants, préparant les consignes écrites pour chaque worker à partir de l'objectif fixé et des standards accumulés, sans que l'auteur n'ait besoin de briefer chaque agent individuellement. Les workers travaillaient dans des git worktrees séparés — des copies de travail indépendantes évitant qu'ils n'écrasent mutuellement leurs modifications. Leurs consignes précisaient le code à simplifier, les interfaces à préserver, et les vérifications à effectuer avant tout commit.

Certains workers ont eux-mêmes délégué une partie de leur tâche, l'arborescence de délégation atteignant trois niveaux sous l'agent d'origine, celui-ci se consacrant uniquement à la coordination (rédaction des consignes et scripts, lecture des rapports, intégration des branches, exécution des vérifications) plutôt qu'à l'édition directe du code source. L'ensemble tournait dans un unique processus Python sur un poste de bureau équipé d'un i7 et de 64 Go de RAM, les outils s'exécutant en sous-processus locaux tandis que l'inférence était assurée à distance par Claude Fable 5.1.

La vérification portait sur des interfaces précises : le schéma JSON d'un outil devait rester identique, la sortie `--help` d'une commande CLI pouvait être comparée octet par octet, et les workers devaient committer après chaque étape validée. Environ cinquante minutes après le début du run, l'expiration du jeton d'authentification du fournisseur a provoqué une cascade d'échecs qui a interrompu l'exécution — mais les commits et les consignes des workers ont survécu. L'auteur a utilisé une session Hermes distincte pour diagnostiquer la panne et préparer une passation, réinjectée ensuite dans la session reprise : Hermes a alors renvoyé les workers inspecter leurs modifications sauvegardées, réparer les extractions inachevées, puis poursuivre.

Sur `gateway/run.py`, le plus gros fichier du dépôt, les workers ont séparé la répartition des messages, le streaming, les appels RPC et la gestion du cycle de vie en modules distincts. Ailleurs, ils ont fusionné des fonctions utilitaires dupliquées et remplacé de longues chaînes `if/elif` fondées sur des noms par des tables de dispatch.

Les relecteurs ont repéré des noms publics supprimés par les workers parce qu'ils n'avaient aucun appelant à l'intérieur du dépôt, alors même que des plugins externes pouvaient les importer. Une réécriture automatisée des appels à `suppress()` a également modifié la gestion des exceptions sur environ 65 emplacements. Il s'agissait de véritables régressions que les tests existants n'avaient pas détectées ; elles ont été corrigées avant la fusion, au terme de deux tours de revue communautaire, avec des correctifs supplémentaires après la fusion.

### Le code est-il vraiment devenu plus facile à manipuler ?
Les mesures avant/après de la PR montrent l'ampleur du changement :

| Métrique | Avant | Après |
|---|---|---|
| Lignes Python hors tests (tous répertoires) | 1 063 826 | 698 363 |
| Fichiers de plus de 5 000 lignes | 37 | 6 |
| Fonctions de plus de 300 lignes | 192 | 2 |
| Plus longue chaîne `if/elif` | 92 branches | 9 |
| `gateway/run.py` | 34 847 lignes | 5 512 lignes |

La question posée ensuite est de savoir si un code plus facile à parcourir pour un humain l'est aussi pour un agent : découper une fonction raccourcit sa définition mais peut obliger l'agent à suivre des appels dans d'autres fichiers. Pour tester cela, l'équipe a simulé la recherche des mêmes 4 000 symboles dans les deux versions du code, chaque recherche localisant la définition, lisant une fenêtre de 60 lignes, puis élargissant à des fenêtres de 2 000 lignes uniquement si la définition dépassait ce cadre.

Le nombre moyen de tokens retournés par recherche est passé de 2 218 à 993, et le nombre de recherches nécessitant une fenêtre de lecture supplémentaire est passé de 628 à 184. Plusieurs fonctions qui nécessitaient auparavant la lecture de dizaines de milliers de tokens tiennent désormais en quelques milliers. Il s'agit toutefois de coûts de recherche, pas d'une mesure de la capacité des agents à réaliser des tâches d'ingénierie complètes : la valeur médiane des tokens retournés par recherche a en réalité augmenté, car avec moins de commentaires et de docstrings, une fenêtre de lignes fixe contient un code plus dense — c'est la disparition des très grandes définitions qui explique la baisse de la moyenne.

D'autres coûts sont apparus : la multiplication des fichiers a augmenté le nombre de modules et de dépendances d'import, ralentissant l'import de certains points d'entrée. Le refactoring a rendu chaque élément plus lisible individuellement sans pour autant résoudre tout le couplage entre eux, et six fichiers dépassaient encore 5 000 lignes à l'issue du chantier. Les données du benchmark, incluant les résultats de recherche ainsi que les mesures de dépendances et de performance à l'exécution, ont été mises à disposition.

### Les leçons tirées
Faire tourner des centaines de workers a mis en lumière des axes d'amélioration pour Hermes lui-même. Par exemple, les workers dans leurs worktrees séparés avaient chacun démarré leur propre instance de Pyright, le serveur de langage Python, soit une trentaine de copies consommant environ 8,7 Go de mémoire ; un correctif ultérieur a permis aux worktrees de partager un seul serveur, avec une vérification en continu que les diagnostics remontaient bien pour chacun d'eux. L'équipe a également réduit la duplication des transports HTTP et corrigé des références qui maintenaient en mémoire des agents pourtant terminés.

Les consignes et vérifications données aux futurs workers ont été révisées : le dépôt dispose désormais de règles sur la taille des fichiers, la complexité des fonctions et l'emplacement du nouveau code, organisées par zone afin que chaque worker ne reçoive que les règles pertinentes à sa tâche. Une vérification a aussi été ajoutée pour signaler la suppression de noms publics et de tests lors des revues.

Les skills Hermes de l'auteur ont été automatiquement mises à jour avec les enseignements de ce refactoring, partageables avec toute l'équipe — le tout pour environ 1 % du coût et 1 % du temps estimés pour une réalisation manuelle. L'auteur y voit une illustration de ce qui fait de Hermes un multiplicateur de force pour les équipes : traiter un problème avec l'agent, le laisser consigner ce qui a été appris, et rendre cette expérience disponible pour la tâche suivante et pour le prochain ingénieur qui l'utilisera.

## Pourquoi ça compte
Ce cas documente, chiffres à l'appui, le passage des agents IA d'un usage ponctuel (une tâche, un prompt) à une orchestration à grande échelle capable d'absorber une dette technique massive à un coût dérisoire — tout en montrant, via les régressions détectées en revue, que la supervision humaine reste indispensable pour valider ce type d'opération autonome à fort volume.
