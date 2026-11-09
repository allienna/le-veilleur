---
title: "Making Every Core Count: In Pursuit Of Faster Apache Spark Jobs at Uber"
date: 2026-11-09
url: "https://substack.com/redirect/809f5cb9-422c-45b8-9dd7-359eaabe0f0a?j=eyJ1IjoiN3Y1bG1jIn0.HlvPOGYPdVknSYzEK1JIj6IFkAFn8zuyjtfU9Mbft9Q"
authors: ["Xinli Shang", "Sivabalan Narayanan", "Dharshan Tharumia", "Sagar Sumit", "Meenal Binwade", "Vamshi Pasunuru", "Kanan Patel", "Suprit Acharya", "Kumudini Kakwani", "Arnav Balyan", "Nimesh Khandelwal"]
keywords: ["Apache Spark", "Apache Hudi", "Gluten/Velox", "lakehouse", "optimisation de performance", "Uber"]
theme: "Data"
tone: "research"
used_in: ["2026-11-09"]
---

## Résumé

Uber décrit dans cet article d'ingénierie comment elle a cherché à réduire le coût de sa flotte Apache Spark, qui mobilise plus de 200 000 cœurs CPU pour la seule ingestion de données. L'entreprise a d'abord adopté Apache Gluten et Velox pour déporter l'exécution SQL vers un moteur natif vectorisé, obtenant environ 3,5x de gain de vitesse et 3,4x de réduction du coût CPU sur les charges migrées, jusqu'à 79% d'amélioration du temps d'exécution en production, sans changement de code applicatif. Elle a ensuite évalué Onehouse Quanton, un moteur Spark commercial optimisé pour Apache Hudi, sur des données synthétiques représentatives de sa production, mesurant jusqu'à 5,5x de gain en écriture sur une table d'insertion massive et 4,7x sur une table de mise à jour. L'article détaille la méthodologie de benchmark, les résultats phase par phase, et les contributions open source réalisées par Uber dans ce cadre.

## Points clés

- Uber exploite l'une des plus grandes flottes Spark au monde (plus de 500 000 applications/jour, plus d'un million de cœurs, plus de 100 Po lus/écrits par jour), gérée via sa plateforme interne Drogon.
- L'adoption de Gluten/Velox (exécution native vectorisée type SIMD) a produit jusqu'à 98% de réduction de coût et 79% d'amélioration de temps d'exécution sur certains pipelines critiques en production.
- Le choix de la stratégie de shuffle est déterminant : le shuffle natif de Gluten souffre d'un surcoût de conversion colonne/ligne, alors que le shuffle colonnaire de Celeborn apporte un gain moyen d'environ 3,65x.
- Uber a contribué plus de 30 patches (50+ commits) en amont des projets open source Gluten/Velox, portant sur les mécanismes de repli, la sécurité (chiffrement Parquet natif) et le support d'opérateurs/fonctions manquants.
- Le benchmark de Quanton sur la table d'ingestion Hudi montre que le plus grand gain se situe dans la phase d'écriture de la table de données (7,8x plus rapide), alors que la déduplication/indexation et la maintenance de table restent quasiment inchangées voire légèrement plus lentes.
- À itérations égales, Quanton atteint un temps de cycle comparable à Spark OSS en utilisant environ 8 fois moins de cœurs vCPU provisionnés, suggérant un potentiel de réduction de ressources plutôt que de simple accélération.

## Analyse approfondie

### Pourquoi cette enquête

Chez Uber, Spark est au cœur de l'infrastructure data : l'ingestion du data lake consomme à elle seule plus de 200 000 cœurs CPU, et les traitements ETL construits par-dessus en consomment davantage encore. À cette échelle, quelques points de pourcentage d'efficacité représentent un impact réel, ce qui fait de l'optimisation de coût Spark un chantier permanent plutôt qu'un projet ponctuel. La majorité de ce travail passe par Drogon, la plateforme interne de « Spark-as-a-Service » d'Uber, qui contrôle la soumission, la configuration et le déploiement de chaque application Spark, rendant possibles des changements de moteur à l'échelle de toute la flotte.

Pour optimiser l'exécution des requêtes sur certaines charges de production critiques, Uber a adopté Apache Gluten et Velox, qui déportent les opérateurs SQL de Spark vers un moteur natif vectorisé : environ 3,5x de requêtes plus rapides et 3,4x de coût CPU réduit sur les charges migrées, avec des gains de temps d'exécution allant jusqu'à 79%, sans aucune modification du code utilisateur. Uber a par ailleurs contribué plus de 30 patches en amont du projet, et un de ses ingénieurs a été invité à devenir committer Apache Gluten.

En s'appuyant sur ces gains, l'équipe a cherché des améliorations supplémentaires côté ingestion et maintenance de tables, qui représentent la plus grande part du calcul Spark chez Uber. Ces flux de travail vont au-delà des simples opérateurs SQL : ils lisent les données existantes, appliquent des mises à jour, écrivent des fichiers et maintiennent les métadonnées des tables. La plupart des tables du data lake d'Uber sont de simples jeux de données Parquet ; environ 17 200 tables sont gérées avec Apache Hudi, et les charges Hudi représentent une part substantielle du calcul d'ingestion, ce qui fait de leurs chemins de lecture/écriture une cible d'optimisation importante.

Pour évaluer cette opportunité, l'équipe a testé Onehouse Quanton, un moteur Spark candidat « storage-aware », à l'aide de données synthétiques modélisées sur les schémas de production, dans un environnement de test contrôlé. Sur une table de faits de 60 milliards d'enregistrements à dominante d'insertion (1 080 vCPU), le gain médian par cycle d'écriture a été de 5,5x. Sur une table de dimension de 10 milliards d'enregistrements à dominante de mise à jour (3 300 vCPU), le gain a été de 4,7x. Chaque comparaison utilisait la même allocation d'exécuteurs entre Quanton et la base Spark/Hudi open source ; ces résultats excluent les cycles de compaction de métadonnées.

### 1. L'empreinte Spark d'Uber et la vectorisation native avec Gluten/Velox

Apache Spark est depuis longtemps la pierre angulaire de l'infrastructure data d'Uber, de l'analytique aux pipelines de machine learning. Chaque jour, l'infrastructure Spark d'Uber traite plus de 100 Po de données lues et écrites, gère plus de 80 Po de données de shuffle quotidiennes, et exécute des charges couvrant plus de 59 000 empreintes (« fingerprints ») uniques. Elle soutient plus de 500 000 applications par jour, mobilisant plus d'un million de cœurs de calcul.

**Qu'est-ce que Gluten/Velox ?** Apache Gluten est une couche intermédiaire chargée de déporter l'exécution des moteurs SQL basés JVM vers des moteurs natifs comme Velox. Ce déport permet d'exploiter des capacités puissantes comme le SIMD (single instruction multiple data), qui rend l'exécution plus rapide et plus efficace pour des moteurs de calcul comme Spark.

**Benchmarks et résultats.** Sur la base des benchmarks TPC-DS, l'équipe observe une amélioration allant jusqu'à 4x dans le meilleur cas avec 64 exécuteurs, et d'au moins 2,7x dans le pire cas avec 32 exécuteurs sous Gluten, pour une amélioration moyenne globale d'environ 3,4x sur l'ensemble des scénarios.

En comparant requête par requête avec un shuffle natif, le surcoût de conversion colonne-vers-ligne pénalise Gluten sur les requêtes à forte intensité de shuffle : sur une requête donnée, Gluten a mis 1 minute contre 10 secondes pour Spark classique, en raison de ce surcoût de shuffle en ligne. Le shuffle natif de Gluten n'est donc pas optimal et déborde souvent sur disque.

En passant au shuffle colonnaire trié de Celeborn combiné à Gluten, le gain moyen observé est d'environ 3,65x, supérieur aux résultats du shuffle natif, principalement grâce à l'élimination des transformations ligne/colonne pendant le shuffle.

**Résultats en production.** Gluten/Velox a été activé sur certaines charges de production, avec des gains significatifs : jusqu'à 79% d'amélioration moyenne du temps d'exécution, et jusqu'à 98% de réduction de coût sur les pipelines critiques. Le tableau de résultats présenté montre, par exemple, un pipeline passant de 1h07 à 16 minutes (-98% de coût), un autre de 1h15 à 29 minutes (-80%), et un autre de 2h58 à 1h15 (-63%).

**Maturité pour la production.** Pour atteindre une maturité de production à grande échelle, Uber a contribué plus de 30 patches (et 50+ commits) en amont de l'open source. Les travaux clés incluent : des mécanismes de repli (« fallback ») pour atténuer les surcoûts liés aux conversions ligne-colonne et un ajustement de la mémoire (séparation de la mémoire off-heap pour Velox et on-heap pour le reste) ; l'ajout du support du chiffrement/déchiffrement directement dans les lecteurs et écrivains Parquet C++ natifs, pour les pipelines critiques utilisant des fichiers Parquet chiffrés ; et l'implémentation d'opérateurs manquants (Left Semi Join, Existence Join, RangeExec, Collect Limit) ainsi que de fonctions manquantes (unix_timestamp, fonctions de cast, fonctions de date, arrondi de précision, support ANSI, UDF personnalisées).

### 2. Évaluation de Quanton pour l'optimisation « storage-aware »

**Qu'est-ce que Quanton ?** Quanton est le moteur Spark commercial d'Onehouse. Comme l'approche Gluten/Velox décrite plus haut, il utilise une exécution vectorisée native pour accélérer le traitement SQL, mais ajoute aussi des optimisations à la planification des requêtes et à la façon dont les données sont lues, écrites et gérées dans les tables Apache Hudi et Apache Iceberg : des lecteurs natifs gèrent les fonctionnalités propres aux formats de table (logs merge-on-read de Hudi, suppressions Iceberg) avec un I/O pipeliné qui chevauche l'accès aux données et le calcul (Extract) ; des opérateurs vectorisés natifs accélèrent l'exécution SQL tandis que des optimisations du planificateur Spark réduisent le travail redondant comme les scans dupliqués (Transform) ; et des optimisations des opérations d'écriture et de fusion, de création de fichiers, d'indexation et de maintenance de table ciblent le travail nécessaire pour appliquer des changements aux tables existantes (Load). Quanton est conçu pour exécuter sans modification les applications Scala, PySpark et SQL existantes. Cette évaluation s'est concentrée sur le chemin d'écriture, où se concentre la majeure partie du calcul d'ingestion chez Uber ; l'accélération SQL et en lecture de Quanton n'a pas été testée ici.

**Benchmarks et résultats.** L'équipe a testé Quanton dans un environnement contrôlé avec des données synthétiques conçues pour refléter l'échelle, la forme de schéma et les patterns de charge des tables de production d'Uber.

Deux très grandes tables ont été choisies : l'une à plus de 90% d'insertions, l'autre à plus de 90% de mises à jour, pour couvrir les deux scénarios. Dans chaque benchmark, les propriétés de table sont identiques entre les exécutions Spark OSS et Quanton ; les deux tables diffèrent volontairement entre elles. La configuration de cluster et de moteur était proche de la production : Spark 3.5.9 et Hudi 1.1.1 des deux côtés, sur un cluster HDFS dédié et isolé et un Kubernetes on-premise pour les tables de test — pratique standard de benchmarking, sans rapport avec les protections des données de production, permettant d'écarter la variance de latence réseau du cloud public.

La latence par cycle a été mesurée du démarrage d'un job d'écriture au démarrage du suivant, reconstruite à partir des instants de commit Hudi et recoupée avec le Spark History Server. Les deux systèmes déclenchent une compaction de la table de métadonnées environ tous les 6 à 7 commits ; ces cycles sont exclus des chiffres en régime stable afin de ne pas confondre la performance du moteur avec la maintenance de table. Sur la table de faits, le cycle affecté par la compaction a duré 60,42 minutes sous Spark OSS contre 21,27 minutes sous Quanton, un écart de 2,8x plus faible que la performance d'écriture en régime stable.

**Mesurer la mise à l'échelle : Spark OSS contre Quanton.** À l'échelle d'Uber, une question clé pour tout moteur Spark est de savoir comment ses gains évoluent avec la puissance de calcul. L'équipe a rejoué la charge de la table de faits sur des clusters de 141, 564 et 1 128 vCPU (3, 12 et 24 exécuteurs de 47 cœurs et 300 Go chacun), en maintenant fixes la table, l'index et la configuration du moteur, avec 2 commits mesurés par configuration de la même manière.

Le déséquilibre de charge entre tâches (« task skew ») pourrait expliquer une partie de l'écart observé : avec de grandes allocations, quelques tâches longues déterminent le temps de fin d'étape pendant que d'autres cœurs restent inactifs ; avec de petites allocations, les tâches en file peuvent utiliser la capacité disponible en parallèle des tâches longues. La durée médiane des tâches était environ 10 fois plus courte avec Quanton aux deux tailles de cluster testées, bien que confirmer la contribution de l'ordonnancement nécessite une analyse d'utilisation au niveau des étapes.

Le résultat pratique est un temps d'achèvement comparable avec des ressources nettement moindres : Quanton a terminé un cycle d'écriture en 69,8 minutes avec 141 vCPU, contre 78,9 minutes pour Spark OSS avec 1 128 vCPU. À allocation d'exécuteurs fixe, cela correspond à 89% d'heures-vCPU d'exécuteurs provisionnés en moins par cycle. Ces mesures préliminaires ne couvrent que deux commits par configuration mesurée ; l'efficacité soutenue sera évaluée via une intégration en production et des tests de charge complets.

**Analyse des données : où Quanton a réellement progressé.** Le plus grand gain mesuré se situe dans la phase d'écriture de la table de données (SparkRDDWriteClient committant les statistiques), passant de 475,15 à 60,77 minutes, soit un gain de 7,8x. L'écriture de la table de métadonnées s'est également améliorée de 2,8x (de 5,57 à 1,97 minute). Ces résultats montrent que les gains s'étendent aux écritures des tables de données comme des métadonnées.

Les autres phases ont montré peu d'amélioration : la compaction de la table de métadonnées (25,92 contre 25,07 minutes) et le partitionnement des petits fichiers (1,57 contre 1,58 minute) sont restés quasiment inchangés, tandis que la déduplication et l'indexation ont pris environ 9% de temps en plus (25,00 contre 27,22 minutes). Ces mesures aident à identifier les opportunités d'optimisation restantes : accélérer l'écriture des tables de données n'élimine pas les coûts d'indexation, de partitionnement et de maintenance de table.

### 3. Synthèse et pistes futures

L'article présente l'expérience d'Uber dans l'amélioration des performances Spark pour certaines charges de production critiques via l'exécution vectorisée native avec Gluten/Velox. Le choix de la stratégie de shuffle — natif contre Celeborn — a un impact significatif sur la performance des requêtes. L'article présente également le benchmark de Quanton, une distribution Spark d'Onehouse qui ajoute des optimisations à la planification des requêtes et à la gestion de la lecture, de l'écriture et de la maintenance des données dans les tables Apache Hudi et Apache Iceberg. Uber exécute un grand nombre de charges d'ingestion écrites en Spark avec Hudi comme format de table.

L'évaluation de Quanton s'est concentrée sur les pipelines d'ingestion Hudi à forte intensité d'écriture, avec les gains les plus importants mesurés sur les écritures de tables de données. Onehouse décrit Quanton comme accélérant plus largement les charges ETL, y compris les transformations SQL. Uber prévoit d'étendre les tests à d'autres pipelines d'ingestion et d'ETL via une intégration en production et des tests de charge complets, en évaluant la correction, la compatibilité, la fiabilité et la performance soutenue, y compris la maintenance de table et la reprise après panne.

## Pourquoi ça compte

Ce cas d'usage chiffré chez un opérateur à très grande échelle (Uber) illustre concrètement comment l'exécution vectorisée native (Gluten/Velox) et les moteurs « storage-aware » comme Quanton peuvent réduire drastiquement le coût CPU des pipelines Spark/Hudi, un signal utile pour toute équipe data qui envisage de moderniser son infrastructure lakehouse sans réécrire son code applicatif.
