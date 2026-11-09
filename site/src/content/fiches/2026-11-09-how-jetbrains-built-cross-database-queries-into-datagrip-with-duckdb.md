---
title: "How JetBrains Built Cross-Database Queries into DataGrip with DuckDB"
date: 2026-11-09
url: "https://substack.com/redirect/fddebd3a-0edb-4809-b300-70c949dc431d?j=eyJ1IjoiN3Y1bG1jIn0.HlvPOGYPdVknSYzEK1JIj6IFkAFn8zuyjtfU9Mbft9Q"
keywords: ["DuckDB", "DataGrip", "JetBrains", "requêtes inter-bases", "SQL", "custom table functions"]
theme: "Data"
tone: "news"
used_in: ["2026-11-09"]
---

## Résumé
JetBrains a intégré le moteur DuckDB dans DataGrip, son IDE pour bases de données, afin de répondre à une demande récurrente des utilisateurs : pouvoir joindre, en une seule requête, des données provenant de connexions à différentes bases. Plutôt que de développer son propre moteur de requêtes inter-bases, l'équipe a choisi DuckDB pour la simplicité de son intégration, notamment grâce à son système de « custom table functions ». Les développeurs peuvent désormais joindre des données issues de PostgreSQL, MySQL, MongoDB ou d'autres bases prises en charge, sans infrastructure supplémentaire, sachant que ces requêtes sont écrites dans le dialecte SQL propre à DuckDB. Il s'agit d'une première version : JetBrains compte observer les usages réels avant d'exploiter davantage les optimisations de DuckDB et d'étendre l'approche aux sources de données basées sur des fichiers.

## Points clés
- Demande historique des utilisateurs de DataGrip : exécuter une requête unique joignant des données de plusieurs connexions à des bases différentes.
- JetBrains a comparé plusieurs options (Apache Calcite, une solution interne basée sur PSI, H2) avant de retenir DuckDB pour la facilité de son intégration.
- La fonctionnalité clé ayant fait pencher la balance : les « custom table functions » de DuckDB, qui permettent de le connecter directement au moteur d'exécution de requêtes déjà présent dans DataGrip.
- DuckDB apporte aussi des optimisations avancées (comme le projection pushdown) que des alternatives plus légères comme H2 n'offraient pas facilement.
- Les requêtes inter-bases sont explicitement écrites dans le dialecte SQL de DuckDB, et DataGrip le signale clairement à l'utilisateur ; JetBrains a même ajouté la coloration syntaxique dédiée à DuckDB, y compris la syntaxe introduite dans DuckDB 2.0.
- Il s'agit d'une première version : les prochaines étapes envisagées sont une exploitation plus poussée des optimisations de DuckDB et son usage pour des sources de données basées sur des fichiers.

## Analyse approfondie
Lorsque JetBrains a voulu permettre aux développeurs de joindre des données provenant de connexions à des bases différentes au sein d'une seule requête, l'entreprise a choisi de ne pas construire son propre moteur de requêtes inter-bases. À la place, DataGrip, son IDE dédié aux bases de données, embarque DuckDB pour exécuter ces requêtes, et expose directement aux développeurs le dialecte SQL de DuckDB.

Comme le résume Ilia Epelbaum, de l'équipe DataGrip chez JetBrains : « DuckDB s'est avéré être l'option la plus simple à intégrer. »

DataGrip est l'IDE de JetBrains consacré au travail sur les bases de données et à l'écriture de SQL, développé depuis 2015. Les mêmes fonctionnalités sont également disponibles sous forme de plugin dans les autres IDE de JetBrains, ce qui élargit considérablement la portée de cette fonctionnalité au-delà de DataGrip lui-même.

Depuis longtemps, les utilisateurs demandaient une chose en particulier : pouvoir exécuter une seule requête portant sur plusieurs sources de données à la fois. La demande la plus fréquente consistait à joindre des données provenant de connexions différentes au sein d'une même requête. DataGrip pouvait déjà exécuter des requêtes sur chaque connexion séparément, mais rien ne permettait de relier les résultats entre eux — l'équipe avait donc besoin d'un moteur capable de le faire.

JetBrains a exploré plusieurs pistes : Apache Calcite, une gestion interne des requêtes via PSI (Program Structure Interface, la représentation de code interne utilisée par JetBrains dans l'ensemble de ses IDE), et DuckDB.

C'est finalement la simplicité d'intégration qui a fait gagner DuckDB. La fonctionnalité décisive a été la possibilité d'enregistrer une fonction de table personnalisée (« custom table function ») : cela a offert à JetBrains un moyen direct de relier DuckDB au système d'exécution de requêtes déjà présent dans DataGrip. DuckDB a également été préféré à des alternatives plus légères comme H2, car il apportait davantage de capacités, notamment des optimisations de requêtes telles que le « projection pushdown ».

Maxim Sobolevskiy, responsable de l'écosystème bases de données chez JetBrains, formule le résultat en termes concrets : « Avec DuckDB et son support des fonctions de table personnalisées, les requêtes inter-bases sont enfin devenues praticables dans DataGrip. Les utilisateurs peuvent joindre des données issues de PostgreSQL, MySQL, MongoDB, ou de toute autre base prise en charge, au sein d'une même requête, sans avoir à mettre en place d'infrastructure supplémentaire. » Les alternatives embarquées évaluées par l'équipe ne permettaient pas cela, car, selon lui, « les étendre aurait nécessité soit du code natif, soit une implémentation complexe ».

Epelbaum connaissait bien ce terrain avant de rejoindre le projet : il avait été développeur de bases de données sur Trino avant de passer à l'outillage pour bases de données, et connaissait déjà la flexibilité de DuckDB. Cette expérience explique en partie pourquoi l'équipe s'est tournée vers cet outil plutôt que d'écrire et de maintenir son propre moteur de requêtes inter-bases.

Les développeurs savent que DuckDB est à l'œuvre. Comme une jointure entre sources passe par une fonction de table DuckDB, la requête elle-même est écrite dans le dialecte SQL de DuckDB, et DataGrip le signale explicitement aux développeurs. « Nous mettons en avant le fait qu'il s'agit de DuckDB », explique Epelbaum, afin que quiconque écrit une jointure entre connexions sache qu'il écrit une requête DuckDB.

JetBrains est allé plus loin en prenant en charge DuckDB comme dialecte à part entière, et non plus seulement comme moteur sous-jacent aux jointures inter-sources. Epelbaum a lui-même contribué à la coloration syntaxique de DuckDB, y compris pour la syntaxe introduite dans DuckDB 2.0.

Il s'agit encore d'une première version. « Nous avons construit la solution initiale, et nous voulons voir comment les utilisateurs s'en servent réellement en pratique », indique Epelbaum. Ce n'est qu'ensuite que l'équipe prévoit d'ajouter davantage des optimisations propres à DuckDB.

Deux directions figurent sur la feuille de route : d'une part, tirer pleinement parti des optimisations de requêtes de DuckDB ; d'autre part, utiliser DuckDB pour les sources de données basées sur des fichiers, en lisant les fichiers de la même façon qu'il lit déjà à travers les connexions. Epelbaum souligne aussi que le SQL « convivial » de DuckDB est une qualité que l'équipe apprécie dans son usage quotidien.

Pour l'instant, DuckDB est au cœur d'une fonctionnalité que les utilisateurs de JetBrains réclamaient depuis des années, leur permettant de joindre leurs bases de données sans que JetBrains n'ait eu à devenir lui-même un éditeur de moteur de requêtes pour y parvenir.

JetBrains conçoit des outils professionnels pour développeurs, dont IntelliJ IDEA, PyCharm et le langage Kotlin, utilisés par des millions de programmeurs depuis plus de 20 ans. DataGrip, son IDE pour bases de données, aide les développeurs et ingénieurs data à interroger, explorer et gérer plusieurs bases depuis un seul environnement.

## Pourquoi ça compte
Ce cas illustre une tendance de fond dans l'outillage data : plutôt que de réinventer un moteur de requêtes, les éditeurs intègrent des moteurs analytiques embarqués comme DuckDB pour accélérer le développement de fonctionnalités avancées (requêtes fédérées, optimisations) tout en réduisant la dette technique à long terme.
