---
title: "The age of frivolous software"
date: 2026-11-03
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fianmccrystal.com%2Fposts%2Fthe-age-of-frivolous-software%2F%3Futm_source=tldrdev/1/010001a19c304b30-8984ed05-1c42-40dd-8196-6fbd2d0dac82-000000/Sk5UFTQSkJa1Tv1IqgU6utveNeQnCBvMw4vKb34_Yy4=452"
authors: ["Ian McCrystal"]
keywords: ["IA générative", "vibe coding", "développement web", "agents IA", "Anthropic", "Stripe"]
theme: "IA"
tone: "opinion"
used_in: ["2026-11-03"]
---

## Résumé
L'auteur raconte comment il a construit worldcupdash.com, un tableau de bord personnalisé pour suivre la Coupe du Monde 2026, en utilisant le modèle Fable 5 d'Anthropic combiné à Stripe Projects, sans écrire une seule ligne de code lui-même. Lancé en moins de 8 heures et amélioré pendant six semaines par itérations guidées à l'oral (« vibe coding »), le site est passé de 1 à environ 50 000 utilisateurs. L'auteur en tire une thèse plus large : les agents IA rendent désormais viables des projets web auparavant jugés « frivoles » car trop coûteux en temps et en énergie, ouvrant une nouvelle ère du logiciel personnel et ludique.

## Points clés
- Le site worldcupdash.com a été créé avec Fable 5 (Anthropic) pour le code/les données et Stripe Projects pour provisionner l'infrastructure (compte Netlify, jeton d'authentification pour l'agent).
- Mise en ligne de la première version en environ 8 heures, puis des centaines de déploiements itératifs sur six semaines, pilotés par retours esthétiques et nouvelles idées de fonctionnalités à la volée.
- Croissance de 1 à ~50 000 utilisateurs en quelques semaines, certains devenant des utilisateurs quotidiens.
- Des fonctionnalités « purement pour le plaisir » (comme un thème visuel en chiffres romains, blague interne sur l'Italie) illustrent la frivolité revendiquée du projet.
- Thèse centrale : l'IA agentique abaisse tellement le coût de création logicielle que des idées jugées non rentables deviennent réalisables, et peuvent quand même trouver un large public.

## Analyse approfondie
# L'ère du logiciel frivole

Tous les quatre ans, je consacre tout le temps que je peux à une seule chose : regarder la Coupe du Monde.

Me voici avec un ami, le 11 juin, au Berkeley Greek Theater, en train de regarder un match de phase de groupes (la Corée du Sud a battu la République tchèque 2-1 ; un beau match). James Blake donnait un concert quelque part hors champ, à droite.

J'aime ce sport et j'approuve avec enthousiasme son surnom parfois raillé de « beau jeu », mais, plus que cela, j'aime la Coupe du Monde et la façon dont elle rassemble une grande partie du monde dans une liesse compétitive (globalement) bon enfant et une célébration de la fierté nationale. C'est un événement merveilleux et un formidable rappel périodique que nous sommes tous humains et que nous pouvons nous amuser ensemble même en étant dans des camps opposés. Les gens voyagent du monde entier pour y assister, et je rencontre systématiquement des inconnus avec qui je m'amuse plus pendant la Coupe du Monde qu'à n'importe quel autre événement de ma vie : c'est vraiment l'humanité à son apogée.

Au moment même où débutait la Coupe du Monde, nos amis d'Anthropic sortaient leur modèle d'IA Fable 5, alors très attendu, et dont les capacités de codage étaient, m'avait-on dit, impressionnantes. Mon ancien employeur, Stripe, venait lui aussi de lancer Stripe Projects, un outil à l'air futé permettant de provisionner de l'infrastructure web de façon agentique. J'avais envie de tester ces nouveaux outils de développement et j'étais frustré par le manque de bons sites web consacrés à la Coupe du Monde (ils semblaient tous vouloir me vendre quelque chose), alors je me suis demandé : puis-je utiliser Fable + Projects pour construire le meilleur site web de Coupe du Monde du monde (pour moi) ? Et puis-je le faire sans écrire moi-même une seule ligne de code ni configurer manuellement la moindre infrastructure ?

Il s'est avéré que la réponse était oui ! J'ai mis en ligne la première version de worldcupdash.com le 12 juin, un jour après le match d'ouverture de la Coupe du Monde et environ 8 heures après avoir eu l'idée de le faire, puis j'ai passé les 6 semaines suivantes à en « vibe-coder » les améliorations tout en regardant et en assistant aux matchs. Le site est passé de 1 utilisateur (moi-même) à environ 50 000 utilisateurs en quelques semaines seulement, et j'ai récolté de nombreux témoignages de personnes me disant qu'il s'agissait de leur site de Coupe du Monde préféré et qu'elles en étaient devenues des utilisatrices quotidiennes. Plutôt cool !

### De quoi s'agit-il ?

Un tableau de bord de la Coupe du Monde actualisé en direct, dense en informations, sans fioritures[0], avec les scores, les détails des matchs en direct, les probabilités de victoire, les classements de groupes, etc.

Je voulais qu'il soit rapide, adapté au mobile, facile à utiliser et agréable pour les utilisateurs (moi). Il ne devait jamais être agaçant. Je peux le consulter à tout moment et obtenir un instantané de l'avancement du tournoi et de ce qui s'annonce.

Il devait aussi être facile à maintenir pour le mainteneur (moi aussi), c'est-à-dire :

- aucune dépendance
- pas de système de build délirant, pas de package.json, etc.
- pas de backend
- fonctionne entièrement dans un navigateur
- utilise des API publiquement disponibles
- déployé via Netlify, sur un forfait très bon marché

Avec Fable et Projects, j'ai pu lancer une première version en quelques heures seulement et avec juste quelques prompts. Fable a largement trouvé lui-même les sources de données et la plomberie nécessaire, avec peu de direction de ma part (il y a eu davantage de direction par la suite, lorsque de nouvelles fonctionnalités ont nécessité d'autres sources de données). Projects a provisionné un compte Netlify et a donné à l'agent un jeton d'authentification qu'il pouvait utiliser pour agir sur ce compte (comme déployer le site).

Le design initial du site venait en grande partie de Fable, moi me contentant de fournir une direction esthétique et des retours/ajustements. Au cours des six semaines suivantes, j'ai déployé le site des centaines de fois, le produit final n'étant donc en rien le résultat d'un seul coup. Faire en sorte que l'interface soit véritablement réussie, et pas seulement utilisable, a été la partie la plus délicate et celle où j'ai passé le plus de temps à diriger l'agent.

J'ajoutais de nouvelles fonctionnalités dès qu'elles me venaient à l'esprit en regardant les matchs : « Encore un but en prolongation ! J'aimerais que le tableau de bord suive ça. » Ou bien, à mesure que le tournoi avançait, je livrais des fonctionnalités juste-à-temps nécessaires pour suivre le rythme de la compétition ; par exemple, quand la phase de groupes se termine et que la phase à élimination directe commence, cela implique tout un ensemble de nouvelles fonctionnalités que je n'avais pas préconstruites, mais que j'ai pu ajouter et déployer rapidement, parfois en quelques minutes à peine après en avoir eu besoin.

C'était l'une des parties les plus amusantes du projet : découvrir, implémenter et déployer de nouvelles fonctionnalités presque en temps réel. Certaines de ces fonctionnalités étaient nécessaires et je n'y avais pas pensé ; à l'époque pré-IA (autrement dit, à l'époque des dinosaures), on les aurait sans doute soigneusement spécifiées et cadrées à l'avance, inscrites sur une roadmap. D'autres étaient purement pour le plaisir : par exemple, un soir, en assistant à un match à Santa Clara, un ami a plaisanté en disant que la dernière fois que les Italiens s'étaient qualifiés pour la Coupe, c'était à l'époque des Romains, et que chaque match était consigné en chiffres romains. J'ai trouvé ça drôle, alors je suis rentré chez moi et j'ai fait implémenter par l'IA un thème « romain », qui réaffiche le tableau de bord dans une palette de couleurs travertin et remplace tous les chiffres par des chiffres romains incompréhensibles. Cela n'avait aucun autre but que de transformer notre blague sur le piètre parcours qualificatif de l'Italie en logiciel : c'était totalement frivole.

D'une certaine manière, tout ce projet était frivole, et c'est bien ce qui le rend si formidable ! Il y a quatre ans, je n'aurais pas construit World Cup Dash. J'aurais peut-être eu l'idée, mais j'aurais enduré l'usage de sites web agaçants-mais-disponibles, et à un niveau profondément insatisfaisant, « suffisamment bons », parce qu'il m'aurait coûté trop de temps et d'énergie mentale de construire un site de Coupe du Monde juste pour moi, juste pour le plaisir, entièrement personnalisé selon mes particularités et mon sens de l'humour. Même la simple mise en place de l'infrastructure aurait été suffisamment pénible pour me bloquer. Mais, depuis la Coupe du Monde 2026 (et sûrement encore davantage aujourd'hui), les outils existent, si bien que toute idée de site web amusante, auparavant écartée comme frivole et ne valant pas le temps investi, revient sur la table et, même si l'on construit uniquement pour soi-même, il se pourrait que 50 000 autres personnes là-bas veuillent ce que l'on a à offrir. Et n'est-ce pas génial ? Nous sommes entrés dans l'ère du logiciel frivole, et j'adore ça.

Et oui, j'ai fini par ajouter un mini-jeu jouable de tirs au but façon NES :

[0] enfin, un peu de fioritures tout de même, mais toujours pour le plaisir et dissimulées derrière un clic ou deux.

## Pourquoi ça compte
Ce témoignage concret illustre à quel point les agents IA de codage (modèle + outils de provisioning d'infrastructure) changent l'économie de la création logicielle : des projets personnels autrefois jugés trop coûteux en temps deviennent réalisables en heures et peuvent malgré tout rencontrer un vrai public, un signal fort pour quiconque suit l'évolution du « vibe coding » et des outils agentiques.
