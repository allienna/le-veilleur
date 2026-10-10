---
title: "Bringing local models and sandboxed tools to Windows and GitHub Copilot"
date: 2026-10-10
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fcommandline.microsoft.com%2Flocal-models-sandboxed-tools-github-windows%2F%3Futm_source=tldrit/1/010001a1209bd94c-50b00a8e-1fd5-41f6-bd14-0faf19701108-000000/wWhfcvK1dnP-fGxQTnskxC4B3-6R3NLATDugrG3KPjQ=452"
keywords: ["GitHub Copilot", "modèles locaux", "sandboxing", "MAI Code 1.1 Flash", "inférence edge", "Windows"]
theme: "IA"
tone: "news"
used_in: ["2026-10-10"]
---

## Résumé
Microsoft et GitHub annoncent l'arrivée de modèles d'IA locaux et d'outils « sandboxés » (isolés) dans GitHub Copilot sous Windows, avec un objectif : laisser les développeurs choisir entre inférence sur l'appareil et inférence cloud selon la tâche, tout en sécurisant l'exécution des agents. Un nouveau modèle propriétaire optimisé pour le code, MAI Code 1.1 Flash, est quantifié pour tourner localement sur du matériel comme le Surface Laptop Ultra (NVIDIA RTX Spark), avec des performances proches de sa version cloud complète. L'isolation des commandes shell et des serveurs MCP locaux repose sur Microsoft Execution Containers (MXC), une bibliothèque open-source qui traduit des politiques de sécurité en contrôles natifs du système d'exploitation. L'article illustre le tout avec un exemple concret : un agent local, sandboxé, qui génère chaque matin un tableau de bord HTML à partir des dépôts GitHub.

## Points clés
- GitHub Copilot va orchestrer automatiquement (« Auto ») le choix entre modèles locaux et modèles cloud selon la tâche, via une logique héritée du projet HydraFusion ; un choix manuel du modèle local reste possible.
- Le nouveau modèle MAI Code 1.1 Flash est un mixture-of-experts de 137 milliards de paramètres au total (6,8 milliards actifs), quantifié à environ 3,3 bits par poids pour une empreinte de 53 Go (soit une réduction de 80 % par rapport à la version Bfloat16 cloud).
- Sur le Surface Laptop Ultra, le pic de mémoire atteint 75,5 Go à un contexte de 256k tokens, avec un débit de traitement de prompt de 923,5 tokens/s à 64k et 769,8 tokens/s à 128k de contexte.
- Sur les benchmarks cités, la version locale quantifiée reste proche de la version cloud (SWE-Bench Verified : 70,8 % contre 72,6 % ; Terminal-Bench 2.1 : 66,29 % contre 62,9 %) et dépasse largement GPT-OSS-120B (32,0 % et 23,6 % respectivement).
- La sécurité des agents repose sur MXC : BaseContainer (ProcessContainer) sous Windows, Seatbelt sous macOS, bubblewrap sous Linux — ces sandboxes locales contrôlent l'accès aux fichiers, réseau, identifiants et capacités système, configurables via la commande `/sandbox` du CLI Copilot.
- Un exemple d'automatisation quotidienne (génération d'un tableau de bord de triage pour un dépôt) montre comment combiner modèle local, sandboxing et accès restreint en lecture/écriture pour sécuriser une tâche agentique récurrente.

## Analyse approfondie
Lorsqu'ils s'appuient sur des agents, les développeurs ont besoin à la fois de choix et de contrôle. Ils ont besoin de technologies offrant des limites claires pour leurs agents et permettant de choisir facilement le modèle au bon profil de vitesse, de performance et de coût pour chaque tâche. C'est pourquoi GitHub propose des modèles de pointe issus des principaux fournisseurs, ainsi que des options comme Project HydraFusion, un orchestrateur qui choisit un ou plusieurs modèles pour chaque tâche en équilibrant performance, coût et latence. C'est aussi pourquoi Windows a développé Microsoft Execution Containers (MXC), pour aider à sécuriser les sessions de codage agentiques, interactives ou non.

D'ici la fin du mois, GitHub Copilot déterminera quand une tâche est mieux traitée par de l'intelligence embarquée sur l'appareil et quand elle doit s'appuyer sur des modèles à l'échelle du cloud. Plutôt que de forcer les développeurs à gérer eux-mêmes ces décisions d'infrastructure, GitHub Copilot coordonne automatiquement l'inférence locale et cloud en coulisses. Pour les PC Windows équipés de NVIDIA RTX Spark, comme le Surface Laptop Ultra, cela signifie que le codage local dans GitHub Copilot est activé grâce à des modèles d'inférence locale puissants et un matériel capable d'offrir une excellente expérience en périphérie (« edge »).

Le résultat s'annonce comme la prochaine étape de la vision HydraFusion : une orchestration intelligente qui s'étend non seulement à plusieurs modèles, mais aussi à plusieurs environnements de calcul, y compris en périphérie. GitHub Copilot peut exécuter des commandes dans ces environnements avec un accès contrôlé aux fichiers, réseaux, capacités système et identifiants. Les développeurs peuvent ainsi automatiser en toute confiance, dans un esprit de sécurité.

### Pourquoi la mémoire compte pour un agent de codage local
L'inférence locale commence par un budget mémoire. Le Surface Laptop Ultra est construit autour du NVIDIA RTX Spark, avec jusqu'à 128 Go de mémoire unifiée et jusqu'à 1 pétaflop de calcul IA.

Avec un GPU dédié, la mémoire vidéo dédiée est une contrainte importante : déplacer les données du modèle entre la mémoire système et le GPU peut ajouter de la surcharge. La mémoire unifiée donne au CPU et au GPU un accès à un même pool physique partagé. Cela rend plus de capacité disponible pour la charge de travail, mais ne rend pas pour autant toute cette capacité disponible pour les poids du modèle.

Le système d'exploitation, les applications et le runtime d'inférence ont eux aussi besoin de mémoire. C'est aussi le cas du cache clé-valeur, qui stocke l'état d'attention pour les tokens déjà traités par le modèle. Lorsqu'un agent lit des fichiers et reçoit des résultats d'outils, son contexte peut croître, augmentant l'utilisation mémoire et le travail nécessaire pour traiter la requête suivante.

Garder un modèle chargé entre les requêtes permet d'éviter un travail de chargement répété. Cependant, cela ne garantit pas un temps de réponse constant : la longueur du contexte, la pression mémoire et le reste de la charge de travail comptent toujours. C'est pourquoi la question utile n'est pas seulement de savoir si un modèle « rentre », mais comment il se comporte sur une tâche de codage complète.

### Présentation de MAI Code 1.1 Flash pour le codage local
Pour donner vie à cette expérience de développement local, Microsoft AI a développé une version locale de MAI Code 1.1 Flash, un modèle de type mixture-of-experts optimisé pour le code, comptant 137 milliards de paramètres au total et 6,8 milliards de paramètres actifs. Le travail sur l'appareil applique de la quantification et du décodage spéculatif pour réduire l'empreinte du modèle et améliorer la réactivité de bout en bout, tout en préservant la qualité d'exécution des tâches et d'utilisation des outils essentielle dans une boucle d'agent.

La quantification réduit la précision utilisée pour représenter les poids et activations du modèle, abaissant les besoins en mémoire. Comme le code ne se dégrade pas « gracieusement », l'évaluation de la publication doit mesurer à la fois le succès des tâches de codage et l'empreinte : un seul token incorrect peut produire une erreur de syntaxe, un mauvais identifiant, un appel d'outil malformé ou un diff cassé.

Le décodage spéculatif échange de la mémoire de travail supplémentaire contre un débit de décodage plus élevé et une latence de bout en bout plus faible. Un modèle « brouillon » (drafter) propose des blocs de tokens candidats, que le modèle cible vérifie ensuite.

Pour un agent de codage, l'arbitrage important est de savoir si le modèle plus petit peut toujours accomplir les mêmes tâches. Une empreinte plus petite n'est utile que si l'on comprend les changements en matière de qualité du code et d'utilisation des outils.

Avec notre première version de MAI Code 1.1 Flash livrée sur le Surface Laptop Ultra, nous atteignons les performances suivantes à différentes longueurs de contexte, avec une utilisation mémoire de pointe de 75,5 Go à 256k de contexte. À 64k et 128k de contexte, le débit de traitement des prompts atteint respectivement 923,5 et 769,8 tokens par seconde.

La version quantifiée de MAI Code 1.1 Flash utilisée sur l'appareil conserve une capacité impressionnante comparée à la variante cloud Bfloat16, pour une taille de 53 Go, soit une réduction de 80 %.

| **Benchmark** | **Taille du jeu de données** | **MAI Code 1.1 Flash** | **GPT OSS 120B\*** | **MAI Code 1.1 Flash quantifié sur l'appareil** |
|---|---|---|---|---|
| SWE-Bench Verified | 500 | 72,6 % | 32,0 % | 70,80 % |
| Terminal-Bench 2.1 | 89 | 62,9 % | 23,6 % | 66,29 % |

*La version GPT OSS utilisée pour comparaison était le GGUF GPT-OSS-120B d'Unsloth. Tests réalisés le 5 octobre 2026 avec MAI Code 1.1 Flash (quantification en précision mixte, environ 3,3 bits par poids) utilisant le décodage spéculatif par fenêtre glissante DFlash2 et un runtime llama.cpp CUDA pour Windows ARM64. Les résultats reflètent le débit de décodage pour une charge de travail synthétique de génération de code ; les résultats réels peuvent varier selon l'appareil, la configuration et d'autres facteurs.

### Deux façons d'utiliser des modèles locaux dans GitHub Copilot
GitHub Copilot ajoute deux façons d'utiliser des modèles locaux dans le CLI GitHub Copilot, l'application Copilot et VS Code. Les développeurs peuvent laisser l'orchestration intelligente « Auto » de Copilot choisir quand utiliser l'inférence locale ou cloud, ou sélectionner explicitement un modèle local pour les flux de travail nécessitant un contrôle direct.

Avec Auto, les développeurs n'ont pas besoin de décider où chaque tâche doit s'exécuter. Au fil d'une session multi-tours, Copilot peut tenir compte du contexte de la tâche et de l'état du cache pour router le travail entre modèles locaux et cloud, en préservant le travail mis en cache utile à mesure que la session évolue.

Cette expérience orchestrée complète la sélection directe de modèle, offrant aux développeurs le choix entre laisser Copilot optimiser le placement du modèle ou choisir eux-mêmes un modèle local spécifique.

La sélection explicite de modèle local prend en charge les flux de travail nécessitant un fournisseur, un modèle ou un point de terminaison spécifique. Les développeurs peuvent sélectionner MAI Code 1.1 Flash via le fournisseur Windows ML, ou connecter GitHub Copilot à des points de terminaison locaux compatibles OpenAI et choisir parmi les modèles que ces points de terminaison exposent.

### Comment les sandboxes aident à sécuriser l'exécution des outils
Les commandes shell d'un agent héritent normalement des droits du compte qui les exécute. Déplacer l'inférence sur l'appareil ne change rien à cela. Le sandboxing applique une politique aux processus et services locaux que l'agent lance, contrôlant l'accès aux fichiers, réseaux, identifiants, capacités système et chemins d'exécution, quel que soit le modèle à l'origine de la demande.

GitHub Copilot utilise Microsoft Execution Containers, ou MXC, une bibliothèque open-source de l'équipe Windows qui traduit la politique en contrôles natifs du système d'exploitation. Sous Windows, GitHub Copilot utilise le niveau BaseContainer du backend ProcessContainer. Sous macOS, il utilise Seatbelt. Sous Linux, il utilise bubblewrap. Ces backends locaux ne nécessitent pas de machine virtuelle ou d'image de conteneur séparée, mais nous prévoyons de proposer ces options via MXC à l'avenir.

Lorsque le sandboxing est activé, les commandes shell et, par défaut, les serveurs Model Context Protocol (MCP) locaux ainsi que les serveurs de langage s'exécutent à l'intérieur de la limite de processus. Les outils de fichiers intégrés s'exécutent au sein de GitHub Copilot lui-même : le harnais de l'agent vérifie leurs requêtes par rapport à la politique effective, mais ces vérifications ne constituent pas une isolation de processus enfant imposée par l'OS. Les serveurs MCP distants sont eux aussi en dehors du sandbox de processus local ; lorsque les contrôles de sandbox MCP s'appliquent, GitHub Copilot vérifie leur politique de connexion « in process ».

Ouvrir le CLI GitHub Copilot et exécuter la commande slash `/sandbox` permet de configurer ces paramètres à tout moment.

### Un exemple concret : tableau de bord quotidien de dépôt
Pour montrer comment ces technologies fonctionnent ensemble, prenons un exemple concret.

Considérons une tâche qui lit des dépôts locaux, exécute leurs tests dans des copies de travail, et écrit un rapport HTML chaque matin. Les dépôts sources doivent rester en lecture seule, et les processus de test ne doivent pas accéder au réseau. Le choix du modèle est indépendant : la même tâche peut utiliser un modèle local ou cloud configuré.

**Activer le sandboxing pour votre projet**
Ouvrez la boîte de dialogue des paramètres en cliquant sur l'icône d'engrenage dans l'application GitHub Copilot et en sélectionnant votre projet dans le menu de gauche. Pour cet exemple, nous utilisons le dépôt `copilot-sdk`, qui héberge notre projet open-source GitHub Copilot Runtime/SDK.

Activer le bouton `Sandbox new sessions` active le sandboxing par défaut chaque fois que vous travaillez au sein de ce projet. Par défaut, le répertoire de travail courant est en lecture/écriture tandis que le reste du système reste largement en lecture seule ou inaccessible à un agent.

**Créer une nouvelle automatisation**
Sélectionnez la section `Automations` dans la navigation de gauche et cliquez sur le bouton `Start automation` pour ouvrir la boîte de dialogue permettant de configurer une nouvelle automatisation.

Après avoir défini un titre clair et une heure de déclenchement de 9h quotidiennement, collez des instructions de base pour guider l'agent dans la création d'un tableau de bord quotidien de triage.

« Créer le tableau de bord de triage public du jour pour github/copilot-sdk en utilisant uniquement les métadonnées des issues et PR GitHub (sans dépôts locaux, code, tests ou liens hors dépôt), en résumant les éléments ouverts/fermés/fusionnés, les travaux récemment mis à jour, les éléments obsolètes, les labels, auteurs, assignés et l'ancienneté ; générer .\dashboard\index.html avec du CSS et SVG en ligne, ajouter les résultats du jour à .\history.json pour un maximum de sept dates, et terminer par exactement trois lignes : chemin du rapport, échecs, et travail ignoré ou indisponible. »

En sélectionnant le nouveau modèle local MAI Code 1.1 Flash et le dépôt `copilot-sdk` sur lequel le sandboxing a été activé, l'agent peut travailler hors-ligne avec des garde-fous aidant à limiter les changements non voulus sur votre machine locale — tout en permettant à l'agent de générer et d'exécuter des scripts dans son répertoire de travail courant pour trier et créer un tableau de bord interactif.

Après l'enregistrement, cliquer sur `Run it now` lance immédiatement l'exécution de la nouvelle automatisation pour vérification.

**Inspecter le résultat**
Une fois que l'agent GitHub Copilot a terminé la tâche, vous pouvez ouvrir les artefacts de la session pour visualiser une copie générée du tableau de bord, qui sera rafraîchi quotidiennement. Le tout réalisé localement, avec des sandboxes offrant une protection de base contre les changements système non désirés pendant qu'il génère et exécute des scripts pour accomplir la tâche.

### Conclusion
Ce n'est que le début de ce parcours. Les modèles locaux et les outils sandboxés se déploient dès maintenant pour donner aux développeurs davantage de choix sur l'endroit où s'exécute l'intelligence, et un contrôle plus clair sur ce que les agents sont autorisés à faire.

### Remerciements
L'article liste de nombreux contributeurs aux équipes Produit, Ingénierie, Science et Marketing ayant travaillé sur ce projet chez Microsoft et GitHub, en précisant que la liste n'est pas exhaustive.

## Pourquoi ça compte
Ce lancement illustre une tendance de fond : l'inférence IA en périphérie (edge) devient suffisamment performante pour des tâches de codage complexes, et la sécurisation des agents (sandboxing systématique des commandes et serveurs MCP) devient un standard attendu plutôt qu'une option. À suivre pour toute veille sur l'évolution des assistants de codage agentiques et sur la montée en puissance du matériel IA local (NPU, mémoire unifiée) face aux API cloud.
