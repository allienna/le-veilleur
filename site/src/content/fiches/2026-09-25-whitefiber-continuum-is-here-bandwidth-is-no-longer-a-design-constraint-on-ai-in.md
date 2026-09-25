---
title: "WhiteFiber Continuum Is Here: Bandwidth Is No Longer a Design Constraint on AI Infrastructure | WhiteFiber"
date: 2026-09-25
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.whitefiber.com%2Fblog%2Fcontinuum-launch%3Futm_source=tldr%26utm_medium=newsletter%26utm_campaign=tofu_continuum_launch%26utm_content=blog/1/010001a0d3599704-54795287-1841-470d-b831-cb9ab81c6189-000000/Sj5MCaEWg-ZvyBPco5gLgCOn2Bq9J6njNgUpT2W1cQk=452"
keywords: ["infrastructure IA", "supercluster GPU", "data center", "bande passante", "latence", "cloud"]
theme: "IA"
tone: "news"
used_in: ["2026-09-25"]
---

## Résumé
WhiteFiber annonce la disponibilité commerciale de Continuum, une solution réseau inter-data centers qui relie deux sites QTS distants de 83 km en un seul supercluster GPU logique, avec jusqu'à 136 Tbps de bande passante agrégée et 0,9 ms de latence aller-retour. L'architecture combine DriveNets AI Fabric pour le réseau et WEKA NeuralMesh pour le stockage et la mémoire, dans le but de supprimer l'arbitrage traditionnel entre échelle, résilience et conformité réglementaire. L'offre cible les laboratoires de modèles fondamentaux, les entreprises réglementées (finance, santé), les acteurs télécoms/edge et les fournisseurs GPUaaS/NeoCloud. WhiteFiber prévoit d'étendre Continuum à d'autres sites et organise un webinaire le 14 octobre 2026 pour présenter l'architecture.

## Points clés
- Continuum relie deux data centers QTS certifiés HITRUST distants de 83 km via 12 brins de fibre noire Zayo.
- Performances annoncées : jusqu'à 136 Tbps de bande passante agrégée et 0,9 ms de latence aller-retour, soit à 8 % près de la limite physique de la lumière dans la fibre.
- Architecture combinant DriveNets AI Fabric (couche réseau) et WEKA NeuralMesh (données/mémoire) pour créer un seul supercluster GPU logique, plutôt que deux clusters simplement reliés par un lien rapide.
- Objectif central : permettre un basculement (failover) actif entre sites sans perte de souveraineté des données pour les secteurs réglementés.
- Cibles commerciales : laboratoires de modèles fondamentaux, entreprises réglementées (finance, santé), opérateurs télécoms/edge, fournisseurs GPUaaS et NeoCloud.
- Disponible commercialement depuis le 23 septembre 2026, avec une extension à d'autres sites prévue et un webinaire public le 14 octobre 2026.

## Analyse approfondie
# WhiteFiber Continuum est là : la bande passante n'est plus une contrainte de conception pour l'infrastructure IA

WhiteFiber Continuum™, notre solution de mise en réseau inter-data centers, est désormais disponible commercialement, transformant deux clusters distribués en un seul supercluster GPU logique.

15 min de lecture

Dernière mise à jour : 23 septembre 2026

En juillet dernier, nous avons publié des chiffres qui ont fait sursauter plus d'une personne : 111,2 Tbps de bande passante et 0,9 milliseconde de latence aller-retour, sur 83 kilomètres de fibre noire reliant deux data centers. À l'époque, il s'agissait d'un résultat de R&D : la preuve que deux installations pouvaient fonctionner comme un seul supercluster plutôt que comme deux systèmes qui prétendent en être un. Nous avions dit que nous partagerions davantage d'informations sur la disponibilité, l'architecture et les tests finaux au moment du lancement commercial. Nous y sommes.

Aujourd'hui, nous annonçons que WhiteFiber Continuum est disponible commercialement.

Continuum relie deux installations QTS certifiées HITRUST, distantes de 83 kilomètres, via 12 brins de fibre noire Zayo, fonctionnant sur DriveNets AI Fabric pour la couche réseau et WEKA NeuralMesh pour l'infrastructure de données et de mémoire à l'échelle du cluster. Après la mise en service de longueurs d'onde supplémentaires, notre conception peut atteindre 136 Tbps de bande passante agrégée, avec une latence aller-retour de 0,9 ms entre les deux sites distants de 83 km. Le résultat est un seul supercluster GPU logique réparti sur deux sites physiques — et non deux clusters reliés tant bien que mal par un tuyau rapide. Réseau, stockage et calcul sont conçus ensemble, et non ajoutés après coup.

« WhiteFiber Continuum est la réponse infrastructurelle à un problème avec lequel le secteur vit depuis des années : la distance géographique comme plafond de ce qu'un cluster peut accomplir. Aujourd'hui, nous le rendons disponible commercialement pour les entreprises qui ont besoin d'une puissance de calcul IA capable de fonctionner à grande échelle, de tenir face aux exigences de conformité, et de ne pas s'effondrer quand un seul site rencontre un problème. »
— Sam Tabar, Directeur général (CEO), WhiteFiber

## Pourquoi cela compte

La plupart des infrastructures considèrent le data center comme la limite d'un cluster. Nous le considérons comme un détail d'implémentation.

Pendant des années, si l'on voulait de la résilience entre plusieurs sites, il fallait accepter un basculement (failover) plus lent et plus froid. Si l'on voulait faire évoluer l'entraînement au-delà de l'enveloppe de puissance d'un seul campus, il fallait déployer un second site distinct et vivre avec les coûts de coordination associés. Si l'on devait garder des données sensibles à l'intérieur d'une seule juridiction, il fallait accepter un plafond sur la taille qu'un cluster conforme pouvait atteindre. Continuum a été conçu pour éliminer ces compromis, afin que l'échelle, la résilience et la conformité cessent de s'opposer les unes aux autres.

Parce qu'aucun site unique ne constitue un point de défaillance unique, un entraînement se poursuit même lorsqu'un site tombe, au lieu de s'arrêter en attendant son rétablissement. Et parce que les charges de travail sensibles n'ont jamais besoin de quitter le site où elles sont générées, les entreprises réglementées obtiennent cette résilience sans renoncer à la souveraineté des données.

## Conçu pour qui

Voici quelques-unes des équipes avec lesquelles nous échangeons déjà au sujet de Continuum :

1. Les laboratoires de modèles fondamentaux et les organisations de recherche en IA dont les entraînements dépassent l'enveloppe de puissance et d'espace d'un seul site, et qui souhaitent faire évoluer l'entraînement sur plusieurs sites comme un seul cluster logique.
2. Les entreprises réglementées des secteurs de la finance et de la santé qui ont besoin d'un basculement actif instantané sans renoncer à la résidence des données dans leur région.
3. Les partenaires télécoms et d'infrastructure en périphérie de réseau (edge) disposant de capacités distribuées en énergie et en fibre, qui souhaitent les transformer en capacité d'inférence monétisable plutôt qu'en infrastructure immobilisée.
4. Les fournisseurs de GPUaaS et de NeoCloud qui doivent offrir à leurs propres clients une élasticité et des accords de niveau de service (SLA) de disponibilité sans avoir à construire eux-mêmes une infrastructure multi-site.
5. Les équipes qui exploitent déjà du calcul ailleurs et souhaitent une couche de résilience plus légère, active ou en veille chaude — la reprise après sinistre (disaster recovery) pour l'IA, vendue en tant que telle.

## Construit avec les bons partenaires

Continuum a été développé en collaboration avec DriveNets, qui fournit le tissu réseau IA haute performance reliant les deux sites, et WEKA, qui fournit l'infrastructure de données et de mémoire haute performance à l'échelle du cluster. Ces deux partenariats sont au cœur de l'offre commerciale.

« WhiteFiber Continuum montre ce qui devient possible lorsqu'une ingénierie ambitieuse est associée à l'architecture réseau adéquate. Le tissu IA Ethernet de DriveNets offre les meilleures performances, même dans les environnements les plus exigeants en bande passante et en faible latence, garantissant que les superclusters à l'échelle déplacent les données efficacement, maximisent l'utilisation des GPU et optimisent l'efficacité énergétique. »
— Yossi Kikozashvili, VP Produit et GTM – Infrastructure IA, DriveNets

« Le secteur a longtemps traité la distance comme un plafond incontournable pour l'infrastructure IA, et WhiteFiber Continuum le fait sauter. Mais un supercluster n'est unifié qu'à la hauteur de ses données. NeuralMesh de WEKA offre à Continuum une fondation de stockage et de mémoire unique et haute performance à travers les sites, de sorte que des GPU distants de plusieurs dizaines de kilomètres fonctionnent comme si les données étaient locales. C'est ce qui transforme deux data centers en un seul moteur, et c'est sur cette base que se construira la prochaine génération d'innovation en IA. »
— Liran Zvibel, cofondateur et CEO, WEKA

## Et ensuite

Nous avons conçu Continuum pour qu'il s'étende, et pas seulement pour relier deux sites. D'autres sites pourront rejoindre le même cluster logique au fil du temps, en utilisant la même approche réseau déjà en place, de sorte que l'investissement en infrastructure s'accumule au lieu de se déprécier. Des tests complets sur l'ensemble du spectre de la fibre sont en cours pour confirmer les spécifications commerciales garanties, et nous partagerons davantage d'informations dès que ces résultats seront disponibles.

## Parlons-en

Si la distance est ce qui sépare vos projets d'infrastructure IA de là où vous devez réellement être, Continuum est disponible dès aujourd'hui. Visitez la page produit pour découvrir son fonctionnement, ou rejoignez-nous le 14 octobre 2026 pour un webinaire en direct avec DriveNets et WEKA, au cours duquel nos ingénieurs présenteront l'architecture et répondront à vos questions.

## FAQ

**Qu'est-ce que WhiteFiber Continuum ?**
WhiteFiber Continuum est notre solution de mise en réseau inter-data centers qui relie des data centers géographiquement séparés en un seul supercluster GPU logique, éliminant la bande passante et le débit comme contraintes sur l'endroit et la manière de déployer l'infrastructure IA.

**En quoi est-ce différent du simple fait de connecter deux data centers par une liaison réseau ?**
Une liaison standard entre deux installations se comporte toujours comme deux systèmes séparés : les charges de travail sont réparties, les tâches sont coordonnées via une connexion plus lente, et le basculement implique généralement un délai le temps que le trafic soit réacheminé. Continuum, construit sur DriveNets AI Fabric et WEKA NeuralMesh, fait fonctionner deux sites physiques comme un seul cluster logique, de sorte qu'une tâche peut s'exécuter sur les deux sites, ou basculer de l'un à l'autre, sans cette perte de performance.

**À quel niveau de performance puis-je m'attendre ?**
La solution offre 136 Tbps de bande passante agrégée avec une latence aller-retour de 0,9 milliseconde sur 83 kilomètres de fibre noire. Cette latence se situe à 8 % près de la limite physique de la lumière dans la fibre sur cette distance.

**Cela compromet-il la souveraineté des données ou la conformité ?**
Non. Continuum est conçu pour garder les charges de travail sensibles à l'intérieur de leur juridiction d'origine, même lorsque le basculement et le calcul mutualisé s'effectuent entre plusieurs sites, de sorte que les entreprises réglementées bénéficient de cette résilience sans renoncer à la résidence des données.

**À qui s'adresse WhiteFiber Continuum ?**
Aux laboratoires de modèles fondamentaux et aux équipes de recherche en IA, aux entreprises réglementées des secteurs de la finance et des sciences de la vie, aux partenaires télécoms et d'infrastructure en périphérie de réseau, aux revendeurs GPUaaS et NeoCloud, ainsi qu'à toute équipe souhaitant une reprise après sinistre active-active ou en veille chaude pour ses charges de travail IA.

**Continuum est-il disponible dès aujourd'hui ?**
Oui. WhiteFiber Continuum est disponible commercialement depuis le 23 septembre 2026. Rendez-vous sur whitefiber.com pour commencer.

**Quelle est la suite pour Continuum ?**
Nous avons conçu Continuum pour qu'il s'étende. D'autres sites pourront rejoindre le même cluster logique au fil du temps, en utilisant la même approche réseau déjà en place. Nous partagerons davantage d'informations sur l'expansion et la feuille de route dans les mois à venir.

## Pourquoi ça compte
Ce lancement illustre une tendance de fond dans l'infrastructure IA : dépasser les limites physiques d'un site unique pour mutualiser le calcul GPU à l'échelle multi-sites tout en respectant les contraintes de souveraineté et de conformité réglementaire, un enjeu clé alors que les entraînements de modèles de fondation deviennent trop grands pour un seul campus.
