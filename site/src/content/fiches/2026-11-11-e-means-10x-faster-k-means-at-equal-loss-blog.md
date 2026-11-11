---
title: "e-means: 10x faster k-means at equal loss - Blog"
date: 2026-11-11
url: "https://click.dataelixir.com/o8u44z23rdiqhn3vp5givhqqpe0q9hohmlmre/9qhzhnhd8788mga9h3/aHR0cHM6Ly9lLW1lYW5zLmdpdGh1Yi5pby8_dXRtX2NhbXBhaWduPURhdGFfRWxpeGlyJnV0bV9zb3VyY2U9RGF0YV9FbGl4aXJfNTk3"
keywords: ["k-means", "clustering", "Faiss", "VQ-VAE", "lois d'échelle", "mini-batch"]
theme: "Data"
tone: "research"
used_in: ["2026-11-11"]
---

## Résumé
e-means est une nouvelle règle de mise à jour des centroïdes pour le problème du k-means, qui atteint une perte inférieure à celle de l'algorithme de Lloyd en seulement 1,2 à 3 epochs au lieu de 25. Mesuré de bout en bout, cela se traduit par une réduction du temps d'exécution de 10 à 45× sur GPU (face à Flash-KMeans) et de 8 à 15× sur CPU (face à Faiss), tout en obtenant une meilleure qualité de clustering — alors que vitesse et qualité sont habituellement antagonistes en k-means. La méthode repose sur des mises à jour par mini-batchs via moyenne mobile exponentielle (EMA), ne nécessite aucun réglage manuel d'hyperparamètres grâce à des lois d'échelle automatiques, et améliore la gestion des clusters morts. Le projet prolonge des travaux initiés chez Meta FAIR et est publié dans Faiss, avec un papier associé sur arXiv.

## Points clés
- Gains de 10 à 45× sur GPU et 8 à 15× sur CPU par rapport aux implémentations de référence (Flash-KMeans, Faiss), avec une perte finale meilleure que celle de Lloyd.
- Utilise des mises à jour par mini-batchs avec moyenne mobile exponentielle (EMA), plutôt qu'un passage complet sur les données (Lloyd) ou une moyenne cumulative depuis le début (MacQueen).
- Aucun réglage d'hyperparamètre requis : deux lois d'échelle fixent automatiquement la taille de batch et le pas d'apprentissage à partir des caractéristiques du problème (n, k, T).
- Nouvelle stratégie de réanimation des clusters morts par scission proportionnelle des gros clusters, nettement plus efficace que le rééchantillonnage utilisé dans EnCodec.
- Le bruit introduit par les mini-batchs permet de mieux échapper aux minima locaux que Lloyd, confirmé sur 200 graines aléatoires.
- Validé sur 24 jeux de données/configurations (embeddings et données synthétiques) et sur 234 configurations supplémentaires (16 jeux de données, de 100k à 100M de points) ; code ouvert dans `faiss/contrib/e_means`.

## Analyse approfondie
Sur une large gamme d'échelles et de jeux de données, e-means atteint une perte de test inférieure à celle de Lloyd à 25 epochs, en seulement 1,2 à 3 epochs. Mesuré de bout en bout, cela représente une réduction du temps d'exécution de 10 à 45× sur GPU par rapport à l'implémentation de Lloyd de référence (Flash-KMeans[2]), et de 8 à 15× sur CPU par rapport à Faiss[1]. Vitesse et qualité s'opposent généralement en k-means, alors qu'e-means obtient à la fois une meilleure vitesse et une meilleure perte.

Étant donné un jeu de données fixe de n points X = {x₁, ..., xₙ} ⊂ Rᵈ et un entier k, le problème du k-means consiste à trouver k centroïdes C = (c₁, ..., cₖ) minimisant la distance quadratique moyenne entre chaque point et son centroïde le plus proche :

Il s'agit d'un jeu de données statique, contrairement à l'apprentissage de codebook dans les VQ-VAE, où la distribution à regrouper est en perpétuel mouvement.

L'objectif d'e-means est de fournir une règle d'optimisation moderne pour le problème du k-means. Nous avons démarré ce projet à partir des observations suivantes :

Pour e-means, nous avons choisi de réaliser des mises à jour par mini-batchs avec des moyennes mobiles exponentielles (EMA)[6], que nous avons trouvées les plus efficaces pour le problème du k-means. Contrairement aux approches par mini-batchs précédentes, e-means ne nécessite aucun réglage d'hyperparamètre car il fixe automatiquement la taille de batch et le pas (step size) grâce à des lois d'échelle (scaling laws) (voir Réglage automatique des hyperparamètres par lois d'échelle). De plus, e-means améliore l'initialisation et la stratégie de réanimation des clusters morts (dead-cluster revival), ajoute un taux de décroissance planifié en cosinus (cosine-scheduled decay rate), et introduit une étape de finalisation qui réduit la perte d'entraînement pour un coût de calcul négligeable en fin d'entraînement. e-means est hautement parallélisable, et s'accompagne de kernels spécialisés qui traduisent son avantage algorithmique en gains de vitesse réels (wall-clock speedups).

La règle de mise à jour des centroïdes est le composant central d'e-means. Cette section vise à donner un aperçu des règles de mise à jour pour le clustering k-means. Toutes les méthodes maintiennent, pour chaque cluster j, une somme Sⱼ et un compte Nⱼ des points qui lui sont assignés, et prennent le centroïde comme leur rapport :

Elles ne diffèrent que par la façon dont Sⱼ et Nⱼ sont mis à jour. Ci-dessous, sⱼ et nⱼ désignent la somme et le compte des points du batch courant assignés au cluster j (les deux valant zéro si aucun point ne lui est assigné).

**L'algorithme de Lloyd**[7] assigne chaque point à son centroïde le plus proche et recalcule les statistiques depuis zéro, en utilisant le jeu de données complet comme batch :

ainsi cⱼ est la moyenne exacte des points qui lui sont actuellement assignés. Chaque mise à jour coûte un passage complet sur les données, et la procédure est répétée un nombre fixe de fois (typiquement 20 à 50 itérations).

**La mise à jour de MacQueen**[3] accumule les statistiques sans jamais les écarter :

ainsi cⱼ est la moyenne uniforme de tous les points assignés au cluster j depuis le début de l'entraînement, y compris les points assignés sous des positions de centroïdes antérieures, potentiellement médiocres. Ce problème a été partiellement traité plus tard par Staleness-Reduction Mini-Batch K-Means[8], une méthode hybride entre k-means et MacQueen. Elle a permis d'obtenir des gains de vitesse importants, mais uniquement pour de très petits nombres de clusters.

**e-means** fonctionne par mini-batchs et remplace cette somme par une moyenne mobile exponentielle :

ainsi les anciennes assignations sont oubliées au taux α, et le centroïde suit les assignations récentes plutôt que l'historique complet. Cette règle de mise à jour est habituellement utilisée pour des distributions mouvantes, d'où son adoption pour l'entraînement des VQ-VAE[6]. Ce que nous avons découvert, c'est qu'elle est également extrêmement efficace pour des jeux de données statiques, à condition de la combiner avec les autres composants d'e-means et de bien régler les hyperparamètres.

Le projet e-means est parti de travaux antérieurs menés chez Meta FAIR par Hugo Touvron et Hervé Jégou, qui avaient constaté qu'un k-means par mini-batchs via descente de gradient pouvait surpasser l'algorithme de Lloyd. Si j'ai pu reproduire ces résultats, j'ai constaté que la performance des mises à jour de centroïdes basées sur la descente de gradient devient instable à des taux d'apprentissage élevés, contrairement aux mises à jour par moyenne mobile exponentielle. Je soupçonne que cela s'explique par le fait que les mises à jour EMA garantissent que le centroïde reste toujours dans l'enveloppe convexe des points qui lui sont assignés, alors que les mises à jour par descente de gradient peuvent dépasser cette enveloppe.

Afin d'obtenir la perte la plus faible à un nombre fixe d'epochs, nous avons choisi les mises à jour par moyenne mobile exponentielle, d'où le nom e-means donné à notre méthode.

Si l'on fixe le batch au jeu de données complet, B = n, *et* α = 1, alors Nⱼ et Sⱼ deviennent exactement le compte et la somme de l'ensemble du cluster, si bien qu'une itération d'e-means devient exactement une itération de Lloyd. Lloyd est donc un cas extrême d'e-means, sans planification en cosinus du taux d'apprentissage. Cependant, notre recherche d'hyperparamètres a montré que ce réglage extrême est hautement sous-optimal, ce qui explique pourquoi e-means surpasse largement Lloyd. Ci-dessous, la perte est mesurée pour chaque taille de batch B et chaque pas α : Lloyd se retrouve dans un coin, bien en dehors de la région où la perte est la plus faible.

Cette étude d'hyperparamètres nous a motivés à dériver des lois d'échelle qui choisissent automatiquement la taille de batch B et le pas α optimaux.

Pour mieux comprendre pourquoi e-means atteint de meilleures pertes que Lloyd à convergence, nous avons tracé quelques entraînements sur des jeux de données jouets (toy datasets) afin d'évaluer leur capacité à échapper aux minima locaux. En répétant les entraînements sur 200 graines (seeds) aléatoires, nous avons constaté qu'e-means a beaucoup moins tendance à tomber dans des configurations pathologiques que Lloyd.

Notre explication est que les mini-batchs produisent des mises à jour plus bruitées, qui ont davantage de chances d'explorer le paysage d'optimisation et d'échapper aux minima locaux. Lloyd, avec sa perte toujours décroissante, a quant à lui davantage tendance à exploiter les minima locaux trouvés et à ne jamais s'en échapper.

Une propriété essentielle d'e-means est que les praticiens n'ont besoin de régler aucun hyperparamètre supplémentaire par rapport à l'algorithme de Lloyd. Nous avons ajusté deux lois d'échelle pour fixer la taille de batch `B` et le pas initial α₀ à partir des caractéristiques du problème `(n, k, T)`, et avons constaté qu'elles généralisaient fortement à des jeux de données et des échelles de problèmes inédits.

| loi | constante | exposant de | | | | regret, jeux de données retenus | regret, taille retenue | R² |
|---|---|---|---|---|---|---|---|---|
| | | k | B | n | T | | | |
| pas α₀ | 0,824 | −0,46 | 0,90 | −0,45 | −0,11 | 0,07% | 0,07% | 0,95 |
| batch B, par défaut | 0,035 | 0,13 | n/a | 0,88 | 0,81 | 0,19% | 0,20% | 0,96 |
| batch B, loi qualité | 0,0044 | 0,13 | n/a | 0,88 | 0,81 | 0,07% | 0,06% | n/a |

Nous proposons deux équations pour choisir le batch : la loi par défaut et la loi qualité. La « loi qualité » sacrifie du débit (throughput) au profit d'une meilleure qualité de clustering par rapport à la loi « par défaut ». Ci-dessous, nous traçons les données d'entraînement de nos lois d'échelle : la MSE de validation en fonction du pas α₀ (à gauche) et de la taille de batch B (à droite).

Le principal problème du k-means par mini-batchs est sa propension aux clusters « morts » (dead clusters), des centroïdes qui se retrouvent avec zéro point assigné au cours de l'optimisation. Cela réduit la taille effective du codebook, ce qui est particulièrement problématique pour les codebooks de grande taille de plus en plus utilisés aujourd'hui.

Une mitigation courante consiste à réinitialiser les clusters tombant sous un certain seuil de taille, comme le fait EnCodec[10], où les centroïdes morts sont simplement remplacés par des échantillons aléatoires tirés du batch entrant. Si cela aide, cela ne résout pas complètement le problème. Plutôt que d'échantillonner des points arbitraires du batch, nous réanimons les clusters morts en scindant des clusters existants de grande taille : nous échantillonnons un cluster actif avec une probabilité proportionnelle à sa taille, puis le scindons en deux. Nous avons constaté que cette approche, adaptée du k-means de Faiss, est significativement plus efficace pour éliminer les clusters morts et préserver la capacité du codebook.

| jeu de données | politique de réanimation | clusters morts | du codebook | déséquilibre | MSE test |
|---|---|---|---|---|---|
| DEEP | **scission proportionnelle** | **47** | **0,3%** | **1,194** | **0,38762** |
| | rééchantillonnage depuis le batch (EnCodec) | 2 343 | 14,3% | 1,423 | 0,39124 |
| | désactivé | 4 313 | 26,3% | 1,647 | 0,39448 |
| SIFT | **scission proportionnelle** | **10** | **0,1%** | **1,186** | **0,19623** |
| | rééchantillonnage depuis le batch (EnCodec) | 750 | 4,6% | 1,233 | 0,19684 |
| | désactivé | 2 080 | 12,7% | 1,404 | 0,19797 |

Nous avons validé e-means sur 24 jeux de données et configurations différents (embeddings et données synthétiques) (voir le papier). Pour la vidéo, nous avons exécuté 234 configurations d'e-means contre k-means (16 jeux de données, de 100k à 100M de points) : explorez chaque courbe dans la carte des résultats.

Dépôt : faiss/contrib/e_means.

Si vous utilisez e-means, merci de citer le papier (arXiv:2611.09501) :

## Pourquoi ça compte
Pour toute équipe exploitant du clustering à grande échelle (index de recherche vectorielle, codebooks VQ-VAE, compression d'embeddings), e-means offre un remplacement direct et sans réglage de l'algorithme de Lloyd, à la fois plus rapide et plus précis — d'autant plus notable qu'il est déjà intégré dans Faiss, une bibliothèque largement utilisée en production.
