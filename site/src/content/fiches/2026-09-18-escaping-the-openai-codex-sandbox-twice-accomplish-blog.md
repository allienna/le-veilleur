---
title: "Escaping the OpenAI Codex sandbox, twice — Accomplish Blog"
date: 2026-09-18
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Faccomplish.ai%2Fblog%2Fescaping-the-openai-codex-sandbox-twice%2F%3Futm_source=tldrdev/1/010001a0af146874-dc9a6ee3-a5dc-4222-8676-ccbdd199480a-000000/SdlkrtC-N_9dNr4A4eNbsH71tnZ5yCInxizITH6zuXg=452"
keywords: ["sandbox escape", "OpenAI Codex", "agents IA", "vulnérabilité", "isolation VM", "sécurité des agents"]
theme: "Sécurité"
tone: "research"
used_in: ["2026-09-18"]
---

## Résumé
L'équipe d'Accomplish a découvert deux failles distinctes permettant d'échapper au sandbox d'OpenAI Codex, signalées à OpenAI le 12 août 2026 et corrigées en moins de huit jours. La première, baptisée « Overpatch », exploite l'outil `apply_patch` du Codex CLI pour obtenir un accès en écriture sur tout le disque en mode agent normal, sans aucune invite d'approbation. La seconde, « Heapjack », tire parti d'un jeton secret partagé en mémoire dans l'outil `node_repl` de Codex Desktop pour obtenir une exécution de commande hors sandbox, même en mode `read-only`, le plus restrictif. Ces deux découvertes illustrent pourquoi Accomplish a choisi de faire tourner ses agents entièrement à l'intérieur d'une machine virtuelle isolée plutôt que de faire confiance à un sandbox interne au processus.

## Points clés
- **Overpatch** : une ligne anodine dans un patch fait que `apply_patch` accorde un accès en écriture au dossier parent de chaque chemin cité — nommer `/tmp` suffit à obtenir un accès en écriture à `/`, sans approbation requise.
- Cette faille permet d'écrire dans `.zshrc` via un lien symbolique, ce qui donne une exécution de code hors sandbox dès l'ouverture du prochain terminal.
- **Heapjack** exploite le fait qu'un jeton secret censé distinguer code de confiance et code non fiable est stocké dans le même tas mémoire (heap) V8, accessible par un simple `v8.getHeapSnapshot()`.
- Une fois le jeton récupéré, le code non fiable peut forger des requêtes sur le pipe stdout partagé et obtenir une exécution de commande arbitraire, même en mode sandbox le plus strict (`read-only`).
- Le point commun des deux failles : le mécanisme chargé de faire respecter les règles de sécurité se trouvait à l'intérieur même de l'environnement qu'il était censé contraindre.
- Ce constat a motivé l'architecture d'Accomplish, qui exécute l'agent entier (modèle, bash, git, sous-processus) dans une VM isolée, avec identifiants réels tenus hors de la machine invitée et trafic sortant filtré par un proxy côté hôte.

## Analyse approfondie
Nous avons trouvé deux moyens de sortir du sandbox d'OpenAI Codex et avons signalé les deux à OpenAI le 12 août 2026. Les deux ont été corrigés en moins de huit jours.

Le premier se trouve dans le Codex CLI open source. Une ligne supplémentaire dans un patch donne à l'outil de patch un accès en écriture à l'ensemble du disque, en mode agent normal, sans invite d'approbation. Nous l'appelons **Overpatch**.

Le second se trouve dans l'outil JavaScript que Codex Desktop installe. Le sandbox fonctionnait, mais le secret qui distinguait le code de confiance du code non fiable se trouvait en mémoire, accessible en lecture par le code non fiable. Nous l'appelons **Heapjack**. Il s'exécute en mode `read-only`, où l'agent est censé ne rien pouvoir écrire, et se termine par une exécution de commande hors sandbox.

### Overpatch

En mode `workspace-write`, l'agent n'est autorisé à écrire qu'à l'intérieur du dossier de travail (workspace). Une commande shell qui tente d'accéder à `$HOME` est refusée.

Nous avons quand même réussi à faire écrire `apply_patch` à cet endroit.

`apply_patch` est un outil que le harnais Codex donne à l'agent pour modifier des fichiers. Le bug est qu'il accorde un accès en écriture au dossier parent de chaque chemin figurant dans le patch. Nommez `/tmp` et il accorde un accès en écriture à `/`.

Le patch qui déclenche l'écriture comporte deux modifications. L'une ajoute une ligne à `.zshrc` via un lien symbolique pointant vers `$HOME`. L'autre nomme `/tmp` et ne fait rien. Cette modification échoue, car on ne peut pas écrire un fichier par-dessus un dossier. Elle ne figure dans le patch que pour élargir l'autorisation accordée. Retirez cette ligne et l'écriture est refusée.

Écrivez dans `.zshrc` et le prochain terminal que vous ouvrirez l'exécutera hors sandbox.

### Heapjack

Codex Desktop écrit un bloc `[mcp_servers.node_repl]` dans le fichier global `~/.codex/config.toml` lors de l'installation. Aucune option d'adhésion (opt-in), aucun paramètre pour le désactiver. C'est pourquoi le simple CLI `codex` récupère lui aussi cet outil.

L'outil est un programme natif en Rust, non sandboxé. Il ouvre des applications, se connecte à des sockets unix, écrit le fichier de configuration. Il démarre un processus Node à travers le sandbox Codex, de sorte que tout le JavaScript s'exécute en sandbox. À l'intérieur de cet unique processus Node se trouvent deux contextes `vm` V8. Le contexte de confiance contient le propre code d'OpenAI et reçoit le jeton secret. Le contexte non fiable exécute le code de l'agent et ne le reçoit pas.

Le contexte de confiance prouve qu'il est bien le contexte de confiance grâce à un jeton aléatoire, généré à nouveau à chaque exécution.

Un seul processus Node, un seul isolat V8, un seul tas (heap) partagé par les deux contextes. Le jeton est une chaîne de caractères dans ce tas.

Le code non fiable prend un instantané (snapshot) du tas (`v8.getHeapSnapshot()`) et teste toutes les chaînes ayant la forme d'un UUID. Un jeton erroné renvoie *not authorized*. Un jeton correct assorti d'un argument invalide renvoie une véritable erreur de validation.

Le processus Node sandboxé envoie ses requêtes au parent Rust sous forme de lignes JSON écrites sur le descripteur de fichier 1, sa sortie standard (stdout). Un seul tube (pipe), partagé par les deux contextes. Le code non fiable écrit sa propre requête sur ce tube, dans le même format. Le parent natif la lit, vérifie le jeton, et exécute la tâche demandée. Connaître cette seule chaîne de caractères constitue toute la frontière de sécurité.

Le parent exécute la commande système `open`, si bien que launchd démarre l'application hors sandbox, en dehors de l'arborescence de processus de Codex. C'est ce qu'a fait notre preuve de concept (proof of concept). Le même jeton permet de se connecter à n'importe quel socket unix, le socket du démon Docker étant le candidat évident. Il expose également un outil permettant de modifier le fichier global `~/.codex/config.toml`.

Tout cela s'est déroulé en mode `read-only`, le mode de sandbox le plus strict, où l'agent est censé ne rien pouvoir écrire. Codex n'a jamais demandé la moindre approbation.

Ouvrez un dépôt cloné dans Codex en mode sandbox `read-only`, posez-lui une question, et celui qui a écrit ce dépôt obtient une exécution de commande hors sandbox, sans invite et sans rien à l'écran. Le même accès que s'il avait désactivé le sandbox et exécuté lui-même son script.

### Comment nous avons construit Accomplish

Les deux bugs ont la même forme. L'élément chargé de faire respecter les règles se trouvait à l'intérieur de l'élément censé être contraint par elles. `apply_patch` calculait ses propres permissions à partir des entrées qu'on lui fournissait. `node_repl` conservait le secret séparant le code de confiance du code non fiable dans la même mémoire que ce code non fiable. Dans les deux cas, c'est depuis l'intérieur même du sandbox qu'on lui a fait laisser passer quelque chose.

C'est pourquoi Accomplish exécute l'intégralité de l'agent à l'intérieur d'une VM. Le modèle, bash, git, et tous les processus que chacun d'eux démarre. Les identifiants réels n'entrent jamais dans la machine invitée (guest) ; l'agent travaille avec des valeurs de substitution (placeholders), et le trafic sortant passe par un proxy sur l'hôte que l'agent ne peut ni atteindre ni reconfigurer. Nous considérons tout ce qui se trouve dans la machine invitée comme non fiable, y compris root, parce que rien de ce qui décide ce qui est autorisé ne s'y exécute avec lui.

Exécutez Overpatch sous Accomplish et le patch écrit où bon lui semble, à l'intérieur de la VM. Exécutez Heapjack et la requête forgée lance une application, à l'intérieur de la VM. Aucun des deux n'atteint votre ordinateur portable.

## Pourquoi ça compte
Ces deux failles démontrent que les mécanismes de sandboxing internes aux agents IA de type Codex peuvent être contournés dès lors que la logique d'autorisation partage le même espace mémoire ou processus que le code non fiable qu'elle est censée contenir — un signal d'alarme pour toute équipe déployant des agents de codage autonomes sur du code non vérifié.
