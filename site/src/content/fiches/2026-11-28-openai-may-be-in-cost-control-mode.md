---
title: "OpenAI may be in cost control mode"
date: 2026-11-28
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fmicjm.com%2Fblog%2Fopenai-is-in-cost-control-mode%2F%3Futm_source=tldrnewsletter/1/010001a21cc738c3-8384d07b-f7fa-405d-aaed-8a28a016127f-000000/Am9-rZBz6vkAqh0mjzh8Zc_kLPNXw49z14-kjphNG1A=452"
keywords: ["OpenAI", "GPT-6", "coûts d'inférence", "raisonnement", "tokens", "benchmark"]
theme: "IA"
tone: "research"
used_in: ["2026-11-28"]
---

## Résumé
Les nouveaux modèles d'OpenAI, Astra 6.2 et Sol 6.2, ont été largement critiqués à leur sortie. Une analyse de données issues d'un système de confrontation entre modèles montre que leur nombre de tokens de sortie et de tokens de raisonnement par tâche a nettement chuté par rapport à leurs prédécesseurs. Ces baisses sont statistiquement significatives, ce qui suggère un ajustement délibéré en faveur de la réduction des coûts d'inférence plutôt que de la qualité du raisonnement. Les auteurs qualifient ces deux modèles de valeurs aberrantes en matière de sous-raisonnement comparé au reste de l'écosystème.

## Points clés
- Astra 6.2 et Sol 6.2 ont été critiqués par les utilisateurs dès leur sortie.
- Les tokens de sortie et de raisonnement par tâche ont nettement chuté par rapport aux versions précédentes (Astra 6, Sol 6.1).
- Les baisses sont statistiquement significatives : p = 0,0055 (sortie, Sol), 0,022 (sortie, Astra), 0,00013 (raisonnement, Sol), 0,0064 (raisonnement, Astra).
- Comparés à leurs concurrents dans un système de confrontation basé sur le score Elo, Astra 6.2 et Sol 6.2 apparaissent comme des valeurs aberrantes en matière de sous-raisonnement.
- L'hypothèse avancée est qu'OpenAI a délibérément optimisé ces modèles pour réduire les coûts d'inférence, au détriment de la qualité perçue.

## Analyse approfondie
La récente sortie par OpenAI d'Astra 6.2 et de Sol 6.2 a été largement critiquée. Que s'est-il passé ?

D'après nos données, il semble que ces modèles aient été ajustés pour réduire les coûts. Plus précisément, le nombre de tokens de sortie par tâche et le nombre de tokens de raisonnement par tâche ont diminué.

Voici un graphique de l'évolution globale du coût entre GPT-6 et GPT 6.2 :

L'axe des X du graphique ci-dessus représente le ratio de dépense du modèle GPT par rapport à ses concurrents dans notre système de confrontation (« battle system ») pour des tâches réelles. L'axe des Y du graphique ci-dessus correspond au score Elo de notre classement (leaderboard).

Les évolutions observées sur le graphique sont significatives ; voici le même graphique avec les intervalles de confiance :

### Ce qui a changé

Par rapport à leurs concurrents, Astra et Sol semblent raisonner beaucoup moins. Voici un graphique montrant combien les modèles raisonnent par rapport à leurs concurrents dans la même confrontation. Au-dessus de la ligne signifie plus de raisonnement, et au-dessous signifie moins.

On peut voir qu'Astra 6 et Sol 6.1 étaient tous deux des modèles plutôt normaux, mais qu'Astra 6.2 et Sol 6.2 deviennent des valeurs aberrantes (outliers).

On observe le même effet sur les tokens de sortie :

Ces changements sont-ils significatifs ? La valeur p sur la baisse des tokens de sortie est de 0,0055 pour Sol et de 0,022 pour Astra. La valeur p sur la baisse du raisonnement est de 0,00013 pour Sol et de 0,0064 pour Astra.

En conclusion, Astra et Sol semblent avoir été ajustés sur le plan des coûts par rapport à leurs prédécesseurs, et à un degré qui en fait des valeurs aberrantes en matière de sous-raisonnement (« underthinking »).

## Pourquoi ça compte
Ce signal illustre une tension croissante entre coûts d'inférence et qualité perçue chez les laboratoires d'IA, un facteur déterminant à surveiller pour quiconque évalue ou dépend des modèles frontière d'OpenAI.
