---
title: "Nightmare mode: simulating disk failures | Antithesis"
date: 2026-11-26
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fantithesis.com%2Fblog%2F2026%2Fnightmare-mode%2F%3Futm_source=tldrnewsletter/1/010001a212797b17-8a9c39a2-35de-4646-9734-dec19be00572-000000/UhxmDiAVSSxSvs7inbxqTBOasApWMciJen7MWDerTi8=452"
keywords: ["simulation de pannes", "fiabilité du stockage", "systèmes distribués", "fsync", "FUSE", "test logiciel"]
theme: "Software"
tone: "research"
used_in: ["2026-11-26"]
---

## Résumé
Antithesis, qui propose une plateforme de simulation déterministe pour tester des systèmes complexes, détaille dans cet article comment elle a construit un injecteur de pannes disque en « nightmare mode » pour aider ses clients à vérifier la robustesse de leurs systèmes de stockage. L'équipe est passée par deux implémentations successives (LazyFS puis son propre système maison, Amnesia, écrit en Rust au-dessus de FUSE) pour émuler de façon crédible pertes d'alimentation, écritures tronquées, erreurs d'I/O disque et latences aléatoires. L'article explique en détail le mécanisme du tristement célèbre bug « fsyncgate » qui a touché PostgreSQL, et présente un bug réel découvert dans bbolt (le moteur de stockage d'etcd) grâce à cette technique. Le message central : le stockage persistant est bien plus fragile et imprévisible qu'on ne le pense, et seule une simulation fidèle des pannes permet de révéler les bugs de durabilité avant qu'ils ne surviennent en production.

## Points clés
- Un simple SIGKILL ne suffit pas à tester la résilience au crash : le cache page du noyau continue d'écrire les données sur disque après la mort du processus, contrairement à une vraie coupure de courant.
- Antithesis a d'abord utilisé LazyFS (basé sur FUSE) pour émuler fidèlement les pertes d'alimentation, avant de développer sa propre solution, Amnesia, en Rust, plus rapide et travaillant directement au niveau des inodes plutôt que des chemins de fichiers.
- Le bug « fsyncgate » montre qu'un fsync qui échoue avec une erreur EIO peut faire croire au noyau que les données sont « propres », alors qu'elles n'ont jamais atteint le disque — elles sont alors silencieusement perdues.
- L'injecteur simule aussi des latences disque (achèvement d'opérations dans le désordre, écritures/lectures partiellement appliquées) pour révéler des bugs de concurrence liés aux accès disque.
- Le dispositif cible précisément les instants « intéressants » (juste avant/pendant/après une opération disque) pour que le fuzzer explore efficacement l'espace des défaillances possibles, plutôt que de couper l'alimentation à des moments arbitraires.
- Cette approche a permis de découvrir un bug réel et reproductible dans bbolt (moteur de stockage d'etcd), où une combinaison précise d'erreur d'I/O puis de perte d'alimentation corrompt irrémédiablement la base.

## Analyse approfondie
Construire un système distribué correct est très difficile. Construire un système distribué correct qui doit stocker des données sans jamais les perdre est encore plus difficile.

Beaucoup de clients d'Antithesis construisent des systèmes où le stockage fiable des données est primordial. Le stockage est déjà compliqué même quand tout se passe bien : certains clients surveillent le remplissage de leurs disques et compactent les données quand nécessaire, ou les répartissent entre plusieurs machines avant qu'un disque n'atteigne sa limite. D'autres maintiennent un journal d'écriture (write-ahead log) pour pouvoir récupérer après un redémarrage de processus. D'autres encore s'appuient sur une séquence précise d'opérations pour garantir durabilité et atomicité — par exemple écrire une nouvelle copie d'un fichier puis la renommer à la place de l'ancienne, afin qu'un changement soit appliqué entièrement ou pas du tout.

Malheureusement, les périphériques de stockage sont peu fiables, ce qui ajoute encore de la complexité à chaque interaction avec le disque. Prenons une simple écriture : si elle échoue avec une erreur, le système doit décider s'il est sûr de réessayer ou s'il doit abandonner. Si elle échoue parce que le disque est plein, le système doit peut-être déclencher une compaction avant de continuer. Même la création d'un fichier peut échouer parce que le système de fichiers a épuisé ses inodes, obligeant alors le système à supprimer d'autres fichiers pour faire de la place.

Par ailleurs, cette non-fiabilité peut aussi prendre la forme de latence. Un disque peut être lent, par exemple à cause d'une contention d'E/S ou d'un périphérique défaillant, ce qui peut étirer les opérations de sorte qu'elles se chevauchent de manières inhabituelles. Si une lecture et une écriture ont lieu en même temps, le lecteur peut voir les anciennes données, les nouvelles, ou un entrelacement aléatoire des deux.

La complexité s'accroît encore dès qu'on suppose que le disque ne sera pas toujours disponible. Si une écriture réussit et que la machine perd l'alimentation immédiatement après, une lecture après redémarrage pourrait voir toutes les données, une partie aléatoire, ou rien du tout.

Au sein de l'équipe Forward Deployed Engineering d'Antithesis, des discussions récurrentes avec les clients qui construisent ce type de logiciel critique ont fait émerger le besoin d'injecter des pannes disque ou des erreurs de stockage pendant les simulations Antithesis, afin de reproduire ces situations et de s'assurer que leur logiciel peut y faire face. L'une des premières choses constatées est que les clients avaient des attentes très différentes sur leur stockage et sur les garanties qu'il devait offrir — certains tournant sur ext4, d'autres sur XFS ou ZFS, chacun ayant son propre comportement en cas de défaillance.

Cette diversité d'exigences a rendu difficile la construction d'une solution universelle d'emblée. L'équipe a donc d'abord travaillé avec des clients individuels pour construire plusieurs solutions adaptées à leurs cas d'usage spécifiques. Par exemple, pour tester la logique de récupération d'espace, elle simulait le remplissage complet du système de fichiers.

Une fois une vue d'ensemble des besoins des différents clients obtenue, l'équipe a travaillé à intégrer ces pièces du puzzle dans un mécanisme complet d'injection de pannes au niveau du système de fichiers. Cet article propose un tour d'horizon des pannes disque qu'un injecteur de pannes en « nightmare mode » doit pouvoir émuler : la panne la plus demandée, la perte d'alimentation, puis les choses plus subtiles qu'un disque peut faire — écritures tronquées, erreurs d'I/O (dont celle derrière le bug fsyncgate), et les pannes de latence qui révèlent des bugs de concurrence.

**Le chemin heureux : comment fonctionne l'écriture de fichiers**

Quand un programme écrit dans un fichier, les données ne vont pas directement sur le disque. Elles vont d'abord dans le cache page du noyau. Le noyau les écrit ensuite sur disque selon son propre calendrier, via un processus appelé writeback. Si un programme a besoin que les données soient sur disque immédiatement, il peut appeler fsync, qui demande au noyau d'écrire les données de ce fichier sur disque et ne retourne qu'une fois l'écriture terminée. Les données écrites mais non synchronisées (fsync) pourraient être détruites par une perte d'alimentation.

**La perte d'alimentation**

Antithesis dispose déjà d'un type de panne apparenté, les « node kills », qui envoient aléatoirement un SIGKILL à un conteneur. Le SIGKILL détruit le processus mais n'a aucun effet sur la machine, qui continue de fonctionner normalement : le noyau et son cache page poursuivent leur travail comme si rien ne s'était passé. Chaque écriture que le processus a effectuée finit par atteindre le disque, fsync ou pas, grâce au mécanisme de writeback du noyau. Du point de vue du processus, un SIGKILL est une mort plutôt « polie », puisqu'on ne perd que les données que le processus n'a jamais transmises au noyau.

Une perte d'alimentation est beaucoup moins polie. Elle fait perdre tout ce que le noyau a accepté mais n'a pas encore synchronisé : les données écrites mais non encore fsync sont simplement perdues.

Malheureusement, lorsqu'on simule des pannes dans Antithesis, il n'est pas possible de simplement débrancher la machine. La solution a donc consisté à la simuler. Cela impliquait de gérer les deux éléments qui empêchent un simple kill de conteneur de provoquer une perte de données ou de cache : le cache page du noyau, qui conserve les données non synchronisées, et le writeback du noyau, qui enregistre les données non synchronisées sur disque.

Le problème est que ces deux éléments vivent à l'intérieur du noyau, hors de portée. Il n'existe actuellement aucun moyen de demander au noyau d'oublier le contenu de son cache, ni d'arrêter son writeback automatique. Une solution de contournement a toutefois été trouvée : LazyFS, un système de fichiers open source de l'INESC TEC et de Jepsen.

LazyFS utilise FUSE, une fonctionnalité Linux qui permet à un programme en espace utilisateur d'agir comme un système de fichiers. Comme chaque lecture et écriture passe par LazyFS, celui-ci peut conserver les données écrites dans son propre cache interne, émulant le cache page du noyau en espace utilisateur. Les écritures vers LazyFS restent dans ce cache interne jusqu'à ce que le programme appelle fsync, et ce n'est qu'à ce moment-là que LazyFS les écrit sur le stockage persistant — sans aucun writeback en arrière-plan entre-temps. Cela permet d'« oublier » les données non synchronisées à n'importe quel moment opportun, simplement en vidant le cache. En faisant cela exactement au moment où l'application est tuée, les deux effets combinés sont indiscernables d'une véritable perte d'alimentation.

Avant de se fixer sur FUSE, d'autres mécanismes d'injection de pannes ont été envisagés. eBPF était tentant, car il permet d'implémenter facilement certaines pannes, comme renvoyer un code d'erreur particulier depuis un appel système. Cependant, il aurait été difficile d'émuler une perte d'alimentation, car eBPF ne permet que d'observer et de modifier les appels au moment où ils passent — il ne peut pas conserver des données pour les libérer (ou les perdre) plus tard, ce qui est pourtant exactement l'astuce nécessaire. L'idée d'un périphérique bloc personnalisé a aussi été envisagée, mais avec le problème inverse : il peut conserver des données, mais se situe au mauvais niveau d'abstraction. Étant en dessous du système de fichiers, il voit des blocs plutôt que des appels système, ce qui rend difficile l'implémentation de pannes au niveau syscall. La perte d'alimentation est particulièrement délicate à ce niveau car il est impossible de distinguer les données arrivées via un fsync de celles que le writeback du noyau a simplement poussées — ce qui ferait perdre la rigueur permettant de détecter les fsync manquants.

LazyFS s'est donc révélé très utile, et l'équipe tient à remercier ses auteurs pour la qualité de cet outil. Une version modifiée (enrichie de types de pannes supplémentaires) a été exécutée pendant un certain temps sur plusieurs environnements clients, révélant quelques bugs subtils de perte de données.

**Amnesia : le système de fichiers maison**

Par la suite, l'équipe a décidé de développer son propre système de fichiers FUSE : Amnesia. L'objectif était de passer à Rust pour sa sécurité mémoire, et de repenser la conception pour un modèle plus simple et plus rapide, car beaucoup d'autres fonctionnalités devaient être construites par-dessus.

Par exemple, Amnesia travaille directement sur les inodes, alors que LazyFS utilise le chemin du fichier pour chaque opération et doit le retraduire en inode. Comme un chemin n'est qu'un nom pour un fichier, cela rend des opérations comme les renommages, les liens physiques (hard links), ou la suppression d'un fichier encore ouvert, difficiles à suivre. Travailler directement avec les inodes fait disparaître cette complexité. Amnesia ne touche également jamais à un vrai disque : LazyFS écrit les données synchronisées sur le système de fichiers sous-jacent, alors qu'Amnesia conserve à la fois l'état volatile et l'état « durable » en mémoire, ce qui permet de modéliser un fsync comme une simple mise à jour comptable plutôt qu'une nouvelle opération d'E/S réelle. Cela rend le système beaucoup plus rapide, et tout aussi sûr, puisque la machine ne perd jamais réellement l'alimentation. Plusieurs autres changements ont également été apportés.

Au-delà de la conception, LazyFS a fait découvrir les effets plus subtils d'une véritable perte d'alimentation : les écritures tronquées et les séquences d'écritures tronquées, causées par le fait que le noyau et le disque ne persistent pas les données dans l'ordre ou par les unités qu'un programme pourrait attendre.

LazyFS a aussi révélé les subtilités de travailler au niveau de la couche FUSE. Par exemple, le cache page du noyau se situe toujours en amont du système de fichiers FUSE, et peut conserver des copies des données qu'on vient de « perdre » en simulant une panne d'alimentation. Heureusement, LazyFS avait déjà identifié les bons réglages et schémas FUSE pour garantir que le programme ne les voie jamais.

**Les erreurs d'I/O disque**

Le fait de s'appuyer sur FUSE a permis d'ajouter facilement les erreurs d'I/O disque, un autre type de panne demandé par les clients. L'approche évidente consiste à simplement renvoyer l'erreur, et ce seul modèle a déjà permis de trouver des bugs. Mais comme le cache page du noyau est émulé, il est parfois possible d'appliquer les effets secondaires possibles de ces erreurs à ce cache, ce qui donne un niveau de fidélité supérieur.

Par défaut, LazyFS ne simule pas les erreurs d'I/O disque comme type d'injection de panne — ce terrain était donc nouveau. La capacité de renvoyer plusieurs types d'erreurs d'I/O disque sur les appels système a été ajoutée. L'une des plus intéressantes est EIO (« Error: Input/Output », l'erreur générique « le disque a échoué ») sur fsync.

Cette erreur peut interagir avec le cache page du noyau de manière surprenante. C'est exactement ce qui se cache derrière le célèbre bug « fsyncgate ». Sa découverte a conduit PostgreSQL à corriger la façon dont il gère un fsync en échec (il plante désormais et récupère depuis son journal plutôt que de réessayer), et a changé durablement la manière dont la promesse de fsync est comprise. Comme l'a résumé Craig Ringer, le développeur PostgreSQL à l'origine du signalement du problème :

> Quand fsync() renvoie un succès, cela signifie « toutes les écritures depuis le dernier fsync ont atteint le disque », mais nous supposons que cela signifie « toutes les écritures depuis le dernier fsync RÉUSSI ont atteint le disque ».

Pour comprendre pourquoi Craig a raison, il faut un peu de contexte sur ce qui se passe pendant un fsync sur un système de fichiers Linux classique comme ext4. Le cache page du noyau conserve les données de fichier en blocs de taille fixe appelés pages, et marque une page comme « sale » (dirty) lorsqu'elle a été modifiée mais pas encore écrite sur disque. Quand un programme appelle fsync, le noyau envoie chacune des pages sales du fichier vers le périphérique de stockage via un pilote. Fait crucial : le noyau efface le drapeau « sale » d'une page avant de la transmettre. Le fsync attend ensuite que le pilote indique si chaque écriture a réussi.

Supposons maintenant que l'une de ces écritures vers le périphérique échoue. Le fsync renverra alors EIO, mais rien ne vient remarquer la page comme sale à nouveau. Du point de vue du noyau, cette page est désormais propre, donc ni le prochain fsync ni le writeback en arrière-plan ne tenteront plus jamais de la soumettre au périphérique. Comme il n'y a plus de pages sales associées au fichier, le fsync suivant réussit. À moins que le programme n'écrive à nouveau les mêmes données et ne salisse de nouveau les pages, ces données n'atteignent jamais le disque.

Ce scénario peut être émulé au niveau de la couche FUSE. Quand la panne se déclenche, fsync renvoie EIO et les pages concernées sont marquées propres dans le cache interne, sans être écrites sur le stockage persistant. Un fsync réessayé réussit alors, mais les données seront perdues à la prochaine panne d'alimentation émulée, à moins que le programme ne les réécrive et n'appelle fsync à nouveau.

**La latence disque**

S'appuyer sur FUSE a aussi permis d'ajouter la « latence disque », un autre type de panne fréquemment demandé.

La latence disque vise avant tout à révéler des bugs de concurrence. Communiquer avec le disque peut être lent et imprévisible, et les programmes qui supposent le contraire peuvent avoir des races. Ces races peuvent survenir pour plusieurs raisons : par exemple, les données peuvent atteindre le disque dans un ordre imprévisible, ou arriver dans le cache page du noyau par morceaux plutôt que d'un seul bloc. L'objectif était donc de rendre ces races plus faciles à détecter.

Deux types de panne de latence sont actuellement pris en charge :

1. **Achever les opérations dans le désordre.** Plutôt que de répondre aux appels système dans l'ordre d'arrivée, c'est le fuzzer qui décide de l'ordre dans lequel ils s'achèvent. Comme Amnesia se situe sous le programme et voit chaque opération comme une requête, il peut choisir de répondre immédiatement ou de conserver la requête en attente. Par exemple, lorsque les données d'une opération d'écriture arrivent, elles sont parfois conservées avec une échéance pendant que d'autres opérations continuent d'être traitées (l'échéance servant de garde-fou : une fois celle-ci dépassée, l'opération se termine quoi qu'il arrive). Le fuzzer décide ensuite du moment où l'opération en attente doit être exécutée.

2. **Opérations partiellement achevées.** Les appels système ne sont pas atomiques, et une lecture en concurrence avec une écriture peut voir l'écriture partiellement appliquée. Supposons qu'un programme réécrive quelques kilo-octets d'un fichier pendant qu'un autre thread lit la même plage. Sur ext4, le lecteur peut voir l'ancien contenu, le nouveau, ou un patchwork des deux. Le fuzzer choisit lequel de ces résultats le lecteur obtient. Ceci a été implémenté dans Amnesia en retenant une écriture et en la découpant en petits morceaux. Plutôt que de les appliquer tous, le fuzzer décide quels morceaux sont appliqués immédiatement et lesquels sont retenus. Combiné à l'achèvement dans le désordre décrit ci-dessus, cela signifie qu'une lecture arrivant pendant qu'une écriture est en attente sera probablement répondue à partir de l'état partiellement appliqué, et verra donc le même mélange d'anciennes et de nouvelles données qu'une véritable race pourrait produire.

De même, des lectures peuvent être retenues et découpées en plusieurs morceaux capturés à des moments différents. Par exemple, une seule lecture peut renvoyer le début du fichier d'avant une écriture et la fin d'après celle-ci. Avec plusieurs opérations en attente sur le même fichier, le fuzzer choisit l'ordre dans lequel elles s'achèvent. Chaque combinaison testée correspond à un entrelacement légal que le cache page du noyau ou le disque aurait pu produire.

**Pannes corrélées et efficacité du fuzzing**

Le système de fichiers FUSE a été conçu pour fonctionner main dans la main avec l'injecteur de pannes et le fuzzer d'Antithesis. Cela permet d'injecter pertes d'alimentation, écritures tronquées et erreurs d'I/O disque aux moments que le fuzzer juge « intéressants ». Cela signifie aussi que les pannes disque sont contrôlées de la même manière que les autres pannes, ce qui apporte les bénéfices du swarm testing.

À la différence des « node kills » classiques, qui peuvent être intéressants à n'importe quel moment, pour les pertes d'alimentation il suffit d'échantillonner un seul instant parmi trois catégories de moments où une perte d'alimentation peut survenir : avant l'appel système, pendant, ou après. Pour une opération disque donnée, au sein des fenêtres « avant » ou « après », le moment exact n'a pas d'importance : une panne d'alimentation émulée n'importe où dans cette fenêtre produit le même résultat. Les états intéressants révélés « pendant » une opération sont relativement courts, donc ces moments sont rares, en particulier dans les systèmes qui touchent peu souvent le disque. En liant la panne à l'opération disque elle-même, le fuzzer consacre moins d'énergie à trouver ces états vulnérables et davantage à les explorer une fois trouvés.

L'injecteur de pannes disque aide ainsi le fuzzer en réduisant l'espace d'états non pertinents qu'il doit explorer. Plutôt que de laisser le fuzzer couper l'alimentation à des instants arbitraires, c'est à chaque appel système que la décision est prise, et la panne est injectée depuis l'intérieur même du système de fichiers FUSE.

À chaque fois que le programme est au milieu d'une opération disque, il existe trois points précis où l'injecteur peut déclencher une perte d'alimentation : avant qu'une quelconque partie de l'opération n'ait été appliquée au cache interne, après qu'une partie l'a été, et après que la totalité l'a été (mais avant que l'appel système ne retourne). Ces trois points correspondent aux trois catégories mentionnées plus haut : rien appliqué, partiellement appliqué, ou totalement appliqué. Quand une panne d'alimentation se déclenche, le système de fichiers FUSE tue le conteneur, supprime le cache interne, et s'assure que les appels système actifs sont traités correctement. Ces pannes sont appelées *pannes corrélées*, car le moment de chaque perte d'alimentation est lié à une opération disque spécifique.

**Étude de cas : le bug bbolt / etcd**

Le travail d'injection de pannes disque a déjà porté ses fruits en révélant plusieurs bugs dans des logiciels clients. Un bug open source qui peut être partagé se trouve dans bbolt, le moteur de stockage derrière etcd. Toutes les pannes disque décrites dans cet article ont été injectées pendant les tests du système, mais celles pertinentes pour ce bug précis sont la perte d'alimentation et l'injection d'erreurs.

Le problème vient du fait que bbolt valide une transaction en deux étapes, chacune suivie d'un fsync. Il écrit d'abord les nouvelles pages de données, puis écrit une unique page de métadonnées (meta page) qui pointe vers elles.

Un cas a été trouvé où les pages de données sont écrites avec succès, mais le fsync de la page de métadonnées échoue avec un EIO. Cela provoque l'arrêt d'etcd, ce qui est normal en soi.

Au redémarrage, bbolt relit la page de métadonnées via le cache page du noyau, où la page de métadonnées non persistée existe toujours, et considère à tort cette transaction comme validée. Il reconstruit sa liste de pages libres à partir de cette page de métadonnées, si bien que les commits suivants peuvent réutiliser des pages vers lesquelles la page de métadonnées réellement sur disque pointe encore.

Une fois la page de métadonnées en cache évincée — via l'émulation de pression mémoire ou de perte d'alimentation —, ce qui reste sur disque est une ancienne page de métadonnées pointant vers des pages désormais écrasées. À partir de là, bbolt plante à chaque ouverture. Le journal d'écriture (write-ahead log) du nœud etcd ne peut pas aider à reconstruire la base, car le nœud ne parvient jamais à l'ouvrir.

Ce bug ne pouvait être découvert que par la combinaison d'une erreur d'I/O suivie d'une perte d'alimentation — exactement le genre de problème que l'injection de pannes disque est conçue pour trouver.

**Conclusion**

L'article couvre beaucoup de terrain : pertes d'alimentation, écritures et séquences d'écritures tronquées, erreurs d'I/O disque (y compris celle derrière fsyncgate), et les pannes de latence qui révèlent des bugs de concurrence. Toutes ces pannes sont disponibles aujourd'hui dans l'injecteur de pannes disque d'Antithesis, et la liste continue de s'allonger à mesure que les clients font part de ce qui les préoccupe.

L'injecteur de pannes disque est personnalisable : il n'est pas nécessaire de tout activer d'un coup. On peut commencer par les pannes les plus préoccupantes — la perte d'alimentation pour un moteur de stockage, par exemple, ou les erreurs d'I/O — et en ajouter progressivement d'autres.

Pour les clients existants, il est possible de demander à son ingénieur Forward Deployed de déployer les pannes disque dans son environnement. Pour les autres, intéressés de voir comment leur système se comporte en « nightmare mode », il suffit de prendre contact.

Et si un type de défaillance disque a déjà causé des problèmes mais n'est pas couvert ici, l'équipe serait ravie d'en entendre parler — les meilleures pannes de cet article sont justement nées de ce genre de conversations.

## Pourquoi ça compte
Cet article illustre de façon très concrète une pratique encore peu répandue mais cruciale pour les systèmes distribués critiques : la simulation déterministe et précisément ciblée des pannes de stockage, bien au-delà d'un simple "chaos engineering" aléatoire. Pour une veille tech, il montre aussi comment des bugs de durabilité réels (ex. bbolt/etcd) peuvent rester invisibles en production pendant longtemps, renforçant l'intérêt pour les outils de test par fuzzing/simulation dans l'infrastructure logicielle.
