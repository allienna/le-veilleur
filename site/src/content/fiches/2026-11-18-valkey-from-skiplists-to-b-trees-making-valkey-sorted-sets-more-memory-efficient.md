---
title: "Valkey: From Skiplists to B+ Trees: Making Valkey Sorted Sets More Memory Efficient"
date: 2026-11-18
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fvalkey.io%2Fblog%2Ffrom-skiplist-to-b%2Btree%2F%3Futm_source=tldrdev/1/010001a1e96da0ec-0ccbff55-d502-446e-8501-982cb380bf12-000000/wU596TRLt6Ff-8mCpymLRZ4s3wFhJL96XGB_GmaSEuA=452"
keywords: ["bases de données in-memory", "Valkey", "structures de données", "optimisation mémoire", "B+ tree", "performance"]
theme: "Data"
tone: "research"
used_in: ["2026-11-18"]
---

## Résumé
Valkey 9.2 remplace la skiplist historique des sorted sets par une nouvelle structure appelée fbtree, un B+ tree à haut fan-out (61 voies) optimisé pour la charge de travail et l'allocateur mémoire de Valkey. Ce changement réduit le surcoût mémoire par membre de 36 à 43 % sur un test à 5 millions de membres (jusqu'à 109 Mo économisés), tout en augmentant le débit de certaines commandes comme ZADD (+105 %) et ZREM (+76 %). Le changement est purement interne : le comportement des commandes reste identique, seule la valeur renvoyée par OBJECT ENCODING passe de skiplist à btree. Valkey 9.2 est en phase release-candidate et l'équipe invite les utilisateurs à tester leurs charges réelles avant la disponibilité générale (GA).

## Points clés
- La skiplist coûtait environ 37 octets de surcoût (pointeurs + score) par nœud et provoquait de nombreux cache misses dépendants à cause d'allocations dispersées en mémoire.
- fbtree (Feature B+ Tree) utilise un fan-out de 61, des nœuds dimensionnés aux classes d'allocation jemalloc, des scores et membres packés ensemble, des « features » comparables en SIMD pour accélérer le choix de l'enfant, et des feuilles chaînées pour les scans séquentiels.
- Sur 5 millions de membres, le surcoût mémoire par membre chute de 50,3 o à 28,5-32,0 o selon l'ordre d'insertion (réduction de 36 à 43 %, jusqu'à 109 Mo économisés).
- ZADD et ZREM gagnent respectivement +105 % et +76 % de débit grâce à la structure moins profonde ; les opérations de plage et de recherche ponctuelle progressent plus modestement.
- Aucun changement fonctionnel pour les utilisateurs, à l'exception du résultat de OBJECT ENCODING (btree au lieu de skiplist) pour les grands sorted sets.
- Valkey 9.2 est en release candidate ; l'équipe encourage les tests avec des charges de travail réelles avant la GA.

## Analyse approfondie
Un sorted set peut consommer plus de mémoire à décrire l'ordre de ses éléments qu'à stocker les éléments eux-mêmes.
Dans Valkey 9.2, cela change : la skiplist est remplacée par une variante de B+ tree à haut fan-out appelée **fbtree**.
fbtree combine le haut fan-out et le stockage contigu d'un B+ tree classique avec plusieurs optimisations conçues pour la charge de travail de Valkey et son allocateur mémoire, notamment des recherches basées sur des « features », des recherches SIMD, des feuilles chaînées et des chemins rapides pour les insertions et les suppressions séquentielles. Dans un test à 5 millions de membres, cela a réduit le surcoût mémoire par membre de 36 à 43 %, économisant jusqu'à 109 Mo.
Voyons pourquoi ce changement a eu lieu et comment il fonctionne.

### Pourquoi remplacer la skiplist ?
Les grands sorted sets qui dépassent le seuil du listpack sont soutenus par une skiplist associée à une hashtable (les sorted sets plus petits utilisent une représentation compacte en listpack qui stocke les éléments de manière séquentielle dans une mémoire contiguë). La hashtable offre des recherches en O(1) par membre, tandis que la skiplist offre des recherches ordonnées en O(log n) par rang ou par score. Cette association est architecturalement simple, mais la skiplist entraîne un coût mémoire significatif. Elle stocke exactement un élément par nœud, dispersés en mémoire sous forme d'allocations séparées reliées par des pointeurs.

#### Surcoût mémoire
La skiplist de Valkey paie ce prix en mémoire brute. Chaque nœud porte un pointeur arrière (8 o), plus une moyenne de 1,33 niveau de pointeurs avant et de valeurs de span, puisque les skiplists sont probabilistes (chaque nœud a 25 % de chances de gagner un niveau supplémentaire). Chaque niveau coûte 8 o pour le pointeur plus 8 o pour la valeur de span, ce qui donne environ 29 o de surcoût de pointeurs et de span par nœud. En ajoutant les 8 o du score, le total atteint environ 37 o par nœud avant même de compter la chaîne du membre.

#### Cache misses et récupérations dépendantes
Les CPU modernes utilisent une hiérarchie de caches matériels (L1, L2 et L3) pour garder les données fréquemment utilisées proches du processeur.
Ces caches sont beaucoup plus petits et plus rapides que la mémoire principale (RAM), donc lorsque le CPU ne trouve pas les données dont il a besoin dans son cache, il doit les récupérer depuis un niveau plus lent de la hiérarchie mémoire.
À titre d'illustration approximative, un hit dans le cache L1 peut prendre environ 1 ns, tandis qu'un accès à la DRAM peut prendre environ 100 ns.
Un accès mémoire dépendant peut laisser le cœur en attente ; la latence réelle et la part de travail qui peut être masquée varient selon le système et la charge de travail ¹.

Chaque nœud de la skiplist est une allocation séparée, potentiellement dispersée là où le tas (heap) a choisi de la placer, donc parcourir la structure peut nécessiter de récupérer de manière répétée des données depuis des emplacements mémoire sans rapport entre eux.
Comme chaque étape peut déterminer où va l'étape suivante, ces récupérations sont dépendantes, ce qui entraîne davantage d'aller-retours dans la hiérarchie mémoire.
Une étude de 2025 sur les index concurrents en mémoire a constaté que, sur les charges de travail testées, les skiplists traditionnelles subissaient environ 2,4 à 4,8 fois plus de cache misses qu'un B-tree comparable, avec un débit 2 à 8 fois plus faible ² (en testant différentes implémentations de structures de données, pas Valkey).

### Ce qui l'a remplacée : fbtree
Un B+ tree conserve les entrées triées dans des nœuds de taille fixe : les nœuds feuilles contiennent les entrées, ou des pointeurs vers elles, et les nœuds internes contiennent juste assez de données de routage pour choisir l'enfant dans lequel descendre. Regrouper de nombreuses entrées dans chaque nœud règle les deux problèmes ci-dessus : beaucoup moins de surcoût de pointeurs par membre, et beaucoup moins de récupérations dépendantes par recherche.

#### Disposition mémoire
fbtree, abréviation de Feature B+ Tree, utilise un fan-out à 61 voies : chaque nœud peut contenir jusqu'à 61 entrées ou pointeurs d'enfants.
Les nœuds feuilles et internes sont dimensionnés pour s'ajuster aux classes d'allocation de jemalloc sans gaspiller d'espace sur les builds 64 bits ; sur les builds 32 bits pris en charge, `innerNode` est arrondi à la classe de 1280 octets.

Une feuille de 512 octets contient jusqu'à 61 pointeurs de valeur, donc 61 membres partagent un seul nœud au lieu que chacun obtienne le sien. Plutôt que de stocker le score et le membre séparément, fbtree les stocke ensemble comme une valeur packée unique : le score normalisé sur 8 octets suivi des octets du membre. Cela garde ensemble les données nécessaires aux comparaisons et supprime un niveau supplémentaire d'indirection par pointeur.

#### Moins de récupérations mémoire
La règle des 25 % par niveau de la skiplist lui donne un facteur de branchement effectif d'environ 4, tandis que le fan-out de fbtree est de 61. Les deux structures conservent une complexité de recherche en O(log n), mais le B+ tree a nettement moins de niveaux à traverser et donc moins d'occasions de récupérations mémoire coûteuses.

Un CPU moderne peut aussi récupérer efficacement plusieurs lignes de cache adjacentes lorsque les données sont disposées de manière contiguë, grâce notamment à la façon dont la mémoire est accédée et au prefetching matériel ¹.
Un nœud de B+ tree qui s'étend sur quelques lignes de cache peut donc être lu efficacement pendant que le CPU parcourt son contenu.

#### Optimisations
Par-dessus cette structure, fbtree ajoute des optimisations visant des opérations spécifiques.

Dans un B+ tree indexé par des chaînes de longueur variable, comme les membres d'un sorted set, choisir un enfant signifie comparer la recherche à l'ancre de chaque enfant, le plus grand membre de cet enfant, et lire ces chaînes coûte des récupérations mémoire. Les nœuds internes de fbtree stockent chaque ancre avec une petite « feature » de quatre octets. Comme les ancres partagent souvent un préfixe commun, fbtree stocke ce préfixe commun séparément et utilise les quatre octets de feature pour distinguer les enfants. L'implémentation peut alors comparer ces features en parallèle grâce au SIMD, identifiant souvent le bon enfant avant même d'avoir récupéré le nœud enfant lui-même. Si les features identifient un enfant de façon unique, la recherche peut descendre immédiatement ; sinon, elles réduisent quand même la plage nécessitant une recherche binaire complète.

Les commandes de plage comme `ZRANGE` parcourent le set dans l'ordre.
fbtree relie ses nœuds feuilles dans une liste doublement chaînée, ce qui permet à un scan de passer d'une feuille à l'autre sans remonter dans l'arbre.
La skiplist demande un élément, attend de le recevoir, et ne connaît l'élément suivant à récupérer qu'une fois le premier reçu.
Le B+ tree peut travailler sur jusqu'à 61 éléments en parallèle, et pendant qu'il travaille sur ceux-ci, il peut récupérer le nœud feuille suivant avec les 61 éléments suivants.

Des commandes comme `ZPOPMIN` opèrent aux extrémités du set.
fbtree met en cache ses feuilles la plus à gauche et la plus à droite, donc les trouver est en O(1), comme dans une skiplist, plutôt qu'en O(log n).
Cela maintient les opérations de pop et d'ajout à parité plutôt que de les voir régresser.

Les suppressions de plage retirent une série contiguë de membres, et fbtree les gère sans reconstruire la structure environnante.

### Ce qui change réellement pour vous
Fonctionnellement, rien ne change.

Le changement est interne : les commandes des sorted sets et leur comportement restent inchangés.
La seule différence visible est que `OBJECT ENCODING` renvoie désormais `btree` au lieu de `skiplist` pour un grand sorted set.
Si vous avez du monitoring, des tests ou des outils qui vérifient la chaîne littérale `skiplist`, c'est un endroit à mettre à jour.
Les petits sorted sets sous le seuil du listpack ne sont affectés dans aucun des deux cas, puisqu'ils n'ont jamais utilisé l'encodage skiplist.

### Benchmarks

#### Efficacité mémoire
Les chiffres ci-dessous comparent uniquement l'index ordonné : skiplist contre fbtree, la hashtable et l'intégration des membres restant inchangées.

L'insertion séquentielle de 5 millions de membres de 20 octets a réduit le surcoût mémoire par membre, hors données du membre lui-même, de 50,3 o à 28,5 o, soit une **réduction de 43 %**.
Les mêmes 5 millions de membres insérés dans un ordre aléatoire ont réduit le surcoût par membre de 50,3 o à 32,0 o, soit une **réduction de 36 %**.

La réduction plus faible vient du fait que l'insertion aléatoire laisse davantage de nœuds partiellement remplis que l'insertion séquentielle.

Pour le set de 5 millions de membres de ce test, cela représente environ 109 Mo économisés avec des insertions séquentielles et 92 Mo avec des insertions aléatoires. Les économies sont par membre, pas par octet stocké, donc la réduction relative de la mémoire totale est maximale pour les sets comportant de nombreux petits membres et diminue à mesure que la taille des membres augmente.

#### Performance des commandes
Les benchmarks ci-dessous ont été mesurés sur la branche `oi/pr3-fbtree-v2` de la PR #4206 et n'ont pas été relancés pour le commit fusionné.
Ils ont été exécutés sur un système Graviton3 c7g.metal avec 64 cœurs, neuf threads d'E/S, une profondeur de pipeline de 10, et un sorted set de 3 millions de membres.
Chaque test a été répété cinq fois ; les intervalles de confiance rapportés étaient ≤ 2 % pour toutes les commandes sauf `ZRANDMEMBER`.

Les mêmes changements de conception sous-jacents améliorent aussi le débit pour plusieurs opérations sur les sorted sets :

| Commande | Charge de travail | Amélioration du débit |
|---|---|---|
| `ZADD` | Mise à jour de score (tous hits) | +105 % |
| `ZREM` | Ajout/suppression aléatoire 50/50 | +76 % |
| `ZCOUNT` | Comptage par plage de score | +27 % |
| `ZRANK` | Recherche de rang ponctuelle | +19 % |
| `ZRANGE` | Scan de rang sur 100 éléments | +6 % |
| `ZRANDMEMBER` | 100 échantillons aléatoires | +2 % |
| `ZSCORE` | Recherche de score ponctuelle | +2 % |
| `ZRANGEBYSCORE` | Scan de score sur 100 éléments | +1 % |
| `ZPOPMIN` | Pop du min + ajout d'un nouveau membre | ~0 % |

`ZADD` et `ZREM` repositionnent des éléments dans l'arbre, ils bénéficient donc le plus de la structure moins profonde de fbtree et de la réduction des mises à jour de pointeurs.
Les opérations de plage voient des gains plus faibles car, une fois que la traversée de l'index devient peu coûteuse, produire et renvoyer les éléments demandés devient une part plus importante du coût total.
`ZSCORE` et `ZRANDMEMBER` bougent à peine car elles utilisent la hashtable, pas l'index ordonné.

### Testez Valkey 9.2 avant la GA
Le point essentiel à retenir : **les commandes n'ont pas changé**, mais dans nos tests, les grands sorted sets ont présenté 36 à 43 % de surcoût en moins par membre, et le débit de `ZADD` et `ZREM` a augmenté respectivement de 105 % et 76 %.

L'objectif n'était pas simplement de rendre la structure de données plus rapide dans l'absolu : l'implémentation a été benchmarkée de façon répétée face à la skiplist existante à travers l'ensemble du serveur Valkey, avec des optimisations ajoutées jusqu'à ce que fbtree égale ou dépasse la skiplist sur toutes les commandes de sorted set testées.

Valkey 9.2 est actuellement en phase de test release-candidate.
Avant la GA, testez la release candidate 9.2 avec votre charge de travail réelle, en particulier si les grands sorted sets ou des commandes comme `ZADD`, `ZREM`, `ZRANK` ou `ZCOUNT` sont importantes pour vous.
Vos tests et retours peuvent aider à faire émerger des problèmes avant la sortie finale, donc ouvrez une issue si vous trouvez quoi que ce soit.

## Pourquoi ça compte
Pour qui surveille l'écosystème des bases de données in-memory (Redis/Valkey), ce changement illustre comment des optimisations bas niveau (structures de données, alignement mémoire, SIMD) peuvent apporter des gains de performance et de coût significatifs sans rupture de compatibilité applicative. C'est aussi un signal concret à suivre avant d'envisager une mise à jour en production vers Valkey 9.2.
