---
title: "Pandas Should Go Extinct"
date: 2026-09-16
url: "https://elink56e.dataelixir.com/ss/c/u001.KRh8DuNyfDEy09i_fq1PgVZF1WoBUwF7vgTTCuKnQuIyJVbPPiLrXdrgXxBHIJya-zDYLzIQyiBsKva3e5-dNYBubbgOI3O6JkcPFn2phHG1igqpW8OUx3lTjqNG0sCNzH92Q78M-sDYzTLpynQFvO_V0CDtOKw_uRVV88cfVOAkw4PbK9Pos_c5GXbVfAjAvs4JYdvs031nPK8TSxyKsw/4u2/JDdLB4i8STiLDBQh8-3HAQ/h4/h001.xAK3n6P33K53CsjmMKTgEATq-g1WRoj4gRVQAsJsy20"
keywords: ["Pandas", "Polars", "DuckDB", "benchmark", "Big Data", "performance"]
theme: "Data"
tone: "opinion"
used_in: ["2026-09-16"]
---

## Résumé
L'auteur défend une thèse provocatrice : Pandas, la bibliothèque Python de manipulation de données, devrait être abandonnée car ses inefficiences poussent les utilisateurs à migrer prématurément vers des systèmes distribués coûteux (Spark, Databricks, Snowflake, Dask) alors que leurs volumes de données ne le justifient presque jamais. En s'appuyant sur des statistiques réelles issues de la flotte Amazon Redshift et sur des benchmarks qu'il a lui-même menés (dont le « 1 Billion Row Challenge » et un jeu de données de taxis new-yorkais), il montre que des outils mono-machine modernes comme Polars et DuckDB offrent des gains de vitesse et de mémoire considérables par rapport à Pandas, pour la grande majorité des charges de travail réelles, qui restent en réalité de la « Medium Data » et non du « Big Data ».

## Points clés
- D'après une analyse de la flotte Amazon Redshift (papier « Why TPC is not enough », 2024), 94,68 % des tables contiennent moins de 100 Go et 86,9 % des requêtes portent sur 80 Go de données ou moins : le vrai « Big Data » est rare.
- Sur le « 1 Billion Row Challenge » (1 milliard de lignes), Pandas met 4 min 28 s et consomme 38 Go de mémoire, contre 5,04 s / 18 Go pour Polars et 5,19 s / seulement 1,93 Go pour DuckDB (serveur cloud 32 cœurs/128 Go) ; l'écart se creuse encore sur un ordinateur portable, où Pandas finit par swapper 21 Go.
- Polars et DuckDB reposent sur une évaluation paresseuse (lazy evaluation) et des plans de requêtes optimisés façon base de données (projection, filtrage anticipé, exécution en flux/chunks), alors que Pandas charge tout en mémoire et exécute chaque étape séquentiellement.
- Sur un cas réel (3 Go de fichiers Parquet de trajets de taxis new-yorkais), la requête « pure DuckDB » s'exécute en 21,7 s contre 41,88 s pour « pure Pandas », avec une empreinte mémoire de 216 Mo contre 14,5 Go.
- Le format Apache Arrow, supporté nativement par Polars, DuckDB et Pandas (depuis la version 2.0), permet de faire circuler des DataFrames entre ces outils sans copie mémoire, ce qui facilite une adoption progressive plutôt qu'une réécriture complète.
- L'auteur nuance son propos : les benchmarks ont des limites, le coût de migration peut être élevé pour les équipes très intégrées à l'écosystème Pandas, et le choix entre SQL (DuckDB) et une API façon DataFrame (Polars) dépend surtout des préférences et du profil de l'équipe.

## Analyse approfondie
L'article part du constat d'un « parcours d'adoption » classique des outils d'analyse de données : on commence avec Excel, on migre vers Pandas autour de la gamme des gigaoctets, puis, en dizaines de Go, on se heurte à des problèmes de mémoire, une exécution lente et une API jugée peu intuitive. La réponse traditionnelle consiste alors à basculer vers un outil distribué « pour le Big Data » comme Spark, Databricks, Snowflake ou Dask. L'auteur soutient qu'il existe un écart grandissant entre ce point de rupture de Pandas (« la falaise Pandas ») et le seuil où les systèmes distribués deviennent réellement nécessaires — un seuil qu'il situe autour de 100 Go — et que cet écart peut être comblé efficacement par des outils mono-machine modernes et performants : Polars et DuckDB.

Pour justifier ce seuil de 100 Go, l'auteur s'appuie sur un papier publié par Amazon en 2024 (« Why TPC is not enough: An analysis of the Amazon Redshift fleet »), qui compare les données de télémétrie réelles de Redshift aux benchmarks standards du secteur. En posant deux hypothèses (une ligne moyenne de 1 Ko dans une table Redshift, et un cluster de 10 machines ingérant chacune 8 Go/s depuis S3), il calcule que 94,68 % des tables de la flotte Redshift contiennent moins de 100 Go de données, et que 86,9 % des requêtes portent sur 80 Go ou moins — dont 86,9 % s'exécutent en moins d'une seconde. Même en doublant l'hypothèse de taille de ligne à 10 Ko, la taille de table correspondante resterait autour de 1 To. Conclusion de l'auteur : la plupart des praticiens n'ont pas de problème de Big Data, mais un problème de « Medium Data », qui appelle des solutions à la mesure.

Il présente ensuite Polars (bibliothèque DataFrame écrite en Rust, à l'API proche de Pandas) et DuckDB (base analytique en mémoire, décrite comme « le SQLite de l'analytique ») comme les deux alternatives qu'il recommande. Pour illustrer leurs différences avec Pandas, il reprend le « 1 Billion Row Challenge », un défi consistant à calculer min/moyenne/max sur un fichier CSV d'un milliard de lignes de données météo (le record de la compétition étant de 1,5 seconde en Java). Ses tests sont menés sur une instance cloud équivalente au matériel bare-metal d'origine (32 cœurs, 128 Go de RAM, Debian 12).

Le code Pandas lit l'intégralité du CSV, regroupe par station et calcule les agrégats de façon séquentielle et « eager » (tout est chargé en mémoire avant traitement). Le code Polars, bien que syntaxiquement proche, repose sur une évaluation paresseuse : `scan_csv` ne déclenche aucun calcul tant que `.collect()` n'est pas appelé, ce qui permet à Polars de construire un plan de requête optimisé — comparable à celui d'une base de données — et de lire les données par blocs (streaming) en parallélisant le travail sur plusieurs threads. Le code DuckDB, lui, s'exprime en SQL standard (`select ... group by ...`) directement sur le CSV ou même sur un DataFrame Pandas en mémoire, DuckDB générant lui aussi un plan de requête paresseux, multi-thread et exécuté par blocs.

Les résultats de performance, mesurés par un outil de benchmark maison (30 répétitions après deux passes d'échauffement, sondage mémoire/CPU toutes les 50 ms), sont sans appel. Sur le serveur cloud :

| Bibliothèque | Durée médiane | CPU max médian | Mémoire (USS) max médiane | Swap max médian |
|---|---|---|---|---|
| Pandas | 4 min 28 s | 113,0 % | 38,12 Go | 0 Mo |
| Polars | 5,04 s | 3202,60 % | 18,02 Go | 0 Mo |
| DuckDB | 5,19 s | 3174,64 % | 1,93 Go | 0 Mo |

Sur un ordinateur portable plus modeste (Intel i5-1135G7, 8 cœurs, 16 Go de RAM), l'écart se creuse encore davantage :

| Bibliothèque | Durée médiane | CPU max médian | Mémoire (USS) max médiane | Swap max médian |
|---|---|---|---|---|
| Pandas | 12 min 15 s | 110,35 % | 15,67 Go | 21,02 Go |
| Polars | 39 s | 765,75 % | 15,22 Go | 35,85 Mo |
| DuckDB | 47 s | 807,0 % | 546,87 Mo | 0 Mo |

Pandas s'effondre littéralement, allant jusqu'à swapper 21 Go, tandis que Polars et DuckDB restent rapides et sobres en mémoire. L'auteur en tire quatre avantages structurels des outils modernes : un multithreading automatique sans gestion manuelle des processus ; une utilisation mémoire efficace grâce au traitement par blocs (streaming) ; une évaluation paresseuse qui permet d'optimiser le plan d'exécution global (par exemple via le filtrage anticipé, ou « predicate pushdown ») ; et un mécanisme intelligent de « spill to disk » lorsque les opérations dépassent la RAM disponible, plus efficace que le swap générique du système d'exploitation.

Il évoque brièvement des benchmarks TPC-H publiés par Coiled (une société vendant des services Dask hébergés), tout en invitant à la prudence puisque Coiled est en concurrence directe avec Polars/DuckDB sur ce marché — la même réserve s'appliquant, note-t-il avec autodérision, à ses propres résultats.

Un point central de l'article est le rôle d'Apache Arrow, format de représentation colonnaire en mémoire devenu un standard de facto, créé par Wes McKinney (le créateur originel de Pandas lui-même). Pandas prend en charge Arrow depuis sa version 2.0 (avril 2023), et Polars comme DuckDB le supportent nativement. Cela signifie qu'on peut faire transiter des DataFrames entre Pandas, Polars et DuckDB sans copie mémoire, rendant le passage d'un outil à l'autre quasiment « gratuit » — à condition, pour Pandas, de spécifier explicitement `dtype_backend="pyarrow"` à la création du DataFrame, ce comportement n'étant pas activé par défaut.

Pour un test plus proche d'un cas d'usage réel, l'auteur analyse le jeu de données des taxis new-yorkais (environ 3 Go de fichiers Parquet mensuels, de 2019 à 2022) afin de vérifier si les paiements en espèces ont reculé pendant la pandémie. Il compare quatre combinaisons (lecture et calcul 100 % Pandas, lecture DuckDB + calcul Pandas, lecture Pandas + calcul DuckDB, et 100 % DuckDB) :

| Approche | Durée médiane | CPU max médian | Mémoire (USS) max médiane | Swap max médian |
|---|---|---|---|---|
| 100 % Pandas | 41,88 s | 146,10 % | 14,52 Go | 1,92 Go |
| Lecture DuckDB + calcul Pandas | 28,39 s | 793,7 % | 14,79 Go | 1,22 Go |
| Lecture Pandas + calcul DuckDB | 29,25 s | 765,4 % | 12,39 Go | 0 Mo |
| 100 % DuckDB | 21,70 s | 814,95 % | 216,76 Mo | 0 Mo |

Même verdict : dès que DuckDB intervient, l'utilisation CPU grimpe (multithreading effectif) et la mémoire chute drastiquement, tandis que Pandas seul reste lent et gourmand. Sur le fond de l'analyse (le recul des paiements en espèces pendant la pandémie), l'auteur confirme la tendance tout en rappelant que corrélation n'est pas causalité.

L'article se conclut par une liste de raisons d'être sceptique vis-à-vis de ses propres conclusions : ce ne sont que les benchmarks d'une seule personne (le code est toutefois open source et vérifiable) ; le coût de bascule peut être trop élevé pour des équipes très ancrées dans l'écosystème Pandas ; et Pandas continue de s'améliorer, même lentement, compte tenu de sa position centrale dans l'écosystème. Il reconnaît aussi que DuckDB et Polars ont chacun leurs adeptes naturels — les ingénieurs data pencheraient plutôt vers SQL (DuckDB), les ingénieurs logiciels vers l'API façon DataFrame (Polars) — et que le choix final dépend de la charge de travail, de l'expérience et des préférences de chacun. Sa seule recommandation ferme : ne pas adopter aveuglément un système de requêtage distribué, avec toute la complexité que cela implique, simplement parce que Pandas est peu performant, alors que le besoin réel d'un tel système reste rare.

## Pourquoi ça compte
Ce texte invite les équipes data à remettre en question un réflexe répandu — migrer vers des architectures distribuées coûteuses dès que Pandas montre ses limites — alors que des outils mono-machine comme DuckDB et Polars, associés à Apache Arrow, couvrent déjà l'écrasante majorité des volumes de données réels avec bien moins de coût et de complexité opérationnelle.
