---
title: "Beyond the Databricks and ClickHouse Benchmarks: From 12k to 125k QPS on Open Tables with StarTree"
date: 2026-11-23
url: "https://substack.com/redirect/aedc08c3-1cf0-4cc0-859d-b9486f6ef4b1?j=eyJ1IjoiN3Y1bG1jIn0.HlvPOGYPdVknSYzEK1JIj6IFkAFn8zuyjtfU9Mbft9Q"
keywords: ["benchmark", "lakehouse", "Apache Pinot", "ClickHouse", "Databricks", "requêtes analytiques temps réel"]
theme: "Data"
tone: "research"
used_in: ["2026-11-23"]
---

## Résumé
L'article, publié par StarTree, revient sur la démonstration de Databricks au Data + AI Summit (lancement de « Lakehouse//RT »), qui prétendait atteindre 12 000 requêtes/seconde (QPS) sur des tables lakehouse là où Snowflake et ClickHouse auraient échoué. StarTree conteste la prémisse selon laquelle Apache Pinot nécessiterait une copie séparée des données, et le démontre via ses propres benchmarks TPC-H Q6 exécutés directement sur des tables externes Iceberg/Delta Lake. Les résultats montrent StarTree servant ~12 000 QPS avec 19 ms de latence P90 sur seulement 242 vCPU, puis jusqu'à 125 300 QPS en ajoutant des serveurs, et une tenue correcte même à 100x plus de données (SF100) grâce à un index Star-Tree. L'article conclut que Pinot, via StarTree, permet de servir des charges analytiques à forte concurrence directement depuis le lakehouse, sans ingestion préalable dans un format propriétaire.

## Points clés
- Databricks a revendiqué 12 000 QPS sur données lakehouse lors de sa démo Lakehouse//RT, sans publier le détail du matériel, des requêtes ou du comportement de cache, rendant le résultat non reproductible.
- ClickHouse a reproduit un scénario TPC-H Q6 comparable mais après avoir chargé les données dans son propre format de stockage natif, et non en interrogeant une table lakehouse externe.
- StarTree (Apache Pinot) a exécuté le même test TPC-H Q6 en interrogeant directement une table Parquet externe enregistrée dans Unity Catalog, sans l'ingérer dans le stockage propre de Pinot.
- Avec seulement 12 nœuds (242 vCPU), StarTree a servi 11 996 QPS à 19,2 ms de P90 sans erreur, contre une estimation d'environ 775 vCPU nécessaires à ClickHouse pour atteindre un débit comparable.
- En montant à 150 serveurs, StarTree a atteint 125 300 QPS à 186 ms de P90, sans changer l'architecture de stockage (toujours Parquet externe, sans cache de résultats).
- En passant de l'échelle SF1 (6 millions de lignes) à SF100 (600 millions de lignes), StarTree a maintenu ~12 000 QPS à 147,8 ms de P90 grâce à l'ajout d'un index Star-Tree, sans augmenter les ressources de calcul.

## Analyse approfondie

### Le défi lancé par Databricks
Lors du Data + AI Summit de juin, Databricks a présenté Lakehouse//RT (nom de code Reyden) en défendant une thèse que StarTree dit partager largement : le service analytique à faible latence et forte concurrence — tableaux de bord orientés client, métriques in-app, et de plus en plus les agents IA — a longtemps été dominé par deux moteurs, Apache Pinot et ClickHouse, tous deux situés hors du lakehouse. Les équipes doivent donc maintenir une seconde copie des données pour obtenir des performances de service. La promesse de Reyden est d'offrir cette performance sans sortir les données des tables Delta.

Deux éléments de cette thèse sont justes selon StarTree : Databricks a cité Pinot comme moteur de référence pour ce type de charge, et a soutenu que le service de requêtes devait devenir une charge de travail de premier plan dans la plateforme de données moderne, et non un système séparé greffé en aval.

Là où StarTree conteste la démonstration, c'est sur la prémisse que Pinot nécessiterait une seconde copie des données. StarTree affirme avoir déjà amené Pinot au niveau du lakehouse, interrogeant des tables externes Iceberg et Delta Lake en place, et que cela était disponible en production avant même l'annonce de Reyden en preview privée.

Lors de la démonstration, Databricks a montré son nouveau moteur de requêtes montant en charge jusqu'à 12 000 QPS sur des données lakehouse, tandis que Snowflake et ClickHouse auraient pris du retard ou planté. StarTree estime qu'il était peu probable que ce soit le dernier mot sur le sujet.

### Puis sont venues les réponses
Snowflake et ClickHouse ont tous deux réagi, ouvrant un débat sur la méthode de benchmark des bases analytiques et sur ce qui était réellement possible.

Le problème pour débattre de la démonstration de Databricks, c'est qu'il n'y a pas grand-chose à examiner : plus de 12 000 QPS ont été montrés sur scène, mais sans publication du matériel, de la configuration des requêtes, ni du comportement de cache — personne ne peut donc reproduire ou dimensionner ce résultat.

La réponse de ClickHouse fournissait davantage d'éléments à analyser. L'entreprise a reconstitué ce qu'elle estimait être la charge de travail — TPC-H Q6 à l'échelle 1 (scale factor 1), avec des paramètres fixes — et publié à la fois sa méthodologie et ses résultats. Un seul nœud ClickHouse Cloud de 30 vCPU a géré environ 420 QPS en maintenant une latence P90 sous la seconde. L'ajout de nœuds a permis de pousser le débit vers 15 000 QPS.

Il existait toutefois une différence importante : ClickHouse avait chargé les données dans son propre format de stockage natif avant d'exécuter le benchmark. C'est une façon raisonnable de démontrer la performance de service de ClickHouse, mais cela ne répondait pas tout à fait à la question posée par Databricks : que se passe-t-il quand les données de référence restent dans le lakehouse ?

La réponse de Snowflake s'est concentrée sur la méthodologie. L'entreprise a fait valoir que Databricks n'avait pas configuré Snowflake comme on le ferait en production, et a publié des exécutions TPC-H à 100 Go et 1 To avec un « Interactive Warehouse ». Ces éléments apportaient du contexte utile, mais n'incluaient pas non plus d'exécution à fort QPS contre des données lakehouse gérées de façon externe.

C'est à ce stade que StarTree a décidé d'agir : ClickHouse avait publié suffisamment de détails pour fournir une charge de travail reproductible. StarTree a donc choisi de reproduire le même test de base, mais en laissant les données dans des tables lakehouse, comme Databricks l'avait proposé à l'origine.

### Le benchmark de StarTree face à la démo de Databricks
StarTree repose sur Apache Pinot, conçu à l'origine par LinkedIn pour l'analytique orientée membres. La forte concurrence de requêtes n'est pas un problème nouveau pour Pinot : des déploiements en production fonctionnent depuis longtemps à plusieurs centaines de milliers de requêtes par seconde, pour des charges où une personne — ou une application — attend souvent la réponse.

Ce qui a changé, c'est l'endroit où Pinot peut opérer. Sur StarTree, Pinot peut interroger des tables externes Iceberg et Delta Lake sans d'abord ingérer leurs lignes dans le format de stockage propre à Pinot, ce qui permet de répondre directement au défi posé par la démonstration de Databricks.

Le test reprend la charge de travail identifiable publiquement par ClickHouse : TPC-H Q6, scale factor 1, les paramètres fixes publiés par ClickHouse, et une génération de charge en « boucle ouverte » (open-loop). La table `lineitem` est restée au format Parquet sur S3 et a été enregistrée dans Unity Catalog comme **table externe**. StarTree a interrogé ces fichiers sans ingérer les lignes dans un stockage géré par Pinot.

StarTree conserve néanmoins un état d'accélération : des index sont placés à côté des données, et les pages Parquet fréquemment consultées sont conservées dans un cache local borné. La table de référence, elle, reste dans le stockage objet plutôt que d'être copiée dans une table native dupliquée.

### Premier test : 12 000 QPS
Le jeu de données TPC-H SF1 contient 6 001 215 lignes `lineitem`. StarTree a utilisé un encodage RAW et des index de plage (range indexes) sur `shipdate`, `discount` et `quantity`.

Le cluster de 12 nœuds comprenait :

| Rôle | Instance | vCPU chacun | Nombre |
|---|---|---|---|
| Serveur | i4g.4xlarge | 16 | 12 |
| Broker | m6g.xlarge | 4 | 12 |
| Contrôleur | m6g.large | 2 | 1 |

Soit 242 vCPU au total. La charge a été générée avec k6 en mode « taux d'arrivée constant », afin que la charge offerte ne diminue pas simplement parce que la base ralentit. Chaque palier de charge a duré 45 secondes.

Résultats :

| QPS offert | QPS servi | P90 | Erreurs |
|---|---|---|---|
| 1 000 | 996 | 12,4 ms | 0 |
| 4 000 | 3 995 | 12,6 ms | 0 |
| 8 000 | 7 990 | 13,9 ms | 0 |
| 12 000 | 11 996 | 19,2 ms | 0 |

À 12 000 QPS offerts, StarTree a servi 11 996 QPS à **19,2 ms de P90, sans aucune erreur**. Le même cluster est resté sous une seconde de P90 jusqu'à environ 16 000 QPS. Ce test répond au défi initial : StarTree a atteint la même classe de concurrence que la démo Databricks, sans charger la table au préalable dans le stockage de Pinot.

### Comparaison entre ClickHouse et StarTree
La configuration ClickHouse comptait 20 nœuds pour 600 vCPU et franchissait le seuil d'une seconde de P90 vers 9 300 QPS environ. La configuration StarTree à 12 nœuds n'utilisait que 240 vCPU (serveurs + brokers) et restait à 19 ms de P90 à 12 000 QPS — une performance supérieure avec beaucoup moins de matériel.

Selon l'analyse de StarTree, la courbe de ClickHouse impliquerait environ 775 vCPU pour atteindre 12 000 QPS tout en restant sous le même seuil d'une seconde de P90. Ce chiffre reste une estimation déduite du graphique, ClickHouse n'ayant pas publié le tableau brut des résultats sous-jacents — mais il reste significatif : StarTree semble nécessiter moins de calcul tout en interrogeant une table Parquet externe, un résultat jugé inattendu.

### Montée en charge jusqu'à 125 000 QPS (ou plus)
Pour tester la scalabilité, StarTree a conservé l'architecture de stockage, les données, la charge de travail Q6 et la méthodologie en boucle ouverte, en ajoutant simplement du calcul. Le nombre de serveurs est passé de 12 à 150 instances i4g.4xlarge, avec 120 brokers à la plus grande échelle.

| Serveurs | QPS maximal | P90 |
|---|---|---|
| 12 | 16 000 | 19 ms |
| 120 | 100 000 | 173 ms |
| 150 | 125 000 | 186 ms |

La configuration à 150 serveurs a atteint **125 300 QPS à 186 ms de P90**. En dessous du maximum :

| QPS observé | P90 |
|---|---|
| 86 900 | 35 ms |
| 103 300 | 75 ms |
| 125 300 | 186 ms |

Au-delà de 100 000 QPS, la P90 restait à 75 ms. Rien dans le chemin de stockage n'a changé pour atteindre ce résultat : les requêtes continuaient d'être servies contre la table externe au format Parquet, sans cache de résultats ni conversion au format natif Pinot Segment. StarTree précise que 125 000 QPS n'est pas une limite intrinsèque de Pinot, mais simplement la limite du budget de test alloué.

### De SF1 à SF100
Une objection évidente : six millions de lignes constituent un petit jeu de données, en particulier pour un système censé interroger de grandes tables lakehouse. StarTree a donc répété l'expérience TPC-H Q6 à l'échelle SF100 :

| Métrique | SF1 | SF100 |
|---|---|---|
| Lignes `lineitem` | 6 001 215 | 600 037 902 |
| Parquet sur S3 | ~200 Mo | ~21 Go |
| Calcul | 242 vCPU | 242 vCPU |

La table SF100 est restée au format Parquet sur S3, avec la même architecture de table externe Unity Catalog et le même cluster de 12 nœuds. À cette échelle, un simple scan Q6 toucherait environ 11,4 millions de lignes par requête — répéter cela des milliers de fois par seconde n'étant pas viable, StarTree a ajouté un **index Star-Tree** sur la table externe, créant une colonne de prix remisé pré-agrégée (`SUM(disc_price)`) sur `shipdate`, `discount` et `quantity`. Cela a réduit le nombre de documents touchés par requête de 114 160 (SF1) à **4 002 (SF100)**.

| Métrique | SF1 | SF100 |
|---|---|---|
| Configuration | RAW + index de plage | RAW + index de plage + Star-Tree |
| Documents/requête | 114 160 | 4 002 |
| QPS offert → servi | 12 000 → 11 996 | 12 000 → 11 969 |
| P90 | 19,2 ms | 147,8 ms |

Exécution complète à SF100 :

| QPS offert | QPS atteint | P90 |
|---|---|---|
| 2 000 | 1 992 | 4,7 ms |
| 4 000 | 3 996 | 20,6 ms |
| 8 000 | 7 985 | 91,0 ms |
| 12 000 | 11 969 | 147,8 ms |
| 14 000 | 13 898 | 221,8 ms |
| 16 000 | 13 922 | 2 739,9 ms |

Avec 100 fois plus de lignes et sans calcul supplémentaire, StarTree a servi près de 12 000 QPS à 147,8 ms de P90 ; à 14 000 QPS offerts, la P90 restait à 221,8 ms, puis le palier serveur a saturé au-delà. Cela ne signifie pas que la taille de la table n'a aucun coût — SF100 utilise une optimisation physique différente car un jeu de données plus volumineux rend les scans répétés inefficaces. Le point important est que cette optimisation (l'index Star-Tree) peut être appliquée directement sur la table externe, sans remplacer la table Parquet ouverte par une copie native Pinot.

### Ce que fait le cache
Ces chiffres correspondent à un état « chaud » (warm-state). Chaque serveur StarTree maintient un cache LRU borné des pages Parquet utilisées par la charge de travail ; les pages absentes localement sont récupérées depuis S3. Le cache contient l'ensemble de travail actif, pas une copie complète de la table. « Interroger directement le lakehouse » ne signifie donc pas aller chercher chaque octet sur S3 à chaque requête : les index réduisent le volume de données concerné, et les pages les plus demandées se rapprochent du calcul. Cela ne signifie pas non plus charger la table entière dans une autre base avant de pouvoir la servir.

### Ce que montrent réellement les résultats de Databricks, ClickHouse, Snowflake et StarTree
Databricks et ClickHouse ont défini le terrain de cette étude ; StarTree affirme les y avoir rejoints. **Databricks** a validé le besoin d'un moteur de requêtes à forte concurrence capable de tourner sur le stockage lakehouse, mais ses benchmarks initiaux ne divulguaient pas assez de détails de configuration pour permettre une reproduction indépendante. **Snowflake** a expliqué que le dimensionnement de l'entrepôt et la configuration de production influencent les résultats, mais sa réponse ne démontrait pas la même charge à fort QPS contre des données lakehouse gérées en externe. **ClickHouse** a publié un test à fort QPS plus reproductible ; l'entreprise a pu égaler la concurrence de Databricks en ajoutant du calcul, mais seulement après avoir importé les données dans le format de stockage natif de ClickHouse.

Selon StarTree, leurs résultats démontrent qu'Apache Pinot, déjà conçu autour du service analytique à forte concurrence, peut désormais appliquer ce modèle à des tables lakehouse externes grâce à StarTree. Dans leur test, StarTree a reproduit le niveau de concurrence général de la démo Databricks sans d'abord ingérer la table source dans un stockage géré par Pinot ; face à la charge publiée par ClickHouse, cela a été fait avec sensiblement moins de calcul ; et en ajoutant des serveurs, la même architecture de table externe a continué de monter au-delà de 125 000 QPS. Faire passer la table source de six millions à 600 millions de lignes n'a pas annulé cette capacité, bien que cela ait nécessité une optimisation différente sous forme d'index Star-Tree.

StarTree nuance toutefois : ce résultat ne doit pas laisser penser que toute requête lakehouse peut devenir une requête de l'ordre de la milliseconde — il existe encore de bonnes raisons de charger les données dans une couche de service dédiée. Mais cela ne doit plus être considéré comme un prérequis pour servir de l'analytique à forte concurrence. Bien que limitée dans son périmètre, cette étude montre comment StarTree peut servir des charges analytiques de type applicatif depuis le lakehouse, en quelques dizaines de millisecondes, à forte concurrence, à grande échelle, et sans exiger l'ingestion préalable de la table dans une couche de service séparée.

### Essayer soi-même
StarTree indique que ses clients font déjà tourner Pinot à plusieurs centaines de milliers de requêtes par seconde, des dizaines de milliards de requêtes par semaine, avec des objectifs de niveau de service (SLO) définis sur le P99 plutôt que le P90. L'entreprise invite les lecteurs dont les données analytiques doivent rester dans un stockage lakehouse ouvert, mais dont les applications consommatrices ont besoin d'une couche de service à faible latence et forte concurrence, à venir tester cette approche sur leur propre charge de travail.

## Pourquoi ça compte
Ce benchmark est utile pour la veille data/infra car il illustre une bataille concurrentielle concrète (Databricks vs ClickHouse vs Snowflake vs StarTree/Pinot) autour d'un enjeu stratégique : servir de l'analytique temps réel à forte concurrence directement sur le lakehouse, sans duplication de données — une tendance clé pour les architectures data modernes et les cas d'usage pilotés par des agents IA.
