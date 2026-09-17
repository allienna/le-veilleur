---
title: "Ory Agent Security, the Control Plane for AI Coding Agents | Ory"
date: 2026-09-17
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.ory.com%2Fory-agent-security%3Futm_source=tldr%26utm_medium=ai-newsletter%26utm_campaign=494745831-ADV-2026-Q3-TLDR%2BPLACEMENT-2026-09-16%26utm_content=header_ai_agents_outnumber%26utm_term=2026-09-16_tldr_ai%26sp=SpYF3cX1aS5aVQcAcK7bCfMs/1/010001a0aa675bd7-23c4508e-579e-4af2-bee9-78187ad33044-000000/ehLQUq02fBTUrV7RFuK2aQWF5bFP5rL_hGv584247XI=452"
keywords: ["sécurité des agents IA", "contrôle d'accès", "authentification", "MCP", "audit", "gestion des identités"]
theme: "Sécurité"
used_in: ["2026-09-17"]
---

## Résumé
Ory lance « Ory Agent Security », un control plane destiné à sécuriser les agents IA de codage (Claude Agent SDK, Gemini CLI, OpenAI Codex, Microsoft Agent Framework). Le produit repose sur trois piliers : authentification individuelle de chaque agent/sous-agent, autorisation fine des actions (commandes shell, écritures de fichiers, outils MCP, appels API), et traçabilité complète exportée en OpenTelemetry vers un SIEM. Il s'inscrit dans l'offre plus large « Ory DX », qui combine MCP, plugins, CLI et Ory Elements pour un workflow de développement piloté par des agents conversationnels.

## Points clés
- Chaque agent et sous-agent s'authentifie avec ses propres identifiants avant d'agir ; la chaîne de délégation vers l'utilisateur ou l'agent parent est enregistrée avant l'exécution de tout outil.
- Autorisation fine appliquée aux commandes shell, écritures de fichiers, outils MCP et appels API, selon le même modèle de politique que celui régissant les accès humains.
- Chaque action est enregistrée et exportée via OpenTelemetry vers un SIEM ; la chaîne de délégation subsiste même après l'expiration des tokens.
- Compatibilité annoncée avec les principaux frameworks d'agents : Anthropic Claude Agent SDK, Gemini CLI, OpenAI Codex, Microsoft Agent Framework.
- Le produit s'intègre dans l'écosystème « Ory DX », qui unifie MCP servers, plugins, CLI et Ory Elements.

## Analyse approfondie
### Fonctionne avec vos harnais d'agents et SDK préférés

- **Authentifié** — Chaque agent et sous-agent s'authentifie avec ses propres identifiants avant d'agir. La chaîne de délégation vers l'utilisateur ou l'agent en amont est enregistrée avant l'exécution de tout outil.
- **Autorisé** — Ory applique une autorisation fine aux commandes shell, aux écritures de fichiers, aux outils MCP et aux appels API — le même modèle de politique que celui qui régit les accès humains.
- **Responsabilisé (Accountable)** — Chaque action est enregistrée et exportée via OpenTelemetry vers votre SIEM. La chaîne de délégation survit au token, de sorte que la trace demeure même après l'expiration des identifiants.

### Comment fonctionne la sécurité des agents chez Ory

### Démarrez avec l'outil IA de votre choix

- **Anthropic Claude Agent SDK** — Le Claude Agent SDK d'Anthropic est un framework de développement conçu par Anthropic qui permet la création et le déploiement programmatiques d'agents IA autonomes capables de raisonnement multi-tours, d'exécution de code et d'interaction avec des systèmes de fichiers et des outils externes.
- **Gemini CLI** — Gemini CLI est un agent IA open source développé par Google qui apporte la puissance des modèles Gemini directement dans votre terminal, permettant aux développeurs de comprendre du code, d'automatiser des workflows complexes et d'exécuter des tâches à l'aide de prompts en langage naturel.
- **OpenAI Codex** — OpenAI Codex est un agent de codage propulsé par l'IA conçu pour automatiser les tâches de développement logiciel en naviguant dans les bases de code, en générant des fonctionnalités, en déboguant des problèmes et en exécutant des tests directement dans un environnement terminal ou cloud isolé.
- **Microsoft Agent Framework** — Microsoft Agent Framework est un SDK et runtime open source de Microsoft pour construire, orchestrer et déployer des agents IA et des workflows multi-agents de niveau entreprise en Python et en .NET.

### Questions fréquentes

### En savoir plus sur la sécurité des agents

### *Ory DX* : Développez des applications sécurisées à la vitesse de la pensée, de la bonne manière.

Ory DX est la boîte à outils ultime pour les développeurs, qui unifie l'automatisation par l'IA avec l'écosystème de sécurité durci d'Ory. En combinant harmonieusement les serveurs Model Context Protocol (MCP), les plugins, la CLI et Ory Elements, elle offre aux développeurs un workflow conversationnel piloté par des agents pour développer une gestion des identités, des accès et des permissions fines de niveau entreprise.

## Pourquoi ça compte
À mesure que les agents de codage IA obtiennent un accès direct aux shells, fichiers et API, la question du contrôle d'accès et de l'audit de leurs actions devient centrale pour la sécurité en entreprise ; cette annonce illustre l'émergence d'une nouvelle catégorie de produits — l'IAM appliqué aux agents IA plutôt qu'aux seuls humains.
