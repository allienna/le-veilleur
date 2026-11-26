---
title: "Probing DNS at Cloudflare"
date: 2026-11-26
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fblog.cloudflare.com%2Fprobing-dns-at-cloudflare%3Futm_source=tldrit/1/010001a212ddd499-afd90a86-4924-4b82-8925-625ff46c572e-000000/XtvEPJ4Ymf1zLo_9Qc3wLtK1HImKAa0gSjk1wtypcaw=452"
keywords: ["DNS", "Cloudflare", "tests end-to-end", "fiabilité", "SLO", "Rust"]
theme: "Software"
tone: "news"
used_in: ["2026-11-26"]
---

## Résumé
Cloudflare raconte comment son équipe DNS a été confrontée à un bug de planification ayant retardé pendant des heures la publication de changements d'enregistrements DNS, sans que les dashboards classiques ne détectent le problème. Pour y remédier, l'équipe a étendu Flamingo, son framework de tests end-to-end déjà utilisé pour exécuter des centaines de millions de tests par jour sur l'edge de Cloudflare, afin qu'il puisse aussi sonder le DNS en production, depuis chaque datacenter. Ces mesures de propagation DNS alimentent désormais des SLO qui décident automatiquement si un déploiement se poursuit ou doit être annulé. L'article décrit l'architecture modulaire de Flamingo (écrit en Rust), son DSL de test, et la manière dont ce système permet de détecter des régressions DNS avant qu'elles n'affectent l'ensemble d'Internet.

## Points clés
- Un bug de planification a laissé des changements DNS non publiés pendant des heures malgré un service "healthy" et des tests unitaires verts, illustrant les limites du monitoring classique face au DNS.
- Flamingo est un framework de tests end-to-end interne à Cloudflare, écrit en Rust, conçu pour tourner à grande échelle sur du bare-metal et cibler précisément des environnements, datacenters ou pourcentages de machines.
- Son architecture modulaire repose sur un DSL dédié (setup-request-response) qui isole le débogage du test de celui du système testé, et permet d'ajouter facilement de nouveaux protocoles (HTTP, puis DNS, TCP, UDP, WebSockets...).
- Le module DNS met à jour en continu un enregistrement TXT horodaté et interroge trois serveurs de noms faisant autorité ainsi que le résolveur public 1.1.1.1 depuis chaque datacenter, en vérifiant une fraîcheur inférieure à 90s (autoritaire) et 600s (résolveur).
- Ces mesures nourrissent des SLO/SLI classiques (error budget, burn rate) qui permettent de décider automatiquement de promouvoir ou de rollback un déploiement.
- Le système permet désormais de stopper automatiquement un rollout dès qu'un pic de latence de propagation DNS est détecté dans un datacenter canari, avant impact généralisé.

## Analyse approfondie
Imaginez la scène : vous venez de pousser une release. Tous les tests unitaires sont passés et vos dashboards sont au vert. Vous vous détendez, puis soudain votre téléphone s'affole : la prod est cassée.

C'est une situation que l'équipe DNS de Cloudflare a vécue de première main. Lors d'un déploiement du service qui publie les enregistrements DNS vers leur edge, un bug de planification a laissé certains changements d'enregistrements non publiés pendant des heures. Le service restait up et sain, mais les nouveaux noms d'hôtes étaient lents à résoudre et les certificats ne pouvaient pas être émis jusqu'à ce que le bug soit corrigé.

Les pannes DNS sont difficiles à détecter car elles sont lentes, réparties sur l'ensemble du réseau, et partielles dans leur impact. Il fallait trouver un moyen de tester le DNS comme les clients le vivent réellement : en continu, depuis chaque datacenter, et contre la production.

La réponse a été d'étendre Flamingo, le framework de tests end-to-end déjà utilisé pour exécuter des centaines de millions de tests par jour contre l'edge de Cloudflare. Cet article explique comment la conception modulaire de Flamingo permet d'y ajouter le support du DNS, comment la propagation est mesurée, et comment ces mesures décident désormais si une release est poursuivie ou annulée.

### Un peu de contexte

Chez Cloudflare, l'obsession est d'améliorer la performance et la sécurité pour les clients. Il est crucial que le code soit testé en permanence, à grande échelle et contre le véritable edge Cloudflare dans lequel les utilisateurs opèrent. C'est une des raisons pour lesquelles l'outil Flamingo a été créé : mesurer le comportement des environnements de production et s'assurer que le code dans les environnements de niveau inférieur se comporte comme prévu.

Cloudflare a déjà écrit sur la manière dont cet outil a été utilisé dans les mises à niveau de leur stack CDN. Cependant, cela ne représente qu'une petite partie de l'usage interne de Flamingo. Une des caractéristiques de Flamingo est son architecture modulaire qui permet aux équipes d'étendre les capacités de l'outil pour parler d'autres protocoles réseau. Dans ce cas précis, l'équipe DNS a voulu utiliser ces capacités modulaires pour tester le DNS.

### Qu'est-ce que Flamingo ?

Tester est difficile. Tester à grande échelle, sur un système largement distribué, l'est encore plus. Il existe de nombreux chemins complexes que les requêtes traversent, et de multiples systèmes que chaque requête réseau doit parcourir avant d'atteindre l'origine. Les tests unitaires seuls ne suffisent pas. Il faut exécuter des tests automatisés en continu contre de vrais systèmes et mesurer les résultats de ces requêtes pour prendre des décisions informées sur la santé d'un service.

C'est là qu'intervient Flamingo. Conçu à l'origine autour de tests HTTP multi-étapes complexes, ses capacités et sa portée ont considérablement augmenté au fil des années. Flamingo a été construit en pensant à l'infrastructure de Cloudflare dès le départ. Un plan de contrôle et un planificateur ont été construits pour permettre aux équipes de cibler des environnements spécifiques, des datacenters, ou des pourcentages de métal. Il fallait aussi s'intégrer avec des outils de reporting, de métriques et d'analytics personnalisés. De plus, l'outil devait offrir des performances prévisibles et bien fonctionner sur des serveurs bare-metal dans des environnements aux ressources contraintes.

#### Être agréable à utiliser

Lorsque Cloudflare construit des outils internes comme celui-ci, l'objectif est de créer une expérience développeur agréable. Les outils internes doivent être aussi simples d'utilisation que possible, mais aussi suffisamment puissants pour couvrir plus de 80% de tous les cas d'usage. Et pour qu'un nouveau framework de tests d'acceptation sur l'edge réussisse, il doit être construit de manière à forcer les équipes à suivre des directives communes et à construire des scripts réutilisables dans un environnement stable, scalable, et qui gère la complexité.

Une chose qui n'est pas agréable, c'est de déboguer un test. Si l'on permet à un utilisateur d'écrire des tests dans un langage de programmation classique, lorsque son test échoue, il doit à la fois déboguer le système en amont testé **et** le test lui-même. C'est pourquoi Flamingo a été conçu pour utiliser un langage spécifique au domaine (DSL) personnalisé, consistant en un format simple de type setup-request-response.

Par exemple, imaginons que l'on veuille s'assurer que tout le trafic non chiffré est redirigé vers son équivalent chiffré.

```
TEST test-redirect
SET $hostname www.cloudflare.com
GET "http://$(hostname)/"
ASSERT STATUS IS 301
ASSERT HEADER Location IS "https://$(hostname)/"
```

On voit ici la puissance du DSL. En cinq lignes de code, on obtient un script qui peut tourner n'importe où sur l'edge de Cloudflare et monter en charge jusqu'à des milliers de requêtes par minute. Les données produites à partir des millions de points de données générés peuvent être transformées en un graphique définissant comment le service se comporte réellement dans le monde réel.

En reprenant le format de test setup-request-response ci-dessus et en le modifiant légèrement, Flamingo peut être utilisé pour bien plus que des tests HTTP. Au lieu que l'étape intermédiaire soit une requête, on peut désormais la considérer comme une **action**. Le système est ainsi passé de quelque chose qui fait des requêtes HTTP à quelque chose qui peut exécuter n'importe quelle action dont on souhaite mesurer le résultat.

Dans Flamingo, ces briques sont appelées des **modules**, et un effort considérable a été mis pour qu'elles soient aussi simples que possible à écrire pour n'importe qui. Flamingo est écrit en Rust, pour ses caractéristiques de performance constantes et son système de typage fort. Le système de typage se prête particulièrement bien à cette modularité, en permettant d'utiliser des énumérations fortement typées en entrée et en sortie dans le moteur d'exécution d'actions de Flamingo :

```
pub enum Action {
  Query {
    method: String,
    url: Expression,
    parameters: Vec<http::QueryParameters>,
  },
  DnsQuery {
    query_name: Expression,
    query_type: Expression,
    parameters: Vec<dns::DnsQueryParameters>,
  },
}
pub enum ActionOutput {
  Http(http::FetchResponse),
  Dns(dns::QueryResponse),
}
pub type ActionHandlerFunction = Arc<
  dyn Fn(
      Action,
      Arc<Ctx>,
      InterpreterConfig,
    )
      -> BoxFuture<'static, Result<ActionOutput>>
    + Send
    + Sync
    + 'static,
>;
pub type ActionHandlerLUT = Arc<
  dyn Fn(&Action) -> ActionHandlerFunction
    + Send
    + Sync
    + 'static,
>;
```

Ce qui est fait ici, c'est découpler la logique d'exécution d'une action (dans ce cas une requête HTTP) dans une fonction à répartition dynamique (dynamically dispatched) que l'on peut ensuite appeler indépendamment des autres actions. Cela laisse des opérations de plus haut niveau, comme la planification des tests et la gestion des ressources, à la charge du framework, sans que la personne qui implémente un module n'ait à s'en soucier. Tout ce dont l'auteur doit se préoccuper, c'est la logique.

```
pub async fn query(
  action: Action,
  ctx: Arc<Ctx>,
  cfg: InterpreterConfig,
) -> Result<ActionOutput> {
  let Action::Query {
    method,
    url,
    parameters,
  } = action
  else {
    bail!("Invalid action for module-http::query: {action:?}");
  };
  ...
}
pub async fn execute_module<F>(
  ctx: Arc<Ctx>,
  cfg: &InterpreterConfig,
  handler_lut: F,
) -> Result<ActionOutput>
where
  F: (Fn(&Action) -> ActionHandlerFunction),
{
  let func = handler_lut(action);
  let action_out = (func)(action.clone(), ctx.clone(), cfg.clone()).await?;
  ...
}
```

### Utiliser Flamingo pour sonder le DNS

L'adage dit que lorsque des problèmes surviennent, "c'est toujours le DNS". Comme beaucoup de blagues, il y a toujours un fond de vérité derrière. Le DNS est une pièce incroyablement importante d'Internet, et comme il repose sur un réseau complexe de sources de vérité interconnectées, il peut suffire d'un seul faux pas pour provoquer une tempête de pannes.

Le DNS peut être un système particulièrement capricieux en raison de sa nature hiérarchique. Lorsqu'on change un enregistrement DNS pour une zone Cloudflare, par exemple, cet enregistrement doit être propagé vers les serveurs faisant autorité de sorte que l'enregistrement mis à jour devienne largement disponible. Pour réduire la latence, les enregistrements sont stockés dans des caches physiquement plus proches. Ces enregistrements ont une durée de vie (TTL) associée qui indique au cache DNS local combien de temps attendre avant de devoir récupérer à nouveau cet enregistrement depuis le serveur faisant autorité. Tout délai aura un impact sur des opérations sensibles au temps comme l'émission de certificats ou le basculement de trafic (failover).

Il a déjà été mentionné que Flamingo a été conçu pour être extensible. Un des premiers modules les plus impactants déployés à ce jour a été construit spécifiquement pour ce cas d'usage. L'équipe a pu ajouter du code qui étend Flamingo de sorte qu'au lieu d'envoyer des requêtes HTTP, il envoie des requêtes DNS. En procédant ainsi, tout le reste a été obtenu gratuitement : pas besoin pour l'équipe DNS de se soucier de gérer un nouveau service de sondage, pas besoin de s'intégrer avec les pipelines de reporting. Tout a simplement fonctionné.

Pour sonder le DNS, l'équipe mesure la vitesse à laquelle les changements d'enregistrements des clients se propagent vers les serveurs de noms faisant autorité et vers le résolveur public (1.1.1.1). Le test met à jour en continu un enregistrement TXT avec un horodatage et interroge trois adresses IP de serveurs de noms faisant autorité ainsi que 1.1.1.1 depuis chaque datacenter, en vérifiant une fraîcheur inférieure à 90 secondes (autoritaire) et 600 secondes (résolveur).

```
TEST test-propagation-delay-direct-108-162-193-62
MOD dns
SET $hostname "some.probe.domain"
SET $authNs 108.162.193.62:53 # amir.ns.cloudflare.com
QUERY $hostname TXT
TARGET $authNs
ASSERT DNS.RCODE IS NOERROR
ASSERT DNS.FLAGS CONTAINS AA
ASSERT DNS.ANSWERS[0] GT SUBTRACT(TIMESTAMP(), "90")
```

### Attraper les bugs (SLO et stabilité)

Pour s'assurer que les nombreux systèmes fonctionnent conformément aux attentes, des objectifs de niveau de service (SLO) sont définis pour observer des éléments comme la disponibilité ou la latence. Les SLO sont un pourcentage d'une métrique utilisée comme cible. De plus, les SLO sont mesurés via des indicateurs de niveau de service (SLI), qui sont la série réelle de mesures centrées sur l'expérience de bout en bout vécue par un utilisateur interagissant avec un système.

En envoyant en continu du trafic synthétique Flamingo à travers les systèmes de production, on peut commencer à utiliser cette information pour se construire une image de ce que les utilisateurs finaux vivent réellement — et fournir ces données pour les SLO. Lorsque ce trafic synthétique rencontre des problèmes, on peut être relativement confiant que les clients de Cloudflare rencontrent eux aussi des problèmes, et agir en conséquence (triage).

Une fois cette information disponible, elle permet de prendre des décisions informées lors du déploiement d'un service. Les SLO fonctionnent en termes de budgets d'erreur (error budget) et de taux de consommation (burn rate). Un budget d'erreur est le pourcentage d'indisponibilité qu'un service est prêt à tolérer, tandis que le burn rate est le taux de variation de ce budget à un instant donné. Cela permet à un système automatisé de comprendre la sévérité d'un problème. Par exemple, consommer 10% de son budget d'erreur sur une période de trois jours peut correspondre à un problème de longue durée qui, bien que non urgent, affecte les clients et doit être traité. Mais si 10% du budget d'erreur est consommé en une heure, cela signifie qu'un incident est en cours et que l'impact client sera substantiel si ce n'est pas corrigé immédiatement.

En utilisant ces chiffres, il est possible de surveiller les SLO pendant le déploiement et de prendre des décisions informées sur la santé d'un service. Sur la base de cette information, les systèmes de déploiement peuvent être instruits soit de promouvoir un changement, soit de l'annuler (rollback).

### La suite

En déplaçant le monitoring DNS vers Flamingo, un système a été créé qui peut détecter de manière proactive les problèmes DNS avant qu'ils n'aient la chance de se propager au reste de l'edge de Cloudflare. Si Flamingo détecte un pic de latence de propagation dans un datacenter canari spécifique, il est possible de stopper automatiquement le déploiement d'une nouvelle version logicielle avant qu'elle n'affecte le reste d'Internet.

Le DNS n'est que le début de l'extension de Flamingo. Il existe actuellement des modules pour tester TCP, UDP, WebSockets, et plusieurs autres. Disposer d'un outil permettant de tester et surveiller rapidement des services a permis aux équipes de déployer des changements importants en toute sécurité, sans qu'un humain ait besoin de surveiller constamment.

Si ce type d'ingénierie de fiabilité intéresse le lecteur, Cloudflare invite à consulter sa page carrières pour les postes ouverts.

## Pourquoi ça compte
Cet article illustre une approche concrète et transférable de test d'infrastructure en production — étendre un framework de tests existant plutôt que construire un outil dédié — pour fiabiliser un composant aussi critique et discret que le DNS, avec un couplage direct aux décisions de déploiement via les SLO.
