---
title: "I Gave Grok Bot a Remote Computer"
date: 2026-10-09
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fupstash.com%2Fblog%2Fi-gave-grok-bot-a-remote-computer%3Futm_source=tldrdev/1/010001a11b39b529-c9e6d336-98d3-43b3-bfcc-b86c1bbe2532-000000/NnjAFH_Y4OJyxXcUn9onQxEyNfR6LCBAYZ4GtzRRzsY=452"
keywords: ["agents IA", "MCP", "Upstash", "Grok Bot", "automatisation", "pull request"]
theme: "IA"
tone: "opinion"
used_in: ["2026-10-09"]
---

## Résumé
L'auteur raconte comment il a relié l'assistant conversationnel Grok Bot à une machine distante (un « Box ») via le serveur MCP d'Upstash, lui donnant un shell, un système de fichiers persistant, git et des URLs de prévisualisation publiques. L'expérimentation part d'un simple jeu du serpent et monte jusqu'à des flux complets où Grok Bot lit un message Slack, crée un ticket Linear, clone un dépôt, code le correctif, lance les tests et ouvre une pull request accompagnée de captures d'écran — tout cela pilotable depuis un téléphone, à la voix. L'article se conclut par des conseils pratiques pour reproduire l'expérience et des liens vers la documentation technique.

## Points clés
- La configuration initiale tient en une phrase : connecter Grok Bot au serveur MCP d'Upstash et s'authentifier en OAuth suffit à donner à l'assistant un shell, un système de fichiers persistant, git, des URLs de preview publiques, des tâches planifiées (cron) et des snapshots.
- L'authentification GitHub passe par une GitHub App liée dans la console Upstash : l'agent ne détient donc jamais de token GitHub en propre.
- En combinant Slack, Linear, le Box et GitHub dans une même session, une seule instruction peut transformer un message Slack en ticket, puis en branche de code, puis en pull request, tests inclus.
- Un skill dédié (« upstash-box-remote-work ») automatise le cycle clone → build → preview → capture d'écran → PR, pour éviter de réécrire cette logique à chaque fois.
- Plusieurs agents peuvent partager le même Box : l'un implémente et ouvre la PR, un second relit le diff, exécute les tests et laisse des commentaires de revue, dans une boucle de type humain-à-humain.
- Toute la chaîne (Slack, Linear, Box, GitHub) devient pilotable à la voix depuis un téléphone, sans dépendre d'un ordinateur portable allumé en permanence.

## Analyse approfondie

### Objectif de l'expérience
L'auteur voulait savoir jusqu'où il pouvait aller en donnant un véritable ordinateur à Grok Bot. Plutôt que de se contenter d'une suggestion de correctif ou d'un plan de fonctionnalité, l'idée était de voir si l'assistant pouvait écrire le code, l'exécuter, et renvoyer quelque chose d'utilisable. Pour cela, il l'a connecté à un « Box » Upstash via le serveur MCP : le Box fournit la machine distante, et MCP permet à Grok Bot de la piloter. Après une configuration rapide, il suffisait de décrire une tâche à voix haute pour obtenir en retour une URL fonctionnelle ou une pull request, construite et exécutée sur le Box.

### Une configuration en une seule phrase
L'auteur a simplement demandé à Grok Bot d'ajouter le serveur MCP d'Upstash. Le serveur distant a été ajouté, il a suivi le flux d'authentification OAuth dans le navigateur, et les outils sont apparus immédiatement. C'est toute la configuration nécessaire.

### Ce que signifie concrètement « un ordinateur distant »
Une fois le MCP connecté, Grok Bot dispose de tout ce que propose Box — les mêmes briques que celles utilisées pour de véritables flux d'agents en arrière-plan :
- un conteneur cloud isolé (sandbox) : un vrai shell pour installer des paquets, lancer des tests, démarrer des serveurs ;
- un système de fichiers persistant : on peut fermer la conversation et revenir le lendemain, les fichiers sont toujours là ; un Box peut être mis en pause puis repris ;
- git couplé à GitHub : cloner des dépôts, committer, pousser, ouvrir des PR, l'authentification passant par la GitHub App liée dans la console Upstash — l'agent ne détient ainsi jamais de token GitHub, ce que l'auteur apprécie particulièrement ;
- des URLs de prévisualisation publiques : lancer quelque chose sur un port génère une URL accessible à tous ;
- des tâches planifiées (cron), capables d'exécuter une commande shell ou un prompt d'agent ;
- des snapshots, pour sauvegarder un état stable et y revenir ;
- un Chromium headless optionnel, permettant au Box d'ouvrir ses propres pages et de prendre des captures d'écran.
Son ordinateur portable n'a pas besoin de rester allumé, et l'assistant ne tourne pas dans son terminal : il travaille sur sa propre machine, et l'auteur vient simplement constater les résultats.

### Histoire du jeu du serpent
C'est la première chose testée après la configuration, et ce qui a convaincu l'auteur. Il a demandé à Grok Bot de construire un jeu du serpent et de lui donner l'URL — ce fut l'intégralité de la consigne. L'agent a créé un Box nommé « snake-demo-1007 », écrit le jeu, démarré un serveur sur le port 8080, et ouvert une prévisualisation publique. Le lien fonctionnait : le jeu tournait réellement.
Un jeu du serpent reste un exercice anodin, reconnaît l'auteur, mais ce qui compte est la boucle complète : il a demandé un résultat, pas du code. L'assistant disposait d'une machine pour le construire, d'un moyen de le servir, et d'un lien à renvoyer — sans qu'il ait besoin de copier un fichier et de lancer une commande localement. Comme le Box persiste, il est possible de revenir plus tard et de demander des améliorations (rendre le serpent plus rapide, ajouter un meilleur score) : l'agent reprend dans le même système de fichiers, avec le même serveur.

### Cloner un dépôt et laisser l'agent explorer
L'étape suivante consistait à passer à du vrai code. N'importe quel dépôt accessible via la GitHub App peut être cloné par Grok Bot dans le Box. Les commandes s'exécutent sur le Box, pas sur la machine de l'auteur : l'agent lit les résultats et fait un compte-rendu. En cas d'échec, il se trouve déjà dans le dépôt et peut tenter une correction.
C'est aussi un bon moyen de simplement comprendre une base de code : demander de cloner un dépôt, de trouver où est gérée la limitation de débit (rate limiting), et de l'expliquer. L'assistant peut utiliser grep, exécuter des commandes, et vérifier sa réponse contre le code réel plutôt que de deviner.

### Enchaîner les connexions : Slack → Linear → Box → PR
C'est là que l'expérience change de nature. Grok Bot n'est pas connecté qu'à Upstash : il peut aussi disposer de connexions Slack et Linear. En réunissant tout cela dans une même session, une seule instruction couvre tout le flux :
1. lire le message Slack ;
2. créer le ticket Linear ;
3. créer un Box (ou en réutiliser un) et cloner le dépôt ;
4. effectuer la modification et lancer les tests dans le Box ;
5. committer, pousser, et ouvrir la pull request via la GitHub App.
L'auteur reste celui qui relit et merge, mais toute la partie fastidieuse — transformer le message en ticket, le ticket en branche, la branche en PR — est déjà faite avant même qu'il ait fini de lire le fil de discussion.

### Des captures d'écran dans la PR grâce au skill « remote-work »
Les pull requests frontend sans captures d'écran sont pénibles à relire, et l'auteur ne veut pas avoir à détailler à chaque fois « clone, build, ouvre une preview, capture, upload, ouvre la PR ». C'est le rôle du skill upstash-box-remote-work, livré avec le plugin Upstash, qui indique à l'agent quand une tâche relève d'un Box et comment la mener de bout en bout : clonage, build, preview, capture d'écran, pull request. Il suffit de dire « utilise remote work » ou de demander une capture d'écran ou une URL de preview dans la PR, et le skill prend le relais. En coulisses, cela utilise toujours Box pour le travail et Blob pour les images, afin que les relecteurs obtiennent des captures en markdown directement dans le corps de la PR, sans rien avoir à récupérer localement.

### Des bots qui relisent d'autres bots
Un Box n'est pas lié à un seul assistant. Un autre agent peut se connecter au même Box, voir les mêmes fichiers et la même branche, et relire la pull request. Cela crée une boucle : Grok Bot implémente et ouvre la PR ; un second bot se connecte au même Box, lit le diff, lance les tests, et laisse des commentaires de revue ; Grok Bot reprend ces commentaires, réimplémente, et pousse à nouveau. Les deux agents dialoguent via la PR, à l'endroit même où les humains échangent habituellement. En relisant, l'auteur voit tout l'historique de ce que l'un a demandé et comment l'autre a répondu ; quand cela semble correct, il merge. Le Box est essentiel ici car les deux agents partagent le même état : personne n'a besoin de dire « ça marche chez moi », puisqu'il s'agit de la même machine.

### Le meilleur morceau : piloter tout cela depuis son téléphone
L'auteur garde ce point pour la fin car c'est son aspect favori. Il parle à Grok Bot à la voix ; comme c'est l'agent qui détient les connexions et que le Box vit dans le cloud, rien de tout cela ne nécessite son ordinateur portable — toute la chaîne est accessible depuis son téléphone. Le scénario qui l'a convaincu : on est à l'extérieur, une notification Slack signale un bug. Auparavant, cela voulait dire « je regarderai en rentrant ». Désormais, il suffit de sortir son téléphone et de dire : « Ouvre un ticket Linear pour ça, clone le dépôt sur mon Box, corrige-le, et ouvre une PR avec des captures d'écran. » Puis de remettre le téléphone en poche. En y revenant, on trouve un ticket, une branche, une PR et une URL de preview sur laquelle on peut cliquer pour vérifier le correctif. La voix fonctionne bien car les instructions restent courtes : on ne dicte pas du code, on exprime un résultat souhaité, et l'assistant dispose d'un véritable ordinateur pour l'accomplir.

### Conseils avant de se lancer
- Commencer par quelque chose qui renvoie une URL (un jeu du serpent, un petit tableau de bord, peu importe) : voir le lien de preview est ce qui déclenche la prise de conscience de l'intérêt du dispositif.
- Lier la GitHub App dans la console en premier lieu : ensuite, cloner et ouvrir des PR fonctionne directement, sans jamais remettre de token à l'agent.
- Nommer ses Box de façon reconnaissable (par exemple « snake-demo-1007 ») : la persistance n'a d'intérêt que si l'on se souvient de quel Box correspond à quoi.
- Installer les skills Upstash : le skill upstash-box-remote-work couvre déjà le cycle clone → preview → capture → PR, pas besoin de le réinventer.
- Utiliser les tâches planifiées pour des vérifications récurrentes : une tâche cron qui exécute un prompt d'agent chaque matin est un moyen simple d'obtenir un rapport quotidien sans y penser.

### Pour essayer soi-même
Il suffit de connecter le serveur MCP d'Upstash (`https://mcp.upstash.com/mcp`), de s'authentifier en OAuth, puis de demander à son assistant de construire quelque chose et d'en envoyer l'URL. L'article renvoie vers la documentation MCP, le guide de démarrage rapide de Box, et la procédure de création d'un Box avec liaison GitHub dans la console Upstash. L'auteur invite enfin les lecteurs à venir montrer sur Discord ce qu'ils auront construit — ou le spectacle de deux bots qui se chamaillent dans une PR.

## Pourquoi ça compte
Cet article illustre concrètement la bascule des assistants IA du simple « conseil de code » vers des agents dotés d'un véritable environnement d'exécution persistant (shell, filesystem, git, preview, cron) pilotable à la voix et depuis un mobile. Pour une veille tech, c'est un signal fort sur la maturation des architectures MCP et des flux agentiques multi-outils (Slack, Linear, GitHub) allant jusqu'à la revue de code entre agents, un pattern appelé à se généraliser dans les workflows de développement assistés par IA.
