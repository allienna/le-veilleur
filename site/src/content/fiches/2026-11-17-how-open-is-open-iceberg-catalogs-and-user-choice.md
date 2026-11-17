---
title: "How Open Is Open? Iceberg, Catalogs, and User Choice"
date: 2026-11-17
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.dataengineeringweekly.com%2Fp%2Fhow-open-is-open-iceberg-catalogs%3Futm_source=tldrdata/1/010001a1e4102a7f-1707763f-bcae-44fd-9622-7435fac8cdc6-000000/hxIkSQ845ythsOud2fpv4BvNGwB_eBIsWUpgHasuA84=452"
keywords: ["Apache Iceberg", "catalogues REST", "interopérabilité", "open source", "vendor lock-in", "data engineering"]
theme: "Data"
tone: "opinion"
used_in: ["2026-11-17"]
---

## Résumé
L'article interroge ce que signifie réellement l'« ouverture » d'Apache Iceberg et de son écosystème de catalogues, en réaction aux récents débats sur l'interopérabilité du format. L'auteur soutient que les utilisateurs ont besoin d'une définition de l'ouverture qu'ils peuvent vérifier eux-mêmes, indépendamment des discours des fournisseurs, car le choix du catalogue a des conséquences architecturales et financières majeures (changer de moteur de requête, opérer son propre catalogue, quitter un fournisseur). Il propose que la communauté Iceberg établisse une base de référence opérationnelle commune : un catalogue de production déployable indépendamment, des résultats de compatibilité publics et versionnés, des tests de performance comparatifs, et des procédures de migration documentées. Deux ajouts (probablement des commentaires de lecteurs) viennent nuancer le propos en soulignant que le vrai risque se situe au niveau des écrivains concurrents actifs lors d'un changement de catalogue.

## Points clés
- L'« ouverture » d'un format comme Iceberg ne peut pas se limiter à une déclaration marketing : elle doit être vérifiable indépendamment des fournisseurs.
- Le catalogue REST d'Iceberg occupe une position stratégique car il encapsule la logique de commit et l'accès au stockage, ce qui crée une dépendance commerciale potentielle vis-à-vis de son opérateur.
- L'interopérabilité réelle dépasse la simple connexion moteur-catalogue : elle doit couvrir la montée en charge des métadonnées, les écrivains concurrents, le renouvellement des identifiants et les charges de travail exigeantes.
- Le précédent du Hive Metastore montre l'intérêt d'une cible d'intégration commune et opérable par tous, facilitant la reproductibilité des comportements.
- Des briques existent déjà (Apache Polaris, REST Compatibility Kit) mais manquent d'un lien explicite avec des attentes claires d'adoption, de validation et de choix utilisateur.
- Le vrai test de l'ouverture porte sur les écrivains actifs lors d'un changement de catalogue : un changement mal maîtrisé peut corrompre silencieusement une table.

## Analyse approfondie
Construire une plateforme de données neutre vis-à-vis des fournisseurs a longtemps été un rêve pour les entreprises : une plateforme libre de tout verrouillage fournisseur, offrant un meilleur contrôle des coûts et des analyses plus rapides. Une demande simple et légitime. Mais la réalité est différente, même avec des formats de table dits « ouverts ».

Les débats récents sur l'ouverture et l'interopérabilité d'Apache Iceberg ont ravivé une préoccupation que l'auteur juge essentielle pour l'industrie : les utilisateurs ont besoin d'une définition de l'ouverture qu'ils peuvent vérifier eux-mêmes, indépendamment des affirmations des fournisseurs.

Pour les responsables de l'ingénierie des données, l'ouverture a des conséquences architecturales et financières. Une équipe peut-elle changer de moteur de requête, exploiter son propre catalogue, ou remplacer un fournisseur sans reconstruire toute sa plateforme ? Quelles capacités, performances ou quel contrôle perdrait-elle en chemin ?

Apache Iceberg constitue une base essentielle pour cette indépendance. Le protocole de catalogue REST d'Iceberg place la logique de commit derrière une interface commune et permet de déléguer l'accès au stockage. Le catalogue influence donc la façon dont les moteurs accèdent aux tables et les mettent à jour. Son opérateur occupe de fait une position déterminante dans l'architecture.

Cette position crée une influence commerciale. Les fournisseurs investissent dans des intégrations, la sécurité et la performance pour rendre leurs plateformes attractives. Les utilisateurs doivent comprendre quand ces avantages créent des dépendances qui restreignent leurs choix futurs.

Une interface publiée établit un contrat ; une implémentation partagée et des tests reproductibles permettent d'en révéler les limites pratiques.

Connecter un moteur à un catalogue ne constitue qu'une partie de l'histoire de l'interopérabilité. En production, les métadonnées croissent, les écritures sont concurrentes, les identifiants doivent être renouvelés, et les charges de travail sont exigeantes. Iceberg prend en charge des fonctionnalités comme le chargement différé des snapshots (« lazy snapshot loading ») et la planification de scan côté serveur. Les implémentations de moteurs et de catalogues peuvent utiliser ces capacités différemment, ce qui affecte l'efficacité avant même le traitement des données.

Une meilleure ingénierie devrait se traduire par de meilleures performances. Les utilisateurs ont besoin de preuves pour distinguer ces améliorations réelles des intégrations incomplètes, des fonctionnalités non supportées et des dépendances propriétaires. Sans cela, chaque organisation doit enquêter seule sur les limites réelles de l'ouverture.

La communauté Iceberg devrait établir une base de référence opérationnelle claire et inciter l'écosystème à l'adopter.

Le Hive Metastore constitue un précédent utile. Il offrait aux développeurs de moteurs une cible d'intégration concrète, et aux organisations un service qu'elles pouvaient elles-mêmes exploiter. Ce socle commun a permis aux développeurs de reproduire les comportements et aux utilisateurs d'investiguer les problèmes en dehors de l'environnement d'un fournisseur.

La communauté dispose déjà d'un travail substantiel sur lequel s'appuyer. Apache Polaris implémente l'API REST d'Iceberg, et Iceberg maintient un kit de compatibilité REST (REST Compatibility Kit) pour tester les serveurs de catalogue. La prochaine étape devrait consister à relier ces contributions à des attentes explicites en matière d'adoption, de validation et de choix pour l'utilisateur.

La communauté devrait se rallier autour d'un catalogue prêt pour la production, que les utilisateurs peuvent déployer de façon indépendante, et que les moteurs peuvent prendre en charge comme cible d'intégration commune.

Elle devrait accueillir favorablement les implémentations alternatives tout en maintenant la spécification comme référence faisant autorité. Des résultats de compatibilité publics et versionnés devraient identifier les opérations supportées, les capacités optionnelles, les configurations et les limitations.

Des tests de performance devraient compléter ces résultats. Avec des conditions contrôlées de données, de calcul, de placement réseau et de cache, les utilisateurs pourraient comparer le chargement des métadonnées, le comportement de planification et les commits concurrents. Ces comparaisons expliqueraient les différences de performance et aideraient les équipes à prendre des décisions informées.

La migration doit recevoir une attention égale. Changer de catalogue implique des permissions, des identités, des identifiants, un état spécifique au catalogue, et des écrivains actifs. La communauté devrait publier des procédures testées expliquant ce que les utilisateurs peuvent déplacer et quelles dépendances subsistent.

Une base de référence fiable renforcerait la concurrence. Les fournisseurs pourraient démontrer leurs améliorations par rapport à des attentes partagées. Les utilisateurs pourraient évaluer ensemble les bénéfices et les dépendances. Les développeurs de moteurs pourraient s'intégrer sur un socle que la communauté maintient et teste.

Le débat public a mis en lumière une question qui mérite une réponse technique. La communauté Iceberg devrait transformer cette question en code partagé, en preuves publiées et en recommandations pratiques.

« Jusqu'où est-ce ouvert ? » devrait se résumer à ce que les utilisateurs peuvent exécuter, ce qu'ils peuvent changer, et ce qu'ils peuvent emporter avec eux. La communauté doit leur donner les preuves nécessaires pour faire ce choix.

*Tous droits réservés, Dewpeche Private Limited. L'auteur fournit des liens à titre informatif et ne les cautionne pas. Les opinions exprimées dans cette newsletter lui sont propres et ne représentent les avis d'aucun employeur actuel, passé ou futur.*

Deux remarques complémentaires (probablement issues des commentaires) nuancent l'article. La première souligne que c'est au niveau des écrivains actifs que les migrations de catalogue échouent : la fonction `register_table` d'Iceberg permet de faire pointer un nouveau catalogue vers le `metadata.json` existant, mais la documentation avertit qu'un même fichier enregistré dans deux catalogues peut perdre des mises à jour ou corrompre la table — tout job continuant à committer via l'ancien catalogue la ferait silencieusement diverger (« fork »). Il faut donc arrêter tous les écrivains avant d'enregistrer la table ailleurs, puis rebasculer les moteurs un par un. La seconde remarque relève que les écrivains concurrents et le renouvellement des identifiants sont précisément les points où la plupart des promesses d'« ouverture » risquent de se briser : une base de référence qui ne vérifierait que la connexion et la lecture ne détecterait pas deux moteurs committant simultanément sur la même table via le catalogue — d'où la question de savoir si les tests proposés couvriraient aussi les conflits de commit et le comportement de nouvelle tentative (retry).

## Pourquoi ça compte
Ce texte capture une tension centrale de l'écosystème data lakehouse actuel : la promesse d'ouverture d'Iceberg se heurte à la réalité des dépendances créées par les catalogues propriétaires, un sujet stratégique pour toute organisation évaluant son exposition au vendor lock-in.
