---
title: "A DuckDB Database with No Data in It"
date: 2026-10-14
url: "https://elink56e.dataelixir.com/ss/c/u001.LZK0q19HeV0JD0zsDmsEEW3G-hlPAiJGlzQ0h6QLitBsLSxiOdAylveqoRk0pnDSZ258oL2O2PcKauRA_6A4SA3PMVtqPAxms_BDCJlLFrIEqclg37TNmMhJVep52gdNQJKD_vP49mPjzAzAN5y_32INPJpbCBQPDAPe4qX1MOusOrEHKRwxPHaN9hfwVUoDHovUAuDzxz0yAuTdGDzKjQ/4uu/18J8Mw0nQ4mlJCapgH3IAQ/h4/h001.9ydIUfQfx5T020HfVmXuBCoX0PCI3NZQ2q4Xq-3keaw"
keywords: ["DuckDB", "catalogue de données", "Parquet", "data lake", "stockage objet", "vues SQL"]
theme: "Data"
tone: "tutorial"
used_in: ["2026-10-14"]
---

## Résumé

Cet article montre qu'un fichier DuckDB peut ne contenir aucune donnée, uniquement des définitions de vues pointant vers des fichiers Parquet hébergés sur du stockage objet. Il devient ainsi un catalogue léger (quelques centaines de kilooctets) qui expose un ensemble de relations nommées et interrogeables, tout en laissant les données réelles dans leur emplacement d'origine. À travers l'exemple du jeu de données des trains néerlandais, l'article détaille comment créer ce catalogue, l'héberger sur un bucket S3 ou un endpoint HTTPS, et le partager en lecture seule via une seule URL. Il montre aussi comment les vues permettent de faire évoluer la structure des fichiers sous-jacents (repartitionnement, renommage de colonnes) sans jamais casser les requêtes des consommateurs.

## Points clés

- Un fichier DuckDB peut être composé uniquement de vues, sans aucune donnée propre, et rester minuscule quelle que soit la taille des données référencées.
- Les vues DuckDB stockent le texte d'une requête (par exemple la lecture d'un fichier Parquet distant via l'extension httpfs) et non des lignes, ce qui en fait un catalogue ou une couche sémantique au-dessus d'un data lake.
- Partager un tel catalogue revient à partager une seule URL, attachable en lecture seule (`ATTACH ... (READ_ONLY)`), plutôt qu'une liste de chemins de fichiers.
- DuckDB ne lit que les colonnes et row groups nécessaires à une requête, donc les requêtes filtrées ou agrégées sur de gros volumes distants restent efficaces et ne téléchargent pas tout le fichier.
- Les vues découplent la requête du stockage physique : repartitionnement des fichiers, renommage de colonnes ou déplacement vers un nouveau bucket peuvent se faire en modifiant uniquement le catalogue, sans casser les requêtes des consommateurs.
- Limites : il faut un accès réseau au catalogue et à chaque source de données référencée, l'écriture est impossible en HTTPS/S3 (il faut remplacer le fichier via une copie locale), et la performance dépend du réseau et de l'organisation des fichiers.

## Analyse approfondie

# Une base de données DuckDB sans aucune donnée

*TL;DR : Un fichier de base de données DuckDB n'est pas obligé de contenir des données. Il peut ne stocker que des définitions de vues qui pointent vers des fichiers Parquet sur du stockage objet, de sorte que quelques centaines de kilooctets se comportent comme un catalogue partagé sur tout un data lake. Cet article montre comment en construire un, l'héberger, et s'y connecter en lecture seule.*

Un fichier de base de données DuckDB n'est pas obligé de contenir des données. Il peut ne stocker que des définitions de vues qui pointent vers des fichiers situés ailleurs, comme des fichiers Parquet sur du stockage objet. Le fichier reste de quelques centaines de kilooctets, quelle que soit la taille des données qu'il décrit, et toute personne qui l'attache voit un ensemble de relations nommées, prêtes à être interrogées.

Nikolas Goebel a décrit cette idée dans *DuckDB doesn't need data*, où il soutient que les bases de données modernes ont séparé l'endroit où les données sont stockées de la manière dont elles sont lues, au point que la plupart des bases de données n'ont plus besoin de détenir leurs propres données. Dans cette perspective, DuckDB devient un navigateur pour le cloud de données, où l'on accède à un jeu de données via une URL plutôt que via une copie sur son propre disque.

Dans cet article, nous transformons cette idée en un petit catalogue partageable.

Une table DuckDB stocke ses lignes à l'intérieur du fichier de base de données. Une vue, elle, ne stocke que le texte d'une requête. Lorsqu'on lit la vue, DuckDB exécute cette requête et renvoie le résultat courant. Si la requête lit un fichier Parquet distant, les données résident dans le stockage objet et la vue ne contient que l'instruction indiquant comment les lire.

Un fichier de base de données entièrement constitué de telles vues ne contient aucune ligne qui lui soit propre. C'est un catalogue : un ensemble de relations nommées, prêtes à être interrogées, construites sur des données qui restent dans leur emplacement et leur format d'origine. On peut publier ce catalogue comme une couche sémantique organisée au-dessus d'un data lake, où les définitions de vues encodent les jointures, les filtres et les noms de colonnes que les consommateurs doivent utiliser, sans copier ni déplacer les données sous-jacentes.

Les exemples utilisent le jeu de données public des services ferroviaires de DuckDB, qui enregistre une ligne pour chaque arrêt effectué par un train des chemins de fer néerlandais. Les données proviennent des jeux de données ouverts publiés par l'application Rijden de Treinen (« Les trains circulent-ils ? »), et on peut les lire directement depuis leur URL.

Commencez par installer l'extension `httpfs` afin que DuckDB puisse lire des données via le réseau. Cette opération n'a besoin d'être effectuée qu'une seule fois.

```
INSTALL httpfs;
```

Créez ensuite un fichier de base de données persistant et définissez une vue sur les données distantes. Utilisez un emplacement totalement qualifié, une URL distante ou un chemin absolu, afin que la vue se résolve correctement quel que soit le répertoire de travail du client.

```
ATTACH 'rail_catalog.duckdb' AS rail;
USE rail;
CREATE VIEW services AS
    SELECT *
    FROM 'https://blobs.duckdb.org/train_services.parquet';
```

Le catalogue expose désormais une relation `services` qui lit le fichier distant chaque fois qu'elle est interrogée.

```
SELECT departure_time, station_name, type
FROM rail.services
LIMIT 3;
```

| departure_time | station_name | type |
|---|---|---|
| 2023-05-15 00:00:00 | Rotterdam Centraal | Intercity |
| 2023-05-15 00:13:00 | Delft | Intercity |
| 2023-05-15 00:29:00 | Den Haag HS | Intercity |

Comme le fichier ne stocke que la définition de la vue, il reste petit, quelle que soit la croissance du jeu de données référencé. Le fichier `train_services.parquet` contient 380 959 lignes, et pourtant le catalogue qui le lit ne pèse que quelques centaines de kilooctets.

Téléversez `rail_catalog.duckdb` vers n'importe quel emplacement que DuckDB peut lire via le réseau, par exemple un bucket `s3://` ou un point de terminaison `https://`. Le bucket qui héberge déjà les fichiers Parquet est un endroit pratique pour le placer.

Partager le catalogue revient alors à partager une seule URL plutôt qu'une liste de chemins de fichiers individuels. Le destinataire n'a pas besoin de savoir combien de fichiers alimentent chaque vue ni où ils sont stockés, seulement l'adresse du catalogue.

Les consommateurs attachent le catalogue en lecture seule et interrogent les vues comme s'il s'agissait de tables locales. Chaque requête lit les données courantes dans les fichiers référencés, si bien que le résultat reflète ce qui se trouve dans le stockage objet à cet instant précis.

```
ATTACH 'https://example.com/rail_catalog.duckdb' AS rail (READ_ONLY);
SELECT station_name, count(*) AS calls
FROM rail.services
GROUP BY station_name
ORDER BY calls DESC
LIMIT 3;
```

| station_name | calls |
|---|---|
| Utrecht Centraal | 7663 |
| Amsterdam Centraal | 7591 |
| Zwolle | 5013 |

Les consommateurs ont besoin de l'extension `httpfs` et, pour les sources `s3://`, d'identifiants donnant accès aux données sous-jacentes. DuckDB ne lit que les colonnes et les groupes de lignes nécessaires à une requête, de sorte qu'une requête filtrée ou agrégée sur un grand jeu de données distant ne télécharge pas l'intégralité du fichier.

Comme une requête lit la vue plutôt que les fichiers directement, l'éditeur peut modifier les fichiers sans changer la requête. Le consommateur exécute la même requête avant et après.

Supposons que le fichier Parquet unique devienne trop volumineux et que l'éditeur le découpe en un fichier par année. Mettre à jour la vue pour lire un répertoire de fichiers ne représente qu'une modification d'une seule ligne dans le catalogue, et les consommateurs ne remarquent rien.

```
CREATE OR REPLACE VIEW services AS
    SELECT *
    FROM read_parquet('s3://my-bucket/rail/services/year=*/*.parquet');
```

Une vue peut aussi maintenir le schéma stable lorsque les fichiers changent. Si un lot de fichiers ultérieur renomme `station_name` en `station`, la vue peut faire correspondre la nouvelle colonne au nom que les consommateurs utilisent déjà.

```
CREATE OR REPLACE VIEW services AS
    SELECT
        * EXCLUDE (station),
        station AS station_name
    FROM read_parquet('s3://my-bucket/rail/services/*.parquet');
```

Si vous repartitionnez les fichiers ou les déplacez vers un nouveau bucket, il suffit de mettre à jour le catalogue. Quiconque l'interroge continue d'exécuter les mêmes requêtes qu'avant.

Utilisez ce schéma lorsque vous voulez partager un jeu de données sans envoyer au destinataire une longue liste de chemins de fichiers individuels, et lorsque les données sont déjà dans un format que DuckDB lit bien, comme Parquet. Les lecteurs obtiennent un ensemble de relations nommées à interroger, et l'éditeur peut modifier l'organisation des fichiers sans casser ces requêtes.

Notez les limitations suivantes :

- Les consommateurs doivent pouvoir accéder à la fois au fichier catalogue et à chacune des sources de données que ses vues référencent.
- Les connexions via HTTPS et l'API S3 sont en lecture seule, donc le catalogue ne peut pas être modifié en place. Pour changer une vue, il faut modifier une copie locale puis la téléverser à nouveau.
- La performance des requêtes dépend du réseau et de l'organisation des fichiers référencés. Les conseils pour interroger des fichiers distants s'appliquent ici aussi.

Un fichier DuckDB qui ne contient que des vues est un petit catalogue que l'on peut partager sous la forme d'une seule URL. Les données restent dans leur emplacement d'origine, l'éditeur peut modifier la façon dont elles sont stockées, et le lecteur dispose d'un ensemble stable de relations à interroger.

Pour la référence complète, consultez le guide *Share a DuckDB Database That Only Stores Views*.

## Pourquoi ça compte

Ce pattern illustre une approche légère et peu coûteuse pour construire une couche sémantique ou un catalogue partagé sur un data lake sans dupliquer les données, un point utile en veille pour les équipes data qui cherchent à simplifier le partage d'accès à des jeux de données Parquet sur S3 ou HTTPS tout en gardant la gouvernance du schéma côté éditeur.
