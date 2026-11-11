---
title: "Could a modern chess engine on a Pentium have defeated Kasparov in 1996?"
date: 2026-11-11
url: "https://click.dataelixir.com/o8u44z23rdiqhn3vp5givhqqpe0q9hohmlmre/l2hehmhlpgpp97a6h0/aHR0cHM6Ly9uaWNob2xhcy5jYXJsaW5pLmNvbS93cml0aW5nLzIwMjYvYWxnb3JpdGhtaWMtaW1wcm92ZW1lbnRzLWNoZXNzLmh0bWw_dXRtX2NhbXBhaWduPURhdGFfRWxpeGlyJnV0bV9zb3VyY2U9RGF0YV9FbGl4aXJfNTk3"
authors: ["Nicholas Carlini"]
keywords: ["échecs", "Stockfish", "Deep Blue", "Elo", "matériel vintage", "progrès algorithmique"]
theme: "Tech"
tone: "research"
used_in: ["2026-11-11"]
---

## Résumé

Nicholas Carlini se demande si, en 1996, un simple PC de bureau équipé d'un moteur d'échecs plus intelligent aurait suffi à battre Garry Kasparov, sans recourir au supercalculateur spécialisé Deep Blue d'IBM. Pour y répondre, il a remis en service un véritable Pentium Pro à 200 MHz de 1995 et y a fait tourner des versions modernisées des moteurs Crafty (1996) et Stockfish. Résultat : son portage de Stockfish sur ce matériel vintage atteint un Elo estimé à 3300, loin au-dessus des 2800 de Kasparov, et dans un match de 100 parties contre une version de Crafty « boostée » avec les techniques modernes, il l'emporte 78 victoires, 17 nulles et seulement 5 défaites. L'auteur en conclut que l'essentiel du progrès (+720 Elo sur +1335 gagnés) vient des avancées algorithmiques, et non de la puissance brute du matériel.

## Points clés

- Deep Blue (1996-97) utilisait du matériel sur mesure à plusieurs millions de dollars ; Carlini montre qu'un Pentium Pro grand public de l'époque, avec un logiciel moderne, aurait largement suffi à battre Kasparov.
- Sur l'échelle Elo, l'essentiel du gain de force des moteurs d'échecs depuis 1996 (+720 Elo sur +1335) s'explique par de meilleurs algorithmes et une meilleure évaluation des positions, pas par la vitesse du matériel.
- Deux expériences menées : (1) moderniser pas à pas Crafty 11.13 (moteur de 1996) avec les techniques actuelles (fail-soft, LMR, historique de correction, NNUE, SPSA...) ; (2) porter Stockfish moderne sur les contraintes du Pentium Pro (32 bits, 64 Mo de RAM, mono-cœur, sans SIMD).
- Le Stockfish ainsi porté atteint un Elo estimé à ~3300 en cadence classique ; la version modernisée de Crafty atteint environ 2938 Elo à 10 s/coup — les deux dépassant largement Kasparov (2800).
- Le code du projet (portage, « hyperviseur » sur disquette, serveur HTTP embarqué) a été écrit par des IA (Fable 5.1, Opus 5.5, GPT-6) sous la supervision de l'auteur, qui n'a écrit que le texte de l'article.
- L'auteur relie cette expérience à une réflexion plus large sur l'IA actuelle : il s'interroge sur la part de marge de progression purement logicielle qui reste à exploiter dans les modèles de langage, indépendamment des gains de puissance de calcul.

## Analyse approfondie

**Le contexte historique.** Le 10 février 1996, Deep Blue d'IBM bat pour la première fois un champion du monde en exercice, Garry Kasparov, lors d'une partie isolée, avant de perdre le match complet ; un an plus tard, une version améliorée de Deep Blue prend sa revanche en l'emportant 3,5 à 2,5. Cette machine reposait sur 30 processeurs P2SC à ~120 MHz et 480 puces VLSI dédiées à l'évaluation d'échecs, pour un coût de plusieurs millions de dollars ; elle figurait alors au 259ᵉ rang des supercalculateurs mondiaux et analysait plus de 200 millions de positions par seconde.

La question posée par Carlini est simple : ce déploiement massif de matériel spécialisé était-il réellement nécessaire, ou un ordinateur de bureau de l'époque, muni d'un logiciel d'échecs plus performant, aurait-il suffi ?

**Le dispositif expérimental.** Pour trancher, l'auteur s'est procuré un véritable PC d'époque : un Pentium Pro à 200 MHz sur carte mère Intel VS440FX, avec 64 Mo de RAM SIMM cadencée à 66 MHz, démarrant depuis une disquette 3,5 pouces de 1,44 Mo, connecté à Internet via une carte Ethernet Realtek RTL8139C (une carte graphique Trio64V+ et un clavier PS/2 sont présents mais inutilisés, l'auteur communiquant avec la machine via un port série relié à son PC moderne). À sa sortie en novembre 1995, un tel poste de travail (Pentium Pro + RAM + périphériques) coûtait environ 4000 à 5000 dollars — un bon poste de travail, mais en aucun cas un supercalculateur. Il note aussi qu'avec la dépréciation rapide du matériel informatique, cette même configuration ne vaudrait plus qu'environ mille dollars un an plus tard, en 1997, date du match retour.

Pour faire tourner un moteur d'échecs sur cette machine et la connecter au réseau, l'auteur a fait développer un « système d'exploitation » minimal — en réalité plus proche d'un hyperviseur — tenant sur la disquette de démarrage. Son unique rôle est de faire démarrer le Pentium Pro en mode protégé 32 bits, d'initialiser la carte réseau, puis d'attendre et d'exécuter un programme « utilisateur » envoyé en RAM. Le programme en question est un serveur HTTP maison qui reçoit des requêtes contenant une position d'échecs (au format FEN) et un temps de réflexion maximal, fait tourner le moteur jusqu'à expiration du délai, puis renvoie la réponse — permettant même de défier la machine en ligne. L'auteur précise que tout ce code a en réalité été écrit par des modèles de langage (un mix de Fable 5.1, Opus 5.5 et GPT-6) sous sa direction ; seul le texte de l'article est rédigé par un humain.

**Rappel sur l'échelle Elo.** Un écart de 200 points d'Elo signifie que le joueur le plus fort doit gagner environ trois parties sur quatre face au plus faible, et cette relation s'accentue de façon multiplicative : un écart de 400 points correspond à un score attendu de 90 %, un écart de 1000 points à 99,7 %. Les meilleurs moteurs tournant sur du matériel grand public de 1996 plafonnaient autour de 2300 Elo ; Deep Blue était évalué à 2700 ; Stockfish moderne atteint aujourd'hui près de 3700.

La question centrale devient alors : quelle part de cet écart provient de la puissance brute des machines modernes, et quelle part provient des progrès purement logiciels ? Carlini conclut que la majorité du gain (+720 Elo sur +1335 au total) est attribuable aux progrès algorithmiques, et non à la puissance de calcul.

**Expérience 1 : moderniser Crafty.** Carlini part de Crafty 11.13, moteur compétitif de 1996 dont le code source est aujourd'hui disponible, et l'améliore par étapes successives sur le Pentium Pro. Dans sa version d'origine (telle que livrée en 1996), ce moteur atteint un Elo de 1999 ± 90 à 1 seconde par coup, et de 2383 ± 77 à 10 secondes par coup. Les étapes d'amélioration, mesurées à chaque fois à 1 s et 10 s par coup, sont les suivantes :

1. **Micro-optimisations** (remplacement de tables de correspondance par les instructions processeur `bsf`/`bsr`, migration des calculs d'attaques des pièces à longue portée) : le moteur devient 15 % plus rapide à algorithme inchangé → 2063 ± 73 (1 s) / 2323 ± 75 (10 s).
2. **Meilleurs algorithmes de recherche** : fail-soft (renvoi du score réel plutôt que tronqué), élagage par futilité et par « late-move », réduction de profondeur pour les coups tardifs (LMR), tri des coups via tables d'historique → 2022 ± 73 (1 s) / 2420 ± 76 (10 s).
3. **Réglage fin de la recherche et de l'évaluation** : réglage automatique (SPSA) de toutes les constantes de recherche sur plusieurs milliers de parties jouées contre soi-même ; séparation des valeurs d'évaluation phase médiane/finale (pondérées par le matériel restant) et réajustement des poids (« Texel tuning ») ; ajout de termes de mobilité récompensant le contrôle de cases sûres → 2224 ± 72 (1 s) / 2520 ± 74 (10 s).
4. **Première évaluation par réseau de neurones (NNUE)** : remplacement de la fonction d'évaluation par un petit réseau entraîné sur 11 millions de positions issues de parties contre soi-même → 2192 ± 72 (1 s) / 2565 ± 74 (10 s). Cette étape prépare surtout la suivante.
5. **Entraînement du NNUE avec un meilleur « professeur »** : utilisation de Stockfish comme source de vérité plutôt que l'auto-apprentissage, ce qui réduit le temps de calcul nécessaire d'environ 4000 années-cœur « façon 1996 » à seulement quelques jours sur du matériel moderne → 2420 ± 82 (1 s) / 2712 ± 74 (10 s).
6. **Adapter la recherche à la nouvelle évaluation** : ajout d'un élagage par futilité inversée, optimisations de l'évaluateur (cache, accumulateurs partagés), élargissement du réseau par 6, nettoyage de cas particuliers devenus inutiles → 2630 ± 82 (1 s) / 2810 ± 75 (10 s).
7. **Nouveau réglage SPSA et affinements du NNUE** : correction de bugs, ajout de têtes de sortie multiples selon le nombre de pièces restantes, davantage d'unités cachées, doublement des données d'entraînement → 2720 ± 82 (1 s) / 2938 ± 74 (10 s), score final de cette lignée.

**Expérience 2 : porter Stockfish vers 1996.** La seconde approche consiste à partir du meilleur moteur actuel, Stockfish, et à le réécrire pour qu'il tourne sur les contraintes matérielles d'un Pentium Pro (architecture 32 bits, pas de SIMD, 64 Mo de RAM maximum, sans bibliothèque standard C++, sans multithreading, sans tables de fin de partie, avec un NNUE fortement réduit par rapport aux 71 Mo d'origine, et des plateaux de jeu représentés par une paire d'entiers 32 bits). Cette version naïve atteint déjà 2496 ± 64 (1 s) / 2940 ± 76 (10 s). Les affinements suivants sont plus progressifs, car il reste peu de gains algorithmiques majeurs à exploiter :

- Meilleure mise à jour de l'accumulateur du NNUE → 2590 ± 67 (1 s) / 2961 ± 74 (10 s).
- Évaluation moins coûteuse (mélange PeSTO, réglage des options de compilation, réseau NNUE réduit et accéléré, divisant par 3 le temps d'évaluation) → 2752 ± 68 (1 s) / 3006 ± 74 (10 s), le gain le plus important à 1 s/coup.
- Réentraînement « on-policy » du NNUE avec Stockfish comme source d'évaluation → 2780 ± 67 (1 s) / 3070 ± 72 (10 s).
- Nouveau réglage SPSA de la recherche et suppression de PeSTO devenu inutile → 2784 ± 65 (1 s) / 3070 ± 72 (10 s).
- Ajout de l'historique de correction hors-pion, réglage conjoint des paramètres et du NNUE → 2819 ± 65 (1 s) / 3074 ± 72 (10 s).
- Changements purement liés à la compilation (optimisations à la liaison, alignement du code sur 32 octets, sans changement de code) → 2846 ± 35 (1 s) / 3109 ± 79 (10 s), puis 3180 ± 80 à 30 s/coup.

**Estimation finale et confrontation.** En extrapolant la progression observée entre 1, 10 et 30 secondes par coup (environ +70 Elo à chaque triplement du temps de réflexion) vers une cadence classique (environ six minutes par coup en moyenne, temps de l'adversaire inclus), Carlini estime que son portage de Stockfish atteindrait un Elo d'environ 3300 en cadence classique — largement suffisant pour battre Kasparov (2800) avec un score attendu proche de 9 sur 10. Pour trancher de manière plus directe, il a fait jouer 100 parties entre ses deux moteurs modernisés : Stockfish-1996 (sur Pentium Pro) l'emporte 78 fois, fait match nul 17 fois et perd seulement 5 fois contre Crafty-2026 (sur matériel moderne).

L'auteur reconnaît une limite méthodologique : les scores Elo qu'il cite proviennent des classements CCRL (Computer Chess Rating Lists), qui peuvent légèrement diverger de l'échelle Elo FIDE utilisée pour les humains — de la même façon que l'Elo en ligne d'un joueur ne correspond pas exactement à son Elo FIDE. Il estime toutefois que l'écart entre 3200-3300 et les 2800 de Kasparov est suffisamment large pour absorber cette incertitude, et lance même l'invitation à un grand maître classé 2700+ de tenter sa chance contre ce moteur de 2026 tournant sur du matériel de 1996.

**Conclusion et portée plus large.** Carlini relie cette expérience à une réflexion générale sur les premières solutions à un problème : on commence souvent par une approche qui fonctionne en la déployant à grande échelle (ici, le matériel spécialisé de Deep Blue), avant de découvrir, avec le temps et une meilleure compréhension du problème, qu'on pouvait arriver au même résultat de façon beaucoup plus efficace. Il a mené ce projet par curiosité, mais y voit aussi un éclairage sur la vitesse des progrès algorithmiques en « IA » au sens large : si les moteurs d'échecs de 1997 semblaient déjà très avancés (le premier programme d'échecs remontant à Alan Turing, un demi-siècle plus tôt), il paraissait alors plausible qu'il ne restât plus beaucoup d'idées à découvrir — une intuition que l'histoire a clairement démentie. Il pose donc la question, sans y répondre définitivement, de savoir combien de progrès purement logiciels restent à accomplir avec les grands modèles de langage actuels, et si ces gains pourraient dépasser ceux obtenus par la seule montée en puissance du matériel. Il relève enfin, en aparté, l'ironie d'avoir utilisé des IA modernes pour accélérer la recherche sur les limites du progrès algorithmique lui-même.

## Pourquoi ça compte

Cet exemple historique chiffré, où le logiciel explique l'essentiel du progrès (+720 Elo sur +1335), est un argument concret et mesurable pour la veille IA : il invite à se demander si les gains attendus des futurs modèles de langage viendront davantage de l'ingénierie algorithmique que de la simple augmentation de puissance de calcul.
