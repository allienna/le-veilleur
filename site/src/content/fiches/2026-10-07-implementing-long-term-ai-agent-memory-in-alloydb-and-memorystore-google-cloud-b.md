---
title: "Implementing long-term AI agent memory in AlloyDB and Memorystore | Google Cloud Blog"
date: 2026-10-07
url: "https://cloud.google.com/blog/products/databases/implementing-long-term-ai-agent-memory-in-alloydb-and-memorystore/"
authors: ["Itai Rosenblatt", "Paul Ramsey"]
keywords: ["mémoire agent IA", "AlloyDB", "Memorystore", "recherche hybride", "architecture deux niveaux", "embeddings"]
theme: "IA"
tone: "tutorial"
used_in: ["2026-10-07"]
---

## Résumé
Cet article de blog Google Cloud présente une architecture de mémoire à deux niveaux pour les agents IA d'entreprise, combinant Memorystore for Valkey (mémoire tampon à court terme) et AlloyDB AI (mémoire persistante à long terme). L'objectif est de permettre à des agents conversationnels multi-sessions de se souvenir des préférences et contraintes des utilisateurs sans « bourrer » le contexte du LLM à chaque tour, ce qui dégrade la latence, les coûts et la fiabilité. Les auteurs affirment que cette séparation des niveaux de mémoire peut réduire la consommation de tokens jusqu'à 70 % dans des scénarios de dialogues longs et complexes. L'article détaille aussi les fonctions natives d'AlloyDB AI (embeddings automatiques, recherche hybride, génération en base) ainsi que les mécanismes de gouvernance multi-tenant nécessaires en production.

## Points clés
- Les LLM sont intrinsèquement sans état (stateless) : sans mémoire long terme, un agent oublie tout entre deux sessions, ce qui oblige l'utilisateur à tout réexpliquer.
- Les approches naïves (« context stuffing » ou résumés successifs par LLM) sont coûteuses, lentes et avec perte d'information (effet « lost in the middle », détails critiques écrasés par la compression).
- L'architecture recommandée sépare un tampon de session court terme (Memorystore for Valkey, lectures/écritures sub-milliseconde) d'une mémoire persistante long terme (AlloyDB AI, intégrité transactionnelle et recherche hybride vecteurs + texte).
- AlloyDB AI intègre nativement la génération d'embeddings transactionnels, l'exécution de modèles génératifs (ex. Gemini) en SQL, et la recherche hybride via Reciprocal Rank Fusion (RRF).
- Un benchmark interne (dialogues de 45+ tours avec exécutions d'outils) montre des gains mesurables de coût et de latence par rapport au « context stuffing » classique.
- La gouvernance multi-tenant (Row-Level Security, vues sécurisées paramétrées) et la compaction automatique de la mémoire sont essentielles pour un déploiement en production.

## Analyse approfondie

### Le conflit entre workflows avec état et nature sans état des LLM
Les agents IA sont de plus en plus utilisés pour des conversations multi-tours et des workflows de longue durée, mais les grands modèles de langage restent sans état d'une session à l'autre. Lorsqu'un utilisateur revient vers un agent plusieurs jours après, le modèle repart avec une fenêtre de contexte vide. Sans mécanisme pour reconstruire le contexte passé via une mémoire long terme, l'utilisateur doit tout réexpliquer, ce qui crée une expérience frustrante et fragmentée.

Avec la généralisation des fenêtres de contexte à un million de tokens, un raccourci courant consiste à tout injecter dans le prompt à chaque tour — historiques de conversation bruts, journaux d'exécution d'outils, etc. (le « context stuffing »). Ce fut un schéma fréquent dans les débuts de l'usage des modèles IA, mais il pose rapidement des problèmes à grande échelle : les coûts en tokens augmentent à chaque message, les temps de réponse peuvent dépasser 30 secondes même pour des requêtes simples, et le modèle souffre du phénomène « lost in the middle », ignorant des instructions critiques enfouies dans un prompt trop volumineux.

Une autre approche consiste à utiliser des résumés glissants, en demandant périodiquement au LLM de compresser les anciens messages en un paragraphe de synthèse. Cela réduit la taille du prompt, mais la synthèse par LLM est par nature avec perte d'information : après plusieurs cycles de compression, des détails subtils mais importants se perdent comme du bruit de fond. Quelques tours plus tard, l'agent viole discrètement les contraintes fixées plus tôt par l'utilisateur. Une approche plus évolutive est donc nécessaire pour conserver la mémoire des conversations ou tâches passées, sans dégrader l'expérience ni créer de nouveaux goulots d'étranglement.

### Mise en place d'une architecture de mémoire à deux niveaux
Pour construire des agents d'entreprise fiables et économiques qui respectent les garde-fous et contraintes définis, les auteurs recommandent une **architecture de mémoire à deux niveaux** :

- **Tampon de session court terme** : met en cache les tours de conversation actifs en mémoire via une fenêtre glissante bornée en tokens, permettant de garder une taille de contexte stable sur plusieurs échanges, y compris entre appareils, tout en gardant les derniers messages à jour. Ce niveau nécessite des accès sub-milliseconde à haut débit à chaque tour, ce qui rend Memorystore for Valkey particulièrement adapté pour maintenir l'état de session actif.
- **Mémoire persistante long terme** : stocke les faits importants, préférences utilisateur et faits épisodiques à travers les sessions. Ce niveau nécessite une intégrité transactionnelle, une gouvernance des données et une récupération hybride combinant données relationnelles et vecteurs — des capacités fournies nativement par AlloyDB AI.

Bien qu'il soit possible de stocker la mémoire long terme et les tampons de session actifs directement dans une base relationnelle, une architecture à deux niveaux avec un cache en mémoire offre de meilleures performances et une meilleure scalabilité. Les tampons de session actifs sont très éphémères et nécessitent des mises à jour sub-milliseconde à très haut débit à chaque tour de conversation. Traiter ces écritures rapides dans un cache clé-valeur en mémoire évite l'amplification d'écriture et la fragmentation de table dans la base relationnelle, qui nécessiterait sinon des suppressions de lignes fréquentes et un « vacuuming » intensif. C'est analogue à l'ajout d'une couche de cache devant une base de données pour décharger les lectures fréquentes sur des lignes « chaudes ». Cette répartition des tâches garde la base de données principale légère et réactive, lui permettant de se concentrer sur ce pour quoi elle est conçue : la cohérence transactionnelle, la recherche vectorielle hybride complexe, et l'exécution de requêtes analytiques long terme.

En associant la mise en cache court terme de Memorystore for Valkey aux capacités natives d'AlloyDB AI, il devient possible d'exécuter l'extraction d'entités, la compaction de mémoire, la mémoire inter-session et la récupération hybride directement au niveau de la base de données, en gardant les prompts actifs légers, rapides et économiques.

### Les quatre types de mémoire
Pour organiser efficacement l'état long terme d'un agent, les auteurs divisent la mémoire de l'agent en quatre types complémentaires, répartis entre les deux niveaux de stockage décrits ci-dessus. En isolant le contexte de conversation court terme des règles structurées long terme, l'agent récupère le contexte pertinent à la demande sans remplir les fenêtres de tokens avec des journaux d'interaction bruts.

### Le schéma architectural de mémoire à deux niveaux
Le schéma de l'article illustre les chemins de lecture et d'écriture reliant la couche d'orchestration applicative, le tampon court terme **Memorystore for Valkey**, et le dépôt long terme **AlloyDB AI**. Le système fonctionne selon deux chemins d'exécution coordonnés :

- **Le chemin de lecture** : lorsqu'un utilisateur pose une question, l'application récupère la fenêtre glissante active depuis **Memorystore for Valkey**, exécute une normalisation de requête en base via `ai.generate`, puis interroge **AlloyDB** avec `ai.hybrid_search` pour récupérer les règles d'entités pertinentes et les faits épisodiques associés.
- **Le chemin d'écriture** : après génération de la réponse, le tour est immédiatement mis en cache dans **Memorystore for Valkey**. Un worker de file d'attente asynchrone en arrière-plan extrait les entités structurées de l'échange et les écrit directement dans **AlloyDB**, où des embeddings automatiques transactionnels calculent et stockent immédiatement les représentations vectorielles en base.

### Impact business et retour sur investissement
Dans des tests de benchmark sur des dialogues de développement multi-tours (45+ tours avec exécutions d'outils intensives), la séparation entre mise en cache court terme et persistance long terme a permis des améliorations mesurables de coût et de performance par rapport au « context stuffing » naïf.

Les auteurs précisent que ces métriques reflètent des résultats de benchmark interne issus d'une charge de travail simulant un assistant de pair-programming IA d'entreprise interagissant avec un développeur sur plusieurs sessions, projets et changements de contexte. Les économies et latences réelles varient selon la structure des prompts, la fréquence des requêtes et le volume de données.

Ces résultats montrent comment une mémoire à paliers change l'économie unitaire des agents : au lieu d'une courbe de coût croissante à chaque tour supplémentaire, la taille des prompts reste bornée, réduisant les dépenses continues d'API LLM tout en gardant des temps de réponse rapides.

### Avantages techniques clés d'AlloyDB AI
**AlloyDB AI** réduit la charge opérationnelle liée à l'implémentation d'une mémoire d'agent persistante en intégrant les fonctions IA essentielles directement dans le moteur de base de données :

- **Embeddings automatiques transactionnels en base (`ai.initialize_embeddings`)** : AlloyDB génère automatiquement des embeddings vectoriels pour les colonnes de texte via une intégration native avec **Agent Platform** (anciennement Vertex AI), produisant jusqu'à 3 000 embeddings par seconde. Avec `incremental_refresh_mode => 'transactional'`, AlloyDB maintient les embeddings à jour à mesure que les données source changent, dans la même transaction, supprimant le besoin de pipelines d'embeddings personnalisés, de planificateurs externes ou de logique de nouvelle tentative complexe.
- **Fonctions IA générative en base (`ai.generate`)** : AlloyDB permet d'exécuter des modèles de fondation, comme Gemini, directement depuis des requêtes SQL. Cela permet par exemple de décomposer des requêtes composées en sous-requêtes à un seul aspect, et de résoudre des expressions temporelles relatives (comme « la dernière session ») en identifiants explicites — sans aller-retour séparé depuis l'application.
- **Recherche hybride native avec Reciprocal Rank Fusion intégrée (`ai.hybrid_search`)** : AlloyDB fournit une fonction SQL native qui exécute la Reciprocal Rank Fusion (RRF) directement dans le moteur. Elle combine la similarité cosinus vectorielle (`<=>` sur des index HNSW ou ScaNN) avec la recherche plein texte PostgreSQL (BM25, RUM ou GIN) en un seul appel base de données, mêlant correspondance sémantique et récupération par mot-clé exact, tout en supportant le filtrage par métadonnées (`filter_condition`) pour une meilleure performance et une isolation de périmètre déterministe.
- **Intégration directe à Agent Platform avec identifiants IAM** : AlloyDB se connecte directement aux modèles de fondation d'**Agent Platform** via le réseau privé de Google Cloud, en utilisant les rôles de compte de service IAM de Google Cloud et l'authentification base de données, évitant de stocker, faire tourner ou transmettre des clés API dans le code applicatif.
- **Moteur unifié opérationnel, vectoriel et de gouvernance** : AlloyDB consolide les données métier relationnelles, les embeddings vectoriels, les index plein texte et les permissions d'entreprise dans une seule base PostgreSQL conforme ACID, évitant la dérive des données et la complexité d'intégration entre bases opérationnelles et vectorielles séparées.

### Principaux schémas d'implémentation
L'article décrit les schémas de base de données utilisés pour configurer l'architecture de mémoire à deux niveaux (le code complet en Python et SQL est disponible dans le codelab associé) :

1. **Mise en place du schéma et des embeddings automatiques** : dans AlloyDB, installer les extensions nécessaires et définir la table `agent_entities` avec des métadonnées structurées, une colonne `tsvector` générée pour la recherche plein texte, et une colonne d'embedding vectoriel. Générer ensuite les embeddings via `ai.initialize_embeddings` en mode `transactional` pour qu'ils restent à jour. Enfin, créer l'index vectoriel HNSW et l'index plein texte RUM pour des recherches hybrides rapides et efficaces.
2. **Interrogation de la mémoire long terme via la recherche hybride native** : sur le chemin de lecture, récupérer les entités long terme pertinentes avec `ai.hybrid_search`, qui exécute la RRF directement dans AlloyDB en combinant et en réordonnant les résultats de recherche vectorielle et de recherche plein texte en une seule requête.
3. **Compaction de mémoire en base avec des fonctions IA** : pour gérer la croissance du stockage long terme sans écrire de scripts de nettoyage personnalisés, des requêtes d'extraction et de compaction automatisées peuvent être exécutées directement dans AlloyDB afin d'identifier les éléments importants à conserver. Ce schéma utilise une expression de table commune (CTE) SQL avec `ai.generate` pour consolider les anciennes entrées épisodiques en un résumé dense. Par exemple, une longue interaction sur la complexité de changer des vols avec des enfants peut aboutir à un résumé du type « je préfère les vols sans escale ».
4. **Connexion de l'architecture à deux niveaux à un agent ADK** : une fois l'architecture configurée, il est possible d'étendre le fournisseur de mémoire par défaut d'ADK pour utiliser cette architecture à deux niveaux (par exemple via un `ADKTieredMemoryProvider`). Pour attacher la mémoire long terme à un agent ADK, il suffit de la fournir comme un outil (par exemple `longterm_memory_tool`).

### Gouvernance d'entreprise et sécurité multi-tenant
Faire fonctionner la mémoire d'agent en production d'entreprise exige des frontières de sécurité et des contrôles d'accès stricts. D'abord, il faut maintenir l'**isolation de périmètre et multi-tenant** : en indexant les colonnes `user_id`, `project_id` et `scope` dans `agent_entities` et en appliquant la sécurité au niveau des lignes (Row-Level Security) de PostgreSQL, il est possible d'isoler les mémoires entre départements, équipes et utilisateurs individuels au sein du même cluster de base de données. Les vues sécurisées paramétrées (Parameterized Secure Views, PSV) offrent une couche supplémentaire de sécurité déterministe au niveau applicatif, aidant à se protéger contre les prompts malveillants et les requêtes SQL trop larges.

Il faut aussi assurer une **gestion automatisée du cycle de vie de la mémoire**, comme montré dans le schéma d'implémentation ci-dessus. Combiner des requêtes de compaction SQL planifiées avec un élagage de partitions basé sur le temps aide à maintenir une empreinte de base de données et des latences de requête prévisibles dans la durée.

### Synthèse et prochaines étapes
Découpler les fenêtres de contexte actives du stockage persistant est une approche pragmatique pour construire des agents IA prêts pour la production. En associant **Memorystore for Valkey** pour la mise en cache de session sub-milliseconde et **AlloyDB AI** pour le stockage long terme transactionnel, il est possible d'obtenir des économies de coût en tokens substantielles et des temps de réponse plus rapides, tout en maintenant des règles métier strictes sur des tâches de longue durée et des expériences agentiques à de nombreux tours. Pour démarrer, les auteurs recommandent de suivre le codelab pratique « AlloyDB Agent Memory », de consulter la documentation AlloyDB AI sur le machine learning côté base de données, et d'explorer les guides sur la génération d'embeddings automatiques et la recherche vectorielle hybride.

## Pourquoi ça compte
Ce billet illustre une tendance de fond dans l'infrastructure IA d'entreprise : déplacer la gestion de la mémoire et de la récupération hybride directement dans la couche base de données plutôt que dans l'application, ce qui simplifie l'architecture des agents tout en réduisant significativement les coûts de tokens sur des workflows longs. À surveiller pour quiconque conçoit des agents IA de production avec des contraintes de coût, de latence et de gouvernance multi-tenant.
