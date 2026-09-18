---
title: "MCP Server Visibility: Finding What Employees Connected on Their Own Laptops"
date: 2026-09-18
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Frepello.ai%2Fblog%2Fmcp-server-visibility-employee-devices%3Futm_source=tldrit/1/010001a0af4cf319-1031fadd-7514-4e10-a19f-5ad4018bc42d-000000/koTUXp0rAYJd8i-59U2dZtWsVBKMmDRUisqpI7EnZtc=452"
keywords: ["MCP", "shadow IT", "sécurité endpoint", "inventaire", "postes de travail", "credentials"]
theme: "Sécurité"
tone: "opinion"
used_in: ["2026-09-18"]
---

## Résumé
L'article de Repello.ai montre qu'il n'existe aucun moyen centralisé de savoir quels serveurs MCP (Model Context Protocol) les développeurs ont connectés à leurs outils d'IA (Claude Desktop, Cursor, Claude Code, VS Code/Copilot). Chaque client stocke sa propre configuration dans un fichier JSON local, modifiable sans approbation ni journalisation, ce qui rend la question purement organisationnelle impossible à répondre via les canaux classiques (SSO, achats, console d'admin, surveillance réseau). L'auteur insiste sur le fait qu'un simple nom de serveur ne dit rien de ce qu'il exécute réellement : ce qui compte, c'est la commande résolue, le package et sa version, les identifiants transmis, et le protocole de transport. Il en conclut que c'est un problème de sécurité des postes de travail (endpoint), pas d'identité ni de réseau, et présente en conclusion l'outil Workstation Lens de Repello.ai comme réponse.

## Points clés
- Aucun registre central n'existe pour MCP : chaque client (Claude Desktop, Cursor, Claude Code, VS Code) garde sa propre configuration JSON locale, non synchronisée entre elles.
- Ajouter un serveur MCP est une simple édition de texte, sans approbation ni trace d'audit — l'inventaire change en continu et sans événement observable.
- Le nom donné à un serveur ne garantit rien : un serveur appelé « docs » peut en réalité lancer n'importe quel exécutable, y compris un shell.
- Les éléments réellement significatifs sont : le point d'entrée résolu, le package/version effectivement exécuté (souvent via `npx` avec un tag flottant, donc non figé), les identifiants passés en variables d'environnement, et le type de transport (stdio vs HTTP).
- Ni une approche identité (tokens/OAuth) ni une approche réseau ne suffisent, car la majorité des serveurs sont des processus locaux communiquant par pipe stdio, invisibles au niveau réseau.
- Un inventaire fiable doit être mesuré en continu, par machine et par utilisateur, en lisant directement les fichiers de configuration et la table des processus.

## Analyse approfondie

**Le problème de départ**
Poser la question « quels serveurs MCP nos développeurs ont-ils connectés ? » semble anodine, mais aucune méthode habituelle n'y répond. Il n'y a pas de journal SSO, car la plupart des serveurs MCP tournent localement sans jamais s'authentifier auprès d'un système contrôlé par l'entreprise. Il n'y a pas de trace d'achat, puisque rien n'est acheté. Il n'y a pas de console d'administration, car le protocole n'en prévoit pas. Il n'y a pas de signature réseau, car un serveur en mode stdio communique via un simple pipe entre deux processus sur la même machine. La seule source de vérité est un fichier JSON dans le répertoire personnel d'un développeur, qu'il a édité lui-même — et ce fichier se trouve sur un ordinateur portable, hors de portée des outils de gouvernance classiques.

**Où vit réellement la configuration**
Chaque client garde sa propre configuration, ce qui signifie qu'un développeur utilisant trois outils a trois inventaires distincts qui s'ignorent mutuellement :
- Claude Desktop : fichier `claude_desktop_config.json` dans le répertoire applicatif de l'utilisateur.
- Cursor : fichier `.cursor/mcp.json`, au niveau utilisateur ou projet.
- Claude Code : fichier `.mcp.json` dans le projet, complété par une configuration au niveau utilisateur.
- VS Code / Copilot : entrées MCP intégrées aux paramètres de l'éditeur.

Lire un seul de ces fichiers ne renseigne que sur un client, sur une machine. La question organisationnelle exige de tous les agréger, sur toutes les machines, en continu — car la réponse change dès qu'un fichier est modifié.

**Pourquoi un nom de serveur ne suffit pas**
L'erreur la plus fréquente dans un premier inventaire est de se contenter de collecter les noms des serveurs. Ce nom est un simple libellé choisi par celui qui a écrit la configuration : il n'est ni validé, ni enregistré, ni lié à ce que le serveur fait réellement. Une entrée nommée « docs » peut très bien lancer n'importe quel exécutable avec n'importe quels arguments. L'auteur rapproche cela d'un problème déjà documenté dans Claude Code, la « confiance indexée par le nom » : ce que l'utilisateur approuve et ce qui s'exécute réellement ne sont reliés que par une chaîne de caractères, que l'attaquant peut choisir librement.

Ce qui importe, c'est donc la commande réellement résolue :
- *Le point d'entrée* : un serveur dont le point d'entrée est `/bin/bash`, `/bin/sh` ou `python -c` donne en pratique un accès shell à l'agent connecté sur la machine. Ce risque, loin d'être subtil, est pourtant visible dans la configuration — à condition que quelqu'un la lise.
- *Le package et la version réellement exécutée* : la plupart des serveurs MCP se lancent via `npx` avec une étiquette de version flottante, résolue au démarrage. Le code exécuté aujourd'hui est donc celui le plus récemment publié par le registre, pas nécessairement celui qui a été audité. L'auteur cite en exemple un correctif de CVE sur le serveur MCP de Figma, livré silencieusement à la plupart des utilisateurs sans qu'ils aient rien décidé.
- *Les identifiants* : des clés d'API et jetons sont couramment transmis aux serveurs MCP via des variables d'environnement, dans ce même fichier de configuration. Un inventaire qui note les noms de serveurs sans noter ce qui leur a été confié passe à côté de l'élément le plus critique pour une équipe sécurité.
- *Le transport* : stdio et HTTP présentent des surfaces d'exposition très différentes, comme l'ont montré les trois CVE du serveur MCP n8n — toutes nécessitaient un mode HTTP multi-tenant, aucune n'affectait un déploiement stdio local.

**Pourquoi c'est un problème de poste de travail (endpoint)**
Il est tentant de traiter ce sujet comme un problème d'identité, à résoudre avec des jetons et des scopes. Cela aide pour les serveurs distants adossés à OAuth, mais ne change rien pour la majorité des cas, qui sont des processus locaux lancés depuis un fichier de configuration. Il est tout aussi tentant d'en faire un problème réseau — mais cela échoue pour la même raison que la détection des LLM locaux échoue au niveau réseau : un serveur stdio parle à son client via un pipe, sans jamais traverser une interface observable. Le fichier de configuration, le processus et les identifiants sont tous sur le poste de travail. Toute réponse qui ne lit pas directement l'endpoint relève de la déduction — et déduire, c'est risquer d'annoncer avec assurance un chiffre faux.

**Ce que doit contenir un inventaire sérieux**
Par machine, par utilisateur, et rafraîchi en continu plutôt que capturé une seule fois :
- Quels clients agents sont installés et actifs.
- Quels serveurs MCP chaque client déclare.
- Le point d'entrée résolu pour chaque serveur déclaré.
- Le package et la version réellement en cours d'exécution, et non celle nominalement épinglée.
- Les identifiants et secrets transmis via l'environnement.
- Le type de transport, et pour les serveurs HTTP, ce à quoi ils sont exposés.

Cette liste n'a rien d'exotique : il s'agit d'un ensemble de fichiers et d'une table de processus, données qu'un agent d'endpoint collecte déjà pour d'autres besoins. Ce qui manque, c'est que personne ne lui pose ces questions.

**FAQ**

*Comment obtenir une visibilité sur les connexions MCP effectuées par les employés depuis leurs ordinateurs portables ?*
En lisant les fichiers de configuration des clients, seule source faisant autorité. Les serveurs MCP sont déclarés dans des fichiers JSON propres à chaque utilisateur — Claude Desktop, Cursor, VS Code et Claude Code ayant chacun les leurs — sans registre central, console d'admin ni journal SSO à interroger à la place. Seul un outillage d'endpoint capable de lire ces fichiers, de résoudre ce que chaque entrée lance réellement, et de le remonter de façon centralisée, produit un inventaire fiable.

*Existe-t-il une console d'administration pour les serveurs MCP ?*
Non, et il s'agit d'un problème structurel, pas d'une lacune propre à un éditeur. MCP a été conçu pour qu'un client local lance un serveur local pour le compte d'un seul utilisateur. Rien dans le protocole ne définit de plan de contrôle organisationnel, de workflow d'approbation, ni de moyen pour quiconque autre que l'utilisateur de voir ce qui est connecté. Ajouter un serveur est une simple édition de texte, sans approbation requise.

*Où sont stockées les configurations des serveurs MCP ?*
Dans des fichiers propres à chaque client, dans le répertoire personnel de l'utilisateur : `claude_desktop_config.json` pour Claude Desktop, `.cursor/mcp.json` (niveau utilisateur ou projet) pour Cursor, `.mcp.json` plus une configuration utilisateur pour Claude Code, et des entrées dans les paramètres pour VS Code. Un développeur utilisant trois clients a donc trois inventaires distincts, qui s'ignorent entre eux.

*Pourquoi une liste de noms de serveurs ne suffit-elle pas ?*
Parce que le nom est choisi par l'auteur de la configuration et ne contraint rien. Une entrée nommée « docs » peut lancer n'importe quel exécutable avec n'importe quels arguments. Ce qui compte, c'est la commande résolue — le binaire, le package et sa version, ainsi que les variables d'environnement et identifiants qui lui sont confiés. Un serveur dont le point d'entrée pointe vers un shell donne un accès shell à l'agent connecté.

*Que doit réellement enregistrer un inventaire MCP ?*
Par machine et par utilisateur : les clients installés, les serveurs déclarés par chacun, le point d'entrée résolu pour chaque serveur, la version du package réellement exécutée (plutôt que celle nominalement épinglée), les identifiants transmis via l'environnement, et le transport utilisé. Les versions comptent particulièrement car la plupart des serveurs se lancent via `npx` avec une étiquette flottante : le code exécuté aujourd'hui est celui le plus récemment publié par le registre.

*À quelle fréquence cet inventaire évolue-t-il ?*
En continu, et sans aucun événement visible par ailleurs. Installer un serveur MCP se résume à une édition de texte suivie d'un redémarrage du client — pas de ticket, pas d'étape d'achat, pas de trace de connexion. Un inventaire capturé une seule fois n'est que l'instantané d'une configuration potentiellement déjà obsolète : il faut donc une mesure permanente plutôt qu'un audit ponctuel.

**Conclusion de l'article**
L'inventaire existe déjà, mais il est dispersé dans des fichiers JSON propres à chaque utilisateur, sur chaque poste, et rien ne le centralise aujourd'hui. L'article se conclut par la présentation de Workstation Lens, l'outil de Repello.ai, qui lit ces fichiers à l'échelle du parc informatique, résout ce que chaque serveur lance réellement, signale les points d'entrée pointant vers un shell, et remonte les versions effectivement en service.

## Pourquoi ça compte
Avec l'adoption rapide de MCP dans les outils de développement assistés par IA, cet article met en lumière un angle mort de sécurité concret et actuel : un shadow IT invisible aux couches identité et réseau, qui échappe aux dispositifs de gouvernance existants et nécessite une réponse au niveau du poste de travail.
