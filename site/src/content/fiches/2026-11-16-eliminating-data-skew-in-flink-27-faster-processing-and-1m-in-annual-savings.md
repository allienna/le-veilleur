---
title: "Eliminating Data Skew in Flink: 27% Faster Processing and $1M in Annual Savings"
date: 2026-11-16
url: "https://substack.com/redirect/352feb5b-0f04-4e25-9f5d-ec576ae3100d?j=eyJ1IjoiN3Y1bG1jIn0.HlvPOGYPdVknSYzEK1JIj6IFkAFn8zuyjtfU9Mbft9Q"
authors: ["Jeffrey Chuc"]
keywords: ["Apache Flink", "Kafka", "CDC", "Aurora", "optimisation de pipeline", "data skew"]
theme: "Data"
tone: "research"
used_in: ["2026-11-16"]
---

## Résumé
L'équipe Query and Data Platform de Rippling a identifié un goulot d'étranglement majeur dans son pipeline CDC MongoDB-vers-Aurora construit sur Apache Flink : un partitionnement par companyId créait des "hot subtasks" saturés pendant que d'autres restaient inactifs. En re-architecturant le système autour d'une clé de partition Kafka (sourcePartitionId) plutôt que du companyId, combinée à un hash MurmurHash3 inversé, une déduplication avant batching et des écritures concurrentes multi-shard vers Aurora, l'équipe a porté l'utilisation moyenne du CPU de 44% à 90%. Résultat : un gain de 27% sur le temps de traitement total et environ 1 million de dollars d'économies annuelles.

## Points clés
- Le partitionnement historique par companyId liait la charge d'un subtask Flink entier au volume d'un seul client, créant des "hot subtasks" saturés à 100% de CPU pendant que d'autres restaient inactifs.
- La solution repose sur un re-partitionnement par sourcePartitionId (la partition Kafka) via une fonction "InverseMurmur" qui inverse mathématiquement MurmurHash3 pour garantir une correspondance déterministe 1:1 entre partition Kafka et subtask Flink.
- Un opérateur personnalisé (KeyedProcessFunction) déduplique les messages avant la constitution des batches, garantissant des lots pleinement remplis envoyés à Aurora.
- Un nouvel écrivain concurrent (AuroraBatchWriter) répartit les enregistrements d'un même batch entre plusieurs shards Aurora et les écrit en parallèle via un pool de threads.
- Les gains mesurés : utilisation CPU moyenne de 44% à 90%, débit moyen en hausse de 38%, temps de traitement total réduit de 17h à 12,4h (-27%).
- Impact business : environ 80% d'économies mensuelles sur l'infrastructure, soit environ 84 000$/mois ou 1 million de dollars par an.

## Analyse approfondie

**Jeffrey Chuc**, Senior Software Engineer au sein de l'équipe Query and Data Platform de Rippling, a été confronté à un goulot d'étranglement critique dans le pipeline CDC MongoDB-vers-Aurora de Rippling, construit sur Apache Flink.

Pour résoudre ce problème, l'équipe a re-architecturé le système vers une architecture par clé de partition (Partition-Keyed Architecture). Ce changement a porté l'utilisation moyenne du CPU à 90%, réduit le temps de traitement total de plus de 27%, et devrait permettre d'économiser environ 1 million de dollars par an. La suite de cet article explique comment.

### Introduction

La pile analytique de Rippling ingère des données provenant de dizaines de produits et de centaines de modèles de données, les répliquant en temps réel depuis des sources comme MongoDB vers des stores optimisés pour les requêtes comme Aurora et Iceberg. Notre couche de requête spécifique au domaine, Rippling Query Language (RQL), s'appuie sur ce pipeline pour alimenter le reporting et les visualisations sur l'ensemble de la plateforme.

Dans cet article, nous nous concentrons sur le pipeline MongoDB-vers-Aurora de ce système, construit sur Apache Flink, et sur la façon dont nous avons éliminé un goulot d'étranglement critique en re-architecturant la répartition du travail entre les subtasks Flink. Nous passerons en revue le problème, les changements techniques nécessaires pour le résoudre, ainsi que les gains de performance et de coûts obtenus.

### Contexte

*Figure 1. Flux de données ETL Flink avec keyBy(companyId).*

Notre architecture Flink de Change Data Capture (CDC) consomme des messages depuis Kafka et les répartit entre les subtasks au sein du job ETL Flink. Chaque subtask traite un lot de messages pour une seule entreprise et écrit les résultats sur un shard Aurora RDS. Un shard Aurora RDS est une instance à l'échelle horizontale d'une base de données relationnelle Amazon Aurora, où chaque shard contient les données d'un sous-ensemble d'entreprises afin de répartir la charge de requêtage et de stockage entre plusieurs instances de base de données.

### Le problème : le goulot d'étranglement du "hot subtask"

Notre job Flink historique répartissait le travail en se basant sur le companyId (notre principal identifiant de "tenant"). Bien que pratique, cette approche liait la performance d'un subtask entier au volume de données d'un seul client. Les gros clients saturaient un subtask unique à 100% de CPU, tandis que les subtasks desservant de plus petits clients restaient inactifs. Ces "hot subtasks" devenaient des goulots d'étranglement pour l'ensemble du pipeline. Nous ne pouvions pas exploiter toute la capacité CPU disponible, ce qui entraînait une latence de traitement élevée et un gaspillage de dépenses d'infrastructure.

*Figure 2. Messages traités par seconde — ancienne architecture keyBy(companyId). La forte variance du débit de messages entre subtasks est le résultat d'une répartition inégale.*

*Figure 3. Utilisation moyenne du CPU — ancienne architecture keyBy(companyId). La plupart des subtasks restent inactifs tandis que quelques-uns sont saturés, plafonnant l'utilisation moyenne à 44%.*

### Le brainstorming

Pour 95% de nos cas d'usage, le pipeline fonctionnait exactement comme prévu. Mais une poignée de collections MongoDB avec des motifs d'écriture intenses et par rafales révélaient les limites de notre architecture par clé companyId. Un seul gros client pouvait inonder un subtask tandis que le reste du cluster restait inactif, sans aucun moyen de redistribuer cette charge après coup.

Nous savions que Kafka répartissait déjà les messages de manière équilibrée entre les partitions ; la démarche évidente était donc de partitionner par partition plutôt que par entreprise. Le problème était que nous n'avions aucun moyen d'ancrer chaque subtask Flink à une partition Kafka spécifique.

Nous avons passé la semaine suivante à expérimenter plusieurs approches, y compris l'API expérimentale reinterpretAsKeyedStream de Flink, mais rien ne nous donnait le contrôle déterministe dont nous avions besoin. Puis, en examinant l'implémentation interne de keyBy dans Flink, nous avons remarqué qu'elle utilisait MurmurHash3 en interne. Et si nous l'inversions simplement ?

### La solution : architecture par clé de partition

*Figure 4. Exemples de répartitions de données avec différentes clés keyBy.*

Kafka répartit déjà les messages de manière équilibrée entre les partitions. En re-partitionnant notre job Flink sur sourcePartitionId plutôt que sur companyId, nous pouvons tirer parti de cette répartition homogène. Cette refonte nécessitait trois changements techniques majeurs :

**1. Routage déterministe "InverseMurmur"**
- **Défi :** L'opérateur keyBy de Flink utilise MurmurHash3 en interne pour assigner les clés aux subtasks. Partitionner naïvement sur sourcePartitionId, un petit entier séquentiel, produit un regroupement sévère dans l'assignation des key-groups. Avec 10 partitions Kafka et 10 subtasks disponibles, MurmurHash3 mappait les 10 identifiants de partition sur seulement 5 subtasks, avec 60% de la charge totale concentrée sur seulement 2 d'entre eux. Les 5 autres subtasks restaient totalement inactifs.
- **Solution :** Nous avons implémenté une fonction MurmurHash inversée qui précalcule une clé synthétique garantie de hasher vers un subtask spécifique. Cela crée une correspondance déterministe 1:1 entre chaque partition source Kafka et un subtask Flink, garantissant une répartition parfaitement homogène sur l'ensemble du cluster.
- **Comment ça fonctionne :** MurmurHash3 est une fonction de hachage non cryptographique entièrement construite à partir d'opérations réversibles sur entiers 32 bits : rotations de bits, XOR, et multiplications par des constantes impaires (qui possèdent des inverses multiplicatifs modulaires). En appliquant chaque étape dans l'ordre inverse, on peut calculer l'entrée unique qui produit n'importe quel hash de sortie souhaité. Pour un sourcePartitionId donné, la fonction inverse génère une clé entière qui, une fois hashée en interne par le keyBy de Flink, aboutit exactement au subtask cible de cette partition.
- **Compromis :** Bien que s'appuyer sur la réversibilité d'un algorithme de hachage interne soit généralement déconseillé, nous avons choisi l'approche de hash inversé pour sa simplicité et sa prévisibilité par rapport aux alternatives. Nous avons mis en place des tests de régression robustes pour nous alerter immédiatement si la logique de hachage interne de Flink venait à changer.

**2. Opérateur personnalisé de fenêtrage et de déduplication**
- **Défi :** Dans l'ancienne architecture, la taille des lots était déterminée avant la déduplication. Les messages dupliqués gonflaient le compte de lots, si bien qu'une fois les doublons supprimés, les lots réellement envoyés à Aurora étaient systématiquement sous-dimensionnés. Cela gaspillait de la capacité d'écriture et augmentait le nombre d'allers-retours vers la base de données.
- **Solution :** Nous avons implémenté une KeyedProcessFunction personnalisée qui déduplique les messages avant la constitution des lots. L'opérateur met en tampon les enregistrements entrants dans un MapState Flink, indexé par identifiant d'enregistrement, et ne conserve que l'enregistrement avec l'offset Kafka le plus élevé pour chaque clé. Lorsque le tampon atteint la taille de lot configurée ou qu'un timeout se déclenche, il envoie en aval un lot pleinement rempli et dédupliqué. Cela garantit que chaque lot envoyé à Aurora est utilisé au maximum, réduisant les allers-retours et maximisant le débit d'écriture.

**3. Écritures par lots concurrentes vers Aurora**
- **Contexte :** Notre pipeline était initialement construit sur Apache Pinot, qui fonctionnait bien pour ses premiers cas d'usage : des requêtes sur des jeux de données plus petits avec des filtres favorables au pushdown. Mais en nous orientant vers un reporting plus large, nous avons rencontré une inadéquation fondamentale. Le modèle scatter-gather de Pinot est conçu pour des agrégations à fort débit, pas pour récupérer des centaines de mégaoctets de données brutes à joindre avec des sources externes avant agrégation. Cela transformait les Brokers de Pinot en une couche de brassage de données bloquée à 100% de CPU et sujette à des crashs OOM réguliers. Aurora était un choix peu conventionnel pour une charge analytique, mais nos benchmarks ont montré que Postgres égalait les performances de Pinot pour la taille de nos jeux de données. Aurora nous a apporté stabilité, gestion mémoire prévisible, et la maturité de l'écosystème Postgres. Pour les modèles vraiment massifs, nous sommes passés à Iceberg. Contrairement à Pinot, Aurora ne gère pas la mise à l'échelle horizontale en interne ; nous shardons donc nous-mêmes entre plusieurs instances Aurora, en routant le trafic via une clé de sharding, principalement le companyId.
- **Défi :** Lorsque nous partitionnions par companyId, chaque subtask traitait une seule entreprise par lot, si bien que chaque lot correspondait exactement à un shard Aurora. Le writer était conçu autour de cette hypothèse. Avec la nouvelle architecture par clé de partition, chaque subtask traite des messages de nombreuses entreprises, ce qui signifie qu'un seul lot peut contenir des enregistrements destinés à plusieurs shards Aurora différents. Le writer existant n'avait aucun mécanisme pour gérer cela.
- **Solution :** Nous avons remplacé le writer par AuroraBatchWriter, un writer concurrent qui regroupe les enregistrements d'un lot par shard Aurora cible, puis exécute des upserts parallèles sur tous les shards cibles via un pool de threads. Chaque shard dispose de son propre thread, de sorte que les lots multi-shards sont écrits en une seule passe plutôt que séquentiellement, shard par shard.

*Figure 5. Messages traités par seconde — nouvelle architecture keyBy(sourcePartitionId).*

*Figure 6. Utilisation moyenne du CPU — nouvelle architecture keyBy(sourcePartitionId).*

Nous avons benchmarké la nouvelle architecture sur un jeu de données fixe (3,5 millions de messages). La nouvelle architecture utilise en moyenne **90% du CPU** (contre 44% auparavant), ce qui indique que nous avons éliminé avec succès le goulot d'étranglement et exploitons pleinement le matériel.

Comme le montre la **Figure 6**, on observe une baisse du nombre de messages traités par seconde vers la fin du graphique ; cela s'explique par le fait que le traitement des partitions arrive à son terme, et le débit global de messages par seconde diminue naturellement à mesure que cela se produit.

#### Résultats du benchmark de performance

| | | **Ancienne architecture** | **Nouvelle architecture** | **% de variation** |
|---|---|---|---|---|
| **Débit (msg/sec)** | **Moyenne** | 3 430 | 4 750 | **38,48%** |
| | **Maximum** | 5 570 | 5 630 | **1,08%** |
| **Utilisation CPU** | **Moyenne** | 44,0% | 90,1% | **104,77%** |
| | **Maximum** | 60,6% | 100,0% | **65,02%** |
| **Temps de traitement (heures)** | **Total** | 17,0 | 12,4 | **-27,24%** |

*Tableau 1. Résultats de performance : ancienne architecture vs nouvelle architecture.*

*Figure 7. Messages traités par seconde — ancienne vs nouvelle architecture, côte à côte.*

En comparant le débit de messages de l'ancienne et de la nouvelle architecture dans la **Figure 7**, on observe une amélioration de la régularité du traitement sur le même jeu de données. La nouvelle architecture traite les messages avec un débit moyen par seconde plus élevé et un écart plus faible entre maximum et moyenne. Nous avons également constaté une **amélioration d'environ 27%** du temps de traitement, le même jeu de données étant désormais traité en **12,4 heures**, contre 17 heures auparavant.

### Impact business

Les optimisations techniques se sont traduites directement par une stabilité opérationnelle et des réductions de coûts significatives :

- **Résilience aux pics :** les pics de trafic CDC limités à un seul client sont désormais répartis sur tous les subtasks plutôt que d'étouffer un seul, réduisant drastiquement la latence de queue lors des événements à fort volume.
- **Réduction de l'infrastructure :** les gains d'efficacité nous ont permis de réduire l'échelle des jobs Flink dans tous les environnements.
- **Économies :** sur l'ensemble des environnements, nous avons réalisé des économies d'environ 80% par mois. À notre échelle actuelle, cela représente environ 84 000$/mois, soit environ 1 million de dollars par an.

### Conclusion

Ce projet a résolu le goulot d'étranglement le plus critique de notre pipeline MongoDB-vers-Aurora, mais ce n'est qu'un élément d'un effort plus large au sein de l'équipe Query and Data Platform. Nous appliquons désormais une réflexion similaire à nos autres chemins d'ingestion — en optimisant notre réplication vers Iceberg, en améliorant les garanties de fraîcheur des données, et en faisant évoluer l'infrastructure qui alimente RQL sur l'ensemble de la surface produit croissante de Rippling.

Si vous êtes passionné par le traitement de flux, l'infrastructure de données, et la résolution de problèmes de systèmes distribués qui impactent directement des millions d'utilisateurs, nous serions ravis d'échanger avec vous.

**Auteur**

Jeffrey Chuc est Senior Software Engineer au sein de l'équipe Query and Data Platform de Rippling, où il construit des pipelines de traitement de flux en temps réel. Il se concentre sur l'automatisation de systèmes ETL évolutifs et sur l'infrastructure de données qui alimente les produits analytiques de Rippling.

## Pourquoi ça compte
Ce cas pratique illustre de façon concrète et chiffrée comment un choix de clé de partitionnement dans un pipeline de streaming peut déterminer l'utilisation réelle du CPU disponible, et comment une astuce d'ingénierie (inverser un hash interne) peut débloquer des gains à six chiffres sans changer d'infrastructure sous-jacente. Il offre aussi un retour d'expérience intéressant sur les arbitrages Pinot vs Aurora/Postgres pour des charges analytiques hybrides.
