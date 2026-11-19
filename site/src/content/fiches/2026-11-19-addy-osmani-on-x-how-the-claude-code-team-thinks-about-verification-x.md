---
title: "Addy Osmani on X: \"How the Claude Code team thinks about verification\" / X"
date: 2026-11-19
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Flinks.tldrnewsletter.com%2FK8O6Qc/1/010001a1ee96e867-c9c1cb9b-0168-4ef0-9d7e-fa9e6587e653-000000/oLnJbPBdEUCe3aC77wOT-2iVtY7vpE9075XUmp-47Cc=452"
authors: ["Addy Osmani"]
keywords: ["verification", "tests automatisés", "Claude Code", "revue de code", "CI/CD", "agents IA"]
theme: "Software"
tone: "tutorial"
used_in: ["2026-11-19"]
---

## Résumé
Cet article décrit comment l'équipe Claude Code chez Anthropic conçoit ses boucles de vérification pour pouvoir déléguer massivement l'écriture de code à des agents IA : environ 90 % du code de l'équipe est écrit et relu par Claude. La thèse centrale est que la vérification — et non la relecture humaine systématique — est le véritable levier qui permet de faire tourner des dizaines, voire des centaines d'agents en parallèle sans perte de qualité. L'article détaille trois familles de tests à privilégier (end-to-end, tests par propriétés, tests différentiels), puis expose les pratiques internes concrètes de l'équipe Claude Code : exécution réelle des changements, escalade humaine après échecs répétés, check-lists de fiabilité, gating des commits, et boucle d'amélioration continue des règles de revue à partir des incidents passés.

## Points clés
- Donner aux agents une capacité de vérification fiable est ce qui permet de faire passer le travail humain de « relire chaque diff » à « définir ce que signifie *terminé* et examiner les preuves ».
- Un grader séparé évaluant le travail de Claude selon une grille (rubric) améliore le taux de succès jusqu'à 10 points par rapport à un simple prompting, avec les gains les plus importants sur les tâches difficiles.
- Trois types de tests sont jugés les plus rentables : les tests end-to-end (difficiles à tromper), les tests par propriétés (pour débusquer les cas limites qu'on n'a pas anticipés) et les tests différentiels (l'ancien système sert d'oracle lors des migrations).
- Chez Claude Code, la vérification passe avant tout par l'exécution réelle de l'application (navigateur, simulateur mobile, computer use, service lancé localement), encapsulée dans une « skill » dédiée appelée *verify*.
- Une check-list de fiabilité de 39 points, déclenchée automatiquement selon le contenu du diff, remplace la mémorisation humaine des incidents passés.
- Les règles de revue (REVIEW.md) vivent sur la branche de base, ne peuvent pas être modifiées par la PR qu'elles évaluent, et sont enrichies en continu à partir des reverts, des incidents et des bugs manqués.

## Analyse approfondie

### Les boucles de vérification comme condition de la mise à l'échelle
Au sein de l'équipe Claude Code, la quasi-totalité du code (environ 90 %) est produite et relue par Claude lui-même. À cette échelle, la façon de donner aux agents les moyens de prouver, avec des preuves concrètes, que leur travail fonctionne devient un enjeu central. Les boucles de vérification sont présentées comme la brique de base qui permet de déléguer davantage de travail à Claude : sans elles, on ne peut faire tourner qu'un ou deux agents à la fois, car il faut tout vérifier soi-même ; avec elles, on peut en faire tourner des dizaines, voire des centaines, en parallèle.

La raison est que donner à un agent un moyen de vérifier sa propre production améliore nettement la qualité du résultat. Dans des tests internes sur la génération de fichiers structurés, le fait de faire évaluer le travail de Claude par un correcteur séparé, selon une grille de notation, a amélioré le taux de réussite des tâches jusqu'à 10 points par rapport à une simple boucle de prompting classique — avec les gains les plus marqués sur les problèmes les plus difficiles.

Ce qui était autrefois coûteux à vérifier (tests, benchmarks, spécifications, exécutions de bout en bout réelles) est désormais bon marché à demander à un agent : comme pour le code, les agents peuvent générer rapidement des tests, des benchmarks et des spécifications. Et une fois générés, ces tests et benchmarks s'exécutent comme n'importe quel logiciel, donc on peut les lancer fréquemment sans consommer beaucoup de tokens supplémentaires.

Il est également possible de refermer la boucle de vérification en utilisant les résultats pour améliorer la performance future de l'agent sur une tâche donnée. Par exemple, si un agent échoue de façon répétée à un test vérifiant que des données utilisateur ne se retrouvent pas dans des logs, on peut créer un hook, ou une règle plus explicite dans le fichier CLAUDE.md, pour éviter que le problème ne se reproduise. Cela empêche (en grande partie) que l'incident ne se répète.

### Tous les tests ne se valent pas : trois types à privilégier
Quel que soit le type de test choisi, certains pièges doivent être évités. Des tests instables (flaky) entraînent l'agent à simplement relancer le test plutôt qu'à corriger le code en cause. Des tests trop lents réduisent le nombre de tests que l'agent peut exécuter par lot, ce qui complique l'identification des problèmes. Les tests les plus lourds doivent donc être exécutés de préférence avant la validation (commit) des changements.

**Les tests end-to-end (E2E)**
S'il ne fallait retenir qu'un seul type de test, ce seraient les tests end-to-end. Ils décrivent de vrais parcours utilisateurs — ajouter un article au panier, passer la commande, atteindre la page de confirmation. Leur efficacité vient du fait qu'ils sont difficiles à tromper : soit la fonctionnalité marche dans son ensemble, soit elle ne marche pas. Ils ont des critères de réussite clairs et indiquent concrètement ce qui est cassé.

Les tests unitaires, bien que plus rapides et moins instables, peuvent être tous verts sans que la fonctionnalité réelle ne fonctionne, car ni l'agent ni le test ne couvrent nécessairement la tâche dans son ensemble. Avec des tests E2E, il est efficace de donner à l'agent des « mains et des yeux » sur le système réel en fonctionnement, via des outils comme CDP, des simulateurs, ou des harnais d'API pour démarrer, piloter et inspecter l'application. Une cartographie des fonctionnalités (« feature map ») peut servir de guide et de grille d'évaluation, car elle liste typiquement les fonctionnalités du point de vue de l'utilisateur, avec les parcours, raccourcis clavier, sélecteurs et résultats attendus.

**Les tests par propriétés : des contraintes qui ne doivent jamais être violées**
Beaucoup de tests reposent sur ce qu'on imagine *a priori* pouvoir casser. Les tests par propriétés ciblent au contraire les cas limites que l'on a tendance à oublier — précisément ceux où les agents échouent le plus souvent. On commence par écrire un énoncé que l'on pense infaillible, puis on utilise une bibliothèque de test (fast-check pour JS/TS, Hypothesis pour Python, proptest pour Rust, etc.) pour générer des milliers d'entrées qui tentent de le contredire.

On retrouve ce type de propriété dans presque tous les projets logiciels, par exemple :
- **Encodage aller-retour** : « si on encode X puis qu'on le décode, on retrouve X » — valable aussi pour le parsing et la sérialisation.
- **Invariants** : des propriétés qui doivent toujours rester vraies, comme « le solde d'un compte ne peut jamais devenir négatif ».
- **Idempotence** : exécuter une action (migration, normalisation, retry) deux fois produit le même effet qu'une seule fois.
- **Équivalence** : une version optimisée du code doit produire le même résultat qu'une version naïve mais correcte.

Les bibliothèques de tests par propriétés permettent de garder les agents « honnêtes », en les confrontant à des cas limites qui n'ont pas le même biais que celui de l'agent ayant écrit le code original. Elles sont particulièrement utiles lors de réécritures, lorsque la spécification a dérivé par rapport au comportement en production et n'est donc plus une source de vérification fiable.

**Les tests différentiels : l'ancien système comme oracle**
Les tests différentiels sont particulièrement efficaces pour les migrations à grande échelle où l'on s'attend à ce que le comportement fonctionnel reste identique. Le principe consiste à faire tourner l'ancien système et le nouveau sur les mêmes entrées, et à comparer les résultats. Toute divergence signale un bug ou une régression à corriger.

La clé de ces tests est d'utiliser des entrées générées aléatoirement ou un échantillon de trafic de production réel. Il faut également normaliser les facteurs non pertinents (espaces, formatage) et conserver une liste des différences approuvées, pour les cas où il est normal que le nouvel environnement diverge de l'ancien.

### Comment l'équipe Claude Code pense la vérification
Anthropic avait déjà publié un article sur le fonctionnement de la revue de code en interne ; celui-ci va plus loin sur la façon dont le travail est vérifié.

**Vérifier, c'est exécuter le changement**
Faire tourner l'application de bout en bout compte davantage que les tests eux-mêmes. On ne livrerait pas un changement iOS sans l'essayer dans un simulateur — il en va de même pour Claude. Claude peut tester toute l'application comme le ferait un humain ou un ingénieur QA : utiliser l'extension Chrome de Claude pour les changements web, un MCP iOS ou Android pour le mobile, le *computer use* pour le bureau, ou lancer le service localement pour le backend.

Pour formaliser la façon de démarrer le simulateur ou de lancer l'application, l'équipe crée une « skill » appelée *verify*, placée dans un dossier `.claude/skills/` du dépôt, aussi proche que possible du code concerné — avec autant de variantes que nécessaire. Claude sait qu'il doit utiliser cette skill *verify* avant de valider ses changements. Il est recommandé d'investir pour la rendre rapide et fiable, en demandant à Claude lui-même d'itérer et de la stress-tester, car elle constitue le harnais de smoke-test de référence. Donner à Claude un moyen de smoke-tester ses changements de bout en bout produit de bien meilleurs résultats : il itère et détecte les vraies erreurs plus vite, à la manière d'un humain. C'est ainsi que sont testés quasiment tous les changements chez Anthropic.

**Un test qui échoue appelle une attention humaine**
Personne ne peut relire chaque changement ; les échecs de tests servent donc de signal pour décider ce qui nécessite une intervention humaine. Claude exécute les vérifications et tente de corriger ce qui échoue. Si une vérification échoue encore après trois tentatives, Claude s'arrête et fait appel à un humain.

**Les propriétaires du code écrivent leurs propres vérifications**
Les personnes responsables d'un morceau de code écrivent elles-mêmes les vérifications correspondantes, et les affinent jusqu'à ce qu'elles signalent exactement ce que le propriétaire aurait lui-même relevé. Lorsqu'une vérification déclenche l'intervention d'un relecteur, elle doit indiquer pourquoi, afin que ce dernier n'ait pas à le déduire seul du diff.

**Des vérifications de fiabilité déclenchées par le diff**
L'équipe maintient une check-list de fiabilité de 39 points, chacun associé à un déclencheur identifiable depuis un diff, à une vérification, et aux incidents ou PR qui en sont à l'origine. Un exemple : « --resume charge les anciennes transcriptions » — lorsque le format de stockage de session ou les types de messages changent, on se demande si un nouveau champ se charge sans risque, puisque les anciennes transcriptions ne le contiennent pas. Claude lit le diff et ne vérifie que les points dont le déclencheur correspond — généralement entre 3 et 10 — de sorte que personne n'a besoin de mémoriser les anciens incidents.

**Un seul relecteur, plusieurs passes**
L'équipe ne cherche pas à améliorer la qualité des revues en ajoutant davantage de relecteurs : empiler un second relecteur, plus coûteux, par-dessus le relecteur principal est souvent moins efficace que d'affiner ce dernier. À la place, un fichier REVIEW.md précise les points d'attention spécifiques au code concerné. L'équipe considère aussi que les passes de revue et de vérification doivent s'appuyer les unes sur les autres : chaque passe est orientée par le contexte des passes précédentes et des échecs passés, plutôt que de tout re-vérifier depuis zéro — ce qui est à la fois moins coûteux et plus efficace.

**Un changement ne peut pas modifier les vérifications qui le jugent**
Si un changement peut modifier la vérification censée le juger, cette vérification est cassée par construction. L'outil Code Review lit le fichier REVIEW.md depuis la branche de base ou par défaut, jamais depuis les modifications de la pull request elle-même. L'équipe s'assure ainsi que les règles qui conditionnent la validation d'un changement se trouvent sur une branche que ce changement ne peut pas altérer.

L'équipe réserve également les revues à des commits précis : si quelqu'un pousse du code pendant qu'une revue est en cours, le résultat de cette revue devient obsolète — une revue validée sur un commit périmé ne veut rien dire. Elle fait aussi passer les vérifications bon marché en premier : si un agent pousse sans avoir testé localement, il consomme du temps de revue et de CI partagé qu'il aurait pu économiser en détectant le bug lui-même. Chez Anthropic, Claude exécute les tests, le build et le linter avant d'ouvrir une pull request. Cela peut être imposé via un hook qui lance les tests quand Claude termine, ou via un objectif de suite de tests entièrement verte.

**Démarrer un nouveau garde-fou en mode observation**
Dans les dépôts internes, chaque commit est annoté avec la façon dont il a été vérifié — y compris la mention « aucune », afin de pouvoir retrouver les commits non vérifiés. Un garde-fou (« gate ») de commit a été créé : il peut bloquer un commit si la session ne contenait pas de `/code-review` ou de `/verify`. Il dispose de trois modes : désactivé, observation et application stricte. Le mode observation se contente de journaliser ce qui aurait été bloqué, afin de repérer les faux positifs et de s'assurer que personne n'est pénalisé à tort. Le mode application stricte bloque réellement le commit ; un message de commit peut néanmoins expliquer pourquoi la vérification n'a pas été faite. Si un commit a déjà été bloqué deux fois dans la même session, le suivant est autorisé automatiquement, afin que Claude ne reste pas bloqué — Claude Code n'est pas parfait.

**Tester ses propres vérifications sur ce qui compte vraiment**
L'équipe Claude Code réexamine régulièrement ses propres relecteurs. Elle suit le nombre de changements fusionnés qui ont dû être annulés (reverts), le nombre de changements rejetés par un mainteneur avant fusion, ainsi qu'un sous-ensemble de changements restés propres, de taille comparable, servant de témoin.

Cela peut aussi prendre la forme d'une évaluation formelle. Comme décrit dans leur précédent article sur la revue de code, l'équipe Code Review a constitué une évaluation fondée sur des incidents et des reverts passés. Pour chaque exemple, ils reconstituent l'état du dépôt au moment de la revue et fournissent une réponse de référence en une phrase décrivant le bug en question. Seules les détections qui décrivent correctement ce bug précis rapportent des points. Des changements fusionnés et restés stables servent de groupe témoin, pour éviter de récompenser un excès de signalements. Le jeu de données utilisé pour le réglage (tuning) est distinct du jeu de test fixe utilisé pour l'évaluation finale.

L'équipe évalue séparément le taux de rappel (recall) des détections brutes, après vérification, et lors de la revue finale — ce qui permet de voir si le système perd en route des bugs qu'il avait pourtant déjà repérés. Une évaluation qui traiterait tout cela comme un score unique de bout en bout ne capturerait pas cette nuance.

Au-delà de la validité des détections, l'autre dimension qui compte est l'importance du changement signalé : un bon relecteur détecte la plupart des problèmes techniquement réels, mais ce qui importe aux humains, c'est de savoir si un bug donné est bloquant, souhaitable à corriger, ou un simple détail. L'outil Code Review reprend exactement cette logique en étiquetant chaque signalement comme « Important », « Nit » (détail mineur) ou « Pre-existing » (préexistant) — cette dernière étiquette signifiant que l'auteur du changement ne doit pas être tenu responsable d'un bug qui existait déjà avant son intervention. Enfin, l'équipe Claude Code règle le rappel du système jusqu'au point où toute amélioration supplémentaire relèverait du surapprentissage sur l'évaluation plutôt que d'une détection réelle de bugs supplémentaires.

**Transformer les erreurs manquées en règles**
Dans le dépôt de Claude Code, deux méthodes permettent de transformer des cas manqués en nouvelles règles. La première consiste à extraire des motifs récurrents dans les commentaires de revue humaine et les reverts de PR afin d'identifier des problèmes communs : pour être retenu comme règle potentielle, un motif doit apparaître dans au moins deux PR et être identifiable directement depuis un diff. Trois agents tentent ensuite de réfuter chaque règle candidate, avant qu'elle ne soit examinée et validée par un humain dans le cadre d'une pull request.

La seconde méthode consiste à rejouer trois détecteurs de bugs sur une PR associée à un incident connu. Si au moins deux d'entre eux détectent le bug, celui-ci est considéré comme détectable. Si, en revanche, le bug est manqué alors que le diff est petit, cela révèle une lacune qui mérite d'être transformée en règle dans le fichier REVIEW.md.

Les tests instables (flaky) reçoivent le même traitement rigoureux : Claude n'a pas le droit de les ignorer, d'ajouter des pauses (sleep) ou de relancer le test jusqu'à ce qu'il passe. S'il ne parvient pas à identifier la cause racine, il supprime le test et consigne la raison de cette suppression. Les règles elles-mêmes doivent aussi être nettoyées régulièrement : suites de tests, étapes de vérification et fichiers .md ont tendance à ne faire que croître si on les laisse faire — l'équipe les élague donc de façon routinière.

### De bons tests, de bons résultats
L'enseignement central de l'équipe est que doter un agent d'un moyen de vérifier son propre travail, via une boucle de retour solide, change radicalement la donne. Il faut traiter la couche de vérification comme n'importe quel autre système critique : la garder hors de portée des changements qu'elle évalue, la calibrer sur les bugs qui comptent réellement, consigner les leçons tirées des erreurs manquées pour qu'elles ne se reproduisent pas, et élaguer régulièrement ces leçons pour qu'elles restent pertinentes. En procédant ainsi, le rôle humain passe de la relecture systématique de chaque diff à la définition de ce que signifie « terminé » et à l'examen des preuves apportées — ce qui est précisément ce qui permet de faire tourner de nombreux agents Claude en parallèle.

## Pourquoi ça compte
Cet article formalise un enjeu central pour toute organisation qui adopte des agents de codage à grande échelle : sans boucles de vérification robustes (E2E, tests par propriétés, tests différentiels, check-lists déclenchées par diff, gating des commits), la relecture humaine reste le goulot d'étranglement qui limite le passage à l'échelle de l'IA générative dans le développement logiciel.
