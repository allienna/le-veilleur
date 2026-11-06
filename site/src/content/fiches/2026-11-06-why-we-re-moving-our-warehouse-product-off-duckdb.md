---
title: "Why we're moving our warehouse product off DuckDB"
date: 2026-11-06
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fposthog.com%2Fblog%2Fmoving-off-duckdb%3Futm_source=tldrdata/1/010001a1ab694425-7b102ef4-fad4-4bac-bacb-26aa96fcab72-000000/YrPdx-2WlSnxvmF3KI18G38x7UrGM1Sim8ffZHyxlMI=452"
keywords: ["DuckDB", "entrepôt de données", "DuckLake", "architecture distribuée", "PostHog", "Trino"]
theme: "Data"
tone: "news"
used_in: ["2026-11-06"]
---

## Résumé
PostHog explique pourquoi, après avoir reconstruit son produit d'entrepôt de données sur DuckDB il y a cinq mois, l'entreprise l'abandonne déjà. DuckDB et son extension DuckLake, pensés pour un usage mono-nœud, se sont heurtés à des limites de scalabilité, de coût et de fiabilité une fois déployés en production à l'échelle de PostHog (environ 2 Po, 1 000 milliards de lignes). L'entreprise a aussi renoncé aux connexions Postgres directes (port 5432), jugées trop difficiles à faire évoluer par rapport à HTTP. PostHog a donc repensé son produit autour de sa propre variante de Trino et d'un nouveau format de table ouvert, HogLake.

## Points clés
- DuckDB est excellent en mono-nœud mais mal adapté à un déploiement cloud multi-locataires : il faut dimensionner les workers avant même de connaître la requête.
- DuckLake (le format lakehouse construit sur DuckDB) impose un schéma de catalogue portable entre SGBD, ce qui limite les optimisations spécifiques et provoquait des écritures de plus de 3 minutes par table.
- Plus de 99 % des lignes de statistiques du catalogue appartenaient à des tables déjà supprimées, un problème récurrent malgré des nettoyages ponctuels.
- Les connexions Postgres directes (port 5432) se sont révélées bien plus difficiles à répartir en charge et à maintenir que de simples connexions HTTP.
- PostHog a dogfoodé DuckLake en interne à très grande échelle (~2 Po, 15,3 millions de snapshots) avant de devoir forker le projet, perdant ainsi le bénéfice de la communauté open source.
- La nouvelle architecture repose sur une variante maison de Trino et un format de table propriétaire, HogLake, testé d'abord en interne avant d'être proposé à des partenaires de conception.

## Analyse approfondie
# Pourquoi nous retirons DuckDB de notre produit d'entrepôt de données

Il y a cinq mois, nous avons reconstruit le produit d'entrepôt de données de PostHog sur DuckDB plutôt que sur ClickHouse, comme nous l'avions expliqué à l'époque. Nous l'avons fait parce qu'un cluster ClickHouse partagé ne pouvait pas gérer des requêtes de modélisation durant des heures, et qu'il manquait d'un optimiseur de requêtes basé sur les coûts. DuckDB offrait à chaque client sa propre instance, et des outils comme dbt pouvaient se connecter via Postgres. Nous restons des adeptes de DuckDB.

Mais nous avons sous-estimé l'ampleur et la complexité que prendraient les charges de travail de nos clients. Nous ne voulions pas seulement leur offrir une bonne expérience, nous voulions la meilleure expérience possible quand on paie quelqu'un d'autre pour faire tourner son entrepôt de données. Cela doit fonctionner à n'importe quelle échelle, à un prix juste.

Nous avons donc passé les trois derniers mois à le réarchitecturer, cette fois sans DuckDB.

Nous aimons DuckDB. C'est probablement le meilleur outil mono-nœud pour analyser des montagnes de données, et ce nœud peut être votre ordinateur portable. Il est robuste et fiable. Il termine presque toujours vos requêtes, et s'il manque de mémoire, il déborde sur le disque.

Les mêmes caractéristiques qui en font un excellent outil en local nous ont posé problème dans le cloud. Les clients exécutaient des requêtes plus complexes que prévu, nous avons donc dû ajouter des instances énormes. Ajouter des disques était une option, mais les requêtes auraient été trop lentes et trop coûteuses pour être viables.

Pour faire tourner un moteur mono-nœud en toute sécurité dans le cloud, il faut dimensionner le worker avant même l'arrivée de la requête. L'ergonomie ici est bancale. Nous n'avons pas trouvé de bonne façon d'indiquer aux clients de quelles ressources leurs requêtes auraient besoin. Prédire le CPU et la mémoire nécessaires pour une requête donnée était encore plus difficile.

Les utilisateurs ne devraient pas avoir à s'en soucier. Ils devraient pouvoir exécuter tout ce dont ils ont besoin pour faire leur travail. Notre rôle est de gérer le reste et de le rendre aussi prévisible que possible.

Nous avons aussi rencontré d'autres goulots d'étranglement, comme la récupération de grandes quantités de données depuis S3 sans récupération asynchrone. DuckDB n'a ajouté cette fonctionnalité que récemment.

Pour utiliser DuckDB comme un véritable entrepôt de données à part entière, nous avons installé par défaut l'extension DuckLake. C'est un nouveau format lakehouse créé par les mêmes auteurs, qui suit les mêmes principes que DuckDB : rester simple et fonctionner sur presque n'importe quelle configuration. Cela fonctionne bien jusqu'à un certain point, mais à l'échelle de PostHog, il nous fallait quelque chose conçu dès le départ pour l'échelle distribuée.

Le schéma de catalogue de DuckLake doit rester portable entre de nombreuses bases de données SQL, ce qui limite les optimisations spécifiques à un moteur. À notre échelle, l'écriture d'une seule table pouvait prendre plus de trois minutes, car chaque commit relisait les statistiques de l'intégralité du catalogue.

Nous avons optimisé DuckLake avec des index de table et des ajustements similaires. Mais pour continuer à proposer DuckLake, nous devions rester 100 % compatibles avec son schéma « officiel » existant. Cela nous laissait moins de marge d'optimisation.

Autre problème : plus de 99 % des lignes de statistiques du catalogue appartenaient à des tables qui n'existaient plus. Les nettoyer rendait les écritures 30 à 50 fois plus rapides, mais ces lignes finissaient toujours par repousser.

Nous avons aussi passé beaucoup de temps sur le nombre de connexions que DuckLake ouvre vers les bases de métadonnées. Cela pèse lourd sur des instances Postgres partagées, où chaque connexion a un coût réel.

DuckLake chez PostHog n'a pas commencé petit avant de monter en puissance. Nous nous sommes pleinement engagés et avons mis l'intégralité de PostHog dans un DuckLake pour le dogfooder en tant que premier client.

Au moment où nous l'avons quitté, il contenait environ 2 Po : à peu près 1 000 milliards de lignes et 15,3 millions de snapshots. Il s'est cassé de nombreuses façons, difficiles à corriger dans le périmètre de DuckLake.

Nous aurions préféré contribuer à la communauté existante et l'aider à grandir. Mais nous ne pouvions pas faire aboutir les changements aussi vite que nécessaire, nous avons donc fini par maintenir des correctifs dans un fork, ce qui va à l'encontre d'un des principaux avantages d'utiliser DuckLake : la communauté.

Proposer des connexions Postgres directes sur le port 5432 semble être une excellente idée. En pratique, c'était beaucoup plus difficile à faire évoluer que le HTTP.

Les reconnexions manquantes, la gestion des TTL et des connexions inactives à grande échelle sont compliquées, et les connexions de longue durée sont coûteuses. Il existe aussi très peu d'outillage pour l'équilibrage de charge en pgwire comparé au HTTP. Comparez l'ergonomie d'un AWS NLB à celle d'un ALB, et vous verrez ce que nous voulons dire. Les en-têtes HTTP rendent également le routage dans Kubernetes beaucoup plus flexible.

Il existe aussi une liste interminable de clients Postgres, chacun attendant son propre comportement Postgres particulier. Les clients nous demandaient sans cesse de corriger leur client ou leur bibliothèque. Nous avons passé beaucoup de temps à livrer bon nombre de ces correctifs, mais la couverture n'a jamais été suffisante. Nous préférons consacrer notre temps à construire un excellent produit d'entrepôt de données plutôt qu'à courir après la longue traîne de la compatibilité Postgres.

Nous avons appris à ne plus autant survendre la technologie derrière un entrepôt de données. Ce qui compte, c'est l'expérience qu'elle procure.

Néanmoins, nous sommes heureux de partager ce que nous préparons. Nous avons tout reconstruit autour de notre propre variante de Trino et créé notre propre format de table ouvert, HogLake. Et oui, nous le testons d'abord à l'échelle du pétaoctet de PostHog. Nous l'avons rendu solide avant de le confier à des partenaires de conception.

Si votre entrepôt de données actuel est lent ou coûteux, parlons-en, surtout si vous avez beaucoup de données à interroger. Nous sommes toujours à la recherche de partenaires de conception.

PostHog est la couche de contexte de votre produit. Avec une suite complète d'outils pour développeurs — observabilité IA, analytics produit, replay de sessions, feature flags, expériences, suivi d'erreurs, logs, et plus encore — PostHog ingère et stocke toutes les données dont les agents ont besoin pour diagnostiquer des problèmes, découvrir des opportunités et déployer des correctifs. Un entrepôt de données et un CDP relient le tout, unifiant ce contexte en une seule source que les agents peuvent lire de façon transverse. Vous pouvez tout piloter depuis Slack, l'application web, le bureau (PostHog Desktop), ou votre propre éditeur via le MCP.

## Pourquoi ça compte
Ce retour d'expérience illustre concrètement les limites d'un moteur analytique mono-nœud (DuckDB/DuckLake) une fois poussé à l'échelle multi-tenant du cloud, un cas d'école utile pour quiconque évalue DuckDB, DuckLake ou des architectures lakehouse pour un produit de données exposé à des clients externes.
