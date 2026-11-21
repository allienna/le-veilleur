---
title: "Coding harnesses are cheap to swap now. Model behavior isn't. | The Davenporter"
date: 2026-11-21
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fdavenporter.com%2Fwritings%2Fagent-harnesses-cheap-to-swap-behavior-isnt%3Futm_source=tldrdev/1/010001a1f8e20cf0-04c1a8d2-b096-40a7-9fd6-0fd535581342-000000/mCwyACLJGv09tRV34Gcp2VfCRVq1hLemRZekUZypRW0=452"
authors: ["The Davenporter"]
keywords: ["agents de codage", "harnais IA", "MCP", "comportement des modèles", "orchestration"]
theme: "Software"
tone: "opinion"
used_in: ["2026-11-21"]
---

## Résumé
L'auteur du blog *The Davenporter* soutient que les harnais d'agents de codage (orchestration, boucles d'édition, parsing d'outils) sont devenus interchangeables à coût quasi nul, car les grands laboratoires d'IA (Anthropic, Google, OpenAI) ont absorbé cette plomberie directement dans leurs API de modèles. En revanche, le comportement des modèles eux-mêmes reste profondément différent d'un modèle à l'autre, même sous des règles et des outils identiques, comme le montrent ses tests comparant Gemini et Claude Opus dans Antigravity. Il en conclut que la valeur d'ingénierie durable réside désormais dans les politiques de sécurité, le code et les outils à double accès, la gestion de la mémoire/contexte en fichiers ouverts, et les boucles d'évaluation — pas dans la plomberie d'orchestration elle-même.

## Points clés
- Les API de modèles (Claude Managed Agents, Gemini Interactions API, OpenAI Agents API) ont absorbé la boucle centrale des agents de codage, rendant la majeure partie du code "harnais" obsolète.
- Des standards ouverts (AGENTS.md, SKILL.md, MCP) uniformisent le contrat externe entre harnais concurrents (Antigravity, Claude Code, Codex), rendant leur remplacement quasi gratuit.
- OpenAI illustre cette bascule : fermeture de l'Assistants API puis lancement, deux semaines plus tard, de l'Agents API directement issue de son harnais interne Codex.
- Malgré des harnais et des règles identiques, les modèles adoptent des comportements très différents (usage des outils, respect des consignes, habitudes d'UI) : Gemini suit scrupuleusement les instructions, Opus s'appuie sur ses propres réflexes par défaut.
- Ce qui reste à "posséder" : politiques de sécurité hors prompt, code et outils à double accès (MCP + CLI), mémoire/contexte en fichiers ouverts, et hooks d'évaluation/vérification.
- Un incident concret (facture dépassant 120 $ chez FreightFloor à cause d'un compteur de dépense obsolète) illustre la nécessité de garde-fous indépendants du comportement du modèle.

## Analyse approfondie
Les équipes qui débattent encore de frameworks et de boucles personnalisées passent à côté de l'essentiel : il est désormais quasiment gratuit de changer de "harnais" (harness) agentique. Dans les agents de codage en particulier, Anthropic, Google et OpenAI ont tous intégré la boucle centrale directement dans leurs API (Claude Managed Agents, Gemini Interactions API, OpenAI Agents API). Des spécifications ouvertes comme AGENTS.md, SKILL.md et MCP ont standardisé le contrat externe entre harnais concurrents (Antigravity, Claude Code, Codex). Même en jetant tout son pipeline pour le reconstruire sur un autre SDK, un agent de codage peut réécrire cette plomberie en une après-midi.

Le vrai problème, c'est le comportement du modèle.

Ce que la plupart des équipes appelaient leur "harnais" de codage est aujourd'hui en grande partie du code mort, absorbé dans l'API du modèle.

### Pourquoi les API de modèles ont avalé le harnais de codage initial
Les premières API textuelles étaient sans état (stateless) : des tokens entraient, des tokens sortaient. Tout ce qui transformait un modèle en agent de codage vivait dans le code "glue" interne de chaque équipe — tableaux d'historique de conversation, boucles d'édition-vérification faites main, parseurs de diff par regex, logique de relance des appels d'outils en JSON, cache de préfixe géré manuellement, wrappers de recherche de dépôt, et boucles génériques du type `while tool_call:`.

Ce n'était pas un avantage défendable (*a moat*).

Chaque laboratoire majeur a absorbé cette couche directement dans son API : état de raisonnement natif (*thinking*), cache implicite, sorties structurées, recherche de code et de fichiers intégrée, état côté serveur, et sandboxes d'exécution distants — tout est passé côté serveur.

OpenAI a donné l'indice le plus clair de cette dynamique : l'entreprise a fermé l'ancienne Assistants API et lancé l'Agents API deux semaines plus tard, transformant son harnais interne Codex en un simple endpoint cloud.

Pourquoi tuer Assistants et sortir Agents immédiatement après ? Assistants était un pari précoce, conçu avant que les laboratoires ne fassent tourner de vrais agents de codage à grande échelle. Les API d'agents qui ont survécu (les agents distants de l'Interactions API, l'Agents API d'OpenAI, et les Claude Managed Agents) ont été directement extraites de harnais de codage testés au combat.

| Couche du harnais de codage historique | Équivalent dans l'API du modèle | Statut dans le code utilisateur |
|---|---|---|
| Boucles de prompt ReAct / édition-vérification | Raisonnement natif + état de pensée préservé | Code mort |
| Parseurs de diff par regex & relances d'appels d'outils | Décodage contraint / Sorties structurées | Code mort |
| Historique de conversation & découpage manuel du cache de préfixe | État côté serveur + cache implicite | Majoritairement absorbé |
| Recherche de dépôt et glue de schéma faites main | Recherche intégrée + MCP distant | Majoritairement absorbé |
| Sandboxes cloud génériques en `while tool_call:` | Sandboxes de codage hébergées dans l'API | Absorbé pour les exécutions cloud |
| Politiques, code, mémoires & évaluation | Absent de l'API du modèle | Ce que vous possédez encore |

Là où la plateforme n'est que glue et boucles, il faut considérer que les API de modèles ont déjà absorbé ce comportement, ou l'absorberont bientôt. Ce qui reste propre à chaque équipe : les politiques, le code, les mémoires et l'évaluation. Le reste est interchangeable.

### Harnais interchangeables, comportements de modèles différents
Cela ressemble à Kubernetes ou aux conteneurs, mais il y a une différence majeure. Il y a environ 10 ans, la CNCF et Kubernetes voyaient le jour. Cette année, c'est l'Agentic AI Foundation. Les standards améliorent l'écosystème MCP et des plugins, rendant le "harnais" réellement interchangeable (*plug and play*). Mais contrairement aux conteneurs, où le matériel sous-jacent se comporte aussi de façon similaire, les modèles se comportent très différemment (un peu comme ARM face à Intel : ils acceptent la même entrée mais produisent des sorties différentes).

Une série d'exemples récents tirés de la propre machine de l'auteur illustre ce point.

Premièrement, mêmes règles, habitudes d'outils opposées. Lors d'un audit de Gemini 4 Argon et de Claude Opus 5.5 dans Antigravity, changer de modèle n'a demandé aucune modification de code, sous les mêmes règles AGENTS.md et le même plugin ast-graph. Argon lisait les schémas d'outils et interrogeait le graphe dans la plupart des sessions. Opus ignorait complètement les schémas et restait en bash à lancer des `grep`, sauf dans FreightFloor, où un script d'une ligne lui permettait d'appeler le graphe depuis le shell.

Deuxièmement, les règles se dégradent au fil des générations de modèles. L'auteur a observé l'effet inverse avec ses règles d'interface utilisateur (score complet dans ses notes). D'anciennes règles d'UI écrites pour des modèles Flash plus petits traînaient encore dans ses dépôts. Opus a ignoré le menu de compétences (*skills*) et construit des mises en page propres à partir de ses propres valeurs par défaut. Gemini, lui, a lu scrupuleusement chaque compétence correspondante et produit fidèlement des tableaux de bord encombrés et brunâtres, couverts de pastilles statiques. Supprimer 95 % de la configuration d'agent a immédiatement corrigé la construction des interfaces.

Troisièmement, même après ce nettoyage, la reconstruction d'une interface pour un projecteur de 10 pieds a montré que l'écart reste bien réel. Gemini a ouvert une compétence intégrée de guidage web dès la première étape, tandis qu'Opus ne l'a jamais ouverte. Il a construit des menus déroulants de type bureau jusqu'à ce qu'on lui rappelle qu'un projecteur n'est pas un navigateur de bureau. Changer de modèle, ou même monter en gamme chez un même fournisseur, modifie encore les habitudes de codage de l'agent.

### Ce qu'il reste réellement à posséder dans un harnais de codage
L'auteur a déjà écrit que 100 % des développeurs devraient construire des outils pour améliorer leur flux de travail plutôt que de corriger à la main des sorties défectueuses.

Posséder son flux de travail ne signifie pas maintenir de la glue d'orchestration banalisée. Écrire aujourd'hui une boucle d'édition personnalisée ou un wrapper de relance d'outils, c'est comme écrire un ordonnanceur de conteneurs sur mesure il y a dix ans.

En réalité, les parties d'un harnais de codage qui valent la peine d'être possédées sont les limites qu'une API de modèle ne peut pas imposer depuis l'intérieur de ses propres poids, ainsi que les boucles de feedback qui détectent la dérive comportementale lors des changements de modèle.

Dans les propres dépôts de l'auteur, quatre couches gardent toute leur valeur :

- **Les politiques en dehors du prompt** : sandboxes de commandes au niveau OS, règles d'approbation "fail closed" pour le shell et l'écriture de fichiers, et de véritables plafonds de dépense ou de tokens. Sur FreightFloor, un compteur de dépense obsolète combiné à du trafic de crawlers a fait grimper la facture de la semaine de lancement à plus de 120 $ avant qu'elle ne soit vérifiée. Les garde-fous ne comptent que lorsqu'ils ne dépendent pas du bon comportement du modèle.
- **Le code et les outils à double accès** : les *worktrees* git pour les branches parallèles, les frontières des dépôts privés, et le fait d'exposer les outils de développement clés à la fois en MCP et en CLI, pour que des modèles aux habitudes différentes puissent y accéder.
- **Les mémoires et le contexte du dépôt** : conserver ses règles de codage, ses compétences et son contexte de projet dans des fichiers ouverts et simples (AGENTS.md et SKILL.md), et élaguer les instructions obsolètes avant qu'elles n'empoisonnent les modèles plus récents.
- **Les points de vérification et d'évaluation** : des contrôles d'arrêt qui bloquent la finalisation quand les tests échouent, des hooks d'édition qui maintiennent les index de code locaux à jour, et des audits des journaux de session chaque fois que l'on change ou met à niveau un modèle de codage.

C'est là que le temps d'ingénierie continue de créer de la valeur.

L'auteur invite chacun à regarder ce que son équipe appelle cette semaine un "harnais de codage" ou un "framework d'agent", et à couper la glue : supprimer les boucles de relance, la plomberie de cache et les wrappers d'outils personnalisés que les API de modèles ont déjà absorbés, tout en gardant les flux de travail de dépôt dans des fichiers ouverts et simples (AGENTS.md, SKILL.md, et de simples sidecars CLI / MCP) pour que changer de harnais reste peu coûteux.

Il recommande ensuite d'investir le temps ainsi libéré dans les politiques, le code, les mémoires, et la lecture des journaux de session de codage chaque fois qu'on change de modèle — on y trouve généralement une surprise.

L'article se termine par une question ouverte aux lecteurs : quelle glue de harnais de codage personnalisé ont-ils supprimée, et où un changement de modèle les a-t-il quand même "mordus" ?

## Pourquoi ça compte
Ce billet offre un cadre utile pour une veille tech sur les agents IA : il aide à distinguer ce qui relève désormais de l'infrastructure commoditisée (à ne plus développer soi-même) de ce qui reste un investissement d'ingénierie différenciant face à des modèles dont le comportement varie fortement et évolue à chaque mise à jour.
