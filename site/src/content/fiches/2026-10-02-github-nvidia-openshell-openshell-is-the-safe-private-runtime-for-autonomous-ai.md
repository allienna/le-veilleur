---
title: "GitHub - NVIDIA/OpenShell: OpenShell is the safe, private runtime for autonomous AI agents."
date: 2026-10-02
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fgithub.com%2FNVIDIA%2FOpenShell%3Futm_source=tldrai/1/010001a0f7aa9805-70743e14-a261-4a3a-b799-4b3fad25a075-000000/eLenn5wwvva_TDUSwhNS9uzgFg5yVU7tO2U1HXIz5rk=452"
authors: ["NVIDIA"]
keywords: ["agents IA", "sandboxing", "vérification formelle", "isolation noyau", "NVIDIA", "gestion des identifiants"]
theme: "Sécurité"
used_in: ["2026-10-02"]
---

## Résumé
OpenShell est un runtime open-source publié par NVIDIA, conçu pour exécuter en sécurité des flottes d'agents IA autonomes. Il leur donne accès aux fichiers, API et identifiants dont ils ont besoin sans leur accorder un accès illimité aux données, secrets ou réseau de l'utilisateur. Le projet combine une application des politiques au niveau du noyau (sandbox isolé par agent) avec une vérification formelle des changements de politique pour repérer les extensions de privilèges risquées avant leur déploiement. Il fournit une CLI, des SDK dans plusieurs langages, une intégration Kubernetes/Helm et des « skills » pour agents de codage, le tout sous licence Apache 2.0.

## Points clés
- Sandbox isolé par agent avec contrôle au niveau du noyau sur les accès fichiers, les appels système et les connexions réseau.
- Vérification formelle des changements de politique avant leur application, pour signaler les accès risqués (nouvel hôte, nouvelle méthode d'API) en vue d'une revue humaine.
- Gestion sécurisée des identifiants : les agents ne voient jamais les secrets réels, qui ne sont injectés que dans les requêtes vers des points de terminaison approuvés.
- Installation simple via un script curl, image sandbox minimale (Ubuntu) par défaut, compatible Linux, macOS (Apple Silicon) et Windows (WSL 2, expérimental).
- SDK disponibles en Python, TypeScript, Go et Rust, plus un déploiement de la gateway via Helm sur Kubernetes.
- Télémétrie anonyme limitée à des catégories et comptages opérationnels, désactivable ; projet sous licence Apache License 2.0.

## Analyse approfondie
Important

**Nouveauté dans OpenShell 0.1.x :** un rythme de publication stable, de nouvelles primitives d'isolation, une surface d'extension élargie et de nouvelles API. Consultez le guide de mise à niveau vers la 0.1.0.

OpenShell est le runtime sûr et privé pour des flottes d'agents IA autonomes. Les agents sont les plus utiles lorsqu'ils peuvent lire des fichiers, installer des paquets, appeler des API et utiliser des identifiants. OpenShell leur donne cette capacité sans leur accorder un accès illimité à vos données, secrets ou réseau. Vous déclarez ce que chaque agent peut toucher dans une politique (policy), et OpenShell l'applique.

OpenShell régit ce que les agents peuvent faire de deux manières : il instrumente le noyau (kernel) pour appliquer la politique à chaque accès fichier, appel système et connexion réseau en temps réel, et il utilise la vérification formelle pour contrôler ce qu'un changement de politique autoriserait avant qu'il ne soit appliqué.

- **Application au niveau du noyau.** Chaque agent s'exécute dans un sandbox isolé. Des contrôles du noyau limitent les fichiers auxquels il peut accéder et les appels système qu'il peut effectuer, et chaque connexion réseau passe par un contrôle de politique avant de quitter le sandbox. Les agents ne voient jamais les identifiants réels ; OpenShell ne les ajoute qu'aux requêtes destinées à des points de terminaison (endpoints) approuvés.
- **Changements de politique vérifiés formellement.** Avant qu'un changement de politique ne soit approuvé, OpenShell utilise la vérification formelle pour signaler tout nouvel accès risqué qu'il accorderait, comme atteindre un nouvel hôte avec des identifiants ou appeler une nouvelle méthode d'API, afin que ces changements attendent une revue humaine.

Voir Architecture pour comprendre comment la gateway, le superviseur (supervisor) et le sandbox s'articulent.

Vous avez besoin de Linux, macOS sur Apple Silicon, ou Windows avec WSL 2 (expérimental), plus Docker, Podman, ou une virtualisation hôte. Voir la Support Matrix pour plus de détails.

```
curl -LsSf https://raw.githubusercontent.com/NVIDIA/OpenShell/main/install.sh | sh
openshell sandbox create --name demo
```

L'installeur met en place la CLI et une gateway locale. L'image de sandbox par défaut est une Ubuntu minimale sans agent installé. Pour exécuter un véritable agent, suivez Run Your First Agent : ce guide exécute OpenCode sur un modèle OpenRouter gratuit et montre comment approuver de nouveaux accès au fur et à mesure que l'agent en a besoin.

- Sandboxes : images, runtimes, GPU, et cycle de vie.
- Policies : règles de système de fichiers, réseau et processus, avec l'advisor et le prover pour examiner les changements.
- Providers : identifiants qui ne fonctionnent qu'aux points de terminaison approuvés, y compris pour l'inférence.
- Gateways : le plan de contrôle pour les sandboxes, les politiques et l'accès.
- Kubernetes : déployer la gateway avec Helm. Votre CNI doit appliquer `NetworkPolicy`.
- Extensibility : middleware, intercepteurs et pilotes de calcul (compute drivers).
- Tutorials : parcours pas à pas sur les politiques et les agents.
- Versions préliminaires et de développement : essayez une prochaine version ou le dernier commit sur `main`.

Installez les skills publics d'OpenShell pour votre agent de codage :

`npx skills add NVIDIA/OpenShell`

Ces skills apprennent à votre agent à piloter la CLI OpenShell, à écrire des politiques de sandbox, et à déboguer les gateways et le routage d'inférence. Elles se trouvent dans `skills/` et fonctionnent sans checkout des sources d'OpenShell.

Les SDK connectent des applications à une gateway OpenShell. Ils n'installent pas la CLI. Utilisez la même version d'OpenShell pour le SDK et la gateway si possible.

| Langage | Installation | Docs |
|---|---|---|
| Python | `uv add openshell` | README |
| TypeScript | `npm install @nvidia/openshell-sdk` (GitHub Packages) | README |
| Go | `go get github.com/NVIDIA/OpenShell/sdk/go@latest` | README |
| Rust | `cargo add openshell-sdk --git https://github.com/NVIDIA/OpenShell --tag <release-tag>` | Installation and usage |

- **Questions et discussions :** GitHub Discussions
- **Rapports de bugs et demandes de fonctionnalités :** GitHub Issues, en utilisant les modèles de ticket
- **Vulnérabilités de sécurité :** suivez SECURITY.md. N'ouvrez pas de ticket GitHub.
- **Feuille de route :** OpenShell Roadmap et le RFC board
- **Essayer dans le cloud :** Brev Launchable

OpenShell est conçu agent-first : il est développé avec les mêmes workflows pilotés par agents qu'il permet. Voir CONTRIBUTING.md pour la configuration de développement et le processus de contribution, et AGENTS.md pour les conventions de code du dépôt.

OpenShell collecte une télémétrie anonyme, limitée à des catégories et des comptages opérationnels, pour aider à améliorer le projet. Elle ne collecte ni noms de sandbox, ni noms d'hôtes, ni chemins de fichiers, ni prompts, ni identifiants, ni noms de providers ou de modèles, ni contenu utilisateur. Pour la désactiver, définissez `OPENSHELL_TELEMETRY_ENABLED=false` sur la gateway, ou `server.telemetryEnabled=false` pour les installations Helm. Vous pouvez également compiler le projet sans la télémétrie. Voir Telemetry pour plus de détails et les rapports communautaires de télémétrie pour les tendances d'usage publiées.

Ce logiciel récupère, accède ou interagit automatiquement avec des éléments externes. Ces éléments récupérés ne sont pas distribués avec ce logiciel et sont régis uniquement par des conditions et licences distinctes. Vous êtes seul responsable de trouver, d'examiner et de respecter toutes les conditions et licences applicables, ainsi que de vérifier la sécurité, l'intégrité et l'adéquation de tout élément récupéré à votre cas d'usage spécifique. Ce logiciel est fourni « EN L'ÉTAT », sans garantie d'aucune sorte. L'auteur ne fait aucune déclaration ni garantie concernant les éléments récupérés, et décline toute responsabilité pour toute perte, dommage, responsabilité ou conséquence juridique résultant de votre utilisation ou de votre incapacité à utiliser ce logiciel ou tout élément récupéré. Utilisez ce logiciel et les éléments récupérés à vos propres risques.

Ce projet est sous licence Apache License 2.0.

## Pourquoi ça compte
OpenShell illustre une réponse concrète à un problème croissant de la veille sécurité/IA : comment donner aux agents autonomes un accès réel aux systèmes et aux identifiants sans ouvrir la porte à des abus, grâce à une isolation noyau et une vérification formelle des politiques plutôt qu'à de simples bonnes pratiques déclaratives.
