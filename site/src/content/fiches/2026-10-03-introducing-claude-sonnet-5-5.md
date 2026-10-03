---
title: "Introducing Claude Sonnet 5.5"
date: 2026-10-03
url: "https://elinkb7e.mail.aiwithremy.com/ss/c/u001.uHwUjkMJbGfC93XwTHDGyl4Ww6TyRIS1haYlnDQ5EwkmBYkBqEvktpuPemBjd-GmH5wypJtiKBusEuRoWstD998OqWp72QsSFJGnfaD7pPdzBaiGtO4DTn8JGPPw5eEgTYpPP41v37T2Ik2re5mIJAstLUFg4FyU21X-SzkQERKuz3gfyAuitv8R0DWLnQYB_ycigpTYbok30di1k2EkIrC7p-7XXRSyhqy3TvtYZUzZ2hDGqoLlcJVH3d6A3mbQtcyumFeNK2bIckl7EWHnuX1gs5hCAVtK_D7RsNZ53wc/4uj/iyYzyNEMQwKDJINrvZRz6g/h4/h001.KhrfTHCLAHgPhYYFbFGOHj5wDaEhkZ0i1H_a5PJFatE"
authors: ["Anthropic"]
keywords: ["Claude Sonnet 5.5", "Anthropic", "benchmarks", "sécurité IA", "codage agentique", "tarification"]
theme: "IA"
tone: "news"
used_in: ["2026-10-03"]
---

## Résumé
Anthropic annonce Claude Sonnet 5.5, deuxième modèle de la famille Claude 5.5, pensé comme un complément plus rapide et moins coûteux à Claude Opus 5.5. Le modèle affiche des gains de performance majeurs, notamment en codage agentique (70,6 % contre 10,3 % pour Sonnet 5 sur Terminal-Bench 4.0) et en travail de connaissance, où il talonne Opus 5.5 sur GDPval-AA. Il conserve la même tarification par token que Sonnet 5 mais coûte jusqu'à 30 % moins cher par tâche et génère ses réponses plus de 30 % plus vite, grâce à une consommation de tokens réduite. Le lancement s'accompagne de nouveaux garde-fous de cybersécurité (alignés sur ceux d'Opus 5) et de classifieurs anti-distillation, bien que le modèle reste en retrait par rapport à Opus 5.5 sur les tâches complexes nécessitant un jugement soutenu.

## Points clés
- Bond de performance : 70,6 % sur Terminal-Bench 4.0 (vs 10,3 % pour Sonnet 5), score proche d'Opus 5.5 sur plusieurs benchmarks (GDPval-AA, OSWorld, Chartography).
- Même tarification que Sonnet 5 (2 $ / 10 $ par million de tokens en entrée/sortie) mais jusqu'à 30 % moins cher par tâche et plus de 30 % plus rapide.
- Positionnement produit : complément rapide et économique à Opus 5.5 pour les tâches quotidiennes bien définies, la correction de bugs et les documents/slides soignés.
- Sécurité renforcée : premier modèle Sonnet avec des garde-fous cyber de niveau Opus 5, et premiers classifieurs anti-distillation pour empêcher l'extraction du raisonnement.
- Disponible sur AWS, Google Cloud, Microsoft Azure et la Claude Platform (`claude-sonnet-5-5`), avec zero data retention.
- Limite assumée par Anthropic : Opus 5.5 reste clairement supérieur sur le travail complexe et ouvert nécessitant un jugement soutenu.

## Analyse approfondie
Présentation de Claude Sonnet 5.5, le second modèle de la famille Claude 5.5. Il s'agit d'une nette amélioration par rapport à Claude Sonnet 5 : il est plus de 30 % plus rapide et coûte jusqu'à 30 % moins cher pour la plupart des tâches.

Sonnet 5.5 est un complément plus rapide et moins coûteux à Claude Opus 5.5. Là où Opus 5.5 est conçu pour des tâches complexes nécessitant un jugement fin, Sonnet 5.5 excelle sur les tâches quotidiennes bien définies, la correction de bugs, et la création de documents, de présentations (slides) et de feuilles de calcul soignés. Il a également un sens aigu du design. Claude Haiku 5.5, conçu pour les applications à fort volume et sensibles aux coûts, rejoindra la famille Claude 5.5 dans les prochaines semaines.

Sonnet 5.5 s'améliore par rapport à Sonnet 5 sur les points suivants :

**Performance.** Sonnet 5.5 obtient un score de 70,6 % sur Terminal-Bench 4.0, une évaluation de codage agentique, contre 10,3 % pour Sonnet 5. Il obtient un score deux points inférieur à celui d'Opus 5.5 sur GDPval-AA, un test de tâches réelles couvrant une variété de métiers. Il excelle aussi sur les tâches à long horizon et la compréhension d'images — c'est le premier modèle Sonnet à battre *Pokémon Rouge* en ne travaillant qu'à partir de captures d'écran.

**Collaboration.** Comme Opus 5.5, Sonnet 5.5 écrit de façon plus claire que notre génération précédente de modèles ; les premiers testeurs l'ont décrit comme un meilleur partenaire de collaboration que Sonnet 5. Sa rapidité le rend également bien adapté à l'itération rapide sur des tâches moins complexes.

**Coût.** Sonnet 5.5 est au même tarif que Sonnet 5 : 2 $ par million de tokens en entrée, 10 $ par million de tokens en sortie, et 0,20 $ par million de tokens pour les lectures de cache, mais il a généralement besoin de bien moins de tokens pour accomplir le même travail. Dans nos tests, il coûte jusqu'à 30 % moins cher par tâche que son prédécesseur.

**Vitesse.** Sonnet 5.5 génère ses réponses plus de 30 % plus vite que Sonnet 5, ce qui en fait notre modèle Sonnet le plus rapide à ce jour.

**Alignement et sécurité.** Dans notre audit comportemental automatisé, Sonnet 5.5 s'améliore ou égale Sonnet 5 sur la plupart des mesures d'alignement. Comme ses capacités en cybersécurité sont comparables à celles d'Opus 5, c'est le premier modèle Sonnet à être lancé avec des garde-fous (safeguards) et des mécanismes de repli (fallbacks) en cybersécurité similaires à ceux développés pour nos modèles les plus capables. Ses garde-fous en biologie sont identiques à ceux de Sonnet 5. Ces deux types de garde-fous ne visent qu'un ensemble restreint de requêtes à haut risque ; le développement logiciel courant et la majorité des travaux en sciences de la vie ne sont pas affectés.

### Performance

Sonnet 5.5 s'améliore par rapport à Sonnet 5 dans tous les domaines — parfois de façon spectaculaire. Sur plusieurs évaluations, Sonnet 5.5 en effort Max obtient même des performances comparables à celles d'Opus 5.5. Cependant, les scores de benchmark ne capturent qu'une seule facette des capacités d'un modèle ; dans nos propres tests, comme dans ceux de testeurs externes, Opus 5.5 reste clairement plus fort sur les tâches complexes et ouvertes nécessitant un jugement soutenu.

| | Sonnet 5.5 | Sonnet 5 | Opus 5.5 | GPT-6 Sol |
|---|---|---|---|---|
| Codage agentique – Terminal-Bench 4.0 | 70,6 % | 10,3 % | 66,4 %¹ | — |
| Codage agentique – FrontierCode 1.1 (Main) | 46,2 % Max² / 52,1 % Xhigh | 42,4 % | 54,4 % | 49,3 % |
| Codage agentique – CursorBench 4.0 | 55,5 % | 34,1 % | 57,8 % | — |
| Travail de connaissance – GDPval-AA v2.1³ | 1844 | 1449 | 1846 | 1487⁴ |
| Travail de connaissance – AA-Briefcase v1.1³ | 1811 | 1359 | 1822 | 1483⁴ |
| Raisonnement multidisciplinaire – Humanity's Last Exam | 64,5 % avec outils | 54,9 % avec outils | 67,7 % avec outils | — |
| Utilisation d'ordinateur – OSWorld 2.1 | 80,1 % partiel | 57,0 % partiel | 81,8 % partiel | — |
| Reconnaissance visuelle de graphiques – Chartography | 61,6 % sans outils | 15,6 % sans outils | 64,4 % sans outils | 53,6 %⁴ sans outils |

Pour plus de détails sur la façon dont nous menons nos évaluations, voir la System Card de Sonnet 5.5.

Les graphiques ci-dessous représentent le score de chaque modèle en fonction de son coût par tâche, à chaque niveau d'effort. Plus l'effort augmente, plus les modèles travaillent généralement longtemps, ce qui entraîne un coût par tâche plus élevé mais aussi, en général, un score plus élevé. Plus un point est proche du coin supérieur gauche du graphique, plus il offre de capacité par dollar dépensé.

Sur plusieurs benchmarks, Sonnet 5.5 en effort Low ou Medium bat le meilleur score de Sonnet 5 pour environ un dixième du coût par tâche. Il complète le mieux Opus 5.5 lorsqu'il fonctionne à des niveaux d'effort plus bas, où il coûte moins cher par tâche. À des niveaux plus élevés, il peut obtenir des performances comparables à un coût similaire.

### Codage

Le bond de performance de Sonnet 5.5 est particulièrement visible en codage. En effort High sur FrontierCode, il obtient un score 10 points supérieur à celui de Sonnet 5 au même niveau d'effort, pour environ un quinzième du coût par tâche. Sur CursorBench, qui teste les modèles sur des tâches issues de véritables sessions de codage sur Cursor, son meilleur score se situe à environ deux points de celui d'Opus 5.5.

Les premiers testeurs ont apprécié la rapidité avec laquelle Sonnet 5.5 parvient à comprendre une base de code. Ils ont aussi été frappés par son efficacité : lors de comparaisons directes, il regroupait davantage les appels d'outils (tool calls) que Sonnet 5, ce qui se traduisait par moins d'étapes et des coûts réduits.

### Travail de connaissance

Sonnet 5.5 progresse dans plusieurs domaines du travail de connaissance. Sur GDPval-AA, qui teste les modèles sur des tâches réelles couvrant 44 métiers et neuf grandes industries, Sonnet 5.5 obtient un score quasiment au niveau d'Opus 5.5, soit environ 400 points au-dessus de Sonnet 5. Il est proche d'Opus 5.5 en utilisation d'ordinateur et en reconnaissance de graphiques, et surpasse clairement Sonnet 5 et GPT-6 Sol sur les tâches de connaissance à long horizon.

Les premiers testeurs ont souligné des améliorations moins quantifiables. Ils ont trouvé le modèle plus naturel comme partenaire de conversation et ont remarqué son talent pour le design, notant qu'il apporte de la finition aux interfaces utilisateur et qu'il peut suivre des modèles de présentation (templates de slides) pour créer des decks nécessitant un minimum de retouches. Lors d'un test interne, nous lui avons fourni les documents de résultats trimestriels d'une société cotée ainsi que les transcriptions de ses appels, avec un modèle de slides, et lui avons demandé une revue d'activité de 10 diapositives. Deux experts ont jugé que sa première version était prête à être envoyée telle quelle.

### Coût et vitesse

Tarification

| Prix par million de tokens | Claude Sonnet 5.5 | Claude Opus 5.5 |
|---|---|---|
| Lectures de cache | 0,20 $ | 0,20 $ |
| Écritures de cache | 2,50 $ | 5 $ |
| Tokens en entrée | 2 $ | 4 $ |
| Tokens en sortie | 10 $ | 20 $ |

Sonnet 5.5 nécessite moins de tokens par tâche que Sonnet 5, ce qui le rend moins coûteux à utiliser. Il génère également ses réponses plus de 30 % plus vite, et son efficacité est immédiatement perceptible :

Une nuée de 400 étourneaux dans un seul fichier HTML

Le vent façonnant des dunes de sable dans un seul fichier HTML

Une horloge composée de 24 petites horloges dans un seul fichier HTML

Ajuster le niveau d'effort permet d'équilibrer coût et vitesse par rapport à la qualité globale. Dans Claude Code et nos applications, l'effort par défaut est réglé sur Medium, tandis que la Claude Platform utilise High par défaut. À des niveaux plus bas, Claude répond plus vite et utilise moins de tokens, ce qui convient aux tâches courantes. À des niveaux plus élevés, Claude raisonne plus longtemps et vérifie son travail de façon plus approfondie.

### Sécurité

#### Alignement

Sonnet 5.5 ne fait pas progresser la frontière des capacités de nos modèles ; notre évaluation de l'alignement s'est donc concentrée sur un ensemble ciblé de risques applicables aux modèles de tout niveau de capacité, notamment agir contre les intérêts des utilisateurs, les induire en erreur, et coopérer à des usages abusifs à enjeux élevés.

Dans notre audit comportemental automatisé, qui teste Claude sur environ 1 850 scénarios, Sonnet 5.5 s'améliore ou égale Sonnet 5 sur la plupart des mesures d'alignement, de résistance aux usages abusifs et d'honnêteté. Sur nos évaluations de confinement (containment) les plus récentes, Sonnet 5.5 se rapproche d'Opus 5.5, le meilleur modèle testé, par la rareté avec laquelle il tente de s'échapper de son sandbox, et il est celui, parmi tous nos modèles, qui est le moins susceptible de tester les limites de ses conteneurs. Sur l'ensemble de l'audit, Opus 5.5 reste globalement un peu meilleur, mais nous n'avons trouvé aucune preuve que Sonnet 5.5 poursuive des objectifs en conflit avec l'intention de l'utilisateur.

Comme nous l'avons décrit dans notre récente évaluation de l'alignement, aucun ensemble d'évaluations ne permet de détecter de façon fiable toutes les défaillances, et Sonnet 5.5 pourrait avoir des tendances que nous n'avons pas encore identifiées — c'est pourquoi nous associons notre travail d'alignement aux garde-fous décrits ci-dessous.

#### Garde-fous

**Cybersécurité.** Les capacités de Sonnet 5.5 en cybersécurité constituent une amélioration importante par rapport à Sonnet 5 ; nous le déployons donc avec des garde-fous similaires à ceux d'Opus 5.5. Les utilisateurs peuvent toujours trouver et corriger des bugs dans leur code dans le cadre du développement logiciel courant, mais les tâches de cybersécurité à plus haut risque basculeront de façon visible vers Sonnet 5. Bientôt, les cyberdéfenseurs pourront postuler à notre Cyber Verification Program élargi pour obtenir un accès à paliers à des capacités plus avancées sur Sonnet 5.5, Opus 5.5 et les modèles Claude Mythos.

**Biologie.** Sonnet 5.5 utilise le même ensemble de garde-fous en biologie que Sonnet 5. Ceux-ci visent les requêtes nuisibles ; la majorité des travaux de recherche, d'éducation et de pratique clinique ne sont pas affectés, bien que certaines requêtes en microbiologie et en virologie puissent être signalées à tort. Les organisations peuvent postuler à notre Life Sciences Verification Program pour accéder à des garde-fous conçus pour couvrir l'ensemble des travaux liés à la biologie.

**Distillation.** Les attaques par distillation, dans lesquelles des attaquants utilisent des milliers de faux comptes pour extraire les capacités d'un modèle à l'échelle industrielle, permettent à des acteurs malveillants de créer des modèles très capables sans les garde-fous que nous intégrons à Claude. Comme Sonnet 5.5 est bien plus capable que son prédécesseur, c'est le premier modèle Sonnet à être lancé avec des classifieurs de sécurité empêchant l'extraction du raisonnement. Sonnet 5.5 étend également le « preserved thinking » (raisonnement préservé), de sorte que le raisonnement de Claude ne peut pas être découplé du compte qui l'a créé. La plupart des développeurs ne remarqueront aucun changement. Si vous déplacez des conversations entre comptes, y compris en changeant de compte en cours de session dans Claude Code, notre article de documentation explique ce changement.

### Pour commencer

Comme Opus 5.5 et Sonnet 5, Claude Sonnet 5.5 est disponible avec une politique de zéro conservation des données (zero data retention).

Claude Sonnet 5.5 est désormais disponible sur toutes les plateformes, y compris Amazon Web Services, Google Cloud et Microsoft Azure. Les développeurs peuvent démarrer sur la Claude Platform avec `claude-sonnet-5-5`. Si vous utilisez Sonnet avec le thinking désactivé, vous devrez passer au nouveau paramètre `between_tools`, qui maintient le thinking initial désactivé, avant de migrer vers Sonnet 5.5. Voir notre guide de migration pour plus de détails.

### Notes

¹ Les résultats de Terminal-Bench 4.0 sont rapportés pour Claude Opus 5.5 en effort Xhigh, ce qui représente le score le plus élevé du modèle.

² Sonnet 5.5 obtient un score plus bas en effort Max qu'en Xhigh. FrontierCode évalue si une modification de code pourrait être fusionnée (merged) sans retouches humaines. Ce benchmark pénalise les modifications hors périmètre, même si elles sont de bonne qualité ou utiles. En effort Max, Sonnet 5.5 a plus souvent exécuté la compétence (skill) de revue de code de Claude Code, qui répartit la revue entre de nombreux sous-agents, et dans deux cas examinés par Cognition, cela a entraîné un timeout ou des modifications supplémentaires dépassant le périmètre de la tâche, et donc un score plus bas.

³ Artificial Analysis a exécuté GDPval-AA et AA-Briefcase sur un déploiement préliminaire (pre-release) de Sonnet 5.5 sur la Claude Platform, dont nous avons découvert qu'il comportait un bug susceptible de dégrader les réponses aux requêtes utilisant des sorties structurées (structured outputs). Nous estimons que l'effet sur les scores de Sonnet 5.5, s'il existe, est faible et sous-estime sa performance. Ce bug a depuis été corrigé.

⁴ OpenAI a récemment corrigé un bug qui dégradait la compréhension d'images dans GPT-6 Sol. Les scores officiels AA-Briefcase v1.1 et GDPval-AA v2.1 d'Artificial Analysis, ainsi que les scores Chartography de Surge AI, n'ont peut-être pas encore été mis à jour pour refléter la dernière version du modèle. Artificial Analysis ne s'attend pas à un impact majeur sur AA-Briefcase v1.1 et GDPval-AA v2.1. Les tests internes de Chartography suggèrent que son score n'a pas été affecté.

## Pourquoi ça compte
Ce lancement illustre la stratégie d'Anthropic de segmenter sa gamme de modèles par rapport coût/performance plutôt que de ne viser qu'une capacité maximale unique, et étend à un modèle de milieu de gamme des garde-fous de sécurité avancés (cyber, anti-distillation) jusque-là réservés aux modèles les plus puissants — un signal utile pour quiconque évalue le coût total et les risques de ses déploiements LLM en production.
