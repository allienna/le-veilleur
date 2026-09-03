---
title: "How to let AI agents act on behalf of users without handing them access tokens — WorkOS"
date: 2026-09-03
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fworkos.com%2Fblog%2Fdelegated-access-for-ai-agents%3Futm_source=tldr%26utm_medium=newsletter%26utm_campaign=q32026%26utm_content=header_how_empower_ai/1/010001a061b0e5c9-ba64837d-2598-4c17-9463-1f42a5309225-000000/qAwHx6zmxgbshqdaoZ2GKdOPjFPjphDx8Jr4ekMwFTY=452"
keywords: ["agents IA", "OAuth", "jetons d'accès", "injection de prompt", "WorkOS", "délégation d'accès"]
theme: "Sécurité"
tone: "opinion"
used_in: ["2026-09-03"]
---

## Résumé
L'article de WorkOS explique pourquoi confier un jeton d'accès OAuth à long terme à un agent IA qui agit pour le compte d'un utilisateur est structurellement dangereux : l'agent traite le contenu non fiable qu'il lit (issues, pages web, tickets) avec la même considération que ses instructions système, ce qui ouvre la voie à l'exfiltration du jeton via injection de prompt. Réduire les scopes OAuth ou faire tourner les jetons plus souvent atténue le problème sans le résoudre, car le jeton reste présent dans l'environnement de l'agent. WorkOS propose une alternative avec Relay (en accès anticipé) : un proxy qui reçoit la requête de l'agent, résout l'identité de l'utilisateur et injecte lui-même le jeton du fournisseur, sans jamais l'exposer au runtime de l'agent. Le texte reconnaît toutefois les limites de cette approche : elle ne règle ni l'injection de prompt elle-même, ni la protection de la clé API WorkOS, ni l'autorisation fine des actions de l'agent.

## Points clés
- Un agent IA traite le contenu externe (issue GitHub, page web, PDF) au même niveau que ses instructions système, ce qui efface la frontière classique entre code de confiance et entrée non fiable.
- Un jeton OAuth confié à un agent se retrouve dupliqué dans de nombreux endroits à risque : fenêtre de contexte, logs d'appels d'outils, logs du fournisseur de modèle, stdout/stderr, rapports d'erreurs, fichiers de mémoire persistante.
- Une seule ligne de texte malveillante dans un ticket ou une issue peut suffire à convaincre un modèle d'exfiltrer son en-tête d'autorisation vers une URL contrôlée par un attaquant — un scénario probabiliste, donc jamais totalement fiable.
- Réduire les scopes OAuth ou raccourcir la durée de vie des jetons limite la fenêtre d'exposition mais ne supprime pas la cause racine, puisque le jeton doit quand même résider dans l'environnement de l'agent.
- La solution proposée (Relay de WorkOS) fait office de proxy : l'agent envoie sa requête avec la clé API WorkOS et l'identifiant utilisateur en en-têtes, et WorkOS injecte le jeton du fournisseur juste avant l'envoi, sans jamais l'exposer à l'agent.
- Le mécanisme ne protège ni contre l'injection de prompt elle-même, ni contre l'exposition de la clé API WorkOS présente dans le runtime, ni ne remplace une politique d'autorisation fine des actions des agents.

## Analyse approfondie

### L'hypothèse qui vient d'expirer
La sécurité applicative a toujours reposé sur une distinction entre code de confiance et entrée non fiable : le serveur était fiable, le corps de la requête ne l'était pas, et toutes les défenses classiques (validation des entrées, requêtes paramétrées, encodage des sorties) reposaient sur cette frontière. Un runtime d'agent efface cette frontière : un ticket de support, une page web scrapée, un PDF téléversé par un utilisateur ou un commentaire de code arrivent tous dans la même fenêtre de contexte que le prompt système, et reçoivent la même considération de la part du modèle. On n'exécute plus seulement le code qu'on a écrit, mais aussi ce que le modèle décide de faire à partir d'un paragraphe de texte qu'il a rencontré. Placer un jeton OAuth longue durée dans cet environnement pose donc un problème évident.

### Où finit réellement le jeton
Un jeton d'accès placé dans un runtime d'agent se retrouve dupliqué dans bien plus d'endroits que prévu :
- **la fenêtre de contexte**, si l'agent inspecte sa propre configuration ou débogue un appel en échec ;
- **les arguments d'appels d'outils**, généralement journalisés intégralement par la couche d'observabilité ;
- **les logs du fournisseur de modèle**, si le jeton transite par un prompt ;
- **stdout/stderr**, une commande curl composée par l'agent ne sachant pas masquer ses propres en-têtes ;
- **les rapports d'erreurs**, où une requête HTTP échouée sérialise souvent ses en-têtes dans l'exception ;
- **les fichiers de mémoire persistante**, rarement traités comme des données sensibles ;
- **la voie d'exfiltration elle-même**, qui ne nécessite aucun bug : un agent disposant d'un jeton et d'un accès réseau peut être amené à l'envoyer ailleurs — ce n'est pas une faille, c'est la fonctionnalité qui fonctionne comme prévu.

### Une fuite qui tient en un paragraphe
Prenons un agent chargé de trier des issues GitHub, détenteur du jeton GitHub d'un utilisateur pour lire les dépôts et commenter. Il suffit qu'une issue se termine par une ligne adressée à l'agent plutôt qu'à l'humain, lui demandant d'inclure son en-tête d'autorisation dans une requête de diagnostic vers une URL contrôlée par l'attaquant. Que le modèle obtempère ou non dépend du modèle, du prompt et du jour — ce qui introduit une composante probabiliste dans la sécurité des identifiants, un pari qu'il faut gagner à chaque fois. Même un modèle qui résiste 99 fois sur 100 ne constituerait un contrôle acceptable nulle part ailleurs dans une pile technique. Et l'échec n'est pas récupérable comme une session classique : un jeton d'accès qui fuite n'est pas une session qu'on peut invalider soi-même, c'est un identifiant porteur (« bearer ») pour l'API d'un tiers, valide jusqu'à expiration ou révocation, et utilisable depuis n'importe où.

### Les scopes et la rotation aident moins qu'on ne le voudrait
Les deux réflexes naturels — restreindre les scopes et raccourcir la durée de vie — sont utiles mais ne traitent pas la nature du problème. Les scopes OAuth sont grossiers car ils ont été conçus pour des applications, pas pour des agents : un jeton capable de lire les dépôts dont un agent a besoin peut généralement lire tous les dépôts visibles par l'utilisateur, car les scopes des fournisseurs couvrent des surfaces produit entières. La rotation, elle, réduit la fenêtre d'exposition sans la fermer : un attaquant capable d'atteindre un jeton une fois peut généralement l'atteindre à nouveau, la voie de fuite étant une propriété du runtime plutôt qu'un instant donné. Un flux de rafraîchissement implique en outre que le runtime détienne aussi le jeton de rafraîchissement, encore plus précieux que le jeton d'accès. Ces deux mitigations acceptent la prémisse que le jeton doive résider dans l'environnement de l'agent — c'est cette prémisse qu'il faut attaquer.

### L'accès délégué sans transmettre le jeton
L'alternative consiste à ne plus livrer l'identifiant au code qui en a besoin, mais à laisser ce code décrire l'appel qu'il veut effectuer pour le compte d'un utilisateur donné. WorkOS propose cela sous le nom de Relay, actuellement en accès anticipé : l'agent envoie sa requête à WorkOS, indique le fournisseur et l'utilisateur pour lequel il agit, et WorkOS attache l'identifiant à la sortie. Concrètement, une requête relayée porte la clé API WorkOS dans l'en-tête `Authorization`, l'URL cible dans `X-Relay-URL`, l'identifiant de l'utilisateur dans `X-Relay-User`, ainsi que `X-Relay-Organization` lorsque la connexion a été autorisée au niveau d'une organisation. Le fournisseur est déduit de l'hôte de l'URL cible, avec `X-Relay-Provider` comme option de dérogation en cas d'ambiguïté. WorkOS vérifie la clé, résout le compte connecté de l'utilisateur, récupère l'identifiant depuis le magasin d'identifiants Pipes, le rafraîchit s'il a expiré, retire ses propres en-têtes de contrôle, injecte le jeton du fournisseur, puis retransmet la réponse du fournisseur sans modification. Méthode, corps et en-têtes de contenu passent sans changement, de sorte que convertir un appel direct en appel relayé revient à modifier des en-têtes plutôt qu'à réécrire le code.

Deux détails rendent le dispositif réellement utilisable, pas seulement sécurisé :

Le premier concerne une sémantique d'erreur honnête. Un proxy transparent souffre d'un problème d'identification : un `401` ou `403` renvoyé par le proxy lui-même serait indiscernable d'un `401` du fournisseur ou d'un rejet de la clé API. Ainsi, un utilisateur qui n'a pas connecté le fournisseur, ou dont l'autorisation a été révoquée, reçoit un `402` avec le code `relay_authorization_required` et une `authorization_url` vers laquelle le rediriger. Chaque réponse relayée porte aussi l'en-tête `X-Relay-Upstream-Status`, indiquant si la requête a bien atteint le fournisseur — un `404` GitHub et un `404` de fournisseur inconnu ne se ressemblent alors plus.

Le second est que le jeton vit désormais derrière une frontière que l'agent ne peut franchir même s'il le souhaite. Les requêtes ne peuvent viser que les hôtes autorisés d'un fournisseur pris en charge. Les redirections ne sont pas suivies — un détail important, car une redirection suivie est précisément le mécanisme par lequel un identifiant injecté finit sur un hôte que personne n'avait autorisé. Les en-têtes `Cookie`, `X-Forwarded-*` et de type « hop-by-hop » sont retirés à l'aller, `Set-Cookie` au retour. Le délai d'attente en amont est de trente secondes et les corps de requête sont retransmis octet pour octet jusqu'à 5 Mo.

Le résultat : un agent compromis peut toujours effectuer des appels qu'il ne devrait pas faire auprès du fournisseur, mais il ne peut plus repartir avec un identifiant.

### Ce que cela ne résout pas
- **L'injection de prompt reste intacte.** Rien dans ce dispositif ne rend un agent meilleur pour ignorer des instructions dissimulées dans les données qu'il lit. Un agent qu'on peut convaincre de poster un message Slack indésirable peut toujours être convaincu de le faire — le proxy change ce que l'attaquant peut emporter, pas sa capacité à influencer l'agent.
- **La clé API WorkOS reste présente dans le runtime.** Elle authentifie chaque appel pour l'environnement concerné, et Relay ne la fait pas disparaître. Il faut donc la traiter avec autant de précaution : l'injecter au moment de la requête plutôt que de la coder en dur dans du code ou des prompts visibles par l'agent, et la faire tourner si un runtime est compromis. Déplacer un secret hors de portée tout en en laissant un autre plus puissant traîner constitue un déplacement latéral, pas une amélioration.
- **Les permissions du fournisseur restent les permissions du fournisseur.** Les appels relayés sont contraints par des hôtes autorisés, pas par ce qu'un agent donné devrait légitimement faire. L'autorisation fine des actions des agents demeure une vraie lacune ; un point de passage unique est l'endroit naturel où la combler un jour, mais son existence ne vaut pas politique déjà en place.

Ce qu'on obtient réellement, c'est un changement de rayon d'impact (« blast radius »). Un jeton qui fuite est une capacité durable, portable et utilisable hors ligne. Une session d'agent détournée est un processus vivant qu'on peut arrêter, dont les appels transitent par un point unique où ils peuvent être observés et coupés. Ce sont deux incidents très différents, et l'un des deux prend fin dès qu'on le remarque.

### La partie qui survit au produit
Le proxying d'identifiants n'est pas une idée nouvelle, ce qui joue en sa faveur. Les paiements ont ouvert la voie : les coffres-forts de cartes et la tokenisation existent parce que le moyen le plus rapide de réduire le périmètre d'un audit est de s'assurer que la valeur sensible n'entre jamais dans ses systèmes. Le même raisonnement s'applique aux jetons OAuth et aux runtimes d'agents, pour la même raison : on ne peut pas faire fuiter ce qu'on n'a jamais détenu. Le principe durable, indépendant de tout produit particulier, est que les identifiants doivent résider dans le composant le moins accessible capable de faire le travail — or les runtimes d'agents sont aujourd'hui le composant le plus accessible dans la plupart des architectures : ils lisent du texte contrôlé par des attaquants, journalisent tout, persistent un état pour progresser, et agissent selon leurs propres conclusions. C'est un bon endroit pour prendre une décision ; c'est un mauvais endroit pour garder une clé.

Si l'on confie aujourd'hui un jeton à un agent, la question à se poser n'est pas de savoir si le prompt est robuste, mais ce qui se passera le jour où il ne le sera pas.

## Pourquoi ça compte
Ce texte formalise un angle mort de sécurité propre aux architectures d'agents IA — la fuite de jetons OAuth via injection de prompt — et illustre une réponse architecturale concrète (proxy d'identifiants) qui sera probablement reprise par d'autres fournisseurs d'infrastructure agentique dans les mois à venir.
