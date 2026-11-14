---
title: "Put MCP Next to Your API, Not on Top of It | Naftiko"
date: 2026-11-14
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fnaftiko.io%2Fblog%2Fput-mcp-next-to-your-api-not-on-top%3Futm_source=tldrdev/1/010001a1d4d6d4f1-3f79bd2d-3bd3-45e7-9808-ba3d194e24a0-000000/Oc7htz5oxxwjR97DgRTXUMO5vF9Vqo3hhNMOoqy6eLM=452"
keywords: ["MCP", "API", "REST", "GraphQL", "agents IA", "architecture logicielle"]
theme: "Software"
tone: "opinion"
used_in: ["2026-11-14"]
---

## Résumé
Cet article de blog Naftiko défend une architecture alternative à la pratique courante consistant à empiler un serveur MCP au-dessus d'un serveur API existant. Selon l'auteur, cette approche "stackée" ajoute un saut réseau, double les contrats à maintenir, et surtout limite MCP aux capacités de l'API REST/GraphQL sous-jacente. La solution proposée, incarnée par le concept de "capability" d'Ikanos, consiste à exposer REST et MCP côte à côte à partir des mêmes flux internes, sans qu'un protocole ne serve de couche au-dessus de l'autre. L'article argumente que MCP dispose de mécanismes natifs (découverte, elicitation, tâches longues) sans équivalent standard en REST ou GraphQL, ce qui rendrait l'empilement structurellement limitant pour l'ère des agents.

## Points clés
- Empiler un serveur MCP sur un serveur API ajoute un saut réseau, un second contrat à synchroniser et un déploiement supplémentaire à opérer.
- Un serveur MCP stacké ne peut jamais dépasser les capacités de l'API REST/GraphQL qu'il enveloppe.
- Le modèle de "capability" Ikanos déclare ce qu'il consomme (API amont), les flux qui les agrègent, et ce qu'il expose — REST et MCP étant deux adaptateurs du même flux, référencés via `ref`.
- Une primitive `forward` permet de migrer une API existante ressource par ressource, en ajoutant un outil MCP à chaque étape, sans réécriture complète.
- MCP intègre nativement la découverte (`tools/list`), l'elicitation (poser une question à l'utilisateur en cours d'appel) et les tâches longues durables — des capacités sans équivalent standard en REST ou GraphQL.
- La thèse centrale : MCP deviendra l'interface principale de l'ère agentique, REST et GraphQL demeurant utiles pour les applications et partenaires qui en ont besoin.

## Analyse approfondie
La plupart des équipes ajoutent MCP de la même façon : elles prennent le serveur API qu'elles exploitent déjà, placent un serveur MCP devant, et font correspondre chaque outil (tool) à un endpoint. Cela se déploie vite. Mais cela laisse aussi deux couches à faire fonctionner, deux contrats à garder alignés, et un saut réseau supplémentaire à chaque appel d'agent.

Il y a un problème plus profond. **Un serveur MCP empilé sur un serveur API ne peut faire que ce que ce serveur API sait faire.** Et les agents commencent à avoir besoin de choses que REST ou GraphQL n'ont jamais été conçus pour offrir.

### L'empilement ajoute un saut et un second contrat

Dans la configuration empilée, chaque appel d'outil transite ainsi : agent → serveur MCP → serveur API → systèmes amont. Le serveur MCP re-sérialise ce que le serveur API vient de sérialiser, gère sa propre authentification, et nécessite son propre déploiement, ses propres logs et sa propre astreinte (on-call).

Cela ajoute également un second contrat. Le serveur API dispose d'une description OpenAPI, et le serveur MCP possède des descriptions d'outils qui paraphrasent cette dernière. Quand la signification d'un champ change, les deux doivent être mis à jour — et généralement, un seul le sera.

### Une capability expose les deux, côte à côte

Une "capability" Ikanos est construite différemment. Elle déclare ce qu'elle **consomme** (les API amont), les flux dans lesquels elle les **agrège**, et ce qu'elle **expose**. REST et MCP sont deux adaptateurs dans la même liste `exposes`. Les deux référencent le même flux via `ref`, de sorte qu'aucun des deux ne se place devant l'autre :

```
capability:
  consumes:
    - import: legacy
      from: ./shared/legacy-consumes.yaml
  aggregates:
  - namespace: crew-resolver
    flows:
      resolve-crew-for-ship:
        description: "Resolve crew member names and roles for a given ship"
        steps:
          # call the upstream APIs, join and map the results once
  exposes:
  - type: rest
    namespace: shipyard-api
    resources:
      ship-crew:
        path: "/ships/{{imo}}/crew"
        operations:
          get-ship-with-crew:
            method: GET
            ref: crew-resolver.resolve-crew-for-ship
      voyages:
        path: "/voyages/{{path}}"
        forward:
          targetNamespace: legacy
  - type: mcp
    namespace: shipyard-tools
    tools:
      get-ship-with-crew:
        description: "Get ship details with resolved crew names"
        ref: crew-resolver.resolve-crew-for-ship
```

Les appels amont, les identifiants, les mappings et la logique des étapes sont écrits une seule fois. Un seul moteur les exécute pour les deux adaptateurs. L'appel d'outil d'un agent va directement au flux, sans détour par REST.

### Faire évoluer l'API existante, et ajouter MCP dans le même mouvement

Cela ouvre également une voie de migration. On place la capability là où se trouve le serveur API actuel, et on la fait migrer une ressource à la fois :

- **Pas encore migrée :** un `forward` REST relaie la requête vers l'API existante, inchangée. Les clients ne voient aucune différence.
- **Migrée :** la ressource devient une opération adossée à un flux. Elle peut désormais joindre plusieurs systèmes amont, remodeler le payload, ou corriger un nommage dont l'ancienne API restait prisonnière.
- **Prête pour les agents :** le même flux devient un outil MCP avec une seule référence (`ref`). Pas de seconde implémentation, pas de second déploiement.

Chaque étape est petite et réversible, et chacune améliore les deux interfaces en même temps. Quand le dernier `forward` disparaît, l'ancienne API est remplacée. MCP est arrivé en chemin, et non comme un projet séparé.

### MCP dépasse désormais REST et GraphQL

Le fait de les placer côte à côte compte pour une seconde raison : les protocoles s'éloignent l'un de l'autre. MCP propose désormais des interactions que les API REST et GraphQL n'offrent généralement pas :

- **La découverte** est intégrée au protocole. `tools/list` renvoie chaque outil avec une description écrite pour un modèle, depuis le serveur en cours d'exécution. REST s'appuie sur un document OpenAPI publié séparément, s'il existe. L'introspection GraphQL renvoie un schéma, pas la finalité de chaque opération.
- **L'elicitation** permet à un serveur d'interrompre un appel en cours pour poser une question à l'utilisateur : quel compte, confirmer le montant, choisir une date. Ni REST ni GraphQL ne disposent d'un moyen standard de poser une question à l'appelant au milieu d'une requête.
- **Les tâches (tasks)** permettent à un appel de longue durée de renvoyer immédiatement un identifiant (handle), afin que le client puisse vérifier son statut, récupérer le résultat plus tard, ou l'annuler. REST et GraphQL laissent ce contrat à l'initiative de chaque API.

Ainsi, un serveur MCP empilé ne peut pas offrir d'elicitation ni de tâches. Le serveur API sous-jacent n'a nulle part où poser la question, et aucune tâche à rapporter. Une capability le peut, car ses flux ne sont pas limités par REST. Le support d'Ikanos pour les deux est en cours de revue : une étape `elicit` met un flux en pause et interroge l'utilisateur via MCP, et un flux marqué `mode: task` s'exécute comme une tâche MCP durable qui survit à un redémarrage. Via REST, le même flux répond `501 Not Implemented` et nomme l'étape qui nécessitait une saisie. L'écart est réel, et il se manifeste jusque dans le moteur lui-même.

C'est pourquoi nous pensons que **MCP deviendra l'interface principale de l'ère agentique**, REST et GraphQL restant utilisés en parallèle pour les applications et partenaires qui en ont besoin. Empiler MCP sur une API existante limite le protocole le plus récent à ce que l'ancien sait faire. Les placer côte à côte permet à chaque protocole d'exploiter tout son potentiel.

### À retenir

- Empiler MCP sur un serveur API ajoute un saut, un second contrat et un second déploiement.
- Une capability Ikanos expose REST et MCP côte à côte, à partir des mêmes `consumes` et des mêmes flux.
- Utilisez `forward` pour reprendre un serveur API existant une ressource à la fois, et ajoutez un outil MCP pour chaque flux au fur et à mesure.
- La découverte, l'elicitation et les tâches intégrées n'ont pas d'équivalent standard en REST ou GraphQL. Un serveur MCP empilé ne peut pas offrir d'elicitation ni de tâches. Une capability le peut.
- À mesure que les agents s'appuient sur ces fonctionnalités, MCP devient l'interface principale, et REST un de ses protocoles frères.

## Pourquoi ça compte
Cet article éclaire un débat architectural central pour quiconque conçoit des interfaces destinées aux agents IA : empiler MCP sur une API existante est rapide mais plafonne ses capacités, alors qu'une conception "flow-first" permettrait à MCP d'exploiter des primitives (elicitation, tâches durables, découverte) qui n'existent pas en REST/GraphQL. C'est un signal à suivre pour la veille sur l'évolution des standards d'intégration agent-API.
