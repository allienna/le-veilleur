---
title: "e-means: 10x faster k-means at equal loss - Blog"
date: 2026-11-18
url: "https://click.dataelixir.com/92uoov93pginhxqqm24t9hzzkeo2dcwhl6l90/n2hohvhvdo6xm3c6hg/aHR0cHM6Ly9lLW1lYW5zLmdpdGh1Yi5pby8_dXRtX2NhbXBhaWduPURhdGFfRWxpeGlyJnV0bV9zb3VyY2U9RGF0YV9FbGl4aXJfNTk3"
keywords: ["k-means", "clustering", "optimisation GPU", "scaling laws", "mini-batch", "codebooks"]
theme: "Data"
tone: "research"
used_in: ["2026-11-18"]
---

## Résumé
E-means est une nouvelle règle d'optimisation pour le problème du k-means, qui remplace la mise à jour classique de l'algorithme de Lloyd par une moyenne mobile exponentielle appliquée par mini-lots. Sur une large gamme d'échelles et de jeux de données, elle atteint une perte de test inférieure à celle de Lloyd après 25 epochs en seulement 1,2 à 3 epochs, soit un gain de temps de calcul de 10 à 45× sur GPU (face à Flash-KMeans) et de 8 à 15× sur CPU (face à Faiss). La méthode se règle automatiquement grâce à des lois d'échelle qui fixent la taille de lot et le pas d'apprentissage, et améliore aussi l'initialisation, la relance des clusters « morts » et la phase de finalisation. Le code est publié dans le dépôt Faiss et l'approche est documentée dans un article arXiv.

## Points clés
- E-means obtient simultanément une meilleure vitesse et une meilleure qualité (perte plus basse), alors que ces deux objectifs sont généralement antagonistes en k-means.
- La règle de mise à jour centrale repose sur une moyenne mobile exponentielle (EMA) par mini-lots, plutôt que la recomputation complète (Lloyd) ou l'accumulation sans oubli (MacQueen).
- Aucun réglage manuel d'hyperparamètres n'est nécessaire : deux lois d'échelle déterminent automatiquement la taille de lot B et le pas α à partir des caractéristiques du problème (n, k, T).
- Une nouvelle stratégie de relance des clusters morts, par division proportionnelle de clusters actifs, réduit drastiquement le nombre de centroïdes inactifs comparé à la méthode d'EnCodec.
- Les mini-lots apportent du bruit qui aide à échapper aux minima locaux, alors que Lloyd, en diminuant toujours sa perte, reste plus souvent piégé dans des configurations sous-optimales.
- La méthode a été validée sur 24 jeux de données/configurations et 234 configurations comparatives (16 datasets, de 100k à 100M points).

## Analyse approfondie
**Le problème du k-means.** Étant donné un ensemble fixe de n points X = {x₁, ..., xₙ} ⊂ Rᵈ et un entier k, le problème consiste à trouver k centroïdes C = (c₁, ..., cₖ) minimisant la distance quadratique moyenne entre chaque point et son centroïde le plus proche. Il s'agit d'un jeu de données statique, à la différence de l'apprentissage de codebooks dans les VQ-VAE, où la distribution à regrouper évolue constamment pendant l'entraînement.

**Objectif du projet.** E-means vise à fournir une règle d'optimisation moderne pour le k-means. Les auteurs ont opté pour des mises à jour par mini-lots combinées à une moyenne mobile exponentielle, jugée la plus efficace pour ce problème. Contrairement aux approches par mini-lots précédentes, e-means ne nécessite aucun réglage d'hyperparamètres car il fixe automatiquement la taille de lot et le pas via des lois d'échelle. La méthode améliore également l'initialisation et la stratégie de relance des clusters morts, ajoute une décroissance du taux d'apprentissage selon un planning cosinus, et introduit une étape de finalisation qui réduit la perte d'entraînement pour un coût de calcul négligeable. E-means est fortement parallélisable et s'accompagne de noyaux de calcul spécialisés qui traduisent cet avantage algorithmique en gains de temps réels.

**Comparaison des règles de mise à jour des centroïdes.** La mise à jour des centroïdes est l'élément central d'e-means. Toutes les méthodes maintiennent, pour chaque cluster j, une somme Sⱼ et un compte Nⱼ des points qui lui sont assignés, le centroïde étant leur ratio. Elles ne diffèrent que par la façon dont Sⱼ et Nⱼ sont mis à jour (sⱼ et nⱼ désignant la somme et le compte des points du lot courant assignés au cluster j, les deux étant nuls si aucun point n'y est assigné) :

- *Algorithme de Lloyd* : chaque point est assigné à son centroïde le plus proche et les statistiques sont recalculées entièrement, en utilisant le jeu de données complet comme lot. Le centroïde est donc la moyenne exacte des points qui lui sont actuellement assignés. Chaque mise à jour coûte un passage complet sur les données, et la procédure est répétée un nombre fixe de fois (typiquement 20 à 50 itérations).
- *Mise à jour de MacQueen* : les statistiques sont accumulées sans jamais être écartées, si bien que le centroïde est la moyenne uniforme de tous les points assignés au cluster depuis le début de l'entraînement, y compris ceux assignés sous des positions de centroïdes antérieures, potentiellement mauvaises. La méthode « Staleness-Reduction Mini-Batch K-Means », hybride entre k-means et MacQueen, a partiellement corrigé ce défaut et obtenu des gains de vitesse importants, mais seulement pour un très faible nombre de clusters.
- *E-means* : travaille par mini-lots et remplace cette somme par une moyenne mobile exponentielle, de sorte que les assignations plus anciennes sont oubliées à un taux α, et que le centroïde suit les assignations récentes plutôt que tout l'historique. Cette règle de mise à jour est habituellement utilisée pour des distributions mouvantes, d'où son adoption pour l'entraînement des VQ-VAE. Les auteurs ont constaté qu'elle est aussi extrêmement efficace sur des jeux de données statiques, à condition d'être combinée aux autres composants d'e-means et avec des hyperparamètres correctement réglés.

**Origine du projet.** E-means prend sa source dans des travaux antérieurs menés chez Meta FAIR par Hugo Touvron et Hervé Jégou, qui avaient montré que le k-means par mini-lots via descente de gradient pouvait surpasser l'algorithme de Lloyd. L'auteur du projet a pu reproduire ces résultats, mais a constaté que la performance des mises à jour de centroïdes basées sur la descente de gradient devient instable à grand taux d'apprentissage, contrairement aux mises à jour par moyenne mobile exponentielle. L'hypothèse avancée est que les mises à jour EMA garantissent que le centroïde reste toujours dans l'enveloppe convexe des points qui lui sont assignés, alors que la descente de gradient peut dépasser cette enveloppe. C'est pour atteindre la perte la plus basse à un nombre fixe d'epochs que le choix s'est porté sur les mises à jour par moyenne mobile exponentielle — d'où le nom « e-means ».

**Lloyd comme cas particulier.** Si l'on fixe la taille de lot au jeu de données complet (B = n) et α = 1, alors Nⱼ et Sⱼ deviennent exactement le compte et la somme de l'ensemble du cluster : une itération d'e-means devient alors exactement une itération de Lloyd. Lloyd est donc un cas extrême d'e-means, sans décroissance cosinus du taux d'apprentissage. Or, la recherche d'hyperparamètres a montré que ce réglage extrême est fortement sous-optimal, ce qui explique pourquoi e-means surpasse largement Lloyd : en mesurant la perte pour chaque taille de lot B et chaque pas α, Lloyd se retrouve dans un coin de l'espace de recherche, bien loin de la région où la perte est la plus basse. Cette étude a motivé la dérivation de lois d'échelle permettant de choisir automatiquement la taille de lot B et le pas optimaux.

**Échapper aux minima locaux.** Pour comprendre pourquoi e-means atteint de meilleures pertes que Lloyd à convergence, les auteurs ont tracé plusieurs entraînements sur des jeux de données synthétiques afin d'évaluer leur capacité à échapper aux minima locaux. En répétant les entraînements sur 200 graines aléatoires, ils ont constaté qu'e-means tombe beaucoup moins souvent dans des configurations pathologiques que Lloyd. L'explication avancée est que les mini-lots introduisent des mises à jour plus bruitées, ce qui favorise l'exploration du paysage d'optimisation et permet d'échapper aux minima locaux, alors que Lloyd, dont la perte ne fait que décroître, a davantage tendance à exploiter les minima locaux trouvés sans jamais s'en échapper.

**Lois d'échelle pour le réglage automatique.** Une propriété essentielle d'e-means est qu'aucun hyperparamètre supplémentaire n'est à régler par rapport à l'algorithme de Lloyd. Deux lois d'échelle ont été ajustées pour fixer la taille de lot B et le pas initial α₀ à partir des caractéristiques du problème (n, k, T), et elles montrent une forte généralisation sur des jeux de données et des échelles de problème non vus à l'entraînement :

| loi | constante | exposant de k | exposant de B | exposant de n | exposant de T | regret (datasets non vus) | regret (tailles non vues) | R² |
|---|---|---|---|---|---|---|---|---|
| pas α₀ | 0,824 | −0,46 | 0,90 | −0,45 | −0,11 | 0,07% | 0,07% | 0,95 |
| lot B, loi par défaut | 0,035 | 0,13 | n/a | 0,88 | 0,81 | 0,19% | 0,20% | 0,96 |
| lot B, loi « qualité » | 0,0044 | 0,13 | n/a | 0,88 | 0,81 | 0,07% | 0,06% | n/a |

Deux équations sont proposées pour choisir la taille de lot : la loi « par défaut » et la loi « qualité », cette dernière sacrifiant du débit en échange d'une meilleure qualité de clustering par rapport à la loi par défaut.

**Relance des clusters morts.** Le principal écueil du k-means par mini-lots est sa propension à produire des clusters « morts », des centroïdes qui se retrouvent sans aucun point assigné en cours d'optimisation. Cela réduit la taille effective du codebook, un problème d'autant plus sensible que les codebooks utilisés aujourd'hui sont de plus en plus grands. Une parade courante consiste à réinitialiser les clusters dont la taille tombe sous un certain seuil, comme le fait EnCodec, où les centroïdes morts sont simplement remplacés par des échantillons aléatoires tirés du lot entrant. Si cela aide, le problème n'est pas pleinement résolu. Plutôt que d'échantillonner des points arbitraires dans le lot, les auteurs relancent les clusters morts en divisant des clusters actifs existants et de grande taille : un cluster actif est tiré avec une probabilité proportionnelle à sa taille, puis scindé en deux. Cette approche, adaptée du k-means de Faiss, s'avère nettement plus efficace pour éliminer les clusters morts et préserver la capacité du codebook :

| dataset | politique de relance | clusters morts | % du codebook | déséquilibre | MSE de test |
|---|---|---|---|---|---|
| DEEP | division proportionnelle | 47 | 0,3% | 1,194 | 0,38762 |
| DEEP | rééchantillonnage du lot (EnCodec) | 2 343 | 14,3% | 1,423 | 0,39124 |
| DEEP | désactivé | 4 313 | 26,3% | 1,647 | 0,39448 |
| SIFT | division proportionnelle | 10 | 0,1% | 1,186 | 0,19623 |
| SIFT | rééchantillonnage du lot (EnCodec) | 750 | 4,6% | 1,233 | 0,19684 |
| SIFT | désactivé | 2 080 | 12,7% | 1,404 | 0,19797 |

**Validation et disponibilité.** E-means a été validé sur 24 jeux de données et configurations différents, mêlant embeddings et données synthétiques (détails dans l'article). Pour la démonstration vidéo, 234 configurations d'e-means ont été comparées à k-means sur 16 jeux de données allant de 100k à 100M de points. Le code est disponible dans le dépôt Faiss (faiss/contrib/e_means), et les auteurs demandent de citer l'article correspondant (arXiv:2611.09501) en cas d'utilisation.

## Pourquoi ça compte
Le k-means reste un algorithme de base pour la quantification vectorielle (codebooks, VQ-VAE, recherche de similarité à grande échelle) ; un gain de 10 à 45× en temps de calcul sans perte de qualité, obtenu sans réglage d'hyperparamètres, est directement exploitable dans les pipelines de données et d'IA qui s'appuient sur du clustering massif.
