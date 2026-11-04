---
title: "Expanded semantic model support in Knowledge Catalog | Google Cloud Blog"
date: 2026-11-04
url: "https://cloud.google.com/blog/products/data-analytics/expanded-semantic-model-support-in-knowledge-catalog/"
authors: ["Maggy Hu", "Paulina Trzeciak"]
keywords: ["Knowledge Catalog", "modèles sémantiques", "agents IA", "gouvernance des données", "Google Cloud", "graphe de contexte"]
theme: "Data"
tone: "news"
used_in: ["2026-11-04"]
---

## Résumé

Google Cloud annonce la disponibilité générale de l'extension de Knowledge Catalog aux modèles sémantiques métier provenant de Looker LookML, BigQuery Graph, dbt MetricFlow, Snowflake Semantic Views, Databricks Metric Views et SAP Core Schema Notation (CSN). L'idée est de rassembler ces définitions, aujourd'hui dispersées dans des outils cloisonnés, dans un unique graphe de contexte, afin que tous les agents IA (Gemini, BigQuery Conversational Analytics, agents maison) s'appuient sur les mêmes métriques, filtres et chemins de jointure que les analystes. Google avance, sur la base de benchmarks internes, des agents jusqu'à 4x plus précis, avec une latence réduite de 33% et une consommation de tokens diminuée de 75% lorsqu'ils sont ainsi ancrés. L'ingestion se fait sans déplacer les données ni réécrire la logique métier dans un nouveau langage.

## Points clés

- Le problème ciblé : un agent IA peut donner une réponse chiffrée fausse (ex. revenu net incluant des commandes annulées, puisées dans une table de staging non validée) non pas parce que le modèle de langage est mauvais, mais parce qu'il ignore les définitions métier déjà formalisées ailleurs.
- Knowledge Catalog ingère nativement les modèles sémantiques de six écosystèmes (Looker, BigQuery, dbt, Snowflake, Databricks, SAP) et les relie, dans un même graphe, au schéma, au lignage, aux profils de qualité des données et au glossaire métier.
- En cas de définitions concurrentes d'une même métrique entre deux outils, les deux versions sont conservées côte à côte avec leur provenance, pour que les data stewards arbitrent plutôt que de voir une définition écrasée silencieusement.
- Au-delà des définitions déjà documentées, un mécanisme d'enrichissement auto-appris (propulsé par Gemini) extrait du contexte additionnel depuis des sources non structurées (playbooks, notes de réunion, discussions, code) pour garder les définitions à jour.
- Le graphe sémantique est également connecté aux signaux de qualité, de fraîcheur et de lignage des données, afin qu'un agent sache si une donnée est fiable avant de l'utiliser dans une requête.
- Knowledge Studio (en preview) offre une interface pour explorer ce graphe en langage naturel, visualiser les chemins de connexion, puis packager des ensembles de contexte réutilisables par cas d'usage ou domaine métier.

## Analyse approfondie

### Le problème : des définitions métier éclatées entre outils

L'article part d'un scénario concret : avant une revue d'activité, un VP Sales demande à un assistant IA le revenu net des principaux comptes entreprise du dernier trimestre. L'agent répond vite, avec un graphique soigné — mais le chiffre ne correspond pas au rapport financier, car l'agent a compté des commandes annulées comme du revenu et a pioché dans une table de staging non validée. Selon les auteures, l'échec ne vient pas du modèle de langage ni de sa capacité à traduire une question en requête : il vient du fait que l'agent ne comprend pas le fonctionnement réel de l'entreprise. Cette compréhension existe pourtant déjà, sous forme de modèles sémantiques dans des outils comme Looker, dbt, Snowflake, Databricks ou SAP. Le problème est que chaque définition reste enfermée dans son propre outil, ce qui pousse chaque agent à deviner — et donc parfois à se tromper.

### La réponse : un graphe de contexte unique

C'est le rôle de Knowledge Catalog : regrouper les modèles sémantiques de tous ces outils dans un seul graphe de contexte, pour que chaque agent travaille à partir des mêmes définitions de confiance. Quand deux outils définissent une même métrique différemment, les deux définitions apparaissent avec leur provenance, ce qui permet aux data stewards de réconcilier le conflit avant qu'il n'atteigne les utilisateurs finaux.

Google Cloud annonce la disponibilité générale de cette extension : Knowledge Catalog ingère désormais nativement les modèles sémantiques et définitions de métriques de Looker LookML, BigQuery Graph (y compris les mesures BigQuery), dbt MetricFlow, Snowflake Semantic Views, Databricks Metric Views et SAP Core Schema Notation (CSN). Ces modèles sont connectés au schéma, au lignage, aux profils de données, au glossaire métier et à d'autres métadonnées clés, dans un graphe unique — sans déplacer les données ni réécrire la logique métier dans un nouveau langage.

En ancrant les agents IA dans ces modèles, ceux-ci héritent des mêmes définitions métier que les analystes humains, ce qui aligne leurs réponses sur les chiffres auxquels l'entreprise fait confiance. D'après des benchmarks internes cités par Google, cet ancrage rend les agents près de 4 fois plus précis, avec une latence réduite jusqu'à 33% et une consommation de tokens réduite jusqu'à 75%.

Ce graphe de contexte unifié permet trois choses :

- **Réutiliser les modèles sémantiques déjà en place** : Knowledge Catalog ancre l'agent Gemini, BigQuery Conversational Analytics et les agents personnalisés dans les métriques, filtres et chemins de jointure déjà définis par les équipes, où qu'ils se trouvent.
- **Dépasser les définitions manuellement renseignées grâce à un contexte auto-appris** : Knowledge Catalog associe les métriques et KPI bien définis des modèles sémantiques à du contexte pertinent extrait de sources non structurées — playbooks opérationnels, notes de réunion, fils de discussion, code, etc. Propulsé par Gemini, cet enrichissement auto-appris détecte en continu le contexte manquant ou obsolète et le transforme en ensembles de contexte gouvernés et réutilisables, pour que le contexte des agents reste à jour sans dépendre uniquement d'une curation manuelle.
- **Associer la logique métier à la confiance d'entreprise** : même la bonne formule produit une mauvaise réponse si elle s'applique à une donnée périmée ou non certifiée. C'est pourquoi Knowledge Catalog relie chaque définition sémantique aux scores de qualité des données, aux signaux de fraîcheur et au lignage, afin qu'un agent sache ce qu'il peut considérer comme fiable avant d'écrire une seule ligne de SQL.

Une comparaison côte à côte illustre la même question posée à Gemini sans Knowledge Catalog (à gauche) puis ancrée dans Knowledge Catalog (à droite) : la version ancrée donne une réponse exacte avec moins de tokens et une latence plus faible, contrairement à la version non ancrée qui hallucine tout en consommant davantage de ressources.

### Un graphe de contexte unique sur l'ensemble du patrimoine de données

Le graphe de contexte construit par Knowledge Catalog forme une carte connectée du patrimoine de données et sémantique de l'entreprise : les tables, modèles sémantiques, termes de glossaire et produits de données en sont les nœuds ; le lignage, les associations, les clés de schéma, les jointures extraites de l'historique réel des requêtes, ainsi que les chemins de jointure déclarés dans les modèles sémantiques, en sont les arêtes. Les sémantiques ingérées viennent s'ajouter à ce même graphe, aux côtés des signaux de gouvernance et d'usage déjà présents, ce qui permet à un agent de passer d'un concept métier à une formule de confiance et à des chemins de jointure vérifiés en une seule traversée. Chaque source apporte sa propre perspective sur l'activité de l'entreprise :

- **Looker LookML (GA)** : indexe les modèles, explores, vues et dashboards via une synchronisation en direct avec Looker Core, en capturant le SQL de métrique compilé, les conditions de jointure sécurisées contre les effets de fan-out, les filtres obligatoires et le lignage depuis les tables source jusqu'aux dashboards exécutifs.
- **BigQuery Graph (GA)** : indexe les définitions natives de graphes de propriétés, les tables de nœuds et d'arêtes, les mesures de graphe et les synonymes métier, pour que les agents raisonnent sur des entités connectées via des traversées en Graph Query Language (GQL) plutôt que par des auto-jointures multi-tables fragiles.
- **dbt MetricFlow (GA)** : relie les objets source aux modèles dbt et aux métriques MetricFlow, ainsi qu'aux résultats des tests de qualité des données dbt, aux filtres, aux requêtes sauvegardées, aux SLA de fraîcheur et aux expositions en aval.
- **Snowflake Semantic Views via Horizon Catalog (GA)** : associe les tables BigQuery ou Google Cloud Lakehouse fédérées aux métadonnées Snowflake Horizon, en intégrant les dimensions, faits, formules de métriques, relations et synonymes des Semantic Views, ainsi que les tableaux de bord qualité des Data Metric Functions et les tags de masquage PII.
- **Databricks Metric Views via Unity Catalog (GA)** : ingère les définitions de metric views, les formules de mesure, les filtres de portée et les cardinalités de jointure depuis Unity Catalog, ainsi que les badges de certification de table et les résultats de profilage de Lakehouse Monitoring.
- **SAP Core Schema Notation (CSN) via SAP Business Data Cloud (BDC) (GA)** : capture les libellés métier, les schémas de modélisation en dimensions et cubes, les agrégations par défaut, les associations de devise et d'unité, les jointures par clé et composites, ainsi que les indicateurs de sensibilité des données, lorsque les Data Products SAP BDC sont fédérés via Google Cloud Lakehouse.

Comme chaque source se traduit par un nœud ou une arête dans le même graphe, une jointure LookML, une exposition dbt, une relation Snowflake ou une association SAP peuvent être parcourues côte à côte, avec des liens qui les rattachent toutes aux tables physiques dont elles dépendent. Rien n'est écrasé silencieusement : les définitions qui se recoupent restent affichées côte à côte, chacune étiquetée par sa source, ce qui donne aux data stewards la vue d'ensemble nécessaire pour trancher en faveur d'une version unique.

Tout ce travail d'exploration et de gouvernance peut se faire dans Knowledge Studio (en preview), présenté comme le centre de contrôle pour explorer et gérer son contexte. On peut y explorer le graphe de contexte — y compris les définitions sémantiques — via des requêtes en langage naturel, et parcourir les chemins de connexion sur le canevas du graphe. Une fois les bons actifs et définitions validés, ils peuvent être packagés en ensembles de contexte réutilisables, associés à des cas d'usage et domaines spécifiques de l'organisation, que Gemini et les agents personnalisés peuvent ensuite consommer en production.

### Pour commencer

L'article referme la boucle sur l'exemple initial : avec Knowledge Catalog, l'agent du VP Sales n'a plus qu'à lancer une seule requête de contexte pour retrouver l'actif de confiance, appliquer exactement la formule et les filtres définis par les experts du domaine, respecter les clés de jointure entre systèmes, et vérifier que les données sous-jacentes ont passé les contrôles qualité. Résultat : les chiffres du rapport sont enfin corrects. Google invite les lecteurs à explorer leur graphe de contexte dans Knowledge Studio et à consulter la documentation de Knowledge Catalog pour connecter davantage de sources.

## Pourquoi ça compte

Cette annonce illustre une tendance de fond de la "veille data/IA" : la fiabilité des agents IA en entreprise dépend moins de la puissance du modèle que de leur ancrage dans une couche sémantique gouvernée et partagée entre tous les outils (BI, transformation, cloud warehouses, ERP). C'est un signal fort sur la convergence entre catalogues de données, gouvernance et agents IA générative, un terrain où Google Cloud se positionne frontalement face à Snowflake, Databricks et les éditeurs de catalogues sémantiques indépendants.
