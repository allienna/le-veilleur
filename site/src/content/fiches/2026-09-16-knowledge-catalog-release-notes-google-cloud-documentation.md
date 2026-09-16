---
title: "Knowledge Catalog release notes | Google Cloud Documentation"
date: 2026-09-16
url: "https://docs.cloud.google.com/dataplex/docs/release-notes#September_07_2026"
keywords: ["catalogue de métadonnées", "gouvernance des données", "data lineage", "Google Cloud", "IA générative", "MCP"]
theme: "Data"
tone: "news"
used_in: ["2026-09-16"]
---

## Résumé
Cette page de notes de version documente l'évolution du produit Google Cloud « Knowledge Catalog » (anciennement Dataplex Catalog puis Dataplex Universal Catalog) entre 2022 et septembre 2026. Elle retrace une trajectoire claire : d'un simple catalogue de métadonnées vers une plateforme complète de gouvernance des données pilotée par l'IA, intégrant Gemini pour générer des insights, un serveur MCP distant pour connecter des agents IA, ainsi que des fonctionnalités avancées de data lineage, de data quality et de « data products ». Le produit a connu plusieurs renommages successifs (Dataplex Catalog → BigQuery universal catalog → Dataplex Universal Catalog → Knowledge Catalog), reflétant une consolidation stratégique avec BigQuery, BigLake (devenu Google Cloud Lakehouse) et Dataproc (devenu Managed Service for Apache Spark). En parallèle, l'ancien service concurrent Data Catalog est en cours d'arrêt progressif depuis juin 2026.

## Points clés
- Renommages en cascade en 2025-2026 : Dataplex Catalog → BigQuery universal catalog (avril 2025) → Dataplex Universal Catalog → Knowledge Catalog (avril 2026) ; BigLake → Google Cloud Lakehouse ; Dataproc + Serverless Spark → Managed Service for Apache Spark ; Cloud Composer → Managed Service for Apache Airflow.
- Intégration croissante de l'IA générative : Gemini alimente les « data insights » (génération automatique de requêtes, de documentation et d'insights métier) et l'extraction d'informations sémantiques à partir de données non structurées (PDF, etc.) ; un serveur MCP distant permet aux agents IA d'interroger le lineage et les data products.
- Montée en puissance de la gouvernance : les « data products » passent en disponibilité générale (mai 2026) avec workflows d'approbation d'accès, des workflows de gouvernance automatisés avec mécanisme de demande-revue (juillet 2026), et des « data domains » pour organiser les ressources à l'échelle de l'entreprise (preview, septembre 2026).
- Extension du data lineage : passage du niveau table au niveau colonne (GA en 2025), nouvelle méthode de recherche en largeur (breadth-first) dans le graphe de lineage, et contrôle du lineage au niveau organisation/dossier/projet pour BigQuery, Spark et Airflow.
- Multiplication des connecteurs de métadonnées tiers : dbt Core/MetricFlow, SQL Server, PostgreSQL, Oracle, MySQL, ainsi que des catalogues Iceberg REST fédérés (Databricks Unity, AWS Glue Data Catalog, Snowflake Horizon).
- Arrêt programmé de l'ancien service Data Catalog à partir de juin 2026, ce qui pousse les utilisateurs vers une migration complète vers Knowledge Catalog.

## Analyse approfondie
Vous pouvez consulter les dernières mises à jour produit pour l'ensemble de Google Cloud sur la page Google Cloud, parcourir et filtrer toutes les notes de version dans la console Google Cloud, ou accéder par programmation aux notes de version dans BigQuery.

Pour recevoir les dernières mises à jour produit, ajoutez l'URL de cette page à votre lecteur de flux, ou ajoutez directement l'URL du flux.

### 14 septembre 2026
(aucun contenu associé à cette date)

### 7 septembre 2026
Les « data domains » (domaines de données) dans Knowledge Catalog permettent d'organiser logiquement les ressources au sein de l'entreprise afin de découvrir et de curer vos données à grande échelle. Cette fonctionnalité est disponible en Preview.

Pour en savoir plus, voir À propos des domaines de données.

### 26 août 2026
Le support de Knowledge Catalog pour l'import de métadonnées depuis dbt Core et MetricFlow est disponible en Preview.

Vous pouvez utiliser la commande `gcloud alpha dataplex dbt metadata-jobs` pour extraire et importer des métadonnées techniques, sémantiques (MetricFlow), opérationnelles, de qualité des données et de lineage à partir d'artefacts dbt Core vers Knowledge Catalog.

Pour en savoir plus, voir Importer des métadonnées depuis dbt Core et À propos des connecteurs de métadonnées.

### 24 juillet 2026
Les workflows de gouvernance permettent de mettre en place des contrôles automatisés pour la gestion de l'accès aux data products, via un mécanisme de demande-revue. Cette fonctionnalité est disponible en preview.

Pour en savoir plus, voir À propos des workflows de gouvernance.

### 17 juillet 2026
Le contrôle du data lineage au niveau organisation, dossier ou projet est en disponibilité générale pour BigQuery, Managed Service for Apache Spark et Managed Service for Apache Airflow.

Pour en savoir plus, voir À propos du contrôle de l'ingestion du data lineage et Configurer l'ingestion du data lineage pour un service.

### 9 juillet 2026
Les connecteurs Knowledge Catalog permettant d'importer des métadonnées depuis des sources de données SQL Server et PostgreSQL sont disponibles en Preview.

Les connecteurs Knowledge Catalog extraient automatiquement des métadonnées (techniques, opérationnelles et métier) depuis des sources de données externes et les importent dans des groupes d'entrées Knowledge Catalog. Vous pouvez planifier des exécutions d'import de métadonnées selon un calendrier défini.

Pour en savoir plus, voir À propos des connecteurs de bases de données et Gérer les tâches de connecteur.

### 23 juin 2026
Vous pouvez contrôler l'ingestion du data lineage pour BigQuery et Managed Service for Apache Airflow au niveau organisation, dossier ou projet. Cette fonctionnalité est disponible en preview.

Pour en savoir plus, voir Contrôler l'ingestion de données.

### 22 juin 2026
Les connecteurs Knowledge Catalog permettant d'importer des métadonnées depuis des sources de données Oracle et MySQL sont disponibles en Preview.

Les connecteurs Knowledge Catalog extraient automatiquement des métadonnées (techniques, opérationnelles et métier) depuis des sources de données externes et les importent dans des groupes d'entrées Knowledge Catalog. Vous pouvez planifier des exécutions d'import de métadonnées selon un calendrier défini.

Pour en savoir plus, voir À propos des connecteurs de bases de données et Gérer les tâches de connecteur.

### 14 juin 2026
La découverte automatique de données Cloud Storage par Knowledge Catalog est disponible en GA.

La découverte automatique permet d'analyser les données présentes dans des buckets Cloud Storage afin d'en extraire et cataloguer les métadonnées. Lors d'une analyse de découverte, la découverte automatique crée des tables externes BigLake, des tables externes non-BigLake, ou des tables d'objets BigLake dans BigQuery, rendant ainsi les métadonnées disponibles pour la recherche et l'analyse.

Pour en savoir plus, voir Découvrir et cataloguer les données Cloud Storage.

### 11 juin 2026
Knowledge Catalog prend désormais en charge les analyses de profil de données (« data profile scans ») pour les données non structurées (comme les fichiers PDF dans Cloud Storage) sur des tables d'objets BigQuery existantes. Cette fonctionnalité utilise les modèles Vertex AI Gemini pour extraire des insights sémantiques, notamment des entités et des relations, à partir de contenu non structuré.

Pour en savoir plus, voir À propos des insights sur les données non structurées et Utiliser le profilage de données pour les données non structurées.

### 5 juin 2026
À partir du 1er juin 2026, le service Data Catalog entame un arrêt progressif. À partir de cette date, vous pourriez rencontrer des interruptions, voire une absence totale d'accès aux API Data Catalog. Knowledge Catalog (anciennement Dataplex Catalog) fonctionne sans impact.

Pour en savoir plus sur la migration de Data Catalog vers Knowledge Catalog, voir Passer de Data Catalog à Knowledge Catalog.

### 4 juin 2026
Vous pouvez utiliser la méthode `lookupContext` pour récupérer un ensemble pré-formaté de contexte sur les actifs de données, optimisé pour les workflows agentiques interactifs. Ce contexte prêt pour les LLM aide à ancrer vos agents dans l'évaluation et l'utilisation des actifs de données.

Cette fonctionnalité est disponible en preview.

Pour en savoir plus, voir Récupérer le contexte des actifs de données.

### 29 mai 2026
L'API Data Lineage inclut désormais la méthode `searchLineageStreaming`, qui effectue une recherche en largeur (breadth-first, en amont ou en aval) pour récupérer les liens de lineage d'un actif identifié par son nom pleinement qualifié (FQN).

Pour en savoir plus, voir la référence REST de l'API Data Lineage.

### 27 mai 2026
Vous pouvez utiliser le serveur MCP distant pour le data lineage afin d'interagir avec Knowledge Catalog (anciennement Dataplex Universal Catalog) pour interroger les graphes de data lineage, découvrir la provenance des données en amont et analyser l'impact en aval.

Cette fonctionnalité est disponible en preview. Pour en savoir plus, voir Utiliser le serveur MCP distant pour le data lineage.

### 25 mai 2026
Les data products dans Knowledge Catalog sont désormais en disponibilité générale (GA). Un data product est un package logique et curé d'actifs de données et de contexte, conçu pour résoudre un problème métier spécifique.

Cette version inclut les nouvelles fonctionnalités suivantes :

- **Workflows d'approbation pour la consommation de data products :** les consommateurs de data products peuvent parcourir les data products publiés, soumettre des demandes d'accès et suivre leur statut. Les propriétaires de data products peuvent suivre, approuver ou rejeter les demandes d'accès via la console Google Cloud ou l'API. Pour en savoir plus, voir Utiliser les data products et Gérer les data products.
- **Documentation et insights automatisés :** les propriétaires de data products peuvent tirer parti des data insights de Knowledge Catalog et de Gemini pour générer automatiquement des exemples de requêtes, des insights métier et des modèles de documentation pour les data products. Pour en savoir plus, voir Créer des data products.
- **Support des comptes de service :** les propriétaires de data products peuvent configurer des comptes de service dans les groupes d'accès, et les consommateurs de data products peuvent demander l'accès pour leurs comptes de service. Pour en savoir plus, voir Créer des data products.
- **Support du serveur distant Model Context Protocol (MCP) (Preview) :** les applications de données et les agents IA peuvent interagir de manière programmatique avec les data products. En déployant le serveur MCP distant de Knowledge Catalog, les développeurs peuvent créer des data products, en découvrir et inspecter les métadonnées depuis des IDE externes et des clients LLM. Pour en savoir plus, voir Accéder aux data products via Model Context Protocol.

### 15 mai 2026
Le lineage au niveau colonne pour Dataproc est en disponibilité générale (GA). Cette fonctionnalité permet de suivre le flux de données entre colonnes individuelles dans BigQuery, les tables externes BigLake, les buckets Cloud Storage et d'autres ressources, tel que rapporté par les clusters Dataproc et Serverless for Apache Spark. Pour en savoir plus, voir À propos du data lineage.

L'API Data Lineage est mise à jour avec les changements suivants :

- La méthode `SearchLinks` accepte désormais plusieurs références d'entités source et cible comme critères de recherche.
- Ajout du support des informations de lineage au niveau colonne, à la fois en entrée et en sortie du service.
- Les ressources de type « process » indiquent désormais Dataflow comme origine lorsque celui-ci est utilisé pour générer le lineage.

Pour en savoir plus, voir la référence REST et RPC de l'API Data Lineage.

### 28 avril 2026
Cloud Composer s'appelle désormais Managed Service for Apache Airflow. Les noms des API associées, des bibliothèques clientes, des commandes CLI et de la gestion des identités et des accès (IAM) restent inchangés et continuent de référencer Composer.

**Dataproc** et **Google Cloud Serverless for Apache Spark** sont désormais unifiés sous la marque **Managed Service for Apache Spark**. Ce changement consolide nos options de déploiement Spark managé sous une seule marque ombrelle englobant l'ensemble de nos capacités Spark. Aucune fonctionnalité existante n'est supprimée dans le cadre de ce changement, et il n'y a aucun impact sur l'API Dataproc, le metastore, la bibliothèque cliente, la CLI ou les noms IAM.

### 25 avril 2026
L'arrêt d'une tâche Datascan (« Stop Datascan job ») dans Knowledge Catalog est en disponibilité générale (GA). Vous pouvez annuler des tâches de qualité de données, de profilage de données et de découverte qui prennent plus de temps que prévu ou qui ont été mal configurées. Pour en savoir plus, voir Annuler une tâche d'analyse de qualité des données, Annuler une tâche d'analyse de profil de données et Annuler une tâche de découverte.

### 24 avril 2026
BigLake s'appelle désormais Google Cloud Lakehouse. Le metastore BigLake s'appelle désormais le catalogue d'exécution Lakehouse (« Lakehouse runtime catalog »). Les noms des API associées, des bibliothèques clientes, des commandes CLI et de la gestion des identités et des accès (IAM) restent inchangés et continuent de référencer BigLake.

### 20 avril 2026
Knowledge Catalog découvre les liens entre les actifs de données, ce qui aide à comprendre comment ils se connectent et la nature de leurs relations. Cette fonctionnalité est disponible en preview. Pour en savoir plus, voir Visualiser les relations entre données dans Knowledge Catalog.

### 17 avril 2026
La qualité des données prend désormais en charge la réutilisation des règles. Vous pouvez maintenant définir des règles de qualité des données sous forme de modèles et les réutiliser sur plusieurs entrées de catalogue afin de standardiser vos processus de validation des données. Vous pouvez également utiliser une bibliothèque partagée de modèles de règles système pour des scénarios de validation courants. Pour en savoir plus, voir Réutiliser des règles de qualité des données.

Pour affiner davantage les graphes de lineage, les vues de lineage de Knowledge Catalog incluent de nouveaux modes de mise en évidence et de filtrage. Cette fonctionnalité est disponible en preview. Pour en savoir plus, voir Appliquer des filtres et une mise en évidence pour une vue ciblée.

### 16 avril 2026
Les data insights pour les données non structurées transforment les « dark data » ou fichiers non structurés (sous forme de PDF dans Cloud Storage) en actifs structurés et interrogeables. Cette fonctionnalité est désormais disponible en preview.

Pour en savoir plus, voir À propos des data insights pour les données non structurées.

Le catalogage automatisé de l'Iceberg REST Catalog (IRC) pour le catalogue d'exécution Google Cloud Lakehouse est désormais en disponibilité générale (GA). Cela inclut le support du lineage, du profilage de données, de la qualité des données et des data insights.

Le support fédéré pour Databricks Unity IRC, AWS Glue Data Catalog IRC et Snowflake Horizon IRC est disponible en preview.

Pour en savoir plus, voir À propos de la gestion des métadonnées dans Knowledge Catalog.

### 10 avril 2026
Dataplex Universal Catalog s'appelle désormais Knowledge Catalog. Les noms de l'API, de la bibliothèque cliente, de la CLI et de la gestion des identités et des accès (IAM) restent inchangés.

Le mode de profilage léger (« lightweight profiling mode ») pour les analyses de profil de données est disponible en preview.

Ce mode léger fournit des analyses de profil à faible latence retournant des résultats en quelques secondes, ce qui le rend idéal pour ancrer les réponses des agents IA et l'exploration interactive des données. Pour en savoir plus, voir Modes de profilage.

### 9 avril 2026
Vous pouvez désormais spécifier une identité d'exécution personnalisée pour les analyses de qualité et de profil de données. Par défaut, les analyses s'exécutent avec l'identité du « Service Agent ». Vous pouvez maintenant utiliser un compte de service personnalisé (Bring Your Own Service Account) ou des identifiants d'utilisateur final (EUC — End-User Credentials). L'utilisation d'une identité d'exécution personnalisée permet d'appliquer le principe du moindre privilège, d'utiliser des contrôles d'accès BigQuery précis, et d'unifier les coûts de traitement des analyses directement sous BigQuery.

Pour en savoir plus, voir Configurer l'identité d'exécution pour les analyses de qualité des données et Configurer l'identité d'exécution pour les analyses de profil de données.

### 30 mars 2026
Le catalogage automatisé des métadonnées Looker (Google Cloud core), ainsi que l'ingestion du data lineage depuis des sources BigQuery, sont désormais disponibles en preview. Pour en savoir plus, voir la documentation Looker (Google Cloud core).

### 24 février 2026
(aucun contenu associé à cette date)

### 19 février 2026
Lors de la création d'une règle de qualité des données, vous pouvez désormais éventuellement inclure une requête de débogage à exécuter en parallèle de la règle. Une requête de débogage est une instruction SQL qui retourne jusqu'à 10 valeurs scalaires pour aider à diagnostiquer les échecs de règles. Cette fonctionnalité est disponible en preview.

### 11 février 2026
Vous pouvez désormais utiliser des flux de changement de métadonnées (« metadata change feeds ») pour recevoir des notifications quasi en temps réel sur les changements de métadonnées dans Dataplex. Dataplex publie des notifications vers un sujet Pub/Sub de votre choix, vous permettant de créer des workflows pilotés par événements, de synchroniser les métadonnées vers des catalogues externes, ou de déclencher des contrôles de qualité des données. Pour en savoir plus, voir À propos des flux de changement de métadonnées.

### 29 janvier 2026
(aucun contenu associé à cette date)

### 12 janvier 2026
Certaines métadonnées stockées dans Dataplex Universal Catalog évoluent. Ce changement met en cohérence les métadonnées stockées dans Dataplex avec celles des systèmes source d'origine tels que Vertex AI, Bigtable, Spanner, Pub/Sub, Dataform et Dataproc Metastore. Si vous avez des workloads dépendant de ces métadonnées Dataplex, vous devez les adapter pour préserver la continuité. Pour en savoir plus sur la portée de ce changement et sur ce que vous devez faire, voir Changements apportés aux métadonnées stockées dans Dataplex Universal Catalog.

### 8 décembre 2025
La recherche en langage naturel dans Dataplex Universal Catalog est en disponibilité générale (GA).

La recherche en langage naturel étend la recherche par mot-clé pour prendre en charge des requêtes en langage naturel. Elle permet de trouver des ressources en utilisant un langage courant, éliminant le besoin d'une syntaxe complexe.

### 21 novembre 2025
Les data products dans Dataplex Universal Catalog sont désormais disponibles en preview.

Un data product est un package logique et curé d'actifs de données conçu pour résoudre un problème métier spécifique. Il permet d'accélérer le temps d'accès aux insights et fournit confiance, contexte et mécanismes de demande d'accès en libre-service pour les consommateurs de données. Pour en savoir plus, voir À propos des data products.

### 17 novembre 2025
Auparavant, les résultats des analyses de profil de données n'étaient publiés que dans la console Google Cloud. Vous pouvez désormais publier les résultats d'une analyse de profil de données en tant que métadonnées Dataplex Universal Catalog. Les derniers résultats sont enregistrés dans l'entrée représentant la table source. Vous pouvez consulter les résultats dans la console Google Cloud.

Si vous souhaitez activer la publication au catalogue pour une analyse de profil de données existante, vous devez modifier l'analyse et réactiver l'option de publication.

Pour en savoir plus, voir Utiliser le profilage de données.

Cette fonctionnalité est en disponibilité générale (GA).

### 29 septembre 2025
Le lineage au niveau colonne est en disponibilité générale (GA). Cette fonctionnalité fournit une vue granulaire de vos données en suivant le flux entre colonnes individuelles au sein des tables. Vous pouvez effectuer des analyses telles que la recherche de cause racine, l'analyse d'impact et la vérification de la source des données pour des colonnes spécifiques. Le lineage au niveau colonne n'est pris en charge que pour les tâches BigQuery. Pour en savoir plus sur le lineage au niveau colonne, voir Lineage au niveau colonne.

### 23 septembre 2025
Vous pouvez désormais connecter votre instance Dataplex Universal Catalog à vos outils de développement préférés, tels que Gemini CLI et d'autres IDE. Cette intégration permet la découverte de données et la gestion des actifs pilotées par IA, directement dans votre environnement de développement. Pour en savoir plus, voir Utiliser Dataplex Universal Catalog avec MCP, Gemini et d'autres agents.

### 3 septembre 2025
La recherche en langage naturel dans Dataplex Universal Catalog est disponible en preview.

La recherche en langage naturel étend la recherche par mot-clé pour prendre en charge des requêtes en langage naturel. Elle permet de trouver des ressources en utilisant un langage courant, éliminant le besoin d'une syntaxe complexe.

### 18 juin 2025
Auparavant, les résultats des analyses de qualité des données n'étaient publiés que dans la console Google Cloud. Vous pouvez désormais publier les résultats d'une analyse de qualité des données en tant que métadonnées Dataplex Universal Catalog. Les derniers résultats sont enregistrés dans l'entrée représentant la table source. Vous pouvez consulter les résultats dans la console Google Cloud.

Si vous souhaitez activer la publication au catalogue pour une analyse de qualité des données existante, vous devez modifier l'analyse et réactiver l'option de publication.

Pour en savoir plus, voir Utiliser la qualité de données automatique.

Cette fonctionnalité est en disponibilité générale (GA).

### 19 mai 2025
(aucun contenu associé à cette date)

### 13 mai 2025
L'export en masse des métadonnées du catalogue universel est en disponibilité générale (GA).

Vous pouvez exporter les métadonnées du catalogue universel vers Cloud Storage, puis les utiliser pour des tâches nécessitant une récupération exhaustive des métadonnées. Vous pouvez également interroger et analyser les métadonnées exportées dans BigQuery.

Pour en savoir plus, voir Exporter des métadonnées.

### 7 mai 2025
Des connecteurs personnalisés pour les pipelines de connectivité managés sont disponibles pour diverses sources de données tierces. Ces connecteurs sont fournis par la communauté. Pour en savoir plus, voir Connecteurs personnalisés contribués par la communauté.

### 5 mai 2025
Vous pouvez utiliser des contraintes personnalisées avec Organization Policy pour fournir un contrôle plus granulaire sur des champs spécifiques de certaines ressources Dataplex et de data lineage. Pour en savoir plus, voir Gérer les ressources Dataplex à l'aide de contraintes personnalisées et Gérer les ressources de data lineage à l'aide de contraintes personnalisées. Cette fonctionnalité est en disponibilité générale (GA).

### 28 avril 2025
La découverte automatique Dataplex analyse vos données dans les buckets Cloud Storage pour en extraire et cataloguer les métadonnées, créant des tables BigLake, externes, ou d'objets pour l'analytique et l'IA, à des fins d'insights, de sécurité et de gouvernance. Cette fonctionnalité est en disponibilité générale (GA).

### 14 avril 2025
(aucun contenu associé à cette date)

### 9 avril 2025
Dataplex Catalog a été renommé BigQuery universal catalog. Vous verrez ce nouveau nom sur la page produit de la console Google Cloud, dans l'ensemble de la documentation et dans les supports marketing. Universal catalog réunit les capacités de catalogue de données de Dataplex Catalog et les capacités de metastore d'exécution de BigQuery metastore. Pour en savoir plus, voir Introduction à la gouvernance des données dans BigQuery.

### 17 mars 2025
Dataplex et data lineage sont disponibles dans la région `northamerica-south1` (Mexique).

Dataplex et data lineage sont disponibles dans la région `europe-north2` (Stockholm).

### 13 mars 2025
(aucun contenu associé à cette date)

### 18 février 2025
Dataplex Attribute Store est déprécié et sera abandonné le 18 février 2026. Pour connaître les étapes de transition vers les tags, les policy tags et les conditions IAM, voir Migrer d'Attribute Store vers les tags et les conditions IAM.

### 11 février 2025
(aucun contenu associé à cette date)

### 3 février 2025
L'ingestion des entités Dataplex (y compris celles créées en sortie de Dataplex Discovery) est dépréciée et cessera de fonctionner d'ici le 30 septembre 2025. Les tables externes dans BigQuery publiées par Discovery seront ingérées dans Dataplex Catalog en tant qu'entrées. Voir Passer de Data Catalog à Dataplex Catalog.

### 28 janvier 2025
L'import de métadonnées « aspect-only » pour les métadonnées Dataplex Catalog est en disponibilité générale (GA). Utilisez une tâche d'import de métadonnées aspect-only pour modifier de façon incrémentale des aspects, sans modifier les autres métadonnées appartenant aux entrées dans le périmètre de la tâche. Pour en savoir plus, voir Importer des métadonnées à l'aide d'un pipeline personnalisé.

### 20 janvier 2025
La visualisation du chemin de data lineage est disponible en preview. Les visualisations de chemin de lineage aident à comprendre les liens de lineage entre deux ressources sélectionnées. Pour en savoir plus, voir Visualisation du chemin de lineage.

### 9 décembre 2024
(aucun contenu associé à cette date)

### 5 novembre 2024
La découverte automatique Dataplex est disponible en preview publique. La découverte automatique est une fonctionnalité de BigQuery qui permet d'analyser les données dans des buckets Cloud Storage afin d'en extraire et cataloguer les métadonnées. La découverte automatique crée des tables BigLake ou externes ainsi que des tables d'objets utilisables pour l'analytique et l'IA, et catalogue ces données dans Dataplex Catalog. Pour en savoir plus, voir Découvrir et cataloguer les données Cloud Storage.

### 4 novembre 2024
La recherche sémantique par projet proposée par Dataplex Search est disponible en Preview. La recherche sémantique, propulsée par Gemini, simplifie le processus de recherche sans nécessiter de syntaxe complexe. Elle prend en charge les requêtes en langage naturel. Pour en savoir plus, voir Découvrir des données via la recherche sémantique.

### 18 octobre 2024
Le data lineage est disponible dans les régions Google Cloud suivantes :

- Berlin (`europe-west10`)
- Dammam (`me-central2`)
- Doha (`me-central1`)
- Johannesburg (`africa-south1`)
- Turin (`europe-west12`)

Le data lineage est disponible dans les régions BigQuery Omni suivantes :

- AWS - Asie-Pacifique (Sydney) (`aws-ap-southeast-2`)
- AWS - Europe (Irlande) (`aws-eu-west-1`)
- AWS - Europe (Francfort) (`aws-eu-central-1`)
- AWS - US Ouest (Oregon) (`aws-us-west-2`)

### 15 octobre 2024
Certaines métadonnées BigQuery stockées dans Dataplex Catalog évoluent. Si vous avez des workloads dépendant de ces métadonnées BigQuery, vous devez les adapter pour préserver la continuité. Pour en savoir plus sur la portée de ce changement et sur ce que vous devez faire, voir Changements apportés aux métadonnées BigQuery stockées dans Dataplex Catalog.

### 10 octobre 2024
(aucun contenu associé à cette date)

### 30 septembre 2024
Les pipelines de connectivité managés sont en disponibilité générale (GA). Utilisez un pipeline de connectivité managé pour extraire des métadonnées depuis des sources tierces et les importer dans Dataplex Catalog. Vous développez votre propre connecteur d'extraction de métadonnées, et utilisez Workflows pour l'orchestration et la planification.

Pour en savoir plus, voir Présentation de la connectivité managée, Importer des métadonnées depuis une source personnalisée via Workflows, et Développer un connecteur personnalisé pour l'import de métadonnées.

Par ailleurs, les méthodes de l'API d'import de métadonnées sont en GA. Pour en savoir plus, voir Importer des métadonnées à l'aide d'un pipeline personnalisé.

### 28 août 2024
Data insights est en disponibilité générale (GA). Data insights offre un moyen automatisé d'explorer et de comprendre vos données. Il utilise Gemini pour générer des requêtes basées sur les métadonnées d'une table, et aide à mettre au jour des tendances, évaluer la qualité des données et effectuer des analyses statistiques.

Vous générez des data insights dans BigQuery. Vous pouvez consulter les data insights dans Dataplex et dans BigQuery.

### 12 août 2024
(aucun contenu associé à cette date)

### 29 juillet 2024
(aucun contenu associé à cette date)

### 24 juillet 2024
Le lineage de données au niveau colonne pour BigQuery est disponible en Preview pour les utilisateurs sur liste blanche. La fonctionnalité de data lineage existante suit la façon dont les données BigQuery circulent dans vos systèmes au niveau table. Le lineage au niveau colonne étend cette fonctionnalité pour permettre de suivre les mouvements de données BigQuery au niveau colonne.

Pour vous inscrire, remplissez le formulaire d'inscription au lineage au niveau colonne.

### 22 juillet 2024
(aucun contenu associé à cette date)

### 8 juillet 2024
Dataplex Catalog est en disponibilité générale (GA). Dataplex Catalog fournit une plateforme pour stocker, gérer et accéder à vos métadonnées.

Pour en savoir plus, voir Présentation de Dataplex Catalog, Rechercher des actifs de données, Gérer les aspects et enrichir les métadonnées, et Gérer les entrées et ingérer des sources personnalisées.

### 3 juillet 2024
(aucun contenu associé à cette date)

### 30 juin 2024
(aucun contenu associé à cette date)

### 28 mai 2024
La qualité de données automatique de Dataplex prend en charge les capacités suivantes :

- Notifications par e-mail pour alerter sur le statut et les résultats d'une tâche de qualité des données
- Scores de qualité des données indiquant le pourcentage de règles ayant réussi
- Support de l'API pour des recommandations de règles basées sur des analyses de profilage de données

Pour en savoir plus, voir Utiliser la qualité de données automatique et Présentation de la qualité de données automatique.

### 25 avril 2024
La qualité de données automatique de Dataplex prend en charge les capacités suivantes :

- Le type de règle « assertion SQL » pour les règles SQL personnalisées permet de vérifier un état invalide d'un jeu de données.
- Vous pouvez utiliser le paramètre de référence de données dans une règle SQL personnalisée pour référencer une table source de données et tous ses filtres de précondition, au lieu de mentionner explicitement la table et ses filtres.

### 27 mars 2024
Data insights dans Dataplex est disponible en Preview. Data insights offre un moyen automatisé et intuitif d'explorer et de comprendre vos données. Il utilise les grands modèles de langage Gemini pour générer des requêtes basées sur les métadonnées d'une table, et permet de mettre au jour des tendances, évaluer la qualité des données et effectuer des analyses statistiques.

### 25 mars 2024
Le catalogage automatisé de Vertex AI feature store est disponible en Preview. Avec cette intégration, vous pouvez découvrir les groupes de features et features Vertex AI à travers projets et régions via la console ou l'API Dataplex. Dataplex automatise entièrement le processus d'ingestion et d'indexation des métadonnées, tout en effectuant des vérifications des permissions IAM à la source, offrant une expérience de gouvernance unifiée pour les actifs de données et d'IA à travers les services Cloud.

### 17 décembre 2023
Le catalogage automatisé de Spanner est en disponibilité générale (GA) dans Dataplex. Avec cette intégration, vous pouvez découvrir les instances, bases de données et tables Spanner à travers projets et régions via la console ou l'API Dataplex. Les opérations d'ingestion et d'indexation des métadonnées sont entièrement automatisées, avec des permissions IAM définies au niveau de la source de données, offrant une base essentielle pour la gestion et la gouvernance des données.

### 1 décembre 2023
Le catalogage automatisé des modèles et jeux de données Vertex AI est en disponibilité générale (GA) dans Dataplex. Avec cette intégration, vous pouvez découvrir les modèles et jeux de données Vertex AI à travers projets et régions via la console et l'API Dataplex. Dataplex automatise entièrement le processus d'ingestion et d'indexation des métadonnées, tout en effectuant des vérifications des permissions IAM à la source, offrant une expérience de gouvernance unifiée pour les actifs de données et d'IA à travers les services Cloud.

### 6 octobre 2023
Le catalogage automatisé de Bigtable est en disponibilité générale (GA) dans Dataplex. Avec cette intégration, vous pouvez découvrir les tables et instances Bigtable à travers projets et régions via la console ou l'API Dataplex. Les opérations d'ingestion et d'indexation des métadonnées sont entièrement automatisées, avec des permissions IAM définies au niveau de la source de données, offrant une base essentielle pour la gestion et la gouvernance des données.

### 3 octobre 2023
L'intégration Dataplex BigLake est en disponibilité générale (GA). L'intégration Dataplex BigLake permet de faire évoluer un bucket Cloud Storage vers un mode managé, en créant des tables BigLake et des tables d'objets au lieu de tables externes. Cela permet l'application de politiques au niveau colonne, ligne et table, activant une sécurité fine et un masquage dynamique des données.

### 29 septembre 2023
(aucun contenu associé à cette date)

### 21 août 2023
La qualité de données automatique et le profilage de données de Dataplex sont en disponibilité générale.

- Profilage de données
  - Démarrez rapidement votre analytique de données avec des insights statistiques, tels que les valeurs moyennes, les valeurs uniques, les bornes de données et le top-N.
  - Comprenez les dérives et construisez des modèles d'anomalies grâce aux métadonnées générées.
  - Publiez les informations de qualité et de profilage de données dans la console BigQuery. En savoir plus.
  - Profilez les données dans les tables BigQuery, les vues, BigLake et les tables externes.
  - Facilitez le déploiement grâce à une exécution managée, serverless et sans copie de données (« zero-copy »).
  - Profitez de fonctionnalités avancées telles que le filtrage, l'échantillonnage et l'enregistrement des résultats dans une table BigQuery centrale.
- Qualité de données automatique
  - Fournissez des données fiables en construisant un pipeline de surveillance de la qualité des données de bout en bout.
  - Consultez les recommandations de règles, enrichissez-les avec des règles métier, surveillez de façon routinière ou dans un pipeline, générez des rapports, soyez alerté en cas d'échec et résolvez les problèmes.
  - Consultez les informations de qualité dans l'interface BigQuery, visibles par tous les utilisateurs de la table. En savoir plus.
  - Améliorez la qualité des données dans les tables BigQuery, les vues, BigLake et les tables externes.
  - Facilitez le déploiement grâce à une exécution managée, serverless et sans copie de données.
  - Profitez de fonctionnalités avancées telles que le filtrage, l'échantillonnage et l'enregistrement des résultats dans une table BigQuery centrale.

### 14 août 2023
Le data lineage au niveau entrée pour les tâches Spark exécutées dans Dataproc est en GA.

### 1 août 2023
Dataplex est disponible dans les régions suivantes :

- Los Angeles (`us-west2`)
- Salt Lake City (`us-west3`)
- Las Vegas (`us-west4`)
- Columbus (`us-east5`)
- Santiago (`southamerica-west1`)
- Finlande (`europe-north1`)
- Varsovie (`europe-central2`)
- Madrid (`europe-southwest1`)
- Milan (`europe-west8`)
- Paris (`europe-west9`)
- Jakarta (`asia-southeast2`)

### 18 mai 2023
- La qualité de données automatique (AutoDQ) et le profilage de données de Dataplex peuvent être utilisés sur n'importe quelle table BigQuery, y compris celles ne faisant pas partie d'un lake Dataplex. Il n'est pas nécessaire de créer un lake Dataplex pour exécuter AutoDQ et le profilage de données de Dataplex.
- AutoDQ et le profilage de données de Dataplex prennent en charge les vues BigQuery, les tables BigLake et les tables externes BigQuery.
- AutoDQ et le profilage de données de Dataplex prennent en charge l'échantillonnage de vos données afin de réduire le temps et le coût.

### 13 mars 2023
Le data lineage de Dataplex est en disponibilité générale (GA). Le data lineage permet de suivre comment les données circulent à travers vos systèmes : d'où elles viennent, où elles sont transmises, et quelles transformations leur sont appliquées.

### 30 janvier 2023
Dataplex Attribute Store est désormais disponible en Preview. Dataplex Attribute Store permet d'associer des attributs (avec des spécifications de comportement, telles que l'accès aux ressources et aux colonnes) à des tables et des colonnes.

Dataplex business glossary est désormais disponible en Preview. Dataplex business glossary permet de gérer la terminologie métier et les définitions à travers l'organisation, et de les utiliser pour décrire et découvrir des entrées de données.

### 22 décembre 2022
Le data lineage de Dataplex est désormais disponible en Preview. Le data lineage permet de suivre comment les données circulent à travers vos systèmes : d'où elles viennent, où elles sont transmises, et quelles transformations leur sont appliquées.

### 16 décembre 2022
L'intégration Dataplex BigLake est désormais disponible en Preview. L'intégration Dataplex BigLake permet de faire évoluer un bucket Cloud Storage vers un mode managé, en créant des tables BigLake au lieu de tables externes. Cela permet l'application manuelle de politiques au niveau colonne, ligne et table.

### 12 décembre 2022
Le profilage de données de Dataplex est désormais disponible en Preview. Le profilage de données de Dataplex aide les utilisateurs de données à mieux comprendre leurs données en identifiant les caractéristiques communes des données. Dataplex utilise ces informations pour recommander également des règles de qualité des données.

La qualité de données automatique de Dataplex (AutoDQ) est désormais disponible en Preview. La qualité de données automatique de Dataplex aide les utilisateurs de données à instaurer la confiance dans leurs données grâce à un produit clé en main et automatisé qui encapsule l'ensemble du processus de qualité des données.

### 1 décembre 2022
(aucun contenu associé à cette date)

### 20 octobre 2022
L'atelier d'exploration de données (Explore) est en disponibilité générale (GA). Explore offre une expérience d'exploration de données entièrement managée et serverless, portée par une collaboration entièrement gouvernée, une planification en un clic, et une interrogation interactive à l'aide de scripts Spark SQL et de notebooks Jupyter.

## Pourquoi ça compte
Ce changelog illustre concrètement comment les hyperscalers refondent leurs offres de gouvernance de données autour de l'IA générative (Gemini, MCP, agents) plutôt que de rester de simples catalogues passifs, un signal utile pour toute veille sur l'évolution des plateformes data/IA d'entreprise et sur la stratégie produit de Google Cloud face à Databricks, Snowflake et AWS Glue.
