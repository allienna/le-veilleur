---
title: "Introducing Replit Missions | Replit"
date: 2026-11-19
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Freplit.com%2Fblog%2Fintroducing-replit-missions%3Futm_source=tldrai/1/010001a1ef123c23-e53c2623-adf2-4bba-9846-a9f68bce8542-000000/G9HjEQ0deNb6OyDaBNrNqrB80Et6UGjLp4F0Mpb41cQ=452"
authors: ["Replit"]
keywords: ["agents IA", "essaim d'agents", "Replit Missions", "automatisation", "monitoring applicatif"]
theme: "IA"
tone: "news"
used_in: ["2026-11-19"]
---

## Résumé
Replit lance Missions, une fonctionnalité qui permet de confier un objectif métier complexe à un essaim d'agents IA chargés de le planifier, le construire, le tester et l'itérer, dans un budget et des limites fixées par l'utilisateur. Pour en démontrer la puissance, Replit a utilisé Missions pour construire en deux jours, avec un budget de 3 000 $, DataCat, sa propre plateforme de monitoring applicatif, qui surpasse une plateforme tierce sur plusieurs métriques de performance. L'article présente aussi des benchmarks NumPy montrant que des essaims allant jusqu'à 32 agents obtiennent des gains de performance bien supérieurs à un agent seul, ainsi qu'un résultat state-of-the-art sur un benchmark de simulation e-commerce.

## Points clés
- Missions permet de définir un objectif de haut niveau (ex. « gagner nos 10 premiers clients grands comptes ») et de déléguer la planification, l'exécution et l'itération à un essaim d'agents, sous contrôle explicite du budget et des autorisations requises.
- Un juge IA indépendant vérifie les résultats par rapport aux critères de succès convenus ; la mission se termine quand ces critères sont atteints, ou s'arrête si le budget est épuisé avant.
- Démonstration interne : DataCat, une plateforme de monitoring construite en 2 jours pour 3 000 $, détecte une panne de base de données introduite volontairement en 38 secondes (objectif : 60 s) et absorbe une charge de 26 millions d'enregistrements et 4,4 millions de logs sans aucune perte de données.
- Comparée à une plateforme construite via /goal dans Claude Code à partir du même prompt, DataCat ingère les traces 5× plus vite et les métriques près de 2× plus vite, et réussit davantage de contrôles de compatibilité API, mais couvre moins de domaines produit et ingère les logs moins rapidement.
- Sur 13 tâches de benchmark NumPy, un essaim de 32 agents atteint des accélérations jusqu'à 19×, contre 4× pour un agent seul, illustrant l'intérêt de la parallélisation d'agents pour l'optimisation.
- Sur E-Commerce Bench, un agent Missions multiplie par environ 48 un capital de départ de 100 000 ¥, un résultat state-of-the-art plus de trois fois supérieur au meilleur score du classement public.

## Analyse approfondie
Aujourd'hui, nous lançons Replit Missions pour aider vos équipes à s'attaquer aux tâches complexes pour lesquelles elles n'ont jamais eu le temps ni les ressources : conquérir davantage de clients grands comptes, améliorer les performances d'un produit, ou remplacer un logiciel legacy. Vous définissez le résultat attendu, et Replit coordonne un essaim d'agents qui planifient, construisent, testent et itèrent pour l'atteindre, dans le budget et les limites que vous fixez.

Chez Replit, nous voulions explorer la possibilité d'internaliser le monitoring applicatif afin de réduire les coûts et de gagner en contrôle. Nous avons confié à Missions l'objectif de construire DataCat, une plateforme que nous pourrions personnaliser et exploiter sur notre propre infrastructure. En deux jours, avec un budget de 3 000 $, un essaim d'agents a construit des tableaux de bord, des alertes et un système de tracing applicatif, puis a testé la plateforme par rapport à des objectifs mesurables de performance et de fiabilité.

DataCat n'est qu'un exemple de ce que Missions permet de réaliser. Missions applique la même approche aux objectifs de votre équipe, sans que vous ayez besoin de construire ni de maintenir l'infrastructure complexe nécessaire pour coordonner un essaim d'agents.

## Commencez par les tâches complexes que vous n'avez pas la capacité de traiter

Vous pouvez démarrer avec une mission comme « gagner nos 10 premiers clients grands comptes payants ». Vous n'avez pas besoin de décider à l'avance quels secteurs cibler, quels acheteurs approcher, ou quel problème client résoudre en premier. Trouver et évaluer ces approches fait partie du travail que vous délégez.

Lors de la configuration, Missions pose des questions pour définir ce qu'est le succès. Qu'est-ce qui compte comme un client grand compte pour votre entreprise ? Les pilotes payants comptent-ils parmi les 10 premiers, ou le succès signifie-t-il des contrats annuels signés au-dessus d'un montant minimum ? Vos réponses déterminent les comptes que la mission priorise et la façon dont elle mesure les résultats.

## Gardez le contrôle du budget et des limites

Votre accord Missions fixe la limite de dépenses et détermine quelles actions nécessitent votre autorisation. Vous convenez également des compromis acceptables, comme proposer des pilotes payants ou des remises sur les contrats annuels.

Par exemple, vous pouvez plafonner les dépenses de la mission à 1 000 $ et exiger une approbation avant que l'agent ne contacte des prospects, ne partage une proposition, ne modifie des supports commerciaux destinés aux clients, ou ne prenne des engagements produit. Ces limites et exigences d'approbation restent en place à mesure que l'approche évolue.

## Laissez les agents planifier, construire et itérer

Pour votre mission de vente aux grands comptes, les agents peuvent rechercher des comptes cibles, construire des démonstrations sur mesure et préparer des prises de contact pour votre approbation. Les essaims leur permettent de travailler en parallèle, un agent effectuant une recherche sur les acheteurs tandis qu'un autre développe une démo. Une fois la prise de contact approuvée et envoyée, la mission peut revenir examiner quels comptes et quels messages génèrent des conversations qualifiées.

Ces réponses orientent le prochain cycle de travail. Les agents peuvent se concentrer sur un secteur montrant un intérêt plus marqué, affiner une démo autour d'une question récurrente des acheteurs, ou revoir un message qui obtient peu de réponses.

*La figure montre des essaims d'agents travaillant à l'amélioration de Replit Slides*

## Pourquoi les essaims d'agents rendent Missions plus puissant

*Le graphique montre les accélérations des benchmarks NumPy en fonction du nombre d'agents, avec Auto (Max) et Auto (Power).*

Les essaims d'agents donnent à Missions la capacité d'explorer plusieurs solutions à la fois, de partager leurs découvertes et de s'appuyer les uns sur les autres. Pour un problème comme l'optimisation des performances, les agents testent différentes implémentations en parallèle, utilisent les résultats partagés pour affiner leurs approches, et collaborent pour valider la correction des solutions à mesure qu'ils identifient des implémentations plus rapides.

Nous avons mis cela à l'épreuve sur 13 tâches de benchmark représentatives utilisant NumPy. Les agents ont exploré des implémentations alternatives, optimisé les schémas d'accès mémoire, et validé automatiquement la correction des résultats. Avec Auto (Max), un seul agent a obtenu des accélérations allant jusqu'à 4×. Un essaim de 16 agents a atteint 17×, et un essaim de 32 agents a atteint 19×. Auto (Power) a montré le même schéma : 2×, 7× et 9×, respectivement.

Le résultat le plus frappant est l'ampleur du progrès obtenu par les essaims. Explorer davantage d'approches en parallèle a permis à Missions de trouver des implémentations nettement plus rapides, démontrant le potentiel des essaims d'agents pour les travaux d'optimisation complexes.

## Suivez la progression et sachez comment les résultats sont vérifiés

Lors de la planification, vous choisissez ce que vous souhaitez suivre — blocages, mises à jour de progression, statut général — ainsi que leur fréquence : immédiatement, dans un résumé quotidien, ou hebdomadairement. Vous pouvez fermer votre ordinateur et laisser les agents cloud travailler. Missions envoie des mises à jour selon vos préférences et vous sollicite lorsqu'elle a besoin de votre avis.

Un juge IA indépendant vérifie les résultats par rapport aux critères de succès convenus, et les agents utilisent ses retours pour affiner leur travail. Une mission est marquée comme terminée lorsque ces critères sont atteints. Si le budget est épuisé avant, le travail s'arrête et le résultat reste non résolu.

Chaque fois que vous souhaitez y regarder de plus près, vous pouvez consulter le travail terminé, les tâches actives et les prochaines étapes, y compris tout ce qui attend votre approbation.

## Construire DataCat : notre propre plateforme de monitoring applicatif avec Missions

Nous avons utilisé Missions pour construire DataCat, une plateforme de monitoring applicatif que nous pouvons exploiter et personnaliser nous-mêmes. En 2 jours, avec un budget de 3 000 $, Missions a construit une plateforme fonctionnelle avec tableaux de bord, alertes et tracing applicatif, à partir des objectifs que notre équipe avait définis dans le Mission Contract, puis l'a testée par rapport à des objectifs mesurables de performance et de fiabilité.

Missions a également construit l'agent propre à DataCat, qui collecte les données de monitoring sur chaque serveur, ainsi que ses bibliothèques de tracing. DataCat peut fonctionner indépendamment de l'agent et des bibliothèques de la plateforme d'origine.

Pour tester si DataCat pouvait aider à diagnostiquer une panne, nous avons délibérément introduit un bug de base de données. DataCat a déclenché une alerte en 38 secondes, battant notre objectif de 60 secondes, et a retracé la panne jusqu'à la requête de base de données exacte et ses logs.

La mission a également construit des applications d'exemple pour un test de charge de trois heures. DataCat a stocké 26 millions d'enregistrements d'activité applicative et 4,4 millions d'entrées de logs sans aucune perte de données, tandis que les recherches et les alertes continuaient de fonctionner. Les 36 contrôles de correction des données et les 15 contrôles de fiabilité des alertes ont tous été validés.

La mission a comparé son code de monitoring avec la bibliothèque de tracing et l'agent de la plateforme d'origine. Dans des tests Node.js comparables, l'application a traité davantage de requêtes avec une surcharge processeur liée au monitoring plus faible. L'agent de DataCat consommait également moins de mémoire et rendait les logs consultables plus rapidement.

Nous avons ensuite comparé DataCat à une plateforme de monitoring construite avec le même prompt initial via /goal dans Claude Code. DataCat acceptait tous les types de données provenant de l'agent de la plateforme d'origine (logs, métriques, données hôte et traces), tandis que la version construite avec Claude Code n'acceptait que les logs. DataCat a réussi davantage de contrôles de compatibilité API et ingérait traces et métriques plus rapidement. La version Claude Code couvrait davantage de domaines produit et ingérait les logs plus rapidement. Le tableau ci-dessous résume les résultats.

| **Ce que nous avons testé** | **Résultats avec DataCat** |
|---|---|
| Temps de construction et budget | 2 jours, dans la limite d'un budget plafonné à 3 000 $ |
| Détection d'un bug de base de données introduit délibérément | 38 secondes, contre un objectif de 60 secondes |
| Gestion d'une activité soutenue | 26 millions d'enregistrements d'activité + 4,4 millions d'entrées de logs sur 3 heures, sans aucune perte de données |
| Précision des données et fiabilité des alertes | 51 contrôles sur 51 validés |
| Efficacité du monitoring dans les tests Node.js | 39 % de requêtes traitées en plus, avec 51 % de surcharge processeur liée au monitoring en moins |
| Compatibilité API (suite de tests distincte) | 51 contrôles sur 56 validés pour chaque moteur de stockage de DataCat, contre 45 sur 56 pour la version Claude Code |
| Ingestion des traces applicatives | 49 000 traces/seconde avec DataCat (Postgres), contre 9 800 pour la version Claude Code : 5× plus rapide |
| Ingestion des métriques | 405 100 points de métrique/seconde avec DataCat (Postgres), contre 224 600 pour la version Claude Code : près de 2× plus rapide |
| Mémoire de l'agent sous charge | 82-108 Mo pour l'agent de DataCat, contre 319 Mo pour l'agent de la plateforme d'origine (moyenne sur 240 secondes) |
| Délai avant que les logs soient consultables | 0,5 seconde avec l'agent de DataCat, contre 4,2 secondes avec l'agent de la plateforme d'origine (médiane) |
| Moteurs de stockage | 2 (Postgres et ClickHouse), contre 1 (SQLite) pour la version Claude Code |

Remarques : ces tests contrôlés n'établissent pas de comparaison de performance avec le service hébergé de la plateforme d'origine ni avec les systèmes de production de Replit. La comparaison Node.js a utilisé des charges de travail et un travail de monitoring équivalents.

La comparaison des builds a utilisé une exécution par configuration sur des machines cloud identiques, n'a noté que les domaines produit communs, et a utilisé la version 7.56.2 de l'agent de la plateforme d'origine pour envoyer les données. La compatibilité API faisait l'objet d'une suite de tests distincte de celle portant sur la correction des données et la fiabilité des alertes.

La comparaison des agents a utilisé des exécutions répétées de la même charge de travail, un agent à la fois, les deux envoyant les données au même serveur Radar. La référence était la version 7.56.2 de l'agent de la plateforme d'origine.

DataCat nous donne une base fonctionnelle que nous pouvons inspecter, personnaliser et exploiter sur notre propre infrastructure.

*Aperçu de DataCat, notre propre plateforme de monitoring applicatif construite avec Missions*

## Mettez votre ambition au travail

Missions continue de nous impressionner par l'éventail d'objectifs qu'elle peut prendre en charge. Sur E-Commerce Bench, un agent démarre avec 100 000 ¥ et gère des boutiques en ligne pendant une année simulée, en choisissant ses fournisseurs, en évitant les arnaques et en fixant ses prix. En une seule exécution, Missions a fait passer ce capital à 4,82 millions de ¥, soit environ 48 fois la mise de départ — un résultat state-of-the-art plus de trois fois supérieur au meilleur score du classement public.

Nous pensons que Missions représente une étape concrète vers la Self-Driving Company : les humains fixent la direction, prennent les décisions qui comptent et restent responsables, tandis que les agents assurent l'exécution et la coordination.

Cela change ce qu'une petite équipe peut envisager d'entreprendre. Le lancement produit que vous repoussez sans cesse. Le refactoring qui mobiliserait tout un groupe d'ingénieurs expérimentés. Le logiciel sur étagère que vous voudriez construire en interne mais pour lequel vous manquez de bande passante.

Nous sommes impatients de faire découvrir Missions au monde et de voir ce que vous allez entreprendre avec elle.

Cliquez sur « New » dans la barre latérale, sélectionnez « Mission », et décrivez votre objectif le plus ambitieux.

Pour en savoir plus : replit.com/missions ou contactez notre équipe commerciale pour discuter de l'intégration de Missions dans votre organisation.

## Pourquoi ça compte
Ce lancement illustre la bascule de l'IA générative, de simple assistant de code vers des systèmes d'agents autonomes et parallélisés capables de mener des projets entiers (planification, construction, test, itération) avec une supervision humaine minimale — un signal fort à suivre pour quiconque surveille l'évolution des outils d'agents IA en entreprise.
