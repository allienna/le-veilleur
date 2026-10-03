---
title: "Introducing Strands Decider 2B: a small, open source, decision model"
date: 2026-10-03
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fstrandsagents.com%2Fblog%2Fintroducing-strands-decider%2F%3Futm_source=tldrai/1/010001a0fccd7a72-672389f9-e11b-4cda-ac15-a4ea0d841b32-000000/pOWVv0Hl4FiM5tF2fsSnWSbws5-VJU5bmUTu1vvy0eM=452"
keywords: ["modèle de décision", "agents IA", "open source", "Strands", "latence", "LoRA"]
theme: "IA"
tone: "news"
used_in: ["2026-10-03"]
---

## Résumé
L'équipe Strands présente Strands Decider 2B, un petit modèle de décision open source de 2 milliards de paramètres, conçu pour choisir rapidement entre des options plutôt que pour générer du texte libre. Contrairement aux LLM classiques, ce type de modèle (dit "système 1") répond en quelques dizaines de millisecondes, fournit un score de fiabilité calibré, et s'intègre nativement dans le SDK Strands Harness pour piloter des workflows agentiques (routage de modèles, sélection d'outils, garde-fous, etc.). Le modèle, ses poids, ses données d'entraînement et son code sont publiés en open source sur GitHub et Hugging Face.

## Points clés
- Strands Decider 2B est un modèle de décision (2 milliards de paramètres) qui choisit entre des options ou attribue des scores numériques, plutôt que de générer du texte libre comme un LLM.
- Architecture : un torse LLM pré-entraîné (Qwen3.5-2B) privé de sa tête de génération de texte (LM head), remplacée par une "pointer head" légère (~1 million de paramètres) qui score les options ; le torse est affiné via un adaptateur LoRA de rang 16.
- Performances : 3ème sur 33 modèles de la classe 2B en précision/calibration (Brier score) sur JevBench, avec une latence médiane d'environ 115ms sur GPU (RTX 3090) et 153ms sur MacBook M3.
- Cas d'usage : routage de modèles, sélection d'outils, évaluations, garde-fous (guardrails), gestion de mémoire/contexte, classification de politiques, et agents hybrides combinant LLM (décisions complexes) et modèles de décision (décisions simples et rapides).
- Démonstration concrète via le système d'intervention de Strands (`InterventionHandler`) qui intercepte un appel d'outil avant son exécution et peut le laisser passer, le refuser, demander confirmation humaine, ou guider le modèle avec un retour.
- Le modèle, le code, les données d'entraînement et les scripts sont intégralement open source (GitHub et Hugging Face).

## Analyse approfondie
Plus tôt cette année, nous avons annoncé strands-labs, un espace pour expérimenter concrètement avec les approches de pointe de l'IA agentique. Aujourd'hui, nous sommes ravis d'ajouter Strands Decider 2B : un petit modèle de décision optimisé pour l'expérimentation rapide, le développement local et l'innovation.

Strands decider appartient à une nouvelle classe de modèles de décision, ou modèles "système un", un type de modèle qui suscite beaucoup d'attention depuis le lancement de Jev par TypeSafe AI plus tôt ce mois-ci. À la différence des LLM qui peuvent générer une sortie arbitraire, les modèles de décision sont conçus pour choisir parmi des ensembles d'options (par exemple « La phrase "allume les lumières" concerne-t-elle la machine à café ? Oui ou non. », « Dans quelle langue est la phrase "sihamba ngokushesha" ? Anglais, zoulou ou néerlandais. ») et attribuer des scores numériques simples (par exemple « La phrase "c'est le meilleur document que j'ai jamais lu" exprime-t-elle un sentiment positif ? Entre 0 et 1. »).

En échange de cette réduction de flexibilité, les modèles de décision sont plus rapides et plus performants à taille égale, produisent toujours une réponse parmi les options proposées, et peuvent fonctionner avec une latence très faible.

Le revers de la médaille est que cette approche (générer toutes les sorties en une seule passe parallèle) les rend nettement moins capables de résoudre des problèmes complexes que les modèles de raisonnement, et leur incapacité à générer du texte les rend inadaptés au codage, aux chatbots, au résumé de documents et à d'autres tâches courantes des LLM.

De plus, les modèles de décision attribuent à chaque décision un score de fiabilité de haute qualité (c'est-à-dire « à quel point puis-je être sûr que ce oui/non est correct ? »), ce qui n'est pas disponible via les API d'inférence des LLM de pointe. Ils permettent également de poser très efficacement plusieurs questions sur le même prompt. Cette combinaison de propriétés les rend parfaits pour piloter les types de workflows agentiques que nous voyons de nombreux développeurs construire avec le Strands Harness SDK, et le Strands harness récemment lancé. Nous nous attendons à ce que cette classe de modèles mène à beaucoup d'innovations intéressantes en IA agentique dans les semaines, mois et années à venir.

Strands Decider 2B est notre première contribution à cette innovation. C'est un modèle de 2 milliards de paramètres, adapté pour fonctionner sur un CPU ou un GPU local, capable de renvoyer des réponses à des questions pertinentes en quelques dizaines de millisecondes. Sa précision et sa calibration sont compétitives par rapport aux autres modèles de cette classe que nous connaissons. Nous avons publié `strands-decider-2b` en open source sur GitHub, avec les poids sur Hugging Face, ainsi que toutes les données d'entraînement et les scripts que nous avons utilisés pour construire le modèle, en faisant un excellent point de départ pour votre propre parcours d'innovation.

### Architecture du modèle

L'idée centrale consiste à prendre le torse d'un LLM pré-entraîné (Qwen3.5-2B) et à retirer la tête de génération de langage (LM head), lui enlevant ainsi sa capacité à générer du texte. La LM head est remplacée par une "pointer head" qui score les réponses proposées par le torse pour chaque option. Elle procède en comparant l'état caché à chaque position d'option avec l'état caché à la position `<answer>`. Cette tête est plutôt petite, à peine plus d'un million de paramètres au total. Le torse est affiné avec un adaptateur LoRA de rang 16.

*Figure 1 : L'architecture de Strands Decider 2B.*

En parcourant le dépôt, vous constaterez qu'il s'agit de la deuxième itération majeure de l'architecture. La première était similaire, mais utilisait une "slot head" dont nous avons constaté qu'elle performait nettement moins bien. En réalité, le modèle que nous publions aujourd'hui est la v19, avec de nombreuses itérations sous le capot. Tout ce que nous avons changé à chaque version est documenté dans le dépôt, et vous pouvez suivre le travail que nous avons effectué.

### Quelles sont ses performances ?

Pour les modèles de ce type, nous nous intéressons à trois objectifs de performance : la précision (la qualité des réponses), la calibration (la fiabilité des scores de confiance) et la latence (la rapidité de la prise de décision). Nous avons mesuré les deux premiers ensemble : la précision sur l'ensemble public de JevBench, et la calibration via le score de Brier sur ce même ensemble. Nous avons constaté que `strands-decider-2b` performe bien en précision et en calibration (3ème sur 33 dans la classe 2B, et 1er sur 30 en excluant les modèles juste au-dessus de 2B). À mesure que nous faisons évoluer l'architecture, nos scores s'améliorent, et nous avons beaucoup d'idées pour de futures améliorations. Nous espérons que la communauté se joindra à nous, dans l'esprit de Strands labs, pour apporter ses propres idées nouvelles.

*Figure 2 : Précision et calibration (score de Brier) au fil de la trajectoire d'entraînement. À mesure que l'architecture évoluait au travers des versions successives, les deux métriques se sont améliorées sur l'ensemble public de JevBench.*

En matière de latence, `strands-decider-2b` peut prendre des décisions locales en une médiane d'environ 115ms sur du matériel largement disponible. Le temps nécessaire pour décider dépend de la taille de la tâche, augmentant à peu près linéairement à mesure que la taille de la tâche s'accroît. Les résultats présentés ici concernent une Nvidia RTX 3090 locale, mais les performances sur un MacBook M3 ne sont pas beaucoup moins bonnes, avec une latence médiane d'environ 153ms pour les petites tâches. Comme pour la précision et la calibration, nous avons beaucoup d'idées pour nous améliorer ici, notamment pour réduire le plancher.

*Figure 3 : Latence de décision en fonction de la taille de la tâche (en tokens), mesurée sur une Nvidia RTX 3090 locale avec la v18 du modèle. La latence augmente à peu près linéairement avec la taille de la tâche.*

### Pourquoi 2B ?

Nous avons choisi de proposer Strands decider sous forme de petit modèle pour deux raisons. La première est que nous voulons encourager l'expérimentation. Vous pouvez utiliser, et même entraîner, `strands-decider-2b` sur du matériel que vous possédez déjà. Cela rend les essais faciles, rapides et peu risqués. La seconde est que deux milliards de paramètres au total semblent constituer une sorte de point idéal : suffisamment petit pour l'expérimentation, suffisamment grand pour accomplir un travail significatif. Strands decider réussit par exemple 100% des tâches faciles de JevBench, et ces types de problèmes correspondent bien à certains des problèmes plus simples que nous voyons les gens résoudre avec des agents.

### Que puis-je faire avec Strands decider ?

Tout ce que vous voulez ! Plus sérieusement, nous observons un succès précoce de l'usage de cette classe de modèles pour le routage de modèles, la sélection d'outils, les évaluations, les garde-fous (guardrails), la mémoire, la gestion de contexte et la classification de politiques. Nous avons également vu des innovations intéressantes autour de la construction d'agents hybrides, utilisant les LLM pour prendre les décisions les plus difficiles et les modèles de décision pour les décisions simples et routinières, réduisant ainsi coût et latence. Nous voyons des expérimentations combinant des modèles de décision avec des langages de workflow fixes pour construire un autre type de workflow hybride. Certains utilisent également ce genre de modèles pour jouer à des jeux, automatiser des tâches, naviguer dans des labyrinthes, et plus encore. La vitesse d'innovation dans ce domaine est stupéfiante.

### L'essayer

Le moyen le plus simple de démarrer est via la CLI `strands-decider`.

#### Question à choix

Vous pouvez demander au modèle de choisir en fonction d'un état et d'une question.

Exemple de sortie :

Dans cette sortie, on peut voir que le modèle prédit `billing` comme la réponse ayant le score de probabilité le plus élevé.

Le dépôt inclut également des exemples utilisant `strands-decider-2b` au sein d'un agent Strands, sous `examples/strands/`. L'agent lui-même fonctionne localement, se connecte à Strands decider également exécuté localement, puis utilise le LLM par défaut d'Amazon Bedrock.

C'est un scénario volontairement restreint. L'agent dispose de l'outil de démonstration (obligatoire) `get_weather` et d'un prompt système qui le rend délibérément zélé, si bien que lorsque l'utilisateur demande « Quel temps fait-il ? » sans préciser où, l'agent devine une ville et appelle l'outil quand même. Cependant, avant que cet appel ne s'exécute, `strands-decider-2b` lit la conversation et l'appel d'outil proposé et répond à deux questions oui/non à ce sujet : ces valeurs d'arguments sont-elles ancrées dans quelque chose que l'utilisateur a réellement dit (indice : non !) et est-ce trop tôt pour appeler cet outil de toute façon. Quelques lignes de Python transforment les prédictions en décision, et l'agent retourne alors demander quelle ville était visée plutôt que de rapporter avec assurance le temps qu'il fait nulle part en particulier.

Le schéma ici est le système d'intervention de Strands. Nous utilisons l'`InterventionHandler` avec une méthode `before_tool_call`, le transmettons à `Agent(interventions=[...])`, et il s'exécute avant que tout outil ne soit exécuté. Ce qu'il retourne est une action typée : `Proceed`, `Deny`, `Confirm` (s'arrêter et demander à une personne), ou `Guide`, qui rend la main au modèle avec un retour plutôt que de bloquer purement l'appel. Ce handler existant est une classe Python et Strands n'a aucun avis sur ce qu'elle contient à l'intérieur, de sorte que la même structure vaut que vous appeliez notre modèle de décision, une politique Cedar, ou un autre agent. (Il existe des hooks équivalents autour de l'appel au modèle et autour de l'invocation entière.) Cet exemple est une illustration plutôt qu'une recommandation, donc les questions, le seuil et la politique ont tous été choisis à la main. Le point important est qu'une décision aussi peu coûteuse peut se situer dans un chemin où un appel à un LLM ne le pourrait jamais.

L'équipe Strands travaille sur des bibliothèques pour l'intégration des modèles de décision, donc surveillez le dépôt pour de prochaines mises à jour.

### Conclusion

Vous pouvez télécharger, utiliser ou construire à partir de `strands-decider-2b` dès aujourd'hui. Toutes les données sont disponibles, ainsi que tout ce dont vous avez besoin pour démarrer. Vous pouvez récupérer le code sur GitHub, et les derniers snapshots sur Hugging Face. Maintenant, allez expérimenter !

## Pourquoi ça compte
Ce lancement illustre une tendance émergente dans l'IA agentique : déléguer les décisions simples et fréquentes (routage, sélection d'outils, garde-fous) à de petits modèles spécialisés, rapides et calibrés, plutôt qu'à des LLM coûteux — une architecture hybride à suivre pour quiconque conçoit des systèmes d'agents en production.
