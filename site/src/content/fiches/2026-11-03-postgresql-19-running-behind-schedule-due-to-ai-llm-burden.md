---
title: "PostgreSQL 19 Running Behind Schedule Due To AI/LLM Burden"
date: 2026-11-03
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.phoronix.com%2Fnews%2FPostgreSQL-19-Late%3Futm_source=tldrit/1/010001a19c6ab804-cf5f7c9f-19fa-4841-9a12-e400532b9b70-000000/ZiuZYc5-qTncIphPpwFeib04ePn2sJWJ4K7wupni0dM=452"
authors: ["Robert Haas"]
keywords: ["PostgreSQL", "intelligence artificielle", "LLM", "sécurité", "bug", "open source"]
theme: "Data"
tone: "news"
used_in: ["2026-11-03"]
---

## Résumé
Le développeur PostgreSQL Robert Haas explique dans un billet de blog que la sortie de PostgreSQL 19 est retardée, en grande partie à cause de l'intelligence artificielle. Les agents IA/LLM génèrent un afflux massif de rapports de bugs, et des correctifs générés par IA doivent encore être vérifiés et validés par des humains avant d'être intégrés. Par ailleurs, le temps normalement consacré à la revue de la nouvelle version a été détourné vers la correction de failles de sécurité et de bugs sur les versions antérieures, retardant la décision sur ce qu'il fallait annuler avant la sortie de la v19.

## Points clés
- PostgreSQL 19 accuse un retard par rapport au calendrier prévu.
- L'IA est explicitement pointée comme cause principale de ce retard.
- Les agents IA/LLM génèrent beaucoup plus de rapports de bugs qu'auparavant.
- Les correctifs proposés par les LLM ne sont pas toujours corrects ou conformes aux standards de PostgreSQL, et nécessitent une revue humaine.
- Les équipes ont dû détourner du temps vers des correctifs de sécurité et de bugs sur les anciennes branches (back-ports), au détriment de la revue de la nouvelle version.
- Ces deux facteurs expliquent à la fois les nombreux retraits tardifs (« reverts ») et le report global de la sortie.

## Analyse approfondie
Le développeur PostgreSQL Robert Haas a détaillé aujourd'hui, dans un billet de blog, pourquoi PostgreSQL 19 est en retard sur son calendrier, et pointe l'intelligence artificielle comme responsable. Les développeurs font face à un afflux de rapports de bugs provenant d'agents IA/LLM, et doivent également gérer des rétroportages de correctifs de sécurité et de bugs vers les versions antérieures de PostgreSQL.

Haas a commenté :

« Et je pense que c'est aussi pour cette raison que nous avons eu autant de retraits tardifs (« reverts »), et pourquoi la sortie elle-même est retardée. Deux facteurs sont en jeu ici.

Premièrement, comme beaucoup plus de bugs sont désormais détectés, il faut plus de temps pour les corriger. Les LLM peuvent rédiger des correctifs, mais ces correctifs ne sont pas toujours corrects ou conformes aux standards de PostgreSQL. Ils doivent donc toujours être revus et validés par des humains, et ces humains n'ont pas gagné en intelligence entre 2025 et 2026.

Deuxièmement, le temps qui aurait dû être consacré à la revue de ce qui entrait dans la nouvelle version a été détourné vers la résolution de problèmes de sécurité et d'autres bugs dans les branches antérieures (« back-branches »), ce qui a pris plus de temps pour déterminer ce qui devait être annulé avant la sortie de la v19. »

Plus de détails sur ce retard de PostgreSQL 19 lié à l'IA sont disponibles via ce billet de blog.

## Pourquoi ça compte
Ce cas illustre un effet secondaire concret et peu anticipé de l'adoption massive des LLM dans le développement logiciel : plutôt que d'accélérer la livraison, l'afflux de rapports et de correctifs générés par IA peut surcharger les mainteneurs humains et ralentir des projets open source critiques comme PostgreSQL.
