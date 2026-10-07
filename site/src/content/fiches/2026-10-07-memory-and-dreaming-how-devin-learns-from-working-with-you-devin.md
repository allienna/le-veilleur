---
title: "Memory and dreaming: how Devin learns from working with you | Devin"
date: 2026-10-07
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fdevin.ai%2Fblog%2Fmemory-and-dreaming%3Futm_source=tldrai/1/010001a111643ec8-81ad9ade-ccd3-42bd-9e5c-cead1c259ceb-000000/-otH8A_sAFc8U0kBMizgMEUdcCNFqIFEbofd7gdUW8g=452"
keywords: ["mémoire", "agents IA", "Devin", "apprentissage continu", "personnalisation", "Git"]
theme: "IA"
tone: "news"
used_in: ["2026-10-07"]
---

## Résumé
Cognition introduit deux nouvelles fonctionnalités pour son agent de codage Devin : « Memory », qui permet de conserver d'une session à l'autre des enseignements personnels (préférences, corrections, leçons apprises sur un projet), et « Dreaming », un processus asynchrone quotidien qui réorganise et améliore l'index de ces mémoires. Les mémoires sont stockées dans un dépôt Git personnel de fichiers markdown, synchronisé entre sessions parallèles avec un contrôle de version pour éviter les écrasements silencieux. Cognition a par ailleurs open-sourcé le standard utilisé pour construire ce système, et invite la communauté à l'intégrer dans ses propres agents via cognition.ai/agent-memory-repo.

## Points clés
- « Memory » capture les leçons apprises pendant le travail (corrections, préférences, pièges d'environnement) — ce ne sont pas des résumés de session, mais des notes courtes reliées à la session où elles ont été apprises.
- Les mémoires vivent dans un « Memory Drive » personnel : un dépôt Git de fichiers markdown organisé par dépôt, projet ou thème, avec un `MEMORY.md` central donnant les préférences générales et un index des autres fichiers.
- Chaque session dispose de son propre checkout Git ; Devin commit ses modifications, fusionne les mises à jour d'autres sessions, et un contrôle de révision rejette les écritures obsolètes — les conflits sont signalés pour résolution plutôt qu'écrasés silencieusement.
- « Dreaming » est une session d'arrière-plan quotidienne qui consolide les notes redondantes, supprime les détails transitoires et les mémoires obsolètes inutilisées, et fait émerger de nouvelles connaissances à partir des sessions passées.
- Le standard de mémoire est distinct des « skills » : les skills encodent une procédure réutilisable (ex. les étapes d'une release), tandis que la mémoire accumule du contexte personnel au fil des sessions.

## Analyse approfondie
Aujourd'hui, nous présentons Memory et Dreaming dans Devin.

Memory permet à Devin de conserver, d'une session à l'autre, des enseignements utiles sur la façon dont vous aimez travailler : vos préférences, les corrections que vous avez apportées, et les leçons apprises sur vos projets et vos flux de travail.

Dreaming est un processus asynchrone quotidien qui améliore l'index des mémoires de Devin à votre sujet. Les mémoires générées pendant vos sessions sont dédupliquées, reliées aux sessions et artefacts pertinents, et de nouvelles connaissances émergent.

Vous pouvez parcourir les mémoires de Devin dans Customize → Memory, et inspecter les sessions de dreaming récentes. La mémoire est personnelle à vous au sein de chaque organisation sur devin.ai.

Nous avons également open-sourcé le standard que nous avons utilisé pour construire le système de mémoire de Devin. Nous vous invitons à l'intégrer dans vos agents et à contribuer sur cognition.ai/agent-memory-repo.

Une partie du contexte le plus utile n'émerge qu'une fois le travail engagé. Vous corrigez une hypothèse, expliquez pourquoi une approche ne fonctionnera pas dans votre projet actuel, ou clarifiez une préférence personnelle. D'autres leçons ressortent du travail lui-même : un piège d'environnement qui a nécessité plusieurs tentatives pour être résolu correctement, ou une décision de projet qui comptera à nouveau plus tard.

**Memory** donne à Devin un moyen de retenir proactivement ces leçons au-delà de la session elle-même, sans que vous ayez à interrompre la session pour mettre à jour un skill. Elle est personnelle à **vous**, plutôt que de devenir des instructions partagées pour votre organisation. Les mémoires ne sont pas des résumés de sessions. Ce sont des leçons que Devin a apprises en travaillant avec vous, écrites sous forme de notes courtes avec un lien vers la session où elles ont été apprises.

Les mémoires vivent dans votre **Memory Drive** personnel, un dépôt Git persistant de fichiers markdown. Les notes peuvent être organisées par dépôt, projet ou thème, tandis qu'un court `MEMORY.md` contient les préférences générales et un index des autres fichiers du drive. Au début d'une session, Devin reçoit `MEMORY.md` comme contexte. À partir de là, il peut rechercher et lire les notes pertinentes en utilisant les mêmes outils que ceux employés pour naviguer dans le code, sans charger l'intégralité de l'archive de mémoire dans son prompt.

Chaque session travaille avec son propre checkout Git du drive. Après avoir édité une note, Devin commit ses modifications, fusionne les mises à jour provenant d'autres sessions, et enregistre le résultat dans votre drive de mémoire persistant. Si une autre session enregistre une mise à jour pendant qu'une synchronisation est en cours, un contrôle de révision rejette l'écriture obsolète afin que Devin puisse réessayer avec la version la plus récente. Les modifications conflictuelles sont signalées pour résolution plutôt qu'écrasées silencieusement. Cela permet à des sessions parallèles de contribuer au même drive de mémoire sans traiter la copie locale d'une seule session comme la source de vérité.

Capturer des mémoires pendant une tâche n'est que la première étape. Ces mémoires doivent aussi être revisitées en bénéficiant du contexte global de l'ensemble de vos sessions. **Dreaming** est une session d'arrière-plan quotidienne, dans laquelle Devin revoit les conversations passées à la lumière de sa mémoire existante pour améliorer son index pour les sessions futures.

Pendant le dreaming, Devin :

- consolide les notes qui se recoupent
- supprime les détails transitoires
- recherche des leçons utiles qui n'avaient pas été capturées pendant le travail original
- supprime les enregistrements de mémoire obsolètes qui n'ont été utilisés par aucune session

Devin préserve les références aux sources et les préférences explicites tout en réorganisant les notes et leur index afin que le contexte pertinent soit plus facile à trouver.

Les skills capturent un flux de travail répétable ; la mémoire capture ce que Devin apprend en travaillant avec vous. Un skill de release pourrait décrire les étapes pour tester et publier un changement. La mémoire pourrait enregistrer vos préférences de stack technique, ainsi que la raison que vous avez donnée.

Les deux fonctionnent ensemble : le skill fournit la procédure, tandis que la mémoire fournit le contexte pour l'appliquer à votre travail. Les deux peuvent contenir des instructions, mais leur cycle de vie diffère — les skills sont délibérément packagés pour être réutilisés, tandis que la mémoire est accumulée au fil des sessions et revisitée par le dreaming.

Une préférence que vous avez expliquée ou une leçon apprise à la dure devrait rester utile au-delà d'une seule session. Memory et Dreaming sont conçus pour faire perdurer cette expérience, sans vous rendre responsable de son entretien.

Sur devin.ai, ouvrez **Customize → Memory** pour explorer ce que Devin a appris en travaillant avec vous.

## Pourquoi ça compte
Cet article illustre une tendance de fond chez les agents de codage IA : passer de simples assistants sans état à des systèmes dotés d'une mémoire persistante, personnalisée et versionnée via Git, avec un standard ouvert qui pourrait influencer la façon dont d'autres agents gèrent le contexte long terme.
