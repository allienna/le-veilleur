---
title: "Python UDF Logging for Pipeline Observability in BigQuery | Google Cloud Blog"
date: 2026-10-21
url: "https://cloud.google.com/blog/products/data-analytics/python-udf-logging-for-pipeline-observability-in-bigquery/"
authors: ["Cong Du", "Ming Ma"]
keywords: ["BigQuery", "observabilité", "logging", "UDF Python", "pipeline de données", "Cloud Logging"]
theme: "Data"
tone: "tutorial"
used_in: ["2026-10-21"]
---

## Résumé
Google Cloud annonce une nouvelle fonctionnalité de logging pour les UDF (fonctions définies par l'utilisateur) Python dans BigQuery, permettant d'utiliser la librairie standard de logging Python directement à l'intérieur des UDF pour émettre des logs structurés vers Cloud Logging, sans plugin externe ni connecteur personnalisé. L'article illustre cette fonctionnalité via un pipeline d'ingestion d'événements e-commerce : les lignes corrompues sont journalisées et mises en quarantaine (retour `NULL`) plutôt que de faire échouer la requête entière, tandis que des alertes Cloud Monitoring peuvent être déclenchées en temps réel sur les taux d'erreur. Les données quarantainées restent interrogeables en SQL via la vue `_AllLogs`, ce qui permet de diagnostiquer, corriger et réinjecter les enregistrements récupérés sans perte de données. L'article présente aussi d'autres cas d'usage (exécution en miroir pour migrations, audit de redaction PII, détection de drift en inférence ML) ainsi que des bonnes pratiques.

## Points clés
- Les UDF Python de BigQuery supportent désormais la librairie de logging standard de Python, avec émission native vers Cloud Logging.
- Le pipeline de démonstration suit 3 étapes : validation inline (log + `NULL` sur erreur), alerte temps réel via métrique basée sur les logs, puis triage et réinjection en SQL.
- Les lignes invalides ne bloquent pas l'exécution de la requête : elles sont quarantainées et le reste du traitement continue.
- Les payloads bruts complets sont conservés dans Cloud Logging, ce qui permet une récupération et une réinjection ultérieures des données corrigées.
- Cas d'usage additionnels : exécution en miroir (shadow execution) pour sécuriser les migrations de logique métier, audit de redaction de PII, et détection de dérive (drift) en inférence ML.
- Bonnes pratiques recommandées : activer le mode debug explicitement, éviter de journaliser des données sensibles, et limiter le volume de logs (échantillonnage, logs uniquement sur erreur) pour maîtriser les coûts.

## Analyse approfondie
Nous annonçons une nouvelle fonctionnalité de logging désormais disponible pour les fonctions définies par l'utilisateur (UDF) Python dans BigQuery. Les développeurs peuvent maintenant utiliser la librairie standard de logging de Python directement à l'intérieur des UDF BigQuery pour émettre des logs structurés de façon transparente vers Cloud Logging — sans plugin externe ni connecteur personnalisé.

Bien que le logging des UDF permette un large éventail de workflows de monitoring opérationnel et de debugging, nous présentons dans cet article un exemple de construction de pipelines de données résilients et tolérants aux pannes. Dans l'exemple ci-dessous, nous capturons de la télémétrie de diagnostic au niveau de la ligne pendant l'exécution de la requête, afin que les équipes puissent facilement isoler les enregistrements problématiques, déclencher des alertes en temps réel, et trier les problèmes via SQL sans interrompre l'ensemble des charges de travail.

Dans cet article, nous allons vous montrer comment démarrer avec le logging des UDF Python et parcourir un pipeline d'ingestion d'événements e-commerce comme exemple pratique de bout en bout.

### Vue d'ensemble de l'architecture

Le workflow se compose de trois étapes :

1. **Validation inline** : l'UDF Python parse les payloads JSON entrants. Les enregistrements valides sont transmis à la table de destination ; les lignes corrompues ou non conformes déclenchent `logging.error()` et renvoient `NULL` pour éviter l'échec de la requête.
2. **Alerte en temps réel** : une métrique Cloud Monitoring basée sur les logs notifie votre équipe lorsque les taux d'erreur dépassent les seuils de SLA.
3. **Triage et réinjection en SQL** : les ingénieurs data interrogent les payloads quarantainés dans BigQuery via du SQL standard sur la vue liée `_AllLogs`, diagnostiquent la cause racine, et réinjectent les données récupérées.

Bien que cette démonstration spécifique repose sur Python pour la validation et la transformation des données, vous pouvez intégrer de façon fluide le logging et la validation pilotés par Python dans des pipelines qui effectuent des transformations basées sur SQL.

### Guide de démarrage rapide : étape par étape

#### Étape 1 : Créer l'UDF Python générique

Cette UDF parse le JSON et vérifie la présence d'un champ requis. Si le parsing échoue ou si la clé requise est manquante, elle journalise un JSON de diagnostic structuré et renvoie `NULL`.

#### Étape 2 : Lancer l'ingestion avec le logging activé

Dans cet exemple, nous simulons un pipeline d'ingestion d'événements e-commerce traitant des actions utilisateur entrantes (`click`, `view`, `checkout`). Notre objectif est d'extraire les événements valides vers notre table d'analyse propre tout en mettant proprement en quarantaine les payloads défectueux ou dont le schéma est manquant.

Activez le logging dans votre session avec `SET @@udf.properties` :

**Résultats de l'ingestion**

La requête réussit sans interruption, tandis que les lignes défectueuses (2 et 3) sont routées vers Cloud Logging.

#### Étape 3 : Configurer des alertes en temps réel sur Cloud Logging

Vous pouvez configurer des alertes pour notifier votre équipe d'astreinte dès que les payloads malformés dépassent des seuils acceptables.

**Dans la console Google Cloud (en un clic)**

1. Dans la console Google Cloud, ouvrez **Logs Explorer**.
2. Collez le filtre de log pour votre routine UDF :
3. Cliquez sur **Create alert** dans la barre d'action supérieure.
4. Configurez vos canaux de notification (par exemple Slack, PagerDuty ou Email) et enregistrez la politique.

#### Étape 4 : Trier les lignes défectueuses avec BigQuery Log Analytics

« Remarque : pour interroger vos logs via SQL BigQuery, assurez-vous d'avoir activé BigQuery Log Analytics sur votre bucket Cloud Logging et d'avoir créé un jeu de données lié. »

Interrogez les payloads quarantainés en utilisant du SQL BigQuery via la vue liée `_AllLogs` :

**Résultat de Log Analytics**

### Récupération des données

Parce que les payloads bruts complets sont conservés dans Cloud Logging, vous pouvez récupérer directement les enregistrements quarantainés avec du SQL une fois le problème amont corrigé :

**Résultat final de la table `clean_events` :**

Toutes les données valides et récupérées sont désormais unifiées dans la table de production, sans aucune perte de données.

### Autres cas d'usage

- **Exécution en miroir et migrations sécurisées** : exécutez en parallèle, dans une UDF, l'ancienne et la nouvelle logique métier. Renvoyez le résultat de l'ancienne logique en production tout en journalisant les différences de calcul vers Cloud Logging.
- **Audit de redaction de PII** : masquez les tokens sensibles (comme les numéros de sécurité sociale ou de compte) avant l'écriture dans BigQuery, tout en émettant des événements d'audit anonymisés vers Cloud Logging.
- **Dérive (drift) de l'inférence ML** : journalisez des avertissements lorsque la logique de scoring embarquée rencontre des entrées hors vocabulaire ou une faible confiance du modèle.

### Bonnes pratiques

- **Activer la sortie de debug** : incluez `SET @@udf.properties = JSON '{"enableDebugOutput": true}';` dans la session où vous souhaitez capturer les logs.
- **Éviter les données sensibles dans les logs** : Cloud Logging est visible par les utilisateurs disposant des permissions de Logging Viewer. Ne journalisez pas d'identifiants ou de secrets.
- **Maîtrise des coûts** : sur les pipelines à fort débit, journalisez de façon sélective (par exemple uniquement sur erreur ou via échantillonnage) pour maîtriser le volume d'ingestion des logs.

## Pourquoi ça compte
Cette fonctionnalité réduit significativement la friction pour instrumenter des pipelines BigQuery robustes : elle évite de recourir à des solutions de contournement externes pour l'observabilité et facilite l'adoption de patterns de type dead-letter queue nativement en SQL/Python, un sujet clé pour toute équipe data qui opère des pipelines de production à grande échelle.
