---
title: "The /grill-me Skill"
date: 2026-09-09
url: "https://substack.com/redirect/86776564-7d85-4377-be4d-3b0e271f7f8d?j=eyJ1IjoiM2k5cHByIn0.jwJcWcNFB3-v9tQ21KJ2x6U6-cIPdQq2LfmnXD1TmRY"
authors: ["Matt Pocock"]
keywords: ["agents IA", "coding agent", "spécification produit", "prototypage", "prise de décision", "Claude Code"]
theme: "Tech"
tone: "tutorial"
used_in: ["2026-09-09"]
---

## Résumé
L'article présente `/grill-me`, un skill pour agent de code qui transforme une idée encore floue en une décision assumée, avant même d'écrire un plan. Le principe : l'agent interroge l'utilisateur par « rounds » de questions, chaque round couvrant tout ce qui peut déjà être demandé sans dépendre d'une réponse pas encore donnée. Le skill est "stateless" (aucun fichier écrit, aucune trace), et se distingue de deux variantes plus lourdes — `grill-with-docs` (même principe mais qui lit une base de code et garde une trace dans `CONTEXT.md`/ADR) et `wayfinder` (pour les chantiers trop gros pour une seule session). L'article insiste sur le rôle actif que doit garder l'utilisateur pendant l'interview, sous peine de ressortir avec un plan que l'agent a rédigé et que l'utilisateur a simplement validé sans réflexion.

## Points clés
- `/grill-me` s'invoque manuellement, dans une conversation neuve, et fonctionne sur n'importe quel sujet (pas seulement du code : produit, décision business, écriture).
- Les questions arrivent par vagues ("rounds") qui couvrent la "frontière" des questions posables à un instant donné, pour ne jamais présupposer une réponse non encore donnée.
- Le principal risque est la passivité : répondre "d'accord" à tout donne une illusion de travail accompli sans qu'aucune vraie décision n'ait été prise.
- Certaines questions sont "ungrillable" (non interrogeables) : quand la réponse dépend de ressentir quelque chose (ex. le rendu d'une interface), il faut arrêter l'interview, prototyper, regarder, puis revenir répondre en une ligne.
- Une session se termine quand la "frontière" de questions est vide ; une session anormalement longue (~200 questions) signale un périmètre trop large qu'il faut découper en sous-sujets.
- Le choix du modèle sous-jacent compte plus que pour la plupart des skills, car l'exercice s'appuie sur le jugement du modèle quant aux façons dont un système peut casser.

## Analyse approfondie
**Le principe du skill**
`/grill-me` part d'une idée encore vague — une fonctionnalité, une orientation produit, une décision business, un texte à écrire — et la travaille par une série de questions jusqu'à ce que l'utilisateur puisse s'engager dessus. Il n'est pas nécessaire d'arriver avec un plan déjà construit : c'est justement ce que la session doit produire. Le mécanisme fonctionne par "rounds" : à chaque tour, l'agent pose l'ensemble des questions dont les prérequis ont déjà été réglés lors des tours précédents (ce que l'auteur appelle la "frontière"). Cela évite qu'une question repose sur une réponse pas encore donnée.

Le skill est volontairement "stateless" : il n'écrit aucun fichier et ne laisse aucune trace dans le dépôt de code. Le seul résultat tangible est une version plus nette de l'idée, dans la tête de l'utilisateur.

**Installation et invocation**
Le skill s'installe via `npx skills@latest add mattpocock/skills --skill=grill-me`, puis s'invoque en tapant `/grill-me`. L'agent ne le déclenche jamais de lui-même. Il est recommandé de démarrer une conversation neuve plutôt que de l'enchaîner sur un plan déjà rédigé par un agent.

**Quand l'utiliser**
Il faut y recourir dès qu'une idée mérite d'être prise au sérieux, bien avant de savoir ce qu'elle implique concrètement. Le flou n'est pas une raison d'attendre : c'est précisément la matière que la session va digérer. À l'inverse, si l'idée peut déjà être décrite avec précision, l'interview n'apporte rien.

**Trois variantes selon le contexte**
L'auteur distingue trois "skills de grilling" selon la situation :
- `grill-me` : pour n'importe quel sujet, n'importe où — ne nécessite aucun dépôt de code et n'écrit aucun fichier.
- `grill-with-docs` : la même interview, mais avec état — elle lit le code existant pour s'y aligner et conserve ce qu'elle apprend dans un fichier `CONTEXT.md` et des ADR (Architecture Decision Records).
- `wayfinder` : pour les chantiers trop vastes pour une seule session ; il cartographie l'effort et fait tourner des sessions de "grilling" à l'intérieur de cette carte.

L'auteur recommande de désactiver le "plan mode", car celui-ci pousse l'agent à se précipiter vers la production d'un plan, ce qui va à l'encontre de l'esprit d'enquête recherché.

**Le rôle actif de l'utilisateur**
Le skill pose les questions, mais c'est l'utilisateur qui doit rester maître du périmètre — c'est le point que la plupart des gens ratent, et c'est ce qui distingue une session qui transforme une idée en décisions réelles d'une session qui produit un "n'importe quoi" à l'apparence convaincante.

Le mode d'échec typique est la passivité : répondre "d'accord, d'accord, d'accord" à quarante questions et ressortir avec un plan que l'agent a écrit et que l'on a simplement approuvé d'un signe de tête. Cela donne une impression de productivité parce que la session a été longue, mais rien n'a réellement été décidé, et le résultat affiche une certitude qu'il n'a pas gagnée.

Être actif signifie reprendre la main : contester une question posée à un niveau de précision insuffisant par rapport au besoin réel, signaler quand le périmètre dérive, répondre honnêtement "je ne sais pas" quand c'est le cas. Ce skill est conçu pour épauler un ingénieur, pas pour le remplacer : la qualité du résultat final dépend de la qualité des réponses données, pas du nombre de questions posées.

L'erreur inverse existe aussi, bien que plus rare : rester si longtemps dans l'interview que l'on n'arrive jamais au code.

**Les questions "ungrillable"**
Certaines questions se résolvent en discutant. D'autres non. Des questions comme "un long formulaire ou trois pages ?" ou "quel ressenti doit avoir cette interaction ?" sont dites "ungrillable" : elles ont besoin d'un support concret sur lequel réagir. Quand on tombe sur ce type de question, il faut arrêter l'interview, construire une version jetable avec un outil de prototypage, la regarder, puis revenir répondre en une seule ligne.

Essayer de résoudre une question "ungrillable" par la seule discussion est justement ce qui fait gonfler démesurément une session : l'agent reformule sans cesse, l'utilisateur devine sans cesse, et le périmètre s'étend pour combler l'incertitude.

**Signes qu'une session s'est bien passée**
- L'utilisateur est en désaccord sur au moins un point — une session sans aucune contestation de sa part est une session qui n'était pas nécessaire.
- Les questions arrivent en quelques rounds distincts plutôt qu'en un long flux continu, et les rounds suivants s'appuient clairement sur ce qui a été dit avant.
- On finit à un endroit inattendu, parce qu'une question a mis au jour une décision qui était prise implicitement.
- À la fin, on est capable de justifier chaque choix devant quelqu'un qui n'a pas assisté à la session.

**Foire aux questions**
*Combien de questions dois-je attendre, et comment sais-je que c'est fini ?*
Il faut compter les rounds, pas les questions. Quarante-six questions réparties sur quatre rounds constituent une session ordinaire. Elle se termine quand la "frontière" est vide : toutes les branches ont été explorées, rien n'est resté implicitement supposé.

*L'agent m'a posé deux cents questions, qu'est-ce qui a mal tourné ?*
Généralement, le périmètre était trop large. Il faut demander à l'agent de découper le travail en sous-parties plus petites, puis "griller" chacune séparément. Les sessions très longues finissent aussi par dériver dans ce que l'auteur appelle la "dumb zone" (zone d'abêtissement) : la fenêtre de contexte devient si pleine que la qualité des questions se dégrade.

*Puis-je revenir à une question à la fois ?*
Oui, en ajoutant une instruction correspondante dans son `CLAUDE.md` global.

*Et si je ne connais vraiment pas la réponse ?*
Il faut le dire. "Je ne sais pas" est une réponse valable, et une question à laquelle on ne peut pas répondre est généralement le signe qu'il faut prototyper plutôt que deviner.

*Dois-je démarrer une session neuve avant d'écrire la spécification ?*
Non. La valeur de la session tient justement au contexte qui vient d'être construit. Il faut transmettre cette même conversation directement à l'étape de rédaction de la spécification ("to-spec").

*Le choix du modèle a-t-il une importance ?*
Plus que pour la plupart des skills. L'exercice de "grilling" s'appuie sur la capacité propre du modèle à anticiper la façon dont un système peut se casser : il faut donc lui donner le meilleur modèle disponible. L'implémentation, elle, dépend surtout du contexte fourni et tolère un modèle moins coûteux.

**Portabilité et articulation avec les autres outils**
`grill-me` est conçu comme un outil autonome, utilisable n'importe où, sur n'importe quel sujet. Son caractère "stateless" est précisément ce qui le rend portable : pas besoin de dépôt de code, de workspace, de configuration, ni même que le sujet traité soit lié au logiciel. Des utilisateurs l'appliquent à des décisions business, à de l'écriture, ou à toute idée qui "ne tient pas en place" dans leur tête.

Cette portabilité est justement ce qui le différencie de `grill-with-docs`, qui fait tourner la même interview mais en lisant une base de code pour s'y aligner et en conservant ce qu'il apprend dans `CONTEXT.md` et des ADR. Les deux s'appuient sur le même mécanisme de base ("grilling"), mais `grill-me` en est la porte d'entrée invoquée directement par l'utilisateur, sans rien emporter avec lui.

Si l'idée grillée s'avère finalement être un projet logiciel, il est possible de transmettre la même conversation à l'outil `to-spec` et de poursuivre vers la phase de construction — une option parmi d'autres, pas la finalité du skill. En cas de doute sur le flux à emprunter, un outil nommé `ask-matt` est censé orienter l'utilisateur vers le bon choix.

## Pourquoi ça compte
Cet article illustre une tendance de fond dans l'outillage des agents de code : au-delà de la génération de code, on voit émerger des skills dédiés à la clarification et à la prise de décision en amont, avec un souci explicite d'éviter la fausse certitude que peut donner un agent trop consensuel — un point de vigilance pertinent pour quiconque conçoit ou utilise des workflows d'agents IA.
