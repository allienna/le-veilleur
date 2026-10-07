---
title: "Fireworks Nexus"
date: 2026-10-07
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Ffireworks.ai%2Fnexus%3Futm_source=tldr%26utm_medium=newsletter%26utm_campaign=nexus/1/010001a111643ec8-81ad9ade-ccd3-42bd-9e5c-cead1c259ceb-000000/JijLLI5965pHed0ofwd6-g7Hv8nmgRPJDzgmgNO--XA=452"
keywords: ["routage de modèles", "inférence IA", "optimisation des coûts", "FireRouter", "modèles ouverts", "LLM"]
theme: "IA"
used_in: ["2026-10-07"]
---

## Résumé
Fireworks Nexus est une page produit présentant la plateforme d'inférence IA de Fireworks et son système de routage intelligent FireRouter, destinés aux entreprises qui veulent maîtriser leurs dépenses en IA à grande échelle. Le contenu met en avant la gestion fine des budgets par utilisateur, un routage dynamique entre modèles ouverts et fermés selon le meilleur rapport coût/qualité, ainsi qu'une infrastructure d'inférence désagrégée et hautement optimisée. Des témoignages clients (dont Sourcegraph) et des chiffres clés (plus de 40 000 milliards de tokens servis par jour, économies allant jusqu'à 72 %) viennent appuyer le positionnement du produit comme solution d'optimisation économique de l'IA en entreprise.

## Points clés
- FireRouter oriente chaque requête vers le modèle le plus rentable (ouvert ou fermé), selon des préférences de routage ajustables.
- La plateforme revendique un taux de cache hit supérieur à 95 % sur le trafic de code courant, avec facturation à moitié prix sur les tokens mis en cache.
- Les administrateurs définissent des plafonds de dépense par utilisateur via Settings, `firectl` ou l'API REST ; les ingénieurs voient leur propre limite avant de l'atteindre.
- Un témoignage anonyme évoque jusqu'à 72 % d'économies après avoir remplacé en interne un modèle Opus 4.8 par GLM-5.2, sans impact perçu sur la qualité.
- Fireworks sert plus de 40 000 milliards de tokens par jour avec zéro rétention de données, des options d'hébergement exclusivement aux États-Unis, et les certifications SOC 2, ISO 27001, ISO 42001, HIPAA.
- Nexus s'intègre à une gateway existante via LiteLLM Proxy, en laissant FireRouter gérer l'arbitrage coût/qualité.

## Analyse approfondie
Économies par PR fusionnée

Dépenses IA totales économisées

Tokens par seconde disponibles

Les administrateurs voient les dépenses, la limite et les dérogations de chaque utilisateur. Les ingénieurs voient les leurs avant d'atteindre le plafond. Définissez la limite une seule fois dans Settings, via `firectl`, ou via l'API REST.

Les ingénieurs conservent leurs outils et leur état de flow grâce au CLI FireConnect. Configuration en quelques minutes. Créez davantage de marge de tokens avec FireRouter, votre pilote automatique de modèles, ou fixez vous-même vos choix de modèles.

FireRouter évalue chaque requête et choisit le chemin le plus rentable entre modèles ouverts et fermés, selon des préférences ajustables. Les développeurs peuvent passer `--routing-preference` lors de l'activation d'un harness, ou envoyer l'en-tête `x-routing-preference` sur des appels individuels.

« Les modèles frontier nous ont menés au product-market fit ; maintenant nous poussons plus loin le rapport signal/bruit — plus de vrais bugs, moins de faux positifs. À notre échelle, c'est un problème d'entraînement, et Fireworks rend cela facile. »

« Fireworks a été un partenaire formidable dans la construction d'outils de développement IA chez Sourcegraph. Leur inférence de modèles rapide et fiable nous permet de nous concentrer sur le fine-tuning, la recherche de code alimentée par l'IA et le contexte de code approfondi, faisant de Cody le meilleur assistant de codage IA. Ils sont réactifs et avancent à un rythme impressionnant. »

« Le "tokenmaxxing" a eu son heure de gloire. Mais les équipes qui gagneront avec l'IA à partir de maintenant seront celles qui en feront plus pour moins cher, pas celles qui dépenseront le plus… Après avoir optimisé notre harness pour les modèles à poids ouverts, nous avons secrètement remplacé l'un de nos agents internes les plus utilisés, passant d'Opus 4.8 à GLM-5.2, et personne dans l'entreprise ne s'en est aperçu. Nous constatons désormais des économies de coûts allant jusqu'à 72 %. »

Fireworks a construit un moteur d'inférence entièrement désagrégé, optimisé à chaque couche, des kernels personnalisés à la gestion de la mémoire jusqu'au cache adaptatif. La plateforme sert désormais plus de 40 000 milliards (40T+) de tokens par jour à l'échelle mondiale, avec zéro rétention de données, des options d'hébergement exclusivement aux États-Unis, et les certifications SOC 2, ISO 27001, ISO 42001, HIPAA. Nous entretenons des accords commerciaux avec les principaux modèles frontier ouverts et proposons un accès dès le jour zéro (zero-day) avec des performances optimisées.

S'il est vrai que l'on peut configurer un routeur en un week-end, une « échelle » mal construite donne de moins bons résultats que l'absence totale de routage. Une étude d'Arize a démontré qu'une escalade naïve entre dix modèles obtenait de moins bons résultats que chacun des modèles pris individuellement. Le jugement, c'est la pile logicielle (the stack). Par exemple, Fireworks maintient un taux de cache hit supérieur à 95 % sur le trafic de code courant, et les entrées mises en cache sont facturées à moitié prix. FireRouter intègre ce taux de cache dans chaque décision.

Vous avez déjà une gateway ? Gardez-la. Nexus dispose d'une intégration documentée avec LiteLLM Proxy. Utilisez-la pour la politique, le fan-out et les mécanismes de repli (fallbacks), et laissez FireRouter prendre en charge l'arbitrage coût/qualité pour les tâches qui y transitent.

## Pourquoi ça compte
Ce contenu illustre un virage stratégique du marché de l'inférence IA en entreprise : après la course aux modèles « frontier », l'enjeu se déplace vers l'optimisation des coûts via le routage intelligent entre modèles ouverts et fermés — un signal pertinent pour suivre l'évolution économique des infrastructures d'IA en production.
