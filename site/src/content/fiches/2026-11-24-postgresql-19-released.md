---
title: "PostgreSQL 19 Released!"
date: 2026-11-24
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.postgresql.org%2Fabout%2Fnews%2Fpostgresql-19-released-3449%2F%3Futm_source=tldrdata/1/010001a2081c48fa-0fe56ffc-b235-4b40-9300-61b073fa6ac9-000000/0hDBSw3LFq-J9owej0Z3K_W1I6W84U9syxoAG45ZIy4=452"
authors: ["The PostgreSQL Global Development Group", "Jonathan Katz"]
keywords: ["PostgreSQL", "base de données", "open source", "performance", "réplication logique"]
theme: "Data"
tone: "news"
used_in: ["2026-11-24"]
---

## Résumé
La PostgreSQL Global Development Group a annoncé le 19 novembre 2026 la sortie de PostgreSQL 19, la nouvelle version majeure de cette base de données open source. Cette version vise à simplifier l'administration et le développement des charges critiques à grande échelle, avec notamment la commande `REPACK (CONCURRENTLY)` pour réorganiser les tables sans interruption de service, et l'extension `pg_plan_advice` pour stabiliser les plans d'exécution des requêtes. Elle apporte aussi de nombreuses améliorations pour les développeurs (cohérence « read-your-writes » sur les standbys, pattern « get or create ») ainsi que des gains de performance significatifs, notamment un quasi-doublement de la vitesse des insertions en masse grâce à l'optimisation des vérifications de clés étrangères.

## Points clés
- Nouvelle commande `REPACK (CONCURRENTLY)` qui remplace `VACUUM FULL`/`CLUSTER` pour dégonfler les tables sans bloquer les lectures/écritures.
- Extensions `pg_plan_advice` et `pg_stash_advice` pour stabiliser et corriger les plans de requêtes sans modifier l'application.
- Simplification de la réplication logique : plus besoin de redémarrer le serveur, réplication des valeurs de séquences, clause `EXCEPT` pour `CREATE PUBLICATION`.
- Nouvelle commande `WAIT FOR LSN` apportant la cohérence « read-your-writes » sur les instances standby.
- `INSERT ... ON CONFLICT DO SELECT` pour simplifier le pattern « get or create », et nouvelles vues de supervision (`pg_stat_lock`, `pg_stat_recovery`, `pg_stat_autovacuum_scores`).
- JIT désactivé par défaut et support de SNI côté serveur pour présenter des certificats TLS différents selon l'hôte.

## Analyse approfondie
19 novembre 2026 - Le PostgreSQL Global Development Group a annoncé aujourd'hui la sortie de PostgreSQL 19, la dernière version de la base de données open source la plus avancée au monde.

L'usage critique de PostgreSQL continue de croître rapidement, et PostgreSQL 19 répond à cette tendance en simplifiant à la fois l'administration et le développement pour ces charges de travail à grande échelle. Cette version introduit la commande `REPACK (CONCURRENTLY)`, qui permet aux utilisateurs d'optimiser leurs tables pour leur charge de travail actuelle sans perturber les opérations en cours. PostgreSQL 19 offre aussi un meilleur contrôle sur la stabilité des plans et la performance des requêtes grâce à la nouvelle extension `pg_plan_advice`. Les développeurs trouveront de nombreuses fonctionnalités appréciables dans cette version, allant du support de la cohérence « read-your-writes » sur les standbys au comportement « get or create » qui économise un aller-retour réseau.

« Depuis plus de 30 ans, la communauté open source mondiale a bâti PostgreSQL pour en faire une base de données à laquelle les organisations confient leurs données les plus critiques », a déclaré Jonathan Katz, membre de l'équipe centrale de PostgreSQL. « PostgreSQL 19 poursuit cet engagement en matière de fiabilité, en donnant aux utilisateurs de nouveaux moyens de gérer leurs charges de travail sans interruption et de construire des applications qui s'étendent sur plusieurs systèmes. »

PostgreSQL, un système de gestion de données innovant reconnu pour sa fiabilité, sa robustesse et son extensibilité, bénéficie de 30 ans de développement open source par une communauté mondiale de développeurs et est devenu la base de données relationnelle open source préférée des organisations de toutes tailles.

Les tables qui subissent de nombreuses mises à jour et suppressions peuvent accumuler de l'espace inutilisé, appelé « bloat », ce qui peut aussi affecter significativement les performances des requêtes. Les commandes `VACUUM FULL` et `CLUSTER` étaient auparavant utilisées pour traiter ce problème, mais comportaient des compromis, notamment le blocage de l'accès à la table pendant le nettoyage. PostgreSQL 19 introduit la commande `REPACK`, qui récupère cet espace et peut réordonner les données d'une table pour correspondre à un index, et avec `REPACK (CONCURRENTLY)`, peut le faire sans bloquer les lectures ni les écritures. `REPACK` remplace les commandes `VACUUM FULL` et `CLUSTER`, qui restent toutes deux disponibles pour des raisons de compatibilité.

Le planificateur de requêtes de PostgreSQL choisit généralement un plan efficace pour chaque requête, mais ce plan peut changer à mesure que les données évoluent, et parfois le nouveau plan est plus lent. PostgreSQL 19 ajoute l'extension `pg_plan_advice`, qui permet de stabiliser les choix de plan et d'expérimenter différents plans à l'aide du mini-langage « plan advice ». L'extension complémentaire `pg_stash_advice` stocke ces conseils et les applique automatiquement aux requêtes en fonction de leur identifiant de requête, ce qui permet de corriger un plan lent sans modifier l'application.

PostgreSQL 19 aide aussi l'autovacuum à suivre le rythme sur les systèmes très sollicités. L'autovacuum peut désormais passer les index au vacuum à l'aide de workers parallèles, contrôlés par le nouveau paramètre `autovacuum_max_parallel_workers`, et utilise un nouveau système de notation pour décider quelles tables traiter en priorité. Les requêtes qui lisent une table peuvent désormais marquer automatiquement les pages comme « all-visible » dans la carte de visibilité pendant leur exécution, réduisant le travail que les futurs vacuums devront effectuer. De plus, `vacuumdb --analyze-only` analyse désormais les tables partitionnées lorsqu'aucune table n'est spécifiée.

Cette version ajoute de nouvelles vues pour la supervision des charges de travail, notamment `pg_stat_lock` pour des statistiques par type de verrou, `pg_stat_recovery` pour l'état de la récupération, et `pg_stat_autovacuum_scores` pour montrer comment l'autovacuum priorise les tables. La nouvelle option `IO` de `EXPLAIN ANALYZE` et le paramètre correspondant d'`auto_explain` rapportent l'activité d'E/S asynchrone. PostgreSQL 19 rapporte également la quantité de WAL écrite pour les images de pages complètes (full-page images) dans `pg_stat_wal`, `EXPLAIN (ANALYZE, WAL)`, ainsi que dans les journaux d'événements de vacuum et d'analyze.

Auparavant, PostgreSQL exigeait souvent que les utilisateurs redémarrent leur serveur pour activer la réplication logique, ce qui pouvait être perturbant en production. PostgreSQL 19 simplifie l'initialisation de la réplication logique en élevant automatiquement le niveau de WAL effectif à `logical` dès la création du premier slot de réplication logique. Vous pouvez voir le niveau de WAL utilisé avec le nouveau paramètre `effective_wal_level`.

PostgreSQL 19 ajoute également la réplication logique des valeurs de séquences, que vous pouvez publier en utilisant `FOR ALL SEQUENCES` avec `CREATE PUBLICATION`. `CREATE PUBLICATION` ajoute aussi une clause `EXCEPT` pour exclure des tables lors de la publication `FOR ALL TABLES`, et `CREATE SUBSCRIPTION` peut désormais récupérer ses paramètres de connexion depuis un serveur distant (foreign server), comme ceux définis avec `postgres_fdw`, grâce à la clause `SERVER`. De plus, la nouvelle option d'abonnement `retain_dead_tuples` permet à PostgreSQL de détecter les mises à jour en conflit avec une suppression concurrente, et ces conflits sont désormais comptabilisés dans `pg_stat_subscription_stats`.

Pour les applications qui dirigent leurs lectures vers des standbys, PostgreSQL 19 ajoute la cohérence « read-your-writes » avec la nouvelle commande `WAIT FOR LSN`. Une session sur un standby peut utiliser `WAIT FOR LSN` pour attendre que le standby ait rejoué le journal des écritures (WAL) jusqu'à un numéro de séquence de journal (LSN) spécifique avant d'exécuter une requête, afin que l'application puisse lire les données qu'elle vient juste d'écrire sur le primaire.

PostgreSQL 19 améliore également les requêtes sur les tables distantes (foreign tables). Avec la nouvelle option `import_stats`, `postgres_fdw` peut importer les statistiques de table depuis le serveur distant lors de l'exécution d'`ANALYZE`, au lieu d'échantillonner les lignes de la table distante, ce qui aide le planificateur de requêtes à choisir de meilleurs plans.

PostgreSQL 19 ajoute `INSERT ... ON CONFLICT DO SELECT`, qui permet à la clause `RETURNING` de retourner les lignes existantes en conflit avec une insertion, simplifiant le pattern courant « get or create ». `COPY` peut désormais produire des données en JSON, y compris sous forme d'un unique tableau JSON, et le langage de chemin SQL/JSON ajoute des méthodes de chaîne telles que `lower()`, `upper()`, `replace()`, `split_part()` et `btrim()`. De plus, les fonctions de fenêtrage `lead()`, `lag()`, `first_value()`, `last_value()` et `nth_value()` peuvent désormais ignorer les valeurs `NULL` grâce à `IGNORE NULLS`. La fonction `random()` peut également générer des dates et des timestamps aléatoires dans une plage donnée.

Cette version rend aussi de nombreuses charges de travail plus rapides sans modification de l'application. PostgreSQL 19 améliore la performance des vérifications de clés étrangères, ce qui, lors des tests, a rendu les insertions en masse presque deux fois plus rapides, et ajoute d'autres optimisations du planificateur de requêtes, comme la conversion des clauses `NOT IN` en anti-jointures plus efficaces lorsque les valeurs `NULL` sont absentes, et la réalisation d'une agrégation anticipée (eager aggregation) avant les jointures pour réduire le nombre de lignes à traiter. PostgreSQL 19 s'appuie également sur le sous-système d'E/S asynchrone ajouté dans PostgreSQL 18. Lorsque `io_method` est réglé sur `worker` (valeur par défaut), PostgreSQL ajuste désormais automatiquement le nombre de workers d'E/S entre les nouveaux paramètres `io_min_workers` et `io_max_workers`, qui remplacent le paramètre `io_workers`. Des améliorations de scalabilité sont également apportées à l'utilisation de `LISTEN` et `NOTIFY` pour échanger des notifications dans des charges de travail multi-canaux.

Enfin, le nouveau paramètre `password_expiration_warning_threshold` avertit les utilisateurs lorsque leur mot de passe est sur le point d'expirer.

PostgreSQL 19 ajoute le support côté serveur de Server Name Indication (SNI), permettant à un seul serveur PostgreSQL de présenter un certificat TLS différent selon le nom d'hôte auquel un client se connecte. Vous pouvez associer des noms d'hôtes à leurs certificats et clés dans le nouveau fichier `pg_hosts.conf`. PostgreSQL 19 émet désormais aussi un avertissement après une authentification par mot de passe `md5` réussie, que vous pouvez désactiver avec le paramètre `md5_password_warnings`. L'authentification par mot de passe `md5` a été dépréciée dans PostgreSQL 18 et sera supprimée dans une future version. Si vous avez besoin d'une authentification par mot de passe, utilisez l'authentification SCRAM. Cette version supprime également le support de l'authentification RADIUS.

La compilation à la volée (Just-in-Time, JIT) est désormais désactivée par défaut, car les estimations de coût que PostgreSQL utilisait pour décider quand l'activer se sont révélées peu fiables. Si vous exécutez de nombreuses requêtes analytiques volumineuses, vous voudrez peut-être l'activer. Lorsque PostgreSQL est compilé avec le support LZ4, la méthode de compression TOAST par défaut est désormais `lz4`.

De nombreuses autres fonctionnalités et améliorations ont été ajoutées à PostgreSQL 19 qui pourraient également être utiles selon vos cas d'usage. Veuillez consulter les notes de version pour une liste complète des fonctionnalités nouvelles et modifiées.

PostgreSQL est la base de données open source la plus avancée au monde, avec une communauté mondiale de milliers d'utilisateurs, de contributeurs, d'entreprises et d'organisations. Depuis ses débuts à l'Université de Californie à Berkeley il y a plus de 40 ans, PostgreSQL a poursuivi un rythme de développement sans égal. L'ensemble de fonctionnalités mature de PostgreSQL non seulement égale les systèmes de bases de données propriétaires de premier plan, mais les dépasse en matière de fonctionnalités avancées, d'extensibilité, de sécurité et de stabilité.

Pour des explications sur les fonctionnalités ci-dessus et d'autres, veuillez consulter les ressources suivantes.

Plusieurs méthodes permettent de télécharger PostgreSQL 19.

D'autres outils et extensions sont disponibles sur le PostgreSQL Extension Network.

PostgreSQL 19 est livré avec une documentation HTML ainsi que des pages de manuel, et vous pouvez également consulter la documentation en ligne aux formats HTML et PDF.

PostgreSQL utilise la licence PostgreSQL, une licence « permissive » de type BSD. Cette licence certifiée OSI est largement appréciée pour sa flexibilité et son caractère favorable aux affaires, car elle ne restreint pas l'utilisation de PostgreSQL avec des applications commerciales et propriétaires. Associée au soutien de multiples entreprises et à la propriété publique du code, cette licence rend PostgreSQL très populaire auprès des fournisseurs souhaitant intégrer une base de données dans leurs propres produits sans craindre de frais, de dépendance à un fournisseur (vendor lock-in), ou de changements dans les conditions de licence.

Site web.

Postgres, PostgreSQL et le logo de l'éléphant (Slonik) sont des marques déposées de la PostgreSQL Community Association. Si vous souhaitez utiliser ces marques, vous devez vous conformer à la politique relative aux marques.

PostgreSQL bénéficie du soutien de nombreuses entreprises, qui parrainent des développeurs, fournissent des ressources d'hébergement et nous apportent un soutien financier. Consultez notre page des sponsors pour découvrir certains de ces soutiens au projet.

Il existe également une large communauté d'entreprises offrant du support PostgreSQL, allant de consultants individuels à des entreprises multinationales.

Si vous souhaitez apporter une contribution financière au PostgreSQL Global Development Group ou à l'une des organisations communautaires à but non lucratif reconnues, veuillez consulter notre page de dons.

## Pourquoi ça compte
PostgreSQL 19 confirme la maturité de l'écosystème open source face aux bases propriétaires, avec des gains opérationnels concrets (dégonflage de tables sans interruption, stabilité des plans de requêtes, réplication logique simplifiée) qui réduisent directement le coût d'exploitation des charges critiques à grande échelle — un signal important pour toute équipe data qui évalue ou exploite déjà PostgreSQL en production.
