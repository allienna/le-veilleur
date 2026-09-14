---
title: "From Data Engineer To ?? Engineer"
date: 2026-09-14
url: "https://open.substack.com/pub/juhache/p/from-data-engineer-to-engineer?utm_source=multiple-personal-recommendations-email&utm_medium=email&token=eyJ1c2VyX2lkIjo0NzU1OTI2MjgsInBvc3RfaWQiOjIwNzc1Njk3NSwiaWF0IjoxNzg5MzMxNTU4LCJleHAiOjE3OTE5MjM1NTgsImlzcyI6InB1Yi0xMjExOTgxIiwic3ViIjoicG9zdC1yZWFjdGlvbiJ9.UHqaYEUXf2tI94mGoUK0NVycdcwXBaqsIc1g2Ff9DNc"
authors: ["Ju (Julian)"]
keywords: ["data engineering", "agents IA", "DevOps", "DuckDB", "vibe coding", "data warehouse"]
theme: "Data"
tone: "opinion"
used_in: ["2026-09-14"]
---

## Résumé
L'auteur, data engineer expérimenté, observe une transformation profonde de son métier sous l'effet de l'IA générative et des agents de codage. Les demandes des utilisateurs se simplifient : ils veulent désormais la donnée brute plutôt que des dashboards finis, ce qui réduit le périmètre du data engineer à celui d'un « landing engineer ». En parallèle, le métier se rapproche du DevOps (sandboxes cloud, gouvernance LLM, contrôle des coûts) et du software engineering, puisque les utilisateurs demandent aussi de mettre en production leurs prototypes vibe-codés. L'auteur invite les data engineers à choisir entre spécialisation technique poussée ou polyvalence DevOps-data-software, la maîtrise du codage agentique devenant incontournable dans les deux cas.

## Points clés
- Les consommateurs de données ne demandent plus des dashboards ou des mart tables, mais la donnée brute qu'ils transforment eux-mêmes via des agents comme Claude ou Codex (« vibe coding »).
- Le rôle du data engineer se réduit à l'ingestion et au nettoyage minimal au niveau le plus granulaire (« landing engineer »), les entrepôts cloud comme Snowflake ou Databricks ne servant plus qu'au stockage et au contrôle d'accès.
- Une architecture plus légère et moins coûteuse émerge : tables Parquet partitionnées, Iceberg/DuckLake, transformations via DuckDB.
- Le data engineering se décentralise : utilisateurs et équipes internes construisent leurs propres pipelines via des agents, pendant que le data engineer devient fournisseur d'infrastructure (sandboxes, gouvernance LLM, coûts) — un rôle qualifié à 90 % de DevOps.
- Une nouvelle étape se dessine : les utilisateurs demandent de mettre en production des applications prototypées en vibe-coding, poussant le data engineer vers le software engineering.
- Deux trajectoires de carrière se profilent : la spécialisation technique pointue (streaming, Iceberg) ou le profil généraliste maîtrisant tout le cycle data-DevOps-software.

## Analyse approfondie
Mon post le plus populaire de tous les temps s'intitule : *From Data Engineer to YAML Engineer* (« De Data Engineer à YAML Engineer »).

- From Data Engineer to YAML Engineer, 22 novembre 2023
- From Data Engineer to YAML Engineer, Part II, 22 avril 2025

Près de trois ans après le post initial, je dois admettre que je n'ai aucune idée de la direction que prend ce métier désormais.

Plutôt que de faire une nouvelle prédiction, je vais simplement partager ce que j'observe actuellement sur mes projets et chez mes clients.

### Partie I : De Data Engineer à Landing Engineer

Une chose que j'ai remarquée, c'est à quel point les attentes des consommateurs de données ont changé.

Avant, ils demandaient des dashboards, des mart tables propres, et une couche entièrement modélisée prête à être consommée en BI.

Aujourd'hui, la seule exigence est souvent : « donnez-moi juste la donnée brute ».

Les gens ont Claude, Codex, et des outils similaires.

Ils vibe-codent leur chemin jusqu'au dernier kilomètre... et honnêtement, ça marche bien.

D'où le landing engineer.

Sur de nombreux projets, le rôle du data engineer se rétrécit considérablement : récupérer les données depuis diverses sources, les déposer (« landing ») au niveau de granularité le plus fin possible, et effectuer un peu de nettoyage inter-sources.

Et c'est tout. Ajoutez la documentation du schéma sous forme de fichiers Markdown, et vos utilisateurs sont prêts.

Oui, vous pouvez optimiser le modèle de données au fil du temps en fonction des usages réels.

Oui, il faut toujours gérer le contrôle d'accès et d'autres enjeux de gouvernance.

Mais comparé aux plateformes de données que nous construisions il y a quelques années, le travail à accomplir s'est nettement réduit.

Et, au passage, cela change notre façon de penser les outils.

Dans ce nouveau modèle, les entrepôts de données cloud comme Snowflake et Databricks ne servent principalement plus qu'à deux choses :

- le stockage de la couche de landing
- le contrôle d'accès

Et c'est une technologie plutôt coûteuse pour un ensemble de fonctionnalités aussi limité.

Mon approche de prédilection est désormais plus simple pour les petits projets : déposer les données dans des tables Parquet partitionnées (ou Iceberg/DuckLake si l'on veut faire les malins), exécuter quelques transformations DuckDB pour nettoyer les données au niveau de granularité le plus fin possible, et c'est tout.

Vos consommateurs sont contents. Votre CFO est content.

### Partie II : De Data Engineer à DevOps Engineer

Mon sentiment est que le data engineering se décentralise.

Un data engineer produit des artefacts centraux, tandis que les utilisateurs et équipes internes construisent leurs propres pipelines pour combiner les sources et effectuer des transformations spécifiques.

Pour que cette nouvelle ère fonctionne, un nouveau type d'infrastructure doit émerger au sein des entreprises : des agents de data engineering décentralisés.

Les gens veulent utiliser des agents de codage pour construire leurs dashboards, et ils devraient pouvoir le faire.

Notre rôle en tant que data engineers est de nous assurer qu'ils le peuvent.

Cela implique de mettre en place :

- des sandboxes cloud pour les agents
- du stockage de données (bucket)
- de la gouvernance LLM et du contrôle des coûts
- des compétences et bonnes pratiques de data engineering

Et je crains de devoir dire que c'est à 90 % un travail de DevOps...

Donc oui, les DevOps engineers sont en quelque sorte les nouveaux data engineers (ou peut-être l'inverse ?).

Le seul aspect dont je ne suis pas sûr, c'est la façon dont les artefacts créés dans une sandbox devraient être partagés.

Si l'artefact est une définition de métrique, c'est plutôt facile : on peut construire une sorte de couche sémantique ou de catalogue centralisé.

Mais vous voyez où cela mène : et si l'artefact était une application ?

### Partie III : De Data Engineer à Software Engineer

Voici un pattern que je vois très souvent chez mes clients : les gens ont accès à la donnée, à un agent, et à une sandbox.

Alors quelle est la suite logique ?

Construisons une app et partageons-la !

Je vous épargne le mème du localhost, mais vous voyez l'idée.

En tant qu'ingénieur, vous aurez des utilisateurs qui vous jetteront leurs prototypes affreux à la figure :

« OK, mets juste mon prototype Claude Code en production, s'il te plaît.

Ça m'étonnerait que ça prenne plus d'une heure de travail...

Pas vrai ?

Paaas vrai ? »

### Comment se préparer ?

Je pense que la meilleure façon de se préparer est de choisir entre creuser en profondeur (« go deep ») et s'élargir (« go wide ») :

- **Go deep :** Choisissez un sujet d'infrastructure et devenez spécialiste du streaming, d'Iceberg, ou de quelque chose d'aussi complexe (vous finirez probablement par travailler pour un éditeur de logiciels).
- **Go wide :** Devenez un DevOps-data-software engineer capable de posséder l'ensemble du parcours au sein d'une entreprise.

Dans les deux cas, une compétence devient incontournable : maîtriser le codage agentique dans les règles de l'art...

Merci de m'avoir lu.

Ju

---

*Réactions de lecteurs :*

Je suis d'accord, mais c'est surtout vrai pour les équipes data déjà bien avancées. Tout reste encore à construire pour la majorité des équipes data, et des choses passionnantes peuvent désormais être réalisées avec un peu d'imagination et des tokens : rendre sa plateforme « AI ready » (migration et modernisation vers des stacks de données plus agent-friendly, construction/curation de contexte, mise en place de cet espace de travail DE distant, pipeline factory mise entre les mains des utilisateurs finaux, design systems de dashboards et registre d'artefacts). On parle beaucoup d'IA pour la donnée, mais je pense que les entreprises auront aussi besoin de donnée pour l'IA (comprendre les blocages opérationnels, savoir où sont dépensés les tokens, car cela finira par représenter une ligne de coût énorme). Il n'y a jamais eu de meilleur moment pour être data engineer, gardez la foi 🦡

« Comment se préparer ? Je pense que la meilleure façon de se préparer est de choisir entre creuser en profondeur et s'élargir. »

Bonjour Julian,

Voici mon conseil aux meilleurs architectes de data warehouse au monde.

Si vous voulez diriger votre propre entreprise et vendre vos propres produits ?

Alors construisez un mega model pour un système sur lequel vous avez une grande expérience, puis construisez des applications analytiques par-dessus ce mega model. Ensuite, vendez l'usage de ce mega model dans le cloud ou on premise.

Les meilleurs architectes de data warehouse pourront ainsi prendre une longueur d'avance sur le marché, et ils gagneront très bien leur vie en exploitant un tel produit. Ils pourront bâtir leur entreprise avec des équipes pour accompagner ces clients.

Si vous voulez simplement revendre les mega models de quelqu'un d'autre et toucher une marge sur la vente pour ne pas avoir à faire le travail vous-même ? Alors vous pouvez vendre les mega models d'autres personnes. Cela comporte le risque de vous voir écarté de votre rôle commercial à l'avenir. Vous ne devriez donc vendre que les mega models d'hommes honnêtes, comme moi.

Voilà mon conseil sur la façon de se préparer à ce qui arrive. Le data warehouse construit en interne va suivre le même chemin que les systèmes opérationnels construits en interne. Les Mega Models sont les « ERP » de la business intelligence.

Aujourd'hui, cela n'a absolument aucun sens de construire un data warehouse from scratch. Toute entreprise qui fait cela gaspille énormément d'argent pour un ROI très incertain.

## Pourquoi ça compte
Ce témoignage de terrain illustre concrètement comment les agents de codage redistribuent les rôles entre data, DevOps et software engineering, un signal utile pour anticiper l'évolution des compétences et de l'organisation des équipes data à l'ère de l'IA générative.
