---
title: "Fifty years of the data stack"
date: 2026-10-21
url: "https://elink56e.dataelixir.com/ss/c/u001.-MFUnTWWaQdWz7ZiAG3zQWSOsu4AdascSnR2y9GyrEVuZgGswwlIvjTDWUWHFpUQr_xldVnzm6Aefj1ncqdI34VvsY2qKChw8h2MAAtYRZKJuvLbCfGSHLSlv4YKk4jfEb7NOt1wlij3a6GZw5mfRxgQaI3eThXbGKznRbk_bAeqq3A3g22v_gMqjtJAzNzSrLqk_R2FHfqtW6m2DX-MMvbeyvJ4H8oUIv_Wwo-c3ZE/4v1/4JEsrnusTK635jeU22xpRA/h4/h001.cWjaovFT-fpkC_e2vJpn37p9uYslRxNf5cdlY0BsnKE"
keywords: ["pile de données", "Apache Arrow", "ADBC", "lakehouse", "MCP", "entrepôts cloud"]
theme: "Data"
tone: "opinion"
used_in: ["2026-10-21"]
---

## Résumé
L'article de Columnar présente « Data: The First 50 Years », une chronologie interactive retraçant l'évolution de la pile analytique de données (accès, calcul, stockage) de 1976 à 2026. Il montre comment les systèmes sont passés de monolithes à trois couches distinctes, des bases relationnelles et de SQL aux entrepôts cloud managés, puis au lakehouse et aux tables ouvertes managées. L'auteur, cofondateur de Columnar et contributeur historique au projet Apache Arrow, situe MCP comme une surcouche de coordination plutôt qu'un substitut aux connexions performantes de type ADBC/Arrow. Il conclut que la coexistence croissante de technologies rendra la gestion des connexions de plus en plus stratégique, ce qui est précisément le positionnement de Columnar.

## Points clés
- Le projet « Data: The First 50 Years » (history.columnar.tech) modélise la pile de données en trois couches — accès, calcul, stockage — avec des estimations de part de marché par technologie et par année depuis 1976.
- L'évolution suit une trajectoire claire : fichiers plats et bases hiérarchiques → bases relationnelles/SQL → prolifération de bases propriétaires (années 80) → standardisation via ODBC/JDBC (années 90) → Hadoop et object stores comme S3 (années 2000-2010) → entrepôts cloud managés → lakehouse et tables ouvertes managées (Amazon S3 Tables, Snowflake, Databricks).
- La couche d'accès connaît un nouveau bouleversement : les coding agents facilitent l'adoption de Rust, Go, JavaScript/TypeScript, au-delà des interfaces historiques ODBC/JDBC/DB-API ; Arrow et ADBC apportent un format columnar et des drivers communs inter-langages.
- MCP est vu comme une couche de coordination pour les agents (découverte/invocation d'outils), distincte de l'accès performant aux données : l'auteur juge plus prometteur de combiner MCP pour la coordination et ADBC pour la livraison des résultats Arrow en hors bande.
- Les technologies dominantes du début des années 2000 n'ont pas disparu : elles coexistent avec les nouvelles, contrairement aux systèmes pré-relationnels qui se sont éteints — une dynamique de coexistence durable plutôt que de remplacement.
- L'auteur et ses cofondateurs (David Li, Matt Topol) ont des racines directes dans Arrow et ADBC (David Li en est le créateur, Matt Topol a construit le premier driver ADBC pour un entrepôt cloud, chez Snowflake), ce qui positionne Columnar comme un acteur légitime sur l'interopérabilité des connexions.

## Analyse approfondie
# Cinquante ans de la pile de données

Notre travail chez Columnar s'enracine dans l'histoire des systèmes de données analytiques. Aujourd'hui, nous partageons Data: The First 50 Years, une histoire interactive de la pile de données de 1976 à 2026. Elle retrace comment les systèmes qui exécutent des requêtes analytiques sur des données tabulaires ont évolué de monolithes vers trois couches distinctes, et comment les technologies de chaque couche ont gagné et perdu du terrain.

De haut en bas, les couches sont l'**accès** (comment les applications se connectent et récupèrent les données), le **calcul** (les moteurs qui exécutent les requêtes), et le **stockage** (comment les données sont persistées). La largeur des blocs indique nos estimations de la façon dont le travail analytique de l'année était réparti entre les technologies. Chaque couche totalise 100 %, et le site explique la recherche et la méthodologie derrière ces estimations.

Appuyez sur Play et observez comment un changement dans une couche met la pression sur les autres. La chronologie démarre lentement : le reporting hérité sur fichiers plats et bases de données hiérarchiques cède progressivement la place aux bases de données relationnelles, fondées sur le modèle relationnel d'Edgar F. Codd, et à SQL. Les années 1980 ont vu naître davantage de bases de données, chacune couplant ses propres interfaces, son moteur et son stockage. À mesure que ces produits mûrissaient dans les années 1990, la portabilité est devenue urgente. ODBC, JDBC et les API spécifiques à chaque langage ont offert aux applications des moyens communs de se connecter.

Autour du tournant du millénaire, le calcul et le stockage ont de nouveau commencé à changer rapidement. Hadoop a déplacé davantage d'analytique vers des fichiers partagés, et S3 ainsi que d'autres object stores ont aidé cette séparation à se répandre durant les années 2010. Les équipes ont gagné en flexibilité et ont hérité de la tâche de faire fonctionner ensemble toutes ces pièces.

Les entrepôts cloud managés ont offert un soulagement face à cette charge opérationnelle, connaissant une croissance rapide du milieu des années 2010 jusque dans les années 2020. En retour, des préoccupations renouvelées concernant les coûts et le lock-in ont alimenté l'intérêt pour le lakehouse et les moteurs embarqués interrogeant des tables partagées. Aujourd'hui, les tables ouvertes managées, y compris Amazon S3 Tables et des offres au sein de plateformes comme Snowflake et Databricks, permettent aux fournisseurs de gérer la compaction et la maintenance tout en préservant le choix du moteur, sous réserve des limites d'interopérabilité.

Après des décennies dominées par ODBC, JDBC et DB-API, l'accès est de nouveau en train de changer. Les coding agents facilitent l'adoption par les équipes de Rust, Go et d'autres langages. JavaScript et TypeScript, autrefois périphériques à cette pile, deviennent plus présents à mesure que les frontières entre l'analytique, les systèmes opérationnels et les applications destinées aux consommateurs s'estompent. Les interfaces plus anciennes laissent les développeurs naviguer entre un support inégal des langages et des conversions de données supplémentaires. Arrow et ADBC leur offrent un format columnar commun et des drivers qu'ils peuvent partager entre langages. L'accès aux bases de données basé sur Arrow reste une petite part du graphique, mais son adoption s'accélère.

Notre travail sur ces connexions a commencé bien avant Columnar. Chez Cloudera, j'ai travaillé avec Wes McKinney sur des connexions rapides et portables entre Hive et Impala, et Python et R. Mon co-fondateur David Li et moi avons tous deux contribué à Arrow dès ses débuts, et David a ensuite créé ADBC. Mon co-fondateur Matt Topol a construit le driver Snowflake, le premier driver ADBC pour un entrepôt cloud. Tous les trois, nous siégeons au comité de gestion de projet d'Arrow, et Matt siège également à celui d'Iceberg.

L'accent mis par le graphique sur l'accès, le calcul et le stockage est délibérément réducteur. Il laisse de côté d'autres parties de la pile où l'interopérabilité compte, notamment les catalogues et les couches sémantiques. Nous nous intéressons particulièrement au travail qui s'y déroule via Apache Polaris et Apache Ossie (incubation). Nous laissons également de côté l'évolution rapide des outils d'ingestion et de réplication, le traitement temps réel, et les systèmes de données multimodaux. Les applications au-dessus de ces couches évoluent elles aussi ; nous nous attendons à ce que l'inférence agentique devienne une source de demande dominante.

Nous voyons MCP comme une surcouche au-dessus de la couche d'accès aux bases de données. Il offre aux agents un moyen commun de découvrir et d'invoquer des outils, des bases de données aux agendas. Cela aide les outils à fonctionner à travers les applications d'agents, mais envelopper un driver de base de données dans du JSON-RPC ne rend pas, en soi, la récupération de données plus rapide. Nous voyons plus de potentiel dans le fait que MCP coordonne le travail pendant qu'ADBC livre des résultats Arrow séparément, hors bande.

Un autre motif ressort du graphique : les bases de données et interfaces qui dominaient le début des années 2000 représentent toujours une grande part de la pile actuelle. Elles coexistent avec les technologies plus récentes, contrairement aux systèmes pré-relationnels qui ont largement disparu de l'usage. Nous nous attendons à ce que cette coexistence se poursuive. Davantage de moteurs, de formats et d'applications signifient davantage de connexions à gérer. Nous pensons que l'infrastructure nouvelle la plus précieuse sera celle qui rendra ces choix gérables. C'est ce que nous construisons chez Columnar.

Explorez la chronologie sur history.columnar.tech.

## Notes de bas de page

1. Le titre est un clin d'œil ludique à *Debt: The First 5,000 Years* de David Graeber.
2. Voir la méthodologie. Beaucoup des bases de données présentées sont également largement utilisées dans des systèmes transactionnels, mais seul leur usage en analytique est comptabilisé ici. Un graphique des charges de travail transactionnelles aurait une allure très différente. Malgré des recherches approfondies, la chronologie contient probablement encore des erreurs et des omissions. Si une date, un regroupement ou un pourcentage semble incorrect, ou si une technologie est manquante, les auteurs invitent à leur écrire avec des sources à l'appui.

## Pourquoi ça compte
Cette chronologie offre un cadre historique utile pour resituer les débats actuels (lakehouse, tables ouvertes, Arrow/ADBC, MCP) dans la longue dynamique de coexistence des technologies de données plutôt que dans une logique de remplacement, ce qui est précieux pour toute veille sur l'architecture data et l'essor de l'inférence agentique.
