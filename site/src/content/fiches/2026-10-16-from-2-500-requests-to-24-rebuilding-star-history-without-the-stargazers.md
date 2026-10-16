---
title: "From 2,500 requests to 24: Rebuilding star history without the stargazers"
date: 2026-10-16
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fgithub.blog%2Fengineering%2Farchitecture-optimization%2Ffrom-2500-requests-to-24-rebuilding-star-history-without-the-stargazers%2F%3Futm_source=tldrdata/1/010001a13f0d59fd-c7dedc25-842c-4848-902e-7af2e182448b-000000/AqJ4TP9W92wsfz9uey5ZgKOunQKF80rNMUJUqaKo6NQ=452"
keywords: ["API", "GitHub", "pagination", "performance", "confidentialité", "base de données"]
theme: "Software"
tone: "research"
used_in: ["2026-10-16"]
---

## Résumé

GitHub a restreint l'accès aux listes de stargazers par souci de confidentialité et de charge sur sa base de données, ce qui a cassé des outils comme star-history.com qui s'appuyaient dessus pour reconstruire des courbes de popularité. En dialoguant avec les mainteneurs, l'équipe GitHub a compris que seule la courbe (comptages + dates) comptait, pas l'identité des stargazers, et a conçu un nouvel endpoint agrégé fondé sur un filtrage par plage de dates effectué avant l'agrégation plutôt qu'après. Résultat : reconstituer l'historique complet de `react/react` (~251 000 stars) nécessite désormais environ 24 requêtes au lieu d'environ 2 511, sans jamais exposer d'identité. L'article retrace les itérations de conception (restriction d'accès, renvoi des dates seules, agrégation naïve, puis filtrage avant agrégation) qui ont mené à cette solution.

## Points clés

- Restriction initiale des endpoints stargazers/watchers aux administrateurs et collaborateurs du dépôt, pour stopper le scraping d'identités utilisé pour des campagnes de spam et de phishing.
- Un bug de pagination forçait un comptage complet de toutes les stars à chaque requête ; près de 37 000 requêtes lentes (~3 s en moyenne) par semaine et plus de 1 000 tuées par les garde-fous de la base de données, causant des timeouts.
- Le nouvel endpoint renvoie jusqu'à 30 semaines de comptages quotidiens de stars en une seule requête, sans aucune identité associée.
- La clé technique : filtrer les lignes sur une plage de dates indexée (`created_at`) avant le group-by et le tri, au lieu d'agréger tout l'historique puis de paginer avec `LIMIT`/`OFFSET`.
- Pour `react/react` : 24 requêtes au lieu de 2 511, et chaque star n'est examinée qu'une seule fois sur l'ensemble de l'historique (~251 000 lignes contre ~6 millions avec l'approche d'agrégation naïve).
- Collaboration étroite entre GitHub, les mainteneurs d'outils tiers (star-history.com) et la communauté pour cerner le véritable besoin : la courbe, pas l'identité.

## Analyse approfondie

Obtenez l'historique des stars d'un dépôt, puis partagez vos retours dans la discussion GitHub Community.

Ingénieur logiciel senior

Les mainteneurs consultent l'historique des stars pour répondre à une question pratique : un lancement, une release ou un événement a-t-il changé la trajectoire d'un projet ? Pour reconstruire cette courbe à partir de l'API GitHub, les outils devaient demander des pages d'enregistrements de stargazers (chaque personne qui a actuellement mis une star au dépôt et la date à laquelle elle l'a fait), conserver les horodatages, puis jeter les identités.

Avec le temps, cette conception a créé des problèmes aux deux extrémités. Les identités étaient disponibles pour une collecte en masse, si bien que des acteurs malveillants ont commencé à scraper les listes publiques de stargazers pour des campagnes de spam et de phishing. Pour les dépôts très populaires, l'endpoint pouvait aussi forcer la base de données à traiter plusieurs milliers d'entrées pour renvoyer une seule page.

La solution semblait évidente : renvoyer des comptages plutôt que des personnes. Mais renvoyer moins de données ne rendait pas la requête moins coûteuse pour autant.

Désormais, les mainteneurs disposent d'un moyen direct d'obtenir cette courbe : nous avons créé un endpoint qui renvoie jusqu'à 30 semaines de comptages quotidiens de stars en une seule requête, sans aucune identité associée. Pour que cela reste peu coûteux à servir, il fallait réduire la quantité de données traitées par la base de données, pas seulement la quantité renvoyée, et l'endpoint y parvient en **filtrant les stars par période avant de compter quoi que ce soit**.

Nous avons d'abord traité les risques immédiats pour les développeurs et pour notre base de données en restreignant les listes de stargazers et de watchers aux administrateurs et collaborateurs du dépôt. Après ce changement d'accès, les appelants sans la permission requise pouvaient recevoir une réponse vide ou une réponse `403 Forbidden`.

Ce changement a aussi coupé l'accès aux outils qui utilisaient l'ancienne réponse pour calculer l'historique des stars, souvent sans afficher ni utiliser autrement les noms d'utilisateur renvoyés. Nous avons donc discuté avec les mainteneurs et les créateurs d'outils pour comprendre ce dont ils avaient encore besoin. Ils utilisaient l'historique des stars comme un signal approximatif d'intérêt : pour comparer l'activité avant et après une release, ou pour voir si une annonce avait atteint de nouveaux développeurs. Ce qui comptait pour eux, c'était la courbe.

L'ancienne réponse de l'API donnait l'impression que l'identité faisait partie de ce contrat, car chaque horodatage arrivait associé à un utilisateur. En pratique, des outils comme Star History avaient besoin de comptages et de dates, pas de noms d'utilisateur ni d'autres données personnelles. Une fois que l'identité n'était plus une exigence, nous avons pu concevoir un endpoint agrégé pour la véritable tâche : récupérer l'évolution des comptages de stars dans le temps, à une résolution utile.

Lorsque le changement d'API a perturbé Star History, les utilisateurs se sont mobilisés autour du projet. L'équipe Community de GitHub a été à l'écoute et nous a mis en relation avec l'ingénierie produit, qui a creusé notre cas d'usage et a travaillé avec nous pour concevoir un endpoint sur mesure. Une situation difficile s'est transformée en une collaboration constructive entre GitHub, Star History et la communauté élargie — menant finalement à une meilleure solution.

Tianzhou Chen, mainteneur de star-history.com et co-fondateur de Bytebase

Une fois que nous savions ce dont les mainteneurs avaient besoin, l'étape suivante consistait à comprendre pourquoi la conception d'origine ne pouvait pas le fournir à moindre coût. L'endpoint original `GET /repos/{owner}/{repo}/stargazers` avait été conçu pour répondre à une question simple : qui a mis une star à ce dépôt ? Il renvoyait une liste paginée de personnes, et si la requête spécifiait un type de média personnalisé, chaque entrée incluait aussi la date de création de la star.

Le modèle de données des stars a été construit pour la même tâche. Il enregistre l'ensemble actuel des personnes ayant mis une star à un dépôt, ce qui permet d'afficher simplement un nombre de stars ou une liste de stargazers. Il n'a pas été conçu comme un journal d'événements historique : lorsque quelqu'un retire sa star, l'enregistrement correspondant est supprimé. Quand les outils ont commencé à utiliser cette liste comme une série temporelle, reconstruire une courbe de croissance impliquait de récupérer des identités individuelles et de traiter chaque star actuelle. Comme chaque page contenait au maximum 100 personnes, le travail augmentait avec la popularité du dépôt : construire la courbe complète pour `react/react`, qui compte environ 251 000 stars, nécessitait environ 2 511 requêtes, si bien que les outils se heurtaient souvent aux limites de débit (rate limits) ou échantillonnaient des pages au lieu de toutes les lire.

Servir une page nécessitait que la base de données interroge les stars actuelles du dépôt. En raison d'un bug dans l'implémentation de la pagination, chaque requête comptait aussi la totalité de ces stars pour déterminer combien de pages existaient, même si l'appelant ne recevait qu'une seule page d'au plus 100 personnes. Sur un dépôt très populaire, cela signifiait compter plusieurs milliers d'entrées à chaque requête. Pendant la semaine précédant la restriction de l'accès, près de 37 000 de ces requêtes de comptage ont été suffisamment lentes pour être journalisées, avec une durée moyenne de près de 3 secondes chacune, et les mécanismes de protection de la base de données en ont tué plus de 1 000, ce qui a contribué à des timeouts de requêtes.

Le graphique ci-dessous montre le coût de tout ce comptage. Après la restriction de l'accès, la base de données a servi environ 60 % moins de requêtes de stargazers, et le temps total passé sur la requête de comptage a chuté d'environ 80 %.

Supprimer les identités répondait à l'exigence de confidentialité. La partie la plus difficile consistait à empêcher chaque requête de parcourir l'intégralité de l'ensemble actuel des stars du dépôt.

Notre premier prototype (spike) conservait un enregistrement par star et renvoyait la valeur `starred_at` sans l'identité du stargazer pour les appelants ne disposant pas d'un accès collaborateur. Au premier abord, cela semblait être la voie la plus rapide, car elle répondait directement à la demande entendue auprès des créateurs d'outils. Elle fermait aussi la voie de collecte des identités avec un changement relativement restreint du flux existant de sérialisation et d'autorisation.

Cette approche traitait l'exposition des identités et aurait permis aux outils existants de continuer à fonctionner. Mais les consommateurs de l'API auraient quand même dû paginer et traiter potentiellement plusieurs milliers d'enregistrements individuels pour construire un historique agrégé. Elle liait aussi le nouveau cas d'usage à un endpoint et à un modèle de pagination conçus pour lister des personnes plutôt que pour récupérer des tendances.

L'agrégation semblait être l'étape suivante évidente. Au lieu de renvoyer une ligne par star, la requête pouvait regrouper les stars en buckets quotidiens ou hebdomadaires, trier ces buckets, puis paginer le résultat, bien plus restreint.

Le problème résidait dans le moment où intervenait la pagination. Dans une requête SQL directe, la base de données commence par trouver toutes les stars du dépôt, les regroupe en buckets, puis trie ces buckets. Ce n'est qu'ensuite qu'elle applique `LIMIT`, qui contrôle combien de buckets sont renvoyés, et `OFFSET`, qui détermine où commence la page :

`toutes les stars correspondantes -> regrouper chaque ligne par jour ou semaine -> trier chaque bucket -> OFFSET/LIMIT -> réponse`

Pour un dépôt populaire, une requête anonyme pouvait quand même parcourir et agréger plusieurs milliers d'entrées d'index pour ne renvoyer qu'une poignée de buckets. Renvoyer moins de buckets réduirait la taille de la réponse JSON, mais ne réduirait pas le regroupement et le tri coûteux déjà effectués par la base de données. Pour `react/react`, lire l'historique complet de cette façon aurait signifié examiner environ 6 millions de lignes, car chacune des 24 requêtes aurait retraité l'ensemble de ses stars. Pour réduire le coût de la requête, il fallait restreindre les lignes avant que l'agrégation ne commence.

La conception que nous avons déployée pagine l'historique des stars par semaine calendaire. Pour chaque requête, elle traduit `page` et `per_page` en une plage indexée sur `created_at`, filtre les stars sur ces semaines, puis regroupe les enregistrements correspondants en comptages quotidiens. Une réponse comprend jusqu'à 30 semaines, et augmenter `page` permet de remonter dans l'historique du dépôt.

`plage de dates indexée -> regrouper les lignes de cette plage -> buckets quotidiens -> réponse`

Avec la plage de dates appliquée en premier, chaque requête traite uniquement les semaines renvoyées, au lieu de chaque star actuelle du dépôt. Pour les outils, cela signifie qu'une seule requête couvre désormais jusqu'à 30 semaines d'historique, quel que soit le nombre de stars du dépôt. Pour `react/react`, cela représente environ 24 requêtes au lieu d'environ 2 511, et la base de données examine chaque star environ une fois (environ 251 000 lignes) sur l'ensemble de l'historique. Cela correspond au cas d'usage principal, car les mainteneurs examinent généralement la croissance sur plusieurs semaines ou autour d'une release, d'un lancement ou d'un événement connu. Les plages hebdomadaires s'alignent aussi avec d'autres API d'activité de dépôt : la réponse suit le même format que l'endpoint d'activité de commits hebdomadaire, `GET /repos/{owner}/{repo}/stats/commit_activity`.

Cette conception par plage temporelle limite chaque requête à une période définie, mais elle ne limite pas le nombre de stars à l'intérieur de cette plage. Une semaine avec un nombre anormalement élevé de stars peut donc toujours produire une requête lente ou coûteuse. Le chemin normal des requêtes n'interroge plus chaque star actuelle, mais les semaines exceptionnellement denses restent une limite de scalabilité.

La comparaison des performances entre l'ancien et le nouveau chemin d'API a également révélé d'autres endroits où GitHub comptait les stars à la demande. Nous avons trouvé le même schéma sur la page des stargazers d'un dépôt sur GitHub.com, et nous l'avons mise à jour pour utiliser le comptage de stars mis en cache du dépôt. Les requêtes lentes provenant de cette page, qui se comptaient en centaines chaque semaine, sont tombées à zéro. Nous avons récemment déployé un correctif similaire sur d'autres endpoints de l'API liés aux stargazers.

Le graphique ci-dessous montre les requêtes de comptage de stargazers lentes et tuées chaque semaine, selon leur origine.

`LIMIT` et `OFFSET` réduisaient le nombre de résultats renvoyés, mais pas le regroupement et le tri déjà effectués par la base de données. Il a fallu revoir l'ordre dans lequel le travail s'effectuait.

Restreindre l'endpoint d'origine a réglé le problème immédiat. Mais écouter les mainteneurs nous a donné quelque chose de **meilleur** que ce dont nous étions partis : un historique des stars plus facile à obtenir, moins coûteux à servir, et plus sûr pour tous ceux qui mettent une star à un projet.

## Pourquoi ça compte

Ce cas illustre un principe transposable à toute API exposant des données agrégées à grande échelle : réduire la taille de la réponse ne réduit pas le coût de calcul sous-jacent, il faut filtrer avant d'agréger. C'est aussi un exemple concret de privacy-by-design né d'une collaboration entre une plateforme et sa communauté de mainteneurs d'outils tiers.
