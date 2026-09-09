---
title: "Etienne Dilocker (@etiennedi) on X"
date: 2026-09-09
url: "https://substack.com/redirect/564a0ee1-c333-4f8e-a231-dec7c4bd0d05?j=eyJ1IjoiM2k5cHByIn0.jwJcWcNFB3-v9tQ21KJ2x6U6-cIPdQq2LfmnXD1TmRY"
authors: ["Etienne Dilocker"]
keywords: ["revue de code", "agents IA", "pull request", "human-in-the-loop", "scope creep", "développement logiciel"]
theme: "IA"
tone: "opinion"
used_in: ["2026-09-09"]
---

## Résumé
Dans ce post sur X, Etienne Dilocker partage son point de vue sur la revue de code assistée par agents IA : confier cette tâche entièrement à des agents sans supervision humaine mène soit à un dérapage du périmètre (scope creep), soit à la mise en production de bugs critiques. Il propose un workflow hybride où les agents effectuent la majorité du travail (revue, implémentation des retours) tandis que les humains n'interviennent que pour les décisions critiques de périmètre et les critères de sortie de boucle.

## Points clés
- Laisser la revue de code entièrement aux agents entraîne soit du scope creep, soit des problèmes critiques en production.
- Les agents ont du mal à trouver le bon équilibre seuls, mais une revue humaine intégrale n'est pas réaliste.
- Workflow proposé : un agent (adversarial) fait la revue, un humain tranche sur le périmètre, un agent implémente les retours, puis on répète ou on sort de la boucle.
- La sortie de la boucle reste une décision humaine.
- Environ 90 % du travail est délégué aux agents, avec des humains en supervision uniquement sur les décisions critiques.

## Analyse approfondie
Mon avis : si vous laissez complètement de côté la revue de code humaine pour la confier entièrement à des agents, chaque pull request souffrira soit d'un dérapage du périmètre (scope creep), soit finira par livrer des problèmes critiques. Il est très difficile pour des agents de trouver le bon équilibre. Mais, évidemment, on ne peut pas non plus tout relire à la main. Ma méthode préférée actuellement est donc :
1. un agent (adversarial) effectue une revue
2. un humain prend la décision sur le périmètre (scope)
3. un agent implémente les retours
4. on répète, ou on sort de la boucle (une décision qui revient probablement à l'humain)
En somme, 90 % du travail est laissé aux agents, avec des humains dans la boucle pour les décisions critiques de périmètre et les critères de sortie.

## Pourquoi ça compte
Ce post illustre une réflexion concrète et actuelle sur la place de l'humain dans des workflows de développement de plus en plus automatisés par des agents IA, un sujet central pour toute veille sur l'évolution des pratiques de code review.
