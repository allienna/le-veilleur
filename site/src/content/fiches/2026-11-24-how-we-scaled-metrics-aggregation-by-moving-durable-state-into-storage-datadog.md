---
title: "How we scaled metrics aggregation by moving durable state into storage | Datadog"
date: 2026-11-24
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.datadoghq.com%2Fblog%2Fengineering%2Fhow-we-scaled-metrics-aggregation%2F%3Futm_source=tldrdata/1/010001a2081c48fa-0fe56ffc-b235-4b40-9300-61b073fa6ac9-000000/iKPZ8iCycmtBRjL6dkrRNsX-Vt9wyGC3wHxEMDF5Fjs=452"
authors: ["Khayyam Guliyev"]
keywords: ["agrégation de métriques", "systèmes distribués", "Kafka", "gestion d'état", "streaming", "scalabilité"]
theme: "Data"
tone: "research"
used_in: ["2026-11-24"]
---

## Résumé
Datadog retrace l'évolution sur trois générations de son système d'agrégation de métriques, chaque génération devant absorber environ 10x le volume de la précédente. L'architecture est passée d'un partitionnement statique avec état local dans RocksDB, à une attribution dynamique des partitions avec état transférable via blob storage, puis à une conception où la couche de streaming devient "best-effort" et délègue la réconciliation durable (doublons, données tardives, backfills) au système de stockage de séries temporelles. Ce changement permet désormais de redémarrer directement au "bord en direct" (live edge) sans reconstruire des heures d'état historique, réduisant les coûts et simplifiant le passage à l'échelle.

## Points clés
- Génération 1 : partitions statiques Kafka, paires leader/follower, état dans RocksDB local ; scaling = division manuelle des partitions (~1h30 de travail coordonné) et calcul doublé entre leader et follower.
- Génération 2 : attribution dynamique des partitions, état RocksDB sauvegardé en continu (SSTables) vers du blob storage et découpé par fenêtres temporelles pour restaurer rapidement l'état récent ; a permis l'autoscaling mais la récupération d'état est devenue le nouveau goulot d'étranglement.
- Génération 3 : la couche de streaming ne garantit plus la correction durable elle-même ; elle délègue au stockage la réconciliation des agrégats partiels, doublons et données tardives, via un format fusionnable appliqué en lecture et en compaction.
- Les métriques de distribution utilisent des sketches DDSketch fusionnables, permettant de réduire les dimensions (ex. retirer `pod_name`) tout en gardant des percentiles globalement exacts.
- Le nouveau modèle permet de reprendre le traitement au niveau du flux en direct sans attendre la restauration de l'état historique, validé en production lors d'un incident réel.
- Migration vers la "Streaming Platform" interne de Datadog, qui remplace l'outillage Kafka maison pour la gestion des consommateurs et la bascule au live edge.

## Analyse approfondie

### Le problème : un état durable qui freine la scalabilité
Chaque nouvelle génération du système d'agrégation de métriques de Datadog devait absorber environ 10 fois le volume de métriques de la génération précédente. Avec cette croissance, la gestion et la récupération de l'état d'agrégation sont devenues la principale contrainte de scalabilité.

L'agrégation de métriques doit rester correcte même quand les données arrivent en retard, sont livrées plusieurs fois, ou que le traitement est interrompu. L'approche initiale répondait à cette exigence en gardant l'état historique proche du traitement. Cela fonctionnait bien à l'échelle initiale, mais la croissance a rendu la récupération, le scaling horizontal et les opérations quotidiennes de plus en plus difficiles.

Le système a été repensé sur trois générations : d'une propriété fixe des partitions, vers un état transférable, puis vers une conception où le stockage réconcilie lui-même les agrégats partiels, les livraisons dupliquées et les données tardives.

### Réduction de dimensions et agrégation de tags
Les métriques arrivent avec de nombreux tags décrivant où et comment chaque mesure a été produite. Les clients n'ont pas toujours besoin de conserver toutes ces dimensions sous forme interrogeable. Datadog leur permet de choisir quels tags restent interrogeables, réduisant ainsi le volume de métriques personnalisées indexées, ce qui diminue les coûts et améliore les performances de requête tout en préservant des résultats mathématiquement exacts sur les dimensions conservées.

Exemple : un service tournant sur 100 pods, chacun rapportant une distribution `service.request.duration` avec des tags `env`, `region`, `service`, `endpoint` et `pod_name`. En ne conservant que les quatre premiers tags, Datadog fusionne les distributions par pod en une série indexée unique, tout en calculant des percentiles globalement exacts grâce aux sketches DDSketch, qui se fusionnent sans stocker chaque mesure individuelle.

Le service d'agrégation backend doit : réduire des données de N dimensions à M dimensions (M < N) ; agréger sur des fenêtres courtes (ex. 10 secondes) ; intégrer les données tardives et gérer les doublons sans double comptage. Ces exigences rendent le service "stateful" : il doit se souvenir des données déjà intégrées et suivre les identifiants de message pour éviter les doublons lors des retries. Après panne ou redémarrage, cet état doit rester disponible ou être reconstruit — ce qui transforme la réduction de dimensions en un véritable problème de systèmes distribués.

Les trois architectures décrites ne sont pas des remplacements strictement équivalents ni limitées à un seul type de métrique (le partitionnement statique existait aussi bien pour les métriques ponctuelles que les distributions) ; elles illustrent une progression allant d'une propriété fixe à un état transférable, puis à une délégation de la réconciliation durable au stockage.

### Génération 1 : partitionnement statique
Le premier service d'agrégation distribué est né de l'expérience de Datadog avec Kafka : consommer des payloads depuis un broker, les agréger, puis transmettre les résultats au stockage en aval. Les payloads étaient partitionnés de façon déterministe, avec une topologie de déploiement statique.

Pour chaque payload, le service décodait et dédupliquait les données, sélectionnait les tags configurés, et fusionnait le DDSketch dans le bucket correspondant. Les buckets récents restaient en mémoire, tandis que RocksDB conservait plusieurs heures de buckets et d'identifiants de déduplication. Après un redémarrage sans état local utilisable, une instance devait consommer un intervalle complet de données avant de recommencer à transmettre des résultats — une période de "warm-up" rendant les redémarrages perturbateurs.

Chaque groupe de partitions avait un leader et un follower, qui effectuaient tous deux le travail d'agrégation mais où seul le leader écrivait normalement en aval. Si le leader tombait en panne, le follower prenait le relais avec une interruption minimale, car son état était presque à jour ; reconstruire une instance depuis zéro exigeait néanmoins le warm-up complet. Ce modèle doublait effectivement le calcul et rendait le scaling horizontal difficile, car les partitions étaient liées à des déploiements et tailles d'instance spécifiques.

Diviser une partition devenue trop grande exigeait de créer de nouvelles plages, mettre à jour la configuration, déployer de nouveaux leaders/followers, coordonner la bascule, vérifier les offsets Kafka et la sortie en aval, puis supprimer l'ancien déploiement — une opération documentée ayant nécessité environ 1,5 heure de travail coordonné, fragile et risquée pour la correction des données.

Cette architecture a soutenu une croissance significative, mais le calcul dupliqué, le travail de scaling manuel et les risques de correction sont devenus les principales contraintes, imposant de séparer la propriété des partitions des instances et de rendre l'état transférable.

### Génération 2 : attribution dynamique et état transférable
La deuxième génération a séparé la propriété des partitions des instances individuelles. Kafka pouvait réassigner dynamiquement les partitions selon les changements de composition du cluster, avec une assignation "sticky" pour limiter les mouvements inutiles lors des redémarrages.

Cette attribution dynamique a supprimé le besoin de diviser manuellement les partitions, mais a introduit un nouveau problème : quand une partition se déplaçait vers un autre nœud, celui-ci devait reconstruire son état d'agrégation avant de continuer. Chaque nœud maintenait son état local dans RocksDB, contenant les buckets d'agrégation et les informations de déduplication. Contrairement à la première génération, la base locale n'était plus la seule copie : chaque nœud téléversait en continu des modifications incrémentales SSTable vers du blob storage, permettant à un autre nœud de reconstruire l'état après réassignation.

Comme télécharger l'état complet à chaque réassignation aurait été trop coûteux, l'état RocksDB a été découpé en fenêtres temporelles : un nouveau nœud restaurait d'abord la fenêtre la plus récente, et ne chargeait les fenêtres plus anciennes qu'en cas de données tardives. Cela permettait au traitement courant de reprendre rapidement pendant que l'état historique se récupérait à la demande.

Cette conception a amélioré la récupération, réduit les coûts, et permis d'adopter un modèle d'autoscaling tenant compte non seulement du CPU mais aussi du volume d'état à déplacer, du temps de récupération, et de la capacité des nœuds restants à continuer à traiter pendant la réassignation. Ce comportement a été ajusté par des heuristiques expérimentales : scaler trop lentement laissait le service prendre du retard, scaler trop agressivement déclenchait de multiples restaurations simultanées, aggravant la charge.

Après cette migration, Datadog a pu supporter environ 10x plus de volume avec une intervention opérationnelle minimale. Mais avec la croissance continue, la gestion de l'état (bases locales, snapshots distants, fenêtres de récupération, réassignation) est devenue la principale source de complexité, les incidents amont et les grands backfills pouvant forcer de nombreux nœuds à récupérer simultanément — faisant de la récupération d'état le nouveau goulot d'étranglement.

### Génération 3 : déléguer la correction durable au stockage
La troisième génération repose sur une prémisse différente : le service de streaming n'a pas besoin de posséder l'agrégat final durable. Datadog avait déjà envisagé ce déplacement, mais la complexité ajoutée au stockage était difficile à justifier tant que l'architecture précédente fonctionnait bien ; une fois la récupération d'état devenue une contrainte de coût et de scaling, l'arbitrage a changé.

Le nouveau service rend l'agrégation et la déduplication en streaming "best-effort" : il combine autant de données arrivant à temps que possible et écarte les retries reconnaissables dans sa fenêtre active, tandis que les données tardives, les backfills et le travail non immédiat sont envoyés vers le stockage plutôt que de bloquer le pipeline en direct.

Le système de stockage comporte deux niveaux (temps réel récent et long terme), tous deux comprenant un format représentant des agrégats partiels plutôt que des points individuels. Chaque agrégat partiel identifie sa série et sa fenêtre temporelle, précise comment il doit être combiné avec d'autres contributions, et inclut l'information nécessaire pour détecter les doublons. Le stockage regroupe les contributions par série et fenêtre, supprime les doublons et combine les résultats — règles appliquées aussi bien en lecture entre niveaux de stockage que lors de la compaction en arrière-plan, laquelle consolide progressivement les résultats et intègre les données tardives sans rejouer le flux original ni récupérer l'état du worker. La représentation reste cohérente du stockage récent au stockage long terme.

Cette conception déplace la frontière de correction du système : le service d'agrégation priorise le trafic courant sans conserver plusieurs heures d'état durable, le stockage devenant responsable de combiner le chemin rapide avec les données arrivant plus lentement. Cette responsabilité n'était pas totalement nouvelle : le moteur de stockage de séries temporelles de Datadog devait déjà réconcilier les écritures tardives et désordonnées avant même l'introduction de la pré-agrégation en streaming. Étendre ce chemin de réconciliation a permis de déplacer l'état durable hors du service de streaming plutôt que de reproduire cette responsabilité dans chaque RocksDB de worker.

Les retries et pannes partielles restent gérés correctement : retraiter la même entrée ne change pas le résultat final, et les résultats de requête ne dépendent pas du chemin (streaming ou stockage différé) ayant réalisé l'agrégation. Le système reste stateful, mais son état durable vit désormais dans une couche conçue pour le conserver et le réconcilier.

Ce déplacement change aussi le modèle de récupération : la couche de streaming peut se réinitialiser au bord en direct pendant que le stockage réconcilie les données différées hors du chemin de traitement en direct. Il change également le modèle de coût : les workers de streaming n'ont plus besoin de disques dimensionnés pour plusieurs heures d'état RocksDB, ni de téléversement continu d'état incrémental, ni de téléchargement de gros snapshots à chaque déplacement de partition — permettant de provisionner la flotte pour le trafic courant plutôt que pour le pire cas de restauration simultanée de nombreux workers.

Cette génération marque aussi la première utilisation de la "Streaming Platform" interne de Datadog pour un service d'agrégation, remplaçant l'outillage Kafka maison (récupération, gestion des groupes de consommateurs, inspection d'état, gestion de surcharge, réinitialisation au bord en direct) et libérant l'équipe pour se concentrer sur le système d'agrégation lui-même.

Le déploiement a été validé en production : lors d'un incident, un opérateur a réinitialisé le traitement au bord en direct directement via l'interface de la Streaming Platform, tandis que le stockage gérait le travail d'agrégation différé — démontrant que restaurer le trafic courant ne nécessite plus de reconstruire d'abord tout l'état historique.

### Tableau récapitulatif des générations
| Génération | Propriété des partitions | État durable | Modèle de récupération | Limite principale |
|---|---|---|---|---|
| Première | Statique | RocksDB local | Prise de relais par le follower, ou traitement d'une fenêtre complète de données tardives avant reprise | Redémarrages perturbateurs, division manuelle, calcul dupliqué |
| Deuxième | Attribution dynamique (Kafka) | RocksDB local + blob storage | Restauration de l'état récent d'abord, fenêtres anciennes à la demande | Coût et complexité de récupération d'état |
| Troisième | Attribution dynamique (plateforme) | Stockage de séries temporelles | Reprise au bord en direct, réconciliation différée dans le stockage | Complexité de réconciliation dans le stockage et les requêtes |

Aucune conception n'était universellement meilleure : chacune correspondait à l'échelle et aux contraintes opérationnelles du moment.

### Conclusion : où faire vivre l'état
À travers les trois générations, le défi central était de décider où l'état devait vivre et combien devait être récupéré avant de pouvoir reprendre le traitement. La propriété statique gardait la correction locale, mais le scaling exigeait de changer manuellement la topologie de déploiement : une contrainte de correction était devenue une contrainte de scaling. Rendre l'état transférable a permis un scaling dynamique, mais le déplacer et le reconstruire est devenu le goulot d'étranglement suivant.

La troisième architecture change le modèle de récupération : la couche de streaming reprend au bord en direct sans restaurer d'abord des heures d'état historique, pendant que le stockage réconcilie agrégats partiels, doublons, données tardives et backfills — permettant de provisionner la flotte de streaming pour le trafic courant plutôt que pour le pire cas de restauration simultanée.

La leçon plus large : l'état n'a pas besoin de disparaître pour qu'une couche de traitement devienne plus facile à scaler. Quand la récupération devient un goulot d'étranglement, déplacer l'état entre workers peut ne pas suffire — le placer dans une couche conçue pour le conserver et le réconcilier peut préserver la correction tout en gardant l'historique hors du chemin critique.

## Pourquoi ça compte
Ce retour d'expérience illustre un arbitrage architectural récurrent dans les systèmes distribués à fort volume : déplacer la responsabilité de l'état durable du calcul vers le stockage pour découpler la vitesse de récupération de la taille de l'historique à reconstruire — une référence utile pour la veille sur les pipelines de streaming et l'observabilité à grande échelle.
