---
title: "MCP Server Visibility: Finding What Employees Connected on Their Own Laptops"
date: 2026-09-18
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Frepello.ai%2Fblog%2Fmcp-server-visibility-employee-devices%3Futm_source=tldrit/1/010001a0af4cf319-1031fadd-7514-4e10-a19f-5ad4018bc42d-000000/koTUXp0rAYJd8i-59U2dZtWsVBKMmDRUisqpI7EnZtc=452"
keywords: ["MCP", "shadow IT", "endpoint", "inventaire", "agents IA", "supply chain"]
theme: "Sécurité"
tone: "opinion"
used_in: ["2026-09-18"]
---

## Résumé
L'article de Repello AI expose un angle mort de sécurité propre au Model Context Protocol (MCP) : il n'existe aucune console d'administration centrale pour savoir quels serveurs MCP un employé a connectés sur sa machine. La configuration vit uniquement dans des fichiers JSON par utilisateur et par client (Claude Desktop, Cursor, Claude Code, VS Code), qu'un développeur peut modifier sans validation ni trace. L'auteur montre que le nom d'un serveur ne dit rien de ce qu'il exécute réellement, et que ce qui compte est la commande résolue : binaire lancé, version du paquet réellement exécutée, identifiants transmis et transport utilisé. Il en conclut qu'il s'agit d'un problème de visibilité sur le poste de travail (endpoint), pas d'un problème d'identité ni de réseau, et propose une liste de ce qu'un inventaire MCP sérieux devrait recueillir.

## Points clés
- Il n'existe ni SSO, ni registre d'achats, ni console d'admin, ni signature réseau pour les serveurs MCP : le fichier de config JSON sur le poste de l'employé est la seule source de vérité.
- Chaque client (Claude Desktop, Cursor, Claude Code, VS Code/Copilot) maintient sa propre configuration, isolée des autres, ce qui multiplie les inventaires partiels par machine.
- Le nom déclaré d'un serveur ne garantit rien : une entrée appelée « docs » peut en réalité lancer n'importe quel exécutable, y compris un shell (`/bin/bash`, `python -c`).
- Beaucoup de serveurs se lancent via `npx` avec un tag flottant : le code réellement exécuté est celui livré par le registre au moment du lancement, pas celui qui a été audité.
- Les identifiants (clés API, tokens) transitent souvent en clair dans les variables d'environnement du même fichier de configuration, un point aveugle si l'inventaire ne capture que les noms de serveurs.
- Le transport (stdio local vs HTTP) change radicalement la surface d'exposition ; les vulnérabilités passées (ex. serveur MCP n8n) ne concernaient que le mode HTTP multi-tenant, pas les déploiements stdio locaux.

## Analyse approfondie
**Une question simple sans réponse disponible.** Demander « quels serveurs MCP nos développeurs ont-ils connectés ? » semble anodin, mais aucun canal habituel ne permet d'y répondre : pas de journal SSO (la plupart des serveurs MCP tournent en local sans jamais s'authentifier auprès d'un système central), pas de trace d'achat (rien n'a été acheté), pas de console d'admin (le protocole n'en définit aucune), pas de signature réseau (un serveur en stdio communique via un simple pipe entre deux processus sur la même machine). La seule chose qui existe est un fichier JSON édité à la main dans le répertoire personnel d'un développeur — posé sur un poste de travail, hors de portée des outils classiques de gouvernance.

**Une configuration éclatée par client.** Chaque client garde sa propre déclaration de serveurs, sans lien avec les autres : `claude_desktop_config.json` pour Claude Desktop, `.cursor/mcp.json` (au niveau utilisateur ou projet) pour Cursor, `.mcp.json` plus une configuration utilisateur pour Claude Code, et des entrées MCP dans les paramètres de l'éditeur pour VS Code/Copilot. Lire un seul de ces fichiers ne renseigne que sur un client, sur une machine. Répondre à la question au niveau de l'organisation suppose de les agréger tous, sur tous les postes, en continu — car la réponse change dès qu'un fichier est modifié.

**Le nom d'un serveur ne contraint rien.** L'erreur la plus fréquente dans un premier inventaire consiste à se contenter de collecter des noms de serveurs. Ce nom est un simple libellé choisi par l'auteur de la configuration : il n'est ni validé, ni enregistré dans un registre, ni lié techniquement à ce que le serveur fait réellement. Une entrée nommée « docs » peut très bien lancer n'importe quel exécutable avec n'importe quels arguments. L'article rapproche ce constat d'un biais déjà documenté dans Claude Code, la « confiance indexée par le nom » : ce que l'utilisateur approuve et ce qui s'exécute réellement ne sont reliés que par une chaîne de caractères, et cette chaîne peut être choisie par un attaquant.

Ce qui compte vraiment, c'est la commande résolue, et plus précisément quatre éléments :
- **Le point d'entrée** : un serveur dont l'entrypoint pointe vers `/bin/bash`, `/bin/sh` ou `python -c` donne de fait un accès shell à l'agent connecté sur la machine — un risque visible dès lors qu'on lit effectivement la configuration.
- **Le paquet et la version réellement exécutée** : la plupart des serveurs MCP se lancent via `npx` avec un tag flottant, résolu au moment du démarrage. Le code qui tourne aujourd'hui est celui que le registre a servi le plus récemment, pas celui qui a été revu par quelqu'un — un parallèle est fait avec un cas déjà traité par les auteurs concernant le serveur MCP de Figma, où un correctif de sécurité (CVE) a été appliqué silencieusement via une version mineure que la plupart des utilisateurs ont reçue sans jamais en décider.
- **Les identifiants** : clés API et tokens sont couramment transmis aux serveurs MCP via des variables d'environnement, dans le même fichier de configuration. Un inventaire qui note les noms de serveurs sans noter ce qui leur a été confié passe à côté de l'information la plus sensible pour une équipe sécurité.
- **Le transport** : stdio et HTTP présentent une exposition très différente, comme l'ont montré les trois CVE du serveur MCP n8n — toutes nécessitaient le mode HTTP multi-tenant, aucune n'affectait un déploiement stdio local.

**Pourquoi c'est un problème d'endpoint, pas d'identité ni de réseau.** Il est tentant de traiter ce sujet comme un problème d'identité, à résoudre avec des tokens et des scopes : cela fonctionne pour les serveurs distants adossés à OAuth, mais ne dit rien de la majorité des cas, des processus locaux lancés depuis un fichier de configuration. Il est tout aussi tentant d'en faire un problème réseau, ce qui échoue pour la même raison que la détection des LLM locaux échoue au niveau réseau : un serveur en stdio dialogue avec son client via un pipe, sans jamais franchir une interface observable. Le fichier de configuration, le processus et les identifiants sont tous sur le poste de travail. Toute réponse qui ne lit pas directement l'endpoint relève de l'inférence — et l'inférence, c'est le meilleur moyen de rapporter en toute confiance un chiffre faux.

**Ce qu'un inventaire sérieux doit enregistrer**, par machine et par utilisateur, de façon rafraîchie en continu plutôt que capturée une fois :
- quels clients agents sont installés et actifs ;
- quels serveurs MCP chaque client déclare ;
- le point d'entrée résolu pour chaque serveur déclaré ;
- le paquet et la version effectivement en cours d'exécution, et non celle nominalement épinglée ;
- les identifiants et secrets transmis via l'environnement ;
- le transport utilisé, et pour les serveurs HTTP, leur surface d'exposition.

L'article souligne que cette liste n'a rien d'exotique : il s'agit d'une poignée de fichiers et d'une table de processus, données qu'un agent d'endpoint collecte déjà pour d'autres besoins. Le manque, selon lui, n'est pas technique mais organisationnel — personne ne pose encore ces questions-là à l'agent d'endpoint. Pour évaluer ensuite la sécurité de serveurs spécifiques une fois l'inventaire établi, l'article renvoie vers un guide de sécurité MCP et des revues par éditeur (dont GitHub), qui détaillent ce que chaque serveur peut concrètement atteindre.

**FAQ reprise dans l'article.** Comment obtenir une visibilité sur les connexions MCP des employés ? En lisant les fichiers de configuration des clients, seule source de vérité fiable, via un outillage d'endpoint capable de les parcourir, de résoudre ce que chaque entrée lance réellement et d'en centraliser le reporting. Existe-t-il une console d'admin pour MCP ? Non — le protocole a été conçu pour un client local servant un utilisateur local, sans plan de contrôle organisationnel, workflow d'approbation ni visibilité pour quiconque hormis l'utilisateur ; ajouter un serveur est un simple edit de texte, sans validation requise. Où sont stockées les configurations ? Dans des fichiers propres à chaque client, dans le répertoire personnel de l'utilisateur (détail des chemins ci-dessus), sans lien entre eux. Pourquoi une liste de noms ne suffit-elle pas ? Parce que le nom est choisi librement par l'auteur du fichier et ne contraint rien ; seule la commande résolue (binaire, paquet, version, identifiants) importe. À quelle fréquence cet inventaire change-t-il ? En continu et sans événement visible : installer un serveur MCP se résume à un edit de texte suivi d'un redémarrage du client, sans ticket, ni achat, ni connexion associée — d'où la nécessité d'une mesure permanente plutôt que d'un audit ponctuel.

L'article se conclut par un message promotionnel : l'inventaire existe déjà, dispersé dans des fichiers JSON sur chaque poste, mais personne ne le centralise ; l'outil « Workstation Lens » de Repello AI propose de lire ces fichiers à l'échelle du parc, de résoudre ce que chaque serveur lance réellement, de signaler les points d'entrée pointant vers un shell et de rapporter les versions effectivement en cours d'exécution.

## Pourquoi ça compte
Avec l'adoption rapide du MCP dans les outils de développement assistés par IA, cet article met en lumière un vrai trou de gouvernance : les équipes sécurité pilotent aujourd'hui des risques (shells exposés, identifiants en clair, dépendances non auditées) qu'elles ne savent même pas lister, ce qui en fait un signal d'alerte pertinent pour toute veille sur la sécurité des agents IA en entreprise.
