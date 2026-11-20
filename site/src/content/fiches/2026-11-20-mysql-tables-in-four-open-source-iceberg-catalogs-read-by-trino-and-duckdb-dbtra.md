---
title: "MySQL tables in four open source Iceberg catalogs, read by Trino and DuckDB - dbtrail"
date: 2026-11-20
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fblog.dbtrail.com%2Fmysql-tables-in-four-open-source-iceberg-catalogs-read-by-trino-and-duckdb%2F%3Futm_source=tldrdata/1/010001a1f382eb1c-813c2c29-0e67-4fcb-a679-689a5eec2cc8-000000/CE35BkAGkeyVHQubB9a_hFYAKiPBLgyGr2M_hg_YebQ=452"
keywords: ["Iceberg", "catalogue de données", "MySQL", "Trino", "DuckDB", "export incrémental"]
theme: "Data"
tone: "research"
used_in: ["2026-11-20"]
---

## Résumé
DBTrail est un outil qui copie en continu des tables MySQL vers un catalogue Iceberg afin qu'elles puissent être interrogées, jointes et tenues à jour aux côtés d'autres sources de données. L'équipe de dbtrail a testé l'export DBTrail 0.133.0 sur quatre catalogues REST Iceberg open source (Nessie, LakeKeeper, Apache Polaris, Apache Gravitino), lus ensuite par Trino 484 et DuckDB 2.0, en comparant systématiquement les résultats à ceux de MySQL. Nessie et LakeKeeper (signature distante désactivée) ont fonctionné immédiatement ; Polaris et Gravitino ont nécessité des changements de configuration ou des correctifs à venir dans DBTrail pour gérer la délégation de credentials de stockage. Une jointure avec un CSV externe simulant un CRM a produit des résultats identiques sur les quatre catalogues et les deux moteurs de requête.

## Points clés
- DBTrail exporte les tables MySQL vers un catalogue Iceberg sous forme de copies nommées (`shop.orders`, `shop.customers`), interrogeables par tout moteur compatible Iceberg.
- Sur 5 568 commandes et 200 clients, les cinq métriques comparées (nombre de lignes, somme exacte, id max, commandes payées, jointure CRM) correspondaient à l'identique entre MySQL, Trino et DuckDB, sur les quatre catalogues testés.
- Project Nessie et LakeKeeper (avec la signature distante S3 désactivée) fonctionnent sans modification ; Apache Polaris et Apache Gravitino ont échoué par défaut à cause de la délégation de credentials de stockage (STS) et nécessitent des correctifs prévus dans la prochaine version de DBTrail (`--catalog-scope`, `--catalog-access-delegation none`).
- PyIceberg ne peut pas encore lire les tables après un export incrémental car il ne supporte pas les « equality deletes » Iceberg utilisées par DBTrail pour représenter les mises à jour et suppressions.
- Unity Catalog OSS n'a pas pu être testé faute de configuration de bucket S3 côté serveur ; plusieurs scénarios (vraie délégation STS via rôle IAM, Spark, authentification, hôtes distants) restent non testés.
- L'export est incrémental et sans état externe : la position de lecture du binlog est stockée dans les propriétés de la table Iceberg elle-même, dans le même commit que les données.

## Analyse approfondie
Une équipe qui veut savoir quel chiffre d'affaires provient de chaque segment de clientèle a besoin de deux choses qui vivent à des endroits différents : les commandes, dans MySQL, et les segments, dans l'outil qu'utilise l'équipe commerciale. Quelqu'un exporte généralement les deux à la main dans une seule base de données, ou construit un pipeline qu'il faut ensuite maintenir.

Si votre entreprise exploite déjà un catalogue Iceberg, DBTrail peut y placer les tables MySQL. Il conserve une copie de vos tables MySQL sous forme de tables Iceberg et les enregistre dans ce catalogue sous leurs propres noms, `shop.orders`, `shop.customers`. Tout moteur qui lit le catalogue peut ensuite les interroger par leur nom et les joindre aux autres tables qui y sont enregistrées. Quand MySQL change, l'export suivant n'ajoute que ce qui a changé.

Nous avons testé cela avec quatre catalogues REST Iceberg open source et deux moteurs de requête, Trino et DuckDB, et comparé chaque réponse avec la même requête sur MySQL.

### Ce que nous avons testé

Un serveur MySQL 8.4 avec une petite boutique : 200 clients et environ 5 000 à 6 000 commandes, avec un script écrivant environ neuf instructions par seconde (moitié d'insertions, le reste de mises à jour et de suppressions). DBTrail 0.133.0 a suivi le binlog, puis exporté vers chaque catalogue deux fois : un premier chargement, puis, après 40 secondes d'écritures supplémentaires, un export incrémental portant les insertions, mises à jour et suppressions.

Chaque moteur a ensuite lu les tables par leur nom via le catalogue, les écritures étant arrêtées, et nous avons comparé le nombre de lignes, la somme exacte de la colonne `amount`, l'id le plus élevé et le nombre de commandes payées avec la même requête sur MySQL.

| Catalogue | DBTrail 0.133.0 | Trino 484 | DuckDB 2.0.0 | Jointure CRM |
|---|---|---|---|---|
| Project Nessie 0.110.0 | fonctionne tel quel | Correspond | Correspond | Correspond |
| LakeKeeper 0.15.1 | fonctionne avec la signature distante désactivée | Correspond | Correspond | Correspond |
| Apache Polaris 1.9.0 | a refusé avec son stockage réglé sur « no STS » ; fonctionne avec deux changements prévus dans la prochaine version | Correspond | Correspond | Correspond |
| Apache Gravitino 1.3.0 | a refusé ; fonctionne avec un changement prévu dans la prochaine version | Correspond | Correspond | Correspond |

« Correspond » signifie que chacun des cinq nombres correspondait, après l'export incrémental.

### L'export

La commande d'export avec Nessie, qui n'a demandé aucune option supplémentaire :

```
bintrail export iceberg
  --index-dsn "root:...@tcp(127.0.0.1:3307)/bintrail_index"
  --baseline-dir /opt/rig/baselines
  --catalog rest
  --catalog-uri http://localhost:19120/iceberg
  --catalog-warehouse dbtrail
  --warehouse s3://<bucket>/iceberg/nessie
  --format json
```

La deuxième exécution, après 40 secondes d'écritures, a pris 0,8 seconde :

```
"table": "customers", "verdict": "unchanged", "detail": "no events since the cursor"
"table": "orders",    "verdict": "exported",  "detail": "374 events folded into 333 upserts and 31 deletes"
```

Exécutez la même ligne depuis cron, ou ajoutez `--every 15m` et laissez-la tourner. Chaque exécution ne lit que les changements depuis la précédente. La position atteinte par chaque table est stockée dans les propriétés propres de la table, dans le même commit que les données, si bien que l'export ne conserve aucune progression propre en dehors du catalogue.

### Lire les tables par leur nom

Trino, avec le connecteur Iceberg standard pointé vers le catalogue :

```
connector.name=iceberg
iceberg.catalog.type=rest
iceberg.rest-catalog.uri=http://localhost:19120/iceberg
iceberg.rest-catalog.warehouse=dbtrail
fs.native-s3.enabled=true
s3.region=us-east-1
```

```sql
SELECT count(*), sum(amount), max(id), count_if(status = 'paid'),
       (SELECT count(*) FROM shop.customers)
FROM shop.orders;
```

`"5568","1395471.20","5695","1290","200"`

DuckDB 2.0, en attachant le même catalogue :

```sql
INSTALL iceberg; LOAD iceberg; INSTALL httpfs; LOAD httpfs; INSTALL aws; LOAD aws;
CREATE SECRET s3c (TYPE s3, PROVIDER credential_chain, REGION 'us-east-1');
ATTACH 'dbtrail' AS c (TYPE iceberg, URI 'http://localhost:19120/iceberg',
                       AUTHORIZATION_TYPE 'none', ACCESS_DELEGATION_MODE 'none');
SELECT count(*), sum(amount), max(id), count(*) FILTER (WHERE status = 'paid')
FROM c.shop.orders;
```

`5568 | 1395471.20 | 5695 | 1290`

MySQL, au même instant :

`{"orders_count": 5568, "orders_sum_amount": "1395471.20", "orders_max_id": 5695, "orders_paid": 1290}`

Deux détails concernant DuckDB. La lecture échouait avec `HTTP 403 ... No credentials are provided` jusqu'à ce que nous réglions `ACCESS_DELEGATION_MODE 'none'`, car le catalogue ne distribue aucune credential de stockage, même avec un secret S3 en place. Et chaque requête ici lit la colonne clé (`max(id)` ci-dessus le fait) : la documentation de l'export explique que les anciennes versions de DuckDB en ont besoin pour appliquer les suppressions d'un export incrémental. Nous n'avons pas vérifié si la 2.0 en a toujours besoin.

### La jointure

Pour représenter des données provenant d'un autre système, nous avons pris un CSV avec une ligne par client (`customer_id, segment, account_manager`) et l'avons enregistré dans le même catalogue sous le nom `crm.customer_segments`, avec PyIceberg :

```python
cat = load_catalog("rig", type="rest", uri="http://localhost:19120/iceberg", warehouse="dbtrail")
cat.create_namespace("crm")
t = cat.create_table("crm.customer_segments", schema=tbl.schema)
t.append(tbl)   # 200 rows from the CSV
```

Chiffre d'affaires par segment, avec les commandes issues de MySQL et les segments issus du CSV :

```sql
SELECT s.segment, count(*) AS paid_orders, sum(o.amount) AS revenue
FROM shop.orders o
JOIN crm.customer_segments s ON s.customer_id = o.customer_id
WHERE o.status = 'paid'
GROUP BY s.segment
ORDER BY revenue DESC;
```

Trino :

```
"self-serve","343","87947.70"
"mid-market","343","84817.69"
"smb","314","77131.70"
"enterprise","290","73062.86"
```

DuckDB a renvoyé les quatre mêmes lignes, et MySQL, en joignant ses propres tables avec la même règle de segmentation, a renvoyé les quatre mêmes lignes. Nous avons répété cela sur les quatre catalogues ; chaque fois, les trois réponses étaient identiques.

### Catalogue par catalogue

**Project Nessie 0.110.0** a fonctionné avec la version telle quelle. Nessie choisit lui-même l'emplacement de ses tables sous le warehouse (il ajoute un suffixe tel que `orders_01f46bad-...`), ce qui ne change rien pour les lecteurs.

**LakeKeeper 0.15.1.** Un warehouse sur S3 sans STS bascule par défaut sur la signature distante (« remote signing ») : le catalogue indique au client d'envoyer chaque requête S3 au catalogue pour qu'elle soit signée. La bibliothèque Iceberg sur laquelle DBTrail est construit ne sait pas faire cela, et la première exécution s'est arrêtée avec :

```
failed to load metadata file at s3://.../orders/metadata/00000-....gz.metadata.json:
remote S3 request signing is not supported
```

Avec la signature distante désactivée pour le warehouse (`"remote-signing-enabled": false` dans son profil de stockage), l'export a utilisé les propres credentials AWS de la machine et tout correspondait. Les deux tables vides créées par l'exécution échouée ont été chargées par l'exécution suivante sans aucune étape manuelle.

**Apache Polaris 1.9.0** a nécessité deux changements dans DBTrail. D'abord, la connexion avec une credential client a échoué :

`invalid_scope: The scope is invalid`

DBTrail demande le scope OAuth `catalog`, alors que Polaris veut `PRINCIPAL_ROLE:ALL`. Avec la 0.133.0, vous pouvez récupérer vous-même un token avec ce scope et le passer dans `BINTRAIL_ICEBERG_CATALOG_TOKEN`, et la connexion fonctionne. Mais le token expire après une heure et rien ne le renouvelle, ce qui est un problème pour un export qui s'exécute toutes les quelques minutes. Un changement prévu dans la prochaine version ajoute `--catalog-scope` (dbtrail/dbtrail#2928), avec lequel la credential se connecte et se renouvelle automatiquement :

```
export BINTRAIL_ICEBERG_CATALOG_CREDENTIAL='<client_id>:<client_secret>'
bintrail export iceberg ... --catalog rest
  --catalog-uri http://localhost:8182/api/catalog --catalog-warehouse dbtrail
  --catalog-scope PRINCIPAL_ROLE:ALL
```

Ensuite, DBTrail demande au catalogue des credentials de stockage temporaires à chaque requête. En production, Polaris les obtient en assumant un rôle IAM que vous lui donnez. Nous n'avons pas configuré de rôle IAM pour ce test, nous avons donc essayé deux autres configurations. Avec une option de Polaris réservée au développement (`SKIP_CREDENTIAL_SUBSCOPING_INDIRECTION`, qui distribue les propres credentials du serveur à chaque client, et dont Polaris avertit au démarrage), la 0.133.0 avec le token fait à la main a exporté et chaque vérification correspondait. Ce n'est pas ainsi qu'on exploiterait Polaris, donc nous ne le comptons pas. Avec le stockage réglé sur « no STS available », la configuration la plus proche de la production sans rôle, Polaris a refusé la table :

`Credential vending was requested for table shop.orders, but no credentials are available`

**Apache Gravitino 1.3.0**, son serveur REST Iceberg autonome sans fournisseur de credentials configuré, a refusé pour la même raison :

`No credential provider found for path s3://.../gravitino/shop/orders with scheme s3`

Nous avons envoyé la même requête de création à la main : avec l'en-tête « please vend credentials », Gravitino répondait 400, et sans lui, 200. Un second changement, également prévu dans la prochaine version, ajoute `--catalog-access-delegation none` (dbtrail/dbtrail#2932), qui arrête de demander, si bien que les fichiers sont écrits avec les propres credentials de la machine. Avec lui, Gravitino et Polaris en « no STS available » (connexion avec la credential et `--catalog-scope`) ont passé toutes les vérifications ci-dessus. Un Polaris qui assume un vrai rôle IAM et distribue des credentials devrait fonctionner avec la 0.133.0 plus un token, mais nous ne l'avons pas testé. Un réglage de Gravitino à surveiller : les paramètres du conteneur sont des variables `GRAVITINO_ICEBERG_REST_*`, et avec de mauvais noms, il conservait silencieusement un warehouse par défaut dans `/tmp` à l'intérieur du conteneur.

**Unity Catalog OSS**, nous n'avons essayé que brièvement. Son endpoint Iceberg ne créait pas d'espace de noms (404), et la création de table répondait `S3 bucket configuration not found.` : pour une table S3, il veut que le bucket soit configuré dans sa configuration serveur avec une clé d'accès ou un rôle IAM à distribuer, et nous n'avions ni l'un ni l'autre. Nous nous sommes arrêtés là, donc ce n'est pas dans le tableau ci-dessus.

### Ce qui n'a pas fonctionné, et ce que nous n'avons pas testé

- **PyIceberg ne peut pas lire les tables après un export incrémental.** Il s'arrête avec `PyIceberg does not yet support equality deletes`. DBTrail enregistre une mise à jour ou une suppression comme une equality delete Iceberg, et PyIceberg ne les lit pas encore. Il a enregistré la table CRM sans problème. Trino et DuckDB lisent tout.
- **PyIceberg n'a pas pu communiquer avec notre Gravitino** (`NotAuthorizedException`), nous avons donc enregistré la table CRM avec Trino à la place sur Gravitino (`CREATE TABLE crm.customer_segments AS ...`). Nous n'avons pas creusé la question.
- **La signature distante** (le réglage par défaut de LakeKeeper) ne fonctionne pas avec DBTrail ; désactivez-la pour le warehouse.
- **Non testé** : Polaris ou LakeKeeper avec une vraie distribution de credentials via STS (cela nécessite un rôle IAM, que nous n'avons pas configuré), Spark, l'authentification sur LakeKeeper, Nessie et Gravitino (ils tournaient en accès libre, sur la même machine), des catalogues sur une autre machine en https, et des exécutions longues selon un calendrier à travers ces catalogues.
- Chaque catalogue ici tournait avec un backend en mémoire ou en conteneur unique. Une configuration de production utiliserait un stockage persistant.

### Essayez-le

L'export est disponible dans la version actuelle de DBTrail, avec `--catalog rest` pour n'importe quel catalogue REST Iceberg et `--catalog glue` pour AWS Glue. La référence complète, incluant les options d'authentification, se trouve dans la documentation de l'export Iceberg. Les deux options décrites ci-dessus, `--catalog-scope` et `--catalog-access-delegation`, sont fusionnées et arrivent dans la prochaine version.

## Pourquoi ça compte
Ce billet documente, avec des chiffres vérifiés, l'état réel de l'interopérabilité entre MySQL et l'écosystème Iceberg via quatre implémentations de catalogue REST concurrentes — une information précieuse pour quiconque évalue une architecture lakehouse ouverte plutôt qu'un catalogue propriétaire unique. Il met aussi en lumière un angle mort récurrent de l'écosystem Iceberg (la délégation de credentials de stockage et le support partiel des equality deletes dans PyIceberg) que les équipes data doivent anticiper avant d'adopter ces outils en production.
