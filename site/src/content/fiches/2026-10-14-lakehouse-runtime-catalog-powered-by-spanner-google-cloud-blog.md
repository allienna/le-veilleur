---
title: "Lakehouse runtime catalog powered by Spanner | Google Cloud Blog"
date: 2026-10-14
url: "https://cloud.google.com/blog/products/data-analytics/lakehouse-runtime-catalog-powered-by-spanner/"
authors: ["Vinod Ramachandran", "Mina Mikhail"]
keywords: ["lakehouse", "Apache Iceberg", "catalogue de métadonnées", "Spanner", "Google Cloud", "agents IA"]
theme: "Data"
tone: "news"
used_in: ["2026-10-14"]
---

## Résumé
Google Cloud présente le Lakehouse runtime catalog, un catalogue de métadonnées serverless désormais disponible en disponibilité générale (GA), conforme à la spécification Iceberg REST Catalog et propulsé par Spanner. L'article explique pourquoi les catalogues Iceberg traditionnels peinent à garantir à la fois cohérence transactionnelle, haute disponibilité et scalabilité horizontale à l'ère des requêtes massives générées par les agents IA. Il détaille les bénéfices architecturaux de la solution (interopérabilité multi-moteurs, fédération cross-cloud, credential vending, intégration avec Knowledge Catalog) et cite le cas d'Etsy, qui a accéléré ses requêtes de pipeline de 60 % après migration. L'ambition affichée est de poser les fondations d'un "lakehouse sans frontières" combinant charges analytiques et opérationnelles pour l'ère agentique.

## Points clés
- Le Lakehouse runtime catalog est un catalogue Iceberg REST entièrement serverless et hautement disponible, construit sur Spanner (jusqu'à 99,99 % de disponibilité, scalabilité horizontale automatique).
- Il répond à cinq défis majeurs des catalogues managés : commits atomiques (CAS/OCC), haute disponibilité, scalabilité de la base backend, coordination de la maintenance des tables (compaction, expiration des snapshots), et gouvernance/sécurité.
- Interopérabilité multi-moteurs native : BigQuery, Google Cloud Managed Service for Apache Spark et moteurs open source peuvent lire/écrire sur les mêmes tables Iceberg sans copie de données.
- Fédération bidirectionnelle avec Databricks Unity, Snowflake Horizon et AWS Glue via vended credentials et échange de jetons OIDC.
- Intégration avec Knowledge Catalog, combinant recherche full-text et recherche vectorielle natives dans Spanner, avec cohérence ACID transactionnelle entre les index et les données.
- Etsy a migré son catalogue vers cette solution et a observé une accélération de 60 % des requêtes de pipeline.

## Analyse approfondie
À mesure que les clients modernisent leurs architectures vers le lakehouse, ils standardisent sur des formats ouverts tels qu'Apache Iceberg afin de créer un socle de données partagé entre moteurs compatibles. Cela permet de construire des lakehouses "natifs IA" qui transforment la donnée en connaissance sémantique, permettent une action proactive et fonctionnent à l'échelle agentique.

L'un des composants clés d'un lakehouse est le catalogue, et dans l'environnement Apache Iceberg, cela signifie généralement l'Iceberg REST Catalog. Un catalogue Apache Iceberg est responsable de maintenir les pointeurs de table, de gérer les commits atomiques, et de servir de source unique de vérité pour l'emplacement des tables. Mais à mesure que les grandes organisations se modernisent vers les lakehouses, elles ont commencé à réaliser qu'elles avaient besoin d'un catalogue managé hautement scalable et disponible comme composant de leur architecture lakehouse. Cela devient d'autant plus important que l'interrogation des données s'intensifie avec les agents. Pour supporter un grand volume de petites requêtes répétées émises par des agents, il faut s'appuyer sur un catalogue managé qui garantit atomicité, cohérence, disponibilité et concurrence à très grande échelle.

Dans cet article, nous explorons les défis auxquels fait face un catalogue managé dans les environnements cloud modernes à l'échelle des agents, et nous montrons comment le Lakehouse runtime catalog serverless de Google Cloud peut aider à les résoudre. Propulsé par Spanner, la base de données toujours disponible de Google Cloud à l'échelle virtuellement illimitée, et conçu pour respecter la spécification ouverte Iceberg REST catalog, le Lakehouse runtime catalog constitue la fondation hautement scalable et disponible dont vous avez besoin pour l'ère agentique.

### Les défis qu'un catalogue managé doit résoudre dans le Lakehouse

En discutant avec des ingénieurs data et des responsables infrastructure qui exploitent des analytics en production à grande échelle dans un Lakehouse, les points de douleur suivants reviennent systématiquement et doivent être résolus par un catalogue managé :

**Commits atomiques et contrôle de la concurrence :** Iceberg garantit des transactions ACID via un contrôle de concurrence optimiste (OCC). Un catalogue managé doit implémenter une opération de compare-and-swap (CAS) atomique et infaillible pour permuter le pointeur de métadonnées courant.

**Haute disponibilité et maintenance opérationnelle :** Comme les requêtes échouent immédiatement si le catalogue est hors service, un catalogue managé devient un service critique de niveau 1 (Tier-1).

**Scalabilité de la base de données qui sous-tend le catalogue :** Les architectes de catalogue font généralement face à un compromis difficile lors du choix d'une base de données pour les métadonnées et l'état des tables. Les bases de données relationnelles traditionnelles à scale-up offrent SQL et des transactions ACID, mais atteignent des limites verticales de CPU, de mémoire, de stockage et de connexions sous forte charge de lecture/écriture concurrente, sauf à être shardées manuellement, ce qui entraîne une lourde charge opérationnelle ; tandis que les systèmes de bases de données scale-out sont soit à cohérence éventuelle, soit difficiles à gérer, soit non adaptés à l'entreprise, soit les trois à la fois.

**Coordination de la maintenance des tables :** Un catalogue seul n'optimise pas les données ; il faut construire et exploiter des pipelines annexes pour la compaction, l'expiration des snapshots, la réécriture des manifests et le nettoyage des fichiers orphelins.

**Gouvernance et sécurité :** Un catalogue agit comme le gardien de la sécurité. Le catalogue doit implémenter et maintenir :

- Des protocoles d'authentification (par exemple, échange de jetons OAuth2, fédération IAM)
- Un contrôle d'accès jusqu'au niveau du namespace et de la table
- Des identifiants de stockage "vendus" (vended storage credentials) (par exemple, la génération de jetons de courte durée afin que les moteurs de requête n'aient pas besoin d'identifiants de stockage larges et directs)

### Lakehouse runtime catalog

Pour résoudre ces défis, nous avons construit le Lakehouse runtime catalog (GA) avec support pour l'Iceberg REST Catalog. Le Lakehouse runtime catalog est un registre de métadonnées entièrement serverless, hautement disponible et unifié, conçu dès l'origine pour supporter les formats de table ouverts modernes comme Apache Iceberg. En implémentant nativement la spécification Iceberg REST Catalog, le Lakehouse runtime catalog découple la découverte des métadonnées des moteurs de calcul, garantissant que plusieurs moteurs compatibles Iceberg peuvent accéder à un socle de données partagé et vous permettant de mettre vos charges de travail en production plus rapidement. Nous avons aidé de nombreux clients à simplifier la migration de leurs catalogues managés. Par exemple, Etsy a migré son catalogue vers le Lakehouse runtime catalog, en joignant les données sur place pour accélérer les requêtes de pipeline de 60 %.

Cette approche offre un certain nombre de bénéfices architecturaux :

- **API ouvertes :** le support de l'Iceberg REST Catalog permet à différentes équipes d'utiliser leurs outils d'analytics préférés sur un jeu de données unique et unifié.
- **Interopérabilité multi-moteurs :** une fois enregistrées, les tables sont immédiatement découvrables et interrogeables depuis Google Cloud Managed Service for Apache Spark, BigQuery, et des moteurs open source via des interfaces REST standard.
- **Interopérabilité lecture/écriture pour les tables Iceberg :** exploitez des moteurs compatibles Iceberg tels que BigQuery ou Managed Spark pour écrire dans des tables Iceberg enregistrées dans le Lakehouse runtime catalog. Les clients peuvent également utiliser Managed Spark pour écrire dans des tables Iceberg situées dans des catalogues externes.
- **Stockage Iceberg entièrement managé avec des fonctionnalités de niveau entreprise :** utilisez l'infrastructure différenciée de Google pour exécuter des analytics performants sur des tables Iceberg. Cela vous apporte les bénéfices de la flexibilité open source, combinés à la performance, à l'échelle, à la gouvernance et au traitement multimodal.
- **Zéro copie de données :** les définitions de table pointent directement vers vos données existantes dans le magasin d'objets sous-jacent. Vous ne déplacez, ne réécrivez, ni ne dupliquez vos données sous-jacentes.
- **Fédération de catalogue bidirectionnelle entre clouds :** accédez aux données de Databricks Unity, Snowflake Horizon et AWS Glue, avec support des identifiants vendus (vended credentials) et de l'échange de jetons OIDC. Cela vous permet d'apporter Google AI directement sur vos données AWS et Azure.
- **Accès sécurisé via le credential vending :** le catalogue supporte plusieurs mécanismes d'autorisation, vous laissant choisir entre le credential vending et les identifiants d'utilisateur final. Cela signifie que vous pouvez accéder aux tables avec des mécanismes modernes comme le credential vending sans avoir besoin d'un accès direct aux fichiers dans le magasin d'objets sous-jacent (Cloud Storage, AWS S3, Azure Blob Storage).
- **Contexte et gouvernance pilotés par l'IA :** le Lakehouse runtime catalog s'intègre directement avec Knowledge Catalog et Cloud IAM, vous permettant de définir un contexte de confiance pour vos agents, et d'appliquer une sécurité au niveau table de façon cohérente sur tous les moteurs de calcul. Bénéficiez d'une recherche, d'une traçabilité (lineage) et d'insights prêts à l'emploi pour les tables Iceberg du catalogue.
- **Commits atomiques et contrôle de la concurrence, haute disponibilité et scalabilité :** adossé à l'infrastructure à l'échelle planétaire de Google et à Spanner, vous obtenez la disponibilité, la concurrence et l'échelle nécessaires pour que vos métadonnées suivent la croissance de vos données. Le support des buckets Cloud Storage dual-region et multi-region permet des cas d'usage de basculement (failover). Cela apporte également un TCO réduit grâce à un environnement serverless et sans opérations (no-ops), ainsi qu'une scalabilité pour toute taille de charge de travail.

### Qu'est-ce qui propulse le Lakehouse runtime catalog ?

Le Lakehouse runtime catalog est un catalogue hautement disponible, concurrent et scalable, avec de fortes garanties de cohérence car il est construit sur Spanner. Contrairement aux bases de données relationnelles traditionnelles à scale-up qui atteignent des plafonds verticaux mono-nœud, Spanner combine une sémantique SQL relationnelle complète et des transactions ACID multi-tables avec l'élasticité de scale-out horizontal, tant en lecture qu'en écriture, d'un système NoSQL.

Spanner rend le Lakehouse runtime catalog hautement disponible grâce aux configurations régionales de Spanner, avec jusqu'à 99,99 % de disponibilité. Spanner apporte également une scalabilité prête à l'emploi pour le Lakehouse runtime catalog : en tant que base de données scalable horizontalement, Spanner ne nécessite pas de sharding manuel et fait évoluer le calcul et le stockage de façon indépendante et transparente. Spanner surveille dynamiquement le volume de données et la charge de requêtes, en divisant et en redistribuant les plages de données entre les nœuds. Les nœuds de calcul s'adaptent dynamiquement en fonction de l'utilisation CPU et des seuils de stockage. Spanner détecte automatiquement la surcharge au niveau des splits et déplace les splits lourds loin des nœuds surchargés. Spanner permet également aux utilisateurs du Lakehouse runtime catalog d'éliminer le compromis traditionnel entre cohérence relationnelle et scalabilité distribuée, en offrant les garanties de cohérence de pointe du Lakehouse runtime catalog. Les transactions du Lakehouse sont sérialisables — l'ordre des transactions dans la base de données est le même que l'ordre dans lequel les clients observent que ces transactions ont été validées (committed). Cette fondation permet aux utilisateurs du Lakehouse d'opérer à l'échelle des agents.

Puis, pour renforcer davantage les cas d'usage agentiques, le Lakehouse runtime catalog s'intègre directement avec Knowledge Catalog pour découvrir facilement les tables Iceberg du lakehouse et fournir un contexte de confiance aux agents. Knowledge Catalog exploite une combinaison efficace de recherche full-text et de recherche vectorielle native fournies par Spanner ; cette approche permet un meilleur rappel (recall) pour la récupération de recherche, en associant des recherches lexicales par mots-clés à des embeddings sémantiques au sein d'une seule requête. Comme les deux types d'index sont construits sur un jeu de données de base identique, ils se mettent à jour avec une cohérence ACID stricte et transactionnelle en parallèle des opérations DML sur la table de base. Cela supprime la charge opérationnelle liée à la gestion de pipelines de synchronisation et de systèmes externes de recherche vectorielle et full-text. En somme, le Lakehouse runtime catalog offre un délai de mise sur le marché plus rapide pour vos cas d'usage agentiques.

### Combiner charges analytiques et opérationnelles

Avec le Lakehouse sans frontières de Google Cloud, basé sur Apache Iceberg, vous pouvez combiner vos données analytiques avec vos charges de travail opérationnelles. Les cas d'usage vont de la combinaison d'actifs de données issus de votre Lakehouse avec des données OLTP (issues de Spanner) pour l'analytics, à des applications de service à faible latence où vos actifs Lakehouse sont accessibles dans une base de données opérationnelle comme Spanner, jusqu'à l'analytics conversationnelle dans des agents propriétaires et tiers.

Ci-dessous, à titre d'exemple, vous pouvez voir le Lakehouse runtime catalog avec Spanner en action. Ici, nous combinons des données analytiques pour des trajets de taxi à Manhattan (adossées à Apache Iceberg) avec des données opérationnelles pour les zones de taxi dans Spanner, afin de trouver les itinéraires de circulation les plus congestionnés. L'exemple montre également que vous pouvez utiliser un agent d'analytics conversationnelle pour accéder aux mêmes données et obtenir des insights de second ordre.

### Moderniser vers le Lakehouse sans frontières

Se moderniser vers le Lakehouse de Google Cloud minimise les silos de données entre moteurs d'analytics et agents, unifie la gouvernance multi-moteurs, fournit un contexte de confiance à vos agents et réduit considérablement le TCO opérationnel. S'appuyer sur le Lakehouse runtime catalog basé sur Spanner aide à préparer vos environnements cloud modernes à opérer à l'échelle des agents.

## Pourquoi ça compte
Ce lancement illustre la convergence entre infrastructure de données transactionnelle (Spanner) et architectures lakehouse ouvertes (Iceberg), un signal fort pour la veille sur la préparation des stocks de données à l'usage intensif par des agents IA et sur la bataille d'interopérabilité entre catalogues (Unity, Glue, Snowflake Horizon, Google).
