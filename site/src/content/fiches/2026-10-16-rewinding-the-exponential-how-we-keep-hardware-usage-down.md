---
title: "Rewinding the exponential: How we keep hardware usage down"
date: 2026-10-16
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fblog.cloudflare.com%2Frewinding-the-exponential%3Futm_source=tldrdata/1/010001a13f0d59fd-c7dedc25-842c-4848-902e-7af2e182448b-000000/c0ZPjpt_QflOtwXig-szGQU-5lGUbiXCNJulo0QR2Q0=452"
keywords: ["pipeline de données", "Cloudflare", "échantillonnage", "compression", "ClickHouse", "scalabilité"]
theme: "Data"
tone: "research"
used_in: ["2026-10-16"]
---

## Résumé
L'équipe Data de Cloudflare détaille cinq ans d'optimisations menées pour faire face à une croissance exponentielle du trafic (environ deux milliards d'événements par seconde en mai 2026) alors que les capacités matérielles ne croissent que linéairement. Les leviers combinés — décomposition du schéma monolithique (2022), changement de compression LZ4→zstd (2024), refonte de la réplication par répartition de charge, échantillonnage décentralisé et agrégation précoce dans le pipeline (2026) — ont permis d'éliminer environ 70 Go/s de trafic compressé depuis le printemps 2026. Au total, ces optimisations équivalent à avoir différé environ deux ans et demi d'expansion matérielle. L'article conclut que ces gains structurels divisent par deux le volume de données qui devra être traité dans cinq ans.

## Points clés
- La croissance du trafic est exponentielle alors que le budget matériel croît de façon linéaire, ce qui impose une optimisation logicielle continue plutôt qu'un simple achat de matériel supplémentaire.
- En 2022, le passage d'un schéma de données monolithique à des schémas spécifiques par produit a réduit l'usage de bande passante du backbone de 35 à 40 %.
- En 2024, le remplacement de LZ4 par zstd a réduit le trafic compressé d'environ 40 %, avec un impact CPU négligeable.
- En 2026, une nouvelle architecture de réplication (écriture unique + réplication tardive inter-centres de données, inspirée du modèle de Logpush) a supprimé 43 Go/s tout en n'ajoutant que 7 Go/s.
- Un double échantillonnage (mélange des enregistrements puis échantillon de taille égale à la racine carrée du total par clé) réduit le stockage proportionnellement plus pour les clés à fort volume, tout en conservant un échantillon statistiquement représentatif.
- Déplacer l'agrégation en amont du pipeline (dès Logfwdr) a réduit le trafic du jeu de données HTTP d'environ 80 %, passant de plus de 9 Go/s à moins de 2 Go/s.

## Analyse approfondie
Plus de 20 % du web est protégé par le réseau de Cloudflare, et notre équipe, l'équipe Data, est responsable du pipeline de données qui achemine ces données (et bien d'autres) depuis notre réseau mondial vers les centres de données centraux concernés. Le réseau de Cloudflare est un système distribué à l'échelle mondiale qui prend en charge des dizaines de milliers de serveurs. Les données qui alimentent Cloudflare Logs, la SQL API, l'observabilité, les analyses internes, et plus encore, transitent par ce réseau et utilisent notre pipeline de données pour servir les clients.

En mai de cette année, nous assurions la livraison de données à un débit d'environ deux milliards d'événements par seconde. Cela inclut le trafic client ainsi que les données envoyées par les équipes internes. Année après année, nous faisons face au même problème : une croissance exponentielle du trafic contre une croissance linéaire du matériel. Nous devons réagir à cette augmentation afin de maîtriser les coûts des ressources. Au cours des cinq dernières années, nous avons apporté diverses améliorations pour compenser l'augmentation du volume de données par rapport à l'allocation matérielle, ce qui équivaut à avoir reporté deux ans et demi d'expansion matérielle. Cet article détaille ces changements : la décomposition de notre schéma de données monolithique en 2022, l'ajustement de la compression en 2024, la refonte architecturale de la réplication du pipeline au printemps 2026, la décentralisation de l'échantillonnage à l'été 2026, et l'introduction des agrégations dans le pipeline à l'automne 2026.

### Contexte
Notre pipeline commence par un service interne appelé Logfwdr, où nous collectons les données depuis des sources hautement distribuées (pensez : Workers, FL). Nous transmettons ensuite ces données à un ensemble de récepteurs centralisés, qui les poussent finalement vers notre système de mise en tampon (buffering), Buftee. Des consommateurs récupèrent les données depuis Buftee et les distribuent vers leurs destinations finales, comme ClickHouse, sur lequel nous nous appuyons fortement.

### Déconstruire le monolithe
En 2022, nous avons démantelé notre unique schéma. Auparavant, il existait un flux unique regroupant les champs de tous les produits, ce qui obligeait les consommateurs internes de Cloudflare à tout ingérer puis à démultiplexer ou à écarter des enregistrements via des filtres. À l'époque, la plupart des produits de données de Cloudflare étaient construits sur des métadonnées HTTP, de sécurité et de CDN. En 2021, notre schéma de message ressemblait à ceci :

Certains champs appartenaient au même produit, mais d'autres n'avaient absolument aucun rapport entre eux. L'hypothèse était qu'aucune de ces équipes n'avait besoin de 100 % des champs du schéma monolithique. En d'autres termes, nous pouvions créer des messages plus petits contenant uniquement les champs requis par chaque produit. Bien que cela implique de dupliquer certains champs, parfois dans chaque message, le remplacement de ce flux unique par des schémas spécifiques à chaque produit a en réalité réduit l'utilisation de la bande passante du backbone de 35 à 40 %, ce qui a permis d'éliminer l'équivalent d'environ une année de croissance du trafic compressé.

### Compression
En 2024, alors que le trafic augmentait de façon constante, nous faisions face à des problèmes de congestion réseau au quotidien. Pour y répondre, nous avons remplacé notre algorithme de compression, passant de LZ4 à zstd. Nous avions déjà expérimenté la compression zstd auparavant, mais nous avions alors constaté une utilisation CPU plus élevée. Nous avons donc pris soin de suivre les métriques pour nous assurer que le compromis en valait la peine.

Dans un premier temps, nous avons déployé ce changement sur quelques serveurs. À notre grand soulagement, nous n'avons observé aucune différence notable dans l'utilisation du CPU.

Avec davantage de confiance, nous avons progressivement déployé ce changement sur l'ensemble de notre flotte, ce qui n'a montré, là aussi, qu'un impact minime sur les CPU. Au final, nous avons obtenu une réduction de près de 40 % du débit de trafic compressé. Le volume d'octets non compressés a continué de croître au même rythme, ce qui signifie que nous pouvions supporter plus de 1,5 fois le volume de trafic avec un tuyau de même taille. Autrement dit, les réductions estimées, en équivalent de croissance, nous ramenaient à environ 10 mois en arrière.

Aujourd'hui, en 2026, nous avons tenté trois stratégies pour réduire le nombre d'octets non compressés (et donc d'octets compressés).

### Répartition de charge
Pour rendre les analytics résilients face aux sinistres régionaux, nos systèmes exigent que les données redondantes soient stockées dans plusieurs régions centralisées (les données soumises aux Customer Metadata Boundaries sont, elles, stockées strictement dans leur région désignée). Historiquement, la façon la plus simple d'assurer cette résilience était la double écriture : Logfwdr transmettait deux copies complètes de chaque événement analytique non régional — une vers chaque région centralisée. Chaque région traitait ensuite indépendamment une copie complète jusqu'à ClickHouse. Nous appliquons également de l'échantillonnage (sampling) dans chaque région, une technique incroyablement scalable qui fonctionne pour tous les volumes de données, quelles que soient les conditions de trafic. Nous sous-échantillonnons le trafic à fort volume tout en préservant les événements rares.

Cette infrastructure restait gérable lorsque seule une poignée de flux utilisait des régions secondaires. Cependant, à mesure que nous avons étendu la résilience aux sinistres à la quasi-totalité des flux analytiques, le trafic de Logfwdr a doublé sur l'ensemble du système. Envoyer chaque événement deux fois sur un transit longue distance était insoutenable face à notre croissance exponentielle du trafic.

Nous avions déjà résolu un défi similaire pour Logpush. Pour Logpush, Logfwdr traite les centres de données centralisés comme un pool unifié et partagé de récepteurs : chaque message n'est envoyé qu'à une seule région, avec bascule (failover) vers une autre destination si une machine ou une installation est inaccessible. Ce modèle avait déjà fait ses preuves lors d'incidents majeurs, en déplaçant le trafic sans accroc d'un site à un autre sans intervention humaine. Cette bascule automatique était possible car la livraison de Logpush est sans état (stateless), les destinations clientes ne se souciant pas de savoir quel centre de données centralisé pousse les logs.

Les analytics étaient plus délicats. Contrairement aux logs sans état, les clusters ClickHouse des deux régions ont toujours besoin d'une copie complète des données non régionales pour permettre une bascule de requêtes instantanée et indépendante. La percée a consisté à découpler le transit du pipeline de la redondance en base de données :

**1. Pool d'ingestion partagé :** nous avons adopté le modèle de Logpush pour les flux analytiques. Logfwdr envoie chaque événement exactement une fois sur le transit longue distance, vers n'importe quel récepteur centralisé disponible.

**2. Réplication tardive depuis les régions centralisées :** plutôt que de répliquer le trafic à la source, la réplication intervient le plus tard possible dans le pipeline. Les données arrivent dans notre couche de mise en tampon distribuée, Buftee, et des inserteurs distants (remote inserters) diffusent en aval les copies inter-centres de données.

**3. Gestion résiliente des pannes :** si une région centralisée tombe en panne, les Logfwdr acheminent immédiatement tout le trafic non régional vers la région survivante. Si la connexion entre centres de données a un problème temporaire, chaque cluster continue d'ingérer sa part locale sans contre-pression (backpressure) ; les inserteurs distants se remettent à niveau à partir du tampon de rétention de Buftee une fois que le backbone est rétabli.

Pour les jeux de données migrés, cette bascule a éliminé environ 43 Go/s de trafic de transit compressé, tout en n'ajoutant qu'environ 7 Go/s de réplication inter-centres de données sur notre pipeline. Deux facteurs architecturaux expliquent cette asymétrie :

1. **La réplication intervient après l'échantillonnage** : dans l'ancien modèle, les Logfwdr transmettaient deux copies d'événements bruts, non échantillonnés, sur le transit longue distance. Dans le nouveau modèle, les Logfwdr envoient une seule copie aux récepteurs centralisés, qui appliquent immédiatement l'échantillonnage avant la mise en tampon dans Buftee, qui ne transporte ainsi que ce flux déjà compacté.

2. **Une meilleure compression grâce à un partitionnement uniforme** : à la source, les données sont fragmentées sur des milliers de serveurs individuels. Après centralisation, les flux sont agrégés et partitionnés en lots uniformes sur des fenêtres temporelles plus larges. Cette uniformité structurelle permet aux algorithmes de compression d'atteindre des taux de compression nettement plus élevés que ce que les lots de transit de Logfwdr ne pourraient jamais obtenir.

Au global, il s'agit d'une réduction nette de 36 Go/s sur les réseaux longue distance. Nous avons déployé cela initialement sur deux jeux de données, HTTP analytics et Ready-Analytics, notre produit d'analytics en un clic développé en interne.

Nous migrons activement d'autres jeux de données vers cette architecture équilibrée par répartition de charge depuis le printemps.

### L'échantillonnage dès le départ
Une autre stratégie que nous avons employée a consisté à étendre encore notre mécanisme d'échantillonnage afin de déplacer le traitement critique plus tôt dans le pipeline. L'échantillonnage était déjà utilisé dans nos services centralisés, en particulier les récepteurs, ce qui soulageait la pression sur les systèmes en aval. Nous pouvons être plus efficaces en ressources si nous envoyons moins de données en aval (sans sacrifier la qualité des données).

La solution ici a simplement consisté à échantillonner directement dans Logfwdr, en plus de maintenir l'échantillonnage dans les récepteurs centralisés. Pour résumer le fonctionnement de l'algorithme d'échantillonnage : chaque jeu de données dispose d'une clé que les équipes productrices ont choisie pour indexer et échantillonner les données. Lors de l'échantillonnage, nous mélangeons d'abord (shuffle) les enregistrements de chaque clé pour éliminer tout biais. Ensuite, pour chaque groupe d'enregistrements, nous sélectionnons une taille d'échantillon égale à la racine carrée du nombre total d'enregistrements. Le résultat est un échantillon représentatif, qu'il soit échantillonné une ou deux fois. Pour produire des estimations, nous mettons les calculs à l'échelle en fonction du taux d'échantillonnage. Par exemple, si nous échantillonnons 10 enregistrements sur 100, le taux d'échantillonnage est de 10/100, et l'estimation non biaisée du nombre total serait de 10*10 = 100.

Pour s'assurer que cette approche fonctionnait bien, nous avons comparé le nombre de lignes écrites dans ClickHouse à la somme estimée du nombre total, en utilisant diverses clés sur diverses empreintes de trafic, de sorte que les clés « les moins vues » comme les clés « les plus vues » soient couvertes sur tout le spectre.

Le résultat est que, pour les clés comportant davantage de données, le taux d'échantillonnage diminue. En revanche, les clés comportant moins de données étaient échantillonnées de façon comparable. Nous avons ainsi conservé un échantillon représentatif tout en livrant et en stockant moins d'événements. Nous ne compromettons pas la qualité des données livrées, même lorsque nous en livrons moins en quantité.

Si l'on regarde cela de plus près, à l'aide de lois de puissance, on observe que la courbe doublement échantillonnée (en rouge) croît selon environ x^0,319, contre x^0,485 pour l'échantillonnage simple / le groupe de contrôle (en bleu). Autrement dit, une clé comportant 100 fois plus de données qu'une autre aurait stocké environ 10 fois plus de lignes avec un échantillonnage simple. Désormais, elle ne stockera plus qu'environ 4 fois plus de lignes. Concrètement, un total de 11,6 millions d'événements est désormais représenté par 18 000 lignes dans ClickHouse, contre 79 000 auparavant. Le double échantillonnage atténue le stockage des clés « les plus vues », tout en conservant le même niveau de détail par événement pour les clés « les moins vues ».

Nous avons d'abord mis en œuvre cette stratégie sur trois de nos principaux jeux de données. Chacun d'entre eux a vu son volume de données compressées envoyées sur le réseau vers les récepteurs centralisés réduit d'au moins moitié. Cela représente 25 Go/s au total, soit plus de 2 Po/jour.

### L'agrégation
Cloudflare propose plusieurs jeux de données analytiques construits sur des rollups : des agrégats des événements bruts calculés au moment de l'ingestion. Cela constitue le compromis inverse de l'échantillonnage : plutôt que de répondre de façon approximative à n'importe quelle question, nous répondons de façon exacte à un ensemble fixe de questions, à condition de choisir les dimensions et les métriques en amont.

Par exemple, dans le jeu de données HTTP, nous mesurons le nombre d'occurrences uniques d'adresses IP au cours d'une minute donnée, plutôt que les IP individuelles elles-mêmes. Autre exemple : nous additionnons le nombre total de requêtes GET, POST, PUT, etc. pour un domaine donné, pour cette minute, regroupées par méthode HTTP. Aucun de ces calculs ne nécessite réellement d'attendre la toute fin du pipeline pour commencer.

Historiquement, cette agrégation intervenait vers la fin du pipeline, à l'intérieur des inserteurs qui lisent depuis Buftee et insèrent dans ClickHouse. Décentraliser cette agrégation était l'occasion de répartir la charge et de réduire le volume de données que nous centralisons.

Nous avons donc construit une fonctionnalité d'agrégation utilisée à chaque étape, créant des occasions répétées de combiner des agrégats partiels correspondants au fur et à mesure que les données convergent. Tout comme pour l'échantillonnage, les enregistrements sont regroupés par une clé, qui détermine quels enregistrements peuvent être combinés. Nous agrégeons sur chaque instance de Logfwdr. Nous agrégeons à nouveau une fois que les événements partiellement agrégés atteignent les récepteurs centralisés, qui poussent ces événements ré-agrégés vers des tampons dédiés et partitionnés. Comme ces tampons réunissent des enregistrements provenant de plusieurs récepteurs, nous agrégeons une fois de plus après qu'ils ont été lus par lots par les inserteurs ClickHouse. Enfin, nous agrégeons dans ClickHouse à l'aide de moteurs de tables agrégeantes (aggregating table engines).

Le premier jeu de données sur lequel nous avons déployé cela était le trafic HTTP. Sur ce seul jeu de données, nous sommes passés de plus de 9 Go/s à moins de 2 Go/s de trafic en octets compressés. Bien qu'il s'agisse actuellement du jeu de données à la cardinalité la plus élevée, les agrégations ont malgré tout permis une réduction d'environ 80 % sur le réseau.

Cette fonctionnalité d'agrégation est particulièrement puissante pour les jeux de données qui peuvent se « compresser » facilement, notamment pour des cas d'usage comme les métriques d'utilisation, où la précision des sommes et des comptages est primordiale. Cela signifie également que nous pouvons offrir aux équipes productrices une autre option, en plus de l'échantillonnage, pour réduire leur utilisation de ressources — ce que nous avons fait. À l'image de Ready-Analytics, nous avons créé un produit d'agrégation analytique générique, développé en interne et en un clic, appelé Ready-Aggregates. En continuant à itérer sur cette nouvelle fonctionnalité du pipeline, nous nous attendons à voir les économies continuer de s'accumuler.

### Impact
La preuve la plus frappante de cette croissance exponentielle est la rapidité avec laquelle la croissance du trafic consomme la marge disponible.

Prenons l'exemple de Ready-Analytics, où deux des trois mécanismes — la répartition de charge et les techniques d'échantillonnage — ont été appliqués. À la mi-mai, la répartition de charge a fait chuter le trafic de 50 %, passant d'environ 26 Go/s à environ 13 Go/s. Deux mois plus tard, le trafic avait déjà recommencé à grimper, atteignant environ 20 Go/s. Cela représente environ la moitié de la réduction, effacée par la croissance organique du trafic. Nous avons ensuite créé encore davantage de marge en réduisant le débit de ce jeu de données à un chiffre unique, environ 8 Go/s, lors du déploiement de l'échantillonnage.

Sans ces deux interventions, Ready-Analytics seul aurait dépassé les 60 Go/s dès septembre. En traitant moins de données dans les centres de données centralisés, nous économisons également une quantité significative de CPU et de mémoire. Les graphiques suivants montrent l'impact de la répartition de charge et de l'échantillonnage dans Logfwdr sur l'utilisation CPU et mémoire des seuls récepteurs de Ready-Analytics : une réduction d'environ 50 %, récupérant environ 750 CPU et 3,5 Tio de mémoire.

Sur l'ensemble du pipeline, du printemps à l'automne, la répartition de charge (~38 Go/s économisés), l'échantillonnage (~25 Go/s économisés sur les principaux jeux de données) et l'agrégation (~7 Go/s et plus à ce jour) ont permis d'éliminer environ 70 Go/s de trafic compressé de notre backbone. Ces chutes brutales apportent un soulagement immédiat.

Si l'on prend du recul en se projetant cinq ans dans le futur, les changements réalisés cette seule année auront autant d'impact que les bénéfices à court terme. Nous avons divisé par deux le volume de données que nous aurions eu à traiter dans encore une demi-décennie. Les optimisations structurelles et algorithmiques que nous avons mises en œuvre, et que nous continuerons à mettre en œuvre, sont essentielles pour maintenir des besoins matériels soutenables.

Si vous souhaitez nous aider à résoudre ces défis à grande échelle, nous recrutons !

## Pourquoi ça compte
Ce retour d'expérience offre un cas d'école concret sur la maîtrise des coûts d'infrastructure data à très grande échelle, avec des techniques directement réutilisables (découpage de schéma, choix de compression, mathématiques de l'échantillonnage, agrégation incrémentale, failover sans état) pour toute équipe confrontée à une croissance de trafic plus rapide que son budget matériel.
