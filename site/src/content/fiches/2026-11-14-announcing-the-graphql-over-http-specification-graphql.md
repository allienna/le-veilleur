---
title: "Announcing the GraphQL over HTTP specification | GraphQL"
date: 2026-11-14
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fgraphql.org%2Fblog%2F2026-11-12-announcing-the-graphql-over-http-spec%3Futm_source=tldrdev/1/010001a1d4d6d4f1-3f79bd2d-3bd3-45e7-9808-ba3d194e24a0-000000/qPvYaEjnHk5ak0YahHOEpVI6FmD3nuq9I7Iz4ubHy18=452"
keywords: ["GraphQL", "HTTP", "spécification", "API", "statuts HTTP"]
theme: "Software"
tone: "news"
used_in: ["2026-11-14"]
---

## Résumé
Le projet GraphQL publie officiellement sa première spécification « GraphQL over HTTP », qui vient compléter la spécification principale restée volontairement agnostique au transport depuis 2015. Elle introduit notamment un nouveau type de média `application/graphql-response+json` permettant de distinguer une réponse GraphQL valide d'une erreur réseau, mettant fin au fameux problème du « 200 Not OK ». Le document codifie aussi les pratiques existantes (URL, GET, POST, encodage JSON, en-têtes) et ouvre la voie à de futures évolutions comme le verbe HTTP QUERY, les documents persistés standardisés et le batching de requêtes.

## Points clés
- Première spécification « GraphQL over HTTP », document complémentaire à la spécification GraphQL qui reste transport-agnostique.
- Nouveau type de média `application/graphql-response+json` pour fiabiliser la distinction entre réponses GraphQL authentiques et erreurs d'intermédiaires réseau (proxy, cache).
- Règle générale : code `2xx` si des données sont renvoyées, `4xx`/`5xx` si seules des erreurs sont renvoyées (avec des exemples précis : 405, 406, 415, 431, 500).
- Introduction d'un nouveau code de statut `294 Partial Success` pour les réponses contenant à la fois `data` et `errors`.
- La plupart des frameworks et bibliothèques GraphQL supportent déjà cette spécification sans que les utilisateurs en aient conscience.
- Prochaines pistes de standardisation : le verbe HTTP `QUERY` (récemment adopté comme standard proposé par l'IETF), les « persisted documents », et le batching de requêtes (utile notamment pour les schémas composites / Federation).

## Analyse approfondie
Depuis la sortie initiale de GraphQL en 2015, la spécification GraphQL a toujours été agnostique au transport.

L'essentiel de la spécification GraphQL porte sur les « services » : ils reçoivent des « requêtes », les exécutent, et produisent des « réponses ». La manière dont ces requêtes et réponses sont envoyées et reçues est laissée à la discrétion de l'implémenteur.

C'est globalement un avantage : on peut utiliser GraphQL sur sa machine locale, sur TCP brut, par pigeon voyageur, ou par tout autre moyen. Mais pour la large communauté qui utilise GraphQL par-dessus HTTP, l'absence de spécification rendait l'interopérabilité avec les autres outils HTTP et l'observabilité plus difficiles qu'elles ne devraient l'être.

Cela change aujourd'hui avec la première publication de la spécification GraphQL over HTTP !

La spécification GraphQL demeure agnostique au transport ; la spécification GraphQL over HTTP est un nouveau document, complémentaire à la spécification principale.

Si vous utilisez GraphQL par-dessus HTTP, suivez les recommandations de cette spécification et assurez-vous que vos serveurs, clients, proxys et autres services fonctionnent bien ensemble.

La spécification GraphQL over HTTP introduit un nouveau type de média `application/graphql-response+json`.

Auparavant, de nombreux serveurs GraphQL utilisaient `application/json` pour leurs réponses. Cela rendait difficile, pour les clients, la distinction entre une réponse GraphQL bien formée provenant du serveur d'origine et une réponse d'erreur provenant d'un proxy, d'un cache ou d'un autre intermédiaire réseau.

Comme solution de contournement, la plupart des implémentations fixaient le code de statut à `200` : si un client recevait un code `200`, il savait que la réponse n'avait pas été altérée et qu'il pouvait la parser en toute sécurité comme une réponse GraphQL.

Ce n'est pas idéal du point de vue de l'observabilité, et cela a donné lieu à des blagues sur le « 200 Not OK ». Il est difficile de connaître le statut de son service quand tout est un 200...

C'est désormais corrigé !

Lorsqu'un client reçoit un corps au format `application/graphql-response+json`, il sait qu'il peut le parser comme une réponse GraphQL over HTTP bien formée, quel que soit le code de statut.

La règle générale est la suivante :

- Si la requête a renvoyé des données, renvoyer un code de statut `2xx`.
- Si la requête n'a renvoyé que des erreurs, renvoyer un code `4xx` ou `5xx`.

La spécification fournit des recommandations détaillées sur les codes de statut à utiliser, mais les implémenteurs peuvent choisir un code alternatif si celui-ci correspond mieux à la situation, tant qu'il reste cohérent avec la règle générale. Les codes de statut courants incluent :

- 405 lors d'une tentative de mutation via GET
- 406 lors d'une requête avec un type de média non supporté
- 415 lors de la fourniture d'un type de média non supporté
- 431 lorsque les en-têtes sont excessivement volumineux
- 500 lorsqu'une erreur serveur se produit

Une réponse réussie ressemblerait à ceci :

```
HTTP/1.1 200 OK
Content-Type: application/graphql-response+json
...
{
  "data": {
    "hello": "world"
  }
}
```

Une erreur de requête ressemblerait à ceci :

```
HTTP/1.1 422 Unprocessable Content
Content-Type: application/graphql-response+json
...
{
  "errors": [{
    "message": "Cannot query field 'foo' on type 'Query'."
  }]
}
```

La spécification introduit également un nouveau code de statut `294 Partial Success`, utilisé lorsque `data` et `errors` sont tous deux présents ; vous pouvez en apprendre davantage sur le 294 Partial Success dans les notes non normatives.

Mis à part les soucis liés au « 200 Not OK », beaucoup de choses ont très bien fonctionné pour GraphQL over HTTP au cours de la dernière décennie.

Cette spécification documente tous ces aspects :

- URL
- Requêtes GET
- Requêtes POST
- Encodage JSON
- En-têtes
- et plus encore

Elle inclut également des notes non normatives sur la sécurité, le succès partiel, et la compatibilité future.

Ce n'est que le début !

L'IETF vient de faire passer le verbe HTTP `QUERY` au statut de standard proposé.

`QUERY` correspond parfaitement à GraphQL, et nous avons déjà prévu de le supporter. Nous ne voulions ni repousser cette première publication ni précipiter l'implémentation, mais nous espérons l'inclure dans la prochaine révision de la spécification GraphQL over HTTP.

Un autre élément qui bénéficiera de la standardisation est celui des documents persistés (« persisted documents »). La technique consistant à persister des documents GraphQL (« persisted queries ») est utilisée depuis avant même l'open source de GraphQL en 2015, avec différentes implémentations résolvant différents problèmes : performance, sécurité, observabilité. Nous sommes impatients de travailler avec la communauté pour construire une approche standard capable de résoudre tous ces problèmes tout en conservant une extensibilité future.

Enfin, le batching de requêtes représentera un gain important, en particulier dans le contexte des schémas composites (Federation) ou lorsqu'on effectue des requêtes vers des schémas que l'on ne contrôle pas.

Si vous êtes un utilisateur de GraphQL, il y a de fortes chances que vous utilisiez déjà la nouvelle spécification sans le savoir ! La plupart des frameworks et bibliothèques GraphQL existants supportent déjà la nouvelle spécification.

Si vous êtes auteur d'une bibliothèque, essayez la nouvelle spécification !

Dans tous les cas, faites-nous savoir ce que vous en pensez !

## Pourquoi ça compte
Cette spécification officialise des années de pratiques empiriques autour de GraphQL over HTTP et résout un vrai problème d'observabilité (le « 200 Not OK ») ; les équipes qui opèrent des API GraphQL en production devraient surveiller l'adoption de `application/graphql-response+json` et des codes de statut associés dans leurs frameworks, proxys et outils de monitoring.
