---
title: "Is your eval lying to you?"
date: 2026-09-22
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fblog.mastykarz.nl%2Feval-lying%3Futm_source=tldrai/1/010001a0c42e94b8-7b241079-f6b5-4a4c-afea-c924ebe9e012-000000/w53YPIuwB0DcsAWZhYMHONywcSVCTO8CwOW0jfNOlwA=452"
authors: ["Waldek Mastykarz"]
keywords: ["évaluation IA", "agents de codage", "LLM judge", "tests automatisés", "CI/CD", "fiabilité"]
theme: "IA"
tone: "opinion"
used_in: ["2026-09-22"]
---

## Résumé
L'article dénonce l'usage abusif des graders de type « string contains » (la chaîne est présente) dans les evals pour agents de codage IA : rapides et gratuits, ils sont pourtant trompeurs, car ils ne prouvent que la présence ou l'absence d'une chaîne de caractères, jamais le comportement réel du système. L'auteur propose un test simple — terminer les phrases « si ce grader passe/échoue, je sais que ______ » — pour distinguer ce qu'un check établit réellement de ce qu'on lui fait dire par abus d'inférence. Il recommande d'utiliser des outils déterministes (compilateur, gestionnaire de dépendances, validateur de schéma, exécuteur de tests) quand la propriété mesurée est elle-même déterministe, et de réserver les juges LLM aux questions sémantiques qu'aucun outil n'adresse directement. Enfin, il plaide pour traiter les evals agentiques comme des tests d'intégration, avec des portes de vérification séparées (build, test, run, deploy) plutôt qu'un unique proxy global.

## Points clés
- Un grader « string contains » ne prouve que la présence littérale d'une chaîne dans le contenu inspecté — pas que le comportement attendu a eu lieu (un commentaire, du code mort ou un fichier jamais chargé suffisent à le faire passer).
- L'absence de la chaîne ne prouve pas non plus l'absence du comportement : un agent peut exprimer la même intention avec un vocabulaire différent.
- Le test « si ce grader passe/échoue, je sais que ______ » permet de vérifier que la preuve produite correspond bien à l'affirmation qu'on veut en tirer.
- Les checks faciles et rapides (déterministes) donnent une fausse assurance quand ils sont utilisés pour approximer des propriétés qu'ils ne mesurent pas réellement.
- Pour les propriétés déterministes (compilation, tests, restauration de dépendances, validation de schéma), utilisez l'outil qui peut y répondre directement plutôt qu'un LLM qui ne fait qu'approximer.
- Les juges LLM sont utiles pour les critères sémantiques (intention, cohérence du code) mais ne remplacent pas l'exécution réelle du logiciel ; les evals agentiques gagnent à être structurées comme des tests d'intégration avec des portes de vérification séparées.

## Analyse approfondie
Lorsqu'on construit des évaluations (evals) pour des agents de codage IA, le test « string contains » (la chaîne contient) est incroyablement tentant. Il est rapide et déterministe. Et il ne coûte pratiquement rien, ce qui permet de l'exécuter à chaque changement en CI sans se soucier du coût d'inférence ou de la latence. Mais son utilisation ne fait-elle pas mentir votre eval ?

Vous voulez savoir si l'agent a utilisé Azure ? Cherchez « Azure », n'est-ce pas ? Vous voulez savoir s'il a utilisé une API particulière ? Cherchez le nom de l'API. Vous voulez savoir s'il a créé la bonne configuration ? Vérifiez si la chaîne attendue se trouve dans le fichier. Test réussi. Livrez. Mais vous n'avez rien établi de tout cela.

### Qu'est-ce que votre grader a prouvé ?
Supposons que votre eval exige que la solution générée utilise Azure, et que votre grader vérifie si les fichiers générés contiennent la chaîne « Azure ». Le grader passe. Que savez-vous à présent ? Seulement que la chaîne « Azure » apparaît quelque part dans les fichiers générés. C'est tout.

La chaîne pourrait apparaître dans du code qui utilise Azure, mais elle pourrait tout aussi bien apparaître dans un commentaire. Après tout, une seule ligne suffit à satisfaire votre grader. Voici tout ce qu'il a besoin de voir :

`// Ne pas utiliser Azure ici.`

Ce commentaire passe le test. Du code mort, une dépendance inutilisée, de la documentation ou une fixture de test le passeraient tout autant. Un fichier de configuration pourrait contenir la chaîne même si l'application ne charge jamais ce fichier. Votre grader trouve ce qu'il cherche, mais le comportement qui vous intéresse reste absent.

Le même problème fonctionne à l'inverse. Si la chaîne n'est pas présente, pouvez-vous en conclure que la solution n'utilise pas Azure ? Non. L'agent pourrait utiliser un SDK sans mentionner explicitement Azure, ne faire référence qu'à un nom de package ou de classe, ou exprimer la même intention avec des mots que vous n'aviez pas anticipés. Le langage naturel aggrave encore les choses, car la différence entre *a fait* et *n'a pas fait* peut tenir à un seul mot, alors que le mot-clé recherché reste exactement le même. Un grader déterministe vous donne une réponse déterministe, mais cette réponse ne signifie que ce que le test établit réellement.

### Terminez la phrase
Il existe un test simple que j'aime appliquer aux critères d'évaluation. Complétez une phrase pour un résultat réussi, puis une autre pour un échec. Soyez littéral :

**Si ce grader passe, je sais désormais que ______.**

**Si ce grader échoue, je sais désormais que ______.**

Pour un grader de type « string contains "Azure" », les réponses sont étroites. Elles ne décrivent que ce que le grader a observé. Tout le reste relève de l'inférence :

Si ce grader passe, je sais que la chaîne « Azure » apparaît dans le contenu inspecté.

Si ce grader échoue, je sais que la chaîne « Azure » n'apparaît pas dans le contenu inspecté.

Si c'est bien ce que vous vouliez mesurer, tant mieux. Mais si vous complétez la première phrase par *l'agent a correctement utilisé Azure*, vous avez fait un saut que vos preuves ne justifient pas. Le grader n'est pas forcément inexact. Il peut être parfaitement précis dans ce qu'il fait, alors même qu'on lui demande de prouver quelque chose dont il est incapable.

### Une preuve facile peut vous donner une fausse assurance
On comprend aisément pourquoi les gens utilisent des graders déterministes simples. Les evals agentiques coûtent de l'argent et peuvent prendre beaucoup de temps à exécuter. Les juges LLM ajoutent du coût d'inférence et de la latence. Construire, exécuter ou déployer des applications générées ajoute de l'infrastructure et de la complexité. En comparaison, « string contains » prend quelques millisecondes, ce qui en fait un candidat idéal pour la CI… et potentiellement une preuve épouvantable.

Vous commencez alors à optimiser une eval en fonction de ce qui est pratique à mesurer plutôt que de ce que vous avez besoin de savoir. Le résultat peut être un pipeline d'évaluation rapide et reproductible qui vous donne une fausse assurance à chaque exécution. Je préfère exécuter moins d'evals produisant des preuves significatives plutôt que d'exécuter continuellement des evals qui m'affirment avec assurance très peu de choses.

### Interrogez le système capable de répondre à la question
Si vous voulez savoir si le code généré compile, compilez-le. Nous avons vu des solutions recevoir un score parfait de la part d'un juge LLM avant d'échouer à la compilation. Le juge pouvait évaluer si l'implémentation avait l'air correcte, mais seul le compilateur pouvait le vérifier.

Si vous voulez établir si les dépendances peuvent être restaurées, restaurez-les. Si vous voulez savoir si un fichier JSON respecte un schéma, validez-le. Si vous voulez établir si les tests passent, exécutez-les. Et, dans la mesure du raisonnable, si vous voulez établir si l'application fonctionne, exécutez-la.

C'est là que les graders déterministes fonctionnent bien, car le test établit directement la propriété qui vous intéresse. Utiliser un LLM pour prédire si un projet va compiler n'a guère de sens quand le compilateur peut répondre avec autorité. Vous demanderiez à un LLM d'approximer une réponse qu'un outil existant peut vous donner.

Mais exécuter des applications générées est plus difficile que de les construire. Les applications réelles ont besoin d'identifiants et de configuration. Elles ont aussi besoin de données, d'infrastructure et d'accès à des services externes. Les déployer ajoute une couche de complexité supplémentaire. Malheureusement, les agents de codage peinent souvent sur ces points de friction, ce qui rend tentant de vérifier autre chose de plus simple à la place.

Vous vérifiez alors plutôt la présence des artefacts ou des mots attendus dans la sortie. Un juge LLM dit que l'implémentation semble plausible. Vous traitez ensuite ces observations comme des preuves que l'intégration fonctionne, alors qu'aucune d'entre elles ne l'a réellement mise à l'épreuve. Parfois, exécuter la solution complète n'est vraiment pas praticable, et c'est très bien ainsi. Une eval n'a pas besoin de tout prouver, mais son rapport doit indiquer clairement ce qu'elle a établi et ce qu'elle n'a pas établi.

### Les juges LLM répondent à des questions différentes
Les critères sémantiques sont différents. Un juge LLM peut distinguer *utiliser Azure pour stocker les données* de *ne pas utiliser Azure pour stocker les données*. Il peut inspecter le code environnant, raisonner sur la façon dont les composants sont liés entre eux, et reconnaître des implémentations qui ne contiennent pas le vocabulaire que vous aviez anticipé en écrivant l'eval.

Mais un juge LLM n'élimine pas le problème de la preuve. Il ne peut pas remplacer de manière fiable la construction et l'exécution du logiciel. Et même s'il pouvait reproduire chaque compilateur, gestionnaire de paquets, exécuteur de tests ou vérification à l'exécution pertinents, pourquoi le lui demanderiez-vous ? Nous disposons déjà de ces outils. Utilisez les juges LLM pour les questions sémantiques, et les outils déterministes lorsqu'ils peuvent répondre directement à une question.

### Traitez les evals agentiques comme des tests d'intégration
Lorsque vous évaluez un serveur MCP, une skill, une extension ou une autre capacité destinée à un agent de codage, ce qui vous importe, c'est de savoir si l'agent peut mener la tâche à bien. Trouver un détail d'implémentation particulier dans sa sortie vous en apprend bien moins. C'est pourquoi je trouve plus utile de penser ces evals comme des tests d'intégration plutôt que comme des tests unitaires.

Dans nos evals, la construction, les tests, l'exécution et le déploiement sont des portes (gates) distinctes. À leurs côtés, des juges LLM évaluent les propriétés sémantiques pertinentes pour chaque scénario. Garder ces vérifications séparées vous permet de voir si la restauration des dépendances a échoué, si la compilation a cassé, ou si une implémentation compilable a manqué une exigence importante. Un seul indicateur global (proxy) ne devrait pas avoir à répondre à toutes ces questions.

Cela dit, les graders déterministes sont excellents lorsque la propriété mesurée est elle-même déterministe. Le problème commence lorsque vous choisissez un signal pratique et que vous élargissez discrètement l'affirmation que vous en tirez. Avant d'ajouter un grader à votre prochaine eval agentique, terminez ces deux phrases :

**Si ce grader passe, je sais désormais que ______.**

**Si ce grader échoue, je sais désormais que ______.**

Comparez ensuite ces réponses avec ce que vous comptez affirmer à propos de votre agent, de votre skill, de votre serveur MCP ou de votre extension. Si elles ne correspondent pas, cherchez des preuves plus solides. Votre eval ne devient pas digne de confiance parce qu'elle s'exécute à chaque commit. **Elle devient digne de confiance quand ses preuves soutiennent les affirmations que vous en tirez.**

## Pourquoi ça compte
À mesure que les équipes multiplient les evals CI pour leurs agents IA, cet article rappelle une discipline méthodologique essentielle : un check rapide et déterministe ne vaut que ce qu'il mesure réellement, et confondre « facile à vérifier » avec « prouvé » peut faire passer des agents défaillants en production avec une fausse confiance.
