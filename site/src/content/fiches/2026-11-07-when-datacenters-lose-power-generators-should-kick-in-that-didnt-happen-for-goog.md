---
title: "When datacenters lose power, generators should kick in. That didn’t happen for Google in London"
date: 2026-11-07
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fassets.theregister.com%2F2026%2F11%2F05%2F20265%2F%3Futm_source=tldrit/1/010001a1b103aecf-7f6aba2a-9836-49b7-ba3c-81ff30300544-000000/Z767QTyf9IDziJWYDmFeKRPK3RR8whJTNfxGPdF7h5A=452"
keywords: ["Google Cloud", "datacenter", "panne électrique", "générateurs de secours", "PLC", "résilience infrastructure"]
theme: "Tech"
tone: "news"
used_in: ["2026-11-07"]
---

## Résumé
Google Cloud a révélé que la panne du 20 octobre dans sa zone de disponibilité europe-west-2-b (Londres) résultait d'une mauvaise configuration empêchant le démarrage automatique de ses générateurs de secours. L'incident, survenu alors qu'une des deux alimentations électriques primaires était déjà hors service pour maintenance, a affecté des clients majeurs comme Lloyds, HSBC, Royal Mail et Revolut. Les onduleurs (UPS) ont fonctionné comme prévu mais ne tenaient que cinq minutes, et un défaut de conception dans la détection de tension combiné à une erreur de programmation du PLC a empêché le relais vers les générateurs. Google a depuis reconfiguré ses automates et annoncé deux mesures correctives portant sur la communication et les tests d'infrastructure.

## Points clés
- Cause racine : rupture d'un câble souterrain externe alimentant le site via le fournisseur d'électricité, sur le circuit primaire "A".
- Le circuit "B" était volontairement ouvert pour des réparations suite à un test de charge des générateurs effectué le 14 octobre 2026, rendant le site totalement dépendant du circuit A au moment de la panne.
- Les onduleurs (UPS), censés tenir 5 minutes en cas de coupure réseau, ont fonctionné normalement mais se sont épuisés car les générateurs n'ont jamais pris le relais.
- Un défaut de conception dans la détection de tension, combiné à une mauvaise configuration du PLC (automate redondant gérant la centrale de générateurs), a fait croire au système qu'une source électrique saine restait disponible, donc aucun signal de démarrage n'a été envoyé aux générateurs.
- Google a reprogrammé le PLC et modifié l'installation électrique du site, avec tests de validation à l'appui.
- Deux actions correctives annoncées : un mécanisme d'alerte automatisé pour accélérer la communication lors d'incidents localisés, et une extension des tests à l'échelle de la plateforme pour les événements au niveau infrastructure.

## Analyse approfondie
Lorsqu'un datacenter perd l'alimentation électrique, les générateurs sont censés prendre le relais automatiquement. Ce n'est pas ce qui s'est passé pour Google à Londres.

**La panne d'octobre causée par une mauvaise configuration des PLC, révélée à un moment où des travaux de maintenance réduisaient déjà la résilience du site.**

Google Cloud a révélé que la cause de la panne du 20 octobre dans sa zone de disponibilité europe-west-2-b était une "mauvaise configuration" de ses systèmes, qui a empêché le démarrage de ses générateurs de secours.

Cette panne du site londonien a provoqué des interruptions de service chez des clients comme Lloyds, HSBC, Royal Mail et Revolut.

Dans une mise à jour du 4 novembre sur sa page de statut de service, Google a expliqué ce qui s'était produit.

"Le site repose sur une architecture d'alimentation électrique 2N — où l'installation dispose de chemins d'alimentation entièrement dupliqués pour chaque charge critique — soutenue par une centrale de générateurs haute tension gérée par un automate programmable (PLC) à double redondance", a indiqué Google.

La mauvaise configuration du PLC a empêché la centrale de générateurs du site de recevoir un signal de démarrage automatique.

Le site est alimenté par deux circuits électriques indépendants, que Google appelle "A" et "B". Il existe également une "connexion électrique de secours configurée pour un transfert manuel à l'échelle du site lors d'opérations de maintenance ou d'événements d'urgence".

Google indique que la cause première de l'incident est la défaillance d'un câble souterrain externe par lequel son fournisseur d'électricité achemine le courant jusqu'à ses installations.

Ce câble est relié au circuit primaire A, et il s'est rompu à un moment où le circuit B était déjà hors service.

"Le disjoncteur du circuit B avait été physiquement ouvert pour permettre des réparations correctives suite à des problèmes identifiés lors d'un test de charge trimestriel des générateurs le 14 octobre 2026", a admis Google. "Par conséquent, l'alimentation primaire A supportait l'intégralité de la charge critique pendant que le disjoncteur du circuit B restait en position ouverte pour permettre les réparations sur le chemin du circuit B."

Cela ne devrait pas poser problème pour un opérateur de premier plan comme Google, qui sait qu'il doit installer des sources d'alimentation de secours comme des onduleurs (UPS) et des générateurs sur site.

En effet, la zone europe-west-2-b utilise des onduleurs que Google dit capables de maintenir le fonctionnement pendant cinq minutes en cas de perte de connexion au réseau électrique.

Les onduleurs ont fonctionné, mais "un défaut de conception dans la détection de tension et une mauvaise configuration du PLC ont empêché la centrale de générateurs du site de recevoir un signal de démarrage automatique pour prendre en charge la charge critique".

Les onduleurs de Google se sont donc épuisés, mais les générateurs n'ont pas démarré. La suite appartient à l'histoire.

Le géant de la recherche a compris que ses PLC n'étaient pas configurés pour gérer les conditions rencontrées ce jour fatidique.

"La logique du PLC indiquait qu'une source électrique saine était disponible, alors même que les circuits de distribution primaire et secondaire étaient hors tension, et n'a donc pas émis de commande de démarrage vers la centrale de générateurs", révèle la mise à jour de statut.

Une fois la reconnexion au réseau électrique rétablie, Google a reprogrammé le PLC afin de ne plus reproduire cette erreur.

Big G a depuis apporté de nombreuses modifications à l'installation électrique d'europe-west-2-b et affirme les avoir testées, avec succès.

L'entreprise s'est également fixé deux actions correctives, dont l'une est décrite comme une "amélioration des communications", qui consistera à "renforcer la rapidité des notifications en développant un mécanisme automatisé d'alerte vers communication pour les incidents affectant un site donné".

L'autre consiste à "étendre les résultats des tests à l'échelle de la plateforme pour les événements au niveau de l'infrastructure".

Une fois ces mesures mises en œuvre, Google pourra peut-être mieux gérer les pannes à l'avenir — et, à défaut, au moins informer ses clients plus rapidement de ses difficultés.

## Pourquoi ça compte
Cet incident illustre qu'une architecture de résilience 2N ne protège pas contre les erreurs de configuration logicielle des automates critiques, un rappel utile pour toute veille sur la fiabilité du cloud et la dépendance des services financiers à une poignée d'hyperscalers.
