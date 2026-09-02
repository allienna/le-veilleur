---
title: "How to Write an Effective Software Design Document"
date: 2026-09-02
url: "https://link.mail.beehiiv.com/ss/c/u001.71LCQkoHczeoiEaexlZjthwMm64Iym68hKzQdPM2gmuhJAgJbFM9fpwq3g99YEWQjiKAHbDoEQXmvpARi4FxRwwWPxOvdzmKh0Y_rBG7b4rae40T3xjZpoxHYIdrGhGTNpN4-t_J94pVxtc_9aVMg5HqpuE3i35ZJq_6Q5FUAkCm57QOfGJpH6tFBYwgzMFBF3QLN9BehqoGAWxYXfei_Q/4to/J86wL3ZyRZKrMW8TS6n3xA/h15/h001.xAUAV7S62id1nsgrkEHme0My4L862bIskre8T_U06Aw"
authors: ["Michael Lynch"]
keywords: ["design doc", "documentation technique", "ingénierie logicielle", "revue de conception", "planification produit", "communication d'équipe"]
theme: "Tech"
tone: "tutorial"
used_in: ["2026-09-02"]
---

## Résumé
L'article explique pourquoi et comment rédiger un « design doc » (document de conception) efficace avant de se lancer dans l'implémentation d'un projet logiciel. L'auteur, qui a rédigé ce type de documents chez Google et Microsoft, détaille les sections à privilégier (objectif, contexte, buts/non-buts, scénarios, interfaces, sécurité, SLO, timeline...) et le principe directeur pour trancher ce qui mérite d'y figurer : le coût d'une mauvaise décision. Il illustre chaque section avec l'exemple fictif d'un projet de cache mémoire (« RecencyBank ») entre un serveur web et une base Postgres. L'article se conclut en annonçant un second volet consacré à la conduite de la revue du document.

## Points clés
- Un design doc sert à réfléchir aux décisions difficiles *avant* d'écrire du code, et à coordonner les équipes autour de ces choix.
- On écrit un design doc surtout quand le risque ou la coordination le justifient : projet long, multi-équipes, objectifs ambigus, risques catastrophiques (sécurité, légal).
- Le niveau de détail doit être calibré sur le coût d'une erreur : les décisions difficiles à annuler (langage, stockage) méritent un vrai débat écrit ; les détails triviaux et réversibles (ex. un bouton « voir plus ») n'ont pas leur place dans le doc.
- Le document doit se comprendre sans contexte oral préalable : titre évocateur, métadonnées (auteur, date, statut, signataires), objectif en une phrase, contexte/background en tête de doc.
- Sections utiles selon le projet : buts/non-buts, scénarios d'usage, diagrammes, glossaire, contraintes, SLO et monitoring associé, timeline en jalons livrables, interfaces (API/UI/format de fichier), dépendances, sécurité, confidentialité, aspects légaux, logging.
- Les sections « Alternatives envisagées » et « Problèmes ouverts / résolus » servent à anticiper les questions des relecteurs et à tracer les décisions prises pendant la revue, sans sur-documenter chaque option écartée.

## Analyse approfondie

### Pourquoi un design doc
Écrire un design doc force à anticiper les problèmes difficiles avant d'investir du temps dans une implémentation qui pourrait s'avérer être une impasse. C'est aussi le meilleur outil pour aligner plusieurs personnes ou équipes sur des choix de conception. L'auteur, faute de pouvoir partager les documents rédigés en entreprise (propriété des employeurs), a construit un exemple de A à Z pour une application web réelle, en respectant les principes présentés, et l'a suivi pendant l'implémentation.

### Quand écrire un design doc
Plus un projet est complexe ou risqué, plus un design doc a de valeur. Des indices : plusieurs personnes doivent coordonner leur travail ; le projet dépasse trois mois à temps plein ; le système restera en production plusieurs années ; il implique plusieurs équipes ; les objectifs sont ambigus ; des risques catastrophiques (failles de sécurité, risques juridiques) pourraient être évités en amont. Répondre « oui » à une seule question rend déjà l'exercice probablement utile ; à deux ou plus, il devient quasi indispensable.

### Quel niveau d'investissement
Un design doc peut être une simple page ou un document de cinquante pages nécessitant la validation de cinq équipes. Il n'existe pas de règle universelle : l'investissement dépend des objectifs, risques, délais et de la culture de l'équipe — parfois, le bon niveau d'investissement est nul.

### Que doit contenir un design doc
Si l'on détaille chaque décision possible, on finit par écrire l'implémentation pendant la phase de conception, ce qui annule l'intérêt de l'exercice. La règle proposée : se demander quel est le coût de se tromper sur une décision donnée. Certains choix sont quasi permanents (par exemple choisir C++ plutôt que Ruby on Rails pour une application, découvert 200 000 lignes plus tard) ; d'autres sont triviaux et réversibles en quelques heures (afficher tous les articles d'une liste d'un coup ou par pages de 20 avec un bouton « voir plus »). Seules les décisions coûteuses à corriger méritent un débat détaillé dans le doc.

### Les sections type d'un design doc
L'auteur propose une liste de sections à utiliser sélectivement, pas systématiquement :

- **Titre** : court, distinctif, évocateur (ex. « RecencyBank » plutôt que « Project Flying Silver Horse »).
- **Métadonnées** : auteur et email, date de création, URL de référence (y compris les liens raccourcis internes), personnes ayant validé le document et à quelle date.
- **Objectif** : une phrase, en langage clair, en première page — ex. « Améliorer les performances de l'application en ajoutant une couche de cache entre le serveur web Trogdor et la base Postgres ».
- **Contexte (Background)** : pourquoi l'équipe s'attaque à ce projet, quel problème il résout, quelles tentatives ont déjà eu lieu. L'exemple donné : le temps de chargement des pages est passé de 100 ms à 600 ms en trois ans, l'analyse montre que 80 % du temps de chargement vient des requêtes base de données, et que 95 % des requêtes portent sur seulement 3 % des lignes — un cas typique où un cache mémoire apporte un net bénéfice. L'auteur insiste : le document doit se comprendre sans explication orale préalable, car certains lecteurs le liront sans contexte.
- **Documents liés** : liens vers les plans de test, les design docs de systèmes connexes ou d'itérations précédentes.
- **Buts** : décrits en termes de bénéfice pour les utilisateurs, l'équipe ou l'entreprise plutôt qu'en détails d'implémentation (« augmenter la réactivité perçue » plutôt que « ajouter Kubernetes »).
- **Non-buts** : ce qui est explicitement hors périmètre, notamment ce que les lecteurs pourraient supposer inclus à tort (ex. ne pas construire un cache générique réutilisable, ne pas gérer un cache géo-distribué dans cette v1).
- **Scénarios** : décrire un cas d'usage concret pas à pas pour rendre tangible un but abstrait (ex. Bob partage un rapport via une URL que Charlie peut consulter en lecture seule).
- **Diagrammes** : très utiles car l'auteur a déjà l'architecture en tête, contrairement aux relecteurs. Privilégier des outils permettant de réviser facilement (Excalidraw, draw.io, Google Drawings) ou des langages de diagramme génératifs (Mermaid, D2, Graphviz, éventuellement via un LLM), plutôt qu'une photo de tableau blanc impossible à corriger.
- **Glossaire** : définir les termes ou outils internes que les nouveaux membres ou équipes externes ne connaîtraient pas ; mieux encore, utiliser des termes reconnaissables directement dans le texte.
- **Contraintes** : limites imposées par le budget, les clients, l'infrastructure ou les dépendances (ex. tout le code doit tourner sur une architecture RISC-V).
- **Objectifs de niveau de service (SLO)** : objectifs mesurables (disponibilité, latence, échelle), à distinguer des SLA (qui ajoutent des pénalités financières). Exemple : latence médiane HTTP ≤ 200 ms, latence médiane des requêtes Postgres ≤ 80 ms.
- **Monitoring / alerting** : comment vérifier en production que les SLO sont atteints, quels événements déclenchent une alerte (ex. latence P95 ≥ 3 s, usage CPU moyen ≥ 90 % sur 2 minutes).
- **Timeline** : jalons produisant des livrables utiles aux parties prenantes, idéalement en commençant par une UI avec des données factices pour valider tôt la compréhension du besoin. L'auteur renvoie à l'article classique de Joel Spolsky sur l'estimation de planning logiciel.
- **Interfaces** : à quoi ressemblent les interactions avec le système (UI, API/CLI, format de fichier). L'exemple technique détaille comment introduire une interface Go `Store` entre le serveur `Trogdor` et son implémentation Postgres, pour permettre d'intercaler la couche de cache `RecencyBank` sans changer le reste du code appelant.
- **Dépendances / infrastructure** : langage, hardware/service d'exécution, emplacement des données persistantes — en distinguant les dépendances difficiles à changer plus tard (langage, backend de stockage) de celles faciles à remplacer (ex. un service d'envoi d'emails tiers). Exemple : choix de Go (déjà largement utilisé, adapté aux charges parallèles) et de la bibliothèque clé-valeur `bbolt`.
- **Sécurité** : quelles menaces ont été envisagées, quelle est la surface d'attaque, où se situent les frontières de confiance (ex. les requêtes venant du navigateur d'un utilisateur franchissent une frontière de confiance vis-à-vis du serveur web). Même si le risque semble faible, documenter le raisonnement permet aux relecteurs de repérer des angles morts. Exemple : RecencyBank ne doit jamais recevoir de requêtes directes depuis Internet et doit rester sur un réseau segmenté.
- **Confidentialité (Privacy)** : quelles données sensibles sont traitées, combien de temps elles sont conservées, qui y a accès, comment elles sont protégées (chiffrement au repos et en transit). Exemple : RecencyBank hérite de la politique de confidentialité de Postgres ; l'accès en production nécessite un numéro de ticket associé.
- **Aspects légaux** : pertinent notamment dans les domaines réglementés (finance, santé), ou pour le choix d'une licence open source. Exemple fictif : un contrat client limitant la duplication de données biométriques propriétaires, avec confirmation juridique qu'une couche de cache reste dans le périmètre autorisé du contrat.
- **Logging** : quels événements critiques sont journalisés, niveaux de log, lieu de stockage, durée de rétention, contrôle d'accès, données sensibles à exclure des logs. Exemple : RecencyBank journalise ses paramètres d'initialisation, les échecs de persistance en mémoire et les échecs d'invalidation de cache.
- **Problèmes ouverts** : documenter les points non résolus (faille de conception, choix encore en balance, information manquante), avec les options envisagées et la prochaine étape. Exemple détaillé : choisir la quantité de RAM à allouer au cache, en pesant le coût de tests de simulation (environ 3 jours-développeur pour la première simulation, puis 0,75 jour par simulation supplémentaire) contre une décision empirique de 128 Go sans test approfondi.
- **Problèmes résolus** : une fois un problème ouvert tranché, on résume la décision et on la déplace dans une section « résolus », en conservant la discussion complète pour l'historique. Exemple : décision finale de provisionner 128 Go de RAM, le coût des tests approfondis étant jugé supérieur au coût de RAM supplémentaire.
- **Alternatives envisagées** : quelques lignes expliquant pourquoi une option qui pourrait sembler pertinente a été écartée (ex. Google Cloud Firestore, rejeté pour le risque de dépendance à la plate-forme et la difficulté de tests en local), sans documenter exhaustivement chaque piste rejetée — l'auteur juge cela excessif.

### Suite de l'article
L'article se termine en annonçant qu'un second billet abordera la manière de conduire la revue du design doc pour recueillir des retours constructifs plutôt que de bloquer le projet dans des débats stériles.

## Pourquoi ça compte
Pour une veille tech orientée ingénierie et leadership, cet article propose un référentiel concret et actionnable pour structurer la prise de décision et la communication autour de projets complexes, utile aussi bien pour cadrer des revues d'architecture que pour former des équipes à documenter leurs choix avant d'écrire du code.
