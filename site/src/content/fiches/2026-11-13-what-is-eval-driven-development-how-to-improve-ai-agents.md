---
title: "What Is Eval-Driven Development? How to Improve AI Agents"
date: 2026-11-13
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.langchain.com%2Fblog%2Fwhat-is-eval-driven-development%3Futm_source=tldrdev/1/010001a1cfae83fa-95955eea-26d1-4332-a12c-a331f7108446-000000/Xe9YUjjf89ZeZS9FGm2FE-C3TLOWuhuZFcRPE7LkN7c=452"
keywords: ["eval-driven development", "agents IA", "LangSmith", "tests logiciels", "LLM-as-judge", "benchmarking"]
theme: "IA"
tone: "tutorial"
used_in: ["2026-11-13"]
---

## Résumé
L'article de LangChain présente l'"eval-driven development" (EDD), une méthode qui consiste à construire un agent IA en mesurant en continu sa performance face à un jeu d'évaluations (evals) plutôt qu'en itérant à l'aveugle sur des prompts. La démarche se décompose en trois étapes : définir précisément ce qu'est un "bon" comportement, écrire l'eval avant de coder la fonctionnalité, puis comparer les expériences à chaque changement pour détecter progrès et régressions. L'article détaille comment construire des jeux de données, choisir entre évaluation par code ou par LLM-juge, exécuter une expérience de référence (baseline), puis maintenir ces evals en CI et en production via des traces, des tableaux de bord et des files d'annotation. Il conclut sur une liste d'erreurs fréquentes, comme définir le succès de façon trop vague ou se fier à un score moyen qui masque des régressions locales.

## Points clés
- L'EDD s'inspire du TDD (test-driven development) mais l'adapte à la nature non déterministe des agents IA, où plusieurs réponses peuvent être correctes et où l'agent choisit lui-même ses étapes (outils appelés, actions prises).
- La première étape consiste à rédiger une spécification courte et tranchée : quand le comportement doit se déclencher, ce que l'agent doit faire, ce qu'il ne doit pas faire, et quels comportements existants doivent rester intacts.
- Un jeu de données d'évaluation doit idéalement s'appuyer sur de vraies traces de production (via LangSmith) plutôt que sur des exemples inventés, pour mieux refléter les usages réels, y compris les cas limites.
- Le choix de l'évaluateur dépend du type de vérification : un eval "code" pour les critères déterministes (ex. bon outil appelé), un LLM-as-a-judge pour les critères plus subjectifs.
- Comparer des expériences ne doit pas se limiter au score moyen : il faut vérifier cas par cas qu'un gain sur un comportement n'a pas cassé un comportement déjà fonctionnel (régression), et surveiller le surapprentissage via un jeu d'exemples tenu à l'écart (held-out).
- En production, plusieurs dispositifs complètent les evals de développement : évaluateurs en ligne sur un échantillon de trafic, files d'annotation humaine, tableaux de bord de suivi, et regroupement de traces en clusters pour détecter de nouveaux motifs d'échec.

## Analyse approfondie

### Qu'est-ce que l'eval-driven development ?
Le développement d'un agent IA commence presque toujours de la même façon : on écrit un prompt, on teste quelques questions à la main, on ajuste, on recommence. Cette approche fonctionne bien au début, quand les erreurs de l'agent sont évidentes et les progrès faciles à percevoir. Mais au fil du temps, il devient de plus en plus difficile de savoir si le dernier changement a réellement amélioré l'agent ou l'a dégradé.

L'eval-driven development (EDD) répond à ce problème en fournissant un ensemble cohérent de métriques pour mesurer la performance de l'agent et guider la prise de décision. Chez LangChain, l'EDD a été utilisé pour construire leurs agents les plus avancés, et la méthode se résume à un processus en trois étapes :
1. Définir ce qu'est un bon comportement pour l'agent.
2. Écrire l'eval avant de construire la fonctionnalité.
3. Effectuer le changement, puis comparer.

Le nom et le concept de l'EDD s'inspirent du test-driven development (TDD), où l'on écrit un test qui échoue avant d'écrire le code qui le fait réussir. Mais les agents diffèrent du code traditionnel car ils sont non déterministes :
- **Les sorties varient** : la même question peut recevoir une réponse différente à chaque exécution.
- **Plusieurs réponses peuvent être correctes** : deux résultats en langage naturel peuvent tous deux être jugés corrects malgré une formulation différente.
- **L'agent choisit ses propres étapes** : il peut appeler un outil dont il n'avait pas besoin, ou en sauter un qu'il aurait dû utiliser, et malgré tout atteindre la bonne réponse.

Les agents ont donc besoin d'un type de test différent. Un eval score des exécutions de l'agent sur un ensemble d'exemples. Les evals sont plus flexibles que les tests traditionnels : on peut évaluer n'importe quel aspect du déroulement de l'agent, et on peut utiliser d'autres LLM pour effectuer cette notation (LLM-as-a-judge). Avec l'EDD, comme avec le TDD, ces evals deviennent la définition même du succès, et l'on construit l'agent en direction de cet objectif.

### Étape 1 : définir ce qu'est un bon comportement pour l'agent
La première étape de l'EDD consiste à définir ce que l'agent doit faire, puis à lister les comportements qu'il doit gérer pour y arriver : répondre à des questions à partir d'une base de connaissances, agir pour le compte d'un utilisateur, ou savoir quand poser une question de clarification. On consigne les exigences de chaque comportement ; l'ensemble forme un document d'exigences produit (PRD) pour l'agent.

L'EDD travaille un comportement à la fois. Cela donne une cible étroite vers laquelle progresser ("hill climbing"), sans qu'un changement ne vienne brouiller l'effet d'un autre. Le comportement choisi provient généralement d'une fonctionnalité à venir ou d'un échec constaté dans les exécutions passées de l'agent. Avant d'écrire du code, il est utile de rédiger une spécification courte couvrant :
- Quand le comportement doit se produire
- Ce que l'agent doit faire
- Ce que l'agent ne doit pas faire
- Quels comportements du PRD doivent continuer à fonctionner

Cette spécification doit être suffisamment tranchée pour être notée en succès ou échec.

L'article prend l'exemple d'un agent de documentation interne que les employés interrogent pour obtenir des informations sur l'entreprise. Il dispose de deux outils : `search_docs` pour la documentation interne et `web_search` pour le reste. L'équipe prévoit d'ajouter un outil `create_ticket` pour qu'il puisse ouvrir des tickets IT. La spécification ressemble à ceci :
- Quand : un utilisateur signale quelque chose de cassé, comme "Mon ordinateur ne se connecte pas au VPN."
- À faire : appeler `create_ticket`.
- À ne pas faire : ouvrir un ticket pour des questions de type "comment faire", comme "Comment me connecter au VPN ?"
- À préserver : `search_docs` et `web_search` continuent de traiter les questions qu'ils traitent aujourd'hui

L'évaluation se fera sur ces critères, même si l'agent n'a pas encore la capacité correspondante.

### Étape 2 : écrire l'eval avant de construire
**Construire un jeu de données.** Un jeu de données est une collection de cas de test ("exemples") comportant des entrées et, optionnellement, des sorties de référence ("golden"). L'une des meilleures sources d'entrées est constituée des véritables exécutions de l'agent : les utilisateurs formulent les choses de manières imprévisibles, et leurs requêtes incluent des cas limites qu'on n'aurait pas pensé à écrire soi-même. Si les exemples ressemblent au trafic réel, un bon score à l'eval a plus de chances de refléter un bon comportement en production. Dans LangSmith, on peut ajouter directement de vraies exécutions d'agent à un jeu de données. En l'absence d'exécutions existantes, une alternative courante consiste à construire les exemples à partir de zéro.

Pour l'agent de documentation, une poignée d'exemples suffit pour démarrer : des demandes de ticket, ainsi que des questions qui doivent toujours être dirigées vers `search_docs` et `web_search`, afin de préserver le comportement existant. On peut aussi étendre le jeu de données pour couvrir des cas non encore représentés : par exemple, s'il manque des exemples d'utilisateurs frustrés, on peut demander à un LLM de reformuler des exemples existants sous une forme plus "énervée", puis vérifier que l'agent appelle toujours le bon outil.

**Écrire un évaluateur.** Une fois le jeu de données constitué, on transforme la définition de "bon comportement" issue du PRD en un test ou un eval qui note la performance de l'agent sur ces exemples. Il faut choisir la méthode de notation adaptée : un eval par code quand la vérification est déterministe, un LLM-as-a-judge quand elle ne l'est pas. Veut-on examiner la réponse finale de l'agent, une action qu'il a entreprise en chemin, ou autre chose ? Pour l'agent de documentation, on veut vérifier les outils appelés afin de s'assurer qu'il utilise les bons dans chaque cas ; le choix de l'outil est facile à vérifier par code, donc un eval de type code suffit pour contrôler que chaque exemple a bien appelé l'outil listé dans sa sortie de référence.

Cet agent de documentation reste un chatbot simple avec quelques fonctions précises. Pour des agents plus complexes, la suite d'evals doit souvent prendre une forme différente. Si l'agent modifie un environnement — par exemple un agent de codage opérant dans un bac à sable (sandbox) —, vérifier simplement quelques appels d'outils et la réponse finale ne suffit pas. Il faut contrôler l'état laissé par l'agent dans le système, et chaque exécution a besoin d'un environnement propre pour qu'une exécution n'affecte pas la suivante. Harbor est un framework open source conçu pour exécuter des agents sur ce type de tâches ; c'est le harnais derrière des benchmarks industriels comme Terminal-Bench. Chaque tâche s'exécute dans son propre bac à sable et s'accompagne d'un script de test qui note l'état final.

Optimiser pour un benchmark comme Terminal-Bench suit la même boucle que l'EDD : on écrit d'abord les tâches et les tests, on exécute une baseline, puis on compare les expériences à chaque changement apporté à l'agent. Lors de la construction de LangSmith Engine, l'équipe a créé son propre benchmark à partir d'exécutions réelles et synthétiques, exécuté comme un eval Harbor. Harbor est aussi utilisé pour évaluer Deep Agents, ce qui permet de savoir si certaines parties du harnais — comme le middleware de liste de tâches (todo-list) ou des portions du prompt système — peuvent être supprimées sans dégrader l'agent.

**Exécuter une baseline.** Quelle que soit la méthode choisie pour construire le jeu de données ou l'évaluateur, on exécute l'agent sur chaque exemple et on enregistre les résultats comme une expérience dans LangSmith. Une expérience correspond à une exécution unique de l'agent sur tout le jeu de données, où l'entrée, la sortie et les scores de l'évaluateur de chaque exemple sont enregistrés ensemble dans un même relevé. Disposer d'un système centralisé permet de comparer les résultats de différentes versions de l'agent entre elles. Avant tout changement sur l'agent, il est important d'exécuter une expérience de référence (baseline) comme point de comparaison.

Pour l'agent de documentation, les exemples liés aux tickets obtiennent un score d'échec, puisque l'outil n'existe pas encore. Les autres exemples enregistrent ce qui fonctionne déjà, ce qui permet de vérifier plus tard si l'ajout du nouvel outil casse autre chose.

### Étape 3 : effectuer le changement et comparer
L'équipe construit alors l'outil `create_ticket` et relance le même eval.

L'EDD repose sur l'idée de "hill-climbing" : répéter le processus d'amélioration de l'agent (évaluer, comparer, ajuster) pour établir une boucle bien définie, appuyée sur des preuves objectives de progrès. Chaque nouveau changement sur l'agent donne lieu à sa propre expérience, comparée à la précédente pour vérifier le progrès. Dans LangSmith, on peut ouvrir une vue de comparaison en sélectionnant les deux expériences : elle affiche les scores côte à côte pour chaque exemple, ce qui permet de voir lesquels se sont améliorés et lesquels ont régressé.

Lors de la comparaison des expériences, il est important de ne pas se limiter aux variations du score moyen, mais aussi de repérer les régressions ou l'écrasement d'un comportement qui fonctionnait auparavant. Avec l'agent de documentation, les exemples de tickets réussissent désormais. Mais la question "Comment me connecter au VPN ?" déclenche maintenant l'ouverture d'un ticket au lieu d'une recherche dans la documentation. Le score moyen a augmenté, mais un cas s'est cassé.

Examiner une trace reste le meilleur moyen de comprendre pourquoi un eval échoue. Une trace est l'enregistrement complet d'une exécution de l'agent, incluant chaque appel de modèle et chaque appel d'outil. Le traçage est possible dans LangSmith avec n'importe quel agent construit avec le framework de son choix. En ouvrant la trace en échec de la dernière expérience, on constate que la description de l'outil indique d'utiliser `create_ticket` pour les "problèmes de VPN et d'ordinateur", si bien que toute question mentionnant le VPN correspond au déclencheur. Cela écrase le bon comportement initial (la baseline).

La solution consiste à restreindre la description de l'outil aux demandes qui nécessitent une action de l'équipe IT. Après ce changement, l'eval est relancé : tous les exemples réussissent désormais.

Un score parfait sur un petit jeu de données est bon signe, mais 100 % n'est pas toujours la cible à viser : la description de l'outil a été ajustée en regardant précisément ces exemples. Si l'on continue d'ajuster l'agent jusqu'à ce que chaque exemple réussisse, on risque de sur-ajuster (overfitting) sur le jeu de données plutôt que sur le comportement réellement visé — l'eval passe, mais des requêtes formulées différemment des exemples restent manquées. Pour s'en prémunir, il faut conserver un jeu d'exemples tenu à l'écart (held-out) qu'on ne consulte pas pendant l'itération. Si le score progresse sur les exemples utilisés pour ajuster mais reste stable sur le jeu tenu à l'écart, c'est le signe d'un surapprentissage probable.

Les agents multi-étapes peuvent échouer à n'importe quelle étape, donc LangSmith permet d'évaluer plus que la seule réponse finale : on peut noter une étape unique, la séquence complète d'appels d'outils, ou une conversation multi-tours regroupée en fil (thread).

### Maintenir l'EDD au fil du déploiement
**Automatiser ses evals.** À mesure que les déploiements s'accélèrent, il devient facile d'oublier d'exécuter les evals ou de perdre le fil des anciens exemples. En intégrant l'évaluation automatisée au workflow, on empêche des changements non testés d'atteindre les utilisateurs et on détecte les régressions avant la mise en production. La meilleure stratégie pour construire sa suite d'evals dépend du contexte : des vérifications par code rapides peuvent bloquer une fusion (merge) problématique, tandis que des evals plus lents avec des LLM-juges peuvent s'exécuter chaque nuit ou avant une sortie. On peut utiliser des sous-ensembles du jeu de données pour n'exécuter, pendant l'itération, que les exemples liés au comportement travaillé, puis l'ensemble complet avant la mise en production. LangSmith s'intègre avec pytest et Vitest, ce qui permet de placer les evals aux côtés du code et de les exécuter à chaque pull request ; chaque exécution est enregistrée comme une expérience, visible au même endroit que le reste.

**Évaluer en production.** Avant le déploiement, le jeu de données ne couvre généralement que les cas envisagés en développement. En production, plusieurs méthodes permettent de repérer le reste :
- **Les évaluateurs en ligne** notent les traces en direct à mesure qu'elles arrivent ; on peut attacher des vérifications par code et des LLM-juges à un projet de traçage, et échantillonner une part du trafic pour maîtriser les coûts.
- **Les files d'annotation** permettent à l'équipe de relire manuellement les exécutions signalées ; c'est aussi le moyen de vérifier qu'un LLM-juge est d'accord avec des évaluateurs humains avant de s'y fier.
- **Les tableaux de bord** permettent de suivre dans le temps les scores d'eval, les retours utilisateurs, le coût et la latence, afin de voir si une version a amélioré ou dégradé les choses.
- **Les "Insights"** regroupent les traces de production en clusters pour repérer de nouveaux motifs à grande échelle, sur des milliers d'exécutions.
- **LangSmith Engine** va plus loin en transformant des clusters de problèmes en exemples de jeu de données, assortis d'assertions à passer en revue.

LangChain a également publié les evals utilisés pour Deep Agents dans son dépôt, afin de montrer une suite d'evals de production réelle.

### Erreurs courantes
- **Définir le succès de façon trop vague.** Il faut faire l'effort, en amont, de définir clairement le succès pour que les evals puissent noter facilement un succès ou un échec. "La réponse est utile" n'est pas une métrique bien définie.
- **Écrire l'eval après le correctif.** Une fois qu'on a vu la nouvelle sortie, il est facile d'écrire un eval conçu pour réussir. Il faut l'écrire d'abord et vérifier qu'il échoue sur la version actuelle, défaillante.
- **Ne regarder que le score moyen.** Les améliorations du score moyen peuvent masquer des exemples qui ont régressé ou des changements qui ont écrasé un bon comportement. Il faut revoir chaque exemple avant de conserver un changement.
- **Ajouter des evals superflus.** Chaque eval pousse l'agent dans une direction donnée. Il faut relier chaque eval à un changement précis, comme un échec que l'on corrige ou une fonctionnalité à venir.
- **Faire confiance à un juge non vérifié.** Il faut comparer le LLM-juge à des scores humains avant de l'utiliser, lui poser des questions précises, et préférer une notation succès/échec à une échelle ambiguë de 1 à 10.

## Pourquoi ça compte
L'EDD propose un cadre méthodologique concret pour sortir du tâtonnement manuel sur les prompts et industrialiser l'amélioration des agents IA, un enjeu central pour toute équipe qui déploie des agents en production. Pour une veille tech, c'est un bon marqueur de la maturation des pratiques d'ingénierie autour des LLM, qui empruntent de plus en plus aux disciplines établies du développement logiciel (TDD, CI, observabilité).
