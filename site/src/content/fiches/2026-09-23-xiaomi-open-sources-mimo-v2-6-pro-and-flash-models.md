---
title: "Xiaomi open-sources MiMo-V2.6 Pro and Flash models"
date: 2026-09-23
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.testingcatalog.com%2Fxiaomi-open-sources-mimo-v2-6-pro-and-flash-models%2F%3Futm_source=tldrai/1/010001a0c94ac023-ce61b09e-2653-4bb7-99c9-33f88214b103-000000/OV0t1vX6yfegT9CPNY9vsE6fWIsNTgt5_n2Yu8bs3Oo=452"
keywords: ["open-source", "modèles de langage", "apprentissage par renforcement", "Xiaomi", "omnimodal", "agents IA"]
theme: "IA"
tone: "news"
used_in: ["2026-09-23"]
---

## Résumé
Xiaomi a publié en open-source sa série MiMo-V2.6, comprenant deux modèles nativement omnimodaux (Pro et Flash) destinés au code, aux tâches visuelles et au computer use. Le modèle Pro obtient le meilleur score parmi les modèles open-source sur l'Artificial Analysis Intelligence Index v4.3, devançant Kimi K3 et Qwen3.8 Max. L'entraînement repose sur un apprentissage par renforcement (RL) intensif et coûteux sur des tâches complexes et vérifiables, et les capacités du modèle s'étendent bien au-delà du code, jusqu'à la génération de scènes 3D et le contrôle robotique. Les modèles sont disponibles sur plusieurs plateformes, avec publication du rapport technique et du code RL.

## Points clés
- MiMo-V2.6-Pro et Flash : modèles omnimodaux ouverts pour le code, la vision et le computer use ; variante Pro-UltraSpeed jusqu'à 20 fois plus rapide.
- Pro obtient 46,32 sur l'Artificial Analysis Intelligence Index v4.3, meilleur score open-source, devant Kimi K3 et Qwen3.8 Max.
- Tarifs API inchangés par rapport à la V2.5 : Flash à 0,14 $/M tokens en entrée et 0,28 $ en sortie ; Pro à 0,435 $ et 0,87 $ ; UltraSpeed dix fois plus cher.
- Entraînement RL intensif : 30 étapes en moins de six jours, environ 750 000 trajectoires, coûts de 850 000 $ (Flash) et 2,62 M$ (Pro) ; forte progression des scores DeepSWE v1.1.
- Capacités étendues via le « Vibe World » : construction de scènes 3D interactives, contrôle d'un bras robotique Franka Panda, génération de frontends, vidéos et musique.
- Disponible sur AI Studio, MiMo Code, MiMo Desktop, la plateforme API de Xiaomi et OpenRouter ; publication du rapport technique et du code RL pour la reproductibilité.

## Analyse approfondie
Xiaomi a publié et rendu open-source la série MiMo-V2.6, introduisant deux modèles nativement omnimodaux destinés au code, aux tâches visuelles et au computer use. MiMo-V2.6-Pro est son modèle le plus performant, tandis que MiMo-V2.6-Flash vise un équilibre à moindre coût entre intelligence et efficacité. Pro-UltraSpeed offre une sortie jusqu'à 20 fois plus rapide, à qualité égale, pour les usages sensibles à la latence.

MiMo-V2.6-Pro a obtenu un score de 46,32 sur l'Artificial Analysis Intelligence Index v4.3. Selon Xiaomi, cela le place devant Kimi K3 et Qwen3.8 Max, en tant que modèle open-source le mieux noté de la comparaison. Les tarifs de l'API restent alignés sur ceux de la V2.5 : Flash est facturé 0,14 $ par million de tokens en entrée (non mis en cache) et 0,28 $ en sortie, tandis que Pro est à 0,435 $ et 0,87 $. UltraSpeed coûte dix fois plus cher.

Cette publication repose sur les efforts de Xiaomi pour faire passer à l'échelle l'apprentissage par renforcement (RL) sur des tâches complexes et vérifiables. En moins de six jours, Flash et Pro ont chacun effectué 30 étapes de RL sur environ 750 000 trajectoires, pour un coût d'environ 850 000 $ et 2,62 millions de dollars respectivement. Les scores DeepSWE v1.1 sont passés de 48,8 à 65,68 et de 58,4 à 72,57. L'entraînement a couvert des tâches de codage, d'agents généralistes, de vision et de cybersécurité, avec 1 568 échantillons par mise à jour et des longueurs de contexte allant jusqu'à un million de tokens. Xiaomi a figé le routeur (router) pour limiter la dérive (drift) et a eu recours à l'évaluation adversariale, à la détection d'anomalies et à des recoupements par des vérificateurs (verifiers) pour contrer le reward hacking.

MiMo-V2.6 va au-delà du travail logiciel conventionnel pour s'aventurer dans ce que Xiaomi appelle le « Vibe World ». À partir d'une image, d'une vidéo ou d'un prompt textuel, il peut coordonner des agents pour construire et tester visuellement des scènes 3D interactives. Il peut créer des assets Blender, piloter un bras robotique Franka Panda à partir de flux de caméras, produire des frontends et des présentations, assembler des vidéos, et composer de la musique sous forme de partitions et de fichiers MIDI. Les démonstrations de recherche ont notamment porté sur le criblage de matériaux pour la capture de substances chimiques PFAS, ainsi que sur l'aide à la formalisation d'un théorème en Lean 4 représentant plus de 6 000 lignes de code vérifié par kernel (kernel-verified).

Pro et Flash sont d'ores et déjà disponibles sur AI Studio, MiMo Code, MiMo Desktop, la MiMo API Platform de Xiaomi et OpenRouter. MiMo Desktop sort de sa phase d'accès anticipé (early access) en intégrant les deux modèles, tandis qu'UltraSpeed est proposé pour les workflows en temps réel. Xiaomi publie le rapport technique, les environnements d'entraînement et le code RL aux côtés des modèles, présentant ce lancement comme un test reproductible du RL à grande échelle et de l'auto-amélioration (self-improvement) des modèles.

## Pourquoi ça compte
Ce lancement illustre l'intensification de la compétition open-source portée par les acteurs chinois et la stratégie de RL à grande échelle pour l'auto-amélioration des modèles, un signal important pour toute veille sur la dynamique concurrentielle face aux modèles propriétaires occidentaux.
