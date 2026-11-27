---
title: "Unclean leader election: Kafka trolley problem where you always end up pulling the lever"
date: 2026-11-27
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Faiven.io%2Fblog%2Fkafka-unclean-leader-election%3Futm_source=tldrdata/1/010001a2179059ef-e1ae25d1-8e68-4cca-ab66-399726024991-000000/cxA0D-3YzQAAOHw5EkgUqbDB6GY_GaJL-6HrjkGr_xo=452"
keywords: ["Kafka", "haute disponibilité", "cohérence des données", "reprise après sinistre", "ISR", "Eligible Leader Replicas"]
theme: "Data"
tone: "opinion"
used_in: ["2026-11-27"]
---

## Résumé

L'article explore le dilemme de l'« unclean leader election » dans Apache Kafka : lorsque le dernier broker synchronisé (ISR) d'une partition disparaît, Kafka privilégie par défaut la cohérence en mettant la partition hors ligne, parfois pendant des heures ou indéfiniment. L'auteur montre, via un exemple de boutique en ligne (topics "transactions" et "clicks"), qu'en situation de sinistre réel, la disponibilité l'emporte presque toujours car l'alternative revient à arrêter l'activité. Il recommande donc de définir à l'avance, topic par topic, un plan de reprise après sinistre plutôt que de décider dans l'urgence. Depuis Kafka 4.0, la fonctionnalité Eligible Leader Replicas (ELR) permet d'automatiser une partie de cette récupération sans perte de données, et l'auteur conseille de l'activer sans hésiter.

## Points clés

- Par défaut, Kafka privilégie la cohérence : si tous les brokers de l'ISR (in-sync replicas) tombent, la partition reste hors ligne jusqu'au retour d'un broker synchronisé, ce qui peut prendre un temps indéterminé.
- L'« unclean leader election » permet à n'importe quel broker restant de devenir leader pour restaurer la disponibilité, au prix d'une perte de données potentielle.
- En situation de reprise après sinistre réelle, privilégier la disponibilité l'emporte presque systématiquement : l'alternative (ne rien faire) équivaut à arrêter l'activité.
- La perte de données « théorique » du mode par défaut n'est pas nulle en pratique : les producteurs saturent, et l'absence de flux affecte les traitements en aval sensibles au temps.
- La décision doit se prendre topic par topic selon la criticité des données (ex. métriques de clics vs transactions financières), et doit être anticipée dans un plan de reprise après sinistre écrit à l'avance.
- Depuis Kafka 4.0, les Eligible Leader Replicas (ELR) permettent dans certains cas de promouvoir automatiquement un broker garanti sans perte de données, réduisant le recours manuel à l'unclean leader election — mais ne l'éliminant pas totalement.

## Analyse approfondie

Apache Kafka maintient, pour chaque partition de topic, un ensemble de répliques synchronisées (l'ISR, In-Sync Replica set), dont l'une est le leader. En fonctionnement normal, si le leader est perdu, un autre broker de l'ISR prend sa place. Mais si *tous* les brokers de l'ISR disparaissent, la partition passe hors ligne : producteurs et consommateurs ne peuvent plus l'utiliser.

La configuration par défaut de Kafka fait un choix explicite : privilégier la *cohérence* plutôt que la *disponibilité*. La partition reste hors ligne jusqu'au retour d'un broker ayant appartenu à l'ISR — ce retour pouvant survenir en quelques minutes, plusieurs jours, ou jamais. L'alternative consiste à laisser n'importe quel broker restant devenir leader, quitte à perdre des données : c'est l'« unclean leader election ». Ce choix se configure par topic, et ressemble à un dilemme du type « problème du tramway » : ne rien faire, c'est perdre la disponibilité ; agir, c'est risquer la cohérence.

L'auteur nuance toutefois cette lecture binaire. D'abord, en théorie, le mode par défaut ne perd aucune donnée : les producteurs mettent les messages en mémoire tampon localement et les renvoient une fois la partition rétablie. Mais en pratique, un volume de données trop important peut forcer le producteur à abandonner des messages pour ne pas saturer son disque — ce qui constitue bien une perte. De plus, la notion de perte de données doit s'envisager plus largement : un consommateur privé du flux habituel de messages peut lui-même subir une perte fonctionnelle si ses traitements en aval sont sensibles au temps.

Ensuite, certains cas d'unclean leader election ne sacrifient en réalité aucune cohérence. Si l'ISR compte deux brokers et que le non-leader tombe en premier, puis le leader, la partition passe hors ligne. Si seul le non-leader revient, Kafka ne le promeut pas automatiquement leader, car n'étant plus dans l'ISR au moment de la panne, il pourrait ne pas détenir toutes les données. Pourtant, dans ce scénario précis, ce broker possède bel et bien toutes les données, et le promouvoir via une unclean leader election serait en fait sûr.

L'auteur illustre cela avec l'exemple d'un cluster Kafka alimentant un site e-commerce, avec deux topics : *transactions* (une entrée par achat) et *clicks* (le suivi de navigation). Une nuit, un incident met les deux topics hors ligne ; au matin, l'équipe découvre que l'activité commerciale est bloquée : les clients ne peuvent plus acheter (topic *transactions* indisponible) et l'entreprise perd en plus toute visibilité sur le comportement des visiteurs (topic *clicks* indisponible).

Pour le topic *clicks*, la décision est rapide : effectuer une unclean leader election pour retrouver la visibilité, au prix d'un trou de quelques heures dans les données — un coût négligeable. Pour le topic *transactions*, la réunion de crise aboutit à la même conclusion par nécessité : il n'existe pas d'autre solution que de déclencher une unclean leader election, au risque de perdre des transactions accumulées côté producteurs, afin de remettre la boutique en ligne. Certaines ventes seront peut-être perdues et devront être traitées après coup, mais l'activité reprend.

La leçon que tire l'auteur est que, en situation de reprise après sinistre, privilégier la disponibilité à la durabilité finit presque toujours par s'imposer : il n'existe simplement pas d'autre option viable, l'alternative étant de fermer boutique. Dès lors, pourquoi ne pas configurer Kafka pour déclencher cette élection automatiquement ? Pour un topic de métriques comme *clicks*, cela a du sens : il est plus important de maintenir le flux de messages que de craindre d'en perdre quelques-uns. Pour un topic critique comme *transactions*, c'est bien plus délicat : perdre une seule transaction reste toujours problématique, et l'activation permanente de l'unclean leader election automatique pourrait faire croire à un client qu'une commande a été enregistrée alors qu'elle a été perdue. Automatiser ce choix pour ce type de topic n'est donc pas recommandé.

L'auteur insiste : il s'agit ici de *reprise après sinistre*, pas d'une situation d'exploitation normale — un topic hors ligne ne devrait jamais se produire en premier lieu. Mais une fois le sinistre survenu, des dégâts ont déjà eu lieu, et l'unclean leader election permet d'éviter d'en accumuler davantage. Ce schéma, précise-t-il, est un cas fictif mais représentatif d'un motif observé un peu trop souvent en production.

Que faire, concrètement ? En tant qu'opérateur Kafka, il faut connaître ce mécanisme et savoir déclencher une élection non propre si nécessaire, et en informer les parties prenantes métier. Ensemble, opérateurs techniques et responsables métier devraient établir un plan de reprise après sinistre précisant la conduite à tenir en cas de topic hors ligne — une réflexion bien plus simple à mener à froid qu'en pleine crise.

La communauté Kafka a pris la mesure du problème avec la fonctionnalité *Eligible Leader Replicas* (ELR), disponible depuis Kafka 4.0 — une avancée qui ne profite toutefois pas aux clusters plus anciens, encore nombreux en production. Sans entrer dans tous les détails techniques, l'ELR vise à permettre une récupération automatique sans perte de données dans les situations qui le permettent. En plus de l'ISR, Kafka maintient un ensemble distinct, l'ELR, regroupant les brokers qui ne sont plus dans l'ISR mais dont on garantit qu'ils détiennent tous les enregistrements validés (commis). Lorsqu'il ne reste plus aucun broker vivant dans l'ISR, un broker de l'ELR peut être réintégré et promu leader. Même avec l'ELR, certains cas limites subsistent où une partition hors ligne ne redevient pas disponible automatiquement, nécessitant malgré tout une unclean leader election. Dans l'exemple fictif initial, l'ELR aurait justement permis de promouvoir automatiquement le broker revenu, sans intervention manuelle.

L'article se conclut par deux recommandations : sur Kafka 4.0 ou plus récent, activer l'ELR sans hésitation ; et, quelle que soit la version, rédiger un plan de reprise après sinistre pour les topics hors ligne, car on finit toujours par devoir « actionner le levier ».

## Pourquoi ça compte

Ce billet rappelle un angle mort fréquent des architectures Kafka en production : la configuration par défaut, pensée pour la cohérence, peut se retourner contre la continuité d'activité lors d'un vrai sinistre si aucun plan n'a été anticipé. C'est un point de vigilance concret pour toute équipe data/plateforme opérant du Kafka, d'autant plus avec l'arrivée de l'ELR dans Kafka 4.0 qui change la donne sans la supprimer entièrement.
