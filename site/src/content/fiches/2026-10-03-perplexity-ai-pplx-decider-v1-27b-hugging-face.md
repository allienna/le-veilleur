---
title: "perplexity-ai/pplx-decider-v1-27b · Hugging Face"
date: 2026-10-03
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fhuggingface.co%2Fperplexity-ai%2Fpplx-decider-v1-27b%3Futm_source=tldrai/1/010001a0fccd7a72-672389f9-e11b-4cda-ac15-a4ea0d841b32-000000/Py8zGgPfkI61V5pd0SMIjmiYYFqsCbvg6ivz8Y2O04A=452"
authors: ["Perplexity AI"]
keywords: ["modèle de décision", "Perplexity AI", "Qwen3.8-27B", "benchmarks", "routage de tâches", "Hugging Face"]
theme: "IA"
tone: "research"
used_in: ["2026-10-03"]
---

## Résumé
Perplexity AI publie sur Hugging Face pplx-decider-v1-27b, un modèle de décision affiné à partir de Qwen3.8-27B, destiné aux tâches de classification et de routage (choix multiple ou réponse oui/non) avec probabilités calibrées. Évalué sur 11 benchmarks via l'API Perplexity, il obtient une précision moyenne de 85,71 %, dépassant à la fois son modèle de base Qwen3.8-27B (74,76 %) et un modèle de référence nommé « Jev » (84,51 %). Il tourne sur une seule GPU CUDA avec environ 49 Gio de mémoire pour les poids, et s'installe facilement via `uv`. Le modèle accepte aussi des images en entrée pour la prise de décision.

## Points clés
- Modèle affiné à partir de Qwen3.8-27B, spécialisé dans les tâches de décision/classification plutôt que la génération de texte libre.
- Précision globale de 85,71 %, supérieure à Qwen3.8-27B (74,76 %) et au modèle de référence « Jev » (84,51 %) sur 11 benchmarks.
- Gains particulièrement marqués sur RAGTruth (88,80 % contre 61,53 % pour Qwen3.8-27B) et FinancialPhraseBank (84,18 %).
- Nécessite Python 3.12+ et un GPU CUDA avec environ 49 Gio de mémoire disponible pour les poids.
- API simple (`predict`) supportant les choix multiples, les questions oui/non et les entrées image, avec probabilités calibrées en sortie.
- Cas d'usage typique : routage automatique de requêtes (ex. tickets support) ou détection d'intention/urgence.

## Analyse approfondie
pplx-decider-v1-27b est un modèle de décision affiné (fine-tuné) à partir de Qwen3.8-27B.

Précision sur 11 benchmarks. Les résultats de pplx-decider-v1-27b ont été mesurés via l'API Perplexity.

| Benchmark | Jev | Qwen3.8-27B | pplx-decider-v1-27b |
|---|---|---|---|
| WinoGrande | **90,70 %** | 73,10 % | 83,30 % |
| FinancialPhraseBank | 76,98 % | 75,68 % | **84,18 %** |
| RAGTruth | 77,27 % | 61,53 % | **88,80 %** |
| JudgeBench | **78,57 %** | 68,86 % | 78,29 % |
| BBH | **94,27 %** | 72,80 % | 82,80 % |
| JevBench public hard | **73,27 %** | 72,28 % | 70,30 % |
| TabFact | 89,80 % | 78,60 % | **90,60 %** |
| ContractNLI | 77,45 % | **80,78 %** | **80,78 %** |
| Circa | 84,60 % | 87,00 % | **89,20 %** |
| Belebele | **95,00 %** | 93,20 % | 94,00 % |
| TruthfulQA binary | **92,00 %** | 82,80 % | 85,40 % |
| Overall | 84,51 % | 74,76 % | **85,71 %** |

Le gras indique le meilleur score pour chaque ligne.

Python 3.12+ et un GPU CUDA disposant d'environ 49 Gio pour les poids, plus de la mémoire de travail supplémentaire.

Téléchargez et exécutez l'exemple d'inférence avec uv :

```
uvx --from huggingface-hub hf download perplexity-ai/pplx-decider-v1-27b inference.py --local-dir .
uv run inference.py
```
uv installe les dépendances ; le script télécharge le modèle depuis Hugging Face. Dans un environnement où ces dépendances sont déjà installées, utilisez directement `Decider` :

```
from inference import Decider
model = Decider.from_pretrained("perplexity-ai/pplx-decider-v1-27b")
result = model.predict(
    "My Stripe integration keeps failing. Please help ASAP.",
    {
        "type": "choice",
        "instructions": "Which team should handle this request?",
        "criteria": {
            "billing": "Charges and refunds",
            "technical_support": "Integration errors",
            "sales": "Questions about buying a product",
        },
    },
)
print(result)  # Choix sélectionné et probabilités calibrées.
```
Utilisez `{"type": "noul", "instructions": "Does this message express urgency?"}` pour obtenir une probabilité oui/non. Pour les images, passez `images=["screenshot.png"]` à `predict`, ou exécutez :

```
uv run inference.py --image screenshot.png
```
- Téléchargements le mois dernier
- 165

## Pourquoi ça compte
Ce modèle illustre une tendance à spécialiser des LLM non pas pour la génération de texte mais pour des tâches de décision/routage à faible latence avec probabilités calibrées, un segment utile pour l'automatisation de workflows (support client, triage) plutôt que pour le chat généraliste.
