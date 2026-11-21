---
title: "PostgreSQL 19 Released!"
date: 2026-11-21
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.postgresql.org%2Fabout%2Fnews%2Fpostgresql-19-released-3449%2F%3Futm_source=tldrdev/1/010001a1f8e20cf0-04c1a8d2-b096-40a7-9fd6-0fd535581342-000000/zXVxl-UuhAzGas-Yl68QH8G6Sjn8f-hPP37n52UKE9A=452"
authors: ["PostgreSQL Global Development Group"]
keywords: ["PostgreSQL", "base de données open source", "réplication logique", "performance", "REPACK", "sécurité TLS"]
theme: "Data"
tone: "news"
used_in: ["2026-11-21"]
---

## Résumé
Le PostgreSQL Global Development Group a annoncé le 19 novembre 2026 la sortie de PostgreSQL 19, nouvelle version majeure de la base de données open source de référence. Cette mouture met l'accent sur la réduction des interruptions pour les charges critiques : réorganisation de tables à chaud (`REPACK CONCURRENTLY`), stabilisation des plans de requêtes (`pg_plan_advice`), cohérence « read-your-writes » sur les standbys, et simplification de l'activation de la réplication logique sans redémarrage du serveur. Elle apporte aussi des gains de performance significatifs (vérifications de clés étrangères, planificateur de requêtes, E/S asynchrones) ainsi que plusieurs évolutions côté sécurité (SNI, dépréciation du mot de passe md5, suppression de RADIUS) et SQL (JSON, fenêtrage, `ON CONFLICT DO SELECT`).

## Points clés
- `REPACK (CONCURRENTLY)` remplace `VACUUM FULL`/`CLUSTER` pour dégonfler les tables sans bloquer lectures ni écritures.
- La nouvelle extension `pg_plan_advice` (avec `pg_stash_advice`) permet de stabiliser ou corriger un plan de requête sans toucher à l'application.
- `WAIT FOR LSN` apporte la cohérence « read-your-writes » pour les applications qui lisent sur des standbys.
- L'activation de la réplication logique ne nécessite plus de redémarrage du serveur, et les séquences peuvent désormais être répliquées.
- Performances en hausse : vérifications de clés étrangères presque 2x plus rapides en insertion massive, nouvelles optimisations du planificateur, ajustement automatique des workers d'E/S asynchrones.
- Sécurité renforcée (SNI, avertissements sur md5, suppression de RADIUS) et le JIT est désormais désactivé par défaut.

## Analyse approfondie
19 novembre 2026 — Le PostgreSQL Global Development Group a annoncé aujourd'hui la sortie de PostgreSQL 19, la dernière version de la base de données open source la plus avancée au monde.

L'usage critique de PostgreSQL continue de croître rapidement, et PostgreSQL 19 répond à cette tendance en simplifiant à la fois l'administration et le développement de ces charges de travail à grande échelle. Cette version introduit la commande `REPACK (CONCURRENTLY)`, qui permet aux utilisateurs d'optimiser leurs tables en fonction de leur charge de travail actuelle sans interrompre les opérations en cours. PostgreSQL 19 offre également un meilleur contrôle sur la stabilité des plans d'exécution et les performances des requêtes grâce à la nouvelle extension `pg_plan_advice`. Les développeurs trouveront de nombreuses fonctionnalités appréciables dans cette version, allant du support de la cohérence « read-your-writes » (lecture de ses propres écritures) sur les standbys, à un comportement de type « get or create » qui économise un aller-retour réseau.

« Depuis plus de 30 ans, la communauté open source mondiale a fait de PostgreSQL une base de données à laquelle les organisations confient leurs données les plus critiques », a déclaré Jonathan Katz, membre de l'équipe centrale (core team) de PostgreSQL. « PostgreSQL 19 poursuit cet engagement envers la fiabilité, en offrant aux utilisateurs de nouveaux moyens de gérer leurs charges de travail sans interruption et de construire des applications qui s'étendent sur plusieurs systèmes. »

PostgreSQL, système de gestion de données innovant reconnu pour sa fiabilité, sa robustesse et son extensibilité, bénéficie de 30 ans de développement open source mené par une communauté mondiale de développeurs, et est devenu la base de données relationnelle open source de référence pour les organisations de toutes tailles.

Les tables qui subissent de nombreuses mises à jour et suppressions peuvent accumuler de l'espace inutilisé, appelé « bloat » (gonflement), qui peut lui aussi affecter significativement les performances des requêtes. Les commandes `VACUUM FULL` et `CLUSTER` étaient auparavant utilisées pour y remédier, mais présentaient des inconvénients, notamment le blocage de l'accès à la table jusqu'à la fin du nettoyage. PostgreSQL 19 introduit la commande `REPACK`, qui récupère cet espace et peut réorganiser les données d'une table pour qu'elles correspondent à un index ; avec `REPACK (CONCURRENTLY)`, cette opération peut se faire sans bloquer les lectures ni les écritures. `REPACK` remplace les commandes `VACUUM FULL` et `CLUSTER`, qui restent toutefois disponibles pour des raisons de compatibilité.

Le planificateur de requêtes de PostgreSQL choisit généralement un plan d'exécution efficace pour chaque requête, mais ce plan peut évoluer avec les données, et le nouveau plan est parfois plus lent. PostgreSQL 19 ajoute l'extension `pg_plan_advice`, qui permet de stabiliser les choix de plan et d'expérimenter différents plans à l'aide du mini-langage « plan advice ». L'extension complémentaire `pg_stash_advice` stocke ces recommandations (advice) et les applique automatiquement aux requêtes en fonction de leur identifiant, ce qui permet de corriger un plan lent sans modifier l'application.

PostgreSQL 19 aide également l'autovacuum à suivre le rythme sur les systèmes très sollicités. L'autovacuum peut désormais nettoyer (vacuum) les index à l'aide de workers parallèles, contrôlés par le nouveau paramètre `autovacuum_max_parallel_workers`, et utilise un nouveau système de notation (scoring) pour décider quelles tables traiter en priorité. Les requêtes qui lisent une table peuvent désormais marquer automatiquement des pages comme « all-visible » dans la visibility map pendant leur exécution, réduisant le travail que les futurs vacuums devront effectuer. Par ailleurs, `vacuumdb --analyze-only` analyse désormais les tables partitionnées lorsque aucune table n'est spécifiée.

Cette version ajoute de nouvelles vues pour surveiller les charges de travail, notamment `pg_stat_lock` pour des statistiques par type de verrou, `pg_stat_recovery` pour l'état de la récupération (recovery), et `pg_stat_autovacuum_scores` pour visualiser comment l'autovacuum priorise les tables. La nouvelle option `IO` d'`EXPLAIN ANALYZE`, ainsi que le paramètre correspondant d'`auto_explain`, rendent compte de l'activité d'entrée-sortie asynchrone. PostgreSQL 19 indique également la quantité de WAL écrite pour les images de page complètes (full-page images) dans `pg_stat_wal`, `EXPLAIN (ANALYZE, WAL)`, ainsi que dans les événements de journal de vacuum et d'analyze.

Auparavant, PostgreSQL exigeait souvent le redémarrage du serveur pour activer la réplication logique, ce qui pouvait perturber les charges de travail en production. PostgreSQL 19 simplifie l'initialisation de la réplication logique en élevant automatiquement le niveau de WAL effectif à `logical` dès la création du premier slot de réplication logique. Le niveau de WAL utilisé peut être consulté via le nouveau paramètre `effective_wal_level`.

PostgreSQL 19 ajoute également la réplication logique des valeurs de séquences, que l'on peut publier via `FOR ALL SEQUENCES` avec `CREATE PUBLICATION`. `CREATE PUBLICATION` ajoute aussi une clause `EXCEPT` permettant d'exclure des tables lors d'une publication `FOR ALL TABLES`, et `CREATE SUBSCRIPTION` peut désormais récupérer ses paramètres de connexion depuis un serveur distant (foreign server), comme celui défini avec `postgres_fdw`, grâce à la clause `SERVER`. Par ailleurs, la nouvelle option d'abonnement `retain_dead_tuples` permet à PostgreSQL de détecter les mises à jour en conflit avec une suppression concurrente, ces conflits étant désormais comptabilisés dans `pg_stat_subscription_stats`.

Pour les applications qui orientent leurs lectures vers des standbys, PostgreSQL 19 apporte la cohérence « read-your-writes » grâce à la nouvelle commande `WAIT FOR LSN`. Une session sur un standby peut utiliser `WAIT FOR LSN` pour attendre que le standby ait rejoué le write-ahead log (WAL) jusqu'à un numéro de séquence de journal (log sequence number, LSN) précis avant d'exécuter une requête, ce qui permet à l'application de relire des données qu'elle vient d'écrire sur le primaire.

PostgreSQL 19 améliore également les requêtes sur les tables distantes (foreign tables). Grâce à la nouvelle option `import_stats`, `postgres_fdw` peut importer les statistiques de table depuis le serveur distant lors de l'exécution d'`ANALYZE`, au lieu d'échantillonner des lignes de la table distante, ce qui aide le planificateur de requêtes à choisir de meilleurs plans.

PostgreSQL 19 ajoute `INSERT ... ON CONFLICT DO SELECT`, qui permet à la clause `RETURNING` de retourner les lignes existantes entrant en conflit avec une insertion, simplifiant ainsi le schéma courant « get or create » (obtenir ou créer). `COPY` peut désormais produire des données au format JSON, y compris sous forme d'un unique tableau JSON, et le langage de chemin SQL/JSON ajoute des méthodes de chaîne telles que `lower()`, `upper()`, `replace()`, `split_part()` et `btrim()`. Par ailleurs, les fonctions fenêtrées `lead()`, `lag()`, `first_value()`, `last_value()` et `nth_value()` peuvent désormais ignorer les valeurs `NULL` grâce à `IGNORE NULLS`. La fonction `random()` peut également générer des dates et des timestamps aléatoires dans un intervalle donné.

Cette version accélère aussi de nombreuses charges de travail sans aucune modification de l'application. PostgreSQL 19 améliore les performances des vérifications de clés étrangères, ce qui a rendu les insertions en masse (bulk inserts) près de deux fois plus rapides lors des tests, et ajoute de nouvelles optimisations au planificateur de requêtes, comme la conversion des clauses `NOT IN` en anti-jointures plus efficaces lorsqu'aucune valeur `NULL` n'est présente, ou la réalisation d'une agrégation anticipée (eager aggregation) avant les jointures pour réduire le nombre de lignes à traiter. PostgreSQL 19 s'appuie également sur le sous-système d'entrées-sorties asynchrones introduit dans PostgreSQL 18. Lorsque `io_method` est réglé sur `worker` (valeur par défaut), PostgreSQL ajuste désormais automatiquement le nombre de workers d'E/S entre les nouveaux paramètres `io_min_workers` et `io_max_workers`, qui remplacent le paramètre `io_workers`. On note également des améliorations de scalabilité lors de l'utilisation de `LISTEN` et `NOTIFY` pour échanger des notifications dans des charges de travail multi-canaux.

Enfin, le nouveau paramètre `password_expiration_warning_threshold` avertit les utilisateurs lorsque leur mot de passe est proche de son expiration.

PostgreSQL 19 ajoute une prise en charge côté serveur de l'indication du nom de serveur (Server Name Indication, SNI), permettant à un même serveur PostgreSQL de présenter un certificat TLS différent selon le nom d'hôte auquel le client se connecte. Les correspondances entre noms d'hôte et certificats/clés peuvent être définies dans le nouveau fichier `pg_hosts.conf`. PostgreSQL 19 émet désormais aussi un avertissement après une authentification par mot de passe `md5` réussie, avertissement que l'on peut désactiver avec le paramètre `md5_password_warnings`. L'authentification par mot de passe `md5` a été dépréciée dans PostgreSQL 18 et sera supprimée dans une prochaine version. Si une authentification par mot de passe est nécessaire, il convient d'utiliser l'authentification SCRAM. Cette version supprime également la prise en charge de l'authentification RADIUS.

La compilation à la volée (Just-in-time compilation, JIT) est désormais désactivée par défaut, les estimations de coût que PostgreSQL utilisait pour décider de son activation s'étant révélées peu fiables. Les utilisateurs exécutant de nombreuses requêtes analytiques volumineuses pourront souhaiter réactiver le JIT. Lorsque PostgreSQL est compilé avec le support de LZ4, la méthode de compression TOAST par défaut est désormais `lz4`.

De nombreuses autres fonctionnalités et améliorations ont été ajoutées à PostgreSQL 19 et pourront également s'avérer utiles selon les cas d'usage. Consultez les notes de version pour une liste complète des fonctionnalités nouvelles et modifiées.

PostgreSQL est la base de données open source la plus avancée au monde, portée par une communauté mondiale de milliers d'utilisateurs, de contributeurs, d'entreprises et d'organisations. Depuis ses débuts à l'université de Californie à Berkeley il y a plus de 40 ans, PostgreSQL maintient un rythme de développement inégalé. L'ensemble de fonctionnalités mature de PostgreSQL rivalise avec les meilleurs systèmes de bases de données propriétaires, et les surpasse même en matière de fonctionnalités avancées, d'extensibilité, de sécurité et de stabilité.

Pour des explications sur les fonctionnalités mentionnées ci-dessus et sur d'autres encore, veuillez consulter les ressources suivantes :

Il existe plusieurs façons de télécharger PostgreSQL 19, notamment :

D'autres outils et extensions sont disponibles sur le PostgreSQL Extension Network.

PostgreSQL 19 est livré avec une documentation au format HTML ainsi que des pages de manuel (man pages), et la documentation peut également être consultée en ligne aux formats HTML et PDF.

PostgreSQL utilise la licence PostgreSQL, une licence « permissive » de type BSD. Certifiée par l'OSI, cette licence est largement appréciée pour sa flexibilité et son caractère favorable aux usages commerciaux, puisqu'elle ne restreint pas l'utilisation de PostgreSQL avec des applications commerciales et propriétaires. Combinée à un support multi-entreprises et à une propriété publique du code, cette licence rend PostgreSQL très populaire auprès des éditeurs souhaitant intégrer une base de données dans leurs propres produits, sans craindre des frais de licence, un verrouillage propriétaire (vendor lock-in) ou des changements des conditions de licence.

Site web

Postgres, PostgreSQL et le logo de l'éléphant (Slonik) sont des marques déposées de la PostgreSQL Community Association. Toute utilisation de ces marques doit se conformer à la politique relative aux marques (trademark policy).

PostgreSQL bénéficie du soutien de nombreuses entreprises, qui financent des développeurs, fournissent des ressources d'hébergement et apportent un soutien financier. Consultez notre page des sponsors pour découvrir certains de ces soutiens du projet.

Il existe également une large communauté d'entreprises proposant du support PostgreSQL, allant du consultant indépendant aux multinationales.

Pour effectuer une contribution financière au PostgreSQL Global Development Group ou à l'une des organisations non lucratives reconnues par la communauté, veuillez consulter notre page de dons.

## Pourquoi ça compte
PostgreSQL équipe une part massive des infrastructures de données modernes ; cette version réduit les fenêtres de maintenance et les risques opérationnels (REPACK en ligne, stabilité des plans, réplication logique sans redémarrage), ce qui intéresse directement toute équipe data ou plateforme exploitant PostgreSQL en production à grande échelle.
