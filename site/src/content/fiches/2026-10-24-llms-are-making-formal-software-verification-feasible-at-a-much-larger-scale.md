---
title: "LLMs are making formal software verification feasible at a much larger scale"
date: 2026-10-24
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.anthropic.com%2Fresearch%2Fformal-verification%3Futm_source=tldrnewsletter/1/010001a168518b71-b1d1fbc8-3da4-413f-98b9-c081bac26d89-000000/3O9nxYZAnuxe9-P24JfYER1xDzwY2ov5Lb4k4jJdeXM=452"
authors: ["Keane Lucas", "Aengus Lynch", "Luna Tong", "Luke Champine", "Zygi Straznickas", "Dino Distefano", "Harshikaa Agrawal", "Evyatar Ben Asher", "Ava Howell", "Sami Jawhar", "Chris Rohlf", "Nickolai Zeldovich", "Nicholas Carlini", "Rajashree Agrawal", "Jason Gross"]
keywords: ["vérification formelle", "Claude", "sécurité logicielle", "preuves mathématiques", "bugs logiciels", "RISC-V"]
theme: "Sécurité"
tone: "research"
used_in: ["2026-10-24"]
---

## Résumé

Anthropic, en collaboration avec la société Theorem, montre que les LLM (via Claude) rendent la vérification formelle de logiciels praticable à grande échelle, une discipline historiquement réservée à de rares projets critiques en raison de son coût humain exorbitant. En transformant les tests de fuzzing existants de 123 bibliothèques open source en spécifications mathématiques, Claude a produit des preuves formelles au niveau du code assembleur (RISC-V) démontrant l'absence de crash sur 239 points d'entrée, tout en découvrant et corrigeant au passage des bugs invisibles depuis des années malgré des milliards de tests. L'article détaille la méthode (transformation de fuzz tests en specs), présente d'autres études de cas (zlib, un interpréteur Python en Rust, un lecteur PDF) et discute des gains d'efficacité obtenus avec les modèles récents ainsi que des limites actuelles de l'approche.

## Points clés

- Claude a produit, avec Theorem, des preuves formelles au niveau du binaire RISC-V pour 239 points d'entrée de fuzzing répartis sur 123 bibliothèques open source du projet OSS-Fuzz de Google — une première à cette échelle pour du code de production au niveau assembleur.
- La méthode consiste à convertir un test de fuzzing existant en spécification formelle (« ce test ne plante jamais »), puis à faire démontrer cette propriété par Claude plutôt que de continuer à fuzzer indéfiniment sans garantie d'exhaustivité.
- Au cours du processus, Claude a détecté et corrigé des bugs réels passés inaperçus pendant des années (dépassements de tampon, lectures hors limites, une redécouverte d'une CVE dans libexpat, des bugs logiques sans crash), souvent sur des entrées trop volumineuses ou trop spécifiques pour qu'un fuzzer les trouve seul.
- Les nouveaux modèles réduisent nettement le coût : Opus 5.5 résout la moitié d'un lot de tâches de vérification avec environ 40 % de tokens en moins qu'Opus 5, et le partage de preuves entre agents réduit la consommation de tokens de 17 %.
- D'autres expérimentations (spec formelle de zlib, interpréteur Python en Rust vérifié avec Verus, audit d'un lecteur PDF) confirment la polyvalence de l'approche, tout en révélant quelques bugs mineurs supplémentaires.
- Les auteurs reconnaissent des limites importantes : « formellement vérifié » ne veut pas dire « sans bug », car la preuve ne garantit la conformité qu'à une spécification et à un modèle de machine qui peuvent eux-mêmes diverger de la réalité (architecture, bibliothèque C, usage par l'appelant).

## Analyse approfondie

### Introduction

Même les logiciels matures et intensément testés contiennent des bugs, et les LLM deviennent de plus en plus capables d'en trouver — le noyau Linux, pourtant l'un des logiciels les plus testés au monde, a récemment vu plus de 1 000 vulnérabilités divulguées. Face à des modèles de plus en plus capables d'enchaîner des bugs anodins en exploits critiques, il devient nécessaire de détecter et corriger ces failles avant qu'elles ne soient exploitées. L'idéal serait de pouvoir trouver et corriger tous les bugs, puis de prouver qu'il n'en reste plus : c'est l'objet de la vérification formelle, qui consiste à traduire un programme en modèle mathématique puis à démontrer qu'il respecte toujours un ensemble de règles de sécurité données. Un échec de preuve révèle l'existence potentielle d'un bug et oriente vers sa nature ; répéter le processus en éliminant chaque cause d'échec permet in fine d'obtenir la preuve que le code ne viole aucune des règles visées.

Mais la vérification formelle est difficile : les preuves peuvent être bien plus volumineuses que le code lui-même et exigent une expertise rare. Il a par exemple fallu deux années-personnes pour écrire le noyau de système d'exploitation seL4, mais vingt années-personnes pour le vérifier formellement. C'est pourquoi cette approche n'était jusqu'ici viable que pour des applications réellement critiques, comme le code avionique d'Airbus.

Les LLM changent la donne : les modèles de pointe peuvent désormais produire de façon autonome des preuves de correction pour du logiciel réel. Pour le démontrer, Claude a été chargé de prouver des propriétés de sécurité utiles sur 123 bibliothèques open source, notamment que certains de leurs exécutables ne peuvent jamais planter dans certaines conditions. Concrètement, Claude a prouvé que ces programmes se terminent toujours normalement, sans erreur de sécurité mémoire ni échec d'assertion, pour toute entrée inférieure à 64 Mo et toute réponse modélisée du système Linux, sous certaines hypothèses (programme statique mono-thread à budget mémoire fixe sur un CPU RISC-V sous Linux). On est encore loin d'éliminer tous les bugs possibles, mais c'est une avancée significative qui trace une voie vers cet objectif.

Une partie de ces preuves est publiée afin que chacun puisse les vérifier et les réutiliser, de même que la sémantique RISC-V et OS sous-jacente. Theorem, partenaire du projet, propose d'appliquer le même pipeline à d'autres projets open source et publie une compétence (« skill ») Claude pour aider les développeurs à démarrer la vérification de leur propre code.

La vérification formelle est un domaine vaste ; l'article décrit aussi d'autres explorations utilisant différentes méthodes formelles pour accélérer des tâches de sécurité ou de développement, comme l'évaluation de la sécurité de l'algorithme de compression zlib, la preuve d'équivalence comportementale d'un interpréteur Python écrit en Rust, et la détection de bugs anciens dans des logiciels critiques.

Les perspectives sont jugées prometteuses : le coût d'écriture des preuves diminue à mesure que les modèles progressent, et la réutilisation des preuves entre bases de code amortira encore ce coût à mesure que davantage de code sera formalisé. Les auteurs encouragent tous les développeurs à explorer la vérification formelle assistée par LLM, y compris ceux qui l'avaient essayée sans succès avec des modèles moins capables.

### Transformer les tests en preuves

Prouver qu'un logiciel est correct suppose d'abord de définir ce que « correct » signifie, via une spécification. Pour certains programmes (un décodeur PNG suivant la RFC 2083, par exemple), la spécification est claire. Pour la plupart des logiciels (un éditeur de texte, un navigateur), c'est beaucoup moins évident, et l'obtention d'une spécification complète et non ambiguë constitue un obstacle majeur à la vérification à grande échelle.

Pour contourner ce problème sur les bibliothèques open source visées, l'équipe convertit automatiquement les suites de tests compilables déjà existantes en spécification, en encodant la règle « cette suite de tests passe toujours », à l'aide d'un modèle général de ce que signifie exécuter un binaire compilé en RISC-V sous Linux. Historiquement, prouver de telles spécifications était hors de portée tant il est complexe d'écrire une preuve couvrant tous les comportements possibles de dizaines de milliers d'instructions assembleur pour n'importe quelle entrée (d'où des preuves énormes). C'est précisément le type de tâche où les LLM excellent : parcourir des millions de lignes de code vers un objectif bien défini.

Le point de départ a été les tests de fuzzing : les développeurs définissent un point d'entrée dans leur code qui prend des entrées, de sorte que toute entrée provoquant un crash révèle un bug ; un moteur de fuzzing génère ensuite d'énormes quantités d'entrées semi-aléatoires et mutées pour tenter de déclencher une faille. Plus le fuzzer tourne longtemps, plus il trouve de bugs, mais ce processus reste par nature un brute-force sans garantie de couvrir tous les chemins de code possibles.

Pour retrouver tous les bugs qu'un test de fuzzing aurait pu révéler, l'équipe a transformé ce test en spécification formelle portant sur les instructions RISC-V compilées : la spécification affirme que le test ne plante jamais pour aucune entrée inférieure à 64 Mo. Si Claude parvient à prouver cette spécification, continuer à fuzzer ce point d'entrée devient superflu puisqu'aucun bug supplémentaire n'y sera trouvé.

Cette méthode a été appliquée à des centaines de projets du programme OSS-Fuzz de Google, qui assure un fuzzing continu pour les projets open source éligibles et instrumente automatiquement les programmes C et C++ avec AddressSanitizer (ASan), lequel déclenche un crash dès qu'une mémoire est mal manipulée — une cause majeure de vulnérabilités. Des spécifications génériques comme la sécurité mémoire s'appliquent à la quasi-totalité des logiciels.

En l'espace de quelques semaines, Claude a corrigé les bugs trouvés puis prouvé l'absence de crash pour toute entrée (jusqu'à 64 Mo) sur 239 points d'entrée répartis sur 123 bibliothèques OSS-Fuzz différentes. Ces preuves portent sur les instructions RISC-V compilées (donc sur les binaires exécutables) et représentent environ 180 millions de lignes de Rocq, une preuve typique atteignant environ 600 000 lignes pour garantir la sécurité de binaires d'une longueur médiane de 18 000 instructions RISC-V. Elles sont construites en traduisant le code assembleur RISC-V en modèle mathématique grâce à la sémantique des instructions RISC-V et des processus Linux développée par Theorem — ce qui signifie que ces preuves supposent actuellement un programme statique mono-thread, à budget mémoire fixe, sur CPU RISC-V sous Linux. Étendre la portée de ces preuves (autres architectures, autres processus du système d'exploitation) est jugé tout à fait réalisable.

Malgré le volume considérable de code de preuve produit, presque aucune relecture manuelle n'est nécessaire : le vérificateur de preuves Rocq garantit que la spécification est bien satisfaite. Les seuls éléments qu'un développeur doit donc faire confiance sont : les modèles formels de RISC-V et des processus Linux, les énoncés exacts des théorèmes prouvés, et le vérificateur de preuves Rocq lui-même.

Cela ne signifie pas que ces bibliothèques sont exemptes de bugs : cela signifie que tout bug restant se situe soit dans les composants de confiance listés ci-dessus, soit hors du champ couvert par la preuve de Claude. Renforcer la fiabilité de ces composants de confiance (Rocq, RISC-V, sémantique Linux) reste une tâche non négligeable, mais bien plus abordable que de déboguer chaque ligne de code couverte par les preuves à grande échelle — d'autant que cette approche peut sécuriser un nombre arbitraire de projets sans faire grossir ces composants de confiance.

Les auteurs encouragent la vérification indépendante de leurs preuves et publient les composants de confiance non encore publics créés pour ce projet, les preuves Rocq complètes de Claude pour les tests de fuzzing n'ayant pas nécessité de correctif, ainsi que les spécifications des tests de fuzzing qu'ils n'ont pas réussi à prouver.

### Trouver et corriger des bugs

Le processus de transformation des tests de fuzzing en spécifications prouvables a, en soi, permis de découvrir des centaines de bugs. Pour éviter que Claude ne doive s'arrêter à chaque bug rencontré, l'équipe lui a laissé la main pour corriger directement le code : la spécification était alors régénérée à partir du code corrigé, et Claude poursuivait la preuve sur cette nouvelle spécification.

Beaucoup des bugs trouvés auraient été très improbables à détecter par un fuzzer classique, qui mute généralement de petites entrées (plafonnées à 1 Mo) et s'appuie sur la couverture de code pour s'orienter. En prouvant un point d'entrée, Claude a ainsi trouvé un dépassement de compteur par le bas dans une copie d'un décompresseur, provoquant une écriture hors limites, mais seulement pour des entrées d'environ 20 Mo présentant une disposition rare et spécifique. D'autres bugs incluent une lecture hors limites dans un décodeur d'image nécessitant une entrée de 64 Mo et plus de 2 Go de mémoire, une lecture hors limites dans une autre bibliothèque nécessitant une séquence particulière d'appels sur deux descripteurs du même fichier, et la redécouverte de la CVE-2026-56132 dans libexpat, qui requiert une entrée profondément imbriquée. Claude a également détecté des bugs logiques ne provoquant aucun crash : en prouvant la sécurité mémoire d'une bibliothèque, il a par exemple remarqué qu'une fonctionnalité censée restreindre les fichiers chargeables par une application n'était pas toujours appliquée.

L'objectif ultime du projet était de prouver qu'il ne restait plus aucun crash à découvrir sur les tests de fuzzing compilés en RISC-V ; mais, comme le montrent ces exemples, la simple tentative de ce processus présente déjà l'avantage de révéler de vrais bugs à corriger, indépendamment de l'atteinte de cet objectif final.

#### Prouver plus que la sécurité mémoire

Prouver qu'un test de fuzzing ne plantera plus jamais est plus significatif qu'il n'y paraît. Il est fréquent que les tests de fuzzing réels vérifient des propriétés de haut niveau — round-trip encodage-décodage, idempotence, lois algébriques, tests différentiels, cohérence interne ou équivalence avec une implémentation de référence. Par exemple, un test de fuzzing pour l'algorithme de compression LZO vérifie que compresser puis décompresser une entrée redonne l'entrée d'origine ; si cette propriété est violée, le programme plante, si bien que prouver l'absence de crash équivaut à prouver la propriété elle-même.

Cela peut même survenir sur des propriétés non explicitement spécifiées par le développeur. Par exemple, pour achever la preuve OSS-Fuzz de cpp-httplib, il a fallu écarter la possibilité d'un dépassement de pile dû à une récursion excessive dans le destructeur de std::set. Cette profondeur de récursion étant bornée par la profondeur maximale d'un arbre, Claude a dû prouver — au niveau du code machine — que l'algorithme de rééquilibrage de l'arbre rouge-noir de libc++ est correctement optimisé pour garder une profondeur bornée de façon logarithmique.

#### Autres études de cas de vérification formelle

La vérification formelle est un domaine vaste, et l'exemple du passage « test de fuzzing vers preuve » n'est qu'une des façons dont les LLM rendent la vérification formelle plus largement utilisable, en appliquant directement les preuves au code machine.

D'autres succès ont été obtenus avec d'autres approches. Claude a par exemple rédigé une spécification formelle de la RFC 1950 définissant le format de compression zlib, puis prouvé que l'implémentation zlib du noyau Linux respecte bien cette spécification — cette fois au niveau du binaire x86, en utilisant une sémantique formelle de l'ISA x86 générée (et fortement testée) par Claude lui-même. Le même exercice a ensuite été répété sur une demi-douzaine d'autres bibliothèques largement utilisées, révélant au passage quelques bugs mineurs (non exploitables) dans des cas limites, en cours de signalement en amont. Deux conclusions en sont tirées : ces bases de code extrêmement testées sont déjà quasiment entièrement correctes, et il est possible de prouver des propriétés de correction de bout en bout sur des bases de code réelles existantes.

Dans une autre expérience, Claude a développé un interpréteur pour un large sous-ensemble de Python écrit en Rust, et prouvé (avec l'outil de vérification Verus pour Rust) qu'il respecte la sémantique de CPython décrite dans un article académique. Cette adhérence a ensuite été mesurée empiriquement sur plus de 1,7 million de programmes Python générés aléatoirement, avec un comportement identique à CPython dans 99,95 % des cas, les différences restantes correspondant à des cas limites connus et sans surprise.

Des bugs ont également été trouvés dans plusieurs applications critiques largement utilisées via des tentatives de vérification formelle de propriétés de sécurité simples : un bug logique inconnu, latent depuis plus d'une décennie, a par exemple été découvert ; et lors d'un effort de vérification d'un lecteur PDF très répandu, autant de bugs de sécurité ont été trouvés en une semaine que ce qui est typiquement signalé en un an. L'annexe de l'article détaille davantage ces travaux.

### Ce n'est que le début

Une limite majeure de la vérification formelle assistée par LLM est que les preuves peuvent nécessiter des centaines de millions de tokens à produire. La maîtrise des coûts est donc essentielle si l'objectif est de rendre ces méthodes accessibles à l'ensemble de l'écosystème logiciel. Plusieurs raisons laissent toutefois espérer une amélioration de l'efficacité.

#### Les modèles récents nécessitent moins de tokens

Sur 36 petites tâches de vérification construites à partir de code réel OSS-Fuzz, Opus 5.5 résout la moitié d'entre elles avec environ 40 % de tokens en moins qu'Opus 5 — une tendance que l'on s'attend à voir se poursuivre à mesure que les modèles seront entraînés sur des tâches de vérification longues.

#### Les preuves peuvent être réutilisées

Lorsque des agents travaillent séparément, ils dupliquent souvent beaucoup d'efforts. Or, comme le logiciel, les preuves se construisent de façon récursive à partir de preuves plus petites — et plus une preuve est petite, plus elle est réutilisable. Pour mesurer cet effet, les agents ont été autorisés à copier les preuves des autres pendant qu'ils travaillaient sur leurs propres cibles ; avec cet espace de travail partagé, ils ont eu besoin de 17 % de tokens en moins qu'en travaillant seuls, certains réussissant même après avoir échoué en solo.

Le même phénomène a été observé à grande échelle durant l'effort de preuve sur OSS-Fuzz : la majeure partie d'une preuve concerne du code présent dans quasiment tous les programmes (notamment l'initialisation du runtime C et d'AddressSanitizer), si bien que des programmes très différents peuvent présenter des preuves largement redondantes. Les équipes d'agents en ont profité en copiant la preuve achevée d'une autre équipe puis en l'adaptant à leur propre programme.

Cette réutilisabilité des preuves est ce qui a permis à Mathlib, une bibliothèque partagée de mathématiques formelles en Lean, d'atteindre près de 300 000 théorèmes soumis par plus de 700 contributeurs, chaque nouvelle preuve s'appuyant sur le corpus existant. Un corpus de preuves comparable a été accumulé au cours de l'effort OSS-Fuzz, et une partie en est publiée (à l'exclusion des preuves susceptibles de révéler un bug non corrigé dans le logiciel open source concerné).

Au-delà de ces expériences initiales, une stratégie est nécessaire pour vérifier l'immense corpus de logiciels déjà existants, en commençant par les dépendances les plus critiques. Comme démontré, cela peut se faire à grande échelle en utilisant des spécifications génériques et en travaillant au niveau du binaire, sans avoir à réécrire des bases de code entières dans un autre langage.

Cette approche facilite également la réutilisation des preuves à l'échelle des paquets logiciels, chaque dépendance n'ayant besoin d'être vérifiée qu'une seule fois. Les dépendances suivant une loi de puissance, prouver même un petit ensemble de bibliothèques partagées rend prouvable une proportion considérable de l'écosystème logiciel. Pour plus de détails, l'article renvoie à la feuille de route de Theorem visant à vérifier l'intégralité de l'écosystème Nix, incluant des infrastructures critiques comme glibc, OpenSSL et cURL.

### Limites

En pratique, la vérification formelle peut parfois en dire moins sur la sécurité réelle du code qu'on ne le souhaiterait.

**« Formellement vérifié » ne signifie pas « sans bug ».** Claude peut écrire une preuve montrant qu'un programme compilé respecte les exigences d'une spécification formelle (vérifiée par un outil externe de vérification de preuves). Mais un vérificateur de preuves ne peut pas garantir que la spécification correspond à la réalité. Pour cela, la spécification doit correctement englober et modéliser tout ce qui concerne la machine réelle sur laquelle le programme vérifié s'exécute, y compris le CPU et le système d'exploitation. Lorsque des bugs apparaissent dans du code vérifié, c'est parce que la spécification, ou la sémantique supposée de la machine, diverge de la réalité. Heureusement, cela indique aussi où chercher les bugs restants, et comment concevoir un système minimisant ces zones encore potentiellement fragiles.

**La machine réelle fait des choses que le modèle ne décrit pas.** Les preuves présentées concernent des binaires RISC-V statiques et mono-thread, liés à musl libc. Or la plupart des utilisateurs exécutent ces bibliothèques sur x86 ou ARM, liées dynamiquement à glibc. Combler cet écart nécessiterait des modèles système se rapprochant davantage des systèmes réellement déployés — par exemple en générant une sémantique précise pour x86.

**L'énoncé prouvé peut ne pas couvrir tout ce qui compte.** L'absence de crash a été prouvée pour toute entrée inférieure à 64 Mo sur de nombreux points d'entrée de fuzzing dans Google OSS-Fuzz, y compris les crashs détectés par ASan. Or ASan ne détecte pas tous les bugs de sécurité mémoire, et tous les points d'entrée de chaque bibliothèque n'ont pas été vérifiés ; même si c'était le cas, la bibliothèque entière ne serait pas couverte (notamment en présence de code mort). De plus, un programme réel peut mal utiliser la bibliothèque et provoquer une corruption mémoire côté appelant. Combler cet écart nécessiterait de spécifier ce que chaque appelant doit respecter pour chaque fonction publique, et une adhérence stricte des appelants à cette spécification.

Les auteurs anticipent qu'à mesure que l'usage des LLM pour les méthodes formelles progressera, et que les modèles continueront de s'améliorer, ces limites deviendront traitables, permettant de vérifier une part bien plus large du code dont on dépend.

### Conclusion

La trajectoire est claire : la vérification formelle, historiquement réservée à des garanties sur mesure conçues par des experts pour le code le plus critique en matière de sécurité, deviendra bientôt aussi praticable que le fuzzing l'est aujourd'hui pour la quasi-totalité des logiciels de production. Tout comme le typage statique, les frameworks de test et d'autres outils de correction, la vérification passera du statut d'ajout externe à celui de brique native, porté non seulement par les LLM mais aussi par des innovations dans la conception des langages et des workflows de développement.

Dans un monde où les LLM scannent automatiquement le code pour y trouver toujours plus de vulnérabilités, des processus capables de garantir des propriétés de sécurité deviennent nécessaires. La vérification formelle mise à l'échelle par les LLM constitue une approche prometteuse pour obtenir ces garanties à une portée et une échelle jusqu'ici inatteignables. Les auteurs encouragent la communauté à expérimenter cette approche afin de construire collectivement un monde où les logiciels robustes se généralisent largement et où les bugs logiciels deviennent une rareté bien comprise et rapidement corrigible.

## Pourquoi ça compte

Cet article illustre un changement d'échelle potentiel dans la sécurité logicielle : si la vérification formelle assistée par LLM se généralise, elle pourrait déplacer la défense contre les vulnérabilités du simple test vers la preuve mathématique, avec des implications majeures pour les équipes sécurité, les mainteneurs open source et la gouvernance des dépendances critiques.
