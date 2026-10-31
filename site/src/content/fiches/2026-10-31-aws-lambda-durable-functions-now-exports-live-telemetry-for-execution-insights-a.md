---
title: "AWS Lambda durable functions now exports live telemetry for execution insights - AWS"
date: 2026-10-31
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Faws.amazon.com%2Fabout-aws%2Fwhats-new%2F2026%2F10%2Flambda-durable-telemetry%3Futm_source=tldrit/1/010001a18cc0296b-47ed0e76-3d7e-4e1d-a64c-db183e101824-000000/bEovQPc1mpGSj8p2M58I0xIIcyEbrtGsQNsR25PahPM=452"
keywords: ["AWS Lambda", "télémétrie", "observabilité", "MCP", "fonctions durables"]
theme: "Data"
tone: "news"
used_in: ["2026-10-31"]
---

## Résumé
AWS lance l'Exporteur de Télémétrie d'Exécution Durable, un plugin d'observabilité pour les fonctions durables de Lambda, qui capture l'historique détaillé des exécutions et l'envoie vers une ou plusieurs destinations au choix. AWS publie également un serveur Model Context Protocol (MCP) compagnon permettant à des agents IA comme Kiro d'interroger ces données de télémétrie exportées en langage naturel. Le plugin prend en charge 13 destinations intégrées, dont CloudWatch Logs, S3/Athena, DynamoDB, Aurora et OpenSearch Service, avec options de masquage des champs sensibles et d'échantillonnage. Disponible pour TypeScript, Python, Java et Go, sans surcoût, dans toutes les régions AWS supportant les fonctions durables Lambda.

## Points clés
- Nouveau plugin : l'Exporteur de Télémétrie d'Exécution Durable capture l'historique pas-à-pas des exécutions durables Lambda.
- 13 destinations intégrées disponibles, incluant CloudWatch Logs, S3 (via Athena), DynamoDB, Aurora et OpenSearch Service.
- Serveur MCP compagnon permettant aux agents IA (ex. Kiro) d'interroger les données de télémétrie en langage naturel.
- Fonctionnalités de contrôle des données : masquage des champs sensibles et taux d'échantillonnage réglable.
- Disponible gratuitement, pour TypeScript, Python, Java et Go, dans toutes les régions AWS supportant les fonctions durables Lambda.

## Analyse approfondie
# AWS Lambda durable functions now exports live telemetry for execution insights

AWS Lambda annonce le plugin Exporteur de Télémétrie d'Exécution Durable (Durable Execution Telemetry Exporter) pour les fonctions durables Lambda. Ce nouveau plugin d'observabilité capture l'historique étape par étape de vos exécutions durables et les envoie vers une ou plusieurs destinations de votre choix. Vous pouvez utiliser les données exportées pour recueillir des informations opérationnelles et métier, et conserver un historique au-delà de la période de rétention standard. Nous publions également un serveur Model Context Protocol (MCP) compagnon qui permet à des agents IA tels que Kiro d'interroger vos données de télémétrie exportées en langage naturel.

Les fonctions durables Lambda vous aident à construire des applications multi-étapes résilientes et des workflows d'IA pouvant s'exécuter jusqu'à un an. Le nouvel Exporteur de Télémétrie envoie des données telles que le statut d'exécution, le timing des opérations, les entrées et sorties des étapes, et les erreurs vers 13 destinations intégrées. Les destinations incluent Amazon CloudWatch Logs, Amazon S3 pour Amazon Athena, Amazon DynamoDB, Amazon Aurora et Amazon OpenSearch Service. Vous pouvez masquer les champs sensibles avant l'export et définir un taux d'échantillonnage pour contrôler le volume de données. Avec le serveur MCP, un ingénieur d'astreinte peut demander à un agent IA de lister les exécutions récemment échouées et d'en trouver la cause, et un analyste métier peut retrouver toutes les transactions d'un client spécifique.

L'exportateur est disponible pour TypeScript, Python, Java et Go. Pour démarrer, installez l'exportateur, enregistrez le plugin dans le gestionnaire de votre fonction, puis ajoutez le serveur MCP à votre agent.

L'Exporteur de Télémétrie d'Exécution Durable est disponible sans surcoût dans toutes les régions AWS prenant en charge les fonctions durables Lambda. Pour en savoir plus, consultez la documentation du SDK d'Exécution Durable et l'article de blog.

## Pourquoi ça compte
Cette annonce illustre la convergence entre observabilité cloud traditionnelle et agents IA : exposer la télémétrie d'exécution via un serveur MCP ouvre la voie à des workflows de debugging et d'analyse métier pilotés en langage naturel, une tendance à surveiller dans l'écosystème serverless.
