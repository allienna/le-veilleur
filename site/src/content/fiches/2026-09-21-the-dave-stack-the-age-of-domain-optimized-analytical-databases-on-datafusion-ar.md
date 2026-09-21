---
title: "The DAVE stack: the age of domain-optimized analytical databases on Datafusion, Arrow, and Vortex, Embedded"
date: 2026-09-21
url: "https://substack.com/redirect/2cc82a27-3c89-4da2-aa4b-dd9525169d35?j=eyJ1IjoiN3Y1bG1jIn0.HlvPOGYPdVknSYzEK1JIj6IFkAFn8zuyjtfU9Mbft9Q"
keywords: ["bases de données analytiques", "Apache Arrow", "Datafusion", "Vortex", "génomique", "architecture embarquée"]
theme: "Data"
tone: "opinion"
used_in: ["2026-09-21"]
---

## Résumé
L'auteur présente le « DAVE stack » (Datafusion, Arrow, Vortex, Embedded), une combinaison de briques open source qui rend aujourd'hui économiquement viable la construction de bases de données analytiques optimisées pour un domaine précis, alors que ce type de projet était auparavant réservé à des marchés massifs. Fort de huit années passées à construire Hail (Broad Institute) pour la génomique des populations, il explique comment il applique ce stack à Phoebe, la base de données qu'il développe chez Phoebe Genomics pour les données de variants génétiques. Il détaille, brique par brique, comment Datafusion (moteur de requêtes), Arrow (couche de calcul en mémoire), Vortex (moteur de stockage columnar) et une architecture « embedded » (intégration dans des systèmes distribués tiers) permettent de n'écrire que la logique réellement spécifique au domaine. Il conclut que ce stack, combiné à l'ingénierie assistée par des agents, permet à de petites équipes de s'attaquer à des problèmes de données jusque-là hors de portée.

## Points clés
- Les bases analytiques généralistes (BigQuery, Snowflake, Databricks SQL, Redshift, ClickHouse) couvrent la majorité des besoins, mais une base réellement optimisée pour un domaine surclasse largement ces systèmes dès que l'échelle grandit.
- Construire une base de données sur mesure a toujours été un projet énorme et coûteux, justifiable seulement pour des marchés massifs (données d'entreprise génériques) — ce qui laissait de côté beaucoup de domaines de niche.
- Le stack DAVE combine quatre couches réutilisables : Datafusion (moteur de requêtes extensible), Arrow (représentation et calcul en mémoire), Vortex (format de fichier et moteur de stockage columnar) et une approche « Embedded » (assembler son système distribué en s'intégrant dans ceux des autres plutôt que d'en construire un).
- Phoebe, la base de données de l'auteur pour la génomique des populations, illustre le stack : elle traduit les filtres de lignes/colonnes en bitmaps exploités nativement par Vortex pour éviter toute matérialisation inutile — une optimisation impossible avec Parquet.
- L'architecture embarquée permet de déployer le même moteur dans des contextes très variés (conteneurs AWS Batch/Nextflow/Modal, AWS Lambda, Fargate avec cache NVMe local, Google Cloud Run, conteneurs Docker de recherche) sans reconstruire un système distribué à chaque fois.
- S'appuyer sur DAVE n'élimine pas la complexité : Phoebe compte environ 70 000 lignes de Rust au-dessus du stack, et l'équipe doit maîtriser en profondeur Datafusion, Arrow et Vortex ainsi que la logique de distribution.

## Analyse approfondie

### Les bases de données optimisées par domaine sont géniales, mais elles coûtaient cher
En 2026, les données sont massives et complexes, et il existe déjà de puissantes bases de données analytiques généralistes — Google BigQuery, Snowflake, Databricks SQL, AWS Redshift, ClickHouse — utilisées dans presque toutes les industries. Mais les données ne se ressemblent pas toutes : chaque domaine a ses particularités, car le monde est compliqué. On peut faire rentrer 99 % des requêtes bizarres et spécifiques à un domaine dans ces systèmes généralistes moyennant assez d'efforts, mais si les fondamentaux s'en approchent, une base de données *optimisée pour le domaine* surclassera largement les systèmes généralistes, en étant conçue *pour* les particularités plutôt qu'en les contournant.

C'est une opportunité énorme : ne devrait-on pas construire une base de données pour chaque type de données ? Le problème, c'est que les bases de données ont toujours été des projets **énormes, coûteux et chronophages**. Le jeu en valait la chandelle quand il existe une immense catégorie de *données d'entreprise* qu'on peut conquérir avec une ingestion et des requêtes de séries temporelles ultra-performantes, ou des caches multi-niveaux sur du stockage objet pour de la récupération d'embeddings à faible coût et faible latence. Mais l'effort est difficile à justifier s'il n'y a que des dizaines ou des centaines d'organisations qui ont besoin de votre base de données, plutôt que des milliers.

Cela laisse un entre-deux douloureux : de nombreuses industries gèrent des données pour lesquelles il ne vaut pas la peine de construire une base analytique complète, mais il existe un fossé entre la performance et l'utilité d'une base généraliste et le plafond d'un système expertement optimisé pour le domaine. Cet écart n'a pas d'importance avec quelques gigaoctets, mais il devient significatif à mesure que l'on monte en échelle.

L'auteur a une expérience directe du sujet : il a passé environ huit ans à construire Hail au Broad Institute, avec une équipe restreinte suffisamment ambitieuse (« unhinged », dérangée diraient certains) pour bâtir une base de données analytique complète dédiée à la recherche en génomique des populations.

Hail a démarré en 2015 comme une bibliothèque relativement modeste construite autour des RDD d'Apache Spark (l'interface de type map-reduce). En deux ans, l'équipe avait développé son propre planificateur relationnel, son optimiseur de requêtes, et un compilateur d'expressions ciblant le bytecode JVM et tournant sur Spark. Ils ont en pratique forké Spark, car les couches dataframes et de génération de code arrivaient dans le cœur de Spark au même moment, et l'équipe avait besoin de capacités particulières pour la génomique (un support transverse et profond de l'ordonnancement, partout). L'auteur ne peut imaginer meilleur creuset pour apprendre à déboguer des systèmes de données bas niveau que de traquer des problèmes de performance et des bugs mémoire à travers du bytecode JVM généré, utilisant massivement `Unsafe` en Java, à l'intérieur d'un interpréteur qui réécrit le code en cours d'exécution — à la fois extrêmement pénible et follement amusant. L'équipe a fini par construire aussi son propre gestionnaire de cluster et ordonnanceur de conteneurs, en alternative aux RDD Spark (un peu comme Modal Batch, construit par une poignée d'ingénieurs surdoués dans une organisation à but non lucratif).

Bien que maintenir toute cette pile ait représenté un travail considérable, le bénéfice était que l'équipe pouvait optimiser les requêtes pour les scientifiques qu'elle soutenait en toute liberté : ils pouvaient construire des systèmes d'exécution mêlant logique relationnelle et algèbre linéaire pour calculer le déséquilibre de liaison (« linkage disequilibrium ») en bandes à partir de matrices de génotypes distribuées massives, ou effectuer en une seule passe le calcul simultané d'un nombre déraisonnable d'agrégations imbriquées pour produire les métriques de synthèse du navigateur gnomAD. Et si on pouvait écrire ce genre d'optimisations sans posséder tout le système ?

### Faisons connaissance avec DAVE
En 2026, construire une base de données OLAP optimisée pour un domaine est devenu une proposition tout à fait raisonnable — et pas grâce à l'IA. La raison principale, c'est qu'il faut simplement construire beaucoup moins de choses, grâce à DAVE.

On peut obtenir un très bon niveau d'optimisation spécifique à un domaine sur cinq points du système :
- des plans de requêtes et des noyaux de jointure spécialisés pour des requêtes atypiques ;
- des agencements de tables spécialisés (comment les données sont stockées à travers les fichiers) pour des schémas d'ingestion et d'accès atypiques ;
- des noyaux de calcul spécialisés pour des fonctions atypiques ;
- des encodeurs/décodeurs et agencements de stockage spécialisés (comment les données sont stockées à l'intérieur des fichiers) pour des formats de bits atypiques ;
- des architectures de systèmes distribués spécialisées pour des exigences système atypiques.

Il a toujours existé des bases de données open source, mais il a toujours été extrêmement difficile de forker l'une d'elles et d'en modifier l'interne suffisamment pour en tirer un bénéfice réel. Aujourd'hui en revanche, il est possible de ne construire que ces morceaux spécifiques et d'hériter du reste du système.

**[D]**atafusion, **[A]**rrow, **[V]**ortex, et une architecture système **[E]**mbedded. Ces quatre couches représentent quatre immenses catégories de travail d'ingénierie que l'on n'a **pas besoin de faire soi-même**, car elles permettent une extension précisément là où c'est nécessaire :
- **Datafusion** : pas besoin de construire le moteur de requêtes ;
- **Arrow** : pas besoin de construire la couche de calcul en mémoire ;
- **Vortex** : pas besoin de construire le moteur de stockage généraliste, les agencements sur disque, ni l'ordonnanceur d'E/S ;
- **Embedded** : on assemble le système distribué dont on a besoin en embarquant des morceaux de son moteur dans les systèmes distribués d'autres personnes 🥷.

Prises individuellement, ces technologies sont déjà excellentes et font tourner de nombreux systèmes en aval. Combinées, elles ont bouleversé l'économie et les délais de construction de bases de données analytiques optimisées pour un domaine.

### Phoebe
Phoebe est la base de données que l'auteur construit chez Phoebe Genomics, et elle constitue la preuve principale que **ce stack fonctionne**. Phoebe est conçue pour les données génomiques de population (variants), et l'auteur donne des exemples précis de la façon dont elle étend DAVE pour obtenir d'excellentes performances système et une grande flexibilité, adaptées aux exigences particulières de la génomique. Quelques éléments à connaître sur les données de variants pour comprendre l'exemple :
- Les données de variants d'une population mesurent de nombreux individus (échantillons) à travers de nombreux changements du génome (variants). Les données sont stockées comme un différentiel (diff) par rapport au génome humain de référence.
- Un seul échantillon compte environ 3 à 5 millions de variants/mutations, et les grands jeux de données actuels comptent des centaines de milliers d'échantillons — soit environ des billions (trillions) d'enregistrements de variants dans un seul jeu de données de population.
- La plupart des variants uniques sont très rares au sein des échantillons, mais la plupart des enregistrements appartiennent au petit nombre de variants communs — un peu comme dire que « la plupart des livres sur Amazon se vendent peu, mais la plupart des ventes viennent du petit nombre de best-sellers du New York Times ». Mais il ne s'agit pas seulement de faire des recherches ponctuelles rares sur chaque variant rare en génomique : on lit souvent beaucoup de ces variants en même temps pour agréger un signal, par exemple par gène.
- Entre les variants, chaque échantillon est accompagné de données reflétant la qualité du processus de séquençage, car il est parfois crucial de distinguer « cet échantillon n'avait pas de variant à cette position parce qu'on a observé beaucoup de lectures de référence » de « cet échantillon n'avait pas de variant à cette position et on n'a rien observé indiquant non plus l'allèle de référence ».
- D'un échantillon à l'autre, les variants et intervalles ne s'alignent pas proprement : soit on crée une matrice dense (avec énormément de duplication), soit on scinde l'évidence en deux tables avec des encodages creux (sparse) et on reporte la complexité sur les jointures — c'est la bonne approche.

L'article présente ensuite une requête de recherche représentative, annotée pour décrire comment Phoebe l'exécute. Exécutée sur un conteneur Fargate sans état doté d'un petit cache NVMe en lecture directe, cette requête renvoie un résultat en quelques secondes, en touchant environ 1 Go de données compressées à travers environ 2000 lectures portant sur environ 200 fichiers stockés, principalement dans S3.

### [D]atafusion / [A]rrow
Commençons par Arrow. On approche du dixième anniversaire de sa première version stable, et à ce stade, construire sur Arrow paraît presque banal — Arrow a gagné. C'est devenu la représentation en mémoire évidente et simple, ainsi que la couche de calcul extensible qui a débloqué une immense interopérabilité à faible coût. Si le noyau de calcul dont on a besoin n'existe pas dans la bibliothèque Arrow, on peut l'écrire soi-même sans grande difficulté.

Datafusion est un projet bien plus vaste qu'Arrow : un moteur de requêtes embarquable visant (et atteignant) des performances de pointe, avec des points d'extension aux endroits qui comptent pour les concepteurs de bases de données — le planificateur de requêtes, l'exécution relationnelle, les fournisseurs de tables, et les noyaux de calcul (dans Arrow).

L'auteur ne prétend pas qu'il suffit d'étendre Datafusion à ces endroits pour pouvoir faire absolument tout ce qu'on veut — la requête Phoebe présentée plus haut n'y arrive pas tout à fait, puisque son étape 4 nécessite d'exécuter des requêtes Datafusion concurrentes afin de demander des plages de lignes spécifiques à des lectures Vortex parallélisées. Cela fonctionne très bien, et l'auteur pense qu'à terme ce sera encore plus simple, à mesure que la communauté Datafusion pousse des abstractions extensibles encore plus puissantes dans le système.

### [V]ortex
On pourrait raisonnablement soutenir qu'une architecture **DAPE** basée sur Parquet couvre déjà l'essentiel du chemin — c'est vrai pour beaucoup de problèmes, de domaines et de requêtes. Mais une fois qu'on a réellement construit une couche de stockage qui gère les agencements, encodages et opérations de pushdown atypiques permettant de pousser le matériel au maximum pour des données de domaine particulières, *il devient très difficile de renoncer à ce contrôle*. En génomique des populations, la plupart des requêtes ne touchent qu'un sous-ensemble de lignes et un sous-ensemble de colonnes de la matrice creuse et structurée variant-par-échantillon, et il est impossible d'agencer les lignes/colonnes de façon à ce que les enregistrements recherchés soient contigus.

C'est là qu'intervient Vortex, le plus jeune des trois projets de DAVE. Vortex est un format de fichier et un moteur de stockage columnar qui offre à la fois une puissance brute prête à l'emploi et des points d'extension à tous les niveaux. Phoebe transforme les listes de lignes à conserver en bitmaps d'index de lignes que Vortex utilise pour éviter la matérialisation au sein d'une page (voire pour ignorer des pages entières !). Les listes de colonnes à conserver sont traduites en noyaux de filtrage Vortex personnalisés, utilisant des bitmaps qui s'exécutent en premier (haute sélectivité) sur les valeurs de colonnes et évitent une grande quantité de matérialisation. Impossible de faire cela avec Parquet ! De plus, et c'est très important, Vortex intègre nativement la mécanique d'E/S nécessaire pour interagir efficacement avec le stockage objet, ce dont l'auteur se réjouit particulièrement car ce sujet regorge de pièges.

Vortex a été construit puis donné à l'Apache Software Foundation par des personnes sérieuses, et l'auteur n'est pas le seul à parier sur Vortex comme brique fondamentale de l'infrastructure de données : il cite notamment Spice AI et Polar Signals. Alfonso Marqués écrit à propos de ce dernier :

> « Pour nous, trouver Vortex, c'était comme trouver enfin une paire de chaussures à la bonne pointure après avoir marché trop longtemps avec une taille en dessous. Le résultat a été de pouvoir tourner 70 % plus vite. »

L'auteur ne peut qu'approuver.

### [E]mbedded
Ce n'est pas un composant open source du stack, mais plutôt une approche d'esprit similaire : les bases de données embarquées permettent une stratégie « acheter plutôt que construire » qui laisse un système OLAP optimisé pour un domaine surfer au-dessus d'un océan de complexité plutôt que d'avoir à le traverser à la nage.

En résumé, **ne construisez pas votre propre système distribué complet** : d'autres investissent énormément de sueur, d'argent et d'idées dans des systèmes distribués formidables, et **vous pouvez assembler le système distribué dont vous avez besoin en embarquant votre moteur à l'intérieur des systèmes distribués des autres**. DuckDB a connu une explosion de popularité ces cinq dernières années exactement pour cette raison, et il vaut la peine de se renseigner sur la façon dont les gens utilisent DuckDB pour s'en inspirer. L'auteur est également totalement convaincu que construire autour de stockages objet modernes comme S3 permet de créer des systèmes hautement performants et massivement scalables tout en restant étonnamment simples. Le moteur Phoebe embarqué, qui dialogue avec les données dans le stockage objet, peut se comporter comme un caméléon :
- embarqué dans des conteneurs (AWS Batch | Nextflow | Modal) pour des tâches d'ingestion économiques et de compaction en arrière-plan ;
- embarqué dans des tâches AWS Lambda pour exécuter des requêtes interactives distribuées ;
- embarqué dans un conteneur Fargate longue durée doté d'un cache NVMe en lecture directe de 50 Go sur les données les plus « chaudes », ramenant des requêtes de cohortes volumineuses d'environ 9 s à environ 2,5 s en éliminant la plupart des allers-retours bloquants vers S3 ;
- embarqué dans un service Google Cloud Run pour un backend de recherche qui monte en charge et redescend à zéro ;
- embarqué dans des conteneurs Docker contenant des outils de recherche, en simple chargeur de données capable de dialoguer directement avec S3.

Chacun de ces enrobages ne représente que quelques centaines de lignes de code encapsulant le moteur, principalement du code répétitif. Quand un nouveau système distribué intéressant apparaît sur le marché (bonjour, Modal, qui permet de composer facilement un ensemble de primitives de systèmes distribués), il est très simple de l'essayer. Et la génomique des populations a un besoin encore plus fort de la flexibilité que permettent les systèmes embarqués : copier des données génomiques d'un système à l'autre pour différentes tâches (entreposage, recherche, recherche scientifique) devient très pénible à grande échelle. Tout le monde s'en plaint, et l'auteur pense que l'essentiel de ce problème peut disparaître !

L'auteur admet cependant survoler une bonne partie de la complexité ici. Il existe clairement une opportunité pour une infrastructure extensible également au niveau de la couche de distribution. Il garde un œil sur deux projets en particulier, et ne serait pas surpris que l'un d'eux rejoigne l'arbre de dépendances de Phoebe dans les six prochains mois.

### Il faut quand même posséder toute la base de données
L'auteur ne veut pas vendre du rêve : il reste beaucoup de travail à faire lorsqu'on construit sur DAVE. Pour en tirer pleinement bénéfice, il faut comprendre à la fois le domaine et le fonctionnement des bases de données : savoir repérer une question sémantique dans un domaine, la traduire en requête précise, et raisonner sur l'endroit où les bits doivent résider et comment ils doivent circuler à travers les couches de stockage, de mémoire et de calcul. Comment les données doivent-elles être partitionnées ? Quelles jointures doivent s'exécuter en premier, et selon quelles heuristiques ou quelles données ? Comment encoder les données, et peuvent-elles *rester* encodées tout au long de la requête ? Le cœur de Phoebe représente environ 70 000 lignes de Rust hors tests, ce qui montre qu'il existe une réelle complexité au-dessus de DAVE. Adopter ce stack revient à s'engager à apprendre suffisamment le fonctionnement de Datafusion, Arrow et Vortex pour pouvoir optimiser autour et à l'intérieur de ces systèmes, tout en assumant la responsabilité de l'architecture du système distribué via l'« embedding ».

### Construisons
En combinant le levier de l'ingénierie agentique avec le stack DAVE, de petites équipes disposant d'une expertise du domaine et des bases de données peuvent s'attaquer à de très gros problèmes. Il existe énormément de domaines dans le monde avec des données atypiques. **Construisons donc, nous aussi, un tas de bases de données atypiques.**

*Remerciements à Dan King et Andrew Lamb pour leurs commentaires sur une version préliminaire.*

## Pourquoi ça compte
Ce billet documente, avec un exemple concret et chiffré (Phoebe), un basculement réel dans l'économie de l'ingénierie des bases de données analytiques : Arrow, Datafusion et Vortex rendent désormais réalisable, pour de petites équipes, la construction de moteurs analytiques sur mesure — un signal important pour quiconque suit l'infrastructure data, l'écosystème columnar/embedded (proche de la dynamique DuckDB) et la convergence avec l'ingénierie logicielle assistée par agents.
