---
title: "A skills library for every agent"
date: 2026-09-19
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.notion.com%2Fblog%2Fa-skills-library-for-every-agent%3Futm_source=tldrai/1/010001a0b4b52e44-c3e19932-1b74-4717-8169-487171bd18e3-000000/XsapUDf_iyeTOheF6GJoI97jU-nX-QN-ogs7O5ZzG_w=452"
keywords: ["skills", "IA agentique", "Notion", "API", "collaboration", "GitHub"]
theme: "Tech"
tone: "news"
used_in: ["2026-09-19"]
---

## Résumé
Notion annonce le lancement de la Skills API, un ensemble de points d'accès permettant de charger depuis Notion des « skills » (compétences) pour agents IA dans des formats de fichiers conformes aux standards du secteur. L'objectif est de faire de Notion une bibliothèque de compétences collaborative, accessible à toute l'équipe (pas seulement aux développeurs) et compatible avec n'importe quel agent (Claude, ChatGPT, Grok Bot, etc.). Deux cas d'usage sont mis en avant : la synchronisation des compétences Notion vers GitHub via un kit de démarrage open source, et l'intégration native dans le CLI `skills` de Vercel. Des clients comme Candidly et Brainlabs témoignent de l'intérêt de pouvoir documenter et faire évoluer ces compétences directement dans Notion plutôt que dans un dépôt de code réservé aux ingénieurs.

## Points clés
- Notion lance la **Skills API**, qui exporte les compétences stockées dans Notion vers des formats compatibles avec les agents IA du marché.
- La bibliothèque de compétences est pensée pour être utilisable par des équipes non techniques (ventes, marketing, finance, opérations), pas seulement par des développeurs.
- Un starter kit open source permet de synchroniser automatiquement les compétences Notion vers un dépôt GitHub, tout en conservant des fonctionnalités natives comme l'invocation via `/` et les contrôles d'installation par les administrateurs.
- Le CLI open source `skills` de Vercel intègre désormais Notion, avec les commandes `npx skills add <url notion>` ou `npx skills add notion`.
- Des outils MCP permettent aussi de créer et modifier des compétences dans Notion directement depuis les agents, créant une boucle d'amélioration continue.
- Notion positionne sa bibliothèque comme gouvernable (permissions, historique de versions, analytics d'usage) et agnostique vis-à-vis de l'agent utilisé.

## Analyse approfondie
Les compétences (skills) rendent les agents IA plus performants et adaptés à vos workflows. Et ces compétences prennent encore plus de valeur lorsqu'elles sont partagées, permettant à de nombreuses personnes de bénéficier des efforts de quelques-unes. C'est pourquoi il est essentiel pour les équipes modernes d'adopter une bibliothèque de compétences où elles peuvent les partager et les découvrir.

Nos clients nous disent rechercher une bibliothèque de compétences dotée des qualités suivantes :

- **Conçue pour toute l'équipe** : les compétences ne sont plus réservées aux ingénieurs. Une bibliothèque de compétences doit être facile à utiliser pour tout le monde, y compris pour des fonctions comme les ventes/le marketing, la finance et les opérations.
- **Agnostique vis-à-vis de l'agent** : les compétences deviennent un dépôt essentiel du savoir organisationnel. Vos compétences doivent être disponibles dans tous les agents, sans être enfermées dans un seul.
- **Collaborative** : les compétences doivent s'améliorer en continu grâce aux suggestions de tous les membres de l'équipe. Dans le même temps, il est important de garder le contrôle grâce aux permissions et à l'historique des versions.
- **Observable et gouvernable** : les administrateurs d'équipe ont besoin d'analyses d'usage et de la capacité à contrôler quelles compétences sont accessibles à quels utilisateurs.

Chez Notion, nous construisons une bibliothèque de compétences qui coche toutes ces cases. Vous pouvez éditer des compétences exactement comme des pages Notion classiques, et les organiser dans des bases de données. Vous pouvez stocker des dossiers de fichiers annexes comme des assets et du code, de sorte que la bibliothèque puisse accueillir n'importe quelle compétence conforme aux spécifications. Et l'ensemble du système est profondément collaboratif, avec permissions, suggestions de modifications, analytics, et plus encore.

### Présentation de la Notion Skills API

Une bibliothèque de compétences agnostique vis-à-vis de l'agent doit être disponible partout où votre équipe travaille. Aujourd'hui, nous franchissons une nouvelle étape vers cet objectif avec la Skills API : **un ensemble de points d'accès API pour charger des compétences depuis Notion dans des formats de fichiers conformes aux spécifications.**

Nos premiers clients et partenaires utilisent déjà cette API pour charger des compétences depuis Notion dans l'ensemble de leurs agents et outils. Voici quelques exemples pour vous inspirer.

#### Synchroniser les compétences vers GitHub

De nombreuses équipes stockent leurs compétences dans un dépôt GitHub, qui peut être utilisé comme source de compétences dans des applications d'agents comme Claude, ChatGPT et Grok Bot. GitHub fonctionne bien pour les ingénieurs, mais les autres ont souvent du mal à éditer les compétences, voire n'ont même pas de compte.

Grâce à la Skills API, **vous pouvez synchroniser les compétences de votre équipe depuis Notion vers GitHub.** Cela permet aux équipes non techniques d'utiliser Notion comme foyer collaboratif pour leurs compétences, tout en gardant ces compétences synchronisées dans leurs différents agents. Une fois synchronisées, les compétences prennent en charge les fonctionnalités natives disponibles dans les applications d'agents, comme l'invocation via le menu `/` et les contrôles d'installation par les administrateurs.

Vous pouvez également téléverser et éditer des compétences dans Notion depuis des applications d'agents grâce aux outils MCP. Cela signifie que vous pouvez utiliser des compétences existantes depuis votre agent pour démarrer votre bibliothèque de compétences et alimenter une boucle d'amélioration continue à mesure que les compétences sont réellement utilisées.

Voici ce que nos clients disent de cette nouvelle fonctionnalité :

« **Le fait de pouvoir documenter nos compétences dans Notion renforce la connaissance qu'a notre équipe de ce qui est accessible** et soutient la manière dont elles sont utilisées lorsqu'on travaille avec Claude. » — Hillary Helmling, Product Operations, Candidly

« La raison pour laquelle ces compétences ne peuvent pas simplement rester dans GitHub, c'est que tous ceux qui créent une compétence ne sont pas développeurs. **Notion ne se contente pas d'afficher le résultat de la compétence, il permet aussi une collaboration directe entre membres de l'équipe sur la plateforme qu'ils connaissent**. » — Josh Reid, Product Engineer, Brainlabs

##### Essayez-le

Si vous souhaitez synchroniser des compétences depuis Notion vers GitHub, nous mettons à disposition en open source un kit de démarrage que votre équipe IT peut utiliser pour mettre en place votre propre synchronisation de compétences. Pointez votre agent de codage vers ce dépôt pour commencer.

Dans le même temps, vous n'êtes pas limité à cette synchronisation particulière. Votre équipe peut l'utiliser comme exemple de code pour construire une intégration avec n'importe quel agent ou outil interne.

#### Installer des compétences Notion dans le CLI Vercel

La **Skills API permet également aux entreprises qui construisent des produits d'outillage agentique de prendre en charge la bibliothèque de compétences Notion**.

Vercel a désormais ajouté la prise en charge des compétences Notion à son CLI `skills`, l'un des outils les plus populaires pour installer des compétences.

Exécutez `npx skills add <url notion>` pour installer une page Notion marquée comme compétence, ou exécutez `npx skills add notion` pour installer de manière interactive des plugins entiers parmi tous ceux disponibles dans votre espace de travail. Les membres de votre équipe peuvent utiliser le CLI de façon interactive, ou vous pouvez l'intégrer dans des workflows programmatiques.

En coulisses, ces nouvelles fonctionnalités du CLI s'appuient sur la Skills API. Comme l'API renvoie des fichiers dans des formats conformes aux standards, le CLI `skills` n'a pas besoin de raisonner sur des formats de données propres à Notion. Le CLI `skills` est open source, et vous pouvez l'utiliser comme exemple de la façon d'intégrer la Skills API.

### Pour commencer

Nous pensons que chaque équipe a besoin d'une bibliothèque de compétences collaborative, disponible dans tous ses agents.

Si vous souhaitez en savoir plus sur la façon dont votre entreprise peut utiliser la bibliothèque de compétences Notion, contactez-nous.

Pour en savoir plus sur l'utilisation des compétences dans Notion, consultez la page Skills for Notion Agent de notre centre d'aide.

## Pourquoi ça compte
Ce lancement illustre la bataille en cours autour de l'infrastructure des agents IA en entreprise : au-delà du choix du modèle, la vraie friction se déplace vers la gestion, le partage et la gouvernance des « compétences » qui rendent ces agents utiles au quotidien. En misant sur l'interopérabilité (GitHub, Claude, ChatGPT, Vercel), Notion cherche à devenir la couche de contrôle collaborative de cet écosystème plutôt qu'un simple outil de prise de notes.
