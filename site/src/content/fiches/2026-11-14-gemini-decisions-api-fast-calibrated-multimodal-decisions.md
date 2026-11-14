---
title: "Gemini Decisions API: Fast, calibrated multimodal decisions"
date: 2026-11-14
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fblog.google%2Finnovation-and-ai%2Ftechnology%2Fdevelopers-tools%2Fgemini-decisions-api%2F%3Futm_source=tldrit/1/010001a1d510cfb8-3a9bc1a4-acd1-45e1-94ef-c194a4a5b67b-000000/9IfZl0YhC1mA4BHOmtGkFpeHf49yDVldI2YcCCGsU_Y=452"
keywords: ["Gemini", "API", "intelligence artificielle", "multimodal", "classification", "latence"]
theme: "IA"
tone: "news"
used_in: ["2026-11-14"]
---

## Résumé

Google lance la Gemini Decisions API, un nouvel endpoint basé sur le modèle Gemini Decision 1, conçu pour des décisions rapides à choix fermé (oui/non, choix multiple, score) plutôt que pour la génération de texte libre. Elle traite des entrées multimodales (texte, image, audio, vidéo, PDF jusqu'à 256 000 tokens) et jusqu'à 1 000 questions par requête en 150-250 ms, pour 0,10 $ par million de tokens d'entrée et aucun coût de sortie — soit environ 5 fois moins cher que Gemini 3.5 Flash-Lite via l'Interactions API. Plusieurs équipes internes de Google (Gemini Notebook, Stitch, CC, Search) l'utilisent déjà en production pour du routage de modèles, de la génération rapide d'interfaces, de la sélection d'emoji et de la détection de comportements adversariaux. L'API est disponible dès maintenant via Google AI Studio, avec des intégrations écosystème à venir (LangChain, Vercel, OpenRouter, etc.).

## Points clés

- Nouveau modèle gemini-decision-1 qui note des options candidates en une seule passe directe au lieu de générer du texte token par token.
- Trois types de décision supportés : noul (oui/non), choice (choix multiple jusqu'à 255 options) et score (grille ordonnée), chacun accompagné d'un score de confiance.
- Entrée multimodale unique (texte, image, audio, vidéo, PDF) jusqu'à 256 000 tokens, avec jusqu'à 1 000 questions indépendantes par requête.
- Latence de bout en bout de 150-250 ms, quasi stable de 1 à 100 questions, et coût environ 5 fois inférieur à Gemini 3.5 Flash-Lite via l'Interactions API.
- Tarification de 0,10 $ par million de tokens d'entrée, 0 $ pour la sortie, avec facturation unique de l'input partagé par requête.
- Déjà utilisé en interne chez Google (Notebook, Stitch, CC, Search) et intégrations écosystème en cours (LangChain, Vercel, OpenRouter, LiteLLM, etc.).

## Analyse approfondie

# Gemini Decisions API : des décisions multimodales rapides et calibrées

Aujourd'hui, nous lançons la Gemini Decisions API, un nouveau endpoint destiné aux décisions rapides et à choix fermé, propulsé par notre nouveau modèle Gemini Decision 1 (gemini-decision-1), disponible via la Gemini API dans Google AI Studio.

La Decisions API offre des primitives conçues spécifiquement pour des choix bornés tels que la sélection d'outils, les vérifications de politique, le routage de modèles et l'évaluation du contexte. Vous pouvez transmettre une entrée multimodale unique mêlant texte, images, audio, vidéo et PDF (jusqu'à 256 000 tokens), accompagnée de jusqu'à 1 000 questions indépendantes. Plutôt que de générer du texte token par token, Gemini Decision 1 note vos options candidates en une seule passe directe, en renvoyant des probabilités et des scores de confiance avec une latence de bout en bout de 150 à 250 ms, pour 0,10 $ par million de tokens d'entrée et aucun token de sortie facturé.

## Performances solides et bonne calibration

Sur des benchmarks couvrant le routage d'agents, le raisonnement, le classement et la compréhension multimodale, Gemini Decision 1 arrive en tête de la suite, avec la plus faible erreur de calibration.

Gemini Decision 1 note les options sans décodage token par token, ce qui maintient une latence médiane de calcul du modèle de 50 à 100 ms (150-250 ms de bout en bout), quel que soit le type d'entrée multimodale et pour des contextes allant jusqu'à 16 000 tokens, restant quasiment stable de 1 à 100 questions par requête. Avec zéro token de sortie facturé, Gemini Decision 1 associé à la Decisions API est près de 5 fois moins coûteux sur l'ensemble du benchmark partagé que Gemini 3.5 Flash-Lite avec l'Interactions API.

## Une évaluation multimodale native sur trois types de décision en une seule passe

Construit sur l'architecture multimodale native de Gemini, Gemini Decision 1 peut traiter directement du texte, des images, de l'audio, de la vidéo et des PDF en une seule passe directe. Vous pouvez combiner plusieurs modalités dans une entrée partagée unique, par exemple en associant l'enregistrement d'un appel à des métadonnées de compte, ou un PDF de sinistre scanné à des photos de dégâts, et ajuster la résolution des entrées image et vidéo pour contrôler le niveau de détail visuel et le coût en tokens.

Vous pouvez évaluer plusieurs questions par rapport à cette entrée partagée en une seule requête, en mélangeant des vérifications oui/non, des choix multiples et des notes selon une grille. Chaque réponse inclut un score de confiance (de 0 à 1) afin que votre code puisse router les cas ambigus vers une solution de repli ou un relecteur humain :

- **noul (Oui/Non) :** Estime la probabilité qu'une condition oui/non soit vraie, avec des critères de description optionnels pour le vrai et le faux.
- **choice (Choix multiple) :** Sélectionne parmi 2 à 255 choix, en renvoyant le gagnant ainsi que les probabilités normalisées de chaque candidat.
- **score (Grille ordonnée) :** Note les entrées selon une grille ordonnée (démarrant à 0), en renvoyant un score pondéré continu ainsi que les probabilités par niveau.

Le champ `input` utilise le même format de bloc `Content` que l'Interactions API. Voici comment vérifier une photo du comptoir d'une salle de pause, accompagnée d'une note texte, selon les trois types de questions en une seule requête :

```
from google import genai
client = genai.Client(http_options={"api_version": "v1beta"})
result = client.decisions.create(
    model="gemini-decision-1",
    input=[{
            "type": "image",
            "uri": "https://storage.googleapis.com/generativeai-downloads/images/spill.jpg",
            "mime_type": "image/jpeg",
        },
        {
            "type": "text",
            "text": "Breakroom counter check before the 9 AM client meeting.",
        },
    ],
    questions={
        "has_spill": {
            "type": "noul",
            "instructions": "Is there an uncleaned liquid spill on the counter?",
        },
        "next_action": {
            "type": "choice",
            "instructions": "Which cleanup action fits the scene?",
            "criteria": {
                "wipe_with_cloth": "Small counter spill with a cloth or towel already nearby.",
                "dispatch_janitorial": "Large floor hazard, broken glass, or active leak.",
                "ready_for_meeting": "Counter is clean and ready.",
            },
        },
        "severity": {
            "type": "score",
            "instructions": "Rate the severity of the counter mess.",
            "criteria": [
                "Clean and ready.",
                "Minor localized spill.",
                "Major spill or safety hazard.",
            ],
        },
    },
)
```

## Comment les équipes utilisent la Decisions API

Plusieurs équipes de Google utilisent déjà la Decisions API comme plan de contrôle à faible latence, en livrant des fonctionnalités simplement en définissant des options plutôt qu'en entraînant des classificateurs personnalisés ou en attendant des appels génératifs :

- **Routage de modèles dynamique dans Gemini Notebook :** Gemini Notebook utilise la Decisions API comme routeur en temps réel pour diriger instantanément les requêtes entrantes vers le modèle et le niveau de raisonnement optimaux pour chaque demande. La Decisions API classe l'intention en quelques millisecondes afin de traiter les requêtes courantes avec une latence réduite jusqu'à 40 %, tout en réservant les modèles à raisonnement approfondi aux tâches complexes.
- **Itération rapide de design dans Stitch :** La nouvelle expérimentation de canevas rapide dans Stitch utilise la Decisions API pour générer des wireframes jouables d'un parcours produit en quelques secondes, et pour appliquer presque instantanément des modifications faites à la voix ou au toucher. Lorsque le flux convient, un seul clic transfère les écrans vers l'expérience Stitch complète pour un travail de design plus approfondi.
- **Sélection d'emoji dans CC :** CC de Google Labs utilise la Decisions API pour choisir la bonne réaction emoji parmi une palette de plus de 200 options en une fraction de seconde, afin que les réactions apparaissent instantanément sans ajouter de latence.
- **Couche de sécurité pour les outils MCP dans Search :** Google Search utilise la Decisions API pour détecter les comportements et contenus adversariaux, avec une forte efficacité face aux évaluations adversariales, tout en respectant la contrainte de latence.

Stitch Rapid utilise la Decisions API pour concevoir un parcours produit complet en quelques secondes (vitesse x1).

## Commencez à développer dès aujourd'hui

Gemini Decision 1 est tarifé à 0,10 $ par million de tokens d'entrée et 0 $ pour les tokens de sortie, avec un palier gratuit de l'API disponible dans Google AI Studio pour le prototypage. Votre entrée `input` partagée est facturée une seule fois par requête, quel que soit le nombre de questions évaluées (chaque question n'ajoute que les tokens de ses propres instructions et critères). Il n'y a ni frais sur les tokens de sortie, ni facturation variable de tokens de réflexion, ni coûts séparés de transcription audio ou d'OCR.

Vous pouvez commencer à développer dès aujourd'hui en obtenant une clé API dans Google AI Studio, en testant nos applications de démonstration Doorstep Parcels, Speed Sketch et Find the Zoo Keeper, et en suivant les guides Python, JavaScript et REST de la documentation de la Decisions API.

Les intégrations avec l'écosystème se déploient progressivement sur OpenRouter, LangChain, Vercel, LiteLLM, Pydantic AI, Pipecat, LiveKit et OpenCode, en plus des SDK `google-genai`, avec un support à venir pour Gemini dans Google Cloud.

## Pourquoi ça compte

Cette API illustre une tendance de fond : spécialiser des modèles pour des tâches de classification/décision à faible latence et faible coût plutôt que de tout faire passer par des LLM génératifs classiques, ce qui peut rebattre les cartes de l'architecture des pipelines agentiques (routage, modération, contrôle qualité) en matière de coûts et de latence.
