---
title: "How to read code"
date: 2026-10-08
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.seangoedecke.com%2Fhow-to-read-code%2F%3Futm_source=tldrdev/1/010001a116141a79-0c77fa27-f107-43c8-8993-97c7650472cb-000000/zOiS_I6brQoRXVfa2A57T_aRnibsXkW1G46NPBqIZz0=452"
authors: ["Sean Goedecke"]
keywords: ["lecture de code", "revue de code", "diff", "LLM", "ingénierie logicielle", "complexité"]
theme: "Tech"
tone: "opinion"
used_in: ["2026-10-08"]
---

## Résumé
L'auteur, Sean Goedecke, soutient que lire du code n'a rien à voir avec lire un texte en anglais : le code est organisé pour être exécuté par une machine et non pour une lecture linéaire, il est le plus souvent consulté sous forme de diffs plutôt que comme produit fini, et sa complexité structurelle dépasse largement celle des textes les plus denses. Il propose une méthode de lecture « non linéaire », inspirée du « balayage dyadique » utilisé pour lire les articles de mathématiques, qui consiste à multiplier les passes successives (structure globale, puis sous-structures, puis détails) plutôt que de lire ligne par ligne. Il conclut en affirmant, à partir d'exemples concrets, que le code généré par des LLM reste indispensable à relire attentivement, car les erreurs qu'il contient ne sont pas tant des bugs que des désalignements de valeurs techniques.

## Points clés
- Le code est contraint par la machine (il doit s'exécuter), alors qu'un texte anglais peut être réordonné librement par son auteur pour l'effet recherché sur le lecteur.
- Les ingénieurs lisent surtout des diffs (changements incrémentaux) et non des programmes complets, ce qui complique le suivi de la logique d'ensemble.
- Le code est structurellement plus complexe qu'un texte littéraire : les dépendances peuvent s'étendre à toute la base de code, alors que les dépendances grammaticales restent en général bornées à un paragraphe.
- La technique du « balayage dyadique » (dyadic scanning), empruntée à la lecture des papiers de mathématiques, propose plusieurs passes : structure générale, puis sous-structures, puis détails fins — plutôt qu'une lecture séquentielle.
- L'auteur décrit sa propre méthode : suivre un chemin important (ex. le happy path d'une fonctionnalité) en traçant les appels de fonctions, en traitant tout le reste comme une boîte noire, avant de relire l'ensemble de façon linéaire en dernier lieu.
- Le code généré par des LLM contient souvent des erreurs d'alignement (et non de simples bugs) : il faut donc continuer à le lire attentivement, qu'on le relise soi-même ou qu'on délègue cette relecture à une IA.

## Analyse approfondie
L'article part d'un constat simple : tout le monde sait lire un livre — du début à la fin, mot après mot — mais cette habitude ne s'applique pas au code. Trois différences structurelles l'expliquent.

La première tient à l'ordre. Un texte en anglais n'a (presque) aucune contrainte d'ordre autre que celle choisie par l'auteur pour guider le lecteur ; on peut réorganiser des idées à volonté lors de la rédaction. Le code, en revanche, est écrit pour être *exécuté* par un ordinateur, et son ordre est donc dicté par des facteurs non humains : on ne peut pas déplacer une ligne de code en tête de fichier simplement parce qu'elle ferait une meilleure introduction pour un lecteur humain.

La deuxième différence concerne le mode de lecture. Un texte anglais se lit comme un produit fini, alors que le code se lit presque toujours sous forme de *diff* — c'est-à-dire des modifications ponctuelles apportées à du code existant, et non des programmes entièrement nouveaux. L'auteur illustre cela par une analogie : si cet article devait être lu comme un diff, on lirait chaque brouillon successif dans l'ordre de rédaction, une phrase modifiée ici, une nouvelle phrase là — il deviendrait alors facile de perdre le fil de la cohérence globale.

La troisième différence, que l'auteur souligne en tant qu'amateur de littérature, est la complexité structurelle. Même les livres réputés difficiles restent syntaxiquement plus simples que la plupart des programmes informatiques : les dépendances grammaticales sont en général bornées à un seul paragraphe, alors que les dépendances dans le code peuvent s'étendre à l'ensemble de la base de code. Les grandes bases de code sont aussi simplement plus longues : à titre de comparaison, *Guerre et Paix* compte environ 600 000 mots, un ordre de grandeur que de nombreuses bases de code modernes atteignent... en lignes.

L'auteur rappelle une idée qu'il a défendue ailleurs : les grands programmes sont trop complexes pour qu'une seule personne les comprenne entièrement. Lire du code dans un grand projet relève donc d'un exercice de *compromis* — décider quelles parties approfondir et lesquelles survoler, en répartissant une capacité d'attention limitée sur l'ensemble du code.

Conséquence de tout cela : selon l'auteur, la plupart des gens lisent très mal le code. Soit ils s'acharnent à le lire de bout en bout comme un livre et perdent le fil du flux d'exécution ; soit ils se contentent de lire le diff et manquent l'importance des parties non modifiées du code ; soit, submergés par la complexité, ils abandonnent et devinent simplement ce que fait le code.

Pour faire mieux, l'auteur s'appuie sur un article qu'il juge excellent, consacré à la lecture des articles de mathématiques (dont la structure est similaire à celle du code). Cet article décrit une technique appelée « balayage dyadique » (*dyadic scanning*) : plutôt que de lire lentement et séquentiellement, on effectue plusieurs passes successives — d'abord pour cerner la structure globale, puis la sous-structure, puis enfin les détails.

Appliquée au code, cette méthode implique de lire dans le désordre. L'auteur explique qu'il choisit un chemin important (par exemple le « happy path » d'une fonctionnalité introduite dans un diff) et qu'il trace les appels entre fonctions pour avoir une idée du flux, avant de s'attarder sur ce que ces fonctions font réellement. Il procède généralement par passes multiples, chacune suivant un fil différent : il prend une fonction ou une donnée et cherche à comprendre comment elle est utilisée, en remontant vers plusieurs sites d'appel (y compris hors du diff). Pour les petits diffs, il utilise un simple « ctrl+F » pour naviguer entre les occurrences d'un nom de fonction ; pour les diffs plus volumineux, il ouvre le code dans un éditeur et utilise le « ctrl+clic » pour la navigation. Il s'efforce de rester rigoureusement focalisé sur l'élément qu'il examine à cet instant, traitant tout le reste comme une boîte noire.

Ce n'est qu'une fois sûr d'avoir compris le diff qu'il s'autorise une lecture attentive de bout en bout. Le but de cette dernière passe n'est plus de comprendre la structure — qu'il connaît déjà à ce stade — mais de repérer d'éventuelles bizarreries de code qui auraient échappé aux passes précédentes. S'il repère quelque chose d'inhabituel, il recommence des passes ciblées.

Cette méthode peut sembler lente, mais chaque passe est en réalité très rapide, puisqu'elle évite de décortiquer laborieusement chaque ligne.

L'article aborde ensuite un débat contemporain : beaucoup affirment qu'il n'est plus nécessaire de lire le code, soit parce que les LLM produiraient désormais un code fiable sans supervision, soit parce qu'on pourrait simplement demander à un LLM relecteur de le faire à notre place. L'auteur juge ces deux idées fausses.

Il concède que la qualité du code produit par une IA dépend fortement du contexte : comme il l'a écrit dans un autre billet (*Pure and impure software engineering*), certains domaines du logiciel (jeux vidéo, bibliothèques, outils comme les bases de données) ont des standards, pratiques et valeurs d'ingénierie très différents d'autres domaines (par exemple les systèmes distribués dans les grandes entreprises technologiques). Si l'on construit un outil uniquement pour soi-même, on peut sans doute se permettre de ne pas relire le code. Mais après avoir lu beaucoup de code généré par IA cette année, l'auteur affirme qu'il reste indispensable de le relire.

Il dit trouver *régulièrement* des erreurs massives dans le code généré par IA. Il précise que ce ne sont pas tant des bugs — le code fait généralement ce que l'IA voulait qu'il fasse — que des problèmes d'alignement. Il cite un exemple récent : un petit changement destiné à faire transiter une valeur supplémentaire à travers du code existant s'est transformé en un diff complexe de trois mille lignes, parce que l'agent IA avait repéré une condition de concurrence (race condition) et construit toute une machinerie pour la « corriger ». Or cette condition de concurrence était en réalité inoffensive par conception : deux données sans rapport pouvaient momentanément se désynchroniser, sans aucun impact pour les utilisateurs.

Les LLM peuvent-ils alors simplement lire le code à notre place ? L'auteur répond non, pour la même raison : même s'ils ne commettent aucune erreur, leurs valeurs techniques ne correspondront pas aux vôtres ni à celles de votre entreprise. On peut utiliser les LLM pour s'aider à lire du code, mais il faut alors relire et vérifier soigneusement ce que produit le LLM — tout en continuant à lire attentivement le code lui-même.

L'article se clôt par un renvoi vers un billet complémentaire de l'auteur sur les erreurs que commettent souvent les ingénieurs en revue de code, où il note que la revue de code a gagné en importance depuis que le code est facile à générer via les LLM, mais reste tout aussi difficile à relire.

## Pourquoi ça compte
Ce billet offre un contre-argument utile et bien construit à la tentation ambiante de déléguer entièrement la lecture et la relecture du code aux IA : à l'heure où les agents de codage se multiplient, il rappelle qu'une méthode de lecture rigoureuse — et une vigilance humaine sur l'alignement des choix techniques — reste indispensable pour toute veille sur les pratiques d'ingénierie logicielle assistée par IA.
