---
title: "Co-Evolving Harnesses and Models: On-Policy Correction Helps Weaker Models Catch Up Where Imitation Fails"
date: 2026-09-12
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Farxiv.org%2Fabs%2F2609.09134%3Futm_source=tldrai/1/010001a090aa182a-d18dee2c-9abe-499b-abe2-6b2b9843ff74-000000/NZY5-2hj1o2V8NfdAo8vs-g5dfJ3YRnPCMHRUM05U1w=452"
keywords: ["agents IA", "fine-tuning", "harnais d'agent", "imitation learning", "co-évolution modèle-scaffolding"]
theme: "IA"
tone: "research"
used_in: ["2026-09-12"]
---

## Résumé
Cet article de recherche (arXiv) étudie comment combiner deux leviers d'amélioration des agents IA : l'évolution automatisée du « harnais » (prompt système, outils, hooks d'exécution, gestion du contexte) et le fine-tuning léger du modèle lui-même. Sur sept tâches d'agents en contexte entreprise, les auteurs montrent qu'entraîner un modèle plus faible sur les trajectoires complètes d'un modèle expert, au sein d'un harnais déjà optimisé pour le modèle faible, dégrade fortement les performances (de 4 à 30 points selon les tâches, sur Qwen3-Coder et Gemma 4). La cause identifiée est une rupture de l'adéquation modèle-harnais : le modèle faible imite le style de planification de l'expert sans avoir la compétence pour l'exécuter. La solution proposée est un pipeline de correction « on-policy », piloté par un agent meta de type MLE, qui ne fait réécrire par l'expert que le tour d'action défaillant dans les propres trajectoires du modèle faible, préservant ainsi son style de planification natif.

## Points clés
- Le harnais d'un agent (prompt, outils, hooks, gestion du contexte) est un déterminant critique du succès des tâches agentiques, au même titre que les poids du modèle.
- Faire évoluer automatiquement un harnais autour d'un modèle faible permet à ce dernier d'approcher les performances d'un modèle expert à moindre coût.
- Entraîner le modèle faible par imitation complète des trajectoires de l'expert, sous le harnais déjà évolué, fait chuter les performances sur les sept tâches testées (-4 à -30 points).
- L'imitation transfère des connaissances et augmente l'usage du scaffolding, mais casse l'adéquation entre le style de planification du modèle et le harnais conçu pour lui.
- La correction ciblée « on-policy » — ne réécrire que le tour d'action défaillant dans les rollouts propres du modèle faible — évite ce problème et cumule les gains du harnais évolué et de l'adaptation du modèle.
- Résultat : une recette de co-évolution économique et compatible entre harnais et poids, applicable à des tâches d'agents d'entreprise spécifiques à un domaine.

## Analyse approfondie
# Informatique > Intelligence Artificielle

# Titre : Co-Evolving Harnesses and Models: On-Policy Correction Helps Weaker Models Catch Up Where Imitation Fails
(Co-évolution des harnais et des modèles : la correction on-policy permet aux modèles plus faibles de rattraper leur retard là où l'imitation échoue)

Voir le PDF HTML (expérimental)

**Résumé (abstract) :** Les harnais d'agents (le prompt système, l'ensemble d'outils, les hooks d'exécution et l'échafaudage de gestion du contexte autour d'un modèle) constituent un déterminant critique de la réussite des tâches agentiques. L'évolution automatisée du harnais peut permettre à des modèles plus petits d'obtenir de bonnes performances sur des tâches spécifiques à un domaine, pour une fraction du coût d'un modèle de pointe (frontier model). Étant donné que le harnais et les poids du modèle façonnent tous deux le comportement, nous nous demandons comment l'évolution du harnais et le fine-tuning léger devraient être combinés. Sur sept tâches d'agents d'entreprise, nous faisons d'abord évoluer un harnais avec le modèle le plus faible, puis constatons qu'un expert plus puissant l'utilise souvent plus efficacement, ce qui suggère qu'une supervision par l'expert pourrait combler l'écart restant. Cependant, entraîner le modèle faible sur les trajectoires complètes de l'expert sous le harnais évolué se retourne contre nous : les performances régressent sur les sept tâches, de 4 à 30 points, aussi bien pour Qwen3-Coder que pour Gemma 4, alors que la même procédure aide sous un harnais non évolué. Notre analyse montre que l'imitation transfère des connaissances et augmente l'usage de l'échafaudage (scaffold), mais perturbe l'adéquation modèle-harnais : le modèle faible adopte la stratégie de planification de l'expert sans avoir la compétence nécessaire pour l'exécuter, et ne correspond plus au harnais qui avait évolué autour de son propre style de planification natif. Nous développons donc un pipeline de correction par l'expert on-policy, automatisé par un agent meta de niveau MLE, qui localise le tour d'action défaillant dans le propre déroulé (rollout) du modèle faible et demande à l'expert de ne réécrire que ce tour-là. Cela préserve le style de planification du modèle et combine les gains de l'évolution du harnais et de l'adaptation du modèle. Nos résultats identifient et résolvent une source de conflit entre les mises à jour du harnais et celles des poids, aboutissant à une recette préservant la compatibilité pour une co-évolution économique sur des tâches d'entreprise spécifiques à un domaine.

# Outils bibliographiques et de citation

# Code, données et médias associés à cet article

# Démonstrations

# Outils de recommandation et de recherche

# arXivLabs : projets expérimentaux avec des collaborateurs de la communauté

arXivLabs est un cadre qui permet à des collaborateurs de développer et de partager de nouvelles fonctionnalités arXiv directement sur le site.

Les individus et organisations qui travaillent avec arXivLabs ont adopté et accepté nos valeurs d'ouverture, de communauté, d'excellence et de respect de la vie privée des données des utilisateurs. arXiv s'engage à respecter ces valeurs et ne travaille qu'avec des partenaires qui y adhèrent.

Vous avez une idée de projet qui apporterait de la valeur à la communauté arXiv ? **En savoir plus sur arXivLabs**.

## Pourquoi ça compte
Ce papier apporte une leçon concrète et actionnable pour quiconque construit des agents IA en production : copier bêtement les trajectoires d'un modèle plus puissant vers un modèle moins cher casse l'alignement entre le modèle et son harnais, et une correction ciblée on-policy est une alternative nettement plus robuste pour réduire les coûts sans sacrifier la performance.
