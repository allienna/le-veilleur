---
title: "How Can You Be Responsible for Code You Don't Understand, Especially When You Can No Longer Program?"
date: 2026-11-19
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fnaildrivin5.com%2Fblog%2F2026%2F11%2F11%2Fhow-can-you-be-responsible-for-code-you-don-t-understand.html%3Futm_source=tldrdev/1/010001a1ee96e867-c9c1cb9b-0168-4ef0-9d7e-fa9e6587e653-000000/gpcx6lula0CraHddiLMx1y0hRGw9dkF2DI75Ou3_hHM=452"
authors: ["David Bryant Copeland"]
keywords: ["déskillement", "IA générative", "programmeurs", "product management", "responsabilité", "qualité du code"]
theme: "Leadership"
tone: "opinion"
used_in: ["2026-11-19"]
---

## Résumé

L'auteur part d'un constat : si l'IA écrit tout le code et que plus personne ne le relit, comment rester responsable d'un code qu'on ne comprend plus — et qu'on ne pourra bientôt plus jamais comprendre ? Sa réponse est double : les programmeurs deviennent responsables des résultats ("outcomes") plutôt que du code lui-même, et surtout, l'IA n'est pas un outil d'assistance mais un remplacement, dont la fonction première est de déskiller ceux qui l'utilisent. En s'appuyant sur un témoignage Reddit devenu viral, il montre que des développeurs ayant cessé d'écrire du code perdent rapidement leurs compétences, et que les agents IA eux-mêmes produisent du code redondant et mal structuré. Il en conclut que les équipes doivent accepter que le code devienne une "boîte noire" et redéfinir les responsabilités à un niveau supérieur à la ligne de code.

## Points clés

- Un témoignage Reddit devenu viral illustre un déskillement rapide : des développeurs n'ayant quasiment plus écrit de code "non trivial" depuis un an mettent désormais deux jours pour une tâche qui prenait une après-midi en 2024.
- Les agents IA eux-mêmes peinent : ils réinventent sans cesse des fonctions utilitaires qui existent déjà ailleurs dans le code, aboutissant à plusieurs versions redondantes de la même chose.
- Pour l'auteur, l'IA n'est pas un assistant mais un substitut aux programmeurs, dont l'effet structurel est de déskiller ses opérateurs.
- Les anciens programmeurs deviennent des opérateurs de générateurs de code, mi-techniciens mi-product managers juniors : ils ne répondent plus de la qualité du code mais de résultats, même quand ceux-ci ne sont pas explicitement définis ni mesurés.
- L'idée de "bon code" est selon lui une illusion : un code "bon" n'est qu'un code familier ; et la familiarité repose sur la stabilité, que la vitesse de génération de l'IA vient justement perturber.
- Conclusion : les équipes doivent planifier pour que le code devienne une boîte noire indéchiffrable, redéfinir les niveaux de responsabilité en conséquence, et admettre que le déskillement est difficile, voire impossible, à inverser rapidement.

## Analyse approfondie

**Le déskillement sous nos yeux**

L'auteur part d'un témoignage publié sur Reddit et largement partagé, qui illustre selon lui ce qui se passe quand des programmeurs arrêtent de programmer. Un contributeur y raconte que, ce mois-ci, le management a discrètement recommencé à demander à l'équipe d'"en écrire davantage eux-mêmes" — sauf que la moitié de l'équipe n'a plus rien écrit de non trivial depuis un an, et que cela se voit : une tâche qui aurait pris une après-midi en 2024 en a pris deux jours. Le même témoignage note que les agents IA eux-mêmes rencontrent des difficultés, car ils réimplémentent sans cesse des fonctions utilitaires qui existent déjà ailleurs dans la base de code, créant plusieurs versions concurrentes de la même chose.

Pour l'auteur, le management de cette équipe est probablement surpris par ce résultat, mais aucun programmeur expérimenté ne devrait l'être : cesser d'écrire du code au quotidien entraîne rapidement une perte de familiarité avec la base de code, puis, à terme, une perte de la capacité même à programmer. C'est le déskillement à l'œuvre.

**Bienvenue dans l'équipe product management**

Les anciens programmeurs deviennent, selon l'auteur, en partie des opérateurs de générateurs de code, en partie des product managers juniors. Ils ne sont plus responsables de la qualité du code — comment le pourraient-ils ? — mais ils restent responsables des résultats, même si ces résultats ne sont ni explicitement nommés ni mesurés.

Si ces résultats restent implicites (ou explicites mais non mesurés), tout le monde va en pâtir. L'auteur affirme que, s'il faisait partie d'une équipe où l'usage de l'IA est imposé ou largement répandu, il chercherait rapidement à cartographier la chaîne de valeur du logiciel qu'il écrivait auparavant. Il cesserait de parler de qualité de code ou de couverture de tests pour se concentrer sur le suivi des résultats — une démarche qui relève, au moins en partie, du product management.

Reste alors une question : dans quelles conditions devient-il nécessaire que quelqu'un retourne regarder le code lui-même ?

**Les conséquences du déskillement**

Un manager qui autorise, voire impose, l'usage de générateurs de code IA doit accepter qu'il crée une situation où plus personne ne peut comprendre le code de façon fiable, ni même parvenir à le comprendre un jour. À court terme, les programmeurs expérimentés conserveront certaines compétences et pourront naviguer dans ce qui est, pour eux, une base de code entièrement nouvelle. Mais à long terme, il n'y aura simplement plus de programmeurs expérimentés.

Cette situation est-elle évitable ? Une équipe peut-elle profiter de tous les avantages de l'IA sans subir les inconvénients du déskillement qu'elle entraîne ? S'il faut un jour revenir dans le code, existe-t-il un moyen de garantir qu'on en aura encore la capacité ?

L'auteur répond "non". On pourrait croire que si l'IA produit du code "suffisamment bon", il sera possible, voire facile, pour un programmeur de le comprendre. Mais, selon lui, le "bon code" n'existe pas vraiment en tant que tel : le "bon code", c'est simplement "du code qu'on connaît déjà". Certes, il existe des façons d'écrire du code qui réduisent la charge conceptuelle, mais il n'existe aucun moyen de produire une base de code qu'un nouvel arrivant comprendrait comme par magie. Et même si cela existait, la stabilité reste la condition de la familiarité — or la génération de code par IA produit un renouvellement permanent et massif du code. La vitesse a un coût.

**Prévoir que le code devienne une boîte noire**

La seule conclusion que l'auteur en tire est que l'équipe doit pouvoir produire les résultats attendus sans avoir besoin de regarder le code. Il faut donc définir la compréhension du système à un niveau plus élevé que la ligne de code.

Classiquement, les couches du système sont réparties ainsi : le management est responsable du système dans son ensemble, les product managers des différents modules ou périmètres fonctionnels, et les programmeurs de l'implémentation.

Sans programmeurs, et sans capacité à comprendre ou même à gérer le code, cette répartition change : l'équipe qui pilote les générateurs de code IA ne peut plus vraiment être considérée comme des "programmeurs", puisqu'elle en écrit très peu elle-même. La différence de compétences entre ces "opérateurs IA" et les product managers devient d'ailleurs beaucoup plus floue qu'elle ne l'était entre product managers et programmeurs — sans pour autant que ces rôles deviennent identiques : toutes les compétences liées à la conception et à l'exploitation des systèmes restent nécessaires.

Quant au manager de l'équipe évoquée sur Reddit, l'auteur juge qu'il vit dans un monde imaginaire s'il pense pouvoir simplement arrêter d'utiliser l'IA et reprendre là où l'équipe s'était arrêtée. On ne peut pas déskiller une équipe puis attendre d'elle qu'elle retrouve rapidement ses compétences — certains de ses membres pourraient même ne jamais les retrouver.

## Pourquoi ça compte

Ce billet pose une question organisationnelle rarement formulée aussi crûment : si l'IA devient le principal auteur du code, la gouvernance technique doit se déplacer de la qualité du code vers le pilotage par les résultats, au risque de perdre durablement la capacité d'une équipe à comprendre ses propres systèmes.
