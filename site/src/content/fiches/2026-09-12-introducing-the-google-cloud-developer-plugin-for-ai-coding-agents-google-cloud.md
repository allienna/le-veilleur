---
title: "Introducing the Google Cloud Developer Plugin for AI Coding Agents | Google Cloud Blog"
date: 2026-09-12
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fcloud.google.com%2Fblog%2Ftopics%2Fdevelopers-practitioners%2Fintroducing-the-google-cloud-developer-plugin-for-ai-coding-agents%3Futm_source=tldrai/1/010001a090aa182a-d18dee2c-9abe-499b-abe2-6b2b9843ff74-000000/d3J4fsC4e6X4f6Hg5DE14AE20wa-reSz-3wnwklFa20=452"
authors: ["Jonathan Lee"]
keywords: ["Google Cloud", "agents IA", "plugins", "MCP", "coding agents"]
theme: "Tech"
tone: "news"
used_in: ["2026-09-12"]
---

## Résumé
Google Cloud annonce un nouveau plugin, `google-cloud-developer`, destiné aux agents de codage IA (Claude Code, Antigravity CLI, Codex CLI, etc.). Ce plugin regroupe des Agent Skills et un serveur MCP (Developer Knowledge) en un seul bundle installable, afin de simplifier l'authentification, la gestion de projets et les interactions avec gcloud. Il s'appuie sur la spécification ouverte « Agent Plugins », un standard neutre visant à unifier l'empaquetage des skills et serveurs MCP entre différents assistants IA. L'installation se fait via le dépôt public Google Agent Skills, avec des instructions spécifiques selon l'agent utilisé.

## Points clés
- Le plugin `google-cloud-developer` combine des skills, de la documentation et un accès programmatique à Google Cloud (auth, IAM, gestion de projets, garde-fous pour la CLI gcloud).
- Il embarque la configuration du serveur MCP « Developer Knowledge », qui donne aux agents un accès à jour à la documentation officielle Google.
- Il respecte la spécification ouverte et vendor-neutral « Agent Plugins », pensée pour rendre les skills et serveurs MCP portables entre agents IA.
- Objectif affiché : résoudre le « couplage d'outils » — le fait que des skills isolés sont moins efficaces que des capacités combinées (connaissance du domaine + recommandations de workflow + interaction avec un environnement réel).
- Installable depuis le dépôt public Google Agent Skills sur Antigravity CLI, Claude Code et Codex CLI, via un marketplace de plugins.
- Un exemple d'usage est donné : onboarding d'un nouveau projet avec configuration de la facturation et authentification locale en tant qu'identité de service.

## Analyse approfondie
##### Jonathan Lee
Content Strategist

Les Agent Skills s'intègrent bien aux côtés de la documentation et des serveurs MCP distants en tant que moyens de favoriser la réussite de vos workflows IA. Ils réduisent l'utilisation de la fenêtre de contexte pour certains cas d'usage et sont simples à installer. Cependant, vous avez peut-être remarqué que la gestion de skills individuels peut devenir difficile à manier, ou que certains skills sont surtout utiles lorsqu'ils agissent de concert avec d'autres skills ou serveurs MCP vers un même objectif. C'est là que les plugins entrent en jeu.

Aujourd'hui, nous sommes ravis d'annoncer un nouveau plugin Google Cloud pour les agents de codage IA ! Conçus comme des bundles installables, les agent plugins dotent l'agent IA de votre choix de skills et d'outils pour être plus efficace sur Google Cloud.

## Résoudre le problème du couplage d'outils

À mesure que vous étendez votre usage des agents de codage, vous constaterez peut-être qu'ils deviennent significativement plus performants lorsqu'ils utilisent des skills liés entre eux, ou avec un contexte et un outillage complémentaires. Par exemple, un agent qui analyse une infrastructure est plus efficace lorsqu'il combine à la fois la connaissance du domaine, des recommandations de workflow, et la capacité d'interagir avec un environnement réel.

Les plugins résolvent ce problème de couplage en regroupant des capacités liées en bundles cohérents et installables. Cela permet de tirer parti à la fois de capacités fondamentales larges et d'outils profonds et spécifiques à un produit, sans avoir à gérer des dépendances complexes.

Pour cette version, nous avons commencé par un plugin fondamental qui prend en charge les fonctionnalités d'agent pour tous les utilisateurs de Google Cloud, en mettant l'accent sur le fait de faciliter pour les agents la récupération de skills liés à Google Cloud, l'utilisation de la documentation officielle, et la gestion des interactions programmatiques avec Google Cloud.

## Construit sur un standard ouvert

Nous avons également construit notre plugin en conformité avec la spécification Agent Plugins, un standard ouvert et neutre vis-à-vis des fournisseurs, destiné à empaqueter les Agent Skills et les serveurs Model Context Protocol (MCP) en unités portables et interopérables. Plutôt que d'exiger des développeurs qu'ils maintiennent des configurations et des wrappers différents pour chaque assistant IA, le standard Agent Plugins fournit un manifeste et une structure de répertoire unifiés.

Notre plugin Google Cloud adopte ce standard afin de garantir que les développeurs, à travers une variété d'environnements de codage IA, obtiennent un accès cohérent et de haute qualité aux outils qui les aident à réussir avec Google Cloud. Cela inclut non seulement les plugins dont nous parlons aujourd'hui, mais aussi tous les autres plugins publiés dans le dépôt Google Agent Skills.

Penchons-nous sur le plugin phare que nous venons de publier dans le dépôt Google Agent Skills : `google-cloud-developer`. Ce plugin existe pour aider les agents à naviguer avec succès dans les fondamentaux de l'interaction avec Google Cloud : des éléments comme l'authentification, l'autorisation, la gestion de projets, et les garde-fous pour les opérations de la CLI gcloud. Ce plugin embarque également la configuration du serveur MCP Developer Knowledge, qui donne aux agents un ancrage à jour dans la documentation officielle des développeurs de Google.

### Le plugin en action : onboarding de projet et authentification d'identité

Pour voir comment ce plugin fonctionne, imaginez une situation où vous démarrez un nouveau projet dans le cadre du travail sur un script. Avec le plugin `google-cloud-developer` installé, vous pouvez demander à votre agent :

> Je suis totalement nouveau sur cette plateforme, et j'ai besoin de créer un compte et un premier projet avec la facturation configurée. Ensuite, j'ai besoin que ma machine locale soit authentifiée pour qu'un script que je suis en train d'écrire puisse appeler les API en tant qu'identité de service plutôt qu'en tant que moi.

1. **Conscience de l'environnement :** l'agent exécute silencieusement des vérifications en arrière-plan sur votre environnement réel pour des prérequis comme la disponibilité de la CLI et l'existence potentielle de projets ou d'organisations.
2. **Revue :** l'agent prend en compte les bonnes pratiques IAM afin d'éviter des risques qui pourraient être implicitement supposés dans la demande, comme des fuites accidentelles de clés ou des commits git.
3. **Interaction avec des garde-fous :** l'agent esquisse une feuille de route du workflow et propose d'agir sur ces étapes avant de modifier la moindre ressource.

## Installer les plugins Google Cloud

Comme les plugins Google Cloud sont disponibles depuis le dépôt ouvert Google Agent Skills et respectent la disposition standard des Agent Plugins, les ajouter à votre environnement est simple. Voici par exemple comment installer le plugin `google-cloud-developer` :

### Antigravity CLI

Installez le plugin directement via la CLI en utilisant son chemin dans le dépôt Google Agent Skills.

### Claude Code

Ajoutez le marketplace de plugins Google, puis installez le plugin.

### Codex CLI

Ajoutez le marketplace de plugins Google, puis installez le plugin.

## Prochaines étapes

Si vous êtes déjà utilisateur de Google Cloud, essayez les étapes d'installation ci-dessus pour préparer votre agent à réussir. Nous pensons que le résultat vous plaira ! Pour ceux qui souhaitent une approche plus guidée, notre nouveau codelab vous accompagnera dans l'installation et l'exploration initiale du plugin dans Antigravity.

Si vous découvrez Google Cloud, vous pouvez également démarrer grâce aux instructions de notre documentation pour vous configurer en vue du développement local.

Les lecteurs les plus curieux peuvent aussi explorer plus en profondeur les plugins et agent skills disponibles dès aujourd'hui dans le dépôt Google Agent Skills.

## Pourquoi ça compte
Cette annonce illustre la consolidation en cours autour d'un standard ouvert (« Agent Plugins ») pour packager skills et serveurs MCP, un enjeu clé pour l'interopérabilité des agents de codage IA entre fournisseurs (Google, Anthropic, OpenAI). À surveiller pour toute veille sur l'écosystème des outils agentiques et leur intégration au cloud.
