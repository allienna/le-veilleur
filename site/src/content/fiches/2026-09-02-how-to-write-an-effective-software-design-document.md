---
title: "How to Write an Effective Software Design Document"
date: 2026-09-02
url: "https://link.mail.beehiiv.com/ss/c/u001.71LCQkoHczeoiEaexlZjthwMm64Iym68hKzQdPM2gmuhJAgJbFM9fpwq3g99YEWQjiKAHbDoEQXmvpARi4FxRwwWPxOvdzmKh0Y_rBG7b4rae40T3xjZpoxHYIdrGhGTNpN4-t_J94pVxtc_9aVMg5HqpuE3i35ZJq_6Q5FUAkCm57QOfGJpH6tFBYwgzMFBF3QLN9BehqoGAWxYXfei_Q/4to/J86wL3ZyRZKrMW8TS6n3xA/h15/h001.xAUAV7S62id1nsgrkEHme0My4L862bIskre8T_U06Aw"
authors: ["Michael Lynch"]
keywords: ["design document", "documentation technique", "architecture logicielle", "revue de conception", "gestion de projet"]
theme: "Tech"
tone: "opinion"
used_in: ["2026-09-02"]
---

## Résumé
L'auteur, qui a rédigé des design docs chez Google, Microsoft et dans ses propres entreprises, expose sa méthode pour écrire des documents de conception logicielle efficaces. Un bon design doc permet de trancher les décisions difficiles avant d'investir du temps dans une implémentation qui s'avérera erronée, et sert de support de coordination entre équipes. L'article détaille quand un tel document est justifié, quel niveau de détail y consacrer, puis passe en revue les sections type (titre, objectif, contexte, buts et non-buts, scénarios, diagrammes, SLO, sécurité, dépendances, problèmes ouverts, alternatives envisagées, etc.), chacune illustrée par un exemple fictif autour d'un projet de cache nommé « RecencyBank ». Il conclut en annonçant un second article consacré à la conduite de la revue du document.

## Points clés
- Un design doc se justifie surtout pour les projets complexes, longs (plus de trois mois), risqués, transverses ou dont les exigences sont ambiguës ; deux "oui" ou plus aux questions posées rendent l'exercice quasi obligatoire.
- Le niveau de détail doit rester proportionné : si le document précise tout, on a en fait écrit l'implémentation en phase de conception, ce qui est contre-productif.
- Le critère pour décider si une décision mérite sa place dans le doc est le coût de l'erreur : les choix difficiles à annuler (langage, stockage) méritent discussion, les détails réversibles en quelques heures ne la méritent pas.
- L'auteur propose une liste de sections modulables : titre, métadonnées, objectif, contexte, documents liés, buts/non-buts, scénarios, diagrammes, glossaire, contraintes, SLO, monitoring/alerting, calendrier, interfaces, dépendances/infrastructure, sécurité, vie privée, aspects légaux, logging, problèmes ouverts/résolus, alternatives envisagées.
- Les diagrammes sont jugés indispensables car l'auteur visualise mentalement l'architecture alors que les relecteurs n'en ont pas l'intuition ; il recommande des outils éditables (Excalidraw, draw.io, Mermaid, D2, Graphviz) plutôt qu'une photo de tableau blanc figée.
- Les SLO doivent transformer des objectifs flous (« performant sur mobile ») en métriques mesurables (latence, disponibilité, charge supportée), et la section « problèmes ouverts » doit documenter explicitement les points non tranchés, les options envisagées et la prochaine étape.

## Analyse approfondie
L'article s'organise en deux grands mouvements : le cadrage (pourquoi et combien investir dans un design doc) puis un inventaire commenté des sections qui composent un tel document, chacune accompagnée d'un exemple concret tiré d'un projet fictif de couche de cache (« RecencyBank ») entre le serveur web Trogdor et une base Postgres.

**Pourquoi et quand écrire un design doc.** L'auteur part d'un constat personnel : il n'a jamais vu de design doc public de bonne qualité, tous les siens restant confidentiels chez ses employeurs — ce qui l'a poussé à en rédiger un de A à Z pour un projet web réel, avant d'en commencer le code, et à s'y tenir pendant l'implémentation. Il propose ensuite une grille de questions pour juger de la pertinence de l'exercice : coordination entre plusieurs personnes, durée de développement supérieure à trois mois, durée de vie en production de plusieurs années, collaboration inter-équipes, exigences ambiguës, risques catastrophiques évitables en amont (sécurité, aspects légaux). Répondre « oui » à une seule de ces questions rend le document utile ; à deux ou plus, il devient quasi indispensable.

**Le bon niveau de détail.** Il n'existe pas de règle universelle sur la longueur d'un design doc, tout comme il n'y en a pas sur la quantité de tests à écrire : cela dépend des objectifs, risques, délais et culture de l'équipe — et parfois, l'investissement optimal est nul. Le critère central que propose l'auteur pour trancher quoi inclure est : quel est le coût de se tromper ? Une décision quasi irréversible, comme choisir C++ plutôt que Ruby on Rails pour une application web (un choix qu'on ne peut plus défaire après 200 000 lignes de code), mérite d'être débattue dans le document. À l'inverse, un choix trivial et réversible — afficher 1000 articles d'un coup ou par pages de 20 avec un bouton « charger plus » — ne relève pas du niveau design et ne doit pas consommer de temps de revue.

**Anatomie détaillée d'un design doc.** L'auteur énumère ensuite, section par section, ce qu'un tel document peut contenir — en précisant qu'on n'a pas besoin de toutes les sections pour chaque projet :
- *Titre* : court, distinctif, évocateur (« RecencyBank » plutôt qu'un nom de code creux).
- *Métadonnées* : auteur, date, URL canonique, signataires — utile mais purement administratif.
- *Objectif* : une phrase unique, compréhensible par n'importe quelle partie prenante, en tête du document.
- *Contexte* : pourquoi le projet est lancé, quel problème il résout, quelles tentatives antérieures ont existé — l'auteur insiste sur le fait que le document doit se comprendre sans explication orale préalable, car certains lecteurs le liront sans contexte.
- *Documents liés* : liens vers les plans de test, design docs de systèmes connexes ou d'itérations précédentes.
- *Buts et non-buts* : les buts s'expriment en termes de bénéfice utilisateur ou métier plutôt que d'implémentation ; les non-buts explicitent ce qui est hors périmètre pour éviter les malentendus (par exemple, ne pas construire un cache générique réutilisable, ni un cache géo-distribué dès la v1).
- *Scénarios* : des mises en situation concrètes pour rendre tangible l'usage final du système.
- *Diagrammes* : jugés très précieux car l'auteur a une vue mentale de l'architecture que les relecteurs n'ont pas ; privilégier des outils éditables plutôt qu'une photo figée d'un tableau blanc.
- *Glossaire* : définir les termes internes qui pourraient dérouter des lecteurs externes à l'équipe, en gardant à l'esprit que le mieux reste d'utiliser des termes déjà reconnus.
- *Contraintes* : limites imposées par le budget, les clients, l'infrastructure ou les dépendances (exemple : obligation de tourner sur architecture RISC-V).
- *Objectifs de niveau de service (SLO)* : des métriques mesurables (disponibilité, latence, échelle) qui évitent l'ambiguïté d'un objectif qualitatif comme « performant sur mobile ». L'auteur distingue SLO et SLA, ces derniers ajoutant des pénalités financières, rarement pertinentes entre collègues d'une même entreprise.
- *Monitoring / alerting* : comment on détectera en production un échec à tenir les SLO — panne totale, dégradation de performance, pics anormaux.
- *Calendrier* : découpage en jalons produisant des livrables utiles aux parties prenantes, avec la recommandation de commencer par une UI à données factices pour détecter tôt les malentendus sur les besoins. L'auteur renvoie à l'article classique de Joel Spolsky sur l'estimation logicielle.
- *Interfaces* : ce que voient les utilisateurs ou les systèmes clients — esquisses d'UI, sémantique d'API/CLI, format de fichier — illustré ici par un exemple de refactor Go introduisant une interface `Store` pour découpler le serveur de l'implémentation Postgres.
- *Dépendances / infrastructure* : langage, hébergement, stockage. L'auteur souligne qu'il faut concentrer l'attention sur les dépendances difficiles à changer plus tard (langage, backend de stockage) plutôt que sur celles qu'on peut remplacer facilement (un service tiers d'envoi d'e-mails, par exemple).
- *Sécurité* : quelles menaces ont été envisagées, quelle est la surface d'attaque, où se situent les frontières de confiance entre systèmes moins et plus privilégiés — documenter le raisonnement même si l'on juge le risque faible, car cela peut alerter un relecteur sur un angle mort.
- *Vie privée* : quelles données sensibles sont traitées, combien de temps elles sont conservées, qui y a accès, comment elles sont protégées (chiffrement au repos et en transit).
- *Aspects légaux* : conformité réglementaire dans les domaines sensibles (finance, santé), risques contractuels, choix de licence open source le cas échéant.
- *Logging* : quels événements critiques sont journalisés, niveaux de logs, lieu et durée de conservation, contrôle d'accès, données sensibles à exclure des journaux.
- *Problèmes ouverts* : consigner explicitement les points non résolus — le problème, les options envisagées, la prochaine étape — avec un exemple sur le dimensionnement de la RAM d'un cache, où l'auteur chiffre le coût-temps de tester plusieurs configurations face au coût de la RAM elle-même.
- *Problèmes résolus* : dès qu'un problème ouvert est tranché, on le déplace dans cette section en conservant la trace de la discussion complète, pour la postérité.
- *Alternatives envisagées* : répondre par anticipation à la question « pourquoi pas X ? », en quelques lignes seulement — l'auteur juge excessif de documenter en détail chaque option rejetée.

L'article se termine en annonçant qu'un second billet, non traité ici, abordera les techniques pour faire aboutir la revue collective du document sans qu'elle ne dégénère en débats stériles.

## Pourquoi ça compte
La qualité des design docs conditionne directement le temps perdu en reprises d'implémentation et la fluidité de la coordination inter-équipes ; cette grille de lecture (quoi inclure, à quel niveau de détail, selon quel critère de risque) est directement réutilisable pour structurer ou auditer les documents de conception dans n'importe quelle organisation technique.
