---
title: "Querying Databricks Iceberg tables with Google Cloud’s Lakehouse | Google Cloud Blog"
date: 2026-11-04
url: "https://cloud.google.com/blog/products/data-analytics/querying-databricks-iceberg-tables-with-google-clouds-lakehouse/"
authors: ["Pramod Niralakeri"]
keywords: ["Apache Iceberg", "BigQuery", "Databricks", "Lakehouse", "architecture multicloud", "gouvernance des données"]
theme: "Data"
tone: "tutorial"
used_in: ["2026-11-04"]
---

## Résumé
Google Cloud présente sa fonctionnalité « Lakehouse », qui permet à BigQuery d'interroger directement des tables Apache Iceberg gérées par Databricks sans dupliquer les données. Les métadonnées Iceberg générées par Databricks (Managed Iceberg Tables / UniForm) sont lues nativement par BigQuery via Google Cloud Storage, avec une fédération de catalogue reposant sur l'API REST Iceberg et Unity Catalog, et des jetons temporaires délivrés par « credential vending ». L'article détaille aussi la sécurité centralisée, l'élagage des partitions, la mise en cache multicloud, et les opérations de maintenance (compaction, VACUUM) nécessaires pour garder ce lakehouse performant et peu coûteux.

## Points clés
- Approche « zero-copy » : BigQuery lit directement les fichiers Parquet/Iceberg écrits par Databricks dans GCS, avec un rafraîchissement des métadonnées jusqu'à toutes les 5 minutes.
- La fédération s'étend aussi à AWS S3 et Azure Blob Storage via le catalogue REST Iceberg, mais des frais de sortie (egress) inter-cloud peuvent s'appliquer.
- La gouvernance reste centralisée dans BigQuery (sécurité au niveau ligne/colonne, masquage dynamique) grâce à une connexion de ressource cloud liée à un compte de service IAM.
- Unity Catalog de Databricks sert de couche de métadonnées centrale ; BigQuery obtient un accès temporaire à GCS via des jetons de courte durée (credential vending).
- L'élagage de partitions et les statistiques des manifestes Iceberg réduisent le volume de données scannées, donc les coûts de slots et de stockage.
- La maintenance régulière (OPTIMIZE pour compacter les petits fichiers, VACUUM pour purger les fichiers orphelins après un délai de 7 jours) est indispensable pour préserver la performance.

## Analyse approfondie

#### Comment Lakehouse et Databricks fonctionnent ensemble
Les tables Iceberg gérées par Databricks génèrent automatiquement des métadonnées compatibles Iceberg en parallèle des journaux Delta natifs. Les équipes data stockent les fichiers Parquet une seule fois dans Google Cloud Storage via Databricks. Plutôt que de charger ces données dans BigQuery, Lakehouse lit directement les métadonnées Iceberg et applique le moteur vectorisé de BigQuery aux fichiers au format ouvert stockés dans GCS.

Bien que GCS soit la couche de stockage principale dans cet exemple, Lakehouse étend cette fédération « sans frontières » à des environnements cloud externes comme Amazon S3 et Azure Blob Storage. En combinant le catalogue REST Apache Iceberg ouvert avec des connexions inter-cloud, Lakehouse permet à BigQuery d'interroger des données situées sur différents clouds sans les déplacer. Chaque catalogue fédéré réside dans la région Google Cloud de votre choix, idéalement la plus proche de vos données. BigQuery peut ainsi lire des fichiers Parquet au format ouvert là où ils se trouvent, pour des analyses multicloud sans pipeline de réplication. Des frais de sortie restent applicables pour les clouds distants, mais Cross-Cloud Interconnect (AWS) et la mise en cache Lakehouse permettent de les réduire.

Au-delà de la simple interrogation de données externes, Lakehouse établit une véritable interopérabilité en lecture et en écriture entre les moteurs. Comme la plateforme repose sur des fondations Apache Iceberg ouvertes, les équipes data peuvent exécuter sans difficulté des commandes SQL multi-instructions directement dans BigQuery.

#### Sécurité et gouvernance centralisées
Gérer les contrôles d'accès à travers des systèmes disparates peut introduire des failles. Lakehouse résout ce problème par une délégation des accès. Les administrateurs configurent une connexion de ressource cloud BigQuery (Cloud Resource Connection) liée à un compte de service qui gère les droits IAM sur les buckets GCS. En accordant l'accès à l'entité de table Lakehouse, on peut appliquer les contrôles BigQuery — sécurité au niveau ligne, au niveau colonne, et masquage dynamique des données — sur des tables Iceberg externes, tandis que Databricks gère l'ingestion.

#### Fédération de catalogue et credential vending
Auparavant, relier ces plateformes exigeait de configurer manuellement les requêtes BigQuery pour pointer vers des chemins de métadonnées statiques. Les configurations modernes exploitent l'API REST Catalog ouverte d'Iceberg. Unity Catalog de Databricks fait office de couche de métadonnées centrale, permettant à un administrateur BigQuery de créer un catalogue d'exécution Lakehouse avec une connexion fédérée. Lors de l'exécution d'une requête, Lakehouse contacte Unity Catalog pour obtenir l'état actuel de la table, et des jetons de courte durée sont émis via credential vending pour accorder à BigQuery un accès en lecture temporaire à GCS.

#### Partition pruning (élagage des partitions)
BigQuery utilise les métadonnées Iceberg de chaque table pour planifier la requête, puis ne lit que les fichiers de données pertinents, sur place. Le partitionnement caché d'Iceberg permet de filtrer sur des colonnes logiques, comme des horodatages, sans connaître la structure des répertoires. Notez que les tables Iceberg gérées par Databricks ne supportent pas les transformations de partition ; Databricks recommande plutôt le Liquid Clustering.

Les filtres d'une clause WHERE standard permettent à BigQuery d'utiliser les manifestes Iceberg pour ignorer les partitions qui ne peuvent pas correspondre. Il faut comparer les colonnes de partition à des valeurs littérales pour que l'élagage s'applique. Ces manifestes conservent des statistiques détaillées au niveau des colonnes, permettant à BigQuery d'ignorer immédiatement les enregistrements de manifeste non pertinents et les fichiers Parquet inutiles. Les requêtes ne scannent donc que les plages d'octets nécessaires, accélérant l'exécution tout en réduisant significativement la consommation de slots à la demande et les coûts de scan de stockage.

#### Requêtes rapides avec les métadonnées Iceberg et le cache Lakehouse
Les manifestes Iceberg identifient déjà les fichiers de données à lire, donc BigQuery n'a pas besoin d'un cache de métadonnées pour les tables Iceberg. Pour les tables inter-cloud, comme celles sur Amazon S3, la mise en cache Lakehouse (en preview) conserve les blocs de données récupérés dans Google Cloud afin que les requêtes répétées les lisent localement. BigQuery lit directement les fichiers de manifeste Iceberg lors de la planification de chaque requête ; il n'y a pas de cache de métadonnées à activer. Cet élagage dynamique des partitions évite les fichiers inutiles, réduisant considérablement le temps d'exécution et le volume d'octets scannés.

#### Maintenance et gestion du cycle de vie
Les lakehouses modernes exigent un entretien actif ; sans soin régulier, la performance se dégrade et le lakehouse devient un dépôt inefficace. Heureusement, BigQuery et Databricks offrent tous deux des capacités natives pour préserver l'hygiène des tables et accélérer les charges analytiques.

**Garder vos tables optimisées**
1. Déclencher des pipelines de compaction réguliers via les API Databricks pour fusionner les petits fichiers Parquet en blocs plus volumineux et optimisés, et utiliser l'optimisation prédictive (Predictive Optimization).
2. Exécuter la commande Databricks VACUUM pour supprimer les fichiers non référencés en dehors des snapshots actifs, évitant des coûts de stockage GCS supplémentaires.

**Compaction et le problème des petits fichiers**
Les opérations d'écriture fréquentes, les tâches d'ingestion continue et les charges de streaming produisent en permanence des milliers de petits fichiers Parquet. Cette fragmentation crée un goulot d'étranglement de stockage qui peut limiter l'efficacité de lecture de BigQuery. Établir des milliers de connexions réseau vers GCS et traiter les en-têtes de métadonnées à travers de nombreux petits fichiers consomme un temps de calcul important, diminuant les avantages de performance de l'exécution vectorisée des requêtes.

Exécuter une compaction régulière au sein d'Iceberg résout ces inefficacités. Databricks gère cela automatiquement via Liquid Clustering, qui ajuste dynamiquement la disposition des fichiers selon les schémas d'accès, ou via des utilitaires natifs de gestion de table.

Pour compacter manuellement les petits fichiers sur Databricks, on exécute la commande OPTIMIZE. Cette commande regroupe des segments de fichiers dispersés en blocs structurés plus volumineux, typiquement entre 256 Mo et 512 Mo, ce qui peut améliorer le débit de scan de BigQuery. L'approche « binpack » opère rapidement en priorisant l'équilibrage de la taille totale des fichiers, bien que des stratégies de tri alternatives puissent organiser l'ordre du jeu de données selon des colonnes clés spécifiques.

**Gestion des fichiers orphelins et rétention des snapshots (VACUUM)**
Chaque mise à jour transactionnelle, modification d'enregistrement et compaction de table crée de nouveaux snapshots dans Iceberg pour préserver l'intégrité du jeu de données. Au fil du temps, les anciens objets Parquet détachés des états actifs de la table deviennent orphelins. Bien que ces fichiers historiques permettent des analyses de type « time travel », les négliger peut faire grimper les coûts de stockage GCS.

Les équipes data peuvent utiliser l'opération Databricks VACUUM pour scanner et purger les fichiers de stockage abandonnés.

Les configurations standard appliquent un seuil obligatoire de sept jours (deletedFileRetentionDuration) avant d'exécuter les routines VACUUM. Préserver ce délai évite que des tâches analytiques actives ne rencontrent des erreurs de fichiers manquants, tout en conservant des options de récupération historique. Planifier des tâches VACUUM régulières, ou laisser l'optimisation prédictive s'en charger, supprime les fichiers de données non référencés et, pour les tables avec lecture Iceberg, les anciennes métadonnées Iceberg. Cela permet de maintenir des coûts de stockage bas et une performance élevée à travers votre lakehouse.

#### Conclusion
Connecter des jeux de données Databricks Apache Iceberg à Lakehouse peut aider à activer vos données avec BigQuery. En séparant le traitement du stockage sous-jacent, en adoptant des formats ouverts et en utilisant des API REST standard avec credential vending, on peut exécuter des charges d'ingénierie évolutives et des analyses concurrentes sans migrer de données ni sacrifier la performance.

Combiner les lectures Iceberg de Databricks (UniForm) avec la fédération Lakehouse, la mise en cache Lakehouse, et une maintenance régulière via OPTIMIZE et VACUUM aide à construire un lakehouse efficace et sans copie. Cette approche peut réduire les dépenses de stockage, éviter la maintenance fragile de pipelines, et préparer l'environnement de données pour les analyses modernes et les charges de travail IA émergentes.

Construire une architecture unifiée ne nécessite plus de déplacer des fichiers de données entre plateformes. Il est possible de commencer à interroger des tables Databricks Iceberg en les enregistrant dès aujourd'hui dans le catalogue d'exécution Lakehouse, pour une fédération bidirectionnelle.

## Pourquoi ça compte
Cette fonctionnalité illustre la convergence des architectures data autour des formats ouverts (Iceberg) et de la fédération multicloud, réduisant la dépendance aux pipelines ETL propriétaires entre Databricks et BigQuery — un signal important pour toute équipe data qui doit choisir entre consolidation et interopérabilité entre plateformes.
