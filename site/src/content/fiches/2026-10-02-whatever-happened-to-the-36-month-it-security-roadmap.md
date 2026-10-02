---
title: "Whatever happened to the 36-month IT security roadmap?"
date: 2026-10-02
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.csoonline.com%2Farticle%2F4228518%2Fwhatever-happened-to-the-36-month-it-security-roadmap.html%3Futm_source=tldrit/1/010001a0f767d964-2ab46dd6-3d81-4d41-83b1-af7ba708d553-000000/OeRN-4SxV_84L4uiLTpypIwpvMKCGEEeBVRwxd1bWHI=452"
keywords: ["CISO", "feuille de route", "cybersécurité", "IA", "gouvernance", "agilité"]
theme: "Sécurité"
tone: "news"
used_in: ["2026-10-02"]
---

## Résumé

L'article explore comment les CISO abandonnent progressivement la feuille de route de sécurité fixe sur 2-3 ans au profit d'une planification à deux vitesses : les engagements stratégiques majeurs (conformité, architecture) restent pensés sur le long terme, tandis que les outils et tactiques sont révisés mensuellement, hebdomadairement, voire en temps réel. Cette évolution est portée par la vitesse d'adoption de l'IA en entreprise (agents, identités non humaines, « shadow AI ») qui rend obsolète toute planification figée. Plusieurs RSSI (Insight Global, Grafana Labs, Fable Security, AIVONS) témoignent de ce passage à une gouvernance continue plutôt qu'à un cycle annuel de validation.

## Points clés

- Les RSSI interrogés bifurquent leurs feuilles de route : principes et paris d'architecture majeurs sur plusieurs années, outils et tactiques revus en continu (mensuel, hebdomadaire, voire instantané).
- L'adoption rapide de l'IA par les employés et l'essor des identités non humaines (agents IA, comptes de service) obligent les équipes sécurité à réagir bien plus vite que ne le permettait un cycle annuel.
- Selon l'enquête Gartner 2026 (plus de 1 000 RSSI), l'agilité se définit désormais comme la capacité à reprioriser rapidement feuilles de route et investissements face aux risques métier changeants.
- D'après le KPMG 2026 Cybersecurity and Technology Risk Survey (310 responsables sécurité, entreprises à plus d'1 milliard de dollars de revenus), les attaques pilotées par IA devraient devenir la principale menace cyber dans les deux à trois prochaines années ; 42 % des responsables sécurité disent avoir du mal à démontrer le retour sur investissement de la cybersécurité à leur conseil d'administration.
- Les décisions sur l'horizon temporel d'un projet reposent sur deux critères chez Fable Security : l'ampleur de la coordination nécessaire et le lien direct avec un engagement stratégique déjà pris par l'entreprise.
- La gouvernance évolue d'une logique de conformité ponctuelle (validation unique, checklist) vers une discipline de communication continue avec le conseil d'administration, qui veut désormais des preuves concrètes (ce qui tourne, qui est responsable, ce qui peut atteindre les données sensibles) plutôt que de simples assurances.

## Analyse approfondie

John Dickson, RSSI d'Insight Global, illustre un problème devenu commun : les employés adoptent les outils d'IA plus vite que son équipe sécurité ne peut les cartographier, tandis que de nouveaux agents IA et intégrations de services se propagent dans l'environnement. Son équipe avait prévu de construire une visibilité sur ces identités non humaines (comptes de service, agents IA) — mais seulement un an plus tard. Dickson n'a pas attendu : il a fait développer immédiatement des capacités de découverte, d'observabilité, de contrôle et de reporting sur l'IA, assorties d'une fonction transverse d'assurance IA qu'il qualifie de « Department of Know » plutôt que de « Department of No » (service qui éclaire plutôt que service qui interdit). Désormais, son équipe réévalue formellement sa stratégie chaque trimestre à l'aune des évolutions de la menace et de l'activité de l'entreprise, repoussant l'horizon de trois mois à chaque fois. Pour lui, une revue annuelle revient à décider sur la base d'hypothèses potentiellement vieilles d'un an, alors qu'une cadence trimestrielle garde la stratégie ancrée dans le présent.

Cette logique n'est plus propre à un cycle annuel revisité une fois par an : selon l'enquête Gartner 2026 auprès de plus de 1 000 RSSI, l'agilité des responsables sécurité et risque se définit justement par leur capacité à reprioriser rapidement feuilles de route et investissements en fonction des risques métier changeants. Les RSSI les plus avancés scindent donc leurs feuilles de route traditionnelles de deux-trois ans en deux rythmes : les principes, engagements de conformité et grands paris d'architecture restent planifiés sur plusieurs années, tandis que les outils et pratiques quotidiennes sont révisés au mois, à la semaine, voire dans l'instant.

Chris Cochran, RSSI de terrain et vice-président sécurité IA au SANS Institute, décrit un climat d'incertitude inédit : « Nous opérons avec une incertitude plus réelle qu'à aucun moment dont je me souvienne », estimant que dans ce contexte la flexibilité intellectuelle devient un avantage concurrentiel décisif.

**Quand le trimestre devient trop lent**

Chez Grafana Labs, des agents IA développés par des « citizen developers » ont commencé à révéler des mauvaises configurations et des contrôles incomplets que personne n'avait repérés. Le RSSI Joe McManus n'a pas pu attendre le prochain cycle annuel pour réagir : « Si vous demandez à un agent de faire quelque chose, il va tout essayer pour atteindre cet objectif. » Ces découvertes ont conduit McManus à ajouter des audits de contrôle et une segmentation système à la feuille de route de l'entreprise — deux éléments absents du plan quelques mois plus tôt.

Pour McManus, planifier au-delà d'un an relève presque de l'illusion, tant le paysage change vite, notamment avec une IA désormais peu coûteuse et accessible à presque tout le monde. À ses yeux, la sécurité cloud est globalement un problème résolu ; les véritables zones d'incertitude concernent le « shadow AI », le « shadow code » et les intégrations que les développeurs créent de leur propre initiative. Grafana conserve néanmoins une « carte d'objectifs » sur deux ans, dont la seconde année est reprioritisée au gré des évolutions de la menace. L'équipe a abandonné les longues campagnes de modélisation des menaces avec revues de code complètes, au profit de sprints tactiques hebdomadaires bouclés en six semaines. Pour McManus, la sécurité n'a pas d'état final.

Cochran, du SANS Institute, résume : « Le luxe d'un plan fixe sur trois ans, qu'on établit puis qu'on oublie, a disparu. » Les RSSI doivent désormais produire des réponses trimestre après trimestre, et de plus en plus dans l'instant, sous l'effet cumulé de l'IA, de la vitesse des attaquants, des cycles budgétaires et de la pression des conseils d'administration.

Chez Fable Security, startup spécialisée dans la gestion du risque humain, la revue de sécurité suivait autrefois un processus linéaire : conception produit, revue par la sécurité et l'ingénierie, développement, nouvelle revue sécurité/QA, puis mise en production. Cette séquence a disparu, explique le RSSI Jacob Berry : la sécurité travaille désormais en parallèle de l'ingénierie à mesure que les fonctionnalités sortent plus vite pour suivre le marché. Les points de contrôle n'ont pas disparu, mais l'approche est passée d'un contrôle des équipes à un accompagnement de celles-ci.

Raja Chris, ex-RSSI d'Annaly Capital Management et fondateur-PDG d'AIVONS (société de gouvernance IA), observe que les meilleurs outils de sécurité actuels fonctionnent désormais comme des systèmes vivants, détectant et répondant en continu aux nouvelles expositions plutôt que d'attendre la prochaine revue planifiée — et que l'approche des RSSI en matière de stratégie et de feuille de route devrait suivre la même logique.

**Là où la vision à long terme garde sa place**

Malgré tout, de nombreux responsables sécurité continuent de construire des feuilles de route pluriannuelles pour des menaces comme l'informatique quantique, tout en anticipant que les attaques pilotées par IA deviendront la principale menace cyber dans les deux à trois prochaines années, selon le KPMG 2026 Cybersecurity and Technology Risk Survey mené auprès de 310 responsables sécurité d'entreprises dépassant le milliard de dollars de revenus.

Chez Insight Global, la catégorie long terme inclut des engagements sur la gouvernance des données, la modernisation de la plateforme centrale et la croissance internationale — un plan d'entreprise que suit le calendrier de l'équipe de Dickson. Chez Fable Security, l'équipe de Berry produit toujours un document à long terme, qu'il décrit davantage comme « un plan de direction et d'allocation de ressources qu'une feuille de route technique ».

Il n'existe pas de règle stricte sur la durée idéale d'une feuille de route, note Cochran du SANS Institute : les plans à long horizon portent généralement sur la conformité, les engagements métier, ou les grandes migrations IA et infrastructure — mais même ceux-ci ne sont pas à l'abri d'un bouleversement. Un changement de budget ou de soutien exécutif peut faire dérailler une feuille de route de deux ans du jour au lendemain.

**Déterminer ce qui va où**

Choisir dans quelle catégorie placer un projet donné n'est pas laissé au hasard, précise Berry. Son équipe pose deux questions à chaque initiative : combien de personnes devront être impliquées pour la mener à bien, et dans quelle mesure est-elle directement liée à un engagement stratégique déjà pris par l'entreprise ? Les travaux nécessitant une large coordination et directement rattachés à un engagement établi reçoivent l'horizon long ; les travaux plus restreints et autonomes sont traités dans le même cycle de révision continue que les outils et tactiques.

Pour Raja Chris (AIVONS), des résultats comme l'identité ou la résilience perdurent pendant des années, mais la technologie spécifique qui les produit change rarement aussi longtemps. Il se demande donc si un engagement donné resterait valable même si tous les fournisseurs impliqués étaient remplacés l'année suivante : si oui, il appartient probablement au plan à long terme ; si non, il s'agit en réalité d'un simple choix de mise en œuvre — à traiter sur un cycle plus rapide — déguisé en stratégie. C'est, selon lui, l'une des raisons pour lesquelles les feuilles de route perdent en crédibilité.

**La gouvernance comme conversation permanente**

Une feuille de route réécrite chaque trimestre ne peut plus être gouvernée comme un plan statique de trois ans validé une fois pour toutes via une checklist de conformité. Ce qui distingue les organisations qui gèrent bien cette transition de celles qui peinent, c'est le leadership, selon Cochran : les RSSI qui réussissent sous ce régime de replanification trimestrielle traitent la gouvernance comme une discipline de communication plutôt que de conformité. Leur succès dépend de leur capacité à embarquer le conseil d'administration, le métier et leurs propres équipes à chaque nouvelle évolution du plan.

Berry constate cette attente directement de la part de son propre conseil, qui veut un compte rendu clair de la façon dont la sécurité suit le rythme de l'entreprise, et du risque que ce rythme introduit. Les conseils d'administration posent désormais des questions différentes, ajoute Raja Chris : auparavant ils demandaient si l'organisation était sécurisée ; aujourd'hui ils veulent des preuves — ce qui tourne, qui est responsable, et ce qui peut atteindre les données sensibles. Un rapport incapable de distinguer « nous avons vérifié et tout allait bien » de « nous n'avons jamais vérifié » revendique, selon lui, une confiance qu'il n'a pas gagnée.

Le sondage KPMG 2026 pointe un défi lié : 42 % des responsables sécurité disent avoir du mal à démontrer le retour sur investissement de la cybersécurité auprès de leur conseil d'administration. Cette difficulté à prouver la valeur, autant que le risque, explique en partie pourquoi la feuille de route évolue : les RSSI n'ont pas renoncé à la pensée à long terme, mais ce qu'ils sont prêts à mettre par écrit, et pour combien de temps, change.

« C'est pourquoi je ne pense pas que la feuille de route de sécurité soit morte », conclut Raja Chris d'AIVONS. « C'est la feuille de route statique qui l'est. » Dickson, d'Insight Global, partage cet avis : une feuille de route à long terme garde de la valeur, dit-il, à condition d'accepter de la revoir aussi souvent que le monde qui l'entoure change.

## Pourquoi ça compte

Ce témoignage de plusieurs RSSI illustre un changement structurel dans la gouvernance de la sécurité IT, directement lié à l'accélération de l'adoption de l'IA (agents, shadow AI, identités non humaines) : les organisations qui continuent de piloter leur cybersécurité avec des plans statiques sur plusieurs années risquent de perdre en crédibilité et en réactivité face à des conseils d'administration qui exigent désormais des preuves continues plutôt que des validations annuelles.
