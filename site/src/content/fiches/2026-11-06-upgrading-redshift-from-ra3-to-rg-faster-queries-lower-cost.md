---
title: "Upgrading Redshift from RA3 to RG-Faster Queries Lower Cost"
date: 2026-11-06
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fblogs.halodoc.io%2Fupgrading-redshift-from-ra3-to-rg-and-achieving-faster-queries-at-32-lower-cost%2F%3Futm_source=tldrdata/1/010001a1ab694425-7b102ef4-fad4-4bac-bacb-26aa96fcab72-000000/80s4ANIKEgrtoW4NDDmR7oFhWM8Ifp5CbpZipHl9tmg=452"
keywords: ["Redshift", "AWS", "Graviton", "data warehouse", "migration cloud", "optimisation des coûts"]
theme: "Data"
tone: "research"
used_in: ["2026-11-06"]
---

## Résumé
Halodoc a migré son cluster Redshift de production des instances RA3 vers les nouvelles instances RG (basées sur des processeurs Graviton et un moteur de requêtes vectorisé, lancées par AWS en mai 2026). Plutôt que de faire confiance à la promesse d'AWS d'une « mise à niveau sur place », l'équipe a conçu onze contrôles couvrant les connexions, les permissions, le chargement et l'export de données, le masquage, la maintenance et la performance, avant de basculer via un elastic resize. Les résultats sont nets : chargements jusqu'à 6 fois plus rapides, tables de reporting jusqu'à 5,2 fois plus rapides, temps d'attente en file réduit d'environ 70 % en moyenne hebdomadaire, et facture totale (calcul + stockage) en baisse d'environ 32 %. L'article insiste sur une leçon méthodologique : vérifier que les éléments migrés (politiques de masquage, fonctions personnalisées) fonctionnent réellement, pas seulement qu'ils existent après la restauration du snapshot.

## Points clés
- Passage de Redshift RA3 à RG (processeurs Graviton, moteur de requêtes vectorisé), avec endpoint, port et dialecte SQL inchangés, via un elastic resize de 10 à 15 minutes d'indisponibilité.
- Méthodologie de validation en onze contrôles, suivant le chemin réel des données (connexions, permissions, chargement COPY, pipelines Spark et SQL direct, export, maintenance, masquage, streaming par curseur, performance).
- Gains de performance marqués : chargement de ~6 millions de lignes passé de 145 s à 24 s, tables de reporting 2,1 à 5,2 fois plus rapides, aucune régression détectée.
- Côté production : temps d'attente en file en baisse de 32 % (dashboards) à 83 % (pipelines), temps d'exécution moyen en baisse de 25 % à 57 %.
- Réduction du besoin de concurrency scaling de 45 %, permettant de ramener le nombre maximal de clusters supplémentaires de deux à un.
- Coût de calcul Redshift réduit d'environ 35 %, facture totale (stockage inclus) réduite d'environ 32 %.

## Analyse approfondie

### Introduction
Chez Halodoc, les données aident nos équipes à prendre de meilleures décisions sur les services de santé que nous proposons. Notre data warehouse Redshift est l'endroit où ces données se rassemblent, et nos équipes d'analyse l'utilisent chaque jour pour construire des tableaux de bord et des rapports. Lorsque quelque chose change en dessous, ces tableaux de bord et rapports sont les premiers endroits où les gens le remarquent.

En mai 2026, AWS a lancé les instances Amazon Redshift RG, une nouvelle génération basée sur des processeurs Graviton avec un moteur de requêtes repensé. Sur le papier, le passage depuis RA3 est une « mise à niveau sur place » (in-place upgrade). Même dialecte SQL, même port, même endpoint après un Elastic Resize.

Mais « rien ne change » est une hypothèse dangereuse quand votre entrepôt de données se trouve derrière des centaines de DAGs Airflow, des jobs Spark, des tableaux de bord, des politiques de gouvernance des données et des exports vers d'autres outils. Cet article détaille ce que nous avons testé avant de migrer notre cluster d'entrepôt principal vers les instances RG, ce qui a réellement changé sous le capot, et ce qui n'a pas changé.

### Ce qui change réellement sous le capot
Les nœuds RG fonctionnent sur des processeurs AWS Graviton, qui effectuent davantage de travail par vCPU que ceux des RA3. AWS affirme que cela, combiné au reste de la refonte, se traduit par des charges de travail jusqu'à 2,2 fois plus rapides, pour un prix par vCPU environ 30 % inférieur. Le moteur de requêtes est également nouveau. Il exécute les requêtes de manière vectorisée, ce qui signifie qu'une même requête peut obtenir un plan d'exécution différent de celui d'avant, et qu'un plan qui fonctionnait bien sur RA3 n'est pas garanti de bien fonctionner sur RG. RG apporte aussi un moteur intégré pour lire les fichiers Parquet depuis S3, ainsi que JIT ANALYZE, qui collecte automatiquement des statistiques pour les tables de data lake au fil de l'exécution des requêtes.

Un changement plus mineur mérite d'être mentionné. AWS indique que les nœuds RG ont des tailles de curseur plus petites, ce qui compte pour tout job qui diffuse (stream) de très grands résultats.

Tout le reste reste identique. L'endpoint, le port, le dialecte SQL, nos utilisateurs, groupes et paramètres de charge de travail (workload) sont tous repris depuis le snapshot. Ce dernier point est celui sur lequel nous étions le moins disposés à nous fier sans vérification. « Ça devrait être repris » est facile à dire, donc nous l'avons vérifié quand même.

### Comment nous avons testé
Nous avons construit le test autour d'une seule règle. Chaque endroit où nos systèmes touchent Redshift obtient son propre contrôle (check), et la condition de réussite est écrite avant que nous l'exécutions. Nous avons fini avec onze contrôles. Ils suivent le chemin des données, de la connexion au cluster jusqu'à la mesure de la vitesse d'exécution globale. La plupart de ces contrôles sont de simples tests de type réussite/échec, car la première question était de savoir si quelque chose allait casser. Le contrôle 11 est celui où nous avons comparé les chiffres entre les deux clusters.

#### 1. Un cluster de test sûr
Le premier risque était que le test lui-même touche la production. Nous avons restauré le dernier snapshot de notre cluster de production dans un nouveau cluster RG, après avoir confirmé que la version du cluster était suffisamment récente pour RG et que RG était disponible dans notre région AWS. Ensuite, nous avons donné au cluster de test sa propre connexion et avons fait des copies des pipelines que nous voulions essayer, afin que les pipelines de production ne pointent jamais vers lui. Le contrôle était réussi si la production restait intacte pendant toute la durée du test.

#### 2. Connexions et outils du quotidien
Un cluster ne sert à rien si les personnes et les outils ne peuvent pas l'atteindre. Nous nous sommes connectés depuis notre code Python, depuis Airflow, depuis un client SQL de bureau, depuis notre outil de tableaux de bord et depuis des notebooks exécutés sur notre cluster Spark. Nous avons aussi exécuté quelques fonctions de base dont notre code dépend. Ce contrôle était réussi si tout se connectait et renvoyait ce que nous attendions.

#### 3. Utilisateurs, permissions et fonctions personnalisées
Une restauration de snapshot est censée reprendre les utilisateurs, les groupes, les files d'attente de charge de travail (workload queues) et les fonctions personnalisées, et nous avons comparé chacun d'eux à la production. Pour les fonctions personnalisées qui nettoient les données dans nos tables de reporting, nous ne nous sommes pas contentés de vérifier qu'elles existaient. Nous avons appelé chacune d'elles et vérifié le résultat. Le contrôle était réussi quand tout correspondait à la production.

#### 4. Charger des données dans Redshift
La majorité de nos données arrive sous forme de fichiers Parquet dans S3 et est chargée avec la commande COPY. Nous avons chargé une table de test et comparé le nombre de lignes avec les fichiers source. Seule une correspondance exacte constituait une réussite.

#### 5. Nos pipelines principaux, de bout en bout
Nous écrivons dans Redshift de deux manières différentes, et un seul contrôle couvre les deux chemins. Le premier est le chemin Spark, où les jobs écrivent des fichiers vers S3, les chargent dans des tables de staging puis les fusionnent (merge) dans les tables finales. Le second est un chemin SQL direct utilisé pour certaines de nos tables de reporting, sans Spark ni S3 entre les deux. Pour les deux, nous avons fait passer de vraies tables par le cluster de test du début à la fin. Les contrôles étaient réussis quand les comptages de lignes étaient corrects, qu'il n'y avait pas de doublons sur les clés métier (business keys), et que le hash que nous utilisons pour détecter les lignes modifiées donnait les mêmes résultats qu'avant.

#### 6. Faire sortir les données
Nous envoyons aussi des données hors de Redshift, notamment vers notre plateforme marketing, qui est stricte sur le format des fichiers. Nous avons exporté un fichier de test et l'avons comparé à ce que produit la production, en recherchant les mêmes en-têtes, le même délimiteur et la même structure. Toute différence aurait cassé l'import de l'autre côté, donc le contrôle n'était réussi que si les fichiers étaient identiques en structure.

#### 7. Jobs de maintenance et monitoring
Redshift a besoin d'un entretien régulier, comme le vacuuming et la mise à jour des statistiques sur les tables qu'il stocke lui-même, et nous exécutons des alertes au-dessus de ses vues système. L'une d'elles nous prévient quand une requête s'exécute trop longtemps. Nous avons vérifié que ces vues existaient toujours avec les mêmes colonnes, et que vacuum et analyze s'exécutaient sans erreur.

#### 8. Masquage des données
C'est le contrôle que nous avons pris le plus au sérieux, car le masquage protège les données sensibles. Vérifier qu'une politique de masquage existe est facile. Nous voulions savoir si elle fonctionnait réellement. Nous avons donc comparé le nombre de politiques avec la production, supprimé puis réappliqué une politique sur une colonne non critique, puis interrogé les tables masquées en tant qu'utilisateur normal, et non en tant qu'administrateur. Le contrôle n'était réussi que si nous voyions des valeurs masquées à l'écran. Une politique figurant dans une liste ne prouve que très peu de choses.

#### 9. La configuration Spark vers Redshift
Nous avons confirmé que la recherche d'identifiants (credential lookup) pour le nouveau cluster fonctionnait toujours, et que les requêtes sur les tables externes stockées dans S3 s'exécutaient toujours. Le contrôle était réussi quand un job Spark complet se terminait avec des comptages de lignes corrects.

#### 10. Diffuser (streaming) de grands résultats
Un de nos jobs lit de grands résultats de requête par morceaux (chunks), en utilisant un curseur côté serveur, et les copie dans une base de données Postgres. AWS signale des tailles de curseur plus petites sur RG, ce qui est précisément l'endroit où un job comme celui-ci pourrait casser. Nous n'avons pas rejoué ce test sur le cluster de test, donc nous l'avons surveillé étroitement en production juste après le basculement. Il s'exécute toutes les heures, et les exécutions que nous avons vérifiées se sont toutes terminées avec succès, en diffusant par lots de 1 000 lignes, avec un nombre de lignes correspondant des deux côtés. En cas d'échec, la solution de repli (fallback) aurait été des lots plus petits ou un nœud plus grand.

#### 11. Vitesse et plans de requête
Enfin, nous avons exécuté les mêmes chargements, fusions, exports et jobs de maintenance sur les deux clusters et comparé le temps. Notre règle était simple. Tout ce qui est plus de 10 % plus lent sur RG est signalé. Comme le moteur est nouveau, nous avons aussi choisi nos requêtes de reporting les plus lourdes et comparé leurs plans d'exécution côte à côte, en examinant l'ordre des jointures et la manière dont les données circulent entre les nœuds.

Rien n'était plus lent sur RG. Nous avons exécuté chaque test sur les deux clusters dans les mêmes conditions, après 20h quand la production est calme, afin qu'aucun des deux clusters ne soit en concurrence avec d'autres travaux. Le chargement d'environ 6 millions de lignes avec COPY est passé de 145 secondes à 24, soit environ six fois plus rapide. L'export d'un volume similaire en Parquet est passé de 366 secondes à 301, un gain plus modeste d'environ 18 %. La construction de cinq de nos tables de reporting les plus lourdes s'est exécutée entre 2,1 et 5,2 fois plus rapidement.

Les plans expliquaient une grande partie de cela. Sur RA3, les tables externes stockées dans S3 passaient par une couche de scan séparée, alors que RG les lit directement sur ses nœuds de calcul. RA3 diffusait aussi (broadcast) une table d'environ 10 millions de lignes dans quatre sous-requêtes, alors que RG ne distribuait que les données dont il avait besoin en fonction de la clé de jointure. Et RA3 planifiait avec des statistiques obsolètes, ce qui lui faisait mal évaluer le nombre de lignes sur plusieurs tables.

### Le basculement
Comme l'endpoint reste le même, nos applications n'ont pas eu besoin de changer. Nous avons utilisé un elastic resize pendant une fenêtre planifiée, ce qui prend environ dix à quinze minutes d'indisponibilité (downtime).

### Ce que nous avons observé par la suite
Nous avons mesuré la même charge de travail avant et après le changement de cluster. Il s'agit de la charge matinale habituelle des pipelines planifiés et des requêtes de tableaux de bord, qui s'exécute selon le même calendrier. Nous avons observé la fenêtre matinale de 7h à 13h, quand l'entrepôt est le plus sollicité. Une matinée typique dans cette fenêtre comporte environ 11 000 requêtes, dont environ 8 500 provenant des tableaux de bord et 2 300 des pipelines.

Le graphique compare RA3 et RG sur la même charge matinale. Chaque barre représente le temps en pourcentage de ce qu'il était sur RA3, donc une barre plus courte est meilleure.

- Le temps d'attente en file (queue time) est le temps qu'une requête attend son tour avant de démarrer. Il a chuté d'environ 32 % pour les tableaux de bord et de 83 % pour les pipelines.
- Le temps d'exécution moyen (average run time) est la durée que prend une requête typique une fois démarrée. Il a chuté d'environ 25 % pour les tableaux de bord et de 57 % pour les pipelines.
- Les 5 % les plus lents (aussi appelé p95) est le temps que seules les 5 % de requêtes les plus lentes dépassent. Une bonne moyenne peut cacher quelques requêtes très lentes, et ce sont celles-là que les gens remarquent. Il a chuté d'environ 15 % pour les tableaux de bord et de 46 % pour les pipelines.

Le tableau ci-dessous montre comment le temps d'exécution moyen a évolué sur RG, heure par heure, par rapport à RA3.

Nos pipelines de données ont le plus progressé. Les requêtes ont presque arrêté d'attendre en file, et elles se sont exécutées plus rapidement tout au long de la matinée. Les requêtes de tableaux de bord se sont améliorées dans l'ensemble, mais pas à chaque heure. La plupart des heures étaient plus rapides, une était à peu près identique et une était plus lente qu'avant, et nous les surveillons.

Le résultat qui nous a le plus surpris concernait le concurrency scaling, la fonctionnalité qui ajoute de la capacité supplémentaire quand le cluster principal est occupé. Seules les requêtes de tableaux de bord l'utilisaient. Après le basculement, la capacité supplémentaire que nous avons utilisée a chuté d'environ 45 %, parce que le cluster principal pouvait désormais gérer la charge lui-même. Nous avons donc réduit le nombre maximal de clusters supplémentaires de deux à un.

Les chiffres hebdomadaires se maintiennent depuis le basculement. Ils couvrent toutes les heures, pas seulement la fenêtre matinale, et montrent la même tendance. Le temps d'attente moyen en file est en baisse d'environ 70 % et le temps d'exécution moyen d'environ 35 %.

Le changement a également réduit nos coûts. Le coût du cluster a chuté de 30 %, conforme à l'annonce d'AWS sur le prix par vCPU, et les dépenses de concurrency scaling ont chuté de 76 %, parce que le cluster gère désormais la plupart des pics lui-même et que les crédits quotidiens gratuits couvrent une plus grande partie de ce qui reste. Au total, notre coût de calcul (compute) Redshift est environ 35 % inférieur à avant, et la facture totale, stockage inclus, est environ 32 % inférieure.

### Ce que nous avons appris
Testez les chemins que vos pipelines utilisent réellement. Notre chemin de chargement principal et notre chemin SQL direct sont deux codes différents, et tester l'un ne dit rien sur l'autre.

Vérifiez que les choses fonctionnent, pas seulement qu'elles existent. Les politiques de masquage et les fonctions personnalisées ont bien été reprises depuis le snapshot, mais nous ne leur avons fait confiance qu'après les avoir utilisées.

Un cluster plus rapide change la façon dont vous devriez configurer le concurrency scaling. Regardez combien de temps prennent réellement les requêtes qui débordent (spill over), et pas seulement la fréquence à laquelle il est utilisé.

### Et ensuite
Le moteur intégré de RG lit des formats de data lake comme Parquet et Hudi directement sur les nœuds de calcul du cluster. Nous explorons maintenant la possibilité de faire entrer une partie de nos charges de travail de data lake et d'ETL directement dans le cluster Redshift, et testerons leur comportement avant de déployer quoi que ce soit.

### Références
- Instances Amazon Redshift RG : fonctionnalités
- Découvrez Amazon Redshift RG : des instances basées sur Graviton avec un moteur de requêtes intégré pour le data lake (AWS Big Data Blog)
- DECLARE : contraintes de curseur par type de nœud (documentation Amazon Redshift)
- Redimensionner un cluster : elastic resize (documentation Amazon Redshift)

### Rejoignez-nous
La scalabilité, la fiabilité et la maintenabilité sont les trois piliers qui régissent ce que nous construisons chez Halodoc Tech. Nous recherchons activement des ingénieurs à tous les niveaux, et si résoudre des problèmes difficiles avec des exigences complexes est votre point fort, contactez-nous avec votre CV à careers.india@halodoc.com.

### À propos de Halodoc
Halodoc est l'application de santé généraliste numéro un en Indonésie. Notre mission est de simplifier et de fournir des soins de santé de qualité à travers toute l'Indonésie, de Sabang à Merauke.

Depuis 2016, Halodoc améliore la littératie en santé en Indonésie en proposant une communication, une éducation et une information sur la santé (KIE) conviviales. En parallèle, notre écosystème s'est élargi pour offrir une gamme de services facilitant un accès pratique aux soins de santé, à commencer par Homecare by Halodoc, une fonctionnalité de soins préventifs qui permet aux utilisateurs de réaliser des tests de santé en privé et en toute sécurité depuis le confort de leur domicile ; My Insurance, qui permet aux utilisateurs d'accéder aux avantages de services ambulatoires sans paiement direct (cashless) de manière plus fluide ; Chat with Doctor, qui permet aux utilisateurs de consulter plus de 20 000 médecins agréés par chat, vidéo ou appel vocal ; et les fonctionnalités Health Store qui permettent aux utilisateurs d'acheter des médicaments, des compléments et divers produits de santé auprès de notre réseau de plus de 4 900 pharmacies partenaires de confiance. Pour proposer des solutions de santé holistiques de manière entièrement numérique, Halodoc propose des services de Digital Clinic incluant Haloskin, une plateforme de dermatologie de confiance guidée par des dermatologues expérimentés.

Nous sommes fiers de bénéficier de la confiance d'investisseurs mondiaux et régionaux, notamment la Bill & Melinda Gates Foundation, Singtel, UOB Ventures, Allianz, GoJek, Astra, Temasek, et bien d'autres. Avec plus de 100 millions de dollars levés à ce jour, incluant notre récente Série D, notre équipe s'engage à construire les meilleures solutions de santé personnalisées, et nous restons déterminés dans notre mission de simplifier la santé pour tous les Indonésiens.

## Pourquoi ça compte
Ce retour d'expérience offre une méthodologie de validation concrète et réutilisable pour toute migration de data warehouse critique, et quantifie des gains AWS Graviton (performance et coût) rarement documentés avec un tel niveau de détail opérationnel. Pour une veille tech, c'est un cas d'étude utile sur l'arbitrage performance/coût des nouvelles générations d'instances cloud et sur la rigueur de test à appliquer avant toute migration d'infrastructure de données.
