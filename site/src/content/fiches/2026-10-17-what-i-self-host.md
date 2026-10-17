---
title: "What I Self-Host"
date: 2026-10-17
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fviceconsole.fyi%2Fblog%2F2026%2F10%2F10%2Fwhat-i-self-host%2F%3Futm_source=tldrdev/1/010001a1446c42ee-4d96ed48-b174-40ed-b642-fd7917216e65-000000/Sa8hc4kmuN1WkO61kvSvaeHfO7aILMG8vPosVqn8Svo=452"
keywords: ["autohébergement", "Podman", "vie privée", "serveur domestique", "open source", "systemd"]
theme: "Tech"
tone: "opinion"
used_in: ["2026-10-17"]
---

## Résumé
L'auteur, autohébergeur de longue date, raconte comment il a progressivement remplacé les services cloud et le streaming payant par une infrastructure personnelle tournant sur un simple mini-PC (Beelink S12 Pro, Intel N100, 16 Go de RAM). Le billet détaille une trentaine de services autohébergés (médias, domotique, finances, sauvegardes, mot de passe, etc.), les règles qu'il s'impose (pas d'exposition directe à Internet, préférence pour les binaires natifs via systemd plutôt que Docker, usage ciblé de Podman) et les solutions qu'il a délibérément écartées. Le message central : avec de la discipline sur les choix techniques (résolution vidéo réduite, SQLite plutôt que des piles lourdes PostgreSQL/Redis, binaires uniques), un matériel modeste suffit largement à remplacer la dépendance au cloud.

## Points clés
- Abandon des abonnements de streaming (Netflix, Disney+, Spotify) au profit de Jellyfin, pour échapper au "tapis roulant de l'engagement" (autoplay, recommandations) imposé aux enfants.
- Règle de sécurité stricte : aucun service exposé directement sur Internet, seul le VPN du routeur est joignable publiquement, et uniquement en IPv6 (le CGNAT de son FAI bloque déjà l'IPv4 entrant).
- Préférence marquée pour les services nativement installés et gérés par systemd plutôt que pour des piles Docker lourdes ; Podman est utilisé pour les services plus complexes, mais Docker est banni par lassitude de gérer deux systèmes de gestion de services.
- Tout tourne sur un mini-PC à 180 € (Intel N100, 16 Go RAM, SSD 512 Go + disque 6 To), avec seulement ~7,5 Go de RAM utilisés pour 17 services natifs et 11 conteneurs Podman.
- Des choix d'optimisation récurrents : résolutions vidéo abaissées (720p, voire moins pour les DVD rippés) pour économiser CPU/RAM/disque, SQLite privilégié aux bases serveur lourdes.
- Certains outils (pile *arr, Collabora Online, Firefly III, OwnTracks, Music Assistant) ont été testés puis écartés pour complexité excessive ou mauvais rapport ressources/valeur.

## Analyse approfondie

### Introduction
L'auteur autohéberge depuis ses études, quand il faisait tourner un site web sur une machine Linux sous son lit (jusqu'à ce que son colocataire, gêné par le bruit du ventilateur, l'éteigne). Il est ensuite passé par MythTV puis XBMC/Kodi. Après avoir vécu en Inde, où les abonnements streaming sont très bon marché, il a refusé de payer les tarifs occidentaux à son retour. Mais le déclencheur principal a été l'agacement face au "tapis roulant de l'engagement" des plateformes (recommandations incessantes, autoplay) qu'il jugeait néfaste pour son fils, et la lourdeur de devoir reconfigurer ces réglages service par service. Le passage à Jellyfin autohébergé a ouvert la porte à l'autohébergement de nombreux autres services, réduisant sa dépendance aux fournisseurs cloud et lui apportant une stabilité qu'il apprécie : plus de refontes de site imposées, de fonctionnalités douteuses, ni de déluge d'e-mails sur les CGU. Il lit lui-même les notes de version des logiciels qu'il héberge et décide quand mettre à jour.

### Règles
Trois règles guident ses choix. Premièrement, à l'exception des serveurs VPN tournant sur son routeur, aucun service n'est exposé directement sur Internet public — peu importe la commodité ou la réputation de sécurité de l'application, d'autant plus avec le piratage assisté par IA. Son FAI utilise par ailleurs du CGNAT pour l'IPv4, ce qui rend son réseau domestique inaccessible directement en IPv4 ; ses serveurs VPN ne sont routables publiquement qu'en IPv6, ce qui limite les tentatives de connexion indésirables mais empêche le VPN de fonctionner sur la plupart des Wi-Fi publics (il bascule alors sur la data mobile). Deuxièmement, il préfère les services natifs quand c'est possible, réservant les conteneurs aux applications complexes ou à dépendances nombreuses : un service livré comme un simple binaire Go est apprécié, alors qu'un service exigeant MySQL, Redis et trois autres conteneurs via Docker Compose le pousse à chercher une alternative. Le natif évite la charge mentale de gérer des commandes différentes selon les conteneurs (l'un sans curl, l'autre en busybox) et le mapping réseau/port virtuel. Troisièmement, il n'utilise plus Docker — pas par principe strict, mais par lassitude de maintenir un système de gestion de services parallèle à systemd ; l'intégration de Podman avec systemd est désormais excellente.

### Matériel
L'an dernier, il a acheté un mini-PC Beelink S12 Pro (Intel N100, 16 Go RAM, SSD 512 Go), payé 180 € avant la "rampocalypse" (la même annonce coûte aujourd'hui 359 € sur Amazon). Un disque dur de 6 To y est relié pour le stockage média. Il souligne qu'il n'exécute aucune inférence IA locale sur cette machine, mais que pour tout le reste, le matériel modeste suffit largement, parfois avec de légers ajustements de configuration.

### Services (par ordre alphabétique)
- **Actual Budget** (Podman) — logiciel de budget avec clients desktop et web, rapports personnalisés, catégorisation par règles. Utilisé uniquement pour le suivi des comptes courants/épargne/carte, pas pour les comptes d'investissement (encore gérés via un service cloud). Les transactions bancaires sont importées manuellement chaque mois (format OFX de préférence) plutôt que via l'import automatique.
- **Audiobookshelf** (natif) — gestion et écoute de livres audio et podcasts, avec une bonne gestion des chapitres ; mis en place surtout pour ses enfants.
- **Automatic Ripping Machine (ARM)** (Podman) — automatise le ripping et le transcodage de DVD, utile pour obtenir du contenu bilingue (anglais/français).
- **Backrest** (natif) — interface web pour l'outil de sauvegarde Restic, essentiel notamment pour les photos (Immich) ; Restic déduplique et compresse bien les données, Backrest facilite la gestion des politiques de rétention, avec notifications d'échec envoyées via Gotify.
- **Beszel** (natif) — tableau de bord de supervision simple collectant les statistiques (CPU, mémoire, disque, température, batterie) de divers hôtes de la maison (Raspberry Pis, cluster Proxmox).
- **Caddy** (natif) — serveur web et reverse proxy ; a permis, via un nom de domaine et des certificats LetsEncrypt automatiques, de rendre presque tous les services accessibles en HTTPS avec des sous-domaines conviviaux sur le LAN ou via VPN.
- **Cockpit** (natif) — console d'administration web du serveur, utile surtout pour repérer les services en échec non notifiés ailleurs.
- **Forgejo** (natif) — fork de Gitea déployé en binaire unique, remote Git personnel plus rapide, avec l'idée future d'y ajouter CI/CD pour déployer le blog.
- **FreshRSS** (natif) — lecteur RSS web, peu utilisé au quotidien si ce n'est pour suivre les releases GitHub des logiciels autohébergés.
- **Frigate** (Podman) — enregistreur vidéo réseau (NVR) ayant remplacé Zoneminder, utilisé avec 8 caméras IP ; détecte personnes et véhicules, s'intègre à Home Assistant pour des automatisations (allumer un projecteur à la détection d'une personne). Les caméras tournent à résolution réduite (sous-flux RTSP basse résolution pour la détection) afin d'éviter la congestion Wi-Fi et l'excès de CPU/disque, tout en restant suffisantes pour identifier des visages ; la loi locale interdit de filmer la voie publique, donc les caméras ne visent pas au loin.
- **Gonic** (natif) — serveur compatible Subsonic écrit en Go, utilisé en deux instances distinctes (musique enfants / musique adultes), suite à l'achat ancien d'une licence Subsonic perpétuelle.
- **Gotify** (natif) — service de notification simple en Go, utilisé avec Uptime Kuma pour signaler pannes, ce que regardent les enfants sur Jellyfin, ou la disponibilité d'un nouvel épisode de podcast.
- **Home Assistant** (Podman) — jugé "fantastique", offrant un contrôle et une flexibilité inégalés par rapport aux écosystèmes propriétaires (Google Home, Alexa, Apple Home), malgré une courbe d'apprentissage raide et la nécessité de prévoir une résilience en cas de panne serveur.
- **Homepage** (Podman) — tableau de bord centralisant les liens et widgets de tous les services, devenu nécessaire tant le nombre de services avait augmenté.
- **Immich** (Podman) — alternative à Google Photos adoptée après lassitude des incitations au stockage payant de Google ; plus rapide en local, avec un système de partage d'albums familial mis en place, même s'il reste du travail (doublons, tri moins rigoureux depuis que le stockage n'est plus une contrainte).
- **Jellyfin** (Podman) — serveur média central du foyer, utilisé pour films, séries et vidéos familiales ; apprécié pour l'absence d'autoplay et de recommandations. Préférence pour le 720p (voire 480-576p pour les DVD rippés) plutôt que le 1080p/4K pour limiter la charge, jugé suffisant malgré un téléviseur 4K.
- **Music Player Daemon (MPD)** (natif) — outil stable depuis 23 ans, utilisé en deux instances (musique, podcasts) pour diffuser l'audio dans toute la maison via Snapcast, en complément de Gonic pour l'écoute mobile.
- **PocketBase** (natif) — remplace un ancien fichier SQLite géré via SQL Workbench/J pour suivre transactions et justificatifs de comptes spéciaux (HSA, 529…) ; apporte une interface web type CRUD utilisable par son épouse, tout en permettant encore des requêtes SQL directes.
- **Readeck** (natif) — outil de tag et d'archivage de lectures, choisi après l'échec de Wallabag à archiver du contenu payant même connecté ; Readeck capture fidèlement ce que voit le téléphone.
- **Samba** (natif) — partage de fichiers réseau avec son épouse ; il note l'ironie qu'un protocole des années 1980 associé à Windows reste la meilleure option de partage multiplateforme sur LAN.
- **slskd** (natif) — mentionné sans description.
- **Snapcast** (natif) — audio synchronisé dans toute la maison, comparé à Sonos sans le verrouillage propriétaire ni l'obsolescence programmée ; complexe à configurer mais efficace, avec l'intention d'acheter d'autres récepteurs dédiés.
- **Syncthing** (natif) — synchronisation one-way (réception seule) vers un Macbook, servant de sauvegarde secondaire des photos Immich.
- **Transmission Daemon** (natif) — client torrent, usage jugé évident.
- **Uptime Kuma** (Podman) — mis en place après que son épouse a signalé plusieurs pannes nécessitant un redémarrage manuel ; surveille pings, conteneurs Podman, codes HTTP et peut parser des réponses JSON, avec notification Gotify après plusieurs tentatives.
- **Vaultwarden** (Podman) — réimplémentation open source compatible Bitwarden, adoptée après les limites de KeePass (pas de synchronisation pratique) et les incidents de sécurité de LastPass utilisé par son épouse ; fonctionne avec les clients officiels Bitwarden, avec synchronisation automatique sur le LAN et manuelle via VPN à distance. L'auteur craint qu'à terme Bitwarden ne devienne hostile à la compatibilité avec Vaultwarden ; la seule alternative notable, Keyguard, n'est pas open source et suit un modèle freemium.
- **Vikunja** (Podman) — alternative autohébergée à Trello adoptée après une panne de plusieurs jours de Trello ; utilise SQLite par défaut (il a écarté toute solution nécessitant PostgreSQL/MySQL pour seulement deux utilisateurs), déployable en binaire unique, malgré une application Android incomplète.
- **Yubal** (Podman) — application web pour télécharger des playlists YouTube Music, en complément de yt-dlp et NewPipe, avec un bon nommage/tag automatique des fichiers.

### Ce qu'il n'autohéberge pas
- **La suite *arr** (Sonarr, Lidarr, Radarr…) — jugée gourmande en ressources et structurellement sujette aux pannes fréquentes, à l'opposé de ce qu'il recherche.
- **Collabora Online** — bien qu'il apprécierait se détacher de Google, Google Docs reste très pratique pour le partage ; il préfère LibreOffice Writer/Calc en local sauf besoin spécifique de cloud, jugeant inutile de faire tourner une suite bureautique web alors qu'un partage réseau existe déjà.
- **Firefly III** — testé avant Actual Budget pour la gestion multi-devises, mais configuration complexe (plusieurs conteneurs, dont un dédié à l'import de données) ; Actual Budget s'est révélé bien plus simple, avec un script personnel pour gérer les conversions de devises.
- **OwnTracks** — alternative autohébergée à Google Maps Timeline envisagée après que Google a limité les données de localisation à l'appareil individuel, mais l'application Android ne reportait jamais sa position de façon fiable ; Dawarich, une alternative, exige au moins quatre conteneurs (PostgreSQL, Redis, Sidekiq, application web), ce qui ne justifie pas le coût en ressources.
- **Music Assistant** — jugé peu adapté puisqu'il disposait déjà d'une configuration fonctionnelle (Gonic, Snapcast, MPD) ; l'outil semblait vouloir "tout posséder", par exemple en réorganisant continuellement ses groupes d'appareils Snapcast.
- **L'e-mail** — autohéberger sa messagerie est jugé trop risqué pour un bénéfice limité, ne pouvant se permettre de ne pas pouvoir envoyer/recevoir de mails ; il envisage à terme de passer de Gmail à un fournisseur payant plutôt que de s'autohéberger.

### Conclusion
Au total, l'auteur fait tourner 17 services natifs et 11 services Podman, tous gérés par systemd. `htop` indique environ 7,5 Go de RAM utilisés et une charge CPU fluctuant entre 30 et 40 %. Il conclut que ce mini-PC peut faire tourner énormément de choses, et qu'au vu de la flambée des prix du matériel informatique liée à la demande en IA, il espère voir perdurer des projets autohébergeables privilégiant simplicité et efficacité.

## Pourquoi ça compte
Ce témoignage illustre une tendance de fond en veille tech : la recherche de souveraineté numérique et de sobriété logicielle (binaires natifs, SQLite, systemd/Podman plutôt que des piles Docker lourdes) comme réponse concrète à la fois à l'érosion de confiance envers les plateformes cloud et à la hausse du coût du matériel liée à la demande en IA.
