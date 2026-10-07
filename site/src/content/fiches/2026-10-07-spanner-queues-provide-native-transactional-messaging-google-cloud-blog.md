---
title: "Spanner queues provide native transactional messaging | Google Cloud Blog"
date: 2026-10-07
url: "https://cloud.google.com/blog/products/databases/spanner-queues-provide-native-transactional-messaging/"
authors: ["Nitin Sagar", "Matthew Mucklo"]
keywords: ["Spanner", "messagerie transactionnelle", "agents IA", "files d'attente", "Google Cloud", "orchestration multi-agents"]
theme: "Data"
tone: "news"
used_in: ["2026-10-07"]
---

## Résumé
Google Cloud annonce la disponibilité générale de Spanner queues, un système de messagerie transactionnelle natif intégré directement à sa base de données Spanner. L'objectif est de permettre aux agents IA de modifier leur état interne et d'enfiler des tâches d'exécution (vers d'autres agents ou systèmes) au sein d'une seule transaction ACID, évitant ainsi les incohérences classiques entre bases de données et files de messages séparées. La fonctionnalité apporte la planification temporelle, la lecture en streaming via SQL, les baux de messages (leases) et l'accusé de réception atomique, tout en restant interrogeable avec du SQL standard. Elle vise aussi bien les architectures agentiques que les cas d'usage événementiels plus classiques (flux d'activité, commerce, finance).

## Points clés
- Spanner queues permet d'enfiler un message comme une simple écriture supplémentaire dans une transaction Spanner existante : l'état et l'action associée valident ou échouent ensemble.
- Le système supprime le besoin de patterns outbox, de couches d'idempotence et de workers de réconciliation habituellement nécessaires pour synchroniser base de données et file de messages.
- Fonctionnalités clés : enfilage atomique « decide-and-act », livraison différée/planifiée, lecture en streaming SQL via une fonction table RECEIVE_<QueueName>, et renouvellement de bail via RENEWLEASE_<QueueName>.
- L'accusé de réception utilise ASSERT_ROWS_MODIFIED 1 pour éviter que des workers « en retard » (après expiration de leur bail) n'écrasent un état déjà traité par un autre worker.
- Spanner queues se distingue des Spanner change streams : les change streams servent la capture de changement de données (CDC) vers des systèmes d'analyse, tandis que les queues sont conçues pour l'orchestration transactionnelle de tâches.
- La fonctionnalité est positionnée comme le complément qui « boucle » l'offre agentique de Spanner, déjà doté de capacités relationnelles, de recherche hybride, de graphe et clé-valeur.

## Analyse approfondie
Les agents IA ne se contentent pas de répondre à des requêtes : ils peuvent émettre des remboursements de façon autonome, gérer des stocks, exécuter des transferts en plusieurs étapes et orchestrer des sous-agents, pour ne citer que quelques workflows agentiques complexes. Cela exige fréquemment que les agents maintiennent un état interne dans une base de données opérationnelle tout en déclenchant des actions asynchrones via un système de file de messages ou d'événements séparé. Et malheureusement pour les équipes qui construisent ces applications, gérer deux systèmes avec des points de validation disjoints détruit la cohérence transactionnelle dans les systèmes agentiques.

Aujourd'hui, nous sommes heureux d'annoncer la disponibilité générale de **Spanner queues** : une messagerie transactionnelle native intégrée directement dans Spanner. Conçue spécifiquement pour une exécution agentique fiable, Spanner queues fait de la création d'un message une simple écriture supplémentaire dans votre transaction. Le changement d'état d'un agent et les actions en aval prévues valident de façon atomique, ou échouent complètement.

Comparez cela aux approches traditionnelles : lorsque la mise à jour d'état en base réussit mais que l'envoi de l'action échoue, votre agent IA décide d'agir mais n'exécute rien. Si l'envoi du message réussit mais que la transaction d'état est annulée (rollback), votre agent exécute une action basée sur un état invalide. Dans la coordination multi-agents asynchrone, les tentatives de nouvelle exécution (retries), la spéculation et les situations de concurrence (race conditions) amplifient ces défaillances, forçant les développeurs à construire des patterns outbox complexes, des couches d'idempotence et des workers de réconciliation — une lourde taxe de fiabilité sur l'architecture agentique.

### Capacités clés pour les architectures agentiques

Spanner queues introduit plusieurs capacités fondamentales pour soutenir ces workflows asynchrones complexes sans ajouter de surcharge d'infrastructure.

**Enfilage atomique « decide-and-act ».** Au sein d'une seule transaction de lecture-écriture Spanner, les agents peuvent mettre à jour des tables de mémoire ou d'état interne et enfiler des tâches vers des agents pairs simultanément. Appuyé par la sérialisabilité stricte et la cohérence externe globale de Spanner, le changement d'état et l'intention d'exécution valident comme une unité atomique unique.

**Exécution planifiée et délais.** Les messages de file peuvent être distribués immédiatement après validation ou planifiés pour une livraison future. Des patterns agentiques comme les nouvelles tentatives différées, les points de contrôle planifiés d'agent, ou les minuteurs d'escalade de SLA peuvent être enfilés de façon transactionnelle en même temps que les mises à jour de mémoire, sans nécessiter de planificateurs cron externes ni d'infrastructure de scrutation (polling).

**Extraction SQL en streaming pour les workers d'agents.** Les agents autonomes consomment les tâches de façon dynamique via des lectures SQL en streaming. Les runtimes d'agents diffusent les tâches entrantes, les traitent au fur et à mesure que la capacité se libère, et accusent réception de l'achèvement de la tâche au sein d'une transaction pour garantir la fiabilité de l'état d'exécution de bout en bout.

**Persistance de la mémoire épisodique et transferts.** Les mises à jour de la mémoire d'un agent — y compris les résumés épisodiques long terme, les transitions d'état réflexives, et les transferts de contexte entre sous-agents — peuvent être persistées de façon asynchrone et transactionnelle via les files. Cela garantit que la mémoire interne d'un agent reste pleinement synchronisée avec son historique d'exécution sans bloquer les tours d'interaction en temps réel.

### Pourquoi Spanner queues est essentiel pour les agents autonomes

**Exécution d'agent transactionnelle exactement-une-fois :** lorsqu'un agent évalue les résultats d'un appel d'outil, la modification d'état, la persistance du raisonnement et les tâches d'invocation d'outil en aval sont enregistrées dans une seule transaction. Nous garantissons une livraison au moins une fois et un accusé de réception au plus une fois, ce qui permet d'atteindre un traitement exactement une fois.

**Orchestration et transferts multi-agents robustes :** dans les systèmes multi-agents (A2A), le transfert d'état d'un agent principal vers un agent spécialisé est représenté comme un message durable, validé de façon transactionnelle. Les workers d'agents spécialisés reçoivent des messages livrables tout en maintenant une lignée totalement auditable des interactions entre agents.

**Délais d'attente de premier ordre et workflows avec humain dans la boucle :** les workflows d'agents nécessitent fréquemment une mise en pause pour des approbations humaines ou des suivis planifiés. Spanner queues gère nativement la gestion des délais d'attente : une transaction unique enregistre l'état d'approbation en attente et planifie un message d'escalade automatisé, résolvant la situation selon lequel des deux événements se déclenche en premier.

**Observabilité native en SQL pour les files d'agents :** inspecter les charges de travail d'agents en cours, surveiller les retards de traitement des tâches, ou auditer l'historique d'exécution des agents peut se faire avec des requêtes SQL standard sur les tables de file, évitant les magasins de messages opaques (boîtes noires).

### Au-delà des workflows agentiques

Au-delà des agents IA, Spanner queues sert de plateforme de messagerie flexible et multi-usage pour diverses architectures événementielles traditionnelles. Qu'il s'agisse d'alimenter des flux d'activité en temps réel dans des applications sociales, de délivrer des mises à jour en direct dans l'édition d'actualités, d'orchestrer le traitement des commandes et des workflows de stocks dans le commerce de détail, ou de gérer le traitement asynchrone à haut débit de tâches et les notifications de transaction dans les services financiers, Spanner queues fournit une base solide pour la livraison asynchrone de messages et les workflows événementiels transactionnels au sein de votre base de données principale.

### Sous le capot : la mécanique transactionnelle de Spanner queues

Parce que les files de Spanner queues sont représentées comme des structures relationnelles de premier ordre dans Spanner, vous définissez, inspectez et gérez les files en utilisant le GoogleSQL que vous connaissez déjà.

#### 1. Définir une file et enfiler de façon atomique

Lorsqu'un agent décide d'approuver un remboursement client, il met à jour la table Orders et envoie une tâche d'exécution à la file OrderAgentTasks au sein d'une seule transaction ACID :

Cela garantit que la tâche EXECUTE_REFUND existe si et seulement si le statut de la commande a bien transitionné vers REFUND_APPROVED.

#### 2. Planification temporelle et annulation atomique

Pour les workflows qui dépendent du temps — comme attendre jusqu'à 72 heures l'approbation d'un manager avant d'escalader — les agents renseignent la colonne système DeliverTime pour différer la visibilité du message :

Si le manager approuve la demande après quatre heures, votre application n'a pas à gérer d'alertes d'escalade fantômes se déclenchant des jours plus tard. En une seule transaction, vous mettez à jour le statut de la commande et annulez la tâche d'escalade en attente en utilisant une instruction SQL DELETE standard :

#### 3. Consommation en streaming, renouvellement de bail et accusé de réception atomique

Les workers d'agents en aval consomment les tâches en utilisant la fonction table (TVF) RECEIVE_<QueueName> sur une connexion SQL en streaming (ExecuteStreamingSql). Spanner gère automatiquement les baux de message, retournant un SpannerLeaseToken unique et un horodatage d'expiration à chaque tâche louée :

Parce que les tâches d'agents IA impliquent souvent un raisonnement LLM en plusieurs tours ou des appels d'API externes qui prennent plus de temps que les fenêtres de bail par défaut, les workers peuvent étendre activement leur bail en utilisant la fonction RENEWLEASE_<QueueName> :

Lorsque l'agent termine l'exécution de son outil externe (en passant TaskId comme clé d'idempotence de l'API externe), il ouvre une transaction de lecture-écriture pour enregistrer l'état final et accuser réception du message en le supprimant avec ASSERT_ROWS_MODIFIED 1 :

L'utilisation d'ASSERT_ROWS_MODIFIED 1 protège votre système contre les situations de concurrence liées à l'expiration des baux. Si un worker s'est bloqué en raison d'une interruption réseau et que son bail a expiré, un autre worker a peut-être déjà traité et supprimé la tâche. Lorsque le worker bloqué reprend et tente d'exécuter l'instruction, ASSERT_ROWS_MODIFIED 1 détecte que la ligne de la file a déjà disparu et lève une erreur au niveau de l'instruction. Intercepter cette erreur et annuler cette transaction empêche les workers obsolètes d'écraser un état de base de données plus récent.

### Spanner change streams vs. Spanner queues

Les Spanner change streams capturent les changements de données en base (insertions, mises à jour, suppressions) en quasi temps réel pour une intégration et un audit en aval. Si les change streams et les queues permettent tous deux aux applications de réagir aux changements de données, les Spanner change streams sont conçus pour la capture de changement de données (CDC) continue et le streaming de données vers l'analytique ou le stockage en aval. À l'inverse, Spanner queues est explicitement conçu pour l'orchestration transactionnelle de tâches, prenant en charge des baux de messages natifs, des livraisons planifiées, l'extraction basée sur SQL, et des accusés de réception atomiques au sein de transactions de lecture-écriture.

### Pour commencer

Spanner fournit une fondation unifiée pour les données agentiques, combinant des capacités relationnelles, de recherche hybride, de graphe et clé-valeur sous une cohérence globale stricte. Spanner queues complète la boucle agentique en permettant aux agents de passer de façon transparente du raisonnement sur les données à l'exécution d'actions transactionnelles au sein d'une seule plateforme unifiée. Spanner queues est désormais disponible en disponibilité générale.

Inscrivez-vous à l'essai gratuit de 90 jours de Spanner et consultez la documentation publique pour commencer à construire des charges de travail agentiques résilientes et exactement-une-fois, en créant une table de file dans votre base de données Spanner dès aujourd'hui.

## Pourquoi ça compte
Cette annonce illustre une tendance de fond : les fournisseurs de bases de données intègrent désormais la messagerie directement dans leur moteur transactionnel pour répondre aux contraintes de fiabilité propres aux architectures d'agents IA autonomes. Pour une veille tech, c'est un signal clair que l'infrastructure data évolue spécifiquement pour soutenir les patterns agentiques multi-étapes et multi-agents, au-delà du cas d'usage classique de requête-réponse.
