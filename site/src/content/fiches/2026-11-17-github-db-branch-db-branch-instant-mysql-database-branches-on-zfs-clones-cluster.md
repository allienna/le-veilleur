---
title: "GitHub - db-branch/db-branch: Instant MySQL database branches on ZFS clones, clustered across VMs with ProxySQL routing"
date: 2026-11-17
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fgithub.com%2Fdb-branch%2Fdb-branch%3Futm_source=tldrdata/1/010001a1e4102a7f-1707763f-bcae-44fd-9622-7435fac8cdc6-000000/f8w8VDZJ1oOEc6uQJU9SKsZqAZp0qNo2SFuLL3FSnng=452"
keywords: ["base de données", "ZFS", "copy-on-write", "agents IA", "CI/CD", "open-source"]
theme: "Software"
tone: "tutorial"
used_in: ["2026-11-17"]
---

## Résumé
db-branch est un outil open-source (Apache-2.0) qui crée des branches instantanées et en copy-on-write de bases de données MySQL et PostgreSQL grâce aux clones ZFS, sans copier les données. Il vise à donner à chaque pull request, agent IA ou test de migration sa propre copie jetable d'une base de données volumineuse, prête en quelques secondes. Le projet, encore en version Beta, est auto-hébergé sur Ubuntu/ZFS et propose une interface unique : CLI, API REST, console web et serveur MCP pour les agents LLM. Le cœur est libre, tandis que des modules gratuits (ProxySQL, masquage de données) et des modules payants à code source fermé (SSO, audit, historique, diff, stockage FSx) complètent l'offre ; il n'existe aucune version hébergée ou cloud.

## Points clés
- Clonage copy-on-write via ZFS : une branche PostgreSQL est prête en environ 0,5 s, une branche MySQL en environ 3 s, sans aucun octet copié à la création.
- Cas d'usage principaux : bac à sable pour agents IA via un serveur MCP intégré, une base de données dédiée par pull request/CI, et test de montées de version majeures avant de toucher la base réelle.
- Fonctionnalités de gestion d'état : checkpoints instantanés, restauration, reset complet, et montée de version par branche avec rollback automatique en cas d'échec.
- Architecture en cluster Raft multi-nœuds, avec routage ProxySQL optionnel pour que les applications gardent une seule adresse.
- Modèle économique : cœur Apache-2.0 auto-hébergé, modules payants à code fermé (auth/SSO, audit, historique, diff, FSx) activés par clé de licence, aucune offre cloud hébergée.
- Prérequis techniques stricts : Ubuntu 24.04/26.04 LTS et un pool ZFS ; une démo en ligne et un chemin d'évaluation via Multipass (VM Ubuntu) sont proposés pour les machines Mac/Windows.

## Analyse approfondie

Des branches de bases de données instantanées pour MySQL et PostgreSQL, sur vos propres serveurs.

Testez une migration, laissez un agent IA agir en liberté, ou donnez à chaque pull request sa propre copie de la base de données. db-branch crée en quelques secondes une branche en copy-on-write d'une grosse base de données, sans rien copier. Cassez-la, réinitialisez-la, jetez-la. Construit sur des clones ZFS, auto-hébergé, sous licence Apache-2.0.

**Statut : Beta.** db-branch est utilisable dès aujourd'hui, mais les API et les détails de la ligne de commande peuvent encore changer avant la version 1.0. C'est un projet open-source indépendant, construit à partir de zéro.

**Comment l'essayer**

1. **Dans votre navigateur, 0 minute.** Une démo de console en direct tourne entièrement dans la page (rien de réel n'est créé) : https://demo.db-branch.com/
2. **Sur une machine Mac ou Windows, environ 2 minutes.** db-branch a besoin de Linux et de ZFS ; faites-le donc tourner dans une VM Ubuntu avec Multipass. Une seule commande crée la VM, installe db-branch, l'initialise sur un pool ZFS appuyé sur un fichier, et charge une petite base d'exemple, `shop` (MySQL 8.4) :

```
multipass launch 24.04 --name db-branch-eval --memory 4G --disk 30G --timeout 900 \
  --cloud-init https://raw.githubusercontent.com/db-branch/db-branch/main/scripts/eval-cloud-init.yaml
multipass exec db-branch-eval -- cloud-init status --wait   # attendre la fin de l'installation (environ deux minutes)
multipass exec db-branch-eval -- cat /etc/motd              # URL de la console et identifiants de connexion (admin / admin), ou la raison de l'échec
multipass shell db-branch-eval   # puis : sudo db-branch branch create try --base shop --ttl 1h --record
```

Sous Windows (PowerShell ou cmd), mettez la commande `multipass launch` sur une seule ligne et supprimez le `\` :

```
multipass launch 24.04 --name db-branch-eval --memory 4G --disk 30G --timeout 900 --cloud-init https://raw.githubusercontent.com/db-branch/db-branch/main/scripts/eval-cloud-init.yaml
```

   - Le module historique est activé, et les modules payants fonctionnent pendant 30 jours sans clé. `--record` enregistre une branche afin qu'elle puisse être restaurée à n'importe quel point.
   - Le pool est un fichier, donc c'est plus lent et ce n'est pas fait pour des données réelles. Le mot de passe admin initial est `admin` ; la console en demande un nouveau à la première connexion.
   - Sur Apple Silicon (et les autres machines arm64), l'installation télécharge environ 800 Mo pour MySQL, contre 80 Mo sur Intel, car Oracle ne fournit pas de build minimal pour arm64. `--timeout 900` évite que `launch` abandonne sur une connexion lente.
   - Si l'installation échoue, `/etc/motd` l'indique, et `sudo tail -n 30 /var/log/cloud-init-output.log` dans la VM montre pourquoi.
   - Supprimez la VM avec `multipass delete --purge db-branch-eval`.
3. Le module historique est activé, et les modules payants fonctionnent pendant 30 jours sans clé.
4. **Sur votre propre serveur Ubuntu.** Voir la section Installation.

**Cas d'usage**

- **Bacs à sable pour agents IA.** Le serveur MCP intégré permet à un agent LLM de créer une branche, d'y exécuter une requête ou une migration risquée, puis de supprimer la branche, afin que les données de production ne soient jamais touchées.
- **Une base de données par pull request.** Chaque exécution CI ou PR obtient sa propre copie d'une grosse base de données, prête en quelques secondes, et supprimée via `--ttl` quand elle n'est plus nécessaire.
- **Vérifications de montée de version.** Exécutez d'abord une montée de version majeure (par exemple MySQL 8.0 vers 8.4) sur une branche, avec `branch upgrade --check-only` pour voir sur quoi elle tomberait, avant de toucher la base.

**Fonctionnalités**

- **Branches en quelques secondes.** Sur notre propre cluster de test à 3 nœuds, une branche PostgreSQL est prête en environ 0,5 s et une branche MySQL en environ 3 s, avec 0 octet copié à la création (copy-on-write).
- **Réinitialisation et expiration.** `branch reset` ramène une branche à son état de création ; `--ttl` la supprime automatiquement.
- **Checkpoints.** `branch checkpoint` sauvegarde instantanément l'état d'une branche en cours d'exécution ; `branch restore` la remet en place. La restauration remplace l'état actuel, et chaque checkpoint déjà existant reste restaurable.
- **Montées de version par branche.** `branch upgrade` fait passer une branche à une version plus récente de MySQL ou PostgreSQL, tandis que la base et les autres branches restent inchangées. Un checkpoint est sauvegardé au préalable, et une montée de version échouée revient automatiquement en arrière.
- **MySQL et PostgreSQL, plusieurs versions à la fois.** Les runtimes des moteurs sont installés par version et peuvent coexister.
- **Une seule interface partout.** CLI, API REST, console web et serveur MCP (permettant aux agents LLM de créer et d'interroger leurs propres branches) utilisent tous la même API.
- **Nœud unique ou cluster.** Un cluster Raft de VMs, avec un routage ProxySQL optionnel pour que les applications gardent une seule adresse.

**Prérequis :** Ubuntu 24.04 LTS ou 26.04 LTS, et un pool ZFS (le paquet `zfsutils-linux` est installé comme dépendance).

```
curl -fsSL https://apt.db-branch.com/db-branch.gpg | sudo tee /usr/share/keyrings/db-branch.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/db-branch.gpg] https://apt.db-branch.com stable main" | sudo tee /etc/apt/sources.list.d/db-branch.list
sudo apt update && sudo apt install db-branch
sudo db-branch init --pool <zpool>
```

L'empreinte de la clé de signature du dépôt est `3F404C4E5D49FA653F8385692C6E89E341D4D7A5`. `db-branch init` affiche le mot de passe admin initial une seule fois.

```
db-branch runtime install postgres@18.6                                     # une version de moteur de base de données
db-branch base create prod --runtime postgres@18.6 --dump prod.sql.gz       # une base : vos données, chargées une fois
db-branch branch create feature-x --base prod --ttl 72h                     # une branche : instantanée, copy-on-write
db-branch branch dsn feature-x                                              # URL de connexion (inclut le mot de passe)
db-branch branch checkpoint feature-x --name before-migration               # sauvegarder l'état (instantané)
db-branch branch restore feature-x before-migration                        # revenir à l'état sauvegardé
db-branch branch reset feature-x                                           # annuler tous les changements
db-branch branch delete feature-x                                          # la supprimer
```

MySQL fonctionne de la même façon, par exemple `mysql@8.4.13`. Listez les versions installables avec `db-branch runtime available`. Pour tester une montée de version sur une branche MySQL :

```
db-branch branch upgrade feature-x --runtime mysql@8.4.13 --check-only      # sur quoi la montée de version tomberait-elle ?
db-branch branch upgrade feature-x --runtime mysql@8.4.13                   # déplace uniquement cette branche ; un checkpoint est sauvegardé au préalable
```

Une base est un dataset ZFS contenant une base de données chargée. Une branche est un clone ZFS d'un snapshot de base, si bien que sa création ne copie rien, et chaque branche exécute son propre serveur de base de données sur son propre port. Optionnellement, ProxySQL route les connexions clientes vers la bonne branche par nom d'utilisateur (ou via un commentaire de requête `/*db_branch='name'*/`). Plusieurs nœuds forment un cluster Raft qui partage les bases, les branches, les paramètres et les utilisateurs.

**Modules**

- **Cœur (ce dépôt), Apache-2.0 :** branches, bases, runtimes, clustering, CLI, API, console web, MCP, monitoring, notifications, branches anonymes (sans connexion) avec limites, rafraîchissement programmé des bases, sauvegarde de l'état du cluster.
- **Modules gratuits** dans le même dépôt apt : `proxysql`, `greenmask`, `greenmask-mysql`, `anon` (routage et masquage de données).
- **Modules payants** (authentification/SSO, audit, historique, diff, stockage FSx) sont des paquets séparés, à code source fermé, auto-hébergés et activés avec une clé de licence (mensuelle ou annuelle). Un workflow de masquage gouverné est prévu en beta optionnelle et ne fait partie d'aucune offre pour l'instant. Voir docs/modules.md pour les points d'extension qu'ils utilisent.

Il n'existe pas de version hébergée ou cloud de db-branch.

**Documentation**

- docs/README.md : index des documents de conception et de référence (rédigés en japonais)
- Documentation utilisateur en anglais : https://db-branch.com/docs/
- Site web : https://db-branch.com (anglais), https://db-branch.com/ja/ (japonais)
- api/openapi.yaml : définition de l'API REST lisible par machine
- CHANGELOG.md

**Contribution et support**

- Les contributions sont bienvenues : voir CONTRIBUTING.md. Les commits nécessitent une signature DCO (`git commit -s`).
- Problèmes de sécurité : voir SECURITY.md. Merci d'utiliser le signalement privé de vulnérabilités, et non les issues publiques.
- Support : voir SUPPORT.md. Aucun support n'est garanti ; les issues sont lues quand c'est possible.
- Merci de respecter le Code de conduite.

**Licence**

Apache-2.0. Voir LICENSE et NOTICE.

**Résumé en japonais (traduit)**

db-branch est un outil qui crée, réinitialise et détruit des branches de bases de données MySQL/PostgreSQL via des clones ZFS. Il est actuellement en version Beta et l'API pourrait évoluer avant la version 1.0. Le cœur est sous licence Apache-2.0 ; les modules payants (authentification/SSO, audit, historique, diff, stockage FSx) sont des paquets séparés (à code source fermé, auto-hébergés, avec clé de licence).

Sur Mac/Windows, on peut l'essayer avec une seule commande Multipass : https://db-branch.com/ja/docs/getting-started/#multipass-ですぐ試す (essai rapide via Multipass). Le site en japonais se trouve à https://db-branch.com/ja/, et la documentation de conception se trouve dans docs/ (en japonais).

## Pourquoi ça compte
db-branch illustre une tendance de fond : l'infrastructure de données devient aussi « jetable » et scriptable que le code, via le copy-on-write ZFS, ce qui change la donne pour les tests de migration, les environnements de CI/CD et surtout les agents IA autonomes qui ont besoin d'un bac à sable sûr sur des données réalistes.
