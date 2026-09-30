---
title: "State of agent skills"
date: 2026-09-30
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fvercel.com%2Fblog%2Fstate-of-agent-skills%3Futm_source=tldrai/1/010001a0ed56b287-90a62935-8940-46d3-9a4e-6d8f51356728-000000/3QtQvfP8QTFjUQIwMFUgQC4L0nTgf22n7RBCJ9z9TbQ=452"
keywords: ["agent skills", "skills.sh", "Vercel", "Anthropic", "adoption", "écosystème IA"]
theme: "IA"
tone: "research"
used_in: ["2026-09-30"]
---

## Résumé
En seulement sept mois, le registre skills.sh a atteint un million d'"agent skills" et près de 280 millions d'installations, une croissance bien plus rapide que celle de GitHub, de l'App Store ou de npm à leurs débuts. Un skill donne à un agent IA générique les instructions et le jugement propres à un métier, une entreprise ou une équipe, ce qui le rend plus rapide à produire qu'un logiciel classique. L'offre de skills est majoritairement technique (ingénierie logicielle, workflows d'agents, data, infra, sécurité), mais la demande est beaucoup plus diffuse et couvre toutes les fonctions de l'entreprise. Le rapport, basé sur les données agrégées de Vercel, anticipe que la prochaine vague de valeur viendra des skills propriétaires encodant un savoir-faire spécifique à chaque organisation.

## Points clés
- skills.sh est passé de 0 à 1 million de skills en 7 mois, contre 27 mois pour GitHub (1M repos), plus de 5 ans pour l'App Store et plus de 9 ans pour npm.
- L'offre de skills est dominée par le technique (ingénierie logicielle ≈ 25 % des annonces), mais la demande (installations) est bien plus répartie : ingénierie logicielle 18 %, workflows d'agents 15 %, opérations business et écriture ≈ 11 % chacune.
- Les skills de workflow/automatisation d'agents (planification, routage, usage d'outils) sont la 2e catégorie la plus installée, car ils s'appliquent transversalement à tous les métiers.
- L'installation est extrêmement concentrée : la moitié des skills n'ont été installés qu'une fois, tandis que 0,04 % des skills captent 62 % des installations — sans qu'aucun skill ne domine à plus de 1 %.
- 66 % des skills classés sont transversaux aux industries et captent 87,5 % des installations (3,6x plus d'installations par annonce que les skills spécifiques à une industrie).
- Le rapport prédit un basculement : l'expertise générale deviendra la norme, la valeur différenciante se déplacera vers le savoir propriétaire des entreprises, et la mesure de qualité passera de la popularité (installations) à l'efficacité mesurée (tests, benchmarks).

## Analyse approfondie
En sept mois, le registre skills.sh a atteint un million d'agent skills et enregistré près de 280 millions d'installations.

Un skill donne à un agent IA des instructions réutilisables pour une tâche particulière. Les agents sont compétents mais génériques ; ils peuvent accomplir de nombreuses tâches, mais ils ne savent pas comment une personne, une équipe ou une entreprise en particulier les réalise. Un skill fournit ce contexte manquant et peut être aussi simple qu'un fichier rédigé en langage courant.

Anthropic a introduit les Agent Skills en octobre 2025, et Vercel a lancé le registre skills.sh trois mois plus tard.

À partir des données agrégées du registre, ce rapport retrace les premiers pas de ce nouveau marché à travers son premier million de skills : ce que les gens enseignent aux agents, ce qui est installé, et où va la valeur.

### Les skills transforment l'expertise en logiciel

Pour écrire un skill, une partie du jugement qui sous-tend un métier doit être rendue explicite : les étapes à suivre, à quoi ressemble un bon résultat, et comment évaluer ce résultat. L'agent et ses outils fournissent déjà l'essentiel de la capacité sous-jacente, si bien que le skill n'a plus qu'à apporter le jugement et les instructions propres à une tâche.

Cela rend les skills plus rapides et plus faciles à créer que les logiciels classiques.

skills.sh a atteint un million de skills en sept mois. GitHub a mis 27 mois pour atteindre un million de dépôts. L'App Store d'Apple a mis un peu plus de cinq ans pour atteindre un million d'applications. npm a mis plus de neuf ans pour atteindre un million de packages.

Beaucoup plus de personnes savent décrire comment un travail doit être fait que programmer un ordinateur pour le faire. Et une fois qu'un skill est écrit, il peut être distribué et installé sans devoir être réécrit pour chaque agent. Les skills associent un bassin de créateurs bien plus large à la capacité de réutilisation propre au logiciel, ce qui alimente la croissance explosive de l'écosystème.

### Ce que les gens enseignent aux agents

Nous avons classé les skills les plus installés du registre selon le type de travail qu'ils aident les agents à accomplir. Ensemble, ces skills représentent plus des quatre cinquièmes de toutes les installations. Les annonces publiées montrent l'offre : ce que les auteurs ont mis à disposition des agents. Les installations montrent la demande : ce que les gens veulent que leurs agents apprennent.

L'offre penche vers le technique. Plus de la moitié des annonces enseignent l'ingénierie logicielle, les workflows d'agents, la data, l'infrastructure ou la sécurité, l'ingénierie logicielle représentant à elle seule environ un quart du total.

La demande est plus répartie. Aucune catégorie ne capte plus d'un cinquième des installations. L'ingénierie logicielle reste la plus importante avec 18 %, suivie par les workflows d'agents avec 15 %, puis les opérations business et l'écriture avec près de 11 % chacune.

Pour voir comment chaque catégorie performe par rapport à sa taille, nous avons aussi comparé ses installations par annonce à la moyenne.

Les opérations business, l'écriture et les documents, ainsi que le cloud et l'infrastructure obtiennent le plus d'installations par annonce. La demande pour ce type de travail est répartie sur moins de skills, si bien que chacun en capte une plus grande part. Le skill moyen d'opérations business attire 74 % d'installations de plus que la moyenne, celui d'écriture et de documents 50 % de plus, celui de cloud et infrastructure 42 % de plus.

L'ingénierie logicielle, l'éducation et la productivité, ainsi que la recherche fonctionnent à l'inverse. Le skill moyen d'ingénierie logicielle attire environ 30 % d'installations en moins que la moyenne, celui d'éducation et de productivité 39 % de moins, celui de recherche 55 % de moins.

Pour écrire un skill, il faut comprendre un métier. Pour en installer un, il suffit de vouloir que le travail soit fait. La plupart des skills sont techniques parce qu'ils sont nés dans les outils pour développeurs. Les installations couvrent un éventail bien plus large de travaux parce que les agents sont utiles dans chaque partie d'une entreprise.

### Les skills qui améliorent le fonctionnement des agents comptent parmi les plus installés

Les workflows d'agents et l'automatisation représentent 14,8 % des installations dans le jeu de données classé, juste derrière l'ingénierie logicielle. Parmi les annonces comptant au moins 100 000 installations, les workflows d'agents forment la plus grande catégorie.

Les skills de workflow et d'automatisation d'agents apprennent aux agents à planifier, répartir le travail, utiliser des outils et automatiser des navigateurs, des capacités qui s'appliquent à de nombreux métiers. Un skill de révision de contrats s'applique aux contrats, mais un skill de planification s'applique à n'importe quelle tâche que l'agent entreprend, contrats compris.

Les gens utilisent des agents pour améliorer les agents. Et comme les agents aident aussi à écrire des skills, le catalogue grandit en améliorant la machinerie même qui sert à le construire.

### Une poignée de skills capte la majorité des installations

L'activité d'installation est très concentrée. Près de la moitié de tous les skills n'ont été installés qu'une seule fois. À l'autre extrémité, 375 skills, soit 0,04 % du registre, représentent 62 % des installations, et le top 1,2 % représente 94 % des installations.

Malgré cette concentration, il n'y a pas de vainqueur unique. Même le skill le plus installé représente moins de 1 % de toutes les installations.

Les skills sont en concurrence au sein d'un même métier et s'accumulent d'un métier à l'autre. Une fois qu'une équipe a choisi un skill de notes de frais, elle n'a guère de raison d'en installer un autre pour la même tâche. Mais elle peut utiliser ce skill aux côtés d'autres, pour les tableurs, la recherche ou les présentations. Chaque métier couronne son propre vainqueur, et les vainqueurs réunis portent l'essentiel des installations.

### Sept installations sur huit vont à des skills qui fonctionnent dans toutes les industries

Nous avons aussi classé chaque skill selon que son travail était partagé entre industries ou spécifique à une seule. Des tâches comme nettoyer une feuille de calcul ou déployer un site web reviennent aussi bien dans les banques que dans les hôpitaux, les cabinets d'avocats ou les restaurants. Ces skills transversaux aux industries représentent 66 % des skills classés et 87,5 % des installations. En moyenne, ils reçoivent 3,6 fois plus d'installations par annonce que les skills spécifiques à une industrie.

L'avantage, c'est la portabilité, que ce soit à travers les métiers, comme les workflows d'agents, ou à travers les industries. Les skills les plus installés sont ceux que le plus grand nombre de personnes peuvent utiliser.

### La prochaine génération de skills

Le premier million de skills a appris aux agents ce que tout le monde sait. Le prochain million leur apprendra ce que vous seul savez.

Les skills publics et de meilleurs modèles rendent l'expertise générale accessible à toutes les équipes, ce qui en fera la norme plutôt qu'un avantage. Une plus grande part de la valeur différenciante se déplacera vers le jugement propre à chaque entreprise. Par exemple, savoir quand un client obtient un remboursement ou ce qui peut être livré sans passer par une nouvelle revue.

La mesure d'un skill passera aussi de la popularité à l'efficacité. Aujourd'hui, le meilleur signal de la qualité d'un skill est son nombre d'installations. À mesure que les modèles s'améliorent, la barre se relève, car un skill ne se justifie que si l'agent accomplit mieux la tâche avec lui que sans lui. Les skills auront des tests et des benchmarks qui mesureront exactement cela.

La première génération de skills a transformé l'expertise en logiciel. La prochaine génération verra le catalogue public continuer de croître à mesure que l'offre rattrape la demande. Et les organisations construiront par-dessus, consignant le savoir qu'elles sont seules à détenir et le maintenant de la même façon qu'elles maintiennent aujourd'hui leur code.

Explorez le premier million, ou contribuez au prochain, sur skills.sh.

### À propos de ce rapport

Ce rapport utilise des données agrégées de skills.sh. Quelques notes sur la méthodologie de mesure :

- Les totaux du catalogue comptent les annonces uniques du registre.
- Les chiffres d'installation utilisent les compteurs agrégés du registre. Ils ne représentent pas des personnes uniques ni nécessairement des choix indépendants.
- Les résultats par fonction et par industrie décrivent un échantillon classé plutôt que l'ensemble du catalogue.
- Chaque analyse utilise les données complètes les plus récentes disponibles. Les chiffres peuvent être révisés à mesure que les données sous-jacentes et la méthodologie s'améliorent.

## Pourquoi ça compte
Ce rapport donne l'un des premiers signaux quantitatifs sur l'adoption réelle des "agent skills", une brique clé de l'écosystème IA agentique lancée par Anthropic fin 2025 : il montre que la valeur ne restera pas dans les skills génériques largement partagés, mais migrera vers le savoir propriétaire que chaque organisation encodera elle-même, un signal important pour quiconque suit la structuration du marché des outils IA.
