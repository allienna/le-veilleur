---
title: "Introducing Olmo-core 3: Open, scalable training infrastructure for large MoEs | Ai2"
date: 2026-10-03
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fallenai.org%2Fblog%2Folmocore3%3Futm_source=tldrai/1/010001a0fccd7a72-672389f9-e11b-4cda-ac15-a4ea0d841b32-000000/fSC8K0TsLKvjZXOyFTcMpgis4W2XFeulU_4gyPP8URQ=452"
keywords: ["MoE", "infrastructure d'entraînement", "open source", "parallélisme", "Olmo", "GPU"]
theme: "IA"
tone: "news"
used_in: ["2026-10-03"]
---

## Résumé
Ai2 annonce Olmo-core 3, une refonte de son framework open source pour entraîner de grands modèles de langage, centrée sur un nouveau système d'entraînement pour les architectures de type mélange d'experts (MoE). L'objectif est de permettre à ces modèles de passer à l'échelle du trillion de paramètres tout en conservant une bonne efficacité de calcul. Ai2 publie à la fois le code, un rapport technique détaillant les choix d'architecture et les benchmarks, affirmant ainsi son engagement pour une IA ouverte où l'infrastructure d'entraînement est aussi transparente que les poids des modèles. Ce système servira de base à la prochaine génération de modèles Olmo, qui adoptera elle-même une architecture MoE.

## Points clés
- Olmo-core 3 remplace l'ancienne approche fondée sur le FSDP (fully sharded data parallelism) par un système basé sur le DDP (distributed data parallelism), qui garde les experts résidents sur les GPU plutôt que de réassembler les poids à chaque batch.
- Sur un benchmark, Ai2 a fait passer le nombre d'experts de 8 à 128 (en n'en activant toujours que 4 par token), multipliant la capacité totale du modèle de 4,6 à 47 milliards de paramètres, pour une baisse de débit inférieure à 5 %.
- Sur 8 GPU NVIDIA B300, le nouveau système atteint environ 52 000 tokens/seconde/GPU contre 19 400 avec l'ancienne implémentation FSDP, soit un gain de débit d'environ 2,7x.
- Le système combine parallélisme d'experts, parallélisme de pipeline et un optimiseur distribué, ainsi que des optimisations comme le routage « rowwise », le routage géré directement sur GPU et le regroupement des calculs matriciels (« grouped GEMM »).
- Le format numérique basse précision MXFP8 apporte un gain de débit d'environ 21 % par rapport au format BF16, tout en réduisant la mémoire active maximale de 103 à 95 GiB.
- Les tests de scalabilité ont atteint 1,2 trillion de paramètres totaux sur 512 GPU (858 TFLOP/s/GPU), et jusqu'à 2,38 trillions de paramètres dans un test de capacité à court terme utilisant DeepEP v2.

## Analyse approfondie
**Contexte et objectif.** Entraîner de grands modèles d'IA exige énormément de calcul, ce qui fait grimper les coûts et la consommation d'énergie, rendant le développement de modèles avancés difficile d'accès pour les laboratoires universitaires et les petites structures. Les architectures de mélange d'experts (MoE) offrent une piste d'efficacité : elles permettent d'intégrer beaucoup plus de paramètres appris sans que chaque entrée ait besoin de solliciter l'ensemble du modèle. Mais le modèle complet doit malgré tout être stocké et mis à jour sur l'ensemble de la mémoire GPU, et le fait d'orienter chaque token vers les bons experts à travers un cluster entraîne ses propres coûts de communication et de coordination. À mesure que les MoE grossissent, ces coûts peuvent annuler une bonne partie de l'avantage computationnel procuré par l'activation partielle du modèle. Olmo-core 3 a été conçu pour combler cet écart.

Dans un benchmark, Ai2 a fait passer le nombre d'experts de 8 à 128 tout en continuant à n'en sélectionner que quatre par token, maintenant ainsi le nombre de paramètres actifs par token à environ 3,2 milliards. La capacité totale du modèle est passée de 4,6 à 47 milliards de paramètres, pour une baisse de débit d'entraînement inférieure à 5 %. La même infrastructure a par ailleurs été testée au-delà du trillion de paramètres au total.

**Construire une architecture d'entraînement adaptée au fonctionnement réel des MoE.** Olmo-core a évolué au fil des générations successives d'Olmo. Les premiers travaux d'Ai2 sur les modèles « sparse » remontent à OlmoE, qui utilisait une architecture MoE avec 64 experts routés. Olmo 3, à l'inverse, reposait sur une architecture dense, où la quasi-totalité du modèle était active pour chaque token, et sa chaîne d'entraînement avait été conçue en conséquence. Olmo-core 3 étend désormais le framework avec un système d'entraînement pensé pour des MoE de bien plus grande taille.

L'implémentation MoE précédente d'Olmo-core reposait sur le fully sharded data parallelism (FSDP), configuré pour rassembler puis redistribuer les poids du modèle à chaque petit lot de données. Olmo-core 3 bascule vers un système fondé sur le distributed data parallelism (DDP) : les experts restent résidents sur les GPU, et ce sont les données pertinentes qui sont acheminées vers eux, ce qui évite ce rassemblement répété des poids.

Le Megatron-Core de NVIDIA constitue une solution établie pour entraîner de grands MoE. Olmo-core 3 apporte au framework d'Olmo une chaîne d'entraînement MoE intégrée, dont la refonte améliore le débit par rapport à l'ancienne implémentation fondée sur FSDP. Dans un test préliminaire sur huit GPU NVIDIA B300, un MoE de 47 milliards de paramètres a traité 52 000 tokens par seconde et par GPU avec la nouvelle chaîne, contre 19 400 avec l'ancienne implémentation — soit environ 2,7 fois le débit.

**Mettre à l'échelle et optimiser l'entraînement des MoE.** Olmo-core 3 combine plusieurs techniques de distribution des grands MoE sur des clusters de GPU, associées à des optimisations qui rendent le routage et le calcul plus efficaces.

Trois techniques déterminent la manière dont le modèle et son état d'entraînement sont répartis sur le matériel :
- Le parallélisme d'experts répartit les experts entre les GPU, de sorte que chaque GPU ne stocke qu'une partie du pool complet d'experts.
- Le parallélisme de pipeline répartit les couches du modèle — les étapes successives qui transforment une entrée — entre des groupes de GPU, réduisant la part du modèle que chaque GPU doit garder en mémoire.
- Un optimiseur distribué répartit l'état de l'optimiseur — les données supplémentaires utilisées pour calculer et appliquer les mises à jour pendant l'entraînement — entre les GPU, au lieu d'en stocker une copie complète sur chacun d'eux.

Ensemble, ces techniques permettent à un MoE de passer à l'échelle sans exiger que chaque GPU conserve en mémoire l'intégralité du modèle et de son état d'entraînement.

Olmo-core 3 réduit également le coût du routage des données vers les bons experts et de l'exécution de leurs calculs. Le parallélisme d'experts « rowwise » place directement les données routées dans les buffers d'entrée des experts, minimisant le travail supplémentaire nécessaire pour les réorganiser. Le routage résident sur GPU conserve les métadonnées de routage directement sur les GPU, de sorte que le CPU peut mettre en file d'attente le travail sans attendre que ces informations soient recopiées. Enfin, le « grouped GEMM » regroupe de nombreux petits calculs d'experts afin que les GPU puissent les exécuter plus efficacement.

Enfin, Olmo-core 3 prend en charge le MXFP8, un format numérique de plus faible précision qui représente certaines valeurs avec moins de bits. Cela peut réduire le volume de calcul et la quantité de données déplacées entre GPU, à condition que ces économies compensent le coût de conversion entre formats numériques.

Ai2 a mesuré l'effet du MXFP8 sur le débit d'entraînement de bout en bout dans un benchmark contrôlé sur quatre GPU NVIDIA B300, avec une charge de travail répartie uniformément entre les experts. Avec le MXFP8 activé sur les parties du système où il apportait le plus de bénéfice, le débit d'entraînement était environ 21 % supérieur à celui obtenu avec le BF16 (le format de référence, plus précis), tandis que le pic de mémoire active passait de 103 à 95 GiB. L'essentiel du gain provenait du calcul feed-forward et du déplacement des données entre experts, plutôt que de l'attention seule.

Ces techniques et optimisations doivent fonctionner ensemble : accélérer une partie de l'entraînement peut créer des coûts ailleurs — un calcul plus rapide peut exiger davantage de mouvements de données, et déplacer moins de bits ne sert à rien si leur conversion prend trop de temps. Olmo-core 3 est conçu autour de ces arbitrages sur l'ensemble du processus d'entraînement, donnant à Ai2 — et aux chercheurs utilisant cette chaîne ouverte — la maîtrise de la façon dont les différentes pièces s'articulent. Ai2 propose par ailleurs une visite interactive illustrant comment le parallélisme de données, d'experts et de pipeline s'articulent pour faire passer l'entraînement d'un seul GPU à un très grand nombre.

**Passer à l'échelle du trillion de paramètres.** Ai2 a testé Olmo-core 3 sur diverses configurations de GPU NVIDIA B300, y compris un modèle de 1,2 trillion de paramètres au total, avec 58,36 milliards de paramètres actifs par token répartis sur 512 GPU. Le débit maximal observé a atteint 858 TFLOP/s par GPU — une mesure du calcul utile effectué chaque seconde par GPU. Ces tests reposaient sur un routage aléatoire destiné à mesurer la performance du système plutôt que la qualité d'un modèle réellement entraîné.

Ai2 a également expérimenté DeepEP v2, une autre méthode de gestion des communications entre experts à travers les GPU, atteignant une configuration de 2,38 trillions de paramètres au total. Il s'agissait d'un test de capacité de courte durée plutôt que d'un entraînement complet, destiné à démontrer l'échelle atteignable par Olmo-core 3 plutôt qu'une performance d'entraînement soutenue.

À cette échelle, la performance système n'est qu'une partie du problème. Le rapport technique d'Ai2 documente aussi des expériences qui ont orienté la façon dont l'entreprise entraîne les MoE et en mesure la performance. Parmi les enseignements :
- Un score censé favoriser un routage équilibré peut s'améliorer alors même que la charge de travail réelle devient de moins en moins équilibrée — un phénomène qu'Ai2 appelle le « token gerrymandering ».
- Réduire le taux d'apprentissage des experts (c'est-à-dire l'amplitude de leurs mises à jour d'entraînement) parce qu'ils traitent moins de tokens n'a pas amélioré les résultats dans la famille de modèles testée.
- Les calculs GPU prennent des durées différentes selon les valeurs traitées, même à dimensions matricielles identiques : les comparaisons de performance doivent donc porter sur des valeurs d'entrée identiques, et pas seulement sur des formes identiques.
- Faire chevaucher communication et calcul sur des flux GPU séparés n'accélère pas toujours l'entraînement ; dans certains tests, cela a même ralenti l'exécution de bout en bout — un rappel que davantage de chevauchement ne garantit pas un débit plus élevé.

Le rapport technique détaille ces constats ainsi que les approches testées puis écartées par l'équipe.

**Construit pour la prochaine génération d'Olmo, ouvert à tous.** Olmo-core 3 constitue le socle des développements à venir chez Ai2. La prochaine génération d'Olmo adoptera une architecture MoE, et Ai2 vise à en faire son modèle le plus performant à ce jour, entraîné sur son plus vaste jeu de données et avec sa plus longue fenêtre de contexte.

Cette nouvelle chaîne permet à Ai2 de dépasser ses précédents travaux sur les MoE tout en offrant davantage de flexibilité pour adapter l'entraînement à l'évolution des modèles et du matériel. Elle est en outre entièrement ouverte : chercheurs et développeurs peuvent utiliser Olmo-core 3 pour entraîner leurs propres MoE, l'adapter à différents matériels, et expérimenter avec le routage, le parallélisme et d'autres composants du système.

Cela reflète la conception qu'Ai2 se fait du développement ouvert de modèles : les poids d'un modèle sont d'autant plus utiles que l'infrastructure et les choix d'entraînement qui les sous-tendent sont eux aussi rendus publics. Pour une analyse plus approfondie de la conception du système, des expériences, des études d'ablation et des approches testées, Ai2 renvoie à son rapport technique complet et au dépôt GitHub d'Olmo-core 3.

Ai2 se présente comme un organisme à but non lucratif dédié à une IA transparente et open source, avec pour mission de partager largement les bénéfices de cette technologie plutôt que de rechercher le profit, et indique recruter sur des postes ouverts pour qui souhaiterait rejoindre ce projet.

## Pourquoi ça compte
Ce lancement illustre la course à l'infrastructure d'entraînement open source pour les très grands modèles MoE, un terrain jusque-là dominé par des piles propriétaires ou semi-fermées (Megatron-Core de NVIDIA) : en documentant précisément ses choix d'architecture, ses benchmarks et même ses échecs, Ai2 pousse la transparence au-delà des poids de modèles, un signal à suivre pour quiconque surveille la démocratisation des capacités d'entraînement à grande échelle.
