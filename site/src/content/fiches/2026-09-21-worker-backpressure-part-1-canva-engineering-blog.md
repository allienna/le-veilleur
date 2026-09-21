---
title: "Worker Backpressure (Part 1) - Canva Engineering Blog"
date: 2026-09-21
url: "https://substack.com/redirect/c98eaed3-8baa-40ef-bac9-afe310942c2f?j=eyJ1IjoiN3Y1bG1jIn0.HlvPOGYPdVknSYzEK1JIj6IFkAFn8zuyjtfU9Mbft9Q"
keywords: ["backpressure", "files d'attente", "résilience", "ingénierie backend", "contrôle de flux", "systèmes distribués"]
theme: "Tech"
tone: "research"
used_in: ["2026-09-21"]
---

## Résumé
Canva présente « Worker Backpressure », un mécanisme intégré à sa librairie de files d'attente qui permet à ses workers asynchrones de ralentir automatiquement leur cadence lorsque leurs dépendances (bases de données, services externes) commencent à échouer, puis de reprendre leur vitesse normale dès que ces dépendances se rétablissent. Le système a été testé en conditions réelles lors de deux incidents de production : une panne d'un fournisseur cloud provoquant des pics d'erreurs intermittents pendant environ 4 heures, et une surcharge continue de 32,5 heures liée au dépassement d'un quota de débit. Dans les deux cas, la Dead Letter Queue (DLQ) est restée quasiment vide et aucun ingénieur d'astreinte n'a été sollicité, alors que ce type d'incident aurait normalement généré des milliers de messages en échec. Le mécanisme fonctionne entièrement en local, sans coordination externe, via une boucle de rétroaction qui ajuste la concurrence du worker en fonction du taux d'échec observé.

## Points clés
- Les workers de Canva sont conçus pour être « gourmands » : ils consomment les messages dès que possible, ce qui est optimal tant que les dépendances sont saines, mais devient dangereux quand une dépendance commence à faiblir (surcharge en cascade, messages voués à l'échec, DLQ qui explose, astreinte mobilisée).
- Les solutions existantes (scaling manuel, rate limiting fixe, circuit breakers, backoff exponentiel par message, adaptive backoff façon Google SRE) présentaient chacune des limites : réaction manuelle trop lente, seuils figés inadaptés à une capacité qui varie, ou absence de mécanisme progressif entre pleine vitesse et arrêt total.
- Worker Backpressure repose sur trois composants : des signaux (succès/échec après chaque message), un contrôleur de backpressure (interface pluggable qui maintient un « facteur de recul » entre 0.0 et 1.0 par rapport à un point de consigne de taux d'échec toléré), et des permis (le nombre de messages que le worker est autorisé à traiter en parallèle, réduit proportionnellement au recul).
- Le mécanisme n'ajoute aucun appel réseau : tout se calcule localement avec deux opérations arithmétiques par cycle (mise à jour du facteur de recul, ajustement de la concurrence demandée).
- Lors de la panne cloud, le taux d'échec fleet-wide a culminé à 1,42 % (contre des pics ponctuels à 50 % sur certaines instances) et la DLQ n'a reçu qu'un seul message sur toute la durée de l'incident.
- Lors de la surcharge de 32,5 heures, le débit global est resté au-dessus de la baseline pré-incident (environ 2 millions de messages/heure) et seuls 22 messages sur 1,8 million de tentatives échouées ont fini en DLQ.

## Analyse approfondie

### Le problème : des workers trop gourmands

Une grande partie du travail chez Canva s'exécute de manière asynchrone : une requête arrive, un message est déposé sur une file d'attente, et un worker le récupère plus tard pour effectuer le traitement réel (redimensionner un asset, exécuter un modèle de classification, envoyer un e-mail, réconcilier un abonnement). Cette architecture garde le chemin de la requête rapide pendant que la file absorbe le travail lent ou en rafale, et elle garde la requête fiable : si une dépendance tombe brièvement, la requête de l'utilisateur réussit quand même, le travail attendant simplement dans la file.

Les workers sont conçus pour être gourmands, et la plupart du temps c'est exactement ce qu'on souhaite : dès qu'un message arrive et qu'un worker a de la capacité disponible, il le récupère et le traite. Quand tout est sain en aval, cela offre une latence minimale et une pleine utilisation de l'infrastructure déjà payée.

Pour traiter un message, un worker appelle presque toujours une dépendance : une ressource partagée comme une base de données, ou un autre service. Le problème commence quand cette dépendance se met à échouer. Le worker gourmand ne s'en aperçoit pas et continue à tirer des messages et à envoyer toujours plus de requêtes, ce qui nuit de plusieurs façons :
- Cela verse de l'huile sur le feu, ralentissant encore davantage la récupération de la dépendance.
- Traiter un message voué à l'échec gaspille des ressources déjà rares.
- Les messages échoués sont retentés jusqu'à atterrir sur la Dead Letter Queue (DLQ), qu'il faut ensuite vider et retraiter, souvent manuellement.
- Un ingénieur d'astreinte est alerté et doit surveiller la situation jusqu'au rétablissement de la dépendance.

À l'échelle de Canva, ce n'est pas un cas rare : l'entreprise fait tourner des milliers de files avec une logique métier et des dépendances très diverses. Exemple typique : un utilisateur clique sur « Exporter », un message part sur une file, un worker le récupère, va chercher les données de design dans une base, puis appelle un service de rendu. Si cette base est déjà lente, par exemple à cause d'une migration en arrière-plan, le worker continue de tirer de la file à pleine vitesse. Quelques réponses lentes de la base peuvent alors dégénérer en incident critique, avec des exports en échec pour des milliers d'utilisateurs.

Chaque incident de ce type soulève les mêmes questions : le worker doit-il s'arrêter complètement ou simplement ralentir ? De combien, et pendant combien de temps ? Quels signaux doivent guider cette décision ? Trouver une réponse unique qui fonctionne sur une flotte aussi diverse est loin d'être trivial.

### Ce que les équipes faisaient déjà

**Scaler manuellement la flotte de workers.** Augmenter la capacité en pleine incident risque de déverser encore plus de charge sur la dépendance déjà défaillante, et tout chiffre choisi à la main reste une estimation : trop bas, le backlog continue de croître ; trop haut, on paie des workers qui restent inactifs.

**Rate limiting dans la logique de traitement.** Une limite fixe n'est correcte que pour un monde figé. La capacité change en permanence, surtout pour les dépendances partagées, si bien qu'une limite obsolète soit bride le worker sans raison, soit se situe si loin au-dessus de la capacité réelle qu'elle ne protège presque rien.

**Circuit breakers.** Ils comptent les erreurs, se déclenchent une fois un seuil franchi, et coupent tout le trafic jusqu'à l'expiration d'un délai de repos. Il n'y a pas de montée en charge graduelle entre pleine vitesse et arrêt complet, et le flux soudain repris à la réouverture peut de nouveau faire tomber une dépendance qui venait tout juste de reprendre son souffle.

**Backoff exponentiel.** Appliqué aux retries, il lisse les tempêtes de nouvelles tentatives individuelles, mais il agit message par message et ne régule pas le débit global auquel un worker sollicite une dépendance.

**Backoff adaptatif.** Il encapsule les appels à une dépendance et rejette une fraction croissante d'entre eux à mesure que les erreurs augmentent, sur le modèle du « client-side adaptive throttling » décrit dans le chapitre « Handling Overload » du livre SRE de Google. Contrairement au backoff de retry, il rejette la charge au point d'appel plutôt que de retarder chaque message échoué. Une équipe de Canva avait déjà construit une telle librairie et la faisait tourner en production. Elle fonctionnait bien et a directement inspiré ce projet, mais elle vivait en dehors de la librairie de files partagée et était figée sur un seul algorithme.

### La solution : une boucle de rétroaction intégrée

Canva avait besoin d'une solution de backoff adaptatif suffisamment générale pour sa flotte hétérogène de files, baptisée **Worker Backpressure** : un mécanisme intégré directement à la librairie `queue`. Le worker observe comment se déroule son propre travail et ajuste sa vitesse en conséquence, en levant le pied quand les erreurs montent et en réaccélérant quand la dépendance se rétablit, sans intervention humaine.

Le backpressure est une **boucle de rétroaction** autour des appels du worker à sa dépendance. Il suit le résultat de chaque appel comme un signal de la santé de la dépendance, et régule la concurrence du worker : combien de messages il peut traiter à la fois. Quand la dépendance semble saine, le backpressure reste en retrait ; quand elle peine, il freine le worker. Freiner tôt signifie aussi moins de tentatives vouées à l'échec gaspillant des ressources rares, et moins de messages échoués finissant en DLQ.

Le backpressure se compose de trois éléments :

1. **Signaux.** Après chaque message traité, le worker enregistre le résultat : succès ou échec.
2. **Contrôleur de backpressure.** Un contrôleur pluggable (une interface plutôt qu'un algorithme unique et figé) consomme ces résultats et maintient un seul nombre : le **facteur de recul** (backoff factor), allant de `0.0` (pleine vitesse) à `1.0` (recul complet). Il travaille par rapport à un **point de consigne** configuré : le taux d'échec considéré comme du bruit de fond acceptable. Tant que le taux d'échec reste sous ce point de consigne, le contrôleur ne fait rien. Dès qu'il le dépasse, le contrôleur commence à faire reculer le worker.
3. **Permis.** Avant chaque scrutation (poll), le worker demande au contrôleur combien de messages il peut tirer et traiter en parallèle (`X` dans le schéma original). Le contrôleur réduit ce nombre proportionnellement au recul en cours.

Un choix de conception important est que tout cela se passe localement, sans coordinateur externe et sans appel réseau supplémentaire. Le coût d'exécution total se limite à deux opérations arithmétiques : une pour faire évoluer le facteur de recul après chaque résultat, une autre pour ajuster la concurrence demandée à chaque scrutation.

Note sur le nom : le terme « backpressure » désigne habituellement un signal qui remonte vers l'amont pour ralentir le producteur, alors qu'un worker qui se freine lui-même se rapproche davantage du concept « concurrency-limits » de Netflix. Canva a conservé le nom car refuser du travail au niveau du worker laisse cette charge dans la file, qui est le seul amont vers lequel on peut effectivement repousser la pression.

### Le mécanisme à l'épreuve du réel

Canva n'a pas eu à attendre longtemps pour un vrai test : le backpressure a déjà protégé ses dépendances lors de deux incidents de production.

Sur les tableaux de bord, la ligne pointillée orange marque le point de consigne fixé à 5 %, identique pour les deux workers. Chaque instance est évaluée par rapport à ce point de consigne sur la base de ses propres résultats, si bien qu'une seule instance peut momentanément dépasser 5 % et se faire freiner pendant que le taux d'échec global de la flotte reste bas.

**Panne à pics multiples.** Le premier incident est la panne du fournisseur cloud évoquée en introduction : environ 4 heures de pics d'erreurs intermittents, avec plusieurs dépendances du worker défaillantes en même temps. Deux éléments ressortent :
- Le backpressure a ralenti puis réaccéléré le worker automatiquement, en tournant toujours avec la configuration par défaut déployée au lancement.
- La DLQ n'a grossi que d'un seul message sur toute la durée de l'incident.

Le nombre de succès reflète la charge de travail normale du worker, tandis que le nombre d'erreurs présente des pics à plusieurs moments pendant l'événement cloud. Certaines instances individuelles ont brièvement atteint jusqu'à 50 % d'échec avant d'être freinées, si bien que la moyenne au niveau de la flotte n'a culminé qu'à 1,42 %. Le facteur de recul suit de près les pics d'erreurs, montant quand les erreurs apparaissent et redescendant quand elles disparaissent. La profondeur de la DLQ bouge à peine : une marche d'un seul message plutôt que les milliers de messages en échec qu'un tel événement aurait normalement produits.

| Métrique | Valeur observée |
|---|---|
| Nombre total de succès | 1 610 173 |
| Nombre total d'erreurs | 498 |
| Taux d'échec | 0,03 % en moyenne sur l'incident, pic de 1,42 % au niveau de la flotte |
| Fenêtre de l'incident | ~4 h de pics d'erreurs intermittents |
| Croissance de la DLQ pendant l'incident | 1 message (~0,25 par heure) |

**Une journée et demie de surcharge soutenue.** Le second incident présente un profil de défaillance opposé : une surcharge continue plutôt que des pics courts. Un worker envoie des messages vers une autre file soumise à un quota de débit strict. Un afflux de travail a fait dépasser ce quota au taux d'envoi combiné de la flotte, et la file a rejeté les envois pendant 32,5 heures jusqu'à ce qu'un correctif soit déployé. Le rôle du contrôleur de backpressure ici était de contenir la défaillance en attendant le correctif :
- Le contrôleur est resté actif pendant 32,5 heures d'affilée. Des rafales sur certaines instances ont atteint jusqu'à ~19 % et ont été freinées dès qu'elles franchissaient le point de consigne, tandis que le taux d'échec global de la flotte a culminé à seulement 3,7 %. Le pic plus élevé, à ~43 %, correspond à une brève rafale précurseur sur une instance avant le début de la surcharge soutenue.
- Le débit a tenu bon : la flotte a continué à traiter environ 2 millions de messages par heure, au-dessus de sa baseline pré-incident.
- Sur cette file, un message part en DLQ après 5 tentatives de livraison échouées. Sur 1,8 million de tentatives échouées, seuls 22 messages sont allés jusque-là, soit environ un pour 82 000 échecs (~0,7 par heure). Sans backpressure, le point de comparaison le plus proche disponible est le taux d'échec de ~19 % observé sur les instances que le contrôleur n'avait pas encore ralenties. Ce chiffre est probablement sous-estimé, car il a été mesuré alors que le backpressure ralentissait déjà le reste de la flotte, soulageant la pression sur le quota partagé. Une flotte non protégée aurait aussi retenté chaque message échoué à pleine vitesse, en plus d'une charge déjà supérieure au quota. Même en supposant des échecs indépendants sur les 5 tentatives d'un message, 0,19⁵ appliqué aux 65 millions de messages traités donne environ 16 000 messages en DLQ (~500 par heure) — et ce n'est qu'une borne basse, car un message retenté dans la fenêtre de 32,5 heures aurait toujours heurté le quota dépassé, rendant l'échec des tentatives suivantes plus probable.

| Métrique | Valeur observée |
|---|---|
| Nombre total de succès | 63 285 748 |
| Nombre total de tentatives échouées | 1 795 025 |
| Taux d'échec | 2,76 % en moyenne sur l'incident, pic de 3,7 % au niveau de la flotte |
| Durée sous backpressure | 32,5 h en continu |
| Croissance de la DLQ pendant l'incident | 22 messages (~0,7 par heure) |

**Ce que montrent ces incidents.** Les deux incidents présentaient des profils de défaillance très différents, et dans les deux cas le backpressure a joué le même rôle : freiner le worker tant que des erreurs étaient présentes, puis le ramener à pleine vitesse dès qu'elles cessaient. Un worker non protégé aurait continué à marteler des dépendances déjà en difficulté, produisant un flot de messages en échec et le travail d'astreinte qui s'ensuit habituellement. Le plus satisfaisant, selon l'équipe, a été de voir un mécanisme conçu pendant des mois tenir sans supervision lors de deux incidents réels, faisant exactement ce pour quoi il avait été construit, sans que personne ne soit alerté en pleine nuit.

### Compromis assumés

Dans cette première itération, l'équipe a fait des choix de conception délibérés en faveur d'une solution simple mais efficace, avec l'intention de déployer, d'évaluer, puis d'itérer.

**Un coût en débit.** Le backpressure réduit le taux d'erreur, mais coûte aussi du débit. L'équipe considère cela comme un prix raisonnable pour contenir le rayon d'impact d'une défaillance et éviter le travail manuel qui en découle habituellement. Dans les deux incidents décrits, les workers disposaient d'assez de marge pour absorber le ralentissement, et le worker de l'incident de surcharge soutenue a même maintenu un débit supérieur à sa baseline pré-incident. Un worker déjà à pleine capacité ressentirait, en revanche, ce coût plus nettement.

**Un signal unique et simple.** Le contrôleur ne réagit qu'à un seul signal, succès contre échec, comme indicateur indirect de la santé de la dépendance. Cela garde le mécanisme facile à raisonner, mais un indicateur unique ne convient pas forcément à toutes les charges de travail, et l'équipe ne sait pas encore où cette limite se manifestera. Elle s'attend à le découvrir à mesure que le déploiement expose le backpressure à une plus grande variété de workers et de modes de défaillance. Commencer étroit était un choix délibéré pour cette première implémentation ; le contrôleur reste extensible, et d'autres signaux, comme la latence ou le nombre de messages en cours, pourront être ajoutés plus tard.

### Prochaines étapes

L'objectif immédiat de Canva est de déployer le backpressure sur l'ensemble des workers de files d'attente de l'entreprise.

Ce billet laisse aussi plusieurs questions en suspens : comment exactement le facteur de recul évolue-t-il ? Si un worker entièrement freiné ne tire plus aucun message, comment détecte-t-il que sa dépendance s'est rétablie ? Et comment choisir les deux paramètres qui règlent l'ensemble du mécanisme ? La deuxième partie de cette série, à venir, ouvrira le contrôleur, le soumettra à une série de pannes simulées, et couvrira les pistes explorées au-delà.

### Remerciements

L'article remercie Natalie Tridgell, Ross Black, Michael Yates et Elle Dally pour leur contribution à la construction du backpressure, ainsi que Tim Deng et Xushen Ma, dont les équipes pionnières ont aidé à étudier le problème, ajuster les valeurs par défaut, et qui ont fait confiance au mécanisme en production.

## Pourquoi ça compte
Ce retour d'expérience illustre une approche de résilience simple, locale et peu coûteuse (deux opérations arithmétiques, aucun appel réseau) qui surpasse en pratique les circuit breakers et rate limiters classiques face à des pannes de dépendances réelles ; un pattern directement transposable à toute architecture de traitement asynchrone à grande échelle.
