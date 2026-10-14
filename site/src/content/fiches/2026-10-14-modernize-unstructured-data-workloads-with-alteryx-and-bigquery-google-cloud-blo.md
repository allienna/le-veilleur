---
title: "Modernize unstructured data workloads with Alteryx and BigQuery | Google Cloud Blog"
date: 2026-10-14
url: "https://cloud.google.com/blog/products/data-analytics/modernize-unstructured-data-workloads-with-alteryx-and-bigquery/"
authors: ["Kira Droganova", "Rama Vundela"]
keywords: ["BigQuery", "Alteryx", "données non structurées", "IA générative", "automatisation financière"]
theme: "Data"
tone: "news"
used_in: ["2026-10-14"]
---

## Résumé
Google Cloud et Alteryx présentent l'intégration d'Alteryx One Live Query avec BigQuery, une solution visant à traiter les données non structurées (notamment les factures PDF) directement dans l'entrepôt de données, sans déplacement des données vers des outils tiers. Live Query permet aux utilisateurs métier de construire des pipelines de données sans code, en s'appuyant sur le "SQL pushdown" pour exécuter la transformation directement dans BigQuery, et sur les modèles d'IA de Google (Gemini, Document AI) pour extraire l'information des documents. Le cas d'usage phare est l'automatisation du traitement des factures fournisseurs : extraction des champs clés, classification, normalisation, rapprochement avec l'historique et détection d'anomalies, le tout en conservant la gouvernance et la sécurité des données au sein de BigQuery. Papa Johns est cité comme client ayant adopté cette approche.

## Points clés
- Live Query exécute les transformations directement dans BigQuery via le "SQL pushdown", évitant le déplacement des données hors de l'entrepôt.
- Le workflow d'extraction de factures utilise soit Document AI (fonction ML.PROCESS_DOCUMENT), soit Gemini (fonction AI.GENERATE), selon la configuration choisie par l'utilisateur.
- L'outil Classify applique une classification "zero-shot" (AI.CLASSIFY) pour étiqueter automatiquement les lignes de factures par catégorie métier.
- Le pipeline complet couvre l'ingestion depuis Google Cloud Storage, l'extraction, la classification, la normalisation des numéros de facture, le rapprochement avec l'historique BigQuery, puis la détection d'exceptions (ex. : incohérence entre montant total et somme HT + taxes).
- L'architecture distingue trois couches : le navigateur (conception visuelle du workflow), les services de la plateforme Alteryx One (coordination, traçabilité, observabilité), et Google Cloud (stockage, exécution gouvernée, IA).
- Les bénéfices annoncés incluent un meilleur taux de traitement automatisé ("straight-through processing"), une réconciliation plus rapide, une auditabilité renforcée et une réduction des mouvements de données.

## Analyse approfondie
L'article décrit en détail l'architecture technique de l'intégration Alteryx One Live Query / BigQuery, pensée comme un motif "Google Cloud-native" pour le traitement documentaire à grande échelle.

**Problème adressé** : les équipes finance et opérations doivent traiter de grands volumes de factures PDF hétérogènes (formats de numéros variables, risque d'erreur manuelle), traditionnellement via une chaîne d'outils fragmentée génératrice de doublons ou d'écarts de montants.

**Architecture en trois couches** :
1. *Live Query (navigateur)* : couche d'auteurisation où l'utilisateur configure visuellement l'extraction de documents, la classification, le nettoyage, la validation et le routage, sans écrire de code.
2. *Alteryx One Platform Services* : couche de coordination (via un "Transformation Service") qui gère l'exécution, la planification et la récupération des résultats entre le workflow et l'environnement de données client, tout en assurant traçabilité et observabilité.
3. *Google Cloud* : couche d'exécution gouvernée, où les PDF sont stockés dans Google Cloud Storage, l'historique des factures reste dans BigQuery sous les politiques d'accès fin configurées, et l'extraction IA s'exécute directement sur cet environnement, les résultats étant réécrits dans BigQuery.

**Déroulé du workflow (étape par étape)** :
- *Ingestion* : le workflow pointe vers un répertoire Cloud Storage, énumère les fichiers PDF et récupère leurs métadonnées (chemins, taille, dates) pour alimenter les étapes suivantes.
- *Extraction* : l'outil Document Extract construit une table externe temporaire à partir des URI des documents puis appelle soit ML.PROCESS_DOCUMENT (Document AI), soit AI.GENERATE (Gemini) selon le modèle choisi — l'article détaille le chemin Gemini, où AI.GENERATE renvoie les champs de facture demandés. En mode conception, seul un sous-ensemble de documents est traité en aperçu ; en exécution réelle, l'ensemble des factures est traité.
- *Classification* : l'outil Classify applique une classification "zero-shot" via AI.CLASSIFY pour étiqueter les lignes de facture en catégories métier (ex. fournitures industrielles vs bureautiques), enrichissant les données pour le rapprochement et le reporting.
- *Normalisation* : les numéros de facture extraits sont nettoyés et standardisés pour éviter que de simples différences de format ne masquent des doublons.
- *Rapprochement historique* : les enregistrements normalisés sont comparés à l'historique déjà présent dans BigQuery pour repérer les doublons potentiels (numéros de facture correspondants).
- *Détection d'exceptions* : une étape de formule applique des règles métier (ex. vérifier que invoice_amount = net_amount + tax_amount) pour signaler les anomalies à examiner.
- *Sorties opérationnelles* : le workflow produit deux flux — les factures identifiées comme doublons potentiels, et les factures validées, étiquetées et prêtes pour le traitement des factures impayées.

**Témoignage client** : Michael Wyant (VP Enterprise Data & Corporate Solutions chez Papa Johns) salue l'intégration naturelle d'Alteryx One : Google Edition dans l'écosystème Google Cloud, et la possibilité pour les utilisateurs métier d'accéder aux données BigQuery de façon intuitive et gouvernée.

**Conclusion des auteurs** : au-delà d'un simple outil d'extraction, ce motif architectural permet de transformer des documents non structurés en décisions opérationnelles exploitables, sans déplacer les données hors de BigQuery — combinant l'accessibilité de Live Query à la puissance de calcul et d'IA de BigQuery pour réduire l'effort manuel et accélérer la gestion des exceptions.

## Pourquoi ça compte
Cet article illustre une tendance de fond : l'intégration native de l'IA générative (Gemini) et de l'extraction documentaire directement dans les entrepôts de données cloud, réduisant la fragmentation des outils ETL/ELT classiques et renforçant la gouvernance des données sensibles en entreprise.
