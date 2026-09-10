---
title: "Introducing Muse: The World’s First Personal AI Agent Built for Everyone"
date: 2026-09-10
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fabout.fb.com%2Fnews%2F2026%2F09%2Fintroducing-muse-personal-ai-agent%2F%3Futm_source=tldrai/1/010001a0865dff15-ab1e96d3-e50a-4858-9290-c463567f08de-000000/_F7dchUBzV-qRgpsH1XiCyPq-7sK2unTi4HZX21n8mA=452"
keywords: ["agent IA personnel", "Meta", "vie privée", "sécurité", "paiement automatisé", "machine virtuelle sécurisée"]
theme: "IA"
tone: "news"
used_in: ["2026-09-10"]
---

## Résumé
Meta lance Muse, présenté comme le premier agent d'IA personnel grand public capable d'agir de façon autonome pour accomplir des tâches et des objectifs complexes (réservations, achats, négociations). L'agent tourne sur une machine virtuelle dédiée et isolée, Muse Secure VM, propulsée par le modèle Muse Spark, et est accessible via l'application Muse ou WhatsApp. Meta met en avant une architecture de sécurité en couches (agent de contrôle séparé, stockage isolé des identifiants, audit trail, paiements tokenisés via Link/Stripe) et prévoit une version chiffrée de bout en bout d'ici la fin de l'année. Le déploiement démarre aux États-Unis sur iOS, Android et muse.ai, avec une extension prévue aux lunettes IA.

## Points clés
- Muse est un agent IA personnel grand public, utilisable sans compétence technique, capable d'exécuter des tâches complexes de façon autonome (achats, réservations, négociations, formulaires).
- Il fonctionne dans une VM dédiée et isolée (Muse Secure VM), sous le contrôle d'un agent séparé appelé Sentinel, qui valide toute action sortante vers internet.
- Les identifiants et moyens de paiement restent invisibles pour Muse lui-même ; les paiements passent par Link (Stripe), qui offre des protections d'achat inédites pour un agent IA.
- Les utilisateurs gardent la main : permissions granulaires par service, historique d'audit complet, possibilité de faire « oublier » des informations mémorisées, et opt-out de l'entraînement des modèles Meta.
- Une version « Confidential VM », chiffrée de bout en bout avec une clé détenue uniquement par l'utilisateur, est prévue plus tard cette année.
- Lancement aux États-Unis sur iOS, Android et muse.ai, avec arrivée prochaine sur les lunettes IA de Meta ; gratuit pour l'essentiel des usages, avec des offres d'abonnement.

## Analyse approfondie
Aujourd'hui, Meta présente Muse, un agent d'IA personnel sécurisé et privé qui aide de manière proactive les gens à atteindre leurs objectifs et leur suggère des idées. Parce que les agents personnels ont besoin d'un nouveau type d'ordinateur sécurisé, Muse fonctionne sur Muse Secure VM, une machine virtuelle (VM) dédiée qui héberge à la fois l'agent et les données d'une personne. Muse est conçu autour de la façon dont les gens communiquent déjà, si bien qu'échanger avec lui fonctionne exactement comme envoyer un message à une autre personne, dans l'application Muse ou directement dans WhatsApp.

C'est simple à utiliser. Il suffit de dire à Muse ce qu'il faut faire, et il agit, propulsé par Muse Spark, le modèle le plus performant à ce jour de Meta, conçu pour ce type de travail agentique appliqué au monde réel.

### Comment ça marche

Contrairement aux autres agents, Muse a été conçu pour fonctionner pour des milliards de personnes dans le monde, il n'y a donc aucune courbe d'apprentissage. N'importe qui peut l'utiliser directement, sans expérience technique requise. Il peut gérer des tâches, comme envoyer un e-mail ou réserver un voyage, et il peut se charger d'objectifs ambitieux. Une fois qu'une personne partage un objectif avec Muse, celui-ci l'aide à élaborer un plan personnalisé, à coordonner son temps et ses ressources, puis fait avancer le travail de lui-même. Il peut ouvrir un navigateur, remplir des formulaires et négocier en son nom.

Pour les tâches qui prennent plus de temps, Muse continue de travailler après que la personne a fermé l'application, et revient vers elle lorsque quelque chose change ou lorsqu'il a besoin d'une approbation, par exemple avant d'envoyer un e-mail ou d'effectuer un achat. Il obtient de meilleurs résultats avec moins d'effort : vendre une voiture plus cher, faire baisser une facture, ajuster un plan d'entraînement au fil des changements dans la vie de quelqu'un.

Au moment de payer, Muse peut finaliser l'achat avec Link, développé par Stripe, et il est le premier agent IA couvert par les protections d'achat de Link : couverture gratuite en cas d'articles endommagés ou perdus, baisses de prix, retours sans frais, et une garantie de retour sur les achats éligibles. Le portefeuille de Link pour les agents génère une carte à usage unique, de sorte que les véritables coordonnées bancaires restent cachées, permettant d'acheter en toute sécurité sur internet. Shop Pay arrive bientôt comme un autre moyen de paiement, ainsi que la prise en charge de 1Password afin que Muse puisse utiliser les identifiants qu'une personne possède déjà.

Muse se souvient aussi de ce qui compte pour une personne, ce qui lui permet de faire des suggestions sans qu'on le lui demande et d'agir sur des détails que la personne n'a mentionnés qu'une seule fois. Il peut transformer une recette vue en reel sur Instagram et sauvegardée en liste de courses, suggérer un menu pour un dîner, et se souvenir des restrictions alimentaires des amis avant d'envoyer les invitations.

### Conçu pour être privé, sûr et sécurisé

Les agents personnels ont besoin d'un nouveau type d'ordinateur sécurisé, alors Meta en a construit un pour tout le monde. Muse Secure VM dispose de protections de confidentialité, de sécurité et de sûreté inédites, intégrées dès la conception, qu'aucun autre agent ne propose :

- Muse fonctionne sur son propre ordinateur dédié dans le cloud, isolé de sorte qu'aucun autre agent ne puisse y accéder. C'est là que Muse vit, et c'est là que sont stockées de manière sécurisée les données et les identifiants de tout service auquel une personne se connecte.
- Un agent Sentinel distinct fonctionne sur cette même machine, maintenu séparé de Muse au niveau du système. Rien de ce que fait Muse n'atteint internet sans l'approbation de Sentinel, qui demande la permission à la personne lorsque c'est nécessaire.
- Muse n'a aucune visibilité sur les mots de passe ou les moyens de paiement des utilisateurs. Tout identifiant partagé par une personne est placé dans un espace de stockage sécurisé, de sorte que Muse puisse l'utiliser sans jamais le voir, y compris les mots de passe qu'une personne saisit elle-même dans le navigateur.
- Muse vérifie auprès de la personne avant toute action sensible, comme l'envoi d'un e-mail ou un achat. Muse montre aux utilisateurs un historique complet et détaillé de tout ce qu'il a fait et prévoit de faire.
- Les utilisateurs choisissent à quelles applications Muse se connecte et exactement quel niveau d'accès il obtient. Pour des choses comme l'e-mail, les utilisateurs choisissent ce que Muse est autorisé à faire, qu'il puisse simplement lire leur courrier ou aussi envoyer des messages en leur nom.
- Les utilisateurs peuvent modifier les accès ou déconnecter un service quand ils le souhaitent. Ils peuvent aussi refuser que leurs interactions soient utilisées pour entraîner les modèles d'IA de Meta.
- Muse ne partage ni les conversations d'une personne ni les données de sa VM avec les systèmes publicitaires de Meta.
- Muse se souvient de ce qui compte pour une personne, et celle-ci peut toujours lui demander d'« oublier » certaines choses qu'il a apprises.

Plus tard cette année, Meta introduira Muse Confidential VM, où l'intégralité de la VM, y compris les données d'une personne et ses conversations avec Muse, sera chiffrée avec une clé que seule cette personne détient, de sorte que même Meta ne puisse y accéder.

### Perspectives

Meta estime que la superintelligence personnelle sera l'une des technologies les plus transformatrices d'une vie. Muse est un premier pas : un agent qui prend en charge une plus grande part du travail, afin que les gens puissent se concentrer sur ce qui compte vraiment pour eux.

Muse est déployé aux États-Unis sur iOS, Android et muse.ai, et arrivera bientôt sur les lunettes IA. Il est gratuit pour l'essentiel des besoins, avec des offres d'abonnement pour ceux qui souhaitent aller plus loin.

## Pourquoi ça compte
Ce lancement marque l'entrée de Meta dans la course aux agents IA « agentiques » grand public capables d'agir seuls sur le web et de payer en ligne, avec une architecture de sécurité (VM isolée, agent de contrôle séparé, paiements tokenisés) qui pourrait devenir une référence pour la confiance dans les agents autonomes — un développement à suivre de près en veille IA et sécurité.
