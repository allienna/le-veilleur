---
title: "How our AI Research team uses AI Runtime"
date: 2026-10-27
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.databricks.com%2Fblog%2Fhow-our-ai-research-team-uses-ai-runtime%3Futm_source=tldrdev/1/010001a177ec9e3b-d8a8bcd7-916f-40b1-9f94-99dc86ce5111-000000/JgvxcyCvkeOwTZiDRF2UWkT-PYBT2kI6uX97pusdkOA=452"
keywords: ["Databricks", "infrastructure GPU", "autoresearch", "apprentissage par renforcement", "MLflow", "AI Runtime"]
theme: "IA"
tone: "news"
used_in: ["2026-10-27"]
---

## Résumé
L'équipe de recherche IA de Databricks explique comment elle utilise Databricks AI Runtime (AIR) pour entraîner et évaluer les modèles qui alimentent des produits comme Genie, AI Functions et la recherche optimisée. AIR fournit une résilience GPU intégrée, un CLI pour un déploiement rapide, une intégration MLflow pour le suivi des expériences, et un accès gouverné aux données via Unity Catalog. L'article souligne aussi la montée en puissance de « l'autoresearch » (popularisé par Andrej Karpathy), où des agents proposent, lancent et évaluent eux-mêmes les expériences, ce qui a multiplié par 8 le volume de jobs d'entraînement sur les workloads AI Functions.

## Points clés
- AIR gère des entraînements allant de quelques GPU à des centaines de GPU H100/B300 sur plusieurs jours ou semaines, avec détection et mise en quarantaine automatique des nœuds défaillants.
- Le CLI AIR et les conteneurs Docker personnalisés permettent de lancer des jobs d'entraînement en quelques secondes, raccourcissant les cycles d'itération.
- MLflow est automatiquement intégré par AIR pour le suivi des expériences, sans configuration supplémentaire, et sert aussi aux agents pour évaluer les résultats.
- L'accès aux données de recherche se fait via Unity Catalog, monté comme un système de fichiers local (FUSE), garantissant gouvernance et traçabilité même entre workspaces.
- La priorisation et la préemption des workloads permettent d'allouer la capacité GPU disponible entre projets concurrents, y compris pour des expériences exploratoires pendant les temps creux.
- L'essor de « l'autoresearch » (agents autonomes qui lancent et évaluent les expériences) a multiplié par 8 le nombre de jobs d'entraînement, exigeant une infrastructure capable de supporter des lancements rapides et fiables à grande échelle.

## Analyse approfondie
Chez Databricks, nous développons et évaluons continuellement de nouvelles techniques de recherche en IA pour rendre nos produits plus intelligents, plus efficaces et plus utiles pour nos clients.

Nos recherches couvrent des produits comme Genie, Smart Routing et AI Functions. Récemment, nous avons publié comment nous avons rendu la recherche 3 fois plus rapide, développé de nouvelles techniques d'apprentissage par renforcement hors ligne (offline reinforcement learning), et repoussé les limites de l'extraction de documents complexes.

Pour construire d'excellents modèles d'IA et gérer des centaines de chantiers de recherche en parallèle, nous avons besoin d'une infrastructure capable de suivre le rythme. C'est pourquoi nous utilisons Databricks AI Runtime (AIR).

Dans cet article, nous expliquons comment AIR nous aide à expérimenter rapidement, à monter en échelle pour de grandes charges d'entraînement, et à nous adapter à l'entraînement piloté par des agents, ainsi que ce que nous avons appris sur la gestion des ressources GPU entre projets de recherche.

Notre équipe de recherche développe les modèles qui alimentent les Databricks AI Functions, notamment `ai_parse_document` et `ai_extract`. Par exemple, les Databricks AI Functions offrent une qualité d'analyse de documents à l'état de l'art, portée par des modèles entraînés pour comprendre les documents d'entreprise. Atteindre ce niveau de qualité nécessite une recherche approfondie sur différentes architectures, jeux de données, techniques d'entraînement et hyperparamètres, à travers des dizaines de milliers de runs d'entraînement et d'évaluation.

Nous utilisons le fine-tuning supervisé (SFT), l'apprentissage par renforcement hors ligne (RL) et l'apprentissage par renforcement en ligne pour entraîner des modèles allant de quelques milliards de paramètres à près d'un trillion. Selon la charge de travail, nous utilisons des GPU NVIDIA H100 ou B300, tous deux disponibles via AIR. Nos plus grands entraînements peuvent nécessiter des centaines de GPU travaillant ensemble pendant des jours ou des semaines, avec un réseau à haute bande passante pour maintenir l'efficacité de l'entraînement.

Supporter ces charges de travail crée trois défis :

Notre équipe de recherche est le « client zéro » d'AI Runtime depuis la création du produit l'année dernière. Nous utilisons AIR pour développer, entraîner et tester les modèles qui alimentent les produits IA de Databricks, en nous appuyant sur son infrastructure GPU et son intégration avec nos outils existants.

**Résilience GPU intégrée**

AIR effectue des vérifications préalables (preflight checks) sur les nœuds GPU attribués pour s'assurer qu'ils sont sains et peuvent communiquer efficacement avant le début de l'entraînement. Il surveille également l'état des nœuds pendant l'exécution, détectant des problèmes tels que les échecs de communication NCCL, la limitation thermique ou de puissance (throttling), et les problèmes de pilotes GPU. Si un nœud devient défaillant et provoque l'échec d'un job, AIR détecte le problème et met en quarantaine le nœud concerné afin que les jobs suivants ne soient pas programmés sur la même infrastructure défectueuse.

Ceci est particulièrement important pour des projets comme KARL, où la génération complexe de rollouts et le post-entraînement de modèles de plus de 100 milliards de paramètres peuvent nécessiter des milliers d'heures GPU. Plutôt que de dépanner sans cesse des pannes d'infrastructure, nous pouvons nous concentrer sur l'amélioration de nos modèles.

**Itération rapide avec le CLI AIR et des conteneurs personnalisés**

La recherche nous oblige à changer fréquemment de configurations de modèles, d'approches d'entraînement et de code. Avec le CLI AIR, nous pouvons lancer des charges de travail de manière programmatique, spécifier les GPU dont nous avons besoin, et laisser AIR gérer le provisionnement et la planification, y compris le réseau à haute bande passante pour l'entraînement distribué entre clouds.

Nous nous appuyons également sur des conteneurs Docker personnalisés pour le développement local. AIR nous permet d'utiliser ces mêmes images pour l'entraînement, garantissant la compatibilité sans recréer nos environnements. Nous pouvons téléverser notre base de code, exécuter du code personnalisé dans ces conteneurs, et utiliser le Databricks Artifact Registry pour enregistrer et partager des images entre expériences. Les investissements d'AIR dans la latence de lancement et l'optimisation des conteneurs nous aident à démarrer des jobs d'entraînement en quelques secondes, raccourcissant les boucles de retour lorsque nous testons de nouvelles idées.

**MLflow et journalisation pour le suivi des expériences**

Nous utilisons MLflow pour suivre nos expériences de recherche. AIR crée et gère automatiquement des expériences MLflow pour nos jobs d'entraînement, éliminant toute configuration séparée.

Nous pouvons surveiller l'état des jobs, diffuser et inspecter les journaux d'entraînement, et récupérer des métriques pour comprendre la progression des expériences. Cela donne également à nos agents IA l'accès aux informations dont ils ont besoin pour évaluer les résultats et déterminer la prochaine étape à tenter.

**Accès fluide et gouverné aux données de recherche**

Toutes nos données de recherche sont stockées dans Unity Catalog. Grâce au montage FUSE d'Unity Catalog, AIR nous permet d'accéder à ces données comme si elles faisaient partie d'un système de fichiers local, même en travaillant sur différents workspaces Databricks.

Cela garde nos données accessibles, suivies, partageables et gouvernées, sans changer la façon dont notre code d'entraînement interagit avec les fichiers. Combiné à MLflow et à nos environnements basés sur Docker, cela nous offre un flux de travail cohérent, du développement local à l'entraînement distribué.

**Gestion de la capacité GPU entre projets de recherche**

Nos charges de travail ont des besoins en ressources très différents. Une expérience de débogage peut ne nécessiter que quelques GPU, tandis qu'un entraînement de grande ampleur peut en requérir des centaines pendant des jours ou des semaines. Différents projets ont aussi des échéances et des priorités concurrentes.

Les capacités de priorisation et de préemption des charges de travail d'AIR nous aident à allouer les ressources entre projets, à prioriser les expériences urgentes, et à utiliser la capacité excédentaire lorsqu'elle est disponible. Par exemple, la capacité libre peut soutenir des expériences exploratoires supplémentaires pendant un week-end sans perturber les travaux prioritaires. Notre objectif est de garder les ressources GPU disponibles pour les expériences qui comptent, sans exiger que les chercheurs coordonnent manuellement l'infrastructure.

Popularisé par Andrej Karpathy, « l'autoresearch » change la façon dont nous développons les modèles d'IA. Plutôt que les chercheurs lancent et évaluent manuellement chaque expérience, nous utilisons de plus en plus des agents pour proposer des changements, lancer des expériences, évaluer les résultats et déterminer la prochaine étape.

Ce changement a considérablement augmenté notre volume d'expérimentation. Sur l'ensemble de nos charges de travail de recherche liées à AI Functions, le nombre de jobs d'entraînement a augmenté de **8x**.

À mesure que les agents prennent en charge une plus grande partie du processus de recherche, notre infrastructure doit suivre le rythme. Un démarrage lent ou une erreur de configuration confuse peut être gérable lorsqu'un chercheur lance une poignée d'expériences. Lorsque des agents en lancent des centaines, ces mêmes problèmes deviennent rapidement des goulots d'étranglement.

La recherche pilotée par des agents exige des lancements de jobs rapides, des interfaces programmatiques, des erreurs claires et exploitables, une exécution fiable, et des résultats d'entraînement accessibles.

Notre flux de travail d'autoresearch suit un cycle continu :

AIR est particulièrement bien adapté à ce flux de travail car les agents peuvent interagir avec lui de manière programmatique et bénéficier de ses lancements de jobs rapides, de sa fiabilité intégrée et de sa capacité à monter en échelle. Grâce au CLI Databricks et à `databricks-air-skills`, nos agents peuvent lancer des charges de travail concurrentes, surveiller l'état des jobs, récupérer les métriques MLflow, et itérer en fonction des résultats.

Cela nous permet de mener davantage d'expériences tandis que nos chercheurs se concentrent sur le développement de nouvelles idées et l'amélioration de la qualité des modèles. En avançant davantage vers une recherche pilotée par des agents, AIR nous donne l'infrastructure nécessaire pour soutenir à la fois des modèles plus grands et un rythme d'expérimentation plus rapide.

Notre expérience avec AI Runtime nous a montré à quel point une infrastructure GPU fiable et flexible compte pour la recherche. De l'entraînement à grande échelle et de l'accès gouverné aux données jusqu'à l'expérimentation pilotée par des agents, AIR nous permet de passer moins de temps à gérer l'infrastructure et plus de temps à développer de meilleurs modèles.

Si vous entraînez ou affinez vos propres modèles, consultez la documentation d'AI Runtime pour démarrer.

AI Runtime a également soutenu nos recherches dans des domaines comme la recherche plus rapide, l'apprentissage par renforcement et la compréhension de documents. Découvrez davantage de nos travaux sur Databricks AI Research.

## Pourquoi ça compte
Cet article illustre une tendance de fond dans l'industrie de l'IA : le passage d'une recherche pilotée par des humains à une recherche pilotée par des agents autonomes, qui multiplie le volume d'expérimentation et impose de nouvelles exigences d'infrastructure (latence, fiabilité, gouvernance des données). C'est un signal utile pour la veille sur l'évolution des plateformes MLOps/AI Infra et sur la diffusion du concept d'« autoresearch ».
