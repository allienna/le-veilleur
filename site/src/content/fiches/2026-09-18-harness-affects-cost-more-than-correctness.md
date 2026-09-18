---
title: "Harness affects cost more than correctness"
date: 2026-09-18
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Farena.ai%2Fblog%2Fcoding-agents-harness-tax%3Futm_source=tldrai/1/010001a0af8f638d-dcc57c6a-1a9b-4a37-be52-1a8f5d78e44e-000000/TDH-pKFkluvepNoNbYToNK_qtaaRpWfn1MDGTKC-kUk=452"
keywords: ["agents de codage", "harness", "benchmarks", "coût des LLM", "SWE-bench", "Claude Code"]
theme: "IA"
tone: "research"
used_in: ["2026-09-18"]
---

## Résumé

Une étude (projet « HarnessTax ») compare 21 combinaisons modèle-harness — sept modèles et trois harnais (Claude Code, Codex CLI et Pi) — sur les benchmarks SWE-bench Lite et Terminal-Bench 2.0. Le constat central est que le choix du harness (le système logiciel qui gère les outils, le contexte et l'exécution des tâches d'un agent) influence bien davantage le coût d'exécution que le taux de réussite des tâches. Un harness minimaliste et open source comme Pi, qui ne propose que quatre outils (lecture, écriture, édition, bash), atteint des performances comparables à des harnais plus élaborés pour une fraction du prix. Les auteurs montrent aussi que les modèles ne sont pas systématiquement meilleurs dans le harness de leur propre fournisseur : sur douze comparaisons entre modèles Anthropic et OpenAI, un harness alternatif obtient le meilleur score dans neuf cas.

## Points clés

- Un même modèle peut atteindre un taux de réussite quasi identique avec des coûts variant jusqu'à 5x selon le harness utilisé.
- Claude Code coûte en moyenne 2,0x plus cher que Pi et 1,6x plus cher que Codex CLI sur SWE-bench Lite (et 1,5x plus cher que Pi sur Terminal-Bench 2.0), pour un écart de réussite moyen limité à environ ±2 % (SWE-bench Lite) et ±5 % (Terminal-Bench 2.0).
- Pi, harness open source réduit à quatre outils (read, write, edit, bash), se situe sur la frontière de Pareto coût/performance sur les deux benchmarks, concurrençant des harnais plus riches en fonctionnalités.
- Dans 9 comparaisons sur 12 entre modèles Anthropic et OpenAI, un harness différent de celui du fournisseur d'origine obtient le meilleur taux de réussite observé — l'optimisation propriétaire d'un fournisseur ne garantit donc pas le meilleur appariement modèle-harness.
- Les auteurs qualifient ce surcoût caché de « harness tax » : accepter le harness par défaut d'un agent de codage sans comparer d'alternatives peut faire payer une prime sans gain de qualité réel.
- Ces résultats sont obtenus sur deux benchmarks open source (potentiellement déjà vus par les modèles pendant leur entraînement) et pourraient ne pas se généraliser à d'autres charges de travail ou environnements de développement réels.

## Analyse approfondie

**Contexte.** Les modèles de langage transforment la façon de développer des logiciels et de résoudre des problèmes computationnels. Les agents de codage mettent ces capacités en œuvre via un « harness », c'est-à-dire le système logiciel qui gère les outils, le contexte et l'exécution des tâches du modèle. Si les modèles fournissent l'intelligence de base, le harness est de plus en plus perçu comme déterminant dans la façon dont cette intelligence est effectivement exploitée. Choisir un agent de codage revient donc toujours à choisir à la fois un modèle et un harness, même lorsque l'attention se porte explicitement sur le seul modèle.

Des millions de personnes utilisent déjà des agents de codage, mais l'impact réel du choix du harness reste mal compris. La question posée par les auteurs est simple : un autre harness pourrait-il permettre au même modèle de résoudre davantage de tâches, ou de réduire les coûts ?

Pour y répondre, l'équipe évalue 21 combinaisons modèle-harness, couvrant sept modèles et trois harnais — Claude Code, Codex CLI et Pi — sur les benchmarks SWE-bench Lite et Terminal-Bench 2.0. Trois résultats surprenants émergent de cette étude, détaillés ci-dessous ; les traces de profilage seront rendues publiques.

### Le harness affecte le coût plus que la justesse

Un même modèle atteint souvent un taux de réussite similaire à des coûts sensiblement différents selon le harness employé. GPT-5.6 Luna offre le coût le plus bas sur les deux benchmarks, tandis que Claude Fable 5 atteint le taux de réussite le plus élevé sur SWE-bench Lite. Kimi K3, un modèle à poids ouverts, se rapproche de la frontière de Pareto près de GPT-5.6 Sol sur SWE-bench Lite, et se situe juste en dessous de cette frontière sur Terminal-Bench 2.0. Cependant, ces modèles ne montrent pas de différences de performance substantielles selon le harness utilisé. Ainsi, Claude Fable 5 résout 97,8 % des tentatives avec Claude Code, 96,7 % avec Codex et 96,7 % avec Pi — pourtant Claude Code coûte environ deux fois plus cher que Pi (1,33 $ contre 0,67 $).

Cet écart de coût dépasse le cas de Fable 5 : sur les modèles communs aux trois harnais, Claude Code coûte environ 2,0x le prix de Pi et 1,6x celui de Codex sur SWE-bench Lite, et 1,5x celui de Pi sur Terminal-Bench 2.0 (moyennes géométriques des ratios de coût), alors que l'effet moyen du harness sur le taux de réussite reste compris dans une fourchette d'environ ±2 % sur SWE-bench Lite et ±5 % sur Terminal-Bench 2.0.

Payer davantage pour une qualité pratiquement équivalente simplement parce qu'on utilise un harness différent revient à s'acquitter d'une sorte de « taxe du harness ». Les auteurs avertissent qu'on peut payer cette taxe cachée sans s'en rendre compte lorsqu'on accepte le harness par défaut d'un agent de codage sans en comparer les alternatives. Ils concluent que les évaluations de modèles devraient systématiquement comparer coût et taux de réussite d'un même modèle à travers les harnais couramment utilisés.

### Un harness simple peut être compétitif

Pi atteint la frontière de Pareto sur les deux benchmarks en ne proposant que quatre outils : lecture, écriture, édition et bash. Pour comprendre comment la conception du harness influence les dépenses, les auteurs examinent les coûts sur l'ensemble des tentatives menées à terme, le nombre de tours enregistrés, ainsi que le contexte initial fourni au modèle.

### Les modèles peuvent être compétitifs hors du harness de leur fournisseur

L'optimisation propre à un fournisseur ne garantit pas le meilleur appariement modèle-harness. Les fournisseurs optimisent parfois leurs modèles pour leur propre environnement de codage : OpenAI, par exemple, présente GPT-5-Codex comme optimisé pour l'ingénierie logicielle au sein de Codex. Pourtant, sur les six modèles Anthropic et OpenAI testés et les deux benchmarks, un harness alternatif obtient le meilleur taux de réussite observé dans neuf comparaisons sur douze.

### Notes de fin

Les résultats montrent qu'un même modèle peut atteindre des taux de réussite similaires à des coûts substantiellement différents. Sur les benchmarks testés, des harnais open source simples peuvent être compétitifs, et les modèles peuvent bien performer hors de leur propre harness. Une « taxe du harness » peut ainsi passer inaperçue lorsqu'on se concentre uniquement sur le taux de réussite des tâches.

Toutes plateformes confondues, Pi et Codex atteignent souvent une réussite similaire à moindre coût que Claude Code. Ces conclusions pourraient toutefois être propres aux deux benchmarks open source testés, que les modèles ont pu rencontrer pendant leur entraînement ; les résultats pourraient différer sur d'autres benchmarks et charges de travail.

Des travaux antérieurs, notamment sur les agents de récupération d'information (retrieval agents), montrent déjà l'intérêt de choisir conjointement modèles et configurations système. La sélection du harness est un enjeu d'autant plus pressant pour les agents de codage, étant donné le volume et la diversité de leurs usages. La prochaine étape naturelle consiste à évaluer les harnais et à automatiser leur sélection dans des flux de développement réels, où les exigences évoluent, où les développeurs fournissent des retours, et où les tâches s'étendent sur plusieurs sessions.

Plus largement, le besoin de harnais différents dépend du rôle assigné aux agents de codage. Pour les tâches quotidiennes, ces agents sont essentiellement des interfaces vers l'intelligence du modèle : ils gèrent le contexte, l'accès aux outils et l'exécution des tâches. À mesure que les modèles deviennent plus capables, les agents de codage pourraient nécessiter moins de l'échafaudage (scaffolding) actuel. Les agents de codage généralistes devraient donc privilégier l'efficacité en coût et la fiabilité, de nombreuses tâches ne nécessitant pas de fonctionnalités additionnelles sophistiquées. Pour les problèmes plus difficiles, à la limite des capacités d'un modèle — comme la découverte scientifique —, les agents pourraient encore bénéficier de harnais offrant un guidage structuré pour explorer des idées, évaluer des candidats et apprendre du retour d'expérience. La recherche sur les harnais peut ainsi être vue comme un moyen d'aider les modèles à repousser les frontières de la connaissance. Les auteurs estiment cependant que les utilisateurs ne devraient pas avoir à faire eux-mêmes ces choix de configuration : il faudrait envisager un harness repensé, capable de s'adapter au fil des tâches tout en restant généraliste.

### Sources et remerciements

Le projet, intitulé *HarnessTax: How Much Does Harness Matter for Coding Agents?*, est publié sur harnesstax.github.io. Les auteurs remercient l'Amazon AI Fellowship pour des crédits de calcul AWS, Arena Intelligence pour le financement de l'accès API utilisé dans les expériences de profilage, ainsi que Laude pour des crédits API Anthropic ; ils remercient également Michael Chang et Tyler Griggs pour le soutien aux abonnements IA, et Mert Cemri pour ses retours sur l'article. Le laboratoire à l'origine de l'étude est soutenu par des dons d'Accenture, AMD, Anyscale, Broadcom, Google, IBM, Intel, Intesa Sanpaolo, Lambda, Mibura, Samsung SDS et SAP.

L'article s'appuie sur des références incluant notamment : les travaux d'Anthropic Research sur l'IA au travail (S. Huang et al., déc. 2025) ; AlphaEvolve de Google DeepMind (mai 2025) ; un billet d'Anthropic Engineering sur les harnais pour agents de longue durée (J. Young, nov. 2025) ; un billet d'OpenAI Engineering sur la boucle de l'agent Codex (M. Bolin, janv. 2026) ; l'article SWE-agent (J. Yang et al., NeurIPS 2024) ; une étude Databricks sur le benchmarking d'agents de codage (V. Gaba et al., juil. 2026) ; une communication d'OpenAI sur Codex (juin 2026) ; les descriptions officielles des benchmarks SWE-bench Lite et Terminal-Bench (M. Merrill et al., arXiv:2601.11868) ; un billet de Portkey sur la « taxe du harness » (S. Sambharia, avril 2026) ; la documentation du harness open source Pi ; une annonce OpenAI sur les mises à jour de Codex (sept. 2025) ; et un article sur la configuration d'agents de récupération à partir du langage naturel (M. Pan et al., arXiv:2605.27361).

## Pourquoi ça compte

Cette étude rappelle qu'en matière d'agents de codage, la performance ne dépend pas que du modèle mais tout autant du harness qui l'entoure — un point clé pour toute organisation évaluant le rapport coût/efficacité de ses outils d'IA générative avant de les déployer à grande échelle.
