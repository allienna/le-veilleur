---
title: "Fast is a design decision"
date: 2026-11-25
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fshannadige.com%2Fblog%2Fperformance-is-design%2F%3Futm_source=tldrdev/1/010001a20d7d27e0-53e789d5-a97b-438e-8ffd-f9ea51c829a6-000000/I2vbbA96TlZgVCJ56hXYu_iQ_NrxmE-lKNeBMdCuMog=452"
authors: ["Shanna Dige"]
keywords: ["performance web", "design UX", "Core Web Vitals", "CDN", "lazy-loading", "agents IA"]
theme: "Software"
tone: "opinion"
used_in: ["2026-11-25"]
---

## Résumé

L'article soutient que si la fabrication d'un site web n'a jamais été aussi bon marché — un prompt suffit désormais là où il fallait des semaines — la rendre *rapide* reste un coût réel, payé en attention de la part des équipes et en temps/données du côté des visiteurs. L'auteure, qui a instrumenté un panneau de performance public sur son propre site, détaille les maillons techniques qui ralentissent une page (distance physique au serveur, mode de génération du HTML, cache, priorité de chargement des ressources, travail du thread principal) et montre par l'exemple que la plupart des décisions coûteuses en performance sont en réalité des décisions de design (vidéo en autoplay, polices personnalisées, carrousels, animations). Elle en tire six questions simples à poser à un agent IA pour auditer la performance d'un site, et publie son propre tableau de budgets de performance comparé aux résultats réels mesurés sur son site.

## Points clés

- Les générateurs de sites pilotés par IA ne posent pas spontanément de questions de performance ; un site peut paraître parfait sur la machine de développement tout en étant lent pour un visiteur réel (téléphone ancien, réseau mobile).
- Cinq facteurs techniques expliquent la majorité des lenteurs : la distance physique au serveur (résolue par un CDN), le mode de génération du HTML (statique, rendu serveur, ou assemblé côté client), la stratégie de cache, l'ordre/priorité d'arrivée des ressources, et le temps que le JavaScript bloque le thread principal.
- De nombreuses décisions de performance sont d'abord des décisions de design (vidéo plein cadre en autoplay, police sur mesure, carrousel au-dessus de la ligne de flottaison, animations continues) : le design doit donc être associé à l'arbitrage coût/bénéfice, pas seulement l'ingénierie.
- Le niveau d'exigence de performance dépend du type de page : une landing page se joue sur le premier écran, un formulaire/checkout sur la réactivité au clic, un dashboard sur l'instantanéité après le premier chargement, un portfolio sur l'ordre et le poids des médias.
- Six questions pratiques permettent d'auditer rapidement un site avec l'aide d'un agent IA : origine du HTML, lieu d'hébergement/CDN, règles de cache, poids et priorité du plus grand élément visible, quantité de JavaScript, et ressenti réel sur un téléphone bridé.
- L'auteure illustre sa méthode avec un tableau de budgets de performance (LCP, réactivité, CLS, poids transféré, JavaScript, tâche la plus longue, fréquence d'images) comparés aux résultats réels de son propre site, dont deux indicateurs dépassent légèrement le budget fixé.

## Analyse approfondie

### Une fable en guise d'ouverture

Le texte débute par une petite fable : trois designers d'une entreprise fictive (« Enterpriseland ») soignent chacun un aspect différent de leur travail — les états d'interface, la typographie, les micro-interactions — tout en naviguant dans une organisation bureaucratique où designers, PM et ingénieurs négocient longuement la version finale d'un produit. Résultat : des utilisateurs qui patientent de longues minutes devant des tableaux de bord qui chargent, sans que personne ne s'en aperçoive avant d'être réaffecté ailleurs. La morale, laissée en suspens, pose le thème de l'article : le soin apporté au design ne garantit pas une expérience rapide si la performance n'est pas pensée comme faisant partie du design lui-même.

### Tout le monde peut désormais construire

Il y a encore peu, monter un portfolio, une landing page ou un petit prototype prenait des semaines ou nécessitait un template. Désormais, un simple prompt suffit, ce qui démocratise largement la création web — y compris pour des designers habitués à déléguer l'implémentation. Mais ces outils ne demandent jamais comment le résultat doit *se comporter* en usage réel : personne ne pense à préciser dans son prompt qu'il ne faut pas différer le chargement de la plus grande image, ou qu'il faut servir le HTML depuis un point proche des visiteurs. Le site généré paraît donc impeccable sur l'ordinateur de son créateur, où tout est déjà en cache après des dizaines d'aperçus successifs — le meilleur des scénarios. Le pire, c'est un visiteur sur un téléphone de trois ans, dans un train, ouvrant le site pour la première fois. La création est devenue gratuite, mais une page lente a toujours un coût : c'est le visiteur qui le paie, en temps d'attente. C'est pour rendre ce coût visible que l'auteure a ajouté à son propre site un panneau « Performance », qui expose en toute transparence le temps de réponse serveur, les instants de premier et plus grand affichage, le poids téléchargé, la part de JavaScript, et la fluidité du défilement — autant de métriques que le navigateur mesure nativement.

### Où passe le temps

Le chargement d'une page est une succession de petites étapes, chacune pouvant introduire un ralentissement.

**La distance.** La lumière dans la fibre parcourt environ 200 km par milliseconde, et une connexion HTTPS nécessite plusieurs allers-retours avant que le premier octet de la page ne quitte le serveur. Entre Sydney et un serveur unique situé en Virginie, l'aller-retour avoisine 16 000 km, avant même les détours de routage : près d'une seconde d'attente avant le moindre affichage, un problème qu'aucun framework ne peut contourner puisqu'il relève des lois physiques. La solution consiste à rapprocher une copie du contenu des visiteurs via un CDN (Cloudflare, Fastly, le réseau périphérique de Vercel...), qui met en cache les fichiers dans des datacenters répartis dans le monde. Le site de l'auteure, riche en photos et vidéos, s'appuie ainsi sur Cloudflare pour éviter à ses visiteurs d'attendre le téléchargement de ces ressources depuis un unique serveur distant.

**L'origine du HTML.** Trois approches existent, aux coûts très différents : le HTML peut être *généré à l'avance* au moment du déploiement et simplement servi comme fichier statique (c'est le choix du site de l'auteure, construit avec Astro et distribué via le edge de Cloudflare, sans aucun calcul serveur au moment de la visite) ; il peut être *recalculé côté serveur à chaque requête*, adapté au contenu dynamique mais coûteux si le résultat n'est pas mis en cache ; ou il peut être *assemblé dans le navigateur*, le serveur n'envoyant qu'une coquille vide accompagnée d'un paquet de JavaScript que l'appareil du visiteur doit télécharger, analyser puis exécuter avant que quoi que ce soit ne s'affiche — une approche que moteurs de recherche et agents IA peuvent même percevoir comme une page vide. De nombreux générateurs d'applications grand public démarrent par défaut sur cette troisième option, pratique à prévisualiser mais pénalisante dès qu'il s'agit d'un contenu public (portfolio, blog, page marketing, documentation) plutôt que d'une application derrière authentification.

**Le cache.** Il détermine si une seconde visite, ou une seconde page, doit refaire tout le travail de la première. La règle suivie par l'auteure : donner à chaque fichier un nom qui change avec son contenu (la plupart des outils de build le font automatiquement) et autoriser les navigateurs à le conserver un an, tout en gardant le HTML lui-même à durée de vie courte pour que les nouveaux déploiements soient visibles immédiatement. Elle raconte avoir découvert, à ses dépens, que jusqu'à récemment tous les fichiers de son site étaient servis avec l'en-tête `max-age=0`, obligeant le navigateur à revérifier chaque fichier auprès du serveur avant de l'utiliser — soit une quarantaine d'allers-retours par page vue. À cela s'ajoutait une redirection systématique sur les liens internes (ajout d'une barre oblique finale), qui coûtait environ 800 ms par navigation sur un téléphone bridé.

**Le poids, et l'ordre d'arrivée.** Le volume de données compte, mais l'ordre dans lequel elles arrivent compte plus encore : le navigateur ne peut afficher le plus grand élément visible qu'une fois celui-ci reçu. Si cet élément est une image marquée `loading="lazy"` — un réglage par défaut pertinent pour les images situées plus bas dans la page — le navigateur retarde volontairement son chargement. C'est exactement ce qui pénalisait la version mobile du site de l'auteure : la première carte du carrousel de projets, pourtant le plus grand élément visible sur téléphone, était chargée en différé et à faible priorité, demandée vers 1,1 seconde et reçue seulement vers 2,5 secondes. La correction a consisté à la traiter différemment des autres images : les téléphones reçoivent désormais un petit aperçu pré-rendu de cette carte, chargé immédiatement en haute priorité.

**Le thread principal.** Le JavaScript ne coûte pas seulement du temps de téléchargement : pendant qu'il s'exécute, la page reste insensible aux interactions. Google mesure ce phénomène via l'indicateur *Interaction to Next Paint*, avec un seuil idéal sous 200 ms. Les causes habituelles sont les gros scripts exécutés au chargement ou les animations qui ne s'arrêtent jamais. L'auteure a identifié ce problème sur son propre site : l'animation de réseau décorative de sa section d'accueil continuait de se dessiner même après avoir défilé hors de l'écran, consommant environ 446 ms toutes les cinq secondes sur ordinateur pour afficher quelque chose d'invisible — le double sur les écrans à 120 Hz. Une logique a depuis été ajoutée pour désactiver cette animation dès qu'elle sort du champ visuel.

### L'ingénierie mesure, le design décide

Il serait tentant de réduire tout cela à une simple checklist technique : lancer un audit Lighthouse, corriger les alertes, livrer. L'ingénierie est effectivement l'endroit où la performance se mesure et se suit dans le temps — au même titre que la disponibilité d'un service — mais, selon l'expérience de l'auteure, la plupart des décisions coûteuses en performance sont d'abord des décisions de design. Une vidéo plein cadre en lecture automatique dans une section d'accueil relève du goût ; il en va de même pour une police personnalisée en quatre graisses, un carrousel de médias au-dessus de la ligne de flottaison, des animations pilotées par le défilement, ou une page qui ne devient utilisable qu'après l'exécution de 500 Ko de JavaScript. Aucune de ces décisions n'est condamnable en soi, mais chacune se paie en temps et en données du visiteur. Puisque le design est la discipline qui sait à quoi sert une page, il doit participer à l'arbitrage sur ce qui vaut la dépense — l'exigence dépendant du type de page :

- Une **landing page** se joue entièrement sur son premier écran : le plus grand élément affiché (mesuré par le LCP) constitue la première impression, et chaque seconde perdue coûte des visiteurs qu'on a parfois payé pour attirer. Il s'agit de déterminer la quantité minimale de contenu nécessaire pour transmettre l'essentiel de la marque ou du produit, et la vitesse à laquelle cela peut s'afficher sur les appareils de l'audience ciblée.
- Un **formulaire ou un parcours de paiement** se juge sur la réactivité à la saisie : un bouton qui met 400 ms à accuser réception d'un clic paraît défaillant, pousse les utilisateurs à cliquer à nouveau, et peut générer des cas limites côté API. Comprendre la durée réelle d'un appel permet de concevoir à bon escient un état désactivé ou un indicateur de chargement sur le bouton de validation.
- Un **tableau de bord consulté quotidiennement** peut tolérer un premier chargement plus lourd, dès lors que les visites suivantes bénéficient du cache, mais chaque interaction ultérieure doit être instantanée — ce qui pose la question de la persistance des données entre les sessions et les flux de travail de l'utilisateur.
- Un **portfolio** est avant tout du contenu : images, logos et vidéos incarnent le travail présenté, et l'enjeu consiste à envoyer la bonne taille de chaque élément dans le bon ordre, ce qui laisse ensuite la liberté de soigner leur mise en scène dans le respect des contraintes de performance et d'appareil.

### Six questions à poser à un agent IA

L'auteure soutient qu'aucune de ces vérifications ne nécessite un ingénieur spécialisé en performance : il suffit de poser six questions à l'agent avec lequel on développe. D'où vient le HTML — généré à l'avance, rendu côté serveur, ou assemblé dans le navigateur ? Si c'est la troisième option et que le contenu est public, que faudrait-il pour le pré-générer ? Où le site est-il hébergé — sur un CDN disposant de points de présence proches de l'audience visée, ou sur un unique serveur dans une seule région ? Que met-on en cache, et pour combien de temps (fichiers versionnés pendant un an, HTML à courte durée de vie), et peut-on afficher les en-têtes `Cache-Control` correspondants ? Quel est le plus grand élément du premier écran et à quel moment arrive-t-il — s'assurer qu'il n'est ni différé, ni bloqué derrière un script ? Quelle quantité de JavaScript la page charge-t-elle, et à quoi sert-elle — un demi-mégaoctet de script pour afficher du simple texte est suspect. Enfin, quel est le ressenti réel sur un téléphone lent, en activant la simulation de réseau et de processeur limités dans les outils de développement du navigateur, sachant qu'un ordinateur portable sur wifi rapide représente toujours le meilleur cas possible ? L'auteure conseille ensuite de consigner un budget de performance et de le rendre accessible à l'agent pour les futures sessions de travail (en tant que contexte ou « skill »).

Elle partage, à titre d'exemple, les objectifs retenus pour son propre site, comparés aux mesures réelles obtenues sur la page d'accueil, dans des conditions simulant un téléphone bridé proches de celles de Lighthouse (environ 1,6 Mbps, 150 ms de latence, processeur quatre fois plus lent qu'un ordinateur portable), en médiane sur trois chargements à froid :

| Mesure | Budget | Réel |
|---|---|---|
| Plus grand élément affiché (LCP) | moins de 2,5 s | 1,32 s |
| Réponse à la saisie | moins de 200 ms | 48 ms |
| Décalage de mise en page (CLS) | moins de 0,1 | 0,00 |
| Premier affichage | moins de 1,8 s | 1,32 s |
| Réponse du serveur | moins de 200 ms | 381 ms |
| Page d'accueil, poids transféré | moins de 1 Mo | 488 Ko |
| JavaScript | moins de 250 Ko | 209 Ko |
| Tâche la plus longue | moins de 50 ms | 78 ms |
| Fréquence d'images | 60 fps | 60 fps |

Deux indicateurs dépassent le budget fixé. La réponse du serveur est pénalisée par un problème de routage indépendant de la volonté de l'auteure : ses requêtes, lors du test, aboutissaient au datacenter Cloudflare d'Atlanta plutôt qu'à un point de présence plus proche, ce qui explique une centaine de millisecondes qu'elle aimerait récupérer mais devra arbitrer au regard de ses choix d'hébergement. La tâche la plus longue correspond à un unique segment de 78 ms pendant lequel la page reste insensible à une interaction ; ce chiffre ne s'allonge autant que sur un processeur lent, un test sur ordinateur de bureau se rapprochant davantage du seuil (59 ms observés). Les deux points figurent sur sa liste de corrections à venir.

## Pourquoi ça compte

À l'heure où la génération de sites par prompt se banalise, ce billet rappelle aux équipes produit, design et engineering qu'une expérience rapide reste un choix délibéré et mesurable, et non un sous-produit automatique des outils d'IA générative — un point de vigilance pertinent pour toute veille sur l'usage des agents IA dans la conception web.
