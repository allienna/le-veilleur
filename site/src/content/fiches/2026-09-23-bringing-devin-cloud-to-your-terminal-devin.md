---
title: "Bringing Devin Cloud to your terminal | Devin"
date: 2026-09-23
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fdevin.ai%2Fblog%2Fdevin-cloud-in-your-terminal%3Futm_source=tldrai/1/010001a0c94ac023-ce61b09e-2653-4bb7-99c9-33f88214b103-000000/W7LB8AdoVn-s2_xTBBPnZJK1Z_gcSFI1oc_svQ2rLMI=452"
keywords: ["Devin", "agent IA", "CLI", "cloud", "terminal", "SSH"]
theme: "IA"
tone: "news"
used_in: ["2026-09-23"]
---

## Résumé
Devin, l'agent IA de développement logiciel, annonce l'arrivée de « Devin Cloud » directement dans son interface en ligne de commande (CLI). Les utilisateurs peuvent désormais créer, piloter, reprendre et observer leurs sessions Devin Cloud depuis leur terminal via les commandes `devin --cloud` ou `/cloud`. La fonctionnalité `/handoff` permet de transférer instantanément une tâche vers une VM cloud dédiée, tout en gardant la possibilité de suivre et piloter le travail depuis le terminal. Un accès SSH complet aux VM Devin est également introduit, et l'offre est gratuite (sessions SWE-2) jusqu'au 8 octobre.

## Points clés
- Nouvelles commandes `devin --cloud` et `/cloud` pour gérer des sessions Devin Cloud depuis le terminal.
- `/handoff` transfère une tâche vers une VM cloud dédiée sans changer de workflow, avec possibilité de fermer son ordinateur.
- Les sessions cloud survivent à la fermeture du terminal ; elles peuvent être rouvertes via `/open [web|desktop]` ou `devin --cloud --resume`.
- Accès SSH complet aux VM Devin (`devin ssh`) pour éditer le code, lancer des serveurs de dev et transférer des fichiers via scp.
- `/handoff` peut aussi ramener le travail en local en récupérant la branche de pull request de la session.
- Essai gratuit de sessions SWE-2 jusqu'au 8 octobre via une simple installation en une ligne de commande.

## Analyse approfondie
Présentation de Devin Cloud dans votre terminal. À partir d'aujourd'hui, vous pouvez créer, piloter, reprendre et observer vos sessions Devin Cloud directement depuis votre terminal préféré. Utilisez simplement `devin --cloud` ou `/cloud`.

### Devin CLI rencontre Devin Cloud

Devin CLI est parfait pour l'itération locale rapide avec vos modèles préférés, mais parfois vous voulez confier les détails d'implémentation à un agent. Avec `/handoff`, vous pouvez désormais transférer instantanément n'importe quelle tâche à Devin pour continuer à itérer dessus avec sa propre VM cloud.

Fait important, déléguer une tâche ne nécessite pas de changer de workflow : une fois le travail confié à Devin, vous pouvez continuer à observer et piloter la progression directement depuis votre terminal, comme si Devin travaillait en local — tout en ayant la liberté de fermer votre ordinateur portable et de laisser Devin continuer en arrière-plan.

### Reprenez le travail, où que vous soyez

Les sessions cloud survivent au terminal qui les a lancées.

Lorsqu'un terminal n'est pas la bonne vue, `/open [web]` ouvre la session en cours dans l'application web, et `/open desktop` l'ouvre dans Devin Desktop. Utilisez le terminal pour piloter, et le navigateur lorsque vous voulez regarder le bureau de Devin ou consulter un enregistrement.

```
/open [web|desktop]
```
Et vous pouvez revenir au terminal quand vous le souhaitez. `devin --cloud --resume` rouvre n'importe quelle session cloud directement dans le terminal.

```
devin --cloud --resume https://app.devin.ai/sessions/…
```

## Accès SSH complet

Lorsque vous confiez du travail au cloud, Devin met en place un environnement de développement complet sur une VM dédiée. Nous lançons désormais un support SSH complet pour les VM Devin, vous permettant d'utiliser l'environnement de développement de Devin comme le vôtre. Avec un simple `devin ssh`, vous pouvez vous connecter instantanément à la VM distante et :

- Explorer et éditer le code source directement dans Devin Desktop
- Lancer des serveurs de développement et rediriger des ports pour tester interactivement le travail de Devin
- Copier des fichiers entre la VM et votre machine via scp

## Ramenez le travail à la `$HOME`

Lorsque vous voulez peaufiner les derniers détails en local, vous pouvez également exécuter `/handoff` dans une session cloud pour ramener le travail en local : cela récupère la branche de pull request de la session, fait basculer votre checkout Git sur cette branche, et démarre une session locale sur ce code.

## Essayez Devin dans votre terminal dès aujourd'hui

Nous rendons encore plus simple l'essai de Devin Cloud depuis votre terminal, avec des sessions SWE-2 gratuites disponibles jusqu'au 8 octobre.

Il suffit d'installer Devin CLI et d'exécuter `devin --cloud` pour commencer :

`curl -fsSL https://cli.devin.ai/install.sh | bash`
En savoir plus dans la documentation.

## Pourquoi ça compte
Cette annonce illustre la convergence rapide entre agents IA de codage locaux et infrastructures cloud, une tendance clé pour la veille sur les outils de développement assistés par IA et l'évolution des workflows d'ingénierie logicielle.
