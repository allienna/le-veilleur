---
title: "Business Ontology: Governed Context for AI | Snowflake"
date: 2026-11-06
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.snowflake.com%2Fen%2Fblog%2Fbusiness-ontology-context%2F%3Futm_source=tldrit/1/010001a1ac00e250-2ace9b34-60b7-477f-bc75-94dc55db97c2-000000/7vYCXTtdCEDKiZnritT_BaiG9Ne9A3eicoVNB0A_KNQ=452"
keywords: ["ontologie métier", "gouvernance des données", "agents IA", "contexte sémantique", "Snowflake", "modèle sémantique"]
theme: "Data"
tone: "news"
used_in: ["2026-11-06"]
---

## Résumé
Snowflake annonce « Business Ontology » (bientôt en preview publique), une couche de gouvernance au sein de Horizon Context permettant aux équipes métier de définir, posséder et approuver des termes, entités, relations et métriques partagés, puis de les relier aux données et modèles qui les implémentent. L'objectif est de donner aux humains et aux agents IA une même définition approuvée des concepts métier (ex. « revenu net »), afin d'éviter les incohérences de réponses entre outils et de restaurer la confiance dans les réponses générées par l'IA. Snowflake articule cette offre autour de trois couches complémentaires : Cortex Sense (inférence automatique de contexte), Business Ontology (gouvernance du sens métier) et Semantic Views (exécution précise des métriques). La plateforme s'appuie aussi sur le standard ouvert Apache Ossie et sur le Model Context Protocol pour permettre l'interopérabilité avec d'autres outils (Tableau, Power BI, dbt, Omni, Sigma, ThoughtSpot, etc.).

## Points clés
- Business Ontology centralise la définition, la propriété et l'approbation des termes métier, et les relie aux vues sémantiques, tables et modèles qui les calculent.
- Trois couches de contexte distinctes et complémentaires : Cortex Sense (automatique), Business Ontology (gouvernance/autorité) et Semantic Views (calcul précis et reproductible).
- Seules les définitions approuvées sont servies aux agents IA (CoCo, CoWork), ce qui réduit le risque que les agents « inventent » des définitions divergentes.
- Interopérabilité assurée via le standard ouvert Apache Ossie (incubating) et le format RDF, ainsi que via le Model Context Protocol pour les agents externes à Snowflake.
- Partenaires analytiques (Omni, Sigma, ThoughtSpot) et client (dentsu) cités en soutien, soulignant le risque de « dérive sémantique » dans les environnements multi-outils.
- Les trois couches ne sont pas séquentielles : les clients peuvent démarrer par celle qui répond à leur besoin le plus urgent (glossaire ou métriques exécutables).

## Analyse approfondie
Aujourd'hui, nous annonçons **Business Ontology** (en preview publique prochainement), un moyen gouverné pour les équipes de définir, posséder et approuver des termes métier partagés, des entités, des relations et des métriques, et de les relier aux données et modèles qui les implémentent. Intégrée à Snowflake Horizon Context, la couche de contexte gouvernée au sein de Horizon Catalog, Business Ontology donne aux personnes et aux agents IA les mêmes définitions approuvées, afin que les agents puissent interpréter les données d'entreprise comme le fait le métier. Les équipes peuvent réutiliser cette connaissance à travers agents et applications sans la redéfinir pour chaque outil, tout en préservant les différences entre domaines tels que les ventes, la finance et le marketing.

Par exemple, un agent répondant à une question sur le revenu doit savoir comment la finance définit le « revenu » et comment celui-ci se rapporte aux commandes et aux clients. Cette connaissance réside généralement dans des modèles BI, des projets dbt et l'expérience d'employés de longue date, et les équipes doivent souvent la reconstruire pour chaque nouvel agent. Si un agent se trompe, les gens prennent des décisions basées sur un chiffre erroné et perdent confiance dans les réponses de l'IA. Business Ontology offre aux équipes un lieu officiel unique pour consigner cette connaissance.

Horizon Context rassemble la connaissance issue des outils que les équipes utilisent déjà. Ses connecteurs de métadonnées prêts à l'emploi collectent les schémas, les journaux de requêtes, les définitions de tableaux de bord et les signaux d'usage depuis des sources telles que Tableau, Power BI, dbt, SQL Server, Sigma, Omni et PostgreSQL. La lignée de données inter-plateformes retrace ensuite les données depuis une base source, à travers les transformations, jusqu'au tableau de bord qui les affiche. Le résultat est une vue connectée de votre patrimoine de données, donnant aux équipes une meilleure compréhension de la provenance des données et de leur utilisation, à l'intérieur comme à l'extérieur de Snowflake.

Pour que les agents puissent s'appuyer sur ce contexte, Snowflake propose trois couches de contexte, chacune ayant un rôle distinct : Snowflake Cortex Sense (en preview publique prochainement) infère le contexte automatiquement, Business Ontology gouverne le sens métier, et Snowflake Semantic Views exécutent les métriques.

Pourquoi trois couches plutôt qu'une seule ? Parce que chacune répond à un problème différent, et qu'aucune couche unique ne peut bien gérer les trois. Cortex Sense donne aux agents une couverture large des patrimoines de données immédiatement, sans que l'équipe ait à définir d'abord manuellement chaque table et chaque métrique. Business Ontology ajoute de l'autorité là où c'est le plus important, afin que les personnes et les agents travaillent à partir d'un sens métier approuvé. Semantic Views ajoute de la précision, afin que chaque métrique soit calculée de la même manière à chaque fois.

Les couches ne sont pas séquentielles : les clients peuvent commencer par la couche qui résout leur problème le plus urgent et ajouter les autres au fur et à mesure. Certaines équipes commenceront par des besoins de glossaire ; d'autres par des métriques exécutables. Quel que soit le point d'entrée, les trois couches offrent à chaque agent, application et personne un contexte métier unique, cohérent et autorisé.

Entrons dans le détail de chacune.

### Automatiser le contexte avec Cortex Sense

Pour de nombreuses équipes, Cortex Sense est le point de départ naturel car il prend en charge une grande partie du travail de fond. Il collecte le contexte à mesure que les personnes interrogent les données, construisent des tableaux de bord et exécutent des pipelines, transformant le travail quotidien en compréhension métier, avec moins de temps passé à définir ce que signifie chaque table et métrique et comment elles se relient.

Cortex Sense procède ainsi en construisant le contexte à partir des métadonnées et des schémas d'usage que les équipes produisent déjà, notamment l'historique des requêtes, les tableaux de bord et les modèles dbt. Au fur et à mesure que l'entreprise évolue, cette compréhension suit le rythme, Cortex Sense mettant automatiquement à jour sa connaissance selon la cadence choisie. Les équipes délimitent un cas d'usage métier, connectent le contexte existant pertinent et l'affinent par le feedback et des évaluations, réduisant le besoin de modéliser chaque table manuellement. Cortex Sense identifie intelligemment les connaissances contradictoires et demande aux équipes quelle source privilégier.

Lorsque les équipes sont prêtes à gouverner leurs termes les plus importants, Cortex Sense peut créer un brouillon initial dans Business Ontology avec des définitions, relations et liens vers les données proposés, afin que personne ne parte d'une page blanche. Les équipes peuvent délimiter un cas d'usage métier, connecter le contexte existant pertinent et l'affiner par le feedback et des évaluations, réduisant le besoin de modéliser chaque table manuellement. Cortex Sense identifie intelligemment les connaissances contradictoires et demande aux équipes quelle source privilégier.

### Définir le contexte métier avec Business Ontology

Business Ontology est l'endroit où les équipes consignent ce que signifient leurs termes métier les plus importants, qui les possède et comment ils se relient. Prenons « revenu net ». Plutôt que chaque vue sémantique, tableau de bord et agent porte sa propre version, un analyste le définit une fois (ou l'importe depuis un glossaire existant), fixe son périmètre à « finance », nomme un propriétaire, obtient une approbation et le relie à la métrique de vue sémantique qui le calcule (voir Figure 2). Dès lors, les agents et les autres équipes travaillent à partir de cette définition approuvée. Les équipes peuvent :

- **Ancrer les agents dans les concepts métier :** des experts du domaine définissent des concepts tels que les clients, les commandes et le revenu — et comment ils se relient — et les ingénieurs connectent ces définitions aux données. Les agents interprètent alors les données à travers la connaissance propre de l'entreprise.
- **Aligner les métriques entre les vues sémantiques :** les équipes relient des métriques équivalentes dans leurs propres vues sémantiques à une définition métier partagée unique, alignant le sens sans forcer chaque équipe vers une implémentation unique. Les différences intentionnelles sont également préservées : une chaîne de restaurants peut définir les « ventes en magasins comparables » différemment pour chaque enseigne, chaque version étant approuvée séparément, étiquetée avec sa propre marque et reliée à la vue sémantique qui la calcule.
- **Aider chacun à trouver la bonne définition :** chacun peut rechercher un terme, voir qui le possède et s'il est approuvé, et le suivre jusqu'à l'endroit où il est calculé. Les variantes par marque et par région conservent leur périmètre.

Parce que ces définitions influencent les décisions, les organisations contrôlent qui peut créer, modifier et approuver ces définitions grâce aux contrôles de gouvernance de Horizon Catalog. Les suggestions de l'IA et les définitions importées sont un point de départ pour la révision, et les propriétaires responsables décident de ce qui devient officiel. Lorsqu'une définition approuvée entre en conflit avec ce que Cortex Sense a inféré, les agents utilisent la définition approuvée et Cortex Sense en tire les leçons.

« Business Ontology donne à chaque définition un propriétaire responsable, la relie aux données qui l'implémentent, et en fait la réponse que chaque agent retourne. En tant qu'adopteurs précoces, c'est ce qui nous permet de mettre des agents devant nos données en toute confiance. »

##### Joe Tobey

Head of Data Product Engineering, dentsu

### Appliquer les définitions et la logique une seule fois avec Semantic Views

Semantic Views définit comment chaque métrique est calculée, tandis que Business Ontology gouverne ce qu'elle signifie et qui l'a approuvée. Chaque vue regroupe les métriques, dimensions et jointures d'un domaine dans un objet Snowflake que les agents, les outils BI et le SQL peuvent interroger directement, de sorte que les agents génèrent du SQL à partir d'une logique gouvernée plutôt que de le deviner. Business Ontology relie les définitions approuvées aux vues sémantiques qui les calculent, mais ne modifie pas le calcul. Celui-ci reste sous la responsabilité des propriétaires de chaque vue.

### La qualité du contexte exige une plateforme ouverte par conception

La connaissance métier ne porte ses fruits que si elle peut évoluer avec l'entreprise. C'est pourquoi Snowflake a contribué à fonder Apache Ossie (incubating), le standard ouvert et neutre pour les modèles sémantiques, désormais soutenu par des dizaines d'organisations, dont Microsoft, Salesforce, dbt Labs, Qlik et ThoughtSpot. Les Semantic Views peuvent importer et exporter des définitions Ossie, afin que les métriques puissent circuler entre Snowflake et d'autres outils compatibles Ossie au lieu d'être reconstruites dans chacun d'eux. Les agents extérieurs à Snowflake peuvent également interroger les Semantic Views via le Model Context Protocol, avec Horizon Catalog gouvernant l'accès.

« La dérive sémantique est l'un des risques les plus sous-estimés dans les environnements de données multi-partenaires — et chez Merkle, l'agence data et technologie de dentsu, nous opérons au cœur de certains des environnements les plus complexes du secteur. Business Ontology de Snowflake comble cet écart au niveau de l'infrastructure, en donnant à chaque définition un propriétaire et à chaque système en aval une réponse unique et gouvernée. »

##### Morten Lileng

Global Head of Engineering, dentsu

### Ce que disent les entreprises d'analytique à propos de Snowflake Business Ontology

Beaucoup de gens utilisent des outils de BI et d'analytique pour obtenir des réponses à leurs questions, ce qui rend un contexte métier cohérent essentiel. Voici comment Omni, Sigma et ThoughtSpot voient le défi du contexte et le rôle que joue Business Ontology pour y répondre :

#### Omni

« Pensez au contexte comme à l'intégration d'un nouvel analyste ; c'est tout ce que vous lui enseigneriez pour qu'il sache quand, pourquoi et comment utiliser les choses. Omni a été construit autour d'un modèle sémantique gouverné et dispose de la seule intégration bidirectionnelle avec les Snowflake Semantic Views, et maintenant Business Ontology pousse cette fondation plus loin en capturant les définitions métier approuvées. Ensemble, nous aidons nos clients communs à construire un contexte de confiance qui peut servir chaque utilisateur et chaque agent. »

— Jamie Davidson, Co-fondateur et Président d'Omni

#### Sigma

« Les agents IA ne sont fiables qu'à la mesure du contexte métier et des définitions qui les alimentent. Avec Business Ontology, nos clients communs peuvent définir leurs concepts métier une fois et les réutiliser sans friction à travers Sigma AI pour construire des applications, tableaux de bord et agents gouvernés, et alimenter une analytique de confiance dans Sigma. »

— Zalak Trivedi, Director of Product Management chez Sigma

#### ThoughtSpot

« Une IA de confiance dépend d'un contexte métier de confiance. Snowflake Business Ontology donne aux entreprises un foyer gouverné pour ce que signifient leurs termes métier, et ThoughtSpot enrichit continuellement ce contexte avec la connaissance captée auprès des utilisateurs métier grâce à Spotter, délivrant des réponses et des actions précises et explicables pour chaque utilisateur. Ensemble, nous aidons les clients à faire évoluer l'analytique agentique en toute confiance. »

— Francois Lopitaux, Senior Vice President of Product chez ThoughtSpot

### Transformer la connaissance en un actif d'entreprise cohérent avec Business Ontology

Les personnes changent de rôle, les outils sont remplacés et les modèles de données évoluent. Trop souvent, la connaissance qui les sous-tend se perd en chemin. Business Ontology transforme cette connaissance en un actif d'entreprise durable, avec un propriétaire responsable et un lien clair vers l'endroit où chaque définition est calculée. Chaque nouvel agent ou application peut partir de ce que l'entreprise sait déjà.

Si vous souhaitez approfondir Business Ontology, consultez notre atelier pratique et lisez notre article de blog « Meaning Before Metrics : How We Built a Governed Business Ontology for AI Agents ».

### Questions fréquentes

**Qu'est-ce que Snowflake Business Ontology ?**
Business Ontology (en preview publique prochainement) est une couche de modélisation métier et de gouvernance au sein de Snowflake Horizon Context. Les organisations peuvent l'utiliser pour définir des concepts métier, des métriques et les relations entre eux, indépendamment de tout modèle de données unique. Chaque définition enregistre son propriétaire et son statut d'approbation, et se relie aux vues sémantiques, tables et vues qui l'implémentent. Seules les définitions approuvées sont servies aux agents IA dans CoCo et CoWork, de sorte que les agents travaillent à partir du sens que l'organisation assume plutôt que de choisir parmi des implémentations concurrentes.

**Pourquoi les agents IA ont-ils besoin de contexte métier ?**
Un contexte métier gouverné aide les agents à interpréter les données comme le fait le métier, afin qu'ils puissent fournir des réponses plus précises. Les agents IA peuvent accéder aux données, mais ils ne « comprennent » pas automatiquement ce que signifient les termes métier ou comment les concepts se relient. Ils ont besoin de contexte : des références approuvées qui leur indiquent quelle définition privilégier, quelles politiques suivre et quelle connaissance d'entreprise intégrer. Sans ce contexte, les agents devinent les significations et les sources de données pertinentes et peuvent donner des réponses différentes à la même question.

**En quoi Business Ontology diffère-t-il des Semantic Views ?**
Business Ontology définit ce que signifie un terme métier, qui le possède et comment il se relie à d'autres concepts. Semantic Views définit comment chaque métrique est calculée, en regroupant métriques, dimensions et jointures dans des objets que les agents, outils BI et le SQL peuvent interroger directement. Business Ontology relie des métriques équivalentes entre différentes vues sémantiques à une définition partagée et approuvée unique.

**Les définitions métier peuvent-elles circuler entre Snowflake et d'autres outils ?**
Oui. Business Ontology peut importer et exporter des concepts métier, des définitions et des relations vers des formats ouverts, notamment Apache Ossie (incubating) et Resource Description Framework (RDF), afin que les équipes puissent réutiliser la connaissance métier approuvée dans d'autres outils plutôt que de la redéfinir. Les Semantic Views peuvent également importer et exporter des définitions Ossie, afin que les métriques n'aient pas à être reconstruites. Les agents extérieurs à Snowflake peuvent interroger les Semantic Views via le Model Context Protocol, avec Horizon Catalog gouvernant l'accès.

## Pourquoi ça compte
Cette annonce illustre une tendance de fond dans l'écosystème data/IA : la gouvernance sémantique devient le préalable indispensable à la fiabilité des agents IA en entreprise, et les acteurs de la BI (Snowflake, mais aussi Omni, Sigma, ThoughtSpot via des partenariats) convergent vers des standards ouverts (Apache Ossie, MCP) pour éviter le verrouillage propriétaire et la dérive sémantique entre outils.
