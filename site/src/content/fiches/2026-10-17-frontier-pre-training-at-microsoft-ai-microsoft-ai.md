---
title: "Frontier Pre-training at Microsoft AI | Microsoft AI"
date: 2026-10-17
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fmicrosoft.ai%2Fnews%2Ffrontier-pre-training-at-microsoft-ai%2F%3Futm_source=tldrai/1/010001a144e9b0a1-943e419d-218a-46a6-bdc6-c4e81ff9ef96-000000/x7V-IjW6radKMf3Fj-qTQ7j5OTqJ0a0wi9KWZC-h60Q=452"
keywords: ["pré-entraînement", "MoE", "Microsoft AI", "scaling laws", "Muon", "modèle de fondation"]
theme: "IA"
tone: "research"
used_in: ["2026-10-17"]
---

## Résumé
Microsoft AI présente MAI-Base-2, son nouveau modèle de fondation MoE (80 milliards de paramètres actifs, 2,8 billions au total), dont le pré-entraînement est achevé et qui entre désormais en post-entraînement. Le modèle surpasse tous les modèles à poids ouverts testés et serait 4,2 à 12,3 fois plus efficace en FLOPs que DeepSeek-V4-Pro-Base. L'article détaille les avancées techniques à l'origine de ce gain : échelles de scaling robustes (« source scaling »), nouvelles lois de scaling pour les hyperparamètres, MoE sans perte à chaque couche, optimiseur Muon re-partitionné et écrêtage du gradient d'activation, ainsi qu'un corpus de données organiques élargi incluant désormais la vision native. Microsoft insiste sur sa stratégie full-stack (modèle + infrastructure + données propriétaires) destinée à alimenter Foundry, et annonce que MAI-Base-3 est déjà en préparation.

## Points clés
- MAI-Base-2 : MoE à 80 milliards de paramètres actifs / 2,8 billions au total, entraîné sur 16 000 GPU GB200 pendant 38 jours (MFU moyen 21 %, goodput 89 %).
- Efficacité en FLOPs 4,2-12,3x supérieure à DeepSeek-V4-Pro-Base et 6,3-12,7x supérieure à MAI-Base-1.
- Innovations techniques clés : « source scaling » pour des scaling ladders fiables, nouvelles lois de scaling pour LR/WD/dropout, MoE sans perte (dropless) multi-rounds à chaque couche, optimiseur Muon re-partitionné, écrêtage du gradient d'activation.
- Données 100 % organiques (sans distillation d'autres modèles), corpus en hausse de 36 %, intégration native de la vision (VLM, 4,5T tokens uniques, 18 % du mélange d'entraînement).
- Stratégie commerciale : licencier les poids du modèle à des partenaires via Microsoft Foundry grâce à la traçabilité des données.
- MAI-Base-3 est déjà en préparation pendant le post-entraînement de MAI-Base-2.

## Analyse approfondie
En juin, nous avons annoncé MAI-Thinking-1, un modèle de fondation généraliste post-entraîné sur la base de MAI-Base-1 avec de solides performances de raisonnement. Nous avons récemment terminé le pré-entraînement de notre nouveau modèle de pointe, MAI-Base-2, un modèle de fondation MoE doté de 80 milliards de paramètres actifs et de 2,8 billions de paramètres au total.

MAI-Base-2 surpasse tous les modèles à poids ouverts que nous avons testés sur nos évaluations internes (held-out). Il est 4 à 12 fois plus efficace en FLOPs de pré-entraînement que le modèle de base ouvert le plus performant, DeepSeek-V4-Pro-Base (voir Figure 3), et nous avons réinvesti ce gain dans l'entraînement d'un modèle plus grand.

La Figure 1 montre les performances de MAI-Base-2 et d'autres modèles comptant au moins un billion de paramètres au total, sur un ensemble d'évaluations de pré-entraînement (plus bas est meilleur).

Posséder notre pipeline de modèles de bout en bout permet à Microsoft de proposer une offre distinctive à ses clients. Microsoft dispose d'une forte traçabilité des données (provenance) sur les tokens d'entraînement utilisés dans nos modèles. Notre pré-entraînement s'appuie sur des données organiques, sans distillation à partir d'autres modèles. Cela nous permettra de licencier les poids de nos modèles à des partenaires de confiance via Foundry, offrant aux entreprises une source fiable d'intelligence de classe mondiale répondant à leurs besoins.

Maîtriser l'ensemble de la pile nous permet d'optimiser conjointement nos modèles et notre infrastructure pour obtenir les meilleures performances au coût le plus bas, d'abord dans nos propres produits, puis pour les clients de Foundry. MAI-Base-2 est actuellement en phase de post-entraînement, et nous avons hâte de partager davantage de résultats prochainement.

### Comment se compare MAI-Base-2
Lorsque nous avons terminé l'entraînement de MAI-Base-1, la voie à suivre pour le pré-entraînement était claire : passer à l'échelle. Bien que MAI-Base-1 soit un modèle solide pour sa taille, il est plus petit que les modèles à poids ouverts et propriétaires à la pointe.

Trois initiatives ont été particulièrement importantes pour la réussite du pré-entraînement de MAI-Base-2 :
- Science du scaling : des échelles de scaling (scaling ladders) qui tiennent compte des données d'entraînement répétées, associées à des lois empiriques de scaling des hyperparamètres.
- Co-conception modèle-infrastructure : des implémentations améliorées de MoE et de Muon, ainsi que l'écrêtage du gradient d'activation.
- Scaling des données : des pipelines de données étendus et l'intégration de données visuelles.

MAI-Base-2 est un modèle plus grand et plus épars (sparse) que MAI-Base-1, entraîné sur davantage de données. Nous avons entraîné MAI-Base-2 sur 16 000 GPU GB200 pendant 38 jours, en août et septembre 2026. Au cours de l'exécution, le MFU moyen (model FLOPs utilization) était de 21 % et le goodput (la fraction du temps où l'entraînement progressait) de 89 %. Notre MFU est normalisé par rapport à 2,5 PFLOPS (le maximum théorique du GB200 en BF16) et exclut les FLOPs liés à la rematérialisation et à l'optimiseur.

Nous comparons les modèles pré-entraînés sur du texte held-out à l'aide du BPB (bits-per-byte), une métrique indépendante du tokenizer de chaque modèle. Pour le code held-out, nous utilisons la propre base de code de MAI, tandis que les évaluations STEM, Math et Q&A sont commandées à des prestataires externes afin de réduire le risque de contamination par les données d'entraînement. Nous avons par ailleurs décontaminé tous les ensembles d'évaluation par rapport à nos données d'entraînement.

Nous comparons MAI-Base-2 aux checkpoints de pointe disponibles avant octobre 2026 :
- DeepSeek-V4-Pro-Base est le modèle de base le plus capable à poids ouverts.
- Kimi K3, Qwen3.8-2.4T-A95B et MiMo-V2.6-Pro-RL sont des modèles à poids ouverts très performants. Seuls des checkpoints post-entraînés sont disponibles pour ces modèles. Nous rapportons leurs résultats en précisant que le post-entraînement peut affecter ces évaluations.

Sur l'ensemble de ces évaluations held-out, MAI-Base-2 obtient un BPB inférieur à celui des autres modèles testés. Nous détaillons ci-dessous quelques-unes des avancées qui ont rendu cela possible.

### Des échelles de scaling robustes
Nous évaluons les modifications de modèle à l'aide d'une échelle de scaling (scaling ladder), une famille de modèles de tailles différentes partageant une recette d'entraînement fixe. Chaque échelon de l'échelle porte le nom de son nombre de couches L, et L seul détermine le reste de l'architecture. Par exemple, la taille cachée est (256/3)·L, et le nombre de têtes de requête (query heads) est L, arrondi au multiple de 16 le plus proche. Nous entraînons des modèles de taille croissante en maintenant constant le nombre de tokens d'entraînement par paramètre actif (TPP, training tokens per active parameter).

Pour tenir compte de l'entraînement multi-époque aux petites échelles, nous utilisons une technique que nous appelons *source scaling*. Sur les échelons inférieurs de l'échelle de scaling, le source scaling restreint artificiellement l'ensemble d'échantillons uniques sur lequel le modèle s'entraîne, afin que chaque jeu de données soit répété le même nombre de fois quel que soit l'horizon d'entraînement. Par exemple, si un jeu de données est répété 8 fois sur l'ensemble d'une exécution de 50T tokens, une exécution de 5T tokens bouclera 8 fois sur seulement 1/10 de ces données.

À TPP fixe, le source scaling maintient effectivement constant le ratio entre données uniques et paramètres, ce qui contribue à garantir que les résultats se transposent harmonieusement entre les échelles. Sans source scaling, les expériences à petite échelle peuvent favoriser des choix d'architecture et d'hyperparamètres sous-régularisés qui sur-apprennent (overfit) aux grandes échelles. L'intégration du source scaling dans nos échelles a été déterminante pour passer de manière fiable à un modèle de 2,8T paramètres. La Figure 2 illustre l'utilisation d'une échelle de scaling pour prévoir avec précision la performance de MAI-Base-2.

### Isoler l'efficacité de modélisation du calcul
Les comparaisons directes entre modèles confondent la qualité de la recette d'entraînement avec les différences de taille de modèle et de calcul d'entraînement. Pour isoler la recette, nous estimons la quantité de calcul que notre recette nécessiterait pour égaler un modèle de base externe performant. Nous utilisons DeepSeek-V4-Pro-Base comme référence : c'est le seul checkpoint de pré-entraînement de base publié comptant plus d'un billion de paramètres, bien qu'il soit entraîné sur nettement moins de FLOPs que MAI-Base-2.

Pour chacune des quatre évaluations held-out de la Figure 1, nous ajustons une loi de scaling indépendante du BPB en fonction des FLOPs d'entraînement et estimons le calcul dont un modèle de notre échelle aurait besoin pour égaler le BPB de DeepSeek-V4-Pro-Base. La performance finale de MAI-Base-2 est connue, et nous l'incluons dans les ajustements, de sorte que le point de correspondance se situe dans la plage de nos modèles ajustés plutôt qu'au-delà. En comparant ces estimations au calcul d'entraînement de DeepSeek-V4-Pro-Base, nous constatons que notre recette est 4,2 à 12,3 fois plus efficace en FLOPs, comme le montre la Figure 3. Nous effectuons également la comparaison avec MAI-Base-1 et constatons que nos progrès depuis la sortie de ce modèle en juin dernier ont conduit à une amélioration de l'efficacité en FLOPs de 6,3 à 12,7 fois. Nous attribuons l'efficacité en FLOPs de MAI-Base-2 à la qualité et à la pertinence de nos données, ainsi qu'aux gains d'efficacité issus de nos choix de modélisation, tous deux décrits dans les sections ci-dessous.

### Lois de scaling pour les hyperparamètres
Sélectionner les hyperparamètres optimaux pour un entraînement à grande échelle est complexifié par l'espace combinatoire de l'optimisation des hyperparamètres, où la modification d'un hyperparamètre peut affecter la valeur optimale des autres. Pour MAI-Base-2, nous avons revu notre approche de ce problème.

Nous avons balayé conjointement le taux d'apprentissage (LR) et le weight decay (WD) car leurs effets sur l'entraînement sont couplés. La performance du modèle est surtout sensible au produit de LR et WD, de sorte que les bonnes configurations se situent dans une bande diagonale étroite du plan (log LR, log WD). Une grille rectangulaire dans (log LR, log WD) échantillonnerait cette bande de façon inefficace ; nous avons donc plutôt balayé une grille dans (log LR, log(LR × WD)).

Pour plusieurs combinaisons de taille de modèle et de TPP, nous avons entraîné des modèles le long de la grille de recherche et les avons évalués sur nos évaluations de pré-entraînement. Nous avons ajusté une fonction quadratique 2D aux évaluations et extrait le minimum analytique (LR*, LR* × WD*). La Figure 4 montre quelques coupes de cette expérience.

Nous avons ensuite modélisé log(LR* × WD*) et log LR* en fonction de la taille du modèle, du TPP, ou d'autres caractéristiques telles que le logarithme du nombre de pas (log steps). À l'aide de la sélection de modèle, nous avons constaté que LR* × WD* dépendait principalement du nombre de pas d'entraînement, tandis que log LR* dépendait en outre de log TPP. L'exposant empirique de LR* × WD* par rapport aux pas était très proche de −1, ce qui correspond à l'idée que l'échelle de temps du weight decay découplé (1/(LR × WD)) devrait être une fraction fixe de l'entraînement. L'exposant empirique du LR par rapport aux pas était proche de −0,5, ce qui correspond à la règle empirique largement utilisée selon laquelle, en doublant la taille de batch, il faut multiplier le taux d'apprentissage par √2. Nos lois de scaling finales pour LR* et WD* sont :

LR* × WD* = 17,04 / pas

log LR* = −1,51 + 0,175 log TPP − 0,573 log pas

En utilisant une approche similaire, nous avons également dérivé la loi de scaling suivante pour le dropout :

Dropout = sigmoid(0,526 × (log ParamètresActifs − 27,2))

Nous avons estimé nos nouvelles lois de scaling dans des expériences à petite échelle, puis les avons validées à une échelle intermédiaire, où elles ont systématiquement surpassé les heuristiques précédentes. Ces lois ont défini les hyperparamètres de MAI-Base-2.

### Co-concevoir notre infrastructure et MAI-Base-2
Entraîner des modèles de pointe dans les limites d'un budget de calcul nécessite de co-concevoir modèles et infrastructure, à la fois pour la qualité d'évaluation et l'efficacité computationnelle. Nous utilisons une métrique de gain d'efficacité (EG, efficiency gain) pour guider nos décisions : le ratio de calcul requis par un candidat pour atteindre la même perte d'évaluation que la référence. Le calcul peut être mesuré en FLOPs (EG_FLOPs) ou en temps réel (EG_time), les deux étant complémentaires. Nous nous appuyons principalement sur EG_time, car elle reflète l'état actuel de notre infrastructure. EG_FLOPs, de son côté, mesure le potentiel d'un prototype et guide le développement futur de l'infrastructure : un changement qui gagne en FLOPs mais perd en temps réel nous indique où investir. Cette optimisation conjointe de la modélisation et de l'infrastructure se retrouve dans plusieurs choix de conception présentés ci-dessous.

### Mise à l'échelle du MoE
Nos expériences de modélisation passées ont montré que le MoE à chaque couche présente un avantage constant en EG_FLOPs par rapport à l'alternance de couches FFN denses et de couches MoE. Cependant, des inefficacités dans notre implémentation du MoE faisaient que le MoE une couche sur deux était optimal en EG_time pour MAI-Base-1. Pour MAI-Base-2, nous avons identifié deux inefficacités à l'origine d'un MFU MoE sous-optimal :

1. Le routage dynamique augmentait la fragmentation mémoire et immobilisait davantage de mémoire pour des déséquilibres de charge d'experts rares et extrêmes, mémoire qui aurait pu autrement réduire le recalcul d'activation.
2. L'ajout d'experts plus nombreux et plus finement granulaires augmentait la surcharge par expert.

La résolution de ces inefficacités a fait passer le MFU de nos couches MoE de 24 % à 35 %, ce qui nous a permis d'adopter le MoE à chaque couche pour MAI-Base-2.

*MoE sans perte (dropless) à usage mémoire fixe et réglable*

Dans les couches MoE, chaque expert reçoit un nombre variable de tokens. Cela introduit des défis de mémoire GPU, les experts surchargés pouvant manquer de mémoire. Une solution consiste à fixer un seuil pour chaque expert, au-delà duquel les tokens supplémentaires sont abandonnés (dropped). Nos expériences ont montré que l'abandon de tokens dégrade les performances. Une solution naïve consiste à simplement allouer suffisamment de mémoire par expert pour absorber le plus grand déséquilibre possible, mais cela conduit à une utilisation inefficace de la mémoire en charge normale. Notre MoE sans perte multi-rounds, illustré en Figure 6, atteint un usage mémoire fixe quel que soit le déséquilibre de routage, éliminant la fragmentation et les plantages par manque de mémoire (out-of-memory).

Nous regroupons les experts de chaque rang parallèle d'experts en un ou plusieurs groupes de taille configurable. Chaque groupe d'experts exécute un ou plusieurs rounds de *dispatch → calcul → collecte* avec une capacité de tokens fixe par expert. Si un expert reçoit plus de tokens qu'il ne peut en contenir, le groupe d'experts traite ces tokens en excédent lors de rounds supplémentaires. Pour réduire le nombre de rounds supplémentaires, nous permettons aux experts surchargés d'utiliser la capacité de tokens inutilisée d'autres experts du même groupe. Lors de la passe arrière (backward pass), nous effectuons ensuite un recalcul fin par groupe d'experts, suivant un calendrier multi-rounds similaire. Cela maintient un usage mémoire statique indépendamment du déséquilibre des tokens. La capacité de tokens est configurable : plus de capacité signifie plus de mémoire, et moins de capacité signifie potentiellement plus de rounds, donc davantage de calcul. En pratique, la capacité est configurée pour maintenir un seul round en régime stable.

Les étapes *dispatch*, *calcul* et *collecte* sont pipelinées sur l'ensemble des rounds de tous les groupes d'experts, de sorte que tous les *dispatch* sauf le premier et toutes les *collectes* sauf la dernière se superposent au calcul des experts. Dans la passe avant (forward pass), la quantification des poids et le calcul des experts partagés se superposent à la communication exposée. Dans la passe arrière, toutes les communications d'experts sont entièrement superposées : le *dispatch* exposé en entrée se superpose au recalcul de la même couche, et la *collecte* exposée du gradient se superpose aux calculs de gradient des poids.

*Réduire la surcharge par expert*

Nous réduisons la surcharge par expert de quatre façons. Premièrement, nous améliorons l'efficacité des GEMM et de NVLink en regroupant à la fois le calcul et la communication pour chaque groupe d'experts. Cela réduit la surcharge de lancement des kernels et les effets de traîne (tail effects). Deuxièmement, nous réduisons la synchronisation hôte-device en utilisant des métadonnées de tokens résidant sur le device et en initiant la communication all-to-all directement depuis le GPU. Troisièmement, nous optimisons davantage l'all-to-all grâce à la mémoire symétrique, permettant d'échanger les tokens directement via NVLink sans copies intermédiaires, ce qui améliore le débit de communication et réduit la contention HBM lors de l'exécution simultanée de GEMM. Enfin, nous regroupons la perte d'équilibrage de charge (load-balancing loss) sur l'ensemble des couches, remplaçant les all-reduces par couche par une seule réduction groupée sur toutes les couches. Ces optimisations nous permettent d'entraîner des modèles plus épars sans dégrader significativement le MFU.

### Mise à l'échelle de Muon
En passant à l'échelle pour MAI-Base-2, nous avons constaté que Muon offrait une dynamique d'entraînement plus stable et des gains d'efficacité importants par rapport à AdamW. L'adoption de Muon pour nos plus grands modèles a nécessité de réduire sa surcharge par pas.

Muon orthogonalise le momentum de chaque matrice de poids avec Newton–Schulz, un algorithme itératif composé de plusieurs multiplications matricielles. Cela nécessite la matrice complète, ce qui entre en conflit avec le partitionnement (sharding) du momentum par ZeRO sur la dimension data-parallèle. En nous appuyant sur des travaux antérieurs, nous re-partitionnons (reshard) le momentum pendant l'étape de l'optimiseur. Chaque GPU met à jour son shard local de momentum en FP32 et le convertit en BF16. Un échange all-to-all, groupé par paramètres de même forme, attribue alors à chaque GPU la propriété d'un sous-ensemble de matrices de momentum complètes. Chaque GPU orthogonalise localement ses matrices de momentum complètes à l'aide d'un kernel Newton-Schulz tenant compte de la symétrie. Un second all-to-all renvoie les mises à jour vers leurs shards d'origine, où elles sont reconverties en FP32 et appliquées aux poids.

Nous appliquons en outre plusieurs optimisations bénéfiques à notre efficacité d'entraînement sur 16 000 GPU :
- Nous superposons communication et calcul en préchargeant (prefetching) plusieurs batches.
- Nous mettons en cache et réutilisons les métadonnées de re-partitionnement pour éviter une logique d'indexation répétée. Ceci est particulièrement utile dans les modèles MoE épars comportant des milliers de paramètres de forme identique.
- Certains poids sélectionnés, comme les poids du routeur MoE, sont répliqués sur tous les GPU plutôt que partitionnés. La première phase de communication est alors ignorée, et nous émettons à la place une opération collective all-gather après Newton-Schulz pour obtenir l'ensemble complet des mises à jour répliquées.

Après optimisation, Muon représentait 2,1 % (165 ms) du temps moyen d'une itération d'entraînement de MAI-Base-2. Nous avons suivi la qualité de notre implémentation et priorisé les changements sur la base de profils, en utilisant à la fois des configurations de test à grande et à petite échelle. Nous avons comparé les mesures issues des tests à la performance théorique maximale, que nous avons estimée à 55 ms et limitée par la communication pour la configuration finale d'entraînement de MAI-Base-2. Nous attribuons l'écart entre performance théorique et performance mesurée aux stragglers (GPU à la traîne), aux surcharges de dispatch des kernels, au déséquilibre de charge et aux copies/allocations mémoire pendant le re-partitionnement.

### Écrêtage du gradient d'activation
L'écrêtage de gradient (gradient clipping) est une méthode courante pour stabiliser l'entraînement en réduisant l'impact des gradients aberrants (outliers). L'écrêtage de gradient standard opère sur la norme globale du gradient des poids pour un batch entier. Cependant, les gradients aberrants sont généralement provoqués par une petite portion des données au sein d'un batch. Un outlier peut donc entraîner la réduction d'échelle des gradients de l'ensemble du batch, y compris les contributions d'exemples par ailleurs bien comportés. En guise de mitigation plus ciblée, nous écrêtons les gradients des activations à des endroits sélectionnés du réseau. Combiné à Muon, cela maintient la norme du gradient de MAI-Base-2 dans une plage bien plus restreinte que celle de MAI-Base-1 (Figure 7).

L'écrêtage du gradient d'activation a également rendu l'optimisation plus stable, et son bénéfice s'est accru avec l'échelle, comme le montre la Figure 8. À l'inverse, la plupart des changements que nous avons testés produisent un gain d'efficacité à peu près constant selon les échelles.

Nous utilisons également l'écrêtage du gradient d'activation comme outil de diagnostic pour valider nos données d'entraînement. La Figure 9 montre un exemple d'entraînement malformé identifié par l'écrêtage du gradient d'activation. Dans une pull request issue de nos données de code, un en-tête de licence est brutalement coupé en plein milieu d'une phrase. En retraçant cet exemple écrêté, nous avons découvert un bug dans notre pipeline de prétraitement, qui a depuis été corrigé.

### Mise à l'échelle des données
MAI-Base-2 suit les mêmes principes de données que MAI-Base-1 : notre voie vers la performance de pointe repose sur des données organiques, et non sur la distillation à partir d'autres modèles. Investir dans nos propres pipelines de données continue de porter ses fruits, et nous avons traité en interne chaque token d'entraînement. Notre corpus a crû d'environ 36 % entre MAI-Base-1 et MAI-Base-2, mesuré en tokens d'entraînement uniques (voir Figure 10).

Depuis MAI-Thinking-1, nous avons amélioré notre classification de qualité, le regroupement par sujet (topic binning), l'analyse web (web parsing), la déduplication et la décontamination des évaluations. Pour MAI-Base-2, nous avons étendu nos pipelines pour traiter sensiblement davantage de contenu web¹, avec une date de coupure des connaissances (knowledge cutoff) de mars 2026. Nous avons également utilisé un échantillonnage de diversité basé sur les embeddings pour prioriser les données nouvelles et réduire le contenu redondant. Nos expériences ont montré que ces approches amélioraient substantiellement la performance du modèle.

Contrairement à MAI-Base-1, MAI-Base-2 est pré-entraîné nativement avec de la vision, via une architecture VLM sans encodeur dédié (encoder-free). Nous avons donc investi massivement dans la croissance de notre corpus VLM, couvrant des paires image-texte et des documents mêlant texte et images. Le corpus couvre des tâches telles que le sous-titrage d'images issues du web, la compréhension de graphiques, l'ancrage visuel (visual grounding), le raisonnement spatial, la compréhension médicale, l'utilisation d'ordinateur (computer use), la lecture de partitions musicales, et d'autres domaines que nous anticipons utiles pour nos utilisateurs. Notre corpus VLM contient 4,5T tokens uniques et, avec répétition, les données VLM représentaient 18 % du mélange d'entraînement de 50T tokens.

### Et ensuite
MAI-Base-2 constitue la fondation de notre prochaine génération de modèles, dont nous sommes impatients de vous dire davantage prochainement. Pendant que MAI-Base-2 passe par le post-entraînement, les préparatifs pour MAI-Base-3 sont déjà en cours. Tous nos modèles sont construits selon les mêmes principes qui nous guident depuis MAI-Base-1 :
- L'intelligence doit être apprise à partir de principes premiers.
- Les méthodes simples sont celles qui passent le mieux à l'échelle.
- La rigueur scientifique plutôt que les raccourcis.

Nous avons la conviction que ces principes continueront à nous mener vers la frontière. Entraîner une IA de pointe exige que chercheurs et ingénieurs en modélisation, données et infrastructure travaillent comme une seule équipe. Si cela vous parle, nous recrutons !

¹ Pour les données web, nous utilisons un crawler propriétaire qui respecte le protocole d'exclusion des robots (robots.txt) ainsi que les balises meta et contrôles HTML associés, permettant aux propriétaires de sites de gérer l'accès et l'utilisation du contenu de leurs sites. Nous excluons également les sources qui violent les politiques d'IA responsable de Microsoft ou qui figurent sur la liste des « Notorious Markets » de l'Office of the United States Trade Representative (USTR).

### Construisez l'avenir avec nous
Nous sommes un laboratoire agile et rapide, composé de certains des esprits les plus talentueux au monde. Nous disposons d'une feuille de route de calcul ambitieuse chez MAI, qui monte en puissance rapidement et largement. Et nous portons une mission ambitieuse en laquelle nous croyons profondément. Nous avons également la chance de collaborer avec des équipes produit exceptionnelles, qui donnent à nos modèles l'opportunité d'atteindre des milliards d'utilisateurs et de créer un impact positif immense. Si vous êtes une personne brillante, très ambitieuse et sans ego, vous vous sentirez ici à votre place — venez nous rejoindre alors que nous travaillons sur notre prochaine génération de modèles !

## Pourquoi ça compte
Ce billet illustre la course à l'efficacité computationnelle (et pas seulement à la taille brute) chez les grands acteurs de l'IA, avec un niveau de détail technique rare sur l'ingénierie MoE, l'optimiseur Muon et les lois de scaling à très grande échelle. Il confirme aussi la stratégie de Microsoft visant à bâtir sa propre pile de modèles propriétaires pour alimenter Foundry, plutôt que de dépendre uniquement de partenaires externes comme OpenAI.
