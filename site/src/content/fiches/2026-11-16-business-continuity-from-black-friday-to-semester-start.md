---
title: "Business Continuity: From Black Friday to Semester Start"
date: 2026-11-16
url: "https://leadershipintech.com/links/23733/3d78f33c-7ca0-4e03-9c70-68e56918a4cd/email"
keywords: ["continuité d'activité", "GitOps", "RGPD", "sauvegardes", "infrastructure as code", "transmission"]
theme: "Data"
tone: "opinion"
used_in: ["2026-11-16"]
---

## Résumé

L'auteur, architecte logiciel sur LEAD:FUH (plateforme de données d'apprentissage à la FernUniversität de Hagen), transpose son expérience de la gestion de continuité d'activité (BCM) acquise dans le e-commerce vers un contexte universitaire manipulant des données étudiantes sensibles. Il montre que les fondamentaux techniques (infrastructure as code, GitOps, sauvegardes testées, patchs automatisés) restent valables sans mandat ni auditeur, mais que le modèle de criticité s'inverse radicalement : ce n'est plus la disponibilité qui prime mais la fiabilité du mécanisme de consentement RGPD, et le pic d'activité n'est plus le Black Friday mais la rentrée universitaire. Il insiste enfin sur une contrainte propre au monde académique : concevoir la plateforme pour qu'elle soit exploitable par une équipe qui ne l'a pas construite, une fois le projet de recherche terminé.

## Points clés

- Principe directeur : tout ce qui peut être reconstitué à partir de Git et des sauvegardes de bases de données constitue une capacité de reprise complète (infrastructure as code pilotée par ArgoCD).
- Les sauvegardes et les restaurations sont testées automatiquement chaque semaine ; les données simplement « recréables » (zone d'ingestion) ne sont volontairement pas sauvegardées.
- Inversion de la criticité par rapport au e-commerce : la table de consentement, modeste composant PostgreSQL, devient l'élément le plus critique du système car sa défaillance est un risque RGPD, pas un simple problème de disponibilité.
- Inversion du calendrier des pics : la rentrée universitaire remplace le Black Friday, ce qui justifie l'absence d'astreinte 24/7 et des objectifs de reprise volontairement plus souples (jusqu'à 4 heures).
- Exigence propre au monde académique : concevoir dès le départ pour une transmission à une équipe IT centrale qui n'a pas participé à la construction, avec runbooks et critères d'acceptation vérifiés par des exercices réels.
- Alignement volontaire sur ISO/IEC 27001 dès le lancement du projet, jugé moins coûteux que sa mise en conformité a posteriori.

## Analyse approfondie

### Contexte

L'auteur situe son propos : il est architecte logiciel sur LEAD:FUH, une plateforme de données d'apprentissage (learning analytics) de la FernUniversität de Hagen, qui traite des données étudiantes hautement sensibles. L'article est présenté comme une adaptation de leurs directives opérationnelles internes. Il précise que, à la différence d'autres sujets « plateforme de données » traités ailleurs dans sa série, la gestion de la continuité d'activité (BCM) est le domaine qu'il maîtrisait déjà, pour l'avoir pratiqué dans le e-commerce à grande échelle, où une heure d'indisponibilité se chiffre en sommes importantes et où la capacité réelle de restauration d'une sauvegarde est scrutée en permanence. Cette expérience a forgé chez lui un réflexe : ne jamais construire un système sans infrastructure as code, automatisation complète et scénario de reprise effectivement testé.

Il souligne qu'ici, dans un contexte de recherche universitaire, rien n'impose formellement ce niveau de rigueur : pas d'auditeur, pas d'enjeu de revenu à la minute, pas d'objectif contractuel de temps de reprise. L'équipe choisit malgré tout de s'aligner sur la norme ISO/IEC 27001, estimant que ce référentiel décrit simplement ce à quoi ressemble une exploitation professionnelle, et qu'il est bien moins coûteux de l'adopter dès le départ que de devoir s'y conformer après coup — ce qui arrive toujours, tôt ou tard, qu'il s'agisse d'un délégué à la protection des données, d'un service de sécurité ou d'un futur repreneur de la plateforme. Mais il prévient : on ne peut pas simplement recopier un manuel de BCM e-commerce sur une plateforme universitaire. Si la discipline opérationnelle se transpose, les priorités, elles, ne se transposent pas.

### Ce qui reste : les non-négociables

Le socle du modèle opérationnel ne surprendrait aucun de ses anciens collègues du e-commerce. Il repose sur un principe unique : tout ce qui est reconstructible à partir de Git et des sauvegardes de bases de données équivaut à une capacité de reprise complète. Concrètement, un seul ingénieur, disposant d'un accès au dépôt GitOps, au stockage des sauvegardes et aux identifiants du cluster, peut restaurer l'intégralité de la plateforme. Tout est géré en infrastructure as code et réconcilié automatiquement par ArgoCD : l'état du cluster correspond exactement à l'état du dépôt, si bien qu'une modification manuelle effectuée directement sur un serveur serait tout simplement écrasée à la prochaine synchronisation. Ce qui n'est pas versionné dans Git n'existe tout simplement pas pour le système.

La reprise d'activité est hiérarchisée par niveaux définis à l'avance, et non découverts dans l'urgence d'un incident : les services sans état se restaurent par simple synchronisation Git, les bases de données par combinaison sauvegarde + synchronisation Git, et la zone d'atterrissage de l'ingestion n'est délibérément pas sauvegardée du tout puisqu'elle peut toujours être régénérée depuis les systèmes source — sauvegarder un cache recréable ne ferait que ralentir chaque exercice de reprise. L'auteur insiste : décider de ce qu'il ne faut pas protéger est une décision de BCM à part entière, au même titre que les sauvegardes elles-mêmes.

L'héritage du e-commerce se retrouve surtout dans la discipline des sauvegardes : une sauvegarde jamais restaurée n'est qu'un vœu pieux. Une tâche automatisée, exécutée chaque semaine, restaure donc la dernière sauvegarde dans une base de données jetable, vérifie les tables critiques et déclenche une alerte en cas d'échec. Les correctifs de sécurité suivent la même logique d'automatisation, via des mises à jour nocturnes gérées par Renovate et hiérarchisées selon leur rayon d'impact : les images d'applications sans état sont fusionnées automatiquement, tandis que les mises à jour touchant les bases de données nécessitent une validation humaine et une fenêtre de maintenance dédiée. Rien de tout cela n'est exotique ; il s'agit de l'équipement standard d'une exploitation professionnelle, appliqué ici sans qu'aucune contrainte externe ne l'impose.

### Ce qui s'inverse : la criticité

Dans le e-commerce, le classement de criticité est univoque : la disponibilité prime sur tout le reste, et une boutique hors ligne constitue par définition le pire scénario possible. Sur cette plateforme universitaire, la nature du pire scénario change complètement. Que les tableaux analytiques soient indisponibles pendant une journée n'est qu'un désagrément : les étudiants ne perdent rien, les chercheurs attendent simplement. En revanche, la plateforme traite des données étudiantes sous régime de consentement, lequel peut être retiré à tout moment. C'est ce qui fait de la table de consentement — une modeste table PostgreSQL sans prestige apparent — le composant le plus critique de tout le système : si les étudiants ne peuvent plus donner ou retirer leur consentement, ou si la plateforme perd la trace d'un retrait, ce n'est plus un problème de disponibilité mais un problème de conformité au RGPD, une situation qu'aucune équipe ne souhaite devoir justifier devant un délégué à la protection des données.

Cette hiérarchie se traduit directement dans l'allocation des ressources de protection : la base de données de consentement bénéficie de la cadence de sauvegarde et de la durée de rétention les plus élevées de toute la plateforme, et c'est précisément sa sauvegarde que le test de restauration hebdomadaire vérifie nommément. Les alertes déclenchant une notification immédiate sont « service de consentement indisponible » et « échec répété de sauvegarde », tandis qu'un simple ralentissement de tableau de bord peut attendre ; un score de machine learning livré avec un jour de retard est, par politique explicite, traité comme une affaire à régler le jour ouvré suivant, sans urgence.

La même logique d'inversion s'applique au calendrier : le pic d'activité du e-commerce est le Black Friday, celui de cette plateforme est la rentrée universitaire. En dehors des heures ouvrées, aucune astreinte n'est nécessaire — un luxe que l'auteur reconnaît avoir mis du temps à accepter, et qui constitue lui-même une décision de BCM : un engagement honnête de « meilleur effort en dehors des heures ouvrées » vaut mieux qu'une promesse fictive de disponibilité permanente que personne n'est dimensionné pour tenir. Les objectifs de reprise découlent logiquement de ce choix : un point de reprise fixé à quatre heures, qui serait absurde pour un pipeline de commandes e-commerce, est parfaitement proportionné pour une plateforme d'analyse pédagogique. Fixer par écrit des objectifs aussi souples lui a semblé étrange après des années passées à optimiser chaque minute, mais il conclut que seuls des objectifs réalistes, énoncés et effectivement tenus, sont utiles lors d'un incident réel.

### Ce qui est nouveau : conçu pour être transmis

Une exigence, en revanche, n'a aucun équivalent dans le monde du e-commerce : un projet de recherche a une fin, mais la plateforme, si elle fait ses preuves, doit lui survivre et basculer vers la direction informatique centrale de l'université pour une exploitation de long terme. Les personnes qui l'ont conçue ne seront pas celles qui l'exploiteront au quotidien — ignorer cette réalité est précisément, selon l'auteur, la façon dont les universités accumulent des systèmes qu'aucune équipe n'ose plus toucher une fois le projet initial dissous.

Cette contrainte façonne les choix de conception dès aujourd'hui, et non au moment de la passation. Trois exigences en découlent : d'abord, l'exploitation quotidienne de la plateforme (redémarrages, surveillance des sauvegardes, restaurations, rollbacks) doit être pilotable via des runbooks, sans nécessiter de compétences en Python, en dbt ou en machine learning — la liste de compétences requises pour les opérateurs se limite volontairement aux bases de Kubernetes, à l'administration élémentaire de bases de données et à Git. Ensuite, la passation doit être démontrée par des exercices réels et non actée par un simple document signé : l'équipe qui reprend la plateforme doit effectuer, en conditions réelles, une reprise complète depuis une sauvegarde, un rollback supervisé et une restauration ciblée d'une base de données avant d'accepter officiellement la responsabilité du système — un runbook jamais exécuté par celui qui en dépendra n'est que fiction. Enfin, le mécanisme d'escalade doit être pensé pour survivre au départ de l'équipe projet, avec un support à plusieurs niveaux prévoyant un chemin de remontée vers le niveau architecture, défini pendant que les concepteurs sont encore présents.

L'auteur résume cette différence par une formule : le e-commerce lui a appris à concevoir pour l'incident de trois heures du matin, tandis que le contexte universitaire exige de concevoir pour l'incident survenant après le départ complet de l'équipe — une contrainte plus exigeante encore, et le même réflexe, selon lui, qui les a conduits à privilégier des standards web volontairement sobres pour le frontend.

### Conclusion de l'auteur

L'auteur conclut que la boîte à outils du BCM — infrastructure as code, GitOps, restaurations testées, correctifs automatisés, runbooks éprouvés — relève des bonnes pratiques professionnelles, qu'elle soit imposée ou non par un mandat externe. Ce qui doit en revanche être repensé pour chaque contexte, c'est le modèle de criticité lui-même : ce qu'il est réellement inacceptable de perdre, la période qui constitue le véritable pic d'activité, et l'identité de ceux qui exploiteront le système dans plusieurs années. Dans le contexte universitaire décrit ici, ces réponses se sont révélées suffisamment différentes de celles du e-commerce pour que recopier l'ancien manuel aurait conduit à protéger les mauvaises choses.

### Référence citée

L'article s'appuie sur la norme ISO/IEC 27001:2022 (sécurité de l'information, cybersécurité et protection de la vie privée — exigences relatives aux systèmes de management de la sécurité de l'information), présentée comme le référentiel de contrôles auquel la plateforme s'aligne volontairement ; l'auteur note qu'un référentiel équivalent pour le secteur public allemand serait l'IT-Grundschutz du BSI (Office fédéral allemand de la sécurité des technologies de l'information).

## Pourquoi ça compte

Ce retour d'expérience illustre, de façon concrète et transposable, comment adapter les pratiques matures de résilience (IaC, GitOps, BCM) à un contexte où la criticité réglementaire (RGPD/consentement) prime sur la simple disponibilité, un enseignement directement utile pour toute équipe data confrontée à des données sensibles sous contrainte de conformité plutôt que de SLA commercial.
