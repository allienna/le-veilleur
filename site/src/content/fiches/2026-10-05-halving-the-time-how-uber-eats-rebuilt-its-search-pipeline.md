---
title: "Halving the Time: How Uber Eats Rebuilt Its Search Pipeline"
date: 2026-10-05
url: "https://substack.com/redirect/18f44e95-9f50-460d-a024-f799ec12fef1?j=eyJ1IjoiN3Y1bG1jIn0.HlvPOGYPdVknSYzEK1JIj6IFkAFn8zuyjtfU9Mbft9Q"
authors: ["Nimish Sheth", "Daniel Cai", "Saurabh Kathpalia", "Vishnu Akhilesh Venkataraman", "Colin Schoen"]
keywords: ["latence", "recherche", "architecture logicielle", "Uber Eats", "classement (ranking)", "IA agentique"]
theme: "Tech"
tone: "research"
used_in: ["2026-10-05"]
---

## Résumé
L'équipe ingénierie d'Uber Eats détaille comment elle a divisé par deux la latence de son pipeline de recherche, en intervenant en parallèle sur l'UX, la récupération de candidats (retrieval), le classement (ranking), la diffusion publicitaire et l'infrastructure bas niveau. Les gains cumulés représentent plusieurs centaines de millisecondes, obtenus en supprimant des dépendances inutiles dans le graphe d'exécution, en découplant les données nécessaires au scoring de celles nécessaires à l'affichage, et en optimisant le format de stockage des données (encodage, colonnes, allocation mémoire). Une boucle agentique pilotée par un agent de codage IA a aussi permis de détecter et corriger automatiquement des inefficacités de production via un cycle mesurer → identifier → corriger → valider. L'article se termine sur une feuille de route (microbatching de bout en bout, recherche au niveau produit plutôt qu'item, filtrage précoce dans l'index, streaming de la page) visant une expérience de recherche encore plus rapide.

## Points clés
- Changement de métrique de référence : passage du temps de réponse API pur à l'« Above-the-Fold » (ATF), le temps jusqu'à l'affichage complet du premier écran de résultats avec images.
- Scission de l'hydratation monolithique en deux phases parallèles (signaux de classement vs attributs d'affichage), gain de 100+ ms.
- Suppression de stratégies de retrieval lexical à faible valeur ajoutée (-120 ms) et regroupement des items par produit via des embeddings pour réduire les lookups de données de plus de 100x (-50 ms).
- Refonte du stockage des données publicitaires en format orienté colonnes et mise en mémoire applicative (-130 ms cumulés sur la sélection et la préparation des enchères).
- Optimisations d'infrastructure « détails » (encodage parallèle des résultats, compression des embeddings, connexions réseau multiples, types valeur en Go) : environ -200 ms cumulés.
- Utilisation d'un agent IA autonome, doté d'outils d'observabilité et de benchmarking, pour détecter et corriger lui-même des goulots d'étranglement de latence en production.

## Analyse approfondie

### Introduction
Lorsqu'un utilisateur ouvre Uber Eats et tape une requête, il n'attend pas une réponse réseau : il attend de la nourriture. Chaque milliseconde de latence de recherche est donc une latence produit, qui affecte le taux de conversion, la profondeur de session et la décision même de commander. La latence du système de recherche d'Uber Eats avait atteint un niveau intenable. L'article explique comment l'équipe l'a réduite de moitié, via plusieurs chantiers menés en parallèle sur l'ensemble de la pile technique, et présente les évolutions architecturales en cours pour viser une expérience de bout en bout fluide et de premier plan dans l'industrie.

### Le problème
La phase de récupération (retrieval) remontait des dizaines de milliers de candidats, qui passaient tous par une hydratation complète avant que le classement (ranking) n'en élimine la plupart. L'hydratation était monolithique : une phase unique bloquant à la fois le classement et la présentation, exécutée en série. Le graphe d'exécution (DAG) contenait de fausses dépendances : certaines étapes attendaient des résultats dont elles n'avaient en réalité pas besoin, ce qui sérialisait des traitements qui auraient pu être parallèles. Résultat : un pipeline dont les goulots d'étranglement restaient invisibles tant qu'on ne les mesurait pas au bon niveau de granularité.

### Ce qui a été changé

#### UX
La latence de recherche est un problème de bout en bout, et certains des gains les plus importants sont venus d'une refonte de ce qui est envoyé à l'interface plutôt que de la seule vitesse de calcul.

L'équipe a remplacé sa métrique principale — le temps de réponse de l'API backend — par le temps « Above-the-Fold » (ATF) : le délai entre la soumission d'une requête et le moment où le premier écran de résultats est entièrement rendu, images comprises, dans la zone visible. En effet, la latence API peut s'améliorer sans que l'utilisateur perçoive de différence si le goulot d'étranglement se situe dans le transfert de la charge utile, le rendu des templates ou le chargement des images. L'ATF a donc forcé à optimiser l'ensemble du chemin.

Auparavant, chaque requête de recherche rendait l'intégralité du jeu de résultats avant que l'utilisateur ne voie quoi que ce soit. Une pagination a été introduite avec un cache côté serveur : la couche de présentation renvoie une première page plus petite, tandis que les résultats restants sont mis en cache pour les requêtes de défilement, évitant tout recalcul.

Le pipeline de rendu des templates HTML traitait chaque élément de résultat séquentiellement, si bien que le temps de rendu croissait linéairement avec la taille de la page. L'équipe est passée à un pipeline asynchrone où les éléments sont rendus de façon concurrente, et le service de présentation a été mis à l'échelle verticalement pour supporter ce parallélisme accru par requête. Le rendu asynchrone combiné à la pagination a permis un gain de plus de 200 millisecondes sur la latence ATF.

#### Retrieval
Une part importante de la latence de recherche provenait de la couche de récupération, où plusieurs stratégies de retrieval fonctionnaient en parallèle pour équilibrer précision et rappel.

Des analyses hors ligne et des expérimentations en production ont montré que plusieurs stratégies de retrieval lexical à large rappel ajoutaient une latence substantielle pour une valeur incrémentale faible : beaucoup des résultats pertinents qu'elles remontaient étaient déjà récupérés par d'autres sources, notamment les systèmes de retrieval sémantique. En supprimant ces chemins de retrieval à faible rendement, la latence de bout en bout a été réduite d'environ 120 millisecondes, sans régression mesurable sur la conversion ou la qualité des résultats.

L'efficacité a aussi été améliorée par une déduplication plus précoce des chaînes de magasins, réduisant le traitement en aval tout en ouvrant la voie à un ensemble plus large de résultats pertinents.

Enfin, l'efficacité de la récupération des features a été améliorée en s'appuyant sur des embeddings au niveau produit pour regrouper les items similaires autour d'un même produit. Ce regroupement par identité produit partagée a permis de réduire les accès aux données de plus de 100 fois, de diminuer la latence de retrieval de 50 millisecondes, et de rendre possible le service entier des données directement depuis la mémoire.

Pris ensemble, ces optimisations de retrieval ont nettement amélioré la réactivité de la recherche tout en préservant la qualité et la pertinence des résultats.

#### Population des features et classement (ranking)
Une source majeure de latence résidait dans du travail inutile et des points de synchronisation au sein du pipeline de classement. Historiquement, le classement attendait une phase d'hydratation monolithique des features, qui récupérait à la fois les signaux de classement et les données de présentation. Le classement ne pouvait donc démarrer qu'une fois tous les candidats entièrement hydratés, y compris des attributs d'affichage (prix, promotions, statut de stock) qui n'étaient pourtant pas nécessaires au scoring.

Pour résoudre ce problème, l'hydratation a été scindée en deux phases parallèles : l'hydratation de classement récupère uniquement les signaux nécessaires au scoring, tandis que l'hydratation de présentation récupère de façon asynchrone les attributs de la couche d'affichage. Cela a retiré des données non essentielles du chemin critique, permettant au classement de démarrer plus tôt et réduisant la latence de bout en bout de plus de 100 millisecondes. Cette scission a aussi créé une architecture plus propre, où les données de classement et de présentation peuvent évoluer indépendamment.

Le graphe d'exécution a également été audité pour éliminer les fausses dépendances accumulées au fil du temps : certaines étapes attendaient l'achèvement d'étapes précédentes sans réelle dépendance de données. La parallélisation du classement des items et de l'hydratation a réduit la latence d'environ 35 millisecondes. L'équipe a aussi travaillé avec l'équipe Search ML pour retirer les dépendances aux signaux d'items en temps réel du modèle de classement des magasins, permettant au classement des magasins et des items de s'exécuter indépendamment, avec un objectif de 20 millisecondes supplémentaires.

Pour réduire la latence de queue (tail latency), une technique de « hedging » de requêtes a été introduite sur quatre couches de dépendances d'hydratation de présentation : lorsqu'une requête dépasse un seuil de latence, une requête dupliquée est envoyée à une autre instance, et la réponse la plus rapide des deux est utilisée. Comme la latence d'hydratation était principalement due à des à-coups isolés au niveau des shards plutôt qu'à des ralentissements corrélés, ce hedging s'est révélé très efficace, réduisant la latence d'hydratation agrégée de 40 millisecondes.

L'infrastructure de classement a également été modernisée avec du service de modèles sur GPU, un cache pour le modèle de pertinence, et une livraison de features plus efficace. Ces changements ont réduit la latence de scoring, diminué les coûts de service des modèles, et amélioré davantage la réactivité globale de la recherche.

Pour la suite, malgré de bons progrès sur l'hydratation des features en temps réel, l'équipe travaille à avancer dans le pipeline la récupération des features hors ligne. Aujourd'hui, celles-ci s'exécutent séquentiellement après l'hydratation des features temps réel et avant que le scoring du modèle ne puisse commencer ; l'objectif est de les exécuter en parallèle des autres activités d'hydratation, pour les retirer du chemin critique. Au-delà de l'ordonnancement, l'équipe optimise aussi l'agencement des données dans les systèmes de stockage sous-jacents pour réduire la dispersion (fanout), ainsi que la façon dont les tenseurs de features sont transférés vers le GPU avec un coût de transport minimal.

#### Diffusion publicitaire (Ads Serving)
Le sous-système publicitaire souffrait d'un problème d'agencement des données. Chaque requête traite des centaines d'enchères, chacune avec de nombreuses composantes de scoring. Les données étaient initialement stockées dans un format orienté ligne, qui répétait les métadonnées de chaque composante pour chaque enchère, créant une surcharge de sérialisation/désérialisation importante.

L'agencement des données a été repensé en une représentation orientée colonnes, mieux adaptée au pattern d'accès du scoring. Cela a réduit la surcharge mémoire ; en complément, toutes les données spécifiques aux publicités (campagnes, pacing, etc.) ont été déplacées en mémoire applicative, évitant un appel base de données. Cette amélioration de l'efficacité de traitement a permis d'économiser environ 30 millisecondes sur la sélection des publicités et 110 millisecondes sur la préparation des enchères.

Plusieurs cycles inutiles de sérialisation/désérialisation entre composants internes ont aussi été identifiés. Leur élimination a retiré 20 millisecondes supplémentaires de latence. Enfin, les champs de scoring non utilisés ont été filtrés avant transmission, réduisant encore les coûts de traitement.

L'ensemble de ces optimisations publicitaires a permis une réduction de latence de bout en bout d'environ 130 millisecondes.

#### Soigner les détails : réglage de l'infrastructure
Toutes les améliorations ne sont pas venues de changements architecturaux majeurs. Le profilage a révélé plusieurs inefficacités au niveau infrastructure qui, sans lien direct avec la logique de recherche, ont collectivement réduit la latence de bout en bout d'environ 200 millisecondes.

Lors du retour de larges ensembles de résultats, le système encodait chaque item séquentiellement, laissant la plupart des cœurs CPU inactifs. Les résultats ont été découpés en segments indépendants pouvant être encodés et décodés en parallèle, réduisant la latence de bout en bout de plus de 50 millisecondes.

Les embeddings ML, essentiels à la pertinence de la recherche, sont coûteux à récupérer à grande échelle. En réduisant la précision en virgule flottante à 5 décimales et en utilisant un encodage compact à longueur variable des entiers, la taille des embeddings a été réduite de 46 %, divisant par deux la latence des requêtes en base de données.

Le service mesh utilisait une seule connexion réseau par destination, avec un plafond fixe de requêtes concurrentes en vol. Les services à fort débit atteignaient silencieusement ce plafond, provoquant une mise en file d'attente des requêtes. L'ouverture de connexions parallèles multiples a éliminé ce goulot d'étranglement, réduisant la latence jusqu'à 53 %.

Enfin, en Go, les objets référencés par pointeur sont alloués sur le tas et doivent être nettoyés par le garbage collector — ce qui consommait plus de 40 % du CPU sur certains services. En passant les définitions de modèles de données à des types valeur, ces objets sont désormais alloués sur la pile, ce qui réduit considérablement la charge du garbage collector et libère du CPU pour le traitement effectif des requêtes.

#### Boucle agentique
Un des chantiers les plus inattendus a consisté à utiliser une boucle d'IA agentique pour trouver et corriger directement des problèmes de latence. Un workflow a été construit où un agent de codage IA reçoit un objectif de gain de latence ainsi qu'un ensemble d'outils d'ingénierie personnalisés : la capacité d'extraire des profils de latence en production en direct, d'identifier les principaux goulots d'étranglement par span, de rédiger des correctifs de code pour les pistes les plus prometteuses, d'ouvrir des pull requests, et de lancer des benchmarks de latence pour valider les améliorations avant fusion. La boucle s'exécutait de façon itérative : mesurer → identifier → corriger → valider, en se répétant jusqu'à atteindre l'objectif de gain ou jusqu'à ce que le rendement marginal de chaque correctif supplémentaire tombe sous un certain seuil.

Un facteur clé a été la rapidité de la vérification : un investissement dans un cadre d'évaluation assisté par LLM a permis de valider rapidement que les améliorations de latence ne dégradaient pas la qualité de la recherche, réduisant drastiquement le temps d'évaluation et permettant à la boucle d'optimisation d'itérer beaucoup plus vite.

L'approche agentique s'est révélée particulièrement efficace sur une classe de problèmes individuellement peu spectaculaires mais qui s'accumulent de façon significative à grande échelle : travail redondant sur le chemin critique, émissions de métriques bloquantes plutôt qu'asynchrones, appels de configuration inutiles dans la boucle de requête, et motifs d'allocation sur le chemin chaud qui déclenchent des pauses de garbage collection. Ce sont le type de gains constamment présents dans les profils de production, mais qui finissent rarement sur une feuille de route.

L'intégration des benchmarks garantissait que chaque correctif disposait d'un résultat mesuré avant d'être fusionné — pas de spéculation, juste une boucle serrée entre observation, vérification et changement de code.

### Et après ?
Diviser la latence par deux n'était qu'une étape intermédiaire. L'objectif ultime (northstar) est une expérience de bout en bout de premier plan, un niveau que les référentiels de l'industrie montrent atteignable. Voici quelques-uns des paris en cours.

#### Microbatching de bout en bout
Aujourd'hui, le pipeline de recherche fonctionne par étapes : la récupération se termine avant que l'hydratation ne commence, et l'hydratation se termine avant que le classement ne commence. Cela crée des barrières de synchronisation où les shards rapides doivent attendre le shard le plus lent à chaque étape, amplifiant la latence de queue.

Pour résoudre ce problème, le pipeline de recherche est en cours de refonte avec du microbatching : les candidats commencent à circuler vers les étapes en aval dès qu'ils sont disponibles, permettant à la récupération, à l'hydratation et au classement de se superposer plutôt que de s'exécuter en séquence stricte.

En réduisant l'attente entre les étapes, la latence de bout en bout se rapproche de la latence moyenne des shards plutôt que d'être dictée par le shard le plus lent. Une réduction potentielle de plus de 100 millisecondes est estimée, avec en prime une variance de latence plus faible.

#### Recherche basée sur le produit
Aujourd'hui, la récupération et l'hydratation opèrent au niveau de l'item. Or, si le catalogue Uber Eats contient environ quelques milliards d'items, beaucoup sont des variantes spécifiques à un magasin d'un même produit sous-jacent. Au niveau produit, le catalogue se réduit d'environ 100 fois.

En faisant basculer la récupération et l'hydratation au niveau produit, la quantité de données traitées dans l'ensemble du pipeline de recherche est considérablement réduite. Les premiers tests ont déjà montré une réduction de plus de 50 % de la latence p99.

Un corpus plus petit permet aussi de récupérer davantage de candidats dans le même budget de latence, améliorant le rappel et créant de la marge pour des signaux de classement plus avancés. La recherche basée sur le produit améliore à la fois l'efficacité et la qualité des résultats, en faisant un élément clé de la trajectoire vers une recherche à plus faible latence.

#### ZPR (Zero Pass Ranking)
Aujourd'hui, la récupération rassemble un large ensemble de candidats, et le classement détermine ensuite lesquels valent la peine d'être conservés. Le ZPR (Zero-Pass Ranking) déplace une partie de ce filtrage directement au niveau de la couche d'index, permettant de scorer et de filtrer les candidats au moment même de leur récupération.

En éliminant plus tôt les candidats à faible valeur, le ZPR réduit la quantité de travail effectuée par les étapes d'enrichissement et de classement en aval. Le premier jalon vise environ 30 millisecondes de réduction de latence grâce à ce filtrage précoce, tandis que la vision à plus long terme pourrait débloquer 50 millisecondes ou plus.

Le ZPR complète également le microbatching, en permettant aux candidats de commencer à circuler plus tôt vers les étapes en aval et en réduisant davantage la latence de bout en bout.

#### Streaming
Aujourd'hui, la couche de présentation bloque jusqu'à la génération complète de la page avant d'envoyer quoi que ce soit : l'utilisateur d'Uber Eats attend que l'élément le plus lent soit rendu avant de voir le moindre résultat.

Avec le streaming via des réponses HTTP multi-part, le serveur transmet (flush) les fragments de résultats individuellement dès qu'ils sont disponibles. Le navigateur affiche immédiatement le contenu au-dessus de la ligne de flottaison, tandis que les résultats plus lents (cartes et carrousels en bas de page) arrivent ensuite en streaming. Là où la pagination réduisait la taille des réponses et le rendu parallèle réduisait le temps d'assemblage, le streaming de fragments supprimera l'obligation de tout rendre avant l'envoi puis le rendu côté client.

### Conclusion
Réduire la latence de recherche à l'échelle d'Uber a nécessité des améliorations sur l'ensemble de la pile technique. L'un des plus grands accélérateurs a été l'usage de workflows d'ingénierie agentiques : en combinant observabilité, génération de code, benchmarking et évaluation dans une boucle de rétroaction serrée, l'équipe a pu identifier, valider et déployer des optimisations beaucoup plus rapidement.

Tout aussi important a été l'investissement dans la mesure : extension de la couverture de tracing, construction de tableaux de bord de latence détaillés, et ajout de surveillance automatisée pour identifier rapidement les goulots d'étranglement et mesurer l'impact de chaque changement.

Le travail n'est pas terminé. Les prochains investissements suivent la même philosophie : faire moins de travail, démarrer le travail plus tôt, et mesurer en continu.

La latence a été divisée par deux. L'équipe a l'intention de recommencer.

*(L'article se conclut par des remerciements à de nombreux contributeurs internes et par les biographies des cinq auteurs : Nimish Sheth, Daniel Cai, Saurabh Kathpalia, Vishnu Akhilesh Venkataraman et Colin Schoen, tous ingénieurs seniors ou distingués chez Uber ayant travaillé sur la recherche et le paiement d'Uber Eats.)*

## Pourquoi ça compte
Ce retour d'expérience illustre comment une entreprise à très grande échelle combine refonte architecturale classique (découplage des phases, suppression de fausses dépendances, formats de données plus efficaces) et IA agentique pour chasser la latence de façon systématique — un cas d'école pour toute équipe de veille intéressée par l'ingénierie de recherche à grande échelle et par l'usage opérationnel des agents de codage IA en production.
