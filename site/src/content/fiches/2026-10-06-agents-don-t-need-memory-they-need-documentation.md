---
title: "Agents Don't Need Memory. They Need Documentation."
date: 2026-10-06
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fliao.gg%2Fblog%2Fagents-dont-need-memory%3Futm_source=tldrdev/1/010001a10bc87634-4b09e7a2-14ba-4b02-a3a2-0697ea970f21-000000/vgwDmAXedm6Lb5ie4uBCIYptBV4mFXGWpvgx0Tt6T7o=452"
keywords: ["mémoire agents", "documentation", "RAG", "contexte", "Markdown", "agents IA"]
theme: "IA"
tone: "opinion"
used_in: ["2026-10-06"]
---

## Résumé
L'article soutient que les plugins de « mémoire » pour agents IA, tous bâtis sur la même architecture de recherche vectorielle (RAG), résolvent en réalité le mauvais problème : ils retrouvent des fragments de conversation par similarité sémantique, sans aucune garantie qu'ils soient exacts, à jour ou pertinents pour la tâche en cours. L'auteur détaille cinq limites structurelles de ces systèmes de rappel, puis défend une alternative : une mémoire fondée sur la documentation, sous forme de fichiers Markdown qu'un agent consulte avant de travailler et met à jour après coup. Il présente son propre outil open source, Operator Memory, qu'il développe et utilise depuis plus d'un an, sans base vectorielle, sans embeddings et sans tâches de fond automatisées.

## Points clés
- Tous les plugins de mémoire actuels suivent le même schéma : parcourir les transcriptions de sessions, en extraire des « souvenirs » fragmentaires, les indexer dans une base vectorielle, puis injecter les plus proches voisins à chaque prompt (avec parfois un outil de recherche supplémentaire pour l'agent).
- Cinq failles structurelles identifiées : le rappel se fait par proximité sémantique et non par exactitude ; les fragments perdent tout le contexte environnant ; le passé est traité comme une vérité alors que le code évolue sans cesse ; l'agent ne peut pas chercher ce qu'il ignore ne pas savoir ; et le magasin de souvenirs reste impossible à auditer (quels souvenirs existent, sont obsolètes ou faux ?).
- Thèse centrale de l'auteur : le vrai besoin n'est pas de « mieux se souvenir » mais de documenter — à l'image des humains, qui ne rejouent pas une réunion passée mais s'appuient sur des comptes-rendus écrits.
- Alternative proposée : donner à l'agent un « cerveau » structuré en Markdown (instructions, spécifications, décisions, recherches, index) qu'il consulte avant d'agir et met à jour ensuite, transformant la boucle de travail de « prompt → construire → oublier » en « prompt → consulter → construire → mettre à jour ».
- L'auteur a fait évoluer une pratique personnelle (un dossier `internal/` où l'agent notait tout) en un outil nommé Operator Memory, gratuit et open source, reposant uniquement sur des documents Markdown lisibles, modifiables et partageables, sans aucun composant « boîte noire ».

## Analyse approfondie
### C'est essentiellement du RAG
L'auteur part d'un constat critique : un plugin de mémoire classique analyse les conversations, en tire environ mille fragments isolés, les range dans une base de données vectorielle, puis en rattache les cinq plus similaires à chaque nouveau prompt — et si l'agent reste perdu (ce qui arrive souvent), il doit chercher lui-même d'autres fragments. C'est, selon lui, toute l'architecture derrière l'étiquette « mémoire ». Certains outils ajoutent des raffinements : recherche mot à mot dans les anciennes transcriptions, systèmes multi-niveaux séparant mémoire courte et longue durée, démons de fond chargés de relire, fusionner ou dédupliquer les souvenirs, voire des processus dits « rêveurs » qui réécrivent la mémoire pendant la nuit, en plus de la compression continue de contexte et des re-classeurs. Pour l'auteur, chaque outil ajoute de nouvelles fonctionnalités consommatrices de tokens sur une architecture déjà bancale — ce qui explique qu'aucun ne fonctionne de façon fiable.

### Le problème du rappel
L'article égrène les limites communes à tous ces systèmes :
- **Le rappel se fait par similarité** : la recherche vectorielle mesure la proximité entre fragments dans l'espace des embeddings, rien de plus — elle ne dit pas lequel est correct, à jour, ni ce qui manque.
- **Les souvenirs sont stockés hors contexte** : un fragment RAG ne peut contenir qu'une quantité limitée d'information ; tout le reste — contexte, motivations, leçons apprises, environnement — disparaît.
- **Le passé est traité comme une vérité figée** : ces outils s'appuient sur le rappel de transcriptions ou de vecteurs, alors que la base de code change chaque jour — difficile alors de savoir si l'un des 500 fragments sur l'authentification est encore valable.
- **L'agent ne peut pas chercher ce qu'il ne sait pas** : même avec un outil de recherche à disposition, comment saurait-il quand l'utiliser, puisqu'il ignore ce qu'il ignore ?
- **Le magasin de mémoire n'est pas auditable** : avec dix mille embeddings dans une base SQLite, impossible de savoir lesquels existent, lesquels sont obsolètes, lesquels n'ont jamais été récupérés, ou lesquels sont erronés et influencent discrètement le comportement de l'agent.

L'auteur précise que ce ne sont là que cinq des nombreux problèmes rencontrés par ces plugins, tous fondés sur le même postulat : *les agents oublient, c'est le problème ; la solution est donc de mieux se souvenir, de mieux capturer, mieux indexer, mieux restituer.* Or ce n'est pas ainsi que les humains gèrent la connaissance : personne ne revisionne une réunion vieille de trois ans pour se rappeler les contraintes d'une fonctionnalité — on écrit les choses, et on s'appuie ensuite sur ces écrits. De même, la solution n'est pas de donner à l'agent un outil de recherche fouillant dix millions de tokens de conversations passées pour en reconstituer des fragments. La solution, selon l'auteur, est une mémoire fondée sur des documents. Il note qu'aujourd'hui, nombreux utilisent l'IA pour produire à toute vitesse des produits et fonctionnalités sans jamais lire ni comprendre une seule ligne de code — un contexte dans lequel la documentation devient trop souvent secondaire, alors qu'elle devrait être plus essentielle que jamais.

### La documentation plutôt que le rappel
L'idée que les agents ont besoin de contexte n'est pas nouvelle : c'est précisément ce qui a motivé la création des fichiers `AGENTS.md`, pour éviter qu'un agent aborde un projet à l'aveugle. Cela fonctionne, mais trop souvent ce fichier unique reste la seule documentation existante du projet — ce qui, selon l'auteur, est insuffisant. L'agent a besoin d'un véritable « cerveau », un espace de travail structuré où consigner, sans qu'on le lui demande, instructions, spécifications, décisions, recherches, index : la façon dont fonctionne le processus de revue de code, le compte-rendu des échanges avec l'utilisateur, ou une recherche réutilisable sur une bibliothèque externe.

Lorsqu'il travaille, l'agent peut lire ces documents pour obtenir un contexte pertinent et complet. Une fois le travail terminé — pendant que la vue d'ensemble est encore présente — il met à jour ce qui est devenu obsolète et ajoute de nouveaux documents si nécessaire. La boucle agentique passe ainsi de « prompt → construire → oublier » à « prompt → consulter → construire → mettre à jour ». La mémoire cesse d'être une base RAG greffée sur l'agent pour devenir un espace de travail que l'on peut lire, modifier et même partager.

### Mise à l'épreuve
L'auteur dit avoir identifié ce problème il y a plus d'un an, en débutant la programmation assistée par IA. Pour permettre à un agent de conserver le fil du travail entre les sessions, il a créé un dossier `internal/` où l'agent consignait tout : spécifications, plans, index. Il demandait systématiquement à l'agent de lire les documents et l'index pertinents avant de travailler, puis de les mettre à jour ensuite.

Cet ensemble de règles rudimentaires s'est progressivement transformé en un système formel, puis en un plugin nommé **Operator Memory**, qu'il utilise désormais régulièrement dans tous ses projets. Operator Memory met en œuvre ce modèle de mémoire documentaire : il fournit à l'agent un « cerveau » en Markdown où conserver les connaissances importantes — instructions, spécifications, recherches, index. Avant de travailler, l'agent consulte systématiquement ce cerveau pour les documents pertinents ; après, il le met à jour, révisant les documents obsolètes et en ajoutant de nouveaux là où c'est nécessaire.

Pas de base vectorielle, pas d'embeddings, pas de résumeurs, de curateurs, de metteurs à jour, de « rêveurs » ni d'autre démon de fond consommateur de tokens, pas de restitution en boîte noire. Avec Operator, tout est un simple document Markdown que l'on peut lire, modifier, versionner et partager avec son équipe. L'auteur affirme utiliser ce système depuis plus d'un an et propose de l'essayer : l'outil est gratuit et open source, disponible sur GitHub (dépôt aerovato/operator-memory).

## Pourquoi ça compte
Ce texte capte un débat de fond dans l'outillage des agents IA : la course aux systèmes de mémoire vectorielle masque peut-être une impasse architecturale, et le retour à une documentation structurée, lisible et versionnable pourrait s'avérer une alternative plus robuste et plus simple à auditer pour la mise en production d'agents de codage.
