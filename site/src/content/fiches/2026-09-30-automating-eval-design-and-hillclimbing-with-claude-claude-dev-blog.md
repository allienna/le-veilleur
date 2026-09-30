---
title: "Automating eval design and hillclimbing with Claude / claude.dev Blog"
date: 2026-09-30
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fclaude.dev%2Fblog%2Fautomating-eval-design-and-hillclimbing%2F%3Futm_source=tldrai/1/010001a0ed56b287-90a62935-8940-46d3-9a4e-6d8f51356728-000000/Xf4asCvc6IIpT6RvHbTuXstg-YsQO2p8X_JKHJmgvTs=452"
keywords: ["évaluation IA", "hillclimbing", "surapprentissage", "Claude Code", "skill claude-api", "optimisation des coûts"]
theme: "IA"
tone: "research"
used_in: ["2026-09-30"]
---

## Résumé
Anthropic enrichit le skill `claude-api` de Claude Code avec deux nouvelles commandes, `build-eval` et `hillclimb`, destinées à concevoir des évaluations (evals) fiables et à améliorer les performances d'une application sans tomber dans le piège du surapprentissage (overfitting). L'article expose d'abord les principes d'une bonne conception d'évaluation et d'un hillclimbing rigoureux, puis montre comment ces principes sont mis en œuvre concrètement dans le skill. Il illustre la démarche avec deux études de cas : un benchmark interne de support client, où le coût par ticket est divisé par cinq tout en améliorant la précision, et l'évaluation du skill `claude-api` lui-même, dont le score passe de 66 % à plus de 90 %.

## Points clés
- `build-eval` guide l'utilisateur pour construire une évaluation à partir du trafic de production réel, complété si besoin par des données synthétiques ancrées sur de vrais exemples, avec validation humaine des cas et du grader.
- `hillclimb` améliore une application un changement à la fois, en séparant les données en un ensemble d'entraînement (train) et un ensemble de test tenu à l'écart (held-out) pour détecter le surapprentissage.
- Avant toute optimisation, Claude vérifie que le « bruit » de l'évaluation (variation due au hasard) est plus petit que le gain minimal recherché, sinon il recommande plus de répétitions ou de cas.
- Étude de cas support client : la précision passe de 74,4 % à 98,9 % et le coût par ticket est divisé par environ cinq sur les tickets tenus à l'écart, via un nettoyage du prompt puis un changement de modèle (Opus 4.8 → Opus 5.5 → Sonnet 5).
- Étude de cas du skill `claude-api` : le score passe de 66 % à 77 % en identifiant des fonctionnalités non couvertes et des erreurs dans des tables de types C# et Java.
- Quand le score stagne, Claude effectue une étape de réflexion qui classe les échecs restants par cause racine plutôt que d'appliquer un correctif de plus.

## Analyse approfondie
Principes pour concevoir des évaluations (evals) et pratiquer le hillclimbing sans se tromper soi-même, et comment les commandes build-eval et hillclimb du skill claude-api mettent ces principes en pratique.

Les évaluations fournissent un signal sur la performance de votre application ou de votre skill sur des tâches spécifiques. Mais concevoir des évaluations, et améliorer les performances sans se leurrer, est difficile. Nous avons ajouté des recommandations pour les deux au skill claude-api.

Avec ce skill, vous pouvez exécuter `/claude-api build-eval` pour construire une évaluation directement dans votre codebase, et exécuter `/claude-api hillclimb` pour améliorer votre application par rapport à celle-ci, un changement à la fois, avec un ensemble d'exemples tenu à l'écart (held-out) pour détecter le surapprentissage.

Dans cet article, nous mettons d'abord en avant les principes d'une bonne conception d'évaluation et de hillclimbing, puis nous montrons comment Claude Code, via le skill claude-api, applique ces principes. Nous terminerons en montrant quelques exemples d'utilisation de ces commandes.

Les évaluations bien conçues partagent quelques éléments communs (Figure 1) :

La capacité des modèles est irrégulière (jagged). Si vous choisissez des cas parce que le modèle actuel échoue dessus, vous échantillonnez les creux de la surface de capacité de ce modèle en particulier (Figure 2). L'évaluation risque alors de mesurer l'empreinte d'échec de ce modèle plutôt que ce qui est intrinsèquement difficile ou utile pour votre application.

Choisissez des cas difficiles parce qu'un humain les a jugés difficiles : un bon test consiste à pouvoir expliquer pourquoi une tâche est difficile avant de l'inclure. Incluez des cas correspondant à des échecs spécifiques de votre application, tirés du trafic de production, de rapports de bugs ou de tickets. Cependant, ne faites pas une confiance aveugle au trafic utilisateur : les utilisateurs essaient parfois ce qu'ils s'attendent à voir fonctionner, si bien qu'une distribution de tâches tirée strictement du trafic utilisateur peut être biaisée vers la facilité.

La commande build-eval du skill claude-api transforme ces principes en un flux de travail guidé. Lorsque vous exécutez `/claude-api build-eval` dans Claude Code, Claude vous interroge, construit l'évaluation dans votre codebase, et s'arrête pour recueillir votre approbation à des points précis.

Claude vous aide à échantillonner les entrées pour construire les évaluations dans cet ordre :

Le skill privilégie le trafic de production, mais il peut aussi générer des données synthétiques ancrées sur quelques exemples réels que vous fournissez. Le skill demande à Claude de générer une page simple qui affiche chaque entrée et attend votre confirmation. À titre d'illustration, nous montrons ci-dessous un exemple d'ensemble d'entrées pour une application de routage d'e-mails, que le skill peut demander à l'utilisateur de relire (Figure 3).

Après les entrées, Claude propose le grader le moins coûteux qui convient à la sortie de votre application :

Claude note une poignée de cas et demande si vous auriez noté certains d'entre eux différemment (Figure 4). En général, il est important de lire un échantillon de transcriptions notées avant de faire confiance à votre évaluateur ; les erreurs de notation figurent parmi les causes les plus fréquentes de mauvaise configuration d'une évaluation.

Une fois le grader validé, le skill vous indique la taille de l'ensemble d'évaluation (cas × répétitions × modèle, et une estimation approximative du temps nécessaire), exécute la ligne de base (baseline), et affiche le score avec un intervalle de confiance. Ce que vous obtenez en retour : les cas, le grader, le runner, une ligne JSON et une transcription complète par cas, ainsi qu'une page simple listant le score de chaque cas avec un lien vers sa transcription. Si vous voulez davantage que ce que montre cette page (par exemple un graphique), il suffit de le demander et Claude la construira comme une page supplémentaire à côté. Par défaut, ces pages supplémentaires sont des fichiers statiques qui s'ouvrent localement et ne chargent rien depuis le réseau.

Pendant les exécutions de référence mentionnées ci-dessus, Claude vérifie un certain nombre de choses :

Maintenant que vous disposez d'un moyen fiable de noter la performance de votre application sur une tâche, vous pouvez essayer de l'améliorer. Le hillclimbing est un moyen efficace d'ajuster des paramètres comme l'effort ou les prompts, qui font arbitrer coût et performance. Quelques conseils généraux pour choisir où l'appliquer :

Même une évaluation bien conçue correspond rarement exactement à la distribution de tâches qui vous importe en production. En conséquence, le « surapprentissage » (overfitting) à une évaluation est un problème courant, qui se traduit par un système plus performant sur l'évaluation que sur le trafic de production.

Il existe de nombreuses façons pour une évaluation de « fuiter » dans votre harnais (harness) — le code entourant le modèle, incluant les prompts, les outils et la boucle qui appelle Claude. Par exemple, prenons une tâche d'évaluation qui bénéficie de l'OCR, alors que l'OCR est rarement utile pour vos tâches de production. Le harnais d'évaluation pourrait ajouter un outil OCR à votre application, ce qui améliore le score du benchmark sans aucun impact sur la production. Plus largement, le hillclimbing peut ajouter au harnais des fonctionnalités qui traitent des cas particuliers propres aux exemples d'évaluation que vous avez choisis. Ces ajouts au harnais améliorent votre score d'évaluation, mais ne se traduisent pas par des améliorations en production (Figure 5).

Trois éléments peuvent aider à résoudre ce problème :

Comme nous le verrons plus loin, le skill claude-api applique ces principes pour vous.

La commande hillclimb du skill claude-api transforme ces principes en un flux de travail guidé. Lorsque vous exécutez `/claude-api hillclimb` dans Claude Code, Claude itère pour s'améliorer par rapport à une évaluation donnée. Vous choisissez les types de changements qu'il peut effectuer, notamment :

Avant de commencer, Claude demande ce que vous souhaitez optimiser (par exemple la performance, ou le coût à performance constante), puis divise aléatoirement l'ensemble d'évaluation en un ensemble de test et un ensemble d'entraînement (train). Avec un objectif de coût, il examine quelques facteurs de coût courants, notamment la mise en cache des prompts (prompt caching), l'audit du prompt pour vérifier sa compatibilité avec le modèle choisi, et le choix du modèle et du niveau d'effort.

Avant le premier round, Claude vérifie que le bruit de l'évaluation (l'ampleur dont le score peut varier par pur hasard) est inférieur au plus petit gain sur lequel vous agiriez ; si ce n'est pas le cas, il le signale et suggère davantage de répétitions ou de cas.

À chaque round, Claude lit les transcriptions d'entraînement du round précédent et propose un changement unique sous forme de patch. Il vise à chaque round un changement dont l'effet peut se distinguer au-dessus du bruit de l'évaluation : il corrige le comportement défaillant à sa racine (par exemple en réécrivant la section qui en est la cause ou en ajoutant une règle manquante) plutôt qu'en reformulant une simple ligne. Il exécute ensuite l'évaluation avec le changement appliqué. À ce stade, Claude applique une vérification : si l'ensemble train s'améliore mais que l'ensemble test reste stable, Claude soupçonne un surapprentissage et annule le patch. En cas de régression, il l'annule également. Si les ensembles train et test s'améliorent tous deux, il conserve le patch (Figure 6).

Lorsque le score stagne pendant deux ou trois rounds, Claude lit chaque échec restant sur l'ensemble train et les classe par cause. Il fait de même plus tôt si aucun correctif isolé ne pourrait apporter un gain supérieur au bruit de l'évaluation, et suggère alors davantage de répétitions ou de cas, plutôt que de consacrer des rounds à des changements trop petits pour être mesurés. Cette étape permet de détecter des cas d'évaluation ambigus, des erreurs de harnais, ou de la simple variance d'une exécution à l'autre.

Seuls les échecs légitimes sont inclus dans les rounds de hillclimbing suivants.

Une fois le hillclimbing terminé, Claude laisse votre code dans la version qui a le mieux performé sur l'ensemble de test au regard de votre objectif. Il rapporte le résultat du test par rapport à la ligne de base avec des intervalles de confiance (Figure 7). Si le gain se situe dans la marge de bruit, il le signale et déconseille la fusion (merge).

Nous avons exécuté `/claude-api hillclimb` sur un benchmark interne de support client, avec pour objectif de réduire le coût et d'améliorer la performance. Le benchmark comprenait 44 tickets, dont 30 utilisés pour la recherche et 14 tenus à l'écart. Il a démarré sur Opus 4.8 avec les réglages d'effort par défaut (élevé), avec une précision de décision de 74,4 % sur les tickets de recherche et un coût en tokens de 4,6 centimes par ticket.

Le hillclimbing a d'abord audité le prompt, en supprimant des rituels d'appel d'outils obligatoires, une étape de brouillon (scratchpad) et des règles contradictoires. Il a ensuite testé Opus 5.5 avec un effort faible. Cela a permis de franchir la barre de précision de référence à 87,8 % et de réduire le coût à 1,9 centime par ticket, soit moins de la moitié du coût de départ.

Une partie de cette économie provient de la tarification d'Opus 5.5 : les tokens d'entrée et de sortie coûtent 20 % de moins que sur Opus 4.8, et les lectures de cache coûtent 60 % de moins. Parce qu'Opus 5.5 avait franchi la barre, le hillclimbing est ensuite descendu d'un cran pour vérifier si un modèle moins cher pouvait lui aussi la franchir. Sonnet 5 avec un effort faible a obtenu un score comparable, 88,9 %, pour environ la moitié du coût, soit 1 centime par ticket (Figure 8).

Enfin, Claude a amélioré le prompt avec des règles de routage et un croisement avec le plafond de remboursement, portant Sonnet 5 à 98,9 % pour un coût à peu près équivalent. Sur les 14 tickets tenus à l'écart que la recherche n'avait jamais vus, la configuration finale a obtenu un score de 90,5 % contre 78,6 % pour la configuration d'origine, pour environ un cinquième du coût.

Autre exemple : notre skill claude-api, qui fournit des recommandations sur l'utilisation de nos API et des conseils généraux pour travailler avec Claude (y compris les sous-commandes évoquées dans cet article). Nous voulons nous assurer que notre skill peut implémenter correctement du code utilisant nos API, et nous avons construit un ensemble d'évaluation dérivé de notre documentation pour tester le skill.

Sur notre évaluation, le skill a démarré à 66 %. Nous avons donné au hillclimber l'accès à la documentation et à nos SDK, permettant à Claude d'identifier les erreurs et de s'auto-corriger (Figure 9). Claude a découvert que le skill ne couvrait pas huit fonctionnalités.

L'ajout de sections pour celles-ci dans le skill a fait passer la performance à 74 %. Il a ensuite trouvé des erreurs dans des tables de types C# et Java, portant la performance à 77 %.

Après que le score a stagné pendant deux rounds, Claude a analysé les échecs restants et les a répartis par cause racine. Un round normal effectue une modification pour l'échec le plus fréquent. Cette étape ne fait aucune modification ; elle se contente de classer chaque échec restant par cause. Cette étape de réflexion s'est révélée utile de plusieurs façons :

Ces sous-commandes peuvent être utilisées directement dans Claude Code via le skill claude-api :

Exécutez `/claude-api build-eval` si vous souhaitez générer un ensemble d'évaluation pour un problème particulier. Vous pouvez orienter le processus en donnant accès à des exemples (par exemple des traces). Claude appliquera les recommandations partagées dans cet article pour concevoir les exemples et le grader, et s'assurera que vous approuvez les exemples et le grader.

Exécutez `/claude-api hillclimb` si vous disposez d'une évaluation et souhaitez que Claude l'améliore, guidé par votre objectif (par exemple une meilleure performance, ou un coût réduit à performance constante). Claude appliquera les recommandations partagées dans cet article pour surveiller le surapprentissage pendant la progression et pour détecter les bugs dans l'évaluation elle-même, comme un grader qui note à tort une réponse pourtant correcte, ou une erreur de harnais, à la fois avant le premier round et chaque fois que le score stagne.

Avec des remerciements particuliers à Misha Khalman pour le développement du skill. Avec des remerciements à Misha Khalman, Michael Segner, Matt Bell et Matt Thanabalan pour leurs relectures, contributions et soutien produit.

## Pourquoi ça compte
Ce billet formalise une méthodologie reproductible (et outillée directement dans Claude Code) pour construire des évaluations fiables et éviter le piège classique du surapprentissage lors de l'optimisation d'applications LLM — un enjeu central pour toute équipe qui déploie des agents ou des produits basés sur des modèles en production.
