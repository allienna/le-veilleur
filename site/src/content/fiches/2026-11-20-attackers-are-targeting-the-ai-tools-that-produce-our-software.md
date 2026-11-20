---
title: "Attackers are targeting the AI tools that produce our software"
date: 2026-11-20
url: "https://leadershipintech.com/links/23748/3d78f33c-7ca0-4e03-9c70-68e56918a4cd/email"
keywords: ["sécurité", "chaîne d'approvisionnement", "outils IA", "Claude Code", "zero trust", "MCP"]
theme: "Sécurité"
tone: "opinion"
used_in: ["2026-11-20"]
---

## Résumé
Le 29 octobre 2026, des versions malveillantes de l'extension Claude Code d'Anthropic ont circulé pendant environ 11 heures sur la marketplace de Cursor, exposant potentiellement jusqu'à 5 000 utilisateurs à de la collecte de données et à une tentative de porte dérobée persistante. S'appuyant sur cet incident, Thoughtworks alerte les dirigeants : les assistants de codage IA, éditeurs et serveurs MCP font désormais partie intégrante de la chaîne d'approvisionnement logicielle et sont devenus une cible privilégiée de groupes d'attaquants motivés par le profit, comme l'illustrent les compromissions de Trivy et LiteLLM documentées par le cabinet Wiz. L'article rappelle que cette logique n'est pas nouvelle (parallèle avec SolarWinds en 2020) mais que les outils IA occupent aujourd'hui une position stratégique inédite, proche du code, des identifiants et des pipelines de déploiement. Il propose six mesures pratiques pour établir la confiance envers ces outils et se préparer à une éventuelle compromission.

## Points clés
- Incident Cursor/Claude Code (29 octobre 2026) : extension malveillante disponible pendant 11 heures, jusqu'à 5 000 utilisateurs potentiellement touchés, collecte d'informations machine et tentative d'installation d'une porte dérobée persistante.
- Les outils de développement (assistants IA, éditeurs, serveurs MCP) ont accès au code source, aux sessions authentifiées, aux identifiants cloud et aux pipelines de build/déploiement, ce qui en fait des cibles à fort rendement.
- Le groupe d'attaquants TeamPCP, suivi par Wiz, a compromis des outils comme Trivy (scanner de sécurité) et LiteLLM (passerelle IA), exploitant les identifiants volés en quelques heures puis explorant les environnements cloud des victimes.
- Parallèle avec la brèche SolarWinds (2020) : la stratégie de compromission de la supply chain logicielle précède l'IA, mais les outils de codage IA occupent désormais une position stratégique nouvelle.
- Six mesures recommandées : zero trust sur les dépendances, appropriation de la supply chain par les équipes d'ingénierie, contrôle des mises à jour, limitation du rayon d'impact (blast radius), préparation à la réponse à incident, et surveillance continue des environnements de développement.

## Analyse approfondie
*Les outils de codage IA font désormais partie de notre chaîne d'approvisionnement logicielle. Nous partageons six mesures pratiques qui peuvent aider à répondre à ce risque.*

Pendant environ 11 heures, le 29 octobre 2026, des versions malveillantes de l'extension Claude Code d'Anthropic ont été disponibles sur la marketplace de Cursor, affectant potentiellement jusqu'à 5 000 utilisateurs. Le code malveillant collectait des informations sur les machines des développeurs et tentait d'installer une porte dérobée pour un accès distant persistant.

Si c'étaient vos développeurs, quels systèmes un attaquant pourrait-il atteindre ? C'est le point que les dirigeants doivent retenir de cet incident. Les assistants de codage, les éditeurs, les serveurs MCP et leurs extensions font partie de votre chaîne d'approvisionnement logicielle, et les attaquants l'ont remarqué. Les agents IA d'aujourd'hui peuvent exécuter des commandes shell, lire des secrets locaux et appeler des services externes de manière autonome, ce qui rend un seul outil compromis potentiellement très dangereux.

### Pourquoi les outils de développement sont une cible si attrayante

Le poste de travail d'un développeur contient du code source, des sessions authentifiées, des identifiants cloud et des connexions vers les systèmes de build et de déploiement. Pour certains développeurs, ces connexions atteignent des systèmes de production contenant des données sensibles. Compromettre un seul outil permet d'accéder à un endroit très précieux.

Le modèle économique est simple. Les attaquants obtiennent un accès, déterminent ce qu'il permet de débloquer, puis le monétisent via du vol de code, de l'extorsion, des partenariats de ransomware ou du minage de cryptomonnaie.

Des chercheurs du cabinet de sécurité Wiz ont suivi un groupe d'attaquants de ce type, appelé TeamPCP. Ils ont constaté qu'il avait visé des outils de développement, dont Trivy, un scanner de sécurité logiciel, et LiteLLM, une passerelle pour l'usage de l'IA dans le code qui facilite l'accès aux modèles de langage et la limitation des coûts en tokens. Dans chaque cas, les identifiants volés ont été exploités en quelques heures, suivis d'une exploration des environnements cloud des victimes. Un outil de développement populaire constitue un moyen efficace d'atteindre de nombreux environnements à la fois.

Cette stratégie précède l'IA : en 2020, l'énorme brèche SolarWinds a montré comment une seule mise à jour de confiance pouvait ouvrir la porte à des milliers de clients. Ce qui a changé, c'est que les outils de codage IA occupent désormais cette position stratégique, proches des développeurs, du code, des commandes et des services qui livrent le logiciel. Cela en fait une cible alléchante pour des cyberattaquants cherchant à gagner de l'argent rapidement.

### Les outils de développement détiennent les clés, alors traitons-les comme tels

Cela nous amène à la question centrale pour les organisations : comment établir la confiance dans les outils IA dont dépend de plus en plus la livraison logicielle ?

Six mesures pratiques aident les organisations à établir cette confiance et à se préparer à une compromission.

#### 1. Appliquer le zero trust aux dépendances

Chez Thoughtworks, notre approche par défaut raisonnable consiste à appliquer une logique de zero trust à l'infrastructure de build et de livraison. Pour les outils de développement, cela signifie un zero trust pour les dépendances : établir la confiance par des preuves, n'accorder que l'accès nécessaire et continuer à vérifier le comportement du composant.

- **La confiance n'est pas tout ou rien :** Cela ne signifie pas qu'on ne peut rien faire confiance. Un composant maintenu par une équipe connue, avec du code revu et un processus de publication maîtrisé, donne davantage de raisons d'avoir confiance qu'un paquet inconnu installé sans contrôle.
- **Tout vérifier :** Le processus de build, la marketplace et le mécanisme de mise à jour affectent tous l'intégrité de ce qui arrive sur votre machine.

#### 2. S'approprier sa chaîne d'approvisionnement logicielle

Les équipes de développement doivent assumer la responsabilité première de la chaîne d'approvisionnement du logiciel qu'elles construisent, y compris les assistants IA, les éditeurs, les extensions et les outils de build utilisés pour le produire.

- **Traiter l'adoption d'un outil comme une décision d'ingénierie :** Comprendre pourquoi un outil est nécessaire, d'où il vient, quel accès il requiert et comment il sera maintenu avant de l'adopter.
- **Garder la responsabilité au sein de l'équipe de livraison :** Les orientations et approbations données par les équipes de sécurité centrales sont importantes, mais elles ne transfèrent pas la responsabilité de première ligne ; les spécialistes de la sécurité fournissent des garde-fous et des standards partagés, tandis que les équipes d'ingénierie gèrent le risque au quotidien.

#### 3. Contrôler les mises à jour

Traitez les mises à jour des outils ayant accès au code et aux identifiants comme des changements apportés à un environnement sensible.

- **Utiliser l'épinglage des dépendances lorsque c'est pertinent :** Utiliser des versions éprouvées, des déploiements progressifs ou une courte fenêtre de revue avant de déployer des paquets nouvellement publiés.
- **Vérifier l'intégrité :** Contrôler les signatures de paquets et la provenance partout où ces mécanismes sont pris en charge.
- **Maintenir une voie accélérée :** S'assurer que les contrôles de mise à jour incluent un chemin accéléré pour les correctifs de sécurité urgents et vérifiés.

#### 4. Limiter le rayon d'impact

Partez du principe qu'un outil ou une extension finira par être compromis, et concentrez-vous sur la limitation de ce qu'il peut atteindre.

- **Éliminer les privilèges excessifs :** Faire fonctionner les outils de développement sans droits d'administrateur inutiles, séparer l'accès de développement quotidien des permissions de production, et remplacer les clés à longue durée de vie par des identifiants à portée restreinte et de courte durée.
- **Faire respecter des limites :** Utiliser des sandboxes et des environnements de développement managés avec des contrôles explicites sur les fichiers, les identifiants et les connexions réseau sortantes - couvrant à la fois l'éditeur et les commandes exécutées par un agent IA.

Faites une modélisation des menaces pour explorer l'impact d'un composant compromis. Pourrait-il modifier une copie de travail locale du code ? Pousser des changements vers un dépôt, altérer un pipeline de déploiement ou atteindre des données clients ? Cela devrait révéler des opportunités pour durcir des configurations trop permissives.

#### 5. Être prêt à réagir

Intégrez les outils de développement dans les plans de réponse aux incidents existants de votre organisation avant qu'un incident ne vous force à improviser.

- **Répéter le scénario :** Mener des exercices sur table avec les équipes d'ingénierie, de plateforme et de sécurité pour s'entraîner à identifier les machines concernées, isoler les terminaux, préserver les preuves et révoquer les jetons et sessions exposés.
- **Planifier une remédiation en profondeur :** Le simple fait de désinstaller une extension malveillante laisse souvent des mécanismes de persistance en place, comme on l'a vu dans l'incident Cursor ; prévoyez donc des procédures pour des remises à plat complètes des postes de travail, des réinstallations et des audits de dépôts/cloud.
- **Réinjecter les enseignements :** Utiliser chaque incident ou quasi-incident pour renforcer les processus d'approbation des outils, les limites d'accès et les règles de détection.

#### 6. Surveiller l'environnement de développement

Mettez en place une surveillance de sécurité autour des machines des développeurs et des services auxquels elles accèdent. Des indicateurs utiles peuvent inclure des changements inattendus de clés SSH, de nouveaux mécanismes de démarrage, un accès inhabituel aux identifiants et des processus d'éditeur créant des tunnels vers des destinations inconnues.

Cela devient puissant pour la détection lorsque les signaux des terminaux sont corrélés avec l'identité, le dépôt et l'activité cloud. Un processus inhabituel sur un ordinateur portable devient plus significatif lorsqu'il est suivi d'une authentification inconnue, d'un accès massif à un dépôt ou de changements apportés à un pipeline de livraison. Les alertes ont besoin d'une responsabilité claire et de répondants qui comprennent les flux de travail normaux de l'ingénierie. Établissez une télémétrie de sécurité autour des machines des développeurs et des services en aval auxquels elles accèdent.

- **Surveiller les anomalies des postes de travail :** Alerter sur des changements inattendus de clés SSH, de nouveaux mécanismes de démarrage, un accès inhabituel aux fichiers d'identifiants et des processus d'éditeur ouvrant des tunnels réseau vers des destinations inconnues.
- **Corréler entre systèmes :** Combiner les signaux des terminaux avec les journaux d'identité, de dépôt et de cloud : un processus local inhabituel devient prioritaire lorsqu'il est suivi d'une authentification inconnue, d'un clonage massif de dépôt ou de changements dans le pipeline CI/CD.

### Se préparer à la prochaine attaque de la chaîne d'approvisionnement

L'importance croissante des outils de codage IA fait de la sécurité des environnements de développement un enjeu business. Les outils IA se situent près du code, des identifiants et des connexions par lesquels les organisations livrent le changement. Se préparer, c'est comprendre cette position, contenir les conséquences d'une défaillance et disposer de la visibilité nécessaire pour intervenir avant qu'un outil compromis ne devienne une brèche d'entreprise plus large.

*Avertissement : les déclarations et opinions exprimées dans cet article sont celles de son ou ses auteur(s) et ne reflètent pas nécessairement les positions de Thoughtworks.*

## Pourquoi ça compte
Pour une veille sécurité/IA, cet article illustre de façon concrète comment les outils de codage IA (Claude Code, MCP, extensions d'éditeur) deviennent un vecteur d'attaque de la chaîne d'approvisionnement logicielle, avec des recommandations opérationnelles directement actionnables pour les équipes d'ingénierie et de sécurité.
