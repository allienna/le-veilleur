---
title: "Velox at Uber: Rebuilding Presto's® Execution Engine for Speed and Scale"
date: 2026-11-16
url: "https://substack.com/redirect/c7831b64-4ecb-4650-850a-18a23995494c?j=eyJ1IjoiN3Y1bG1jIn0.HlvPOGYPdVknSYzEK1JIj6IFkAFn8zuyjtfU9Mbft9Q"
authors: ["Hitarth Trivedi", "Jay Narale", "Jianjian Xie", "Yunfei Chen", "Sanah Imani"]
keywords: ["Velox", "Presto", "Uber", "moteur d'exécution vectorisé", "Parquet", "open source"]
theme: "Data"
tone: "research"
used_in: ["2026-11-16"]
---

## Résumé
Cet article de blog d'ingénierie Uber retrace la migration, menée sur deux ans, du moteur d'exécution de Presto depuis la JVM Java vers Velox, un moteur vectorisé en C++ open source initialement développé par Meta. Ce projet, que la communauté appelle Prestissimo, alimente désormais environ 90% du trafic Presto éligible chez Uber et traite près de 100 pétaoctets de données par jour. Les auteurs détaillent les défis d'infrastructure liés à l'adoption d'un moteur natif en C++ (outillage, observabilité, gestion mémoire), les problèmes de compatibilité Parquet rencontrés, ainsi que les gains de performance mesurés avec rigueur (jusqu'à 3,73x de réduction du temps CPU). Ils insistent enfin sur leur stratégie de rester proche du code source amont et sur les travaux restants pour couvrir la totalité du trafic.

## Points clés
- Velox, moteur C++ vectorisé open source issu de Meta, remplace progressivement le moteur JVM de Presto chez Uber depuis décembre 2023.
- Le déploiement s'est fait en deux phases de routage : d'abord une liste blanche de requêtes validées par shadow-testing, puis une liste noire de signatures de requêtes connues pour faire planter Velox.
- Les gains mesurés atteignent jusqu'à 3,73x de réduction du temps CPU et 2,5x de réduction du temps d'exécution, avec la possibilité de fonctionner avec 30% de capacité en moins tout en restant plus performant que Java à pleine capacité.
- D'importants efforts ont porté sur la compatibilité Parquet en lecture et en écriture, l'observabilité (intégration Prometheus/M3) et la gestion mémoire d'un processus natif.
- Uber maintient un fork proche du tronc commun open source (mises à jour quasi hebdomadaires) et contribue activement en amont, notamment sur les fonctions géospatiales.
- Des lacunes subsistent (UDF legacy, connecteurs Kafka/MySQL, anonymisation des données) et une "Phase 3" vise à éliminer complètement la liste noire de signatures de plantage.

## Analyse approfondie
### Introduction
Chaque jour, le parc Presto d'Uber répond à des centaines de milliers de requêtes émises par des ingénieurs, data scientists et analystes, qu'il s'agisse d'investigations ponctuelles ou de pipelines de production planifiés. À cette échelle - des dizaines de clusters, des milliers de machines, des centaines de pétaoctets traités quotidiennement - même de petites inefficacités d'exécution se traduisent par des coûts d'infrastructure réels.

Depuis deux ans, l'équipe Presto d'Uber reconstruit le cœur du moteur qui fait tourner ce parc. Plutôt que de faire transiter les requêtes par le moteur Java basé sur la JVM, l'exécution a été déplacée vers Velox, un moteur d'exécution vectorisé en C++, open source, conçu et publié initialement par Meta. Le résultat - que la communauté open source appelle Prestissimo - consiste à faire tourner Presto sur Velox : le même SQL, sur les mêmes clusters, mais nettement plus rapide et moins coûteux.

Aujourd'hui, Velox alimente environ 90% du trafic Presto éligible chez Uber, traitant de l'ordre de 100 pétaoctets de données par jour. Le taux de succès des requêtes a augmenté, le temps d'exécution moyen a été réduit de plus de moitié, et la consommation CPU par requête a chuté d'environ deux tiers par rapport à l'ancien moteur Java, tout cela en exécutant exactement les mêmes requêtes déjà écrites par les utilisateurs.

### Pourquoi Velox
Presto chez Uber consomme énormément de CPU lors de l'exécution des requêtes. Il y a quelques années, le profilage des clusters a révélé que plus de 90% des cycles CPU étaient consacrés à une seule étape d'exécution : l'opérateur chargé de scanner les données sur disque, d'appliquer les filtres et de projeter les colonnes. Les surcoûts de la JVM (objets boxés, garbage collection, bytecode qui ne se vectorise pas de façon fiable en instructions SIMD) rendaient cette tâche intrinsèquement inefficace, quel que soit le niveau de réglage appliqué.

L'exploration de Velox pour le déploiement Presto d'Uber a commencé en décembre 2023. La preuve de concept initiale a immédiatement attiré l'attention : sur les requêtes dominées par le scan, exactement celles qui pèsent le plus sur le budget CPU, les gains de temps CPU atteignaient jusqu'à 7x. Un chiffre suffisamment significatif pour justifier un investissement bien plus profond qu'un simple projet parallèle.

### Les premiers obstacles
La promesse de Velox est apparue vite, mais sa concrétisation a été plus difficile. L'infrastructure de données d'Uber tourne principalement sur Go, Python et Java ; le C++ n'occupait qu'une place marginale dans la pile technique. Adopter un moteur d'exécution natif en C++ a donc fait surgir une série de problèmes sans rapport avec la performance des requêtes elles-mêmes.

L'outillage interne pour le C++ était immature : systèmes de build, flux de débogage, intégration CI - tout ce qui était acquis pour Java et Go restait à construire pour une base de code C++ aussi volumineuse et évolutive que Velox. La gestion des dépendances est devenue un casse-tête à part entière, Velox et le worker C++ de Presto embarquant un nombre non négligeable de bibliothèques système natives à vendoriser, versionner et maintenir cohérentes sur l'ensemble du parc. L'observabilité, elle aussi, était insuffisante : des années avaient été investies dans l'outillage autour de la JVM (heap dumps, logs GC, métriques JMX), rien de tout cela ne se transposait à un processus natif. Il fallait une visibilité équivalente dès le premier jour pour exploiter ce moteur en production en toute sécurité. Et dans les premiers temps, les plantages de workers et les kills pour dépassement de mémoire étaient fréquents, ce qui, en l'absence d'observabilité adéquate, rendait le diagnostic extrêmement lent.

Aucun de ces problèmes ne concernait la logique d'exécution de Velox proprement dite : ils relevaient de la réalité opérationnelle consistant à faire tourner un nouveau type de processus à l'échelle d'Uber. Les résoudre a constitué la véritable première phase du projet, même si c'est la partie qui n'apparaît jamais sur un graphique de performance.

### Construire les fondations
Avant que Velox puisse porter un trafic de production significatif, il fallait lui donner la même maturité opérationnelle que celle déjà acquise pour Presto en Java.

Côté observabilité, Prometheus a été intégré au processus Prestissimo, selon une proposition développée conjointement avec IBM : un petit sous-processus tourne en parallèle du processus Prestissimo principal, bufferise les métriques via la bibliothèque prometheus-cpp et les expose en HTTP. La plateforme de métriques M3 d'Uber, son back-end open source compatible Prometheus à grande échelle, scrute ce point de terminaison, ce qui a permis de retrouver les mêmes tableaux de bord et alertes que pour Presto en Java.

La gestion de la mémoire s'est révélée être un projet à part entière : la rendre fiable dans un processus natif est sans pitié, d'une manière que le garbage collector de la JVM dissimule habituellement. L'équipe a adopté l'arbitre de mémoire de Velox en mode partagé, combiné à l'allocateur mmap, et a passé beaucoup de temps à ajuster les limites mémoire, les seuils de pushback et les plafonds par requête jusqu'à obtenir des clusters stables en charge de production réelle.

Plutôt que de basculer tout le trafic d'un coup, le déploiement s'est fait en deux phases de routage distinctes. La phase 1 a permis de passer de 0% à environ 30% de migration : chaque requête était d'abord testée en miroir ("shadow-testing"), exécutée à la fois sur Java et sur Velox avec comparaison des résultats, et seules les signatures ("fingerprints") validées étaient ajoutées à une liste blanche autorisant Velox, tout le reste restant par défaut sur Java. La phase 2 a pris le relais : tester en miroir chaque signature à cette échelle n'était plus praticable, le modèle a donc été inversé - au lieu d'une liste blanche de requêtes connues comme sûres, une liste noire de signatures connues pour faire planter Velox est désormais utilisée, laissant passer tout le reste par défaut. Ce modèle par opt-out est ce qui a permis de passer de 30% à environ 90% du trafic éligible actuel.

### Combler les lacunes de format : Parquet
La majeure partie du data lake d'Uber réside en Apache Parquet ; la compatibilité avec ce format n'a donc jamais été optionnelle, et elle s'est révélée être une source de bugs assez subtils.

Côté lecture, des problèmes ont été identifiés et corrigés dans la façon dont le lecteur de Velox traitait les valeurs nulles à l'intérieur de types complexes (structs, tableaux, maps), ce qui produisait dans certains cas des résultats de requêtes incorrects - une catégorie de bug considérée comme particulièrement grave, une réponse silencieusement fausse étant pire qu'un échec franc. Une série de problèmes de rétrocompatibilité affectant d'anciens fichiers Parquet écrits par des versions antérieures de la pile a également été traitée, avec la mise en place d'un cadre de test réutilisant les tests unitaires Java existants de Presto pour générer des fichiers Parquet, puis vérifier le lecteur Velox par rapport à eux - transformant des années de couverture de tests Java en un filet de sécurité pour le nouveau moteur.

L'écriture a posé davantage de problèmes. L'évaluation du writer Parquet de Velox a montré qu'il ne constituait pas encore un remplacement direct dans tous les cas : pas de prise en charge complète de l'évolution de schéma de bout en bout, certains types liés au temps (TIME, TIMESTAMP) pas entièrement supportés, des taux de compression nettement inférieurs pour les types numériques et les colonnes MAP (dus à une politique d'encodage différente dans le writer Velox), et des tables écrites par Velox pas toujours relisibles par Spark SQL - un problème réel dans un environnement où les mêmes tables sont consommées par plusieurs moteurs.

Des correctifs sur les différences d'encodage ont été proposés en amont, et le support CLAC (la couche d'accès et de compression columnaire d'Uber) est devenu l'un des principaux contributeurs à la réduction de cet écart. Plus récemment, l'attention côté lecteur s'est portée sur la stabilité en production : correction de problèmes de fragmentation du tas sous charge soutenue et audit des configurations open source par défaut pour repérer les écarts entre hypothèses et comportement réel.

### Le résultat : les performances
Tout ce travail de fond avait un seul objectif : rendre les requêtes Presto plus rapides et moins coûteuses. Ce gain a été mesuré plusieurs fois, avec une rigueur croissante.

Les premières comparaisons tête-à-tête ont porté sur plus de 40 000 requêtes couvrant plus de 1 000 formes de requêtes uniques. À capacité égale, Velox a apporté une amélioration de 3,73x du temps CPU et de 2,5x du temps écoulé. Plus intéressant encore, la même charge de travail a pu tourner avec 30% de capacité en moins sur Velox tout en restant devant Java à pleine capacité, avec une amélioration de 3,55x du CPU et 1,47x du temps écoulé.

| | Velox 100 vs Java 100 | Velox 70 vs Java 100 |
|---|---|---|
| Capacité | identique | 30% de moins |
| Temps CPU | amélioration de 3,73x | amélioration de 3,55x |
| Temps écoulé | amélioration de 2,5x | amélioration de 1,47x |
| Requêtes totales | 40 000+ | 40 000+ |
| Formes de requêtes uniques | 1 000+ | 1 000+ |

Pour aller au-delà des premiers benchmarks, une étude formelle de type "Performance Improvement Factor" a ensuite été menée pour certifier une nouvelle configuration de machine à 48 cœurs, colocalisée avec Alluxio, pour un déploiement Velox en production. Cette méthodologie, déjà utilisée pour évaluer de nouvelles générations de calcul, repose entièrement sur du shadow-testing de trafic de production réel plutôt que sur des tests synthétiques.

Le dispositif comptait autant que le résultat : le trafic réel d'un cluster Velox de production a été répliqué en miroir vers deux clusters de test de taille identique, l'un tournant sous Java, l'autre sous Velox, grâce à une amélioration de l'outil interne de shadow-testing, Modulator, permettant de rejouer les requêtes avec un timing de soumission correspondant plutôt que d'attendre la fin de la requête d'origine. Comme Velox ne pouvait pas encore absorber tout le trafic de Java (à l'époque, seulement 50 à 60% du trafic global était éligible à Velox), le trafic éligible à Velox a été délibérément choisi comme source du miroir, afin que les deux clusters soient jugés sur la même charge de travail équitable. Les sessions miroir ont également été ordonnées pour que le cluster Java soit poussé jusqu'à ses limites réelles plutôt que d'être protégé par un flux amont plus lent.

Ces résultats se retrouvent clairement dans les métriques du parc à grande échelle. Au cours de l'année écoulée, le nombre de clusters Presto compatibles Velox a été multiplié par environ vingt, passant d'un seul cluster à plus de deux douzaines, avec une accélération plus marquée ces derniers mois à mesure que le réglage des configurations progressait et que l'éligibilité des charges de travail s'élargissait. La part de Velox, à la fois en données lues et en volume de requêtes, a suivi la même courbe, dépassant Java vers la fin de l'année dernière et représentant désormais la grande majorité du trafic sur les clusters compatibles Velox. Aujourd'hui, Velox traite environ 100 pétaoctets de données par jour chez Uber, soit le double de ce qu'il traitait lors des premières communications publiques sur ce projet.

### Au-delà du cœur : élargir la portée de Velox
Une fois le moteur de base stabilisé et performant, l'attention s'est tournée vers des problèmes auparavant hors de portée ou trop coûteux à résoudre correctement.

Le géospatial s'est révélé plus important que prévu : les fonctions géométriques représentent environ 15% de l'ensemble du temps CPU Presto chez Uber, ce qui n'est pas surprenant pour une entreprise dont le produit principal repose entièrement sur des données géospatiales, mais représente tout de même une concentration de calcul considérable. Des contributions ont été faites en amont de la feuille de route open source géospatiale, incluant une dépendance fusionnée pour la manipulation de géométries et une implémentation de type géométrique, avec un support de sérialisation en cours. En interne, des fonctions comme ST_Contains et des opérateurs de cast pour les types géométriques ont été implémentées, ainsi qu'une jointure géospatiale initiale utilisant une stratégie de boucle imbriquée ("nested-loop").

Le routage du trafic vers Velox a également continué d'être affiné, par phases successives : d'abord validation en mode miroir, puis logique de nouvelle tentative, puis protection contre les boucles de plantage, afin que les décisions de routage restent résilientes même lorsque des requêtes ou des clusters individuels se comportent mal.

### Rester proche de l'open source
Rien de tout cela n'aurait été viable si un fork fortement personnalisé et propre à Uber de Prestissimo et Velox avait été développé isolément. Dès le départ, le choix a été fait de rester aussi proche que possible du code amont et de récupérer les changements open source à un rythme régulier, environ hebdomadaire désormais.

Cette décision a porté ses fruits de façon souvent sous-estimée : rester proche de la branche principale signifie rarement courir après des bugs déjà corrigés en amont, et une simple mise à jour de version peut intégrer des centaines de commits amont en une fois - l'opposé d'un effort gaspillé. Cela signifie aussi ne pas résoudre les problèmes seul : les bugs identifiés et corrigés deviennent des problèmes communautaires, et les correctifs profitent à tous, pas seulement à Uber. Cela permet également de savoir précisément ce qui est intégré, pour décider en connaissance de cause quelles fonctionnalités amont activer et quand. Et cela évite le piège de la double maintenance, certaines fonctionnalités comme le support CLAC et l'évolution de schéma ayant historiquement entré en conflit avec la branche principale amont - rester proche réduit la fréquence des réconciliations nécessaires avec une base de code qui évolue rapidement.

Tout aussi important, cette approche a poussé à s'engager réellement avec la communauté open source plutôt que de travailler isolément : contributions de PR, participation aux discussions de conception, et adoption de pratiques et d'astuces de débogage qui n'auraient probablement pas été découvertes autrement.

### Combler le dernier kilomètre
Velox gère désormais la majorité du trafic Presto éligible chez Uber, mais le mot "éligible" fait un vrai travail dans cette phrase. Une part significative des charges de travail ne peut toujours pas tourner sur Velox aujourd'hui, et combler cet écart concentre l'essentiel de l'effort actuel. Le travail en cours porte sur le retrait progressif des tentatives de repli sur les clusters Java (qui servent aujourd'hui de filet de sécurité pour les requêtes ne réussissant pas encore de façon fiable sur Velox), le comblement des UDF legacy dont dépendent des pipelines existants mais qui n'ont pas encore d'équivalent Velox, la résolution des derniers problèmes résiduels de Parquet et des scénarios de plantage résiduels qui n'apparaissent qu'à la marge du trafic de production, ainsi que la fermeture des lacunes fonctionnelles restantes, notamment l'anonymisation des données, le support du writer CLAC, et les connecteurs pour des systèmes comme Kafka et MySQL dont certaines charges de travail dépendent encore.

À plus long terme, une configuration de cluster à workers mixtes est explorée, qui permettrait à un cluster unique de router les requêtes nécessitant des catalogues non supportés (comme Kafka, Pinot ou MySQL) sans basculer vers un cluster Java entièrement séparé. L'investissement continue sur les fonctions géométriques et les jointures spatiales, sur l'augmentation du pourcentage de formes de requêtes bénéficiant d'une couverture Velox complète, et sur la migration des charges de travail batch restantes. Plus loin encore, l'objectif est une "Phase 3" : réduire à néant la liste noire de signatures de plantage, afin que les décisions de routage ne soient plus du tout basées sur des signatures.

### Conclusion
L'adoption de Velox constitue l'un des investissements d'infrastructure les plus marquants réalisés par l'équipe plateforme data d'Uber ces dernières années. Y arriver a nécessité de construire de l'outillage et de l'observabilité C++ à partir de zéro, de combler patiemment les écarts de compatibilité Parquet, et de valider chaque affirmation de performance par des tests rigoureux de qualité production plutôt que de se fier à des benchmarks synthétiques.

Le résultat est substantiel : environ 2,4x de requêtes plus rapides, une utilisation CPU divisée par 3 selon le benchmark de production le plus récent et le plus rigoureux, et une fiabilité nettement améliorée, sur des dizaines de clusters traitant environ 100 pétaoctets de données par jour, avec une empreinte Velox toujours croissante. Les auteurs remercient les communautés open source Velox et Presto, notamment l'équipe Velox de Meta et leurs collaborateurs chez IBM, pour la base commune qui a rendu ce travail possible, et affirment leur intention de continuer à contribuer en retour.

## Pourquoi ça compte
Ce retour d'expérience illustre concrètement comment un acteur majeur migre un moteur de requêtes historique vers un moteur vectorisé C++ en conditions réelles, avec des gains de performance chiffrés et une méthodologie de validation reproductible. C'est un cas d'école pertinent pour toute équipe data infrastructure évaluant Velox, Presto, ou une migration JVM vers un moteur natif.
