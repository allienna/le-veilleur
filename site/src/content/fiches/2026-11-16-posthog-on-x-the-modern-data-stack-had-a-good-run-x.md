---
title: "PostHog on X: \"The modern data stack had a good run\" / X"
date: 2026-11-16
url: "https://substack.com/redirect/89adb543-899e-4c37-b948-703113286fd6?j=eyJ1IjoiN3Y1bG1jIn0.HlvPOGYPdVknSYzEK1JIj6IFkAFn8zuyjtfU9Mbft9Q"
authors: ["PostHog"]
keywords: ["modern data stack", "Fivetran", "dbt Labs", "rebundling", "ELT", "pricing"]
theme: "Data"
tone: "opinion"
used_in: ["2026-11-16"]
---

## Résumé
Le 1er juin 2026, Fivetran et dbt Labs ont finalisé leur fusion, réunissant deux acteurs emblématiques du « modern data stack » sous une même direction et environ 600 millions de dollars de revenus combinés. PostHog analyse ce rapprochement comme le signe d'un mouvement plus large de « rebundling » : après des années d'éclatement de la chaîne data en outils spécialisés (ingestion, modélisation, orchestration, reverse ETL, observabilité, catalogues...), le marché se recompose autour de quelques plateformes qui cherchent à couvrir toutes les couches. L'article retrace les causes de ce basculement — hausse des taux d'intérêt, pression sur les budgets, fatigue liée à la multiplication des outils — puis détaille comment Fivetran et les grands entrepôts cloud (Snowflake, Databricks) rachètent des briques complémentaires pour verrouiller leurs clients. Il se conclut par des recommandations pratiques pour rester maître de ses choix face à cette consolidation.

## Points clés
- Fivetran et dbt Labs ont achevé leur fusion le 1er juin 2026, symbolisant la fin de l'ère de l'« unbundling » du data stack entamée vers 2021.
- La hausse des taux de la Fed à partir de 2022 (plus de 5 % mi-2023) a poussé les entreprises à rationaliser leurs piles d'outils data pour réduire les coûts.
- Une enquête auprès de 232 responsables data (fin 2024) montre que 70 % jonglent avec 5 à 10 outils, 85 % jugent l'intégration de ces outils comme un défi majeur, et 63 % passent plus d'un cinquième de leur temps à maintenir les pipelines.
- Fivetran a racheté en un peu plus d'un an Census (reverse ETL, mai 2025), Tobiko Data/SQLMesh (septembre 2025) et dbt Labs (annoncé octobre 2025, finalisé juin 2026), couvrant quasiment toute la chaîne sauf le compute.
- Les entrepôts cloud élargissent aussi leur périmètre : Snowflake avec Openflow (ingestion basée sur Apache NiFi, juin 2025) et le rachat de Crunchy Data (~250 M$), Databricks avec Lakeflow Connect et le rachat de Neon, service Postgres serverless (~1 Md$, mai 2025).
- PostHog positionne son propre outil ELT comme une alternative « sans verrouillage », avec synchronisation historique gratuite les 7 premiers jours et une tarification au volume dégressive.

## Analyse approfondie

### Une consolidation qui clôt un cycle
La fusion entre Fivetran et dbt Labs, achevée début juin 2026, met fin à une période où l'on pouvait assembler librement son propre data stack en choisissant le meilleur outil pour chaque couche. Les deux sociétés, qui dominaient chacune leur segment, se sont désormais associées sous une direction commune et pèsent ensemble environ 600 millions de dollars de revenus. Si certains acteurs du marché — Fivetran lui-même, mais aussi Matillion ou Hightouch — ont qualifié cet événement de « mort du modern data stack », PostHog nuance ce diagnostic : les catégories logicielles suivent un cycle classique de fragmentation puis de recomposition, et le secteur de la donnée est simplement arrivé à cette étape de « rebundling ». La question centrale n'est plus de savoir si la consolidation aura lieu, mais qui détiendra le pack d'outils regroupés et à quel point les entreprises y seront enfermées.

### Retour sur l'essor du modern data stack
L'éclatement de la chaîne data avait du sens en 2021 : l'arrivée d'entrepôts cloud à coût de stockage très faible a permis aux équipes de charger toutes leurs données avant de les transformer, selon le modèle ELT (Extract, Load, Transform), qui a favorisé une architecture modulaire. Autour de l'ingestion se sont ensuite développées des couches dédiées à la modélisation, l'orchestration, le reverse ETL, l'observabilité, les catalogues de données, les couches sémantiques et les métriques — chacune portée par une vague de startups, dont les leaders se sont progressivement imposés au cours des cinq dernières années. Ce modèle reposait sur un mécanisme vertueux : chaque outil générait du calcul facturé sur l'entrepôt, et les équipes commerciales des entrepôts cloud se chargeaient ensuite de vendre l'ensemble aux clients — plus l'entrepôt vendait, plus les autres outils de la chaîne croissaient rapidement. Mais à partir de 2022, la Réserve fédérale américaine a relevé ses taux pour lutter contre l'inflation, dépassant 5 % mi-2023. Le financement en capital-risque a chuté nettement par rapport à son pic de 2021, et les investisseurs ont commencé à privilégier l'efficacité plutôt que la croissance. Les directions financières se sont alors mises à questionner le retour sur investissement de chaque outil et à chercher des opportunités de suppression ou de consolidation vers des solutions uniques, moins coûteuses.

### La fragmentation, source d'épuisement pour les équipes data
L'entreprise Modern Data Company a interrogé 232 responsables data seniors fin 2024 : 70 % d'entre eux jonglaient quotidiennement avec cinq à dix outils, 85 % plaçaient l'intégration de ces outils parmi leurs trois principaux défis, et 63 % consacraient plus d'un cinquième de leur temps à la maintenance des pipelines. Ce constat prend un relief particulier si l'on considère la taille des équipes concernées : l'enquête communautaire de Metabase révèle que la plupart des équipes data comptent seulement une à trois personnes, même dans de grandes entreprises. Cette même enquête montre aussi que les utilisateurs jugent généralement mieux chaque outil pris isolément que l'ensemble de leur pile — preuve que chaque brique fonctionne bien individuellement, mais que la maintenance des intégrations entre elles reste un casse-tête permanent. La tarification aggrave encore cette complexité : chaque outil facture selon une métrique différente (lignes, crédits, sièges, exécutions de modèles), rendant impossible toute prévision budgétaire fiable et provoquant régulièrement des factures surprises.

### Une recomposition venue de deux fronts
Le mouvement de rebundling se déploie aujourd'hui selon deux dynamiques parallèles.

**1. Des fournisseurs individuels qui rachètent des couches entières de la chaîne.** Fivetran en est l'exemple le plus marquant : en environ 13 mois, l'entreprise a assemblé la quasi-totalité des couches du data stack, à l'exception du calcul pur.
- **Mai 2025 :** rachat de Census, outil de reverse ETL, désormais intégré sous le nom Fivetran Activations.
- **Septembre 2025 :** rachat de Tobiko Data, société à l'origine de SQLMesh.
- **Octobre 2025 :** annonce de la fusion avec dbt Labs, finalisée en juin 2026.

**2. Les entrepôts cloud qui élargissent leur offre.** Snowflake a lancé Openflow en juin 2025, un service d'ingestion natif construit sur Apache NiFi. Databricks dispose de son côté de Lakeflow Connect, ses propres connecteurs pour applications SaaS et bases de données. Les deux géants se sont ensuite attaqués aux bases de données applicatives elles-mêmes : Databricks a racheté Neon, société de Postgres serverless, pour environ un milliard de dollars en mai 2025 ; trois semaines plus tard, Snowflake a racheté Crunchy Data pour environ 250 millions de dollars.

Les deux camps cherchent ainsi à posséder chaque couche de la pile data. Une fois qu'un fournisseur contrôle l'ensemble, quitter son écosystème implique de tout reconstruire — ce qui transforme le client en otage, contraint d'accepter n'importe quelle condition de renouvellement.

### Une simplification qui ne devrait pas s'accompagner de pièges
PostHog affirme apprécier le principe du rebundling : moins de contrats, moins de nuits passées à chercher quel outil est tombé en panne, et la fin des changements de contexte permanents entre cinq outils différents. Mais la question posée est celle du prix à payer : une pile plus simple peut aussi devenir plus difficile à quitter. Selon PostHog, il devrait être possible de réduire le nombre d'outils sans pour autant s'engager sur une plateforme complète et payer pour des fonctionnalités non désirées incluses dans le contrat. C'est la philosophie revendiquée de leur propre outil ELT : il synchronise les données vers l'entrepôt déjà utilisé par le client, ou vers l'entrepôt propre de PostHog si l'entreprise n'en possède pas, avec la possibilité d'ajouter ultérieurement une destination ELT vers son propre entrepôt (ce qui déclenche une resynchronisation complète facturée au nombre de lignes, à anticiper en vérifiant ses volumes). L'outil ne nécessite aucun autre produit PostHog pour être utilisé. Côté tarification, les synchronisations historiques sont gratuites durant les sept premiers jours après connexion d'une nouvelle source (jusqu'à 100 millions de lignes en offre gratuite, sans limite en offre payante), le premier million de lignes mensuel est gratuit, puis le tarif est de 0,000015 $ par ligne, dégressif jusqu'à 0,000001 $ au-delà d'un certain volume, sans minimum par connexion.

### Rester maître de ses choix face au rebundling
PostHog propose cinq recommandations pour garder une marge de manœuvre dans un marché où l'on subit souvent le regroupement d'outils sans l'avoir choisi :
1. **Lire attentivement son renouvellement de contrat :** les regroupements d'offres changent les grilles tarifaires. Fivetran est passé à une facturation par connexion en mars 2025, puis a ajouté un minimum de 5 $ par connexion en janvier 2026 ; les suppressions et les changements de mode d'historisation comptent désormais aussi comme des lignes facturables.
2. **Compter combien d'outils sont nécessaires pour obtenir une réponse :** choisir une question récurrente et en tracer le parcours de la source jusqu'à la réponse ; chaque outil traversé coûte du temps, de l'argent, ou les deux.
3. **Préserver une porte de sortie :** privilégier les formats ouverts et les outils que l'on pourrait héberger soi-même. Fivetran et dbt Labs affirment que dbt Core restera open source sous sa licence actuelle — il convient de vérifier ce point pour chaque dépendance.
4. **Chiffrer le coût d'une sortie avant d'adopter un nouvel outil :** si la réponse implique une migration de six mois, elle ne sera jamais réalisée, et l'entreprise continuera simplement à subir les hausses de prix.
5. **Simuler un mois difficile :** la tarification au volume de lignes rend la facture mensuelle imprévisible — backfills, changements de schéma et tables à forte volatilité peuvent tous peser sur la note. Modéliser le pire scénario permet d'éviter les mauvaises surprises.

### Choisir son camp délibérément
PostHog conclut que, le marché évoluant vers le rebundling, il n'est pas possible d'y échapper totalement — mais il reste possible de choisir consciemment dans quel écosystème on s'installe. L'entreprise met en avant son propre outil ELT comme une option permettant de conserver une pile « interchangeable », notamment grâce à la possibilité de reconstituer son historique de données en parallèle de son outillage existant, sans frais sur ces lignes historiques pendant les sept premiers jours.

## Pourquoi ça compte
Ce mouvement de consolidation redessine les rapports de force dans l'écosystème data : les équipes techniques doivent désormais évaluer leurs choix d'outils non plus seulement sur la fonctionnalité, mais sur le risque de dépendance à long terme envers une plateforme intégrée. C'est un signal à suivre pour quiconque pilote une architecture data ou négocie des contrats avec Fivetran, Snowflake ou Databricks.
