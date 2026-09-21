---
title: "Debugging large datasets with DuckDb"
date: 2026-09-21
url: "https://substack.com/redirect/367facbe-dfac-49f1-b51f-f0e75d17e794?j=eyJ1IjoiN3Y1bG1jIn0.HlvPOGYPdVknSYzEK1JIj6IFkAFn8zuyjtfU9Mbft9Q"
keywords: ["DuckDB", "S3", "ingestion de données", "débogage", "facturation", "requêtes SQL"]
theme: "Data"
tone: "tutorial"
used_in: ["2026-09-21"]
---

## Résumé
Orb, une plateforme d'infrastructure de facturation et de monétisation en temps réel, explique comment elle utilise DuckDB pour déboguer les problèmes d'ingestion de données de ses clients. Lorsque des événements envoyés via S3 échouent à la validation ou à la déduplication, l'équipe support d'Orb utilise DuckDB pour interroger directement les fichiers bruts dans S3, sans infrastructure persistante à maintenir. Cette approche s'est révélée performante, à la demande et suffisamment expressive pour reproduire les requêtes de métriques d'Orb directement sur les données brutes. L'entreprise envisage désormais d'étendre cet usage vers le self-service client, l'exploration de données et des cas d'usage en production.

## Points clés
- Orb ingère les événements de facturation via une API batch ou, de plus en plus, via S3 utilisé comme bus de messages (jusqu'à des centaines de milliers d'événements par seconde).
- Chaque événement passe par une étape de validation (conformité du JSON, présence des IDs Orb, respect d'une fenêtre de tolérance temporelle) et de déduplication (via une clé d'idempotence).
- Les événements rejetés finissent dans une dead letter queue, mais comprendre la nature exacte du problème nécessite un outil d'analyse ad-hoc.
- DuckDB a été choisi pour trois critères : usage à la demande (pas d'infrastructure permanente), performance sur des dizaines à centaines de Go de données en quelques secondes, et expressivité (SQL arbitraire, y compris sur des structs).
- DuckDB permet d'interroger directement des fichiers S3 comme des tables relationnelles, sans infrastructure dédiée — juste un client installé sur une instance EC2 de production.
- Orb envisage d'étendre l'usage de DuckDB au self-service client, à l'exploration de données (à la Rill), à des architectures hybrides via MotherDuck, et à des cas d'usage en production comme l'alerting temps réel.

## Analyse approfondie
Chez Orb, nous construisons une infrastructure temps réel pour la facturation et la monétisation des entreprises modernes. Le processus d'intégration avec Orb commence par l'envoi de données sous forme d'événements d'usage, qui représentent l'usage produit facturable dans votre application. Orb permet de construire des métriques (requêtes d'agrégation sur vos événements) et d'attacher ces métriques à des modèles de tarification.

Bien qu'Orb fournisse une API d'ingestion batch directe, il existe une solution d'ingestion de plus en plus populaire parmi nos clients, en particulier pour les cas d'usage à fort volume : l'ingestion via S3 utilisé comme bus de messages. Du côté d'Orb, nous mettons en place des notifications d'événements S3 inter-comptes sur un bucket auquel vous nous donnez un accès en lecture, et nous ingérons immédiatement tout fichier qui atterrit dans ce bucket. C'est également pratique pour nos clients, puisqu'il existe généralement déjà une sortie vers S3 (que ce soit depuis Kafka, Kinesis, ou un export périodique depuis un data warehouse). Cette dernière méthode a permis de monter en charge jusqu'à des centaines de milliers d'événements par seconde — ce qui n'est pas surprenant, puisque S3 est le graal de la fiabilité et offre un débit de lecture et d'écriture considérable.

Entre la source d'entrée (dans ce cas, S3) et notre datastore d'événements, deux choses doivent encore se produire :

1. **Validation** : Orb s'assure que le payload est valide en vérifiant que le JSON de l'événement respecte le schéma attendu, et que les identifiants Orb sont déjà présents. Orb vérifie également que l'horodatage d'un événement se situe dans la période de tolérance d'ingestion (typiquement quelques heures), ce qui empêche nos clients d'ingérer d'anciennes données qui ne peuvent plus être répercutées sur la facturation.
2. **Déduplication** : Orb déduplique sur la base d'une clé d'idempotence présente dans le corps de l'événement.

Ce n'est que lorsqu'un événement passe la validation et que nous avons vérifié qu'il ne s'agit pas d'un doublon que nous l'ingérons dans notre datastore d'événements.

## Qu'est-ce qui nécessite du débogage ?

Bien qu'Orb dispose d'outils détaillés et flexibles intégrés au produit sur les données ingérées, lorsque les clients intègrent notre plateforme pour la première fois, il existe parfois un problème en amont : tout ce qui se trouve dans le bucket n'est pas ingéré, et finit à la place dans une dead letter queue parce que cela échoue à la validation, à la déduplication, ou aux deux. Bien qu'inspecter la dead letter queue soit un point de départ pour des intégrations basiques, comprendre réellement la nature du problème demande davantage de travail.

Lorsque nous avons commencé à chercher une solution pouvant aider notre équipe de support technique à aider les clients à s'assurer que leurs données étaient prêtes pour la production, nous avions quelques critères pour que ce soit adapté à notre cas d'usage :

1. **À la demande** : nous devions pouvoir interroger les données de manière ad-hoc dans S3 afin d'en déboguer le contenu, mais ce n'était pas une charge de travail de production persistante. Nous n'avons pas exploré de solutions nécessitant de maintenir une infrastructure tournant en permanence.
2. **Performant** : l'outil choisi devait être performant à une échelle « moyenne » (des dizaines ou centaines de gigaoctets de données). Bien que le volume total d'ingestion dans Orb soit souvent bien plus élevé, nous effectuons des analyses sur des plages temporelles plus restreintes, et cette tâche devait prendre quelques secondes afin que nous puissions comprendre avec souplesse l'origine des problèmes.
3. **Expressif** : Orb permet de définir des requêtes SQL arbitraires comme métrique, et pas seulement un nombre limité de fonctions d'agrégation. Nous voulions avoir la possibilité d'exécuter ces requêtes directement sur les données brutes, sans avoir à construire manuellement une couche de traduction supplémentaire.

DuckDB répond à ces trois critères.

## Ce que permet DuckDB

Lorsque les clients constatent une divergence entre leurs métriques et les données qu'ils pensent envoyer à Orb, nous pouvons désormais les aider à déboguer directement à la source ; ils n'ont pas besoin de faire appel à une aide côté data science pour déboguer les jeux de données arrivant dans Orb.

Nous avons installé un client DuckDB sur une instance EC2 de production polyvalente, mais en dehors de cela, il n'y a absolument aucune infrastructure qui tourne.

C'est simple — instantané, en fait — d'attacher une instance DuckDB pour interroger un fichier distant dans S3, en utilisant un rôle personnalisé que l'on endosse temporairement. Nous pouvons commencer par effectuer de simples comptages sur la période concernée, en trouvant les événements dupliqués qui auraient été rejetés par l'API d'ingestion d'Orb. Cela nous aide à comprendre le schéma des doublons, et à quel moment ils surviennent :

Remarquez comme interagir avec le fichier S3 comme s'il s'agissait d'une table relationnelle est fluide ici ! DuckDB nous permet également de reproduire directement les métriques que nous supportons dans Orb sur les événements qui atterrissent dans S3. Supposons, par exemple, que nous découvrions que le client du customer assigne incorrectement les clés d'idempotence, et que nous dédupliquons donc plus de données que prévu. En ignorant la contrainte de doublon et en exécutant la métrique sur les événements bruts du bucket (grâce au support des structs), nous pouvons confirmer que le reste des données est correct, évitant ainsi une boucle de réingestion.

Nous avons trouvé DuckDB très rapide pour ce type de débogage sur des millions de lignes de données — et nous nous attendons à des performances encore meilleures pour les fichiers Parquet, où le protocole httpfs et le format de métadonnées Parquet permettent à DuckDB de ne télécharger que sélectivement certaines portions du fichier.

## Ce qui attend DuckDB chez Orb

Nous envisageons d'étendre les cas d'usage des manières suivantes :

1. **Débogage en self-service** : nous voulons proposer l'expérience de débogage décrite ci-dessus directement à nos clients, afin qu'ils puissent exploiter notre infrastructure de données *et* leurs métriques définies dans Orb sur leurs données brutes.
2. **Meilleure exploration des données** : des produits comme Rill s'appuient sur DuckDB pour construire des tableaux de bord de requêtage instantané, sans le moindre bouton « exécuter ».
3. **Combiner différentes sources de données** : une limitation actuelle de cette architecture (et d'autres cas d'usage que nous envisageons pour DuckDB) est la nécessité de disposer d'une machine unique assez puissante pour héberger DuckDB. Nous sommes enthousiastes à l'idée d'explorer des solutions comme MotherDuck, qui offrent une persistance de données hébergée, ainsi que la capacité d'interroger à la fois des données locales et distantes.
4. **Cas d'usage en production** : DuckDB peut nous aider à accélérer des cas d'usage de production comme l'alerting en temps réel, où nous pouvons exploiter un working set en mémoire nettement plus petit pour nos requêtes.

Utiliser DuckDB comme outil de débogage pour le support peut sembler un cas d'usage mineur, mais cela nous a permis de comprendre ses caractéristiques de performance et de gagner en confiance pour étendre sa place dans la stack technique d'Orb.

## Pourquoi ça compte
Ce retour d'expérience illustre une tendance de fond en data engineering : utiliser DuckDB comme moteur d'analyse ad-hoc directement sur des fichiers dans un data lake (S3), sans infrastructure dédiée ni pipeline ETL préalable — un pattern de plus en plus adopté pour le débogage et l'exploration de données à moindre coût opérationnel.
