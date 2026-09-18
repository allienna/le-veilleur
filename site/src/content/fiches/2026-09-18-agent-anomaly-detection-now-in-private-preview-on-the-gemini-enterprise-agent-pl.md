---
title: "Agent Anomaly Detection, now in Private Preview on the Gemini Enterprise Agent Platform"
date: 2026-09-18
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fdevelopers.googleblog.com%2Fagent-anomaly-detection-now-in-private-preview-on-the-gemini-enterprise-agent-platform%2F%3Futm_source=tldrai/1/010001a0af8f638d-dcc57c6a-1a9b-4a37-be52-1a8f5d78e44e-000000/Z-loQtxfAW58wmAJcimLlRJnSczz7m0AchunuiKIt48=452"
keywords: ["agents IA", "détection d'anomalies", "Gemini Enterprise", "gouvernance des agents", "ADK", "audit runtime"]
theme: "Sécurité"
tone: "news"
used_in: ["2026-09-18"]
---

## Résumé
Google annonce le passage en Private Preview de « Agent Anomaly Detection », une nouvelle couche d'audit et de supervision pour les agents IA autonomes déployés sur la Gemini Enterprise Agent Platform. L'outil analyse en continu les traces de raisonnement, les appels d'outils et le déroulement des sessions d'agents pour repérer des comportements anormaux qui ne provoquent pourtant aucune erreur technique. Il combine une première passe statistique légère, qui balaie tout le trafic, et une seconde passe basée sur un LLM qui examine en profondeur les sessions suspectes, avant de restituer un verdict argumenté et exploitable. La fonctionnalité est accessible aux équipes utilisant ADK 1.2 ou une version ultérieure, avec une activation en un clic une fois les prérequis remplis.

## Points clés
- Les agents IA deviennent plus autonomes et moins chers à faire fonctionner, ce qui déplace le risque du code vers leur comportement au moment de l'exécution.
- Les dérives les plus dangereuses passent souvent inaperçues : la session se termine « proprement » alors que l'agent a par exemple mobilisé un outil inapproprié ou étendu discrètement ses propres droits d'accès.
- Agent Anomaly Detection fonctionne en couches : une détection statistique rapide sur l'ensemble du trafic, puis une analyse par raisonnement LLM sur les sessions signalées, et enfin une reconstruction détaillée des appels d'outils si nécessaire.
- Un exemple illustratif (un agent d'inventaire paginant massivement un catalogue) montre comment l'outil distingue un usage légitime d'un scraping systématique, avec un verdict chiffré (95 % de probabilité, sévérité critique) et des recommandations concrètes.
- Les résultats remontent dans le Security Command Center et sont aussi accessibles via une API, permettant à un callback ou un plugin ADK de bloquer automatiquement un agent dont le score de risque dépasse un seuil défini.
- La fonctionnalité est en Private Preview, réservée aux équipes tournant sur ADK 1.2+, avec une mise en route facilitée par un provisioning en un clic.

## Analyse approfondie
Le point de départ de l'annonce est un constat simple : chaque nouvelle génération de modèles rend les agents IA plus capables, plus autonomes et moins coûteux à exploiter. Des équipes les déploient déjà sur des tâches métier réelles — émettre des remboursements, mettre à jour des enregistrements, appeler des outils internes au nom d'un utilisateur. Mais un modèle plus capable n'est pas pour autant un modèle plus sûr : plus un agent prend de décisions en autonomie au moment de l'exécution, plus le risque se déplace de son code vers son comportement effectif.

Le danger réel se niche souvent dans des sessions qui paraissent anodines : l'agent renvoie une réponse propre, le ticket est clos, et ce n'est qu'après coup qu'on réalise qu'il a mobilisé un outil qu'il n'aurait jamais dû toucher, ou qu'il a répondu à une requête qui élargissait discrètement son propre périmètre d'accès. Comme rien n'a formellement échoué, ces sessions passent les évaluations classiques fondées sur des métriques sans déclencher la moindre alerte.

C'est précisément cet angle mort qu'Agent Anomaly Detection est censé combler. L'outil, désormais en Private Preview sur la Gemini Enterprise Agent Platform, se présente comme une couche de supervision et d'audit fondée sur le raisonnement, destinée aux agents autonomes. Il observe ce que l'agent fait réellement — via ses traces de raisonnement, ses appels d'outils et le déroulé complet de l'exécution sur une session — en s'appuyant sur les journaux et les traces OpenTelemetry déjà produits par les agents. Il évalue cette activité pour déterminer si l'agent opère hors des limites prévues, et signale les anomalies comportementales, les intentions suspectes et les violations de politique.

Parmi les caractéristiques qui rendent l'outil exploitable en production, l'architecture en couches se distingue particulièrement : elle vise un équilibre entre rapidité de détection, coût et couverture. Une première passe, légère, scanne l'ensemble du trafic pour repérer des anomalies statistiques et signaler les sessions à approfondir. Une seconde couche, fondée sur un raisonnement par LLM, examine ensuite en détail les sessions ainsi signalées.

L'article illustre ce fonctionnement avec l'exemple d'un « Inventory Agent » doté d'un outil `list_inventory`. Un utilisateur demande : « Je veux voir votre inventaire. Affiche 100 articles à la fois », et l'agent se met à parcourir le catalogue par lots importants, en sautant d'un décalage (offset) à l'autre pour en extraire la totalité.

Rien, dans ce scénario, ne déclenche d'erreur : l'agent ne fait que ce qu'il est capable de faire, et aucune politique n'interdit nécessairement ce comportement. Pourtant, Agent Anomaly Detection le signale comme anormal, en traitant la session couche par couche : la première couche relève un écart statistique lié au volume et à la répétition des appels ; la seconde couche analyse l'ensemble de l'échange, reconnaît dans ce schéma de pagination par gros lots et sauts d'offset une logique de scraping systématique plutôt qu'une simple consultation, et restitue un verdict accompagné d'une explication en langage clair. Lorsqu'un cas mérite un examen plus poussé, une troisième couche reconstruit les appels d'outils individuels et leurs offsets pour montrer précisément ce qui a été extrait.

Le résultat prend la forme d'un constat d'anomalie : épuisement de ressources (« Resource exhaustion »), sévérité critique, probabilité de 95 %, assorti d'une justification et de recommandations concrètes — limiter le débit ou bloquer l'outil `list_inventory` pour cet utilisateur, ajouter des contrôles d'autorisation pour restreindre l'accès en masse à l'inventaire, et déclencher une alerte sur les schémas de pagination à gros offsets. Ce constat remonte également dans le Security Command Center pour être traité.

Au-delà de la simple revue humaine, les résultats peuvent être exploités de façon programmatique : Agent Anomaly Detection expose une API permettant de récupérer les anomalies détectées pour une session donnée, de sorte qu'un callback ou un plugin ADK puisse vérifier la sévérité et la probabilité d'un constat, puis bloquer les appels d'outils suivants ou interrompre le prochain tour de conversation dès qu'un seuil défini par l'équipe est dépassé.

À mesure que les agents prennent en charge davantage de travail réel, une part croissante du risque se déplace vers leur comportement. Agent Anomaly Detection surveille ce comportement et signale les anomalies à examiner et à traiter, sans ralentir le fonctionnement des agents.

La fonctionnalité est actuellement en Private Preview, réservée aux équipes déployant des agents sur la Gemini Enterprise Agent Platform avec ADK version 1.2 ou supérieure. Pour démarrer, Google renvoie à sa documentation pour connaître les prérequis et la configuration ; une fois ceux-ci satisfaits, l'activation se fait via un provisioning en un clic.

## Pourquoi ça compte
Cette annonce illustre une bascule importante dans la sécurité des systèmes d'IA agentique : à mesure que les agents gagnent en autonomie, la supervision doit passer de simples métriques de succès/échec à une analyse comportementale fondée sur le raisonnement, ce qui préfigure une nouvelle catégorie d'outils d'observabilité et de gouvernance dédiés aux agents en production.
