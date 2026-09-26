---
title: "Why AI Clouds Need a Tiered Storage Architecture"
date: 2026-09-26
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.backblaze.com%2Fblog%2Fwhy-the-best-ai-clouds-dont-run-on-flash-alone%2F%3Futm_source=tldrai/1/010001a0d8c27fe0-6c9b409a-b363-4068-b435-524fdf752c58-000000/4vP9Jarf-uE4pVMyfSginqjHku2zWDPn2OuSrRR8bQ0=452"
keywords: ["stockage", "IA", "GPU", "neocloud", "hyperscaler", "flash"]
theme: "Tech"
tone: "opinion"
used_in: ["2026-09-26"]
---

## Résumé
Cet article de blog Backblaze explique que les neoclouds, bâtis autour de GPU alimentés en stockage flash très rapide, gèrent mal les étapes de leur cycle de vie IA qui n'ont pas besoin de cette vitesse (ingestion, checkpoints, sorties). En redirigeant ces données vers le stockage objet des hyperscalers, ils s'exposent à l'effet de « gravité des données » et à des frais de sortie (egress) prohibitifs, qui finissent par transférer toute la relation client à l'hyperscaler. La solution proposée est une architecture de stockage à plusieurs niveaux, avec du flash réservé à l'entraînement actif et un stockage à haute capacité (comme B2 Neo, disponible en marque blanche) pour le reste, afin que le neocloud conserve la totalité du compte client plutôt que le seul contrat GPU.

## Points clés
- Les GPU vendus par les neoclouds ne valent que ce que vaut le débit de données qui les alimente ; le flash ne sert réellement qu'à l'entraînement actif, pas à l'ensemble du cycle de vie IA.
- Cinq étapes du cycle de vie (ingestion des données, entraînement actif, checkpointing, sorties/outputs, inférence) ont des profils de stockage très différents ; seul l'entraînement actif exige du flash.
- Le checkpointing peut nécessiter la capture de 15 To de données en moins de 5 secondes, répétée toutes les quelques minutes, en continu.
- Envoyer les données non-flash vers les hyperscalers expose les neoclouds au piège de la « gravité des données » et à des frais de sortie (egress) prohibitifs qui verrouillent le client.
- Google, Meta et Microsoft exploitent des architectures de stockage à plusieurs niveaux depuis des années ; les neoclouds peuvent désormais reproduire cette logique via des offres en marque blanche comme B2 Neo (Backblaze).
- Le prix des SSD a augmenté de 257 % en moins d'un an, rendant l'absence d'un niveau de stockage intermédiaire de plus en plus coûteuse à ignorer.

## Analyse approfondie
Les neoclouds sont conçus autour des GPU, et les GPU ne peuvent fonctionner qu'à la vitesse à laquelle les données leur parviennent. Aux vitesses qu'exige l'entraînement de l'IA, les solutions de stockage cloud conventionnelles ne peuvent pas suivre.

C'est là qu'intervient le stockage flash. Le flash est rapide et fiable, conçu spécifiquement pour les charges de travail qui nécessitent une livraison des données à vitesse extrême et à faible latence. Mais une grande partie du travail de stockage qui entoure l'entraînement actif — sauvegarder les checkpoints, stocker les datasets, conserver les modèles terminés — n'a pas besoin de la vitesse du flash (ni de ses prix).

C'est un problème pour les neoclouds. Leur infrastructure est construite autour du flash. Ainsi, pour le stockage qui n'a pas besoin de flash, ils orientent souvent leurs clients vers des solutions de stockage objet chez les hyperscalers. C'est moins cher, ça fonctionne, et cela permet au neocloud de rester concentré sur ce qu'il fait de mieux.

Le problème, c'est la gravité des données (data gravity) : plus vous stockez de données quelque part, plus il devient difficile de partir. Les hyperscalers aggravent délibérément ce phénomène. Ils vous laissent entrer vos données gratuitement, mais facturent des frais de sortie (egress) prohibitifs pour les récupérer. Ainsi, une fois vos données ancrées sur la plateforme d'un hyperscaler, le coût du départ ne cesse d'augmenter. Et là où résident vos données, c'est aussi là que vous avez tendance à acheter davantage de services. Résultat : pendant que le neocloud continue d'être payé pour le calcul GPU, l'hyperscaler prend discrètement le contrôle du compte dans son ensemble. Ce qui a commencé comme une décision de stockage raisonnable finit par laisser l'hyperscaler s'approprier tout, sauf le contrat GPU.

Cet article explique comment une décision de stockage raisonnable peut progressivement livrer un client à un hyperscaler, et comment une architecture de stockage à plusieurs niveaux — avec du flash là où il a sa place et un stockage à haute capacité moins cher partout ailleurs — permet aux neoclouds de se battre pour la totalité du compte.

### Chaque étape du cycle de vie a un profil de stockage différent

Pour comprendre pourquoi le flash seul ne suffit pas, il est utile de passer en revue ce dont chaque étape du cycle de vie de l'IA a réellement besoin en matière de stockage.

- Tout commence par l'**ingestion des données**. Avant le début de l'entraînement, les datasets bruts doivent être nettoyés, étiquetés et préparés. Cette étape nécessite un stockage à haute capacité capable de déplacer efficacement de gros volumes de données. La vitesse compte, mais pas au point de rendre le flash indispensable.
- L'**entraînement actif** est l'étape où le flash trouve pleinement sa place. Les données transitent par plusieurs niveaux de stockage avant d'atteindre le GPU, mais à cette dernière étape, le modèle a besoin qu'elles soient livrées en continu et à très grande vitesse. Seul le flash est assez rapide pour maintenir des milliers de GPU en fonctionnement sans interruption.
- Le **checkpointing** s'exécute tout au long de l'entraînement. Comme l'entraînement de l'IA est un processus synchrone où chaque nœud du cluster travaille en parfaite coordination, la défaillance d'un seul composant peut arrêter l'intégralité de l'exécution de l'entraînement. Et à l'échelle d'un grand cluster moderne, les pannes ne sont pas rares — leur taux augmente même de façon exponentielle avec la taille du cluster. Les checkpoints sont la solution : des instantanés fréquents de l'état actuel du modèle qui permettent de reprendre l'entraînement là où il s'est arrêté. À grande échelle, un checkpoint peut nécessiter de capturer 15 To de données en moins de cinq secondes, répété toutes les quelques minutes, 24 heures sur 24. Cette étape exige un stockage suffisamment rapide pour suivre ce rythme, et suffisamment fiable pour ne rien perdre.
- Une fois l'entraînement terminé, les **sorties** — poids du modèle, journaux et métadonnées — sont placées dans un stockage à plus long terme. Les expériences de fine-tuning et les entraînements supplémentaires s'y ajoutent au fil du temps. Cette étape a besoin de capacité et de durabilité, pas de vitesse.
- Enfin, l'**inférence** : servir un modèle déployé nécessite un accès répété et à la demande aux poids du modèle. Les volumes de données sont bien plus faibles qu'à l'entraînement, et si les déploiements sensibles à la latence peuvent encore bénéficier du flash, les besoins en stockage sont bien moins intensifs.

Le stockage flash n'est conçu spécifiquement que pour une seule de ces étapes (l'entraînement actif). À chaque autre étape, ce qu'il faut, c'est un niveau de stockage à haute capacité et économique — précisément ce que les neoclouds envoient actuellement chez les hyperscalers. (Le programme de certification de stockage de NVIDIA valide les solutions de stockage séparément pour chacune de ces étapes, reconnaissant qu'une architecture de stockage unique ne peut pas bien servir toutes ces étapes.)

### Le flash est le mauvais outil pour la majeure partie du travail

Le stockage flash est cher parce qu'il est conçu pour la vitesse. Mais vous payez cette vitesse, que vous en ayez besoin ou non. Utiliser du flash pour stocker des datasets, des checkpoints et des artefacts de modèles terminés revient à expédier tout son courrier en livraison de nuit alors que la majeure partie pourrait voyager par voie terrestre : vous payez une prime pour une capacité dont vous n'avez pas besoin.

Et il y a un second problème, au-delà du coût. Le flash immobilisé pour stocker des checkpoints et des datasets n'est plus disponible pour les GPU, or ce sont les GPU que les neoclouds vendent. Chaque téraoctet de flash mal utilisé est de la capacité retirée au produit principal.

L'économie a toujours favorisé une approche par niveaux : du stockage rapide là où la vitesse est nécessaire, et du stockage à haute capacité moins cher partout ailleurs. Google, Meta et Microsoft exploitent d'ailleurs des architectures de stockage à plusieurs niveaux depuis des années (l'équipe d'ingénierie de Meta décrit son approche en quatre niveaux explicites, chacun choisi pour la tâche qu'il accomplit le mieux).

Mais construire un niveau de stockage complet en dessous du flash est un chantier considérable, et la plupart des neoclouds sont, on le comprend, restés concentrés sur leur cœur de métier, le GPU. Avec des prix des SSD en hausse de 257 % en moins d'un an, cet écart est devenu trop coûteux pour être ignoré.

### Comment une pile de stockage à plusieurs niveaux correspond au cycle de vie

La solution consiste à suivre la même logique que les hyperscalers utilisent depuis des années : faire correspondre le stockage à la charge de travail, et non l'inverse.

Pour l'entraînement actif, le flash reste la réponse. VAST, WEKA et DDN prennent en charge ce niveau avec un stockage rapide, situé à proximité des GPU, qui permet à l'entraînement de tourner à pleine vitesse.

Pour tout le reste, B2 Neo peut combler l'écart. Les datasets y résident avant le début de l'entraînement. Les checkpoints s'y écrivent en continu pendant l'entraînement. Les poids de modèles terminés et les enregistrements s'y accumulent au fil du temps. Le stockage est rapide et durable, mais tarifé pour des charges de travail de capacité plutôt que pour des charges de travail flash. B2 Neo se connecte directement au niveau chaud (hot tier), de sorte que les données circulent entre les deux sans détour par un hyperscaler.

Le meilleur, c'est que le neocloud n'a rien à construire de tout cela. B2 Neo est disponible en marque blanche, déployé sous la propre marque du neocloud. Le client ne voit qu'une seule plateforme homogène ; ses données restent sur l'infrastructure du neocloud, du dataset brut jusqu'au modèle déployé, sans jamais transiter par un hyperscaler.

### Vue d'ensemble

Le flash est le bon stockage pour une seule étape du cycle de vie de l'IA. À chaque autre étape, c'est un outil coûteux pour une tâche qui n'en a pas besoin.

Les neoclouds qui ne couvrent que le niveau de l'entraînement actif laissent un vide, et les clients comblent souvent ce vide en envoyant leurs données à un hyperscaler. Une fois qu'elles y sont, les frais de sortie les y maintiennent. Le neocloud finit par céder la relation client dans son ensemble à celui qui détient les données.

La bonne nouvelle, c'est que combler cet écart ne nécessite de rien construire à partir de zéro. L'architecture à plusieurs niveaux que Google et Meta exploitent à grande échelle est aujourd'hui accessible aux neoclouds sous forme d'infrastructure en marque blanche.

Sur ce marché, le contrat GPU n'est qu'un point de départ. C'est la rétention des données qui permet de retenir le client.

*Vous butez sur un mur en essayant de faire évoluer votre infrastructure de stockage ? B2 Neo vous emmène jusqu'au bout, sans reconstruction nécessaire. Contactez-nous.*

## Pourquoi ça compte
Ce texte éclaire un enjeu stratégique souvent sous-estimé de l'infrastructure IA : la bataille pour la relation client ne se joue pas seulement sur le calcul (GPU) mais sur la localisation des données, un point clé pour quiconque suit les dynamiques concurrentielles entre neoclouds et hyperscalers.
