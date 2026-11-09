---
title: "Message Queues"
date: 2026-11-09
url: "https://programmingdigest.net/links/23662/8e384055-4ef6-4411-8656-1644e3ae163f/email"
keywords: ["file de messages", "architecture résiliente", "Kafka", "SQS", "RabbitMQ", "découplage", "tolérance aux pannes"]
theme: "Software"
tone: "tutorial"
used_in: ["2026-11-09"]
---

## Résumé
Cet article explique, sous l'angle du system design, pourquoi les files de messages (message queues) existent, comment elles fonctionnent sous le capot, et quand les utiliser ou les éviter. Il détaille les mécanismes clés — accusés de réception, prévention des doublons, garanties de livraison, partitionnement, back pressure, dead letter queue et durabilité — en s'appuyant sur trois produits phares : Amazon SQS, Apache Kafka et RabbitMQ. La thèse centrale est que les files de messages découplent producteurs et consommateurs, absorbent les pics de trafic et isolent les pannes, mais qu'elles introduisent de la latence et retardent la détection des erreurs plutôt que de les éliminer.

## Points clés
- Une file de messages découple les producteurs des consommateurs, leur permettant de scaler indépendamment.
- Trois garanties de livraison existent : *at-least-once* (doublons possibles), *at-most-once* (perte possible) et *exactly-once* (très difficile à implémenter, nécessite idempotence + déduplication).
- Le partitionnement permet le scaling horizontal, mais le choix de la clé de partition implique un compromis entre ordre garanti et distribution équilibrée de la charge.
- Les messages "empoisonnés" doivent être évacués vers une Dead Letter Queue (DLQ) après un nombre maximal de tentatives, avec alerting associé.
- Des outils modernes comme Kafka assurent la durabilité via la persistance sur disque et la réplication entre brokers, avec possibilité de rejouer les messages passés.
- Une file ne supprime pas la panne, elle la retarde et la rend plus silencieuse — mieux vaut surveiller l'âge du message le plus ancien que la seule profondeur de la file.

## Analyse approfondie
Les files de messages sont un outil important dans la boîte à outils de l'architecture résiliente. Cet article adopte une approche de conception système pour répondre à :

- Pourquoi les files existent-elles et quels problèmes résolvent-elles ?
- Comment fonctionnent-elles sous le capot, et quelles en sont les nuances et limites ?
- Quand doit-on les utiliser, et quand ne sont-elles pas le bon choix ?

Nous aborderons aussi le back pressure, la dead letter queue (DLQ), l'ordonnancement, l'idempotence, le comportement à l'échelle, la durabilité, la gestion des erreurs, etc., en utilisant **Amazon SQS**, **Apache Kafka** et **RabbitMQ**.

### Un exemple

Imaginons que vous construisiez une application de partage de photos comme Instagram. Quand un utilisateur télécharge une photo, il faut effectuer plusieurs opérations :

- **Redimensionner** l'image aux tailles standard utilisées dans l'UI.
- Évaluer le contenu selon une politique de **modération** pour garantir la conformité.
- Diffuser des **notifications** et mettre à jour les fils d'activité.
- …

L'implémentation la plus simple exécute ces opérations séquentiellement sur le même serveur.

Cela présente plusieurs inconvénients :

1. **Latence :** l'utilisateur doit attendre que toutes les opérations se terminent. Techniquement, on peut exécuter le *redimensionnement* et la *modération* en parallèle, mais à l'échelle, le serveur sera saturé et fera attendre l'utilisateur.
2. **Inefficacité :** la charge de *modération* peut nécessiter un GPU puissant, tandis que le *redimensionnement* peut nécessiter plus de RAM. Faire cohabiter ces besoins hétérogènes sur le même serveur augmente son coût inutilement.
3. **Fragilité :** si une étape échoue (par exemple la **modération**), l'ensemble de l'opération de téléchargement échoue. Une nouvelle tentative gaspillerait des ressources et du temps en refaisant les étapes précédentes qui avaient réussi.
4. **Pics de trafic :** peut-être que votre application est mise en avant sur un app store, ou qu'une publicité ou un événement spécial fait grimper fortement les téléchargements. Si le service a été conçu pour une exigence non fonctionnelle plus basse, un pic nuira forcément à l'expérience utilisateur. Vous pourriez provisionner des ressources supplémentaires en avance, mais tous les pics ne sont pas prévisibles. De plus, les ressources redondantes (par exemple des répliques de serveur) restent inactives et coûtent de l'argent.

Décomposer ces étapes en services spécialisés faiblement couplés résout la plupart de ces problèmes.

C'est là que la file entre en jeu :

1. L'utilisateur télécharge l'image vers un serveur web.
2. Le serveur web la dépose dans la file.
3. Le serveur web répond immédiatement « téléchargement terminé » à l'utilisateur.
4. Les services de **redimensionnement**, de **modération** et de **notification** récupèrent le travail depuis la file en parallèle.

En quoi la file a-t-elle amélioré notre conception ?

- **Les téléchargements sont rapides :** votre serveur ne fait qu'enregistrer le fichier et le déposer sur une file de messages, sans attendre le traitement.
- **Les pannes sont isolées :** si un worker plante pendant le traitement d'une seule photo, ce message est simplement redistribué à un autre worker, qui reprend là où l'autre s'est arrêté.
- **Les pics de trafic sont absorbés :** quand le trafic augmente, la file s'allonge au lieu d'échouer. On peut aussi créer ou supprimer des workers selon la longueur de la file.

### Qu'est-ce qu'une file de messages ?

Une file de messages est un tampon placé entre un **producteur** et un **consommateur**.

- **Producteurs :** créent les messages déposés dans la file. Par exemple, 5 utilisateurs téléchargent chacun 3 photos. Le serveur web produit 15 messages.
- **Consommateurs :** récupèrent ces messages depuis la file. Dans cet exemple, les services de redimensionnement, de modération et de notification consomment ces 15 messages. Il peut y avoir plusieurs instances de ces workers, traitant les messages en parallèle.

Le rôle de la file est de conserver ces messages jusqu'à ce qu'un consommateur soit prêt à les traiter.

**Les files découplent les producteurs des consommateurs.** Le producteur et le consommateur ne se connaissent pas mutuellement. Cela leur permet de scaler indépendamment et de remplacer l'un ou l'autre sans impact direct.

### Comment fonctionnent les files sous le capot ?

Il y a quelques mécanismes à comprendre :

1. Les accusés de réception (acknowledgements)
2. La prévention du traitement en double
3. Les garanties de livraison

#### 1. Accusés de réception (ACK)

Supposons qu'un worker récupère un message de la file et commence à traiter la photo.

Que se passe-t-il s'il plante à mi-chemin du traitement ?

Si la file supprimait le message dès que le worker s'en empare, cette photo serait perdue pour toujours.

L'**accusé de réception** est le mécanisme qui résout ce problème.

Au lieu de supprimer le message, la file attend que le consommateur envoie explicitement un ACK signalant qu'il a terminé le traitement et que le message peut être retiré en toute sécurité.

Si un consommateur plante avant d'envoyer cet ACK, la file suppose qu'il n'a pas été traité, et ce message finit par être redistribué à un autre consommateur pour traitement.

De même, la file peut aussi envoyer un ACK au producteur dès la réception du message. Cela ajoute de la latence mais augmente la fiabilité.

#### 2. Prévenir le traitement en double

La file conserve les messages jusqu'à ce que les consommateurs les acquittent (ACK). Que se passe-t-il si le worker A traite un message tandis que le worker B vérifie s'il y a de nouveaux messages ?

On ne veut pas gaspiller de ressources pour un travail dupliqué, ni pire, se retrouver avec des effets de bord incohérents.

Différents produits résolvent ce problème différemment :

- **AWS SQS :** quand un consommateur récupère un message, celui-ci devient *invisible* pour tous les autres consommateurs pendant une fenêtre configurable (de `0s` à `12h`. Par défaut : `30s`). Si le consommateur acquitte (ACK) dans cette fenêtre, le message est *supprimé* (le consommateur appelle `DeleteMessage`). Sinon, le message redevient *visible*, le rendant disponible pour un autre consommateur.
- **RabbitMQ :** juste après l'envoi d'un message à un consommateur, celui-ci est marqué comme non acquitté (`unack`), ce qui empêche son envoi à un autre consommateur. Si le consommateur n'acquitte pas le message dans une fenêtre de temps (par défaut : `30m`), il redevient disponible pour d'autres consommateurs. Note : si le consommateur se déconnecte, RabbitMQ n'attend pas aussi longtemps et remet le message en file immédiatement.
- **Apache Kafka :** il divise les topics en partitions. Au sein d'un groupe de consommateurs, Kafka impose une correspondance 1:1 où chaque partition est assignée à exactement une instance de worker, donc il n'y a pas de compétition entre consommateurs.

#### 3. Garanties de livraison

Que se passe-t-il si le worker traite le message avec succès mais plante juste avant d'envoyer l'ACK ? La file pense qu'il n'a jamais été traité, donc elle le redistribue à un autre consommateur.

Dans de nombreux cas (comme nos exemples de redimensionnement ou de modération), il n'y a pas d'effet de bord grave à effectuer le travail plusieurs fois. C'est parce que ces opérations sont **idempotentes** : les exécuter plusieurs fois produit exactement le même état final.

Mais que se passe-t-il s'il y a de l'argent en jeu ? Par exemple, si un message facture 130 SEK à l'utilisateur, exécuter cette opération deux fois le facturera 260 SEK ! Les transactions financières sont typiquement **non idempotentes**.

C'est là que les **garanties de livraison** entrent en jeu, et il y a principalement 3 mécanismes à connaître :

1. **At-Least-Once (au moins une fois) :** les messages sont garantis d'arriver, mais un traitement en double peut survenir. C'est le comportement par défaut de SQS, RabbitMQ et Kafka. Cela fonctionne bien quand le travail est **sans effet de bord** ou **idempotent** :
   1. ✅ Mettre à jour le nom d'utilisateur en « Aleksander » est *idempotent* car l'état final est le même.
   2. ❌ Augmenter le compteur de vues de N est *non idempotent* car chaque exécution augmente le compteur de N.
2. **At-Most-Once (au plus une fois) :** les messages ne sont **jamais dupliqués**, mais des données peuvent être **perdues** si un worker plante en cours de traitement, car l'ACK est envoyé *immédiatement* à la réception du message. Si quelque chose va mal, au plus un worker l'a traité ; dans le pire cas, personne ne l'a traité. On peut utiliser cette approche quand perdre quelques points de données est acceptable.
3. **Exactly-Once (exactement une fois) :** le message est garanti d'être traité exactement une fois, mais c'est très difficile à implémenter. C'est le problème des deux généraux (Two Generals' Problem). En pratique, cela s'implémente en combinant une livraison **At-Least-Once** avec un consommateur idempotent (par exemple via des clés de *déduplication* ou des *transactions* en base de données).

### Quand utiliser une file de messages

Il y a quatre signaux à rechercher :

1. **Travail asynchrone :** quand un utilisateur n'a pas besoin d'un résultat immédiat (par exemple, l'envoi d'un e-mail, la génération d'un rapport, le traitement de téléchargements).
2. **Trafic en rafale (bursty) :** le système doit pouvoir absorber les pics de trafic sans rejeter de requêtes. La file agit comme un tampon qui lisse la charge sur les consommateurs.
3. **Découplage :** votre producteur et votre consommateur peuvent avoir des besoins de scaling ou de matériel complètement différents. Dans l'exemple du traitement d'image, le service de téléchargement accepte simplement le fichier et le dépose dans une file, tandis que le worker de redimensionnement a besoin de plus de RAM et le worker de modération a besoin de GPU. Le découplage permet le scaling et l'efficacité en dimensionnant ces workers en conséquence.
4. **Fiabilité :** quand on ne peut pas se permettre de perdre du travail. Si un service en aval est temporairement indisponible, la file conserve ce message jusqu'à ce qu'il revienne en ligne, garantissant que rien n'est perdu.

⚠️ **Note sur les charges sensibles à la latence :** faites attention en introduisant une file dans un flux synchrone avec des exigences de *latence* strictes (par exemple sous `500ms`). Ajouter une file garantit presque que vous allez briser cette contrainte d'exigence non fonctionnelle. Les files sont faites pour du travail que vous pouvez vous permettre de faire plus tard, même si « plus tard » ne représente que quelques secondes.

⚠️ **Note sur le délai asynchrone :** les files aident pour le travail asynchrone, mais cela signifie aussi qu'elles retardent les erreurs et les boucles de rétroaction (nous y reviendrons plus loin).

### Nuances

#### 1. Partitionnement

Une seule file a ses limites de débit.

Le **partitionnement** permet un scaling horizontal. On divise essentiellement le flux entrant en plusieurs sous-files indépendantes. Différents workers peuvent alors consommer différentes **partitions** en parallèle.

Un **groupe de consommateurs** est un pool de consommateurs qui se répartissent ces partitions entre eux :

- ✅ Si vous avez 8 partitions et 2 consommateurs dans un groupe, chaque consommateur gère 4 partitions.
- ⚠️ Si vous avez besoin de plus de parallélisme, vous pouvez ajouter des consommateurs, mais il y a une limite : vous ne pouvez pas avoir plus de consommateurs que de partitions dans un seul groupe de consommateurs.
- ❌ Si vous avez 8 partitions et 8 consommateurs, ajouter un 9ᵉ consommateur n'aide pas car il ne reste plus aucune partition à consommer.

Chaque partition possède une clé. C'est ce qui détermine dans quelle partition va chaque message.

Choisir la bonne **clé de partition** (partition key) est aussi important que choisir une clé de *sharding* (shard key) de base de données, car :

1. **Ordonnancement :** les messages ayant la même clé de partition vont toujours dans la même partition, où l'ordre est garanti. Cet ordonnancement est important quand les opérations sont **non idempotentes** et que les effets de bord dépendent de l'ordre de traitement (par exemple l'exemple des transactions bancaires).
2. **Distribution équilibrée :** vous voulez que vos clés de partition répartissent le travail de manière homogène entre les partitions. Par exemple, si vous construisez une application de covoiturage, vous ne voulez pas partitionner par ville, car les grandes villes créeraient une **partition chaude** (hot partition) tandis que les petites villes laisseraient leurs workers alloués sous-exploités. Dans cet exemple, vous voudriez plutôt partitionner par `user_id` ou `ride_id`.

*Compromis :* la clé qui vous donne un **ordonnancement** strict n'est pas toujours celle qui vous donne la meilleure **distribution**. Il faut prendre le temps de réfléchir à ce compromis.

#### 2. Back pressure

Si les producteurs créent des messages plus vite que les consommateurs ne peuvent les traiter, la file grossit jusqu'à épuiser la mémoire.

Quelle est la solution ?

- **Autoscaling :** faire démarrer automatiquement plus de consommateurs ou ajouter des partitions selon la taille de la file.
- **Back pressure :** rejeter les nouveaux messages ou renvoyer une erreur demandant aux clients de réessayer plus tard.
- **Alerting :** en dernier recours, il faut toujours connecter le monitoring à des alertes sur la profondeur de la file pour savoir quand un arriéré (backlog) atteint une taille critique.

#### 3. Messages empoisonnés et DLQ

Parfois, un message échoue à être traité, quel que soit le consommateur qui s'en empare. Il peut y avoir de nombreuses raisons : il peut être malformé, contenir un état invalide, ou avoir une charge utile (payload) que les consommateurs ne sont pas capables de traiter. Il peut même s'agir d'un bug dans le code du consommateur.

On appelle cela un **message empoisonné** (poisoned message).

Plutôt que de gaspiller des ressources en réessayant indéfiniment, on fixe un **nombre maximal de tentatives**. Si les consommateurs échouent à le traiter après cette limite, il sera déplacé vers la **Dead Letter Queue (DLQ)**.

Une DLQ est une file séparée (ou une partition séparée) où les messages en échec sont envoyés pour investigation ultérieure par un administrateur, un ingénieur, ou une IA.

Là encore, il faut mettre en place de l'alerting sur la DLQ pour ne pas manquer d'opportunités d'amélioration.

#### 4. Durabilité et tolérance aux pannes

Jusqu'ici, nous avons parlé de la file comme si elle était toujours disponible, mais en pratique, c'est un SPOF (single point of failure, point de défaillance unique).

Que se passe-t-il si la file tombe en panne ?

Les files de messages modernes comme Kafka persistent les messages sur disque avec une fenêtre de rétention configurable (par exemple 1 jour, 1 semaine, ou indéfiniment) et les répliquent sur plusieurs brokers (serveurs). Si un broker tombe, une autre réplique possède les données (similaire aux répliques en lecture dans les bases de données), donc aucun message n'est perdu.

La fenêtre de rétention offre un autre avantage : vous pouvez **rejouer** des messages du **passé** : si vos consommateurs tombent en panne ou traitent les données incorrectement à cause d'un bug, vous pouvez déployer un consommateur corrigé et lui demander de réinitialiser son **offset** pour retraiter les messages passés.

### Kafka vs SQS vs RabbitMQ

Faisons une comparaison rapide entre les produits de files de messages les plus courants.

#### 1. Kafka

Apache Kafka est une plateforme de streaming distribuée. Les messages sont écrits sur disque et conservés pendant une période définie plutôt que supprimés immédiatement après leur consommation.

C'est le choix le plus populaire, particulièrement adapté à un débit élevé, à la durabilité, au streaming d'événements et au rejeu de données.

Il scale via des partitions et des groupes de consommateurs.

#### 2. SQS

AWS SQS (Simple Queue Service) est natif à AWS et constitue un service *managé*, rapide à mettre en place et relativement simple.

Il existe en deux variantes :

- **Standard Queue :** offre un débit maximal avec un ordonnancement "best-effort" et une livraison *At-Least-Once*.
- **FIFO Queue :** garantit un ordonnancement strict et un traitement *Exactly-Once*, mais avec un débit plus faible.

#### 3. RabbitMQ

RabbitMQ n'est pas aussi populaire que les deux autres. Il est écrit en Erlang et utilise des concepts comme les exchanges et les bindings pour le routage des messages.

Il est utilisé pour des configurations traditionnelles de message broker nécessitant une logique de routage complexe.

### Conclusion

Pour résumer :

- Les files de messages **découplent** vos producteurs de vos consommateurs.
- Elles **absorbent les pics de trafic** (buffer bursty traffic) afin que rien ne soit perdu.
- Elles **distribuent le travail** sur des pools de workers.

Mise à jour du 2026-11-02 :

« Une chose que j'ajouterais après des années d'intégration basée sur des MQ : une file ne supprime pas la panne, elle la retarde et la rend plus silencieuse. Le consommateur est en panne, le producteur est content, et une heure plus tard vous avez un arriéré (backlog) qui prend plus de temps à résorber que la panne n'a duré. Je recommande d'alerter sur l'âge du message le plus ancien, pas sur la profondeur de la file, et de décider en amont de ce qui arrive aux messages qui échouent sans cesse. » — Oleksandr Tyshchenko

Si vous préparez un entretien de system design, voici une bonne vidéo de hello interview qui traite de ce sujet.

*Ma stratégie de monétisation consiste à offrir gratuitement la majeure partie du contenu, mais ces articles prennent de quelques heures à plusieurs jours pour être rédigés, édités, recherchés, illustrés et publiés. Je puise ces heures dans mon temps privé, mes jours de vacances et mes week-ends. Le moyen le plus simple de soutenir ce travail est de **liker**, de vous **abonner** et de le **partager**. Si vous voulez vraiment soutenir ma démarche au sein de notre communauté, vous pouvez envisager un abonnement payant. Si vous voulez économiser, vous pouvez obtenir 20 % de réduction via ce lien. En guise de remerciement, les abonnés obtiennent un accès complet aux sections Pro-Tips et à mon livre en ligne Reliability Engineering Mindset. Votre contribution finance aussi mes produits open source comme le Service Level Calculator. Vous pouvez également inviter vos amis pour obtenir un accès gratuit ou économiser via un abonnement de groupe.*

*Et à ceux qui me soutiennent déjà, **merci** de sponsoriser ce contenu pour les autres. 🙏 Si vous avez des questions ou des retours, ou si vous voulez que j'approfondisse un sujet, faites-le-moi savoir dans les commentaires.*

Les doublons SQS qu'on rencontre le plus souvent en pratique viennent du délai de visibilité (visibility timeout). Il est par défaut de 30 secondes, donc un appel de modération qui prend 45 secondes sur un GPU chargé se fait redistribuer, et un second worker commence à traiter la même photo. Il faut dimensionner ce délai en fonction du p99 du temps de traitement, et garder la vérification d'idempotence comme garde-fou.

Merci ! Des fondamentaux, mais utiles. J'ai travaillé avec Kafka, moins avec RabbitMQ, donc c'était utile de voir comment vous avez formulé la différence dans le traitement des doublons.

## Pourquoi ça compte
Ce panorama synthétise des notions fondamentales de system design (découplage, idempotence, garanties de livraison) directement applicables à la conception d'architectures distribuées résilientes, un sujet récurrent en veille technique comme en entretien d'ingénierie.
