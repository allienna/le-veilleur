---
title: "Zero Trust Access to Servers, Kubernetes Clusters, and Cloud"
date: 2026-11-25
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Ffandf.co%2F4Azlet8/1/010001a20d54c987-628780ec-99ee-4bf4-9aa6-dc5a1a4edb6b-000000/OgxH4xLxz3JkLOD4mLRUuJavTpI5ojnkbV3HFThJzOM=452"
keywords: ["zero trust", "identité machine", "infrastructure cloud", "certificats éphémères", "Kubernetes", "agents IA"]
theme: "Sécurité"
used_in: ["2026-11-25"]
---

## Résumé

Cette page présente Teleport Zero Trust Access, une plateforme d'accès à l'infrastructure native à l'identité qui remplace VPN, mots de passe et identifiants statiques par des certificats cryptographiques de courte durée. Elle sécurise l'accès aux serveurs, bases de données, clusters Kubernetes, consoles cloud, applications internes, serveurs MCP et dépôts GitHub, pour les humains comme pour les machines et les agents IA. Le contenu détaille les problèmes des modèles d'accès traditionnels (identifiants statiques, VPN/bastions, privilèges permanents, audits fragmentés), les fonctionnalités clés (Teleport VNet, enregistrement des sessions, double autorisation, conformité réglementaire) et une comparaison avec des solutions concurrentes comme Tailscale et Google IAP. Il s'agit d'une page marketing/produit enrichie d'une FAQ détaillée sur le fonctionnement technique de la solution.

## Points clés

- Teleport remplace les identifiants statiques (mots de passe, clés SSH, tokens API) par des certificats X.509 de courte durée liés à une identité cryptographique vérifiée.
- La plateforme unifie l'accès aux serveurs, bases de données, Kubernetes, consoles cloud, applications web internes, serveurs MCP et GitHub depuis un seul control plane.
- Teleport VNet supprime le besoin de VPN en interceptant les requêtes DNS et en faisant transiter les connexions via les contrôles d'identité de Teleport.
- Le modèle zero trust est étendu aux identités non humaines (CI/CD, services, agents IA) via Teleport Machine & Workload Identity, avec expiration automatique des accès.
- Chaque session est enregistrée et attribuée à une identité vérifiée, ce qui facilite la conformité à SOC 2, FedRAMP, ISO 27001, HIPAA, PCI DSS 4.0, NIS2 et DORA.
- Teleport se positionne face à Tailscale (contrôle réseau par IP) et Google IAP (limité aux apps web GCP) en couvrant tous les environnements et tous les types d'identités depuis une seule plateforme.

## Analyse approfondie

# Mettre fin au chaos de la complexité infrastructurelle

Teleport donne à vos équipes d'ingénierie et à vos identités machine un accès sécurisé et piloté par l'identité aux serveurs, bases de données, clusters Kubernetes, consoles cloud, applications internes et serveurs MCP — sans VPN, sans mots de passe, ni identifiants statiques.

### APPROUVÉ PAR LES LEADERS

**L'INGÉNIERIE A BESOIN D'IAM À GRANDE ÉCHELLE**

## Pourquoi l'accès échoue

Le paysage des menaces moderne exploite facilement les identifiants. La complexité de l'infrastructure entrave les ingénieurs. À l'échelle de l'ingénierie, les modèles d'identité et d'accès du statu quo créent des failles de sécurité, des audits laborieux et une surcharge cognitive pour les ingénieurs.

**Les identifiants statiques se propagent partout**

**Les VPN et les hôtes bastion élargissent la surface d'attaque**

**Les privilèges permanents s'accumulent et persistent**

**La posture des appareils est inconnue ou ignorée**

**Les pistes d'audit sont fragmentées ou incomplètes**

## Teleport Zero Trust Access

Améliorer la résilience, accélérer les ingénieurs

Teleport unifie les identités et sécurise l'accès à l'ensemble de votre infrastructure grâce à :

Des identités utilisateur, machine et agent sécurisées cryptographiquement

Une authentification sans secrets

Des privilèges éphémères qui expirent

L'enregistrement des sessions et une piste d'audit

### Éliminer les secrets grâce à l'identité cryptographique

Supprimez les identifiants statiques pour éliminer le risque de vol et de réutilisation des identifiants, première source des violations de données. Teleport verrouille les surfaces d'attaque grâce à des identités cryptographiques résistantes au phishing, attribuées à tous les utilisateurs, machines et workloads, appareils, ressources, et à l'IA (agents et LLM).

**Appareils**

Attribuez des identités aux appareils clients inscrits équipés de TPM (ordinateurs portables, postes de travail, YubiKeys, et plus encore).

### Unifier le contrôle d'accès

**Décloisonnez l'accès grâce à un inventaire unifié de toutes les ressources d'infrastructure, éliminant le besoin de différents chemins d'accès, mots de passe, secrets partagés, vaults ou VPN.**

Teleport maintient un inventaire auto-actualisé des ressources informatiques de confiance, incluant les serveurs, les clouds, les bases de données, les clusters Kubernetes, les applications web, les serveurs MCP et les dépôts Git, ainsi que les appareils clients inscrits tels que les ordinateurs portables, postes de travail, YubiKeys, et plus encore.

### Réduire la surface d'attaque grâce aux privilèges éphémères

**Appliquez le principe du moindre privilège et réduisez la charge opérationnelle liée à la gestion des privilèges ou à l'application des politiques.**

Teleport remplace les mots de passe, les clés SSH, les tokens API et les identifiants de bases de données par des privilèges éphémères, accordés via des certificats de courte durée pour toutes les ressources. Ceux-ci sont liés à des appareils biométriques et à des enclaves sécurisées via l'autorité de certification intégrée de Teleport pour les certificats X.509 et SSH.

### Éliminer la complexité des VPN avec Teleport VNet

Teleport VNet connecte les identités à des ressources TCP internes, hors navigateur, sans VPN, sans redirection de port ni entrées DNS personnalisées, en utilisant des outils et des workflows familiers — éliminant ainsi l'exposition à l'internet public.

### Obtenir un audit complet et une visibilité totale sur les sessions

Collectez tous les événements générés par les humains, les machines et les agents à travers l'ensemble de votre infrastructure en un seul endroit, et exportez-les vers n'importe quelle plateforme SIEM ou de détection des menaces (y compris Teleport Identity Security) pour une analyse plus approfondie.

- **Événements d'audit basés sur l'identité :** collectez des événements d'audit structurés et détaillés pour chaque session, avec les données d'identité, d'application et de protocole.
- **Double autorisation :** exigez l'approbation de plusieurs membres d'équipe autorisés pour les actions hautement privilégiées (par ex. FedRAMP AC-3 et SOC 2).
- **Contrôles des sessions interactives :** enregistrez, relisez, rejoignez et modérez les sessions interactives SSH et Kubernetes.
- **Partage et modération des sessions :** exigez que vos sessions hautement privilégiées incluent toujours un modérateur pour prévenir les incidents de production et de sécurité.
- **Vue des sessions en direct :** visualisez chaque connexion authentifiée active à travers l'ensemble de votre infrastructure. Intervenez si nécessaire.
- **Enregistrement et lecture des sessions :** enregistrez les sessions pour un examen détaillé de qui a accédé à quoi et de ce qui s'est passé.
- **Accélérer la conformité :** Teleport sécurise les contrôles pour FedRAMP, SOC 2, ISO 27001, HIPAA, PCI DSS 4.0, NIS2, DORA, et plus encore.

RÉDUIRE LA COMPLEXITÉ DE L'INFRASTRUCTURE

## Unifier l'identité et l'accès à travers toutes les ressources d'infrastructure

Teleport sécurise l'accès des utilisateurs, des machines et des agents à travers le cloud, le code et les applications :

### Serveurs

### Bases de données

### Kubernetes

### Consoles cloud

### Applications web

### Serveurs MCP

### GitHub

VALEUR POUR TOUTES LES PARTIES PRENANTES

Conçu pour les équipes d'ingénierie modernes

### Sécurité et ingénierie plateforme

- Appliquer le Zero Trust pour l'identité, les appareils et l'accès
- Éliminer les risques liés aux identifiants et aux appareils
- Réduire considérablement la surface d'attaque
- Automatiser l'application de la conformité

### DevOps et SRE

- Un seul workflow pour tout
- Plus de gestion des clés SSH, des VPN ou des bastions
- Intégration et désinscription rapides
- Réponse aux incidents plus rapide

### Conformité et risque

### Équipes IA

- Humains, machines et agents unifiés
- Contrôles d'accès unifiés
- Sécurité IA agentique et MCP intégrée
- Aucun silo technologique
- Innovation rapide

## Approuvé par les équipes qui construisent des infrastructures critiques.

- Teleport est un partenaire technologique stratégique, car ils aident nos clients communs à faire évoluer leurs ressources AWS de manière sécurisée. Avec la solution d'accès à l'infrastructure native à l'identité de Teleport, les ingénieurs DevOps bénéficient d'une expérience fluide pour gérer une infrastructure qui ne nécessite pas de secrets, tout en mettant en œuvre une architecture zero trust sur AWS.
- Nous utilisons les Access Requests de Teleport en combinaison avec Auth0 pour gérer facilement l'accès à notre infrastructure. Avant Teleport, nous gérions manuellement des clés SSH et une machine bastion, et c'était un cauchemar organisationnel.
- Auparavant, nous devions passer par plusieurs étapes juste pour accéder aux ressources cloud, et maintenant cela se fait presque instantanément. Nos ingénieurs sont vraiment satisfaits de l'amélioration significative de leur workflow.
- La vision de Teleport pour l'Infrastructure Identity change la donne pour sécuriser les infrastructures hybrides.
- Avec Teleport, nous avons même pu fermer l'API Kubernetes sans perdre l'accès pour nos ingénieurs ou nos outils d'automatisation. Cela seul était une victoire énorme.
- Teleport nous permet de respecter les exigences réglementaires liées à l'exploitation d'une bourse internationale. L'utilisation d'hôtes bastion, l'intégration avec notre service d'identité et les capacités d'audit nous offrent un moyen conforme d'accéder à notre infrastructure interne.
- La solution Infrastructure Identity de Teleport offre un aperçu de l'avenir d'une informatique d'entreprise plus sûre, plus résiliente et plus rapide.
- Teleport a rendu l'obtention d'une ATO FedRAMP-Moderate bien plus accessible grâce à ses endpoints FIPS 140-2, à la facilité d'intégration avec notre SSO et notre MFA, et à la visibilité sur les journaux d'audit des sessions de connexion à distance, qui offre les informations nécessaires pour la surveillance continue.
- Au fil des nombreuses années d'utilisation de Teleport, cela a été un élément essentiel de mon infrastructure pour sécuriser l'accès et centraliser mon infrastructure dans un seul tableau de bord, sans avoir à naviguer entre plusieurs outils… Je ne sais pas comment je pourrais m'en passer.

### Ressources complémentaires

### Teleport Zero Trust Access

Découvrez comment fonctionne Zero Trust Access, y compris les concepts clés, les cas d'usage, et plus encore.

### Rush Street Interactive renforce la sécurité de son cloud

Découvrez comment Rush Street Interactive a éliminé les accès permanents et les ports SSH ouverts, tout en accélérant le provisionnement des accès par un facteur 3 grâce à Teleport.

### Sécuriser l'identité à l'ère de l'IA : guide d'achat Teleport

Découvrez comment Teleport résout les risques liés à l'identité IA grâce à une plateforme conçue pour les réalités des infrastructures pilotées par l'IA.

### Questions fréquentes

Teleport Zero Trust Access est une plateforme d'accès à l'infrastructure native à l'identité qui remplace les mots de passe, les clés SSH, les tokens API et les identifiants statiques par des certificats X.509 de courte durée liés à une identité cryptographique. Elle applique les principes fondamentaux du zero trust — vérifier explicitement, utiliser le moindre privilège, présumer la compromission — pour chaque connexion aux serveurs, bases de données, clusters Kubernetes, consoles cloud (AWS, GCP, Azure), applications web internes et serveurs MCP. Chaque session est authentifiée selon des politiques basées sur les rôles, limitée à une ressource spécifique, et enregistrée dans une piste d'audit infalsifiable liée à une identité vérifiée — et non à une adresse IP.

Un VPN accorde un accès réseau large après authentification — une fois connecté, un utilisateur peut atteindre tout ce qui se trouve sur ce segment réseau, sans contrôles au niveau des ressources et sans attribution de session. Teleport est une plateforme d'accès basée sur l'identité qui accorde l'accès à des ressources spécifiques — un serveur, une base de données ou un cluster Kubernetes précis — en utilisant des certificats de courte durée liés à une identité vérifiée. Chaque connexion est une requête distincte, authentifiée, autorisée et enregistrée. Parce que l'accès est limité aux ressources plutôt qu'aux segments réseau, une session compromise ne peut pas être utilisée pour se déplacer latéralement dans l'environnement. Teleport élimine également la charge opérationnelle liée à la gestion des configurations VPN, des règles de pare-feu et des hôtes bastion, en les remplaçant par une politique d'accès unique appliquée de manière cohérente dans chaque environnement. Pour une expérience de connectivité équivalente sans tunnel VPN, voir Teleport VNet.

Teleport VNet intercepte les requêtes DNS pour toute application TCP ou tout serveur SSH inscrit dans Teleport, et fait transiter les connexions via les contrôles d'identité et d'accès de Teleport, en gérant l'authentification par certificat de manière transparente en arrière-plan. Les ingénieurs se connectent aux services internes par nom d'hôte — la même expérience qu'un VPN — sans tunnel séparé, sans gestion d'IP interne, sans entrées DNS personnalisées ni reconfiguration de pare-feu. Contrairement à un VPN, chaque connexion via VNet est individuellement authentifiée, autorisée selon le rôle actuel de l'utilisateur et la posture de son appareil, et enregistrée. Aucune reconfiguration DNS n'est nécessaire, et VNet fonctionne de manière cohérente dans les environnements cloud, sur site et hybrides, sans configuration spécifique à chaque environnement.

Teleport met en œuvre un accès réseau zero trust en émettant des certificats X.509 de courte durée pour chaque connexion, en exigeant que chaque session soit explicitement authentifiée et autorisée avant d'atteindre une quelconque ressource. Il n'y a ni privilèges permanents, ni confiance réseau implicite, ni identifiants statiques à voler ou à réutiliser. L'accès est limité à des ressources individuelles — et non à des segments réseau — à l'aide de politiques basées sur les rôles qui prennent en compte l'identité, la posture de l'appareil et le contexte. Chaque session est enregistrée et attribuée à une identité vérifiée. Teleport applique ces principes ZTNA de manière uniforme sur les serveurs, les bases de données, Kubernetes, les consoles cloud et les applications internes depuis un seul plan de contrôle, plutôt que d'appliquer le zero trust uniquement au niveau réseau.

Teleport prend en charge l'authentification sans mot de passe via des clés matérielles WebAuthn (YubiKey, Touch ID, Windows Hello) et des appareils biométriques. Lorsqu'un utilisateur s'authentifie via son fournisseur d'identité ou directement via le SSO de Teleport, des certificats X.509 de courte durée liés à son identité vérifiée et à son appareil inscrit lui sont délivrés — ils expirent automatiquement à la fin de la session, ne laissant aucun identifiant persistant à voler, à faire tourner ou à exposer accidentellement. Les identités machine, les pipelines CI/CD et les agents IA s'authentifient selon le même modèle basé sur les certificats via l'agent tbot de Teleport, éliminant entièrement les tokens API et les clés SSH de longue durée des workflows d'automatisation.

Teleport Zero Trust Access sécurise les connexions aux serveurs et postes de travail Linux et Windows, aux bases de données (PostgreSQL, MySQL, MongoDB, CockroachDB, et plus), aux clusters Kubernetes, aux consoles cloud AWS/GCP/Azure, aux applications web internes, aux serveurs MCP et aux dépôts GitHub — tout cela depuis un seul plan de contrôle. Les ressources sont inscrites dans Teleport et maintenues dans un inventaire auto-actualisé grâce à la découverte automatique, de sorte que les nouvelles infrastructures sont protégées dès leur mise en service, sans configuration manuelle. Voir la liste complète des protocoles et ressources pris en charge.

Les VPN et les bastions traditionnels accordent un accès réseau large après un unique événement d'authentification — un identifiant compromis donne à un attaquant la même portée qu'un ingénieur légitime, sans barrière supplémentaire pour se déplacer dans l'environnement. Le modèle zero trust de Teleport élimine entièrement la confiance réseau implicite : chaque connexion nécessite une requête authentifiée distincte, utilisant un certificat de courte durée limité à une seule ressource spécifique. Il n'y a ni privilèges permanents ni identifiants persistants à récolter. Même si une session est compromise, le rayon d'impact est contenu à cette seule ressource et à cette seule session, avec un enregistrement complet de la session disponible pour une analyse forensique.

Oui. Teleport applique par défaut les contrôles d'accès requis par SOC 2, FedRAMP, ISO 27001, HIPAA et PCI DSS 4.0 — accès au moindre privilège, enregistrement des sessions, MFA et piste d'audit complète — plutôt que comme des options de configuration supplémentaires. Chaque session privilégiée est enregistrée avec une attribution d'identité complète, une double autorisation peut être exigée pour les actions sensibles, et des journaux d'audit structurés sont exportables vers des plateformes SIEM. Cela réduit considérablement le travail manuel de collecte de preuves qui précède généralement un audit, et favorise une surveillance continue de la conformité plutôt qu'une préparation ponctuelle.

La plupart des mises en œuvre du zero trust se concentrent sur les utilisateurs humains et laissent les identités machine — pipelines CI/CD, comptes de service, microservices et agents IA — s'appuyer sur des tokens API statiques, des clés SSH et des secrets de longue durée, difficiles à faire tourner et faciles à compromettre. Teleport étend le même modèle zero trust basé sur les certificats aux identités non humaines via Teleport Machine & Workload Identity. L'agent tbot délivre des certificats de courte durée aux machines et aux workloads, sous le même moteur de politiques et les mêmes contrôles RBAC que les utilisateurs humains, avec une journalisation d'audit complète et un accès juste-à-temps. Pour les agents IA et les LLM accédant aux ressources d'infrastructure via MCP, Teleport gouverne et enregistre leurs sessions de la même manière qu'il gouverne l'accès des ingénieurs — avec expiration automatique et sans identifiants persistants.

Tailscale et Google IAP résolvent tous deux des problèmes plus restreints que l'accès à l'infrastructure zero trust, et rencontrent des limites significatives à grande échelle.

Tailscale construit un réseau maillé chiffré basé sur WireGuard, qui améliore la connectivité des appareils par rapport aux VPN traditionnels — mais il opère toujours au niveau réseau. Une fois qu'un appareil est sur le tailnet, l'accès est régi par des listes de contrôle d'accès (ACL) basées sur l'IP plutôt que par des politiques d'identité par ressource. Il n'y a pas d'enregistrement natif des sessions, pas de piste d'audit attribuée à une identité, et pas d'accès juste-à-temps à des ressources individuelles. Un appareil compromis sur le tailnet conserve une large portée réseau.

Google IAP est un proxy natif GCP qui gère l'authentification pour les applications web s'exécutant sur Google Cloud. Il fonctionne bien dans ce périmètre, mais ne s'étend pas à SSH, aux bases de données, à Kubernetes ou à l'infrastructure sur site, ne peut pas gouverner les identités non humaines avec le même moteur de politiques, et ne produit aucun enregistrement de session ni journal d'audit structuré. Les équipes évoluant en multi-cloud ou en environnement hybride doivent superposer des outils supplémentaires pour combler les lacunes.

Teleport opère au niveau de l'identité et des ressources, à travers tous les environnements — en émettant des certificats de courte durée par connexion, en appliquant le moindre privilège selon des politiques basées sur les rôles, en enregistrant chaque session, et en appliquant les mêmes contrôles aux humains, aux machines et aux agents IA, que la ressource cible soit sur GCP, AWS, Azure ou sur site. Voir les comparaisons complètes : Teleport vs. Tailscale et Teleport vs. Google IAP.

Teleport Zero Trust Access fait du moindre privilège la norme par défaut, en accordant l'accès juste-à-temps et en l'expirant automatiquement, de sorte qu'aucune identité ne détient de permissions permanentes et que chaque attribution est explicite. Les architectes appliquent une politique unique sur les serveurs, Kubernetes, les bases de données et les consoles cloud, et l'étendent à de nouvelles ressources au fur et à mesure que le périmètre s'agrandit, sans reconstruire les accès pour chaque système. Les rôles et les règles d'accès sont livrés en tant qu'infrastructure-as-code pour garantir la cohérence à grande échelle.

Teleport Zero Trust Access émet automatiquement une identité cryptographique de courte durée via une seule CLI et une interface graphique dans Teleport Connect, de sorte que les ingénieurs obtiennent un accès à moindre privilège et juste-à-temps à n'importe quelle ressource en quelques commandes, plutôt qu'en ouvrant des tickets et en attendant. L'accès est transparent pour les workflows existants, ce qui maintient une vélocité élevée tout en supprimant les privilèges permanents et les secrets partagés. L'expérience développeur est une exigence de conception pour Teleport, pas une réflexion après coup.

Oui. Teleport Zero Trust Access donne aux ingénieurs un accès à moindre privilège aux serveurs SSH, à Kubernetes, aux bases de données et aux consoles cloud depuis un seul plan de contrôle, en utilisant une identité cryptographique de courte durée et une seule CLI. L'accès est juste-à-temps et enregistré, de sorte qu'une seule plateforme couvre tous les types de ressources au lieu d'un outil d'accès séparé par protocole.

Teleport élimine les privilèges permanents grâce à un accès juste-à-temps qui expire automatiquement, et élimine la prolifération d'identifiants en remplaçant les secrets par une identité cryptographique de courte durée plutôt qu'en les stockant ou en les faisant tourner. Les équipes plateforme se retrouvent sans comptes permanents actifs et sans clés de longue durée en production, et chaque accès est à moindre privilège et enregistré dans un seul journal d'audit.

Oui. Teleport délivre une identité cryptographique de courte durée aux identités humaines et non humaines sur une seule couche d'identité unifiée, de sorte que les ingénieurs, les services, les workloads et les agents s'authentifient de la même manière et détiennent un accès à moindre privilège qui expire automatiquement. Teleport Zero Trust Access couvre l'accès humain et Teleport Machine & Workload Identity couvre l'accès non humain, sous une seule plateforme et une seule piste d'audit.

## Pourquoi ça compte

Cette page illustre comment le marché de la gestion des accès évolue vers des identités cryptographiques éphémères plutôt que des identifiants statiques, une tendance clé pour sécuriser les infrastructures hybrides et l'essor des agents IA/MCP. C'est aussi un bon indicateur du positionnement marketing des fournisseurs Zero Trust et de leurs arguments face à des alternatives comme les VPN classiques, Tailscale ou Google IAP.
