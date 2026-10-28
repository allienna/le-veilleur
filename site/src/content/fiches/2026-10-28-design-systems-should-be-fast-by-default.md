---
title: "Design Systems Should Be Fast by Default"
date: 2026-10-28
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fdenodell.com%2Fblog%2Fdesign-systems-should-be-fast-by-default%3Futm_source=tldrdev/1/010001a17d110e42-40976455-dae4-40f7-b116-848fc7e8a288-000000/svDoFDImwxl2_pvGMoL7jO6f3TlgtKNY820d1G440Mc=452"
keywords: ["performance web", "design systems", "virtualisation DOM", "Stencil", "benchmarking frontend", "budgets de performance"]
theme: "Software"
tone: "research"
used_in: ["2026-10-28"]
---

## Résumé

L'auteur soutient que la performance devrait être une priorité des équipes de design systems au même titre que l'accessibilité, car toute lenteur dans un composant partagé (menu déroulant, case à cocher, etc.) se répercute sur toutes les applications qui l'utilisent. Pour étayer ce constat, il a testé en octobre 2026 dix design systems open source populaires (Mantine, Ant Design, Material UI, React Spectrum, Carbon, Fluent, Web Awesome, UI5, Spectrum Web Components, Ionic) sur deux tâches réalistes : ouvrir un sélecteur de pays à 249 options et cocher 100 cases à la fois. Les résultats varient énormément — jusqu'à un facteur 20 entre le plus rapide et le plus lent — et ne dépendent pas uniquement du framework sous-jacent, puisque des bibliothèques construites avec le même socle (Lit, React) affichent des écarts considérables. L'article détaille, pour chaque cas problématique, la cause technique précise (gestion des slots par Stencil, absence de virtualisation, calculs de style en masse, layout thrashing, animations superflues) et propose des correctifs concrets, avant de présenter une méthode de test de performance reproductible (Playwright + API Long Animation Frames) à intégrer en intégration continue.

## Points clés

- Sur l'ouverture d'un sélecteur de 249 pays, les temps varient de 61 ms (Fluent) à plus de 1 266 ms (Ionic), soit un facteur supérieur à 20 ; sur la sélection de 100 cases, Ant Design (421 ms) est six fois plus lent que Material UI (70 ms), pourtant toutes deux construites en React.
- Le framework utilisé n'explique pas tout : parmi les composants basés sur Lit, Carbon (63 ms) est plus de deux fois plus rapide que Spectrum Web Components (165 ms) sur la même tâche.
- Chez Ionic, l'option expérimentale `appendChildSlotFix` de Stencil provoque une vérification répétée de toutes les options déjà ajoutées à chaque nouvel élément inséré dans un slot sans shadow DOM, ce qui rend le temps d'ajout quadratique ; Stencil prévoit de rendre ce réglage actif par défaut dans sa v5.
- La virtualisation (ne rendre dans le DOM que les éléments visibles, comme le fait Ant Design) réduit nettement le nombre d'éléments à styliser, contrairement à UI5 qui insère les 249 options cachées dans le DOM puis doit calculer leurs styles d'un coup à l'ouverture.
- React Spectrum souffre de « layout thrashing » : React Aria mesure la taille de chaque option une par une, forçant le navigateur à recalculer la mise en page à chaque itération au lieu de regrouper les lectures et écritures.
- L'auteur propose une suite de tests de performance (Playwright + API Long Animation Frames, avec des « budgets de performance » chiffrés) à exécuter automatiquement sur chaque pull request, ainsi que des recommandations organisationnelles (rendre le comportement rapide la valeur par défaut, documenter les limites testées, profiler les vraies pages d'applications).

## Analyse approfondie

**Le principe : la performance comme fondation partagée**
Les applications web sont construites en couches : le navigateur, puis un framework (React, Lit…), puis les bibliothèques internes et le design system de l'entreprise, et enfin le code du produit lui-même. Comme le thread principal du navigateur est unique pour exécuter le JavaScript, répondre aux événements et dessiner l'écran, toute lenteur introduite dans les couches basses prive les couches supérieures de marge de manœuvre : si un composant `<select>` d'un design system met une seconde à s'ouvrir, aucune application qui l'utilise ne pourra être plus rapide sur ce point, quelle que soit la qualité du reste de son code. À l'inverse, une optimisation faite une fois au niveau du design system profite instantanément à toutes les applications qui en dépendent. Les équipes de design systems appliquent déjà ce raisonnement à l'accessibilité (support clavier, rôles ARIA testés avant chaque publication) ; l'auteur plaide pour que la performance reçoive la même attention — tester chaque composant avec des volumes de données réalistes et exigeants avant publication, et s'assurer que les performances ne se dégradent pas silencieusement avec le temps.

**Méthodologie de test**
L'auteur a sélectionné dix design systems open source actifs, en veillant à varier les frameworks sous-jacents (React pour Mantine, Ant Design, Material UI, React Spectrum ; Lit pour Carbon, Web Awesome, Spectrum Web Components ; FAST de Microsoft pour Fluent ; framework interne de SAP pour UI5 ; Stencil pour Ionic). Il a volontairement conservé React Spectrum et Spectrum Web Components, qui partagent le même langage visuel mais des bases de code distinctes, pour vérifier si leurs performances convergent.

Il a d'abord vérifié si ces projets disposaient de tests de performance automatisés au niveau composant : seul Spectrum Web Components en exécute à chaque pull request ; Fluent en possède mais ne semble pas les lancer automatiquement ; les autres n'en ont pas. Plusieurs (Ant Design, Material UI, Fluent) surveillent en revanche la taille de leur bundle, ce qui est utile pour le temps de chargement mais ne renseigne rien sur la réactivité d'un composant une fois affiché.

Deux tâches représentatives ont servi de base de comparaison : ouvrir un sélecteur listant les 249 pays de la norme ISO (cas typique d'un formulaire de paiement ou d'inscription), et cocher 100 cases d'un coup (cas typique d'un « tout sélectionner » dans une messagerie). Les tests ont été exécutés sur des builds de production, avec Chrome 155 sur un MacBook Pro M1 Pro, le CPU étant ralenti d'un facteur 4 (équivalent au throttling du panneau Performance de Chrome, recommandé pour approcher le ressenti d'un utilisateur réel). Chaque test a été répété trois fois et la médiane retenue. En plus du temps total d'exécution sur le thread principal (incluant les animations), l'auteur a mesuré la plus longue période d'indisponibilité de l'interface — moment où le thread principal est bloqué et où le navigateur ne peut ni redessiner l'écran ni répondre aux événements ; Chrome ne signalant que les frames dépassant 50 ms, les cas en dessous sont notés « Under 50ms ». L'ensemble des scripts de test est publié dans un dépôt GitHub nommé *design-system-performance-tests*.

**Résultats — ouverture du sélecteur de pays (249 options), du plus rapide au plus lent**

| Design system | Framework | Temps d'ouverture | Plus longue indisponibilité |
|---|---|---|---|
| Fluent | FAST | 61 ms | 52 ms |
| Carbon | Lit | 63 ms | Under 50ms |
| Mantine | React | 84 ms | 63 ms |
| Ant Design | React | 134 ms | 69 ms |
| Web Awesome | Lit | 137 ms | 82 ms |
| UI5 | Framework SAP | 157 ms | 106 ms |
| Spectrum Web Components | Lit | 165 ms | 78 ms |
| Material UI | React | 208 ms | 181 ms |
| React Spectrum | React | 227 ms | 162 ms |
| Ionic | Stencil | 1 266 ms | 1 133 ms |

Fluent et Carbon se détachent nettement, tandis qu'Ionic est plus de cinq fois plus lent que le second plus lent (React Spectrum). En répétant le test avec seulement 50 options, Ionic passe de 1 266 ms à 203 ms tandis que Fluent ne bouge presque pas (41 ms à 61 ms) : la dégradation d'Ionic n'est donc pas linéaire avec la taille de la liste.

**Résultats — sélection de 100 cases à cocher**

| Design system | Framework | Temps de sélection | Plus longue indisponibilité |
|---|---|---|---|
| Fluent | FAST | 29 ms | Under 50ms |
| Carbon | Lit | 41 ms | Under 50ms |
| Material UI | React | 70 ms | Under 50ms |
| UI5 | Framework SAP | 70 ms | Under 50ms |
| Ionic | Stencil | 104 ms | Under 50ms |
| Web Awesome | Lit | 148 ms | Under 50ms |
| Spectrum Web Components | Lit | 158 ms | Under 50ms |
| Mantine | React | 227 ms | 71 ms |
| React Spectrum | React | 298 ms | 53 ms |
| Ant Design | React | 421 ms | 78 ms |

Ant Design met six fois plus de temps que Material UI, bien que les deux soient construits en React. Aucun des dix ne bloque l'interface longtemps sur cette tâche (78 ms maximum, soit environ cinq frames manquées à 60 fps) — un résultat globalement plus rassurant que pour le sélecteur de pays.

Les deux tableaux montrent que le framework seul ne détermine pas la performance : parmi les trois design systems basés sur Lit (Carbon, Web Awesome, Spectrum Web Components), les écarts sont importants, et Ionic, pourtant le plus lent sur le sélecteur de pays, se classe dans la moyenne sur les cases à cocher — un même design system peut donc être lent sur une tâche et rapide sur une autre.

**Diagnostic détaillé via le panneau Performance de Chrome**

*Ionic / Stencil* : le temps d'ouverture augmente plus vite que proportionnellement au nombre d'options, ce qui indique que chaque nouvelle option coûte plus cher à ajouter que la précédente. L'analyse du profil montre qu'une version personnalisée de `appendChild`, issue du runtime de Stencil, consomme environ la moitié du temps total. Cette fonction fait partie de la gestion des *slots* par Stencil : un slot est l'emplacement où un composant web affiche son contenu, par exemple les options placées à l'intérieur d'une liste déroulante. Normalement, les slots sont gérés nativement par le navigateur via le shadow DOM. Mais le composant `ion-radio-group` d'Ionic n'utilise pas de shadow DOM, ce qui oblige Stencil à simuler lui-même le comportement des slots en remplaçant `appendChild` et `insertBefore`. Pour localiser chaque nouvelle option, Stencil parcourt l'ensemble des options déjà présentes, les reparcourt pour déterminer où insérer la nouvelle, puis les reparcourt une troisième fois pour savoir si le contenu de repli du slot doit être affiché. Ajouter la 249ᵉ option implique donc de revérifier trois fois les 248 précédentes, contre seulement 9 pour la 10ᵉ — d'où la dégradation observée. Ce comportement est activé par le réglage `appendChildSlotFix`, lui-même contrôlé par l'option `experimentalSlotFixes` de Stencil ; ces deux réglages sont actuellement désactivés par défaut, mais la documentation de Stencil indique qu'ils devraient devenir actifs par défaut dans la version 5, ce qui affecterait tout composant utilisant des slots sans shadow DOM. Deux correctifs sont proposés : faire en sorte qu'`ion-radio-group` utilise le shadow DOM (le navigateur reprendrait alors la gestion native des slots, au prix d'un changement de style potentiellement incompatible, donc à réserver à une version majeure), ou corriger Stencil lui-même en ne vérifiant le contenu de repli que du slot modifié, et en ignorant cette vérification si le slot contient déjà des options. En testant cette seconde piste sur une copie modifiée de Stencil avec 2 000 éléments ajoutés un par un, l'ajout s'est révélé environ sept fois plus rapide. L'auteur indique avoir signalé le problème aux équipes d'Ionic et de Stencil.

*Material UI vs Ant Design* : en comptant les éléments du DOM avant/après ouverture du sélecteur (`document.querySelectorAll("*").length`), Material UI ajoute environ 250 éléments (un par option) alors qu'Ant Design n'en ajoute qu'environ 40, car son menu ne rend que les options visibles à l'écran et en charge davantage au défilement — une forme de virtualisation qui explique son ouverture plus rapide. L'auteur souligne que la virtualisation exige néanmoins une attention particulière pour le clavier et les lecteurs d'écran, puisque seules les options affichées existent réellement dans le DOM ; Ant Design gère ce point en conservant une copie cachée de l'option en surbrillance, afin que les lecteurs d'écran puissent tout de même l'annoncer.

*UI5* : dans ce cas, c'est la phase de rendu (calcul des styles et de la mise en page) qui domine le temps total, bien plus que l'exécution du JavaScript. L'inspection du DOM révèle que les 249 options sont déjà présentes, mais cachées dans un popover, avant même l'ouverture du menu. Le navigateur ne calcule pas les styles des éléments cachés ; dès que le popover s'ouvre, il doit donc styliser d'un coup environ 1 500 éléments (chaque option possédant son propre shadow DOM avec plusieurs sous-éléments). Virtualiser la liste, comme le fait Ant Design, réduirait fortement ce nombre.

*React Spectrum* : bien qu'il utilise lui aussi la virtualisation, ce composant reste le deuxième plus lent, et sa lenteur ne dépend pas de la longueur de la liste (même durée avec moitié moins d'options). Le profilage révèle un appel répété à la fonction native `checkVisibility`, invoquée par React Aria (la bibliothèque sur laquelle repose React Spectrum) : à chaque ouverture, React Aria parcourt une à une les options visibles, vérifie leur visibilité, réinitialise leur hauteur puis mesure leur taille — chacune de ces étapes forçant le navigateur à recalculer la mise en page, un phénomène appelé *layout thrashing*. Tout cela se produit immédiatement après le clic, bloquant l'interface jusqu'à la fin du calcul. Le correctif suggéré consiste à regrouper les opérations : réinitialiser toutes les hauteurs d'abord, puis vérifier et mesurer toutes les options ensuite, afin que le navigateur ne recalcule la mise en page qu'une seule fois. L'auteur a signalé ce point à l'équipe React Aria.

*Ant Design — cases à cocher* : l'exécution du JavaScript représente moins d'un tiers du temps total nécessaire pour cocher les 100 cases ; le reste provient du calcul des styles et du dessin de l'animation de chaque case, répété 100 fois. En désactivant les animations (transitions et animations CSS mises à `none`), le temps total chute à moins d'un tiers de sa valeur initiale, supprimant presque tout le travail de style et de dessin ainsi qu'une partie du JavaScript lié aux animations. Or l'utilité de l'animation (utile quand on coche une seule case) disparaît lorsque 100 cases changent d'état simultanément. Deux pistes de correction : n'animer une case que lorsqu'elle est cochée directement par l'utilisateur, ou désactiver les animations avant d'exécuter la logique d'un « tout sélectionner ».

*Remarque générale sur les animations* : il ne s'agit pas de supprimer les animations, mais de les rendre moins coûteuses pour le thread principal. Les cases d'Ant Design animent un changement de couleur de fond et de bordure, ce qui oblige le navigateur à repeindre l'élément sur le thread principal à chaque frame. Faire varier l'opacité d'un calque déjà rempli produit un effet similaire tout en pouvant être exécuté sur le *thread de composition* — un thread séparé qui assemble les éléments déjà dessinés par le thread principal et peut donc animer indépendamment, même si ce dernier est occupé.

**Vers des tests de performance automatisés**

La plupart des tests de composants se contentent de rendre une seule instance avec quelques props, ce qui valide le fonctionnement mais ne révèle rien sur la vitesse réelle avec 249 options ou 100 cases cochées simultanément. L'auteur propose donc des tests de performance qui reproduisent un usage réaliste puis mesurent le temps de réponse de la page à une interaction, à l'aide de Playwright. Son dépôt d'exemple introduit ces tests pour un design system fictif appelé « Nettle », reproduits ensuite sur les dix design systems testés, avec une page de test paramétrable par URL (par exemple `?n=249`). Le temps mesuré provient de la métrique Chrome `TaskDuration`, qui cumule le temps d'occupation du thread principal ; en soustrayant la valeur avant clic de celle après clic, on obtient le coût total de l'interaction (JavaScript, rendu, dessin). Avec un CPU ralenti d'un facteur 4, seul le sélecteur de pays d'Ionic dépasse la limite de 300 ms fixée pour ce premier test, avec 249 options.

L'auteur insiste sur l'importance de détecter non seulement la durée totale, mais aussi les blocages ponctuels longs : une seule pause bloquante est perçue comme pire par l'utilisateur que plusieurs pauses courtes de même durée cumulée. C'est le cas comparé de Spectrum Web Components (plusieurs petites pauses) et UI5 (un seul blocage long dû au calcul de style massif), bien que les deux totalisent un temps similaire. D'où l'usage complémentaire de l'API *Long Animation Frames* (LoAF), qui signale toute frame dépassant 50 ms de dessin ; le test échoue si une frame atteint 100 ms ou plus. Avec 249 options, les sélecteurs d'Ionic, Material UI, React Spectrum et UI5 échouent à ce contrôle, Ionic échouant même avec seulement 50 options.

Chaque seuil ainsi fixé constitue un *budget de performance* : la durée maximale tolérée avant qu'un test échoue. L'auteur retient 100 ms comme budget pour une interruption de réactivité (seuil approximatif où une réponse cesse de paraître instantanée), et 300 ms pour le temps total du premier test (qui inclut l'animation d'ouverture du menu). Il recommande de fixer ses propres budgets en mesurant d'abord ses composants actuels, puis en réglant le seuil légèrement au-dessus, afin que le test échoue si une future modification ralentit le composant.

Un second test compare le temps d'ouverture avec 250 options à celui avec moitié moins (125) : la liste complète ne devrait pas prendre plus du double du temps de la liste réduite. Tous les sélecteurs sauf celui d'Ionic passent ce test aisément (bien en dessous du double), tandis qu'Ionic met près de trois fois plus de temps et échoue. L'auteur considère ce second test comme le plus précieux s'il ne devait en garder qu'un seul, car il détecte directement une dégradation non linéaire (chaque option plus coûteuse que la précédente) sans nécessiter d'ajuster le budget selon la machine utilisée.

L'auteur note que Spectrum Web Components dispose déjà d'un test automatisé proche du sien (249 pays), mais celui-ci ne mesure que le temps de rendu du menu fermé, pas le temps nécessaire pour l'ouvrir après un clic utilisateur.

Ces principes de test s'appliquent à d'autres types de composants : les tests de type « sélecteur de pays » conviennent à toute liste longue (menu, tableau), et le test des cases à cocher à tout élément répété de nombreuses fois sur une page (icônes, boutons). Exécutés automatiquement sur chaque pull request (par exemple via GitHub Actions), ils permettent de détecter immédiatement l'impact d'un changement sur la performance d'un composant. Le dépôt GitHub (`design-system-performance-tests`) contient un dossier par design system testé, un README expliquant comment l'adapter à son propre design system, et un workflow GitHub Actions prêt à l'emploi.

**Recommandations organisationnelles**

Au-delà des tests, l'auteur recommande de rendre le comportement performant la valeur par défaut d'un composant : un menu déroulant pourrait basculer automatiquement vers la virtualisation dès que sa liste dépasse son budget de performance, et une case à cocher ne s'animer que lorsqu'elle est sélectionnée individuellement — les équipes applicatives bénéficieraient alors de la version rapide sans même avoir eu connaissance du problème initial.

Il suggère également de documenter, dans la documentation du design system, le nombre d'éléments avec lequel chaque composant a été testé (par exemple : « le menu est testé jusqu'à 500 options ; au-delà, une saisie avec autocomplétion est préférable »), en augmentant progressivement ce nombre dans les tests jusqu'à dépasser le budget fixé. Cela indique aux équipes applicatives jusqu'où elles peuvent utiliser un composant avant qu'il ne devienne lent, et fixe également la portée nécessaire des futurs tests.

Les pages réelles d'applications qui utilisent massivement les composants du design system restent le meilleur indicateur de ce qu'il faut corriger en priorité, car elles révèlent l'usage réel. En demandant régulièrement aux équipes applicatives d'enregistrer un profil via le panneau Performance des DevTools pendant l'utilisation de ces pages, l'équipe du design system peut identifier quels composants pèsent sur la performance. Les builds de développement de React ajoutent à ces profils une piste « Components » montrant le temps de rendu de chaque composant (visible uniquement pour les parties de l'application enveloppées dans le composant `<Profiler>` de React en version profiling) ; les composants web n'ont pas d'équivalent — l'auteur annonce traiter ce point dans un prochain article.

Enfin, il recommande de documenter chaque gain de performance dans les notes de version, avec des mesures avant/après (par exemple : « le menu s'ouvre désormais en 150 ms avec 500 options, contre 300 ms auparavant »), afin que les équipes applicatives puissent vérifier concrètement l'amélioration dans leurs propres applications — de la même manière qu'une mention comme « les lecteurs d'écran annoncent désormais l'option sélectionnée » documente un progrès d'accessibilité.

**Conclusion**

Un design system constitue le socle des applications qui s'appuient sur lui, de la même façon que le navigateur est le socle du design system. Les éditeurs de navigateurs mesurent systématiquement la performance avant chaque publication ; l'auteur appelle à appliquer la même discipline aux design systems. C'est le principe du « Fast by Default » : intégrer la performance dès la conception plutôt que de la corriger après coup, une fois que les utilisateurs se sont plaints. L'article se conclut par la mention du livre de l'auteur, *Fast by Default: Practical Performance Engineering*, qui approfondit cette approche pour le backend et le mobile en plus du web, et détaille la mise en place de budgets de performance vérifiés à chaque pull request ; l'ouvrage est disponible en accès anticipé chez Manning.

## Pourquoi ça compte

Cet article fournit une méthodologie concrète et reproductible (benchmarks chiffrés, profiling, tests Playwright, budgets de performance) pour auditer et fiabiliser la performance des design systems, un sujet souvent relégué derrière l'accessibilité ou la taille des bundles malgré son impact direct sur toutes les applications en aval — particulièrement utile pour une veille sur les pratiques d'ingénierie frontend à grande échelle.
