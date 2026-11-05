---
title: "A Family Tree of Software Job Titles"
date: 2026-11-05
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fzwischenzugs.com%2F2026%2F11%2F03%2Fa-family-tree-of-software-job-titles%2F%3Futm_source=tldrnewsletter/1/010001a1a653c286-17ee683e-b27d-488f-a855-a83ed8d97c8d-000000/shF--bUSmfewoGO09e2T7c3fRb6XcTO-P24qx1ghmVQ=452"
authors: ["Ian Miell"]
keywords: ["titres de poste", "DevOps", "SRE", "platform engineering", "histoire de la tech", "carrière IT"]
theme: "Tech"
tone: "opinion"
used_in: ["2026-11-05"]
---

## Résumé
Ian Miell, ancien « Head of DevOps », a construit avec l'aide de Claude un arbre généalogique interactif de 104 intitulés de poste du logiciel, du « Computer » des années 1940 à l'« AI Agent / Context Engineer » de 2025. L'outil (un fichier Graphviz et un fichier JSON de descriptions) classe les titres en sept familles — développement, architecture/leadership, opérations, réseaux/sécurité, données/IA, qualité, support — reliées par des flèches de filiation ou d'influence. L'auteur en tire six observations sur la manière dont les métiers du logiciel se scindent, se recombinent et se recyclent depuis les années 1940, avec un parallèle final entre les « coders » de 1947 et l'IA d'aujourd'hui.

## Points clés
- Arbre de 104 titres (1940s–2025), construit en Graphviz (.dot + JSON), organisé en sept familles et en lignes de cinq ans.
- Le codage fut d'abord perçu comme une tâche subalterne (souvent féminine) avant de devenir la partie créative du métier — un parallèle que l'auteur établit avec l'IA actuelle.
- Les titres se scindent puis se recombinent (webmaster → développeur web → front-end/back-end → full-stack), selon un balancier centralisation/distribution déjà observé ailleurs par l'auteur.
- Certains titres sont éphémères (prompt engineer absorbé par l'AI engineer, scrum master en reflux), d'autres ressurgissent sous un nouveau nom (configuration management, forward deployed engineer proche du systems engineer IBM des années 1960).
- Le clivage Dev/Ops ne se résout jamais : il change simplement de nom, de DevOps à SRE puis platform engineering.

## Analyse approfondie

### Le projet
L'auteur a occupé le poste de « Head of DevOps » pendant plusieurs années, après avoir fait le même travail sous d'autres noms, et l'a ensuite vu rebaptisé SRE, puis évoluer vers le « platform engineering ». Constatant que les intitulés de poste du logiciel se renouvellent sans cesse sans que leur origine soit claire, il a construit, avec l'aide de Claude, un arbre généalogique des titres de poste du logiciel, des années 1940 à aujourd'hui, publié sur ianmiell.github.io/sw-job-title-family-tree.

### Ce que contient l'outil
L'arbre recense 104 intitulés, du « Computer » (une personne qui calcule, pas une machine) jusqu'à l'« AI Agent / Context Engineer » apparu vers 2025. Le temps s'écoule du haut vers le bas par tranches de cinq ans, les titres étant répartis en sept colonnes colorées par famille : développement ; analyse, architecture et leadership ; opérations et infrastructure ; réseaux et sécurité ; données et IA ; qualité et test ; support et relation client.

Une flèche pleine indique qu'un titre découle directement de son « parent » ; une flèche en pointillés signale une influence ou une évolution de carrière courante. Les titres marquants apparaissent en gras. Le site permet de filtrer par famille (par exemple Data & AI) ou de cliquer sur un titre pour afficher son historique et ses liens (par exemple SRE).

Techniquement, l'ensemble repose sur un unique fichier Graphviz (.dot) et un fichier JSON de descriptions ; chaque titre correspond à une ligne du fichier .dot, et le schéma est généré avec la commande `dot -Tsvg job_title_family_tree.dot -o job_title_family_tree.svg`. Ajouter un titre ne demande que trois petites modifications : un nœud dans la colonne de sa famille, une entrée dans la ligne de sa période de cinq ans, et ses flèches de filiation.

L'auteur précise que les dates correspondent approximativement au moment où un titre est devenu *courant*, et non à sa première occurrence attestée ; il s'agit de ses propres estimations plutôt que de données sourcées. Certaines sont bien documentées (SRE chez Google en 2003, « DevOps » inventé en 2009, « Data Scientist » en 2008), beaucoup d'autres restent approximatives.

### Six observations tirées de l'exercice

**1. Le code a commencé comme la partie administrative du métier.** En 1947, l'article « Planning and Coding of Problems » de Goldstine et von Neumann distinguait déjà deux tâches : les mathématiciens planifiaient le problème, les « coders » traduisaient ce plan en instructions machine — un travail alors jugé subalterne et largement effectué par des femmes. Le codage est finalement devenu la partie difficile et créative du métier, si bien que le « coder » a fusionné avec le « programmer ». En remontant plus loin encore, plusieurs des premiers programmeurs d'ENIAC venaient des « human computers » de l'armée américaine, chargés de calculer à la main : le métier a donné son nom à la machine, et ses praticiens à la programmation.

**2. Les titres se scindent, puis se recomposent.** Le « webmaster » apparaît vers 1993 : souvent une seule personne qui écrivait le HTML, faisait tourner le serveur web (parfois une machine sous un bureau), répondait aux e-mails et maintenait le site en ligne. Vers le milieu des années 2000, le titre a quasiment disparu, jugé démodé : le code est revenu aux développeurs web, les serveurs aux administrateurs système, le contenu aux éditeurs et designers. Le développeur web s'est ensuite scindé en front-end et back-end vers 2005, avant que les deux ne se recombinent sous l'appellation « full-stack » vers 2008 — un exemple du balancier centralisation/distribution que l'auteur avait déjà observé ailleurs, ici appliqué aux intitulés de poste.

**3. Certains titres ne durent pas.** Le « prompt engineer » a fait les gros titres en 2023 avec des offres d'emploi très bien rémunérées ; à mesure que les modèles se sont améliorés, cette compétence s'est diluée dans d'autres métiers, et sur l'arbre elle est absorbée par l'« AI engineer » presque aussitôt apparue. Le « scrum master » suit une trajectoire similaire mais plus lente : la demande a culminé dans les années 2010, avant que de nombreuses organisations ne refondent ce rôle dans le management d'ingénierie ou la livraison de projets. Le titre le plus récent de l'arbre est l'« AI Agent / Context Engineer » (vers 2025), dont la description reconnaît elle-même que « le temps dira s'il reste un titre à part » — l'auteur se garde de faire un pari là-dessus.

**4. Les noms sont recyclés.** « Systems Engineer » désigne en réalité deux métiers différents sur l'arbre : chez IBM dans les années 1960, c'était un rôle d'avant-vente, au contact des clients pour concevoir et mettre en route des installations ; dans les années 1990, notamment via la certification MCSE de Microsoft, le même titre a fini par désigner un administrateur système plus senior et orienté conception — même nom, branche différente, aucun lien de parenté réel. De même, la « configuration management » a démarré dans les années 1960 comme discipline de la défense américaine pour suivre les évolutions matérielles, est devenue gestion de versions logicielles dans les années 1970, avant de ressurgir des décennies plus tard sous le nom d'outils comme Puppet ou Chef.

**5. La nouveauté est souvent un retour en arrière.** Le « forward deployed engineer » (FDE) est l'un des titres les plus en vogue de 2025, OpenAI, Anthropic et de nombreuses start-up IA recrutant des FDE pour faire fonctionner l'IA directement chez leurs clients. Palantir a construit une bonne partie de son activité autour de ce rôle depuis environ 2010 : des ingénieurs logiciels intégrés chez le client, souvent sur site, qui développent ce qu'il faut pour adapter le produit au problème de ce client précis. Un rôle qui ressemble beaucoup, note l'auteur, aux « systems engineers » d'IBM des années 1960, lesquels travaillaient déjà avec les clients avant et après la vente pour concevoir et faire tourner leurs installations — et qui rappelle aussi, admet-il avec ironie, le conseil à l'ancienne.

**6. Le débat DevOps reste ouvert.** Ben Treynor Sloss a défini le SRE comme « ce qui se passe quand on demande à un ingénieur logiciel de concevoir une équipe d'exploitation ». Le DevOps devait au départ désigner une culture de collaboration entre développeurs et exploitants, mais vers 2011 « DevOps Engineer » était déjà devenu un intitulé de poste, généralement attribué à la personne chargée de l'automatisation. Sur l'arbre, la flèche entre SRE et DevOps pointe dans les deux sens, et le « platform engineering » a les deux comme parents : il a été présenté vers 2022 comme « le successeur du DevOps ». Pour l'auteur, le clivage entre développement et exploitation n'a jamais vraiment été résolu : il ne fait que changer de nom.

### Pourquoi se donner cette peine
Quand on lui demande la différence entre un ingénieur DevOps, un SRE et un ingénieur plateforme, la réponse honnête de l'auteur est toujours une mini-leçon d'histoire — cet arbre en est la version la plus courte qu'il ait réussi à produire jusqu'ici. Il reconnaît que les dates sont des estimations, qu'il aura sans doute oublié des titres, mal retracé certaines filiations et tracé des flèches contestables, et invite les lecteurs mieux informés à proposer des corrections, y compris via une pull request sur le dépôt du projet.

Il termine en revenant sur les « coders » de 1947 : à l'époque, le codage était vu comme la tâche administrative, le vrai travail intellectuel résidant dans la planification. Quatre-vingts ans plus tard, avec l'IA, on entend un discours très similaire sur le code — et la dernière fois, ce sont justement les codeurs qui se sont révélés faire la partie la plus difficile du travail. À chacun, conclut-il, de tracer lui-même cette flèche.

## Pourquoi ça compte
Cette rétrospective donne du recul historique sur les débats actuels DevOps/SRE/platform engineering et sur le sort probable des rôles liés à l'IA (prompt engineer, AI engineer, forward deployed engineer), utile pour quiconque fait de la veille sur l'évolution des métiers tech et veut anticiper les prochains intitulés à la mode.
