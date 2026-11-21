---
title: "Distributed, high-performance blob storage on SQLite - Zerodha Tech Blog"
date: 2026-11-21
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fzerodha.tech%2Fblog%2Fhigh-performance-distributed-blob-storage%2F%3Futm_source=tldrdev/1/010001a1f8e20cf0-04c1a8d2-b096-40a7-9fd6-0fd535581342-000000/3JdHuURk6p0GpZ76ZbmDEtx2GrA6usdi6bB703rb5CI=452"
keywords: ["SQLite", "stockage distribué", "Rust", "sharding", "Redis Cluster"]
theme: "Software"
tone: "research"
used_in: ["2026-11-21"]
---

## Résumé
Zerodha explique dans cet article comment son équipe a conçu Blobasaur, un serveur de stockage de blobs distribué et « shardé », construit sur SQLite, pour remplacer SSDB : une base devenue non maintenue et limitée à un seul nœud. Sur Kite, sa plateforme de courtage (~20 millions de clients), ce système héberge les préférences utilisateur et les configurations d'interface — des objets JSON de quelques kilo-octets à plusieurs méga-octets — avec une latence de l'ordre de la milliseconde pour des débits de plusieurs dizaines de milliers d'opérations par seconde. Écrit en Rust et compatible avec les protocoles Redis et Redis Cluster, Blobasaur répartit les données entre plusieurs fichiers SQLite indépendants afin de paralléliser les écritures, tout en s'appuyant sur la compression zstd et la robustesse native de SQLite (transactions ACID, reprise après crash). Le projet, open source sous licence AGPLv3, est en production chez Zerodha et a entièrement remplacé SSDB après une migration progressive.

## Points clés
- SSDB, non maintenu et limité à un seul nœud (blobs plafonnés à 1 Mo), est remplacé par Blobasaur, un magasin clé-valeur distribué écrit en Rust au-dessus de SQLite.
- SQLite a été retenu car il peut dépasser les performances brutes du système de fichiers pour les petits objets, tout en offrant nativement ACID, reprise après crash et un outillage SQL standard.
- L'architecture répartit les données en plusieurs fichiers SQLite (« shards ») via un hachage cohérent multi-probe, chacun doté d'un writer dédié avec « group commit » — ce qui multiplie le débit d'écriture par 3,3 en passant de 1 à 16 shards.
- La compression zstd intégrée réduit la taille moyenne des blobs d'un facteur ~11 (jusqu'à ~16 au centile 99) avant stockage dans SQLite.
- La montée en charge multi-machines repose sur une implémentation du protocole Redis Cluster (16 384 slots répartis via CRC16), avec migration de shards hors ligne via une CLI dédiée.
- En production, un cluster de 3 nœuds (4 vCPU / 8 Go de RAM) tient une latence p99 d'environ 2 ms sur l'ensemble des commandes, et un p50 compris entre 250 et 550 µs pendant les séances de trading.

## Analyse approfondie

**Contexte et problème initial.** Sur Kite, les utilisateurs personnalisent fortement leurs écrans de trading : dispositions multi-graphiques, modèles d'indicateurs financiers, dessins vectoriels, et préférences d'interface diverses, y compris dans le mode « Terminal » où ils composent eux-mêmes leurs espaces de travail en glissant-déposant des widgets. Ces données sont stockées côté backend comme des blobs opaques, majoritairement du JSON, de quelques kilo-octets à plusieurs méga-octets.

Ces blobs étaient historiquement stockés dans CouchDB, qui s'est révélé mal adapté au débit exigé. L'équipe est alors passée à SSDB, un store C++ persistant sur disque parlant le protocole Redis, facile à intégrer. SSDB a tenu la charge en production pendant plusieurs années, mais deux problèmes ont fini par s'imposer : d'une part son abandon par ses mainteneurs, un risque opérationnel d'autant plus sérieux qu'il est écrit en C++, hors du périmètre de compétence de l'équipe ; d'autre part ses limites d'échelle, SSDB ne fonctionnant que sur un seul nœud, ce qui a notamment forcé à plafonner les blobs à 1 Mo pour éviter une dégradation de latence sur les gros volumes.

**Critères de recherche d'une alternative.** Avec l'arrivée du mode Terminal et l'arrivée de nouveaux services internes, l'équipe a défini un cahier des charges : un store clé-valeur à API simple ; dimensionné pour des blobs multi-méga-octets avec un débit soutenu de plusieurs milliers à dizaines de milliers de requêtes par seconde, dans un trafic irrégulier et en rafales lié à la volatilité des marchés ; une architecture distribuée et horizontalement scalable ; une bonne efficacité disque via la compression ; et une solution simple à maintenir, économique.

**Solutions évaluées et écartées.** Plusieurs bases FOSS orientées stockage de blobs à fort débit ont été testées :
- *ScyllaDB* : déjà utilisé en interne pour d'autres charges à fort débit, mais peu performant sur de gros blobs (débit nettement plus faible, consommation de ressources plus élevée), avec un réglage délicat des tombstones liés aux réécritures fréquentes et aux expirations TTL.
- *PostgreSQL* : expérience interne solide, mais le stockage en colonnes `BYTEA` s'est révélé sous-optimal en performance comme en efficacité disque pour ce cas d'usage.
- *YugabyteDB* : propose du stockage de blobs, mais ce n'est pas sa vocation première ; système large et riche en fonctionnalités jugées superflues.
- *RocksDB* : dispose des bonnes primitives, mais n'est pas pensé pour des écritures multi-Mo à fort débit.
- *Ceph* : complexité opérationnelle et besoins en ressources jugés trop lourds — l'équipe ne l'a même pas testé.
- *SeaweedFS* : le candidat le plus proche, mais bloqué par plusieurs limites : usage intensif de réécritures sur une même clé (changement de workspace utilisateur) alors que SeaweedFS accumule avant compaction, ce qui peut faire croître le disque de façon incontrôlée ; les blobs ont leurs propres identifiants à mapper séparément vers les clés utilisateur ; pas de TTL par blob ; installation relativement complexe à plusieurs composants.
- *S3 et MinIO* : latence par requête trop élevée pour les petits blobs, coûts de requêtes importants sous charge d'écriture intensive (50 % du trafic est en écriture), TTL de cycle de vie trop grossiers par rapport à une expiration exacte par clé — et un coût global prohibitif au vu des volumes (milliers d'opérations par seconde, dizaines de millions par jour).
- *Système de fichiers brut (un fichier par blob)* : impliquerait de réimplémenter soi-même les écritures atomiques et leur regroupement, la gestion d'un grand nombre de fichiers/répertoires, les problèmes classiques d'inodes et de performance disque, ainsi qu'un index de métadonnées séparé pour les TTL — sans compter l'orchestration sur des volumes de stockage AWS.

**Le déclic SQLite.** En parallèle, l'équipe expérimentait SQLite sur un autre projet et avait été marquée par son affirmation d'être jusqu'à 35 % plus rapide que le système de fichiers. Elle disposait aussi d'un système de cache de requêtes créant des millions de tables par jour dans une instance Postgres, poussant cette dernière à ses limites. En combinant ces observations, l'idée est venue de construire, sur SQLite, un système capable de stocker des millions de blobs.

C'est ainsi qu'est né **Blobasaur** : un serveur de blobs « shardé » et open source, écrit en Rust, parlant le protocole Redis et utilisant SQLite comme moteur de stockage. Livré comme un binaire unique, simple à déployer et maintenir, il est aujourd'hui en production chez Zerodha et a remplacé SSDB.

### Ce dont l'équipe avait besoin
De nombreux services Go et Python dialoguaient déjà avec SSDB via le protocole Redis, avec d'autres en attente d'intégration. Les exigences posées pour la nouvelle solution étaient :
- Une compatibilité avec le protocole Redis dans la mesure du possible : les clients existants utilisaient des bibliothèques Redis standards (`GET`, `SET`, `HGET`, `HSET`, `DEL`, `EXPIRE`) ; un remplacement « drop-in » permettrait de ne pas toucher aux services existants et de limiter le risque.
- Une faible latence quelle que soit la taille de la charge utile : servir aussi bien des blobs de paramètres de 2 Ko que des dispositions de graphiques de 5 Mo, en quelques millisecondes.
- Une compression intégrée, la quasi-totalité des charges utiles étant du JSON répétitif qui se compresse bien.
- Des opérations CRUD simples avec TTL, sans besoin de structures de données complexes, de scripting côté serveur, ni de requêtes secondaires — juste du clé-valeur et du hash avec expiration.
- Un partitionnement multi-nœuds pour répartir la donnée sur plusieurs machines et éviter qu'un seul nœud ne devienne un goulot d'étranglement.
- Une durabilité relâchée, jugée acceptable : ce store héberge des préférences UI non critiques, pas de données financières sensibles. En cas de coupure électrique soudaine, un utilisateur pourrait perdre une modification récente de disposition de graphique — gênant, mais sans impact sur le trading. Un compromis de performance jugé pertinent pour cet usage.

### Pourquoi SQLite (et Rust)
Parmi les options de stockage envisagées, le système de fichiers brut (un fichier par blob) aurait obligé à tout réinventer : écritures atomiques et leur regroupement, nettoyage des TTL nécessitant des index secondaires ou un parcours de répertoires, gestion des limites de descripteurs de fichiers, et métadonnées à gérer séparément des données brutes.

SQLite a comblé pratiquement toutes les lacunes du système de fichiers brut. Pour les petits blobs, SQLite peut être jusqu'à 35 % plus rapide qu'un accès disque direct. Si les fichiers bruts deviennent plus rapides au-delà d'environ 100 Kio, les blobs sont compressés avant écriture — et 99 % des valeurs compressées restent bien en dessous de ce seuil.

Utiliser SQLite, c'est aussi hériter d'un moteur de stockage éprouvé : transactions ACID, reprise après crash, et outillage standard — chaque shard sur disque peut être inspecté avec le CLI `sqlite3` classique ou interrogé en SQL pur pour de l'analytique.

Bien que l'essentiel de la pile backend de Zerodha soit en Go, Blobasaur a été écrit en Rust. Le driver SQLite standard de Go repose sur CGo, ce qui complique les builds statiques, épingle les threads OS pendant les appels C sous forte concurrence, et ajoute de la pression sur le ramasse-miettes lors de l'allocation et de la compression de buffers multi-méga-octets. En Rust (avec `sqlx`, `rusqlite` et `tokio`), l'appel direct à l'API C de SQLite offre une consommation mémoire prévisible et permet de livrer un binaire statique unique.

### Architecture

**Répartition des données en shards.** En mode WAL (Write-Ahead Logging), une base SQLite unique autorise des lecteurs concurrents mais un seul écrivain à la fois. Comme les écritures représentent environ 50 % du trafic en production, un fichier SQLite unique par nœud deviendrait vite un goulot d'étranglement. Pour obtenir de la concurrence en écriture sur une même machine, Blobasaur répartit les données entre plusieurs fichiers de base SQLite, appelés « shards » :
- Hachage cohérent : chaque clé est associée à un shard via un hachage cohérent multi-probe.
- Un writer dédié par shard avec « group commit » : chaque shard dispose d'une tâche d'écriture alimentée par une file bornée ; au lieu de valider une clé à la fois, le writer puise un lot d'écritures en attente et les exécute dans une seule transaction `BEGIN IMMEDIATE ... COMMIT`, amortissant ainsi le coût de la transaction et du WAL sur plusieurs clients concurrents.
- Des lecteurs concurrents : les lectures passent directement par un pool de connexions SQLite en lecture seule par shard, et s'exécutent en parallèle de l'écrivain.

**Quel est l'apport concret du sharding ?** L'équipe a comparé 1 shard à 16 shards avec un générateur de charge ouvrant 64 connexions concurrentes, chaque requête portant une charge JSON de 64 Kio (proche de la moyenne de production), compressée environ 9 fois par zstd. Tous les tests utilisaient 100 000 clés, des écritures synchrones, une `batch_size` de 50, et un répertoire de données sur `tmpfs` pour isoler le verrouillage et le coût CPU de SQLite des aléas du disque. Les deux configurations disposaient des mêmes ressources totales : 1 600 Mo de cache de pages SQLite et 64 connexions de lecture au total.

| Charge | 1 shard | 16 shards |
|---|---|---|
| `HSET` seul | 7 740 ops/s, p99 10,7 ms | 25 324 ops/s, p99 8,3 ms |
| 50 % `HSET`, 50 % `HGET` | 14 227 ops/s, p99 10,5 ms | 29 538 ops/s, p99 8,5 ms |
| `HGET` seul | 67 128 ops/s, p99 2,1 ms | 70 884 ops/s, p99 2,3 ms |

Avec 16 shards, le débit d'écriture augmente de 3,3x et la latence médiane d'écriture chute de 8,2 ms à 2,1 ms. Le débit de lecture reste quasiment identique, SQLite en mode WAL servant déjà les lecteurs concurrents sans contention. À 25 324 opérations `HSET` par seconde, chacune portant une charge de 64 Kio, Blobasaur traite environ **1,66 Go/s de JSON non compressé** à travers zstd — serveur et générateur de charge tournant sur le même ordinateur portable 16 cœurs, partageant ses ressources CPU.

**Schéma de données.** Les services utilisent à la fois des clés simples (`SET`/`GET`) et des hashes Redis (`HSET`/`HGET`) pour regrouper les blobs par service ou fonctionnalité (par exemple `HSET prefs userID <json>`). Dans chaque shard, les clés simples vivent dans une table `blobs` :

```
CREATE TABLE IF NOT EXISTS blobs (
    key TEXT PRIMARY KEY,
    data BLOB,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    expires_at INTEGER,
    version INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_expires_at
    ON blobs(expires_at)
    WHERE expires_at IS NOT NULL;
```
`SET` écrit dans `blobs`. `HSET` écrit dans une table propre à son espace de noms, `blobs_<namespace>`, avec les mêmes colonnes — par exemple `HSET prefs user42 ...` stocke `user42` dans `blobs_prefs`. L'expiration est portée par la colonne `expires_at` sur la même ligne : les requêtes de lecture filtrent les lignes expirées au moment de la lecture (`expires_at IS NULL OR expires_at > ?`), tandis qu'un worker en arrière-plan supprime les lignes expirées de façon asynchrone. Comme l'index sur `expires_at` est un index partiel (`WHERE expires_at IS NOT NULL`), les lignes sans TTL n'occupent aucune place dans cet index.

**Compression.** Blobasaur prend en charge zstd, lz4, gzip et brotli avant écriture dans SQLite ; zstd est utilisé en production. Taux de compression observé sur une heure de trafic `HSET` en production :

| Charge `HSET` | Envoyée par le client | Stockée dans SQLite | Réduction |
|---|---|---|---|
| Moyenne | 63,6 Kio | 5,5 Kio | environ 11x |
| p99 | 935 Kio | 59,3 Kio | environ 16x |

Avec des pages SQLite par défaut de 4 Kio, faire passer une charge de 63,6 Kio à 5,5 Kio réduit son empreinte de stockage d'environ 16 pages à environ 2, avant même de compter la surcharge des lignes et des index. Moins de pages occupées par les données de blob signifie moins de pression sur le cache de pages et moins de données à écrire via le WAL vers la base.

**Durabilité.** N'ayant pas besoin d'une durabilité stricte pour des préférences d'interface, les shards tournent en mode WAL avec `PRAGMA synchronous = NORMAL` : SQLite ne force pas de `fsync` à chaque validation de transaction. Un crash OS ou une coupure électrique peut donc faire perdre des transactions récemment validées mais pas encore synchronisées sur le disque, tout en préservant la cohérence de la base. Pour les charges voulant une latence d'écriture encore plus faible, Blobasaur propose un mode optionnel `async_write`, qui accuse réception de l'écriture dès son entrée dans la file mémoire du shard, avant même la validation du lot par SQLite.

**Montée en charge entre plusieurs machines.** Pour dépasser la capacité d'un seul serveur, Blobasaur implémente le protocole Redis Cluster, le rendant compatible avec les clients Redis standards sensibles au clustering. Comme Redis Cluster, l'espace de clés est divisé en 16 384 « hash slots » via `CRC16`. Chaque nœud Blobasaur possède une plage de slots configurée, et les nœuds se découvrent entre eux par gossip. Si un client envoie une clé au mauvais nœud, celui-ci répond par une redirection `MOVED` vers le nœud propriétaire. Cela donne à Blobasaur un routage à deux niveaux : au niveau du cluster, `CRC16(clé) % 16384` sélectionne la machine ; au niveau du nœud, le hachage cohérent multi-probe sélectionne le shard SQLite sur cette machine. L'outil présente encore des limites : l'affectation des slots est aujourd'hui statique dans la configuration ; le rééquilibrage à chaud entre nœuds en cours d'exécution et le basculement automatique (failover) ne sont pas encore implémentés.

**Modifier le nombre de shards.** Le hachage cohérent multi-probe a été choisi pour que le resharding d'un nœud ne déplace qu'une quantité minimale de données, sans nécessiter de nœuds virtuels. Avec un simple `hash % num_shards`, passer de 4 à 5 shards déplacerait environ 80 % des clés ; avec le hachage cohérent, seules environ 20 % des clés se déplacent (la part revenant au nouveau shard). Le resharding est aujourd'hui une opération hors ligne, via le CLI intégré : arrêter le serveur, exécuter `blobasaur shard migrate 4 5 --verify`, puis mettre à jour `num_shards` dans `config.toml` et redémarrer le serveur. L'outil de migration ne déplace que les clés dont le shard cible a changé ; avec `--verify`, il vérifie que les clés se trouvent dans les shards attendus et rapporte les comptes de lignes après migration.

### Abandon de SSDB
Le déploiement s'est fait en plusieurs phases :
1. Nouvelles charges d'abord : au lancement du mode Terminal de Kite, son stockage de workspace a été directement dirigé vers Blobasaur.
2. Double écriture et rattrapage : pour les charges existantes comme les préférences de graphiques, les services ont été mis à jour pour écrire simultanément dans SSDB et Blobasaur, tandis qu'une migration en arrière-plan rapatriait les clés historiques. Les lectures allaient d'abord vers Blobasaur, avec repli sur SSDB en cas d'absence en cache ou d'erreur.
3. Bascule : côté client, le seul changement de code a consisté à remplacer un client Redis mono-nœud par un client Redis Cluster pointant vers les trois adresses IP des nœuds Blobasaur.

Après un mois de double écriture sans la moindre divergence constatée, SSDB a été définitivement éteint.

### Ce que l'équipe a appris en cours de route

**Supprimer des lignes ne réduit pas la taille des fichiers SQLite.** Très tôt, l'équipe a constaté que l'usage disque ne faisait que croître, même après l'expiration ou la suppression de millions de clés. Par défaut, SQLite conserve les pages libérées dans une liste interne (« freelist ») pour de futures écritures, plutôt que de rendre l'espace à l'OS. La solution a consisté à activer `PRAGMA auto_vacuum = INCREMENTAL` sur chaque shard et à ajouter une sous-commande `blobasaur shard vacuum` pour récupérer les pages libres de la freelist dans la limite d'une allocation définie (128 Mo par défaut). Comme réduire effectivement la taille du fichier de base en mode WAL nécessite un checkpoint, Blobasaur exécute `PRAGMA wal_checkpoint(TRUNCATE)` immédiatement après chaque vacuum incrémental.

**Les écritures asynchrones doivent être visibles de toute lecture.** Lorsque `async_write` est activé, une écriture renvoie `OK` alors qu'elle est encore dans la file mémoire du shard, en attente de la prochaine validation par lot. Pour préserver la cohérence « lire ses propres écritures », les écritures en file sont aussi placées dans une table de correspondance en mémoire que les lectures consultent avant d'interroger SQLite. Lors des tests, certains chemins de lecture et de vérification d'existence contournaient cette table ou ne tenaient pas compte des suppressions : par exemple, un `DEL` immédiatement suivi d'un `GET` pouvait renvoyer l'ancienne valeur présente dans SQLite, la suppression en file n'ayant pas encore été validée. Le correctif a consisté à stocker des « tombstones » explicites dans cette table en mémoire et à faire passer systématiquement toute lecture (`GET`, `HGET`, `EXISTS`, `TTL`) par celle-ci en premier.

**Le nettoyage des expirations doit partager l'écrivain.** En production, la latence d'écriture p99 se situait normalement sous 5 ms, avec des pics occasionnels à 30-50 ms. L'origine de ces pics a été identifiée dans la tâche de nettoyage TTL en arrière-plan : initialement, ce worker ouvrait sa propre connexion d'écriture et exécutait une unique grande instruction `DELETE` pour toutes les lignes expirées, laquelle entrait en concurrence avec l'écrivain principal du shard pour l'unique verrou d'écriture de SQLite, bloquant les lots clients normaux. Le correctif a consisté, d'une part, à faire passer les lots de nettoyage par la connexion d'écriture existante du shard, afin qu'ils alternent proprement avec les écritures clients, et d'autre part à borner chaque passage via `cleanup_chunk_size` (1 000 lignes par défaut). Les lignes expirées étant déjà filtrées au moment de la lecture, répartir la suppression physique en lots plus petits a éliminé les pics de latence sans affecter la correction du système.

### En production
Le déploiement actuel de Blobasaur tourne en cluster de trois nœuds (4 vCPU, 8 Go de RAM). Sur une séance de trading complète (9h00 à 15h30), la latence p99 toutes commandes confondues reste autour de 2 ms sur chaque nœud, et le p50 se situe entre 250 et 550 µs. En détail par commande, `HSET` affiche un p99 autour de 2 ms, `HGET` autour de 1,4 ms, et `HDEL` reste le plus souvent sous 1 ms.

Blobasaur est open source sous licence AGPLv3 et disponible sur GitHub (iamd3vil/blobasaur). D'autres projets du collectif Zerodha.tech sont regroupés sous l'appellation « 4th Cross Labs ».

## Pourquoi ça compte
Ce cas d'usage illustre comment SQLite, souvent perçu comme une base embarquée pour applications légères, peut servir de brique de stockage distribué à très fort débit quand il est combiné à du sharding applicatif, du group commit et de la compression — une alternative pragmatique aux solutions NoSQL ou objet plus lourdes pour des charges de type clé-valeur à durabilité relâchée.
