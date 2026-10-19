---
title: "How AI has changed my engineering leadership role"
date: 2026-10-19
url: "https://leadershipintech.com/links/23515/3d78f33c-7ca0-4e03-9c70-68e56918a4cd/email"
keywords: ["leadership technique", "IA générative", "productivité ingénieurs", "onboarding", "feature flags", "bus factor"]
theme: "Leadership"
tone: "opinion"
used_in: ["2026-10-19"]
---

## Résumé

L'auteur, un responsable technique, explique comment l'IA (notamment Claude) a transformé sa façon de diriger une équipe d'ingénierie. Alors qu'il privilégiait auparavant une posture purement managériale, l'IA lui permet désormais de redevenir ponctuellement "hands-on" en codant lui-même des outils utiles à l'équipe, tout en accélérant sa compréhension de systèmes qu'il ne maîtrisait pas en détail. Il observe aussi que l'IA réduit certains risques organisationnels classiques (onboarding lent, dépendance excessive à quelques experts, frilosité face aux nouvelles technologies), tout en soulignant que l'industrie est encore en phase d'apprentissage sur le plein potentiel de ces outils.

## Points clés

- En codant lui-même un système de feature flags avec l'aide de son agent IA, l'auteur a résolu un problème opérationnel concret (un déploiement cassé difficile à annuler) et regagné en crédibilité technique auprès de son équipe.
- L'IA accélère l'onboarding : elle permet de comprendre rapidement des systèmes complexes et d'améliorer en continu la documentation (README, CLAUDE.md).
- La réduction du temps d'apprentissage atténue ses réticences passées envers la multiplication des technologies et des microservices.
- Le "bus factor" (dépendance à une poignée d'experts) devient moins critique, car l'IA permet de comprendre rapidement non seulement l'intention du code, mais aussi son comportement réel.
- L'auteur estime que l'organisation collective sur l'usage de l'IA en est encore à ses débuts, en particulier chez les décideurs non-techniques qui la perçoivent comme une "baguette magique" sans vision claire de son potentiel transformateur.

## Analyse approfondie

Si vous avez lu certains de mes articles précédents, vous pourriez croire à tort que je ne suis pas un fan de l'IA. En réalité, bien qu'il y ait certains inconvénients, la plupart des changements que j'ai connus ont été positifs.

### Être plus hands-on

J'avais l'habitude de soutenir que les responsables d'équipes dépassant une certaine taille pouvaient accroître leur impact en consacrant le maximum de leur temps au management plutôt qu'à du travail d'ingénieur individuel (IC). Je pense toujours qu'un bon management, surtout avec des équipes de plus de quelques personnes, doit rester la mission centrale d'un leader, mais l'IA m'a redonné une appréciation renouvelée de la valeur d'être "hands-on".

Par exemple, notre équipe a récemment mis en production une fonctionnalité cassée qu'il a fallu beaucoup trop de temps à annuler. La plupart des entreprises disposent d'un système de feature-flagging permettant d'activer ou désactiver rapidement de nouvelles fonctionnalités sans redéploiement. Ce n'était pas notre cas.

Après quelques heures de recherche et de codage avec mon agent, j'ai construit un système simple de feature-flagging. Rien de sophistiqué, mais ça fonctionnait. J'aurais pu utiliser un produit tiers, mais je voulais quelque chose d'idiomatique à notre système, qui fonctionne comme notre équipe s'y attendrait. Je savais qu'ils ne voulaient pas d'un nouveau login vers un dashboard tiers : ils voulaient le contrôler via des arguments en ligne de commande, avec une documentation appropriée pour que Claude puisse le comprendre. L'équipe a immédiatement adopté les outils que j'ai créés et les a utilisés pour tous nos déploiements critiques, presque sans que j'aie besoin de les solliciter.

C'était une petite victoire, mais significative, car elle a immédiatement amélioré la qualité de nos déploiements sur l'ensemble des équipes, et réduit les risques globaux.

Consacrer du temps à coder de temps à autre ne résout pas seulement le problème immédiat, comme un outil de développement manquant : cela m'aide aussi à rester au courant de nos systèmes et à construire la confiance avec l'équipe. Apporter des contributions directement utiles rend aussi mon travail un peu plus amusant.

### L'onboarding est plus rapide

Pourquoi suis-je capable de contribuer maintenant, alors que je ne le pouvais pas avant ? Ce n'est pas seulement parce que Claude écrit une grande partie du code. C'est aussi parce que je peux apprendre et comprendre de nouveaux domaines du système très rapidement. Je peux demander à Claude d'expliquer comment les choses fonctionnent. Je peux même lui demander de suggérer d'autres façons de résoudre un problème que je n'avais pas envisagées. Je peux approfondir avec des questions pointues sur des sujets que je comprends mais dont je ne suis pas expert, comme la performance de PostgreSQL.

Le même principe s'applique à l'onboarding de n'importe qui sur n'importe quel sujet. Notre équipe a amélioré de manière organique tous nos fichiers `README` et `CLAUDE.md`, et les résultats sont bien meilleurs que ce que nous aurions obtenu avec le projet d'amélioration de la documentation que j'envisageais il n'y a pas si longtemps. Il est désormais beaucoup plus facile pour un nouveau membre de l'équipe (qu'il soit récemment recruté ou nouveau dans une équipe particulière) de trouver le code pertinent et de le comprendre en contexte. En cas de doute, il leur est aussi facile de savoir à qui s'adresser.

### Moins de prudence sur les dépendances et l'adoption de nouvelles technologies

Même si je reste attaché au principe selon lequel l'ajout de nouvelles technologies, comme de nouveaux langages ou microservices, peut complexifier les systèmes plutôt que les simplifier, les évolutions de l'IA au cours des deux dernières années ont considérablement adouci ma position. Parce que les développeurs peuvent s'intégrer plus rapidement à de nouveaux systèmes et langages, j'ai moins de réaction instinctive contre l'ajout de nouvelles technologies et de nouveaux services, et je me sens moins porté à imposer le modèle monolithique lorsque mon équipe pousse dans l'autre sens. Beaucoup des inconvénients liés à une transition prématurée vers les microservices subsistent, mais ils sont moins importants qu'auparavant.

### Le bus factor est moins préoccupant

Ne disposer que d'une ou deux personnes comprenant en profondeur un système critique était autrefois une préoccupation majeure. Ce n'est toujours pas une situation idéale, mais comme les gens peuvent s'auto-former plus rapidement, et que l'information peut être rassemblée si vite, je m'en inquiète moins. Les outils d'IA peuvent comprendre en profondeur non seulement ce que le code est censé faire, mais aussi ce qu'il fait réellement, et cela sans dépendre d'une documentation perpétuellement obsolète.

### Nous sommes encore en apprentissage

Même si la plupart des personnes en ingénierie utilisent l'IA à temps plein depuis un certain temps déjà, nous continuons de construire notre intuition sur ce qu'il est possible de faire avec elle. En dehors de l'ingénierie, les intuitions des gens sont encore moins affinées : de nombreux CEO et product managers à qui j'ai parlé considèrent l'IA comme une baguette magique pour accomplir du travail, mais manquent encore de vision sur la façon dont les produits que nous construisons peuvent changer, et sur les nouvelles catégories de problèmes entières que nous pouvons résoudre avec des produits basés sur l'IA. Je crois que les meilleures idées viendront des personnes qui utilisent ces outils au quotidien et développent une intuition sur ce qu'elles peuvent construire, et je suis impatient de voir où cela nous mènera.

## Pourquoi ça compte

Ce témoignage illustre un retour d'expérience concret sur la manière dont l'IA générative redéfinit le rôle des managers techniques, un angle utile pour la veille sur l'impact organisationnel de l'IA au-delà de la seule productivité des développeurs individuels.
