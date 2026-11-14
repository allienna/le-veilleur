---
title: "The new Genie: autonomous AI for complex enterprise work"
date: 2026-11-14
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.databricks.com%2Fblog%2Fnew-genie-autonomous-ai-complex-enterprise-work%3Futm_source=tldrit/1/010001a1d510cfb8-3a9bc1a4-acd1-45e1-94ef-c194a4a5b67b-000000/KN1NTtYCeiPCNpyo8J-S3yWmkebrCB3PtoKRLPJ2n7I=452"
keywords: ["IA agentique", "Databricks", "ontologie d'entreprise", "recherche d'entreprise", "gouvernance de données", "automatisation"]
theme: "Data"
tone: "news"
used_in: ["2026-11-14"]
---

## Résumé

Databricks dévoile une nouvelle version de Genie, qui passe d'un assistant conversationnel à un véritable "collègue IA" autonome capable de gérer des tâches d'entreprise longues et complexes, dans les limites fixées par les utilisateurs. Cette autonomie s'appuie sur trois piliers : Genie Ontology (une carte du métier de l'entreprise construite par des agents et gouvernée par des humains), Genie Search (une recherche hybride qui agrège les données du lakehouse et des applications métier) et Unity Gateway (un contrôle centralisé des accès, des actions et des coûts). Genie peut désormais surveiller des processus en continu, produire des livrables (slides, tableaux de bord, pages HTML), agir dans des outils tiers via MCP, et être utilisé depuis Slack, Teams, le web, le mobile, ou même depuis ChatGPT et Claude via des plugins. Databricks annonce également un benchmark où Genie, épaulé par Genie Ontology, répond correctement 1,6 fois plus souvent qu'un agent frontier concurrent, avec moins de la moitié des tokens utilisés.

## Points clés

- Genie devient un agent autonome et proactif qui prend en charge des tâches continues (surveillance de fraude, gestion de campagnes marketing, veille des emails/Slack), tout en demandant validation humaine quand nécessaire.
- Genie Ontology fournit le contexte métier (définitions, métriques, relations organisationnelles), construit automatiquement par des agents mais gouverné et validé par des experts humains via Unity Catalog.
- Genie Search unifie la recherche dans le lakehouse et les applications d'entreprise (Google Drive, SharePoint, Jira, Confluence, Workday) en combinant indexation et recherche live via MCP, tout en respectant les droits d'accès natifs de chaque source.
- Unity Gateway centralise la gouvernance : contrôle des accès aux données, des outils/connecteurs utilisables, des budgets de dépense et de l'audit des actions des agents.
- Genie Agents permettent désormais de travailler sur des données non structurées (PDF, slides) via la recherche de contenu dans Unity Catalog Volumes, avec citations au niveau de la page, et peuvent agir dans des outils externes (Slack, GitHub, Gmail) via des connecteurs.
- Un benchmark réalisé avec Turing montre que Genie, grâce à Genie Ontology, obtient 91 % de réussite sur des tâches nécessitant de relier des connaissances dispersées entre tables, tableaux de bord et notebooks, soit 1,6 fois le taux du meilleur agent frontier concurrent, pour moins de la moitié des tokens consommés.

## Analyse approfondie

Genie est désormais un collègue IA autonome qui prend en charge des tâches de longue durée pour votre compte, en opérant dans les limites que vous définissez.

Genie Ontology, une ontologie agentique construite par des agents et gouvernée par des humains, fournit un contexte métier fiable, tandis que Genie Search trouve des informations à travers votre lakehouse et vos systèmes métier pour aider Genie à fournir des réponses précises et complètes.

Unity Gateway permet aux administrateurs de contrôler l'accès aux outils, de tracer les actions et de fixer des limites de dépenses pour garder l'autonomie sous contrôle.

Les assistants IA peuvent exécuter des analyses et résumer des réunions, mais ce sont les employés qui continuent de gérer le travail qui les entoure. C'est parce que la majorité du travail en entreprise est continu, complexe et intensif en données. Pour surveiller la performance d'un pipeline ou gérer des budgets, quelqu'un doit suivre les changements, décider de ce qui compte, et agir.

Plus tôt cette année, nous avons introduit Genie One pour aider les équipes à comprendre leurs données et à agir en conséquence. Des milliers de clients utilisent Genie en production, dont Zillow, Unilever, adidas, Atlassian et AstraZeneca.

Aujourd'hui, nous présentons le nouveau **Genie** : un collègue IA autonome qui prend en charge de manière proactive le travail d'entreprise de longue durée pour vous. Genie reste à son poste en continu, suit les progrès, relance sur les informations manquantes, et agit à mesure que de nouvelles informations arrivent. Vous fixez les garde-fous, supervisez son travail et validez là où c'est nécessaire, et Genie s'occupe du reste.

Cette autonomie dépend du contexte métier et de contrôles clairs. **Genie Ontology** donne à Genie une carte de votre entreprise, incluant ses définitions, métriques, relations et connaissances organisationnelles. **Genie Search** aide les personnes et les agents à trouver des informations à travers votre lakehouse et vos applications métier connectées. **Unity Gateway** et **Unity Catalog** encadrent Genie au sein de vos permissions et politiques existantes, tout en donnant aux administrateurs une visibilité sur ses actions, son usage et son coût.

Vous pouvez interagir avec **Genie** via Genie One, l'email, Slack et Microsoft Teams. Donnez-lui une mission et l'accès aux outils dont il a besoin, et il prend en charge le travail en continu. Il revient vers vous quand il a besoin d'une information ou d'une validation, et s'adapte à vos retours.

Par exemple, Genie peut surveiller les demandes d'indemnisation entrantes à la recherche de schémas de fraude émergents et de dérives de sinistralité, puis constituer le dossier et le transmettre aux souscripteurs lorsqu'un segment sort des normes fixées. En marketing, Genie peut gérer des campagnes en continu, enquêter sur toute sous-performance, et proposer des ajustements budgétaires hebdomadaires à valider. Il peut aussi surveiller votre email et Slack, préparer votre journée, et vous alerter dès que de nouveaux éléments surviennent.

Ce qui rend cela possible, c'est le contexte fourni par Genie Ontology, qui indique à Genie comment votre entreprise fonctionne — depuis ce qui définit un client actif jusqu'à la métrique de revenu qui fait référence. Une mémoire personnelle conserve vos préférences et instructions, pour que vous n'ayez pas à les répéter à chaque mission.

Genie est également proactif. Il repère le travail que vous répétez, comme une mise à jour hebdomadaire, et propose de le prendre en charge. Il peut aussi signaler des problèmes qui nécessitent votre attention avant même que vous ayez configuré une mission. Une fois une mission lancée, elle peut tourner selon un calendrier ou répondre à des déclencheurs, par exemple quand une métrique chute ou quand plus de 10 clients demandent la même fonctionnalité.

Genie peut travailler sur plusieurs missions à la fois. Vous pouvez superviser, orienter et arrêter ces missions dans une seule conversation, avec un panneau de contrôle pour les missions actives et leurs résultats. Vous décidez de ce que Genie fait de manière autonome et de ce qui nécessite votre validation, dans le cadre des garde-fous de votre entreprise.

Nous élargissons également Genie avec de nouvelles façons de trouver de l'information, de produire du travail fini et de collaborer à travers les outils.

**Un seul endroit pour trouver des réponses :** recherchez des collaborateurs, documents, tickets et plus encore depuis la même barre de discussion où vous posez vos questions. Genie Search rassemble des résultats de sources comme Google Drive, SharePoint, Jira, Confluence et Workday, avec les tableaux de bord Databricks, les tables, les Databricks Apps et les Genie Agents. Les annuaires organisationnels vous aident à explorer les structures d'équipe et à trouver le bon collègue.

**Des livrables prêts à partager :** décrivez le diaporama, le tableau de bord ou la page HTML interactive dont vous avez besoin, et Genie le construit directement dans la conversation. Affinez-le dans le chat, puis présentez-le, partagez-le ou réutilisez-le. Des tâches planifiées maintiennent chaque livrable à jour à mesure que vos données évoluent, tandis que des compétences partagées appliquent les chartes graphiques de l'entreprise.

« Avec les livrables dans Genie, nous avons un contrôle créatif total sur la manière de présenter nos données. Nous pouvons obtenir exactement le rendu que nous voulons tout en restant connectés à nos données gouvernées — c'est le meilleur des deux mondes. » — Guilherme Vivian, Data Manager, Agibank

**Travailler à travers les applications :** les connecteurs MCP permettent à Genie de lire et d'agir dans des outils populaires comme Slack, Zoom, Microsoft 365, Jira, GitHub et votre calendrier, tout cela ancré dans la même ontologie qui donne à Genie les définitions, relations et contexte pour comprendre votre entreprise. Via MCP personnalisé, vous pouvez aussi vous connecter à ServiceNow, PagerDuty et plus : Genie peut enquêter sur un incident en utilisant les changements GitHub et Jira, garder le ticket à jour, et tenir l'équipe informée jusqu'à résolution. Et quand quelqu'un obtient d'excellents résultats avec un flux de travail reproductible, il peut le publier comme une compétence et la partager avec son équipe. Les compétences résident dans Unity Catalog et s'exécutent avec les permissions de celui qui les utilise.

**Genie partout où vous travaillez :** envoyez un message ou mentionnez Genie dans Slack et Microsoft Teams, ou utilisez-le dans votre navigateur, sur ordinateur, et sur iOS et Android. Des plugins apportent également le contexte métier de Genie dans des outils IA comme ChatGPT et Claude.

Genie travaille aux côtés de chaque utilisateur métier, et **Genie Agents** apportent une expertise spécialisée à des équipes entières. Des milliers d'équipes les utilisent déjà en marketing, vente, finance et opérations. Un département configure un agent avec les données, fichiers, outils et instructions dont il a besoin, puis gère son accès et son usage. Les équipes peuvent travailler avec les agents dans Genie One ou via des API, des applications personnalisées et des flux de travail automatisés.

**Travailler à travers données structurées et non structurées :** Genie Agents fonctionne désormais non seulement avec des tables structurées, mais aussi avec des PDF, des diaporamas et plus encore. La **recherche de contenu** dans les **Unity Catalog Volumes** rend cela possible sans index vectoriel séparé. Un responsable commercial se demandant pourquoi une région perd des contrats peut obtenir une analyse combinant données de pipeline et rapports gains/pertes, avec des citations au niveau de la page qui rendent les preuves faciles à vérifier.

**De l'investigation à l'action : les connecteurs** permettent à Genie Agents de lire et d'agir dans des outils incluant Slack, Atlassian, GitHub, Gmail, Google Drive et Microsoft 365. Un agent peut enquêter sur un problème, créer un ticket, et préparer un résumé pour le canal de l'équipe, en portant les conclusions dans les systèmes où les équipes travaillent.

**Partager l'expertise au-delà de votre organisation : OpenSharing pour Genie Agents** permet aux équipes de partager des agents gouvernés avec des partenaires et des clients, préchargés avec les données, instructions et connaissances dont ils ont besoin pour obtenir de la valeur immédiatement. Pour les cas d'usage plus sensibles, **Genie Clean Rooms** permet aux destinataires de poser des questions et d'obtenir des réponses sans exposer les données sous-jacentes ni la logique propriétaire, avec des contrôles tels que des limites de conversation et de sortie.

« Genie Agents permet à nos experts métier de productiser directement leur connaissance des données. Ce qui prenait autrefois un cycle de développement complet ne prend désormais que quelques jours, et chaque réponse reste à l'intérieur de notre périmètre de gouvernance. » — Priyanka John, Vice President, S&P Global Energy

Que Genie gère une tâche unique ou une responsabilité continue, il doit comprendre votre entreprise et la manière dont l'information se connecte à travers les systèmes. **Genie Ontology** donne à l'IA, à travers toute votre entreprise, cette compréhension partagée. Elle relie données structurées et non structurées avec des définitions, des relations et des connaissances organisationnelles.

**Construite par des agents, gouvernée par des humains :** les agents construisent automatiquement la majeure partie de Genie Ontology à partir des tableaux de bord, requêtes et notebooks que les gens utilisent déjà, et elle continue d'apprendre à chaque requête et interaction IA à travers votre organisation. Des sources de connaissance externes étendent cet apprentissage à la logique métier dans des outils de BI comme Power BI. Les équipes établissent des définitions de référence dans Unity Catalog, et l'algorithme OntoRank donne la priorité à ces définitions, afin que chaque agent travaille à partir de la même compréhension gouvernée de l'entreprise.

**Comprendre les personnes et les équipes :** les annuaires organisationnels, à commencer par Workday, intègrent les personnes, les équipes et les relations hiérarchiques dans Genie Ontology. OntoRank combine ces relations avec des signaux d'activité montrant qui travaille réellement ensemble, afin que Genie puisse pondérer ce qui est le plus pertinent pour la personne qui pose la question.

**Conserver les contrôles administrateurs : Ontology Manager** donne aux équipes un espace partagé pour gérer et personnaliser le contexte à mesure que l'entreprise évolue. Les administrateurs peuvent surveiller la santé du contexte, tandis que les experts du domaine organisent les connaissances qu'ils maîtrisent le mieux. **Unity Catalog Domains**, **Pages** et **Ontology Snippets** prennent en charge à la fois les définitions organisées par des experts et les connaissances que Genie apprend automatiquement. Des alertes proactives sur les lacunes signalent les concepts fréquemment interrogés qui manquent de définitions gouvernées, et les propriétaires peuvent promouvoir des connaissances apprises utiles en Pages de référence.

Le contexte métier partagé contribue aussi à améliorer la précision et à réduire l'usage de tokens. Dans un nouveau benchmark construit avec Turing, nous avons comparé Genie, propulsé par Genie Ontology, à deux agents frontier de premier plan sur les mêmes tâches dans le même espace de travail Databricks. Genie a répondu correctement dans 91 % des exécutions de tâches, soit 1,6 fois le taux de l'agent frontier le plus performant, tout en utilisant moins de la moitié des tokens. Les tâches exigeaient de relier des connaissances dispersées entre tables, tableaux de bord et notebooks, et non simplement d'accéder aux données.

« Genie Ontology est exactement ce dont nous avons besoin pour faire évoluer l'IA sans perdre le contexte métier qui la rend utile. C'est un multiplicateur de force pour nos équipes data. » — Noah Cepela, SVP, Analytics and Insights, Mode Global

Genie Ontology donne à Genie une compréhension partagée de votre entreprise. Pour mettre cette compréhension en pratique, Genie doit aussi trouver l'information pertinente où qu'elle se trouve, des tables du lakehouse aux documents, tickets et wikis. Tout aussi important, il doit faire respecter les contrôles d'accès de chaque ressource.

Aujourd'hui, nous présentons **Genie Search**, un nouveau type de recherche IA hybride qui apporte la recherche d'entreprise dans Databricks, sans infrastructure de recherche séparée à acquérir ni modèle de permissions séparé à maintenir.

Genie Search combine un index du contenu des applications métier principales comme Google Drive, Jira, Confluence, Workday et SharePoint avec une recherche en direct via MCP. L'index fournit un accès rapide et précis, tandis que MCP récupère les mises à jour les plus récentes et la longue traîne des applications qui ne peuvent pas être indexées. Pour chaque tâche, Genie puise dans l'index, MCP, ou SQL, puis compose une réponse unique avec des citations. Le résultat : des réponses plus complètes avec moins d'appels d'outils et moins de tokens.

Au-delà des bénéfices classiques d'un index de recherche, Genie Search alimente aussi Genie Ontology, si bien que vos tickets et documents deviennent des preuves que OntoRank pèse pour décider en quelles sources faire confiance. Via Unity Catalog, Genie Search fait correspondre les contrôles d'accès de chaque source avec son contenu et les fait respecter avant de renvoyer tout résultat, afin que personne ne voie dans Genie un document qu'il n'aurait pas pu ouvrir dans l'application d'origine.

Le même contexte métier qui alimente Genie peut aussi soutenir le travail dans d'autres assistants IA. Connectez vos données une fois, laissez Genie construire votre ontologie à partir de la façon dont vos équipes travaillent, puis apportez ce contexte via les **plugins Genie** vers ChatGPT, Claude, Copilot et Grok Bot. Vous pouvez aussi utiliser **Genie MCP** directement pour connecter Genie à d'autres outils IA.

Les agents peuvent confier une question métier entière à Genie ou demander le contexte nécessaire pour une tâche plus large. Genie applique les définitions gouvernées, respecte les permissions des utilisateurs, et cite ses sources.

À mesure que Genie prend en charge un travail continu à travers les systèmes d'entreprise, les administrateurs doivent contrôler qui l'utilise, ce à quoi il peut accéder, et combien il coûte. **Unity Gateway** réunit ces contrôles, permettant aux administrateurs de gouverner Genie à côté des agents de code, des modèles, des outils MCP et des compétences.

**Accès aux données :** Genie agit avec votre identité et n'accède qu'aux informations que vous êtes autorisé à voir. Il respecte les permissions d'Unity Catalog et, pour le contenu indexé par Genie Search, les permissions de chaque système source. Quand les utilisateurs ont besoin d'un accès supplémentaire, Genie peut préparer une demande d'accès qu'ils n'ont qu'à examiner et envoyer. Les administrateurs et propriétaires de données conservent l'autorité de validation.

**Outils et actions :** les administrateurs contrôlent l'accès aux connecteurs, aux outils MCP et les exigences de validation. Les utilisateurs métier choisissent ce que Genie peut faire de manière autonome dans ces limites. Unity Catalog gouverne les compétences réutilisables, et les mêmes contrôles s'appliquent quand des agents externes comme Claude appellent Genie via MCP.

**Usage, coût et audit :** chaque action de Genie est tracée et auditable. Les administrateurs peuvent fixer des budgets par espace de travail et par utilisateur, des plafonds de dépense et des alertes. Ils peuvent aussi demander à Genie d'enquêter sur l'usage et les traces d'agents à la recherche de tokens gaspillés et d'appels d'outils coûteux.

Avec Genie, les équipes peuvent passer de l'usage de l'IA pour des tâches individuelles à lui confier la responsabilité d'un travail continu, avec un contexte métier partagé et des contrôles intégrés.

Rejoignez-nous pour **Data + AI Live: Context Is Just the Beginning**, avec Ali Ghodsi et Greg Brockman d'OpenAI. Regardez en direct ou en replay.

## Pourquoi ça compte

Cette annonce illustre le glissement du marché de l'IA d'entreprise, des assistants conversationnels vers des agents véritablement autonomes dotés de contexte métier gouverné, de connecteurs MCP et de contrôles de coûts intégrés — un signal fort pour toute équipe data/plateforme évaluant sa stratégie d'agentic AI.
