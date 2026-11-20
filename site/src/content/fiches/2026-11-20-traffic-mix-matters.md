---
title: "Traffic mix matters"
date: 2026-11-20
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fbrooker.co.za%2Fblog%2F2026%2F11%2F18%2Fworkload-mix.html%3Futm_source=tldrdev/1/010001a1f3bb3b59-ebc0ffb5-47e0-4b94-b036-dfe610dd3710-000000/j6N14ePi198evzSQGn-WdNVysxS_rkv6N_bQU-ro22g=452"
authors: ["Marc Brooker"]
keywords: ["mix de trafic", "load testing", "bases de données relationnelles", "concurrence", "Aurora DSQL", "cache"]
theme: "Software"
tone: "research"
used_in: ["2026-11-20"]
---

## Résumé
L'article revient sur le rapport préliminaire de la panne M365 de la semaine dernière, qui pointait un problème latent non détecté lors des tests de charge en raison du « traffic mix » (mix de trafic) et des SKUs utilisés en labo. L'auteur illustre, via deux simulateurs simples, à quel point la performance des systèmes informatiques est extrêmement sensible à la composition du workload : un système à verrous (locks) souffre d'une distribution de clés très déséquilibrée (loi de Zipf), alors qu'un système avec cache se comporte exactement à l'inverse et profite de ce déséquilibre. La conclusion est que la fidélité du mix de trafic dans les tests de charge est ce qui distingue un bon test de charge d'une perte de temps totale, le débit pouvant varier de plusieurs ordres de grandeur dans un sens ou dans l'autre selon la distribution des clés.

## Points clés
- Le rapport préliminaire sur la panne M365 révèle que les tests de charge habituels n'ont pas détecté le problème latent à cause du mix de trafic et des SKUs utilisés en laboratoire, différents de la production.
- Dans un système à verrous (modèle d'une base relationnelle classique), plus la distribution des clés est déséquilibrée (Zipf), moins le débit global est élevé, car quelques clés très contestées sous-utilisent le reste des ressources.
- Dans un système avec cache local rapide (LRU) adossé à un stockage plus lent (modèle proche de Postgres), c'est l'inverse : plus la distribution est déséquilibrée, meilleure est la performance, sur une plage assez large.
- Ces deux courbes opposées montrent que le débit peut varier de plusieurs ordres de grandeur selon des détails aussi subtils que le skew des clés dans le workload de benchmark.
- Ce phénomène est particulièrement marqué pour les systèmes de type base de données relationnelle, mais s'applique à des systèmes de toutes natures.
- L'auteur y voit un argument en faveur du contrôle de concurrence optimiste et des architectures à mode unique de coût/latence, citant Aurora DSQL comme exemple où toutes les lectures passent par une seule couche de stockage rapide, sans attente sur des verrous.

## Analyse approfondie
Le rapport préliminaire sur la panne M365 de la semaine dernière contient une déclaration qui a particulièrement attiré mon attention :

> Nos tests de charge habituels n'ont pas détecté le problème latent en raison [du] mix de trafic et des SKUs utilisés dans nos laboratoires.

Ce rapport aborde de nombreux aspects (comme c'est le cas pour tout rapport portant sur un système complexe), mais je voulais me concentrer sur ce point précis : le *mix de trafic*. C'est important, car c'est l'élément qui fait toute la différence entre un excellent test de charge et une perte de temps totale.

La performance des systèmes informatiques est extrêmement sensible au mix de workload.

Commençons par un simulateur simple, représentant un système doté d'une table de verrous. Les requêtes arrivent avec une clé, détiennent le verrou associé à cette clé pendant un certain temps, puis libèrent le verrou et se terminent. Ce n'est pas un modèle mental déraisonnable d'une base de données relationnelle, où chaque transaction détient un verrou pendant son exécution.

Clés (N) :

Chaque requête occupe l'un des 16 threads de travail, attend dans une file FIFO le verrou sur sa clé, détient ce verrou pendant une durée distribuée exponentiellement (moyenne de 1 ms), puis le libère et libère son thread. Les clés sont tirées selon une distribution de Zipf sur N clés ; un coefficient de 0 correspond à une distribution uniforme.

Comme on pouvait s'y attendre, plus la distribution est déséquilibrée, moins le débit obtenu du système est élevé. Un petit nombre de clés fait l'objet d'une forte contention, ce qui entraîne une sous-utilisation du reste des ressources de la machine, du fait de la limite globale de concurrence.

Considérons maintenant un modèle mental différent d'une base de données relationnelle (du moins une base mono-système comme Postgres) : un cache local rapide, en mémoire, contenant une partie des données consultées, adossé à un stockage plus lent contenant le reste des données.

Clés (N) : Taille du cache : % des clés Le cache est × fois plus rapide que le stockage

Chaque requête occupe l'un des mêmes 16 threads de travail et lit sa clé. Un hit est servi depuis un cache LRU ; un miss va au stockage (distribué exponentiellement, moyenne de 1 ms) et la clé est ajoutée au cache. Les clés sont tirées selon une distribution de Zipf sur N clés ; un coefficient de 0 correspond à une distribution uniforme. Notez l'échelle logarithmique sur l'axe du débit.

Cette courbe évolue dans l'autre sens ! Plus la distribution est déséquilibrée, meilleure est la performance, sur une plage assez large. C'est précisément ce qui rend si important le fait que le mix de trafic dans les tests de charge et les benchmarks corresponde au trafic réel de production : le débit peut varier de plusieurs ordres de grandeur, dans un sens comme dans l'autre, en fonction d'éléments aussi subtils que le déséquilibre (skew) des clés dans le workload du benchmark. Cela est particulièrement vrai pour les systèmes de type base de données relationnelle, mais s'applique à des systèmes de toutes natures.

**Aparté** : c'est aussi une raison pour laquelle j'apprécie le contrôle de concurrence optimiste, ainsi que les architectures présentant un *mode* unique de coût/latence. Aurora DSQL reflète cette logique visant à rendre les systèmes moins sensibles au workload : toutes les lectures passent par une seule couche de stockage rapide, et personne ne détient de ressources en attendant des verrous.

## Pourquoi ça compte
Cet article rappelle une leçon essentielle pour quiconque conçoit des tests de charge ou dimensionne des systèmes en production : un benchmark dont le mix de trafic ne reflète pas la réalité peut masquer des problèmes critiques, comme l'a illustré la panne M365, et conduire à des décisions d'architecture erronées.
