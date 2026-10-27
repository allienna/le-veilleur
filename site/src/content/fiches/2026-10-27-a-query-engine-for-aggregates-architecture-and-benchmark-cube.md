---
title: "A Query Engine for Aggregates — Architecture and Benchmark | Cube"
date: 2026-10-27
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fcube.dev%2Fresources%2Finside-cube-store%3Futm_source=tldrdata%26utm_medium=newsletter%26utm_campaign=Secondary10262026%26utm_content=secondary-ad_cta_ebook/1/010001a177b312eb-e5823126-cfe6-4c86-8941-97d3b5c4bf0c-000000/WZ-c_-5lsDlE2QY4wlDJqeX1BvBUG2cpCPASVAufHWE=452"
keywords: ["Cube Store", "moteur de requêtes", "agrégats pré-calculés", "benchmark TPC-H", "architecture de données", "analytique embarquée"]
theme: "Software"
tone: "research"
used_in: ["2026-10-27"]
---

## Résumé
Cet ebook gratuit de 18 pages publié par Cube présente l'architecture de Cube Store, un moteur de requêtes spécialisé dans les données pré-agrégées, ainsi qu'un benchmark de performance dérivé de TPC-H. Il détaille le fonctionnement interne du moteur (routeur, workers, coordinateur), les mécanismes d'indexation et de partitionnement, et rapporte 43 combinaisons de mesures de requêtes et d'échelle issues de 11 requêtes TPC-H adaptées. Les résultats montrent des médianes de latence comprises entre 173 et 620 ms et des valeurs p90 entre 291 et 879 ms (temps réseau inclus), en mesurant la latence par requête individuelle plutôt que le débit en conditions concurrentes. Le document propose également une méthode pratique pour évaluer la couverture des agrégats et tester son propre workload.

## Points clés
- Cube Store est conçu pour servir des données pré-agrégées à des tableaux de bord internes, de l'analytique embarquée et des agents d'investigation nécessitant disponibilité et réactivité.
- La capacité à réutiliser un rollup dépend des mesures, dimensions, filtres et de la granularité temporelle de la requête.
- L'ordre physique des données influence le filtrage et le regroupement ; chaque index supplémentaire a un coût de construction et de stockage.
- Les plages de partitions et les statistiques Parquet réduisent le volume de données lues, tandis que le « warmup » rend les données disponibles localement pour les workers.
- Le benchmark couvre 43 combinaisons de requêtes et d'échelle, issues de 11 requêtes TPC-H adaptées, avec une méthodologie et des limites de mesure explicitées.
- Les résultats mesurent la latence individuelle des requêtes (173-620 ms en médiane, 291-879 ms en p90, réseau inclus), pas le débit en situation de concurrence.

## Analyse approfondie
**Architecture et benchmark de performance de Cube Store**

Cet ebook couvre l'architecture de Cube Store ainsi qu'un benchmark de performance dérivé de TPC-H. Découvrez comment le moteur sert des données pré-agrégées, puis explorez les 43 mesures de requêtes et d'échelle rapportées, la méthodologie employée, et ce que les résultats permettent d'établir.

Comment le moteur fonctionne, ce que le benchmark a mesuré, et comment évaluer votre propre workload.

Comment les mesures, dimensions, filtres et la granularité temporelle déterminent si une requête peut réutiliser un rollup.

Pourquoi l'ordre physique des données compte pour le filtrage et le regroupement, et ce que coûte chaque index supplémentaire en construction et en stockage.

Comment les plages de partitions et les statistiques Parquet réduisent les lectures, tandis que le warmup rend les données disponibles localement pour les workers.

Les rôles du routeur, des workers et du coordinateur, ainsi que les ressources nécessaires pour maintenir les données préparées à jour.

Les 43 combinaisons de requêtes et d'échelle rapportées, issues de 11 requêtes TPC-H adaptées, incluant la configuration et les limites de mesure.

Une séquence pratique pour vérifier la couverture des agrégats, inspecter les index et les partitions, et tester le trafic concurrent.

Les tableaux de bord internes, l'analytique embarquée et les investigations menées par des agents ont tous besoin de données préparées pour rester disponibles et répondre rapidement. Ce guide explique l'ingénierie derrière Cube Store et comment l'évaluer au regard des schémas de requêtes et des exigences de fraîcheur de votre application.

18 pages, gratuit. Le benchmark rapporte des médianes de 173 à 620 ms et des valeurs p90 de 291 à 879 ms, temps réseau inclus. Il mesure la latence individuelle des requêtes, pas le débit en conditions concurrentes.

Lisez l'architecture, les tableaux complets du benchmark, et le guide d'évaluation du workload.

## Pourquoi ça compte
Pour une veille technique, ce document illustre une approche concrète de l'optimisation des requêtes analytiques via la pré-agrégation, avec des chiffres de latence benchmarkés qui peuvent servir de référence pour comparer d'autres moteurs OLAP ou solutions d'analytique embarquée.
