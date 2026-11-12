---
title: "How Open Is Open? Iceberg, Catalogs, and User Choice"
date: 2026-11-12
url: "https://substack.com/redirect/2/eyJlIjoiaHR0cHM6Ly93d3cuZGF0YWVuZ2luZWVyaW5nd2Vla2x5LmNvbS9wL2hvdy1vcGVuLWlzLW9wZW4taWNlYmVyZy1jYXRhbG9ncz91dG1fY2FtcGFpZ249ZW1haWwtaGFsZi1wb3N0JnI9N3Y1bG1jJnRva2VuPWV5SjFjMlZ5WDJsa0lqbzBOelUxT1RJMk1qZ3NJbkJ2YzNSZmFXUWlPakl5TkRVeE1qZ3pNU3dpYVdGMElqb3hOemswTkRNd01qWXlMQ0psZUhBaU9qRTNPVGN3TWpJeU5qSXNJbWx6Y3lJNkluQjFZaTAzTXpJM01TSXNJbk4xWWlJNkluQnZjM1F0Y21WaFkzUnBiMjRpZlEuQl9kbEZlZzJiUmF2ZnlfQ1I0ZWVNNEp6a2gtZmphODlGUTVpNnlVampEQSIsInAiOjIyNDUxMjgzMSwicyI6NzMyNzEsImYiOnRydWUsInUiOjQ3NTU5MjYyOCwiaWF0IjoxNzk0NDMwMjYyLCJleHAiOjIxMTAwMDYyNjIsImlzcyI6InB1Yi0wIiwic3ViIjoibGluay1yZWRpcmVjdCJ9.P7zmYF2EAOHD-sDsLnDHeDjZPzEmuKQB2yuh-2jfW8Y?"
keywords: ["Apache Iceberg", "catalogue REST", "interopérabilité", "open source", "vendor lock-in", "data engineering"]
theme: "Data"
tone: "opinion"
used_in: ["2026-11-12"]
---

## Résumé

Ce billet d'opinion revient sur les récents débats autour de l'ouverture réelle d'Apache Iceberg et de son protocole de catalogue REST, qui occupe une position centrale et potentiellement verrouillante dans l'architecture des plateformes data. L'auteur soutient que les utilisateurs ont besoin d'une définition de l'ouverture qu'ils peuvent vérifier eux-mêmes, indépendamment des revendications marketing des fournisseurs, en s'appuyant sur des tests reproductibles, des résultats de compatibilité publiés et des procédures de migration documentées. En s'inspirant du précédent de Hive Metastore, il appelle la communauté Iceberg à transformer les briques existantes (Apache Polaris, REST Compatibility Kit) en une base opérationnelle commune, testée et versionnée. Le texte se conclut par un point technique concret : migrer de catalogue sans arrêter au préalable tous les writers actifs risque de « forker » silencieusement une table.

## Points clés

- L'ouverture d'un format de table « open » comme Iceberg ne garantit pas, en pratique, l'absence de vendor lock-in : le catalogue REST occupe une position d'influence commerciale pour son opérateur.
- Les utilisateurs ont besoin de preuves vérifiables (tests reproductibles, implémentation partagée) plutôt que de simples déclarations d'ouverture des fournisseurs.
- Hive Metastore est cité comme précédent réussi : une cible d'intégration commune, opérable par les organisations elles-mêmes, a favorisé la reproductibilité et l'autonomie des utilisateurs.
- La communauté dispose déjà des briques nécessaires (Apache Polaris, REST Compatibility Kit) mais doit les relier à des attentes explicites d'adoption et de validation.
- Trois piliers sont proposés : résultats de compatibilité publics et versionnés, benchmarks de performance contrôlés, et procédures de migration testées et documentées.
- Point technique critique : la migration de catalogue via `register_table` est dangereuse si des writers continuent de committer sur l'ancien catalogue, pouvant corrompre ou forker silencieusement la table.

## Analyse approfondie

Construire une plateforme de données neutre vis-à-vis des fournisseurs est depuis longtemps le rêve des entreprises : une plateforme libérée du vendor lock-in, avec un meilleur contrôle des coûts, et qui permette des insights analytiques plus rapides. Une demande simple et légitime. Nous savons tous que la réalité est différente, même avec des formats de table « ouverts ».

Les débats récents sur l'ouverture et l'interopérabilité d'Apache Iceberg ont renforcé une préoccupation que l'industrie doit, selon moi, adresser :

les utilisateurs ont besoin d'une définition de l'ouverture qu'ils peuvent vérifier indépendamment des fournisseurs qui en revendiquent le mérite.

Pour les responsables data engineering, l'ouverture a des conséquences architecturales et financières. Une équipe peut-elle changer de moteur de requête, exploiter son propre catalogue, ou remplacer un fournisseur sans reconstruire sa plateforme ? Quelles capacités, quelles performances ou quel contrôle perdrait-elle ?

Apache Iceberg constitue un socle essentiel pour cette indépendance. Le protocole de catalogue REST d'Iceberg place la logique de commit derrière une interface commune et prend en charge des mécanismes de délégation de l'accès au stockage. Le catalogue influence donc la manière dont les moteurs accèdent aux tables et les mettent à jour. Son opérateur occupe une position déterminante dans l'architecture. (**Spécification du catalogue REST**)

Cette position crée une influence commerciale. Les fournisseurs investissent dans les intégrations, la sécurité et la performance pour rendre leurs plateformes attractives. Les utilisateurs doivent comprendre dans quelle mesure ces avantages créent des dépendances qui contraignent leurs choix futurs.

Une interface publiée établit un contrat ; une implémentation partagée et des tests reproductibles permettent d'en révéler les limites pratiques.

Connecter un moteur à un catalogue ne constitue qu'une partie de l'histoire de l'interopérabilité. La production introduit des métadonnées croissantes, des writers concurrents, un renouvellement des identifiants (credentials) et des charges de travail exigeantes. Iceberg prend en charge des fonctionnalités comme le chargement différé des snapshots (lazy snapshot loading) et la planification de scan côté serveur (server-side scan planning). Les implémentations de moteurs et de catalogues peuvent utiliser ces capacités différemment, ce qui affecte l'efficacité avant même que le traitement des données ne commence. (Protocole de catalogue REST)

Une meilleure ingénierie devrait se traduire par de meilleures performances. Les utilisateurs ont besoin de preuves pour distinguer ces améliorations des intégrations incomplètes, des fonctionnalités non supportées et des dépendances propriétaires. Sans cela, chaque organisation doit enquêter elle-même, indépendamment, sur les limites réelles de cette ouverture.

La communauté Iceberg devrait établir une base opérationnelle claire et encourager l'écosystème à l'adopter.

Hive Metastore offre un précédent utile. Il a donné aux développeurs de moteurs une cible d'intégration concrète, et aux organisations un service qu'elles pouvaient exploiter elles-mêmes. Ce socle commun a aidé les développeurs à reproduire les comportements et les utilisateurs à investiguer les problèmes en dehors de l'environnement d'un fournisseur.

La communauté dispose déjà d'une base de travail substantielle. Apache Polaris implémente l'API REST d'Iceberg, et Iceberg maintient un REST Compatibility Kit pour tester les serveurs de catalogue. La prochaine étape devrait relier ces contributions à des attentes explicites en matière d'adoption, de validation et de choix pour l'utilisateur. (**Apache Polaris, REST Compatibility Kit**)

La communauté devrait se rallier autour d'un catalogue prêt pour la production, que les utilisateurs peuvent déployer de façon autonome, et que les moteurs peuvent supporter comme cible d'intégration commune.

Elle devrait accueillir des implémentations alternatives tout en conservant la spécification comme référence faisant autorité. Des résultats de compatibilité publics et versionnés devraient identifier les opérations supportées, les capacités optionnelles, les configurations et les limitations.

Des charges de travail de performance devraient compléter ces résultats. Avec des données, du compute, un placement réseau et des conditions de cache contrôlés, les utilisateurs pourraient comparer le chargement des métadonnées, le comportement de planification et les commits concurrents. Ces comparaisons expliqueraient les différences de performance et aideraient les équipes à prendre des décisions informées.

La migration doit recevoir une attention égale. Changer de catalogue implique des permissions, des identités, des identifiants, un état spécifique au catalogue, et des writers actifs. La communauté devrait publier des procédures testées expliquant ce que les utilisateurs peuvent migrer et quelles dépendances subsistent.

Une base fiable renforcerait la concurrence. Les fournisseurs pourraient démontrer leurs améliorations par rapport à des attentes partagées. Les utilisateurs pourraient évaluer ensemble les bénéfices et les dépendances. Les développeurs de moteurs pourraient intégrer leurs solutions sur un socle que la communauté maintient et teste.

Le débat public a mis en lumière une question qui mérite une réponse d'ingénierie. La communauté Iceberg devrait transformer cette question en code partagé, en preuves publiées et en recommandations pratiques.

« À quel point est-ce vraiment ouvert ? » devrait se résumer à ce que les utilisateurs peuvent faire tourner, ce qu'ils peuvent changer, et ce qu'ils peuvent emporter avec eux. La communauté doit leur fournir les preuves nécessaires pour faire ce choix.

*Tous droits réservés, Dewpeche Private Limited. Je fournis des liens à titre informatif et ne les cautionne pas. Toutes les opinions exprimées dans cette newsletter sont les miennes et ne représentent pas les opinions d'employeurs actuels, anciens ou futurs.*

Les writers actifs sont l'endroit où les migrations de catalogue échouent. La fonction register_table d'Iceberg peut faire pointer un nouveau catalogue vers le metadata.json existant, mais la documentation avertit que le même fichier enregistré dans deux catalogues peut entraîner la perte de mises à jour ou la corruption de la table : tout job qui continue de committer via l'ancien catalogue la fork silencieusement. Arrêtez tous les writers avant d'enregistrer le nouveau catalogue, puis repointez les moteurs un par un.

## Pourquoi ça compte

Pour toute équipe data qui a misé sur Iceberg pour s'affranchir du lock-in, ce texte rappelle qu'un format « ouvert » ne vaut que ce que sa couche catalogue permet réellement de changer, et alerte sur un piège opérationnel concret (writers actifs) à surveiller lors de toute migration de catalogue.
