---
title: "Maybe We Shouldn't Be Reviewing All This Code"
date: 2026-09-14
url: "https://leadershipintech.com/links/23269/3d78f33c-7ca0-4e03-9c70-68e56918a4cd/email"
keywords: ["revue de code", "IA générative", "ingénierie logicielle", "pair programming", "dette cognitive", "architecture logicielle"]
theme: "Leadership"
tone: "opinion"
used_in: ["2026-09-14"]
---

## Résumé
À la suite d'un désaccord public avec Brian Houck (DX) lors d'un panel à Code Remix, l'auteur (un collègue de Martin Fowler, vraisemblablement chez Thoughtworks) répond à l'article de Houck sur l'utilité de la revue de code à l'ère de l'IA générative. Le constat de départ est partagé : l'IA produit désormais bien plus de code que les humains ne peuvent en réviser sérieusement (chez Meta, le nombre de lignes par diff validé aurait augmenté de 106 % en un an ; chez DX, la taille médiane des pull requests aurait grimpé de 64 %). Mais là où Houck craint de perdre, en automatisant la revue, tout ce qu'elle apporte par ailleurs (partage de connaissances, formation, ownership collective, cohérence architecturale), l'auteur retourne la question : pourquoi attendre la revue de code pour obtenir ces bénéfices ? Sa thèse est qu'il faut déplacer ces échanges en amont du développement plutôt que de les concentrer dans une étape de contrôle a posteriori.

## Points clés
- L'explosion du volume de code généré par IA (+106 % chez Meta, +64 % de taille médiane des PR chez DX) rend intenable une revue humaine systématique, ligne par ligne.
- La revue de code a toujours cumulé plusieurs fonctions différentes — détection de bugs, transfert de connaissances, formation des juniors, ownership collective, alignement architectural — qui gagneraient à être traitées séparément et plus tôt.
- L'auteur prône de « décaler le jugement vers la gauche » : pair programming, conception collective au tableau blanc, « fitness functions » pour encoder les contraintes d'architecture, automatisation du formatage, du linting et des contrôles de sécurité déterministes.
- Il propose une « revue par exception » : ne mobiliser un regard humain que sur les changements réellement sensibles (architecture majeure, frontières de sécurité, fort rayon d'impact, incertitude de l'équipe), et non sur chaque diff.
- Il met en garde contre la tentation de faire réviser le code par un agent IA imitant un reviewer humain, ce qui reviendrait à automatiser le rituel sans en interroger la raison d'être.
- Il reconnaît le risque de « dette cognitive et d'intention » pointé par Houck (le logiciel grossit pendant que les humains comprennent de moins en moins pourquoi il fonctionne ainsi), mais pense que la revue obligatoire n'y remédie pas vraiment ; la parade passe plutôt par la conception collaborative, le pairing et une architecture exécutable.

## Analyse approfondie
L'auteur revient sur un panel organisé par Moderne lors de l'événement Code Remix, où il a partagé la scène avec Brian Houck (DX) — un échange qu'il a apprécié précisément parce qu'ils n'étaient pas d'accord, chacun défendant solidement sa position, dans l'esprit de ce que prône Martin Fowler à propos des débats contradictoires. Houck a depuis publié un texte intitulé *À quoi servent vraiment les revues de code ?*, et l'auteur écrit cette réponse en retour, tout en précisant qu'il partage largement les objectifs de Houck : il conteste seulement l'idée que la revue de code soit le bon moyen d'y parvenir.

Le point de friction : l'IA produit aujourd'hui plus de code que les humains ne peuvent raisonnablement en examiner. Houck avance des chiffres marquants — chez Meta, le nombre de lignes de code par diff validé par un humain aurait bondi de 106 % en un an, et les données internes de DX montreraient une hausse de 64 % de la taille médiane des pull requests. Sa crainte, partagée par l'auteur, est que supprimer purement et simplement la revue humaine fasse perdre tout ce qu'elle apporte au-delà de la simple chasse aux bugs : transmission des connaissances, formation des ingénieurs juniors, construction d'une ownership collective, diffusion de la compréhension architecturale.

La question que pose l'auteur est différente : pourquoi attendre l'étape de revue de code pour obtenir tous ces bénéfices ? Il confie n'avoir jamais été pleinement convaincu par la pull request comme centre de gravité du développement logiciel — non pas que les ingénieurs ne devraient pas regarder le code des autres, mais parce qu'il trouve étrange de construire quelque chose, de le finaliser, de l'empaqueter, de le transmettre à quelqu'un d'autre, et alors seulement d'avoir la conversation essentielle sur la pertinence de ce qui a été construit et sur la façon dont ça l'a été. Il ajoute, non sans ironie, ne pas vouloir s'étendre sur les conflits de fusion (merge conflicts), qui lui ont déjà fait perdre trop d'heures.

### Déplacer le jugement plus tôt
L'un des principes appris tôt chez Thoughtworks est de raccourcir les boucles de rétroaction : si un retour a de la valeur, il ne faut pas le supprimer, mais le rapprocher de la décision qu'il est censé éclairer. L'auteur reprend un par un les bénéfices qu'on prête traditionnellement à la revue de code :

- Pour **explorer des solutions alternatives**, il vaut mieux le faire avant d'en implémenter une plutôt qu'après coup.
- Pour le **transfert de connaissances**, le pair programming est plus efficace : observer quelqu'un raisonner en temps réel sur un problème, en personne ou à distance, enseigne bien davantage que de lire sa solution une fois terminée.
- Pour que les **ingénieurs juniors apprennent à penser comme des ingénieurs expérimentés**, il faut les faire travailler avec ces derniers pendant qu'ils réfléchissent — via le pairing, mais aussi via des sessions de conception collectives au tableau blanc avant même d'écrire (ou de demander à un agent d'écrire) la moindre ligne.
- Pour construire une **ownership collective**, il faut organiser les équipes pour qu'elles construisent et exploitent réellement le logiciel ensemble, plutôt que de compter sur une pull request pour informer chacun de ce qu'un autre a déjà fait — là encore via le pairing, le mob programming ou des sessions de conception d'équipe.
- Pour l'**alignement architectural**, concevoir ensemble puis encoder les contraintes importantes sous forme de fitness functions.
- Et pour tout ce qui relève du formatage, du linting, des problèmes de sécurité connus ou de ce qui peut être testé de façon déterministe : automatiser. Selon l'auteur, on ne devrait plus, en 2026, débattre encore des espaces blancs dans le code.

Le pair programming, le développement en trunk-based, les tests automatisés, l'analyse statique, les fitness functions et les scans de sécurité déplacent tous la rétroaction plus tôt dans le cycle. Les agents IA peuvent eux aussi de plus en plus participer à ces boucles — challenger des choix de conception, tester des hypothèses, vérifier en continu ce qui est construit — mais la réflexion de fond doit rester portée par des humains expérimentés. Et si l'on veut que cette expérience profite à toute l'équipe, il faut agir collectivement bien avant l'étape de revue de code, pas seulement à ce moment-là.

### Revue par exception
Rien de tout cela ne signifie que plus personne ne devrait jamais relire de code. Il existe des changements pour lesquels l'auteur souhaite explicitement qu'un autre humain expérimenté pose un regard : un changement architectural fondamental par exemple — en supposant qu'une session de conception collective ait déjà eu lieu, l'équipe pourrait vouloir revoir le code ensemble pour confirmer la bonne implémentation ou discuter d'ajustements. D'autres cas : un changement qui traverse une frontière de sécurité sensible, un changement à très fort rayon d'impact, une zone peu familière d'un système critique, ou simplement une situation où l'équipe dit ouvertement « je ne suis pas sûr de ce point ».

Ce sont précisément les endroits où le jugement humain a de la valeur — mais c'est très différent d'exiger qu'un humain inspecte chaque changement simplement parce que c'est la cérémonie historiquement utilisée pour instaurer la confiance. Or on sait désormais que cette approche n'est plus tenable, ce qui explique que la revue de code revienne sans cesse comme un point de friction ou un goulot d'étranglement. Si un agent produit dix fois plus de code mais que chaque ligne finit par attendre en file qu'un ingénieur senior l'inspecte, on n'a pas créé une organisation d'ingénierie dix fois plus performante : on a créé un immense backlog et un nouveau goulot d'étranglement.

L'auteur ne pense pas non plus que la solution consiste à faire jouer à un agent IA le rôle du reviewer humain pour préserver exactement le même processus, en plus rapide : ce serait automatiser la cérémonie plutôt que d'interroger sa raison d'être.

Il reste toutefois un point de l'argumentaire de Houck qui préoccupe réellement l'auteur : l'idée d'une dette cognitive et d'intention qui s'accumule — le logiciel grossit pendant que les humains responsables en comprennent de moins en moins les raisons de fonctionnement. L'auteur juge ce risque bien réel, mais ne pense pas que les pull requests obligatoires en soient un rempart particulièrement solide. Si les agents produisent une part substantiellement plus grande de l'implémentation, il devient nécessaire d'être beaucoup plus délibéré sur le maintien de la compréhension humaine — via la conception collaborative, le pairing, de bonnes délimitations de responsabilités, une architecture exécutable, une responsabilité opérationnelle partagée, et probablement des pratiques qui restent encore à inventer.

**Il faut que les ingénieurs comprennent les systèmes, pas les diffs.**

C'est peut-être cela que l'IA met en lumière : pendant des années, on a fait porter à l'humble revue de code un nombre extraordinaire de responsabilités — porte de qualité, contrôle de sécurité, revue d'architecture, mécanisme de mentorat, système de partage de connaissances, modèle d'ownership. Cela a plus ou moins fonctionné tant que les humains ne pouvaient produire du code qu'à un certain rythme. Cette contrainte est en train de disparaître. Alors peut-être que la vraie question n'est pas de savoir comment faire réviser le code plus vite, mais pourquoi on attend l'étape de revue de code pour avoir, en premier lieu, toutes les conversations qui comptent vraiment.

## Pourquoi ça compte
Ce texte capture un débat de fond dans l'ingénierie logicielle à l'ère de l'IA générative : à mesure que les agents produisent un volume de code que les humains ne peuvent plus réviser ligne par ligne, les organisations doivent repenser où et quand se joue réellement le jugement humain — un sujet clé pour toute veille sur l'impact organisationnel de l'IA en entreprise tech.
