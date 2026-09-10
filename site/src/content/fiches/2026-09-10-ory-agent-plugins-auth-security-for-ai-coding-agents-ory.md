---
title: "Ory Agent Plugins: Auth & Security for AI Coding Agents | Ory"
date: 2026-09-10
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.ory.com%2Fory-agent-plugins%3Futm_campaign=478444734-ADV-2026-Q3-TLDR%2520PLACEMENT-2026-09-09%26utm_source=tldr%26utm_medium=dev-newsletter/1/010001a085e345e0-e4ed8295-36b0-4db1-9ad1-88297af62686-000000/SbcRvYWTzd6Ku0LI8P653NZ-arqNqmmJRIt8i-6xWtY=452"
keywords: ["agents IA", "authentification", "OAuth", "MCP", "gestion des identités", "sécurité"]
theme: "Sécurité"
used_in: ["2026-09-10"]
---

## Résumé
Ory lance les « Agent Plugins », qui intègrent directement l'authentification et la sécurité d'Ory dans les principaux frameworks d'agents IA (Claude Agent SDK, Gemini CLI, OpenAI Codex, Microsoft Agent Framework, etc.). Ces plugins fournissent un serveur MCP exposant la CLI et l'API REST d'Ory, un stack local démarrable en une seule commande (Kratos, Hydra, Keto), ainsi que des « skills » prêtes à l'emploi pour la connexion, l'inscription ou le login social. L'ensemble sert de socle à « Ory Agent Security », un plan de sécurité unifié destiné à contrôler et auditer les agents IA en production.

## Points clés
- Compatible avec plusieurs harnais et SDK d'agents : Claude Agent SDK, Codex, Gemini CLI, OpenClaw, OpenCode, Microsoft Agent Framework
- Une seule commande (`local up`) démarre localement Kratos, Hydra et Keto, pré-configurés, sans compte cloud ni fichiers de config à écrire
- Un serveur MCP expose la CLI et l'API REST d'Ory comme outils utilisables par l'agent (création d'identités, clients OAuth, tuples de relation)
- Des skills natives prêtes à l'emploi (`ory-auth-setup`, `ory-login-flow`, `ory-social-login`, `ory-local-dev`) intégrées dans chaque agent supporté
- Authentification des agents via dynamic client registration (`/oauth2/register`) ou identifiants statiques, avec jeton bearer traçable dans les journaux d'audit
- Vise à poser les fondations d'« Ory Agent Security », un plan de sécurité unique pour superviser les agents IA en production

## Analyse approfondie
## Fonctionne avec vos harnais d'agents et SDK préférés

## Construire avec Ory n'a jamais été aussi simple

- **Un stack local en une commande** — Une seule commande met en ligne Kratos, Hydra et Keto localement, pré-configurés (seeded) et prêts à l'emploi. Aucun compte cloud, aucun fichier de configuration à écrire de zéro n'est nécessaire.
- **Les bonnes pratiques Ory intégrées d'office** — Construit sur Ory Elements, les SDK Ory et OAuth 2.1 avec PKCE, ce qui garantit que votre agent génère les mêmes schémas que ceux recommandés dans la documentation et les exemples Ory. Mieux encore : les plugins sont prêts à l'emploi pour Ory Agent Security.
- **Des harnais et SDK de premier plan** — Mêmes compétences et politiques sur Claude Code, Codex, Gemini CLI, OpenClaw, OpenCode, et plus encore. Un package par agent sur un client partagé vous permet de rester agnostique vis-à-vis de la plateforme et du framework, y compris pour les frameworks SDK et les agents personnalisés.
- **Serveur MCP inclus** — La CLI et l'API REST d'Ory sont exposées comme outils MCP. Votre agent crée des identités, enregistre des clients OAuth et gère des tuples de relation sans que vous ayez à copier-coller des commandes.
- **Conçu pour la flexibilité et la sécurité**

## Comment fonctionne le plugin d'agent Ory

## *Ory Agent Security* : un seul plan de sécurité pour tous vos agents IA.

Vous construisez des agents ? Vous les faites tourner en production ? Alors la faille est déjà ouverte. La bonne nouvelle, c'est que les plugins d'agent Ory fournissent l'échafaudage nécessaire à Ory Agent Security, apportant des contrôles en temps réel (in-the-loop) et une application des règles directement intégrés dans le runtime de l'agent.

## Démarrez avec l'outil IA de votre choix

- **Anthropic Claude Agent SDK** — Le Claude Agent SDK d'Anthropic est un framework de développement conçu par Anthropic qui permet la création et le déploiement programmatiques d'agents IA autonomes capables de raisonnement multi-tours, d'exécution de code, et d'interaction avec les systèmes de fichiers et outils externes.
- **Gemini CLI** — Gemini CLI est un agent IA open source développé par Google qui apporte la puissance des modèles Gemini directement dans votre terminal, permettant aux développeurs de comprendre du code, d'automatiser des workflows complexes et d'exécuter des tâches en langage naturel.
- **OpenAI Codex** — OpenAI Codex est un agent de codage propulsé par l'IA conçu pour automatiser les tâches de développement logiciel en naviguant dans les bases de code, en générant des fonctionnalités, en déboguant des problèmes et en exécutant des tests directement dans un environnement terminal ou cloud isolé.
- **Microsoft Agent Framework** — Microsoft Agent Framework est un SDK et runtime open source de Microsoft pour construire, orchestrer et déployer des agents IA de niveau entreprise et des workflows multi-agents en Python et .NET.

## Questions fréquentes

(`@ory/claude-code`), Codex (`@ory/codex`), Gemini CLI (`@ory/gemini-cli`), OpenClaw (`@ory/openclaw`), et OpenCode (`@ory/opencode`).

`local up` met en ligne un stack Ory basé sur Docker sur `localhost:4000` avec Kratos, Hydra et Keto pré-configurés. Une fois prêt, les mêmes scaffolds et skills pointent vers un projet Ory Network sans changement dans le code de votre application. Cependant, pour démarrer rapidement, il est recommandé de suivre les instructions fournies dans Ory Network.

`ory-auth-setup` (configuration complète d'Ory Network avec Ory Elements), `ory-login-flow` (connexion, inscription, récupération, vérification, paramètres), `ory-social-login` (Google, GitHub, Apple, Microsoft et autres fournisseurs OIDC), et `ory-local-dev` (piloter une instance Ory locale). Chacune est intégrée dans le mécanisme natif de skills de chaque agent de codage pris en charge.

Point de terminaison `/oauth2/register`. Les identifiants émis persistent localement et sont réutilisés lors des sessions ultérieures. Des identifiants statiques (`ORY_AGENT_API_KEY` ou `ORY_AGENT_CLIENT_ID + SECRET`) peuvent se substituer au DCR (dynamic client registration) lorsque nécessaire — utile en CI. Chaque appel sortant vers l'API Ory porte le jeton bearer de l'agent, de sorte que le journal d'audit montre quel agent a agi, et pour le compte de qui.

## *Ory DX* : construisez des applications sécurisées à la vitesse de la pensée, de la bonne manière.

Ory DX est la boîte à outils de développement ultime qui unifie l'automatisation par IA avec l'écosystème de sécurité renforcé d'Ory. En fusionnant de manière transparente les serveurs Model Context Protocol (MCP), les plugins, la CLI et Ory Elements, elle offre aux développeurs un workflow conversationnel piloté par agent pour développer une gestion d'identité, d'accès et de permissions granulaires prête pour l'entreprise.

## Pourquoi ça compte
Ce lancement illustre une tendance de fond : les fournisseurs d'identité traditionnels (ici Ory, avec Kratos/Hydra/Keto) s'intègrent désormais nativement dans les harnais d'agents de codage (Claude Code, Codex, Gemini CLI) via MCP, signe que l'authentification et l'autorisation deviennent un brique standard de l'outillage agentique plutôt qu'une réflexion après coup.
