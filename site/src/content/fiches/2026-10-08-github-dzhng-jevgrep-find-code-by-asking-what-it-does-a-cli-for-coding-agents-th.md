---
title: "GitHub - dzhng/jevgrep: Find code by asking what it does. A CLI for coding agents that uses Jev to discover relevant files and source context."
date: 2026-10-08
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fgithub.com%2Fdzhng%2Fjevgrep%3Futm_source=tldrdev/1/010001a116141a79-0c77fa27-f107-43c8-8993-97c7650472cb-000000/981MVixC2mdT19Kud6n0y3wBq70q1s6nrCQcZFsCjJE=452"
authors: ["dzhng"]
keywords: ["agents de codage", "recherche de code", "CLI", "SWE-bench", "réduction de coûts", "open source"]
theme: "Tech"
tone: "news"
used_in: ["2026-10-08"]
---

## Résumé
Jevgrep (`jg`) est un outil CLI qui permet aux agents de codage de localiser du code pertinent en posant une question en langage naturel sur un dépôt, plutôt qu'en passant par une recherche par mots-clés classique. Il s'appuie sur un moteur nommé Jev pour juger la pertinence des dossiers, fichiers et déclarations, puis renvoie fichiers pertinents, pistes de lecture et extraits de code vérifiés. Sur un benchmark de dix tâches SWE-bench, Jevgrep a résolu les mêmes 8 tâches sur 10 qu'une baseline sans l'outil, mais à un coût réduit d'environ 25 à 30 % selon la version testée. L'outil s'installe via npm et peut être ajouté comme "skill" à des agents comme Claude Code, Codex ou OpenCode.

## Points clés
- `jg` permet d'interroger un dépôt en langage naturel pour obtenir fichiers pertinents, pistes de lecture et extraits de code source.
- Il s'appuie sur Jev pour évaluer la pertinence à travers dossiers, fichiers et déclarations, avec analyse native des déclarations pour Python, TypeScript/JavaScript, Go et Rust.
- Sur 10 tâches SWE-bench, Jevgrep égale la baseline (8/10 tâches résolues) tout en réduisant le coût de ~28,6 % (coût Sol seul) à ~25,8 % (coût total incluant Jev, mesuré en v0.4.3).
- La version 0.5.0 réduit le coût natif de Jev d'environ 59 %, mais augmente légèrement (2-3 %) le coût combiné Sol+Jev — un compromis jugé acceptable par les auteurs.
- Installation simple via npm, avec un installeur de skill qui détecte automatiquement les agents de codage compatibles et propose une installation globale ou non interactive.
- Le filtrage par défaut exclut les fichiers cachés, binaires, de dépendance/build et d'identifiants évidents, sans garantir une suppression totale des informations sensibles.

## Analyse approfondie
**Même intelligence. Coût ~30 % plus bas.**

Trouvez du code en demandant ce qu'il fait. Dans notre comparaison SWE-bench sur dix tâches, Jevgrep a réussi les mêmes 8 tâches sur 10 que la baseline, à moindre coût.

Les agents de codage passent une partie de chaque tâche inconnue à chercher les bons fichiers. Jevgrep leur donne un point de départ : posez une question sur le dépôt, et `jg` renvoie les fichiers pertinents, des pistes de lecture, et des extraits de code source verbatim dans une seule réponse stdout. Il utilise Jev pour juger la pertinence à travers les dossiers, les fichiers et les déclarations. Votre agent de codage implémente et teste ensuite le changement.

```
npm install -g @dzhng/jevgrep
jg auth
jg skill
jg "How are telemetry events recorded and sent?" ./my-project
```

Nécessite **Node.js 22+**, **macOS, Linux, ou Windows**, et une clé pour **Vercel AI Gateway, TypeSafe, OpenRouter, OpenCode Zen, ou un endpoint compatible TypeSafe personnalisé**. Aucune installation séparée de Python, Bun, ou ripgrep n'est nécessaire pour utiliser `jg`.

La sélection du fournisseur nécessite la version **0.3.0 ou plus récente**. Mettez à jour une installation plus ancienne avec `npm install --global @dzhng/jevgrep@latest`.

Installer seulement le CLI n'apprend pas à votre agent de codage à l'utiliser. **Installez aussi le skill**, depuis le projet où votre agent travaille :

`jg skill`
L'installeur détecte vos agents de codage (Claude Code, Codex, OpenCode et autres) et demande où installer. Ajoutez `--global` pour une installation à l'échelle de l'utilisateur, ou `--yes` pour une installation sans interaction. Le skill explique l'installation, l'invocation et la signification du contexte retourné. Il laisse les décisions de recherche et d'implémentation à l'agent appelant. Le skill du dépôt actuel vérifie la présence de `jg` et installe le CLI s'il est manquant ; l'authentification nécessite toujours la clé du fournisseur sélectionné. L'installeur du skill lui-même ne configure pas les identifiants.

`jg skill` délègue au CLI de skills et nécessite npm/npx ainsi qu'un accès réseau. Vous pouvez aussi exécuter cet installeur directement, sans avoir installé le CLI :

`npx skills add dzhng/jevgrep --skill jevgrep`
Dans la version 0.1.0, `jg skill` ne fait qu'imprimer le skill intégré ; utilisez `npx skills` avec cette version.

Il n'existe actuellement aucune commande `jg upgrade`. Mettez à jour le CLI avec npm :

```
npm install -g @dzhng/jevgrep@latest
jg --version
```

Mettez à jour le skill installé séparément en relançant `jg skill`. La mise à jour du package npm n'écrase pas les fichiers de skill dans vos projets. Consultez le guide du package pour les détails d'authentification.

Utilisez `jg` quand vous savez quel comportement vous devez comprendre mais pas où il se trouve :

```
jg "Where is authentication checked before a request reaches a handler?" .
jg "How are database connections created, pooled, and closed?" ./src
jg "Which tests cover retry behavior when a request times out?" .
```

Jevgrep explore la hiérarchie du dépôt et suit les branches pertinentes. Il sélectionne les fichiers en utilisant des aperçus de contenu, puis identifie les unités de code source utiles et le contexte environnant. Il conserve les emplacements de fichiers pertinents même lorsqu'il ne peut pas retourner un extrait avec confiance ; il ne force pas chaque recherche dans une liste fixe des deux meilleurs résultats.

Le résumé et la liste compacte des fichiers viennent en premier, suivis du code source sélectionné avec des références de lignes, puis des emplacements détaillés des déclarations et des appels. Python, TypeScript/JavaScript, Go et Rust supportent l'analyse des déclarations ; les autres textes utilisent une méthode de repli. La sortie est une preuve que l'agent doit utiliser, non une réponse générée ni une garantie que tous les fichiers pertinents ont été trouvés. Voir un exemple de sortie enregistré.

Quand vous connaissez déjà un symbole ou un chemin exact, une lecture directe ou une recherche `rg` peuvent suffire. Jevgrep est le plus utile pour les questions qui s'étendent sur des fichiers inconnus.

**Même intelligence, coût d'agent de codage ~30 % plus bas.** Jevgrep et la baseline sans Jev ont tous deux résolu **8/10 tâches**. Le coût total de Sol est passé de **7,62 $ à 5,44 $** — une réduction mesurée de **28,6 %**, arrondie à ~30 % — incluant les tentatives échouées et excluant le coût de Jev.

Cette comparaison utilise dix tâches Python SWE-bench ajustées, un package installé figé et le skill public exact de ce dépôt. Elle mesure le succès des tâches et le coût, pas une amélioration de vitesse ni une économie garantie sur chaque dépôt. Voir les résultats et la méthodologie pour les coûts par tâche, les identités des artefacts et les limitations. Une étude de vitesse séparée mesure les optimisations locales de suivi avec l'endpoint TypeSafe natif de Jev.

Le re-test du coût total en version 0.4.3, incluant Jev, a mesuré un coût total **25,8 % plus bas avec les mêmes 8/10 tâches résolues**. Le graphique plus ancien d'environ ~30 % ci-dessus rapporte le coût de Sol seul. Les futurs totaux de benchmark incluront Jev.

L'évaluation de la version 0.5.0 a conservé 8/10 résolutions tout en réduisant le coût natif de Jev d'environ 59 % par rapport à ce run 0.4.3. Le coût combiné Sol-plus-Jev était 2 à 3 % plus élevé, accepté comme un petit compromis pour cette version. Ces observations ponctuelles n'établissent pas d'équivalence statistique ni une amélioration de vitesse.

Les protocoles actuels et les expériences ultérieures se trouvent dans les journaux d'évaluation.

Les recherches envoient le contenu source éligible à Jev via le fournisseur sélectionné lors de l'authentification. Le filtrage par défaut du système de fichiers respecte les fichiers ignore et exclut les fichiers cachés, de dépendance/build, binaires, et les fichiers d'identifiants évidents. Ces filtres ne garantissent pas que toutes les informations sensibles ont été supprimées ; choisissez une racine de recherche que vous avez l'intention d'envoyer. `jg files [root]` compte les fichiers qu'une recherche sous cette racine pourrait lire, regroupés par répertoire de premier niveau, sans clé de fournisseur ni requête réseau. Elle prend les mêmes drapeaux de filtrage que la recherche. Pour ignorer des chemins à l'intérieur de cette racine pour une seule recherche, passez `--exclude` avec un motif gitignore relatif à la racine, par exemple `--exclude '**/*.test.ts' --exclude 'src/generated/'`.

`jg auth` demande votre fournisseur, puis enregistre sa clé dans un fichier de configuration accessible uniquement par le propriétaire. Relancer auth remplace cette configuration ; les recherches utilisent toujours le fournisseur enregistré. `jg doctor` la vérifie avec une entrée synthétique. Les clés enregistrées existantes sans fournisseur restent des clés Vercel. Les identifiants basés sur l'environnement et les surcharges d'endpoint ne sont pas utilisés ; exécutez `jg auth` si vous en dépendiez auparavant. Les réponses d'évaluation sont mises en cache localement par défaut. Le CLI écrit sa sortie sur stdout et ne crée pas de fichiers de rapport. Utilisez `jg --help` pour les contrôles de cache, les surcharges de recherche, et le comportement en cas de résultat incomplet.

Le dépôt utilise TypeScript, les workspaces Bun, et Turborepo. Depuis un checkout :

```
bun install --frozen-lockfile
bun run dev --help
bun run verify
```

La vérification inclut des tests Docker du package Node uniquement installé. Pour le raisonnement derrière la récupération, l'analyse, le cache, et la gestion des échecs, commencez par le dossier d'architecture et d'implémentation. Les directives de release couvrent la publication npm déclenchée par tag et la vérification du package public exact.

## Pourquoi ça compte
Jevgrep illustre une tendance vers des outils spécialisés de recherche sémantique de code pour agents autonomes, avec des mesures de coûts chiffrées plutôt que de simples promesses de performance — un signal utile pour la veille sur l'outillage des agents de codage et l'optimisation des coûts d'inférence.
