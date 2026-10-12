---
title: "After 25 Years in Data, I Only Bet on One Thing: Optionality"
date: 2026-10-12
url: "https://substack.com/redirect/d1872e74-aeca-4354-b32a-cbbe8f4aabac?j=eyJ1IjoiN3Y1bG1jIn0.HlvPOGYPdVknSYzEK1JIj6IFkAFn8zuyjtfU9Mbft9Q"
authors: ["Victor"]
keywords: ["architecture de données", "optionalité", "lakehouse", "Hadoop", "Spark", "vendor lock-in"]
theme: "Data"
tone: "opinion"
used_in: ["2026-10-12"]
---

## Résumé
Après 25 ans dans la data (machine learning dès 2001, Spark en 2014, puis la lente sortie des plateformes Hadoop), l'auteur tire une seule leçon durable : ce qui compte n'est pas de choisir la bonne technologie ou la bonne architecture à un instant donné, mais de préserver sa capacité à changer d'avis plus tard. Il baptise ce principe « l'optionalité », un concept emprunté à la finance, et l'applique au débat centralisation vs décentralisation, aux formats de données ouverts et aux choix d'architecture lakehouse. Il soutient que ce principe devient encore plus critique à l'ère de l'IA, où les piles technologiques évoluent trop vite pour qu'on puisse se permettre un verrouillage fournisseur de plusieurs années.

## Points clés
- Rétrospective sur 25+ ans dans la data : le machine learning méconnu en 2001, la présentation de Spark 0.9 devant une vingtaine de personnes en 2014, et aujourd'hui la migration des entreprises hors de Hadoop vers des architectures hybrides plutôt que vers un nouveau monolithe unique.
- Les technologies passent de mode mais les idées qu'elles portent survivent et se recyclent (Hadoop a préparé le data lake puis le lakehouse sur Iceberg ; le data mesh a laissé les concepts de « data products » et de responsabilité métier).
- Le débat centralisé vs décentralisé est une fausse opposition : le bon mix dépend de la taille, de l'historique et des charges de travail de chaque entreprise, pas d'un dogme universel.
- L'« optionalité » (empruntée à la finance) consiste à payer une petite prime aujourd'hui pour garder la liberté de changer de cap demain, sans tout reconstruire — y compris la liberté de quitter son propre fournisseur si les données restent dans des formats ouverts.
- Cette liberté a un coût : une plateforme intégrée est plus simple à opérer mais impose sa roadmap et ses prix, tandis qu'une architecture best-of-breed est plus flexible mais exige plus de compétences et d'intégration.
- L'IA accentue l'enjeu : modèles, frameworks d'agents et protocoles évoluent en quelques mois, donc lier ses données à une seule plateforme est aujourd'hui l'un des paris les plus risqués qu'une entreprise puisse faire.

## Analyse approfondie

### Le pendule ne s'arrête jamais
L'auteur s'appuie sur une idée de Joe Reis : dans la data, les modes vont et viennent, puis reviennent sous une autre forme. En 25 ans, il a vu personne ne prédire l'essor de Hadoop, de NoSQL, d'Iceberg ou l'explosion actuelle de l'IA, ni la chute rapide de Hadoop ou du data mesh. Il s'interroge même sur les tendances du moment : la « context layer » est-elle le nouveau Far West ? Les catalogues de données sont-ils déjà dépassés ? Mais en regardant de plus près, rien ne meurt vraiment : les idées de Hadoop se retrouvent dans le data lake puis dans le lakehouse construit sur Iceberg, et le data mesh a légué des principes — comme les « data products » et la responsabilité métier des données — que les entreprises adoptent aujourd'hui en partie ou en totalité, sans forcément reprendre tout le concept d'origine. Les technologies s'effacent, mais les bonnes idées sont recyclées.

### Centralisé ou décentralisé ? Mauvaise question.
Le même phénomène de pendule s'observe dans le débat sans fin entre architectures centralisées et décentralisées. À l'époque des data warehouses et de Hadoop, tout centraliser était la norme. Puis le data mesh, avec les moteurs de fédération et de virtualisation comme Trino, a fait de la décentralisation la nouvelle promesse : arrêter de déplacer la donnée, et l'analyser et la gouverner là où elle se trouve. Est-ce toujours possible ? Non : les systèmes de production ne peuvent pas toujours être interrogés directement, et le bon vieux data warehouse reste présent. Le lakehouse moderne — cloud, on-premise ou hybride — simplifie malgré tout beaucoup la gestion d'un lac de données par rapport à l'époque de « l'éléphant jaune » (Hadoop). Les deux approches ont leurs avantages et inconvénients, et le bon dosage dépend de chaque entreprise : sa taille, son histoire, son legacy, son métier, ses charges de travail. On ne peut pas tenir le même discours à une startup née dans le cloud et à un assureur avec cinquante ans de systèmes on-premise. Conclusion de l'auteur : les consultants et les éditeurs de logiciels doivent arrêter de vendre des mots à la mode et commencer à offrir des options.

### Ce que signifie vraiment l'optionalité
Le terme vient de la finance : une option est le droit, mais non l'obligation, de faire un choix plus tard. On paie une petite prime aujourd'hui pour éviter de tout miser sur une prévision. C'est exactement ce qu'une bonne architecture de données devrait offrir : la capacité de changer d'avis sans repartir de zéro. En pratique, cela veut dire garder des portes de sortie sur les choix de formats, de moteurs et de plateformes. L'auteur, qui travaille pour un éditeur (Starburst), précise que ce principe doit aussi s'appliquer à son propre employeur : si les données sont dans des formats ouverts, il doit être possible de quitter n'importe quel moteur, y compris le leur. C'est tout le sens de la démarche.

### Il n'y a pas de repas gratuit
Mais l'optionalité n'est pas gratuite. Rien ne l'est : garder les mêmes processus, tout changer, centraliser, décentraliser — chaque choix a un coût humain, technique ou financier. Une plateforme totalement intégrée est plus simple à exploiter, mais on vit alors selon sa roadmap et ses tarifs. Une architecture best-of-breed est plus flexible, mais elle demande davantage de compétences et de travail d'intégration. L'auteur compare cela à un menu de restaurant : les entreprises ont besoin d'options au menu, et de la liberté de choisir leur restaurant — la pizzeria du quotidien, le restaurant chic une fois par mois, ou même un kebab. Elles doivent aussi pouvoir changer de restaurant si le patron change et que la qualité baisse. La pire situation, c'est de n'avoir qu'un seul restaurant en ville et aucun choix de plat.

### Pourquoi cela compte encore plus avec l'IA
Les choses changent plus vite que jamais. Modèles, frameworks d'agents et protocoles évoluent tous les quelques mois. Personne ne sait quelle pile IA l'emportera dans cinq ans, ni même dans deux ans. Lier aujourd'hui ses données à une seule plateforme est probablement le pari le plus risqué qu'on puisse faire. Les entreprises qui avanceront le plus vite avec l'IA seront celles capables de connecter de nouveaux outils à leurs données sans devoir relancer un projet de migration de trois ans — en d'autres termes, celles qui ont su garder leurs options ouvertes.

### Quelques questions à se poser
L'auteur reconnaît n'avoir pas de réponse parfaite pour l'architecture de données de chacun, mais propose des questions à se poser pour évaluer son niveau d'optionalité (le détail de la liste n'est pas repris dans le contenu disponible). Il ajoute : si une de ces réponses met mal à l'aise, il est temps de réfléchir sérieusement à l'optionalité.

### Garder les yeux ouverts
En conclusion, après plus de 25 ans dans l'industrie — du machine learning en 2001, à Spark devant 20 personnes, jusqu'à la fin de l'ère Hadoop — l'auteur retient une seule chose : rester les yeux ouverts, curieux, lire, poser des questions, tester et comparer, et ne jamais croire aux solutions miracles qui prétendent tout faire, car elles n'existent pas. Ce qui compte vraiment pour lui, c'est l'optionalité. Il précise avoir utilisé l'IA pour l'aider à rédiger cet article, son anglais n'étant selon lui pas excellent, et que les opinions exprimées sont les siennes, pas nécessairement celles de son employeur.

Dans les réactions en commentaire, un lecteur relève que la baisse du coût du code (grâce aux agents IA) rend l'optionalité plus pratique à mettre en œuvre concrètement, par exemple en générant plusieurs variantes d'une interface avant de choisir. Un autre souligne un parallèle avec le débat sur l'open source : les architectures ouvertes créent de la valeur d'option pour les clients (changer de fournisseur, forker, s'auto-héberger), mais cela limite le verrouillage et donc la capacité des fournisseurs d'une technologie sous-jacente à capter de la valeur économique — ce qui est stratégiquement précieux pour le client peut être économiquement inconfortable pour le fournisseur. Un autre lecteur ajoute une cinquième question à la liste de l'auteur : pourrait-on reconstruire ses définitions métier ailleurs ? Car si Iceberg rend la donnée portable, le sens de notions comme « client actif » ou « revenu net » vit souvent dans des champs calculés de BI ou des fichiers Excel — un verrouillage plus difficile à repérer sur un schéma d'architecture, mais tout aussi réel, et d'autant plus critique que les agents IA ont besoin de ces définitions métier plus que d'un moteur particulier.

## Pourquoi ça compte
Ce témoignage rappelle, à l'heure où l'IA rebat les cartes des piles technologiques data, qu'éviter le verrouillage fournisseur (via des formats ouverts type Iceberg et des architectures hybrides) est devenu un critère de résilience stratégique plus important que le choix d'une techno ou d'un camp architectural donné.
