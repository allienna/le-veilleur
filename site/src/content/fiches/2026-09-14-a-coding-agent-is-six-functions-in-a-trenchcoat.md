---
title: "A coding agent is six functions in a trenchcoat"
date: 2026-09-14
url: "https://programmingdigest.net/links/23275/8e384055-4ef6-4411-8656-1644e3ae163f/email"
authors: ["Hadley Wickham"]
keywords: ["agents de codage", "LLM", "tool use", "sécurité", "harness", "R/ellmer"]
theme: "IA"
tone: "tutorial"
used_in: ["2026-09-14"]
---

## Résumé
L'article défend l'idée qu'un agent de codage n'est rien de plus qu'un harness (un système qui exécute des outils pour le compte d'un LLM) doté d'une poignée de fonctions spécifiques permettant d'explorer et de modifier un code comme le ferait un humain : lire, écrire, éditer, lister, chercher et exécuter des commandes shell. Pour le démontrer, l'auteur construit pas à pas, en R avec le package ellmer, un agent de codage minimal ne comportant au départ que trois outils (lecture, écriture, exécution de commande), avant d'ajouter progressivement le listing et la recherche de fichiers, puis un mécanisme d'édition ciblée plus efficace. Le texte insiste aussi longuement sur les risques de sécurité inhérents à ces outils (accès à des fichiers hors du projet, lecture de secrets) et sur les moyens simples de les limiter.

## Points clés
- Un agent de codage = un harness générique + des outils particuliers qui donnent à un LLM la capacité d'explorer et de modifier un dépôt de code.
- Six outils reviennent typiquement chez les agents de codage : read file, write file, edit file, list files, search, run command.
- Trois outils seulement (lire, écrire, exécuter une commande shell) suffisent à construire un agent fonctionnel minimal — démonstration en R via `chat_anthropic()` et `register_tool()` d'ellmer.
- L'outil shell (`run_command`) est le plus puissant (il permet tout : `ls`, `grep`, `git`, etc.) mais aussi le plus dangereux, car il est très difficile d'évaluer a priori si une commande est sûre.
- Sécuriser les outils de fichiers passe par une fonction `safe_path()` qui résout les chemins et vérifie qu'ils restent bien à l'intérieur du répertoire du projet, empêchant par exemple la lecture de `/etc` ou de fichiers de secrets comme `.Renviron`.
- Un outil d'édition ciblée (remplacement exact d'un extrait de texte plutôt que réécriture complète du fichier) rend l'agent plus rapide, moins coûteux et plus sûr, car une édition ratée échoue bruyamment plutôt que de corrompre silencieusement le fichier.

## Analyse approfondie

### Ce qui fait qu'un agent est un agent "de codage"
Depuis novembre 2025, des agents comme Claude Code, Cursor ou Codex ont profondément transformé la pratique du développement logiciel. L'auteur part d'une distinction déjà posée dans des billets précédents : un outil est une fonction, un harness est le système qui exécute ces fonctions pour le compte du LLM, et un agent est simplement un harness équipé d'outils de lecture et d'écriture. Ce qui fait qu'un agent est spécifiquement un agent *de codage*, ce sont les outils précis qu'on lui fournit — des outils qui permettent à un LLM d'explorer et de modifier une base de code de la même façon qu'un humain le ferait.

La plupart des agents de codage proposent une variation autour des six outils suivants :
- **Read file** : lire le contenu d'un fichier, ou une partie de celui-ci.
- **Write file** : créer un nouveau fichier avec un contenu neuf.
- **Edit file** : apporter une modification ciblée à un fichier existant, généralement en remplaçant un morceau de texte par un autre.
- **List files** : afficher les fichiers et répertoires à un chemin donné, pour que l'agent puisse s'orienter dans la structure du projet.
- **Search** : trouver les lignes correspondant à un motif dans toute la base de code, pour localiser rapidement le code pertinent.
- **Run command** : exécuter une commande shell arbitraire, ce qui permet à l'agent de faire à peu près tout le reste.

Un bon agent de codage embarque généralement aussi un long prompt système truffé de bonnes pratiques. Ces prompts ne sont pas open source, mais ils sont assez faciles à extraire, et plusieurs personnes s'y sont employées — un exercice instructif pour prendre la mesure de leur complexité.

### Construire un agent minimal
Sur les six outils cités, seuls trois sont réellement indispensables à un agent de codage basique. Pour le démontrer, l'auteur construit un tout petit agent de codage en R avec le package ellmer, en commençant volontairement au strict minimum : lecture de fichier, écriture de fichier et exécution de commande — puis en montant en complexité par la suite.

Les trois fonctions-outils sont écrites en R délibérément simple :
- `read_file(path)` lit un fichier ligne par ligne et renvoie son contenu sous forme de chaîne.
- `write_file(path, content)` écrit le contenu dans le fichier et confirme l'opération.
- `run_command(command)` exécute une commande système et renvoie ce qu'elle affiche.

Chaque fonction renvoie une chaîne de caractères qui est réinjectée au LLM comme résultat de l'appel d'outil.

On crée ensuite un chat et on enregistre les trois fonctions comme outils via `chat_anthropic()` puis `chat$register_tool(tool(...))`, en fournissant à chaque fois une description précise (elle indique au LLM quand et comment utiliser l'outil) ainsi qu'un prompt système basique invitant l'agent à lire un fichier avant de le modifier, à exécuter les tests pertinents après une modification, et à persévérer jusqu'à ce que la tâche soit terminée. Le modèle utilisé par défaut est `claude-sonnet-4-5-20250929`.

Et c'est tout : l'agent est complet avec ces trois outils. Le shell est la carte "sortie de prison gratuite", puisqu'avec une commande shell on peut tout faire : lister des répertoires (`ls`), chercher du code (`grep`), exécuter du R (`Rscript`), utiliser git. Techniquement, les outils dédiés de lecture et d'écriture ne sont même pas nécessaires puisque l'agent pourrait se contenter d'`echo` et `cat`, mais l'auteur choisit de lui laisser cet os à ronger. Le tool shell est en contrepartie plutôt dangereux, un point sur lequel l'article reviendra.

Avec cet agent minimal, on peut déjà lancer une tâche simple : trouver la fonction qui parse les dates et lui ajouter un test unitaire. En coulisses, le modèle utiliserait `run_command` avec `grep` pour localiser la fonction, puis `read_file` pour l'étudier ; il lirait ensuite les fichiers de tests existants, ajouterait le nouveau test via `write_file`, et terminerait en relançant la suite de tests via `run_command`. Ce n'est pas Claude Code, mais on est dans la même galaxie.

### Trouver des fichiers : lister et chercher
L'agent minimal peut déjà lister et chercher des fichiers via `run_command`, mais s'appuyer uniquement sur le shell pour cela a des inconvénients : les commandes shell varient d'une plateforme à l'autre (Windows n'a ni `ls` ni `grep`) et leur sortie est bruitée. Plus important encore, donner au modèle un accès shell généraliste constitue un vrai risque de sécurité, car il est très difficile de juger si une commande shell donnée est sûre ou dangereuse. Il est bien plus facile d'ajouter des garde-fous à des outils plus stricts.

L'auteur implémente donc deux outils dédiés :
- `list_files(path)` liste les fichiers d'un répertoire.
- `search_files(pattern, path)` parcourt récursivement les fichiers d'un répertoire et retourne les lignes correspondant à une expression régulière, sous la forme `chemin:ligne: texte`.

Ces deux fonctions sont ensuite enregistrées comme outils auprès du chat, avec des descriptions expliquant leur usage.

### Sécuriser les outils
Ces outils de listing et de recherche sont plus faciles à sécuriser qu'un shell généraliste, car leurs entrées sont plus simples. Mais ils ne sont pas sûrs par défaut : rien n'empêche le modèle de passer `path = ".."` ou un chemin absolu comme `/etc`, ce qui permettrait à l'outil de "chercher dans le projet" de lire tout le disque dur, y compris des mots de passe.

La parade proposée est une fonction `safe_path()` qui résout le chemin (ce qui élimine les `..` et suit les liens symboliques) et vérifie qu'il reste bien sous le répertoire de travail ; si ce n'est pas le cas, elle lève une erreur explicite ("Path is outside the project directory").

Il vaut aussi la peine de vérifier que ces outils ne peuvent pas lire le fichier `.Renviron`, où les développeurs R rangent traditionnellement leurs clés d'API et autres secrets. Bonne nouvelle : ce garde-fou est déjà présent gratuitement, car `list.files()` a par défaut `all.files = FALSE`, ce qui exclut les fichiers cachés — `.Renviron`, `.Rhistory` et le contenu de `.git/` sont donc déjà exclus de la recherche.

En combinant les deux, `search_files` est réécrite pour appeler `safe_path(path)` avant de lister les fichiers. Le même enrobage `safe_path()` doit aussi être appliqué à `read_file`, `write_file` et `list_files` : sinon, le modèle peut toujours sortir du projet en lisant ou écrivant directement un fichier situé ailleurs.

### Rendre l'agent efficace
La plus grande faiblesse de l'agent minimal est que la seule façon de modifier un fichier consiste à le réécrire intégralement avec `write_file`. Pour un fichier de 500 lignes dont on veut changer une seule ligne, cela oblige le modèle à reproduire fidèlement les 500 lignes — lent, coûteux, et difficile même pour les modèles actuels.

La solution est un outil d'édition ciblée, `edit_file(path, old, new)`, qui remplace un morceau de texte exact par un autre dans le fichier : il vérifie d'abord que le texte `old` apparaît bien dans le fichier (sinon il lève une erreur), puis effectue la substitution et réécrit le fichier.

Cet outil est utile pour deux raisons. D'abord, le modèle n'a besoin d'écrire que les quelques lignes qui changent, et non tout le fichier, ce qui le rend à la fois plus rapide et moins coûteux. Ensuite, il est beaucoup plus sûr : comme le texte `old` doit correspondre exactement, une édition ratée échoue bruyamment plutôt que de corrompre silencieusement le fichier. C'est exactement la logique des outils d'édition des agents de codage réels, aux nuances près (gestion des espaces, protection contre les correspondances multiples, détection d'une édition humaine concurrente).

L'auteur annonce qu'un prochain billet reviendra plus en détail sur la sécurité, et sur les approches permettant de rendre des outils généraux (comme l'exécution d'une commande shell) aussi sûrs que possible.

Dans les commentaires, un lecteur remercie l'auteur ("Hadley") d'avoir décortiqué le fonctionnement d'un agent de codage, précisant que cela l'aide à construire son propre harness pour des agents comme gemini-cli ou claude-code. Un autre commentaire signale un billet similaire publié par Amp ("How to build an agent", sur ampcode.com/notes).

## Pourquoi ça compte
Ce billet démystifie de façon concrète l'architecture des agents de codage (Claude Code, Cursor, Codex) en la ramenant à un noyau de quelques outils simples et à des questions de sécurité très identifiables (contrôle des chemins, dangers du shell) — une référence utile pour quiconque conçoit ou évalue des harnesses d'agents en veille technologique IA.
