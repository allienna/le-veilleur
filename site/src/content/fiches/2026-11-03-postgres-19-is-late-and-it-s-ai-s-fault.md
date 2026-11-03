---
title: "Postgres 19 is late, and it's AI's fault"
date: 2026-11-03
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Frhaas.blogspot.com%2F2026%2F10%2Fpostgres-19-is-late-and-its-ais-fault.html%3Futm_source=tldrnewsletter/1/010001a19c0aca0e-dd5f7a8a-9589-4b62-b678-e5a111c4a772-000000/6Z6dQVrZKAbPk1-zdcA5Zp2dxeXTipJwBHV5kzFcKQA=452"
authors: ["Robert Haas"]
keywords: ["PostgreSQL", "intelligence artificielle", "bugs logiciels", "open source", "base de données", "qualité du code"]
theme: "Data"
tone: "opinion"
used_in: ["2026-11-03"]
---

## Résumé
L'auteur, développeur PostgreSQL de longue date, explique pourquoi la version 19 du système, habituellement publiée entre mi-septembre et mi-octobre, sera repoussée à novembre 2026. Plusieurs fonctionnalités majeures ont dû être retirées tardivement du cycle de développement (entre fin août et mi-septembre), un événement inhabituel à ce stade avancé. Sa thèse centrale : ce retard n'est pas dû à une baisse de rigueur des contributeurs, mais à l'explosion du nombre de bugs détectés grâce aux LLM, qui absorbent désormais une part croissante du temps de révision humaine. Il en tire une conclusion plus large sur l'avenir du développement logiciel face à l'IA.

## Points clés
- Le cycle de sortie de PostgreSQL, très régulier depuis dix ans, est perturbé en 2026 : la version 19 sortira en novembre, voire plus tard.
- Trois fonctionnalités importantes (UPDATE/DELETE FOR PORTION OF, SQL/PGQ, ALTER TABLE … MERGE/SPLIT PARTITION) ont été annulées très tardivement dans la période de beta.
- Entre avril et septembre, les correctifs rétro-portés (back-patched) vers les anciennes branches ont bondi de plus de 60 % par rapport à l'année précédente, et de plus de 74 % pour les branches encore plus anciennes.
- La cause identifiée : un afflux massif de signalements de bugs trouvés via des LLM, que les mainteneurs humains doivent toujours valider et corriger eux-mêmes, car les correctifs générés par l'IA ne sont pas toujours fiables.
- Le temps consacré à la correction de ces bugs rétroactifs a mécaniquement réduit le temps disponible pour finaliser les nouvelles fonctionnalités de la v19, d'où les révocations tardives.
- L'auteur juge ce retard sain (gage de qualité) mais s'inquiète d'un défi de fond : rattraper quarante ans de bugs invisibles aux humains mais désormais détectables par l'IA, sans freiner l'innovation.

## Analyse approfondie
L'auteur pose d'abord le constat : la cadence des sorties majeures de PostgreSQL est devenue, au fil de la dernière décennie, remarquablement prévisible — toujours entre la mi-septembre et la mi-octobre. 2026 rompt ce schéma : la version 19 ne devrait pas sortir avant novembre, et un report supplémentaire n'est pas exclu. Fait encore plus inhabituel, trois fonctionnalités de poids — la clause UPDATE/DELETE FOR PORTION OF, les requêtes sur graphes de propriétés SQL (SQL/PGQ), et les commandes ALTER TABLE de fusion/scission de partitions — ont été retirées du projet entre le 27 août et le 15 septembre, soit bien après le gel des fonctionnalités (fixé chaque année au 8 avril). Si des annulations ponctuelles juste après ce gel ne sont pas rares, en voir plusieurs majeures à une date aussi tardive est exceptionnel.

Selon l'auteur, la cause tient en un mot : les LLM. Le code de PostgreSQL est volumineux, complexe et ancien — son historique Git, repris depuis CVS, couvre plus de trente ans, et les premières lignes remontent à une décennie avant cela. Un tel volume de code a toujours charrié son lot de bugs, sans que cela nuise au succès du projet. Ce qui change aujourd'hui, c'est la facilité avec laquelle ces bugs sont désormais détectés — la capacité à les corriger progressant, elle, beaucoup plus lentement.

L'auteur appuie son propos sur des chiffres de commits. Entre le 8 avril et le 25 septembre 2025, la branche principale (master) a reçu 1037 commits et la branche stable REL_18 724 commits. Sur la même période en 2026, master en compte 1443 et la branche stable REL_19 1169. En isolant les commits sur master entre le gel des fonctionnalités et le 25 septembre, leur nombre a même légèrement baissé d'une année sur l'autre — mais les commits rétro-portés (back-patched) vers une version déjà publiée ont bondi de plus de 60 %.

L'auteur écarte l'idée que les committers auraient simplement commis davantage d'erreurs ; la réalité, selon lui, est qu'ils sont restés tout aussi prudents qu'avant, mais qu'une proportion bien plus grande de leurs erreurs est désormais repérée rapidement par des outils d'IA. Le phénomène ne se limite pas à la dernière version : sur la même fenêtre temporelle, les commits rétro-portés vers REL_17 (en 2025) étaient de 248, contre 433 vers REL_18 (en 2026) — soit une hausse de plus de 74 % en un an. En clair, un nombre croissant de personnes sur Internet signalent des bugs PostgreSQL qu'elles ont découverts grâce aux LLM, et les committers du projet ont dû mettre les bouchées doubles pour les corriger.

L'auteur identifie deux mécanismes qui expliquent à la fois les révocations tardives et le report de la sortie. Premièrement, la multiplication des bugs détectés allonge mécaniquement le temps de correction : les LLM peuvent esquisser des correctifs, mais ceux-ci ne sont pas toujours corrects ni conformes aux standards du projet — ils doivent donc être relus et validés par des humains, dont la capacité de travail n'a, elle, pas progressé entre 2025 et 2026. Deuxièmement, le temps qui aurait dû être consacré à l'examen des nouvelles fonctionnalités de la version en préparation a été détourné vers la résolution de problèmes de sécurité et d'autres bugs sur les branches déjà publiées, retardant d'autant la décision de ce qu'il fallait retirer avant de livrer la v19.

L'auteur conclut que ce retard n'est, en soi, pas inquiétant : il reste modéré et découle directement du souci de qualité du projet. Il juge en revanche la perspective de long terme plus trouble : comment rattraper quarante années de bugs que les humains n'avaient jamais su détecter, mais que les LLM révèlent aujourd'hui, sans pour autant freiner la capacité du projet à innover ? Il admet ne pas avoir de réponse certaine, tout en précisant que lui-même, comme beaucoup d'autres contributeurs, travaille activement à la trouver.

Il termine sur une note personnelle et réflexive : il a choisi de devenir développeur PostgreSQL en partie parce que la base de code lui semblait parmi les plus propres et les plus abouties sur lesquelles il ait eu le privilège de travailler. Le fait que l'IA y débusque aujourd'hui davantage de bugs ne change rien, selon lui, à cette haute estime — aucun logiciel n'est parfait, et un code moins rigoureux aurait sans doute révélé un nombre de défauts bien plus élevé encore sous l'examen des LLM. Il conclut que l'arrivée des LLM va obliger chaque développeur PostgreSQL — et, dans une certaine mesure, chaque développeur logiciel au monde — à élever son niveau d'exigence : toute fonctionnalité écrite désormais sera scrutée par l'IA, et des défauts qui seraient restés indéfiniment ignorés dans une autre époque seront désormais mis en évidence, parfois en quelques heures seulement. Il présente cela à la fois comme un défi et comme une opportunité.

## Pourquoi ça compte
Ce billet illustre un effet concret et mesurable de l'IA sur le développement logiciel open source : au-delà de la génération de code, les LLM transforment déjà les cycles de release et la charge de maintenance des projets critiques d'infrastructure comme PostgreSQL.
