---
title: "[FREE] A file format claims to be 100x faster than Parquet"
date: 2026-10-27
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fvutr.substack.com%2Fp%2Ffree-a-file-format-claims-to-be-100x%3Futm_source=tldrdata/1/010001a177b312eb-e5823126-cfe6-4c86-8941-97d3b5c4bf0c-000000/wxttDigaVqvHEfOsdm6BR7yfg7h3zEcM6MjjygqxlcA=452"
authors: ["Vu Trinh"]
keywords: ["formats de fichiers", "stockage colonnaire", "Parquet", "Lance", "accès aléatoire", "IA"]
theme: "Data"
tone: "tutorial"
used_in: ["2026-10-27"]
---

## Résumé
L'article compare Parquet, format colonnaire de référence pour les données tabulaires, au format Lance, conçu pour les charges de travail IA/ML nécessitant un accès aléatoire rapide (recherche sémantique, embeddings vectoriels, images). L'auteur explique que Parquet, optimisé pour les scans séquentiels, souffre de limites structurelles (pages trop grosses à décoder, métadonnées non indexables, row groups contraignant la mémoire) lorsqu'il s'agit de récupérer seulement quelques lignes. Lance répond à ces limites en abandonnant le concept de row group, en introduisant deux modes d'encodage de page (mini-block pour les petites valeurs, full-zip pour les grandes), et en rendant les métadonnées de colonnes directement adressables.

## Points clés
- Parquet organise les données en row groups puis en chunks de colonnes composés de pages ; la page est la plus petite unité lisible, ce qui pénalise la lecture d'une seule ligne.
- Les métadonnées Parquet (FileMetadata, encodées en Thrift/Protobuf) doivent être désérialisées entièrement, même pour accéder au schéma d'une seule colonne — coûteux avec des tables à des milliers de colonnes (cas fréquent en ML).
- Le row group impose de bufferiser tout le groupe en mémoire avant écriture, ce qui cause des out-of-memory avec des colonnes à grandes valeurs (ex. embeddings), et oblige toutes les colonnes d'un même groupe à avoir le même nombre de lignes.
- Lance supprime le row group : chaque colonne est découpée en pages indépendantes (par défaut 8 Mo), référencées par offset absolu, ce qui permet un découpage mémoire et un parallélisme de lecture flexibles, à n'importe quelle frontière de ligne.
- Lance utilise un encodage mini-block (chunks ~4-8 KiB) pour les petites valeurs et full-zip (encodage transparent, métadonnée collée à la donnée) pour les grandes valeurs comme les embeddings, permettant de décompresser une seule valeur sans toucher aux voisines.
- Chaque colonne a son propre message protobuf de métadonnées, rendant l'accès au schéma en O(1) sans décodage des autres colonnes — contrairement à Parquet.

## Analyse approfondie
L'article part d'un constat : les charges de travail en ingénierie des données ont évolué, passant de données tabulaires destinées à des scans séquentiels à des données multimodales (embeddings vectoriels, images, documents) nécessitant un accès aléatoire — typiquement lors d'une recherche sémantique où le système ne récupère qu'un petit nombre de lignes.

L'auteur détaille d'abord l'architecture interne de Parquet (layout PAX hybride : row groups horizontaux puis chunks de colonnes composés de pages), en soulignant trois limites critiques pour l'accès aléatoire :
1. La page comme plus petite unité de lecture, impliquant le décodage complet d'une page pour en extraire une seule ligne, donc une latence croissante avec la taille de page.
2. Les métadonnées de fichier (FileMetadata) sérialisées en Thrift/Protobuf, non adressables de façon aléatoire : il faut tout désérialiser même pour une seule colonne, un problème amplifié dans les tables ML à dizaines de milliers de colonnes.
3. La contrainte du row group, qui lie l'unité logique à l'unité physique d'I/O, forçant à bufferiser tout un groupe en mémoire (risque d'OOM avec de grosses valeurs) et à aligner le nombre de lignes de toutes les colonnes d'un groupe sur la colonne la plus volumineuse — générant potentiellement de nombreux petits row groups, donc plus de métadonnées, plus de lectures non contiguës et une compression moins efficace.

L'article présente ensuite Lance, un format colonnaire open source créé vers 2022 par LanceDB (issu du YC W22) pour répondre à ces limites dans le contexte IA/multimodal. Sa spécification se structure en quatre zones : les pages de données (référencées par offset absolu), les métadonnées de colonnes (messages protobuf individuels avec table d'offsets), puis un tableau d'offsets et un footer en fin de fichier.

Sur le plan du layout de page, Lance distingue deux stratégies selon la taille des valeurs : l'encodage mini-block pour les petites valeurs (chunks de 4-8 KiB, jusqu'à 4096 valeurs), plus rapide à décoder que les grosses pages Parquet car plus petit ; et l'encodage full-zip pour les grandes valeurs (embeddings, images, texte long, seuil à 256 octets), qui entrelace métadonnée et donnée pour chaque valeur et n'autorise que des encodages « transparents » — décodables valeur par valeur sans dépendance aux voisines (ex. dictionnaire), à l'inverse des encodages « opaques » comme le delta, qui économisent de l'espace mais nécessitent de décoder toute la séquence précédente. Le mini-block peut utiliser des encodages opaques, le full-zip non.

La décision la plus structurante est l'abandon total du row group : les données d'une colonne sont réparties sur des pages de 8 Mo par défaut, référencées par offset absolu, sans besoin de contiguïté. Cela permet au writer d'utiliser un buffer séparé par colonne plutôt que de bufferiser tout un row group, et fait que le nombre de pages par colonne suit simplement sa taille réelle de données (l'article illustre avec un fichier d'un million de lignes : une colonne booléenne tient dans une seule page, une colonne d'embeddings de 3 KiB nécessite environ 384 pages). Côté lecture, cette liberté se traduit par un parallélisme à la granularité de la ligne plutôt que du row group : deux threads peuvent se partager un fichier de deux millions de lignes à n'importe quelle frontière, chaque page enregistrant la ligne de départ et mappant toute plage de lignes à une plage d'octets.

Enfin, comme chaque colonne a son propre message protobuf, le schéma d'une colonne donnée est accessible directement, sans décodage des métadonnées des autres colonnes — contrairement à Parquet.

L'article cite ses sources : le papier Lance (Pace, She, Xu, Jones, Lockett, Wang, Shah, 2025) sur l'encodage structurel adaptatif, la spec Lance v2 (2024), et un article de Julien Le Dem sur le stockage colonnaire à l'ère de l'IA. Un commentaire additionnel souligne un point pratique : sur S3, le coût par requête devient souvent plus déterminant que le décodage de page, la latence médiane des petites requêtes GET se comptant en dizaines de millisecondes — ce qui signifie qu'un top-50 après une recherche vectorielle peut se traduire par 50 lectures distinctes à moins de trier les identifiants de lignes et de fusionner celles qui tombent dans la même page.

## Pourquoi ça compte
Ce document éclaire une tension de fond dans l'écosystème data/IA actuel : les formats colonnaires historiques (Parquet), pensés pour l'analytique en scan séquentiel, montrent leurs limites face aux besoins d'accès aléatoire des charges IA (vector search, embeddings), ce qui motive l'émergence de formats dédiés comme Lance — un signal à suivre pour quiconque conçoit des pipelines de données pour le ML.
