---
title: "Design Systems Should Be Fast by Default"
date: 2026-11-07
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fdenodell.com%2Fblog%2Fdesign-systems-should-be-fast-by-default%3Futm_source=tldrdev/1/010001a1b0ca9ef6-6fdd9b32-4ee1-4763-ae77-1d47fae7c361-000000/7sRUVH_HtpQEhTQoiQM7Siy8zoWDYcWTxhS_uJ3rC4c=452"
keywords: ["systèmes de design", "performance web", "benchmark", "virtualisation", "composants web", "tests automatisés"]
theme: "Software"
tone: "research"
used_in: ["2026-11-07"]
---

## Résumé
L'auteur a comparé la performance de dix systèmes de design open-source populaires (Mantine, Ant Design, Material UI, React Spectrum, Carbon, Fluent, Web Awesome, UI5, Spectrum Web Components, Ionic), construits sur différents frameworks (React, Lit, FAST, Stencil, etc.), en chronométrant deux scénarios réalistes : l'ouverture d'un sélecteur de pays à 249 options et la sélection simultanée de 100 cases à cocher. Les résultats montrent des écarts considérables entre bibliothèques — jusqu'à un facteur de plus de 20 entre la plus rapide et la plus lente — et révèlent que la lenteur ne vient pas du framework utilisé mais de choix d'implémentation précis (gestion des slots, absence de virtualisation, animations inutiles, layout thrashing). L'article défend l'idée que la performance devrait être un critère de qualité au même titre que l'accessibilité pour les équipes de design systems, testée systématiquement avant chaque publication plutôt que corrigée après coup.

## Points clés
- Un design system est une fondation : un composant lent y ralentit automatiquement toutes les applications qui l'utilisent, aussi bien optimisé que soit le code applicatif au-dessus.
- Sur 10 systèmes testés, seul Spectrum Web Components exécute des benchmarks de performance automatisés à chaque pull request ; la plupart ne mesurent que la taille du bundle, pas la réactivité réelle des composants.
- Le framework sous-jacent (React, Lit, etc.) n'explique pas les écarts de performance : trois bibliothèques basées sur Lit obtiennent des résultats très différents entre elles.
- Le profilage révèle des causes concrètes : logique de slots en O(n²) dans Stencil/Ionic, absence de virtualisation dans Material UI et UI5, recalculs de layout répétés (« layout thrashing ») dans React Aria, animations CSS coûteuses jouées 100 fois dans Ant Design.
- L'auteur propose des tests de performance automatisés (Playwright + API Long Animation Frames) avec des « budgets de performance » explicites, intégrables en CI/CD.
- Recommandation centrale : rendre le comportement rapide la valeur par défaut (virtualisation automatique, animations limitées à l'élément manipulé) plutôt que de compter sur la vigilance des équipes produit.

## Analyse approfondie
**Le principe de base.** Une application web s'empile en couches : le navigateur, puis un framework (React, Lit...), puis les bibliothèques partagées et le design system de l'entreprise, et enfin le code du produit lui-même. Le thread principal du navigateur étant unique pour exécuter le JavaScript, gérer les événements et dessiner l'écran, tout temps économisé dans les couches basses profite à l'ensemble des applications construites dessus. L'auteur note que les équipes de design systems appliquent déjà ce raisonnement à l'accessibilité (support clavier, rôles ARIA testés avant chaque version), mais rarement à la performance : les composants sont testés isolément, avec peu d'éléments, ce qui masque les problèmes qui n'apparaissent qu'à l'échelle réelle d'une application. Une équipe produit qui ressent une lenteur venant du design system ne peut généralement pas la corriger elle-même — d'où l'argument que la performance doit figurer, au même rang que l'accessibilité, sur la liste des priorités des équipes de design systems.

**Méthodologie.** Dix systèmes ont été retenus (versions testées en octobre 2026), volontairement bâtis sur des bases technologiques variées : Mantine, Ant Design et Material UI (React), React Spectrum (React, via React Aria), Carbon, Web Awesome et Spectrum Web Components (Lit), Fluent (FAST, de Microsoft), UI5 (framework interne SAP) et Ionic (Stencil). Les projets non maintenus activement ont été exclus pour garder la comparaison équitable ; React Spectrum et Spectrum Web Components, bien que partageant le même langage visuel, ont été testés séparément car leurs bases de code diffèrent.

Un premier constat : l'examen des dépôts montre que seul Spectrum Web Components fait tourner un benchmark de performance par composant à chaque pull request ; Fluent en possède aussi mais ne semble pas les exécuter automatiquement. Les autres ne testent pas la performance au niveau composant. Ant Design, Material UI et Fluent surveillent la taille de leur bundle, ce qui est utile pour le temps de chargement mais ne dit rien de la réactivité d'un composant une fois affiché.

Deux scénarios ont été chronométrés, choisis pour leur caractère représentatif de tâches fréquentes dans de vraies applications : ouvrir un sélecteur de pays listant les 249 pays de la norme ISO (comme sur un formulaire de paiement ou d'inscription), et cocher 100 cases simultanément (comme un « tout sélectionner » au-dessus d'une liste de messages). Les tests ont été réalisés avec des builds de production, sous Chrome v155 sur un MacBook Pro M1 Pro, avec un script simulant le clic puis mesurant la durée d'occupation du thread principal (y compris animations), le tout sous un throttling CPU ×4 — équivalent au réglage de limitation du panneau Performance de Chrome, jugé plus représentatif des appareils réels. Chaque test a été exécuté trois fois, la médiane étant retenue. L'auteur a aussi mesuré la plus longue période d'inactivité de l'interface (lorsque le thread principal est bloqué et que la page semble figée) ; Chrome ne signalant que les frames dépassant 50 ms, la mention « moins de 50 ms » est utilisée en l'absence de signalement. Les scripts de test sont publiés dans un dépôt GitHub (« design-system-performance-tests »).

**Résultats — ouverture du sélecteur de pays (du plus rapide au plus lent) :**

| Système | Framework | Temps d'ouverture | Plus longue inactivité |
|---|---|---|---|
| Fluent | FAST | 61 ms | 52 ms |
| Carbon | Lit | 63 ms | Moins de 50 ms |
| Mantine | React | 84 ms | 63 ms |
| Ant Design | React | 134 ms | 69 ms |
| Web Awesome | Lit | 137 ms | 82 ms |
| UI5 | Framework SAP | 157 ms | 106 ms |
| Spectrum Web Components | Lit | 165 ms | 78 ms |
| Material UI | React | 208 ms | 181 ms |
| React Spectrum | React | 227 ms | 162 ms |
| Ionic | Stencil | 1 266 ms | 1 133 ms |

Ionic est plus de cinq fois plus lent que le deuxième plus lent (React Spectrum). En testant Ionic et Fluent avec seulement 50 options, Ionic passe de 203 ms (50 options) à plus de 1,2 s (249 options), alors que Fluent ne varie quasiment pas (41 ms à 61 ms) — signe d'une complexité non linéaire chez Ionic.

**Résultats — sélection de 100 cases à cocher :**

| Système | Framework | Temps de sélection | Plus longue inactivité |
|---|---|---|---|
| Fluent | FAST | 29 ms | Moins de 50 ms |
| Carbon | Lit | 41 ms | Moins de 50 ms |
| Material UI | React | 70 ms | Moins de 50 ms |
| UI5 | Framework SAP | 70 ms | Moins de 50 ms |
| Ionic | Stencil | 104 ms | Moins de 50 ms |
| Web Awesome | Lit | 148 ms | Moins de 50 ms |
| Spectrum Web Components | Lit | 158 ms | Moins de 50 ms |
| Mantine | React | 227 ms | 71 ms |
| React Spectrum | React | 298 ms | 53 ms |
| Ant Design | React | 421 ms | 78 ms |

Ant Design met six fois plus de temps que Material UI, bien que les deux soient construits avec React — preuve que le framework seul ne détermine pas la performance. Aucun système ne bloque longtemps l'interface sur ce test (78 ms maximum, soit environ cinq frames manquées à 60 fps).

Les deux tableaux combinés montrent que l'appartenance à un même framework ne garantit rien : Carbon, Web Awesome et Spectrum Web Components sont tous trois en Lit, mais Spectrum Web Components met plus de deux fois plus de temps que Carbon à ouvrir son sélecteur. Ionic, le plus lent sur le sélecteur de pays, se classe pourtant dans la moyenne sur les cases à cocher — un même système peut donc être lent sur une tâche et rapide sur une autre.

**Diagnostic par profilage.** L'auteur a utilisé le panneau Performance de Chrome (onglets Summary et Bottom-Up) pour identifier les causes précises des ralentissements :

- *Ionic/Stencil* : l'essentiel du temps provient d'une version maison de `appendChild` propre au runtime de Stencil, chargée de gérer les « slots » (emplacements où s'insère le contenu d'un composant) lorsque le composant n'utilise pas le Shadow DOM natif — c'est le cas du groupe de boutons radio `ion-radio-group` du sélecteur de pays. Pour chaque nouvelle option ajoutée, Stencil doit parcourir trois fois l'ensemble des options déjà présentes (recherche du bon emplacement, positionnement, vérification du contenu de repli du slot), ce qui donne une complexité quadratique : ajouter la 249ᵉ option implique de revérifier les 248 précédentes, contre seulement 9 pour la 10ᵉ. Ce comportement est piloté par les réglages `appendChildSlotFix` et `experimentalSlotFixes`, actuellement désactivés par défaut mais que la documentation de Stencil prévoit d'activer par défaut dans la future version 5 — ce qui affecterait alors tout composant Stencil utilisant des slots sans Shadow DOM. L'auteur propose deux correctifs : faire utiliser le Shadow DOM natif par `ion-radio-group` (ce qui reporterait la gestion des slots au navigateur), ou modifier Stencil pour ne vérifier le contenu de repli que du slot modifié. Un test réalisé en retirant cette troisième vérification a montré un gain de vitesse d'un facteur sept sur l'ajout de 2000 éléments. Ces problèmes ont été signalés aux équipes Ionic et Stencil.
- *Material UI vs Ant Design* : en comptant les éléments DOM avant/après ouverture (`document.querySelectorAll("*").length`), Material UI ajoute environ 250 éléments (un par option) alors qu'Ant Design n'en ajoute qu'environ 40, car il virtualise sa liste — il ne rend que les options visibles et en charge davantage au défilement. D'où sa plus grande rapidité. L'auteur souligne que la virtualisation exige une attention particulière pour le clavier et les lecteurs d'écran (seuls les éléments visibles existent réellement dans le DOM) ; Ant Design gère cela en conservant une copie cachée de l'option en surbrillance, accessible aux lecteurs d'écran.
- *UI5* : le temps est dominé par le calcul de styles (« Rendering »), pas par le JavaScript. Les 249 options sont déjà présentes dans le DOM, dans un popover masqué ; le navigateur ne calcule pas les styles des éléments cachés, donc à l'ouverture il doit soudain styliser environ 1 500 éléments (chaque option ayant son propre Shadow DOM). Une virtualisation à la manière d'Ant Design réduirait fortement ce nombre.
- *React Spectrum* : bien que virtualisé, il reste le deuxième plus lent. Réduire de moitié le nombre d'options ne change presque rien au temps d'ouverture, ce qui écarte la taille de la liste comme cause. Le profilage pointe la fonction navigateur `checkVisibility`, appelée par React Aria (la bibliothèque sous-jacente) : à chaque ouverture, React Aria parcourt les options visibles une par une, vérifie leur visibilité, réinitialise leur hauteur puis mesure leur taille — chaque étape forçant un recalcul de layout. C'est un cas classique de « layout thrashing ». L'auteur suggère de regrouper toutes les réinitialisations de hauteur avant de mesurer, pour ne forcer qu'un seul recalcul de layout global ; un ticket a été ouvert auprès de l'équipe React Aria.
- *Ant Design (cases à cocher)* : l'exécution JavaScript représente moins d'un tiers du temps total ; le reste vient du calcul de styles et du dessin de l'animation de chaque case, répétée 100 fois. En désactivant les animations via CSS (`transition`/`animation: none`), la sélection des 100 cases devient trois fois plus rapide. L'auteur relativise : il ne s'agit pas de supprimer les animations, mais de les rendre moins coûteuses — par exemple faire varier l'opacité d'un calque plein plutôt que la couleur de fond/bordure, ce qui permet au navigateur d'exécuter l'animation sur le thread de composition plutôt que sur le thread principal, laissant ce dernier libre même pendant l'animation.

**Vers des tests de performance automatisés.** L'auteur propose des tests Playwright reproductibles (illustrés avec un design system fictif nommé « Nettle »), mesurant via la métrique Chrome `TaskDuration` le temps d'occupation du thread principal avant/après une interaction, combinés à l'API Long Animation Frames (LoAF) qui signale toute frame de dessin dépassant 50 ms. Il recommande de fixer des « budgets de performance » : par exemple 100 ms maximum d'inactivité de l'interface (seuil où une réponse cesse de paraître instantanée) et 300 ms pour le temps total d'une interaction animée. Un second test compare le temps d'ouverture avec le nombre d'options complet contre la moitié : le temps ne devrait pas plus que doubler ; seul Ionic échoue nettement à ce test (quasiment triplé), ce qui en fait, selon l'auteur, le test le plus révélateur à exécuter si l'on ne peut en choisir qu'un seul, car il détecte directement une complexité non linéaire sans dépendre des caractéristiques de la machine de test.

**Recommandations générales.** Au-delà des tests, l'auteur insiste sur l'idée de rendre le comportement rapide la valeur par défaut : par exemple basculer automatiquement vers la virtualisation lorsqu'une liste dépasse un certain budget, ou ne jouer l'animation d'une case à cocher que lorsqu'elle est sélectionnée individuellement — les équipes produit héritent alors de la rapidité sans avoir à en connaître la cause. Il suggère aussi de documenter les limites testées (« ce menu déroulant est testé jusqu'à 500 options, au-delà préférez une saisie avec autocomplétion »), et de publier des mesures avant/après dans les notes de version, au même titre que les annonces d'amélioration d'accessibilité. Il recommande enfin de s'appuyer sur de vraies pages d'application riches en composants, en demandant régulièrement aux équipes produit un enregistrement du panneau Performance des DevTools ; en React, les builds de développement incluent une piste « Components » montrant le temps de rendu par composant (visible aussi en production via le composant `<Profiler>`), fonctionnalité qui n'existe pas nativement pour les Web Components — l'auteur annonce vouloir traiter ce point dans un prochain article.

**Conclusion.** Un design system est une fondation, au même titre que le navigateur lui-même ; de même que les fabricants de navigateurs mesurent la performance avant chaque sortie, les équipes de design systems devraient faire de même. C'est l'idée du « Fast by Default » : intégrer la performance dès la conception plutôt que de la corriger après coup, sous la pression des utilisateurs. L'article renvoie vers le livre de l'auteur, *Fast by Default: Practical Performance Engineering* (Manning, en accès anticipé), qui étend cette approche au backend et au mobile et détaille la mise en place de budgets de performance vérifiés à chaque pull request.

## Pourquoi ça compte
Cet article propose une méthodologie concrète et reproductible (benchmarks Playwright, budgets de performance, profilage ciblé) pour traiter la performance comme un critère de qualité systématique dans les design systems, un sujet souvent négligé face à l'accessibilité ou à la taille des bundles — pertinent pour toute équipe plateforme ou toute veille sur l'ingénierie frontend à grande échelle.
