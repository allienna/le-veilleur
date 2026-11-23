---
title: "Do Data Roles Have a Future?"
date: 2026-11-23
url: "https://open.substack.com/pub/joereis/p/do-data-roles-have-a-future?utm_source=multiple-personal-recommendations-email&utm_medium=email&token=eyJ1c2VyX2lkIjo0NzU1OTI2MjgsInBvc3RfaWQiOjIyNDk3MTg2NiwiaWF0IjoxNzk1MzcxMjQ2LCJleHAiOjE3OTc5NjMyNDYsImlzcyI6InB1Yi00NzIxNCIsInN1YiI6InBvc3QtcmVhY3Rpb24ifQ.jUEdSrYMn8Dqr60z6JGStVqZQ_9ZQI7O9zVLWIlEJI4"
authors: ["Joe Reis"]
keywords: ["data engineering", "IA générative", "rôles data", "automatisation", "data modeling", "organisation du travail"]
theme: "Data"
tone: "opinion"
used_in: ["2026-11-23"]
---

## Résumé
Joe Reis, coauteur de *Fundamentals of Data Engineering*, répond à la question récurrente : les métiers de la donnée ont-ils un avenir ? Sa thèse : oui, le cycle de vie de l'ingénierie des données perdure, mais le travail tactique quotidien (écrire du SQL, du dbt, du Python) devient rapide et bon marché à automatiser grâce à l'IA. Ce qui ne s'automatise pas, selon lui, c'est l'interprétation du contexte métier et la responsabilité des décisions — des problèmes sociotechniques, pas seulement techniques. Il anticipe un brouillage des rôles data (ingénieur, analytics engineer, analyste, data scientist, architecte, manager) vers une figure plus générique de « data practitioner », où l'exécution compte plus que le titre.

## Points clés
- Reis distingue trois dimensions du travail data : la **production** (coder, construire des pipelines/dashboards), l'**interprétation** (comprendre le sens métier des données, trancher des ambiguïtés) et l'**accountability** (assumer les décisions et les risques) — seule la première est massivement automatisée par l'IA.
- Une enquête 2026 citée montre un paradoxe : 80% des répondants utilisent l'IA quotidiennement, mais seuls 10% l'ont intégrée aux workflows organisationnels, et 89% peinent encore sur des problèmes basiques de modélisation des données.
- L'exemple du calcul de revenu (brut vs net, reconnu vs facturé) illustre que l'IA génère du code syntaxiquement correct mais ne résout pas l'ambiguïté sémantique métier — un problème humain, pas technique.
- Les rôles data convergent : ingénieurs vers l'architecture/fiabilité/coûts, analytics engineers vers la sémantique et les contrats de données, analystes vers les questions stratégiques, data scientists vers le design expérimental et l'inférence causale.
- Reis s'inquiète de la formation des juniors : si les tâches de code basiques sont automatisées, comment développeront-ils le jugement diagnostique qui vient traditionnellement de la pratique (coder, casser, réparer) ?
- Il prédit des équipes plus petites mais plus efficaces, une fluidité accrue entre rôles (au détriment des organigrammes rigides), et un besoin croissant de gouvernance et de traçabilité des données à mesure que des agents autonomes deviennent eux-mêmes producteurs et consommateurs de données.

## Analyse approfondie
Reis structure son argument autour d'un déplacement de la valeur économique dans le travail data. Historiquement, la rareté et le coût de production des « artefacts techniques » (code, pipelines, dashboards, documentation) justifiaient des équipes importantes de spécialistes. L'IA générative fait chuter ce coût de production de façon spectaculaire — il affirme ne plus connaître personne qui écrive du code « à la main » au sens traditionnel. Mais il insiste : produire un artefact n'est pas résoudre un problème métier. C'est pourquoi il découpe le travail data en trois strates — production, interprétation, accountability — et soutient que seule la première s'effondre en coût, les deux autres restant fondamentalement humaines et organisationnelles.

Il illustre ce point avec le cas classique du calcul de revenu : une IA peut produire du code impeccable, mais ne peut pas arbitrer seule si « revenu » signifie brut ou net, reconnu ou facturé. Sans clarté sémantique et modélisation solide en amont, l'automatisation ne fait qu'accélérer la production d'une logique métier erronée — ce qui n'est pas forcément négatif selon lui, car cela permet de détecter les erreurs plus vite, mais cela ne dispense pas de résoudre l'ambiguïté humaine sous-jacente. Il relie cela à l'échec récurrent des projets IT sur plusieurs décennies : la dimension sociotechnique du travail reste intrinsèquement complexe.

Sur l'évolution des rôles, Reis esquisse une trajectoire pour chaque fonction : les ingénieurs data passeraient de la plomberie manuelle de pipelines à la conception système, la fiabilité et la gestion des coûts ; les analytics engineers délaisseraient la production de modèles dbt/SQL pour se concentrer sur la sémantique métier et les contrats de données ; les analystes évolueraient du reporting statique vers des questions stratégiques et l'analyse de cas limites ; les data scientists délègueraient la modélisation standard à l'IA pour se concentrer sur le design expérimental et l'inférence causale ; les architectes prendraient une vue macro sur des environnements complexes incluant knowledge graphs et workflows agentiques ; les managers devraient rester techniquement impliqués tout en pilotant des équipes plus réduites mais plus productives.

Cette convergence des rôles, qu'il observait déjà il y a un an et qu'il voit s'accélérer, donnerait naissance à des généralistes polyvalents plutôt qu'à des spécialistes de fonction — sauf dans des niches de spécialisation profonde (systèmes distribués, performance, sécurité) qui resteraient recherchées. Les titres de poste rigides perdraient en pertinence au profit de la capacité réelle à exécuter.

Reis exprime une inquiétude particulière pour la formation des ingénieurs juniors : la séniorité technique s'est historiquement construite par la pratique directe (écrire, casser, réparer du code), un apprentissage qui risque de disparaître si les tâches d'entrée de gamme sont entièrement automatisées. Il appelle les entreprises à créer délibérément des parcours permettant aux jeunes ingénieurs de développer un vrai jugement diagnostique, plutôt que d'accepter passivement les suggestions de l'IA.

Il conclut sur quatre tendances : des équipes plus petites mais plus percutantes ; une fluidité croissante entre rôles qui bouleverse les organigrammes traditionnels ; l'émergence d'agents autonomes agissant à la fois comme producteurs et consommateurs de données, ce qui va exiger plus de gouvernance, de traçabilité (lineage) et de cohérence sémantique ; et une importance égale, voire supérieure, accordée à la validation et à l'évaluation du code généré par rapport à sa simple écriture. Pour lui, la question centrale de l'industrie devient : quelle valeur les professionnels de la donnée apportent-ils quand produire du code n'est plus le facteur limitant ? Sa réponse passe par un retour aux fondamentaux, une refonte des compétences et le renforcement des réseaux professionnels.

## Pourquoi ça compte
Ce témoignage d'un auteur de référence en ingénierie des données capture un débat central de la veille tech actuelle : la bascule de la valeur depuis la production de code automatisable vers l'interprétation sémantique et la responsabilité humaine, avec des implications concrètes sur l'organisation des équipes, la formation des juniors et la définition même des métiers data face à l'IA générative.
