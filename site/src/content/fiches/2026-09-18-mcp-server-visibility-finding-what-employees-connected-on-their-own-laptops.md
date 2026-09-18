---
title: "MCP Server Visibility: Finding What Employees Connected on Their Own Laptops"
date: 2026-09-18
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Frepello.ai%2Fblog%2Fmcp-server-visibility-employee-devices%3Futm_source=tldrit/1/010001a0af4cf319-1031fadd-7514-4e10-a19f-5ad4018bc42d-000000/koTUXp0rAYJd8i-59U2dZtWsVBKMmDRUisqpI7EnZtc=452"
keywords: ["MCP", "shadow IT", "endpoint", "inventaire", "supply chain", "DevSecOps"]
theme: "Sécurité"
tone: "opinion"
used_in: ["2026-09-18"]
---

## Résumé
L'article de Repello AI soutient qu'il n'existe aucune console d'administration pour le Model Context Protocol (MCP) : chaque serveur MCP est déclaré dans un fichier JSON local, propre à chaque client (Claude Desktop, Cursor, Claude Code, VS Code), qu'un développeur peut modifier sans validation ni journalisation. Il en résulte qu'aucune méthode classique (SSO, achat, console d'admin, signature réseau) ne permet de savoir quels serveurs MCP sont réellement connectés sur le parc de postes. L'auteur montre que le nom d'un serveur ne dit rien de ce qu'il exécute réellement, et qu'un inventaire fiable doit lire la configuration résolue (binaire, package, version, identifiants, transport) directement sur le poste de travail. La conclusion : il s'agit d'un problème d'endpoint, pas d'identité ni de réseau, qui appelle une mesure continue plutôt qu'un audit ponctuel.

## Points clés
- MCP ne dispose d'aucun registre central : chaque client (Claude Desktop, Cursor, Claude Code, VS Code/Copilot) stocke sa propre configuration JSON dans le profil de l'utilisateur, sans lien entre elles.
- Ajouter un serveur MCP est une simple modification de fichier texte, sans approbation ni trace d'audit.
- Le nom d'un serveur est arbitraire et ne garantit rien : une entrée nommée « docs » peut en réalité lancer n'importe quel exécutable (y compris un shell) avec n'importe quel argument.
- Ce qui compte réellement, c'est la commande résolue : le point d'entrée exécuté, le package et sa version réellement installée (souvent via `npx` avec un tag flottant), les identifiants transmis via des variables d'environnement, et le type de transport (stdio local vs HTTP exposé).
- Ni les outils d'identité (tokens, scopes) ni la surveillance réseau ne suffisent, car la majorité des serveurs sont des processus locaux communiquant par pipe (stdio) invisibles sur le réseau.
- Un inventaire pertinent doit être recueilli au niveau de l'endpoint, par machine et par utilisateur, et rafraîchi en continu plutôt que capturé une seule fois.

## Analyse approfondie
**Poser la question de façon classique ne donne aucune réponse**
Demander « quels serveurs MCP nos développeurs ont-ils connectés ? » semble une question raisonnable, mais toutes les méthodes habituelles pour y répondre échouent. Il n'y a pas de journal SSO, car la plupart des serveurs MCP démarrent localement sans jamais s'authentifier auprès d'un système contrôlé par l'entreprise. Il n'y a pas de trace d'achat, puisque rien n'a été acheté. Il n'y a pas de console d'administration, car le protocole n'en définit aucune. Il n'y a pas de signature réseau, car un serveur en mode stdio communique via un tube (pipe) entre deux processus sur la même machine. Ce qui existe réellement, c'est un fichier JSON dans le répertoire personnel d'un développeur, édité à la main. Ce fichier constitue la seule source de vérité, et il se trouve sur un ordinateur portable.

**Où se trouve réellement la configuration**
Chaque client conserve sa propre configuration, ce qui signifie qu'un développeur utilisant trois clients a trois inventaires distincts qui s'ignorent mutuellement :

| Client | Configuration |
|---|---|
| Claude Desktop | `claude_desktop_config.json`, dans le répertoire application-support de l'utilisateur |
| Cursor | `.cursor/mcp.json`, au niveau utilisateur ou projet |
| Claude Code | `.mcp.json` dans le projet, plus une configuration au niveau utilisateur |
| VS Code / Copilot | entrées MCP intégrées aux paramètres de l'éditeur |

Lire l'un de ces fichiers ne renseigne que sur un client, sur une machine. La question organisationnelle nécessite de les agréger tous, sur toutes les machines, en continu — car la réponse change dès qu'un fichier est modifié.

**Un nom de serveur ne garantit rien**
L'erreur la plus fréquente dans un premier inventaire est de se contenter de collecter les noms des serveurs. Le nom est un simple libellé choisi par celui qui a écrit la configuration : il n'est ni validé, ni enregistré, ni lié à ce que le serveur fait réellement. Une entrée appelée « docs » peut lancer n'importe quel exécutable avec n'importe quel argument. C'est le même défaut que celui déjà documenté dans Claude Code sous le nom de « confiance indexée par le nom » : ce que l'utilisateur approuve et ce qui s'exécute réellement ne sont reliés que par une chaîne de caractères, et cette chaîne peut être choisie par un attaquant.

Ce qui compte donc, c'est la commande résolue, en particulier :

- **Le point d'entrée.** Un serveur dont le point d'entrée est `/bin/bash`, `/bin/sh` ou `python -c` donne à l'agent connecté un accès shell sur le poste. Ce n'est pas un risque subtil, et il est parfaitement visible dans la configuration — encore faut-il la lire.
- **Le package et la version réellement exécutée.** La plupart des serveurs MCP démarrent via `npx` avec un tag flottant, résolu au lancement. Le code exécuté aujourd'hui est celui que le registre a servi le plus récemment, pas celui qui a été revu par quelqu'un. L'article de Repello sur le serveur MCP Figma illustre ce cas concret, où une CVE a été corrigée dans une version mineure que la plupart des utilisateurs ont reçue sans jamais prendre de décision explicite.
- **Les identifiants.** Les clés API et jetons sont couramment transmis aux serveurs MCP via des variables d'environnement, dans le même fichier de configuration. Un inventaire qui note les noms de serveurs sans noter ce qui leur a été confié passe à côté de l'élément le plus critique pour une équipe sécurité.
- **Le transport.** stdio et HTTP présentent des surfaces d'exposition très différentes, comme l'ont montré les trois CVE du serveur MCP n8n — toutes trois nécessitaient le mode HTTP multi-tenant, et aucune n'affecte un déploiement stdio local.

**Pourquoi c'est un problème d'endpoint**
Il est tentant de traiter ce sujet comme un problème d'identité, à résoudre avec des jetons et des scopes. Cela aide pour les serveurs distants authentifiés via OAuth, mais ne résout rien pour la majorité des cas, qui sont des processus locaux lancés depuis un fichier de configuration. Il est tout aussi tentant d'en faire un problème réseau. Cela échoue pour la même raison que la détection des LLM locaux échoue au niveau réseau : un serveur stdio dialogue avec son client via un tube, sans jamais traverser une interface observable. La configuration est sur l'endpoint. Le processus est sur l'endpoint. Les identifiants sont sur l'endpoint. Toute réponse qui ne lit pas l'endpoint relève de la déduction — et la déduction, c'est ainsi qu'on finit par annoncer avec assurance un chiffre erroné.

**Ce qu'un véritable inventaire doit enregistrer**
Par machine, par utilisateur, et actualisé en continu plutôt que capturé une seule fois :
- quels clients agents sont installés et actifs ;
- quels serveurs MCP chaque client déclare ;
- le point d'entrée résolu pour chaque serveur déclaré ;
- le package et la version réellement en cours d'exécution, et non celle nominalement épinglée ;
- les identifiants et secrets transmis via l'environnement ;
- le transport utilisé, et pour les serveurs HTTP, leur surface d'exposition.

Cette liste n'a rien d'exotique : ce sont quelques fichiers et une table des processus, soit exactement le type de données qu'un agent d'endpoint collecte déjà pour d'autres besoins. Le problème, c'est que personne ne lui a encore posé ces questions. Pour évaluer la sécurité d'un serveur donné une fois l'inventaire établi, le guide de sécurité MCP de Repello traite de l'évaluation, et ses analyses par éditeur — dont GitHub — détaillent ce que chaque serveur peut atteindre.

**FAQ**

*Comment obtenir de la visibilité sur les connexions aux serveurs MCP effectuées par les employés depuis leurs ordinateurs portables ?*
En lisant les fichiers de configuration des clients, seule source de vérité fiable. Les serveurs MCP sont déclarés dans des fichiers JSON propres à chaque utilisateur sur chaque machine — Claude Desktop, Cursor, VS Code et Claude Code ont chacun le leur — et il n'existe ni registre central, ni console d'administration, ni journal SSO à interroger à la place. Seul un outil d'endpoint capable de lire ces fichiers, de résoudre ce que chaque entrée lance réellement, et de centraliser le rapport, permet d'obtenir un inventaire véritable.

*Existe-t-il une console d'administration pour les serveurs MCP ?*
Non, et il s'agit d'un problème structurel plutôt que d'une lacune laissée par un éditeur en particulier. MCP a été conçu pour qu'un client local lance un serveur local pour le compte d'un seul utilisateur. Rien dans le protocole ne définit un plan de contrôle organisationnel, un flux d'approbation, ni un moyen pour quelqu'un d'autre que l'utilisateur de voir ce qui est connecté. Ajouter un serveur est une simple modification de texte, sans approbation requise.

*Où sont stockées les configurations des serveurs MCP ?*
Dans des fichiers propres à chaque client, situés dans le répertoire personnel de l'utilisateur. Claude Desktop utilise `claude_desktop_config.json`, Cursor lit `.cursor/mcp.json` au niveau utilisateur ou projet, Claude Code utilise `.mcp.json` avec une configuration complémentaire au niveau utilisateur, et VS Code conserve ses entrées MCP dans ses paramètres. Un développeur utilisant trois clients dispose donc de trois inventaires distincts, sans lien entre eux.

*Pourquoi une simple liste de noms de serveurs n'est-elle pas suffisante ?*
Parce que le nom est choisi par l'auteur de la configuration et ne garantit rien. Une entrée nommée « docs » peut lancer n'importe quel exécutable avec n'importe quel argument. Ce qui compte, c'est la commande résolue — le binaire, le package et sa version, ainsi que les variables d'environnement et identifiants qui lui sont transmis. Un serveur dont le point d'entrée pointe vers un shell donne un accès shell à l'agent connecté.

*Que doit réellement enregistrer un inventaire MCP ?*
Par machine et par utilisateur : quels clients sont installés, quels serveurs chacun déclare, le point d'entrée résolu de chaque serveur, la version du package réellement exécutée plutôt que celle nominalement épinglée, les identifiants transmis via les variables d'environnement, et le transport utilisé. Les versions comptent particulièrement, car la plupart des serveurs démarrent via `npx` avec un tag flottant, si bien que le code exécuté aujourd'hui est celui que le registre a servi le plus récemment.

*À quelle fréquence cet inventaire change-t-il ?*
En continu, et sans aucun événement visible autrement. Installer un serveur MCP consiste en une modification de texte suivie d'un redémarrage du client : pas de ticket, pas d'étape d'achat, pas de trace de connexion. Un inventaire capturé une seule fois n'est que la photographie d'une configuration potentiellement déjà obsolète, d'où la nécessité d'une mesure permanente plutôt que d'un audit ponctuel.

**Lire les fichiers de configuration à l'échelle du parc**
L'inventaire existe bel et bien : il est dispersé dans des fichiers JSON propres à chaque utilisateur, sur chaque poste, et rien ne le centralise. L'outil Workstation Lens de Repello lit ces fichiers à l'échelle du parc, résout ce que chaque serveur lance réellement, signale les points d'entrée pointant vers un shell, et rapporte les versions effectivement en cours d'exécution.

## Pourquoi ça compte
Ce texte met en lumière un angle mort de sécurité largement sous-estimé dans l'adoption rapide de MCP en entreprise : l'absence de gouvernance centralisée transforme chaque poste de développeur en source potentielle de shadow IT et de supply-chain risk. Pour une veille tech, c'est un signal fort que la sécurisation des agents IA doit désormais passer par l'endpoint, au même titre que l'EDR classique.
