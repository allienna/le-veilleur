---
title: "Fifty years of the data stack"
date: 2026-10-28
url: "https://elink56e.dataelixir.com/ss/c/u001.-MFUnTWWaQdWz7ZiAG3zQWSOsu4AdascSnR2y9GyrEVuZgGswwlIvjTDWUWHFpUQr_xldVnzm6Aefj1ncqdI34VvsY2qKChw8h2MAAtYRZKJuvLbCfGSHLSlv4YKk4jfEb7NOt1wlij3a6GZw5mfRxgQaI3eThXbGKznRbk_bAeqq3A3g22v_gMqjtJAzNzSrLqk_R2FHfqtW6m2DX-MMvbeyvJ4H8oUIv_Wwo-c3ZE/4v8/Ta7YDp2DSwWtaVWcP8Q17w/h16/h001.jK5Y3JGMevlZ01jRCC0145TIju_nzcXWeJv0E8piWPE"
keywords: ["pile de données", "bases de données analytiques", "Apache Arrow", "ADBC", "lakehouse", "MCP"]
theme: "Data"
tone: "opinion"
used_in: ["2026-10-28"]
---

## Résumé
Cet article de blog de Columnar présente "Data: The First 50 Years", une chronologie interactive retraçant l'évolution de la pile de données analytiques de 1976 à 2026. Il montre comment les systèmes analytiques sont passés de monolithes à trois couches distinctes — accès, calcul et stockage — chacune ayant connu des vagues successives de technologies dominantes (bases relationnelles, Hadoop, entrepôts cloud managés, lakehouse, tables ouvertes managées). Les auteurs, issus de l'écosystème Apache Arrow et ADBC, soutiennent que malgré l'émergence constante de nouvelles technologies, les anciennes coexistent plutôt que de disparaître, rendant l'interopérabilité de plus en plus cruciale. Ils positionnent MCP comme une surcouche de coordination pour les agents, complémentaire — et non substituable — à ADBC pour le transfert rapide de données.

## Points clés
- La pile de données analytiques se décompose en trois couches (accès, calcul, stockage), chacune ayant basculé entre monolithes et composants séparés au fil de cinq décennies.
- Les bases relationnelles et SQL, nées du modèle d'Edgar F. Codd, ont supplanté le reporting sur fichiers plats dans les années 1980-1990 ; ODBC/JDBC ont ensuite standardisé l'accès.
- Hadoop puis S3/object stores ont séparé calcul et stockage dans les années 2000-2010 ; les entrepôts cloud managés ont ensuite allégé la charge opérationnelle, avant que les coûts et le lock-in ne relancent l'intérêt pour le lakehouse et les tables ouvertes managées (Amazon S3 Tables, Snowflake, Databricks).
- Arrow et ADBC émergent comme nouveau standard columnar multi-langages (Rust, Go, JavaScript/TypeScript), porté par les agents de codage, mais restent encore minoritaires dans l'accès aux données.
- MCP est présenté comme une couche de coordination pour les agents (découverte et invocation d'outils), distincte d'ADBC qui reste responsable du transfert performant des résultats Arrow.
- Contrairement aux systèmes pré-relationnels, les technologies des années 2000 (bases et interfaces) continuent de coexister avec les nouvelles, un phénomène que les auteurs anticipent voir se poursuivre.

## Analyse approfondie
Notre travail chez Columnar s'enracine dans l'histoire des systèmes de données analytiques. Nous partageons aujourd'hui Data: The First 50 Years, une histoire interactive de la pile de données de 1976 à 2026. Elle retrace comment les systèmes exécutant des requêtes analytiques sur des données tabulaires ont évolué de monolithes vers trois couches distinctes, et comment les technologies de chaque couche ont gagné ou perdu du terrain.

De haut en bas, les couches sont l'accès (comment les applications se connectent et récupèrent les données), le calcul (les moteurs qui exécutent les requêtes) et le stockage (comment les données sont persistées). La largeur des blocs représente nos estimations de la répartition du travail analytique de l'année entre les technologies. Chaque couche totalise 100 %, et le site explique la recherche et la méthodologie derrière ces estimations.

Appuyez sur Play et observez comment un changement dans une couche met les autres sous pression. La chronologie démarre lentement : le reporting historique sur fichiers plats et bases de données hiérarchiques cède progressivement la place aux bases de données relationnelles, fondées sur le modèle relationnel d'Edgar F. Codd, et à SQL. Les années 1980 ont vu apparaître davantage de bases de données, chacune couplant ses propres interfaces, son moteur et son stockage. À mesure que ces produits arrivaient à maturité dans les années 1990, la portabilité est devenue urgente. ODBC, JDBC et les API spécifiques à chaque langage ont offert aux applications des moyens communs de se connecter.

Autour du tournant du millénaire, le calcul et le stockage ont de nouveau commencé à changer rapidement. Hadoop a déplacé davantage d'analytique vers des fichiers partagés, et S3 ainsi que d'autres object stores ont contribué à répandre cette séparation durant les années 2010. Les équipes ont gagné en flexibilité, mais ont aussi hérité de la tâche de faire fonctionner ensemble toutes ces pièces.

Les entrepôts cloud managés (cloud warehouses) ont allégé ce fardeau opérationnel, connaissant une croissance rapide du milieu des années 2010 jusqu'aux années 2020. En retour, des inquiétudes renouvelées concernant les coûts et le lock-in ont nourri l'intérêt pour le lakehouse et les moteurs embarqués interrogeant des tables partagées. Aujourd'hui, les tables ouvertes managées (managed open tables), notamment Amazon S3 Tables et les offres intégrées à des plateformes comme Snowflake et Databricks, permettent aux fournisseurs de gérer la compaction et la maintenance tout en préservant le choix du moteur, dans la limite de l'interopérabilité.

Après des décennies dominées par ODBC, JDBC et DB-API, l'accès évolue à nouveau. Les agents de codage (coding agents) facilitent l'adoption par les équipes de Rust, Go et d'autres langages. JavaScript et TypeScript, autrefois périphériques à cette pile, gagnent en importance à mesure que les frontières entre l'analytique, les systèmes opérationnels et les applications destinées aux consommateurs s'estompent. Les interfaces plus anciennes laissent les développeurs composer avec un support inégal des langages et des conversions de données supplémentaires. Arrow et ADBC leur offrent un format columnar commun et des drivers qu'ils peuvent partager entre langages. L'accès aux bases de données basé sur Arrow ne représente encore qu'une petite part du graphique, mais son adoption s'accélère.

Notre travail sur ces connexions a commencé bien avant Columnar. Chez Cloudera, j'ai travaillé avec Wes McKinney sur des connexions rapides et portables entre Hive et Impala, et Python et R. Mon co-fondateur David Li et moi avons tous deux contribué à Arrow dès ses débuts, et David a ensuite créé ADBC. Mon co-fondateur Matt Topol a construit le driver Snowflake, le premier driver ADBC pour un entrepôt cloud. Nous siégeons tous les trois au comité de gestion du projet (PMC) Arrow, et Matt siège également à celui d'Iceberg.

L'accent mis par le graphique sur l'accès, le calcul et le stockage est délibérément réducteur. Il laisse de côté d'autres parties de la pile où l'interopérabilité compte, notamment les catalogues et les couches sémantiques. Nous nous intéressons particulièrement aux travaux qui s'y déroulent via Apache Polaris et Apache Ossie (en incubation). Nous laissons aussi de côté l'évolution rapide des outils d'ingestion et de réplication, le traitement temps réel et les systèmes de données multimodaux. Les applications situées au-dessus de ces couches évoluent elles aussi ; nous nous attendons à ce que l'inférence agentique devienne une source de demande dominante.

Nous considérons MCP comme une surcouche (overlay) au-dessus de la couche d'accès aux bases de données. Il offre aux agents un moyen commun de découvrir et d'invoquer des outils, des bases de données aux calendriers. Cela aide les outils à fonctionner à travers différentes applications d'agents, mais envelopper un driver de base de données dans du JSON-RPC ne rend pas, en soi, la récupération des données plus rapide. Nous voyons davantage de promesse dans un MCP qui coordonne le travail tandis qu'ADBC livre les résultats Arrow séparément, hors bande (out of band).

Un autre motif se dégage du graphique : les bases de données et interfaces qui dominaient au début des années 2000 représentent encore une grande partie de la pile actuelle. Elles coexistent avec des technologies plus récentes, à la différence des systèmes pré-relationnels qui ont largement disparu de l'usage. Nous pensons que cette coexistence va se poursuivre. Davantage de moteurs, de formats et d'applications signifie davantage de connexions à gérer. Nous croyons que l'infrastructure nouvelle la plus précieuse sera celle qui rendra ces choix gérables. C'est ce que nous construisons chez Columnar.

Explorez la chronologie sur history.columnar.tech.

### Notes de bas de page
1. Le titre est un clin d'œil espiègle à *Debt: The First 5,000 Years* de David Graeber.
2. Voir la méthodologie. Beaucoup des bases de données présentées sont également largement utilisées dans des systèmes transactionnels, mais seul leur usage analytique est comptabilisé ici. Un graphique des charges transactionnelles aurait une allure très différente. Malgré des recherches approfondies, la chronologie contient probablement encore des erreurs et des omissions. Si une date, un regroupement ou un pourcentage semble incorrect, ou si une technologie est manquante, envoyez un email à [email protected] avec des sources à l'appui.

## Pourquoi ça compte
Cette rétrospective éclaire les tendances actuelles (lakehouse, tables ouvertes, Arrow/ADBC, montée en puissance de MCP pour les agents) en les replaçant dans une dynamique longue de 50 ans d'alternance entre consolidation et fragmentation de la pile de données, utile pour anticiper les choix d'architecture data à venir.
