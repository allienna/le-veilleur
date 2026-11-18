---
title: "Reverse ETL: BigQuery exports to AlloyDB | Google Cloud Blog"
date: 2026-11-18
url: "https://cloud.google.com/blog/products/data-analytics/reverse-etl-bigquery-exports-to-alloydb/"
authors: ["Jelson A. Cordeiro", "Vinod Ramachandran"]
keywords: ["Reverse ETL", "BigQuery", "AlloyDB", "pipeline de données", "Google Cloud", "PostgreSQL"]
theme: "Data"
tone: "news"
used_in: ["2026-11-18"]
---

## Résumé
Google Cloud annonce la disponibilité générale (GA) de l'export BigQuery vers AlloyDB, une fonctionnalité de Reverse ETL intégrée permettant de synchroniser des données analytiques (OLAP) vers une base transactionnelle (OLTP) via une seule instruction SQL déclarative. L'article illustre ce gain grâce au cas de Copel, un fournisseur d'électricité brésilien, qui a remplacé un pipeline Airflow complexe et fragile par cette approche native. Résultat : suppression du staging intermédiaire sur Cloud Storage, réduction des coûts et de la maintenance, et des débits d'export dépassant 4 millions de lignes par minute sur des champs `JSONB` complexes. L'article invite les équipes data à adopter ce même mécanisme pour d'autres cibles comme Bigtable, Spanner ou Pub/Sub.

## Points clés
- BigQuery propose désormais un export natif en GA vers AlloyDB via une simple instruction SQL `EXPORT DATA`, sans middleware ETL.
- Copel a remplacé une architecture historique en 4 étapes (CSV sur Cloud Storage, tables temporaires, scripts gCloud, bascule transactionnelle) par une connexion directe et parallélisée.
- Les benchmarks de Copel montrent un débit soutenu d'environ 4,2 millions de lignes/minute, y compris sur des données `JSONB` complexes de télémétrie.
- Les bénéfices annoncés : réduction des coûts de stockage intermédiaire, sécurité renforcée (données jamais déversées en CSV lisible), et maintenance quasi nulle grâce à un pipeline Airflow réduit à une seule tâche `BigQueryInsertJobOperator`.
- La fonctionnalité s'étend également à d'autres cibles OLTP/streaming : Bigtable, Spanner et Pub/Sub.

## Analyse approfondie
Combler le fossé entre les systèmes analytiques (OLAP) et les bases de données transactionnelles (OLTP) est notoirement complexe. Synchroniser les données entre ces deux systèmes, souvent appelé Reverse ETL (Extract, Transform, Load), nécessite traditionnellement un middleware lourd, des buckets de staging et une orchestration complexe, en particulier à l'échelle de l'entreprise.

Nous annonçons la disponibilité générale (GA) des exports BigQuery vers AlloyDB, permettant aux équipes d'ingénierie des données d'utiliser une seule instruction SQL déclarative pour exporter des données de BigQuery vers AlloyDB. Cette approche élimine complètement le besoin d'un middleware ETL complexe.

Pour démontrer les bénéfices de cette fonctionnalité, nous présentons comment Copel, un fournisseur d'électricité brésilien, a éliminé un goulot d'étranglement massif lié à l'orchestration et a mis à l'échelle la télémétrie de ses compteurs intelligents en migrant vers un Reverse ETL intégré et haute performance.

### Le défi de la mise à l'échelle de la télémétrie des compteurs intelligents

Chez Copel, la gestion des données de télémétrie provenant de millions de compteurs électriques intelligents est une opération critique. Ces données sont diffusées en continu et consolidées dans une couche analytique « Gold » dans BigQuery. Cependant, pour alimenter les « systèmes d'action » de Copel — tableaux de bord du service client à faible latence, applications mobiles et systèmes de facturation opérationnels — ce riche ensemble de données doit être constamment resynchronisé vers sa base de données transactionnelle haute performance, AlloyDB pour PostgreSQL.

Jusqu'à récemment, Copel orchestrait cette architecture de Reverse ETL via un DAG complexe dans le service managé de Google pour Apache Airflow. Cependant, le processus d'enrichissement et d'exportation de centaines de millions d'enregistrements de BigQuery vers AlloyDB comportait de multiples étapes intermédiaires fragiles :

Figure 1 : l'architecture historique multi-étapes de Copel, nécessitant des dépôts de fichiers dans Cloud Storage et des scripts gCloud séquentiels.

1. BigQuery exécutait des requêtes d'enrichissement et d'extraction, déversant les résultats SQL dans des dizaines de fichiers CSV fragmentés au sein d'un bucket Google Cloud Storage.
2. Apache Airflow exécutait du SQL pour créer des tables temporaires dans AlloyDB afin d'éviter le verrouillage en écriture ou la corruption des données sur les tables de production.
3. Des scripts gCloud séquentiels parcouraient les fichiers CSV de Cloud Storage pour charger les données dans le cluster et les shards AlloyDB correspondants.
4. Enfin, un bloc de transaction SQL supprimait en toute sécurité la table de production et renommait la table temporaire en table de production.

Pour faire fonctionner cette architecture historique, l'équipe de Copel devait maintenir le pipeline, gérer minutieusement le stockage intermédiaire des fichiers, effectuer une impersonation IAM complexe entre plusieurs services, et surveiller en permanence la santé du système de bout en bout.

### La percée : le Reverse ETL intégré

Avec la fonctionnalité `EXPORT DATA` de BigQuery vers AlloyDB, Copel a pu remplacer l'ensemble de cette infrastructure de pipeline multi-étapes par une seule instruction SQL élégante.

Désormais, les exports BigQuery communiquent directement avec les instances AlloyDB via des connexions hautement optimisées et parallélisées — plus besoin de fichiers de staging dans Cloud Storage, de scripts gCloud, ni de gestion de tables temporaires !

Figure 2 : la nouvelle architecture montrant une connexion directe et parallèle de Reverse ETL entre BigQuery et AlloyDB.

Voici à quel point le nouveau processus de Reverse ETL est simple en code :

Les valeurs BigQuery résultantes se mappent parfaitement sur les colonnes d'AlloyDB lors de l'export, laissant les structures imbriquées entièrement interrogeables et indexables côté PostgreSQL.

### Évaluation de la performance et de la scalabilité

Pour valider cette nouvelle architecture, Copel a exécuté deux benchmarks de Reverse ETL à grande échelle : comparant la performance et la scalabilité d'un export incrémental plus modeste à celles d'un export complet de table, bien plus volumineux.

Les résultats de performance ont dépassé toutes les attentes initiales :

**Astuce pratique sur l'ingestion** : soutenir un débit d'export d'environ 4,2 millions de lignes par minute sur des champs de télémétrie `JSONB` complexes constitue une performance technique remarquable. Cela met en lumière les optimisations de bas niveau entre le moteur de traitement distribué de BigQuery et la couche de stockage avancée d'AlloyDB.

### Principaux enseignements et bénéfices

En adoptant cette approche SQL déclarative, Copel a pu supprimer des dizaines de lignes de scripts complexes et de blocs de gestion d'erreurs personnalisés. Leur DAG Airflow ne contient désormais qu'une seule tâche simplifiée `BigQueryInsertJobOperator` qui exécute la requête d'export.

Cette approche intégrée débloque plusieurs bénéfices métier essentiels :

- **Réduction directe des coûts :** en contournant entièrement Cloud Storage, il n'y a plus de coûts de stockage intermédiaire ni de frais associés aux opérations de lecture/écriture d'API.
- **Sécurité des données renforcée :** les données circulent directement de BigQuery vers AlloyDB au sein du réseau interne sécurisé de Google, sans jamais être déversées dans des fichiers CSV lisibles.
- **Maintenance quasi nulle :** les erreurs de pipeline sont désormais contenues dans une seule instruction SQL, ce qui simplifie considérablement le dépannage et la journalisation.
- **Écriture massive et distribuée :** l'export direct a atteint des vitesses d'écriture dépassant 4 millions d'enregistrements par minute, en s'appuyant sur le parallélisme massif de BigQuery combiné à la performance d'écriture PostgreSQL optimisée d'AlloyDB.

Désormais, plutôt que de consacrer de précieuses heures d'ingénierie à surveiller les échecs de pipeline et les buffers de stockage intermédiaires, les équipes d'ingénierie des données peuvent se concentrer sur l'essentiel : offrir des analyses intelligentes et des expériences premium à leurs clients.

### Pour commencer dès aujourd'hui : modernisez votre Reverse ETL

Maintenant que les exports BigQuery vers AlloyDB sont disponibles en général (GA), il n'y a jamais eu de meilleur moment pour simplifier votre architecture de données. Si votre équipe peine avec des pipelines complexes et multi-étapes pour transférer les données BigQuery vers des bases de données OLTP en aval, nous vous invitons à essayer dès aujourd'hui la fonctionnalité d'export intégrée pour AlloyDB, Bigtable, Spanner ou Pub/Sub.

## Pourquoi ça compte
Ce type de Reverse ETL natif simplifie radicalement l'architecture data des entreprises en supprimant une classe entière de middleware et de staging, un signal important pour toute veille sur l'évolution des plateformes cloud analytiques vers des usages opérationnels temps réel.
