---
title: "Five years after the fork, OpenSearch is slowly stepping out of AWS’s shadow"
date: 2026-11-03
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fthenewstack.io%2Fopensearch-foundation-aws-elasticsearch%2F%3Futm_source=tldrit/1/010001a19c6ab804-cf5f7c9f-19fa-4841-9a12-e400532b9b70-000000/qMbYG-Z4T_fy6APq0sxfKTRBDqNURB8l_IvFj_NGKSQ=452"
keywords: ["OpenSearch", "Elasticsearch", "AWS", "Linux Foundation", "open source", "IA/RAG"]
theme: "Data"
tone: "news"
used_in: ["2026-11-03"]
---

## Résumé
Cinq ans après sa création par AWS en réaction au changement de licence d'Elasticsearch, OpenSearch continue de prendre ses distances avec son créateur. Depuis son transfert à la Linux Foundation en septembre 2024 (naissance de l'OpenSearch Software Foundation), la part d'AWS dans les contributions et le mainteneurship a diminué, tandis que les déploiements auto-gérés progressent plus vite que le service managé d'Amazon. Le projet mise désormais sur la recherche vectorielle et hybride pour devenir une brique centrale de l'infrastructure IA (RAG), mais la perception d'une dépendance à AWS freine encore une partie des entreprises non-adoptantes. Bianca Lewis, directrice exécutive de la Fondation, défend l'indépendance juridique acquise et l'ambition d'une plateforme qu'aucun vendeur ne domine.

## Points clés
- OpenSearch est né en janvier 2021 lorsque AWS a forké Elasticsearch/Kibana après leur passage à des licences propriétaires/source-available chez Elastic.
- En septembre 2024, AWS a transféré le projet à la Linux Foundation, créant l'OpenSearch Software Foundation sous gouvernance « vendor-neutral ».
- La part d'AWS dans les contributions au dépôt principal est passée de 91 % la première année à 72 % en 2025-2026 ; la part des mainteneurs affiliés à Amazon est passée de 95 % (avril 2022) à 71 % aujourd'hui.
- Les déploiements auto-gérés dans le cloud sont passés de 37 % à 60 % des utilisateurs depuis 2024, dépassant la croissance du service managé d'AWS (de 44 % à 48 %) ; 24 % des non-adoptants citent encore les liens historiques avec AWS comme frein.
- AWS garde néanmoins un poids important : 4 des 15 sièges votants du Technical Steering Committee, et un employé AWS (Andrew Ross) vient d'être réélu président du comité en octobre.
- OpenSearch 3.9 (sorti en septembre) renforce la recherche vectorielle/hybride utile au RAG, positionnant le projet comme choix par défaut pour une infrastructure IA ouverte.

## Analyse approfondie

### Origines du fork
OpenSearch a été annoncé par Amazon Web Services en janvier 2021, en réponse à la décision d'Elastic de faire migrer Elasticsearch et Kibana de la licence Apache 2.0 vers une combinaison de licences propriétaires et « source-available ». Elastic justifiait alors ce choix par la volonté d'empêcher des géants du cloud comme AWS de proposer Elasticsearch « en tant que service » sans contrepartie, tout en accusant AWS de violer sa marque. Elastic est ensuite revenu à l'open source en ajoutant l'AGPL comme option de licence, et s'est réconcilié avec AWS. De son côté, OpenSearch a poursuivi son propre chemin en tant que projet open source indépendant, bien que toujours étroitement associé à l'entreprise qui l'a créé.

### Réduire la dépendance à AWS
Un tournant majeur survient en septembre 2024, quand AWS transfère OpenSearch à la Linux Foundation, créant l'OpenSearch Software Foundation sous une gouvernance présentée comme « neutre envers les vendeurs ». L'objectif est de rassurer les autres entreprises sur le fait qu'elles peuvent contribuer sans que AWS garde le contrôle ultime du projet.

Deux ans plus tard, des signes de traction au-delà du soutien initial apparaissent. Selon des chiffres fournis par l'OpenSearch Software Foundation à *The New Stack*, la part d'AWS dans les activités de contribution sur les dépôts du projet est passée de 91 % la première année à 72 % en 2025-2026. Dans le même temps, la part d'ingénieurs affiliés à Amazon parmi les mainteneurs du dépôt principal est passée de 95 % en avril 2022 à 71 % aujourd'hui.

Cette évolution se retrouve aussi dans les usages. Le *2026 Open Data Infrastructure Report*, publié le mois dernier par la Linux Foundation et l'OpenSearch Software Foundation, montre que les déploiements auto-gérés ont progressé plus vite que le service managé OpenSearch d'Amazon depuis 2024 : 60 % des utilisateurs interrogés exploitent désormais des déploiements auto-gérés dans le cloud, contre 37 % en 2024, tandis que l'usage du service managé d'Amazon n'a progressé que de 44 % à 48 %.

Malgré cela, l'association historique avec AWS reste un obstacle pour certains utilisateurs potentiels : près d'un quart (24 %) des 71 non-adoptants interrogés citent des inquiétudes sur la neutralité vis-à-vis des vendeurs et les liens historiques avec AWS comme raisons de ne pas adopter le projet. Ces chiffres illustrent un défi qu'un simple changement de gouvernance ne suffit pas à résoudre : convaincre utilisateurs et contributeurs potentiels que l'avenir d'OpenSearch n'est plus déterminé principalement par AWS.

### « Un moment décisif » pour OpenSearch
*The New Stack* s'est entretenu avec Bianca Lewis, directrice exécutive de l'OpenSearch Software Foundation, lors de l'Open Source Summit Europe à Prague ce mois-ci, pour discuter de l'évolution du projet au-delà de ses origines liées à Elasticsearch, et de la perception persistante d'une influence d'AWS.

Pour Lewis, l'indépendance juridique obtenue il y a plus de deux ans constitue une base importante pour construire cette confiance : le don à la Linux Foundation a représenté, selon elle, « un moment décisif », car AWS ne pouvait plus fermer OpenSearch ni en changer la licence — l'entreprise ne possédait plus l'application.

Lewis estime également que cette décision avait un sens commercial pour AWS, dont l'activité cloud génère des revenus à partir des ressources de calcul utilisées pour faire fonctionner les applications, plutôt que de la possession des applications elles-mêmes. Selon elle, AWS ne gagne pas d'argent avec les applications mais avec le calcul ; faire croître OpenSearch sur le long terme n'a donc jamais fait partie des plans d'AWS.

Des questions subsistent toutefois sur l'influence que conserve AWS. L'entreprise représente encore près des trois quarts des activités de contribution enregistrées sur les dépôts d'OpenSearch. Et si AWS ne détient que 4 des 15 sièges votants du Technical Steering Committee (TSC), un employé d'AWS, Andrew Ross, vient d'être réélu président du comité en octobre.

### L'opportunité de l'IA pour OpenSearch
Si l'influence d'AWS reste visible dans la gouvernance, le logiciel lui-même a considérablement évolué depuis le fork. Lewis reconnaît volontiers à quel point il ressemblait à Elasticsearch à ses débuts : les premières versions d'OpenSearch étaient, dit-elle, « Elasticsearch sous un autre nom », partageant les mêmes plugins et une documentation largement reprise d'Elasticsearch. Mais au moment du don à la Linux Foundation, le projet avait déjà nettement divergé de son projet d'origine.

Aujourd'hui, OpenSearch se positionne comme une infrastructure pour les applications qui doivent rechercher, analyser et récupérer des données, y compris celles construites autour de grands modèles de langage (LLM). Son support de la recherche vectorielle et hybride le rend pertinent pour la génération augmentée par récupération (RAG), où les applications d'IA puisent des informations externes pour enrichir les réponses des modèles.

La dernière version du projet, OpenSearch 3.9, sortie en septembre, prolonge ces capacités avec des améliorations destinées à aider les développeurs à rechercher et récupérer de l'information pour des applications d'IA, ainsi que des mises à jour en matière de performance, de supervision et d'alerte. Lewis y voit une opportunité pour OpenSearch de devenir une composante centrale de l'infrastructure IA en entreprise : si une organisation veut une infrastructure IA sur une plateforme ouverte, OpenSearch est aujourd'hui, selon elle, « le choix par défaut ».

### Convaincre les entreprises
Les ambitions sont une chose, les transformer en adoption durable en entreprise en est une autre. Le rapport de la Fondation indique qu'une proportion importante des déploiements OpenSearch reste expérimentale, les organisations étant encore en phase d'évaluation ou l'utilisant pour des usages qui pourraient être remplacés.

Interrogée sur ce point, Lewis souligne le temps que peut prendre le passage d'une entreprise depuis des plateformes commerciales établies, notamment lorsqu'elles sont liées par des contrats de licence pluriannuels — par exemple un contrat de trois ans avec Splunk ou de cinq ans avec Elastic — que les entreprises ne jettent pas simplement à la poubelle. En d'autres termes, des entreprises peuvent tester OpenSearch tout en continuant à utiliser des produits déjà payés, sans garantie que ces évaluations se traduisent par des déploiements permanents.

Lewis avance qu'une des raisons pour lesquelles les organisations pourraient finir par basculer est la liberté de changer de fournisseur technologique sans devoir reconstruire leurs applications. Elle évoque la crainte du verrouillage (« lock-in ») : si l'on se retrouve enfermé chez un fournisseur et que l'on veut partir, faut-il réarchitecturer toutes ses applications ? Cette préoccupation dépasse le seul coût des licences : les entreprises doivent aussi considérer l'effort d'ingénierie nécessaire pour changer de fournisseur, migrer les données et maintenir les applications dans le temps.

Tout cela ramène à la question de l'indépendance d'OpenSearch : si les organisations choisissent la plateforme en partie pour éviter de dépendre d'un vendeur unique, la capacité du projet à attirer et retenir des contributeurs au-delà d'AWS devient d'autant plus importante. Interrogée sur ce qu'elle espère pour OpenSearch dans cinq ans, Lewis revient sur la question de l'influence des vendeurs et son ambition d'une plateforme durable, rapide et innovante, qui ne soit dominée ou fortement influencée par aucun vendeur unique — gage, selon elle, d'une plateforme stable.

## Pourquoi ça compte
Ce cas illustre comment un projet open source né d'un fork stratégique peut progressivement gagner en légitimité face à son créateur initial, un enjeu clé pour toute veille sur la gouvernance des infrastructures data/IA open source et les risques de lock-in cloud.
