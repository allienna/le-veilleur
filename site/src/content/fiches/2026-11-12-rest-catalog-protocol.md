---
title: "REST Catalog Protocol🔗"
date: 2026-11-12
url: "https://substack.com/redirect/8f9ae49b-e4df-4898-9ed6-9a378a58ebd9?j=eyJ1IjoiN3Y1bG1jIn0.HlvPOGYPdVknSYzEK1JIj6IFkAFn8zuyjtfU9Mbft9Q"
keywords: ["Apache Iceberg", "catalogue REST", "API", "métadonnées", "délégation de stockage", "planification de scan"]
theme: "Software"
tone: "research"
used_in: ["2026-11-12"]
---

## Résumé
Le protocole REST Catalog standardise l'accès aux catalogues Apache Iceberg en plaçant la logique catalogue derrière une API HTTP commune, définie par la spécification Iceberg REST Catalog API : un seul client fonctionne avec n'importe quel serveur conforme. Parce que le serveur détient la logique de commit, le protocole permet des capacités impossibles côté client, comme la résolution de conflits côté serveur, les commits multi-tables atomiques et le partage sécurisé de tables via la délégation d'identifiants ou la signature distante. Le document détaille aussi la découverte de configuration, le cache et la fraîcheur des métadonnées, les retries idempotents, la pagination et le reporting de métriques.

## Points clés
- Découverte de configuration via `GET /v1/config`, avec des `defaults`, `overrides` et une liste d'`endpoints` annoncés par le serveur.
- Le commit passe par des `Requirements` (conditions sur l'état actuel) et des `Updates` (changements de métadonnées), validés côté serveur ; un commit multi-tables atomique est aussi prévu.
- La délégation d'accès au stockage se fait via deux mécanismes : la distribution d'identifiants temporaires (credential vending) ou la signature distante des requêtes (remote signing).
- La planification de scan peut être déléguée au serveur (mode `server`), avec un cycle de vie asynchrone (soumission, polling, batches de tâches).
- Des mécanismes de fraîcheur (ETag/`If-None-Match`) et de chargement paresseux des snapshots (`snapshot-loading-mode=REFS`) réduisent le coût de chargement des métadonnées.
- Des clés d'idempotence, la pagination des listes et le reporting de métriques complètent le protocole.

## Analyse approfondie
# Protocole REST Catalog

## Vue d'ensemble

À mesure que l'écosystème Iceberg grandissait, chaque moteur et chaque langage avait besoin de son propre client pour chaque implémentation de catalogue. Le protocole de catalogue REST résout ce problème en plaçant la logique du catalogue derrière une API HTTP commune, définie par la spécification Iceberg REST Catalog API : une seule implémentation client fonctionne avec n'importe quel serveur conforme. Parce que le serveur détient la logique de commit, le protocole permet également des capacités que les catalogues côté client ne peuvent pas offrir, comme la résolution de conflits côté serveur, les commits multi-tables, et le partage sécurisé de tables via la distribution d'identifiants (credential vending) ou la signature distante (remote signing).

Cette page explique les concepts derrière les fonctionnalités du protocole et la façon dont le client Java les utilise. Pour configurer une connexion à un catalogue REST et consulter la référence complète des propriétés du client, voir la page du catalogue REST.

## Découverte des endpoints et configuration fournie par le serveur

À l'initialisation, le client appelle la route de configuration du serveur (`GET /v1/config`, en passant le `warehouse` configuré comme paramètre de requête si celui-ci est défini). La réponse peut ajuster la configuration du client de trois manières :

- **`defaults`** : des propriétés suggérées par le serveur ; la configuration propre du client a priorité sur elles.
- **`overrides`** : des propriétés exigées par le serveur ; elles ont priorité sur la configuration du client. Un override courant est `prefix`, que le client insère dans tous les chemins de requête suivants (`/v1/{prefix}/namespaces/...`) afin qu'un même serveur puisse héberger plusieurs catalogues.
- **`endpoints`** : la liste des endpoints d'API supportés par le serveur. Le client n'utilise que les fonctionnalités dont les endpoints sont annoncés, de sorte qu'un serveur qui n'implémente pas, par exemple, les endpoints de vues ou de planification de scan, rend simplement ces fonctionnalités indisponibles plutôt que de produire des requêtes en échec.

Si le serveur omet entièrement le champ `endpoints`, le client suppose un ensemble par défaut d'endpoints de namespaces et de tables. Pour les anciens serveurs qui supportent les vues mais précèdent la découverte d'endpoints, définissez `view-endpoints-supported=true` (voir les propriétés du catalogue REST).

## Protocole de commit

Contrairement aux catalogues côté client, un client REST n'écrit jamais lui-même un fichier de métadonnées et ne bascule jamais un pointeur. Pour committer, il envoie au serveur la liste des changements qu'il souhaite effectuer (`POST /v1/{prefix}/namespaces/{namespace}/tables/{table}`), exprimée en deux parties :

- Les **Requirements** (exigences) énoncent ce qui doit encore être vrai des métadonnées actuelles de la table pour que le commit soit valide — par exemple, qu'une branche pointe toujours vers le snapshot sur lequel le changement était basé, ou que l'UUID de la table correspond.
- Les **Updates** (mises à jour) sont les changements de métadonnées eux-mêmes, comme l'ajout d'un snapshot, la définition d'une référence de branche, ou la mise à jour du schéma.

Le serveur valide chaque exigence par rapport aux métadonnées actuelles de la table et, si elles sont toutes respectées, applique les mises à jour et écrit les nouvelles métadonnées. Si une exigence échoue, le commit est rejeté et le client rafraîchit la table puis réapplique ses changements avant de réessayer. Parce que le serveur possède cette validation, tous les moteurs bénéficient de la même détection de conflits, et le serveur peut résoudre les conflits ou rejeter les changements invalides de façon centralisée.

Le protocole définit également un endpoint optionnel pour committer des changements sur plusieurs tables en une seule opération atomique (`POST /v1/{prefix}/transactions/commit`), exposé en Java sous la forme `RESTCatalog.commitTransaction`. Les moteurs committent les tables individuellement aujourd'hui, donc il s'agit principalement d'une fonctionnalité de l'API Java, et les serveurs ne sont pas obligés de la supporter.

## Délégation d'accès au stockage

Le protocole REST permet au serveur de catalogue de contrôler l'accès aux données des tables, de sorte que les clients n'ont pas besoin de leurs propres identifiants de stockage à longue durée de vie. La spécification définit l'en-tête `X-Iceberg-Access-Delegation` avec deux mécanismes, et un serveur peut fournir l'accès via l'un ou l'autre, ou les deux :

### Distribution d'identifiants (credential vending)

Le serveur retourne des identifiants de stockage de courte durée, limités à une table (`storage-credentials`), dans la réponse de chargement de table. Lorsqu'ils sont présents, le client les applique lors de la création du `FileIO` de la table, de sorte que les lectures et écritures des fichiers de données et de métadonnées utilisent les identifiants distribués. Parce que chaque identifiant est limité aux préfixes de stockage d'une table, le catalogue devient le point unique de contrôle d'accès.

Le fait que des identifiants soient distribués ou non dépend du serveur. Certains serveurs ne distribuent des identifiants que lorsque la requête porte l'en-tête `X-Iceberg-Access-Delegation`.

Les identifiants distribués expirent ; l'endpoint dédié aux identifiants de la spécification (`GET /v1/{prefix}/namespaces/{namespace}/tables/{table}/credentials`) permet aux clients de récupérer des identifiants frais pour les tâches de longue durée. Le `FileIO` S3 rafraîchit les identifiants de cette manière lorsque `client.refresh-credentials-endpoint` est défini, ce que les serveurs fournissent généralement dans la configuration de table retournée.

### Signature distante (remote signing)

Avec la signature distante, le serveur ne distribue jamais d'identifiants du tout. À la place, le client envoie chaque requête de stockage à l'endpoint de signature du catalogue, et le serveur retourne la requête signée que le client doit exécuter. La configuration de signature est fournie par le serveur dans la réponse de chargement de table. Pour S3, la signature est activée par `s3.remote-signing-enabled=true`, que les serveurs définissent généralement dans la configuration de table qu'ils retournent, de sorte qu'aucune configuration côté client n'est nécessaire.

## Planification de scan côté serveur

Par défaut, le client planifie lui-même les scans : il lit la liste des manifestes et les manifestes, et produit localement les tâches de scan de fichiers. Avec la planification de scan côté serveur, le client soumet plutôt le scan (filtre, snapshot, colonnes sélectionnées) au serveur, qui retourne les tâches de scan. Cela permet au serveur d'appliquer ses propres optimisations — caches de métadonnées, index — et évite au client de télécharger les fichiers de métadonnées.

La planification suit un cycle de vie asynchrone : le client soumet un plan, et le serveur répond soit immédiatement avec le résultat complet, soit retourne un identifiant de plan que le client interroge (poll) jusqu'à ce que la planification se termine. Les résultats volumineux sont retournés en lots de tâches de plan que le client récupère séparément. Le client annule un plan dont il n'a plus besoin, et abandonne après `rest-scan-planning.poll-timeout-ms` (5 minutes par défaut) ou la requête initiale plus `rest-scan-planning.poll-num-retries` tentatives de relance (10 par défaut), selon la limite atteinte en premier.

Le mode de planification est contrôlé par la propriété de catalogue `scan-planning-mode` (`client`, la valeur par défaut, ou `server`), et le serveur peut surcharger le mode par table dans la réponse de chargement de table. La planification côté serveur exige que le serveur annonce les endpoints de planification de scan. Voir les propriétés du catalogue REST pour les clés associées.

## Fraîcheur et mise en cache des métadonnées

Charger une table signifie normalement télécharger l'intégralité de ses métadonnées. Le protocole REST propose deux fonctionnalités qui réduisent ce coût :

**Chargement de table sensible à la fraîcheur.** Lorsque le serveur retourne un en-tête `ETag` avec une réponse de chargement de table, le client mémorise en cache la table chargée et présente l'ETag lors des chargements suivants via `If-None-Match`. Si la table n'a pas changé, le serveur répond `304 Not Modified` et le client réutilise la table en cache au lieu de reparcourir les métadonnées. Le cache est borné et limité dans le temps ; voir les propriétés de cache de table.

**Chargement paresseux des snapshots.** Avec `snapshot-loading-mode=REFS`, le client demande au serveur uniquement les snapshots référencés par les branches et les tags plutôt que l'historique complet des snapshots de la table. Les snapshots restants sont récupérés de manière paresseuse s'ils sont effectivement nécessaires, ce qui accélère le chargement des tables ayant un long historique.

## Relances de commit idempotentes

Un commit dont la réponse est perdue (par exemple, à cause d'un timeout réseau) est dangereux à relancer sans précaution : la première tentative a pu réussir. Si le serveur annonce son support en retournant `idempotency-key-lifetime` dans sa réponse de configuration, le client attache un en-tête `Idempotency-Key` unique aux requêtes de mutation. Lorsqu'une requête est relancée avec la même clé, le serveur la reconnaît et retourne le résultat original au lieu d'appliquer le changement deux fois.

## Pagination

Les endpoints de listage (namespaces, tables, vues) supportent la pagination. Définir `rest-page-size` fait que le client demande des résultats par pages de cette taille ; sinon, la valeur par défaut du serveur s'applique.

## Reporting de métriques

Lorsque le serveur annonce l'endpoint de métriques, le client rapporte les métriques de scan et de commit au serveur (en plus de tout `metrics-reporter-impl` configuré), donnant à l'opérateur du catalogue une visibilité sur l'usage des tables. Cela peut être désactivé avec `rest-metrics-reporting-enabled=false`. Voir Metrics reporting pour le contenu des rapports.

## Pourquoi ça compte
Ce protocole illustre la maturation d'Apache Iceberg vers un véritable standard d'interopérabilité pour les lakehouses : en centralisant la logique de catalogue côté serveur, il simplifie l'intégration multi-moteurs et renforce la sécurité (gestion fine des identifiants), un sujet clé pour toute équipe data qui opère plusieurs moteurs de calcul sur un même lac de données.
