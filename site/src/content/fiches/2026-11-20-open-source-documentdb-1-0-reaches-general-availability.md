---
title: "Open Source DocumentDB 1.0 Reaches General Availability"
date: 2026-11-20
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.infoq.com%2Fnews%2F2026%2F11%2Fmongodb-compatible-documentdb%2F%3Futm_source=tldrdata/1/010001a1f382eb1c-813c2c29-0e67-4fcb-a679-689a5eec2cc8-000000/DsRVknoyLw77phwCYJftK9eXJK29-iJ3idWAjbCFNrE=452"
keywords: ["DocumentDB", "MongoDB", "PostgreSQL", "open source", "licence MIT", "FerretDB"]
theme: "Data"
tone: "news"
used_in: ["2026-11-20"]
---

## Résumé
DocumentDB 1.0, base de données documentaire open source sous licence MIT construite sur PostgreSQL et compatible avec le protocole MongoDB, atteint la disponibilité générale (GA). Porté par Microsoft depuis début 2025 puis rattaché à la Linux Foundation avec le soutien d'AWS, Google, Cockroach Labs, Snowflake et Yugabyte, le projet vise à offrir une alternative ouverte à MongoDB (sous licence SSPL). Le choix du nom « DocumentDB » suscite la confusion avec Amazon DocumentDB, et les premières comparaisons de performance avec le projet concurrent FerretDB — qui s'appuie sur les mêmes extensions PostgreSQL — restent préliminaires et non tranchées.

## Points clés
- DocumentDB 1.0 atteint la disponibilité générale (GA) : licence MIT, compatibilité avec le wire protocol MongoDB, la plupart des drivers et requêtes MongoDB fonctionnant sans modification.
- Architecture technique : une extension PostgreSQL compatible API MongoDB + une gateway traduisant les requêtes MongoDB en appels PostgreSQL ; support de PostgreSQL 15 à 18, paquets Linux pour les versions 17/18, opérateur Kubernetes inclus.
- Projet initié par Microsoft en 2025, désormais sous l'égide de la Linux Foundation, avec le soutien d'AWS, Cockroach Labs, Google, Snowflake et Yugabyte.
- La licence MIT, permissive, autorise usage commercial, modification et hébergement sans divulgation du code propriétaire, à l'inverse de la licence SSPL de MongoDB.
- Le nom « DocumentDB » crée de la confusion avec Amazon DocumentDB, critique relayée sur Hacker News malgré une page officielle de désambiguïsation.
- Des benchmarks YCSB (Layerbase) comparant DocumentDB et FerretDB, ainsi qu'une issue GitHub signalant une latence supérieure à MongoDB 9.0.4, donnent des résultats non concluants et non vérifiés de façon indépendante.

## Analyse approfondie
DocumentDB 1.0 est la première version en disponibilité générale (GA) de cette base de données documentaire open source, sous licence MIT, construite sur PostgreSQL et compatible avec le protocole réseau (wire protocol) de MongoDB. La plupart des drivers, outils et requêtes MongoDB fonctionnent sans modification.

DocumentDB se compose d'une extension PostgreSQL qui fournit une fonctionnalité compatible avec l'API MongoDB, ainsi que d'une passerelle (gateway) qui traduit les requêtes du protocole MongoDB en appels PostgreSQL. La version 1.0 prend en charge PostgreSQL 15 à 18 via des images de conteneurs, avec des paquets Linux disponibles pour PostgreSQL 17 et 18, et inclut un opérateur Kubernetes ; cette version GA se concentre sur la sécurité, la stabilité, ainsi que des corrections pour l'indexation, l'agrégation et les requêtes géospatiales.

Microsoft a annoncé ce projet open source début 2025, avec l'objectif d'offrir à la communauté des développeurs un datastore NoSQL construit sur PostgreSQL, en donnant une visibilité complète sur l'architecture et l'implémentation du moteur. Le projet a rejoint la Linux Foundation quelques mois plus tard, avec le soutien d'autres grandes organisations du monde des bases de données, dont AWS, Cockroach Labs, Google, Snowflake et Yugabyte. Dans un récent article intitulé « DocumentDB and the MIT License: What to Know Before You Build, Deploy, and Distribute » (« DocumentDB et la licence MIT : ce qu'il faut savoir avant de développer, déployer et distribuer »), l'équipe explique comment la licence MIT permissive de DocumentDB autorise l'usage commercial, la modification et l'hébergement sans obligation de divulguer le code propriétaire, contrairement à la licence SSPL de MongoDB.

Même si le projet propose une page de désambiguïsation du nom « DocumentDB », couvrant le projet open source, Azure DocumentDB et Azure Cosmos DB, la communauté reste perplexe face à ce choix. Dans un fil Hacker News très suivi, l'utilisateur *marifjeren* écrit :

> Appelez-le n'importe comment d'autre, pour l'amour de Dieu. DocumentDB, c'est déjà le nom que tout le monde utilise pour désigner Amazon DocumentDB.

Avec désormais plusieurs options open source sur le marché, Patty Chow, product manager chez Microsoft, explique pourquoi les bases de données documentaires open source ont besoin de plusieurs implémentations afin d'offrir aux développeurs davantage de choix en matière de déploiement et d'infrastructure, tout en préservant la compatibilité avec les drivers et requêtes MongoDB. Chow écrit :

> MongoDB a offert aux développeurs une façon largement répandue de travailler avec des données documentaires. Les drivers familiers et les modèles de requêtes méritent d'être préservés. Les implémentations alternatives donnent aux développeurs l'occasion de continuer à exploiter ces connaissances tout en évaluant différentes approches de stockage et de déploiement.

Dans un fil Reddit, certains praticiens font part de leurs inquiétudes concernant la compatibilité actuelle avec MongoDB et la confusion avec des produits portant des noms similaires. L'utilisateur *716green* commente :

> La compatibilité entre MongoDB et FerretDB a été absolument minimale, bien en deçà de ce à quoi on pourrait s'attendre. Je suis fan de DocumentDB depuis longtemps et j'adore que Microsoft soutienne FerretDB.

DocumentDB fournit les extensions PostgreSQL ainsi que sa propre passerelle compatible MongoDB, tandis que FerretDB est un projet distinct qui utilise les extensions de DocumentDB comme backend et propose sa propre interface compatible MongoDB.

Layerbase a récemment mené une comparaison initiale entre FerretDB et DocumentDB (basé sur PostgreSQL) à l'aide de benchmarks YCSB, constatant que DocumentDB offrait un débit de lecture supérieur de 20 à 33 %, tandis que FerretDB présentait une latence de queue (tail latency) plus faible pour les mises à jour dans des charges de travail mixtes, tout en précisant que ces résultats ne sont pas concluants. Une issue GitHub ouverte signale une latence de requête plus élevée dans DocumentDB 1.0 que dans MongoDB 9.0.4 sur plusieurs charges de travail, mais ces résultats n'ont pas été vérifiés de manière indépendante.

Les notes de version de DocumentDB incluent des chemins de mise à niveau et les problèmes connus. Le projet prévoit des filières distinctes de support à long terme et de développement, sa politique de versionnement étant encore en discussion.

## Pourquoi ça compte
Ce lancement illustre la montée en puissance des alternatives open source « compatibles MongoDB » adossées à PostgreSQL, portées par un consortium de poids (Microsoft, AWS, Google, Linux Foundation) — un signal à suivre pour quiconque évalue des options NoSQL ouvertes, même si la maturité réelle en termes de performance et de compatibilité reste à confirmer.
