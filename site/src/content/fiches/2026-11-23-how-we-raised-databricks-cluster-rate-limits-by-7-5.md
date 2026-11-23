---
title: "How we raised Databricks cluster rate limits by 7.5×"
date: 2026-11-23
url: "https://substack.com/redirect/a504296a-f48b-4873-8890-7467a8e23504?j=eyJ1IjoiN3Y1bG1jIn0.HlvPOGYPdVknSYzEK1JIj6IFkAFn8zuyjtfU9Mbft9Q"
keywords: ["rate limiting", "concurrence adaptative", "cloud", "Databricks", "scalabilité", "fiabilité"]
theme: "Data"
tone: "research"
used_in: ["2026-11-23"]
---

## Résumé
L'équipe Compute Platform de Databricks explique comment elle est passée de limites fixes de débit (rate limiting) à des limites de concurrence adaptatives pour protéger la création de clusters, une opération longue et asynchrone répartie sur AWS, Azure et GCP. Les limites fixes forçaient des arbitrages impossibles : trop conservatrices, elles rejetaient des requêtes alors que de la capacité était disponible ; trop permissives, elles continuaient d'accepter du travail pendant les ralentissements des fournisseurs cloud, provoquant des « tempêtes de retry » invisibles au niveau de l'API. En combinant file d'attente bornée, limites de concurrence qui s'ajustent à la santé du système et ordonnancement équitable entre clients, Databricks a pu multiplier par 7,5 les limites par défaut de création de clusters tout en réduisant de plus de 99,99 % les erreurs de rate-limiting et en supprimant une centaine de dérogations spécifiques à des clients. La limite de débit fixe à l'entrée de l'API est conservée, mais seulement comme garde-fou ultime contre un afflux de trafic exceptionnellement élevé.

## Points clés
- Pour des opérations longues et asynchrones (la création de cluster peut durer des minutes alors que l'appel API ne prend que des millisecondes), une limite de débit fixe est un mauvais modèle de la capacité réelle du système.
- Les limites de concurrence adaptatives comptent le travail *en cours* (workflows actifs occupant un « slot ») plutôt que le nombre de requêtes entrantes par seconde, et s'ajustent selon des signaux de santé (latence de provisioning, saturation des pools de threads).
- Les retries internes déclenchés par un dépendance cloud dégradée créent des « tempêtes de retry » que le rate-limiter de l'API ne voit jamais, car ce travail a déjà été accepté.
- Une file d'attente bornée, avec expiration et rejet peu coûteux, permet d'absorber les pics de charge sans transformer une perturbation passagère en heures de retard.
- L'ordonnancement doit distinguer équitablement « qui attend », car faire attendre un peu chacun de cent clients n'a pas le même impact perçu que faire attendre longtemps un seul client pour cent requêtes.
- Résultat mesuré : limites par défaut multipliées par 7,5, plus de 99,99 % d'erreurs de rate-limiting éliminées, et plus de 100 dérogations client supprimées, sans nouvelle dérogation manuelle depuis.

## Analyse approfondie
*(synthèse détaillée et structurée de l'article, en français)*

**Contexte et problème initial**
L'équipe Compute Platform de Databricks transforme l'infrastructure cloud brute en clusters prêts à exécuter les charges de travail des clients : provisionnement de machines virtuelles et coordination de la création de clusters sur AWS, Azure et Google Cloud. L'objectif est de garder ces systèmes disponibles tout en laissant les clients utiliser le maximum de capacité qu'on peut leur fournir en toute sécurité.

Historiquement, la protection reposait sur des limites de débit fixes (rate limits), testées contre différents profils de charge et scénarios de panne, avec une mise à l'échelle obtenue surtout en ajoutant des ressources et en ajustant des limites par client. Mais la combinaison des types de charge de travail et des pannes de dépendances rendait ces limites de plus en plus difficiles à calibrer : des limites prudentes refusaient des requêtes clients alors qu'il restait de la capacité disponible, tandis que des limites généreuses continuaient d'accepter des requêtes même quand les services ou leurs dépendances (notamment les fournisseurs cloud) ralentissaient. Les ingénieurs devaient abaisser manuellement les limites en incident puis les relever après coup.

**L'analogie de la cuisine**
L'article compare la plateforme de calcul à une cuisine qui veut servir autant de commandes que ses cuisiniers et équipements le permettent. Une règle fixe du type « dix nouvelles commandes acceptées par minute, quoi qu'il arrive aux fourneaux » pose deux problèmes : elle refuse des commandes même quand il reste de la capacité de cuisson, et elle continue d'accepter des commandes plus vite que les cuisiniers restants ne peuvent les traiter dès qu'un four tombe en panne — obligeant le responsable à réécrire sans cesse la pancarte. Une cuisine mieux organisée maintient plutôt une courte file d'attente et limite le nombre de plats en préparation simultanée : si un four casse, moins de plats démarrent ; quand la capacité revient, davantage peuvent commencer. Les commandes peuvent attendre brièvement, mais seulement s'il reste du temps pour les servir.

**Pourquoi un débit fixe ne convient pas aux opérations longues**
Un appel API peut déclencher bien plus de travail que ce que le gestionnaire exécute lui-même. Pour la création de cluster, le gestionnaire valide la requête, enregistre un item de travail, puis répond immédiatement — tandis qu'un workflow en arrière-plan coordonne plusieurs services, met à jour l'état et provisionne les ressources cloud. Ces opérations se terminent de façon asynchrone et leur durée dépend de la santé et de la capacité de leurs dépendances : l'appel API prend des millisecondes, le workflow lui-même peut prendre des minutes.

Un limiteur de débit placé à l'entrée de l'API plafonne les requêtes par fenêtre de temps — utile pour faire respecter des quotas, prévenir les abus et protéger les ressources qui traitent l'appel lui-même. Mais ce mécanisme suppose une capacité disponible et un coût de traitement par requête raisonnablement prévisibles. Pour la création de cluster, ni l'un ni l'autre n'est stable : une requête peut provisionner quelques VM, une autre beaucoup plus, et la santé du fournisseur cloud fait varier la durée de provisioning. Lors d'un ralentissement partagé, de nombreux workflows prennent plus longtemps en même temps : le même débit de requêtes entrantes peut donc laisser beaucoup plus de travail « en vol », alors même que la capacité du système à le terminer diminue.

**Les tempêtes de retry**
Lorsqu'une dépendance se dégrade, davantage d'appels échouent ou expirent. Les workflows de longue durée relancent ces appels pour se rétablir de pannes temporaires. Multiplié par le nombre de workflows actifs, cet effort de retry ajoute de la pression sur la dépendance déjà en difficulté, provoquant davantage d'échecs et donc davantage de retries — une « tempête de retry ». Ces retries internes proviennent d'un travail déjà accepté : le limiteur de débit de l'API ne les voit donc jamais, et ils peuvent entretenir la surcharge même après le retour à la normale du trafic entrant. Limiter le nombre de workflows actifs aide à contenir cette pression et donne une chance au travail non terminé de s'écouler.

Baisser la limite ne règle pas ce décalage structurel : cela achète simplement une marge en rejetant davantage de travail en période saine, marge qu'un ralentissement suffisamment important finit par épuiser. Augmenter la limite exploite mieux la capacité saine, mais accepte davantage de travail en période de dégradation. Un seul chiffre doit couvrir les deux situations — d'où l'intérêt d'un mécanisme adaptatif.

**Terminologie**
L'article distingue deux mécanismes selon ce qu'ils comptent :

| Terme | Signification dans l'article |
|---|---|
| **Opération** | Le workflow complet, incluant le travail en arrière-plan après la réponse de l'API. |
| **Limite de débit** | Un plafond de requêtes acceptées par unité de temps (ex. 10 req/s), avec une éventuelle tolérance de pic. |
| **Concurrence** | Le nombre d'opérations actives à un instant donné, y compris celles en attente de dépendances. |
| **Limite de concurrence** | Un plafond d'opérations actives (ex. 100 en même temps) ; chaque opération occupe un « slot » jusqu'à sa fin. |
| **Backlog** | Le travail accepté mais en attente de démarrage, n'ayant pas encore obtenu de slot actif. |

Chacun de ces deux mécanismes peut être fixe ou adaptatif ; la comparaison centrale de l'article porte sur les limites de débit fixes versus les limites de concurrence adaptatives pour protéger un travail de longue durée.

**Le mécanisme des « slots »**
Dans Databricks classic compute, l'équivalent des « plats en préparation » de la cuisine est l'ensemble des workflows de création de cluster encore en train de provisionner l'infrastructure. Chaque workflow actif obtient un slot, et le nombre de slots disponibles est ajusté selon les conditions.

Pour une requête CreateCluster portant sur un cluster avec un driver et plusieurs VM worker : une fois la requête acceptée, son workflow de provisioning attend un slot avant de démarrer. Le travail est donc suivi comme étant en file d'attente, en traitement actif, ou terminé. Si tous les slots sont occupés, la requête reste en attente ; un workflow actif garde son slot pendant qu'il provisionne les VM et patiente sur ses dépendances ; une fois le workflow terminé, son slot se libère pour un autre lancement de cluster. Un cluster lancé avec succès peut ensuite tourner pendant des heures sans occuper ce slot de provisioning — le slot couvre l'*ensemble* de l'opération de provisioning, pas uniquement l'appel API, et suivre un slot ne nécessite pas de garder un thread occupé.

Ce contrôleur compte les workflows de provisioning actifs — une mesure distincte du nombre de clusters en cours d'exécution ou du nombre de VM/vCPU alloués. Un seul workflow pouvant provisionner de nombreuses VM, un slot ne correspond pas à un coût en ressources fixe.

Si un fournisseur cloud met plus de temps à provisionner des VM, les workflows actifs gardent leur slot plus longtemps, donc de nouveaux lancements démarrent moins souvent même si la limite de slots reste inchangée — les clients perçoivent alors des délais de lancement plus longs du fait des requêtes en attente.

**Le contrôle adaptatif**
Le contrôle adaptatif ajuste aussi la limite de slots elle-même. Pour la création de cluster, les signaux utiles incluent la durée de provisioning et la saturation des pools de threads critiques. Quand ces signaux indiquent une congestion, le contrôleur réduit le nombre de workflows de provisioning concurrents ; à mesure que les conditions s'améliorent, il en autorise prudemment davantage. La pression de capacité agit donc au moment où le travail accepté démarre, tandis que les rejets au niveau du rate-limit RPC restent réservés aux pics de trafic entrant exceptionnellement élevés.

Réduire la limite empêche de nouvelles opérations de démarrer jusqu'à ce que le travail actif retombe sous ce seuil, mais les opérations déjà en cours ont quand même besoin de temps pour se terminer — un délai de réponse qui compte quand les workflows durent plusieurs minutes. Les retries ont également besoin de backoff et d'un nombre maximal de tentatives, afin que les workflows actifs ne continuent pas d'accabler une dépendance en cours de rétablissement. La limitation de concurrence ne peut pas réparer une dépendance indisponible, mais elle peut limiter la pression supplémentaire pendant que cette dépendance se rétablit.

**Au-delà du contrôle : qui attend, combien de temps, et pourquoi**
La boucle de contrôle répond à la question « combien de travail démarrer ». Construire un service utile implique aussi de décider qui attend, combien de temps, et ce qu'on communique à l'utilisateur.

« Trop de requêtes » peut cacher deux situations très différentes : (1) un client envoie son trafic habituel mais une dépendance partagée ralentit — la capacité a chuté, et demander au client de modifier son trafic revient à mal attribuer un problème de service ; (2) un client envoie un pic de trafic inhabituel alors que le service reste sain et que d'autres clients se disputent les mêmes ressources — limiter ce pic protège alors la part équitable des autres. Pour distinguer ces cas, il faut suivre séparément la santé du système, la demande entrante de chaque tenant, et la décision d'ordonnancement elle-même. Un grand nombre d'opérations en vol ne prouve pas à lui seul qu'un client a envoyé trop de trafic : ces opérations peuvent être bloquées derrière une dépendance lente. De même, un pic ne doit pas nécessairement être limité par souci d'équité si de la capacité disponible existe et que la politique le permet.

Cette distinction doit apparaître dans les métriques et les explications données aux clients : elle indique aux opérateurs s'il faut enquêter sur une perte de capacité ou sur une charge inhabituelle, et dit aux clients si modifier leur comportement aiderait. Les échecs causés par une dégradation de service doivent être comptés dans les métriques de fiabilité du service, même lorsqu'ils se manifestent comme du throttling ; pour les requêtes acceptées qui attendent en file, on mesure plutôt l'impact sur la latence de lancement du cluster.

**La file d'attente**
Pour une opération qui dure plusieurs minutes, une courte attente vaut souvent mieux qu'une erreur immédiate suivie d'un nouvel essai : une file peut absorber un pic et laisser le système rattraper le retard. Mais cela ne fonctionne que si l'attente respecte le délai acceptable de la requête : il faut borner la taille de la file et le temps d'attente de chaque requête, rendre la progression visible, et rejeter ou faire expirer le travail qui ne peut plus se terminer utilement. Une file ne peut pas transformer une surcharge soutenue en capacité ; une file non bornée peut transformer une perturbation brève en des heures de retard.

Une requête en file doit être un petit enregistrement, pas un worker actif occupant des ressources rares. Un backlog plus important ne doit pas rendre chaque opération active plus coûteuse via des scans répétés ou une compétition pour les threads et connexions. Le nettoyage mérite la même attention : si un gros backlog expire d'un coup, le service doit pouvoir l'écarter dans un délai prévisible — il faut prévoir le pire backlog, garder l'expiration et le rejet peu coûteux, et éviter toute préparation coûteuse pour un travail dont le délai est déjà dépassé ; sinon, la file peut occuper le service bien après la fin de la congestion initiale.

**L'équité entre clients**
Si un service doit retarder cent requêtes, vaut-il mieux que cent clients voient chacun une requête légèrement lente, ou qu'un seul client voie cent requêtes lentes ? La métrique globale peut paraître identique, mais l'expérience client, elle, ne l'est pas. Un ordonnanceur fait ce choix, qu'on le spécifie ou non. Il faut donc définir quel travail passe en premier, quelle part chaque tenant doit recevoir en cas de contention, et comment le travail de priorité moindre évite d'attendre indéfiniment — tout en laissant les tenants utiliser la capacité par ailleurs inactive quand la politique le permet, tout en préservant un accès équitable quand d'autres tenants ont besoin de leur part.

**Le système déployé et les résultats**
Ces idées ont été appliquées à un système intégré de gestion de charge pour la création de clusters sur Databricks classic compute : une courte requête API démarre un workflow bien plus long qui coordonne plusieurs dépendances, notamment les fournisseurs cloud publics, pour provisionner les ressources de calcul. Le système combine requêtes en file, limites de concurrence adaptatives et ordonnancement équitable ; il utilise le travail déjà en vol et la santé du système pour décider quand les opérations en attente peuvent démarrer.

La limite de débit de l'API est conservée comme ultime ligne de défense contre un trafic entrant exceptionnellement élevé, et fournit une borne de débit communicable aux clients. Les limites de concurrence adaptatives restent internes au service et gouvernent le démarrage du travail accepté — une réponse API réussie ne garantit donc pas un lancement immédiat du cluster ni son achèvement dans un délai fixe.

L'analyse du déploiement initial rapporte trois résultats : les limites par défaut de débit pour la création de cluster ont été multipliées par 7,5 ; les erreurs de rate-limiting sur la création de cluster ont chuté de plus de 99,99 % dans le périmètre étudié ; et plus d'une centaine de dérogations spécifiques à des clients ont été supprimées dans ce même périmètre. Depuis cette augmentation, peu de clients ont atteint les nouvelles limites plus hautes, et aucune nouvelle dérogation manuelle n'a été ajoutée.

**Pistes d'extension**
Appliquer cette approche à d'autres types de travail long soulève d'autres questions de conception : quand les opérations ont des coûts en ressources très différents, compter chacune comme un seul slot peut être trop grossier — des slots pondérés ou des limites séparées sont des extensions possibles. Pour des workflows avec plusieurs goulots d'étranglement, une autre question est de savoir où appliquer le contrôle afin qu'une dépendance lente ne bloque pas un travail sans rapport. Enfin, lors d'un ralentissement d'un fournisseur cloud, des workflows déjà en train de provisionner des VM peuvent continuer à relancer des tentatives même après que les nouveaux lancements ont ralenti : il faut donc associer les limites de concurrence à un backoff de retry et à un nombre maximal de tentatives pour réduire cette pression pendant la phase de rétablissement.

L'article renvoie enfin à un article complémentaire, « High Performance Ratelimiting at Databricks », pour le problème distinct de l'application de quotas API à grande échelle.

## Pourquoi ça compte
Ce cas d'usage illustre un principe de fiabilité transférable à tout système distribué gérant des opérations asynchrones de longue durée : remplacer un rate-limiting statique par un contrôle de concurrence adaptatif, couplé à une file bornée et à un ordonnancement équitable, permet de scaler sans multiplier les dérogations manuelles ni s'exposer aux tempêtes de retry invisibles pour les équipes SRE et plateforme.
