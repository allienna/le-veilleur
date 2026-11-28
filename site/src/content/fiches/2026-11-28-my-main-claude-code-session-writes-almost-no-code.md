---
title: "My main Claude Code session writes almost no code"
date: 2026-11-28
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fjurajb.dev%2Fmain-session-manager%2F%3Futm_source=tldrdev/1/010001a21cf08720-a1a3e8d5-31b1-49de-837d-f0489d0b4604-000000/dSAMmCJzCwgYV4INrXe4vUWe7DKjmKkG3WdyoYAmhH4=452"
authors: ["Juraj B."]
keywords: ["Claude Code", "agents IA", "orchestration multi-agents", "git worktree", "automatisation du développement", "revue de code"]
theme: "IA"
tone: "opinion"
used_in: ["2026-11-28"]
---

## Résumé
L'auteur décrit comment sa session principale de Claude Code a cessé d'écrire du code pour devenir un véritable "manager" : elle planifie le travail, briefe d'autres agents Claude Code, vérifie leurs livrables, fusionne et déploie. Résultat sur 5 jours : 37 bêtas TestFlight (contre 9 les 5 jours précédents), 84 agents lancés et 303 messages reçus, alors que seulement 2 % des actions du manager sont des modifications de fichiers. Le système repose sur un fichier Markdown de 129 lignes (une "skill"), enrichi d'une règle chaque fois qu'un incident survient, et sur des agents isolés dans des git worktrees séparés plutôt que sur de simples subagents. L'auteur partage aussi les détails pratiques et les pièges rencontrés avec Herdr, l'outil utilisé pour orchestrer les agents.

## Points clés
- La session principale ne code presque plus : elle planifie, briefe les agents, vérifie leurs preuves (commits, tests, vidéo, build Release) et décide du déploiement.
- Gains de productivité spectaculaires : 37 bêtas en 5 jours (builds 12 à 48) contre 9 sur la période précédente, avec 84 agents démarrés et 303 messages échangés.
- Le "manager" tient dans un seul fichier Markdown de 129 lignes, qui s'enrichit d'une règle à chaque échec rencontré.
- Chaque fonctionnalité suit un pipeline fixe : plan validé → build avec tests et vidéo de preuve → auto-revue via `/code-review` + revue croisée par GPT → reproduction et correction des vrais problèmes → vérification et déploiement par le manager.
- Des agents séparés dans des git worktrees distincts (via l'outil Herdr et son CLI `hc`) sont préférés aux subagents pour le travail long, car ils persistent indépendamment du manager et gardent le contexte de ce dernier léger.
- Plusieurs pièges pratiques sont documentés (différence entre `hc send` et `hc keys`, nécessité du Remote Control pour les approbations, portée limitée du nettoyage des agents).

## Analyse approfondie
### Ma session Claude Code principale n'écrit presque aucun code

Depuis une semaine, ma session Claude Code principale est devenue un manager. Elle planifie le travail, briefe d'autres agents Claude Code, vérifie ce qu'ils livrent, fusionne et déploie. Elle n'écrit presque aucun code elle-même.

- **37 bêtas TestFlight** de Note to Self en **5 jours**, des builds 12 à 48.
- Durant les 5 jours précédents, j'en avais livré **9**.
- Le manager a démarré **84 agents**, qui lui ont envoyé **303 messages**.

Le manager tout entier tient dans un seul fichier Markdown de 129 lignes.

#### Pourquoi votre session principale ne devrait pas écrire le code

Quand votre session principale écrit le code, c'est vous qui êtes le manager. Vous la regardez travailler. Vous vérifiez chaque "c'est fait", vous fusionnez, vous déployez et vous passez à la suite. Vous répétez les mêmes règles à chaque nouvelle session, car chacune repart de zéro.

Le manager prend ce rôle à sa charge. Il ne fait pas confiance à un simple "c'est fait" : il vérifie lui-même les commits, les tests, la vidéo de preuve et un build Release. Chaque règle que je lui donne est intégrée au brief que chaque agent suivant lira, donc je n'ai à la dire qu'une seule fois.

Mon travail consiste à approuver les plans et à essayer les bêtas sur mon téléphone.

Seulement 44 des 2 057 appels d'outils du manager durant ces 5 jours étaient des modifications de fichiers, soit environ 2 %, et la plupart concernaient des briefs et des notes. Mes autres sessions se situent à 11 %. Ce n'est pas totalement pur : quelques fois, il a lui-même corrigé un build Release ou un fichier de test.

#### L'organisation mise en place

Une session Claude Code est le manager.
Chaque fonctionnalité est confiée à son propre agent Claude Code, dans son propre git worktree, les agents tournant en parallèle là où deux tâches ne peuvent pas se gêner.
Les agents s'exécutent dans Herdr, une application terminal pour agents de codage.
Son CLI `hc` démarre les agents, fait passer les messages entre eux et attend leurs résultats, et `hc --skill` affiche un manuel qui enseigne tout cela au manager.

Chaque fonctionnalité suit le même pipeline :

1. L'agent écrit un plan. Je l'approuve.
2. Il construit, avec des tests et une vidéo de simulateur comme preuve, en committant chaque bloc logique.
3. Il relit son propre diff avec `/code-review`, et GPT le relit comme second modèle.
4. Il reproduit d'abord chaque problème signalé, puis corrige ceux qui sont réels.
5. Le manager vérifie la preuve, fusionne et déploie une bêta TestFlight.

#### Pourquoi des agents séparés plutôt que des subagents

Les subagents sont parfaits pour une question rapide et bornée. Une fonctionnalité qui demande une heure de construction, de tests et de revue a besoin de plus :

- Une session complète peut démarrer ses propres subagents, elle peut donc exécuter `/code-review` comme je le ferais moi-même.
- Je peux ouvrir le terminal de n'importe quel agent, le lire, et y taper directement.
- Le manager ne voit que de courts messages ("plan prêt", "commité", "terminé"), ce qui garde son contexte léger sur une file de 20 fonctionnalités.
- Les agents continuent de tourner quand le manager redémarre ou se compacte, et je peux en arrêter un sans toucher aux autres.

Le coût, c'est la plomberie : une application terminal, des messages entre sessions, et le nettoyage des terminaux et des worktrees.

#### Chaque échec est devenu une règle

La skill a eu 9 commits durant ses 2 premiers jours, et presque chacun venait de quelque chose qui avait cassé :

- Des agents restaient bloqués sur des invites de permission que personne ne surveillait. Désormais, chaque agent tourne en mode automatique.
- Des agents exécutaient toute la suite de tests UI pour un changement d'une ligne. Désormais, ils n'exécutent que les classes de tests concernées.
- Des agents ne construisaient qu'en Debug, et une bêta Release a échoué à l'archivage. Désormais, ils construisent en Release avant de signaler que c'est terminé.
- Le manager a fusionné trois fonctionnalités sans bêta. Désormais, une bêta suit chaque fonctionnalité, et une bêta échouée bloque la file.
- Une fonctionnalité de synchronisation a tourné une journée entière, avec environ 35 remarques de revue, la plupart causées par les propres corrections antérieures de la fonctionnalité. Désormais, le travail fortement comportemental démarre avec une spécification, et les agents s'arrêtent pour demander quand une correction nécessite une nouvelle mécanique.

Le système s'améliore chaque fois que quelque chose casse, car la correction atterrit dans le brief que chaque agent suivant lira.

#### Trois détails sur Herdr qui m'ont coûté du temps

- `hc send` délivre un message de chat à un autre agent, donc une commande slash envoyée ainsi ne s'exécute pas. Les commandes slash ont besoin de `hc keys`.
- Quand le mode automatique d'un agent bloque sur quelque chose, une approbation relayée par le manager ne compte pas comme mon consentement. La solution est le Remote Control sur ce terminal, pour que j'approuve moi-même depuis mon téléphone.
- Le manager ne peut nettoyer que les agents qu'il a lui-même démarrés, jamais mes propres terminaux.

#### Faites-la vôtre

La skill est du Markdown pur, donc la modifier revient à éditer une phrase. La mienne a des règles iOS (simulateurs, builds Release, TestFlight), et la vôtre aura les siennes. Remplacez la bêta par un déploiement, la vidéo de simulateur par une capture d'écran, GPT par le second relecteur de votre choix. Chaque fois que quelque chose casse, ajoutez une ligne.

Ou commencez plus petit que ma skill. Démarrez Claude Code dans une session Herdr et collez ceci :

> Tu es le manager et tu n'écris aucun code. Lance `hc --skill` et suis-le. Pour chaque élément de ma liste, démarre un agent Claude Code en mode automatique, dans son propre git worktree. Chacun planifie d'abord et attend mon accord. Quand l'un est terminé, vérifie-le, fusionne-le, démarre le suivant.

La skill complète, avec ses modèles et le script de revue, est disponible sur GitHub. Forkez-la, supprimez ce qui ne convient pas à votre projet, et ajoutez votre première règle la première fois que quelque chose casse.

## Pourquoi ça compte
Ce témoignage illustre un motif émergent dans l'usage des agents de codage : le passage d'une IA "qui code" à une IA "qui orchestre d'autres IA", avec des gains de cadence mesurables. C'est un signal concret à suivre pour quiconque conçoit des workflows multi-agents avec Claude Code ou des outils équivalents.
