---
title: "What’s Going To Matter In 2027 For Data Engineers?"
date: 2026-11-23
url: "https://open.substack.com/pub/seattledataguy/p/whats-going-to-matter-in-2027-for?utm_source=multiple-personal-recommendations-email&utm_medium=email&token=eyJ1c2VyX2lkIjo0NzU1OTI2MjgsInBvc3RfaWQiOjIyMjczOTE4NiwiaWF0IjoxNzk1MzcxMjQ2LCJleHAiOjE3OTc5NjMyNDYsImlzcyI6InB1Yi0yMTEwNSIsInN1YiI6InBvc3QtcmVhY3Rpb24ifQ.d8ewYa6JjMo7Ji7OOHrK5VWNrU27J-JwVND0K-nj5rU"
authors: ["Ben (SeattleDataGuy)"]
keywords: ["ingénierie des données", "modélisation de données", "IA générative", "confiance dans les données", "knowledge graph"]
theme: "Data"
tone: "opinion"
used_in: ["2026-11-23"]
---

## Résumé
Dans cette newsletter, Ben (SeattleDataGuy), consultant en infrastructure de données, dresse un bilan des tendances observées en 2026 chez les équipes data (startups, PME établies, Fortune 500) et anticipe ce qui comptera en 2027. Il soutient que l'essor des outils d'IA type Claude Code ne supprime pas le besoin de modélisation de données ni de compréhension métier, mais déplace le goulot d'étranglement : il ne s'agit plus de produire des analyses plus vite, mais de prouver qu'on peut leur faire confiance. Il insiste sur le fait que la connaissance métier critique reste souvent tacite, dispersée dans la tête des employés et mal capturée par les ERP. Il appelle les équipes data à davantage aligner donnée et métier, notamment via des knowledge graphs intégrés aux workflows d'analyse.

## Points clés
- Les LLM (Claude Code, etc.) sont passés d'outils expérimentaux à des outils utilisés quotidiennement par les équipes, changeant le volume et la nature du travail produit.
- Les tendances diffèrent selon la taille d'entreprise : startups agiles avec des "analystes LLM", PME établies avec des projets greenfield plus lents côté opérations physiques, Fortune 500 avec des données éclatées entre multiples plateformes et instances SAP.
- La modélisation des données reste essentielle car une grande partie de la connaissance métier critique (clients, commandes, fret, sinistres santé) n'est que partiellement documentée et vit surtout dans la tête de quelques personnes.
- Le vrai goulot d'étranglement en 2027 ne sera plus la vitesse de production des analyses, mais la capacité à prouver leur fiabilité et obtenir l'adhésion ("buy-in") du métier.
- Les équipes devront davantage aligner donnée et métier, potentiellement via des knowledge graphs intégrés à l'analyse plutôt que de simples catalogues de données.
- L'auteur anticipe une possible évolution des intitulés de poste (AI engineer, FDE) sans changement fondamental du cœur du métier de data engineer.

## Analyse approfondie
Salut, futurs et actuels Data Leaders, c'est Ben 👋

L'année touche rapidement à sa fin. Dans cet article, je voulais donc évoquer certaines des tendances que j'ai observées en 2026 et ce que je prévois que les équipes data feront en 2027.

Avant d'entrer dans le vif du sujet, je voulais parler d'autre chose sur laquelle de nombreuses équipes data passent encore des mois (voire des années) : les migrations. Passer d'une plateforme ou d'un outil de pipeline de données à un autre. Si vous avez un projet de migration à venir, ou un projet que vous repoussez depuis longtemps, j'aimerais en discuter avec vous. L'un de mes objectifs pour 2027 est de rendre les migrations beaucoup moins pénibles et chronophages ; donc si vous envisagez un projet de migration de plus de 9 mois, parlons-en !

Maintenant, entrons dans le sujet !

J'ai quitté Facebook il y a une demi-décennie pour me lancer dans le conseil en infrastructure de données.

Ces cinq années ont débuté à ce qui était probablement le pic du « modern data stack », et son déclin progressif. Nous nous retrouvons maintenant, d'une manière ou d'une autre, dans l'ère Claude Code (ou quel que soit le nom qu'on lui donnera plus tard).

Quand ChatGPT est sorti, je me souviens l'avoir essayé. J'avais aussi testé Microsoft Copilot et je trouvais amusant qu'il complète automatiquement mon code.

Puis Claude Code est arrivé, et je pense que c'est à ce moment-là que j'ai vraiment commencé à remarquer le changement. Les LLM sont passés d'outils que les gens testaient à des outils sur lesquels les équipes s'appuyaient quotidiennement.

Je recevais des e-mails de deux à trois paragraphes de personnes dont j'avais plutôt l'habitude de recevoir 2-3 phrases.

Aujourd'hui, nous voyons arriver les Claude Dashboards et tout ce qui s'annonce pour 2027. Et il est difficile de ne pas se demander ce que tout cela signifie pour les équipes data.

Quel est le rôle d'une équipe data dans cette véritable ère moderne ? Le modern data stack était « disruptif », en quelque sorte, mais au final, nous construisions toujours des pipelines, modélisions des données et créions des dashboards. Aujourd'hui, nous observons des outils qui pourraient fondamentalement changer la part de ce travail qui est réellement effectuée.

Alors, à quoi ressemblera le travail des équipes data en 2027 ?

### Observations sur les équipes data en 2026

Avant d'aborder 2027, je veux partager quelques observations de 2026.

J'ai eu la chance de travailler avec des entreprises couvrant un large spectre : PME établies, startups, plusieurs entreprises du Fortune 500, et plusieurs universités.

Beaucoup d'entre elles utilisaient Snowflake, Databricks, Airflow, dbt, et bien sûr une dizaine d'autres outils (incluant Claude Code et Codex). Beaucoup utilisaient plusieurs plateformes de données en les connectant entre elles, là où elles jugeaient chaque outil optimal.

Voici comment je résumerais les tendances générales.

1. **Startups** — Elles peuvent adopter les nouvelles tendances beaucoup plus vite que les organisations plus établies. Cela signifie que beaucoup d'entre elles utilisaient l'IA pour créer des « analystes LLM » leur permettant d'explorer plus facilement leurs données. Elles ont aussi généralement des flux de données et métier plus simples. Cela ne veut pas dire que c'était facile ; cela veut simplement dire qu'on pouvait réellement cartographier l'essentiel sur un seul tableau blanc, avec peu de cas particuliers. Dans ces cas-là, les équipes data étaient généralement petites et soudées.
2. **PME établies** — Il existe tant d'entreprises qui existent depuis des décennies, qui dirigent des activités prospères et qui cherchent à améliorer et développer leurs opérations. Beaucoup de ces projets partent de zéro (greenfield). Elles ont parfois besoin de travail pour déterminer quelle est leur donnée « cœur ». Dans certains cas, cela peut être simple si leur activité est numérique, mais je dirais que les opérations plus physiques prennent davantage de temps.
3. **Fortune 500** — Ces entreprises sont évidemment énormes. Si grandes que l'on essaie souvent de relier des données provenant de multiples plateformes. On a des données dans plusieurs instances SAP correspondant à différentes parties de l'entreprise, et celle-ci a probablement acheté toutes les solutions existantes en espérant qu'elles l'aideraient toutes à tirer parti de l'IA.

Premièrement, je ne serais pas surpris de voir de plus en plus de data engineers adopter de nouveaux intitulés comme « AI engineer » ou « FDE ». Je ne dis pas que nos rôles s'y intègrent, mais je ne serais simplement pas surpris.

Une des nombreuses tendances concernant le travail qui doit encore être fait, et que je ne vois pas devenir plus facile tout de suite, c'est la modélisation du métier.

Toutes les entreprises n'ont pas une empreinte numérique suffisamment forte pour être facilement « scrapée » par un LLM puis transformée en modèle de données fonctionnel. Que je travaille avec une startup ou une organisation plus grande, j'ai constaté que chacune avait besoin de quelqu'un pour aller discuter de la manière dont la donnée circule du point A au point B — pas tant le pipeline de données, et pas tant la donnée elle-même.

Mais les clients, les commandes, le fret, les demandes de remboursement de santé. La façon dont ces entités sont traitées, qui les touche et y ajoute ses propres modifications en cours de route, où elles peuvent se perdre ou être rejetées du système, etc. Tout cela n'était souvent que partiellement capturé par les ERP et autres systèmes de référence. Et souvent, les informations cruciales se trouvaient uniquement dans la tête de telle ou telle personne.

Et je pense que c'est l'une des choses qui se perdent dans tout le débat sur l'IA remplaçant les data engineers.

Nous passons tellement de temps à parler de la vitesse à laquelle nous pouvons écrire du code, construire des pipelines et créer des dashboards. Mais dans beaucoup des projets sur lesquels j'ai travaillé cette année, écrire le code n'était pas forcément la partie la plus difficile.

### L'objectif des équipes data

Ce cadrage posé, je pense qu'il est important de d'abord réfléchir à l'objectif global de nombreuses équipes data, en particulier les équipes de data engineering.

Dans le passé, il était facile de confondre notre objectif avec principalement les pipelines de données, les analyses ad hoc, les dashboards et la modélisation de données.

Mais si on y réfléchit vraiment, l'objectif de nombreuses équipes data est de permettre à l'entreprise de répondre plus facilement à des questions pouvant améliorer ses décisions. Cela ne signifie pas toujours indiquer exactement la bonne prochaine décision.

Cela signifie bien créer des couches de données, d'analyses et d'artefacts utilisables pour prendre des décisions plus informées. Y a-t-il des endroits où la donnée peut indiquer la meilleure action suivante ? Oui. Quand il s'agit de décisions stratégiques de plus haut niveau, elle tend généralement à servir de guide.

…Quand elle n'est pas ignorée.

Maintenant que nous connaissons l'objectif, parlons de la façon dont les équipes data vont réussir à l'atteindre à l'avenir.

### Le goulot d'étranglement passe de la création d'analyses à la confiance dans ces analyses

Très bien, nous pouvons écrire des requêtes et construire des graphiques plus vite. Cela ne veut pas dire que l'entreprise va croire les chiffres qu'elle voit. Surtout si tout ce que votre équipe data produit a l'air d'avoir été fait par Claude.

Et je ne pense pas que ce problème va s'atténuer à mesure que de plus en plus d'entreprises commencent à générer leurs propres analyses à partir de quelques échanges rapides avec un chatbot.

Je pense qu'une grande partie du travail des équipes data en 2027 consistera à prouver que leur analyse est correcte et à obtenir l'adhésion de l'entreprise. Chaque fois que nous présentons nos résultats, il y a toujours de nombreuses questions de suivi. Principalement, l'entreprise veut savoir : comment savons-nous que cette conclusion est juste ?

Ce qui est une question légitime. Il est facile de lancer des requêtes. Mais il est difficile de savoir si la donnée sous-jacente ou la logique écrite est réellement valide.

Une équipe data bien organisée peut désormais consacrer plus de temps à démontrer ses conclusions, soit en parlant à de vrais utilisateurs et responsables opérationnels, soit en trouvant de nouvelles sources de données venant étayer ses conclusions.

Des réponses plus rapides, c'est bien. Mais ce que les entreprises et les dirigeants veulent, ce sont des réponses étayées qui leur donnent réellement confiance dans leurs décisions.

### Le besoin de modélisation des données persiste

Je pense qu'au fond, l'entreprise aimerait pouvoir simplement charger toutes ses données dans un emplacement central, puis y poser une IA capable de comprendre comment toutes les réponses qu'elle recherche peuvent émerger, et comment répondre à chacune de ses questions. Une sorte de système « schema-on-read » qui résoudrait toute l'ambiguïté et toutes les nuances propres à son activité.

J'aimerais pouvoir dire « peut-être qu'un jour ce sera vrai ». Mais à cause de nombreux systèmes de référence, des ERP, de la politique interne des entreprises et des flux métier en général, je ne vois pas cela arriver de sitôt.

Il n'y a pas grande incitation à rendre la donnée facile à intégrer quand on vend un ERP ou un CRM. De plus, certains outils veulent simplement être votre outil « tout-en-un », comme Salesforce et SAP.

Et pour ne rien arranger, nous sommes en 2026, et je continue de rencontrer des problèmes comme des données historiques mal capturées ou des champs de données non renseignés, ce qui complique le suivi et le travail.

Bien sûr, vous pourriez jeter tous vos jeux de données dans Claude, et peut-être qu'il arriverait à tout comprendre, mais je ne pense pas que cela se produira en 2027. Du moins, pas en termes d'adoption immédiate.

Je crois que la modélisation de données continuera de jouer un rôle important pour les années à venir, car ce n'est pas un exercice purement technique ; cela demande aussi une compréhension bien plus profonde du métier que ce que la plupart des équipes ont jamais pleinement. La différence que l'on observe déjà se situe du côté de l'implémentation : de nombreuses équipes s'appuient désormais beaucoup plus lourdement sur l'IA pour écrire les transformations elles-mêmes.

### Aligner la donnée et le métier

L'un des défis auxquels de nombreuses entreprises sont confrontées est le fait que la simple analyse des données est rarement suffisante. Il existe des couches de métadonnées qui ne vivent que dans la tête de quelques personnes. Pire encore, chacune de ces personnes ne connaît généralement qu'une petite partition de cette donnée, et ce n'est qu'en commençant à tout assembler que l'on peut identifier des opportunités. Je prévois que les équipes data travailleront davantage à ce niveau en 2027. Certaines se contenteront d'obtenir l'information au moment où elles en ont besoin et de l'utiliser pour leur cas d'usage spécifique.

D'autres construiront des systèmes qui exposent cette information de manière exploitable. Je précise ce dernier point car cette logique mène souvent vers une forme de knowledge graph, et les difficultés que j'y observe fréquemment sont que les équipes data ont du mal à faire en sorte que le knowledge graph soit plus qu'un simple catalogue de données. Il doit être intégré dans votre workflow d'analyse. Quand vous posez une question ou écrivez une requête, la nuance que vous avez capturée doit ressortir. Sinon, elle finit par mourir dans un système qui n'est que partiellement rattaché à votre data warehouse.

Je veux aussi souligner certains pièges lorsque vous vous engagez dans cette voie d'alignement avec le métier. Si vous travaillez dans une grande entreprise, vous pouvez probablement creuser longtemps, à la fois verticalement et horizontalement, pour trouver les personnes liées au problème ou à l'opportunité que vous essayez d'améliorer. Donc, tout comme pour la partie technique de votre analyse, vous devez à un moment donné savoir trancher. Il faut finir par savoir quand vous avez suffisamment d'informations pour agir.

L'objectif ne doit pas être de créer une copie parfaite, un-pour-un, de l'entreprise entière. Il doit être de capturer suffisamment de contexte pour prendre de meilleures décisions et améliorer les processus sur lesquels vous travaillez réellement.

### Réflexions finales

Si vous m'aviez demandé il y a dix ans si nous aurions un jour une boîte de dialogue nous permettant de faire des demandes et d'obtenir des milliers de lignes de code en quelques minutes, j'aurais probablement été trop concentré sur une migration de données pour même envisager ce que vous me proposiez.

Mais nous voilà.

Beaucoup d'entre nous se demandent quel rôle nous jouerons dans quelques années si l'IA continue de progresser. C'est amusant : quand je publiais mes premières vidéos, beaucoup de gens me demandaient si le métier de data engineer était un métier « sûr ». C'est toujours une question difficile à répondre, car les choses changent si fréquemment.

Pendant longtemps, les améliorations et les changements dans le monde de la donnée signifiaient... un data warehouse plus rapide, en quelque sorte.

Même avec autant de changements, je crois qu'il existe toujours un besoin de personnes capables de capturer le métier, de mieux le modéliser, et de construire des processus auxquels l'entreprise fait confiance pour prendre ses décisions.

J'aimerais aussi connaître votre avis. Où va le monde de la donnée en 2027 ?

Merci, comme toujours, de votre lecture.

### Articles qui valent le détour

Des milliers de nouveaux articles sont publiés chaque jour sur le web ! J'ai passé beaucoup de temps à parcourir certains de ces articles, ainsi que TechCrunch et les blogs techniques d'entreprises, et je voulais partager quelques-uns de mes favoris !

#### Les pendules de la donnée
Par Joe Reis

Il y a quelques années, la décentralisation faisait fureur dans le monde de la donnée. Data mesh, propriété par domaine, self-service, pipelines décentralisés, schema-on-read, et le fait de laisser les équipes posséder leurs propres data products étaient censés nous libérer des goulots d'étranglement des équipes et plateformes data centralisées. Avant cela, bien sûr, nous avons passé des décennies à centraliser la donnée dans des entrepôts parce que la donnée dispersée était un désastre. Aujourd'hui, on reparle de plateformes communes, de gouvernance centralisée, de couches sémantiques partagées, de contrats de données, et de la manière de gouverner les agents IA. Ce qui est vieux est de nouveau neuf.

#### Repenser le code généré par IA : une architecture à trois couches pour le développement logiciel

La prochaine grande amélioration du code généré par IA viendra peut-être moins de meilleurs modèles que de meilleures architectures logicielles construites autour de ces modèles.

Chez CodeStrap, nous explorons une architecture construite autour de trois couches complémentaires, conçue pour améliorer la justesse, réduire les coûts de génération, et rendre les logiciels générés par IA plus faciles à maintenir et à faire évoluer.

#### Votre entrepôt de données n'est pas intégré simplement parce que les tables sont au même endroit

De nombreuses entreprises ont réussi à « centraliser » leur donnée sans vraiment l'intégrer.

**Centraliser n'est pas intégrer !**

Intégrer la donnée à travers les systèmes, les équipes et les unités métier reste un défi. C'est aussi de là que vient une grande partie de la valeur de la construction d'un data warehouse.

Un entrepôt n'est pas intégré simplement parce que toutes les tables se trouvent au même endroit, et c'est pourtant ce à quoi aboutissent de nombreuses entreprises. Elles ont un ensemble de tables clients Salesforce et une table clients dans la base de données produit, mais elles ne communiquent pas entre elles.

Aujourd'hui, de nombreuses entreprises veulent que tout soit unifié et intégré... mais ce n'est simplement pas là où les choses finissent.

Pour une raison ou une autre, de nombreuses entreprises se retrouvent avec un fatras de tables. Parlons donc de la façon dont beaucoup d'entreprises en arrivent là, et comment l'éviter.

### Fin du jour 228

Merci d'avoir découvert notre communauté. Nous publions 2 à 4 newsletters par mois sur la donnée, la tech et les startups.

Si vous avez apprécié, pensez à aimer, partager et aider cette newsletter à grandir.

## Pourquoi ça compte
Cet article offre un contrepoint utile au narratif « l'IA remplace les data engineers » en montrant que la valeur du métier se déplace vers la confiance, la gouvernance et la compréhension métier plutôt que vers la seule vitesse d'exécution du code — un signal pertinent pour toute veille sur l'impact de l'IA générative sur les métiers de la donnée.
