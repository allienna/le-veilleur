---
title: "Seamless graph intelligence for your Snowflake data estate: The Neo4j and Snowflake partnership - Neo4j Graph Intelligence Platform"
date: 2026-11-06
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fneo4j.com%2Fblog%2Fknowledge-graph%2Fgraph-intelligence-for-your-snowflake-data-estate%2F%3Futm_source=tldrit/1/010001a1ac00e250-2ace9b34-60b7-477f-bc75-94dc55db97c2-000000/NrIShlnqEO4GLCWiIJpCL11sw_dDBTvHizdYVT8ReKE=452"
keywords: ["knowledge graph", "Snowflake", "Neo4j", "LLM", "agents IA", "graph analytics"]
theme: "Data"
tone: "news"
used_in: ["2026-11-06"]
---

## Résumé
Neo4j et Snowflake annoncent un partenariat approfondi pour apporter l'intelligence des graphes directement dans l'AI Data Cloud de Snowflake, via trois briques complémentaires : Virtual Graph (requêtes Cypher sur les données Snowflake sans aucun déplacement), Graph Analytics for Snowflake (plus de 65 algorithmes de graphes exécutés en SQL, en mode serverless) et AuraDB pour les cas d'usage temps réel nécessitant une latence milliseconde et des transactions ACID. L'objectif affiché est de fournir aux LLM et aux agents IA un contexte métier connecté, Neo4j citant une étude IDC selon laquelle cela réduirait les hallucinations des LLM de 44 % et générerait un ROI de 230 %. Le cas client Audience Acuity illustre des gains concrets, avec une résolution d'identité sur plus de 2 milliards de signaux de données accélérée de plusieurs semaines à moins de 24 heures.

## Points clés
- Trois offres intégrées : Virtual Graph (Public Preview, GA prévue le 16 novembre 2026), Graph Analytics for Snowflake (déjà disponible sur le Marketplace) et AuraDB (temps réel).
- Virtual Graph traduit les requêtes Cypher en SQL déterministe exécuté directement sur Snowflake, sans déplacer les données ni casser la gouvernance existante.
- Graph Analytics for Snowflake est une application serverless facturée à l'usage, avec plus de 65 algorithmes de graphes disponibles en SQL.
- Argument central du partenariat : contextualiser les LLM/agents avec des knowledge graphs réduirait les hallucinations (-44 %) et améliorerait le ROI (+230 % selon une étude IDC commanditée par Neo4j).
- Cas client cité : Audience Acuity a réduit son temps de résolution d'identité sur 2 Md+ de signaux de plusieurs semaines à moins de 24 heures.
- Virtual Graph est désormais accessible à plus de 12 000 organisations clientes de Snowflake via la Aura Console.

## Analyse approfondie
Les fournisseurs d'entrepôts de données modernes comme Snowflake offrent une plateforme consolidée pour l'écosystème de données et d'IA d'une organisation. Les grands modèles de langage (LLM) offrent des capacités évolutives extraordinaires dans les interactions homme-IT. Pourtant, l'analytique traditionnelle et les recherches vectorielles seules échouent souvent à mettre en lumière les relations profondes et complexes cachées au sein des données de l'entreprise. Cela ralentit la prise de décision et limite la valeur des actifs de données existants. Cela peut également provoquer des erreurs critiques pour les applications d'IA générative. Pour résoudre ce problème, Neo4j et Snowflake se sont associés afin d'apporter un contexte d'entreprise à l'AI Data Cloud de Snowflake. Ce partenariat permet aux organisations d'obtenir des insights plus profonds, de stimuler l'innovation et d'établir un nouveau standard de prise de décision intelligente, sans les processus ETL laborieux et chronophages.

Cependant, une solution unique ne convient jamais à tous les cas. Nos efforts de co-développement visent à apporter aux utilisateurs les capacités d'intelligence des graphes de Neo4j dont ils ont besoin pour leur data estate Snowflake, avec des options de déploiement adaptées à différents cas d'usage. Le portefeuille intégré comprend Virtual Graph, Graph Analytics for Snowflake, et l'Aura Data Importer for Snowflake.

### Construire des knowledge graphs sans déplacer les données Snowflake grâce à Virtual Graph
*Construisez et interrogez des knowledge graphs directement sur les données Snowflake sans aucun déplacement de données – traduisez automatiquement Cypher en SQL, préservez la gouvernance existante et accélérez le raisonnement de l'IA.*

Virtual Graph for Snowflake, actuellement en Public Preview avec une disponibilité générale (GA) prévue pour le 16 novembre, permet aux utilisateurs de construire un knowledge graph sur les données Snowflake d'une organisation, leur permettant d'exécuter des requêtes Cypher sur les données de l'entrepôt de données sans aucun déplacement de données. Virtual Graph traduit les requêtes Cypher en instructions SQL déterministes qui sont poussées vers un entrepôt de données Snowflake, puis renvoie les résultats (et non les données) sous forme de graphe pour exploration et utilisation dans Bloom et Query, par les Aura Agents, et plus encore. Cypher est conforme à GQL, ce qui rassure les organisations exigeant des standards robustes pour les langages de requête.

Cela apporte la puissance des outils de graphes pilotés par l'IA de Neo4j au cœur relationnel des données d'une organisation, en s'appuyant sur les règles de gouvernance des données existantes et sur la plateforme de calcul dans laquelle elle a déjà investi. Virtual Graph propose une conception de schéma de graphe assistée par IA à partir des données Snowflake existantes. Les utilisateurs peuvent générer instantanément leur premier modèle de graphe et adopter un knowledge graph opérationnel en quelques minutes (et non en semaines), accélérant ainsi le temps nécessaire pour créer de la valeur métier. Avec Cypher dans leur boîte à outils, les utilisateurs peuvent élaborer des requêtes pour poser des questions sur des données connectées telles que : « si l'entrepôt X à Houston ferme à cause d'une tempête, quelles commandes en attente doivent être réacheminées, via quels hubs secondaires, pour respecter les délais de livraison garantis ? » ou « quels résultats cliniques ont été obtenus chez des patients présentant des mutations génétiques, des profils d'âge et des comorbidités similaires lorsqu'ils ont reçu le Traitement A par rapport au Traitement B ? ». Les utilisateurs qui ne maîtrisent pas Cypher peuvent utiliser le Copilot piloté par l'IA pour traduire le langage naturel en requêtes de graphe.

Au-delà des cas d'usage classiques et éprouvés des knowledge graphs, tels que la vision 360° client/produit, la gestion de la chaîne d'approvisionnement, la prévention de la fraude et la recherche médicale, la croissance exponentielle des agents et des outils agentiques sur le marché accélère l'adoption de cas d'usage transversaux des graphes, capables d'améliorer les résultats des agents. Les LLM offrent une vaste étendue de connaissances et des capacités impressionnantes de génération de contenu multimodal, mais leur manque de contexte et de compréhension spécifiques à l'entreprise peut limiter leur utilité et, par conséquent, leur adoption à grande échelle.

Des recherches récentes¹ ont montré que les organisations utilisant Neo4j pour apporter un contexte métier connecté à leurs ensembles de données d'entreprise peuvent « améliorer la précision du raisonnement des LLM, fournir des résultats plus cohérents et explicables, et réduire les hallucinations des LLM de 44 % ».² La capacité à visualiser les connexions (entre applications, définitions de métriques, départements, et les autres éléments d'histoire et nuances qui rendent une entreprise unique) ancre les LLM dans des résultats optimisés et propres à l'organisation. Jesús Barrera, AI Field CTO chez Neo4j, a partagé sa vision éclairante ainsi qu'un décryptage utile des termes associés dans son article de blog, *The knowledge layer for enterprise AI*. Virtual Graph for Snowflake permet aux entreprises de construire la couche de connaissance essentielle au raisonnement de l'IA, en opérant directement au sein de leur infrastructure Snowflake existante, avec un temps de mise en valeur minimal.

### Découvrir de nouveaux schémas dans les données Snowflake avec Graph Analytics for Snowflake
*Exécutez des analyses de graphes à la demande avec SQL — créez des graphes en mémoire à partir des tables Snowflake, appliquez des algorithmes, et réécrivez les résultats pour une utilisation en aval, le tout entièrement contenu dans Snowflake.*

Graph Analytics for Snowflake, disponible dès aujourd'hui via le Snowflake Marketplace, aide les entreprises à découvrir de nouveaux schémas dans leurs données sans ETL, en utilisant uniquement du SQL et du calcul élastique, tout en restant dans le cadre de gouvernance de leur Snowflake AI Data Cloud. Les utilisateurs peuvent exploiter les plus de 65 algorithmes de graphes de Neo4j pour en extraire des insights plus profonds, là où les données résident. L'application serverless, entièrement managée, démarre à la demande pour exécuter des algorithmes de graphes en mémoire via SQL, réécrit les résultats dans des tables Snowflake, puis s'arrête à nouveau.

Avec Graph Analytics for Snowflake, les utilisateurs ne sont facturés que pour les ressources qu'ils consomment, sans minimum mensuel ni frais d'inactivité. Les utilisateurs métier peuvent combiner Snowflake Cortex AI et le contexte de graphe de Neo4j pour poser des questions en langage naturel et obtenir des réponses tenant compte des relations. Graph Analytics for Snowflake offre le temps de valorisation le plus rapide pour les utilisateurs souhaitant extraire des insights de l'ensemble de leur data estate Snowflake sans ETL coûteux et chronophage. Les principaux cas d'usage incluent l'optimisation de la chaîne d'approvisionnement (« quel est l'itinéraire le plus optimal à travers un réseau logistique ? »), la détection de fraude en communauté (« existe-t-il des groupes d'acteurs malveillants partageant des identifiants ? »), la résolution d'entités pour le marketing (« identifier les utilisateurs uniques à travers tous nos canaux clients pour des campagnes plus efficaces »), et la segmentation client/next best action (« que dois-je recommander ensuite à ce client ? »).

### Passer à AuraDB pour les cas d'usage en temps réel
*Déployez des bases de données de graphes natives avec une latence de l'ordre de la milliseconde et une conformité ACID pour alimenter des applications critiques en temps réel.*

Certaines charges de travail — celles qui nécessitent une latence de l'ordre de la milliseconde, des opérations CRUD, des transactions ACID, ou des requêtes croisant plusieurs sources de données — restent mieux servies par une base de données de graphes native Neo4j, disponible via AuraDB (le service de base de données de graphes entièrement managé de Neo4j) ou via notre offre autogérée. Pour soutenir la prise de décision en temps réel dans des cas d'usage tels que l'analyse des cybermenaces, les recommandations de type « prochaine meilleure action », l'analyse des causes profondes réseau et IT, et la détection de fraude en direct, les utilisateurs peuvent migrer des points chauds (« sous-graphes ») vers une base de données Neo4j. Le service d'import de Neo4j Aura prend en charge Snowflake comme source de données, facilitant la migration de jeux de données transactionnels à forte concurrence vers une base de données de graphes native Neo4j.

### L'intelligence des graphes en action
L'extension des capacités de graphes au sein du Snowflake Data Cloud constitue une étape importante pour notre partenariat. Des organisations utilisent déjà Neo4j Graph Analytics for Snowflake pour transformer de nouveaux insights issus des données en résultats business concrets. Par exemple, Audience Acuity a accéléré la résolution d'identité sur plus de 2 milliards de signaux de données interconnectés au sein de son data estate Snowflake, réduisant le temps de traitement de plusieurs semaines à moins de 24 heures.³ Désormais, Virtual Graph for Snowflake permet d'interroger sur place les données Snowflake sous forme de graphe, et ce pour plus de 12 000 organisations,⁴ ouvrant de nouvelles possibilités pour le raisonnement de l'IA en entreprise.

### Explorer comment la technologie Neo4j complète votre data estate Snowflake
Virtual Graph for Snowflake est désormais disponible dans la Aura Console. Connectez un entrepôt de données Snowflake, générez un modèle, et exécutez votre première requête Cypher en quelques minutes. Le récent article de blog pour développeurs de Ben Lackey fournit un guide pas à pas.

Graph Analytics for Snowflake est disponible dès aujourd'hui sur le Snowflake Marketplace. L'article de blog pour développeurs de Prash Medirattaa illustre le processus.

AuraDB, la base de données de graphes entièrement managée de Neo4j, fonctionne sur AWS, Azure et Google Cloud. Lancez-vous gratuitement dès aujourd'hui !

#### En savoir plus
- Documentation Public Preview de Virtual Graph for Snowflake
- Atelier Neo4j Graph Academy : Neo4j Virtual Graph with Snowflake
- Article de blog *Zero-Copy Graph Reasoning on Snowflake: Getting Started With Neo4j Virtual Graph*
- Manuel utilisateur de Graph Analytics for Snowflake
- Article de blog développeur *Identify Bottlenecks and Model Disruptions using Neo4j Graph Analytics*
- Documentation d'AuraDB
- Article de blog *Getting Started with Neo4j Aura*

1. Livre blanc IDC, *The Business Value of the Neo4j Graph Intelligence Platform*, mai 2026.
2. *New research finds enterprises earn 230% ROI with Neo4j Graph Intelligence Platform*, mai 2026.
3. *Audience Acuity Accelerates Identity Resolution to Under 24 Hours with Neo4j Graph Analytics for Snowflake*.
4. *About Snowflake*, 2026.

## Pourquoi ça compte
Ce partenariat illustre la convergence entre entrepôts de données cloud et knowledge graphs comme réponse au besoin de contexte fiable pour les LLM et les agents IA en entreprise — un signal à suivre pour quiconque évalue des architectures RAG ou agentic au-delà de la simple recherche vectorielle.
