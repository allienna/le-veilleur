---
title: "ML compiler eng, your job is NP-hard"
date: 2026-11-26
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fianbarber.blog%2F2026%2F11%2F24%2Fml-compiler-eng-your-job-is-np-hard%2F%3Futm_source=tldrai/1/010001a2131daf4f-90f44adf-0961-488c-a5cb-31386993ed9d-000000/G0B9XBGN5Q5bJUguzJo1AfsvsthUk6N4VAA-s0MkMBk=452"
authors: ["Ian Barber"]
keywords: ["compilateurs", "disposition de tenseurs", "NP-difficile", "Triton", "GPU", "ptxas"]
theme: "Software"
tone: "opinion"
used_in: ["2026-11-26"]
---

## Résumé
L'article commente un papier d'Amazon démontrant que le choix optimal de disposition mémoire ("layout") des tenseurs pour les accélérateurs Trainium est un problème NP-difficile, même dans des cas restreints. L'auteur confronte ce résultat théorique à la pratique du compilateur Triton, où une passe baptisée *RemoveLayoutConversions* élimine les conversions de layout superflues à l'aide d'une heuristique de coût très simpliste (un coût de 0 ou de 32×octets). Des expériences montrent que cette heuristique est très imprécise (jusqu'à 19x d'erreur), mais qu'un modèle de coût plus fidèle ne change presque rien aux performances réelles, car la plupart des conversions sont évitées par réemission du calcul (rematerialization) plutôt que choisies. En creusant les écarts de performance restants, l'auteur découvre que la vraie source de variabilité se situe en aval, dans l'allocation de registres du compilateur `ptxas`, et non dans le choix du layout lui-même.

## Points clés
- Le papier "Tensor Seeks Layout" d'Amazon prouve que la sélection de layout est NP-difficile même avec un nombre constant d'entrées par opérateur et peu de layouts possibles par tenseur.
- Sur ResNet-50, leur solveur exact avec leur propre modèle de coût atteint 63,9M cycles, contre seulement 20,9M cycles pour les heuristiques "maladroites" existantes — signe que leur modèle de coût est lui-même discutable.
- Dans Triton, la passe *RemoveLayoutConversions* utilise une règle grossière (coût nul pour une permutation de registres locale, coût de 32×octets pour un passage par mémoire partagée).
- Des tests de l'auteur montrent que cette heuristique surestime le coût réel d'environ 4x en fp32, jusqu'à 19x en fp16 (et plus encore en fp8), mais qu'un modèle de coût corrigé ne modifie presque aucun résultat : sur les cas testés, 8 kernels ralentissent, 4 accélèrent, 9 restent inchangés.
- La raison : la plupart des conversions sont évitées grâce à la "rematerialization" (recalculer/recharger dans le format voulu plutôt que convertir), ce qui rend le choix de layout largement anecdotique dans la pratique.
- Les vrais écarts de performance observés (jusqu'à 15-26x sur un matmul) proviennent en réalité d'un autre compilateur en aval, `ptxas`, dont l'allocation de registres — très sensible à l'ordre des instructions — peut provoquer des "spills" massifs en mémoire (passage de 255 à 40 registres dans un cas cité).

## Analyse approfondie
L'auteur part d'un résultat du papier "Tensor Seeks Layout" d'Amazon : la sélection de disposition mémoire (layout selection) pour les tenseurs reste NP-difficile même dans des configurations restreintes — chaque opérateur n'ayant qu'un nombre constant d'entrées, et chaque tenseur n'admettant qu'un petit nombre de layouts possibles. Cette difficulté persiste même dans des configurations proches des graphes typiques dominés par des multiplications matricielles (matmul-heavy graphs).

Ce papier se concentre sur une analyse formelle très poussée du problème de layout, appliquée aux charges de travail Trainium. Les auteurs construisent un solveur exact de sélection de layout, et constatent que, sur ResNet-50, l'optimum prouvé selon leur propre modèle de coût nécessite 63,9 millions de cycles. Étonnamment, les règles heuristiques pourtant jugées "maladroites" n'en nécessitent que 20,9 millions. L'auteur du blog attribue cet écart à un modèle de coût peu fiable chez Amazon, point sur lequel il revient plus loin.

De nombreux travaux récents se sont penchés sur la nature même des layouts, mais cet article s'intéresse plutôt au moment et à l'endroit où l'on effectue les conversions entre eux.

En descendant d'un niveau de granularité, dans le compilateur Triton, cette décision est principalement gérée par la passe *RemoveLayoutConversions* : pendant la compilation, Triton insère des conversions de layout chaque fois qu'elles pourraient être nécessaires, puis cette passe les élague. Sa règle, très peu sophistiquée, attribue à chaque conversion un coût de `0` ou de `32×octets`. Un coût de "0" signifie que la conversion est une simple permutation de registres, entièrement locale. La valeur plus élevée s'applique aux "shuffles" et aux allers-retours par la mémoire partagée.

Cela a conduit l'auteur à se demander à quel point cette règle était erronée, comparée à l'approche plus structurée du papier d'Amazon. Après expérimentation, il constate que l'heuristique est effectivement assez fausse. Par rapport à une simple addition élément par élément, l'heuristique surestime le coût d'environ 4x en fp32, 19x en fp16, et parfois davantage encore en fp8. Pourtant, si l'on bascule vers le modèle de coût correct, peu de choses changent réellement : aucun kernel de tutoriel ne change de comportement, et globalement les variations de performance s'équilibrent : sur les cas testés, 8 deviennent plus lents, 4 plus rapides, et 9 restent identiques.

La raison principale est la "rematerialization" : plutôt que de convertir un layout, on remonte la chaîne de calcul pour recalculer ou recharger directement dans le format requis. Les conversions interviennent surtout dans les cas où l'on ne peut produire les données que d'une seule façon, tout en devant les consommer d'une autre. Dans ces cas, le choix de layout est en grande partie arbitraire, mais généralement sans grande conséquence : la majorité des kernels n'imposent en réalité aucun choix, et quand un choix existe, l'option par défaut s'avère presque toujours être la bonne.

L'auteur rappelle les efforts précédemment évoqués d'OpenAI pour éliminer les heuristiques du compilateur, mais souligne que ce cas précis semble être une zone où l'heuristique fait un travail raisonnable. En revanche, lorsqu'on creuse les cas où un écart de performance réel existe, on découvre que le problème vient encore d'un compilateur — mais un autre : `ptxas`.

La passe *RemoveLayoutConversions* existe pour réduire le nombre de conversions, ce qui est globalement une bonne chose. Mais sa sortie est ensuite transmise à `ptxas`, qui peut se montrer très sensible à des détails apparemment mineurs : dans un cas observé, un kernel de multiplication matricielle a vu ses performances multipliées par 15 à 26, uniquement grâce à un changement dans l'ordre des instructions. C'est `ptxas` qui décide de l'allocation des registres, et s'il estime qu'il n'y en a pas assez, il "déborde" (spill) vers la mémoire, ce qui dégrade fortement les performances.

Le constat du papier d'Amazon — que la recherche de layout est un problème calculatoirement difficile — est valide, et constitue un bon argument à partager avec sa direction. Mais en pratique, il n'est pas nécessaire d'explorer un très grand nombre d'options : il n'existe généralement que quelques emplacements possibles où placer une conversion dans un kernel donné. Le véritable défi consiste à choisir la bonne option en s'appuyant sur un modèle potentiellement imprécis du coût réel de ces opérations, compte tenu à la fois de la pile logicielle en aval (qui reste fermée/propriétaire) et du matériel lui-même. C'est précisément cette partie qui s'avère la plus délicate.

*Notes de l'auteur :*
- La passe en question contient d'ailleurs un commentaire "TODO: add a proper heuristic" (il faudrait ajouter une vraie heuristique) — ce comportement grossier n'est donc pas une surprise pour les développeurs de Triton.
- Dans le cas du gain de 15 à 26x, le simple fait de déplacer une instruction `local_load` six opérations plus tôt a permis à `ptxas` de passer de 255 registres utilisés à seulement 40 — sans que l'auteur sache expliquer précisément pourquoi.
- L'auteur ajoute, avec ironie, qu'il faut profiter de ce type de résultat NP-difficile pour impressionner sa direction tant que personne n'a encore produit 150 millions de lignes de preuve Lean démontrant que NP n'est finalement pas si difficile.
- Il note enfin que le papier d'Amazon applique ce même raisonnement à des graphes entiers comptant plus de 10 000 opérateurs, ce qui reste comparable, bien que d'une échelle très différente, au problème local traité dans Triton.

## Pourquoi ça compte
Ce billet illustre un phénomène classique en ingénierie des compilateurs ML : la complexité théorique (NP-difficile) n'implique pas forcément un impact pratique significatif, et les vrais goulots d'étranglement de performance se nichent souvent plus loin dans la chaîne d'outils (ici, l'allocation de registres de `ptxas`) plutôt que dans la décision qu'on croyait critique. Un signal utile pour quiconque travaille sur l'optimisation de kernels GPU ou suit les débats sur la place des heuristiques face aux solveurs formels dans les compilateurs IA.
