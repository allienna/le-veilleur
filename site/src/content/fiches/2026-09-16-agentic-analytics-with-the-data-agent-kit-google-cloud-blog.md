---
title: "Agentic analytics with the Data Agent Kit | Google Cloud Blog"
date: 2026-09-16
url: "https://cloud.google.com/blog/products/data-analytics/agentic-analytics-with-the-data-agent-kit/"
authors: ["Jeff Nelson"]
keywords: ["agent IA", "MCP", "BigQuery", "Cloud SQL", "dbt", "analytique agentique"]
theme: "Data"
tone: "tutorial"
used_in: ["2026-09-16"]
---

## Résumé
Google Cloud présente le Data Agent Kit, un ensemble de serveurs MCP (Model Context Protocol) et de "skills" agentiques permettant aux data practitioners de mener des investigations de données directement depuis leur IDE, sans jongler entre plusieurs consoles et dialectes SQL. L'article illustre son fonctionnement à travers un cas concret : comprendre pourquoi la valeur moyenne des commandes (AOV) a chuté de 7% en janvier alors que le chiffre d'affaires total restait stable. En interrogeant successivement BigQuery, Cloud SQL et Cloud Storage via un agent conversationnel, l'auteur identifie la cause racine (un nouveau canal B2B associé à un code promo à -25%) puis transforme cette investigation ponctuelle en pipeline dbt reproductible. Le kit est disponible en preview pour plusieurs IDE et outils agentiques, dont Claude Code.

## Points clés
- Le Data Agent Kit combine le protocole MCP (connexion de l'agent aux outils, bases de données et infrastructures cloud) et des "skills" (fichiers markdown enseignant à l'agent les spécificités d'une stack donnée).
- Il est disponible comme extension pour les forks de VS Code (Antigravity IDE, Cursor) et comme plugin pour Antigravity 2.0, Antigravity CLI, Claude Code et Codex.
- Dans l'exemple traité, l'agent interroge tour à tour un entrepôt de données (BigQuery), une base opérationnelle (Cloud SQL/Postgres) et un stockage d'objets (Cloud Storage) au sein d'une même conversation.
- L'IDE demande une autorisation explicite avant d'exécuter des outils MCP (ex. `execute_sql_readonly`), avec la possibilité d'accepter une fois ou de façon permanente, et permet d'inspecter chaque requête SQL générée.
- La cause de la baisse d'AOV n'était pas un déclin réel, mais un effet de mix produit : l'apparition d'un canal B2B-Wholesale à faible panier moyen (~75$) diluant la moyenne globale, liée à un code promo BIGORDER25 à -25%.
- L'agent peut aussi industrialiser une investigation ad hoc en projet dbt reproductible, y compris en déboguant lui-même les échecs de build (ex. doublons sur `order_id` dus à des foyers multi-animaux).

## Analyse approfondie
### Le point de départ : une question ouverte du directeur
L'auteur, Jeff Nelson (Developer Advocate chez Google), part d'un scénario familier : un lundi matin, le directeur envoie un message demandant pourquoi la valeur moyenne des commandes a baissé de 7% en janvier alors que le chiffre d'affaires total est resté stable. Ce type de question est difficile car il n'existe pas de tableau de bord unique pour y répondre : il faut creuser, et chaque élément de réponse se trouve dans un système différent — l'historique des ventes dans un entrepôt de données, les fiches clients en production dans une base PostgreSQL, et les règles des campagnes marketing sous forme de fichiers JSON bruts dans un espace de stockage objet. Chaque requête prise isolément est simple à écrire, mais on finit par répéter les mêmes clauses `WHERE` et sous-requêtes, changer de dialecte SQL à chaque système, et perdre une après-midi entière avec dix onglets ouverts pour une seule question.

### Le Data Agent Kit
C'est ce problème que le Data Agent Kit cherche à résoudre. Il s'agit d'un ensemble de serveurs MCP et de skills agentiques permettant aux développeurs de données d'exécuter leurs workflows directement depuis leur IDE. Il est proposé à la fois comme extension pour les forks de VS Code (Antigravity IDE, Cursor) et comme plugin pour d'autres outils (Antigravity 2.0, Antigravity CLI, Claude Code, Codex) — inutile donc de quitter son environnement de développement pour obtenir des réponses.

Le kit repose sur deux mécanismes principaux :
- Le Model Context Protocol (MCP) : un standard ouvert qui connecte l'agent à des outils, des bases de données et des infrastructures cloud distantes.
- Les skills : des fichiers markdown qui enrichissent la connaissance de l'agent en lui enseignant comment interagir avec une stack technique spécifique.

Au lieu de générer des extraits SQL à copier-coller dans une console, le Data Agent Kit permet à l'agent d'exécuter lui-même les requêtes et d'en lire les résultats pour le compte de l'utilisateur.

L'article illustre ce fonctionnement sur le scénario de l'AOV, avec un entrepôt de données BigQuery, une instance Postgres sur Cloud SQL, et les règles de campagne stockées sur Cloud Storage.

### Comprendre ce qui s'est passé
L'investigation démarre dans le panneau de chat de l'IDE, avec un prompt en langage naturel visant à confirmer les chiffres de départ.

### Vérifier le travail de l'agent
L'agent traite le prompt, invoque les skills pertinentes et se prépare à interroger les données. Mais avant toute exécution, l'IDE marque une pause pour demander l'autorisation d'utiliser les outils MCP nécessaires (par exemple `execute_sql_readonly`). L'utilisateur peut autoriser ponctuellement, à des fins d'audit, ou choisir "toujours autoriser" pour fluidifier le workflow. Une fois l'approbation donnée, l'agent envoie ses requêtes.

Les IDE agentiques permettent d'inspecter la trace d'exécution, qui révèle chaque appel d'outil MCP ainsi que le SQL brut envoyé à BigQuery. Il reste important de surveiller le code généré, même si relire une requête prend généralement bien moins de temps que d'en écrire une sur des schémas peu familiers.

### Décomposer les chiffres
Les données montrent que la valeur moyenne des commandes est restée autour de 110$ d'août à décembre, avant de chuter à 103$ en janvier. Pour comprendre pourquoi, l'utilisateur demande à l'agent d'approfondir l'analyse.

Les résultats révèlent une moyenne faussée plutôt qu'un véritable déclin de l'activité : les canaux Online et Offline restent sains (~110$), mais un nouveau canal appelé B2B-Wholesale apparaît en janvier avec une AOV de seulement ~75$. Rien n'a donc réellement décliné — c'est le mix produit qui a changé.

### Basculer vers Cloud SQL
Une fois la cause de la baisse identifiée, il reste à savoir qui sont ces acheteurs B2B. Les fiches clients étant stockées dans une base opérationnelle Cloud SQL/Postgres, l'utilisateur poursuit dans le même fil de conversation.

L'agent bascule alors vers le serveur MCP Cloud SQL et inspecte la table `customers`. Il apparaît que les 100 comptes wholesale sont de toutes nouvelles entités professionnelles créées au cours des 30 derniers jours ; aucune n'existait en décembre.

### Passer par le terminal
Un examen rapide des commandes B2B dans BigQuery montre que 92% d'entre elles ont utilisé le code promo `BIGORDER25`. L'utilisateur demande alors à l'agent de retracer ce code jusqu'aux fichiers de campagne, ce qu'il fait en utilisant le serveur MCP Google Cloud Storage pour accéder au fichier concerné.

La campagne marketing révèle qu'un code de réduction de 25% a généré un grand nombre de commandes wholesale à bas prix, ce qui a fait baisser l'AOV mixte tout en laissant le chiffre d'affaires total stable.

En une seule session de chat, l'agent a ainsi interrogé des données analytiques (BigQuery), des données opérationnelles (Cloud SQL) et des métadonnées non structurées (Cloud Storage) pour identifier la cause racine du problème.

### Informer le directeur
L'utilisateur peut ensuite demander à l'agent de produire un résumé exécutif à destination du directeur. Et voilà : avec quelques prompts en langage naturel depuis l'IDE, la question ouverte du directeur trouve sa réponse.

### Construire un pipeline reproductible
L'analyse de cause racine n'est qu'une partie du travail. La prochaine fois que ce problème surviendra, il ne sera pas nécessaire de refaire toute l'investigation : celle-ci peut être transformée en modèle de données reproductible. L'utilisateur demande donc à l'agent de convertir son analyse ad hoc en projet dbt persistant.

À partir d'un seul prompt, l'agent crée un environnement virtuel Python avec `dbt-bigquery`, puis rédige les modèles et tests du projet. Mais la commande `dbt build` échoue : le test d'unicité détecte des doublons sur `order_id`. La cause : certains clients possèdent plusieurs animaux de compagnie, et la première version du modèle rattachait ces profils directement à chaque commande — une commande provenant d'un foyer à trois animaux se retrouvait ainsi dupliquée en trois lignes (non unique).

L'agent lit lui-même la sortie de son terminal, détecte l'échec, réécrit la logique dbt et relance le processus jusqu'à ce que le build passe. Ce point souligne une leçon importante sur les workflows agentiques : les agents sont capables d'écrire des quantités de code considérables, mais il reste nécessaire d'appliquer des contrôles de qualité des données sur son pipeline (heureusement, un agent peut aussi les écrire). La prochaine fois que la direction demandera pourquoi l'AOV a bougé, un modèle dbt sera prêt à répondre.

### Conclusion
Un IDE agentique évite d'avoir à naviguer sans cesse entre l'entrepôt de données, les bases de données, le stockage d'objets et le terminal. En associant des standards ouverts comme MCP à des skills d'agent modulaires et éditables, le Data Agent Kit supprime la friction entre la question et la réponse. Explorer des schémas peu familiers, traduire entre dialectes, écrire des jointures déjà écrites des centaines de fois : tout cela devient le travail de l'agent. L'utilisateur, lui, reste aux commandes de l'investigation.

### Essayer soi-même
Le Data Agent Kit est en preview et fonctionne nativement avec Antigravity (2.0, CLI, IDE), Claude Code, Codex, Cursor et d'autres outils populaires. Google Cloud propose un codelab pas à pas ("Analytics with Data Agent Kit and Antigravity IDE"), une documentation dédiée à l'extension Data Agent, ainsi qu'un dépôt GitHub open source regroupant les skills et outils du plugin.

## Pourquoi ça compte
Ce cas d'usage illustre concrètement comment le MCP et les agents "skills-augmentés" commencent à transformer le travail des data practitioners, en unifiant des sources hétérogènes (entrepôt, base opérationnelle, stockage objet) directement depuis l'IDE — une tendance clé à suivre pour l'évolution des outils d'analytique agentique en entreprise.
