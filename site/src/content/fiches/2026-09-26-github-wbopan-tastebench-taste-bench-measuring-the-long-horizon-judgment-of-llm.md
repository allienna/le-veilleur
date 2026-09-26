---
title: "GitHub - wbopan/tastebench: Taste-Bench: measuring the long-horizon judgment of LLM agents at real decision forks"
date: 2026-09-26
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fgithub.com%2Fwbopan%2Ftastebench%3Futm_source=tldrai/1/010001a0d8c27fe0-6c9b409a-b363-4068-b435-524fdf752c58-000000/fnWAKEWKmEDaUckpggJpL0PC85V5ST-jNyvwGC6yMZ8=452"
authors: ["Wenbo Pan", "Zhichao Liu", "Shujie Liu", "Jingying Zeng", "Chin-Yew Lin", "Xianfeng Tang", "Yan Lu", "Qi He", "Xiaohua Jia"]
keywords: ["agents LLM", "benchmark", "prise de décision", "ingénierie logicielle", "évaluation de modèles", "long horizon"]
theme: "IA"
tone: "research"
used_in: ["2026-09-26"]
---

## Résumé
Taste-Bench est un benchmark qui évalue le « goût » (taste) des agents LLM, c'est-à-dire leur capacité à choisir la meilleure direction à un embranchement décisionnel réel au sein d'une tâche à long horizon. Les 502 questions du jeu de données sont extraites de trajectoires réelles d'ingénierie logicielle et de recherche en machine learning (SWE-bench, SWE-bench Pro, METR MALT), sans annotation d'expert : c'est le déroulement ultérieur de la trajectoire qui révèle rétrospectivement quel choix était le bon. Le meilleur modèle de pointe testé, GPT-5.6 Sol, ne répond correctement qu'à 59,7 % des questions, et le protocole exige une réponse correcte dans les deux ordres de présentation des options pour neutraliser le hasard. Le code est sous licence MIT et le jeu de données sous licence CC BY 4.0, avec accès restreint (gated) sur Hugging Face pour limiter la contamination des entraînements.

## Points clés
- Taste-Bench mesure la capacité d'un agent LLM à choisir la bonne direction à un « fork » décisionnel dans une tâche longue, avant que les conséquences ne soient visibles.
- 502 questions retenues sur 4 657 embranchements extraits, réparties en deux constructions (« parallel forks » et « detour forks ») et deux domaines (ingénierie logicielle et recherche ML).
- Chaque question est posée dans les deux ordres d'options ; une réponse n'est jugée correcte que si le modèle réussit dans les deux cas, ce qui ramène le score du hasard à 25 et celui d'un biais de position fixe à 0.
- Meilleur score : GPT-5.6 Sol avec 59,7 % de moyenne, suivi de près par GPT-5.5 (59,5 %) ; Claude Opus 5 arrive à 55,5 % et Claude Sonnet 5 à 51,6 %.
- Les modèles les plus faibles (ex. Grok 4.20 Reasoning à 15,7 %) échouent aussi massivement à produire une réponse exploitable (jusqu'à 459 sorties non analysables sur 1 004).
- Le jeu de données et le code sont publics (dataset gated sur Hugging Face, code MIT), avec un protocole reproductible via une CLI (`tb download`, `tb run`, `tb score`).

## Analyse approfondie
Taste-Bench mesure le *goût* (taste) d'un agent LLM : sa capacité à choisir la meilleure direction à un embranchement décisionnel réel dans une tâche à long horizon. Étant donné la tâche, la trajectoire jusqu'à l'embranchement, et deux étapes suivantes candidates, le modèle doit choisir l'étape que le reste caché de la trajectoire prouve être la bonne. Un mauvais choix semble souvent raisonnable sur le moment et coûte à l'agent la majeure partie de son budget plus tard. Les 502 questions sont extraites de trajectoires d'ingénierie logicielle et de recherche en machine learning, sans annotation d'expert, et le meilleur modèle de pointe (frontier model) répond correctement à 59,7 % d'entre elles.

*Un embranchement décisionnel issu d'une trajectoire de machine learning. Le modèle choisit avant que les pertes (losses) ultérieures ne révèlent que A est la meilleure option.*

Une question ne compte comme correcte que si le modèle y répond correctement dans les deux ordres d'options, si bien qu'une réponse aléatoire obtient un score de 25 et qu'un modèle qui choisit toujours la même position obtient 0. La colonne « Average » est la moyenne 1:1 des sous-ensembles recherche et ingénierie.

| Modèle | Average | D-Eng | D-Res | P-Eng | P-Res | Unparsed |
|---|---|---|---|---|---|---|
| GPT-5.6 Sol | 59,7 | 48,1 | 67,2 | 75,8 | 56,2 | 0 |
| GPT-5.5 | 59,5 | 47,4 | 68,8 | 73,4 | 56,2 | 0 |
| Claude Opus 5 | 55,5 | 35,3 | 64,1 | 71,0 | 64,6 | 0 |
| Grok 4.5 | 54,6 | 47,7 | 57,8 | 61,3 | 56,2 | 10 |
| GPT-5.6 Terra | 54,0 | 40,6 | 57,8 | 70,2 | 58,3 | 0 |
| GLM-5.2 | 53,9 | 40,2 | 59,4 | 64,5 | 60,4 | 17 |
| Claude Sonnet 5 | 51,6 | 36,1 | 60,9 | 62,1 | 56,2 | 0 |
| GPT-5.6 Luna | 49,0 | 32,3 | 57,8 | 67,7 | 50,0 | 0 |
| MiniMax M3 | 45,3 | 34,6 | 39,1 | 64,5 | 56,2 | 3 |
| DeepSeek V4 Flash | 43,3 | 29,3 | 46,9 | 58,1 | 50,0 | 2 |
| GPT-5.4 Mini | 40,1 | 25,2 | 54,7 | 26,6 | 54,2 | 112 |
| Mistral Medium 3.5 | 37,7 | 40,6 | 28,1 | 43,5 | 41,7 | 24 |
| GPT-5.4 Nano | 36,6 | 25,6 | 39,1 | 46,0 | 43,8 | 93 |
| Grok 4.20 Reasoning | 15,7 | 19,9 | 9,4 | 28,2 | 8,3 | 459 |

*D = detour (détour), P = parallel (parallèle) ; Eng = engineering (ingénierie, 390 questions), Res = research (recherche, 112). Les présentations non analysées (unparsed), sur 1 004, comptent comme fausses. Toutes les lignes utilisent le protocole `paired_order_v1`, août 2026. Pour ajouter un modèle, exécutez le protocole complet et ouvrez une pull request avec son `summary.json` sous `results/<model>/`.*

La partie ultérieure d'une trajectoire constitue une preuve rétrospective (hindsight) de la décision prise à l'embranchement, de sorte que les trajectoires s'auto-étiquettent. Les questions se déclinent en deux constructions et deux domaines.

- **Embranchements parallèles (Parallel forks).** Des tentatives indépendantes sur la même tâche divergent au même point et se terminent par des résultats enregistrés différents. Le résultat de chaque tentative étiquette la meilleure direction.
- **Embranchements de détour (Detour forks).** Un agent prend une direction, l'abandonne après avoir observé un échec, puis se rétablit au sein de la même exécution (run). La direction abandonnée et le rétablissement ultérieur constituent les candidats.
- **Filtrage.** Une question est écartée comme *triviale* lorsque chaque modèle juge y répond à partir du seul libellé des candidats, et comme *indécidable* lorsqu'un juge quelconque conteste son étiquette après avoir lu l'enregistrement complet. Sur 4 657 embranchements extraits, 502 survivent : 266 questions de détour et 124 de type parallèle en ingénierie (rollouts SWE-bench et SWE-bench Pro), 64 de détour et 48 parallèles en recherche (runs RE-Bench et HCAST de la publication MALT de METR).

## **Exemple de question** (parallèle, ingénierie)

**Tâche.** Modifier le code source de production de NodeBB pour que le point de terminaison (endpoint) d'upload de fichiers admin valide le dossier demandé avant l'enregistrement. Résoudre le dossier en utilisant `nconf.get('upload_path')` configuré comme base, rejeter les cibles manquantes ou qui ne sont pas des répertoires avec `[[error:invalid-path]]`, et empêcher les chemins de sortir de la racine d'upload.

**Progression.** 30 étapes enregistrées : l'agent a inspecté le harnais (harness), trouvé le contrôleur d'upload admin et ses tests, et lu les fonctions utilitaires de fichiers environnantes.

**A.** Ajouter une fonction utilitaire ciblée de vérification d'existence du dossier, qui résout la cible sous la racine d'upload configurée et vérifie qu'il s'agit bien d'un répertoire. Avant d'appeler la fonction de sauvegarde, rejeter les cibles invalides avec `[[error:invalid-path]]` et supprimer le fichier temporaire uploadé.

**B.** Intégrer en ligne (inline), dans le bloc try/catch de sauvegarde existant du contrôleur, les vérifications de confinement à la racine d'upload et de statut du répertoire. Lever `[[error:invalid-path]]` pour les cibles invalides et laisser le catch existant transmettre l'erreur via `next`.

Caché au modèle : **A** est la bonne réponse. La tentative ayant pris la direction A a passé les tests cachés ; B a transmis l'erreur sans nettoyer l'upload temporaire, et sa tentative a échoué.

Spécifié dans `protocol/paired_order_v1.yaml`. Le modèle voit la tâche, la trajectoire complète précédant la décision telle que publiée dans `prefix_text` (identifiants et noms d'utilisateur expurgés, budget de 64 000 tokens avec un marqueur d'omission explicite en cas de dépassement), ainsi que les deux candidats. Le prompt demande une seule ligne, `ANSWER: X`, sans chaîne de raisonnement (chain of thought) visible. Chaque question est posée dans l'ordre des options tel que publié, puis dans son exact inverse, avec les lettres recalculées à chaque fois. Le dénominateur est constitué de toutes les questions publiées, et les erreurs de requête ainsi que les sorties non analysables comptent comme fausses. `tb validate` vérifie les hachages (hashes) de la publication et les invariants de chaque question.

L'accès au jeu de données est restreint (gated) afin de limiter la contamination des entraînements : demandez l'accès sur sa page Hugging Face, puis exécutez `hf auth login` une seule fois.

```
git clone https://github.com/wbopan/tastebench && cd tastebench && uv sync
uv run tb download                                   # wenbopan/taste-bench@v1.0 dans ./data
export TASTEBENCH_API_KEY=...                        # tout endpoint compatible OpenAI
uv run tb run --model gpt-5.5 --api https://api.openai.com/v1/chat/completions
uv run tb score runs/gpt-5.5/<date>                  # affiche l'exactitude par cellule et la moyenne (Average)
```

`tb run` écrit un enregistrement par question et par ordre, est reprenable (resumable), et accepte `--limit N` pour des tests rapides (smoke tests). Une exécution complète représente 1 004 requêtes et environ 8 millions de tokens en entrée. Les paramètres de requête propres à chaque modèle se trouvent dans `configs/models.yaml`.

Les données elles-mêmes se présentent sous forme de deux configurations parquet, `engineering` (390 lignes) et `research` (112 lignes), chacune avec un split `test`. Une ligne contient `query`, le `prefix_text` complet, les deux `choices` dans l'ordre publié, et la lettre `answer`, ainsi que `cell`, `task_id`, et un canari de contamination (contamination canary). Elles se chargent sans ce dépôt :

```
from datasets import load_dataset
rows = load_dataset("wenbopan/taste-bench", "engineering", split="test", revision="v1.0")
```

```
@article{pan2026tasteful,
  title   = {The Tasteful Agent: Measuring and Improving Taste in Long-Horizon Tasks},
  author  = {Pan, Wenbo and Liu, Zhichao and Liu, Shujie and Zeng, Jingying and Lin, Chin-Yew and Tang, Xianfeng and Lu, Yan and He, Qi and Jia, Xiaohua},
  journal = {arXiv preprint arXiv:2609.25804},
  year    = {2026}
}
```

Les trajectoires proviennent de SWE-bench, SWE-bench Pro, et de la publication MALT de METR. Le code est publié sous licence MIT et le texte du jeu de données sous licence CC BY 4.0.

## Pourquoi ça compte
Taste-Bench apporte une mesure chiffrée et reproductible d'une faiblesse peu couverte jusqu'ici : le jugement des agents LLM face à des choix ambigus dans des tâches longues, là où l'erreur ne se révèle que bien plus tard. C'est un signal utile pour la veille sur l'évaluation des agents autonomes, à l'heure où les modèles de pointe plafonnent encore autour de 55-60 % sur ce type de décision, loin d'une fiabilité suffisante pour de l'autonomie prolongée en production.
