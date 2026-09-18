---
title: "MCP Server Visibility: Finding What Employees Connected on Their Own Laptops"
date: 2026-09-18
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Frepello.ai%2Fblog%2Fmcp-server-visibility-employee-devices%3Futm_source=tldrit/1/010001a0af4cf319-1031fadd-7514-4e10-a19f-5ad4018bc42d-000000/koTUXp0rAYJd8i-59U2dZtWsVBKMmDRUisqpI7EnZtc=452"
keywords: ["MCP", "sécurité endpoint", "shadow IT", "inventaire", "credentials", "supply chain"]
theme: "Sécurité"
tone: "opinion"
used_in: ["2026-09-18"]
---

## Résumé
Les serveurs MCP sont déclarés dans des fichiers JSON propres à chaque utilisateur et à chaque client (Claude Desktop, Cursor, Claude Code, VS Code), sans console d'administration, log SSO ni signature réseau permettant de savoir ce qui est connecté à l'échelle d'une organisation. Le nom d'un serveur ne renseigne sur rien : ce qui compte est l'entrypoint résolu, le package et la version réellement exécutés (souvent via `npx` avec un tag flottant), les identifiants transmis par variables d'environnement, et le type de transport (stdio vs HTTP). L'article soutient qu'il s'agit fondamentalement d'un problème d'endpoint et non d'identité ou de réseau, puisque configuration, processus et credentials résident tous sur le poste de travail. Il se conclut par la présentation de l'outil Workstation Lens (Repello.ai), censé lire ces fichiers à l'échelle du parc pour produire un inventaire continu.

## Points clés
- Il n'existe aucune console d'administration, log SSO ou registre d'achat pour MCP : chaque client conserve sa propre configuration JSON locale, invisible aux autres.
- Ajouter un serveur MCP se résume à une simple modification de fichier texte, sans approbation ni traçabilité (pas de ticket, pas de log).
- Le nom d'un serveur (« docs », par exemple) est un simple libellé choisi par l'auteur de la config et ne garantit rien sur ce que le serveur exécute réellement.
- Les champs qui comptent réellement sont l'entrypoint résolu (un shell type `/bin/bash` donne un accès shell), le package/version effectivement exécutés, les credentials passés en variables d'environnement, et le transport (stdio local vs HTTP exposé).
- Le lancement via `npx` avec un tag flottant signifie que le code exécuté aujourd'hui est celui que le registre npm a servi le plus récemment, pas celui qui a été audité.
- Un inventaire MCP fiable doit être continu et couvrir chaque machine/utilisateur, car la configuration peut changer à tout moment sans laisser de trace.

## Analyse approfondie
**TL;DR :** Il n'existe aucune console d'administration pour MCP. Les serveurs sont déclarés dans des fichiers JSON propres à chaque utilisateur, sur des laptops individuels, un jeu de fichiers par client, et en ajouter un revient à faire une simple modification de texte qui ne nécessite aucune approbation et ne génère aucun log. Le fichier de configuration est la seule source faisant autorité sur ce qu'un employé a connecté, ce qui fait de ce sujet un problème d'inventaire des postes de travail (endpoint) plutôt qu'un problème d'identité ou de réseau.

### Poser la question de façon habituelle ne donne aucune réponse

« Quels serveurs MCP nos développeurs ont-ils connectés ? » est une question raisonnable, et chaque façon habituelle d'y répondre échoue.

Il n'y a pas de log SSO, car la plupart des serveurs MCP se lancent localement et ne s'authentifient jamais auprès de quoi que ce soit que vous contrôlez. Il n'y a pas de trace d'achat, car rien n'a été acheté. Il n'y a pas de console d'administration, car le protocole n'en définit aucune. Il n'y a pas de signature réseau, car un serveur stdio communique via un pipe entre deux processus sur la même machine.

Ce qui existe, c'est un fichier JSON dans le répertoire personnel d'un développeur, qu'il a édité à la main. Ce fichier constitue à lui seul la source de vérité, et il se trouve sur un laptop.

### Où se trouve réellement la configuration

Chaque client conserve la sienne, ce qui signifie qu'un développeur utilisant trois clients dispose de trois inventaires distincts qui s'ignorent totalement les uns les autres.

| Client | Configuration |
|---|---|
| Claude Desktop | `claude_desktop_config.json` dans le répertoire application-support de l'utilisateur |
| Cursor | `.cursor/mcp.json`, au niveau utilisateur ou projet |
| Claude Code | `.mcp.json` dans le projet, plus une configuration au niveau utilisateur |
| VS Code / Copilot | Entrées MCP au sein des paramètres de l'éditeur |

Lire l'un de ces fichiers vous renseigne sur un client, sur une machine. La question à l'échelle de l'organisation nécessite de les consulter tous, sur chaque machine, en continu — car la réponse change dès que quelqu'un modifie un fichier.

### Un nom de serveur ne garantit rien

L'erreur la plus courante lors d'un premier inventaire est de se contenter de collecter les noms des serveurs et de considérer le travail terminé. Le nom est une étiquette choisie par celui qui a écrit la configuration. Il n'est ni validé, ni enregistré, ni lié à ce que le serveur fait réellement.

Une entrée nommée `docs` peut lancer n'importe quel exécutable avec n'importe quels arguments. C'est la même faille que nous avons documentée dans Claude Code sous le nom de « confiance indexée sur le nom » (name-keyed trust) : ce qu'un utilisateur approuve et ce qui s'exécute réellement ne sont liés que par une chaîne de caractères, et cette chaîne peut être choisie par un attaquant.

Le champ qui compte réellement est donc la commande résolue. Plus précisément :

**Le point d'entrée (entrypoint).** Un serveur dont le point d'entrée est `/bin/bash`, `/bin/sh` ou `python -c` donne à l'agent connecté un shell sur le laptop. Ce n'est pas un risque subtil, et il est trivialement visible dans la configuration — encore faut-il que quelqu'un la lise.

**Le package et la version réellement exécutée.** La plupart des serveurs MCP se lancent via `npx` avec un tag flottant, qui se résout au démarrage. Le code exécuté aujourd'hui est celui que le registre a servi le plus récemment, pas celui que quelqu'un a réellement vérifié. Nous avons détaillé ce que cela signifie en pratique dans notre analyse du serveur MCP Figma, où une CVE a été corrigée dans une version de patch que la plupart des utilisateurs ont reçue sans jamais avoir décidé de l'installer.

**Les identifiants (credentials).** Les clés API et les tokens sont couramment transmis aux serveurs MCP via des variables d'environnement, dans ce même fichier de configuration. Un inventaire qui recense les noms des serveurs mais pas ce qui leur a été confié est passé à côté de la partie dont une équipe sécurité a le plus besoin.

**Le transport.** stdio et HTTP présentent une exposition très différente, comme l'ont démontré les trois CVE du serveur MCP n8n — les trois nécessitaient le mode multi-tenant HTTP, et aucune ne concerne un déploiement stdio local.

### Pourquoi il s'agit d'un problème d'endpoint

Il est tentant de traiter ce sujet comme un problème d'identité et de le résoudre avec des tokens et des scopes. Cela aide pour les serveurs distants adossés à OAuth, mais cela ne fait rien pour la majorité des cas, qui sont des processus locaux lancés par un fichier de configuration.

Il est tout aussi tentant de le traiter comme un problème réseau. Cela échoue pour la même raison que la détection des LLM locaux échoue au niveau réseau : un serveur stdio dialogue avec son client via un pipe, et rien ne transite par une interface que l'on peut surveiller.

Le fichier de configuration est sur le poste de travail (endpoint). Le processus est sur l'endpoint. Les identifiants sont sur l'endpoint. Toute réponse qui ne lit pas l'endpoint relève de la déduction, et c'est précisément ainsi que l'on finit par annoncer avec assurance un chiffre erroné.

### Ce qu'un véritable inventaire doit recenser

Par machine, par utilisateur, et actualisé en continu plutôt que capturé une seule fois :

- Quels clients agents sont installés et en cours d'exécution
- Quels serveurs MCP chaque client déclare
- Le point d'entrée résolu pour chaque serveur déclaré
- Le package et la version réellement exécutés, et non ceux nominalement épinglés (pinned)
- Les identifiants et secrets transmis via l'environnement
- Le transport, et pour les serveurs HTTP, ce à quoi ils sont exposés

Cette liste n'a rien d'exotique. Il s'agit d'une poignée de fichiers et d'une table des processus, soit exactement le type de données qu'un agent endpoint collecte déjà pour d'autres raisons. Le problème, c'est que personne ne lui a jamais posé ces questions.

Pour évaluer les propriétés de sécurité de serveurs spécifiques une fois que vous savez ce que vous avez, notre guide de sécurité MCP couvre cette évaluation, et nos analyses par éditeur — dont celle de GitHub — détaillent ce à quoi chaque serveur peut accéder.

### FAQ

#### Comment obtenir de la visibilité sur les connexions aux serveurs MCP effectuées par les employés depuis leurs laptops ?

Il faut lire les fichiers de configuration des clients, car ce sont la seule source faisant autorité. Les serveurs MCP sont déclarés dans des fichiers JSON propres à chaque utilisateur sur chaque machine — Claude Desktop, Cursor, VS Code et Claude Code conservent chacun les leurs — et il n'existe ni registre central, ni console d'administration, ni log SSO à interroger à la place. Un outillage endpoint capable de lire ces fichiers, de résoudre ce que chaque entrée lance réellement, et de le remonter de façon centralisée, est la seule approche qui produise un véritable inventaire.

#### Existe-t-il une console d'administration pour les serveurs MCP ?

Non, et il s'agit d'un problème structurel plutôt que d'une lacune laissée par tel ou tel éditeur. MCP a été conçu pour qu'un client local lance un serveur local pour le compte d'un seul utilisateur. Rien dans le protocole ne définit un plan de contrôle organisationnel, un workflow d'approbation, ou un moyen pour quiconque d'autre que l'utilisateur de voir ce qui est connecté. Ajouter un serveur revient à modifier un fichier texte, et cela ne nécessite l'approbation de personne.

#### Où sont stockées les configurations des serveurs MCP ?

Dans des fichiers propres à chaque client, situés dans le répertoire personnel de l'utilisateur. Claude Desktop utilise `claude_desktop_config.json`, Cursor lit `.cursor/mcp.json` au niveau utilisateur ou projet, Claude Code utilise `.mcp.json` en complément d'une configuration au niveau utilisateur, et VS Code conserve les entrées MCP dans ses paramètres. Un développeur utilisant trois clients dispose de trois inventaires distincts, dont aucun n'a connaissance des autres.

#### Pourquoi une liste de noms de serveurs ne suffit-elle pas ?

Parce que le nom est choisi par celui qui a écrit la configuration et ne contraint rien. Une entrée intitulée « docs » peut lancer n'importe quel exécutable avec n'importe quels arguments. Ce qui compte, c'est la commande résolue — le binaire, le package et la version qu'il récupère, ainsi que les variables d'environnement et les identifiants qui lui sont transmis. Un serveur dont le point d'entrée pointe vers un shell donne un shell à l'agent connecté.

#### Que doit réellement recenser un inventaire MCP ?

Par machine et par utilisateur : quels clients sont installés, quels serveurs chacun déclare, le point d'entrée résolu de chaque serveur, la version du package réellement exécutée plutôt que celle épinglée, les identifiants transmis via les variables d'environnement, et le transport. Les versions comptent car la plupart des serveurs se lancent via `npx` avec un tag flottant, si bien que le code exécuté aujourd'hui est celui que le registre a servi le plus récemment.

#### À quelle fréquence cet inventaire change-t-il ?

En continu, et sans le moindre événement visible par ailleurs. Installer un serveur MCP consiste à modifier un fichier texte puis à redémarrer le client. Il n'y a ni ticket, ni étape d'achat, ni trace de connexion. Un inventaire capturé une seule fois n'est que la photographie d'une configuration qui a peut-être déjà changé, ce qui explique pourquoi cela doit être une mesure permanente plutôt qu'un audit ponctuel.

### Lire les fichiers de configuration à l'échelle du parc

L'inventaire existe. Il est dispersé dans des fichiers JSON propres à chaque utilisateur, sur chaque laptop, et rien ne le collecte. Workstation Lens lit ces fichiers à l'échelle du parc, résout ce que chaque serveur lance réellement, signale les points d'entrée pointant vers un shell, et remonte les versions véritablement exécutées.

## Pourquoi ça compte
Ce papier met en lumière un angle mort critique de l'adoption rapide de MCP en entreprise : un shadow IT invisible généré par les agents IA locaux, avec des risques concrets de fuite de credentials et d'exécution shell non contrôlée sur les postes de travail. Pour la veille sécurité, il illustre pourquoi les modèles classiques de contrôle (identité, réseau) ne suffisent plus face à des protocoles conçus pour un usage local et sans gouvernance centralisée.
