---
title: "Use DMS to shrink Cloud SQL for SQL Server disk | Google Cloud Blog"
date: 2026-11-04
url: "https://cloud.google.com/blog/products/databases/use-dms-to-shrink-cloud-sql-for-sql-server-disk/"
authors: ["Nithin Tomson", "Adi Shtatfeld"]
keywords: ["Cloud SQL", "SQL Server", "migration de bases de données", "DMS", "réduction de disque", "haute disponibilité"]
theme: "Data"
tone: "tutorial"
used_in: ["2026-11-04"]
---

## Résumé

L'article explique comment utiliser le Database Migration Service (DMS) de Google Cloud, habituellement pensé comme un outil de migration unique vers le cloud, comme un véritable outil d'exploitation quotidienne pour les instances Cloud SQL for SQL Server. Le cas d'usage central est la réduction de la taille du disque persistant (après archivage de données, pic de stockage ponctuel ou refonte de schéma) sans passer par la fenêtre de maintenance longue qu'exige la fonctionnalité native de réduction de disque. La méthode proposée consiste à répliquer en continu la base vers une nouvelle instance dotée d'un disque plus petit, puis à basculer la production lors d'une courte fenêtre de coupure. L'article détaille le mécanisme de réplication sous-jacent de DMS ainsi que les étapes manuelles indispensables avant et après la bascule (objets au niveau serveur, utilisateurs orphelins).

## Points clés

- DMS peut servir d'outil d'exploitation récurrent (« day-two operations »), pas seulement de passerelle de migration initiale vers le cloud.
- La réduction native du disque Cloud SQL impose un temps d'arrêt proportionnel à la capacité totale allouée, pouvant atteindre plusieurs heures pour des disques multi-téraoctets.
- La méthode DMS consiste à provisionner une nouvelle instance avec un disque plus petit, à y répliquer les données en continu, puis à basculer l'application lors d'une fenêtre de coupure courte.
- La réplication DMS fonctionne au niveau des bases utilisateur (sauvegarde complète initiale puis sauvegardes de journal de transactions en continu) ; les objets au niveau serveur (logins, serveurs liés, jobs SQL Server Agent, TDE, configurations d'instance) ne sont pas répliqués automatiquement et doivent être migrés manuellement.
- Après la bascule, les utilisateurs de base de données peuvent devenir « orphelins » car les logins recréés sur la nouvelle instance obtiennent de nouveaux identifiants de sécurité (SID) ; une détection et une correction via `ALTER USER` sont nécessaires.
- Cette approche permet de réduire les coûts de stockage en s'alignant sur l'usage réel du disque, tout en préservant la disponibilité de l'application.

## Analyse approfondie

### Pourquoi réduire la taille de son disque ?

Dans de nombreux environnements de production, le stockage ne évolue que dans un sens : vers le haut. Des fonctionnalités comme l'augmentation automatique du stockage de Cloud SQL sont essentielles pour éviter les pannes dues au manque d'espace lors de pics de trafic imprévus, d'imports par lots volumineux, d'opérations de maintenance d'index ou de charges temporaires de préparation de données. De la même façon, au fil du cycle de vie d'une application, on peut archiver des données historiques, purger des données obsolètes ou supprimer des index inutilisés.

Lorsque des données sont supprimées, SQL Server marque l'espace libéré à l'intérieur des fichiers de données (.mdf, .ndf) comme réutilisable pour de futures écritures ; de la même manière, la troncature du journal libère de l'espace dans les fichiers de journal de transactions (.ldf). Cependant, les fichiers de base de données eux-mêmes conservent leur espace utilisé maximal (« peak ») à moins que l'option AUTO_SHRINK ne soit activée — un paramètre généralement déconseillé en production en raison d'une fragmentation d'index sévère et d'une surcharge de performance.

Une opération de réduction manuelle des fichiers de base via `DBCC SHRINKFILE` permet de restituer cet espace inutilisé de SQL Server vers le disque sous-jacent. Mais même après cette réduction des fichiers de base, le disque persistant Cloud SQL reste alloué à sa capacité maximale atteinte. Si l'on ne prévoit pas que la base reviendra occuper cet espace alloué dans un futur proche, il devient pertinent de réduire le disque lui-même pour diminuer les coûts de stockage continus, notamment dans les cas suivants :

- **Après un archivage ou une purge massive de données** : les données historiques ont été définitivement déplacées vers un stockage froid ou vers BigQuery, et le jeu de données actif ne représente plus qu'une fraction de sa taille maximale passée.
- **Après un pic de stockage ponctuel** : une transaction incontrôlée, une migration de données volumineuse ou une charge temporaire de préparation a déclenché l'augmentation automatique du stockage, laissant l'utilisateur payer pour des téraoctets de capacité provisionnée désormais inutiles.
- **Après une refonte ou une optimisation de schéma** : des tables ont été extraites d'une base monolithique vers des services séparés, de grands index inutilisés ont été supprimés, ou une compression de données a été appliquée.

Il est possible d'examiner, via une requête, à la fois la capacité allouée et l'espace libre disponible pour chaque fichier de base de données. Deux métriques Cloud Monitoring permettent d'identifier une opportunité de réduction de disque : `database/disk/bytes_used` (espace disque réellement consommé par les fichiers de base et les journaux) et `database/disk/quota` (capacité disque totale provisionnée pour l'instance).

Cloud SQL propose une fonctionnalité native de réduction du stockage qui fonctionne bien lorsque la charge applicative peut tolérer une fenêtre de maintenance planifiée. Toutefois, cette réduction native impose un temps d'arrêt de l'instance proportionnel à la taille totale du disque alloué — ce qui peut représenter des heures de maintenance hors ligne pour des disques multi-téraoctets.

Si les SLA de production ne permettent pas une interruption prolongée, le Database Migration Service (DMS) offre une alternative à temps d'arrêt minimal. En répliquant en continu les bases de données vers une instance Cloud SQL nouvellement provisionnée, dotée d'un disque dimensionné de façon adéquate, il devient possible de récupérer le stockage inutilisé tout en gardant l'application en ligne — seule une brève fenêtre de bascule étant nécessaire.

### Fonctionnement de DMS en coulisses : réplication entre instances Cloud SQL for SQL Server

Pour tirer efficacement parti de DMS, il est utile de comprendre son mécanisme de réplication sous-jacent. Lors d'une migration entre deux instances Cloud SQL for SQL Server, DMS coordonne un processus de synchronisation similaire à l'expédition native de journaux SQL Server (« log shipping ») :

1. **Sauvegarde complète initiale** : DMS capture une sauvegarde complète initiale (.bak) des bases de données utilisateur sélectionnées et la restaure sur l'instance cible.
2. **Sauvegardes de journal en continu** : DMS capture et applique en continu des sauvegardes du journal de transactions (.trn) afin de maintenir l'instance cible synchronisée quasiment en temps réel.

Comme la synchronisation s'opère au niveau de la base de données utilisateur, les objets situés en dehors de celle-ci — logins, serveurs liés, jobs SQL Server Agent — ne sont pas répliqués automatiquement vers l'instance de secours. Ces objets au niveau serveur doivent donc être migrés manuellement.

### Réduire son disque avec un minimum d'interruption

Grâce à ce pipeline de réplication continue, il est possible de récupérer du stockage non alloué sans passer par une longue fenêtre de maintenance. Plutôt que de réduire le disque existant sur place pendant que l'instance est hors ligne, on migre la charge applicative vers une nouvelle instance Cloud SQL dotée d'un disque correctement dimensionné, tandis que l'application de production reste en ligne.

**Le déroulé de la réduction de disque via DMS :**

1. Provisionner une nouvelle instance cible avec un disque plus petit mais adéquatement dimensionné (en laissant suffisamment de marge pour les journaux de transactions et la croissance future des données).
2. Démarrer une tâche DMS continue en utilisant l'instance Cloud SQL existante comme source.
3. Laisser la réplication se synchroniser pendant que l'application de production continue de fonctionner sans interruption.
4. Réaliser une courte bascule : arrêter le trafic applicatif, laisser s'appliquer le dernier journal de transactions, promouvoir l'instance cible dans DMS, puis rediriger l'application vers celle-ci.

Un tableau comparatif entre la réduction native et la migration via DMS est présenté dans l'article original ; il souligne que, parce que DMS migre la charge de travail au niveau de la base utilisateur, une bascule fluide nécessite de migrer également les objets au niveau serveur et les correspondances d'utilisateurs, en plus des données elles-mêmes.

### Avant et après la bascule : au-delà de la simple réplication de données

**Préparation avant la bascule — migrer les objets au niveau serveur**

Comme DMS opère au niveau de la base utilisateur, les objets serveur ne sont pas répliqués automatiquement ; il faut les recréer manuellement sur l'instance de destination avant la bascule :

- **Logins** : les extraire depuis la source via `sp_help_revlogin` et les recréer sur l'instance cible (cette méthode préserve les identifiants de sécurité, les SID).
- **Jobs SQL Server Agent et objets au niveau serveur** : comme DMS réplique les bases de données et non l'état de l'instance serveur, ces objets doivent être scriptés depuis la source puis déployés sur l'instance Cloud SQL de destination. Dans SQL Server Management Studio (SSMS), on se connecte à l'instance source, on navigue jusqu'à l'objet dans l'Explorateur d'objets, puis on fait un clic droit pour sélectionner « Scripter [Objet] en tant que > CREATE vers > Nouvelle fenêtre de requête / fichier ».
  - Jobs SQL Server Agent : vérifier que les scripts générés ne référencent pas de chemins de fichiers on-premises ni de dépendances système non prises en charge.
  - Serveurs liés : suivre la même démarche de scripting, en veillant à activer le flag de base de données `cloudsql.linked_servers` sur l'instance Cloud SQL avant le déploiement.
  - Extended Events : suivre la même démarche de scripting.
- **Chiffrement TDE** : pour les instances avec TDE activé, exporter le certificat TDE depuis la source puis l'importer sur la destination avant la bascule.
- **Configurations d'instance** (flags de base de données, Active Directory, Entra ID, etc.) : elles doivent être configurées manuellement sur l'instance de destination pour correspondre exactement aux paramètres de la source.
- **Polybase** : si utilisé, il faut réencoder la clé maître de base de données (DMK) pour que les identifiants à portée de base de données fonctionnent correctement.

**Remédiation après la bascule — résoudre les utilisateurs orphelins**

Les utilisateurs de base de données associés à des logins absents ou mal configurés sur l'instance serveur ne peuvent pas s'authentifier ; on les appelle « utilisateurs orphelins ». Comme les logins créés sur l'instance de destination possèdent des identifiants de sécurité (SID) propres, qui ne correspondent pas aux SID d'origine conservés dans les bases migrées, les utilisateurs deviennent orphelins par défaut. Une correction manuelle est nécessaire une fois la base cible en ligne après la bascule.

- Utiliser `sp_help_revlogin` pour migrer les logins préserve les SID d'origine ; en revanche, créer les logins sur la destination par d'autres méthodes génère de nouveaux SID au niveau serveur. Comme ceux-ci diffèrent des SID d'origine conservés dans les bases restaurées par DMS, les utilisateurs de base de données deviennent orphelins après la bascule et nécessitent une remise en correspondance.

1. **Détecter les utilisateurs orphelins** : se connecter à chaque base utilisateur de destination et exécuter la requête de diagnostic fournie dans le guide officiel de Microsoft sur le dépannage des utilisateurs orphelins.
2. **Corriger les utilisateurs orphelins** (`ALTER USER`) : pour chaque utilisateur de base de données non lié retourné par la requête, exécuter l'instruction `ALTER USER` correspondante dans le contexte de cette base afin de remettre proprement en correspondance le principal et ses permissions avec le nouveau login serveur Cloud SQL.

### Résumé et prochaines étapes

DMS est plus qu'une simple passerelle unique depuis les environnements on-premises vers Google Cloud — c'est un outil polyvalent pour les opérations quotidiennes (« day-two operations ») dans la boîte à outils de l'ingénieur Cloud SQL. Lorsque des SLA de production stricts empêchent de recourir à de longues fenêtres de maintenance pour une réduction native du disque, DMS offre un pipeline de réplication managé et fiable permettant de redimensionner son empreinte de stockage et de réduire les coûts d'infrastructure avec un minimum d'interruption. L'article renvoie vers la documentation officielle pour configurer Cloud SQL for SQL Server comme source DMS, ainsi que vers une introduction à Cloud SQL for SQL Server pour les nouveaux utilisateurs.

## Pourquoi ça compte

Cet article illustre une tendance notable dans la gestion des bases de données managées sur le cloud : détourner des outils de migration pour des opérations courantes (day-two operations) afin de contourner les limites natives des services managés, ici le temps d'arrêt imposé par la réduction de disque. C'est un signal utile pour les équipes Data/Infra qui cherchent à optimiser les coûts de stockage sans compromettre la disponibilité de leurs bases SQL Server sur Google Cloud.
