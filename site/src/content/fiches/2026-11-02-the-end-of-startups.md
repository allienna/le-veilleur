---
title: "The end of startups"
date: 2026-11-02
url: "https://leadershipintech.com/links/23639/3d78f33c-7ca0-4e03-9c70-68e56918a4cd/email"
keywords: ["compute", "GPU", "startups IA", "crédit", "marché des forwards", "SF Compute"]
theme: "IA"
tone: "opinion"
used_in: ["2026-11-02"]
---

## Résumé
L'article avance que, dans les six prochains mois, la pénurie mondiale de capacité de calcul va rendre l'accès aux GPU structurellement impossible pour la plupart des startups d'IA, faute de statut « investment grade ». Ce goulot d'étranglement de crédit force les startups à payer des acomptes énormes (jusqu'à 100 % du contrat), pendant que les marges de l'inférence s'érodent et que les grandes entreprises prennent un avantage croissant. L'auteur (SF Compute) présente sa solution : un marché de forwards physiquement réglés qui transforme l'heure de GPU, plutôt que le cluster lui-même, en collatéral liquide pour les prêteurs.

## Points clés
- Le compute mondial est totalement vendu ; les startups non « investment grade » doivent verser des acomptes pouvant atteindre 100 % du contrat pour obtenir des GPU.
- Les prêteurs et les clouds ne peuvent souscrire le risque qu'en fonction de la solidité financière du client (l'offtaker), pas du cluster GPU en tant qu'actif.
- Les marges actuelles de l'inférence (ex. : un B300 loué ~6 $/h permettant de revendre ~30 $/h d'inférence) sont considérées comme non durables et vouées à s'éroder avec la hausse des prix des GPU et l'arbitrage concurrentiel.
- Ce « credit bottleneck » crée un cercle vicieux auto-renforçant : avoir du crédit permet d'obtenir des tokens, ce qui permet de construire de meilleurs produits plus vite, de générer plus de revenus, et donc d'obtenir encore plus de crédit.
- Les grandes entreprises (type Fortune 500) capables de déployer d'un coup des milliards en tokens prennent un avantage structurel écrasant sur les startups qui doivent d'abord lever ces montants avant même d'avoir un produit.
- SF Compute propose de résoudre ce problème via un marché liquide de forwards physiquement réglés, où l'heure de GPU devient un collatéral cessible, réduisant la dépendance au risque de crédit du client final.

## Analyse approfondie
Dans les six prochains mois, la plupart des startups d'IA ne pourront plus acheter de capacité de calcul. Le compute mondial est entièrement vendu. Pour obtenir de la capacité, il faudra s'inscrire pour un nouveau cluster. Cependant, il devient de plus en plus difficile d'obtenir de la capacité en ligne auprès d'acteurs qui ne sont pas « investment grade » (de qualité d'investissement).

Les startups ne sont pas « investment grade ». Donc, pour obtenir de la capacité, on leur demande de payer des acomptes de plus en plus élevés. Nous avons vu ce chiffre monter jusqu'à 100 % du contrat payé à l'avance, une exigence née du fait que ni le prêteur ni le cloud ne pouvaient absorber de risque de crédit supplémentaire.

Pendant ce temps, les locataires « investment grade » restent rares. Les quelques locataires « investment grade » qui subsistent voient leur notation se dégrader progressivement à mesure qu'ils s'endettent davantage pour revendre ensuite à des acheteurs de tokens qui, eux, ne sont pas « investment grade ».

C'est le goulot d'étranglement de crédit (the credit bottleneck).

Nous nous attendons à ce que les acheteurs « investment grade » de GPU exigent de plus en plus que les acheteurs de tokens soient eux-mêmes « investment grade », ou qu'ils versent un acompte important à l'avance. Aujourd'hui, les entreprises d'inférence sont capables de servir leurs clients avec des marges élevées, ce qui signifie que leurs flux de trésorerie peuvent leur permettre d'être considérées comme solvables, même lorsque leurs clients ne le sont pas.

Cependant, il n'est pas certain que ces marges soient durables. Au moment où ces lignes sont écrites, on peut louer un B300 pour 6 $/h, puis générer environ 30 $/h en revendant de l'inférence sur cette capacité. C'est une marge saine, mais rien n'empêche d'autres acteurs d'arbitrer cette marge jusqu'à la faire disparaître. Nous anticipons une hausse des prix des GPU, ce qui signifie que les marges baisseront au niveau de la couche d'inférence. Des marges en baisse rendent plus difficile l'obtention d'une meilleure notation de crédit, ce qui renforce l'incitation à s'assurer des clients « investment grade » pour les tokens.

Lorsque cela se produit, il devient structurellement plus difficile de construire une startup, dans n'importe quel secteur. Si vous avez du crédit, vous obtenez des tokens, et si vous obtenez des tokens, vous construisez de meilleurs produits plus rapidement, vous gagnez plus d'argent, et vous obtenez un meilleur crédit. Ces tokens deviendront plus difficiles à acquérir pour les clients ayant un mauvais crédit. Pendant ce temps, la concurrence au niveau de la couche applicative exigera de dépenser des tokens plus rapidement ; une entreprise du Fortune 500 capable de déployer 1 milliard de dollars en tokens en quelques jours dispose d'un avantage écrasant sur une startup qui doit d'abord lever 1 milliard de dollars avant même que son produit n'existe.

Pour résoudre ce problème, il faut amener les prêteurs à considérer le cluster de GPU comme un collatéral de valeur. Aujourd'hui, les prêteurs sont contraints de souscrire uniquement sur la base du risque de crédit de l'offtaker (le laboratoire d'IA). À mesure que l'IA prend de l'ampleur, ces acteurs épuisent leur capacité à absorber le risque de crédit, ce qui pousse l'ensemble du secteur à rechercher des contreparties toujours plus solvables.

C'est le problème que SF Compute résout, en construisant un marché de forwards physiquement réglés pour le compute. Nous permettons aux prêteurs d'utiliser l'heure de GPU comme collatéral, sur un carnet d'ordres liquide, plutôt que le cluster de GPU, qui est non fongible et nécessite un gestionnaire (servicer) susceptible de faire défaut précisément au moment où l'on a le plus besoin de lui. Si un prêteur obtient une heure de GPU comme collatéral, le risque de crédit du client compte moins ; si le laboratoire d'IA de deux personnes installé dans une maison victorienne de San Francisco ne parvient pas à honorer ses paiements, le prêteur dispose d'une voie réelle pour vendre le collatéral. Cela rend les startups possibles, alors même que cette voie semble de plus en plus difficile dans l'IA.

Si vous raisonnez à partir des premiers principes et que ce problème vous tient à cœur, nous recrutons chez San Francisco Compute.

## Pourquoi ça compte
Ce texte met en lumière un risque structurel pour l'écosystème des startups d'IA : la pénurie de GPU se traduit par un verrouillage par le crédit qui pourrait avantager durablement les grands groupes au détriment des jeunes entreprises. C'est un signal à surveiller en veille tech, car il touche aux fondations économiques (financement, collatéralisation du compute) qui conditionnent qui pourra innover dans l'IA demain.
