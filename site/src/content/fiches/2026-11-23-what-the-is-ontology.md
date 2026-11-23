---
title: "What the !@#$% is Ontology?"
date: 2026-11-23
url: "https://open.substack.com/pub/dataengineeringcentral/p/what-the-is-ontology?utm_source=multiple-personal-recommendations-email&utm_medium=email&token=eyJ1c2VyX2lkIjo0NzU1OTI2MjgsInBvc3RfaWQiOjIyMzIwMDI0MSwiaWF0IjoxNzk1MzcxMjQ2LCJleHAiOjE3OTc5NjMyNDYsImlzcyI6InB1Yi0xMjI0Nzk5Iiwic3ViIjoicG9zdC1yZWFjdGlvbiJ9.IMqKLiDRtv0Ta4OVwW2XpIacx7xRr-1yyu9JTwOZYzg"
keywords: ["ontologie", "semantic layer", "agents IA", "context layer", "Databricks", "knowledge graph"]
theme: "Data"
tone: "opinion"
used_in: ["2026-11-23"]
---

## Résumé
L'article retrace l'histoire du mot « ontologie », de la philosophie du XVIIe siècle à son usage en informatique (dès 1967, puis DARPA en 1997, Stanford en 2006) jusqu'à son explosion marketing en 2024-2025 porté par l'IA agentique. L'auteur, blogueur data, part en enquête pour comprendre ce que les grands éditeurs (Databricks, Snowflake, AWS, Microsoft) et le monde open source entendent réellement par « ontologie », et la distingue d'une simple couche sémantique. Il conclut que l'ontologie n'est, au fond, qu'une nouvelle tentative — parmi des décennies d'autres (modèles entité-relation, dictionnaires de données, data mesh, data contracts) — de coder la connaissance métier pour que les machines, et désormais les agents IA, puissent l'exploiter correctement.

## Points clés
- Le terme « ontologie » existe depuis le XVIIe siècle (philosophie) et est utilisé en informatique depuis 1967 ; son usage dans les outils SaaS n'explose qu'en 2024-2025 avec la vague d'agents IA.
- Définition retenue : une ontologie est un modèle lisible par machine des concepts d'un domaine, de leurs relations, et des règles qui les régissent — à distinguer d'une couche sémantique (qui répond à « comment calculer », alors que l'ontologie répond à « qu'est-ce que c'est »).
- L'idée n'est pas nouvelle : ERD, dictionnaires de données, modèles de données d'entreprise, web sémantique, catalogues de données, data mesh et data contracts poursuivaient déjà, chacun à leur façon, le même objectif de coder la connaissance métier.
- Côté open source, l'offre est encore très pauvre : seulement deux projets notables, tous deux portés par de grands éditeurs — NVIDIA (auto-ontology, basé SQL) et AWS (context-ontology-accelerator, très intégré à l'écosystème AWS et coûteux).
- Databricks a sorti en GA « Genie Ontology », présentée comme une « context layer » combinant connaissance définie par des humains et connaissance extraite automatiquement des données, avec des fonctionnalités comme OntoRank (classement de la fiabilité des connaissances), les Unity Catalog Pages/Domains, ou Genie Search.
- L'auteur reste sceptique sur la valeur ajoutée réelle par rapport à une bonne couche sémantique classique, faute de preuves chiffrées (evals) justifiant le coût de cette nouvelle infrastructure.

## Analyse approfondie
L'article s'ouvre sur un ton volontairement informel : l'auteur avoue avoir été dépassé par la soudaine omniprésence du mot « ontologie » dans son fil d'actualité, et décide de remonter aux origines du terme. Il rappelle que le mot latin *ontologia*, apparu vers 1600, désignait à l'origine l'étude de la nature de l'existence — un clin d'œil ironique de l'auteur, qui s'amuse à dire que ce « moine » du XVIIe siècle avait presque prédit que les « data peasants » d'aujourd'hui se questionneraient sur leur propre utilité à l'ère agentique.

Il propose ensuite une chronologie de l'usage du terme en informatique :
- 1967 : les informaticiens commencent à utiliser « ontologie » pour désigner le lien entre les données/le code et le monde réel.
- Années 1980 : construction d'outils de « connaissance » (knowledge tools).
- 1997 : grand projet DARPA « Toward Distributed Use of Large-Scale Ontologies ».
- 2006 : publications de Stanford utilisant le terme dans la recherche en informatique.
- 2024-2025 : vague d'adoption massive par les éditeurs SaaS.

L'auteur observe que, comme les « data contracts » ou le « data mesh » avant elle, l'ontologie est une idée ancienne qui n'avait pas trouvé son cas d'usage grand public — jusqu'à l'arrivée des agents IA, qui semblent lui offrir enfin ce moment.

**Qu'est-ce qu'une ontologie, au juste ?** L'auteur retient la définition suivante : un modèle lisible par une machine des concepts d'un domaine, de leurs relations, et, si nécessaire, des règles qui gouvernent ces concepts. Il s'interroge immédiatement sur le chevauchement avec d'autres notions voisines : la couche sémantique, ou le « contexte »/« mémoire » des LLM et agents. Sa distinction de travail : une couche sémantique répond à « comment calcule-t-on tel ou tel chiffre », tandis qu'une ontologie répond à « qu'est-ce que cette chose ». Il prédit néanmoins un chevauchement croissant entre ces concepts, nourri par le marketing des éditeurs.

Pour clarifier les choses, l'auteur passe en revue les définitions données par les grands fournisseurs cloud/data (Databricks, Snowflake, AWS, Microsoft), notant qu'ils sont globalement alignés sur une approche « agentique » de l'ontologie (à l'exception notable, selon lui, de Snowflake, jugée plus confuse). Il relie cela à son expérience personnelle de « data warehouse » classique, où consultants et développeurs se disputaient pendant des heures pour coder la logique métier dans un entrepôt de données — un problème, selon lui, aussi vieux que la data elle-même.

Il liste les tentatives historiques qui ont, chacune à sa manière, tenté de résoudre ce même problème de codification de la connaissance métier :
- Modélisation entité-relation (ERD)
- Dictionnaires de données
- Modèles de données d'entreprise
- Web sémantique
- Architecture orientée services (SOA)
- Graphes de connaissances
- Catalogues de données / gouvernance
- Couches sémantiques / couches de métriques
- Data mesh / data products
- Data contracts

Il mentionne au passage que Palantir dispose probablement d'un des guides les plus complets et réalistes sur l'implémentation d'une couche d'ontologie en production.

**La vraie question : qui gagnera la guerre des implémentations ?** L'auteur compare la situation naissante autour de l'ontologie à celle vécue récemment avec les catalogues de données du Lakehouse (Unity, Polaris, Lakekeeper, Nessie), devenus du jour au lendemain une brique d'architecture incontournable. Il se demande si une « guerre de l'ontologie » va suivre le même chemin. Il note également un changement d'époque : alors que Stack Overflow, Google et Reddit dominaient autrefois la diffusion des idées via le marketing classique, aujourd'hui tout le monde « armé » de Claude ou ChatGPT se sent expert en tout, et l'ère des « influenceurs tech » s'intensifie face à une audience lassée du contenu généré par IA.

**L'open source est encore très pauvre.** L'auteur constate qu'il n'existe presque aucun projet open source sérieux et populaire autour de l'ontologie — les deux seuls exemples notables étant construits par de grands éditeurs eux-mêmes :
- NVIDIA – *auto-ontology*
- AWS – *context-ontology-accelerator*

Il mentionne aussi des versions SaaS comme Genie Ontology de Databricks.

*NVIDIA auto-ontology* est décrit comme un outil assez lourd, principalement basé sur SQL, nécessitant sa propre infrastructure de calcul et de base de données. Il s'agit d'une couche sémantique/contextuelle pour des agents interrogeant des bases SQL analytiques : l'outil lit les métadonnées de la base, utilise un LLM pour rédiger une première « ontologie » (termes métier, jointures, définitions de métriques), laisse des humains la réviser et la certifier, puis répond aux questions en langage naturel via du SQL ancré dans cette ontologie — chaque réponse étant accompagnée du SQL et des étapes utilisées. L'outil repose sur trois concepts :
1. **Term** : un concept métier avec description et synonymes, relié à des colonnes physiques.
2. **SQL attribute** : une expression SQL validée, rattachée à un terme, réutilisée pour qu'une métrique soit toujours calculée de la même façon.
3. **Relationship** : la manière dont les tables se joignent (y compris tables de liaison), inférée des clés et des données.
L'outil se connecte à des sources comme Postgres, MySQL, Databricks, Snowflake, ClickHouse, Trino, Kyuubi, HeavyDB, DuckDB ou SQLite, et automatise, selon sa propre documentation, « les 80 % fastidieux de la construction d'une couche sémantique ». L'auteur en profite pour s'interroger : y a-t-il vraiment une différence durable entre une couche sémantique et un outil d'ontologie, ou finiront-elles par fusionner ? Sa comparaison : un format de type Apache Ossie serait le fichier, et Auto-Ontology le moteur capable de le lire et de l'écrire. Son principal reproche : l'outil ne semble pas prendre en charge l'ingestion de sources multimodales (PDF, documents Word), alors que c'est là, selon lui, que se trouve l'essentiel de la richesse métier non structurée aujourd'hui.

*AWS context-ontology-accelerator (COA)* est présenté comme encore plus lourd, profondément intégré à l'écosystème AWS (DataZone, Neptune, Athena, AgentCore, Bedrock, Lake Formation), avec un coût d'entrée élevé avant même de poser une question. En contrepartie, il permet, contrairement à auto-ontology, de construire un graphe de connaissances à partir de PDF et de fichiers Word. L'auteur estime que seules les très grandes organisations, avec des dizaines de milliers d'employés et une connaissance institutionnelle très dispersée, justifieraient un tel investissement.

L'auteur s'interroge alors : « est-ce que ça vaut vraiment le coup ? » Après des mois à construire bases vectorielles, bases de connaissances et outillage agentique, il reconnaît ne pas savoir si le gain apporté par une ontologie « lourde » dépasse celui d'un bon agent couplé à une simple couche sémantique — faute de preuves ou d'évaluations chiffrées démontrant que le coût de cette nouvelle infrastructure est justifié.

**Le cas Databricks Genie Ontology.** Passé en disponibilité générale, cet outil est présenté par Databricks comme une « context layer » d'entreprise pour les agents IA — l'auteur souligne que Databricks emploie lui-même ce terme plutôt qu'« ontologie ». Genie Ontology combine une connaissance métier définie explicitement par des humains avec une connaissance extraite automatiquement des actifs de données existants, puis détermine quelles informations sont les plus pertinentes et fiables pour la tâche d'un agent. Contrairement à une couche sémantique traditionnelle, qui repose surtout sur des métriques et dimensions définies manuellement, Genie Ontology vise à découvrir, organiser et réutiliser automatiquement la connaissance métier à travers l'organisation — une approche que l'auteur juge très proche de celle d'auto-ontology de NVIDIA (exploration automatique, puis raffinement humain). Parmi les fonctionnalités, certaines nouvelles, d'autres déjà existantes :
- **Ontology Snippets** : définitions métier, calculs, relations et règles extraits automatiquement.
- **OntoRank** : classe la connaissance par autorité, pertinence, certification, popularité et fraîcheur.
- **Unity Catalog Metric Views** (déjà existant) : définitions de KPI et métriques gouvernées et réutilisables.
- **Unity Catalog Domains / Subdomains** : organisation de la connaissance et des actifs métier par domaine.
- **Unity Catalog Pages** : définitions de concepts métier rédigées et validées par des humains, faisant autorité.
- **Genie Search** : recherche dans les documents d'entreprise, tickets et wikis.
- **External Knowledge Sources** : import de définitions sémantiques depuis des outils BI externes, à commencer par Power BI.
- **Organizational Directories** : ajout de personnes, équipes, relations hiérarchiques et signaux d'expertise.
- **Ontology Manager** (à venir) : interface visuelle pour inspecter, organiser et gouverner l'ontologie.

**Conclusion de l'auteur.** Au terme de son enquête, il retient que le concept d'ontologie reste très jeune, en particulier côté open source, et que son avenir dépendra des implémentations qui s'imposeront. Les versions SaaS, comme Genie Ontology, lui semblent déjà assez bien définies, mélangeant des fonctionnalités classiques de couche sémantique avec de nouvelles briques de « base de connaissances » et de classement technique, au service d'agents plus précis. Fondamentalement, il estime que l'ontologie n'est qu'une nouvelle tentative de répondre à un problème vieux comme la donnée elle-même : la donnée brute n'a aucun sens sans contexte métier (que signifie réellement « client » selon les équipes et les départements ?). Historiquement, c'étaient des humains qui devaient trouver ce sens ; aujourd'hui, ce sont les LLM et les agents qui doivent, eux aussi, disposer de ce contexte — non seulement savoir *comment* calculer X, Y ou Z, mais aussi savoir ce que X, Y et Z *signifient* selon les situations. Il termine sur une note humoristique et un brin fataliste sur le risque que les agents, correctement outillés en contexte métier, finissent par remplacer les travailleurs du secteur data.

## Pourquoi ça compte
Ce texte offre un décryptage clair et sans filtre marketing d'un terme ambigu que les grands éditeurs (Databricks, AWS, Snowflake) poussent fortement comme brique indispensable de l'IA agentique en entreprise, tout en rappelant utilement que le problème qu'il recouvre — coder la connaissance métier pour qu'elle soit exploitable par des systèmes automatisés — est en réalité très ancien et encore loin d'être résolu de façon consensuelle.
