---
title: "Claude Code skills for teams: what to move out of CLAUDE.md"
date: 2026-10-29
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fdev.to%2Faiworkspacebuilder%2Fclaude-code-skills-for-teams-what-to-move-out-of-claudemd-4f6o%3Futm_source=tldrdev/1/010001a18238e1f8-ddd7e87c-e55b-4c81-83eb-9084da787664-000000/dxgcDt00DNp4PB32JAAA5vw5rj4JDCHbkbrK7F4R8ek=452"
keywords: ["Claude Code", "CLAUDE.md", "skills", "agents IA", "organisation d'équipe"]
theme: "Software"
tone: "tutorial"
used_in: ["2026-10-29"]
---

## Résumé
L'article explique comment un fichier CLAUDE.md finit par devenir trop long à force d'accumuler des procédures ponctuelles (checklist de release, migrations, conventions d'API), ce qui nuit à la fiabilité de l'agent puisque tout le fichier est chargé à chaque session. La solution proposée est de déplacer ce contenu occasionnel vers des « skills » : des dossiers contenant un fichier SKILL.md, chargés uniquement quand c'est pertinent plutôt que systématiquement. L'article détaille la structure d'un skill, les règles de priorité entre skills de projet/personnels/entreprise, et les champs de frontmatter qui contrôlent qui peut déclencher un skill (l'utilisateur, Claude automatiquement, ou les deux).

## Points clés
- CLAUDE.md doit rester court (moins de 200 lignes recommandées) et ne contenir que ce qui est utile à *chaque* session (commandes de build/test, conventions générales, contexte produit).
- Les skills sont des dossiers `.claude/skills/<nom>/SKILL.md` chargés à la demande ; ils remplacent et étendent les anciennes commandes custom (`.claude/commands/`).
- Trois emplacements de skills existent : projet (committé, partagé par l'équipe), personnel (`~/.claude/skills/`), et entreprise (déployé via les paramètres managés) — en cas de conflit de nom, entreprise > personnel > projet.
- Deux champs de frontmatter sont cruciaux pour une équipe : `disable-model-invocation: true` (seul un humain peut lancer le skill, ex. déploiement) et `user-invocable: false` (seul Claude peut l'invoquer automatiquement, ex. connaissance de fond).
- Le champ `allowed-tools` d'un skill partagé mérite une revue en pull request car il peut accorder des permissions larges à l'agent sans confirmation.
- Bonnes pratiques : description concise (limite de 1536 caractères affichés), fichier SKILL.md de moins de 500 lignes, et renvoi du contenu volumineux vers des fichiers annexes dans le dossier du skill.

## Analyse approfondie
L'article part d'un constat très concret : dans une équipe, chaque contributeur ajoute « raisonnablement » une section à CLAUDE.md (checklist de release, étapes de migration de base de données, règles d'écriture d'endpoints API), et la somme de ces ajouts légitimes rend le fichier trop long pour être suivi de manière fiable par l'agent, puisque Claude Code charge l'intégralité du fichier à chaque session.

La distinction centrale proposée est la suivante : CLAUDE.md doit contenir ce dont l'agent a besoin *à chaque session* (commandes de build/test, conventions transverses, description du produit, critères de refus systématiques en revue de code), tandis qu'un skill encode une procédure dont on a besoin seulement *pour un type de tâche donné* (checklist de release, étapes de migration, écriture d'un nouvel endpoint, débogage d'une intégration de paiement spécifique).

Un skill est un dossier avec un fichier SKILL.md composé de deux parties : un frontmatter qui décrit ce que fait le skill et quand l'utiliser, et le corps qui contient les instructions que Claude suit lors de l'exécution. Le nom du dossier (ou le champ `name`) devient une commande tapable (`/add-migration` par exemple). Tant que le skill n'est pas déclenché, seule sa description réside en contexte — pas les instructions elles-mêmes — ce qui limite le coût en tokens.

L'article précise que les anciennes commandes custom dans `.claude/commands/` continuent de fonctionner ; les skills en sont une extension, ajoutant un dossier pour des fichiers de support et un contrôle plus fin de qui peut les exécuter.

Trois emplacements de stockage déterminent la portée d'un skill :
- **Projet** : `.claude/skills/<nom>/SKILL.md` dans le dépôt, committé pour que toute l'équipe en bénéficie — l'option privilégiée pour un usage d'équipe.
- **Personnel** : `~/.claude/skills/<nom>/SKILL.md`, disponible sur toutes les sessions de la machine de l'utilisateur.
- **Entreprise** : déployé via les paramètres managés à toute l'organisation.

Un piège signalé : en cas de conflit de nom entre skills, l'ordre de priorité est entreprise > personnel > projet. Ainsi, un développeur ayant un vieux skill personnel nommé `deploy` verra sa version s'exécuter à la place de celle committée par l'équipe en tapant `/deploy`. La recommandation est donc de nommer les skills partagés de façon spécifique au dépôt (ex. `deploy-web`) pour éviter les collisions.

Dans un monorepo, un paquet peut avoir son propre dossier `.claude/skills/`, chargé dès la première lecture ou édition d'un fichier de ce paquet par Claude Code. Si la racine et `apps/web` ont chacun un skill `deploy`, les deux restent disponibles, et `/apps/web:deploy` cible spécifiquement celui du paquet.

Deux champs de frontmatter sont présentés comme les plus importants pour un usage en équipe : en comportement par défaut, l'utilisateur et Claude peuvent tous deux lancer le skill. Avec `disable-model-invocation: true`, seul un humain peut le déclencher — Claude ne peut pas décider de son propre chef de l'exécuter. Avec `user-invocable: false`, c'est l'inverse : seul Claude peut l'invoquer automatiquement, et ce n'est pas une commande que quelqu'un taperait.

L'article recommande d'appliquer `disable-model-invocation: true` à tout skill ayant des effets de bord (déploiement, publication de release, message envoyé à un canal), citant la documentation officielle qui met en garde : on ne veut pas que Claude décide de déployer simplement parce que le code « a l'air prêt ». Avec ce champ activé, même la description du skill n'est pas chargée en contexte, ce qui signifie qu'il ne coûte rien jusqu'à ce que quelqu'un tape explicitement son nom.

À l'inverse, `user-invocable: false` convient à des connaissances de fond, comme le fonctionnement d'un système legacy : Claude doit le savoir quand c'est pertinent, mais ce n'est pas une commande que quelqu'un taperait.

L'article propose ensuite trois catégories concrètes de skills à committer en premier :
1. **La release** — les étapes exactes que l'équipe suit pour livrer, dans l'ordre, avec les vérifications entre chaque étape, et `disable-model-invocation: true` pour que seul un humain puisse la lancer.
2. **La tâche que tout le monde rate légèrement** — chaque équipe a la sienne (une migration, un nouvel endpoint API, un feature flag) : écrire les étapes une seule fois, en incluant celle que les gens oublient habituellement, et laisser Claude pouvoir l'invoquer automatiquement quand une demande correspond.
3. **Les conventions propres à un domaine** — règles de conception d'API, format d'erreur, nommage des événements : du contenu de référence que Claude applique en parallèle du travail plutôt que comme une suite d'étapes, pertinent seulement pour qui travaille dans ce domaine précis.

Un autre point d'attention porte sur le champ `allowed-tools`, qui permet à un skill de lister les outils que Claude peut utiliser sans demander confirmation durant le tour où le skill s'exécute. Utile pour un script de release, mais la documentation prévient qu'un skill committé dans un dépôt peut s'octroyer un accès large, et ce champ s'applique même lors d'une exécution non interactive dans un dossier jamais approuvé auparavant — il est donc recommandé de le revoir en pull request comme tout autre changement de permission.

Enfin, l'article conseille de garder la description précise et le fichier court : Claude décide quand charger un skill à partir de sa description, et la liste des skills tronque cette description à 1536 caractères, d'où l'intérêt de placer le cas d'usage principal en premier. La documentation recommande de garder SKILL.md sous les 500 lignes et de déplacer le contenu de référence volumineux dans des fichiers séparés au sein du dossier du skill, chargés seulement en cas de besoin.

En conclusion pratique, l'auteur invite le lecteur à relire son CLAUDE.md, repérer chaque section qui ne concerne qu'un type de tâche précis, et à la transformer en skill — puis à vérifier que le fichier lu à chaque session est devenu plus court. Un commentaire de lecteur en fin d'article confirme que cette distinction (instructions permanentes vs workflows ponctuels) n'est pas intuitive au premier abord, mais s'avère nécessaire à mesure qu'un projet grossit.

## Pourquoi ça compte
Ce contenu est pertinent pour une veille sur les outils d'agents IA en contexte professionnel : il formalise une pratique d'hygiène de configuration (CLAUDE.md vs skills) qui devient un enjeu réel dès qu'une équipe, et non un seul développeur, adopte Claude Code au quotidien.
