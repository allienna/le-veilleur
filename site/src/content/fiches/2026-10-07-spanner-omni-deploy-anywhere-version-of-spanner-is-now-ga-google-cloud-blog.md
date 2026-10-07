---
title: "Spanner Omni, deploy-anywhere version of Spanner, is now GA | Google Cloud Blog"
date: 2026-10-07
url: "https://cloud.google.com/blog/products/databases/spanner-omni-deploy-anywhere-version-of-spanner-is-now-ga/"
authors: ["Jagan R. Athreya", "Wenzhe Cao"]
keywords: ["Spanner Omni", "base de données distribuée", "multi-cloud", "IA agentique", "Google Cloud", "recherche vectorielle"]
theme: "Data"
tone: "news"
used_in: ["2026-10-07"]
---

## Résumé
Spanner Omni, la version déployable n'importe où de la base de données distribuée Spanner de Google, est désormais disponible en version générale (GA), permettant de l'exécuter sur site, sur d'autres clouds ou en local tout en conservant la cohérence forte et les capacités multi-modèles (SQL, graphe, vecteur, recherche plein texte) de Spanner. Depuis sa préversion présentée à Google Cloud Next '26, l'outil a dépassé les 2 millions de téléchargements et compte des clients comme Attio, une CRM native IA, qui l'utilise pour ses workflows agentiques critiques. La version GA ajoute des fonctionnalités entreprise (chiffrement TLS, audit, sauvegarde/restauration, nœuds de calcul dédiés) ainsi que deux formules de licence : une édition développeur gratuite et une édition commerciale payante basée sur le vCPU. Google précise viser la parité avec le service managé, tout en restant un logiciel autogéré, sans SLA de disponibilité fourni par Google et avec certaines intégrations natives Google Cloud (BigQuery, Gemini Enterprise) encore exclues.

## Points clés
- Spanner Omni atteint la disponibilité générale (GA) et peut être déployé sur VM, Kubernetes, sur site, en multi-cloud ou en local.
- Plus de 2 millions de téléchargements depuis son lancement en préversion à Google Cloud Next '26.
- Intègre nativement la recherche vectorielle, Spanner Graph et le support du Model Context Protocol (MCP) pour les applications d'IA agentique.
- La GA ajoute des fonctionnalités entreprise : sécurité TLS, authentification/autorisation, audit, sauvegarde/restauration, nœuds de calcul dédiés (worker nodes) et support Google Cloud.
- Deux licences disponibles : Édition Développeur gratuite (90 jours, ou perpétuelle sous 4 vCPU) et Édition Commerciale payante en abonnement annuel basé sur le vCPU.
- Reste un logiciel autogéré : pas de SLA Google, et certaines intégrations propres à Google Cloud (BigQuery, Gemini Enterprise) ne sont pas disponibles.

## Analyse approfondie
##### Jagan R. Athreya
Group Product Manager

##### Wenzhe Cao
Group Product Manager

Spanner Omni, la version de Spanner déployable n'importe où, est désormais disponible en version générale (GA), prête à faire fonctionner vos charges de travail de production les plus exigeantes dans votre centre de données sur site ou sur d'autres clouds.

Avec Spanner, Google a été pionnier du marché du SQL distribué il y a plus d'une décennie, en combinant l'évolutivité horizontale du NoSQL avec la conformité ACID et la forte cohérence d'une base de données relationnelle traditionnelle. Depuis, Spanner a évolué pour devenir une base de données multi-modèle interopérable qui simplifie les charges de travail complexes et alimente l'IA agentique, en combinant SQL, graphe, clé-valeur, recherche plein texte, recherche vectorielle et traitement analytique avec un moteur colonnaire, tout cela au sein d'une seule base de données.

Lorsque nous avons présenté Spanner Omni pour la première fois lors de Google Cloud Next '26, nous avons détaché notre base de données distribuée de Google Cloud pour l'apporter directement sur votre propre infrastructure. Cela a généré un intérêt incroyable, à la fois chez les clients entreprises et au sein de la communauté des développeurs. En effet, depuis son lancement, Spanner Omni a dépassé les 2 millions de téléchargements.

Spanner Omni offre les mêmes capacités fondamentales que le service Spanner entièrement managé, avec en plus la liberté de le déployer où vous en avez besoin. Que vous exécutiez des machines virtuelles ou Kubernetes dans vos centres de données privés, que vous déployiez sur plusieurs clouds, ou que vous testiez localement sur un ordinateur portable, Spanner Omni apporte directement la cohérence, la disponibilité, l'échelle et les capacités multi-modèles interopérables dignes de Google à vos prochaines applications d'IA agentique.

*Spanner Omni offre la liberté de déployer n'importe où avec les mêmes capacités fondamentales de Spanner*

### Attio accélère la vélocité de ses applications agentiques grâce à Spanner Omni

Spanner Omni permet aux équipes de développer une seule fois et de déployer n'importe où, offrant une portabilité des applications entre Google Cloud, les environnements sur site et d'autres clouds. Attio, une entreprise de CRM native IA basée à Londres, a construit sa plateforme sur Spanner. Attio a migré son environnement d'applications agentiques vers une combinaison complète et containerisée de Spanner Omni et de Spanner managé.

« Chez Attio, nous construisons l'environnement d'applications agentiques le plus avancé au monde sur Spanner, afin de réaliser notre vision d'une plateforme CRM native IA. Spanner Omni a été une avancée majeure pour nous en apportant les capacités et les performances de Spanner dans tous nos environnements, permettant à nos agents de mettre en production des workflows complexes et critiques, comme les files d'attente Spanner récemment annoncées. Avec Spanner Omni, nous avons pu accélérer notre vélocité de production à un niveau d'échelle et de confiance véritablement renforcé, ce qui n'était pas possible auparavant. » — Alexander Christie, cofondateur et CTO d'Attio

### Des capacités d'IA intégrées pour tout environnement

Spanner Omni étend les fondations multi-modèles convergées de Spanner directement à votre infrastructure privée et aux clouds tiers, en fournissant des capacités essentielles pour les charges de travail d'IA :

- **Recherche vectorielle et Spanner Graph** : stockez et indexez nativement des embeddings vectoriels à côté de vos tables relationnelles. Avec la prise en charge de la recherche KNN et ANN, vous pouvez combiner la similarité sémantique avec des filtres SQL structurés. Spanner Graph intègre des graphes de propriétés directement dans le moteur, ce qui permet de tracer des relations complexes entre entités et de relier les parcours de graphe à la recherche vectorielle.
- **Prise en charge du Model Context Protocol (MCP)** : intégrez-vous directement aux systèmes agentiques grâce à MCP Toolbox. Cette norme ouverte permet aux agents autonomes d'inspecter les schémas, de récupérer le contexte pertinent et d'utiliser Spanner Omni comme couche de mémoire opérationnelle à travers des déploiements multi-cloud.

### Les nouveautés de Spanner Omni

Depuis la préversion, nous avons travaillé à étendre les capacités de Spanner Omni et à affiner le modèle de tarification pour les déploiements prêts pour la production.

#### Fonctionnalités entreprise pour les déploiements en production

La version GA débloque l'ensemble complet des capacités de niveau entreprise nécessaires aux charges de travail de production critiques, notamment :

- **Sécurité et gouvernance robustes** : prise en charge de la sécurité d'entreprise avancée, incluant le chiffrement TLS, l'authentification et l'autorisation, ainsi que la journalisation d'audit.
- **Protection des données** : des capacités de sauvegarde et de restauration haute performance pour protéger vos données contre les suppressions accidentelles (« fat-finger ») ou la corruption de données.
- **Nœuds de calcul (worker nodes)** : des nœuds de calcul dédiés et sans état, propres à Spanner Omni, conçus pour décharger les opérations en arrière-plan et gourmandes en ressources des serveurs Spanner Omni principaux, afin que ceux-ci puissent se concentrer sur le traitement des charges de travail essentielles de la base de données.
- **Support de niveau entreprise** : un accès direct au service client de Google Cloud pour garantir le bon fonctionnement de vos charges de travail critiques.

#### Licences flexibles et tarification conforme aux standards du secteur

Pour vous accompagner à chaque étape du développement, Spanner Omni propose deux niveaux de licence distincts, conçus pour s'adapter à votre échelle et à votre budget :

- **Édition Développeur (gratuite)** : conçue pour le développement, les tests et le prototypage dans des environnements non commerciaux, hors production, ainsi que pour un usage personnel, elle inclut toutes les fonctionnalités essentielles de Spanner, vous permettant de construire et de valider vos applications avant de passer à l'échelle en production. L'Édition Développeur comprend une licence de 90 jours et inclut toutes les fonctionnalités de l'édition commerciale, à l'exception des fonctions de sauvegarde et des nœuds de calcul (worker nodes). Lorsqu'elle est utilisée dans un déploiement à serveur unique de 4 vCPU ou moins, la licence de l'Édition Développeur n'expire pas et toutes les fonctionnalités du serveur unique, y compris la sauvegarde-restauration, sont prises en charge. Si vous avez besoin d'utiliser l'Édition Développeur au-delà de 4 vCPU ou de la limite de 90 jours, vous pouvez demander une licence perpétuelle en remplissant ce formulaire.
- **Édition Commerciale (payante)** : conçue pour les charges de travail commerciales en production, cette édition fournit l'ensemble complet des capacités de Spanner Omni, avec le support entreprise en complément. Elle repose sur un modèle d'abonnement annuel basé sur le vCPU, prévisible et conforme aux standards du secteur. Nous proposons également une licence de preuve de concept pour l'évaluation en pré-production, à un tarif réduit.

### Spanner Omni comparé à Spanner entièrement managé sur Google Cloud

Notre objectif avec Spanner Omni est d'offrir une parité avec le service Spanner entièrement managé sur Google Cloud. Cependant, en tant que logiciel autogéré, le déploiement et l'exploitation de Spanner Omni diffèrent de ceux de Spanner entièrement managé sur Google Cloud de plusieurs façons :

- **Opérations autogérées** : vous êtes responsable de l'ensemble des opérations quotidiennes, y compris la maintenance de routine, les mises à niveau de version et la surveillance de l'infrastructure.
- **Disponibilité et SLA** : comme Spanner Omni s'exécute sur une infrastructure gérée par le client, Google ne fournit pas de SLA de disponibilité. Cependant, un déploiement conforme à nos architectures de référence recommandées vous aidera à atteindre un niveau de haute disponibilité comparable.
- **Intégration avec Google Cloud** : afin de garantir sa capacité à fonctionner n'importe où, Spanner Omni exclut les fonctionnalités disponibles dans Spanner managé qui dépendent de capacités propres à Google Cloud, telles que les intégrations natives avec BigQuery, Knowledge Catalog, ou Gemini Enterprise et d'autres services Google Cloud.
- **Feuille de route vers la parité des fonctionnalités** : bien que certains écarts fonctionnels existent aujourd'hui entre Spanner Omni et Spanner entièrement managé, nous développons activement des mises à jour pour combler ces écarts dans les prochaines versions.

### Pour commencer dès aujourd'hui

Que vous soyez en train de moderniser des systèmes existants sur site ou de construire une architecture multi-cloud résiliente, Spanner Omni est prêt à vous aider à passer à l'échelle.

- Pour plus d'informations, consultez le site de Spanner Omni afin d'explorer la documentation et les cas d'usage.
- Pour utiliser l'édition commerciale de Spanner Omni avec toutes ses fonctionnalités, contactez votre équipe de compte Google Cloud ou adressez-vous à nous via https://cloud.google.com/consulting/spanner-omni.
- Pour le développement et les tests à des fins non commerciales et hors production, téléchargez l'édition développeur de Spanner Omni.

## Pourquoi ça compte
Ce lancement illustre la stratégie de Google consistant à détacher ses bases de données phares du cloud propriétaire pour répondre à la demande de portabilité multi-cloud et on-premise, en particulier pour les charges de travail d'IA agentique nécessitant une mémoire opérationnelle unifiée (vecteurs, graphe, MCP) — un signal important pour qui suit la concurrence entre offres de bases de données distribuées et l'infrastructure de l'IA agentique.
