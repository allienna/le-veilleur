---
title: "Escaping the OpenAI Codex sandbox, twice — Accomplish Blog"
date: 2026-09-18
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Faccomplish.ai%2Fblog%2Fescaping-the-openai-codex-sandbox-twice%2F%3Futm_source=tldrdev/1/010001a0af146874-dc9a6ee3-a5dc-4222-8676-ccbdd199480a-000000/SdlkrtC-N_9dNr4A4eNbsH71tnZ5yCInxizITH6zuXg=452"
keywords: ["sandbox", "Codex", "OpenAI", "sécurité des agents IA", "vulnérabilité", "isolation"]
theme: "Sécurité"
tone: "research"
used_in: ["2026-09-18"]
---

## Résumé
L'équipe d'Accomplish a découvert et signalé à OpenAI, le 12 août 2026, deux failles permettant d'échapper au bac à sable (sandbox) de Codex, corrigées en moins de huit jours. La première, baptisée « Overpatch », exploite l'outil `apply_patch` du Codex CLI pour obtenir un accès en écriture à tout le disque en mode agent normal, sans validation. La seconde, « Heapjack », exploite un tas mémoire V8 partagé dans l'outil `node_repl` installé par Codex Desktop pour extraire un jeton secret et forger des requêtes non autorisées, aboutissant à une exécution de commande hors bac à sable même en mode `read-only`. L'article se conclut en expliquant comment ces découvertes ont motivé l'architecture de leur propre produit, Accomplish, qui isole les agents dans des machines virtuelles complètes.

## Points clés
- **Overpatch** : une ligne anodine dans un patch (`apply_patch`) élargit l'autorisation d'écriture au dossier parent de n'importe quel chemin cité, permettant d'atteindre `/` en nommant `/tmp`.
- Cette faille permet d'écrire dans `.zshrc` via un lien symbolique, assurant une exécution de code hors bac à sable au prochain terminal ouvert.
- **Heapjack** : le jeton secret séparant le code de confiance (OpenAI) du code non fiable (l'agent) réside dans le même tas V8, accessible via `v8.getHeapSnapshot()`.
- Une fois le jeton extrait, du code non fiable peut forger des requêtes sur le pipe stdout partagé, obtenant une exécution de commande non sandboxée même en mode `read-only`, le niveau de sécurité le plus strict.
- Le point commun aux deux failles : le mécanisme chargé d'appliquer les règles de sécurité s'exécutait à l'intérieur même de l'environnement qu'il était censé contraindre.
- Ce constat a conduit Accomplish à choisir une isolation par VM complète, avec identifiants réels jamais exposés au invité et trafic sortant filtré par un proxy côté hôte.

## Analyse approfondie
Nous avons trouvé deux moyens de sortir du bac à sable d'OpenAI Codex, et nous avons signalé les deux à OpenAI le 12 août 2026. Les deux ont été corrigées en moins de huit jours.

La première se trouve dans le Codex CLI open source. Une ligne supplémentaire dans un patch donne à l'outil de patch un accès en écriture à tout le disque, en mode agent normal, sans invite d'approbation. Nous l'appelons **Overpatch**.

La seconde se trouve dans l'outil JavaScript installé par Codex Desktop. Le bac à sable fonctionnait, mais le secret qui distinguait le code de confiance du code non fiable se trouvait dans une mémoire que le code non fiable pouvait lire. Nous l'appelons **Heapjack**. Elle s'exécute en mode `read-only`, où l'agent est censé ne rien pouvoir écrire, et elle se termine par une exécution de commande hors du bac à sable.

### Overpatch

En mode `workspace-write`, l'agent n'est autorisé à écrire qu'à l'intérieur du dossier de l'espace de travail (workspace). Une commande shell qui tente d'accéder à `$HOME` est refusée.

Nous avons réussi à faire écrire `apply_patch` là-bas malgré tout.

`apply_patch` est un outil que le harnais Codex donne à l'agent pour éditer des fichiers. Le bug est qu'il accorde un accès en écriture au dossier parent de chaque chemin présent dans le patch. Nommez `/tmp` et il accorde un accès en écriture à `/`.

Le patch qui réalise l'écriture comporte deux modifications. L'une ajoute une ligne à `.zshrc` via un lien symbolique pointant vers `$HOME`. L'autre nomme `/tmp` et ne fait rien. Cette modification échoue, car on ne peut pas écrire un fichier par-dessus un dossier. Elle ne figure dans le patch que pour élargir l'autorisation accordée. Retirez cette ligne et l'écriture est refusée.

Écrivez dans `.zshrc`, et le prochain terminal que vous ouvrirez l'exécutera hors du bac à sable.

### Heapjack

Codex Desktop écrit un bloc `[mcp_servers.node_repl]` dans le fichier global `~/.codex/config.toml` lors de l'installation. Aucune option d'adhésion (opt-in), aucun paramètre pour le désactiver. C'est pourquoi le simple CLI `codex` hérite aussi de cet outil.

L'outil est un programme natif écrit en Rust, hors bac à sable. Il ouvre des applications, se connecte à des sockets Unix, écrit le fichier de configuration. Il démarre un processus Node via le bac à sable de Codex, de sorte que tout le JavaScript s'exécute dans le bac à sable. À l'intérieur de cet unique processus Node se trouvent deux contextes `vm` de V8. Le contexte de confiance contient le propre code d'OpenAI et reçoit le jeton secret. Le contexte non fiable exécute le code de l'agent et ne le reçoit pas.

Le contexte de confiance prouve qu'il est bien le contexte de confiance grâce à un jeton aléatoire, généré à nouveau à chaque exécution.

Un seul processus Node, un seul isolat V8, un seul tas (heap) partagé par les deux contextes. Le jeton est une chaîne de caractères dans ce tas.

Le code non fiable prend un instantané du tas (`v8.getHeapSnapshot()`) et essaie toutes les chaînes ayant la forme d'un UUID. Un mauvais jeton renvoie *not authorized*. Un bon jeton accompagné d'un argument invalide renvoie une véritable erreur de validation.

Le processus Node en bac à sable envoie ses requêtes à ce parent Rust sous forme de lignes JSON écrites sur le descripteur de fichier 1, sa sortie standard (stdout). Un seul tube (pipe), partagé par les deux contextes. Le code non fiable écrit sa propre requête sur ce tube, dans le même format. Le processus parent natif la lit, vérifie le jeton, et effectue le travail demandé. Connaître cette seule chaîne de caractères constitue toute la frontière de sécurité.

Le parent exécute la commande système `open`, de sorte que launchd démarre l'application hors du bac à sable, en dehors de l'arborescence de processus de Codex. C'est ce qu'a fait notre preuve de concept. Le même jeton permet de se connecter à n'importe quel socket Unix, le socket du démon Docker étant le candidat le plus évident. Il expose également un outil permettant d'éditer le fichier global `~/.codex/config.toml`.

Tout cela s'est déroulé en mode `read-only`, le mode de bac à sable le plus strict, où l'agent est censé ne rien pouvoir écrire. Codex n'a jamais demandé d'approbation.

Ouvrez un dépôt cloné dans Codex en mode bac à sable `read-only`, posez-lui une question, et l'auteur de ce dépôt obtient une exécution de commande hors du bac à sable, sans invite et sans rien afficher à l'écran. Exactement le même accès que s'il avait désactivé le bac à sable et exécuté lui-même son script.

### Comment nous avons construit Accomplish

Les deux failles ont la même forme. Ce qui assurait l'application des règles se trouvait à l'intérieur même de ce qui était censé être contraint. `apply_patch` calculait ses propres permissions à partir des données qu'on lui fournissait. `node_repl` conservait le secret séparant le code de confiance du code non fiable dans la même mémoire que ce code non fiable. Dans les deux cas, on a dit au bac à sable, depuis l'intérieur, de laisser passer quelque chose.

C'est pourquoi Accomplish exécute l'agent entier à l'intérieur d'une VM : le modèle, bash, git, et tout processus que l'un d'eux démarre. Les véritables identifiants (credentials) n'entrent jamais dans la machine invitée (guest) ; l'agent travaille avec des placeholders, et le trafic sortant passe par un proxy sur l'hôte, que l'agent ne peut ni atteindre ni reconfigurer. Nous traitons tout ce qui se trouve dans la machine invitée comme non fiable, y compris root, car rien de ce qui décide ce qui est autorisé ne s'exécute à l'intérieur avec lui.

Exécutez Overpatch sous Accomplish, et le patch écrit où bon lui semble, mais à l'intérieur de la VM. Exécutez Heapjack, et la requête forgée lance une application, mais à l'intérieur de la VM. Aucune des deux n'atteint votre ordinateur portable.

## Pourquoi ça compte
Ce cas illustre un problème structurel des sandbox d'agents IA : quand le mécanisme d'application des règles vit dans le même processus ou la même mémoire que le code non fiable qu'il doit contenir, la frontière de sécurité devient contournable de l'intérieur. À mesure que les agents de codage autonomes se généralisent, cette analyse plaide pour une isolation stricte au niveau machine (VM) plutôt que des sandbox applicatifs, un point de vigilance clé pour toute équipe déployant des agents IA sur du code non fié.
