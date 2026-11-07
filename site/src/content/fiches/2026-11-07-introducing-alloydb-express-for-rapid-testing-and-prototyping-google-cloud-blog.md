---
title: "Introducing AlloyDB Express for rapid testing and prototyping | Google Cloud Blog"
date: 2026-11-07
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fcloud.google.com%2Fblog%2Fproducts%2Fdatabases%2Fintroducing-alloydb-express-for-rapid-testing-and-prototyping%3Futm_source=tldrit/1/010001a1b103aecf-7f6aba2a-9836-49b7-ba3c-81ff30300544-000000/CRHu9s5VomlIdMZ7H89iyXxXbQWxYTVuRSPbHi4jJJc=452"
authors: ["Ravi Murthy", "Gopal Ashok"]
keywords: ["AlloyDB", "PostgreSQL", "Google Cloud", "base de données", "IA", "scale-to-zero"]
theme: "Software"
tone: "news"
used_in: ["2026-11-07"]
---

## Résumé
Google Cloud annonce la préversion d'AlloyDB Express, une nouvelle offre d'AlloyDB pour PostgreSQL pensée pour les développeurs et les agents de codage IA. Le service permet de créer une base de données prête à l'emploi en moins de deux secondes, de la mettre en pause automatiquement après 15 minutes d'inactivité pour ne pas facturer de calcul inutile, et de passer en un clic vers une échelle de production avec haute disponibilité et reprise après sinistre. Il embarque aussi des capacités d'IA natives (recherche vectorielle, accès direct aux modèles Gemini en SQL, génération de requêtes en langage naturel) tout en conservant les garde-fous de sécurité d'entreprise habituels.

## Points clés
- Création d'une base PostgreSQL en moins de deux secondes via `gcloud`, l'API REST, MCP, Terraform ou la Console.
- Mise en pause automatique (scale-to-zero) après 15 minutes d'inactivité, avec réveil instantané à la prochaine requête — aucun coût de calcul pendant la pause.
- Sécurité d'entreprise intégrée par défaut : endpoints DNS privés, Private Service Connect, IAM, VPC Service Controls et rôles PostgreSQL natifs.
- IA native dans la base : recherche vectorielle (pgvector HNSW et ScaNN), accès direct aux modèles Gemini en SQL (`ai.if`, `ai.rank`, `ai.generate`), et génération de requêtes en langage naturel.
- Tarification à l'usage : 0,115 $ par heure de Compute Unit active, 0 $ en pause, 0,30 $ par Go-mois de stockage utilisé, avec un palier gratuit de 50 CU par mois.
- Upgrade en un clic vers AlloyDB complet pour la production, en conservant données, schémas, utilisateurs et chaînes de connexion.

## Analyse approfondie
Les bases de données ont du mal à suivre le rythme du développement logiciel propulsé par l'IA. Dans les équipes d'ingénierie et de plateforme que nous rencontrons, nous voyons des agents de codage bloqués par un provisionnement de base de données trop lent, des pipelines de test CI/CD freinés par la complexité, et des applications internes qui se heurtent à un mur lorsqu'elles passent du bac à sable à la production. Jusqu'à présent, aucun service PostgreSQL du marché ne combinait des capacités adaptées aux agents avec une sécurité et une scalabilité d'entreprise sans compromis.

Pour résoudre ce problème, nous sommes heureux d'annoncer la préversion d'**AlloyDB Express**, une nouvelle offre d'AlloyDB pour PostgreSQL conçue spécifiquement pour les développeurs et les agents de codage IA. Capable de démarrer en quelques secondes et de se mettre automatiquement en pause en cas d'inactivité, elle aide à combler l'écart entre un développement rapide piloté par l'IA et une infrastructure d'entreprise robuste. Le résultat est un environnement de base de données hautement sécurisé et économique qui accélère la façon dont vous construisez des applications et qui peut facilement évoluer jusqu'à l'échelle de production. Démarrez avec le palier gratuit et ne payez que ce que vous utilisez.

AlloyDB Express est une base de données prête pour les agents, qui vous offre :

- **Création de base de données en moins de deux secondes :** créez une base PostgreSQL prête à l'emploi en moins de deux secondes via `gcloud` CLI, l'API REST, MCP, Terraform ou la Console.
- **Scale-to-zero :** votre base se met automatiquement en pause après 15 minutes d'inactivité, afin que vous n'engagiez aucun coût de calcul pendant qu'elle est inactive. À l'arrivée d'une nouvelle requête, elle se réveille automatiquement en quelques secondes.
- **Prête pour l'entreprise, avec IA et sécurité intégrées :** accédez à des capacités d'IA d'entreprise, y compris la recherche vectorielle, textuelle et hybride, pour construire rapidement des applications d'IA, tout en étant protégé par des garde-fous de sécurité d'entreprise intégrés.
- **Démarrez gratuitement et ne payez que ce que vous utilisez :** démarrez avec notre allocation mensuelle gratuite et, à mesure que vous évoluez, ne payez que ce que vous utilisez.
- **Mise à niveau en un clic vers l'échelle de production :** lorsque votre application est prête pour la production, mettez à niveau votre base de données existante vers AlloyDB en un clic — en conservant intactes les données, les schémas, les utilisateurs et les chaînes de connexion, tout en gagnant la haute disponibilité (HA) d'entreprise, les réplicas de lecture et la reprise après sinistre (DR).

### Accélérer le développement sans compromettre la sécurité

AlloyDB Express combine la rapidité du self-service avec une sécurité d'entreprise intégrée. Pour les créateurs d'applications et les agents de codage, cela signifie que vous pouvez provisionner instantanément des bases PostgreSQL entièrement isolées sans configuration manuelle, permettant à chaque test et prototype de s'exécuter dans sa propre base dédiée. Et pour les administrateurs de plateforme et de sécurité, vous définissez une seule fois, de façon centralisée, les politiques IAM, réseau et d'organisation, et chaque base AlloyDB Express créée par un développeur ou un agent de codage reste automatiquement dans le périmètre de sécurité de votre entreprise.

Que le code soit écrit par des développeurs ou par des agents IA, la sécurité reste assurée par des mécanismes de protection intégrés qui :

- **Minimisent l'exposition grâce à des connexions sécurisées par défaut :** gardez vos données à l'abri de l'internet public en utilisant des endpoints DNS publics qui masquent les adresses IP et bloquent le trafic entrant jusqu'à autorisation explicite.
- **Sécurisent les intégrations internes via un réseau VPC privé :** connectez en toute sécurité vos charges de travail internes grâce à Private Service Connect (PSC) ou au DNS privé.
- **Appliquent le principe du moindre privilège avec des contrôles d'accès granulaires :** restreignez en toute confiance les permissions des agents et des utilisateurs en utilisant Google Cloud IAM, VPC Service Controls, et les rôles natifs de PostgreSQL.

### AlloyDB Express apporte des capacités d'IA intégrées

À la différence des bases de données qui s'appuient sur des magasins vectoriels externes ou des configurations complexes, AlloyDB Express intègre directement des outils d'IA d'entreprise dans votre base de données, afin que vous puissiez vous concentrer sur la construction de fonctionnalités. Vous pouvez accélérer le développement de vos applications d'IA grâce à des outils tels que :

- **Recherche vectorielle rapide (index pgvector HNSW et ScaNN de Google) :** stockez et recherchez des embeddings vectoriels aux côtés de vos données opérationnelles pour la recherche sémantique, les moteurs de recommandation et la mémoire d'agent (RAG) — sans synchroniser les données vers une base vectorielle séparée.
- **Accès direct aux modèles Gemini au sein des requêtes SQL :** générez des embeddings de texte ou d'image à la volée, et exécutez du filtrage sémantique, du classement et de la synthèse (`ai.if`, `ai.rank`, `ai.generate`) directement dans des instructions `SELECT` et `INSERT` standards.
- **Génération de langage naturel vers SQL :** permettez aux développeurs et aux agents IA de poser des questions en anglais courant pour générer, exécuter et affiner des requêtes en quelques secondes, grâce à AlloyDB Studio intégré et aux API de langage naturel.

### Démarrez avec le palier gratuit et ne payez que ce que vous utilisez

AlloyDB Express propose une tarification simple et intuitive, et passe à zéro lorsqu'elle est inactive. Les données restent en sécurité, et la base de données se réveille instantanément dès qu'une nouvelle requête arrive. Voici un bref résumé de notre tarification :

- **Calcul actif :** 0,115 $ par heure de Compute Unit (CU-hr), facturé à la seconde.
- **Calcul en pause :** 0,00 $ par heure en cas d'inactivité de plus de 15 minutes.
- **Stockage utilisé :** 0,30 $ par Go-mois, facturé uniquement pour l'espace disque réellement utilisé par vos données.

Par ailleurs, Google Cloud offre un palier gratuit, ce qui facilite les débuts avec 50 CU gratuites chaque mois. Pour plus de détails, consultez la page de tarification d'AlloyDB Express.

### Commencez dès aujourd'hui

AlloyDB Express est disponible dès aujourd'hui en préversion. Essayez-la dans la console Google Cloud ou consultez la page de documentation d'AlloyDB Express pour plus de détails sur la façon de démarrer.

## Pourquoi ça compte
Ce lancement illustre la course des fournisseurs cloud à adapter leurs bases de données aux workflows pilotés par des agents IA (provisionnement instantané, scale-to-zero, IA native en SQL), un signal à suivre pour quiconque surveille l'évolution de l'infrastructure data au service du développement assisté par IA.
