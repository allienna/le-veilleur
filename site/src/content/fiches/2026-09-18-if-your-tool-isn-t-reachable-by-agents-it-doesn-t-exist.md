---
title: "If Your Tool Isn't Reachable by Agents, It Doesn't Exist"
date: 2026-09-18
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Flws.io%2Fblog%2Fif-your-tool-isnt-reachable-by-agents-it-doesnt-exist%2F%3Futm_source=tldrdev/1/010001a0af146874-dc9a6ee3-a5dc-4222-8676-ccbdd199480a-000000/gRl1uEkLlHNken33sGQ5kf4JE627rCb4poxy6OK5hNo=452"
keywords: ["agents IA", "skills", "MCP", "distribution logicielle", "Apify"]
theme: "IA"
tone: "opinion"
used_in: ["2026-09-18"]
---

## Résumé
L'auteur, créateur de Wordsworth (un outil web pour rédacteurs techniques), raconte comment il a transformé son application en « skill » installable en une commande pour agents IA. Il défend l'idée que la distribution logicielle bascule du modèle « dashboard/site web » vers des capacités directement invocables par des agents, via les skills et les serveurs MCP. Selon lui, un outil qui n'est pas accessible à un agent devient invisible, quelle que soit sa qualité. Il illustre son propos avec l'exemple d'Apify, dont le serveur MCP rend des dizaines de milliers d'outils IA soudain découvrables.

## Points clés
- Wordsworth, une app web avec sept outils d'analyse d'écriture, a été convertie en skill installable via une simple commande (`npx skills add ...`).
- Le dashboard web est présenté comme une couche de friction (identité, navigation, attention) devenue un surcoût plutôt qu'un atout.
- Le modèle de distribution classique (bannières, newsletters, SEO, landing pages) est jugé à bout de souffle face à l'usage via un agent unique interfaçant plusieurs plateformes.
- Avec les skills et MCP, l'agent découvre, appelle et exploite directement la capacité, sans interface humaine intermédiaire.
- Chez Apify, des dizaines de milliers d'outils IA exposés via serveur MCP deviennent enfin utilisés dès qu'ils sont rendus « joignables » par un agent.
- La compétition se déplacera vers qui rend sa capacité réellement accessible aux agents plutôt que vers qui construit le produit le plus sophistiqué.

## Analyse approfondie
La semaine dernière, j'ai fusionné une pull request qui transforme Wordsworth, mon application web destinée aux rédacteurs techniques, en une skill pour agent. Il suffit de l'installer avec `npx skills add phazonoverload/wordsworth` pour que n'importe quel agent doté d'un accès aux outils reçoive d'un coup sept outils d'analyse d'écriture.

Si votre outil ne se connecte pas à l'agent de quelqu'un, la partie est perdue.

J'ai construit Wordsworth. Je l'ai lancé. Je ne l'ai pas ouvert moi-même depuis des mois.

Ce n'est pas un échec du produit. C'est le sens du marché. Le dashboard est une friction : une identité à gérer, une page à charger, une interface à parcourir, de l'attention à mobiliser. Si la même capacité existe sous forme de skill qui s'exécute silencieusement quand mon agent en a besoin, le dashboard devient un poids superflu.

Le dashboard a toujours été la couche de distribution. Bannières cliquables, newsletters par email, pages optimisées pour le référencement, pages d'atterrissage. On se bat pour capter l'attention. On convainc quelqu'un de visiter une URL et d'utiliser son outil. Cela fonctionne si l'on dispose d'un budget marketing, d'un bon timing, et de la patience d'un missionnaire.

Ce modèle est aujourd'hui cassé. Non pas parce que les applications web et les dashboards seraient mauvais en soi — ils fonctionnent très bien — mais parce que la manière dont les gens interagissent avec les logiciels est en train de changer.

Dans un monde où chaque utilisateur dispose d'un agent unique s'intégrant à diverses plateformes, votre travail consiste à vous intégrer à cet agent. Les skills et les serveurs MCP sont le moyen d'y parvenir.

L'agent ouvre votre outil, appelle votre capacité, et l'analyse s'effectue. Aucune interface humaine n'est nécessaire. L'utilisateur décrit ce qu'il veut. L'agent se charge du routage. Votre outil fonctionne, tout simplement.

Chez Apify, des dizaines de milliers d'outils IA sont mis à disposition via notre serveur MCP. Prêts à être découverts. Prêts à être utilisés. Je le constate chaque jour : des outils qui existent, qui fonctionnent, qui sont utiles, mais que personne n'ouvre parce que personne ne sait qu'ils existent. Puis quelqu'un les rend accessibles sous forme de skill, et soudain ils se retrouvent entre les mains de milliers d'utilisateurs qui ignoraient jusque-là en avoir besoin.

Wordsworth compte sept outils. Chacun fait quelque chose de différent : notation de lisibilité, détection de mots d'atténuation (« hedge words »), vérification de la tenue des promesses du texte. En tant qu'application web, il faut se souvenir de l'URL, ouvrir le navigateur, coller le texte, cliquer sur des boutons, lire les résultats, les recopier ailleurs. En tant que skill, mon agent l'appelle et l'analyse se fait directement.

Le format skill n'est pas nouveau. Mais la prolifération des plateformes d'agents qui consomment des skills change la donne en matière de distribution. Une capacité publiée comme skill peut tourner sur n'importe quel agent supportant ce format. Une distribution avec un onboarding standard et une manière standard de l'invoquer.

Vous pourriez construire la plateforme d'analyse d'écriture la plus sophistiquée au monde (la mienne ne l'était pas, pour ce que ça vaut). Si votre concurrent se déploie sous forme de skill qui s'installe en une commande et fonctionne dans l'agent que votre équipe utilise déjà, c'est ce concurrent qui gagne. Parce qu'il est réellement joignable.

Wordsworth en tant qu'application web est un coût irrécupérable (« sunk cost »). L'avenir de ce produit, ce sont des agents qui l'appellent. Je m'en accommode.

Il y a dix ans, distribuer un logiciel signifiait mettre en place une infrastructure d'hébergement, construire une landing page, faire de la publicité ou du SEO, écrire des articles de blog, participer à des conférences, démarcher des journalistes. Tout cela représentait un surcoût pour une capacité que les gens voulaient simplement pouvoir utiliser.

Désormais, il s'agit d'une capacité qui vit partout où les agents opèrent. Un simple fichier markdown. Une définition d'outil. Voilà la nouvelle distribution.

Mon application web n'est plus un produit. C'est une skill. Et c'est là qu'est désormais la place de Wordsworth.

## Pourquoi ça compte
Ce texte capture un changement de paradigme concret pour la veille tech : la valeur d'un outil logiciel dépend de plus en plus de sa capacité à être découvert et invoqué par des agents IA (via skills/MCP), et non plus de sa présence en tant qu'application autonome — un signal fort pour repenser les stratégies produit et de distribution.
