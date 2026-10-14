---
title: "BigQuery TimesFM 3.0 with multivariate time-series forecasting | Google Cloud Blog"
date: 2026-10-14
url: "https://cloud.google.com/blog/products/data-analytics/bigquery-timesfm-3-0-with-multivariate-time-series-forecasting/"
authors: ["Haiyang Qi", "Haoming Chen"]
keywords: ["BigQuery", "TimesFM", "séries temporelles", "prévision multivariée", "IA générative", "Google Cloud"]
theme: "Data"
tone: "news"
used_in: ["2026-10-14"]
---

## Résumé
Google Cloud annonce la préversion de TimesFM 3.0 dans BigQuery, un modèle de fondation développé par Google Research (330 millions de paramètres) qui introduit la prévision multivariée native de séries temporelles directement en SQL via AI.FORECAST. Ce modèle se classe numéro 1 sur les trois grands classements publics de séries temporelles (GIFT-Eval, FEV-Bench et TIME) et sert également de mise à niveau directe pour la prévision univariée (AI.FORECAST) et la détection d'anomalies (AI.DETECT_ANOMALIES) déjà existantes. L'article illustre ces capacités avec un exemple basé sur le jeu de données public NYC Citi Bike, combinant cibles corrélées, covariables passées et covariables futures, et montre aussi l'usage du modèle en langage naturel via BigQuery Conversational Analytics.

## Points clés
- TimesFM 3.0 entre en préversion dans BigQuery : un modèle de fondation de 330 millions de paramètres conçu par Google Research.
- Il se classe #1 sur les trois grands benchmarks publics de séries temporelles : GIFT-Eval, FEV-Bench et TIME.
- Nouveauté principale : la prévision **multivariée** nativement en SQL via AI.FORECAST, avec trois paramètres clés — `target_cols` (cibles corrélées), `past_covariate_cols` (covariables passées) et `future_covariate_cols` (covariables futures connues à l'avance).
- Mise à niveau transparente (« drop-in ») pour les usages univariés existants : il suffit de spécifier `model => 'TimesFM 3.0'` dans AI.FORECAST ou AI.DETECT_ANOMALIES pour bénéficier d'une meilleure précision.
- Exemple concret sur le jeu de données NYC Citi Bike : prévision conjointe des trajets abonnés et occasionnels sur 7 jours, en tenant compte de la durée moyenne des trajets (covariable passée) et des week-ends (covariable future).
- Les prévisions multivariées sont aussi accessibles en langage naturel via BigQuery Conversational Analytics, avec génération automatique de la requête, graphiques interactifs et intervalles de prédiction.

## Analyse approfondie
##### Haiyang Qi
Software Engineer

##### Haoming Chen
Engineering Manager

### Vue d'ensemble

Depuis l'introduction de la prévision de séries temporelles en zero-shot dans BigQuery avec AI.FORECAST — initialement propulsée par TimesFM 2.0 puis mise à niveau vers TimesFM 2.5 — il est possible de générer des prévisions directement en SQL, sans entraîner ni gérer de modèles personnalisés. Cependant, jusqu'à TimesFM 2.5, ces modèles de fondation se limitaient à la prévision univariée, c'est-à-dire à la prédiction des valeurs futures à partir de l'historique d'une seule série temporelle. En pratique, la plupart des problèmes de prévision réels sont multivariés : des cibles liées entre elles et des facteurs externes comme la météo, les promotions ou les jours fériés façonnent conjointement les résultats futurs.

Aujourd'hui, nous sommes ravis d'annoncer la préversion de TimesFM 3.0 dans BigQuery. Développé par Google Research, TimesFM 3.0 est un modèle de fondation de pointe à 330 millions de paramètres, conçu pour débloquer nativement la prévision multivariée de séries temporelles directement dans BigQuery SQL. TimesFM 3.0 se classe numéro 1 sur les trois grands classements publics de séries temporelles — GIFT-Eval, FEV-Bench et TIME — atteignant la meilleure précision en zero-shot à la fois sur les tâches de prévision avec covariables et sur les tâches multivariées, comparé aux modèles de fondation existants.

Outre ses nouvelles capacités multivariées, TimesFM 3.0 sert également de mise à niveau transparente (« drop-in ») pour la prévision univariée via AI.FORECAST et la détection d'anomalies via AI.DETECT_ANOMALIES. Les workflows existants peuvent immédiatement bénéficier d'une précision supérieure sur les benchmarks simplement en spécifiant `model => 'TimesFM 3.0'`.

### Nouveauté : la modélisation de fondation multivariée

Avec TimesFM 3.0, BigQuery apporte une modélisation multivariée de niveau entreprise dans les workflows SQL familiers via AI.FORECAST :

#### Prévision multivariée avec BigQuery SQL

Pour voir comment ces capacités fonctionnent ensemble, prévoyons les trajets quotidiens en vélo des navetteurs (subscriber_trips) et des usagers de loisir (casual_trips) sur un horizon de sept jours, en utilisant le jeu de données public NYC Citi Bike (bigquery-public-data.new_york.citibike_trips).

BigQuery utilise un format d'entrée à table unique pour la prévision multivariée, combinant deux ensembles de lignes :

- **Lignes d'observation historique** : horodatages compris entre la date de début (2016-01-01) et la date de coupure de la prévision (2016-06-01), entièrement renseignées avec les métriques cibles, les covariables passées et les covariables futures connues.
- **Lignes de l'horizon futur** : horodatages couvrant l'horizon de prévision de sept jours (2016-06-01 à 2016-06-07), renseignées avec les covariables futures connues, tandis que les colonnes cibles et les covariables uniquement passées sont fixées à NULL.

Cette requête met en évidence les trois dimensions multivariées prises en charge par TimesFM 3.0 :

1. **Prévision de cibles corrélées (`target_cols`)** — Plutôt que d'exécuter des modèles séparés pour chaque segment d'usagers, passer `TARGET_COLS => ['subscriber_trips', 'casual_trips']` permet de prévoir les deux métriques conjointement en un seul appel. TimesFM 3.0 capture la dynamique croisée entre les cyclistes navetteurs et occasionnels — comme une sensibilité météo partagée et des schémas de fréquentation divergents le week-end.
2. **Utilisation de covariables passées (`past_covariate_cols`)** — Certains signaux ne peuvent être observés qu'historiquement et ne sont pas connus à l'avance, comme la durée moyenne des trajets (avg_duration_min), l'affluence piétonne historique, ou des perturbations de service imprévues. Passer `PAST_COVARIATE_COLS => ['avg_duration_min']` (avec les lignes de l'horizon futur fixées à NULL) donne au modèle un contexte historique lui permettant de distinguer les chocs temporaires des tendances sous-jacentes, sans nécessiter de valeurs futures pour cette variable.
3. **Utilisation de covariables futures (`future_covariate_cols`)** — D'autres facteurs externes sont connus à l'avance, à la fois sur la fenêtre historique et sur l'horizon de prévision — comme les week-ends (is_weekend), les jours fériés ou les promotions planifiées. Passer `FUTURE_COVARIATE_COLS => ['is_weekend']` (renseigné sur toutes les lignes jusqu'au 2016-06-07) permet à TimesFM 3.0 de conditionner directement ses prédictions à sept jours sur les événements calendaires à venir.

#### Comprendre le résultat

La fonction retourne des prédictions structurées pour chaque colonne cible spécifiée dans `target_cols`. Pour chaque colonne de `target_cols`, AI.FORECAST retourne une structure (struct) contenant la prévision ponctuelle (value) ainsi que les bornes inférieure et supérieure de l'intervalle de prédiction.

### TimesFM 3.0 dans BigQuery Conversational Analytics

Il est également possible d'exécuter des prévisions multivariées en langage naturel dans BigQuery Conversational Analytics. Sur ce même jeu de données bigquery-public-data.new_york.citibike_trips, il suffit de demander : « Prévoir à la fois les trajets quotidiens des abonnés et des usagers occasionnels pour le 1er au 7 juin 2016 en utilisant deux mois de données historiques, avec la durée moyenne des trajets comme covariable passée et l'indicateur de week-end comme covariable future. » Conversational Analytics génère et exécute automatiquement la requête AI.FORECAST sous-jacente avec TimesFM 3.0, retournant un résumé des résultats, des graphiques de prévision interactifs avec des intervalles de prédiction pour chaque cible, ainsi que des points clés d'analyse.

La prévision multivariée avec TimesFM 3.0 dans BigQuery Conversational Analytics génère des prédictions à 7 jours, des graphiques interactifs et des analyses à partir d'une simple invite en langage naturel.

### Résumé et prochaines étapes

Avec la prise en charge native du multivarié, TimesFM 3.0 apporte à BigQuery une prévision par modèle de fondation de pointe pour des jeux de données d'entreprise complexes et interconnectés, sans nécessiter de déplacement de données, de pipelines d'ingénierie de caractéristiques personnalisés, ni d'infrastructure dédiée d'hébergement de modèles.

Pour commencer à prévoir avec TimesFM 3.0 dans BigQuery :

- Lire l'article du blog Google Research pour en savoir plus sur l'architecture et les capacités du modèle TimesFM 3.0.
- Explorer la documentation BigQuery TimesFM.
- Suivre le tutoriel pas à pas de prévision multivariée.
- Essayer AI.FORECAST avec `model => 'TimesFM 3.0'` directement dans l'espace de travail SQL de BigQuery Studio.
- Essayer AI.DETECT_ANOMALIES avec `model => 'TimesFM 3.0'` pour la détection d'anomalies sur séries temporelles univariées dans BigQuery.
- Essayer AI.EVALUATE avec `model => 'TimesFM 3.0'` pour l'évaluation de séries temporelles univariées dans BigQuery.

## Pourquoi ça compte
Cette annonce illustre la tendance de fond consistant à intégrer des modèles de fondation IA directement dans les entrepôts de données via SQL, supprimant le besoin de pipelines ML dédiés pour des tâches de prévision pourtant complexes (multivariées, avec covariables). Pour une veille data/IA, c'est un signal clair que les foundation models spécialisés (ici pour les séries temporelles) deviennent des briques natives des plateformes cloud, accessibles même sans expertise ML approfondie.
