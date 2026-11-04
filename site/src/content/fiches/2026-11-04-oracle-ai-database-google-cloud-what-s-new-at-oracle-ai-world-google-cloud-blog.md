---
title: "Oracle AI Database@Google Cloud: What's new at Oracle AI World | Google Cloud Blog"
date: 2026-11-04
url: "https://cloud.google.com/blog/products/databases/oracle-ai-databasegoogle-cloud-whats-new-at-oracle-ai-world/"
authors: ["Kiran Shenoy", "Kunal Agarwal"]
keywords: ["Oracle", "Google Cloud", "IA agentique", "bases de données", "Gemini", "BigQuery"]
theme: "Tech"
tone: "news"
used_in: ["2026-11-04"]
---

## Résumé
À l'occasion d'Oracle AI World à Las Vegas, Google Cloud et Oracle annoncent un approfondissement de leur partenariat autour d'Oracle AI Database@Google Cloud, en intégrant plus étroitement cette offre avec l'Agentic Data Cloud de Google et les modèles Gemini. L'objectif est de connecter les données opérationnelles critiques d'Oracle (ERP, finance, chaînes d'approvisionnement) à l'écosystème IA de Google, afin de permettre des workflows agentiques autonomes plutôt que de simples analyses statiques. Les annonces couvrent un serveur MCP distant, un connecteur Gemini pour les bases Oracle, l'intégration d'Oracle dans Gemini et de Gemini dans les applications Oracle, ainsi que de nouvelles options d'unification des données (lakehouse bidirectionnel, streaming CDC, fédération de requêtes BigQuery) et une expansion géographique et réglementaire (nouvelles régions, certification FedRAMP High).

## Points clés
- Disponibilité générale du serveur MCP distant (Model Context Protocol) pour Oracle, couplé à l'API ExecuteSQL Data gouvernée par IAM, supprimant le besoin de middleware NL-to-SQL, de VM bastion ou de mots de passe en clair.
- Préversion du connecteur Gemini pour Oracle AI Database@Google Cloud, permettant des requêtes en langage naturel directement dans l'app Gemini, avec ancrage des réponses via le Knowledge Catalog.
- « Oracle in Gemini » (disponible dès aujourd'hui) introduit l'analytique conversationnelle et un agent Oracle AI Database dans Gemini, avec plus de 135 compétences métier/dev pré-construites couvrant JD Edwards, E-Business Suite, NetSuite et Oracle Fusion.
- Nouvelle intégration bidirectionnelle entre le borderless Lakehouse de Google (BigQuery/Managed Spark) et Oracle AI Lakehouse via Apache Iceberg, permettant lecture ET écriture sans ETL ni réplication.
- CDC sub-seconde via OCI GoldenGate pour streamer les données Oracle vers BigQuery, et fédération de requêtes BigQuery (EXTERNAL_QUERY) pour interroger Oracle en direct sans copie de données.
- Expansion vers deux nouvelles régions (Turin, Queretaro) et poursuite de la certification FedRAMP High pour les charges de travail du secteur public américain.

## Analyse approfondie
Pendant des décennies, les opérations critiques des entreprises — des chaînes d'approvisionnement mondiales aux registres financiers et moteurs de facturation — se sont appuyées sur la performance et l'intégrité transactionnelle des bases de données Oracle. Aujourd'hui, à Oracle AI World à Las Vegas, Google Cloud et Oracle élargissent leur partenariat sur l'ensemble de la pile IA — incluant le calcul et l'infrastructure IA (avec la mise à disposition des TPU Google via Oracle Cloud Infrastructure), les données d'entreprise et l'IA agentique — en approfondissant l'intégration entre Oracle AI Database@Google Cloud, l'Agentic Data Cloud de Google et Gemini.

En unifiant les données et applications opérationnelles critiques d'Oracle avec l'écosystème data et IA de Google Cloud — incluant BigQuery et les modèles Gemini — les entreprises peuvent dépasser l'analytique statique et construire des workflows agentiques autonomes. Cette architecture fait tomber les silos de données traditionnels, donnant aux agents un accès direct, sécurisé et en temps réel aux données d'entreprise fondamentales nécessaires pour déclencher des actions concrètes.

### Briques fondamentales pour l'IA agentique

Pour débloquer une IA agentique prête pour la production, les entreprises ont besoin de plus que de la pure capacité des modèles : elles ont besoin d'une connectivité robuste aux bases de données, d'une gouvernance unifiée des données et d'un contexte sémantique riche, fonctionnant ensemble comme une fondation cohérente. Annoncées pour la première fois lors de Google Cloud Next '26, les capacités suivantes constituent les briques de base pour construire de l'intelligence conversationnelle, une gouvernance de bout en bout, et des environnements d'agents autonomes sur Oracle AI Database@Google Cloud :

- **Serveur MCP distant avec Data API** : Le serveur MCP (Model Context Protocol) distant pour les charges de travail Oracle — alimenté par l'API ExecuteSQL Data gouvernée par IAM — est désormais disponible en version générale. Ensemble, ils fournissent une interface unifiée et standardisée permettant aux agents IA, aux services Google Cloud et aux applications d'entreprise d'exécuter du SQL en toute sécurité et d'interagir directement avec les bases de données Oracle. En résolvant automatiquement les identifiants de base de données via Secret Manager et en appliquant les politiques IAM de Google Cloud, cette capacité élimine le besoin de middleware personnalisé langage-naturel-vers-SQL, de VM bastion, ou de mots de passe en texte clair.
- **Intégration du Knowledge Catalog** : L'intégration du Knowledge Catalog de Google Cloud, actuellement en préversion, unifie la découverte des métadonnées d'entreprise et la gouvernance à travers les bases de données Oracle et l'Agentic Data Cloud de Google au sens large. En cataloguant automatiquement les schémas et les métadonnées métier, les organisations peuvent appliquer des contrôles d'accès cohérents, suivre la provenance des données, et fournir le contexte sémantique riche dont les agents ont besoin pour raisonner avec précision sur des données opérationnelles complexes. Cliquez ici pour vous inscrire à cette fonctionnalité.

### Connecteur Gemini pour Oracle AI Database@Google Cloud

En s'appuyant directement sur les capacités fondamentales évoquées ci-dessus, nous annonçons également la préversion du **connecteur Gemini pour Oracle AI Database@Google Cloud**. Avec cette intégration native, les utilisateurs métier et les développeurs peuvent interagir directement avec leurs bases de données Oracle sur Oracle AI Database@Google Cloud en utilisant des requêtes en langage naturel, directement dans l'application Gemini. En coulisses, Gemini s'appuie automatiquement sur le Knowledge Catalog pour découvrir, rechercher, et ancrer ses réponses strictement dans les données Oracle gouvernées que chaque utilisateur est autorisé à consulter — transformant des bases de données opérationnelles complexes en une expérience conversationnelle intuitive, sans compromettre la sécurité de l'entreprise. Cliquez ici pour vous inscrire à cette fonctionnalité.

### Oracle dans Gemini et Gemini dans Oracle

Au-delà des requêtes directes sur les bases de données, Google Cloud et Oracle connectent les workflows agentiques à travers la couche applicative plus large — en apportant les données Oracle dans Gemini et en intégrant nativement les modèles Gemini dans les applications Oracle :

- **Oracle dans Gemini :** Disponible dès aujourd'hui, Oracle in Gemini introduit l'analytique conversationnelle, des connecteurs de bases de données cross-cloud, et des agents spécialisés par domaine — incluant le nouvel agent Oracle AI Database dans Gemini. Fort de plus de 135 compétences opérationnelles et de développement pré-construites et d'une connectivité MCP standardisée sans identifiants en texte clair, les entreprises peuvent orchestrer des workflows multi-agents à travers JD Edwards, E-Business Suite, NetSuite et Oracle Fusion sans SQL personnalisé ni middleware fragile.
- **Modèles Gemini dans les applications Oracle** : Parallèlement, le raisonnement de pointe de Gemini est intégré directement dans Oracle Fusion AI Agent Studio, Fusion Claw, les applications Oracle Fusion, et NetSuite — combinant l'intelligence des bases de données Oracle avec les capacités agentiques de Gemini pour automatiser l'exécution à travers les systèmes transactionnels de référence.
- **Modèles agentiques prêts pour les partenaires :** Pour aider les organisations à déployer rapidement ces workflows gouvernés, Google Cloud et Oracle collaborent avec des partenaires de premier plan et des intégrateurs systèmes mondiaux — incluant Argano, Automus, Calfus, HCL, IBM, Infosys, LTM, Pythian, TCS et Tessell — qui fournissent des compétences opérationnelles pré-construites, des connecteurs MCP personnalisés, et des modèles sectoriels pour des architectures agentiques de niveau production.

### Donner le choix avec lakehouse, streaming et fédération

Chaque entreprise a des priorités architecturales, des seuils de latence et des exigences de gouvernance distincts lorsqu'il s'agit de connecter les données opérationnelles Oracle à BigQuery et aux charges de travail IA. Plutôt que d'imposer un schéma d'intégration unique, Google Cloud et Oracle offrent un spectre complet de choix d'unification des données afin que les clients puissent sélectionner — ou combiner — l'approche exacte qui correspond le mieux à leur charge de travail et à leur cas d'usage :

#### Google Cloud borderless Lakehouse et Oracle AI Lakehouse bidirectionnels

Les architectures de données d'entreprise modernes sont de plus en plus multi-cloud et ancrées dans des standards ouverts. En s'appuyant sur notre partenariat stratégique, Google Cloud et Oracle ont livré plus tôt cette année une innovation clé pour soutenir l'interopérabilité des données cross-cloud, propulsée par le standard ouvert Apache Iceberg : l'intégration du **borderless Lakehouse de Google avec Oracle AI Lakehouse**.

Ce travail a permis au borderless Lakehouse de lire les tables Apache Iceberg créées par Oracle AI Lakehouse, à travers n'importe quel cloud public ou environnement sur site, en s'appuyant sur les catalogues et le stockage pris en charge par les deux plateformes.

Aujourd'hui, nous allons plus loin en la rendant entièrement bidirectionnelle avec **l'accès Oracle au borderless Lakehouse de Google Cloud (préversion)**. Désormais, Oracle Autonomous AI Database et le borderless Lakehouse de Google (propulsé par BigQuery et Managed Spark) peuvent directement interroger et exécuter des opérations d'écriture/DML sur des tables Apache Iceberg partagées dans Google Cloud Storage, éliminant complètement le besoin d'ETL ou de réplication de données.

En utilisant un catalogue REST de runtime Lakehouse intégré à Oracle via DBMS_CATALOG, cette intégration bidirectionnelle livre un cadre de stockage à standards ouverts tout en permettant aux équipes analytiques (utilisant BigQuery et Gemini) et aux équipes opérationnelles (utilisant Oracle SQL) de collaborer sur une source de vérité unique et unifiée. Vous pouvez cliquer ici pour vous inscrire à cette fonctionnalité.

#### Streaming CDC sub-seconde avec OCI GoldenGate

Pour les organisations qui préfèrent refléter en continu leurs données opérationnelles critiques dans BigQuery pour de l'analytique et de l'IA à grande échelle, la capture de changement de données (CDC) en temps réel offre un avantage compétitif immédiat. Grâce à l'intégration native OCI GoldenGate, les événements CDC sont extraits directement des journaux de rejeu (redo logs) Oracle sans toucher aux blocs de table ni ajouter de surcharge aux charges de travail transactionnelles. Les transactions circulent de manière sécurisée à travers les réseaux privés de Google Cloud, directement vers les tables gérées de BigQuery, offrant une fraîcheur analytique sub-seconde pour alimenter Gemini, les feature stores, et les tableaux de bord de business intelligence en direct, tout en simplifiant les migrations depuis des environnements sur site vers Oracle AI Database@Google Cloud.

#### Fédération de requêtes BigQuery avec Oracle

Lorsque les charges de travail exigent une visibilité opérationnelle à la demande ou des jointures cross-estate peu fréquentes sans déplacer les données, la fédération de requêtes BigQuery avec Oracle, en préversion, permet une analytique en temps réel et sur place directement sur des bases de données Oracle en direct. En utilisant la fonction EXTERNAL_QUERY, les équipes data peuvent exécuter du SQL Oracle natif directement depuis des requêtes, tableaux de bord et pipelines BigQuery pour récupérer des enregistrements transactionnels en direct et les joindre facilement avec des jeux de données BigQuery à l'échelle du pétaoctet. Cette approche sans copie simplifie les opérations et réduit le coût total de possession (TCO) en éliminant le stockage dupliqué et la maintenance ETL pour les recherches ad hoc, le reporting de risque intrajournalier, et la détection de fraude en direct. Veuillez contacter votre équipe de compte Google Cloud si vous souhaitez vous inscrire à cette fonctionnalité.

### Expansion mondiale et conformité secteur public

Nous continuons à étendre l'empreinte physique mondiale et les frontières de conformité d'Oracle AI Database@Google Cloud pour rencontrer les clients où qu'ils opèrent, avec de nouvelles régions et certifications.

- Les régions `europe-west12-a` (Turin, Italie) et `northamerica-south1-b` (Queretaro, Mexique) sont désormais en production, rejoignant les hubs mondiaux incluant Milan, l'Iowa, São Paulo, Tokyo, Sydney et Mumbai, pour offrir un accès à très faible latence et une résidence locale des données.

**Certification FedRAMP High**

- Lors d'Oracle AI World, Oracle a annoncé son intention de poursuivre la certification FedRAMP High pour Oracle AI Database@Google Cloud. Cette initiative permettra aux entités gouvernementales américaines et du secteur public d'exécuter des charges de travail réglementées en utilisant Oracle Exadata Database Service sur une infrastructure dédiée au sein de Google Cloud Assured Workloads.
- Fonctionner au sein d'un environnement autorisé FedRAMP High permet aux agences fédérales de protéger les données sensibles non classifiées tout en co-localisant les charges de travail Oracle avec les applications existantes et Gemini. Les agences peuvent accéder aux données Oracle en direct avec une latence minimale, une facturation simplifiée, et une acquisition facilitée via Google Cloud Marketplace ou des partenaires certifiés — tout cela dans le respect de leurs frontières de conformité.

### Construire l'avenir agentique

En combinant le moteur transactionnel éprouvé d'Oracle avec l'Agentic Data Cloud de Google, les données d'entreprise passent de systèmes d'enregistrement passifs à un moteur opérationnel actif et intelligent. Qu'il s'agisse d'unifier les données via des lakehouses Apache Iceberg ouverts, de streamer des changements sub-seconde via GoldenGate, de fédérer des requêtes en direct depuis BigQuery, ou de converser directement avec des données Oracle gouvernées via Gemini, les organisations disposent désormais de toute la flexibilité et de la sécurité nécessaires pour déployer des agents IA autonomes à grande échelle — générant des insights prédictifs et des actions automatisées à travers leurs processus métier les plus critiques.

### Pour commencer dès aujourd'hui

Oracle AI Database@Google Cloud est disponible directement via Google Cloud Marketplace, vous permettant de déployer en utilisant vos engagements Google Cloud existants, une facturation unifiée, et les Oracle Support Rewards.

Pour en savoir plus, visitez la présentation d'Oracle AI Database@Google Cloud, consultez la documentation officielle d'Oracle Database@Google Cloud, ou contactez votre équipe de compte Google Cloud pour planifier un briefing d'architecture.

## Pourquoi ça compte
Cette annonce illustre la consolidation rapide de l'écosystème IA agentique autour des données d'entreprise critiques, avec deux géants du cloud (Google et Oracle) qui lèvent les barrières techniques (SQL, ETL, silos) pour permettre à des agents IA d'agir directement sur des systèmes transactionnels sensibles. Pour une veille tech, c'est un signal fort sur la direction que prennent les partenariats cloud/data/IA — gouvernance et interopérabilité (MCP, Iceberg) devenant le nouveau champ de bataille plutôt que la seule puissance des modèles.
