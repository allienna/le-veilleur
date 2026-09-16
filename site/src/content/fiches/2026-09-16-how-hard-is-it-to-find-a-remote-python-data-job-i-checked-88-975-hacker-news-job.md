---
title: "How Hard Is It to Find a Remote Python Data Job? I Checked 88,975 Hacker News Job Posts"
date: 2026-09-16
url: "https://elink56e.dataelixir.com/ss/c/u001.5r3FSAOML_uDG8gnrJ3iiMMkDNFVXKH-VFIqmKYLhNiTzk8OBWESYY39Fea7Exkl1hEIxI4r1x5zkRuw8H6qMcGvIEH8bhUkxfBmBCKxx2fRQrlO1KAa_eCfwL3-ZJ4sOstJhzmGq7k7OyBfwVgl74t2y4ItKi35s-LdMDVC3BmVOSZ-YMYFpaks5K69Ugc76RkxXaBA9w10oyHlf-D3xJv0ivBKJJmrK_AAzwyAhQw/4u2/JDdLB4i8STiLDBQh8-3HAQ/h14/h001.7UFqLkjOxSkrili80TmfrI-x0FatOCXhmm5UvncTqgk"
authors: ["Piotr Płoński"]
keywords: ["marché de l'emploi tech", "Hacker News", "télétravail", "salaires tech", "IA dans les offres d'emploi", "Python"]
theme: "Data"
tone: "research"
used_in: ["2026-09-16"]
---

## Résumé
L'auteur a analysé 88 975 commentaires issus des 163 threads mensuels « Ask HN: Who is hiring? » sur Hacker News, de décembre 2012 à août 2026, pour construire un « funnel » de recherche d'emploi (remote, langage, rôle data, rémunération). Le constat central est que le volume d'offres a chuté de moitié depuis le pic de 2021, que le télétravail recule après son pic de 2022 au profit du mode hybride, et que la transparence salariale a nettement progressé sous l'effet des lois américaines sur la divulgation des salaires. Malgré un marché plus restreint, la part d'offres qui cochent toutes les cases (remote, Python, data, rémunération affichée) a presque doublé entre 2018 et 2025.

## Points clés
- Le nombre d'offres publiées sur le thread HN a chuté de 10 286 (2021) à environ 4 000/an depuis 2023, une baisse de 59 % en deux ans, sans que la taille moyenne des annonces n'ait changé.
- Le télétravail est passé de ~21 % (années 2010) à un pic de 83 % en 2022, puis a reculé à 54 % en 2026 ; le travail hybride, quasi inexistant avant 2020, concerne désormais une offre sur cinq.
- Python et JavaScript/TypeScript ont maintenu leur part de marché (respectivement ~25 % et ~27 % en 2026) tandis que Ruby, Java, PHP et C#/.NET ont perdu 70 à 78 % de leur part ; Rust est passé d'anecdotique à 8,6 %, devançant Go, Java, Ruby et C#.
- Plus de la moitié des offres 2026 mentionnent l'IA (contre moins de 3 % en 2016), une offre sur cinq cite LLM/GPT/RAG/GenAI, alors que la crypto est retombée à 2,2 % après un pic de 5,6 % en 2022.
- La divulgation d'une rémunération est passée de 14 % (2016) à plus d'un tiers des offres, sous l'effet des lois de transparence salariale (Colorado, New York, Californie, Washington) ; le salaire médian affiché a grimpé de 117 500 $ à 185 000 $, soit +57 % nominal mais seulement ~14 % en termes réels sur dix ans.
- Les mentions de postes « senior » ont plus que triplé (11,5 % en 2013 à 41 % en 2026) alors que les mentions « junior/débutant » sont tombées de 12,4 % à 4,8 %, un déclin amorcé dès 2014-2015, bien avant la récession tech actuelle et l'essor de l'IA.

## Analyse approfondie
Depuis 2011, Hacker News publie chaque mois le même fil de discussion : *Ask HN: Who is hiring?* Un commentaire par entreprise, sans recruteur ni algorithme. Quatorze années de ces fils constituent l'une des rares archives longues et cohérentes de ce que les entreprises tech recherchaient réellement.

L'auteur a récupéré 88 975 commentaires issus de 163 threads mensuels, de décembre 2012 à août 2026, et a construit une application de type « entonnoir » (funnel) au-dessus de ces données. On part de toutes les offres d'une année donnée, puis on ajoute un critère à la fois pour observer combien d'offres passent chaque filtre.

À titre d'exemple, la recherche par défaut (remote + Python + rôle data + rémunération indiquée) ne retient que 61 offres sur plus de quatre mille, soit 1,5 %, et chaque filtre est pourtant appliqué de façon généreuse : « remote » suffit à apparaître n'importe où dans le texte, et le critère de rémunération accepte un symbole monétaire suivi d'un nombre, ou les mots « compensation »/« comp ».

Le plus intéressant n'est pas ce chiffre final, mais le fait que chaque étape du filtre a évolué dans une direction différente au cours de la dernière décennie, et que deux d'entre elles ont pris le sens inverse de ce que l'auteur attendait.

### Étape 0 : deux fois moins d'offres
Avant même d'appliquer un filtre, le volume de départ a changé de taille. Le nombre d'offres a culminé à 10 286 en 2021 avant de tomber à 4 175 en 2023, soit une baisse de 59 % en deux ans. Depuis, le volume reste stable autour de 4 000 par an. Sur la base des données de janvier à août, 2026 devrait atteindre environ 3 700 offres.

Ce n'est pas un artefact de mise en forme : la longueur médiane d'une offre est restée la même qu'en 2015, environ 950 caractères. Parmi les années complètes, toutes comptent leurs douze threads mensuels, sauf 2015 à qui il en manque deux. Il y a simplement moins d'entreprises qui publient.

### Étape 1 : le télétravail a culminé en 2022 puis reflué
C'est le signal le plus net du jeu de données. Le télétravail est resté autour de 21 % pendant des années, a bondi à 60 % en 2020, atteint 83 % en 2022, puis a reculé chaque année depuis pour tomber à 54 % en 2026. Les mentions de travail sur site ont touché un plancher d'environ 23 % en 2022 avant de remonter à 34 %.

L'hybride est la vraie histoire : quasiment inexistant avant 2020 (moins de 1 % des offres pendant huit ans), il apparaît désormais dans une offre sur cinq. Le retour au bureau n'a pas annulé le télétravail : il a créé une troisième catégorie qui a grignoté des parts aux deux autres modes.

Une réserve s'impose : le format « Entreprise | Lieu | ONSITE/REMOTE » n'est devenu courant qu'entre 2015 et 2016. Avant cela, les modalités de travail étaient noyées dans le texte et probablement sous-comptées, ce qui explique que ce graphique démarre en 2016.

### Étape 2 : Python et JavaScript ont tenu bon
Entre 2016 et 2026, les parts de langages ont beaucoup évolué : JavaScript/TypeScript passe de 24,5 % à 26,7 %, Python de 21,9 % à 25,1 %, tandis que Ruby s'effondre de 16,7 % à 4,4 %, Java de 11,4 % à 3,4 %, Go de 7,7 % à 5,9 %, C#/.NET de 7,5 % à 2,5 % et PHP de 5,4 % à 1,2 %. À l'inverse, Rust bondit de 0,3 % à 8,6 %.

Ruby a perdu les trois quarts de sa part, Java 70 %, PHP 78 %. Go, souvent présenté comme le langage qui a dominé les années 2010, a culminé à 10,2 % en 2022 avant de décliner. Rust est passé d'un chiffre négligeable à une part supérieure à celle de Go, Java, Ruby ou C#.

Python et JavaScript n'ont pas beaucoup grandi : ils ont simplement refusé de rétrécir alors que les langages plus anciens autour d'eux perdaient du terrain. Sur un marché qui a perdu la moitié de ses offres, conserver sa part suffit à gagner la partie.

### Étape 3 : le rôle est resté le même, mais l'étiquette a changé
Les rôles data et machine learning sont restés remarquablement stables : 18 % des offres en 2016, 19 % en 2026, sans jamais s'écarter beaucoup de 20 % entre-temps. C'est le constat le moins surprenant.

Ce qui l'est davantage, c'est la façon dont les entreprises se présentent désormais. Plus de la moitié des offres publiées en 2026 mentionnent l'IA, contre moins de 3 % en 2016. Une offre sur cinq cite LLM, GPT, RAG, GenAI ou un laboratoire de pointe par son nom, une catégorie qui n'existait pas de façon mesurable avant 2022.

À l'inverse, la crypto a culminé à 5,6 % des offres en 2022 avant de retomber à 2,2 %. Quel que soit ce que représente l'IA aujourd'hui, sa part dans les offres d'emploi est plus d'un ordre de grandeur supérieure à celle qu'occupait la crypto.

### Étape 4 : le seul filtre devenu plus facile à satisfaire
C'est ici que l'entonnoir surprend l'auteur : tous les autres critères sont devenus plus difficiles à remplir, sauf la divulgation salariale, qui est allée dans le sens inverse.

Plus d'un tiers des offres de 2026 indiquent désormais un montant ou une mention de rémunération, contre 14 % en 2016. Les fourchettes explicites (un véritable « X $ à Y $ ») sont passées de 4 % à 24 %.

L'inflexion se situe entre 2021 et 2022, ce qui coïncide avec les règles de transparence salariale du Colorado, suivies de la loi de New York, puis de nouvelles obligations en Californie et dans l'État de Washington. Les entreprises publiant sur un forum à forte dominante américaine ont commencé à divulguer ces informations parce qu'une part croissante d'entre elles y était tenue légalement.

Le tableau se nuance toutefois : sur 4 134 offres comportant une fourchette de salaire exploitable, le point médian affiché est passé de 117 500 $ en 2016 à 185 000 $ en 2026, soit +57 %. Exprimé en dollars constants de 2026 (indice des prix américain), cela correspond à un gain réel d'environ 14 % sur dix ans, soit environ 1,3 % par an.

Un biais de sélection existe : les entreprises qui acceptaient de publier un chiffre en 2016 ne formaient pas la même population que celles qui le font aujourd'hui. Les valeurs d'inflation 2025 et 2026 restent aussi des hypothèses du notebook, les moyennes annuelles définitives n'étant pas encore disponibles. La tendance reste cependant claire : la rémunération affichée a beaucoup progressé sur le papier, et un peu en termes réels.

Un détail connexe : 32 % des offres qui divulguent une rémunération mentionnent aussi de l'equity, contre 6,8 % de celles qui n'en divulguent pas. La hausse des mentions d'« equity » depuis 2023 relève largement du même phénomène : une fois qu'on rédige une ligne de rémunération, on a tendance à la rédiger en entier.

### Le constat bonus que personne n'avait demandé
En 2013, les mots « senior » et « junior / new grad / entry-level / intern » apparaissaient dans une part comparable des offres : 11,5 % et 12,4 % respectivement. Aujourd'hui, ces chiffres sont de 41,0 % et 4,8 %.

Les mentions « junior » n'ont pas chuté récemment : elles ont fortement reculé entre 2014 et 2015 et n'ont cessé de diminuer depuis, bien avant le ralentissement actuel et bien avant l'IA. La courbe « senior », elle, a plus que triplé. C'est la tendance la plus durable de tout le jeu de données.

### En combinant les deux
Moins d'offres et un entonnoir plus étroit ne signifient pas forcément une recherche d'emploi plus difficile. En 2018, seulement 33 offres sur 9 691 franchissaient les quatre filtres (0,3 %). En 2025, ce sont 61 offres sur 4 046 (1,5 %). Le marché est moins de moitié aussi grand qu'avant, mais presque deux fois plus d'offres, proportionnellement, correspondent à un poste data en Python, en télétravail, avec une rémunération identifiable.

C'est le résumé honnête de la dernière décennie de ce fil de discussion : moins d'employeurs, mais ceux qui publient encore sont bien plus susceptibles d'indiquer où l'on peut travailler, ce que l'on va construire, et combien on sera payé.

### Ce que ces chiffres ne disent pas
La recherche par mots-clés est un instrument grossier, et l'auteur tient à être transparent sur ses limites :
- Un commentaire est traité comme une seule entrée, alors qu'un même commentaire peut annoncer cinq postes différents.
- Une mention n'est pas une exigence : « nous utilisons Postgres, pas MySQL » compte tout de même comme une mention de MySQL.
- « Remote » inclut le télétravail géographiquement restreint ; environ 1 mention « remote » sur 100 est en réalité une négation du type « pas de télétravail ».
- Les chiffres de rémunération sont libellés en dollars et fortement orientés vers les États-Unis, si bien que le graphique salarial est en réalité un graphique salarial américain.
- Hacker News représente une tranche spécifique et auto-sélectionnée de l'industrie (startups, entreprises d'infrastructure, nombreuses entreprises issues de Y Combinator) : il ne faut pas y voir un reflet de l'ensemble du marché du travail.
- Les données 2026 ne couvrent que la période de janvier à août.

Chaque chiffre de l'article provient de motifs transparents documentés dans le notebook. Si l'on n'est pas d'accord avec la définition retenue pour un « rôle data » ou pour « junior », il suffit de modifier l'expression régulière correspondante et de relancer l'analyse — c'est tout l'intérêt de publier le code.

### Reproduire l'analyse soi-même
Deux applications Mercury interactives alimentent cette analyse : un « Remote Tech Job Funnel » qui permet de choisir une année, un mode de travail, un langage et une famille de rôle pour observer l'entonnoir se resserrer (chaque offre correspondante renvoie vers le commentaire Hacker News d'origine), et un « Programming Language Sankey » qui permet de comparer la répartition des langages entre plusieurs années.

Les deux applications ainsi que le notebook d'analyse sont disponibles dans le dépôt d'exemples Mercury, avec les commandes d'installation et de lancement en local. Le jeu de données regroupe les 88 975 commentaires répartis en un fichier CSV compressé par année, pour un total d'environ 36 Mio. Le dépôt inclut le notebook qui a produit chaque graphique de l'article, permettant d'inspecter les motifs, de modifier une définition et de reconstruire soi-même les résultats.

### À propos de l'auteur
Piotr Płoński est ingénieur logiciel et data scientist, titulaire d'un doctorat en informatique. Il a une expérience à la fois académique — travaux sur des expériences liées aux neutrinos dans de grands laboratoires de recherche et projets interdisciplinaires — et industrielle, ayant accompagné de grands clients chez Netezza, IBM et iQor. En 2016, il a fondé MLJAR pour rendre la data science plus simple et plus accessible, en créant des outils comme AutoML, Mercury et MLJAR Studio.

## Pourquoi ça compte
Cette analyse offre un indicateur empirique rare et vérifiable sur les vraies tendances du marché tech (télétravail, langages, montée de l'IA, transparence salariale) à partir d'une source primaire longue de 14 ans, ce qui en fait une référence utile pour toute veille sur l'évolution du recrutement tech plutôt que sur de simples perceptions ou sondages déclaratifs.
