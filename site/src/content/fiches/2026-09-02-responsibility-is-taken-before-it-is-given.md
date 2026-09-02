---
title: "Responsibility Is Taken Before It Is Given"
date: 2026-09-02
url: "https://link.mail.beehiiv.com/ss/c/u001.WjplEBHoYsVAvmS39jW9CU-zx4FtprlcLTuYkS0xsz6rK40QvE7fjoYMwHY-m0__bQbK41aViT7eTJjSRA3NdGIuKvDKet5o_MI7S79uKA6SEXAPvUlsMwa1mxNflAGqbUgHIb29YZOcufVtQYsNA2pOQNI0NIB6sHP3-xJG7w1GCwW5rR5gXtGnGHey820X/4to/J86wL3ZyRZKrMW8TS6n3xA/h11/h001.5OSqv4xn0z9hdgfkDxKFvk_G7Fz9PjtJFQZdhb_euLE"
keywords: ["ownership", "responsabilité", "management", "confiance", "carrière ingénieur"]
theme: "Leadership"
tone: "opinion"
used_in: ["2026-09-02"]
---

## Résumé
L'auteur, ingénieur ayant travaillé sur le projet Perfetto chez Google, développe une thèse simple : en Big Tech, la responsabilité (« ownership ») n'est pas d'abord accordée par un manager puis exercée, elle est d'abord exercée à petite échelle puis reconnue formellement. Les jeunes ingénieurs qui attendent qu'on leur confie un périmètre avant de faire preuve de jugement autonome tombent dans un piège classique. L'auteur illustre ce mécanisme par sa propre trajectoire sur l'outillage d'analyse de traces de Perfetto, où il est passé du statut d'exécutant supervisé à celui « d'owner » reconnu. Il insiste sur le fait que prendre des responsabilités ne veut pas dire empiéter sur le périmètre d'autrui.

## Points clés
- La responsabilité formelle est un indicateur retardé (« trailing indicator ») : elle vient après la confiance gagnée, pas avant.
- Un tech lead délègue davantage quand il constate qu'un collaborateur traite les problèmes aussi bien, ou mieux, que lui-même le ferait.
- L'auteur a progressé en cherchant à comprendre le raisonnement de son tech lead (pourquoi telle idée, quelle approche) plutôt qu'en se contentant d'exécuter ses corrections.
- Un exemple concret : plusieurs structures de données jugées distinctes par l'auteur ont été unifiées, sur l'insistance de son TL, en une abstraction commune de « tables » qui structure aujourd'hui plus de 100 tables dans Perfetto.
- Prendre des responsabilités par petites touches (proposer, anticiper les objections, fixer l'agenda) fonctionne dans un environnement sain, mais peut échouer face à un mauvais manager où la progression relève davantage de la politique interne que du mérite.
- Le signal ultime de la reconnaissance : le changement de vocabulaire du TL, qui passe de « l'ingénieur qui travaille sur X » à « l'owner de X ».

## Analyse approfondie
L'article part d'une question récurrente chez les ingénieurs juniors en Big Tech : comment démontrer de l'ownership si le manager ne leur a rien confié à posséder ? L'auteur qualifie ce raisonnement de piège, car il inverse la logique réelle : la responsabilité n'est pas un paquet complet distribué a priori, elle se construit par la confiance accumulée au fil de décisions jugées pertinentes.

Du point de vue du tech lead, accepter de déléguer signifie accepter par avance les conséquences des décisions du collaborateur. La question implicite que se pose le lead est de savoir si la personne traiterait les problèmes de la même manière que lui — ou mieux. Si la réponse est positive, la délégation suit naturellement.

L'auteur retrace son propre parcours sur l'outillage d'analyse de traces de Perfetto. Initialement, il exécutait les décisions d'implémentation sous la direction de son TL, qui repérait régulièrement des problèmes de fond que lui-même n'avait pas vus. L'exemple donné : l'auteur avait conçu plusieurs classes distinctes pour des structures de données qu'il pensait non liées entre elles ; son TL a insisté pour les unifier sous le concept de « tables », même si l'auteur ne voyait pas encore comment. Cette abstraction est devenue le socle de plus de cent tables déclaratives dans le processeur de traces de Perfetto aujourd'hui.

Plutôt que de simplement appliquer les corrections, l'auteur explique avoir cherché à comprendre le cheminement intellectuel de son TL : comment celui-ci était-il arrivé à repérer ce que lui-même avait manqué, quelle méthode avait-il employée. En intériorisant progressivement ces méthodes, il a commencé à les utiliser lui-même pour éprouver ses propositions de changements d'API ou d'optimisations de performance avant même de les soumettre. Ses idées ont alors de plus en plus reçu un simple feu vert. À ce stade, il définissait lui-même l'agenda : échanger avec les utilisateurs, comprendre leurs problèmes, les traduire en évolutions de code et décider des priorités. Le rapport de force s'est même parfois inversé, l'auteur expliquant à son TL pourquoi une suggestion de celui-ci ne fonctionnerait pas.

Le signal de bascule a été un changement de langage : son TL a commencé à le désigner comme « l'owner des outils d'analyse de traces » plutôt que « l'ingénieur qui travaille sur ces outils ».

L'auteur nuance toutefois son propos sur deux points. D'abord, prendre des responsabilités ne signifie pas s'accaparer des projets ou marcher sur les plates-bandes d'autrui : il s'agit d'exercer un jugement sûr dans le périmètre existant, ce qui, avec un TL raisonnable, débouche progressivement sur davantage de responsabilité. Ensuite, ce mécanisme suppose un management et un environnement sains ; dans une mauvaise organisation, gagner en responsabilité relève souvent davantage de la politique interne que du mérite réel.

La conclusion résume la thèse centrale : la responsabilité formelle est un indicateur retardé, jamais un point de départ. Les personnes commencent à faire confiance à votre jugement et à s'appuyer sur lui bien avant que cette responsabilité ne devienne officielle — elle se prend par petites touches avant d'être donnée pleinement.

## Pourquoi ça compte
Ce texte offre un cadre concret et actionnable pour les ingénieurs et les managers sur la dynamique réelle de la délégation et de la progression de carrière en tech, utile en veille RH/leadership autant qu'en gestion d'équipes techniques.
