---
title: "Salesforce in Claude | Claude by Anthropic"
date: 2026-09-22
url: "https://elinkb7e.mail.aiwithremy.com/ss/c/u001.YBM5Qp34ySTr_4wyLjJQ5QeoEWjTJUfssqedBKuhHkdCvmnT9RL1Mal5ioC5GbAkrnulgea9xtd7bn84q7Jl1vHxYRGFyB7S3DyoRuIEHn1CZJg6bhkqzphhrYu6rdH_S7Cct7fUTG_QD0F7LT9vUKNwA5VeOeRBc7kIxKhy4su2K8NmacDkjs-PF_sDILVogBhj-RKOMoYrYIzWzUUimkghkn71RDKTHjbkFKiCueGVaEWvI83kY4_lXuIJq0W9hK1Ho5I25spizCdcKXKvHg/4u8/RGvxY133TvuMGlNkVoxNaw/h16/h001.awLMRg2Jzg75ZCUA8SsaDqiIhCX0Z9TwSs13P23jQOA"
keywords: ["Claude", "Salesforce", "IA agentique", "CRM", "ventes", "automatisation"]
theme: "IA"
tone: "news"
used_in: ["2026-09-22"]
---

## Résumé
Anthropic lance en bêta « Salesforce in Claude », un plugin conçu avec Salesforce qui fait entrer les comptes, opportunités et pipeline d'un commercial directement dans Claude, sous ses permissions Salesforce existantes. Il regroupe 37 compétences couvrant la recherche de comptes, la préparation d'appels, la revue de pipeline et les mises à jour du CRM, en s'appuyant sur des connecteurs Salesforce et Slack. Le plugin automatise les tâches administratives récurrentes (briefing quotidien, préparation de réunions, plans de clôture, tableaux de bord de pipeline) tout en laissant le commercial approuver chaque modification avant son écriture dans Salesforce. Déjà déployé chez GitLab, Siemens et Legora et utilisé par 7 000 commerciaux Salesforce, il est disponible en bêta sur tous les forfaits payants de Claude.

## Points clés
- 37 compétences dédiées au travail quotidien des account executives : recherche de comptes, préparation d'appels, revue de pipeline, mises à jour CRM.
- Deux connecteurs (Salesforce et Slack) permettent à Claude de lire les données et d'agir dessus, dans la limite des permissions existantes du commercial.
- Briefing matinal automatisé (réunions du jour, deals à risque, fils sans réponse) avec un récapitulatif hebdomadaire le vendredi à destination du manager.
- Après chaque appel, Claude rédige automatiquement e-mails de suivi, résumés pour Slack et propositions de mise à jour d'opportunité.
- Tableaux de bord de pipeline interactifs et récits de prévisions générés pour la direction commerciale.
- Chaque changement proposé doit être approuvé par le commercial avant d'être écrit dans Salesforce ; par défaut, pas d'entraînement des modèles sur les données des clients Team/Enterprise.

## Analyse approfondie
# Faire entrer Salesforce dans Claude

Les commerciaux peuvent désormais faire des recherches sur les entreprises, préparer leurs appels, examiner leur pipeline et rédiger des mises à jour CRM grâce à notre nouveau plugin Salesforce in Claude.

Nous lançons aujourd'hui Salesforce in Claude en version bêta, un plugin conçu avec Salesforce qui fait entrer les comptes, opportunités et pipeline d'un commercial dans Claude, dans le cadre de ses permissions Salesforce existantes. Il comprend 37 compétences (skills) couvrant le travail quotidien des account executives : recherche de comptes, préparation d'appels, revue de pipeline et mises à jour du CRM.

Les commerciaux passent souvent plusieurs heures par jour à préparer leurs réunions ou à effectuer le suivi de rendez-vous clients, en rassemblant manuellement des informations dispersées entre Salesforce, les e-mails, les enregistrements d'appels et Slack. Avec ce nouveau plugin, Claude prend en charge ce travail administratif et met à jour Salesforce une fois que le commercial a validé les changements.

Le plugin dispose également de deux connecteurs qui permettent aux commerciaux de commencer à l'utiliser dès qu'un administrateur connecte Salesforce et qu'ils se connectent. Avec le connecteur Salesforce, Claude peut lire les données Salesforce et agir dessus : résumer l'historique d'un compte, mettre à jour des opportunités, consigner des appels ou créer des tâches de suivi. Le connecteur Slack couvre les résumés des canaux de deals et les fils de discussion des équipes de compte, que les compétences peuvent lire et dans lesquels elles peuvent écrire. Lors de la première utilisation du plugin, une compétence de configuration identifie les outils et connecteurs du commercial et crée un Artifact Claude adapté à son rôle et à son portefeuille de comptes.

**Commencer la journée avec un briefing.** Chaque matin, Claude livre un briefing personnalisé comprenant les réunions du jour, les deals qui doivent se conclure prochainement, les opportunités à risque et les fils de discussion non lus nécessitant une réponse. Une fois programmé, il s'exécute en arrière-plan et est accessible partout via Claude, y compris en déplacement avec l'application Claude. À partir du briefing, les commerciaux peuvent demander à Claude de repousser une date de clôture, de changer une étape ou d'ajouter une tâche de suivi, et Claude effectuera la mise à jour dans Salesforce. Le vendredi, le briefing fait le bilan de la semaine et rédige une mise à jour destinée au manager du commercial.

**Préparer un appel.** Un commercial peut demander à Claude de préparer sa prochaine réunion : Claude puise alors les informations dans Salesforce, Slack et les e-mails — les opportunités ouvertes et où elles en sont, ce dont l'équipe de compte a discuté cette semaine, les fils sans réponse, et les questions encore en suspens depuis les appels précédents. S'il repère dans ces fils des parties prenantes qui ne figurent pas encore dans Salesforce, Claude les ajoute comme contacts sur le compte.

**Examiner un deal et construire le plan de clôture.** Pointé sur une opportunité, Claude évalue le deal selon la méthodologie de l'équipe, en tenant compte des lacunes de qualification, des parties prenantes non encore rencontrées et des facteurs mettant en péril la date de clôture. Si on lui demande de continuer, il rédige le business case et un plan de clôture mutuel daté, remplit les champs de qualification, et ajoute les parties prenantes manquantes en tant que rôles de contact. Tout cela est enregistré sur l'opportunité une fois approuvé.

**Terminer chaque réunion avec un Salesforce à jour.** Après chaque appel, Claude transforme la transcription ou les notes du commercial en e-mail de suivi, en résumé pour le canal du deal dans Slack, et rédige des mises à jour de l'opportunité (prochaines étapes, étape, date de clôture) que le commercial n'a plus qu'à valider.

**Examiner le pipeline et partager des prévisions.** Un commercial peut demander une vue du pipeline, et Claude construit un tableau de bord interactif montrant la couverture par étape, les deals les plus susceptibles de glisser et pourquoi, avec une exploration détaillée par compte. Depuis ce tableau de bord, un commercial peut demander à Claude de déplacer une date de clôture ou de changer une étape, et Claude met à jour l'enregistrement dans Salesforce. Les tableaux de bord peuvent être partagés avec la direction ou l'équipe, et Claude peut rédiger le récit des prévisions dans le format attendu par la direction. Les responsables commerciaux peuvent exécuter les mêmes vues à l'échelle de l'équipe.

**Construit sur les permissions existantes de l'organisation.** Salesforce reste le système d'enregistrement de référence. Les commerciaux se connectent avec leurs identifiants Salesforce, et Claude ne lit que ce que leurs permissions autorisent. Par défaut, Claude demande au commercial d'approuver chaque modification proposée avant qu'elle ne soit écrite. Sur les forfaits Team et Enterprise, nous n'entraînons pas nos modèles sur vos données par défaut.

Les administrateurs connectent Salesforce une seule fois pour toute l'organisation et choisissent quels groupes reçoivent le plugin.

Les clients d'Anthropic GitLab, Siemens et Legora ont déployé Salesforce in Claude au sein de leurs organisations, et 7 000 commerciaux Salesforce l'utilisent déjà dans leur travail. Voici ce qu'ils nous ont dit à propos de Salesforce in Claude :

« Avec Salesforce in Claude, nos commerciaux transforment les données en direct en briefings de réunion en quelques secondes au lieu de plusieurs heures. À mesure que notre équipe commerciale grandit, chaque nouveau commercial démarre avec une vision complète des cabinets d'avocats que nous servons. » — David Eckstein, directeur financier, Legora

« Avec Salesforce in Claude, les commerciaux peuvent commencer leur journée avec la revue de pipeline déjà faite et l'historique du compte déjà disponible. Ce temps gagné est directement réinvesti dans les conversations avec les clients. » — Alexa Vignone, présidente et directrice des revenus, Salesforce

Salesforce in Claude est disponible en version bêta sur tous les forfaits payants de Claude. Le MCP Salesforce peut dès aujourd'hui être installé directement depuis la marketplace. Pour installer le plugin, les administrateurs peuvent demander l'accès via AgentExchange et connecter Salesforce une seule fois pour l'ensemble de leur organisation. Pour les administrateurs, un guide de configuration détaille comment activer cette fonctionnalité pour leur organisation. Pour les responsables commerciaux, un guide explique comment piloter une organisation commerciale efficace avec Claude.

Recevez la newsletter développeurs — mises à jour produit, tutoriels, mises en avant de la communauté et plus encore, livrée chaque mois dans votre boîte de réception.

## Pourquoi ça compte
Ce lancement illustre la stratégie d'Anthropic consistant à intégrer Claude au cœur des workflows métier via des plugins verticaux supervisés (ici la vente), plutôt que via une automatisation totalement autonome. C'est un signal à suivre dans la bataille agentique qui oppose Claude, Microsoft Copilot et Salesforce Agentforce sur le terrain du CRM.
