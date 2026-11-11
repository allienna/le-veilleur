---
title: "Nuclei, five years later: what a mean Dice hides – Data Science Guts"
date: 2026-11-11
url: "https://click.dataelixir.com/o8u44z23rdiqhn3vp5givhqqpe0q9hohmlmre/n2hohvhv4d44pvf6hg/aHR0cHM6Ly9kYXRhc2NpZW5jZWd1dHMuY29tL3Bvc3RzLzIwMjYtMTEtMDYtbnVjbGVpLW1lYW4tZGljZS8_dXRtX2NhbXBhaWduPURhdGFfRWxpeGlyJnV0bV9zb3VyY2U9RGF0YV9FbGl4aXJfNTk3"
keywords: ["segmentation d'images", "U-Net", "score Dice", "évaluation de modèle", "deep learning", "imagerie médicale"]
theme: "Data"
tone: "tutorial"
used_in: ["2026-11-11"]
---

## Résumé

L'auteur reprend un U-Net entraîné en 2020 sur les images de noyaux du Data Science Bowl (package `rplatypus`) et l'évalue cette fois correctement, sur le découpage de validation exact sur lequel les poids publiés ont été mesurés. Le Dice moyen de 0,92 se révèle être essentiellement la moyenne des 105 images de fluorescence, tandis que les trois images en champ clair (brightfield) obtiennent les pires scores (0,72 à 0,77), sans qu'on puisse trancher si la cause est le type de microscopie ou la taille minuscule des noyaux une fois l'image redimensionnée en 256x256. Le billet plaide pour toujours accompagner une métrique agrégée d'une analyse par image et du pire cas, plutôt que de se fier à un chiffre unique.

## Points clés

- Le modèle publié `dsbowl-unet` est réévalué sur les 134 images de validation exactes de son découpage d'origine (seed 1), afin d'éviter toute fuite de données vers l'entraînement.
- Le Dice moyen de 0,9205 (pire cas à 0,7240) correspond bien aux chiffres de la fiche du modèle, confirmant que c'est le bon découpage.
- `evaluate_cases()` produit une ligne par image plutôt qu'un score global, révélant une forte hétérogénéité : fluorescence (0,935 en moyenne sur 105 images), tissus colorés (0,883 sur 26), champ clair (0,749 sur seulement 3 images).
- Les trois images en champ clair sont à la fois les seules de ce type dans le découpage et celles où les noyaux sont les plus petits une fois ramenés à la grille 256x256 du modèle - deux explications concurrentes impossibles à départager avec seulement trois exemples.
- Réévaluer à la résolution native des fichiers ne règle rien, car le détail est déjà perdu au moment de la prédiction (faite en 256x256) ; seule une approche par tiling plutôt que par redimensionnement permettrait de distinguer les deux hypothèses.
- Conclusion méthodologique : un score de segmentation agrégé doit toujours être accompagné du pire cas et d'une ventilation par sous-groupe d'images.

## Analyse approfondie

`data_dir <- "stage1_train"   # BBBC038v1, unzipped`
En 2020, j'ai entraîné un U-Net sur les noyaux du Data Science Bowl 2018 avec la première version de ce package, j'ai regardé un score Dice grimper pendant l'entraînement, et j'ai terminé ce billet avec quatre masques prédits sur les images de test de la compétition. Ces images n'ont pas de masques. Les images avaient l'air bonnes, et je n'avais aucun moyen de savoir où le modèle se trompait - alors je ne me suis jamais posé la question.

Ce billet se la pose. Rien n'y est entraîné : le modèle est le `dsbowl-unet` publié dans le premier billet de la série, évalué sur les images dont il a été exclu. Les évaluer toutes a pris environ douze secondes sur un processeur.

### Les images dont il a été exclu

Les données sont BBBC038v1 du Broad Institute - les images du Data Science Bowl sous licence CC0. Son dossier `stage1_train` contient 670 images annotées, un dossier par image, avec un fichier de masque par noyau.

`data_dir = "stage1_train"   # BBBC038v1, unzipped`
Les poids ont été mesurés sur un découpage 80/20 des 670 images avec seed 1, ce qui permet de refaire ce découpage. `split_dataset()` ne copie rien ; elle écrit des CSV listant les fichiers :

```
library(rplatypus)
split <- split_dataset(data_dir, tempfile("splits"),
                       fractions = c(0.8, 0.2), seed = 1)
split
#> platypus split
#>   train        536 samples
#>   validation   134 samples
#>   every sample its own group
#>   seed 1 - the same inputs give this split again
```
```
import tempfile
import pyplatypus as pp
split = pp.split_dataset(data_dir, tempfile.mkdtemp(),
                         fractions=(0.8, 0.2), seed=1)
split["samples"]
#> {'train': 536, 'validation': 134, 'test': 0}
```
Refaire le découpage importe plus qu'il n'y paraît. Ma propre copie de ce jeu de données contient un dossier nommé `stage1_validation` avec exactement 134 images - le même nombre - et 101 d'entre elles font partie de la portion d'entraînement du découpage sur lequel les poids ont été mesurés. Évalué sur ce dossier, le modèle serait en partie noté sur des images dont il a appris, et le simple décompte ne le révélerait jamais.

### Un seul chiffre

```
spec <- platypus_spec(
  data = segmentation_data(split, colormap = binary_colormap),
  models = list(
    u_net("nuclei", input_shape = c(256, 256), blocks = 4, filters = 16,
          weights = "dsbowl-unet", fit = FALSE,
          metrics = list(metric_dice(include_background = FALSE)))
  )
)
fit <- platypus_fit(spec, verbose = FALSE)
cases <- evaluate_cases(fit)
summary(cases)
#>   metric   n      mean         sd    median       min       max
#> 1   dice 134 0.9205236 0.05322748 0.9313503 0.7239583 0.9860661
#>                                                         worst_case
#> 1 7f38885521586fc6011bef1314a9fb2aa1e4935bd581b2991e1d963395eab770
```
```
engine = pp.build_engine(pp.from_dict({
    "task": "semantic_segmentation",
    "data": {
        "train_path": str(split["paths"]["train"]),
        "validation_path": str(split["paths"]["validation"]),
        "colormap": [[0, 0, 0], [255, 255, 255]],
        "mode": "config_file",
    },
    "models": [{
        "name": "nuclei",
        "architecture": "u_net",
        "input_shape": [256, 256],
        "blocks": 4,
        "filters": 16,
        "weights": "dsbowl-unet",
        "fit": False,
        "metrics": [{"name": "dice", "include_background": False}],
    }],
}))
engine.fit()
cases = engine.evaluate_cases("nuclei")
pp.summarise_cases(cases)
#> [{'metric': 'dice', 'n': 134, 'mean': 0.9205236150257623,
#>   'sd': 0.05322747958922138, 'median': 0.9313502907752991,
#>   'min': 0.7239583134651184, 'max': 0.9860661029815674,
#>   'worst_case':
#>     '7f38885521586fc6011bef1314a9fb2aa1e4935bd581b2991e1d963395eab770'}]
```
Un Dice moyen de 0,9205 et une pire image à 0,7240 - les chiffres de la fiche du modèle au quatrième chiffre près, ce qui confirme qu'il s'agit bien du découpage de cette fiche. `include_background = FALSE` exclut l'arrière-plan de la moyenne ; en l'incluant, un modèle qui ne trouverait aucun noyau obtiendrait quand même un score d'environ 0,5.

0,92 est un bon chiffre, et il est vrai. La question est de savoir de quoi il est la moyenne.

### Une ligne par image

`evaluate()` renvoie une ligne par modèle. `evaluate_cases()` renvoie une ligne par image, et c'est ce tableau qui vaut la peine d'être lu :

```
head(cases[order(cases$dice), ], 5)
#> platypus scores by case (5 rows)
#>                                                              case      dice
#>  7f38885521586fc6011bef1314a9fb2aa1e4935bd581b2991e1d963395eab770 0.7239583
#>  29ea4f6eb4545f43868a9b40a60000426bf8dfd9d062546656a37bd2a2aaf9ec 0.7531800
#>  8f94a80b95a881d0efdec36affc915dca9609f4cba8134c4a91b219d418778aa 0.7541562
#>  a6515d73077866808ad4cb837ecdac33612527b8a1041e82135e40fce2bb9380 0.7588775
#>  2a1a294e21d76efd0399e4eb321b45f44f7510911acd92c988480195c5b4c812 0.7702851
```
```
worst = sorted(cases, key=lambda row: row["dice"])[:5]
[(row["case"][:16], round(row["dice"], 4)) for row in worst]
#> [('7f38885521586fc6', 0.724), ('29ea4f6eb4545f43', 0.7532),
#>  ('8f94a80b95a881d0', 0.7542), ('a6515d7307786680', 0.7589),
#>  ('2a1a294e21d76efd', 0.7703)]
```
Ces identifiants ne disent rien, alors donnons un libellé à chaque image. Le Data Science Bowl mélangeait trois types de microscopie, et deux indicateurs suffisent à les distinguer : si l'image est en couleur, et si son arrière-plan est clair ou sombre.

```
image_kind <- function(case) {
  path <- list.files(file.path(data_dir, case, "images"), full.names = TRUE)
  pixels <- png::readPNG(path[1])[, , 1:3]
  colour <- mean(abs(pixels[, , 1] - pixels[, , 2])) +
    mean(abs(pixels[, , 2] - pixels[, , 3]))
  if (colour > 0.02) return("stained")
  if (mean(pixels) > 0.5) "brightfield" else "fluorescence"
}
cases$kind <- vapply(cases$case, image_kind, character(1))
aggregate(dice ~ kind, cases, function(x) {
  round(c(n = length(x), mean = mean(x), min = min(x)), 3)
})
#>           kind  dice.n dice.mean dice.min
#> 1  brightfield   3.000     0.749    0.724
#> 2 fluorescence 105.000     0.935    0.753
#> 3      stained  26.000     0.883    0.805
```
```
from pathlib import Path
import numpy as np
from PIL import Image
def image_kind(case):
    path = next((Path(data_dir) / case / "images").glob("*.png"))
    pixels = np.asarray(Image.open(path).convert("RGB")) / 255
    colour = (np.abs(pixels[..., 0] - pixels[..., 1]).mean()
              + np.abs(pixels[..., 1] - pixels[..., 2]).mean())
    if colour > 0.02:
        return "stained"
    return "brightfield" if pixels.mean() > 0.5 else "fluorescence"
for row in cases:
    row["kind"] = image_kind(row["case"])
kinds = sorted({row["kind"] for row in cases})
dice = {k: [r["dice"] for r in cases if r["kind"] == k] for k in kinds}
{k: (len(d), round(float(np.mean(d)), 3), round(min(d), 3))
 for k, d in dice.items()}
#> {'brightfield': (3, 0.749, 0.724), 'fluorescence': (105, 0.935, 0.753),
#>  'stained': (26, 0.883, 0.805)}
```
```
library(ggplot2)
ggplot(cases, aes(dice, kind)) +
  geom_vline(xintercept = mean(cases$dice), linetype = "dashed",
             colour = "grey50") +
  geom_jitter(height = 0.15, width = 0, alpha = 0.7, size = 2) +
  labs(x = "Dice, per image", y = NULL) +
  theme_minimal(base_size = 13)
```
```
import matplotlib.pyplot as plt
rng = np.random.default_rng(1)
fig, ax = plt.subplots(figsize=(7, 3.2))
ax.axvline(np.mean([r["dice"] for r in cases]), linestyle="--", color="grey")
for i, k in enumerate(kinds):
    jitter = rng.uniform(-0.15, 0.15, len(dice[k]))
    ax.scatter(dice[k], i + jitter, alpha=0.7)
ax.set_yticks(range(len(kinds)), kinds)
ax.set_xlabel("Dice, per image")
```
Il y a trois images en champ clair (brightfield) parmi les 134, et elles obtiennent 0,72, 0,75 et 0,77 - trois des cinq pires scores. La fluorescence obtient en moyenne 0,93 sur 105 images, et c'est elle qui détermine l'essentiel de la moyenne. Les tissus colorés (stained) se situent entre les deux, à 0,88.

```
predictions <- predict(fit, split = "validation")
files_of <- function(case, what) {
  list.files(file.path(data_dir, case, what), full.names = TRUE)
}
truth_of <- function(case) {
  masks <- lapply(files_of(case, "masks"), function(f) {
    read_masks(f, binary_colormap, size = c(256, 256))[1, , ]
  })
  unite_masks(masks)
}
middle <- which.min(abs(cases$dice - median(cases$dice)))
shown <- c(which(cases$kind == "brightfield"), middle)
images <- read_images(
  vapply(cases$case[shown], function(k) files_of(k, "images")[1], ""),
  size = c(256, 256)
)
truth <- simplify2array(lapply(cases$case[shown], truth_of))
plot_masks(
  images,
  prediction = predictions[shown, , ],
  truth      = aperm(truth, c(3, 1, 2)),
  colormap   = binary_colormap,
  labels     = sprintf("%s, Dice %.2f", cases$kind[shown], cases$dice[shown])
)
```
```
predictions = engine.predict("nuclei", "validation")
data = engine.dataset(engine.runs["nuclei"].spec, "validation")
middle = np.median([r["dice"] for r in cases])
shown = [i for i, r in enumerate(cases) if r["kind"] == "brightfield"]
shown.append(min(range(len(cases)),
                 key=lambda i: abs(cases[i]["dice"] - middle)))
pp.plot_masks(
    np.stack([data[i][0] for i in shown]),
    prediction=predictions[shown],
    truth=np.stack([data[i][1] for i in shown]),
    labels=[f"{cases[i]['kind']}, Dice {cases[i]['dice']:.2f}"
            for i in shown],
)
```
### Le type de microscope, ou la taille d'un noyau ?

Les images suggèrent une seconde lecture. Les images en champ clair font 1024 par 1024 pixels, et le modèle voit chaque image en 256 par 256 - un noyau de seize pixels de large arrive donc sous la forme de quatre pixels. Mesurons le noyau moyen sur la grille du modèle :

```
nucleus_area <- function(case) {
  files <- list.files(file.path(data_dir, case, "masks"), full.names = TRUE)
  areas <- vapply(files, function(f) {
    sum(read_masks(f, binary_colormap) == 2)
  }, numeric(1))
  size <- dim(read_masks(files[1], binary_colormap))[2:3]
  mean(areas) * 256^2 / prod(size)
}
cases$area <- vapply(cases$case, nucleus_area, numeric(1))
aggregate(area ~ kind, cases, function(x) round(range(x)))
#>           kind area.1 area.2
#> 1  brightfield     11     17
#> 2 fluorescence     69    957
#> 3      stained    137   1893
```
```
def nucleus_area(case):
    files = sorted((Path(data_dir) / case / "masks").glob("*.png"))
    masks = [np.asarray(Image.open(f)) > 0 for f in files]
    height, width = masks[0].shape[:2]
    return np.mean([m.sum() for m in masks]) * 256**2 / (height * width)
for row in cases:
    row["area"] = nucleus_area(row["case"])
areas = {k: [r["area"] for r in cases if r["kind"] == k] for k in kinds}
{k: (round(min(a)), round(max(a))) for k, a in areas.items()}
#> {'brightfield': (11, 17), 'fluorescence': (69, 957),
#>  'stained': (137, 1893)}
```
Sur toutes les autres images, un noyau moyen couvre au moins 69 pixels de la grille. Sur les trois images en champ clair, il en couvre onze à dix-sept. Ces trois images sont donc à la fois les seules en champ clair du découpage et les seules où les noyaux sont aussi petits, et **trois images ne suffisent pas à distinguer ces deux explications**. L'entraînement n'aide pas non plus : parmi les 536 images d'entraînement, 13 sont en champ clair, toutes également en 1024 par 1024.

Évaluer à la résolution propre des fichiers ne permet pas non plus de les distinguer, car le détail avait déjà été perdu avant que le score ne soit calculé - la prédiction a été faite en 256 :

```
summary(evaluate_cases(fit, at = "source"))
#>   metric   n     mean         sd    median       min       max
#> 1   dice 134 0.920808 0.05371718 0.9313503 0.7164674 0.9860661
#>                                                         worst_case
#> 1 7f38885521586fc6011bef1314a9fb2aa1e4935bd581b2991e1d963395eab770
```
```
pp.summarise_cases(engine.evaluate_cases("nuclei", at="source"))
#> [{'metric': 'dice', 'n': 134, 'mean': 0.920808045276955,
#>   'sd': 0.053717183966230486, 'median': 0.9313502907752991,
#>   'min': 0.7164673805236816, 'max': 0.9860661029815674,
#>   'worst_case':
#>     '7f38885521586fc6011bef1314a9fb2aa1e4935bd581b2991e1d963395eab770'}]
```
Ce qui permettrait de les distinguer, c'est un modèle qui verrait ces images à une résolution où un noyau serait aussi grand que partout ailleurs - du tiling plutôt que du redimensionnement (resizing), ce qui fera l'objet d'un billet à part plus loin dans la série.

### Ce qu'il faut en retenir

La moyenne n'était pas fausse. 0,92 est bien ce que ce modèle obtient sur ces 134 images. Mais c'est surtout une moyenne sur 105 images de fluorescence, et les trois images sur lesquelles il se comporte le plus mal partagent deux propriétés à la fois, chacune pouvant être la cause. Rien de tout cela n'est visible dans un seul chiffre ; tout cela devient visible dans un tableau avec une ligne par image et une colonne que l'on ajoute soi-même.

Si vous rapportez un score de segmentation, indiquez le pire cas à côté de la moyenne, et regardez ce que les pires cas ont en commun. Ici, cela a demandé un seul appel de fonction et quelques lignes de R ou de Python.

### La série jusqu'à présent

1. rplatypus reconstruit : deep learning pour l'imagerie médicale en R - pourquoi le package de 2020 a dû être réécrit, comment il installe désormais son propre Python, et un premier masque obtenu avec les mêmes poids publiés que ceux utilisés ici.
2. **Nuclei, cinq ans plus tard** - ce billet.

Le prochain reste sur la segmentation mais prend du recul par rapport à un seul jeu de données : ce que rplatypus propose pour elle - quatre architectures et leurs différences, les fonctions de perte et métriques disponibles, et le fichier YAML qui décrit une expérience complète, champ par champ.

## Pourquoi ça compte

Ce billet illustre de façon concrète et reproductible un piège classique en évaluation de modèles de machine learning : une métrique agrégée séduisante peut masquer une forte hétérogénéité de performance selon des sous-groupes de données. Pour une veille tech orientée data science, c'est un rappel méthodologique utile sur l'importance de l'analyse par échantillon avant de valider ou publier un modèle de segmentation.
