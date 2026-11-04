---
title: "How to stop rewriting your agent’s code · Oct 28 replay"
date: 2026-11-04
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fgetunblocked.com%2Fevents%2Fhow-to-stop-rewriting-your-agent-s-code-oct-28%2F%3Futm_source=tldrdev%26utm_medium=email%26utm_campaign=primary_20261023/1/010001a1a1565131-99f227e0-edaf-4364-84ac-c8357cefdb86-000000/qEGjTlKwgyn4bflKtrVQalJ73sVjrtpytFmxnCFK4NY=452"
keywords: ["contexte", "agents IA", "ingénierie logicielle", "MCP", "revue de code", "automatisation"]
theme: "IA"
used_in: ["2026-11-04"]
---

## Résumé

Ce texte promotionnel annonce un webinaire (« replay » du 28 octobre) organisé par getunblocked.com sur le thème du « context engineering » pour les agents de codage IA. La thèse centrale est que les développeurs agissent aujourd'hui eux-mêmes comme le moteur de contexte de leur agent — en rédigeant des règles, en maintenant des skills, en copiant-collant des informations — ce qui ne tient pas à l'échelle et produit du code qui compile mais ne correspond pas au système réel. L'alternative proposée est un « context engine » qui curate automatiquement le contexte (code, PRs, docs, conversations), résout les conflits entre sources et respecte les permissions. Le document liste le contenu de la session, ce que les participants en retireront, et le public ciblé.

## Points clés

- Le contexte géré manuellement par les développeurs devient rapidement obsolète et ne scale pas en équipe.
- Plus de MCPs, de règles ou de fenêtres de contexte plus grandes donnent accès à l'information, pas une meilleure compréhension.
- Un « context engine » automatique peut résoudre les conflits quand les sources se contredisent et appliquer les permissions.
- Le webinaire propose une démo live comparant une même tâche de code avec contexte fourni manuellement vs. contexte automatique.
- Deux outils open source sont mentionnés : un agent de règles de dépôt (Repo Rules Agent) et un constructeur de graphe social d'ingénierie (Engineering Social Graph Builder).
- Le public visé inclut les responsables techniques pilotant l'adoption de l'IA et les développeurs travaillant avec des agents IA.

## Analyse approfondie

# Comment arrêter de réécrire le code de votre agent

Actuellement, c'est vous qui êtes le moteur de contexte de votre agent, il utilise votre cerveau.

Vous rédigez les fichiers de règles, maintenez les skills, et collez le fil de discussion Slack que l'agent a manqué. Mais le contexte curaté à la main devient obsolète. Quand les sources se contredisent, votre agent ne peut pas savoir laquelle est correcte. Et rien de tout cela ne scale à l'échelle d'une équipe. Vous obtenez finalement du code qui compile mais ne correspond pas à votre système, avec en prime une facture de tokens plus élevée et des revues de code plus longues. Et à mesure que les équipes se tournent vers des agents autonomes et en arrière-plan, l'écart de contexte ne fait que s'aggraver en erreurs coûteuses.

Les équipes qui prennent de l'avance utilisent un moteur de contexte qui curate le contexte automatiquement : il synthétise le code, les PRs, la documentation et les conversations, résout les conflits, applique les permissions, et fournit aux agents exactement ce dont ils ont besoin pour la tâche en cours.

Ce que nous couvrirons :

- Les 8 niveaux de maturité IA et où les équipes restent bloquées
- Pourquoi plus de MCPs, de règles, et des fenêtres de contexte plus grandes donnent accès à l'information, pas de la compréhension
- Comment un moteur de contexte curate le contexte automatiquement et résout les conflits quand les sources divergent
- Démo en direct : la même tâche de codage avec contexte fourni à la main vs. contexte automatique
- Cas d'usage au-delà de la génération de code : revue de code, triage de bugs, questions-réponses d'ingénierie, et un agent qui transforme une discussion Slack en une PR riche en contexte

Ce que vous en retirerez :

- Un modèle mental pour passer d'un contexte curaté à la main à un contexte qui reste à jour de lui-même
- Des moyens concrets de réduire les coûts en tokens et les cycles de revue
- Des exemples réels d'agents conscients du contexte à travers le flux de travail de développement
- 2 outils open source à essayer dès aujourd'hui si vous voulez construire votre propre couche de contexte : Repo Rules Agent (qui ne fait apparaître que les règles pertinentes pour la tâche) et Engineering Social Graph Builder (qui cartographie qui possède quel code à partir de l'historique des PRs)

Qui devrait y assister :

- Les responsables d'ingénierie qui pilotent l'adoption de l'IA à grande échelle
- Les développeurs travaillant avec des agents IA dans leur flux de travail de développement

## Pourquoi ça compte

Ce document illustre une tendance émergente dans l'outillage pour agents de codage : le passage d'un contexte géré manuellement à des « context engines » automatisés, un enjeu central pour toute organisation qui déploie des agents IA autonomes à l'échelle d'une équipe d'ingénierie.
