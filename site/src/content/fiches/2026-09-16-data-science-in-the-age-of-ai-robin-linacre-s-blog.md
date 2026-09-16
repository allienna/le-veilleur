---
title: "Data Science in the Age of AI | Robin Linacre's blog"
date: 2026-09-16
url: "https://elink56e.dataelixir.com/ss/c/u001.IgA5xx2nQ-1ekHkKegwAeZ4lFMjuPUX_D6yGa5EFAIGH-R6wO9m9XEfvl8oTIUAL2rgBk9qaseYmv475jipn7bcTq0FzOzQYy5W6joTt24dkx9ra1zQvrgi8hfrWi6L9KORXwmZZlVKwXd_M__a9_QGpL_4lFNrP7Yexc3JHW6kpDveBjlbKAvU7l6DBASHvYo1rvc53D_mGZspaqOXJbA/4u2/JDdLB4i8STiLDBQh8-3HAQ/h3/h001.cP31S-L8rAa5oVNtqyM2wCCHOMLeqPBjtQiv3tSaOaw"
authors: ["Robin Linacre"]
keywords: ["agents IA", "boucle de feedback", "data science", "vérification", "travail agentique"]
theme: "IA"
tone: "opinion"
used_in: ["2026-09-16"]
---

## Résumé
Robin Linacre, data scientist depuis plus d'une décennie, explique que l'essor des LLM a bouleversé son métier plus qu'aucune autre évolution technologique auparavant : il code désormais à peine. Il défend l'idée que le rôle du data scientist devient celui de guider des agents IA vers de bonnes solutions grâce à des boucles de feedback robustes, plutôt que d'écrire du code lui-même. À travers neuf exemples tirés de ses propres projets (Splink, uk_address_matcher, un jeu vidéo, une bibliothèque d'écriture cursive...), il montre comment des prompts courts peuvent déclencher un travail agentique considérable, à condition que la vérification soit fiable. Il anticipe une évolution vers des agents plus nombreux, plus autonomes et plus durables, la vraie valeur du data scientist se déplaçant vers le jugement et la capacité à accélérer la boucle de feedback avec les clients.

## Points clés
- La compétence centrale du data scientist n'est plus d'écrire du code mais de construire des boucles de feedback fiables qui guident les agents IA et évitent le « slop » et les hallucinations.
- Plus la boucle de feedback est solide, plus la tâche déléguée à l'agent peut être grande — illustré par des cas allant d'une optimisation de performance (25 % de gain pour 15 lignes ajoutées) à un portage complet vers le web en moins de 10 prompts.
- Quand la vérification automatique est difficile (ex. écriture cursive, esthétique visuelle), il faut réintégrer un humain dans la boucle via des outils dédiés plutôt que de laisser l'agent seul.
- Des projets de recherche semi-autonomes (nouvelle fonction phonétique, amélioration d'un géocodeur) montrent que les agents peuvent mener des semaines de travail exploratoire, avec des résultats parfois négatifs mais instructifs.
- À court terme, l'auteur anticipe des agents cloud, « always-on », plus nombreux et dotés d'une meilleure mémoire de contexte — chaque data scientist finissant par gérer une équipe d'agents.
- La valeur humaine se déplace vers le jugement métier et la capacité à accélérer, en parallèle, la boucle de feedback avec les clients.

## Analyse approfondie
Les data scientists mobilisent les meilleurs outils et technologies pour maximiser la valeur des données. Je suis dans la profession depuis plus d'une décennie, et avec le recul, il est surprenant de voir à quel point les choses ont évolué lentement pendant l'essentiel de cette période. Les outils ont évolué, mais au fond, mon travail quotidien se ressemblait en 2013 et en 2023.

L'essor des LLM a été le plus grand bouleversement que j'aie connu dans ce métier. Le travail a radicalement changé. Je passais autrefois le plus clair de mon temps à programmer, mais au cours de la dernière année, je n'ai pratiquement pas écrit une seule ligne de code [1].

Comment l'IA a-t-elle changé notre rôle ? **Notre travail consiste de plus en plus à guider l'IA vers de bonnes solutions, plutôt qu'à écrire nous-mêmes le code.** [2] Le défi consiste à traduire les problèmes en boucles de feedback qui orientent de façon fiable les agents dans la bonne direction.

Ces boucles de feedback sont essentielles à un usage efficace de l'IA : elles constituent notre principale défense contre le « slop » et les hallucinations, et font de la fiabilité des résultats une affaire de compétence plutôt que de chance.

Cette nouvelle compétence met l'accent sur le jugement et l'esprit critique. Mais à un niveau plus général, notre travail reste le même. Que nous écrivions le code nous-mêmes ou que nous guidions un agent, l'élément crucial est de comprendre ce que l'on vise et de savoir à quoi ressemble un bon résultat.

Heureusement, les data scientists sont bien placés pour concevoir ces boucles, car les compétences sous-jacentes leur sont familières : construire des solutions a toujours été un processus itératif consistant à mener des expériences et à évaluer rigoureusement les performances.

Le système de feedback lui-même n'a que rarement besoin d'être développé explicitement : les agents IA cherchent déjà du feedback sans qu'on le leur demande — ils exécutent des tests, en écrivent de nouveaux, inspectent les sorties et enquêtent sur les échecs. Notre rôle consiste à juger si ce feedback constitue une bonne mesure de succès, et à découper le problème en tâches de taille appropriée selon la meilleure boucle de feedback que l'on puisse imaginer. **Plus la boucle de feedback est solide, plus la tâche que l'on peut déléguer en toute sécurité est grande.**

Voyons à quoi cela ressemble en pratique, à travers une série d'exemples concrets qui illustrent les manières les plus efficaces que j'ai trouvées d'utiliser des agents, allant de simples améliorations de performance à des projets de recherche semi-autonomes.

Dans ces exemples, portez attention à l'interaction entre deux éléments de la boucle de feedback :
- Comment l'agent parvient à générer de nouvelles preuves spécifiques à la tâche (absentes de ses données d'entraînement), généralement en exécutant du code.
- Comment l'agent vérifie qu'il est sur la bonne voie.

**Exemple 1 — Optimisation de performance de Splink.** Mon projet principal est Splink, une bibliothèque Python d'appariement d'enregistrements (record linkage) comptant plus de 20 000 lignes de code.

J'ai donné à l'agent un prompt ouvert lui demandant de profiler le temps d'exécution du code de Splink et de trouver des optimisations permettant d'accélérer le code sans changer les résultats.

Je lui ai demandé d'essayer différentes options jusqu'à en trouver une qui ne nécessite que de petits changements de code pour un grand bénéfice. Il a travaillé seul pendant une heure et a fait le genre de choses que j'aurais faites moi-même : profilage, analyse du flamegraph et identification des problèmes.

Il est revenu avec un gain de vitesse de 25 % dans la partie Python, avec seulement 15 lignes de code supplémentaires.

C'est le type de travail agentique que je préfère : un prompt court entraîne un travail considérable de la part de l'agent, mais le résultat final est un changement petit et ciblé.

Dans cet exemple, les nouvelles preuves générées par l'agent sont :
1. Les résultats de profilage, tels que le nombre d'appels de fonctions et les temps d'exécution.
2. Les résultats de benchmarking, qui mesurent la vitesse après les changements apportés au code.

La vérification consiste à s'assurer que la suite de tests de Splink passe.

**Exemple 2 — Mise à jour du code d'exemple vers Splink v5.** Nous travaillons sur la version 5 de Splink, dont la sortie est prévue prochainement. Nous disposons de beaucoup de code d'exemple écrit dans l'ancienne version qui doit être mis à jour. C'est une tâche minutieuse, car une partie du code se trouve dans des extraits au sein de docstrings et de documentation Markdown. J'estime que cela aurait pris plus d'une semaine de travail à la main.

Dans cet exemple, j'ai demandé à l'agent de rassembler des preuves en examinant chaque pull request menant à Splink v5, afin de générer un document résumant les changements nécessaires au code. Je lui ai ensuite demandé d'utiliser ce document comme guide pour mettre à jour le code.

La vérification était simple : le code utilisant Splink v5 donnait-il la même réponse que Splink v4 ?

**Exemple 3 — Portage de DoubleMetaphone en C++.** J'ai porté la fonction DoubleMetaphone d'Apache Commons (Java) vers le C++ afin qu'elle puisse être utilisée dans une extension DuckDB. C'est simple à vérifier car la fonction Java dispose d'une suite de tests : il suffit de s'assurer que tous les tests passent. De plus, j'ai demandé à l'agent de générer les encodages DoubleMetaphone de plusieurs milliers de mots à l'aide de la fonction Java, puis de vérifier que le portage C++ qu'il avait écrit donnait exactement le même résultat.

**Exemple 4 — Portage de Splink vers le navigateur.** Une démonstration plus impressionnante de la puissance des agents est que j'en ai chargé un de porter Splink vers le navigateur web à l'aide de DuckDB WASM, un travail que j'estime à au moins un mois. Il a réussi à le faire en moins de 10 prompts. Vous pouvez trouver le résultat ici. Bien qu'encore très expérimental, c'est déjà utile car cela fournit une interface graphique interactive permettant à l'utilisateur d'explorer les résultats, ce qui est très utile pour comprendre le fonctionnement de Splink.

**Exemple 5 — Équilibrage d'un jeu de tower defense.** Je construis un jeu de tower defense à deux joueurs pour mon fils, avec une particularité : pour construire des tours à canon et des monstres, il faut résoudre des problèmes de calcul mental.

Un problème clé dans ce type de jeu est l'équilibrage. On ne veut pas qu'une seule arme ou une seule stratégie domine. Mais équilibrer le jeu est difficile, avec 7 types de canons, chacun disposant de 16 améliorations.

J'ai demandé à l'agent de rassembler des preuves en faisant jouer 1 000 parties contre lui-même, en calculant des statistiques sur la force de chaque canon après chaque partie, et en rééquilibrant jusqu'à ce qu'aucune stratégie ne soit totalement dominante.

C'est un autre exemple de mon type de travail agentique préféré : un prompt simple entraîne une quantité de travail énorme. L'agent a dû construire un joueur artificiel capable de jouer contre lui-même, puis exécuter de nombreux scripts gourmands en CPU et en analyser les résultats. Mais le changement final apporté au code du jeu était minime : il s'agissait simplement de modifier les constantes de dégâts de chaque canon [3].

**Exemple 6 — Recherche sur une nouvelle fonction phonétique.** Dans cet exemple, j'ai utilisé des agents pour mener un projet de recherche visant à déterminer si l'on pouvait utiliser le machine learning pour améliorer DoubleMetaphone et Soundex. Ce sont des fonctions largement utilisées en appariement d'enregistrements pour déterminer si deux mots orthographiés différemment pourraient se prononcer de la même façon.

Une fonction idéale devrait avoir deux propriétés importantes, comme le montre l'image suivante :
- Si les noms se prononcent de la même façon, le code doit correspondre exactement.
- Si les noms se prononcent différemment, le code doit être différent.

La question que je me posais était de savoir si nous pouvions apprendre une nouvelle fonction qui surpasserait DoubleMetaphone. Plutôt que de coder les règles à la main, l'idée était de laisser l'ordinateur les optimiser à partir des données.

J'ai orienté l'agent pour qu'il commence par collecter le plus de données possible sur les mots qui se prononcent de la même façon : des paires de mots qui devraient partager le même code, et des paires qui ne le devraient pas. Par exemple, une source était un dictionnaire lisible par machine comportant des guides de prononciation. L'agent pouvait l'utiliser pour créer des paires « qui se prononcent de la même façon » et des paires « qui se prononcent différemment », avec un jeu d'entraînement et un jeu de test. De même, je lui ai demandé de trouver des listes de noms de lieux dans d'autres pays avec différentes translittérations.

J'ai ensuite fixé des contraintes : nous cherchions à apprendre un ensemble de règles pouvant être exprimées avec une logique de contrôle simple, exprimable en SQL, afin d'optimiser la précision.

En le guidant sur environ 20 prompts, l'agent a pu mener ce projet de recherche à ma place, remplaçant sans doute deux semaines ou plus de travail humain. Il a découvert une fonction qui surpassait nettement Soundex, et surpassait légèrement DoubleMetaphone.

En ce sens, ce fut un échec : l'amélioration n'était pas suffisante pour justifier son adoption. Mais j'ai beaucoup appris : que Soundex est un classifieur médiocre comparé à DoubleMetaphone, et qu'il existe une limite supérieure de précision due à l'ambiguïté inhérente à la prononciation.

**Exemple 7 — Amélioration d'uk_address_matcher.** Un second exemple de recherche semi-autonome portait sur l'amélioration de la précision d'uk_address_matcher, notre géocodeur gratuit.

Nous disposons de centaines de milliers de lignes de données étiquetées, et donc chaque fois que nous avons une idée de nouvelle fonctionnalité à concevoir, ou de nouvelle règle de nettoyage de données, nous pouvons demander à l'agent de faire le travail de bout en bout à notre place.

Dans cet exemple, je me demandais si le concept de « tokens distinctifs » dans une adresse pouvait être utilisé pour améliorer la précision.

J'ai donné à l'agent l'image illustrant ce concept, accompagnée d'un court prompt. Il a implémenté toute la logique nécessaire pour dériver la fonctionnalité, puis a exécuté notre suite de benchmarking pour déterminer si cela améliorait la précision sans réduire la vitesse d'inférence ni trop augmenter la taille du fichier. Le résultat a été une amélioration sans ambiguïté de la précision, et la pull request se trouve ici.

Bien sûr, il faut veiller à ce que l'IA ne surapprenne pas (overfitting) dans ce cas. Le jugement humain a également été important dans cet exemple : en examinant des cas réels de vrais et de faux positifs, j'ai pu constater que la fonctionnalité avait un sens intuitif en tant que signal important, ce qui a renforcé ma confiance dans le fait qu'elle pouvait réellement améliorer la précision.

C'est un autre bel exemple d'un petit changement de code précieux, résultant d'un travail important de collecte de preuves et de vérification effectué par l'agent pour notre compte. Je dois ajouter que nous avons mené de nombreuses autres expériences similaires qui, elles, ont échoué !

**Exemple 8 — Bibliothèque d'écriture cursive.** Je travaille sur une bibliothèque d'écriture cursive pour mes enfants, destinée à alimenter des applications éducatives. C'est un travail très visuel, où tout dépend de la forme des lettres et des liaisons entre elles. Les LLM, du moins pour l'instant, sont plutôt faibles sur ce point.

On peut le constater en comparant deux prompts : dans le premier, nous demandons à un modèle de pointe de générer la géométrie du mot « cursive ». Le résultat est un échec cuisant. Le second est le résultat final obtenu en plaçant un humain dans la boucle.

Cette image résume assez bien pourquoi tout se passe mal lorsque l'on ne parvient pas à intégrer de vérification dans notre travail.

L'incapacité du LLM à distinguer une bonne écriture cursive d'une mauvaise brise la boucle agentique. Il ne peut donc pas se donner de feedback à lui-même, et l'on se retrouve avec le « slop » illustré dans l'image générée uniquement par le LLM.

L'astuce consiste donc à intégrer l'humain dans la boucle de la manière la plus efficace possible. Souvent, on peut utiliser l'IA pour réduire au strict minimum le travail de vérification que l'humain doit effectuer. Dans cet exemple, j'ai construit une série d'applications jetables, notamment un éditeur de courbes de Bézier pour les lettres, un analyseur de liaisons (join analyser) et un éditeur de crénage (kerning editor), afin de m'insérer moi-même dans la boucle de vérification. Vous pouvez en lire davantage dans un billet de blog séparé.

**Exemple 9 — Visualiser un algorithme.** Un second exemple consistant à mettre un humain dans la boucle est l'utilisation de l'IA pour visualiser et comprendre un algorithme, une approche que j'ai mise à profit pour comprendre les propriétés des tries tolérants aux fautes (fault-tolerant tries) pour l'appariement d'adresses.

**Vers où cela nous mène-t-il ?** Le rythme d'amélioration des capacités rend impossible de le savoir à long terme.

Mais à court terme — au cours de la prochaine année ou des deux prochaines années — je pense que la tendance ira vers des agents plus nombreux et fonctionnant plus longtemps :
- Les agents cloud deviendront la norme, facilitant l'exécution de plusieurs agents dans des environnements séparés et jetables [4].
- Cela se traduit par un sandboxing plus robuste, réduisant le besoin d'approbations, et permettant donc un travail autonome plus long.
- Les agents « always-on » deviendront plus courants, triant les rapports de bugs et menant des projets de recherche de longue durée, comme l'optimisation de la précision de modèles de machine learning.
- Les agents deviendront meilleurs dans la gestion de la mémoire et du contexte, se souvenant bien davantage de l'historique complet d'un projet : expériences passées, succès, échecs, conventions et préférences du projet.
- Les agents deviendront meilleurs pour comprendre l'intention et reconnaître quand ils s'écartent de la trajectoire ou ont besoin d'une intervention de l'utilisateur.

Le résultat est que les data scientists individuels géreront de plus en plus une équipe d'agents.

Je trouve tout cela à la fois inquiétant et enthousiasmant, à parts égales. Mais en prenant du recul, la programmation a toujours été un moyen plutôt qu'une fin. Le prolongement naturel de la question « comment mon agent sait-il qu'il fait du bon travail » est « comment sais-je moi-même que je fais du bon travail ».

La valeur des data scientists réside toujours dans notre créativité et notre jugement : comprendre les problèmes métier, les traduire en implémentations techniques, et travailler de manière itérative avec nos clients vers de meilleures solutions.

À mesure que l'implémentation devient moins coûteuse, nous devrons accepter que l'entreprise attende légitimement de nous que nous livrions davantage, plus vite. Si la nouvelle compétence technique consiste à construire des boucles de feedback agentiques serrées, la compétence de plus haut niveau pour les data scientists sera aussi d'accélérer la boucle de feedback avec nos clients, afin de pouvoir livrer des produits plus utiles, plus rapidement.

**Notes**
1. Malgré cela, je pense que mes compétences en programmation restent aussi précieuses que jamais. Je continue à relire beaucoup de code et à concevoir l'architecture, mais j'écris rarement les lignes individuelles. Pour en savoir plus, voir Simon Willison ici et ici.
2. Ceci est une reformulation d'idées évoquées dans le billet « AI Zealotry » de Matt Rocklin.
3. Bien sûr, ce n'était pas parfait — l'agent n'a pas trouvé de stratégies plus avancées permettant de casser le jeu, comme construire un « labyrinthe » de murs.
4. J'apprécie beaucoup ChatGPT Work pour cela (la version Cloud). Je préfère cette interface à celle d'un IDE pour de nombreuses tâches, et je pense que cette application est un bon indicateur de la direction que prend l'outillage.

## Pourquoi ça compte
Ce témoignage de terrain, rare et concret, illustre comment les data scientists redéfinissent leur métier autour de la conception de boucles de feedback pour piloter des agents IA plutôt que d'écrire du code — une tendance clé à suivre pour quiconque observe l'évolution des rôles techniques à l'ère agentique.
