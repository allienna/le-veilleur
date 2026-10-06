---
title: "How many AI agents could we run?"
date: 2026-10-06
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fepoch.ai%2Fpublications%2Festimating-the-agent-population%3Futm_source=tldrai/1/010001a10c44d18a-eddc2289-2c6b-45fb-ac5a-a80f99042684-000000/1uYUyH9u1T9sBFi4ty73YgXESV8b2mN5exJMPlPA4RU=452"
keywords: ["agents IA", "infrastructure de calcul", "mémoire HBM", "centres de données", "économie de l'IA", "modèles frontières"]
theme: "IA"
tone: "research"
used_in: ["2026-10-06"]
---

## Résumé

Cette étude d'Epoch AI tente de chiffrer combien d'agents IA le parc mondial de puces pourrait faire fonctionner simultanément, en se fondant sur les livraisons de mémoire à large bande passante (HBM) entre 2025 et 2027. Les auteurs estiment que ce matériel pourrait soutenir, une fois pleinement déployé, entre 30 et 170 millions d'agents concurrents fondés sur des modèles de pointe, soit l'équivalent des heures de travail hebdomadaires de 140 à 720 millions d'employés à temps plein. Même une utilisation modeste (20 %) de cette capacité impliquerait une dépense annuelle en équivalent API de 2 600 à 5 300 milliards de dollars, bien au-delà du millier de milliards de dollars de revenus que les développeurs de modèles pourraient atteindre fin 2027 en maintenant une croissance quintuplée chaque année. L'article souligne ainsi un risque de surcapacité : l'investissement massif dans les puces pourrait devancer largement la demande réelle en agents IA.

## Points clés

- Les puces HBM livrées jusqu'en 2027 pourraient faire tourner de dizaines à centaines de millions d'agents IA concurrents fondés sur des modèles frontières, selon les hypothèses de coût et de rendement retenues.
- Des modèles plus efficaces (ex. DeepSeek V4 Pro) pourraient porter cette capacité jusqu'à environ 1,9 milliard d'agents concurrents sur le même matériel.
- Le coût horaire d'un agent varie fortement selon le modèle et l'outil utilisé : environ 16-18 $/heure pour les charges de travail Codex, contre 24-50 $/heure pour Claude Code.
- Même une utilisation partielle (20 %) de la capacité matérielle impliquerait une demande en dépenses API 2,6 à 5 fois supérieure aux revenus projetés des développeurs de modèles fin 2027.
- La HBM (fabriquée essentiellement par Micron, Samsung et SK hynix) est le goulot d'étranglement commun à tous les accélérateurs IA, et sa pénurie freine déjà le déploiement malgré l'accumulation de puces.
- Le prix d'une performance IA donnée chute d'environ 47 % par trimestre depuis 2023, ce qui peut réduire le coût de possession du matériel mais aussi réduire les besoins en matériel par tâche, rendant l'absorption de la capacité incertaine (paradoxe de Jevons).

## Analyse approfondie

### Vue d'ensemble

Les entreprises d'IA dépensent des centaines de milliards de dollars par an en puces et en centres de données, misant sur le fait que ce matériel fera fonctionner des agents IA capables d'accomplir des tâches aujourd'hui réalisées par des humains. La question posée est : combien d'agents ce déploiement matériel pourrait-il réellement soutenir ?

Les puces IA livrées jusqu'en 2027 pourraient faire fonctionner des dizaines à des centaines de millions d'agents concurrents fondés sur des modèles frontières. En tournant sans interruption, ces agents fourniraient autant d'heures de travail hebdomadaires que 140 à 720 millions d'employés à temps plein. Des modèles plus efficaces pourraient porter cette capacité à plusieurs milliards d'agents sur le même matériel : en appliquant les benchmarks de service de DeepSeek V4 Pro à l'offre matérielle projetée, on obtient environ 1,9 milliard d'agents concurrents, soit l'équivalent des heures de travail hebdomadaires de 8 milliards de personnes travaillant 40 heures chacune. Même une utilisation modeste de cette capacité exigerait une hausse massive de la demande mondiale en IA : utiliser seulement 20 % de l'estimation centrale impliquerait une dépense annuelle en équivalent API de 2 600 à 5 300 milliards de dollars, contre environ 1 000 milliards de dollars de revenus développeurs projetés fin 2027 avec une croissance annuelle quintuplée. Enfin, les dépenses horaires par agent varient fortement selon modèles et outils : dans l'analyse des traces d'agents, les charges Codex coûtaient en moyenne 16-18 $ de l'heure d'activité continue, contre 24-50 $ pour les charges Claude Code.

### Capacité potentielle en agents et dépenses associées

Dario Amodei (Anthropic) a évoqué un futur « pays de génies dans un centre de données » — mais combien d'agents les futurs centres de données pourraient-ils réellement soutenir ? Cette échelle compte pour l'impact potentiel de l'IA sur l'économie et le marché du travail.

Le matériel utilisant de la mémoire à large bande passante (HBM) livré en 2025-2027 pourrait, à terme, soutenir des dizaines à des centaines de millions d'agents concurrents fondés sur des modèles frontières, en supposant un déploiement complet et une allocation totale à ces charges de travail. La HBM livrée en 2025-2026 pourrait soutenir 16 à 56 millions d'agents concurrents une fois déployée ; en intégrant les livraisons jusqu'en 2027, l'estimation grimpe à environ 30-170 millions.

À la différence des humains, un agent IA peut travailler 168 heures par semaine, soit 4,2 fois la semaine de travail de 40 heures d'un employé à temps plein. Ces agents pourraient donc fournir autant d'heures de travail hebdomadaires qu'environ 67 à 240 millions de personnes à partir des livraisons jusqu'en 2026, et 140 à 720 millions à partir des livraisons jusqu'en 2027. À titre de comparaison, les États-Unis comptent 342 millions d'habitants et environ 100 millions de travailleurs du savoir. Ces comparaisons ne portent que sur les heures de travail : les agents peuvent aussi produire des résultats bien plus rapidement que les humains, quoique la qualité varie.

Même en n'utilisant que 20 % de la capacité issue de la mémoire livrée jusqu'en 2027, la dépense implicite aux prix de l'API atteindrait 2 600 à 5 300 milliards de dollars par an une fois le matériel déployé. À titre de comparaison, si les revenus des développeurs de modèles continuent de quintupler chaque année, leur revenu annualisé combiné atteindrait environ 1 000 milliards de dollars fin 2027.

La demande pourrait rester en retrait de cette offre potentielle, créant une surabondance de capacité. L'incertitude clé est de savoir si la croissance de la demande en services IA sera suffisamment rapide et durable pour justifier cet investissement.

### Méthodologie d'estimation de la capacité en agents

Les auteurs estiment le nombre d'agents concurrents potentiels ($A$) : combien d'agents pourraient fonctionner simultanément sur la mémoire livrée en 2025-2027, en supposant un déploiement complet et une allocation totale à la charge de travail modélisée. Cette estimation se décompose en deux termes :

$$A = E \times c$$

où $E$ est l'offre matérielle effective en équivalents GB300, et $c$ le nombre d'agents par équivalent GB300.

**Offre matérielle effective ($E$)** : mesurée en unités d'inférence équivalentes GB300, de façon analogue aux équivalents H100 basés sur les FLOP. Pour ces charges de travail, c'est la capacité mémoire qui contraint la concurrence (le nombre de sessions simultanées), tandis que la bande passante mémoire contraint la vitesse de diffusion des tokens. Les auteurs comptent la HBM livrée depuis 2025 (HBM3E et générations plus récentes) en unités de 288 Go, correspondant à un GPU GB300, puis ajustent selon la concurrence que le matériel plus récent peut supporter.

**Capacité de service ($c$)** : nombre de sessions d'agents actives simultanées par équivalent GB300. Pour les modèles fermés, on utilise $c = (G \times K) / S$, où $S$ est la dépense API par heure d'agent active (après ajustement des temps d'attente humains et plafonnement des autres temps morts), $G$ le coût de location GPU par heure de GB300, et $K$ le ratio entre revenu équivalent API et coût de service de référence. Pour les modèles ouverts, on utilise directement la concurrence mesurée par des benchmarks.

**Hypothèses principales** : $S = 30 \$$/heure-agent, $G = 5\$$/heure-GB300, $K = 5$ à $10\times$, et un facteur d'amélioration HBM4 $u = 2\times$ (avec tests à $1\times$ et $4\times$). Pour les modèles ouverts, les cibles de vitesse de diffusion utilisées sont de 50 et 100 tokens de sortie par seconde par utilisateur (P90), avec 200 en test de sensibilité. Les exigences actuelles de modèles et de charges de travail sont maintenues constantes.

### Estimer les sessions d'agents par GPU aujourd'hui

**Que compte-t-on comme « agent » ?** Le terme désigne une charge de travail agentique fonctionnant dans un outil comme Codex ou Claude Code : une session d'agent inclut les appels au modèle et l'usage d'outils, pas seulement la génération continue de tokens. Les auteurs s'appuient sur deux sources : le benchmark de service AgentX de SemiAnalysis pour les modèles ouverts, et TraceLab, un jeu de données public de sessions d'agents journalisées, pour les modèles fermés. Une session continue d'agent inclut le temps d'attente des appels d'outils ; le temps de travail continu est estimé en retirant les attentes de réponse humaine et en plafonnant les temps morts non identifiés. Une heure de cette activité ajustée compte comme une « heure-agent ».

**Modèles ouverts : les benchmarks de service mesurent directement la concurrence.** Le benchmark InferenceX AgentX de SemiAnalysis utilise un jeu de données de traces de sessions d'agents Claude Code, rejoué avec du texte synthétique tout en préservant longueurs de requêtes, contexte partagé, timing et structure des appels. La concurrence y est définie par le nombre de sessions d'agents lancées, divisé par le nombre total de GPU (GPU combinés pour les configurations prefill-decode désagrégées), donnant des sessions d'agent concurrentes par GPU. Les cibles de vitesse retenues sont 50 et 100 TPS/utilisateur (200 en annexe), sachant qu'OpenAI et Anthropic servent généralement leurs modèles frontières autour de 50-70 TPS. L'« interactivité P90 » décrit la vitesse de sortie pour la partie la plus lente de la distribution, hors temps jusqu'au premier token (TTFT) et hors latence de bout en bout.

**Modèles fermés : la concurrence déduite des dépenses API.** Faute de détails d'architecture permettant des benchmarks matériels transparents pour les modèles fermés, les auteurs analysent les coûts API d'un agent fonctionnant en continu, à partir du jeu de données TraceLab (sessions Codex et Claude Code), ajusté des délais d'attente humains puis normalisé en taux horaire. En appliquant un ratio de marge supposé entre revenu API et coût de service, puis en comparant au coût de location horaire d'un GPU GB300, on obtient le nombre d'agents concurrents soutenables par GPU.

**30 $ par heure-agent se situe entre les coûts de Codex et de Claude Code.** Les dépenses horaires varient fortement selon modèles et outils. Sous les hypothèses de cache retenu et de plafonnement des écarts à cinq minutes, les taux regroupés de TraceLab sont de 18,2 $/heure pour GPT-5.5, 15,5 $ pour GPT-5.6 Sol, 24,3 $ pour Opus 4.8, et 50,2 $ pour Fable 5. Les auteurs retiennent 30 $/heure comme point de référence, légèrement vers le haut de la fourchette. Les futurs modèles pourraient voir leurs prix augmenter (comme les sauts vers Fable chez Anthropic ou GPT-6 Astra chez OpenAI) ou diminuer sous l'effet de la concurrence et des gains d'efficacité ; une fourchette de 10 à 100 $ par heure-agent est testée en sensibilité.

Avec $S = 30\$$/heure-agent et $G = 5\$$/heure-GB300 (tarif de location 3 ans de SemiAnalysis), à $K = 10\times$ le coût de service implicite est de 3 $ par heure-agent, et un GPU à 5 $/heure soutient 1,67 session d'agent concurrente. Le tableau ci-dessous résume :

| Ratio revenu/coût $K$ | Coût implicite par heure-agent | Agents par équivalent GB300 |
|---|---|---|
| 5× | 6,00 $ | 0,833 |
| 10× | 3,00 $ | 1,667 |

L'estimation centrale retient $K = 5$ à $10\times$, soit 0,833 à 1,667 session d'agent par GB300 équivalent à 30 $/heure-agent. Les benchmarks de modèles ouverts sur AgentX à 50 TPS/utilisateur impliquent des ratios $K$ d'environ 4 à 10,5× :

| Modèle / palier API | GPU | 50 TPS/utilisateur | 100 TPS/utilisateur |
|---|---|---|---|
| DeepSeek V4 Pro (hors pic) | GB300 | 4,4× | 2,1× |
| DeepSeek V4 Pro (pic) | GB300 | 8,8× | 4,2× |
| GLM-5.2 | GB300 | 10,5× | 9,3× |
| Kimi K3 | GB300 | 4,1× | 2,9× |
| MiniMax M3 | B300 | 4,8× | 4,1× |

Les auteurs ont vérifié que les charges de travail AgentX (traces WEKA) et TraceLab sont suffisamment comparables en comparant la consommation horaire de tokens par type pour les modèles Claude communs aux deux jeux de données.

### Estimer la capacité future à partir de la mémoire à large bande passante (HBM)

**La HBM, goulot d'étranglement commun à tous les accélérateurs IA.** La HBM offre une mesure commune de l'offre entre GPU et accélérateurs personnalisés, car elle est à la fois un composant clé pour l'inférence et le principal frein à la production de puces. Seules trois entreprises produisent la HBM : Micron, Samsung et SK hynix. Micron indique que la demande en mémoire dépasse l'offre et que la construction de nouvelles usines prend des années ; SK hynix fait le même constat. Nvidia envisagerait même des configurations à mémoire réduite pour le Rubin Ultra en raison de ces contraintes d'approvisionnement. La capacité mémoire limite le nombre de requêtes actives simultanées (poids du modèle + cache KV, qui croît avec la longueur du contexte), tandis que la bande passante HBM peut limiter la vitesse de décodage lorsque le flux de données depuis la mémoire est le facteur limitant. Les auteurs comptent la HBM physique en unités de 288 Go (équivalent GB300), puis ajustent pour exprimer l'offre en équivalents GB300 effectifs.

**Les systèmes HBM4 plus récents devraient soutenir plus d'agents par gigaoctet.** Les spécifications Nvidia montrent que le GB300 utilise 288 Go de HBM3E tandis que le VR200 utilise 288 Go de HBM4 ; à capacité égale, la bande passante passe de 8 à 22 To/s (soit un gain de 2,75×). Quand la capacité mémoire est la contrainte, la concurrence est plafonnée par le nombre maximal de requêtes tenant en mémoire ; davantage de bande passante permet de soutenir plus d'agents à vitesse de sortie donnée lorsque la bande passante est le facteur limitant. L'hypothèse centrale retenue est que les systèmes HBM4/4E soutiennent deux fois plus d'agents concurrents par 288 Go que les systèmes HBM3E ($u = 2$), avec des tests à $u = 1$ (aucune amélioration) et $u = 4$ (amélioration incluant de meilleures interconnexions et logiciels de service).

**Comptage de toute la HBM3E et générations plus récentes livrées depuis 2025.** Selon la méthodologie d'Epoch sur les composants de puces IA, il faut environ huit semaines entre l'entrée de la HBM dans l'assemblage de l'accélérateur et la finalisation de celui-ci — le délai de déploiement effectif pouvant être bien plus long selon la construction des centres de données. En reconstruisant l'offre annuelle à partir des publications de TrendForce (livraisons HBM 2026 supérieures à 3,75 milliards de Go, croissance d'usage HBM 2026 supérieure à 70 %, croissance de livraison 2027 projetée à 50-60 %), les auteurs obtiennent :

| Année de livraison | Total HBM (Mds Go) | Part HBM3E | Part HBM4/4E |
|---|---|---|---|
| 2025 | 2,21 | 80 % | 0 % |
| 2026 (est.) | 3,75 | 62,5 % | 37,5 % |
| 2027 (est.) | 5,81 | 20 % | 80 % |

Ces parts par génération pour 2026-2027 sont des hypothèses des auteurs, faute de données officielles détaillées par année.

**Les livraisons jusqu'en 2027 pourraient soutenir 33 à 171 millions d'agents fondés sur des modèles frontières.** Sous l'hypothèse matérielle centrale, les livraisons jusqu'en 2026 soutiendraient environ 20 à 40 millions d'agents concurrents, montant à 50-101 millions avec les livraisons jusqu'en 2027 (le total 2027 inclut celui de 2026 ; allouer seulement la moitié de la mémoire à cette charge de travail diviserait ces chiffres par deux). La capacité diminue proportionnellement à la hausse du coût par heure-agent : en faisant varier ce coût de 10 à 100 $ (contre 30 $ en estimation centrale), les fourchettes de résultats dépendent aussi du ratio $K$ (5-10×) et du facteur HBM4 $u$ (1-4×).

Pour les modèles ouverts, le front d'InferenceX pour les GPU GB300 donne, pour DeepSeek, 31,4 sessions d'agents par GPU à 50 TPS/utilisateur et 14,4 à 100 TPS/utilisateur (par interpolation), chiffres ensuite mis à l'échelle de l'offre matérielle effective.

### Conclusion : ce que ces totaux impliquent pour la demande en IA

À travers tous les scénarios matériels et de coût de service testés, la mémoire livrée en 2025-2027 pourrait soutenir environ 30 à 170 millions d'agents concurrents fondés sur des modèles frontières une fois déployée et pleinement allouée, fournissant autant d'heures de travail hebdomadaires qu'environ 140 à 720 millions d'employés à temps plein. La question posée est de savoir si la demande sera suffisamment importante pour exploiter cette capacité.

En comparant à l'échelle du marché de l'inférence, sous un scénario conservateur (40 % d'allocation à l'inférence génératrice de revenus et 50 % de taux d'utilisation, soit 20 % d'usage effectif de la capacité totale), le matériel issu de la mémoire livrée en 2025-2026 pourrait soutenir environ 1 100 à 2 100 milliards de dollars de dépense annuelle en équivalent API, montant à 2 600-5 300 milliards avec les livraisons jusqu'en 2027, à 30 $ par heure-agent. À titre de comparaison, les principaux développeurs de modèles génèrent déjà plus de 100 milliards de dollars de revenu annualisé combiné ; en maintenant la croissance quintuplée récente, ce chiffre atteindrait environ 1 000 milliards de dollars fin 2027 — encore nettement inférieur à la dépense impliquée par le scénario de capacité.

Des pénuries de capacité de service à court terme peuvent coexister avec cette offre potentielle future : fin 2025, Satya Nadella (Microsoft) a indiqué que l'entreprise disposait de puces en stock qu'elle ne pouvait pas brancher faute d'espace alimenté disponible dans ses centres de données. Ces retards de déploiement laissent du temps à la demande pour croître.

Le prix d'une performance IA donnée chute rapidement : une analyse récente d'Epoch estime un déclin de 47 % par trimestre depuis 2023 sur les benchmarks étudiés. Cela joue dans les deux sens : des coûts matériels de possession et d'exploitation plus bas réduisent le revenu nécessaire pour justifier l'investissement, mais des modèles et systèmes de service plus efficaces réduisent aussi le matériel requis par tâche — maintenir le taux d'utilisation exigerait alors que la demande en activité d'agents croisse suffisamment pour compenser ces gains d'efficacité.

La demande pourrait croître via une adoption plus large des agents et leur usage sur des tâches plus difficiles et plus coûteuses en calcul. Des agents persistants, comme « dots » d'OpenAI, pourraient aussi accroître la quantité de travail délégué par utilisateur en prenant en charge des responsabilités continues et des projets de longue durée ; des prix plus bas rendraient ces usages plus rentables. Si la croissance d'activité résultante dépasse les gains d'efficacité du calcul, la demande totale en calcul d'inférence augmenterait malgré la baisse de calcul requis par tâche — un exemple du paradoxe de Jevons.

Ces estimations suggèrent un risque que la construction de capacité de calcul devance la demande en inférence. L'absorption de cette capacité dépendra du volume de travail délégué par les utilisateurs, du calcul que ce travail requiert, et du prix qu'ils sont prêts à payer. À des coûts horaires comparables aux salaires humains, les agents devront apporter une valeur suffisante pour justifier cette dépense. Ce déploiement matériel massif constitue un pari : que l'IA dépasse la simple réponse à des questions pour accomplir un travail économiquement utile dans un large éventail d'industries.

### Annexes (points essentiels)

- **Vitesse de diffusion et premier token** : à 50 TPS/utilisateur cible (P90), le temps jusqu'au premier token atteint 39,8 secondes pour la configuration Kimi K3/GB300 la plus chargée répondant à ce critère ; il tombe à 12,4 s pour une cible à 100 TPS et à 4,6 s pour 200 TPS.
- **Échantillon TraceLab** : les taux horaires moyens pondérés sont de 18,19 $ (GPT-5.5/Codex), 15,50 $ (GPT-5.6 Sol/Codex), 24,34 $ (Opus 4.8/Claude Code) et 50,16 $ (Fable 5/Claude Code), sur la base de 3 390 groupes session/modèle issus de 3 382 sessions d'agents sources, couvrant la période du 23 avril au 24 juillet 2026.
- **Prix des tokens utilisés** (par million de tokens) : GPT-5.5 : 5,00 $ entrée / 0,50 $ entrée en cache / 30,00 $ sortie ; GPT-5.6 Sol : 4,00 $ / 0,40 $ / 20,00 $ (écriture cache 5,00 $) ; Claude Opus 4.8 : 5,00 $ / 0,50 $ / 25,00 $ (écriture 6,25 $) ; Claude Fable 5 : 10,00 $ / 1,00 $ / 50,00 $ (écriture 12,50 $).
- **Sensibilité aux ratios revenu/coût ($K$)** : à 20× et 40×, le coût de service implicite tombe à 1,50 $ et 0,75 $ par heure-agent, soit 3,333 et 6,667 agents par équivalent GB300.
- **Part Nvidia de la HBM** : Nvidia représenterait 66 % de la demande HBM en 2025 (58 % projetés en 2026) selon TrendForce (69 % selon une estimation antérieure d'Epoch). Selon le mix d'accélérateurs retenu, la capacité globale varie de 75 % à 92,5 % de l'estimation principale.
- Le code permettant de reproduire les figures et l'analyse des traces est disponible sur GitHub (epoch-research/compute-to-agents).

## Pourquoi ça compte

Cette étude chiffre pour la première fois de façon rigoureuse l'écart potentiel entre l'offre massive de calcul IA en construction et la demande réelle en agents, un signal clé à suivre pour évaluer le risque de surcapacité et de bulle d'investissement dans l'infrastructure IA.
