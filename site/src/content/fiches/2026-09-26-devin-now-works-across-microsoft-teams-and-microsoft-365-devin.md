---
title: "Devin now works across Microsoft Teams and Microsoft 365 | Devin"
date: 2026-09-26
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fdevin.ai%2Fblog%2Fmicrosoft-teams-and-microsoft-365%3Futm_source=tldrit/1/010001a0d8832bfb-05088f4b-6fee-4987-9374-70b9e343d5ca-000000/zQG5o4aphL5_69qbrMu4NFH_aCfSt6tUL3F5wQCodIo=452"
authors: ["Cognition"]
keywords: ["Devin", "Microsoft Teams", "Microsoft 365", "IA agentique", "MCP", "intégration entreprise"]
theme: "Tech"
tone: "news"
used_in: ["2026-09-26"]
---

## Résumé
Cognition annonce une intégration majeure de son agent IA Devin avec l'écosystème Microsoft : un support natif pour mentionner Devin dans Microsoft Teams, ainsi qu'une intégration de première partie avec Microsoft 365 (mail, calendrier, fichiers, tâches, chats, annuaire). Devin peut désormais être ajouté à des canaux, des discussions et des fils Teams, démarrer des sessions automatiquement à partir de messages, et agir via six connecteurs MCP couvrant Outlook, Calendar, OneDrive/SharePoint, Microsoft To Do, Teams et Microsoft Entra ID. L'article met l'accent sur un modèle de permissions délégué par utilisateur, avec consentement granulaire et accès en lecture par défaut. Les deux intégrations sont disponibles immédiatement pour tous les clients de Devin.

## Points clés
- Devin peut être mentionné directement dans les messages privés, les discussions de groupe et les canaux Microsoft Teams, avec des réponses dans la conversation elle-même.
- Devin peut surveiller un canal Teams et démarrer un travail de façon autonome dès qu'un message pertinent arrive (rapport de bug, alerte, demande).
- Six connecteurs MCP Microsoft 365 (Mail & Contacts, Calendar, OneDrive & SharePoint, Microsoft To Do, Microsoft Teams, Directory/Entra ID) permettent à Devin d'agir comme l'utilisateur connecté.
- Le modèle de sécurité repose sur des permissions déléguées par utilisateur, un accès en lecture minimal par défaut, et un consentement admin requis pour les scopes les plus sensibles.
- Plus de 90 % des entreprises du Fortune 500 utilisent Microsoft Teams, ce qui en fait un point d'entrée stratégique pour l'adoption d'agents IA en contexte professionnel.

## Analyse approfondie
Aujourd'hui, nous lançons une mise à jour majeure pour les ingénieurs qui utilisent Devin et l'écosystème Microsoft : un support natif pour mentionner Devin (@) dans Microsoft Teams, et une intégration Microsoft 365 de première partie qui connecte Devin à la messagerie, au calendrier, aux fichiers, aux tâches, aux discussions et à votre annuaire.

Plus de 90 % des entreprises du Fortune 500 utilisent Microsoft Teams pour tout, des rapports de bugs aux spécifications produit. Avec cette nouvelle version, Devin peut désormais être ajouté à des canaux, des discussions et des fils de conversation, récupérer des sessions avec le bon contexte et les bonnes parties prenantes, puis partager son travail au même endroit.

### Devin dans Microsoft Teams

**Messages privés et discussions de groupe.** Devin est disponible dans les canaux Teams depuis l'année dernière, mais vous pouvez désormais lui envoyer un message directement, ou l'ajouter à une discussion de groupe, et il démarre une session et répond dans la conversation. Vous pouvez échanger avec lui de la même manière que dans l'application web de Devin.

**Automatisations depuis les canaux Teams.** Devin peut surveiller un canal et démarrer un travail de sa propre initiative dès qu'un message arrive : un rapport de bug, une alerte, une demande.

**Cartes pour les questions, les approbations et les connexions.** Quand Devin a besoin de quelque chose de votre part, il envoie une carte plutôt qu'un mur de texte. Répondez à une question de clarification, approuvez une action, ou connectez-vous à un serveur MCP en un clic.

Devin a également reçu plusieurs autres améliorations : il peut mentionner des personnes (@), envoyer des pièces jointes et se mettre lui-même en sourdine au sein d'une discussion.

### Une intégration Microsoft 365 de première partie

En plus de fonctionner nativement dans Teams, nous annonçons également une nouvelle intégration de Devin avec Microsoft 365. À partir d'aujourd'hui, vous pouvez accéder à un ensemble de serveurs MCP Microsoft 365, conçus et hébergés par Cognition et disponibles dans la Marketplace MCP de Devin. Il y a six connexions :

1. Mail & Contacts : lire, organiser et envoyer des e-mails Outlook, et gérer les contacts
2. Calendar : consulter, créer, modifier et supprimer des événements
3. OneDrive & SharePoint : parcourir, lire et téléverser des fichiers, y compris des fichiers partagés avec vous par lien
4. Microsoft To Do : lister, créer, modifier et compléter des tâches
5. Microsoft Teams : lister vos équipes, canaux et discussions, et envoyer un message en votre nom. Ceci est distinct de l'application Teams mentionnée plus haut.
6. Directory (Microsoft Entra ID) : rechercher des personnes, leurs responsables, et votre propre profil

Grâce à ces connecteurs, vous pouvez désormais confier à Devin des tâches comme :

*Lis le document de conception que Priya a partagé dans SharePoint ainsi que le fil d'e-mails sur la migration de facturation, puis ouvre une pull request pour la phase un. Ajoute une réunion de revue à mon calendrier pour jeudi et ajoute les points de suivi à ma liste de tâches To Do.*

Devin agit en tant qu'utilisateur connecté. Il peut atteindre tout ce que cet utilisateur peut atteindre dans Microsoft 365, et rien de plus.

### Sécurité et permissions

Nous avons conçu les deux intégrations pour qu'elles soient rapides et faciles à examiner par votre équipe sécurité :

- L'installation de l'application Teams n'accorde aucun accès à la messagerie, aux fichiers ou aux calendriers. L'application Teams mise à jour ne demande aucune nouvelle permission par rapport à la version actuelle. L'accès aux messages ne provient que d'un consentement spécifique à la ressource, limité aux équipes et discussions où Devin est installé. Supprimer l'application révoque cet accès.
- Le MCP Microsoft 365 utilise uniquement des permissions déléguées, par utilisateur. Il n'existe aucune permission au niveau de l'application. Chacune des six connexions dispose de son propre écran de consentement. Le minimum pour chacune est un accès en lecture seule, et l'accès en écriture est une option que vous pouvez décocher lors de la connexion. Les tenants qui restreignent le consentement des utilisateurs peuvent exiger une approbation administrateur au préalable, et quelques scopes d'annuaire plus larges nécessitent toujours un consentement administrateur. Les administrateurs peuvent également choisir d'utiliser le serveur MCP de première partie de Cognition ou d'apporter leur propre application Entra.

La liste complète des permissions pour Teams se trouve dans notre documentation.

### Prise en main

Les deux intégrations sont disponibles dès maintenant pour tous les clients de Devin.

- Microsoft Teams : installez l'application Devin AI depuis la Microsoft Marketplace, puis connectez-la sous Paramètres > Connexions dans Devin. La configuration nécessite un administrateur Microsoft Teams et un administrateur Devin. Ensuite, chaque personne relie son propre compte une fois. Pour envoyer un message à Devin en message privé, chaque utilisateur doit également installer lui-même l'application Devin AI depuis le magasin d'applications Teams ; l'installation par un administrateur pour une équipe ne couvre pas les discussions personnelles.
- Microsoft 365 : ouvrez la Marketplace MCP dans Devin et connectez les serveurs Microsoft 365 que vous souhaitez utiliser.

Consultez la documentation Microsoft Teams pour la mise en place, et dites-nous ce que vous aimeriez que Devin fasse ensuite dans Microsoft 365.

## Pourquoi ça compte
Cette annonce illustre la stratégie de distribution des agents IA d'entreprise : s'intégrer directement dans les outils déjà installés (Teams, Outlook, SharePoint) plutôt que de créer une nouvelle interface, tout en soignant le modèle de permissions pour rassurer les équipes sécurité. C'est un signal fort pour la veille sur l'adoption des agents IA autonomes en contexte professionnel B2B.
