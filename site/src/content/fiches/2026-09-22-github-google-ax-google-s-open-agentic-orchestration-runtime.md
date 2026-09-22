---
title: "GitHub - google/ax: Google's open agentic orchestration runtime"
date: 2026-09-22
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fgithub.com%2Fgoogle%2Fax%3Futm_source=tldrai/1/010001a0c42e94b8-7b241079-f6b5-4a4c-afea-c924ebe9e012-000000/OBJwCUnM5rt_obI0e9Px-dH7MlUNvN7Y1pP8xjsaxHc=452"
authors: ["Google"]
keywords: ["orchestration d'agents", "Kubernetes", "sandboxing", "IA agentique", "Google", "CLI"]
theme: "IA"
tone: "tutorial"
used_in: ["2026-09-22"]
---

## Résumé
AX est un nouvel orchestrateur déclaratif open source publié par Google, conçu pour exécuter des milliards de charges de travail d'agents autonomes à l'échelle d'un cluster, en s'appuyant sur Agent Substrate pour l'exécution en bac à sable (sandbox). Son fonctionnement rappelle volontairement celui de Kubernetes, avec une interface en ligne de commande calquée sur `kubectl` (`apply`, `get`, `describe`, `watch`, `delete`) et des verbes propres aux agents (`suspend`, `resume`, `ssh`). Le projet repose sur quatre primitives déclaratives — `Task`, `Workspace`, `Gateway` et `Model` — qui gèrent respectivement l'isolation, le pré-câblage des ressources (dépôts Git, serveurs MCP), le contrôle du trafic réseau sortant et la configuration du LLM utilisé. Le projet est encore en phase d'évolution active, sous licence Apache 2.0, avec des changements majeurs non rétrocompatibles attendus avant une version stable.

## Points clés
- AX est un orchestrateur déclaratif à haut débit visant à exécuter des milliards de tâches d'agents autonomes par cluster, avec une approche « Kubernetes pour les agents ».
- Quatre primitives centrales : `Task` (bac à sable isolé avec limites CPU/mémoire), `Workspace` (pré-configuration des dépôts Git, serveurs MCP et packages de compétences), `Gateway` (liste blanche d'hôtes pour le trafic sortant) et `Model` (configuration du LLM avec identifiants Kubernetes).
- La CLI `ax` reproduit délibérément les commandes de `kubectl`, tout en ajoutant des verbes spécifiques aux agents comme `suspend`, `resume` et `ssh`.
- Le déploiement nécessite un cluster Kubernetes, l'outil `ko`, un registre de conteneurs et une API de contrôle Agent Substrate joignable.
- Le projet reconnaît explicitement que les agents forment une nouvelle catégorie de charge de travail (ni microservice sans état, ni job batch), nécessitant une isolation stricte et une surveillance des coûts.
- Statut expérimental assumé : les concepts, protocoles et spécifications sont encore en cours d'affinement, avec risque de changements majeurs avant une version stable.

## Analyse approfondie
**Avertissement**

Nous sommes encore en train d'affiner activement nos concepts fondamentaux, protocoles et spécifications. Nous introduirons probablement des changements majeurs et non rétrocompatibles avant une publication stable.

Déclarez une tâche agentique avec des spécifications de workspaces et de gateway. AX la met en bac à sable (sandbox), configure son workspace, cloisonne son réseau, et aide à la faire fonctionner à grande échelle.

AX est un orchestrateur déclaratif à haut débit conçu pour exécuter des milliards de charges de travail d'agents autonomes dans un cluster. Il fonctionne au-dessus d'Agent Substrate pour l'exécution en bac à sable et est conçu pour exécuter des milliards de tâches par cluster. Si vous avez déjà utilisé Kubernetes, `ax` vous semblera familier.

```
# task.yaml
apiVersion: ax.io/v1alpha1
kind: Workspace
metadata:
  name: golang
spec:
  git:
    - repo: https://github.com/golang/go.git
      branch: "my-fix"
---
apiVersion: ax.io/v1alpha1
kind: Task
metadata:
  name: test
spec:
  workspaces:
    - name: golang
      goal: "Ensure that Go tool chain is available and is built from source"
  debug: true   # lets you `ax ssh` into the sandbox
```

Appliquez-la ensuite, observez son démarrage, et surveillez l'agent par-dessus son épaule :

```
ax apply -f task.yaml
ax watch task test
ax ssh test -- ls -al /workspace
```

Les agents constituent un nouveau type de charge de travail. Ce ne sont ni des microservices sans état, ni des tâches batch qui s'exécutent jusqu'à leur terme. Ils accumulent de l'état, ont besoin d'une isolation stricte, font appel à des API de modèles et à des serveurs d'outils, et peuvent dépenser de l'argent en boucle si personne ne surveille. AX fournit quatre primitives simples qui gèrent tout cela de manière déclarative :

| Vous voulez... | AX vous donne... |
|---|---|
| Exécuter du code d'agent non fiable dans un bac à sable isolé avec des limites CPU/mémoire | **`Task`** |
| Pré-configurer des dépôts Git, des serveurs MCP et des packages de compétences (skill packages) pour que chaque agent démarre à chaud | **`Workspace`** |
| Verrouiller le trafic sortant sur une liste blanche explicite d'hôtes | **`Gateway`** |
| Configurer le LLM utilisé par la plateforme elle-même, avec des identifiants issus d'un secret Kubernetes | **`Model`** |
| Mettre en pause un agent inactif et reprendre exactement là où il s'était arrêté | `ax suspend` / `ax resume` |
| Se connecter en shell à un agent en cours d'exécution pour voir ce qu'il fait | `ax ssh` |

Tout est exprimé sous forme de manifestes `ax.io/v1alpha1` et appliqué avec une seule commande.

`go install github.com/google/ax/cmd/ax@latest`

Ceci place le binaire `ax` dans `$(go env GOPATH)/bin`. Assurez-vous que ce répertoire figure dans votre `PATH`.

Vous avez besoin d'un cluster Kubernetes, de `ko` (`brew install ko`), d'un registre de conteneurs accessible par votre cluster, et d'une API de contrôle Agent Substrate joignable (par défaut, en interne au cluster : `api.ate-system.svc.cluster.local:443`).

`make deploy AX_IMAGE_REPO=<your-registry>`

Cette commande déploie Redis, puis construit et déploie les images du control plane avec `ko`. Tout est placé dans le namespace `ax-system`.

```
ax apply -f examples/task.yaml       # Task + Workspace + Gateway + Model en un seul fichier
ax get tasks
# NAME      ATESPACE   PHASE     ACTOR           WORKER-IP    AGE
# task123   default    Running   task123         10.20.3.67   1m
ax watch task task123                # suivre en flux les changements de phase et de condition
ax ssh task123 -- ls -la /workspace  # explorer l'intérieur du bac à sable
ax suspend task task123              # sauvegarder l'état et mettre en pause
ax resume task task123               # reprendre là où on s'était arrêté
```

Vous voulez voir le cycle de vie complet de bout en bout ? Exécutez `./demo.sh`. Ce script applique un workspace personnalisé, attend qu'il soit prêt, exécute des commandes via `ax ssh`, puis suspend la tâche.

| Guide | Lisez-le pour... |
|---|---|
| Concepts | Comprendre ce que font respectivement un `Task`, un `Workspace`, une `Gateway` et un `Model`, et comment une tâche progresse à travers ses phases et conditions. |
| Manifests | Écrire votre propre YAML, avec un exemple annoté de chaque type. |
| Sandbox | Voir ce que fait le runner au démarrage et sur quoi votre commande peut s'appuyer : serveur de métadonnées, services invités, environnement. |
| Runners | Comprendre le contrat entre le control plane et le conteneur de tâche, et construire votre propre image de runner pour remplacer celle par défaut. |
| Networking | Atteindre une tâche en cours d'exécution via le routeur atenet, depuis le cluster, votre ordinateur portable, ou un client gRPC. |
| Architecture | Comprendre comment le control plane s'articule, ainsi que la référence de l'API. |
| Development | Construire, tester et livrer des modifications à AX lui-même. |

`ax` communique avec le control plane via gRPC. Il a délibérément la forme de `kubectl` : `apply`, `get`, `describe`, `watch`, `delete`, plus quelques verbes spécifiques aux agents.

```
# Appliquer n'importe quoi (YAML multi-documents, fichier ou stdin)
ax apply -f examples/task.yaml
# Tâches
ax get tasks                          # lister
ax get tasks -a my-atespace           # lister dans un autre atespace
ax get task task123                   # spec complète + statut en direct au format YAML
ax describe task task123              # détail lisible par un humain
ax watch task task123                 # suivre en flux les transitions de statut et de condition
ax suspend task task123               # sauvegarder l'état de l'acteur et mettre en pause
ax resume task task123                # reprendre une tâche suspendue
ax delete task task123
# Se connecter en shell au bac à sable en cours d'exécution
ax ssh task123                        # shell interactif (la tâche doit avoir spec.debug: true)
ax ssh task123 -- ls -la /workspace   # commande ponctuelle
ax ssh task123 -- python3 main.py
# Les gateways, workspaces et models suivent le même schéma
ax get gateways
# NAME              ATESPACE   LISTENERS             EGRESS-HOSTS
# default-gateway   default    8494/gRPC,8080/HTTP   *
ax describe gateway default-gateway
ax delete gateway default-gateway
ax get workspaces
# NAME                ATESPACE   GIT-REPOS   MCP-SERVERS
# default-workspace   default    1           1
ax describe workspace default-workspace
ax delete workspace default-workspace
ax get models
# NAME            ATESPACE   PROVIDER   MODEL
# default-model   default    google     gemini-3.8-flash
ax describe model default-model
ax delete model default-model
# Plomberie de connexion
ax ctx                                # contexte kube actif et comment ax joint le control plane
ax tunnel list                        # tunnels en arrière-plan (l'état est stocké dans ~/.ax/tunnels)
ax tunnel stop
ax version
```

`ax` suit votre contexte Kubernetes actif. Changez de cluster et `ax` résout et établit en arrière-plan un tunnel vers le control plane de ce cluster.

```
kubectx staging-cluster
ax get tasks
kubectx prod-cluster
ax get tasks
# Ou cibler un contexte sans changer
ax --context=dev-cluster get tasks
```

| Flag | Description | Valeur par défaut |
|---|---|---|
| `-a`, `--atespace` | Portée (atespace) de la commande | `default` |
| `-n`, `--namespace` | Namespace Kubernetes où AX est installé | `ax-system` |
| `--context` | Contexte Kubernetes à cibler | `kubectx`/`current-context` actif |
| `--server` | Adresse du control plane, en contournant la détection automatique | dérivée du contexte kube, ou `$AX_SERVER` |

Licence Apache 2.0. Voir le fichier LICENSE pour plus de détails.

## Pourquoi ça compte
AX illustre la tendance des grands acteurs cloud à traiter les agents IA comme une catégorie d'infrastructure à part entière, nécessitant leur propre couche d'orchestration façon Kubernetes plutôt qu'un simple wrapper au-dessus des outils existants. À suivre pour quiconque déploie des agents autonomes en production et doit résoudre les problèmes d'isolation, de coûts et de mise à l'échelle.
