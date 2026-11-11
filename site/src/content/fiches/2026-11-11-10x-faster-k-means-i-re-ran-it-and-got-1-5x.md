---
title: "10x faster k-means? I re-ran it and got 1.5x"
date: 2026-11-11
url: "https://click.dataelixir.com/o8u44z23rdiqhn3vp5givhqqpe0q9hohmlmre/3ohphkh38w88l7irhn/aHR0cHM6Ly9kZXYudG8vZnJhbmtjaHUvMTB4LWZhc3Rlci1rLW1lYW5zLWktcmUtcmFuLWl0LWFuZC1nb3QtMTV4LTI0YmI_dXRtX2NhbXBhaWduPURhdGFfRWxpeGlyJnV0bV9zb3VyY2U9RGF0YV9FbGl4aXJfNTk3"
authors: ["frankchu"]
keywords: ["k-means", "clustering", "Faiss", "Meta FAIR", "reproductibilité", "machine learning"]
theme: "Data"
tone: "research"
used_in: ["2026-11-11"]
---

## Résumé
L'article e-means (Meta FAIR) revendique un k-means 10 à 45x plus rapide que Lloyd à perte égale, en remplaçant les mises à jour full-batch par des moyennes mobiles exponentielles en mini-batch. L'auteur, n'ayant pas accès au code promis (lien GitHub en 404), réimplémente la règle publiée en NumPy et ne reproduit qu'une accélération de 1,5x avec une perte 1,4 % plus mauvaise sur des données synthétiques bien séparées, et aucun gain sur des données sans structure. Une expérience-jouet du blog original (deux blobs de tailles très différentes) ne se reproduit correctement qu'après avoir ajouté deux éléments non triviaux du papier, l'initialisation par vecteurs aléatoires et la « réanimation » des clusters morts, sans lesquels e-means est en fait pire que Lloyd. L'auteur conclut que le chiffre de 10x est une affirmation valable dans un régime précis (grands k, vrais embeddings, kernels GPU) et non une vérité universelle.

## Points clés
- Réimplémentation indépendante de la règle de mise à jour e-means (Meta FAIR, arXiv:2611.09501) en NumPy, le code officiel annoncé par le blog étant introuvable (404 sur GitHub).
- Sur des blobs gaussiens synthétiques bien séparés : accélération de seulement 1,5x (contre 10x annoncé) et perte finale 1,4 % plus mauvaise que Lloyd.
- Sur des vecteurs aléatoires sans structure de cluster : aucun gain réel, et donner plus d'epochs (10 au lieu de 5) rend le résultat à la fois plus lent et moins bon.
- L'expérience-jouet du blog (deux blobs de tailles très différentes) ne se reproduit que si l'on implémente l'initialisation par vecteurs aléatoires et la réanimation des clusters morts — sans ces éléments, e-means est pire que Lloyd.
- Conclusion : la règle de mise à jour EMA seule n'est pas « l'algorithme » ; l'initialisation, la réanimation et la finalisation sont des composants structurants, et le gain de 10x semble réel surtout à grande échelle (embeddings réels, k élevé, GPU).

## Analyse approfondie
e-means promet un k-means 10 fois plus rapide à perte égale. Ma réimplémentation, construite à partir de leur règle de mise à jour publiée, a obtenu une accélération de 1,5x et une perte 1,4 % plus mauvaise — et le code vers lequel pointe leur article de blog renvoie une erreur 404.

L'article a été publié sur Hacker News aujourd'hui (251 points) : e-means, conçu par des chercheurs de Meta FAIR, remplace les mises à jour en full-batch de Lloyd par des moyennes mobiles exponentielles en mini-batch. Les chiffres annoncés sont impressionnants : une réduction du temps d'exécution de 10 à 45x sur GPU par rapport à Flash-KMeans, de 8 à 15x sur CPU par rapport à Faiss, et 1,6 à 2,4 epochs pour atteindre la perte de test que l'algorithme de Lloyd met 25 epochs à atteindre. L'article scientifique est arXiv:2611.09501, et le blog est inhabituellement précis sur la méthode — il publie la règle de mise à jour exacte ainsi que les lois d'échelle ajustées pour la taille de batch et le pas d'apprentissage. C'est cette précision qui en a fait quelque chose de testable.

Premier problème : le lien vers le code dans le blog pointe vers faiss/contrib/e_means. À ce jour, ce chemin renvoie une erreur 404 sur GitHub, et faiss-cpu 1.15.1 — la dernière version publiée sur pip — ne contient aucun module e_means. Le code n'est pas encore diffusable. J'ai donc réimplémenté moi-même la règle publiée en NumPy, en reprenant leurs constantes des lois d'échelle telles quelles :

```
# la mise à jour e-means, d'après le blog
S_j <- (1-a) * S_j + a * s_j
N_j <- (1-a) * N_j + a * n_j
c_j = S_j / N_j
# lois d'échelle, loi par défaut (tableau du blog)
B  = 0.035 * k**0.13 * n**0.88 * T**0.81
a0 = min(0.824 * k**-0.46 * B**0.90 * n**-0.45 * T**-0.11, 1)
```

S'ajoute une décroissance en cosinus de a, de a0 jusqu'à 0,1*a0, ainsi que l'étape de finalisation décrite par le blog : terminer sur la moyenne exacte de chaque cluster au dernier epoch. C'est l'intégralité de l'algorithme tel que publié. La référence est Faiss Kmeans (Lloyd), 25 itérations, mêmes données, même initialisation par points aléatoires, même machine : une VM à 4 vCPU.

Des blobs gaussiens synthétiques — 64 clusters structurés, le type de données où Lloyd converge vite et où il y a peu de marge pour faire mieux.

```
Lloyd 25 iters: 18.7s  final MSE=121.7232
e-means (my impl) 5 epochs: 12.4s  B=7972 a0=0.5197
  per-epoch MSE: [124.6628, 124.4564, 123.9563, 123.604, 123.5087, 123.4541]
  final MSE=123.4541  vs Lloyd 121.7232 (+1.42%)
  wall-clock speedup vs Lloyd-25: 1.51x
  e-means did NOT beat Lloyd-25 MSE within 5 epochs
```

1,5x, pas 10x — et une perte 1,4 % plus mauvaise, pas égale. Deux éléments jouent contre le chiffre phare ici. D'abord, mes données sont favorables à Lloyd : des blobs bien séparés, où 25 passes complètes de Lloyd sont peu coûteuses (Faiss les exécute en 18,7 secondes). Le chiffre de 8 à 15x sur CPU annoncé dans l'article est mesuré sur de vrais jeux de données d'embeddings (DEEP, SIFT, VIBE) comptant de 1M à 100M de points avec un k allant jusqu'à 65 536, où une passe complète de Lloyd représente la partie coûteuse. Ensuite, mon implémentation combine NumPy et un index Faiss reconstruit à chaque mini-batch — sans kernels fusionnés (fused kernels), ce qui est précisément, selon l'article, ce qui transforme les gains en epochs en gains de temps d'exécution réel.

Des vecteurs aléatoires normalisés, n=50 000, d=256, k=1 024 — sans aucune structure de cluster.

```
Lloyd 25 iters: 10.7s  MSE=0.9248
e-means T=5: 10.4s B=4331 a0=0.410
  per-epoch MSE=[0.9396, 0.9417, 0.9387, 0.936, 0.9352, 0.9347]
  final 0.9347 vs Lloyd 0.9248 (+1.07%)  speedup 1.03x
e-means T=10: 16.8s B=7594 a0=0.630
  final 0.9380 vs Lloyd 0.9248 (+1.43%)  speedup 0.64x
```

Pas de structure, pas de gain : 1,03x à 5 epochs, et lui donner 10 epochs l'a rendu plus lent et moins bon (0,64x, +1,43 %). La loi d'échelle augmente la taille du batch avec T, donc l'exécution à 10 epochs effectue moins d'étapes, mais plus grandes — et sur des données sans structure, la moyenne mobile exponentielle (EMA) se contente de tout lisser. C'est un régime que l'article ne prétend jamais couvrir : ses jeux de données sont de vrais embeddings avec une véritable structure en clusters.

L'affirmation la plus facilement vérifiable du blog repose sur un exemple-jouet (toy example) : deux blobs de tailles très différentes (900 points contre 100), k=8, 200 démarrages aléatoires. Lloyd reste bloqué dans la configuration pathologique — deux centroïdes sur le petit blob, le grand blob privé d'un centroïde — dans 26 % des démarrages ; e-means dans 3,5 % des cas.

Ma première tentative n'a rien reproduit : Lloyd bloqué à 0 %, e-means bloqué à 72 %. L'erreur venait de moi, et à deux niveaux. J'avais initialisé à partir de points de données aléatoires (ce qui place chaque centroïde sur un blob réel, si bien que Lloyd ne se retrouve presque jamais piégé) et j'avais sauté la réanimation des clusters morts (dead-cluster revival) que l'article mentionne explicitement. En corrigeant les deux points — initialisation par vecteurs aléatoires, comme dans les figures de l'article, plus une réanimation par division proportionnelle (on tire un cluster vivant avec une probabilité proportionnelle à sa taille, puis on le scinde en deux) — le résultat s'est inversé :

```
revive=False: Lloyd stuck 12.0%, e-means stuck 49.0%,
              mean MSE Lloyd 0.5934 vs e-means 0.6271 (+5.68%)
revive=True:  Lloyd stuck 25.5%, e-means stuck 14.0%,
              mean MSE Lloyd 0.5934 vs e-means 0.5909 (-0.43%)
blog claimed: Lloyd stuck 26%, e-means 3.5%
```

Le 25,5 % obtenu pour Lloyd, contre les 26 % annoncés, constitue une reproduction propre. Mon taux de blocage pour e-means (14,0 %) va dans le même sens que les 3,5 % annoncés, mais de façon plus faible — avertissement honnête de ma part : ma réanimation n'est qu'une approximation grossière de la leur, et mon critère de « blocage » est un indicateur approché (plus de 1 % plus mauvais que le meilleur des deux runs pour cette graine aléatoire), pas leur définition exacte de configuration pathologique. Malgré cela, la perte moyenne (MSE) change de signe une fois la réanimation activée : e-means passe de +5,68 % plus mauvais à -0,43 % meilleur.

Le chiffre phare de 10x est une affirmation valable dans un certain régime, pas une vérité universelle. Il se vérifie là où les passes complètes de Lloyd constituent le goulot d'étranglement — k élevé, vrais embeddings, kernels GPU — et il dépend des composants que l'article qualifie d'essentiels. L'expérience-jouet en est la preuve : la même règle de mise à jour EMA, sans réanimation des clusters morts, est plus mauvaise que Lloyd sur le propre exemple-jouet des auteurs (49 % de blocage contre 12 %). Avec la réanimation, elle bat Lloyd. La règle de mise à jour n'est pas l'algorithme. L'initialisation, la réanimation et la finalisation sont des éléments structurants (load-bearing), et une réimplémentation qui les omet mesure en réalité une autre méthode.

Deux mises en garde honnêtes. D'abord, il s'agit de ma réimplémentation d'une règle publiée, pas du code des auteurs — qui n'est pas encore disponible publiquement, malgré le lien présent dans le blog. Ensuite, mes jeux de données sont synthétiques et de petite taille ; les chiffres de l'article proviennent de 24 jeux de données allant jusqu'à 100M de points. Le facteur 10x est peut-être bien réel à cette échelle. Mais à l'échelle à laquelle la plupart d'entre nous effectuons réellement du clustering — 100 000 points, k de l'ordre de quelques milliers, sur CPU — ce que j'ai mesuré est un facteur 1,5x et une perte légèrement plus mauvaise, et le résultat de l'exemple-jouet ne se reproduit qu'une fois qu'on implémente les parties qu'il est facile de négliger.

Sources : blog e-means, e-means.github.io (Hacker News, 9 novembre 2026) ; arXiv:2611.09501, « e-means: outperforming k-means (in one-tenth the epochs) » ; vérification via l'API GitHub sur facebookresearch/faiss, chemin faiss/contrib/e_means (404, 9 novembre 2026) ; faiss-cpu 1.15.1. Tous les temps ont été mesurés sur cette même machine (VM à 4 vCPU) : Faiss Kmeans comparé à ma réimplémentation NumPy, même initialisation, mêmes données.

## Pourquoi ça compte
Ce cas illustre un réflexe essentiel pour la veille tech en data/IA : les chiffres marketing d'un papier (« 10x ») masquent souvent des composants d'implémentation non triviaux (initialisation, réanimation, finalisation) sans lesquels le gain annoncé ne se matérialise pas, voire s'inverse à petite échelle ou en l'absence de code source public.
