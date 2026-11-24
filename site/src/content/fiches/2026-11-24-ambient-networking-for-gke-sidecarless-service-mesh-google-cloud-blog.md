---
title: "Ambient networking for GKE: sidecarless service mesh | Google Cloud Blog"
date: 2026-11-24
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fcloud.google.com%2Fblog%2Fproducts%2Fnetworking%2Fambient-networking-for-gke-sidecarless-service-mesh%3Futm_source=tldrit/1/010001a2089020f9-043233d8-eb54-4687-9c0f-67a02ba30045-000000/GGyURcbvbmPqbc4rXPRfZ3C3tVw-CSllu8duMlUy6zM=452"
authors: ["Chris Crall"]
keywords: ["service mesh", "GKE", "sidecarless", "mTLS", "Kubernetes", "Envoy"]
theme: "Software"
tone: "news"
used_in: ["2026-11-24"]
---

## Résumé
Google Cloud annonce la disponibilité générale du « ambient networking » pour GKE, une architecture de service mesh sans sidecar. Cette approche déplace les fonctions réseau (sécurité, observabilité, routage) des pods applicatifs vers des composants partagés au niveau du nœud et un plan de contrôle managé. L'objectif est de réduire la surcharge opérationnelle et la consommation de ressources inhérentes aux proxys sidecar traditionnels, tout en apportant du mTLS, des politiques d'autorisation et une télémétrie riche. Google revendique jusqu'à 10x moins de ressources consommées et jusqu'à quatre fois moins de perturbations annuelles liées aux redémarrages de pods pour les correctifs CVE.

## Points clés
- Passage à une architecture sans sidecar : les fonctions de mesh réseau sont déplacées vers des composants partagés par nœud plutôt qu'injectées dans chaque pod.
- Plan de contrôle composé de Traffic Director (xDS), Certificate Authority Service (certificats d'identité managés), le plan de contrôle GKE et un contrôleur Gateway.
- Composants au niveau du nœud : plugin NRI, agent xDS, proxy Envoy L4 partagé par nœud, et les pods de service eux-mêmes.
- Bénéfices clés : architecture Zero Trust avec mTLS automatique, politiques d'accès simplifiées, télémétrie L4/L7 riche via Network Services Monitoring.
- Gains opérationnels : jusqu'à 10x moins de ressources pour les fonctions mesh L4, et jusqu'à 4x moins de perturbations annuelles liées aux patchs CVE grâce au découplage proxy/application.
- Solution entièrement managée, installable à la création du cluster ou ajoutée à un cluster existant, avec maintenance automatisée.

## Analyse approfondie
##### Chris Crall

Product Manager

Les sidecars réseau ont une réputation méritée de consommation excessive de ressources et de surcharge de gestion accrue, en particulier dans un environnement de service mesh. Aujourd'hui, nous annonçons la disponibilité générale du réseau ambiant (« ambient networking ») pour Google Kubernetes Engine (GKE). Cette étape marque une évolution importante dans la façon dont vous exécutez le service mesh sur GKE, en amenant une architecture sans sidecar en production. Introduit plus tôt cette année, le réseau ambiant découple les fonctionnalités traditionnellement fournies par un service mesh des charges de travail applicatives, permettant aux opérateurs de plateforme et aux développeurs d'aider à sécuriser, observer et router le trafic sans la surcharge de ressources et la complexité opérationnelle liées à la gestion des proxys sidecar.

### **Architecture du réseau ambiant**

L'architecture du réseau ambiant déplace les responsabilités réseau des pods applicatifs individuels vers des composants partagés par nœud et des services de plan de contrôle managés.

#### Plan de contrôle

Le plan de contrôle du réseau ambiant orchestre les opérations à travers le cluster.

- **Traffic Director :** Sert de plan de contrôle xDS centralisé, livrant en continu les règles de routage, les politiques de contrôle d'accès et les mises à jour de l'état du cluster aux proxys au niveau du nœud.
- **Certificate Authority Service :** Authentifie les charges de travail et émet dynamiquement des certificats d'identité de charge de travail managés, à la demande, pour permettre un chiffrement mTLS transparent à travers les communications de service à service.
- **Plan de contrôle GKE :** Gère le cluster.
- **Contrôleur Gateway :** Lit les CRD Gateway et transmet les informations de configuration à Traffic Director.

#### Composants du nœud GKE

Dans le même temps, plusieurs composants de gestion au niveau du nœud opèrent de manière sécurisée dans l'espace de noms `gke-managed-ambient` :

- **Plugin d'interface d'exécution réseau ambiant (NRI) :** S'intègre au NRI pour effectuer une redirection réseau de bas niveau, interceptant le trafic entrant et sortant des pods applicatifs activés pour l'ambient.
- **Agent xDS (agent ambiant) :** S'exécute à l'intérieur du pod proxy de nœud pour recevoir les mises à jour de configuration xDS depuis Traffic Director et demander des certificats au plan de contrôle GKE à la demande.
- **Proxy de nœud (proxy Envoy L4) :** Une instance Envoy performante et partagée par nœud qui traite le trafic L4 intercepté, applique le TLS mutuel (mTLS), évalue les politiques d'autorisation, effectue l'équilibrage de charge et émet des métriques de télémétrie riches.
- **Pods de service :** Les pods d'application/service de l'utilisateur communiquent via le proxy de nœud GKE pour effectuer du mTLS service à service à travers le cluster.

### **Fonctionnalités principales**

Ensemble, ces fonctionnalités se combinent pour offrir un certain nombre de capacités avancées pour les environnements GKE :

- **Architecture Zero Trust :** Le réseau ambiant permet aux clients d'établir une posture de sécurité Zero Trust. Le trafic entre les charges de travail peut être automatiquement chiffré en utilisant le TLS mutuel (mTLS) avec des identités de charge de travail managées, aidant à protéger et sécuriser les communications de service à service à travers le cluster.
- **Politique d'accès simplifiée :** Un contrôle granulaire sur les communications de service est simplifié grâce aux politiques d'autorisation. Les opérateurs peuvent définir des règles d'accès précises pour appliquer des limites de sécurité à moindre privilège entre les microservices.
- **Télémétrie riche :** Obtenez des informations opérationnelles avec des métriques L4 et L7 prêtes à l'emploi. Les données d'observabilité peuvent être collectées automatiquement, donnant aux équipes une visibilité sur les modèles de trafic, la latence et l'état des connexions pour une surveillance et un dépannage efficaces.
Pour voir ces métriques, utilisez Network Services Monitoring, une nouvelle capacité Google Cloud également disponible aujourd'hui. Network Services Monitoring montre le trafic géré par le réseau ambiant, par exemple les connexions service à service, la latence et les taux d'erreur, à travers vos clusters GKE, afin que vous puissiez comprendre les dépendances de service sans construire vos propres tableaux de bord. Pour en savoir plus, consultez la documentation.

### Avantages du réseau ambiant

Le réseau ambiant apporte une valeur tangible pour les opérateurs GKE :

- **Opérations plus simples :** Traditionnellement, les produits de service mesh s'appuient sur l'injection de conteneurs sidecar directement dans chaque pod de charge de travail. Le réseau ambiant élimine cette dépendance au sidecar en déplaçant les fonctionnalités réseau vers des composants de nœud partagés. Cette solution entièrement managée simplifie le déploiement et rationalise les opérations quotidiennes du cluster.
- **Gestion du cycle de vie simplifiée :** Lorsque la logique du proxy est découplée des conteneurs applicatifs, la gestion du cycle de vie est simplifiée. La mise à niveau des versions de proxy ou l'application de mises à jour de configuration permet d'éviter de redémarrer les charges de travail applicatives ou de planifier des fenêtres d'indisponibilité, permettant une disponibilité continue pour vos services. Le réseau ambiant peut réduire la surcharge administrative et les perturbations applicatives d'une moyenne de quatre fois par an en éliminant les redémarrages de pods requis par les correctifs CVE pour l'usage du mesh L4.
Cette solution entièrement managée peut être installée soit à la création du cluster, soit ajoutée à un cluster existant. La maintenance continue des composants du cluster est gérée par des systèmes automatisés et est effectuée en même temps que la maintenance normale du cluster GKE.
- **Consommation de ressources réduite :** En s'éloignant des proxys sidecar pour chaque pod, le réseau ambiant réduit la surcharge de calcul et de mémoire. Le réseau ambiant permet une réduction jusqu'à 10 fois de l'utilisation des ressources GKE pour les fonctionnalités de mesh de couche 4 (L4), y compris le mTLS, l'équilibrage de charge, la télémétrie, et plus encore.

### **Essayez le réseau ambiant dans vos clusters GKE dès aujourd'hui**

Simplifiez l'adoption en supprimant les barrières de coût et de complexité des sidecars. Essayez-le dans votre environnement GKE et découvrez les avantages du réseau ambiant :

- Installation et mises à niveau entièrement managées
- mTLS service à service et politiques d'autorisation
- Utilisation des ressources inférieure à celle des sidecars
- Métriques L4 et L7

Consultez notre documentation pour plus d'informations : https://docs.cloud.google.com/kubernetes-engine/docs/concepts/ambient-overview

Tarification : https://cloud.google.com/products/gke-service-networking/pricing

## Pourquoi ça compte
Cette annonce illustre la tendance de fond vers des architectures de service mesh plus légères, abandonnant le modèle sidecar historique (Istio classique, Linkerd) au profit de composants partagés par nœud — un enjeu direct pour toute équipe infra gérant des clusters Kubernetes à grande échelle avec des contraintes de coût et de résilience opérationnelle.
