---
title: "Escaping the OpenAI Codex sandbox, twice — Accomplish Blog"
date: 2026-09-18
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Faccomplish.ai%2Fblog%2Fescaping-the-openai-codex-sandbox-twice%2F%3Futm_source=tldrdev/1/010001a0af146874-dc9a6ee3-a5dc-4222-8676-ccbdd199480a-000000/SdlkrtC-N_9dNr4A4eNbsH71tnZ5yCInxizITH6zuXg=452"
authors: ["Accomplish"]
keywords: ["sandbox", "OpenAI Codex", "vulnérabilité", "isolation VM", "agents IA", "exécution de code"]
theme: "Sécurité"
tone: "research"
used_in: ["2026-09-18"]
---

## Résumé

Accomplish, éditeur d'un outil qui isole les agents IA dans des machines virtuelles, a découvert et signalé à OpenAI, le 12 août 2026, deux méthodes distinctes pour s'échapper du bac à sable (sandbox) de Codex ; les deux failles ont été corrigées en moins de huit jours. La première, baptisée « Overpatch », détourne l'outil `apply_patch` de la CLI Codex pour obtenir un accès en écriture à l'ensemble du disque en mode `workspace-write`, sans la moindre invite d'approbation. La seconde, « Heapjack », exploite le serveur MCP `node_repl` installé par défaut avec Codex Desktop : le jeton secret censé séparer le code de confiance du code non fiable réside dans une mémoire partagée (le tas V8), ce qui permet une exécution de commande hors sandbox même dans le mode le plus strict, `read-only`. L'article conclut que les deux bugs partagent le même défaut structurel — le mécanisme de contrôle s'exécute à l'intérieur du périmètre qu'il est censé protéger — ce qui motive l'architecture d'Accomplish, qui fait tourner l'agent entier dans une VM externe.

## Points clés

- Deux failles de sandbox trouvées dans OpenAI Codex, signalées le 12 août 2026 et corrigées par OpenAI en moins de huit jours.
- **Overpatch** : `apply_patch` accorde par erreur un accès en écriture au dossier *parent* de chaque chemin mentionné dans un patch ; en visant `/tmp`, on obtient un accès en écriture à la racine du système de fichiers, ce qui permet d'écrire un `.zshrc` malveillant exécuté dès l'ouverture du terminal suivant.
- **Heapjack** : le serveur `node_repl` fait cohabiter code de confiance et code non fiable dans le même processus Node / isolat V8 ; le jeton secret qui les distingue peut être extrait d'un instantané mémoire (`v8.getHeapSnapshot()`), ce qui permet de forger des requêtes vers le processus Rust parent, non sandboxé lui.
- Heapjack fonctionne même en mode `read-only`, le plus restrictif, et sans aucune invite d'approbation à l'écran — le simple fait d'ouvrir un dépôt cloné suffit à donner à son auteur une exécution de commande hors sandbox.
- Le jeton forgé permet notamment de lancer des applications via la commande système `open`, de se connecter à des sockets Unix arbitraires (dont potentiellement un démon Docker), et de modifier le fichier de configuration global de Codex.
- Cause racine commune aux deux bugs : le composant chargé d'appliquer les règles de sécurité tourne à l'intérieur même du périmètre qu'il doit surveiller, ce qui a conduit Accomplish à concevoir son propre outil autour d'une VM complète, avec des identifiants réels jamais exposés à l'agent et un proxy réseau côté hôte hors de portée de ce dernier.

## Analyse approfondie

**Overpatch — contourner le mode `workspace-write`**

En mode `workspace-write`, l'agent Codex n'est censé pouvoir écrire qu'à l'intérieur du dossier de travail : toute tentative d'écrire dans `$HOME` via une commande shell classique est refusée. Les chercheurs d'Accomplish ont néanmoins réussi à faire écrire l'agent en dehors de ce périmètre, en passant par l'outil `apply_patch` fourni par le harnais Codex pour l'édition de fichiers.

Le bug tient au fait que cet outil accorde un droit d'écriture non pas sur le fichier ciblé, mais sur le *dossier parent* de chaque chemin mentionné dans le patch. En incluant `/tmp` dans la liste des chemins visés, le patch obtient de fait un droit d'écriture sur la racine du système de fichiers (`/`).

Le patch malveillant contient deux modifications : la première ajoute une ligne au fichier `.zshrc` en passant par un lien symbolique pointant vers `$HOME` ; la seconde cible `/tmp` sans y apporter de changement réel — cette opération échoue nécessairement, puisqu'on ne peut pas remplacer un dossier par un fichier, mais elle sert uniquement à élargir artificiellement le périmètre d'écriture autorisé. Sans cette seconde ligne, la modification du `.zshrc` est refusée. Une fois ce fichier modifié, il s'exécute sans aucune restriction sandbox au prochain lancement d'un terminal.

**Heapjack — un secret partagé dans la même mémoire**

À l'installation, Codex Desktop inscrit automatiquement un bloc `[mcp_servers.node_repl]` dans le fichier de configuration global `~/.codex/config.toml`, sans option pour refuser cet ajout ni pour le désactiver ensuite. C'est ce qui explique que même la CLI Codex standard bénéficie (ou souffre) de cet outil.

Ce serveur `node_repl` est un programme natif écrit en Rust, non sandboxé : il peut ouvrir des applications, se connecter à des sockets Unix et modifier le fichier de configuration. Il démarre un processus Node à l'intérieur du sandbox Codex, de sorte que tout le code JavaScript exécuté par l'agent reste, en apparence, confiné. Mais ce processus Node unique héberge deux contextes V8 (`vm`) distincts : l'un, de confiance, exécute le code d'OpenAI et reçoit un jeton secret ; l'autre, non fiable, exécute le code de l'agent et n'y a pas accès. Ce jeton, généré aléatoirement à chaque exécution, est la seule preuve que présente le contexte de confiance pour s'authentifier.

Or, un seul processus Node signifie un seul isolat V8, donc un seul tas mémoire partagé par les deux contextes — et le jeton n'est qu'une chaîne de caractères stockée dans ce tas. Le code non fiable peut donc capturer un instantané complet du tas (`v8.getHeapSnapshot()`) et tester systématiquement toutes les chaînes ayant la forme d'un UUID : un mauvais jeton renvoie une erreur « non autorisé », tandis qu'un bon jeton associé à un argument invalide renvoie une véritable erreur de validation — ce qui permet de confirmer par élimination la valeur correcte.

Le processus Node sandboxé communique avec le processus Rust parent en écrivant des requêtes JSON, ligne par ligne, sur sa sortie standard (fd 1) — un canal partagé par les deux contextes. Le code non fiable peut donc y injecter directement ses propres requêtes, dans le même format. Le processus parent les lit, vérifie le jeton, et exécute l'action demandée sans se soucier de savoir quel contexte l'a réellement émise : toute la frontière de confiance repose sur la possession de cette seule chaîne de caractères.

Ce processus parent peut notamment invoquer la commande système `open`, ce qui permet à `launchd` de démarrer une application entièrement hors du contrôle et de l'arborescence de processus de Codex — c'est ce qu'a démontré la preuve de concept des chercheurs. Le même jeton permet aussi de se connecter à n'importe quel socket Unix, dont, par exemple, celui d'un démon Docker, et donne accès à un outil de modification du fichier de configuration global `~/.codex/config.toml`.

Tout ceci fonctionne alors même que l'agent tourne en mode `read-only`, le réglage de sandbox le plus strict, où il n'est en principe autorisé à rien écrire — et sans qu'aucune invite d'approbation ne s'affiche à aucun moment. Concrètement : il suffit d'ouvrir un dépôt cloné dans Codex en mode `read-only` et de lui poser une question pour que la personne ayant écrit ce dépôt obtienne une exécution de commande non sandboxée, silencieuse, équivalente à ce qu'elle obtiendrait en désactivant purement et simplement le sandbox.

**Comment Accomplish a été conçu**

Les deux failles partagent une même structure : le composant chargé de faire respecter les règles de sécurité se trouve lui-même à l'intérieur du périmètre qu'il est censé surveiller. `apply_patch` déterminait ses propres autorisations à partir d'une entrée qu'on lui fournissait ; `node_repl` conservait le secret séparant code de confiance et code non fiable dans la mémoire même de ce code non fiable. Dans les deux cas, le sandbox recevait, de l'intérieur, l'instruction de laisser passer quelque chose qu'il aurait dû bloquer.

C'est cette observation qui a guidé la conception d'Accomplish : l'ensemble de l'agent — le modèle, le shell, git, et tous les processus que ceux-ci démarrent — s'exécute à l'intérieur d'une machine virtuelle complète. Les identifiants réels de l'utilisateur n'entrent jamais dans cette VM : l'agent ne manipule que des identifiants de substitution (placeholders), et tout le trafic sortant transite par un proxy situé côté hôte, que l'agent ne peut ni atteindre ni reconfigurer. Tout ce qui s'exécute dans la VM invitée est considéré comme non fiable, y compris les processus tournant en `root`, puisqu'aucun composant décidant de ce qui est autorisé ne s'exécute à l'intérieur de cet environnement.

Rejouée sous Accomplish, la faille Overpatch permettrait bien au patch d'écrire où il veut, mais uniquement à l'intérieur de la VM ; de même, Heapjack pourrait bien forger une requête et lancer une application, mais toujours confinée à la VM. Dans les deux cas, aucune des deux attaques n'atteint la machine réelle de l'utilisateur.

## Pourquoi ça compte

Ce cas illustre un défaut structurel récurrent dans les harnais d'agents IA actuels — le contrôle de sécurité s'exécute dans le même espace de confiance que le code qu'il doit surveiller — et montre qu'une isolation par VM externe, plutôt qu'un sandbox logique interne, constitue une réponse plus robuste ; un point de vigilance direct pour toute équipe déployant des agents IA autonomes (Codex ou équivalents) sur du code non fiable.
