---
title: "Can data agents do real analysis?"
date: 2026-10-27
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Froundup.getdbt.com%2Fp%2Fcan-data-agents-do-real-analysis%3Futm_source=tldrdata/1/010001a177b312eb-e5823126-cfe6-4c86-8941-97d3b5c4bf0c-000000/Wnr21OefFjC8yFT79mwA_OCDk1SkY2JobecNWlbzpSI=452"
authors: ["Shreya Shankar", "Tristan Handy"]
keywords: ["agents de données", "benchmark", "SQL", "couche sémantique", "LLM judge", "evals"]
theme: "IA"
tone: "research"
used_in: ["2026-10-27"]
---

## Résumé
Cet épisode de podcast (dbt Labs) interroge Shreya Shankar, future professeure à Carnegie Mellon, sur l'écart entre la promesse des agents d'IA en analyse de données et la réalité mesurée. Son benchmark Data Agent Bench (DAB), construit sur un environnement volontairement réaliste (bases multiples, données non structurées, connaissances tribales), montre que le meilleur agent ne réussit que 61 % des requêtes du premier coup. L'ajout d'une couche sémantique améliore nettement les résultats, ce qui souligne l'importance persistante de la structuration humaine des données. L'échange aborde aussi les limites des « juges LLM » pour évaluer la qualité des sorties, et le coût explosif des requêtes SQL pilotées par IA.

## Points clés
- Le benchmark DAB teste des agents dans des conditions proches du travail réel d'un analyste junior : plusieurs bases de données, absence de table unique en contexte, données textuelles à interpréter, savoir tacite non documenté.
- Meilleur score obtenu : 61 % de réussite au premier essai (pass@1) ; des scores plus élevés affichés sur certains leaderboards proviendraient de prompts surajustés à chaque requête.
- Fournir une couche sémantique aux agents améliore significativement la précision, mais cette couche doit rester compréhensible et maintenue par des humains pour éviter de devenir du « slop ».
- Les agents n'ont pas d'équivalent du raccourci visuel qu'offre une visualisation aux humains pour repérer rapidement ce qui est intéressant dans des données.
- Évaluer des sorties de LLM avec des « juges LLM » reste difficile : les critères d'évaluation des développeurs évoluent au fur et à mesure qu'ils observent des exemples (phénomène de « dérive des critères »).
- Les requêtes SQL enrichies d'opérateurs IA (chez Snowflake, BigQuery, Databricks) peuvent devenir extrêmement coûteuses, faute d'optimisation des appels aux modèles.

## Analyse approfondie
Shreya Shankar situe ses travaux à l'intersection des bases de données, des agents d'IA et de l'interaction homme-machine. Après un passage chez Google Brain et une expérience en ingénierie ML dans une startup d'analytique, elle s'est orientée vers les bases de données en constatant que l'essentiel des problèmes rencontrés relevait de l'ingénierie des données plutôt que du machine learning pur.

Son benchmark DAB part du constat que les évaluations existantes (text-to-SQL, ou question-réponse sur table entière en contexte) sont trop "propres" pour refléter le travail réel d'un analyste. Elle distingue une « boucle interne » (les bases de données, qui répondent vite à une question déjà formulée) d'une « boucle externe » (les outils de BI, qui aident à trouver la bonne question) — et note que les agents actuels n'ont pas d'équivalent du raccourci cognitif qu'offre la visualisation aux humains.

Les résultats du benchmark montrent un écart important entre les agents évalués dans des conditions réalistes et les scores plus flatteurs obtenus ailleurs, souvent via un prompting spécifique à chaque requête qu'elle qualifie de peu réaliste. La présence d'une couche sémantique améliore nettement les performances, ce qui, selon elle, renforce l'argument en faveur du travail des ingénieurs analytiques plutôt que de le rendre obsolète.

Sur le volet évaluation, elle revient sur son papier « Who Validates the Validators? », qui a mis en évidence la « dérive des critères » : les développeurs ne savent pas précisément ce qu'ils veulent évaluer avant d'avoir observé un grand nombre de sorties de modèles. Elle défend l'utilité des évaluations (evals) face à l'argument selon lequel il suffirait d'attendre de meilleurs modèles, tout en reconnaissant que les sauts de qualité les plus importants viennent historiquement des nouveaux modèles plutôt que du prompt engineering.

Enfin, elle évoque son prochain chantier au CMU Database Group : l'optimisation des requêtes « AI SQL » (où des opérateurs IA sont intégrés directement dans des requêtes SQL), aujourd'hui implémentées de façon naïve — un appel HTTP par ligne vers un fournisseur de LLM — ce qui explique des factures parfois démesurées. Elle envisage un moteur d'inférence dédié, pensé pour le prefill plutôt que pour la génération token par token.

## Pourquoi ça compte
Ce témoignage chiffre, pour la première fois de façon rigoureuse, l'écart entre le discours ambiant sur les « agents analystes » et leurs performances réelles — un signal utile pour calibrer les attentes de toute organisation qui envisage de déléguer de l'analyse de données à des agents IA.
