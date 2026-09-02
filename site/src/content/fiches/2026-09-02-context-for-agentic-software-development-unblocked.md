---
title: "Context for agentic software development | Unblocked"
date: 2026-09-02
url: "https://link.mail.beehiiv.com/ss/c/u001._d02Us3GR26SqbxiB_QNfbCW_0mE6VIvIcMRm-rYBXdFZwDloIfsKGcxkC5KBkS3FjBaUbNL6uYFy6jbys0IFzL1j99ZwyGugbZ_UBLjFOKVTsI2xya1N-Y8zxFcariNCbq14GOTwgoD2kMy6ddT_w/4to/J86wL3ZyRZKrMW8TS6n3xA/h2/h001.2HyRnWqoTPWJWqLQeXHHTyXgIGDbIgBMUpUS3fh8DiU"
keywords: ["context engineering", "agents IA", "développement logiciel", "connaissance organisationnelle", "MCP"]
theme: "IA"
tone: "news"
used_in: ["2026-09-02"]
---

## Résumé
Unblocked se présente comme une « couche de contexte » pour le développement logiciel agentique : un moteur qui agrège code, conversations, tickets, documentation et systèmes de production dans un graphe de connaissance unique afin que les agents IA disposent du contexte nécessaire pour accomplir des tâches correctement avec moins d'intervention humaine. Le produit met en avant quatre capacités clés — résolution de conflits entre sources, raisonnement cross-source via un graphe unique, livraison respectueuse des permissions, et extraction de « mémoire organisationnelle » (conventions implicites, expertise réelle). Des témoignages clients (Webflow, Rally, RB Global) illustrent des gains en onboarding, réduction du nombre de révisions et fiabilité des agents.

## Points clés
- Objectif : donner aux agents IA une compréhension partagée de l'organisation (code, docs, tickets, Slack, production) au-delà du seul code.
- Résolution automatique des contradictions entre sources via signaux de récence, autorité et proximité, avec liens de traçabilité vers les sources.
- Un graphe de connaissance unique permet de traverser en une seule passe des relations cross-outils (ticket Jira → PR liée → fil Slack → code).
- Le contexte est scopé selon l'identité et l'historique de contribution avant récupération, puis compressé côté serveur pour limiter les tokens gaspillés.
- Extraction de conventions implicites (retours de code review, évolution du codebase) et identification de l'expertise réelle par domaine, injectées dans le contexte des agents.
- Intégration via MCP, CLI, API ou connecteurs directs ; sécurité et confidentialité présentées comme exigences fondamentales (données isolées, chiffrées, non utilisées pour l'entraînement).

## Analyse approfondie
Vos agents connaissent le code. Donnez-leur le reste du contexte.

Unblocked est la couche de contexte pour le développement logiciel agentique. Il raisonne sur votre code, vos conversations, vos tickets, votre documentation, votre produit et vos systèmes de production afin que les agents puissent accomplir leur travail correctement avec moins d'intervention humaine.

Nous avons résolu les problèmes les plus difficiles de la livraison de contexte — résolution de conflits, application des permissions, fraîcheur, pertinence et optimisation des coûts — pour que vous n'ayez pas à le faire. Connectez votre code, vos conversations, vos tickets, votre documentation, votre produit et vos systèmes de production. Unblocked raisonne sur l'ensemble pour donner à vos agents une compréhension partagée de votre organisation, afin qu'ils puissent accomplir leur travail correctement avec moins d'intervention humaine.

**À l'intérieur du Context Engine**

*Résolution de conflits et pertinence*

Une seule réponse réconciliée, personnalisée pour vous.

Les contradictions entre sources sont résolues automatiquement grâce à des signaux de récence, d'autorité et de proximité.

Les résultats sont personnalisés selon l'historique de contribution de chaque développeur, ses zones de travail actives et sa terminologie.

Chaque réponse est accompagnée de liens vers ses sources — pas de raisonnement en boîte noire, tout est traçable jusqu'à l'origine.

*Raisonnement cross-source*

Un seul graphe, toutes les sources, parcourues en une seule fois.

Le code, la documentation, les tickets et les conversations sont ingérés dans un graphe de connaissance vivant unique — pas des silos consultables séparément.

Les relations entre systèmes sont parcourues en une seule passe (un ticket Jira → une PR liée → un fil Slack → le code).

La meilleure réponse pour la tâche est transmise directement, plutôt que d'interroger séquentiellement chaque source en espérant trouver la bonne.

*Livraison respectueuse des permissions*

Scopée à vos dépôts, vos coéquipiers et votre historique de travail.

Le scoping commence par l'intention et l'identité, garantissant que chaque requête est authentifiée.

L'historique de contribution et les collaborateurs aident à affiner le périmètre de recherche avant l'exécution de la récupération.

Le contexte est noté, compressé et assemblé côté serveur — moins de tokens gaspillés, une entrée de meilleure qualité pour l'agent.

*Mémoire organisationnelle*

Les règles non écrites, rendues explicites et actionnables.

Les conventions implicites sont extraites des retours de revue de code, de l'évolution du codebase et des schémas cross-source.

La topologie d'expertise identifie qui détient réellement l'autorité dans chaque domaine — pas seulement qui la revendique.

Les règles et conventions vivantes sont injectées dans le contexte de l'agent, afin que le code généré corresponde à la façon dont l'équipe travaille réellement, pas seulement à ce que dit la documentation.

**Unblocked fonctionne partout où vous travaillez**

Connectez Unblocked à vos outils et agents en quelques minutes. Utilisez MCP, CLI, API ou des intégrations directes pour apporter du contexte à chaque workflow.

**Les équipes qui vont plus vite avec Unblocked**

Des résultats réels d'équipes réelles — onboarding plus rapide, moins de cycles de revue, et des agents IA qui restent fiables.

« Unblocked est le cerveau qui fait vraiment fonctionner nos agents. »

L'organisation de productivité d'ingénierie de Webflow fait tourner du développement agentique distant à grande échelle avec Claude, Cursor et Codex. Unblocked est le moteur de contexte qui donne à chaque ingénieur et agent IA la connaissance institutionnelle derrière un codebase de plus de 10 ans, réduisant les tokens et le travail répété, détectant les incidents passés, et rendant le code écrit par les agents sûr à merger.

L'équipe go-to-market de Rally fonctionne sur Unblocked. Elle ouvre en toute sécurité le codebase, Slack et Linear de l'entreprise aux non-ingénieurs, afin que le support, le service client et les ventes puissent répondre à toute question produit sans détourner les ingénieurs de la construction de Rally. Le CTO et co-fondateur Alec estime que cela lui fait gagner cinq à dix heures par semaine, et a réduit de 90 % les questions produit qu'il traite lui-même.

Comment l'équipe plateforme de RB Global a pris possession de sa stack en trois mois, pas six

Lorsqu'une nouvelle équipe plateforme a internalisé une stack gérée jusque-là par des consultants chez RB Global, Unblocked a été le moteur de contexte qui a transformé des années de connaissances éparpillées entre GitHub, CircleCI, Confluence, Jira et Slack en réponses instantanées. L'équipe a pris pleine possession en trois mois au lieu de six, et s'appuie désormais sur Unblocked comme bras de support pour plus de 200 développeurs.

Unblocked est conçu avec la sécurité et la confidentialité comme exigences fondamentales. Les données clients sont isolées, autorisées et chiffrées, et vos données ne seront jamais utilisées pour entraîner des modèles.

## Pourquoi ça compte
C'est un signal de plus sur la montée du « context engineering » comme couche distincte des agents eux-mêmes : au-delà du choix du modèle, la vraie friction du développement agentique en entreprise devient l'accès fiable, scopé et à jour au contexte organisationnel dispersé.
