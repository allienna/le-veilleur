---
title: "Agent Substrate available on GKE | Google Cloud Blog"
date: 2026-09-18
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fcloud.google.com%2Fblog%2Fproducts%2Fcontainers-kubernetes%2Fagent-substrate-available-on-gke%3Futm_source=tldrai/1/010001a0af8f638d-dcc57c6a-1a9b-4a37-be52-1a8f5d78e44e-000000/eQnN6nLAOAWEyYqb10FKXZ0IWpE9l4qmvfGj1_hQy9c=452"
authors: ["Alex Zakonov", "Tim Hockin"]
keywords: ["agents IA", "Kubernetes", "GKE", "sandboxing", "sécurité", "scalabilité"]
theme: "IA"
tone: "news"
used_in: ["2026-09-18"]
---

## Résumé
Google Cloud annonce la disponibilité d'Agent Substrate sur GKE, un runtime open source « secure-by-default » conçu pour exécuter des millions de sandboxes d'agents IA avec une densité 10 fois supérieure à celle des runtimes de conteneurs classiques. L'outil promet des reprises d'activité en moins de 500 ms et plus de 500 activations de suspend/resume par seconde, grâce à une isolation réseau et noyau de type zero-trust. Nous Research, éditeur de l'agent Hermes (classé numéro 1 mondial sur OpenRouter), fait partie des premiers partenaires à construire sur cette infrastructure. L'article détaille les principes architecturaux qui permettent de faire cohabiter forte isolation, faible latence et économie de calcul à grande échelle.

## Points clés
- Agent Substrate est open source, tourne sur n'importe quel cluster Kubernetes, et est optimisé pour GKE (notamment les processeurs Arm « Axion » de Google).
- Il vise les contraintes propres aux flottes d'agents autonomes : exécution de code non fiable, accès outillé (CLI, navigateurs headless), pics massifs de création de sandboxes, et calcul majoritairement inactif.
- L'isolation repose au choix sur des microVM Cloud Hypervisor (compatibilité noyau Linux complète) ou sur gVisor (isolation plus légère), avec une passerelle dédiée pour contrôler finement les flux réseau entrants/sortants.
- Un plan de contrôle et un plan de données séparés permettent la suspension/reprise en quelques centaines de millisecondes, avec des snapshots persistés sur disque local et Google Cloud Storage.
- Ce modèle « zero-idle » permettrait d'héberger plus de 1000 agents dormants par machine, soit une densité 10x supérieure aux approches traditionnelles ; un contrôleur de volumes Filestore optionnel apporte du stockage NFS partagé et persistant entre les tours d'exécution.
- Nous Research (agent Hermes) est cité comme partenaire de conception ayant validé la capacité du système à gérer l'isolation et le contrôle d'accès par agent à grande échelle.

## Analyse approfondie
**Alex Zakonov, VP Engineering, et Tim Hockin, Engineer,** signent cette annonce.

Google Cloud présente Agent Substrate comme un runtime d'exécution d'agents open source et « secure-by-default », taillé pour faire tourner des millions de sandboxes avec une densité dix fois supérieure aux runtimes de conteneurs standards. Le système atteint des reprises en moins de 500 ms et plus de 500 activations de suspend/resume par seconde, avec une isolation réseau et noyau native de type zero-trust.

Agent Substrate fonctionne sur n'importe quelle infrastructure Kubernetes et est optimisé pour GKE. Plusieurs équipes IA de premier plan s'appuient déjà sur lui : Nous Research, l'éditeur de l'agent Hermes, construit activement dessus. Hermes est aujourd'hui classé agent IA numéro 1 au monde en usage sur OpenRouter, toutes catégories confondues (productivité, développement, CLI, agents personnels).

### Du prototype local à un million d'agents
Des développeurs font déjà tourner localement Antigravity, Claude Code, Codex, OpenClaw, Hermes et d'autres harnais d'agents — mais c'est très différent de faire tourner des centaines de milliers d'agents concurrents et de longue durée, qui génèrent du code, interagissent avec des outils et pilotent une exécution automatisée. Les architectures existantes ont souvent du mal à répondre à ces défis.

Faire passer une plateforme d'agents d'un prototype local à une exécution à grande échelle change fondamentalement les contraintes d'infrastructure, notamment :

- **Des frontières de confiance opaques** : les modèles peuvent générer et exécuter du code arbitraire à la volée. Sans isolation au niveau noyau et contrôles réseau dynamiques, exécuter du code non fiable qu'aucun humain n'a jamais examiné expose à des évasions (« host escape »), au vol d'identifiants et à l'exfiltration de données.
- **Des frictions d'accès aux outils** : les agents ont besoin d'environnements informatiques complets pour invoquer des outils en ligne de commande, des navigateurs headless et des espaces de travail sur système de fichiers. Faire cela de façon sûre doit être rapide et simple.
- **Des pics massifs** : les harnais d'agents, les benchmarks et les déploiements de reinforcement learning peuvent générer des milliers de sandboxes par minute. Les ordonnanceurs généralistes ont du mal à supporter cette rotation, et la décompression répétée d'images de conteneurs peut provoquer une forte contention disque.
- **Du calcul inactif** : les agents autonomes passent la majorité de leur temps dormants, en attente d'une inférence de modèle, d'une réponse d'outil ou d'un retour humain. Réserver du CPU et de la RAM dédiés à des conteneurs inactifs gaspille des ressources précieuses.

### Un substrat conçu pour les agents
Lorsque les équipes plateforme se heurtent à ces défis, elles font face à un compromis inacceptable : sacrifier le contrôle et l'isolation, ou subir la latence élevée et l'inefficacité des VM. Google Cloud estime que les équipes ne devraient pas avoir à choisir.

Agent Substrate évite ce compromis en découplant l'exécution des agents de la gestion des machines. Construit sur une infrastructure Kubernetes cloud-native, il offre une nouvelle couche d'exécution pensée spécifiquement pour les charges de travail agentiques.

Cette couche d'exécution gère directement le cycle de vie des environnements d'agents sandboxés avec :

- **Sécurité par défaut** : des microVM Cloud Hypervisor isolées matériellement ou des sandboxes gVisor, couplées à des proxys de sortie qui appliquent des politiques réseau granulaires et injectent les identifiants hors de portée des agents eux-mêmes, empêchant le vol de credentials.
- **Activation en moins d'une seconde** : un déploiement en quelques millisecondes des agents activés sur des workers pré-chauffés, à la demande, sans délai de démarrage de conteneur.
- **Une forte efficacité** : les acteurs inactifs sont suspendus et désordonnancés en quelques centaines de millisecondes, libérant des ressources de calcul.
- **Open source et portable** : fonctionne sur n'importe quel cluster Kubernetes, dans n'importe quel environnement de calcul, et avec n'importe quel framework ou harnais d'agents, y compris Claude Code, OpenClaw et Hermes.

### Principes architecturaux fondamentaux
Quatre principes architecturaux guident la façon dont Agent Substrate répond à ces défis.

#### 1. Sécurisé par défaut au niveau du noyau et du réseau
Les agents IA génèrent et exécutent du code et des commandes terminal non fiables, c'est une fonction centrale de leur activité. Exécuter ce code sur un serveur partagé crée des risques sérieux d'évasion et de fuite de données non intentionnelle, au niveau du noyau partagé ou du réseau.

Agent Substrate adopte une posture sécurisée par défaut, à la fois pour la couche hôte/noyau et pour la couche réseau. Les équipes peuvent choisir entre des microVM Cloud Hypervisor isolées matériellement, offrant une compatibilité complète avec le noyau Linux, ou un sandboxing gVisor, avec une isolation noyau à overhead encore plus faible. La passerelle intégrée d'Agent Substrate gère toutes les requêtes entrantes et sortantes, permettant un contrôle fin et extensible de l'accès réseau.

#### 2. Un plan de contrôle et un plan de données conçus pour une activation à faible latence
Pour optimiser la densité de charges de travail d'agents isolées et de longue durée, il faut un plan de contrôle et un plan de données conçus sur mesure pour permettre la latence la plus faible possible et le taux le plus élevé possible d'opérations de suspend/resume. Agent Substrate introduit un plan de contrôle dédié qui gère un ordonnancement conscient des données avec une latence minimale. Le plan de données, lui, gère des centaines d'opérations de suspend/resume par seconde directement sur des workers pré-chauffés, réduisant l'overhead de préparation de l'environnement. Les snapshots sont écrits sur disque local et sur Google Cloud Storage pour une persistance durable de l'état. En moins de 500 ms, un environnement sandboxé peut être repris dans son état précédent, puis immédiatement re-suspendu une fois redevenu inactif.

#### 3. Une économie de calcul à haute densité et « actif uniquement »
Les agents passent la majeure partie de leur temps à attendre une inférence de modèle, une réponse d'outil ou une entrée utilisateur. Réserver des CPU physiques et de la RAM pour des conteneurs inactifs peut immobiliser une capacité coûteuse et rare, rendant l'exécution de flottes d'agents à grande échelle intenable.

Agent Substrate libère les ressources dès qu'un agent se met en pause. Il capture l'état de l'hyperviseur invité sur le disque local et sur Cloud Storage, libérant RAM et CPU pour faire tourner d'autres agents, tout en gardant l'état intact. Quand le tour suivant ou un appel d'outil arrive, Agent Substrate reprend la session capturée en quelques millisecondes. Ce modèle « zéro inactivité » permet d'empiler plus de 1000 agents dormants par machine hôte, soit une densité de calcul 10 fois supérieure au calcul traditionnel. Pour les charges de travail nécessitant des systèmes de fichiers partagés entre les tours, un contrôleur de volumes d'agents Filestore optionnel fournit un stockage NFS persistant — détaillé plus bas.

#### 4. Kubernetes comme fondation : échelle et fiabilité
Construire un orchestrateur de sandboxes sur mesure au-dessus de VM standards oblige les équipes à maintenir un outillage opérationnel fastidieux : reprise après panne des nœuds, autoscaling, ordonnancement multi-zone et politiques réseau. Mais faire passer chaque invocation d'outil, de l'ordre de la sous-seconde, par le cycle de vie standard d'un Pod Kubernetes ajoute des secondes de délai à chaque requête.

Agent Substrate combine les deux approches. Le cycle suspend-resume à haute fréquence tourne directement sur les workers locaux via un plan de données conçu sur mesure. Pendant ce temps, Kubernetes gère les machines : nœuds auto-réparants, autoscaling de la flotte, fiabilité du cluster, ainsi que le cycle de vie des pods workers eux-mêmes. Pour les charges de travail nécessitant une sémantique Pod standard, les primitives existantes comme Agent Sandbox et les Pods isolés au niveau noyau continuent de fonctionner en parallèle.

### Optimisé pour l'infrastructure Google Cloud
Construire une plateforme d'agents capable d'atteindre l'échelle du million d'agents dépend de disposer de la bonne infrastructure de calcul et de stockage sous-jacente. Agent Substrate sur GKE maximise l'accessibilité et la flexibilité des machines grâce à des ComputeClasses personnalisées qui gèrent dynamiquement des pools de machines selon les formats et familles, y compris des pools spot et à la demande. Cela inclut un support natif de Google Axion, les processeurs Arm personnalisés de Google, qui offrent jusqu'à 30 % de meilleur rapport prix/performance pour les charges de travail de sandboxing par rapport aux offres cloud concurrentes. Pour les espaces de travail à état, Agent Substrate sur GKE peut être intégré de façon optionnelle aux volumes d'agents Filestore, une nouvelle offre qui attache et détache les montages NFS en quelques millisecondes, permettant aux agents de démarrer/reprendre quasi instantanément, avec un accès natif Read-Write-Many (RWX) et un verrouillage de fichiers conforme POSIX pour permettre une collaboration multi-agents sûre sans collisions d'écriture.

### Construire sa plateforme d'agents sur une fondation scalable
Lors de la construction d'applications d'agents en production, on ne devrait pas avoir à choisir entre sécurité forte, faible latence et échelle opérationnelle.

Nous Research construit Hermes, l'agent IA numéro un au monde en usage selon OpenRouter, où il se classe également premier dans les catégories productivité, développement, agents personnels et CLI. Nous Research a été un partenaire de conception précoce sur Agent Substrate, évaluant comment le runtime gère les exigences d'isolation et d'identité qu'introduisent les charges de travail d'agents.

« Nous avons construit Hermes Enterprise pour permettre à nos clients de le déployer dans leur infrastructure existante, tout en gérant l'isolation par agent et un contrôle d'accès extensible. Agent Substrate répond aux deux enjeux au niveau de la plateforme, tout en préservant des ressources de calcul précieuses. Notre expérience avec Agent Substrate nous donne confiance dans le fait que cette architecture peut monter en charge efficacement à mesure que les charges de travail d'agents grandissent. » — Hervé Bizira, Chief Business Officer, Nous Research

En associant la résilience des machines, les nœuds auto-réparants et la gestion déclarative de Kubernetes à un plan de données natif pour les agents, conçu pour l'isolation noyau, le calcul « actif uniquement » et l'exécution en moins d'une seconde, Agent Substrate offre aux équipes d'ingénierie une voie claire vers la mise à l'échelle.

Agent Substrate est open source et disponible pour tous les clients GKE pour des charges de travail non-production. Le support GA pour la production est disponible sur liste d'autorisation (allowlist). Pour le déployer sur des clusters GKE, Google renvoie vers la documentation d'Agent Substrate sur GKE, et pour en savoir plus, vers la page « About Agent Substrate » ou le dépôt open source.

## Pourquoi ça compte
Ce lancement illustre la bascule de l'infrastructure cloud vers des primitives natives pour les agents IA autonomes (isolation, densité, activation quasi instantanée), un terrain de compétition clé entre Google, AWS et Microsoft alors que les flottes d'agents passent du prototype à la production à très grande échelle.
