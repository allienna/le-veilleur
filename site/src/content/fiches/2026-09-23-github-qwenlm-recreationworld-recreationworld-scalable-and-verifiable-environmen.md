---
title: "GitHub - QwenLM/RecreationWorld: RecreationWorld: Scalable and Verifiable Environments for Hybrid Computer-Use Agents"
date: 2026-09-23
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fgithub.com%2FQwenLM%2FRecreationWorld%3Futm_source=tldrai/1/010001a0c94ac023-ce61b09e-2653-4bb7-99c9-33f88214b103-000000/e2yvPdykEdLOzlxwur1tM3XiI3mLCgF4Z0yn_wyM6WE=452"
authors: ["Qwen Team (Alibaba)"]
keywords: ["agents IA", "computer-use", "benchmark", "Qwen", "évaluation LLM", "open source"]
theme: "IA"
tone: "research"
used_in: ["2026-09-23"]
---

## Résumé
RecreationWorld est un framework en cinq plateformes (Ubuntu, macOS, Windows, Android, Web) publié par l'équipe Qwen d'Alibaba pour étudier et entraîner des agents « hybrid computer-use » capables d'alterner exploration d'interfaces graphiques, implémentation via des outils de code, et vérification visuelle de leurs propres artefacts. Le projet transforme des applications open source en un oracle exécutable de référence, générant une expérience d'entraînement scalable et vérifiable qui se transfère au-delà de la seule tâche de recréation. Il s'accompagne de RecreationBench, un banc d'essai de 250 tâches évaluées de façon programmatique et visuelle par rapport à une référence. Sur ce benchmark, GPT-6 Astra domine largement le classement (58,06 % de score moyen), devant Claude Opus 5, GPT-5.6 Sol et une série d'autres modèles, avec des écarts de coût par tâche très marqués.

## Points clés
- Boucle récurrente « explorer–implémenter–vérifier » plutôt qu'un pipeline figé en étapes fixes.
- Évaluation fondée sur le comportement observable (assertions programmatiques et visuelles validées par la référence), pas sur la similarité au code source — les implémentations peuvent utiliser des langages ou architectures différents.
- RecreationBench couvre 250 tâches réparties sur 5 plateformes (50 par plateforme), chacune avec sa propre interface d'évaluation (AT-SPI, AXUIElement, UI Automation, UiAutomator, assertions navigateur).
- GPT-6 Astra en tête (58,06 % de moyenne), suivi de Claude Opus 5 (44,16 %) et GPT-5.6 Sol (42,06 %) ; les modèles Qwen, Kimi, GLM et Gemini restent nettement en retrait.
- Coûts estimés par tâche très hétérogènes, de 1,23 $ (Qwen3.7-Plus) à plus de 117 $ (Claude Opus 5), en supposant 90 % de lectures en cache.
- Environnement, code et jeux de tâches publiés sous licence MIT, avec données disponibles sur Hugging Face et ModelScope.

## Analyse approfondie
*Environnements scalables et vérifiables pour agents hybrides d'utilisation d'ordinateur*

Site web · Rapport · Hugging Face · ModelScope

Résultats · Démarrage rapide · Citation

RecreationWorld est un framework à cinq plateformes conçu pour étudier et améliorer les **agents hybrides d'utilisation d'ordinateur** (hybrid computer-use agents) qui interfolent de manière autonome l'exploration d'interfaces graphiques (GUI), l'implémentation à l'aide d'outils de codage, et la vérification visuelle de leurs propres artefacts en cours d'exécution. En construisant la recréation autour d'une référence en fonctionnement utilisée comme oracle exécutable, le framework transforme des applications open source en une expérience d'entraînement scalable et vérifiable, qui se transfère au-delà du seul cadre de la recréation, tandis que RecreationBench fournit 250 tâches mises de côté (held-out) avec une évaluation programmatique et visuelle ancrée dans la référence.

Chaque tâche fournit à l'agent une requête de haut niveau, un accès interactif à une référence en cours d'exécution, ainsi que des outils de contrôle GUI et de développement logiciel. L'agent décide lui-même quand explorer la référence, implémenter le code source, construire et lancer son candidat, inspecter le résultat, puis le réviser — formant une boucle récurrente **explorer–implémenter–vérifier** plutôt qu'une séquence figée d'étapes.

Le candidat final est évalué par une suite figée d'assertions programmatiques et visuelles validées par la référence. Le score dépend du comportement observable plutôt que de la similarité au niveau du code source, de sorte que les implémentations restent libres d'utiliser des langages, frameworks et architectures différents.

Les scores sont moyennés (macro-average) au sein de chaque plateforme, puis pondérés également entre les plateformes. La « Moyenne » est la moyenne non pondérée de Prog et VLM ; les coûts estimés supposent 90 % de lectures en cache.

| Modèle | Prog (%) | VLM (%) | Moyenne (%) | Prog ≥ 90 % (% d'apps) | Prog = 100 % (% d'apps) | Coût estimé (USD/tâche) |
|---|---|---|---|---|---|---|
| GPT-6 Astra | 58,19 | 57,92 | 58,06 | 17,60 | 2,80 | 115,80 |
| Claude Opus 5 | 45,99 | 42,34 | 44,16 | 5,53 | 0,80 | 117,17 |
| GPT-5.6 Sol | 40,63 | 43,49 | 42,06 | 5,20 | 0,40 | 25,46 |
| Grok 4.6 | 39,02 | 34,45 | 36,73 | 1,60 | 0,00 | 12,58 |
| Qwen3.8-Max-0902 | 35,53 | 34,07 | 34,80 | 2,00 | 0,00 | 38,76 |
| Kimi K3 | 32,07 | 30,74 | 31,41 | 2,00 | 0,00 | 63,10 |
| Claude Opus 4.8 | 32,40 | 29,81 | 31,10 | 1,60 | 0,40 | 69,16 |
| GLM-5.3 | 26,30 | 22,46 | 24,38 | 2,00 | 0,00 | 70,98 |
| Gemini 3.7 Flash | 24,91 | 17,34 | 21,12 | 2,40 | 0,00 | — |
| Qwen3.7-Plus | 9,18 | 9,12 | 9,15 | 0,00 | 0,00 | 1,23 |

Installez uv, puis exécutez depuis la racine du dépôt :

```
uv sync
uv run rb run --help
```

Une exécution notée nécessite également un lot de tâches figé correspondant, provenant de Hugging Face ou ModelScope, un environnement d'exécution préparé, ainsi que des points de terminaison (endpoints) pour le modèle et le juge. Choisissez une plateforme pour la configuration et les exécutions par lot :

| Plateforme | Tâches | Interface d'évaluation | Configuration et exécution |
|---|---|---|---|
| Ubuntu | 50 | AT-SPI | Guide Linux |
| macOS | 50 | AXUIElement | Guide macOS |
| Windows | 50 | UI Automation | Guide Windows |
| Android | 50 | UiAutomator | Guide Android |
| Web | 50 | Assertions navigateur | Guide Web |

L'index canonique des tâches se trouve dans `tasks/`.

Pour vérifier l'installation, exécutez ces contrôles hors ligne ; ils ne nécessitent ni données de benchmark ni identifiants :

```
uv run python scripts/release/smoke_providers.py
uv run python scripts/release/smoke_runtime.py
```

Pour toute question, contactez xiezhihui.xzh@alibaba-inc.com ou gaochang.gao@alibaba-inc.com.

Si vous trouvez cet environnement utile, merci de bien vouloir le citer :

```
@misc{qwen2026recreationworld,
      title={RecreationWorld: Scalable and Verifiable Environments for Hybrid Computer-Use Agents},
      author={Shuai Bai and Jiayong Deng and Sicheng Fan and Yikun Fu and Chang Gao and Xuhao Hu and Mianqiu Huang and Yizhen Jiang and Yuheng Jing and Dehui Kong and Keliang Li and Ning Li and Wanli Li and Dayiheng Liu and Dunjie Lu and Changwei Luo and Que Shen and Zheyuan Wang and Zijian Wang and Jie Wu and Gao Wu and Zhihui Xie and Rui Xie and Haiyang Xu and An Yang and Jiakang Yuan and Yanming Zhang and Jiajun Zhang and Xi Zhang and Zhenru Zhang and Zhuo Zhen and Mingkang Zhu and Bowen Zhou},
      year={2026},
      eprint={2609.22000},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2609.22000},
}
```

Publié sous licence MIT. Les composants tiers conservent leurs licences d'origine ; voir `THIRD_PARTY_NOTICES.md`.

## Pourquoi ça compte
Ce projet illustre une tendance forte de la veille IA 2026 : le passage de benchmarks statiques à des environnements exécutables et vérifiables pour évaluer les agents autonomes sur des tâches réelles d'utilisation d'ordinateur. Le classement révélant un écart net entre GPT-6 Astra et les modèles Claude/Qwen/Grok donne un signal concret sur l'état de la compétition entre laboratoires sur les capacités agentiques.
