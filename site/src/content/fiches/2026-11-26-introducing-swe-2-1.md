---
title: "Introducing SWE-2.1"
date: 2026-11-26
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fcognition.com%2Fblog%2Fswe-2-1%3Futm_source=tldrai/1/010001a2131daf4f-90f44adf-0961-488c-a5cb-31386993ed9d-000000/1SoAcgjO4T7GHryVSPpfQTFAOuDHsp_zXcCfWaw2K_Q=452"
keywords: ["IA", "cybersécurité", "modèle de langage", "exploitation de vulnérabilités", "Devin", "benchmark"]
theme: "Sécurité"
tone: "news"
used_in: ["2026-11-26"]
---

## Résumé
Cognition annonce SWE-2.1, une mise à jour majeure de SWE-2, entraînée par apprentissage par renforcement pur sur Kimi K3, qui progresse fortement sur des benchmarks de code (FrontierCode 2.0, Terminal-Bench 4.1) et surtout en cybersécurité (ExploitBench, ExploitGym). Le modèle montre une capacité accrue à trouver ET exploiter des vulnérabilités de bout en bout sur des sessions autonomes de plusieurs heures, ce qui a nécessité des garde-fous spécifiques (red-teaming, évaluation canari de tentative d'évasion du sandbox). Une variante plus permissive, SWE-2.1 Cyber, est déployée dans Devin Security pour donner aux défenseurs un niveau de capacité comparable à celui des attaquants. Cognition lance aussi SWE-2.1 Ultrafast, 10 fois plus rapide via un partenariat avec Cerebras.

## Points clés
- SWE-2.1 est entraîné par RL pur sur Kimi K3 et améliore les performances de codage général ainsi que les workflows autonomes de longue durée.
- Gains marquants en cybersécurité : 80 % sur ExploitBench et 27,3 % de flags capturés via des exploits intentionnels sur ExploitGym.
- Des mesures de sécurité dédiées ont été intégrées à l'entraînement : red-teaming des sandboxes et une évaluation canari qui alerte les chercheurs en cas de tentative d'évasion (déclenchée quatre fois pendant l'entraînement).
- Une version plus permissive, SWE-2.1 Cyber, est proposée via Devin Security pour renforcer les capacités défensives face à des attaquants eux-mêmes assistés par IA.
- La performance s'améliore de façon log-linéaire avec le temps de calcul alloué, avec une pente de mise à l'échelle au moment de l'inférence supérieure à celle du modèle de base.
- SWE-2.1 Ultrafast, développé avec Cerebras, offre une vitesse d'inférence 10× supérieure, utile en situation d'incident urgent.

## Analyse approfondie
Nous publions SWE-2.1, une mise à niveau majeure par rapport à SWE-2. Comme son prédécesseur, il est entraîné par apprentissage par renforcement pur sur Kimi K3. Il obtient des gains importants sur un large éventail de benchmarks, notamment FrontierCode 2.0 et Terminal-Bench 4.1. Nous obtenons l'essentiel de nos gains en performance de codage en ciblant l'intelligence générale et les workflows à long horizon. Cela entraîne également des améliorations dans divers autres domaines, en particulier la cybersécurité.

Une amélioration notable obtenue grâce à notre entraînement concerne la capacité, considérablement accrue, en cybersécurité, dans la recherche et l'exploitation de vulnérabilités. SWE-2.1 atteint 80 % sur ExploitBench et 27,3 % de flags capturés via des exploits intentionnels sur ExploitGym. Le modèle démontre ainsi de solides performances non seulement pour trouver des vulnérabilités, mais aussi pour mener à bien la chaîne d'exploitation complète, souvent sur plusieurs heures de travail autonome.

Voir les Notes de méthodologie des benchmarks à la fin de cet article pour savoir comment ExploitBench et ExploitGym sont notés.

* Ces scores concernent Muse Wonder Full.

Entraîner un modèle doté de capacités avancées en cybersécurité nécessite des garde-fous supplémentaires. Nous avons donc intégré plusieurs mesures de sécurité à l'entraînement :

- Nous avons soumis notre dispositif d'entraînement à du red-teaming, en particulier autour des sandboxes.
- Nous avons mis en place une surveillance de sécurité continue. Nous avons créé une évaluation « canari » où le modèle tente de s'évader du sandbox. En cas de succès, notre infrastructure alerte les chercheurs.

L'évaluation canari s'est révélée être une intervention efficace. Même après un red-teaming poussé, le modèle a découvert de nouvelles vulnérabilités dans notre sandbox à quatre reprises pendant l'entraînement. Les chercheurs ont été alertés et ont réagi immédiatement chaque fois.

Parce que des capacités avancées, en particulier en cybersécurité, comportent un risque de mauvais usage, nous avons déployé SWE-2.1 avec des garde-fous qui détectent et empêchent les comportements les plus dangereux. Ces garde-fous visent un ensemble restreint d'activités à fort potentiel de nuisance, et sont calibrés pour laisser inchangé la majorité du travail légitime, y compris le travail de défense cyber.

Dans le même temps, certains travaux défensifs avancés nécessitent des capacités que ces garde-fous restreignent. L'IA élève le niveau de base accessible aux attaquants : des exploits qui exigeaient autrefois une expertise rare sont désormais à la portée de quiconque dispose d'un modèle performant. Nous voulons donner aux défenseurs le même levier, c'est pourquoi nous déployons SWE-2.1 Cyber, une version de SWE-2.1 aux garde-fous plus permissifs, au sein de Devin Security.

Devin Security propose déjà des analyses approfondies (deep scans) propulsées par des modèles cyber de pointe comme Mythos. Avec SWE-2.1 Cyber qui alimente désormais les analyses normales, nous espérons apporter des capacités cyber accrues pour la défense à tous les utilisateurs.

À mesure que les modèles gagnent en capacité, l'aptitude à opérer de manière autonome sur de longs horizons temporels, pendant des heures voire des jours, devient de plus en plus importante.

Les problèmes réels d'ingénierie et de sécurité se résolvent rarement en quelques minutes. Pour observer comment SWE-2.1 se comporte sur des sessions autonomes prolongées, nous traçons son taux de résolution cumulé sur ExploitGym en fonction du temps d'exécution normalisé (calculé à un TPS fixe, un TTFT de 1 s, plus le temps réel d'exécution des outils).

#### ExploitGym — Flags capturés en fonction du temps

Plus le modèle travaille longtemps, plus il est capable de résoudre des tâches complexes. Dans nos évaluations, nous observons que la performance s'améliore de façon log-linéaire à mesure que l'horizon temporel s'allonge, ce qui signifie que le modèle continue de trouver des exploits en travaillant pendant davantage d'heures. De plus, la pente de la courbe de mise à l'échelle au moment de l'inférence (test-time scaling) a nettement augmenté par rapport au modèle de base, démontrant une capacité significativement accrue à gérer et mener à terme de manière autonome des tâches complexes.

Pour entraîner SWE-2.1, nous avons étendu nos tâches et environnements à la fois pour les workflows à court et à long horizon, couvrant des domaines allant des sciences et de l'ingénierie de performance à la cybersécurité. Cette diversité a rendu le modèle plus polyvalent tout en repoussant encore davantage ses performances en ingénierie logicielle.

Nous avons également amélioré nos algorithmes de post-entraînement pour contrôler la longueur des rollouts pendant l'entraînement. Auparavant, les oscillations de longueur déstabilisaient souvent la dynamique d'entraînement. Réduire ces oscillations nous a permis d'entraîner le modèle de façon fiable sur des tâches allant de quelques minutes à de nombreuses heures.

Ensemble, nos améliorations de données et de méthode nous ont permis d'entraîner le modèle de manière stable sur des durées bien plus longues, avec une performance sur les tâches d'évaluation retenues (held-out) s'améliorant de façon constante sur plusieurs jours d'entraînement. Cette nouvelle méthode a également contribué à l'amélioration de la mise à l'échelle au moment de l'inférence de SWE-2.1, l'aidant à mieux exploiter le calcul supplémentaire sur les tâches difficiles.

Nous publions également SWE-2.1 Ultrafast. Grâce à un partenariat avec Cerebras, nous sommes en mesure de proposer le même modèle à une vitesse 10 fois supérieure. Comme SWE-2.1 continue de s'améliorer avec davantage de calcul au moment de l'inférence, la vitesse d'inférence déterminera la quantité de travail qu'il peut accomplir dans un délai serré. Lors d'un incident actif ou d'une correction urgente, un débit 10 fois supérieur transforme des heures d'investigation et d'itération en quelques minutes seulement.

Gratuit jusqu'au 8/12 sur Desktop et CLI. Disponible dans Devin Desktop, Cloud et CLI à un tarif réduit jusqu'au 30/1. Obtenez SWE-2.1.

**Harness :** Nous rapportons les scores en amont (upstream) ou auto-déclarés lorsqu'ils sont disponibles. Sinon, nous évaluons les modèles sur notre cadre d'évaluation interne. Pour les modèles fermés, nous utilisons le harness préféré du développeur du modèle. Pour les modèles ouverts et les modèles SWE, nous utilisons le harness Devin CLI.

**Budgets de temps :** Pour que les scores des benchmarks restent indépendants de la vitesse d'inférence, nous appliquons des limites de temps sur une horloge simulée qui facture à chaque appel de modèle 1 s de temps jusqu'au premier jeton (TTFT) plus une constante c secondes par jeton de sortie (un TPS fixe), correspondant à nos vitesses de production.

**ProgramBench :** Nous rapportons le pourcentage de tâches pour lesquelles le modèle réussit au moins 95 % des tests. SWE-2.1 et SWE-2 sont exécutés dans notre harness avec un contexte de 250k tokens et jusqu'à 3 compactions (1M tokens au total). Les autres modèles sont évalués dans mini-swe-agent avec la fenêtre de contexte native de chaque modèle (jusqu'à environ 1M tokens).

**ExploitBench :** Nous avons exécuté chaque tâche cinq fois avec une horloge simulée de 3 heures et pris l'union des flags capturés pour chaque tâche. Prendre l'union des flags est une pratique standard pour ce benchmark (voir par exemple la fiche système de GPT-5.6).

**ExploitGym :** Nous rapportons le pass@1 sur l'ensemble des 869 tâches avec un délai de 6 heures. Nous évaluons avec les mitigations désactivées, en suivant la méthode d'Opus 5.5 et Gemini 4 Neon. Nous rapportons deux métriques — flags capturés et succès — en suivant l'article ExploitGym. « Flags capturés » inclut les exploits réels et réussis sans lien avec la vulnérabilité visée initialement spécifiée dans le prompt. Pour calculer le « succès », nous avons adopté l'implémentation amont d'agent-as-a-judge.

## Pourquoi ça compte
Ce lancement illustre la course entre capacités offensives et défensives portées par l'IA en cybersécurité : un modèle capable de mener des chaînes d'exploitation complètes de façon autonome change la donne pour les équipes de sécurité comme pour les attaquants potentiels, rendant les garde-fous d'entraînement et de déploiement (red-teaming, évaluations canari) un sujet de veille central.
