---
title: "How to Eliminate Shared Database Passwords: MySQL, PostgreSQL, and More"
date: 2026-10-15
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Ffandf.co%2F4hm6kP4/1/010001a13a5aa09e-34e2f72b-f2ca-4fc4-b6b9-06b3141e4efd-000000/Y34VHb433ETSjPObpIWkJd0jBuCATOg8a36kit80gpM=452"
keywords: ["gestion des identités", "sécurité des bases de données", "Teleport", "zero standing privileges", "agents IA", "audit"]
theme: "Sécurité"
tone: "tutorial"
used_in: ["2026-10-15"]
---

## Résumé
Cet article de Teleport explique comment les mots de passe de base de données partagés créent des angles morts en matière de sécurité et de conformité, un problème amplifié par l'arrivée des agents IA capables d'interagir avec des données de production. Il présente l'approche de Teleport reposant sur une identité cryptographique, des certificats X.509 de courte durée et des rôles mappés sur le SSO pour remplacer les identifiants statiques dans MySQL, PostgreSQL et d'autres bases de données. Le guide détaille l'enregistrement des bases, la connexion via CLI (`tsh`) ou GUI (Teleport Connect), la définition de rôles YAML à permissions granulaires, l'exigence de MFA matériel pour les accès en écriture, et l'attribution de chaque requête à une identité précise dans un journal d'audit exportable vers un SIEM. Un cas client (Turo) illustre ces principes à grande échelle.

## Points clés
- Les mots de passe partagés empêchent d'attribuer une action à une personne précise, ce qui complique les audits de conformité et la réponse à incident.
- Teleport remplace les identifiants statiques par des certificats X.509 de courte durée liés à une identité cryptographique issue de l'IdP de l'entreprise.
- Les rôles Teleport (définis en YAML) permettent des permissions granulaires (SELECT, INSERT, UPDATE, DELETE) par base de données et par groupe SSO, sans provisionnement manuel.
- L'accès en écriture peut être verrouillé derrière une authentification multifacteur matérielle (ex. Touch ID), y compris pour les agents IA comme Claude Code, qui doivent obtenir une approbation humaine avant d'écrire en production.
- Chaque requête est journalisée avec l'identité réelle de l'exécutant (champ `teleport_user`), indépendamment du nom d'utilisateur de base de données partagé, et ces journaux peuvent être envoyés vers un SIEM (Splunk, Datadog, Elastic) ou un bucket S3.
- La connexion reste possible via CLI (`tsh db connect`) ou via GUI (Teleport Connect) avec les clients existants (psql, pgAdmin, DBeaver, MongoDB Compass).

## Analyse approfondie
# Comment éliminer les mots de passe de base de données partagés : MySQL, PostgreSQL, et plus

Traditionnellement, les ingénieurs se sont appuyés sur des mots de passe de base de données partagés. Lorsqu'une personne a besoin d'exécuter une requête, soit elle dispose déjà d'un accès permanent accordé via un identifiant statique que toute l'équipe connaît, soit quelqu'un doit se précipiter pour créer une solution de contournement rapide. Chaque nouvel utilisateur, chaque règle d'exception, ou chaque redirection de port via un hôte bastion devient un correctif « juste cette fois ».

Mais à mesure que les équipes et l'infrastructure se développent, ces correctifs « ponctuels » peuvent se transformer en problèmes plus importants. Par exemple, un nom d'utilisateur de base de données partagé peut rendre impossible l'attribution d'actions à une identité individuelle. Au moment d'une revue d'incident ou d'un audit de conformité, les journaux peuvent vous dire que quelque chose s'est produit dans cette base de données, mais pas qui en est responsable. Et à mesure que les agents IA rejoignent votre infrastructure et commencent à toucher aux données de production, comprendre quel humain ou quel agent peut accéder à vos bases de données n'a jamais été aussi urgent.

### Lisez ce guide pour apprendre :

- Comment les privilèges de base de données de courte durée éliminent les identifiants statiques
- Comment utiliser Teleport pour accéder à MySQL, PostgreSQL et d'autres bases de données à l'aide de certificats de courte durée
- Comment configurer des rôles de base de données et exiger une approbation par clé matérielle pour les accès en écriture
- À quoi ressemble l'attribution au niveau des requêtes dans le journal d'audit de Teleport

## Comment les privilèges de base de données de courte durée éliminent les identifiants statiques

Ces défis proviennent des identifiants statiques ou de l'emplacement réseau. Alors qu'un mot de passe donne accès à quiconque le détient et qu'un VPN donne accès à tout ce qui se trouve derrière lui, ni l'un ni l'autre ne répond à la question de savoir quel utilisateur ou quelle machine se connecte réellement, ce qu'il est autorisé à faire, ou quand ses privilèges doivent expirer.

L'identité cryptographique résout ces défis en rattachant des privilèges liés à une tâche à l'identité demandeuse (tirée de votre IdP) plutôt qu'à un secret ou une plage d'adresses IP. Les permissions suivent cette identité, ne s'appliquent que tant que le rôle s'applique, et relient chaque action à la personne ou à la charge de travail responsable. Les sections suivantes expliquent comment Teleport établit cette identité, applique une politique à son égard, et enregistre ce que fait chaque identité une fois connectée à MySQL, PostgreSQL, ou d'autres bases de données critiques.

## Comment fonctionne l'accès aux bases de données avec Teleport

Avec Teleport, chaque connexion à une base de données utilise un certificat X.509 de courte durée dans lequel est encodée l'identité cryptographique de l'utilisateur, de sorte qu'il n'y a ni mot de passe partagé ni privilège permanent. À la place, des permissions de courte durée liées à une tâche sont accordées via l'identité SSO et expirent en même temps que le certificat. Chaque action et chaque requête sont attribuées à cette identité dans le journal d'audit, qu'elles aient été effectuées par un humain, une machine, ou un agent IA.

Du point de vue de l'utilisateur, le flux est simple : s'authentifier à l'aide d'une identité vérifiée plutôt que de secrets partagés, et Teleport se charge d'établir un chemin sécurisé vers la base de données via des tunnels inversés (reverse tunnels).

### Enregistrement des bases de données

L'enregistrement des ressources de base de données auprès de Teleport peut être automatique ou manuel. Vous pouvez configurer une relation de confiance basée sur IAM avec des fournisseurs cloud comme AWS, GCP et Azure, et Teleport peut découvrir automatiquement les nouvelles bases de données à mesure qu'elles sont mises en ligne. Pour les bases de données auto-hébergées, Teleport utilise l'authentification par certificat client.

Les politiques basées sur les rôles dans Teleport sont directement mappées sur votre IdP, de sorte que les permissions reflètent le rôle organisationnel actuel de chaque utilisateur, et non une affectation statique faite quelques mois plus tôt. Les administrateurs peuvent accorder des permissions en lecture seule ou en lecture/écriture, ou configurer Teleport pour provisionner dynamiquement des utilisateurs de base de données selon les besoins. Chaque requête est attribuée à une identité cryptographique dans le journal d'audit, quel que soit le nom d'utilisateur de base de données sous-jacent, garantissant qu'il existe toujours un enregistrement traçable de qui a fait quoi et quand.

### Connexion via la CLI

Une fois qu'une base de données est enregistrée et que le rôle d'un utilisateur inclut des permissions de base de données, la connexion via la CLI est simple grâce au client `tsh`, l'interface en ligne de commande principale de Teleport. Avec `tsh`, il suffit de se connecter et d'exécuter :

`% tsh db connect <ressource de base de données> --db-user=<utilisateur> --db-name=<nom de la base de données>`

Dans cet exemple, Teleport ouvre le client CLI approprié (psql pour PostgreSQL, mysql pour MySQL, etc.) comme si vous vous étiez connecté directement.

### Connexion via une interface graphique (GUI)

En plus de la CLI, vous pouvez également utiliser des outils graphiques pour vous connecter aux ressources de base de données. Teleport Connect, qui fournit un accès simple et sécurisé aux serveurs SSH, aux bases de données, aux applications, aux serveurs MCP et aux clusters Kubernetes, vous permet de vous authentifier une seule fois puis d'ouvrir un port local auquel n'importe quel client de base de données peut se connecter. La plupart des clients graphiques — comme PGAdmin, DBeaver, MongoDB Compass, et d'autres — peuvent tous se connecter via localhost sur un port de tunnel attribué. Cela vous permet de conserver vos outils et flux de travail existants tout en éliminant le besoin d'identifiants partagés et de VPN, et garantit que chaque action est attribuée à une identité cryptographique dans le journal d'audit.

Par exemple, Teleport Connect vous permet de vous connecter à Teleport et de définir un écouteur de port local pour que PGAdmin puisse s'y connecter.

*Configuration de Teleport Connect pour ouvrir un port local.*

*Utilisation du port local pour se connecter à PGAdmin.*

### Les rôles Teleport comme politique de base de données

Les rôles Teleport définissent ce que chaque identité peut faire dans une base de données, y compris les utilisateurs sous lesquels elle peut se connecter, les bases de données auxquelles elle peut accéder, et avec quelles permissions. Les rôles sont directement mappés sur votre fournisseur SSO, de sorte que la politique suit les attributs organisationnels de l'utilisateur : équipe, groupe, ou manager. Lorsqu'une personne change de rôle ou quitte l'organisation, ses privilèges sont mis à jour automatiquement.

Voici un exemple de rôle Teleport qui accorde un accès en lecture seule à une base de données PostgreSQL avec création dynamique d'utilisateur, créant un utilisateur appelé « analyst » avec des permissions `SELECT` :

```
kind: role
version: v7
metadata:
  name: db-analyst
spec:
  allow:
    db_labels:
      env: production
    db_names:
      - analytics
    db_users:
      - analyst
    db_permissions:
      - match:
          object_kind: table
        permissions:
          - SELECT
  options:
    create_db_user_mode: keep
```

Le rôle défini ici est hérité en fonction du groupe de l'utilisateur ; il n'y a ni transmission d'identifiant ni mot de passe partagé. Cela garantit que l'utilisateur accède au système et effectue son travail, mais s'il quitte l'équipe des analystes, le rôle ne s'applique plus et il ne peut plus accéder à la base de données avec cette politique. Ceci est particulièrement utile pour les équipes disposant de nombreuses bases de données ou dans des environnements où les personnes ne devraient pas avoir de privilèges permanents.

### Application de la clé matérielle pour les rôles de base de données

Dans les bases de données sensibles, l'accès en lecture devrait être contrôlé séparément de l'accès en écriture. Les exigences de sécurité devraient toujours être plus élevées pour les rôles pouvant écrire dans une base de données, et plus encore avec la montée des agents IA.

Teleport vous permet d'exiger une authentification multifacteur (MFA) par session pour des rôles spécifiques, ce qui signifie qu'un utilisateur doit se ré-authentifier avec une clé matérielle ou une donnée biométrique (comme Touch ID sur un Mac) avant que la session ne soit ouverte. Par exemple, voici un rôle qui accorde un accès en lecture-écriture, mais qui exige une ré-authentification par Touch ID pour chaque session :

```
kind: role
version: v7
metadata:
  name: db-engineer
spec:
  allow:
    db_labels:
      env: production
    db_names:
      - analytics
    db_users:
      - engineer
    db_permissions:
      - match:
          object_kind: table
        permissions:
          - SELECT
          - INSERT
          - UPDATE
          - DELETE
  options:
    create_db_user_mode: keep
    require_session_mfa: hardware_key_touch
```

Lorsqu'un utilisateur disposant de ce rôle exécute `tsh db connect`, Teleport demande un contact physique sur une clé de sécurité matérielle avant d'ouvrir la session de base de données.

Cela s'applique également aux agents IA tout comme aux utilisateurs humains. Bien que les agents puissent être configurés pour interroger des bases de données, l'accès en écriture — celui qui peut modifier, supprimer ou exfiltrer des données — est verrouillé derrière un rôle qui exige qu'un humain l'approuve physiquement. Par exemple, un utilisateur disposant de Claude Code sur son poste de travail devrait approuver manuellement une tâche nécessitant un accès en écriture à l'aide de la biométrie. Cela garantit que les agents ne peuvent pas escalader leurs propres privilèges ni procéder sans qu'un humain soit dans la boucle. Et même si un agent découvre un identifiant intégré, reçoit des instructions plus larges, ou subit une injection de prompt, il est incapable d'agir au-delà de ce que le rôle autorise.

### Enregistrement des sessions de base de données avec attribution d'identité

Alors que les contrôles d'accès vous indiquent qui devrait se trouver dans vos bases de données, le journal d'audit vous indique ce qu'ils ont réellement fait. Teleport capture une piste d'audit complète et inviolable pour chaque requête émise, indiquant contre quelle base de données, par quelle identité, et quand — le tout attribué à une identité cryptographique dans le journal d'audit, et non simplement à l'utilisateur de base de données auquel ils se sont connectés.

Voici à quoi ressemble un événement d'audit typique pour une requête de lecture :

```
{
  "event": "db.session.query",
  "uid": "a3c2e891-4f12-4b56-8932-1234abcd5678",
  "code": "TDB03I",
  "time": "2026-05-20T14:32:11.204Z",
  "cluster_name": "teleport.example.com",
  "db_service": "postgres-prod",
  "db_name": "analytics",
  "db_user": "analyst",
  "teleport_user": "[email protected]",
  "db_query": "SELECT order_id, total FROM orders WHERE customer_id = 42",
  "success": true
}
```

Le champ `teleport_user` désigne la personne, la charge de travail, ou l'agent IA responsable de la requête, et non simplement l'utilisateur de base de données. Cela garantit que même si plusieurs personnes partagent le même nom d'utilisateur de base de données, vous saurez toujours qui a réellement exécuté la requête. Le journal d'audit est stocké dans le backend de Teleport et peut être diffusé vers votre SIEM de choix — y compris Splunk, Datadog, Elastic, et d'autres — ou vers un bucket S3 pour une conservation à long terme.

Consultez la documentation de référence sur les événements d'audit pour d'autres exemples d'événements d'audit de base de données Teleport, ainsi que des exemples issus des sessions MCP, Kubernetes, et autres.

## Pourquoi les bases de données ont besoin d'une identité d'infrastructure unifiée

L'ère des mots de passe partagés est révolue. Non pas parce que la conformité l'exige, mais parce que votre infrastructure, et les agents IA qui y fonctionnent désormais, exigent quelque chose de plus responsable.

Teleport établit une couche d'identité unifiée à travers vos bases de données, serveurs, clusters Kubernetes et consoles cloud, qui instaure une identité cryptographique, des certificats de courte durée, zéro privilège permanent, et une piste d'audit complète pour chaque ressource, chaque identité, humaine ou machine. Cela signifie que vos ingénieurs continuent d'utiliser psql, pgAdmin, ou le client de leur choix, que les bases de données n'ont pas besoin de migrer vers une DMZ ni de nécessiter un saut VPN, et que les agents fonctionnent sans privilèges permanents sur les données de production.

En savoir plus sur Teleport pour l'accès aux bases de données.

### Comment Turo élimine les identifiants de base de données statiques avec Teleport

Lisez cette étude de cas pour découvrir comment Turo, la plus grande place de marché de partage de voitures entre particuliers au monde, utilise Teleport pour :

- Éliminer les identifiants de base de données statiques et les privilèges permanents
- Automatiser l'application des politiques sur Amazon RDS, EKS, et plus encore
- Offrir aux ingénieurs un accès rapide et sans friction aux bases de données dont ils ont besoin

## Articles connexes

### Rendre l'accès à PostgreSQL plus simple et plus sécurisé avec Teleport

Découvrez comment simplifier et sécuriser l'accès à PostgreSQL grâce à un accès unifié et juste-à-temps sur l'ensemble des clouds et des centres de données, qui permet à vos ingénieurs de garder leur rythme.

### Accéder aux bases de données AWS RDS dans EKS avec Teleport Machine ID, sans mot de passe

Découvrez comment sécuriser l'accès aux bases de données dans des charges de travail Kubernetes. Éliminez les secrets, conservez les bases de données dans des réseaux privés, et améliorez la journalisation d'audit avec Teleport.

### Comment les contrôles d'accès aux bases de données ont évolué pour répondre aux besoins modernes de sécurité

Découvrez comment les contrôles d'accès aux bases de données de Teleport — incluant les permissions au niveau des objets et l'intégration Identity Security — offrent une sécurité et une facilité d'utilisation renforcées.

## Pourquoi ça compte
À mesure que les agents IA obtiennent un accès direct aux bases de données de production, l'incapacité à distinguer qui — humain ou machine — a exécuté quelle requête devient un risque de sécurité et de conformité majeur. Cette approche d'identité cryptographique éphémère, combinée à une approbation humaine obligatoire pour les écritures, illustre un modèle de gouvernance concret et déjà opérationnel pour encadrer les agents autonomes en production.
