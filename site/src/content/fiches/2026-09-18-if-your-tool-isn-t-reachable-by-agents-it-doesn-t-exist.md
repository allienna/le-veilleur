---
title: "If Your Tool Isn't Reachable by Agents, It Doesn't Exist"
date: 2026-09-18
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Flws.io%2Fblog%2Fif-your-tool-isnt-reachable-by-agents-it-doesnt-exist%2F%3Futm_source=tldrdev/1/010001a0af146874-dc9a6ee3-a5dc-4222-8676-ccbdd199480a-000000/gRl1uEkLlHNken33sGQ5kf4JE627rCb4poxy6OK5hNo=452"
keywords: ["agents IA", "MCP", "skills", "distribution logicielle", "Apify", "dashboard"]
theme: "IA"
tone: "opinion"
used_in: ["2026-09-18"]
---

## Résumé

L'auteur, créateur de Wordsworth (une application d'analyse d'écriture technique) et employé chez Apify, raconte avoir transformé son produit en « skill » installable en une commande pour agents IA, plutôt que de continuer à miser sur son interface web classique. Il constate qu'il n'a lui-même plus ouvert le dashboard de son outil depuis des mois, signe selon lui d'une bascule de fond : les utilisateurs délèguent de plus en plus leurs tâches à un agent unique qui orchestre directement les outils, rendant les interfaces humaines superflues. Il en tire une thèse plus générale : la distribution logicielle historique (SEO, publicité, landing pages) devient obsolète face à l'intégration directe dans les agents via des formats comme les skills et les serveurs MCP. Sa conclusion : un outil injoignable par un agent devient, de fait, invisible — quelle que soit sa qualité.

## Points clés

- Wordsworth a été transformé en skill agent (installable via `npx skills add ...`), exposant sept outils d'analyse d'écriture directement utilisables par un agent, sans passer par l'interface web.
- L'auteur lui-même n'utilise plus le dashboard de son propre produit depuis des mois — preuve à ses yeux que ce type d'interface devient une couche de friction plutôt qu'un atout.
- Les canaux de distribution traditionnels (bannières, newsletters, SEO, landing pages) perdent en pertinence dans un monde où un agent unique sert de point d'entrée vers de multiples outils.
- Chez Apify, des dizaines de milliers d'outils IA sont déjà exposés via un serveur MCP, mais restent souvent invisibles et sous-utilisés tant qu'ils ne sont pas packagés en skill facilement descouvrable.
- La nouvelle unité de distribution logicielle devient minimale : un fichier markdown ou une définition d'outil, installable en une commande, utilisable par tout agent compatible avec le format.
- Dans ce nouveau paradigme, un concurrent moins abouti techniquement mais mieux intégré aux agents (installation immédiate, usage transparent) l'emporte sur un produit plus sophistiqué mais uniquement accessible via une interface humaine classique.

## Analyse approfondie

L'auteur ouvre son propos sur un fait concret : il vient de fusionner une pull request qui convertit Wordsworth, son application web destinée aux rédacteurs techniques, en une « skill » pour agents. L'installation se fait en une seule commande, et tout agent disposant d'un accès aux outils récupère alors sept fonctions d'analyse d'écriture regroupées. Le constat qu'il en tire est brutal : si un outil ne se connecte pas à l'agent de quelqu'un, la partie est perdue d'avance.

Il confie avoir lui-même construit et lancé Wordsworth, mais ne plus l'avoir ouvert depuis des mois. Il précise que ce n'est pas un échec du produit, mais le reflet d'une évolution du marché. Le dashboard, dit-il, est devenu une source de friction : il faut gérer une identité, charger une page, naviguer dans une interface, mobiliser de l'attention. Si la même capacité existe sous forme de skill s'exécutant silencieusement dès que l'agent en a besoin, le dashboard devient un coût superflu.

Selon lui, le dashboard a toujours été avant tout une couche de distribution : bannières publicitaires, newsletters, pages optimisées pour le référencement, pages d'atterrissage. Il fallait se battre pour capter l'attention, convaincre quelqu'un de visiter une URL et d'utiliser le produit — une approche qui fonctionnait à condition de disposer d'un budget marketing, d'un bon timing, et d'une patience à toute épreuve. Ce modèle est aujourd'hui, selon lui, dépassé — non pas parce que les applications web et les dashboards seraient mauvais en soi (ils restent tout à fait valables), mais parce que la façon dont les utilisateurs interagissent avec les logiciels change en profondeur.

Dans un monde où chaque utilisateur dispose d'un agent unique qui s'intègre à diverses plateformes, la mission de tout créateur d'outil devient de s'intégrer à cet agent. Les skills et les serveurs MCP (Model Context Protocol) constituent, pour lui, les deux véhicules de cette intégration. L'agent ouvre l'outil, invoque la capacité voulue, et l'analyse se déroule sans qu'aucune interface humaine ne soit nécessaire : l'utilisateur décrit ce qu'il souhaite, l'agent se charge de router la demande, et l'outil fonctionne en coulisses.

L'auteur illustre ce phénomène par son expérience chez Apify, où des dizaines de milliers d'outils IA sont mis à disposition via leur serveur MCP — prêts à être découverts, prêts à être utilisés. Il observe quotidiennement des outils qui existent, fonctionnent et sont utiles, mais que personne n'ouvre faute d'en connaître l'existence. Dès qu'un de ces outils est rendu accessible sous forme de skill, il se retrouve soudain entre les mains de milliers d'utilisateurs qui ignoraient jusqu'alors en avoir besoin.

Il revient sur Wordsworth : sept outils aux fonctions distinctes — score de lisibilité, détection des tournures de prudence excessive (« hedge words »), vérification du respect des promesses formulées dans un texte, etc. En tant qu'application web, l'utilisation exigeait de se souvenir de l'URL, d'ouvrir un navigateur, de coller le texte, de cliquer sur des boutons, de lire les résultats, puis de les recopier ailleurs. En tant que skill, il suffit que l'agent de l'auteur l'invoque pour que l'analyse s'exécute directement.

L'auteur note que le format « skill » n'est pas nouveau en soi. Ce qui change, c'est la multiplication des plateformes d'agents capables de consommer ce format, ce qui transforme radicalement les mathématiques de la distribution logicielle : une capacité publiée comme skill peut désormais fonctionner sur n'importe quel agent supportant ce format, avec un onboarding standardisé et un mode d'invocation uniforme.

Il pousse le raisonnement jusqu'à sa conclusion compétitive : on pourrait construire la plateforme d'analyse d'écriture la plus sophistiquée au monde (il admet que la sienne ne l'était pas) — si un concurrent la propose sous forme de skill installable en une seule commande et fonctionnant directement dans l'agent déjà utilisé par une équipe, ce concurrent l'emporte, tout simplement parce qu'il est réellement accessible.

En conclusion, l'auteur affirme que Wordsworth en tant qu'application web représente désormais un coût irrécupérable (« sunk cost »). L'avenir du produit, selon lui, réside dans le fait que ce sont des agents qui l'appelleront — un état de fait avec lequel il se dit en paix. Il rappelle qu'il y a dix ans, distribuer un logiciel impliquait de monter une infrastructure d'hébergement, de construire une page d'atterrissage, de faire de la publicité ou du référencement, de rédiger des articles de blog, d'assister à des conférences, de démarcher des journalistes — autant d'efforts superflus pour une capacité que les gens veulent simplement pouvoir utiliser. Désormais, cette capacité vit là où opèrent les agents : un simple fichier markdown, une définition d'outil. C'est, selon lui, la nouvelle forme de la distribution logicielle. Et c'est là, conclut-il, que Wordsworth a désormais sa place — non plus en tant que produit autonome, mais en tant que skill.

## Pourquoi ça compte

Ce billet illustre un basculement structurel dans la manière dont les logiciels sont distribués et consommés à l'ère des agents IA (skills, MCP), un signal utile pour quiconque suit l'évolution des stratégies produit et go-to-market dans un contexte où l'agent devient le principal point d'accès aux outils numériques.
