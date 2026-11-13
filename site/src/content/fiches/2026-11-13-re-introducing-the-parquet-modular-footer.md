---
title: "Re: Introducing the Parquet Modular Footer"
date: 2026-11-13
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.mail-archive.com%2Fdev%2540parquet.apache.org%2Fmsg28218.html%3Futm_source=tldrdata/1/010001a1cf75fe31-ac9c430c-f0af-42e8-b127-f520ccf5a92f-000000/7TSHoMCcEo4B8GWm-N0pBb6IkQ7sGa7yDKSLtxQK9is=452"
authors: ["Jiayi Wang", "Julien Le Dem", "Micah"]
keywords: ["Apache Parquet", "footer modulaire", "format colonnaire", "stockage de données", "encodage Thrift", "big data"]
theme: "Data"
tone: "news"
used_in: ["2026-11-13"]
---

## Résumé
Ce fil de discussion de la liste de diffusion dev@parquet.apache.org porte sur la proposition de « footer modulaire » (Modular Footer) pour le format Apache Parquet, portée par Jiayi Wang. Après plusieurs mois de travail en groupe dédié, une première version a été proposée en septembre, puis révisée en octobre pour répondre aux retours de la communauté, notamment sur la flexibilité des layouts de données et la lisibilité du format. Julien Le Dem (co-créateur de Parquet) et Micah ont répondu pour saluer l'effort et apporter des retours de relecture, notamment sur la densité et le manque de documentation du proto du footer. L'objectif affiché est de stabiliser durablement le format du footer après cette refonte.

## Points clés
- La proposition introduit un « footer modulaire » pour Parquet, avec une nouvelle version publiée fin octobre 2026 corrigeant les retours sur la première version (septembre 2026).
- Deux axes de refonte majeurs : des « layouts de données flexibles » (les row groups ne sont plus supposés être des frontières physiques, les stats sont redéfinies par plages de lignes) et une « représentation basée sur les pages » remplaçant le concept jugé opaque d'EncodedArray.
- L'usage des pages Parquet pour stocker les métadonnées du footer permettrait d'obtenir gratuitement la compression par page, un point sensible quand le footer devient volumineux et ralentit les lectures à froid (cold reads).
- La piste de réutiliser les encodages Parquet existants pour le footer avait été écartée faute de support de l'accès aléatoire, mais elle redevient envisageable avec le développement de PFOR.
- Julien Le Dem souligne le caractère « transformationnel » du changement et espère qu'il stabilisera durablement le format de footer.
- Micah, après relecture, juge la conception bonne dans l'ensemble mais pointe un proto de footer dense nécessitant davantage de documentation pour en comprendre l'articulation.

## Analyse approfondie
Salut Jiayi,

J'ai fait une passe de relecture. Globalement, j'aime la conception. J'ai laissé une série de commentaires sur le proto du footer, que je trouve assez dense et qui gagnerait à être nettoyé/complété en documentation pour que les lecteurs puissent mieux comprendre comment tout s'articule.

Merci,
Micah

Le mar. 3 nov. 2026 à 16:21, Julien Le Dem via dev <[email protected]> a écrit :

> Merci Jiayi d'avoir porté cet effort, et merci à tous ceux qui ont contribué.
> J'encourage les personnes sur la liste à relire la proposition, car elle est plutôt transformationnelle pour le projet.
> Je pense qu'après cela, nous éviterons de changer à nouveau le format du footer pendant un certain temps.
>
> Le ven. 30 oct. 2026 à 07:20, Jiayi Wang <[email protected]> a écrit :
>
> > Bonjour à tous,
> >
> > Comme mentionné précédemment, nous avons révisé la proposition [1] pour la rendre plus flexible et répondre également aux retours existants. Je souhaite partager la nouvelle version de la proposition [2], incluse sous forme de nouvel onglet dans le même document. Voici un résumé de ce qui a changé et pourquoi :
> >
> > **Layouts de données flexibles**
> >
> > Suite aux discussions sur l'évolution du layout de données Parquet (par exemple la proposition de « pages non contiguës »), notre objectif est que le nouveau footer gère de façon fluide les layouts existants et les layouts futurs potentiels. La proposition mise à jour ne suppose plus que les row groups constituent des frontières physiques. Elle conserve la terminologie de « column chunks », mais ceux-ci sont simplement définis comme un ensemble contigu de pages pour une colonne donnée. Différentes colonnes peuvent avoir des nombres de chunks différents dans un même fichier. La terminologie « row group » est également conservée, mais les métadonnées de row group deviennent optionnelles. Enfin, les statistiques sont redéfinies sur la base de plages de lignes plutôt que de row groups ; différentes colonnes peuvent publier des statistiques à des granularités différentes.
> >
> > **Représentation basée sur les pages**
> >
> > Un retour important sur la proposition initiale était que le concept d'EncodedArray était opaque/confus. Il avait été ajouté pour modéliser efficacement des tableaux en Thrift et offrir un accès aléatoire, au prix de la lisibilité. La proposition mise à jour utilise les pages Parquet pour représenter les modules, ce qui produit un layout auto-descriptif qui évolue naturellement à mesure que Parquet gagne de nouveaux encodages. Cela permet également une compression optionnelle par page.
> >
> > Globalement, la nouvelle proposition produit un footer de taille et de performance comparables à la proposition d'origine, mais plus simple et plus flexible pour gérer les futurs changements de layout Parquet. Nous apprécions tout retour sur la proposition.
> >
> > Cordialement,
> >
> > Jiayi
> >
> > [1] https://docs.google.com/document/d/1xN4Nqh-fh-eH-cUz9e6Rqs_gPXRBKUh4s29EzX_NU8M/edit?tab=t.o42wlmqbbdma#heading=h.kfs863ye4rzw
> >
> > [2] https://docs.google.com/document/d/1xN4Nqh-fh-eH-cUz9e6Rqs_gPXRBKUh4s29EzX_NU8M/edit?tab=t.cbl5qtgc5xhz
> >
> > Jiayi Wang <[email protected]>, le lundi 19 octobre 2026 à 20:49, a écrit :
> >
> > > Bonjour à tous,
> > >
> > > Je souhaite partager une mise à jour sur l'avancement de la proposition de footer modulaire [1]. Nous avons reçu des retours précieux, et une suggestion récurrente était de rendre le footer plus pérenne en réutilisant les encodages Parquet.
> > >
> > > Nous avions auparavant écarté cette approche parce que les encodages Parquet existants ne supportent pas l'accès aléatoire. Cependant, avec PFOR en cours de développement et potentiellement d'autres encodages plus favorables à l'accès aléatoire à venir, nous pensons qu'il peut être utile de revisiter cette idée.
> > >
> > > Un autre point fréquemment soulevé concernait la compression, en particulier pour les cas où le footer devient suffisamment volumineux pour que sa taille constitue un goulot d'étranglement majeur lors des lectures à froid (cold reads). Si nous réutilisons les pages Parquet pour stocker les métadonnées du footer, nous pourrions aussi obtenir le support de la compression gratuitement, réduisant potentiellement encore davantage la taille du footer.
> > >
> > > En parallèle, nous voulons rendre le footer modulaire suffisamment flexible pour s'adapter aux futurs changements du layout de données Parquet. Par exemple, le layout de pages non contiguës proposé précédemment [2] nécessiterait la présence de l'offset index optionnel, et nous aimerions rendre sa représentation plus efficace. Notre objectif est de concevoir un footer capable de supporter de potentiels changements de layout comme celui-ci, tout en représentant efficacement le layout actuel.
> > >
> > > Nous continuons d'explorer ces pistes et partagerons des mises à jour à mesure que nous progressons. En attendant, n'hésitez pas à partager vos réflexions, préoccupations ou idées alternatives !
> > >
> > > Merci encore à tous ceux qui ont relu la proposition et apporté des retours !
> > >
> > > Cordialement,
> > > Jiayi
> > >
> > > [1] https://docs.google.com/document/d/1xN4Nqh-fh-eH-cUz9e6Rqs_gPXRBKUh4s29EzX_NU8M/edit?tab=t.o42wlmqbbdma
> > >
> > > [2] https://docs.google.com/document/d/1nntcYM98PFSkHT70RexSBPtCnWqg1uRJ5_7m--ZgbsA/edit?tab=t.0#heading=h.k4r8orckhbx0
> > >
> > > Jiayi Wang <[email protected]>, le lundi 21 septembre 2026 à 17:26, a écrit :
> > >
> > >> Bonjour à tous,
> > >>
> > >> Nous discutons du Footer Modulaire depuis un bon moment déjà, notamment via une réunion dédiée du groupe de travail sur le footer toutes les deux semaines, et nous avons enfin une proposition prête pour une relecture plus large.
> > >>
> > >> La proposition couvre la motivation, la conception du format, les considérations de compatibilité et les résultats de benchmarks. Un grand merci à tous ceux qui ont contribué au projet et aux discussions jusqu'à présent.
> > >>
> > >> Le document de proposition, la PR sur parquet-format et le ticket de suivi sont tous disponibles ici :
> > >>
> > >> Document de proposition : https://docs.google.com/document/d/1xN4Nqh-fh-eH-cUz9e6Rqs_gPXRBKUh4s29EzX_NU8M/edit?usp=sharing
> > >>
> > >> PR : https://github.com/apache/parquet-format/pull/623/changes
> > >>
> > >> Ticket parquet-format : https://github.com/apache/parquet-format/issues/622
> > >>
> > >> La proposition introduit plusieurs changements conceptuels significatifs, donc je m'attends à ce qu'il y ait beaucoup de discussion et de retours. Pour ce premier tour de relecture, je suggère de se concentrer principalement sur l'orientation générale et les choix de conception de haut niveau, et de laisser les questions plus détaillées (par exemple, si un champ particulier peut être déprécié) pour une discussion ultérieure. Je pense que cela nous aidera à converger d'abord sur les grandes questions de conception et à garder le processus de relecture efficace.
> > >>
> > >> Merci !
> > >>
> > >> Cordialement,
> > >> Jiayi

## Pourquoi ça compte
Ce fil illustre en temps réel le processus de gouvernance d'un projet Apache majeur (Parquet) face à une refonte structurelle rare de son format binaire, un sujet clé pour toute organisation s'appuyant sur ce format colonnaire omniprésent dans les stacks data (Spark, Iceberg, DuckDB, etc.) ; suivre ces discussions permet d'anticiper des changements de compatibilité et de performance pour les systèmes de stockage analytique.
