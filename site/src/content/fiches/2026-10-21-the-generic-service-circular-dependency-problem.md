---
title: "The 'generic' service circular dependency problem"
date: 2026-10-21
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.jayfreestone.com%2Fwriting%2Fthe-generic-circular-dependency-problem%2F%3Futm_source=tldrdev/1/010001a1590528e5-7bd99b87-b914-4994-a1b4-a75f54780554-000000/TARoUUYWxclqHQZzM84_1ujHUDbQgqIEpGgxSsdUZpo=452"
authors: ["Jay Freestone"]
keywords: ["dépendances circulaires", "architecture logicielle", "couplage", "TypeScript", "services génériques", "design patterns"]
theme: "Software"
tone: "opinion"
used_in: ["2026-10-21"]
---

## Résumé
L'article décrit un piège architectural récurrent : les services « génériques » (analytics, emails, notifications, autorisation...) censés rester découplés du reste du système finissent, par souci de typage fort, par importer les types des domaines métier qu'ils servent — créant des dépendances circulaires. L'auteur distingue un couplage « de type » (bénin, disparaît à l'exécution) d'un couplage « de logique » (grave, le service générique se met à contenir de la logique métier). Il propose plusieurs remèdes concrets : encapsuler la dépendance via un adaptateur, répartir la logique dans des handlers spécifiques au domaine, accepter une duplication contrôlée des types, ou mettre en place un système d'enregistrement par plugin (avec, en TypeScript, l'« augmentation de module » pour garder le typage sans import circulaire). Il conclut qu'un service générique doit rester ignorant du vocabulaire métier de ses consommateurs — sinon, il faut admettre qu'il n'a jamais été vraiment générique.

## Points clés
- Un service « générique » (analytics, email, notifications...) dérive souvent vers une dépendance circulaire dès qu'on veut le typer fortement : il doit importer les types des domaines qui l'utilisent, alors que ce sont ces domaines qui l'appellent.
- Deux formes de couplage : le couplage *de type* (un `import type` qui disparaît à la compilation, inoffensif mais signe avant-coureur) et le couplage *de logique* (le service générique contient des branches `if/else` métier — bien plus dangereux et difficile à défaire).
- Solution la plus simple : envelopper la dépendance générique dans un adaptateur propre au domaine (wrapper typé), plutôt que de faire remonter les types métier dans le service générique.
- Pour la logique métier égarée dans un service générique : déplacer les handlers spécifiques vers le domaine concerné, qui appelle ensuite le service générique comme simple dépendance d'exécution (couplage runtime assumé, pas structurel).
- Alternative : accepter une duplication raisonnée des types (interface minimaliste côté service générique, validation/parsing plus précis côté consommateur) — proche du principe de ségrégation des interfaces.
- Pour les systèmes monolithiques : un mécanisme d'enregistrement par plugin (registration), combiné en TypeScript à l'augmentation de module (`declare module`), permet au service générique de rester agnostique tout en gardant un typage fort.

## Analyse approfondie
**Le piège de départ.** Tout commence avec de bonnes intentions : un service de feature flags, un service d'analytics, un service d'emails transactionnels, un parseur de messages — bref, un service générique et agnostique du domaine, volontairement découplé du reste parce que plusieurs autres services partagent le même besoin. Mais on veut aussi la sécurité du typage, alors on se met à tout typer fortement : un type `AnalyticsEvent` en union discriminée (`ORDER_PLACED`, `PRODUCT_ADDED`, `USER_REGISTERED`...) avec une interface `AnalyticsClient` exposant une méthode `send`. Même chose côté email, avec un type `EmailPayload` listant `ORDER_CONFIRMATION`, `FORGOTTEN_PASSWORD`, etc.

Le projet grossit, et une question se pose vite : le service d'email doit-il connaître tous les emails (après tout, c'est dans son nom), ou bien le service `users` doit-il connaître les emails liés aux utilisateurs, et le service de commandes ceux liés aux commandes ? Les deux options semblent défendables en début de projet.

On réalise rapidement qu'à moins de dupliquer les structures de données entre services génériques et services métier, il faut les partager : le service d'analytics se met à importer `OrderPlacedDetails` depuis `#orders`, `ProductDetails` depuis `#products`, `UserRegisteredDetails` depuis `#users`. Le service générique doit alors importer la cuisine entière, et se retrouve à connaître tous les domaines qui l'utilisent — alors que ce sont précisément ces domaines qui l'appellent. On obtient une dépendance circulaire (si le langage le permet ; impossible en Go), ce qui n'est pas un problème en soi, mais c'est le début d'une mauvaise odeur.

**Deux formes de couplage.** La majorité de ce couplage prend l'une de ces deux formes : typée ou logique.

Le couplage *de type* peut être aussi anodin qu'un client analytics qui se contente de retransmettre un payload. Le module `orders.ts` appelle `trackOrder(order)` depuis le module analytics ; en retour, `analytics.ts` importe le type `Order` uniquement pour typer l'appel — il ne lit jamais `id` ni `total`, il sérialise juste le payload tel quel. On a donné au module analytics une dépendance vers `orders` dans le seul but de garder l'appel typé. Comme c'est un `import type`, cela disparaît à l'exécution, donc il n'y a pas de cycle *runtime* — mais ça sent quand même mauvais.

Le couplage *logique* est bien plus terrifiant. L'auteur cite un exemple rencontré récemment dans un service `notifications` censé se contenter d'envoyer des emails : un handler d'événements avec une vingtaine de branches `if/else` qui, selon le nom de l'événement (`TaskReassignmentRequired`, `ProjectAnnouncementPosted`, `ProjectCommentPosted`, `ProjectCreated`, etc.), appelle des fonctions différentes (`handleTaskReassignment`, `handleProjectAnnouncement`, `handleComment`, `handleProjectSetup`...). Ce qui est censé être un simple « expéditeur » générique de notifications :
- décide qui doit recevoir un email ;
- va chercher les données nécessaires à la composition de l'email auprès d'autres services ;
- envoie l'email.

C'est bien pire, et bien plus difficile à démêler. Un service d'email peut légitimement connaître destinataires, objets et corps de messages. Un moteur de rendu de confirmation de commande doit forcément comprendre les données de commande. Un domaine « notifications » peut légitimement posséder les préférences, les abonnements et la sélection des destinataires. Mais un monstre hybride comme celui-ci connaît tout, et ne fera que grossir avec le temps.

**Solution 1 — Envelopper la dépendance.** La façon la plus simple et la plus classique de gérer ce couplage générique consiste à envelopper la dépendance, exactement comme on le ferait pour n'importe quelle bibliothèque externe — que la frontière soit un appel HTTP (microservice) ou une frontière de module en mémoire. C'est en général la première chose à essayer.

Avant : le service `analytics.ts` importe directement `SubscriptionPlan` depuis `#subscriptions` pour typer un `Payload` (`SubscriptionStarted`, `SubscriptionCancelled`...) consommé par une classe `AnalyticsClient.track()`.

Après : le service `analytics.ts` expose un `AnalyticsClient` générique dont la méthode `track` accepte un `payload: Record<string, unknown>` — peu importe la forme exacte, tant qu'elle est structurellement compatible (on pourrait même utiliser un type `JSON` générique de `type-fest`). Puis, côté domaine, un `services/subscriptions/analytics.ts` définit son propre type `Payload` (spécifique aux abonnements) et une classe `SubscriptionAnalyticsClient` qui enveloppe le client générique injecté par constructeur — c'est l'option la plus flexible, puisqu'elle offre un endroit où insérer une conversion ou une logique particulière si besoin, en plus de la sécurité de typage.

Si l'on contrôle les deux côtés et qu'ils sont structurellement compatibles, on peut aussi rendre `AnalyticsClient` générique via un paramètre de type `T`, et définir côté domaine un alias `SubscriptionAnalyticsClient = AnalyticsClient<Payload>`.

Au niveau service (et non plus module), cette même approche est un peu plus lourde, car les consommateurs doivent probablement appeler un endpoint différent.

Revenons au handler de notifications monstrueux évoqué plus haut : là, de la vraie logique métier existe dans le service générique, donc on ne peut pas se contenter de l'envelopper dans un handler spécifique au domaine — il faut redistribuer la logique pour que ce soit le bon service qui en soit responsable.

Une façon de faire consiste à découper la logique en handlers d'événements séparés plutôt que d'en partager un seul : par exemple, un handler `services/tasks/notifications/eventHandler.ts` dédié, typé sur un `NotificationEvent` restreint (`TaskCommentPosted`, `TaskAttachmentCommentPosted`), qui contient la logique propre au service des tâches, puis appelle le service de notifications générique (via un `commentClient.sendComment(...)`) une fois prêt. On a mis en place un handler séparé, possédé par le service concerné. Cela ne signifie pas qu'il doive tout réimplémenter : il peut parfaitement appeler le service de notifications comme une dépendance. C'est bien un couplage à l'exécution, mais c'est précisément le type de couplage pour lequel un service générique est conçu.

Il est tentant de diffuser des événements de domaine et de laisser le service de notifications les interpréter lui-même. Mais quelqu'un doit malgré tout connaître la signification de ces événements. Si le service de notifications est censé n'être qu'un simple expéditeur générique, lui apprendre ce que sont des commentaires de tâche ou une mise en place de projet, c'est exactement la façon dont on s'est retrouvé dans ce pétrin. Il faut garder cette interprétation dans le domaine concerné, puis transmettre à l'expéditeur un message qu'il sait livrer — une idée proche de celle de « l'enveloppe », mais avec davantage de pièces mobiles.

**Solution 2 — Accepter une duplication raisonnée.** Si le problème de dépendance ne sert qu'à préserver un typage fort, on peut tout simplement accepter un peu de duplication. Un scénario où cela a vraiment du sens, et ne paraît pas « sale », consiste à laisser les consommateurs déclarer un contrat plus spécifique, fondé sur les seuls champs qui les intéressent réellement.

Le service d'email, par exemple, ne se préoccupe que d'un type générique `Email` (avec un `organizationId` et le reste en `unknown`), et expose un `EmailClient` avec `get(id)` et `send(email)`. Les consommateurs, eux, peuvent désérialiser les valeurs reçues vers un type plus spécifique : le service de commandes définit son propre schéma `OrderShippedEmail` (via `zod`, avec `organizationId`, `orderId`, `customerId`, etc.) et une fonction `getOrderShippedEmail` qui récupère l'email générique puis le valide/parse avec ce schéma précis.

Au lieu de faire remonter tous les types vers le service d'email, on laisse les consommateurs parser et valider ce qui les intéresse. C'est généralement une bonne pratique de toute façon, pour éviter le couplage entre domaines (génériques ou non), et cela facilite grandement les tests puisqu'on n'a plus à inventer des fixtures complexes juste pour satisfaire le vérificateur de types. De toute manière, les contrats entre services n'avancent jamais en parfaite synchronisation, puisque les déploiements ne sont jamais atomiques (même si les commits, eux, peuvent l'être).

On peut voir cela comme une extension du principe de ségrégation des interfaces : ne déclarer que ce dont on a besoin. En Go, c'est très courant, d'autant que les interfaces y sont implémentées implicitement — les modules ne déclarent souvent qu'un petit sous-ensemble des méthodes des types qu'on leur passe.

Beaucoup des problèmes de dépendance circulaire observés viennent d'un côté qui reçoit bien plus d'informations qu'il n'en a besoin, juste pour pouvoir réutiliser un type. Il faut toujours prendre du recul et se demander : *de quoi ce module/service/composant a-t-il réellement besoin ?*

**Solution 3 — Enregistrement de type plugin.** Dans un monolithe, une phase d'enregistrement façon plugin est une autre option intéressante, notamment quand le module générique a réellement besoin de connaître tous ses consommateurs, même sans les référencer directement dans le code.

Prenons un module d'autorisation (`authz`) comme exemple : il répond à une seule question — cet *utilisateur* peut-il effectuer cette *action* sur cette *ressource* ? Dans une version « dieu tout-puissant », `authz.ts` importe directement les types `Project` et `Document`, et contient un `switch` géant sur `resource.type` avec toute la logique d'autorisation de l'application.

On peut à la place rendre le module d'autorisation extensible : une fonction `createAuthz()` maintient une `Map` associant un type d'entité à une politique (`Policy`), expose une méthode `register(type, policy)` et une méthode `can(user, action, resource)` qui va chercher la politique correspondante dans la map. Puis, côté domaine, `projects/policy.ts` définit sa propre fonction `registerProjectPolicy(authz)` qui enregistre la politique spécifique aux projets (vérification de l'organisation, règle d'archivage, etc.).

Désormais, le module d'autorisation ne connaît plus aucune entité ni politique de domaine. Celles-ci vivent à côté du domaine qu'elles protègent, ce qui casse le cycle et constitue aussi un gain en termes de colocalisation et de découvrabilité.

Ce type d'architecture à base de plugins est très utilisé, par exemple dans le module CQRS de NestJS (dont le nom prête un peu à confusion, mais passons) : chaque module spécifique vit dans son propre domaine, mais au démarrage, il « s'enregistre » auprès du système. À la différence d'un simple appel à `register()`, la plupart de ces modules fonctionnent en parcourant l'arbre d'injection de dépendances et, via la réflexion, en extrayant les métadonnées de décorateurs des classes concernées pour construire le code d'enregistrement. Ce n'est sans doute pas un mécanisme à imiter tel quel, mais le concept reste le même : laisser la racine de l'application tout assembler, et garder l'arbre de dépendances acyclique grâce à l'enregistrement. Cela permet de définir localement, puis d'enregistrer auprès du parent, tout ce qui a réellement besoin d'être global (gestionnaires de routes HTTP, écouteurs d'événements, etc.).

Reste la question du typage. Quand on enregistre une politique dans le module des projets, comment garantir un typage fort ? En TypeScript, on peut utiliser l'« augmentation de module » (*module augmentation*) : le module générique expose une `interface` vide (volontairement), que les autres modules étendent via `declare module` (ça doit être une `interface`, pas un `type`, pour permettre la fusion de déclarations). Par exemple, `authz.ts` déclare une interface vide `AuthzResources`, et un type `Authz` dont la méthode `register` est paramétrée par les clés de cette interface. Le module `projects/policy.ts` étend ensuite `AuthzResources` via `declare module '#authz'` pour y ajouter l'entrée `Project` (avec sa ressource et ses actions possibles), et appelle `authz.register('Project', ...)` — le typage reste inféré correctement.

L'augmentation de module fonctionnerait tout aussi bien pour l'exemple du client analytics purement typé évoqué plus haut. Ce n'est toutefois pas toujours possible ou pratique : si l'on ne peut pas (ou ne veut pas) fusionner une interface globale, on peut utiliser un simple générique — faire en sorte qu'`Authz` prenne la carte des ressources en paramètre de type, chaque domaine définissant sa propre carte et déclarant `Authz<ProjectResources>` partout où il l'utilise. (Image mentale suggérée par l'auteur : imaginez que tout est un plugin jQuery, pour ceux qui se souviennent encore de cette époque.)

**La fausse bonne idée du « noyau partagé ».** Si l'on ne parle que de DTOs, on pourrait être tenté d'extraire un noyau partagé et de le partager sous forme de package, par exemple `@app/event-catalog`, qui réexporterait des centaines de types d'événements (`OrderPlaced`, `OrderCancelled`, `SubscriptionStarted`, `UserRegistered`...). Les deux côtés (service analytics, service d'abonnements) peuvent alors l'importer sans se toucher directement. Mais tout ce qu'on a fait, c'est tromper ESLint/Oxlint, car :
- l'événement ne vit nulle part près de la chose à laquelle il se rapporte ;
- on a créé un fourre-tout encore plus flagrant qu'un dossier `src/helpers` ;
- on reste tout aussi couplé conceptuellement, même sans dépendance circulaire au sens strict.

Selon la façon dont on type-check et transpile, cela peut malgré tout apporter un bénéfice de performance : le service analytics n'a plus besoin d'importer l'intégralité du service d'abonnements (ni la totalité de ses fichiers `.d.ts`, encore une fois selon les cas). Mais cela ne règle pas le problème qu'on cherche réellement à résoudre.

**Et si ce n'était pas vraiment un problème ?** Si l'on observe certains symptômes décrits ici sans avoir de véritable dépendance circulaire, c'est probablement qu'on n'aime simplement pas la façon dont les domaines ont été découpés — et ce sera sans doute difficile à corriger, pour un gain décroissant.

L'auteur cite un extrait d'un service de commentaires récemment rencontré : un schéma `CommentEntityTypeSchema` (via `zod`) énumérant les types d'entités commentables (`project`, `task`, `document`, `taskAttachment`). On voit immédiatement que ce service de commentaires va continuer à grossir, puisqu'il doit connaître tout ce qui peut recevoir un commentaire. On peut sans doute imaginer plusieurs conceptions plus génériques.

Mais tant que les services de domaine ne relisent pas les types du service de commentaires (c'est-à-dire que personne n'importe ses types en retour, et que les flèches ne pointent que dans un seul sens), y a-t-il vraiment un problème ? Pas forcément : on a simplement décidé que le service de commentaires n'est pas véritablement générique. Il faut plutôt réfléchir en termes de coût de coordination et de fréquence de changement : rendre un nouvel élément « commentable » nécessite-t-il un changement de code, un déploiement, et une coopération entre services ? Si non, peut-être que ça ne vaut pas la peine de tout repenser.

**Conclusion.** Alors, le service d'email doit-il connaître tous les emails ? Non. Le service d'email sait *envoyer* un email : destinataires, objets, corps de message. Le service `users` sait ce que dit un email de bienvenue, et le service de commandes sait ce que contient une confirmation de commande. Idéalement, les flèches ne doivent pointer que dans un seul sens.

Protégez vos services « génériques ». Ne laissez entrer aucune logique métier qui ne parle pas le langage de leur propre contexte délimité (*bounded context*) : les notifications doivent connaître les emails, pas les projets.

Ou alors, admettez que le service n'était en réalité jamais vraiment générique, et laissez-le posséder son domaine à part entière. Si l'on ouvre les vannes, la théorie des vitres brisées (*broken windows theory*) prendra le dessus, et on se retrouvera avec un enchevêtrement de code indigeste.

## Pourquoi ça compte
Ce pattern de dépendance circulaire touche quasiment toutes les équipes qui construisent des services « transverses » (analytics, notifications, autorisation) dans un monolithe modulaire ou une architecture microservices ; les solutions proposées (adaptateurs, enregistrement par plugin, augmentation de module TypeScript) sont directement actionnables pour prévenir la dette technique avant qu'elle ne s'installe.
