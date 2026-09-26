---
title: "Managed Deep Agents delivers a better user experience for agents in production"
date: 2026-09-26
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.langchain.com%2Fblog%2Flangsmith-managed-deep-agents-whats-new%3Futm_source=tldrai/1/010001a0d8c27fe0-6c9b409a-b363-4068-b435-524fdf752c58-000000/2njH5RnIyBQhWDmOTN9ZLrrgqiv6NN_J624sBuK2tEg=452"
keywords: ["agents IA", "LangChain", "mémoire utilisateur", "authentification", "Slack", "recherche web"]
theme: "IA"
tone: "news"
used_in: ["2026-09-26"]
---

## Résumé
LangChain annonce la version 0.8 de Managed Deep Agents (MDA), sa plateforme managée pour déployer des agents IA en production. Cette mise à jour ajoute une mémoire scopée à l'utilisateur, des identifiants (credentials) possédés par l'utilisateur, des canaux HTTP génériques en plus de Slack (avec transfert de fichiers), ainsi qu'un outil de recherche web intégré propulsé par Parallel. L'objectif affiché est de décharger les équipes d'ingénierie de l'infrastructure répétitive (mémoire, auth, canaux, gestion des outils) pour qu'elles se concentrent sur le comportement de l'agent. Deux témoignages clients (Kyth.ai, Consensus) illustrent des cas d'usage réels en production.

## Points clés
- Mémoire à deux niveaux : une couche « agent » partagée par tous les utilisateurs et une couche « utilisateur » scopée à l'identité authentifiée de l'appelant, sans copie de contenu entre les deux.
- Connexions (« connections ») permettant de lier un agent à des services externes (GitHub, Notion, Salesforce, etc.) avec des identifiants soit au niveau agent, soit au niveau utilisateur ; plus de 23 services pris en charge nativement.
- Nouveaux canaux HTTP génériques (webhooks JSON) en complément de Slack, qui gagne le transfert de fichiers (logs, contrats, captures d'écran...).
- Recherche web intégrée « clé en main » via Parallel, sans compte fournisseur ni clé API à gérer séparément, avec traçabilité dans LangSmith.
- Architecture en projet « code-first » structurée par répertoires (agent, mémoire, identité, outils, canaux, middleware, schedules, connecteurs, skills, sandbox, evals).
- Recherche web Parallel offerte gratuitement pendant la période bêta de MDA.

## Analyse approfondie
### Points clés à retenir

- **Authentification et mémoire scopées à l'identité :** des identifiants possédés par l'utilisateur et une mémoire au niveau utilisateur permettent aux agents d'agir avec les bonnes permissions et de se souvenir du contexte propre à chaque appelant.
- **Canaux HTTP :** utilisez les agents dans des outils internes, des portails clients, des systèmes de support, et d'autres surfaces produit capables d'envoyer des webhooks.
- **Recherche web intégrée :** Managed Deep Agents inclut désormais nativement la recherche web propulsée par Parallel.

Aujourd'hui, nous lançons Managed Deep Agents 0.8, qui ajoute la prise en charge des identifiants possédés par l'utilisateur, de la mémoire au niveau utilisateur, des canaux HTTP, du transfert de fichiers dans Slack, et intègre un outil prêt à l'emploi pour la recherche web propulsée par Parallel.

Managed Deep Agents (MDA) est le moyen le plus simple de construire, déployer et exécuter des agents critiques en production, afin que les équipes d'ingénierie puissent se concentrer sur le comportement de l'agent plutôt que de reconstruire la même infrastructure dont chaque agent a besoin. Avec cette sortie, nous étendons Managed Deep Agents pour répondre à quatre défis auxquels la plupart des équipes sont confrontées en production : la mémoire de l'agent, l'authentification, les canaux et la gestion des outils.

### À propos de Managed Deep Agents

Managed Deep Agents combine le harnais Deep Agents avec toute l'infrastructure nécessaire pour exécuter des agents en production. Un Managed Deep Agent est un projet « code-first » dans votre dépôt qui vous permet d'organiser facilement toutes les primitives de votre agent dans un répertoire simple :

```
my-agent/
  agent.py | agent.ts | agent.tsx
  pyproject.toml | package.json    	# dépendances du projet
  instructions.md                  		# prompt synchronisé avec Context Hub
  identity.py | identity.ts        		# auth, scoping des threads, scoping de la mémoire
  memory.py | memory.ts            	# définit la mémoire de votre agent
  tools/                           			# outils personnalisés
  channels/                       	 	# points d'entrée comme Slack et GitHub
  middleware/                      		# middleware personnalisé
  schedules/                       		# planifications (cron) managées
  connectors/                      		# connecteurs managés
  skills/                          			# skills synchronisées avec Context Hub
  sandbox/                         		# configuration du sandbox
  evals/                           			# évaluations de l'agent
```

### Managed Deep Agents en pratique

Imaginez que vous construisiez un agent interne pour soutenir votre équipe commerciale (nous appellerons cet agent notre **GTM Agent** dans cet article). Vous voulez que votre agent puisse consulter les détails de comptes, faire des recherches sur les comptes, rédiger des briefs de réunion, des e-mails de suivi, etc., et aider à maintenir l'engagement des comptes de votre équipe. Pour cela, votre agent a besoin de mémoire, d'accès à des outils, de recherche web, de raisonnement et de planification.

Les harnais d'agents, comme Deep Agents, aident à construire ces agents. Ils fournissent des primitives pour construire des agents complexes capables de prendre en charge des tâches longues et critiques. Avec Deep Agents, faire fonctionner un prototype est simple, mais faire fonctionner l'agent de manière fluide en production demande beaucoup plus.

C'est là qu'intervient Managed Deep Agents. Il packages votre harnais Deep Agents personnalisé avec l'infrastructure managée nécessaire pour exécuter un tel agent à grande échelle. Cela inclut l'ajout de canaux comme Slack, l'identité et l'authentification, et la gestion des permissions pour les outils. Construire cette infrastructure prend généralement des trimestres de feuille de route et nécessite une maintenance continue. Managed Deep Agents permet aux ingénieurs de se concentrer sur la construction de la logique de l'agent et de déléguer le code répétitif.

### La mémoire de votre agent, scopée à l'utilisateur

Lorsqu'un agent est utilisé par plusieurs utilisateurs en production, des systèmes robustes et sécurisés pour gérer la mémoire sont importants. Managed Deep Agents prenait déjà en charge une mémoire d'agent durable, qui permet à un déploiement de conserver des instructions et des préférences à travers les conversations. La configuration de la mémoire peut se faire via de simples fichiers de déclaration :

```
# Un fichier de déclaration de mémoire active la mémoire durable au niveau agent et au niveau utilisateur.
my-agent/
  agent.py
  memory.py
```

Avec Managed Deep Agents 0.8, nous avons ajouté une seconde couche pour la mémoire au niveau utilisateur, scopée à la personne authentifiée qui lance l'exécution de l'agent. Cela donne à l'agent un endroit où stocker un contexte propre à l'appelant, comme des préférences, un style de travail, des tâches récurrentes, ou des détails que l'utilisateur a demandé de retenir, sans mélanger ce contexte avec la mémoire partagée au niveau agent.

```
from managed_deepagents import MemoryLayer, define_memory
memory = define_memory(
    agent=MemoryLayer(),
    user=MemoryLayer(),
)
```

Sous le capot, la mémoire durable s'appuie sur LangSmith Context Hub, qui permet aux équipes de stocker, versionner et collaborer sur des fichiers d'agent comme les Skills et AGENTS.md. La mémoire de l'agent est montée sur `/memories/agent/` et partagée par tous les utilisateurs du déploiement. La mémoire utilisateur est montée sur `/memories/user/` et indexée sur l'identité authentifiée de l'appelant. Le runtime ne copie jamais de contenu entre ces couches, ce qui permet aux équipes de garder par défaut une séparation entre connaissance partagée et contexte personnel. Ceci est utile dans des cas d'usage réels, tels que :

- Un agent de support pourrait utiliser la mémoire d'agent pour les règles d'escalade à l'échelle de l'équipe, et la mémoire utilisateur pour se souvenir qu'un coéquipier spécifique préfère des mises à jour Slack concises.
- Un agent de recherche pourrait conserver des procédures de recherche partagées dans la mémoire d'agent, tout en stockant les types de sources préférés ou les conventions de mise en forme d'un utilisateur individuel dans la mémoire utilisateur.

*« Construire avec Managed Deep Agents a été une expérience si fluide. L'équipe LangChain collabore bien avec nous et nous a aidés à résoudre les problèmes rapidement. Notre application de chat en production fonctionne comme un Managed Deep Agent — avec Context Hub et la mémoire au niveau utilisateur, nous sommes en mesure de préserver la confidentialité des clients tout en offrant une expérience supérieure. »*
— *Zahid, CTO, Kyth.ai*

La mémoire est facilement configurable et vit dans un seul fichier au sein d'un projet Managed Deep Agents. Vous pouvez activer la couche agent, la couche utilisateur, ou les deux. Vous pouvez aussi définir des politiques d'accès pour chaque couche, donnant aux équipes le contrôle sur le moment où la mémoire est disponible et le périmètre auquel elle s'applique. Sauf indication contraire, Managed Deep Agents utilise des valeurs par défaut.

Cette approche en couches garantit que les informations au niveau utilisateur ne « fuient » pas dans une conversation impliquant plusieurs utilisateurs. Prenons l'exemple du **GTM agent** mentionné plus haut. Les utilisateurs pourraient lancer des requêtes dans un message direct (DM) avec l'agent, ou démarrer une requête dans un groupe Slack. Les politiques d'accès et valeurs par défaut définies garantissent que :

- Un DM direct fait agir l'agent selon la préférence de l'utilisateur.
- Les requêtes impliquant plusieurs utilisateurs dans un fil ou un groupe Slack font que l'agent revient par défaut aux préférences de l'espace de travail / de l'équipe.
- Il n'y a pas de fuite de préférences ou de mémoire stockée entre les deux scénarios.

Pour en savoir plus sur la configuration de la mémoire au niveau agent et utilisateur, consultez la documentation.

### Fournir en toute sécurité l'identité de l'utilisateur et de l'agent via les connexions

Les connexions relient un Managed Deep Agent à un service externe tel que GitHub, Notion ou Tavily. Les connexions sont des identifiants nommés dans votre espace de travail LangSmith que vos outils ne font que lire au moment de l'exécution.

Comme pour la mémoire, il est important de scoper les identifiants selon l'objectif de l'agent et la manière dont les utilisateurs interagissent avec lui. Avec Managed Deep Agents, vous pouvez scoper les identifiants au niveau utilisateur ou au niveau agent.

Les identifiants possédés par l'agent sont partagés entre tous les utilisateurs, ce qui est utile pour une capacité d'agent qui ne diffère pas selon la personne, comme la recherche web. À l'inverse, les identifiants possédés par l'utilisateur sont importants lorsque l'utilisateur dispose de permissions propres au sein d'un outil. C'est souvent nécessaire pour des outils comme GitHub, Linear et Notion.

Par exemple, notre **GTM agent** devrait pouvoir transmettre les identifiants de l'utilisateur et utiliser les données Salesforce lorsqu'un utilisateur en fait la demande dans un DM. L'agent devrait aussi pouvoir utiliser des identifiants d'agent pour rechercher sur le web et trouver des informations sur un client.

Managed Deep Agents prend en charge nativement 23 services, dont Linear, GitHub et les outils Google Workspace, où LangSmith gère l'autorisation, les tokens et les méthodes, de sorte que les développeurs n'ont besoin de configurer que l'ID utilisateur et les secrets.

Apprenez comment configurer et utiliser les identifiants dans les connexions ici.

### Accéder aux agents via les canaux préférés des utilisateurs

Les agents internes sont couramment accessibles via des canaux de communication existants comme Slack. Managed Deep Agents fournit un support Slack préconstruit pour simplifier l'exposition des agents là où votre équipe travaille déjà.

Avec cette sortie, Managed Deep Agents prend désormais en charge des workflows Slack plus riches avec le transfert de fichiers, et ajoute des canaux HTTP pour connecter des agents à n'importe quel service capable d'envoyer un webhook JSON.

```
# channels/orders.py
from managed_deepagents import channels
from lib.orders import parse, verify, messaging
channel = channels.http(
    provider="orders",
    verify=verify,
    parse=parse,
    messaging=messaging,
)
```

Pour les workflows basés sur Slack, les utilisateurs peuvent invoquer un agent depuis un DM, une mention d'application, ou une réponse dans un fil. Avec le support du transfert de fichiers, ils peuvent aussi envoyer directement dans la conversation les documents dont l'agent a besoin, comme des logs, des feuilles de calcul, des contrats, des captures d'écran ou des documents clients. Par exemple, avec notre **GTM agent**, un utilisateur peut désormais ajouter des notes d'un appel précédent ou des documents partagés par un client directement dans Slack tout en formulant une requête à l'agent. L'agent récupère alors le fichier, l'ajoute à son contexte et répond en conséquence.

Les canaux HTTP permettent aux équipes d'intégrer des agents dans des outils internes, des portails clients, des systèmes de support, des systèmes de commande, ou toute surface produit capable d'envoyer un webhook. Cela est utile pour les agents orientés client qui vivent sur plusieurs canaux. Par exemple, un agent de support client qui gère la prise en charge et le tri peut vivre dans votre produit, tandis qu'un agent qui planifie des démonstrations et des réunions peut vivre sur votre page web.

Pour les méthodes Slack comme HTTP, les équipes gardent le contrôle de l'authentification, de l'identité et de la mémoire, tout en donnant aux utilisateurs accès aux agents dans les canaux qu'ils préfèrent déjà.

*« [Managed Deep Agents est] de loin la plateforme d'agents la plus complète, de bout en bout. L'intégration Slack a fonctionné parfaitement et nous a facilité la vie puisque nous accédons à tous nos agents via Slack. Nous avons pu déployer plusieurs agents, avec des serveurs MCP personnalisés, en production en utilisant la CLI et GitHub Actions. Nous disposons désormais d'un triage permanent avec accès à la bonne supervision et la capacité d'ouvrir des PR et d'alerter les équipes. »*
— *Derek Gilbert, ingénierie, Consensus*

### Recherche web intégrée, propulsée par Parallel

La recherche web est l'un des outils d'agent les plus courants, nous avons donc décidé de l'intégrer directement à Managed Deep Agents. Désormais, vous pouvez utiliser la recherche web propulsée par Parallel sans créer un compte fournisseur séparé, gérer une clé API supplémentaire, ni câbler vous-même un outil de recherche dans l'agent.

Il suffit de spécifier le serveur MCP dans le dossier des outils, et LangSmith gère les identifiants Parallel et exécute l'outil. L'agent reçoit des extraits pertinents et des URL sources qu'il peut citer, tandis que les appels, la latence et les erreurs apparaissent dans les traces LangSmith.

Ajoutez Parallel à la carte des serveurs dans `tools/mcp.py / tools/mcp.ts`. Définissez `mcp` une seule fois :

```
from managed_deepagents import define_mcp
mcp = define_mcp(
    servers={
        "Parallel": {
            "transport": "http",
            "url": "https://api.smith.langchain.com/v1/managed-tools/servers/parallel/mcp",
        },
    },
)
```

### Pour commencer

Managed Deep Agents 0.8 simplifie l'authentification, la mémoire et les canaux des agents, et introduit la recherche web comme outil prêt à l'emploi.

Nous sommes impatients de voir comment les équipes utilisent ces nouvelles capacités, c'est pourquoi nous rendons **la recherche web Parallel disponible gratuitement** via Managed Deep Agents pendant que MDA est en bêta.

En savoir plus dans la documentation de Managed Deep Agents, ou démarrez avec :

```
uvx --from managed-deepagents mda init my-agent
cd my-agent
uv run mda deploy
```

Nous continuons à améliorer Managed Deep Agents et aimerions savoir ce que vous construisez. Rejoignez notre communauté Slack pour partager vos projets et nous faire part de vos retours.

## Pourquoi ça compte
Cette sortie illustre la course actuelle des plateformes d'orchestration d'agents (LangChain face à des acteurs comme LlamaIndex, CrewAI ou les offres cloud natives) à combler le fossé entre prototype et production via une infrastructure managée standardisée (mémoire, identité, canaux). C'est un signal clair que la gestion fine de la mémoire par utilisateur et l'authentification scopée deviennent des prérequis attendus pour tout agent d'entreprise déployé à grande échelle.
