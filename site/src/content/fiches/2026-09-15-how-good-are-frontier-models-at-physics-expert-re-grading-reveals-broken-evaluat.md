---
title: "How Good Are Frontier Models at Physics? Expert Re-Grading Reveals Broken Evaluations and Near-Saturation of Leading Benchmarks"
date: 2026-09-15
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Farxiv.org%2Fabs%2F2609.13009%3Futm_source=tldrai/1/010001a0a01d5872-5c963d3e-2a09-4018-8d07-d0f0737cf930-000000/QQ6QH5Dvza11yqr3YY1LGqKrkKDpDvJU3k_GzQKqPsg=452"
keywords: ["benchmarks", "physique", "évaluation", "raisonnement scientifique", "grands modèles de langage", "saturation"]
theme: "IA"
tone: "research"
used_in: ["2026-09-15"]
---

## Résumé
Cette étude ré-examine les scores jugés faibles des modèles de langage frontière sur les benchmarks de physique en faisant réviser les évaluations par des experts du domaine. Sur six benchmarks largement utilisés, la majorité des réponses initialement notées incorrectes s'avèrent en réalité être des erreurs de correction, de solutions de référence ou des énoncés ambigus, et non des erreurs de raisonnement physique du modèle. Après correction de ces défauts d'évaluation, le score moyen (mean@4) de GPT-5.6-Sol passe de 47,3 % à 78,7 % sur HLE-Physics et de 61,0 % à 87,2 % sur CMT-Benchmark, avec un pass@4 atteignant 94,4 % sur les 54 défis CritPt retenus. Les auteurs concluent que les benchmarks actuels sous-estiment fortement la capacité réelle des modèles frontière à résoudre des problèmes de physique bien posés.

## Points clés
- Six benchmarks de physique largement utilisés ont été audités par des enseignants-chercheurs et doctorants spécialistes de chaque sous-domaine.
- La plupart des cas notés « incorrects » proviennent de problèmes de benchmarking (erreurs de correction automatique, solutions de référence fausses, questions ambiguës ou sous-spécifiées) et non d'erreurs de raisonnement du modèle.
- Après correction des solutions de référence et exclusion ou réparation des questions défectueuses, les scores de GPT-5.6-Sol progressent fortement : de 47,3 % à 78,7 % sur HLE-Physics, de 61,0 % à 87,2 % sur CMT-Benchmark.
- Le pass@4 atteint 94,4 % sur les 54 défis CritPt retenus après filtrage.
- Des hausses substantielles sont également observées sur les sous-ensembles audités de UGPhysics, PRISM-Physics et PHYBench.
- Les benchmarks de physique fermés (à réponse vérifiable) approchent la saturation, ce qui appelle des évaluations plus exigeantes et validées par des experts.

## Analyse approfondie
Les scores rapportés, faibles, sur les principaux benchmarks de physique — y compris ceux figurant dans l'Artificial Analysis Intelligence Index (2026) — suggèrent que les modèles de langage frontière peinent encore avec la physique avancée, un test exigeant de leurs capacités de raisonnement scientifique et de résolution quantitative de problèmes. Pourtant, cette impression ne correspond pas toujours à l'expérience des experts du domaine qui utilisent ces modèles dans leur travail. Les auteurs réexaminent ces résultats rapportés en évaluant des modèles frontière sur six benchmarks de physique largement utilisés et en les auditant avec des experts, en se concentrant sur des problèmes textuels dont la réponse finale est vérifiable. Pour chaque sous-domaine de la physique, des enseignants-chercheurs et doctorants possédant l'expertise pertinente examinent soigneusement les énoncés des problèmes, les solutions de référence et les réponses des modèles, afin de distinguer les véritables erreurs du modèle des erreurs de correction, des solutions de référence incorrectes et des questions ambiguës ou sous-spécifiées.

La plupart des cas audités initialement évalués comme incorrects reflètent ces problèmes de benchmarking plutôt que des erreurs dans le raisonnement physique des modèles. Les auteurs demandent ensuite aux experts de corriger ces problèmes de benchmarking en rectifiant les solutions de référence erronées et en réparant ou en excluant les questions défectueuses. Ils constatent que le score moyen (mean@4) de GPT-5.6-Sol passe de 47,3 % à 78,7 % sur HLE-Physics et de 61,0 % à 87,2 % sur CMT-Benchmark, tandis que son pass@4 corrigé atteint 94,4 % sur les 54 défis CritPt retenus. Les scores corrigés sont calculés sur les sous-ensembles d'évaluation retenus à l'issue de la révision par les experts. Les scores sur les sous-ensembles audités de UGPhysics, PRISM-Physics et PHYBench progressent également de manière substantielle après correction.

Ces résultats suggèrent que les benchmarks actuels sous-estiment fortement la capacité des modèles frontière à résoudre des problèmes de physique bien posés. La quasi-saturation observée sur ces tâches fermées (closed-ended) met en évidence le besoin d'évaluations plus exigeantes et validées par des experts.

## Pourquoi ça compte
Ce travail rappelle qu'un benchmark n'est fiable que si sa méthode de correction et ses solutions de référence le sont elles-mêmes — un point crucial pour quiconque suit ou communique sur les progrès réels des modèles d'IA en raisonnement scientifique.
