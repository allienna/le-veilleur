---
title: "GitHub - docker/docker-agent: AI Agent Builder and Runtime by Docker Engineering"
date: 2026-10-09
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fgithub.com%2Fdocker%2Fdocker-agent%3Futm_source=tldrdev/1/010001a11b39b529-c9e6d336-98d3-43b3-bfcc-b86c1bbe2532-000000/jExqHVJehjAVhwl4rRtlzxDU3pOYW0fOgtLMin3GqeI=452"
authors: ["Docker Engineering"]
keywords: ["agents IA", "Docker", "multi-agent", "YAML", "MCP", "RAG"]
theme: "Tech"
tone: "tutorial"
used_in: ["2026-10-09"]
---

## Résumé
docker-agent est un plugin CLI de Docker qui permet de créer, exécuter et partager des agents IA définis de manière déclarative en YAML. Il prend en charge l'orchestration multi-agents, un écosystème d'outils riche (y compris via MCP), la recherche augmentée (RAG) et fonctionne avec de nombreux fournisseurs de modèles (OpenAI, Anthropic, Gemini, Bedrock, Mistral, xAI, ou des modèles locaux via Docker Model Runner). Les agents peuvent être packagés et distribués comme n'importe quelle image via un registre OCI.

## Points clés
- Configuration déclarative des agents en YAML, versionnable et partageable
- Architecture multi-agents permettant à des agents spécialisés de se déléguer des tâches
- Compatible avec de multiples fournisseurs de modèles (cloud ou local)
- Outils intégrés avancés : raisonnement (think), gestion de tâches (todo), mémoire
- RAG modulable avec BM25, embeddings, recherche hybride et reranking
- Distribution des agents via n'importe quel registre OCI (push/pull comme des images Docker)

## Analyse approfondie
Construisez, exécutez et partagez des agents IA avec une configuration YAML déclarative, un écosystème d'outils riche, et une orchestration multi-agents.

`docker-agent` vous permet de créer et d'exécuter des agents IA intelligents qui collaborent pour résoudre des problèmes complexes — sans écrire de code.

`docker-agent` est un plugin CLI `docker` et peut être exécuté avec `docker agent`.

Définissez des agents en YAML, donnez-leur des outils, et laissez-les travailler.

```
agents:
  root:
    model: openai/gpt-5-mini
    description: A helpful AI assistant
    instruction: |
      You are a knowledgeable assistant that helps users with various tasks.
      Be helpful, accurate, and concise in your responses.
toolsets:
      - type: mcp
        ref: docker:duckduckgo
```
`docker agent run agent.yaml`

- **Architecture multi-agents** — Créez des équipes d'agents spécialisés qui se délèguent automatiquement des tâches
- **Écosystème d'outils riche** — Outils intégrés + n'importe quel serveur MCP (local, distant, ou basé sur Docker)
- **Agnostique au fournisseur IA** — OpenAI, Anthropic, Gemini, AWS Bedrock, Mistral, xAI, Docker Model Runner, et plus
- **Configuration YAML** — Déclarative, versionnable, partageable
- **Raisonnement avancé** — Outils intégrés think, todo et memory
- **RAG** — Récupération modulable avec BM25, embeddings, recherche hybride et reranking
- **Packager et partager** — Poussez les agents vers n'importe quel registre OCI, tirez-les et exécutez-les n'importe où

**Docker Desktop** (4.63+) — le plugin CLI docker-agent est préinstallé. Exécutez simplement `docker agent`.

**Homebrew** — `brew install docker-agent`. Exécutez `docker-agent` directement ou créez un lien symbolique du binaire vers `~/.docker/cli-plugins/docker-agent` et exécutez `docker agent`.

**Versions binaires** — Téléchargez depuis les GitHub Releases. Créez un lien symbolique du binaire `docker-agent` vers `~/.docker/cli-plugins/docker-agent` pour pouvoir utiliser `docker agent`, ou utilisez `docker-agent` directement.

Définissez au moins une clé API (ou utilisez Docker Model Runner pour des modèles locaux) :

`export OPENAI_API_KEY=sk-...        # ou ANTHROPIC_API_KEY, GOOGLE_API_KEY, etc.`

Consultez Set Up a Model pour le guide complet des deux approches (clé API cloud ou modèle local).

```
# Exécuter l'agent par défaut
docker agent run
# Exécuter depuis un registre OCI
docker agent run myorg/agent:tag
# Générer un nouvel agent de manière interactive
docker agent new
# Exécuter votre propre configuration
docker agent run agent.yaml
```

Plus d'exemples dans le répertoire `examples/`.

- Installation · Set Up a Model · Quick Start
- Agents · Models · Tools · Multi-Agent
- Configuration Reference
- TUI · CLI · MCP Mode · RAG
- Model Providers · Docker Model Runner

Lisez le guide de contribution pour commencer. Nous utilisons `docker-agent` pour construire `docker-agent` :

`docker agent run ./golang_developer.yaml`

Nous collectons des données d'usage anonymes pour améliorer l'outil. Voir Telemetry.

## Pourquoi ça compte
Docker entre sur le terrain des frameworks d'agents IA en misant sur une approche déclarative (YAML) et son écosystème de conteneurisation/OCI existant, ce qui pourrait simplifier le déploiement et le partage d'agents multi-fournisseurs pour les équipes déjà outillées avec Docker.
