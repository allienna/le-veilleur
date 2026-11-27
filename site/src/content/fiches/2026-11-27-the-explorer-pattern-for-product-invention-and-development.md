---
title: "The Explorer Pattern for product invention and development."
date: 2026-11-27
url: "https://leadershipintech.com/links/23816/3d78f33c-7ca0-4e03-9c70-68e56918a4cd/email"
keywords: ["Explorer Pattern", "méthodologie produit", "ingénierie logicielle", "organisation d'équipe", "retravail logiciel", "culture d'entreprise"]
theme: "Leadership"
tone: "opinion"
used_in: ["2026-11-27"]
---

## Résumé

L'article présente le « Explorer Pattern », un modèle de développement produit utilisé chez Imprint où une petite équipe construit une implémentation fonctionnelle en minimisant au maximum les dépendances inter-équipes, puis réconcilie les détails avec les autres équipes une fois le prototype achevé, en acceptant un retravail potentiellement important. L'auteur justifie ce changement par le fait qu'écrire et retravailler du logiciel est devenu quasiment gratuit depuis 2026, rendant obsolètes les anciens processus conçus pour éviter le retravail d'ingénierie. Il illustre le concept par l'analogie des architectures de bases de données primaire/répliques, puis par un exemple concret : le déploiement du support des agrégateurs financiers (via Plaid) chez Imprint. Le texte se conclut par neuf règles pratiques pour appliquer ce pattern sans provoquer de chaos organisationnel.

## Points clés

- Le Explorer Pattern : une équipe restreinte (5 personnes maximum) construit une solution complète avant de synchroniser avec les autres équipes, plutôt que l'inverse.
- Analogie technique centrale : ce modèle s'apparente à une architecture base de données primaire-secondaire (écriture vérifiée en amont, propagation en aval), par opposition aux systèmes à quorum type Dynamo/Cassandra, plus lents et incohérents à ressources égales.
- Contexte 2026 : le coût de production et de retravail du code, des designs et des analyses s'est effondré, ce qui invalide des décennies de pratiques organisationnelles conçues pour éviter le retravail d'ingénierie.
- Exemple concret : le support des agrégateurs financiers (Plaid) chez Imprint a été développé en « alpha privée » par un seul responsable technique avant d'être synchronisé puis livré.
- Neuf règles pratiques encadrent la méthode : objectif et sponsor clairs, petit groupe flexible, communication publique des progrès, changements minimaux, jugement rapide sur les hypothèses, tolérance à l'erreur, livraison jusqu'en production derrière un feature flag.

## Analyse approfondie

tl;dr : Le Explorer Pattern consiste en un individu ou une équipe qui construit une implémentation fonctionnelle minimisant autant qu'humainement possible les impacts inter-équipes et inter-fonctionnels, puis qui réconcilie les détails avec les autres équipes une fois ce prototype terminé, en acceptant que cette approche puisse nécessiter un retravail substantiel de ce développement initial.

### Pourquoi écrire ceci ?

Imprint appelait auparavant cela le modèle de développement « piloté par la tech » ou « piloté par l'ingénierie », mais ce que cela signifie reste assez flou pour beaucoup. Ce billet propose un terme plus précis, le « Explorer Pattern », et explique plus en détail son fonctionnement.

### Pourquoi devons-nous ajuster notre façon de travailler ?

Avant 2026 :

- Le code est coûteux, et nous concevons les processus pour minimiser l'implémentation et le retravail

Pendant et après 2026 :

- Écrire du logiciel est devenu extrêmement bon marché, mais c'est un phénomène plus large : **produire un résultat est devenu, de fait, gratuit dans de nombreuses dimensions**. Le code est quasiment gratuit — si l'on dispose des contraintes appropriées. Les designs sont quasiment gratuits — s'ils suivent des patterns. L'analyse est quasiment gratuite — si on a correctement instrumenté les choses
- **Retravailler un logiciel est devenu extrêmement bon marché**. Historiquement, l'industrie a optimisé pour éviter le retravail d'ingénierie parce que l'ingénierie était le coût le plus élevé / la contrainte la plus étroite. Dans beaucoup d'entreprises, cela s'est traduit par l'idée que l'écriture de code était la contrainte, ce qui n'a jamais été vrai, mais de nombreuses pratiques courantes ont été conçues comme si ça l'était (par exemple, impliquer l'ingénierie tardivement dans la résolution de problèmes « pour protéger son temps »)
- **Travailler sur le système est bien plus efficace qu'historiquement si l'on met correctement en place l'intégration automatisée et les boucles de feedback**, c'est-à-dire ne pas se contenter d'améliorer un design ponctuel mais améliorer le système de design. Tout endroit où l'amélioration du processus à plus fort effet de levier est plus lente que la résolution du cas ponctuel constitue un bug dans notre processus

### Explorer Pattern : la métaphore primaire-et-répliques

La métaphore la plus simple pour penser à l'Explorer Pattern est la réplication de bases de données. Des bases de données comme MySQL et PostgreSQL ont une base primaire, où les écritures sont effectuées. Chaque écriture est vérifiée à cet endroit, et une fois vérifiée, on sait que les écritures vont se propager en aval vers différentes répliques secondaires. Ces répliques en aval peuvent être *en retard* mais elles ne peuvent pas être *fausses*, car les écritures sont vérifiées en amont. (Je me suis retenu de parler du théorème CAP.)

Un autre modèle de conception de base de données est celui utilisé par Dynamo ou Cassandra (ou MongoDB dans une certaine mesure), où l'on dispose d'un ensemble de répliques, et où il faut obtenir un accusé de réception de la majorité de cet ensemble pour qu'une écriture soit fortement cohérente. C'est une configuration très fiable, car elle permet de tolérer la perte d'un nœud, mais elle introduit aussi des incohérences, et pour une quantité fixe de matériel, ces configurations ont tendance à être bien, bien plus lentes qu'un système primaire-secondaire (ou s'appuient sur de mauvaises métriques de performance qui ne font pas de `fsync` sur disque pour créer l'illusion d'un débit élevé).

L'Explorer Pattern correspond au premier modèle, primaire-secondaire, où la grande majorité du travail est réalisée par l'individu ou l'équipe en charge. Cela rend tout le travail cohérent en interne, car il passe par le même petit groupe. Cela ne signifie pas pour autant que le travail est parfait. Par exemple, on peut toujours insérer une donnée qui respecte les contraintes de la table mais qui reste intrinsèquement fausse (par exemple, `200` est un entier valide, mais cela ne signifie pas que ma limite de crédit était censée être `200` — cela dépend de la logique applicative environnante).

Les autres équipes prennent connaissance des changements en aval, pas de façon synchrone et en amont, et c'est à l'équipe qui travaille sur le sujet qu'il revient à la fois de justifier son approche et de créer de la visibilité sur son travail pour que les autres équipes puissent s'y engager de façon non bloquante.

### Exemple : le support des agrégateurs financiers

Un exemple concret de cette pratique chez Imprint a été le déploiement du support des agrégateurs financiers, c'est-à-dire permettre aux utilisateurs de connecter leurs comptes Imprint via Plaid. C'est quelque chose que les utilisateurs demandent depuis toujours, mais c'est particulièrement important dans le contexte du commerce agentique, où de plus en plus d'agents analysent l'état financier des gens pour leur compte. Pour ce projet, l'un de nos responsables d'ingénierie (Ron) a construit une première version de la fonctionnalité à faible intensité, tout en cherchant à comprendre la forme du problème dans le cadre d'une alpha privée. Il a échangé périodiquement sur certains détails pour tenir les autres équipes informées, mais il s'agissait plutôt d'un projet secondaire.

Cependant, une fois qu'il a identifié la forme complète du problème et mis en œuvre une solution complète, nous avons réduit à presque zéro le « décalage de réplique » entre les équipes, identifié et traité la poignée de problèmes restants, puis livré la fonctionnalité. Comme beaucoup de nos projets cette année, elle n'a jamais officiellement figuré sur une roadmap, et pourtant nous avons livré une fonctionnalité de qualité que nos membres attendaient depuis longtemps.

### Comment suivre l'Explorer Pattern

Les règles générales pour suivre l'Explorer Pattern :

1. **Connaître son objectif et son sponsor** : toute initiative doit en fin de compte viser un résultat précis et avoir un sponsor qui la finance. Cela n'a pas toujours besoin d'être explicite, surtout pour les petits projets, mais dès qu'un projet dépasse environ 3 semaines d'effort, si vous ne pouvez pas identifier très explicitement qui est le stakeholder qui sponsorise votre projet et qu'il n'approuverait pas avec enthousiasme, alors vous êtes probablement plus proche d'être « perdu » que d'être en « exploration »
2. **Le petit groupe de travail est petit** : au maximum 5 personnes, de préférence moins. Chaque membre du groupe doit garder l'intégralité du projet en tête aussi longtemps que possible pour détecter les problèmes et les opportunités
3. **Le petit groupe de travail est flexible** : les membres des petits groupes de travail doivent « chercher un moyen de dire oui » plutôt que « chercher un moyen de dire non ». Explorer, c'est découvrir la forme fondamentale d'un problème plutôt que de prétendre qu'on la connaît déjà
4. **Publier les progrès dans un canal public** : les explorateurs doivent rendre compte régulièrement des progrès réalisés afin que les autres en soient informés. Cela passe à la fois par un Linear Project et un canal Slack
5. **Apporter les changements les plus restreints possibles à ce qui existe déjà** : lorsque nous introduisons des changements inutiles, nous invalidons les modèles mentaux des autres sur le fonctionnement du système. Et quand nous n'avons pas fait ces changements avec soin, nous n'invalidons pas seulement leur modèle mental, nous créons aussi l'attente que nous l'avons fait très intentionnellement pour une bonne raison — ce qui a un effet dissuasif sur la capacité des autres à les améliorer plus tard, ce qui est très coûteux, alors que l'Explorer Pattern repose justement sur le fait d'être aussi peu coûteux que possible
6. **Exercer un bon jugement pour identifier des hypothèses raisonnables** : écarter immédiatement les mauvaises idées, puis filtrer le reste en essayant de les implémenter aussi vite que possible. Une fois que l'on voit la forme de l'implémentation, on peut déterminer lesquelles des hypothèses restantes sont intéressantes
7. **Maintenir certaines hypothèses constantes pour éviter de rester bloqué** : la seule façon de naviguer dans des problèmes complexes et ambigus est de fixer certains éléments, même en sachant qu'ils sont imparfaits. Par exemple, pour planifier les effectifs, nous devons connaître notre revenu ; pour connaître notre revenu, nous devons le prévoir ; pour le prévoir, nous devons connaître la date à laquelle les partenaires seront en production l'année prochaine. Nous ne connaissons vraiment aucune de ces choses, donc simplement ancrer une estimation plausible pour nous débloquer est bien plus utile que de chercher à obtenir des chiffres précis. Un peu de travail préparatoire est utile, mais en faire beaucoup n'est qu'une précision artificielle qui distrait du progrès
8. **Laisser de la place à l'idée de se tromper totalement** : quand on avance vite, avec peu d'informations, on trouve toujours une issue, mais ce n'est souvent pas celle que l'on avait anticipée au départ. Il faut être prêt à tout jeter et à recommencer une deuxième, une troisième, une quatrième fois
9. **Déployer jusqu'en production derrière un feature flag** : les fonctionnalités et les produits avancent vite quand on fait fonctionner chaque élément, du frontend au backend en passant par les récupérations de données. C'est la première étape de l'exploration. Veillez simplement à ce que ce soit derrière un feature flag activé uniquement pour les équipes internes !

## Pourquoi ça compte

Ce texte illustre une évolution de fond dans l'organisation du travail d'ingénierie à l'ère où le coût de production (et de retravail) du code chute drastiquement, remettant en cause des décennies de pratiques de gouvernance produit conçues pour éviter le retravail — un signal utile pour quiconque suit l'évolution des méthodologies de développement produit et d'organisation des équipes tech.
