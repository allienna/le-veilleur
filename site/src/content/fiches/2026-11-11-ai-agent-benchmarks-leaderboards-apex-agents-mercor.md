---
title: "AI Agent Benchmarks & Leaderboards: APEX-Agents | Mercor"
date: 2026-11-11
url: "https://click.dataelixir.com/o8u44z23rdiqhn3vp5givhqqpe0q9hohmlmre/48hvhehm3o33e6bxh7/aHR0cHM6Ly93d3cubWVyY29yLmNvbS9hcGV4L2FwZXgtYWdlbnRzLWxlYWRlcmJvYXJkLz91dG1fY2FtcGFpZ249RGF0YV9FbGl4aXImdXRtX3NvdXJjZT1EYXRhX0VsaXhpcl81OTc="
authors: ["Mercor"]
keywords: ["benchmark agents IA", "APEX-Agents", "Mercor", "tâches professionnelles", "leaderboard LLM", "évaluation long horizon"]
theme: "IA"
tone: "research"
used_in: ["2026-11-11"]
---

## Résumé
APEX-Agents, développé par Mercor en collaboration avec Box et Harvey, est un benchmark qui évalue la capacité des agents IA de pointe à exécuter des tâches longues et multi-applications dans trois métiers des services professionnels : la banque d'investissement, le conseil en management et le droit des affaires. Construit avec des professionnels de cabinets comme Latham & Watkins, McKinsey ou Goldman Sachs, il comprend 31 « mondes » et 240 tâches notées à l'aide de grilles expertes combinées à un LM judge. Le dataset et l'infrastructure d'évaluation (Archipelago) sont open source, tandis que l'ensemble complet des tâches reste privé pour éviter tout entraînement des modèles sur le benchmark lui-même. Le leaderboard actuel affiche des scores allant d'environ 73 % à plus de 91 % selon le domaine testé, avec des modèles comme Gemini 4 Argon, Fable 5.2 et GPT-6 Astra parmi les mieux classés.

## Points clés
- APEX-Agents mesure les performances d'agents IA sur des tâches réalistes de long horizon dans trois métiers : analyste en banque d'investissement, consultant en management, avocat d'entreprise.
- Le benchmark repose sur 31 « mondes » riches en données et 240 tâches, conçus par des professionnels de cabinets comme Latham & Watkins, Skadden, Cravath, McKinsey, BCG, Goldman Sachs ou JPMorgan.
- Deux métriques principales : le Mean Score (pourcentage moyen de critères validés) et le Pass@1 (pourcentage de tâches réussies dès la première tentative).
- Le dataset et l'outil d'exécution/évaluation Archipelago sont open source, mais le jeu de tâches complet reste privé pour éviter la contamination des données d'entraînement.
- Le classement évolue à chaque sortie de modèle frontier, et s'inscrit dans une famille plus large de benchmarks Mercor (APEX-SWE, APEX-Accounting, APEX-1).
- Les meilleurs scores actuels dépassent 91 % sur le volet conseil, autour de 87 % sur le volet banque, et environ 77 % sur le volet droit des affaires.

## Analyse approfondie
L'AI Productivity Index pour les agents (APEX-Agents) mesure si les agents IA de pointe (frontier) peuvent exécuter des tâches de long horizon, cross-application, dans trois métiers des services professionnels.

Nous avons créé APEX-Agents pour évaluer les agents sur le travail quotidien réel de professionnels : analystes en banque d'investissement, consultants en management, et avocats d'entreprise. Les tâches exigent des agents qu'ils raisonnent, démontrent des connaissances avancées, utilisent plusieurs applications, et planifient sur de longs horizons.

APEX-Agents a été construit en trois étapes. D'abord, des professionnels du secteur ont créé un monde riche en données, basé sur un scénario de projet unique. Ensuite, ils ont créé des tâches réalistes et exigeantes à partir des fichiers de ce monde. Enfin, nous avons donné aux agents accès à ces tâches pour qu'ils puissent les exécuter (avec tous les logiciels qu'un humain utiliserait).

APEX-Agents comprend 31 « mondes », soit 240 tâches et grilles de notation (rubrics). L'ensemble du dataset APEX-Agents est disponible en open source, ainsi qu'Archipelago, notre service d'infrastructure pour exécuter et évaluer les trajectoires des agents.

Experts de Latham & Watkins, Skadden, Cravath

Voir plus

**Classement (extraits) :**

Gemini 4 Argon — 76,7 %

Gemini 4 Carbon — 73,8 %

GPT-6 Astra — 73,4 %

Experts de McKinsey, BCG, Deloitte, Accenture, EY — 91,9 %

Fable 5.2 — 91,2 %

(modèle non précisé) — 88,4 %

Experts de Goldman Sachs, Morgan Stanley, JPMorgan, Barclays — 86,9 %

(modèle non précisé) — 81,9 %

(modèle non précisé) — 80,9 %

Le Mercor AI Productivity Index (APEX) est une famille de benchmarks qui mesure l'efficacité avec laquelle les modèles et agents IA réalisent des tâches à valeur économique. APEX-Agents évalue des workflows multi-étapes de long horizon dans des secteurs à forte valeur, comme le droit des affaires, la banque d'investissement et le conseil en management. Il a été développé en collaboration avec Box et Harvey.

Les classements peuvent évoluer à chaque sortie d'un modèle de pointe. Les nouveaux modèles sont évalués sur APEX-Agents, APEX-SWE, APEX-Accounting et APEX-1 dès leur sortie.

Des professionnels en exercice issus de cabinets de référence que les tâches simulent, notamment des avocats de Latham & Watkins, Skadden et Cravath ; des consultants de McKinsey et BCG ; et des banquiers de Goldman Sachs, Morgan Stanley et JPMorgan.

APEX-Agents évalue la qualité du travail accompli. Les résultats des modèles sont notés à l'aide de grilles rédigées par des experts, avec un LM judge (modèle de langage faisant office de juge).

Le Mean Score mesure le pourcentage moyen de critères validés sur l'ensemble des tâches du benchmark. C'est la métrique principale utilisée pour classer le leaderboard APEX-Agents. Le Pass@1 mesure le pourcentage de tâches qu'un agent réussit dès sa première tentative (c'est-à-dire qu'il obtient 100 % sur la grille). Ensemble, ces deux métriques captent à la fois la capacité globale des modèles et leur fiabilité de bout en bout.

Oui, sur le sous-ensemble ouvert (open subset). Le harnais d'évaluation est publié sur GitHub et des exemples de tâches sont disponibles sur HuggingFace, ce qui permet d'exécuter le même pipeline de notation sur votre propre modèle. L'ensemble complet des tâches reste privé afin que les modèles ne puissent pas être entraînés dessus.

## Pourquoi ça compte
Ce benchmark offre un point de repère concret et sectoriel pour juger si les agents IA peuvent réellement remplacer ou assister des professionnels qualifiés sur des tâches complexes et multi-outils, un signal clé à suivre pour évaluer la maturité réelle de l'automatisation agentique au-delà des annonces marketing.
