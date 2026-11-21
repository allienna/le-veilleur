---
title: "GitHub - replit/datacat: Self-hosted observability: metrics, logs, traces, dashboards and alerts. Stores data in PostgreSQL or ClickHouse. Accepts OpenTelemetry data."
date: 2026-11-21
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fgithub.com%2Freplit%2Fdatacat%3Futm_source=tldrdev/1/010001a1f8e20cf0-04c1a8d2-b096-40a7-9fd6-0fd535581342-000000/MZ2FELnrCM1ggNYPaijwct19YQAmCEgHSObJkS7cZk0=452"
authors: ["Replit"]
keywords: ["observabilité", "self-hosted", "OpenTelemetry", "PostgreSQL", "ClickHouse", "monitoring"]
theme: "Data"
tone: "tutorial"
used_in: ["2026-11-21"]
---

## Résumé
DataCat est un projet open source de Replit proposant une plateforme d'observabilité auto-hébergée regroupant métriques, logs, traces distribuées, tableaux de bord et alertes en un seul outil. Il tourne entièrement sur l'infrastructure de l'utilisateur, stocke les données dans PostgreSQL (ou ClickHouse pour la télémétrie) et accepte le trafic OpenTelemetry ainsi que le format d'agent compatible Datadog, sans nécessiter de compte hébergé ni de service externe. Le dépôt fournit des instructions de déploiement via Docker Compose, des outils de build/test complets, et une suite de benchmarks de correction et de performance. Le projet est distribué sous licence Apache 2.0 et précise qu'il n'est ni affilié ni approuvé par Datadog, Inc.

## Points clés
- Plateforme tout-en-un : métriques, logs, traces distribuées, cartographie d'infrastructure et alertes, avec corrélation entre logs et traces.
- Compatible avec les protocoles OpenTelemetry (OTLP/HTTP) et avec l'API d'intake publique Datadog, ce qui permet de réutiliser des agents Datadog existants.
- Déploiement simple via Docker Compose (Docker Engine, Git, OpenSSL requis) avec configuration des secrets via `.env`.
- Développement basé sur Node.js 22.15+, pnpm 10.11.0, PostgreSQL 14+, et un agent écrit en Go 1.26.11+.
- Pipeline de CI complet (typecheck, tests unitaires, audits de dépendances/vulnérabilités, tests end-to-end sur les deux backends de stockage, scan de secrets) et suite de benchmarks dédiée (`bench/kit`) vérifiant débit, latence de requête et délai d'indexation.
- Licence Apache 2.0 ; projet indépendant explicitement non affilié à Datadog.

## Analyse approfondie
Observabilité auto-hébergée : métriques, logs, traces, tableaux de bord et alertes en un seul endroit. DataCat fonctionne sur votre propre infrastructure, stocke les données dans PostgreSQL (ou la télémétrie dans ClickHouse, si vous le souhaitez ; voir docs/SELF_HOSTING.md), et accepte le trafic OpenTelemetry ainsi que le trafic d'agent compatible Datadog. Aucun compte hébergé ni service externe n'est requis.

- Explorateur de métriques, formules, tableaux de bord et cartes d'hôtes
- Logs consultables avec facettes, suivi en direct (live tail) et corrélation avec les traces
- Catalogue de services APM, explorateur de traces et vue en cascade (waterfall)
- Moniteurs de métriques, logs et traces avec notifications webhook/Slack
- Organisations, comptes locaux, invitations à usage unique, clés API/application
- Agent hôte basé sur le OpenTelemetry Collector et bibliothèques d'instrumentation Node.js/Python
- Un seul processus de production servant l'API, l'interface web, l'installeur et les téléchargements

Prérequis : Docker Engine avec le plugin Compose, Git, et OpenSSL.

```
git clone https://github.com/replit/datacat
cd datacat
cp .env.example .env
sed -i "s/^POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=$(openssl rand -hex 24)/" .env
sed -i "s/^SESSION_SECRET=.*/SESSION_SECRET=$(openssl rand -hex 32)/" .env
chmod 600 .env
mkdir -p downloads
docker compose up -d --build
```
Ouvrez **http://localhost:3000**, créez votre compte administrateur et votre organisation, puis créez une clé API dans **Organization Settings**. La configuration demande un jeton de setup, affiché dans le journal du serveur (`docker compose logs datacat | grep "setup token"`) sauf si vous définissez `DATACAT_SETUP_TOKEN`. Définissez `PUBLIC_URL` sur votre origine HTTPS accessible depuis l'extérieur avant d'inviter des collègues ou d'installer des agents à distance.

Les binaires d'agent et les packages SDK sont des ressources de release séparées. Placez-les (y compris `SHA256SUMS`) dans `downloads/` pour les servir depuis votre instance.

DataCat accepte l'API d'intake publique Datadog ainsi que OTLP/HTTP :

| Émetteur | Statut |
|---|---|
| Datadog Agent 7.56.2 (métriques, logs, check runs, traces) | Testé via des exécutions de type CI |
| Datadog Agent 7.85.4 (métriques, logs, check runs, traces) | Testé avec des payloads capturés ; y compris le nouveau format de trace à table de chaînes (string-table) |
| Datadog Agent 7.57–7.84 | Non testé individuellement. Les agents qui envoient des traces dans un format que DataCat ne peut pas lire reçoivent un 422, jamais un 202 silencieux |
| OpenTelemetry Collector / SDKs (OTLP/HTTP) | `/v1/traces`, `/v1/metrics`, `/v1/logs` (aussi disponibles sous `/otlp/v1/*`) |
| Agent et bibliothèques DataCat | Testé en CI |

`GET /api/v1/intake/stats` indique, pour chaque chemin d'intake, combien d'éléments ont été stockés et combien ont été rejetés depuis le démarrage du serveur.

La connexion utilise des comptes locaux email/mot de passe ; les membres rejoignent via des liens d'invitation à usage unique.

Utilisez Node.js **22.15+**, pnpm **10.11.0** et PostgreSQL **14+**. Node 22 satisfait également l'exigence du SDK Node ; les anciennes versions Node 20 ne sont pas prises en charge par le SDK actuel.

```
corepack enable
corepack prepare pnpm@10.11.0 --activate
pnpm install --frozen-lockfile
BASE_PATH=/ pnpm run build:selfhost
# Définissez DATABASE_URL, SESSION_SECRET et PUBLIC_URL dans votre environnement.
NODE_ENV=production PORT=3000 pnpm start
```
Le serveur migre automatiquement son schéma avant de démarrer l'écoute. Il n'y a pas de push de schéma manuel ni de serveur frontend séparé.

Voir **Self-hosting** pour une installation propre sur Ubuntu, tous les paramètres d'environnement, les sauvegardes, systemd, l'installation des agents, l'instrumentation Node/Python et un tutoriel de moniteur webhook.

```
pnpm run typecheck:libs
pnpm --filter @workspace/api-server run dev
# Dans un autre terminal :
API_PROXY=http://localhost:3000 PORT=5173 pnpm --filter @workspace/web run dev
```
L'API nécessite `DATABASE_URL` ; utilisez une base de données de développement séparée.
L'agent est construit avec Go 1.26.11+ :

```
bash agent/build.sh
DESTDIR="$PWD/dist/downloads" bash agent/release.sh
```
Tests :

```
pnpm --filter @workspace/api-server test     # tests unitaires du serveur
DATACAT_URL=http://localhost:3000 DATACAT_SETUP_TOKEN=<token> bash scripts/e2e.sh   # vérifications de bout en bout à réponse connue sur une installation fraîche
```
La CI (`.github/workflows/ci.yml`) exécute les vérifications de types, les tests unitaires, les audits de dépendances et de vulnérabilités, les vérifications de bout en bout sur les deux options de stockage, les tests de bibliothèque et d'agent, un build Docker et un scan de secrets à chaque pull request.

Des exemples exécutables se trouvent dans `examples/`. Voir Contributing, Security et le Changelog.

`bench/kit` envoie des métriques, logs et traces à travers DataCat et vérifie chaque réponse par rapport à une valeur connue ; il rapporte le débit, la latence de requête et le délai avant que les données deviennent consultables, pour les deux options de stockage. Les autres dossiers de `bench/` contiennent les tests de correction, de résilience, d'alerting, de charge soutenue (soak) et d'isolation ; les résultats bruts derrière les chiffres publiés se trouvent dans `bench/evidence/`.

Licence Apache 2.0. Les dépendances tierces conservent leurs propres licences. DataCat est un projet indépendant, non affilié à et non approuvé par Datadog, Inc. Datadog est une marque déposée de Datadog, Inc. ; elle n'est mentionnée ici que pour décrire la compatibilité de protocole.

## Pourquoi ça compte
DataCat illustre la montée en puissance des alternatives open source et auto-hébergées aux plateformes d'observabilité SaaS comme Datadog, en misant sur la compatibilité de protocole (OTLP, API Datadog) pour faciliter la migration ; un signal intéressant pour les équipes cherchant à reprendre le contrôle de leurs coûts et de leurs données de télémétrie.
