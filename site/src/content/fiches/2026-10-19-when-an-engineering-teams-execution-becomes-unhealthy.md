---
title: "When an Engineering Team’s Execution Becomes Unhealthy"
date: 2026-10-19
url: "https://leadershipintech.com/links/23499/3d78f33c-7ca0-4e03-9c70-68e56918a4cd/email"
keywords: ["gestion d'équipe", "exécution", "priorisation", "charge de travail", "estimations", "leadership technique"]
theme: "Leadership"
tone: "opinion"
used_in: ["2026-10-19"]
---

## Résumé
L'article explore comment une équipe d'ingénierie passe d'un état sain à un état malsain sur le plan de l'exécution : trop de projets démarrés et peu finis, délais qui glissent en continu, priorités changeantes et tout devenant « urgent ». L'auteur soutient que la réponse ne consiste pas à pousser l'équipe à travailler plus dur, mais à diagnostiquer et corriger le système qui l'entoure. Il propose une méthode en plusieurs étapes : réduire le travail en cours, examiner comment le travail entre dans le système, rendre les priorités explicites, et aider l'équipe à mieux estimer et à comprendre le poids de ses estimations. L'idée centrale est que la prévisibilité, et non la perfection du plan, est le véritable indicateur de santé d'une équipe.

## Points clés
- Une exécution malsaine se reconnaît à des symptômes précis : trop de travaux commencés et peu terminés, délais qui glissent sans cesse, priorités instables, ou à l'inverse tout devenant urgent.
- Le rôle du leader n'est pas de faire travailler l'équipe plus fort, mais de modifier le système autour d'elle pour restaurer une livraison prévisible.
- Limiter le travail en cours (WIP) et traiter l'équipe comme une file d'attente (queue) permet de créer de l'espace pour terminer ce qui est déjà commencé avant d'accepter de nouvelles demandes.
- Un système de priorisation explicite (par exemple une grille de sévérité pour les bugs non planifiés comme les « P0 ») évite le changement constant de priorités basé sur l'urgence perçue ou le poids de la personne qui demande.
- Estimer un problème encore mal compris donne une fausse impression de certitude ; il faut d'abord réduire l'inconnu (investigation technique, preuve de concept) avant de produire une estimation utile à la décision.
- La prévisibilité, pas l'absence d'imprévus, est le véritable signe de santé d'une équipe : les glissements, changements de priorités et incidents de production occasionnels sont normaux tant que l'équipe reste capable de livrer de manière constante.

## Analyse approfondie
Une équipe peut rapidement passer d'un état sain à un état malsain.

Il y a un trimestre, une équipe pouvait être saine et bien équipée pour atteindre ses objectifs ; ce trimestre-ci, elle pourrait être passée de saine à malsaine.

Plusieurs facteurs peuvent rendre une équipe malsaine, par exemple :

- Une équipe peut être malsaine parce que son exécution est malsaine.
- Une équipe peut être malsaine parce que ses membres sont en mauvaise santé (c'est-à-dire épuisés, malades, avec un moral bas, etc.).
- Une équipe peut être malsaine parce qu'elle manque des compétences ou des talents nécessaires pour atteindre son objectif.
- Une équipe peut être malsaine parce que ses fondations techniques sont malsaines.
- Une équipe peut être malsaine parce que sa relation avec les parties prenantes (stakeholders) est tendue et malsaine.
- Une équipe peut être malsaine parce qu'elle manque de direction ou que sa direction est floue.
- Et ainsi de suite.

Cet article se concentrera sur le premier point : quand l'exécution d'une équipe devient malsaine, et comment l'en sortir.

Lorsqu'une équipe tombe dans un état où l'exécution est malsaine, elle peut commencer beaucoup de choses mais n'en terminer que peu. Trop de projets sont lancés, mais peu sont menés à terme. Un autre signe d'exécution malsaine est le glissement continu des délais.

Les priorités peuvent aussi changer trop fréquemment, maintenant une liste de travaux commencés qui ne cesse de grandir, sans fin.

Les délais peuvent finir par ressembler à des dates arbitraires sorties de nulle part — des dates auxquelles personne ne croit vraiment ni ne prête attention. Quand cela arrive, les estimations deviennent dénuées de sens, car il n'y a plus de lien réel entre l'estimation, le délai et ce que l'équipe livre réellement.

À l'autre extrême, tout devient urgent. Chaque demande doit être traitée pour hier. L'équipe fonctionne continuellement au-delà de sa capacité pendant que de nouvelles demandes continuent de s'accumuler. Cela peut être particulièrement difficile à l'ère de l'IA, où les attentes quant à la vitesse à laquelle les équipes peuvent produire du code ont considérablement augmenté, sans que les systèmes, processus et capacités nécessaires pour soutenir, réviser, maintenir et exploiter ce code suivent le même rythme.

Lorsqu'une équipe n'est pas capable d'exécuter les objectifs fixés à un rythme prévisible et attendu, et qu'elle est incapable de soutenir ces objectifs compte tenu de la capacité et des ressources dont elle dispose, l'équipe se trouve probablement dans un état où l'exécution est malsaine.

Le mot important ici est *prévisibilité*. L'exécution ne signifie pas nécessairement que tout se déroule toujours comme prévu. Parfois, des projets glisseront, et ce n'est pas grave. Plus encore, les priorités changeront, et ce n'est pas grave non plus. Des problèmes de production imprévus surviendront, et c'est également acceptable.

Mais une exécution saine signifie que l'équipe peut prendre des engagements raisonnables, concentrer sa capacité, identifier quand quelque chose dérape, et finalement livrer une quantité significative de travail pour l'entreprise de manière constante.

Mais comment aider une équipe à sortir d'un état d'exécution malsain ?

### Diagnostiquer le système

La première étape consiste à comprendre où le système se dégrade et ce qui est responsable de l'état actuel de l'équipe.

Lorsqu'une équipe ne livre pas de manière prévisible, la réaction naturelle est d'ajouter plus de process : introduire un nouveau workflow, ajouter plus de réunions, demander de meilleures estimations, ou simplement pousser l'équipe à livrer davantage.

Mais j'ai un jour lu un post d'un VP Engineering à qui l'on avait demandé ce qu'il ferait si ses équipes d'ingénierie ne livraient pas de manière prévisible. Sa réponse m'est restée en tête. Il a dit que son travail n'était pas de faire travailler l'ingénierie plus dur, mais de changer le système autour de l'équipe pour qu'elle livre de façon prévisible.

Je pense que c'est la bonne façon d'aborder le problème. Avant de demander à l'équipe de faire plus, il faut regarder l'environnement dans lequel elle travaille. Qu'est-ce qui crée le goulot d'étranglement ? Où le travail reste-t-il bloqué ? Qu'est-ce qui rend difficile pour l'équipe de terminer ce qu'elle commence ?

Une des premières choses que je regarde, c'est le travail en cours (work in progress). S'il y a trop de WIP, il faut donner un peu d'air à l'équipe. Arrêter d'ajouter du nouveau travail et créer de l'espace pour que l'équipe termine ce qui est déjà ouvert.

Pensez à un système de file d'attente (queue). Dans de nombreuses architectures logicielles, les files d'attente existent parce que le travail arrive plus vite qu'il ne peut être traité immédiatement. La queue offre un moyen de gérer ce travail, de contrôler les priorités et de s'assurer que les workers ne sont pas submergés en essayant de tout traiter à la fois.

Les équipes ne sont pas si différentes. Lorsque les demandes de travail dépassent constamment la capacité d'une équipe, la réponse n'est pas de continuer à empiler plus de travail sur l'équipe. Il faut un mécanisme pour gérer la queue : décider ce qui est traité maintenant, ce qui attend, et ce qui ne sera pas traité du tout.

Il y a peu de valeur à demander à une équipe déjà submergée d'aller plus vite tout en continuant à empiler plus de travail par-dessus. C'est comme regarder quelqu'un suffoquer et lui donner autre chose à porter au lieu de l'aider à respirer.

Cela peut parfois sembler inconfortable. Les parties prenantes peuvent toujours avoir une longue liste de choses qu'elles veulent que l'équipe traite. Mais ajouter plus de travail à une équipe qui a déjà du mal à terminer ce qu'elle a en cours ne fait généralement qu'aggraver le problème.

L'équipe doit d'abord apprendre à sprinter avant de pouvoir courir à nouveau.

Vous pourriez donc temporairement restreindre le focus de l'équipe à un petit nombre de choses déjà en cours et poser des questions plus profondes :

- Que peut-on terminer ?
- Que peut-on arrêter ?
- Qu'est-ce qui nous bloque ?
- Que faut-il pour que ces éléments soient réellement considérés comme terminés ?

Puis, gérez les parties prenantes en les contactant pour leur faire savoir que c'est le défi actuel, voici le diagnostic, et gérez leurs attentes pendant la période où l'équipe reprend son souffle.

### Examiner comment le travail entre dans le système

Une fois que vous avez réduit ou stoppé l'arrivée de nouveau travail dans la queue pour laisser à l'équipe l'espace de se concentrer sur le WIP et de le terminer, regardez plus attentivement comment le travail entre dans la queue en premier lieu.

Vous utilisez peut-être Jira ou un autre outil de gestion de tâches, mais l'outil lui-même n'est pas l'élément important. Ce qui compte davantage, c'est le système qui se trouve derrière.

- Comment le travail passe-t-il d'une idée à quelque chose que l'équipe s'engage réellement à faire ?
- Qui décide de ce qui est prioritaire ?
- À quelle fréquence les priorités changent-elles ?
- Comment une tâche passe-t-elle de « à faire » à « en cours » ? Quelqu'un peut-il introduire du nouveau travail dans le sprint actuel de l'équipe ?
- Que se passe-t-il quand une partie prenante senior arrive avec quelque chose d'urgent ?
- Existe-t-il un processus de planification prévisible et un ordre clair dans lequel le travail est priorisé ?

C'est quelque chose que j'ai vécu moi-même et dont j'ai appris.

Une équipe peut devenir si performante pour livrer et réagir rapidement aux demandes que tout le monde est content. Il suffit de faire une demande, et vous êtes certain qu'elle sera traitée une heure plus tard.

L'équipe est félicitée pour être motivée, fiable, digne de confiance, et pour faire avancer les choses. Sur le moment, le moral est au plus haut.

Le problème, c'est que cela peut se produire si souvent que le système conçu pour contrôler la façon dont le travail entre dans la queue disparaît progressivement.

Plus rien n'est planifié ou réfléchi clairement. Le travail est simplement fait rapidement, et la priorisation disparaît peu à peu.

Avant même de s'en rendre compte, il y a trop de demandes et trop de travail, et l'équipe commence à peiner, voire à s'épuiser.

Ce n'est pas que l'équipe soit devenue moins compétente. En fait, c'est souvent l'inverse qui est vrai. Elle est devenue si bonne pour répondre aux demandes entrantes que le système conçu pour protéger sa capacité et assurer une priorisation adéquate s'est progressivement érodé.

Et une fois que cela se produit, chaque demande commence à ressembler à une priorité qui doit être traitée immédiatement.

Si le flux de travail ne suit pas un chemin prévisible permettant des équilibres et des contrôles, ce n'est qu'une question de temps avant que les gens ne commencent à se sentir submergés, et le résultat, plus tôt qu'on ne le pense, est une équipe malsaine.

### Rendre les priorités explicites

L'exécution ne peut pas être prévisible si tout est urgent et important.

Une équipe ne peut pas exécuter de manière prévisible si elle ne sait pas ce qui est important lorsqu'il y a plusieurs choses sur lesquelles elle pourrait travailler. S'assurer qu'il existe une compréhension partagée de ce qui est important et de ce qui ne l'est pas est crucial.

Cela signifie aussi créer un mécanisme pour traiter les nouvelles choses qui surviennent pendant que l'équipe exécute autre chose.

Les bugs sont souvent non planifiés lorsqu'ils apparaissent et peuvent survenir en plein milieu de l'exécution d'autre chose. S'il n'y a pas de mécanisme pour décider quel niveau de bug nécessite que l'équipe arrête ce qu'elle est en train de faire, on peut rapidement se retrouver avec un changement de contexte fréquent qui entrave l'exécution.

Il y a souvent des problèmes ou des bugs qui semblent importants. L'urgence avec laquelle ils sont soulevés, et la personne qui les soulève, peuvent avoir un certain poids. Les équipes peuvent avoir l'impression qu'elles doivent arrêter ce qu'elles font pour corriger le problème immédiatement.

À la place, définissez un cadre de priorisation du travail non planifié.

Par exemple, vous pourriez définir les bugs P0 comme des problèmes ayant un certain niveau d'impact sur les utilisateurs ou l'entreprise, accompagnés d'un processus clair sur la façon dont l'équipe doit réagir lorsque cela se produit.

Par exemple :

Les définitions exactes dépendront de l'équipe et du produit. Ce qui compte, c'est que chacun comprenne ce que signifie chaque niveau de priorité et, plus important encore, quelle réponse il exige.

En définissant cela, on force les gens à comprendre d'abord l'impact d'un problème plutôt que de simplement réagir à son urgence.

Connaître l'impact aide l'équipe à réagir de manière appropriée et rend la communication autour du problème beaucoup plus facile. Cela protège également l'équipe contre des changements constants de priorités basés sur qui a soulevé un problème ou avec quelle urgence il a été communiqué.

### Aider l'équipe à mieux estimer et à comprendre le poids que portent les estimations

Une fois que le flux de travail est plus sain, regardez comment l'équipe pense aux estimations qu'elle fournit et aidez-la à comprendre le poids que ces estimations portent.

Je détestais les estimations en tant qu'ingénieur. Une des choses que je détestais le plus était qu'on me demande : *« Combien de temps cela va-t-il prendre ? »* alors que je ne savais pas encore comment j'allais résoudre le problème. Parfois, je ne savais même pas si le problème était résoluble de la façon dont nous le voulions.

Comment aurais-je pu donner à quelqu'un un chiffre pertinent ?

En gagnant en expérience, j'ai commencé à voir ce qui se cache derrière une estimation.

Les estimations aident les entreprises à prendre des décisions et des compromis : quel problème résoudre, sur quelle idée miser, que faire maintenant par rapport à plus tard, et si la valeur attendue de quelque chose vaut le coût et le temps nécessaires pour le construire.

Pour ces décisions, une estimation est l'une des données nécessaires pour comprendre l'investissement impliqué.

Mais estimer ce qui n'est pas connu est également dénué de sens. Si l'équipe ne comprend pas encore le problème, comment il sera résolu, ou si la solution proposée est techniquement faisable, mettre un chiffre dessus peut créer un faux sentiment de certitude.

Dans ces situations, le travail avant l'estimation devrait être de rendre l'inconnu connu.

Cela peut signifier faire une investigation technique, une phase de découverte, ou une preuve de concept (proof of concept). L'objectif n'est pas nécessairement d'éliminer toute incertitude. C'est d'en réduire suffisamment pour que l'équipe puisse fournir une estimation utile à la prise de décision.

Un délai ne devrait pas simplement être une date remise à l'équipe et transformée en engagement. L'équipe devrait comprendre ce que représente ce délai, quelles hypothèses se trouvent derrière, et quels compromis sont disponibles si l'estimation et le délai ne s'alignent pas.

Et enfin, elle devrait comprendre qu'elle est responsable des estimations qu'elle fournit.

### Conclusion

Lorsque l'exécution devient malsaine, la réponse n'est pas nécessairement de demander à l'équipe de travailler plus dur, d'ajouter plus de process, ou d'augmenter la pression.

La première responsabilité du leader est de comprendre ce qui se passe dans le système.

Y a-t-il trop de travail en cours ? Trop de travail entre-t-il dans le système ? Les priorités sont-elles floues ? Les interruptions tirent-elles constamment l'équipe loin de ce à quoi elle s'est engagée ? Demande-t-on aux gens d'estimer un travail qu'ils ne comprennent pas encore ? Et les gens comprennent-ils à quoi servent leurs estimations ?

Une fois que vous comprenez ce qui cause le problème, vous pouvez commencer à changer le système autour de l'équipe.

*Lecture très intéressante. On observe généralement ce phénomène lorsque les parties prenantes traitent chaque demande comme une urgence. Pousser les équipes à aller plus vite sans périmètre défini crée du frottement (drag).*

*Leur niveau cognitif de base chute, car elles doivent gérer la queue au lieu de construire l'architecture du système.*

*On élimine la latence décisionnelle lorsqu'on parvient enfin à transformer une livraison prévisible en un atout structurel.*

*Petite question : comment vous assurez-vous que les parties prenantes respectent ces limites ?*

## Pourquoi ça compte
Ce texte offre un cadre concret pour diagnostiquer et corriger les dérives d'exécution dans les équipes d'ingénierie, un sujet récurrent en leadership technique, d'autant plus pertinent dans un contexte où l'IA accélère la production de code sans que les capacités de support suivent. Il est utile en veille tech pour nourrir des réflexions sur la gestion de la charge de travail, la priorisation et la culture d'équipe plutôt que sur un sujet purement technologique.
