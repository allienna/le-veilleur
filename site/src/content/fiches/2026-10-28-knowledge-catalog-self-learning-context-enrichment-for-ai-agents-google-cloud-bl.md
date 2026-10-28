---
title: "Knowledge Catalog: self-learning context enrichment for AI agents | Google Cloud Blog"
date: 2026-10-28
url: "https://cloud.google.com/blog/products/data-analytics/knowledge-catalog-self-learning-context-enrichment-for-ai-agents/"
authors: ["Firat Elbey", "Vasiya Krishnan"]
keywords: ["gestion de la connaissance", "agents IA", "Google Cloud", "catalogage de données", "contexte d'entreprise", "gouvernance des données"]
theme: "IA"
tone: "news"
used_in: ["2026-10-28"]
---

## Résumé
Google Cloud lance en préversion l'enrichissement contextuel auto-apprenant et une expérience repensée de Knowledge Studio au sein de Knowledge Catalog, son moteur de contexte pour agents IA. S'appuyant sur l'enrichissement déjà propulsé par Gemini, cette nouvelle capacité analyse les interactions entre agents et utilisateurs pour détecter les lacunes de contexte et maintenir à jour les définitions métier, en les extrayant automatiquement de documents, dépôts de code et pages wiki. Knowledge Studio devient le centre de pilotage conversationnel permettant aux context engineers et data stewards d'explorer le graphe de contexte et de valider les changements avant publication. Selon des benchmarks internes de Google, ces capacités rendent les agents près de 4 fois plus précis, avec jusqu'à 33 % de latence réduite et jusqu'à 75 % de tokens économisés.

## Points clés
- L'enrichissement auto-apprenant analyse les traces d'interaction (agents Gemini, Conversational Analytics dans BigQuery, agents personnalisés) pour repérer les métriques non ancrées, définitions manquantes ou questions reformulées, tout en respectant la confidentialité (redaction des PII).
- Chaque proposition de changement (définitions métier, descriptions de tables/colonnes, relations de jointure, golden queries, instructions d'agent) est accompagnée de citations de sources et d'un score de confiance.
- Les administrateurs peuvent configurer un seuil de confiance (ex. 85 %) pour l'auto-publication ; en dessous de ce seuil, ou pour les suppressions sensibles, une Change Request est créée pour validation humaine.
- Les "context sets" sont des sous-ensembles gouvernés du graphe de contexte, propres à un domaine, une équipe ou un agent, avec contrôle d'accès fin via IAM et portabilité grâce à l'Open Knowledge Format (OKF).
- Knowledge Studio offre une cartographie visuelle de l'estate de données, une exploration conversationnelle du graphe de contexte, et un suivi des runs d'enrichissement (planification, usage de tokens, durée).
- Chaque modification est traçable, réversible et journalisée avec provenance complète ; Google précise ne jamais utiliser les données des clients pour entraîner ses modèles.

## Analyse approfondie
Aujourd'hui, nous lançons l'enrichissement contextuel auto-apprenant (préversion) ainsi qu'une expérience Knowledge Studio repensée (préversion) dans Knowledge Catalog, le moteur de contexte de Google Cloud pour les agents. S'appuyant sur l'enrichissement existant de Knowledge Catalog propulsé par Gemini, l'enrichissement auto-apprenant analyse les interactions entre agents et utilisateurs pour détecter les lacunes et maintenir votre contexte métier précis et à jour. Knowledge Studio est le nouveau centre de commande permettant aux context engineers et data stewards d'explorer leur patrimoine de données de manière conversationnelle, de naviguer dans un graphe de contexte visuel, et de passer en revue les changements proposés au graphe de contexte avant leur publication auprès des utilisateurs et des agents.

Un agent ne vaut que ce que valent les définitions, règles et relations à l'échelle de l'organisation sur lesquelles il raisonne — c'est-à-dire le contexte. C'est pourquoi la curation du contexte est devenue l'une des disciplines les plus importantes des capacités agentiques en entreprise. Aujourd'hui, ce travail se fait majoritairement à la main. Les context engineers rédigent des prompts et des mappings agent par agent, tandis que les data stewards tentent de maintenir manuellement à jour les définitions à travers des milliers d'actifs. Mais cette approche s'effondre lorsque les organisations passent d'une poignée d'agents à des milliers, puis à des millions.

L'enrichissement auto-apprenant propulsé par Gemini de Knowledge Catalog transforme cette maintenance manuelle en une boucle de rétroaction continue. En analysant les interactions entre agents et utilisateurs, il identifie le contexte manquant ou obsolète et extrait des définitions vérifiées depuis les playbooks, dépôts de code et documents métier pour les intégrer dans des ensembles de contexte gouvernés et réutilisables. Ensuite, grâce à une recherche optimisée, chaque agent reçoit précisément le contexte dont il a besoin, au lieu de raisonner sur des prompts surchargés et des schémas bruts, et bénéficie d'un apprentissage partagé à l'échelle de l'organisation. Knowledge Catalog rend les agents IA près de 4 fois plus précis, avec jusqu'à 33 % de latence en moins et jusqu'à 75 % de tokens en moins utilisés, selon des benchmarks internes.

### **Maintenir le contexte à jour grâce à l'enrichissement auto-apprenant propulsé par Gemini**

Prenons une question simple posée à un agent Gemini : « Quel a été le revenu net en EMEA le trimestre dernier ? » Y répondre correctement nécessite de savoir comment votre entreprise définit le revenu net, quelles tables contiennent les réservations, et comment elles se joignent — or cette connaissance est généralement dispersée entre un playbook financier dans Google Docs, un modèle de données sur GitHub, et une page Confluence. Les catalogues statiques attendent des experts métier qu'ils capturent et mettent à jour manuellement en amont les définitions métier, les métriques et autres éléments de contexte, afin qu'un agent puisse interroger efficacement les bonnes données. Mais en réalité, les experts ont rarement le temps de documenter chaque actif, et dès que l'équipe finance révise la manière dont les crédits partenaires sont traités le trimestre suivant, les définitions statiques prennent du retard et chaque agent disposant d'une formule codée en dur commence à donner de mauvaises réponses.

La capacité d'enrichissement de Knowledge Catalog agit là où vous conservez déjà vos connaissances métier : dans chaque document, dépôt et table de votre équipe. Elle se connecte à vos données structurées, qu'elles proviennent de sources internes ou tierces, ainsi qu'à vos données non structurées dans Cloud Storage, Google Workspace, GitHub, Confluence et SharePoint. Elle trouve, extrait, assemble et maintient cette connaissance métier pour vous, en reliant ces sources non structurées comme les playbooks et les wikis, et leur contexte, à vos métadonnées structurées dans Knowledge Catalog comme les tables et les schémas, rendant ainsi vos données structurées bien plus découvrables et exploitables. À la demande ou selon un calendrier, elle propose des définitions métier, des descriptions de tables et de colonnes, des relations de jointure, des golden queries, et des instructions d'agent spécifiques à une tâche, chacune accompagnée de citations de sources et d'un score de confiance. À chaque exécution, elle détecte ce qui a changé à la source, retire les définitions obsolètes et signale les conflits pour révision.

Elle apprend à la fois de vos interactions utilisateurs et agents. Vous pouvez configurer l'enrichissement pour analyser les traces d'interaction des agents Gemini, de Conversational Analytics dans BigQuery, ou de vos agents personnalisés, tout en masquant les informations personnelles identifiables (PII). Elle identifie où les agents ont rencontré des difficultés, comme des recherches de colonnes ambiguës, des métriques non ancrées, des définitions manquantes, ou des utilisateurs reformulant la même question. Elle trouve ensuite la réponse faisant autorité et prépare une correction, afin que la même erreur ne se reproduise pas. C'est ainsi que l'ingénierie du contexte parvient à suivre le rythme de millions d'interactions d'agents, libérant les experts qui peuvent réviser les changements plutôt que les rédiger de zéro.

*Configuration d'une tâche d'enrichissement avec sources connectées, évaluation et auto-apprentissage*

L'automatisation ne signifie pas abandonner le contrôle. Vous pouvez choisir d'activer ou de désactiver la publication automatique à tout moment, et définir le score de confiance exact (par exemple 85 %) à partir duquel les changements proposés sont automatiquement approuvés. Tout ce qui est en dessous de votre seuil, ainsi que les mises à jour sensibles comme les suppressions, deviennent une Change Request qu'un steward doit approuver, modifier ou rejeter. Vous pouvez également fournir votre propre jeu d'évaluation pour tester de bout en bout les mises à jour proposées. Chaque changement est journalisé avec une provenance complète et peut être annulé. Et bien entendu, Google n'utilise jamais vos données pour entraîner ses modèles.

*Révision des propositions d'enrichissement, des scores de confiance et des diffs de changement avant publication*

### **Définir le bon contexte pour chaque audience avec les context sets**

Par conception, un graphe de contexte d'entreprise est assez large, mais pour une tâche donnée, les agents comme les utilisateurs n'ont souvent besoin que du bon segment, de confiance, de ce graphe. Knowledge Catalog y répond avec les context sets — des sous-ensembles curatés et gouvernés du graphe de contexte, contenant les définitions, métriques, logique de jointure et golden queries propres à un domaine, une équipe, un agent ou un groupe d'utilisateurs finaux donné. Par exemple, un agent commercial peut être lié au context set « Ventes », tandis que l'assistant d'un analyste financier peut être lié au context set « Finance ». Parce que « revenu net » peut légitimement signifier des choses différentes selon le groupe, chaque domaine maintient ses propres définitions au sein du même catalogue. Cependant, les agents n'ont pas à être liés à un seul ensemble ; grâce à la recherche dans Knowledge Catalog, un agent peut également rechercher dynamiquement et trouver le bon context set pour une tâche donnée.

Les context sets offrent également une gouvernance des données intégrée et un contrôle d'accès granulaire. L'accès à chaque context set est géré via IAM, de sorte que les stewards décident quels agents et utilisateurs peuvent le lire, l'utiliser ou le modifier. Les agents ne récupèrent du contexte que depuis les ensembles pour lesquels ils sont autorisés, et l'accès aux données sous-jacentes continue de suivre vos permissions existantes. Chaque mise à jour est traçable et réversible, et parce que les context sets s'appuient sur l'Open Knowledge Format (OKF), vous pouvez importer un bundle OKF pour en faire un context set et l'exporter à nouveau en OKF, afin que votre contexte reste portable.

*Enrichissements approuvés publiés dans un context set gouverné*

### **Explorer et gouverner l'ensemble dans Knowledge Studio**

Toutes ces capacités se rejoignent dans l'expérience repensée de Knowledge Catalog, conçue pour les context engineers et les data stewards qui curatent et gouvernent le contexte destiné aux agents.

*Navigation visuelle dans le graphe de contexte au sein de Knowledge Studio*

Le nouveau Knowledge Studio transforme Knowledge Catalog, d'un simple répertoire d'inventaire statique, en un centre de commande interactif, vous permettant de :

- **Visualiser la couverture du contexte en un coup d'œil :** naviguez dans une carte visuelle de votre patrimoine de données multicloud, des bases de données opérationnelles et entrepôts de données aux modèles sémantiques, context sets et documentation.
- **Explorer le contexte de manière conversationnelle :** posez des questions métier en langage naturel, parcourez les relations à travers votre graphe de contexte d'entreprise, et observez exactement comment les agents raisonnent sur vos métadonnées.
- **Réviser et valider les enrichissements en un seul endroit :** inspectez chaque changement proposé, les citations de sources et le score de confiance. Testez les context sets face à de vraies questions, et approuvez, modifiez ou annulez les change requests avec un contrôle de version de type logiciel.
- **Surveiller les runs d'enrichissement :** suivez le calendrier, les résultats, l'usage de tokens et la durée d'exécution de chaque tâche d'enrichissement, et recevez une notification par e-mail lorsqu'un run se termine.

## Pourquoi ça compte
Cette annonce illustre une tendance de fond : la gouvernance et le maintien automatisé du contexte métier deviennent un prérequis critique pour déployer des agents IA fiables à grande échelle en entreprise, au même titre que l'observabilité l'a été pour les microservices.
