---
title: "Postal codes and tessellations | One World"
date: 2026-11-11
url: "https://click.dataelixir.com/o8u44z23rdiqhn3vp5givhqqpe0q9hohmlmre/08hwh9h248445nalh5/aHR0cHM6Ly9kaWVnaGVybmFuLmdpdGh1Yi5pby8yMDI2MTFfcG9zdGFsLWNvZGVzLz91dG1fY2FtcGFpZ249RGF0YV9FbGl4aXImdXRtX3NvdXJjZT1EYXRhX0VsaXhpcl81OTc="
authors: ["Diego Hernangómez"]
keywords: ["Voronoi", "codes postaux", "R", "géomatique", "sf", "cartographie"]
theme: "Tech"
tone: "tutorial"
used_in: ["2026-11-11"]
---

## Résumé

L'article explique comment transformer des points d'adresses (ou des points postaux représentatifs) en zones estimées de codes postaux à l'aide de diagrammes/tessellations de Voronoi, en s'appuyant sur le package R **sf**. L'auteur reprend d'abord la méthode développée pour son projet "Postal codes of Spain" (inspiré des travaux de Goerlich 2022 et Sánchez 2020), puis l'applique pas à pas à la Slovénie avec les données postales de **GISCO** (2024). La démonstration couvre la construction des cellules, leur découpage par limites communales, la récupération des codes postaux par relation spatiale, la gestion des composantes sans point assigné, et des contrôles de validité géométrique. L'auteur insiste sur le fait que ces polygones restent une approximation par proximité géométrique, sans lien garanti avec les véritables zones de distribution postale.

## Points clés

- Un diagramme de Voronoi découpe un plan en cellules autour de "sites" (points générateurs), chaque cellule regroupant les emplacements les plus proches de ce site que de tout autre — la méthode est reprise ici pour approximer des zones de codes postaux.
- La démonstration passe d'un exemple jouet à 5 points (R, packages sf + ggplot2) à un cas réel complet : les points postaux GISCO 2024 de Slovénie, projetés en ETRS89/LAEA Europe (EPSG:3035) pour travailler en mètres.
- Le nettoyage des données est crucial : points dupliqués aux mêmes coordonnées (79 retirés), codes en conflit sur une même localisation (16 cas) — autant de limites à garder en tête avant de construire les cellules.
- La construction procède commune par commune (et composante par composante pour les communes multi-parties), avec une marge intérieure ("inward margin", 200 m puis 50 m en repli) pour réduire l'effet des points proches d'une frontière, avant intersection avec les limites communales.
- Les composantes sans point assigné peuvent parfois être récupérées par imputation si la commune correspondante n'a qu'un seul code postal distinct ailleurs — une inférence, pas une certitude.
- Des vérifications géométriques finales (différence de couverture, chevauchements) valident la cohérence technique des polygones, mais ne garantissent en rien leur exactitude postale réelle.

## Analyse approfondie

L'auteur a publié un projet sur les codes postaux d'Espagne, avec des zones postales estimées, une carte interactive et des téléchargements GeoPackage. Restait une question non traitée : comment des points d'adresses deviennent-ils des polygones ? La réponse tient en un concept : les **polygones de Voronoi**.

### Qu'est-ce qu'un polygone de Voronoi ?

Imaginons quelques commerces sur une carte plane : quel est le plus proche de chez soi ? En posant cette question pour chaque emplacement et en attribuant une couleur par commerce, on obtient un **diagramme de Voronoi** — aussi appelé **tessellation de Voronoi**, **décomposition de Voronoi**, **partition de Voronoi** ou **tessellation de Dirichlet**. Cette technique découpe un plan en régions selon la distance à un ensemble de points donnés.

Dans cet exemple, chaque commerce est un **site**, ou point générateur. Sa **cellule de Voronoi**, aussi appelée **polygone de Thiessen**, regroupe les emplacements au moins aussi proches de ce site que de tout autre. Le long d'une frontière partagée, deux sites sont à égale distance ; là où plusieurs cellules se rencontrent, l'égalité peut concerner plus de deux sites. Avec une distance euclidienne classique, les frontières suivent les médiatrices entre sites. Certaines cellules s'étendent à l'infini, d'où le besoin de les découper (clip) selon une zone d'étude.

Le nom honore Georgy Voronoi, qui a étudié ces partitions au début du XXe siècle, mais l'idée a des racines plus anciennes, notamment les travaux de Dirichlet au XIXe siècle (d'où le nom alternatif). Pokojski et Pokojska (2018) en retracent l'histoire et les applications géographiques.

Ces partitions servent par exemple à étudier la proximité aux commerces ou services publics, à répartir des zones entre stations météo, ou à analyser des structures spatiales — les polygones de Thiessen peuvent ainsi fournir des poids de surface pour estimer la pluviométrie à partir de pluviomètres. La question sous-jacente reste toujours celle de la distance choisie : l'hôpital le plus proche à vol d'oiseau n'est pas forcément le plus rapide à atteindre.

#### Un petit exemple en R

L'auteur part de cinq points dans un carré imaginaire, dont un au centre, avec seulement les packages **sf** et **ggplot2**. Les coordonnées sont arbitraires, sans système de référence géographique.

```r
library(sf)
library(ggplot2)
# Define a common theme for the maps.
background <- "#faf8f2"
ink <- "#203b47"
theme_set(
  theme_void() +
    theme(
      plot.background = element_rect(fill = background, colour = NA),
      panel.background = element_rect(fill = background, colour = NA),
      plot.title = element_text(face = "bold", colour = ink),
      plot.subtitle = element_text(colour = ink),
      plot.caption = element_text(colour = "grey40", hjust = 0),
      legend.position = "bottom",
      plot.margin = margin(10, 10, 10, 10)
    )
)
sites <- data.frame(
  site = c("A", "B", "C", "D", "E"),
  x = c(2, 7, 3, 8, 5),
  y = c(2, 3, 8, 7, 5)
)
toy_points <- st_as_sf(sites, coords = c("x", "y"))
study_area <- st_as_sfc(st_bbox(c(xmin = 0, ymin = 0, xmax = 10, ymax = 10)))
toy_cells <- toy_points |>
  st_union() |>
  st_voronoi(envelope = study_area) |>
  st_collection_extract("POLYGON") |>
  st_intersection(study_area)
ggplot() +
  geom_sf(
    data = toy_cells,
    fill = c("#a8dadc", "#f4c89a", "#c6b8df", "#bfd59b", "#f2b5c4"),
    colour = "white", linewidth = 1
  ) +
  geom_sf(data = toy_points, colour = "#203b47", size = 3) +
  geom_text(
    data = sites, aes(x, y, label = site),
    nudge_y = 0.5, colour = "#203b47", fontface = "bold"
  ) +
  coord_sf(datum = NA) +
  labs(
    title = "Five points, five Voronoi cells",
    subtitle = "Each location belongs to the closest site"
  )
```

Cinq points, cinq cellules. Le point E, en `(5, 5)`, obtient une cellule bornée entourée par les quatre autres. Les cellules extérieures s'étendent au-delà du carré et sont découpées à ses bords. `st_union()` regroupe les points en une seule géométrie, `st_voronoi()` construit le diagramme, et `st_intersection()` le découpe selon le carré. Les couleurs permettent simplement de distinguer les cellules — aucun code postal n'a encore été assigné.

Le diagramme ne connaît rien des routes, rivières ou limites administratives. En passant aux points postaux réels, il faudra rendre explicites les choix concernant ces frontières.

### Avant de commencer : que cherche-t-on à estimer ?

Le projet espagnol utilise les points d'adresses CartoCiudad associés à leurs codes postaux, en suivant la méthode de Goerlich (2022), elle-même développée à partir d'une idée présentée par Sánchez (2020) ; la version en ligne mise à jour détaille la méthode.

Pour la Slovénie, l'auteur utilise les points postaux de **GISCO**, récupérés via le package **giscoR**. Différence importante : un point représentatif pour un code postal donne beaucoup moins d'information que des milliers d'adresses portant ce même code. Des adresses détaillées permettent à la partition de mieux suivre leur distribution réelle, même si la seule proximité géométrique ne peut pas reproduire les décisions effectives de distribution postale.

Rien ne garantit par ailleurs que les zones postales slovènes suivent les limites communales : imposer ces limites est ici un choix de modélisation, inspiré du flux de travail espagnol, et non une propriété vérifiée du système postal slovène.

### Récupération des données

On récupère d'abord les limites communales et les points postaux, dans leur édition 2024.

```r
library(giscoR)
library(sf)
library(dplyr)
municipalities <- gisco_get_lau(
  year = 2024, country = "SI", epsg = 3035
) |>
  select(GISCO_ID, LAU_NAME) |>
  st_make_valid()
raw_points <- gisco_get_postalcodes(
  year = 2024, country = "SI", epsg = 3035
)
```

Le travail se fait dans le système **ETRS89 / LAEA Europe (EPSG:3035)**, un système de coordonnées projetées en mètres — ce qui donne un sens concret aux marges de 200 m et 50 m utilisées plus loin. Voronoi utilise des distances euclidiennes dans ce plan, pas des distances routières, et la projection elle-même ne préserve pas toutes les distances de façon exacte.

Avant de tracer quoi que ce soit, un premier état des lieux des données téléchargées :

```r
postal_points <- raw_points |>
  mutate(POSTCODE = trimws(as.character(POSTCODE))) |>
  filter(!is.na(POSTCODE), POSTCODE != "") |>
  select(POSTCODE)
code_counts <- postal_points |>
  st_drop_geometry() |>
  count(POSTCODE, name = "points_per_code")
knitr::kable(data.frame(
  Indicator = c(
    "Municipalities", "Downloaded points", "Points with a postal code",
    "Distinct postal codes", "Codes represented by one point"
  ),
  Value = c(
    nrow(municipalities), nrow(raw_points), nrow(postal_points),
    nrow(code_counts), sum(code_counts$points_per_code == 1)
  )
))
```

| Indicateur | Valeur |
|---|---|
| Communes | 212 |
| Points téléchargés | 557 |
| Points avec un code postal | 557 |
| Codes postaux distincts | 557 |
| Codes représentés par un seul point | 557 |

Ces chiffres donnent un premier aperçu du fichier, mais ne constituent pas un contrôle qualité : ils ne disent rien sur l'exhaustivité des codes ni sur la justesse des coordonnées. Avec un seul point par code, on dessinera des zones autour de représentants, et non des estimations à partir d'adresses individuelles.

Deux points aux coordonnées strictement identiques ne peuvent pas générer deux cellules de Voronoi distinctes. On trie par code postal et on garde le premier point à chaque emplacement, comme dans le flux de travail original — une règle de départage reproductible, non une preuve que le code conservé est correct. Les comptages suivants montrent combien d'enregistrements sont retirés et combien d'emplacements présentent des codes en conflit.

```r
postal_points <- postal_points |> arrange(POSTCODE)
conflicts <- postal_points |>
  group_by(geometry) |>
  summarise(codes = n_distinct(POSTCODE), .groups = "drop") |>
  filter(codes > 1)
duplicates <- duplicated(postal_points$geometry)
knitr::kable(data.frame(
  Indicator = c("Duplicate locations removed", "Locations with conflicting codes"),
  Value = c(sum(duplicates), nrow(conflicts))
))
```

| Indicateur | Valeur |
|---|---|
| Emplacements dupliqués retirés | 79 |
| Emplacements avec codes en conflit | 16 |

```r
postal_points <- postal_points[!duplicates, ]
```

### Point de départ : Ljubljana

On sélectionne Ljubljana et les points situés à l'intérieur de son territoire. `st_within()` évite qu'un point exactement sur une frontière partagée soit assigné aux deux communes voisines.

```r
city <- municipalities |> filter(LAU_NAME == "Ljubljana")
city_points <- st_filter(postal_points, city, .predicate = st_within)
base_map <- ggplot() +
  geom_sf(data = city, fill = "#e8e4d8", colour = ink, linewidth = 0.4)
gisco_attr <- gisco_attributions()
base_map +
  geom_sf(data = city_points, colour = "#bd5137", size = 2) +
  labs(
    title = "Ljubljana: the starting point",
    subtitle = "A municipal boundary and points with postal codes",
    caption = gisco_attr
  )
```

#### Construction des cellules

Chaque cellule regroupe les emplacements au moins aussi proches de son point générateur que de tout autre. Les frontières de cellules apparaissent où les distances à deux points sont égales. Pour cette première démonstration, tous les points intérieurs sont conservés, sans les marges utilisées dans le flux national.

```r
cells <- city_points |>
  st_union() |>
  st_voronoi(envelope = st_as_sfc(st_bbox(city))) |>
  st_collection_extract("POLYGON") |>
  st_sf(geometry = _)
base_map +
  geom_sf(data = cells, fill = NA, colour = "#bd5137", linewidth = 0.5) +
  geom_sf(data = city_points, colour = ink, size = 2) +
  labs(
    title = "An area of proximity for every point",
    subtitle = "Cells still extend beyond the municipal boundary",
    caption = "Own elaboration using data from Eurostat / GISCO, 2024"
  )
```

`st_union()` rassemble les points pour construire un seul diagramme. Point important : `envelope` ne fournit qu'une étendue de travail, il **ne découpe pas** les cellules selon la commune — une intersection est nécessaire pour cela.

#### Découpage et récupération des codes postaux

Il serait pratique que les cellules sortent dans le même ordre que les points d'entrée, mais ce n'est pas garanti. On récupère donc le code de chaque cellule via une relation spatiale avant le découpage ; chaque cellule doit contenir exactement un point générateur.

```r
point_matches <- st_intersects(cells, city_points)
cells$POSTCODE <- city_points$POSTCODE[unlist(point_matches)]
clipped_geometry <- st_intersection(st_geometry(cells), st_geometry(city))
city_cells <- st_sf(
  POSTCODE = cells$POSTCODE[attr(clipped_geometry, "idx")[, 1]],
  geometry = clipped_geometry
)
city_areas <- city_cells |>
  group_by(POSTCODE) |>
  summarise(.groups = "drop") |>
  st_make_valid()
city_colours <- setNames(
  hcl.colors(nrow(city_areas), palette = "Dark 3"),
  sort(city_areas$POSTCODE)
)
city_labels <- st_sf(
  POSTCODE = city_areas$POSTCODE,
  geometry = st_point_on_surface(st_geometry(city_areas))
)
ggplot(city_areas) +
  geom_sf(aes(fill = POSTCODE), colour = background, linewidth = 0.6) +
  geom_sf(
    data = city_points, shape = 21, fill = ink,
    colour = background, size = 2.4
  ) +
  geom_sf_text(
    data = city_labels,
    aes(label = POSTCODE), colour = ink, fontface = "bold", size = 3.5
  ) +
  scale_fill_manual(values = city_colours, guide = "none") +
  coord_sf(datum = NA) +
  labs(
    title = "From points to estimated areas",
    subtitle = "Cells clipped and merged by postal code",
    caption = "Teaching example · Not official postal boundaries"
  )
```

On intersecte les colonnes de géométrie, puis on utilise la matrice `idx` de l'intersection pour récupérer le code postal de chaque cellule — ce qui rend explicite l'affectation des attributs. Les positions des étiquettes sont également calculées à partir des seules géométries. Regrouper par code postal avec `summarise()` fusionne les géométries : avec de nombreuses adresses partageant un code, leurs cellules se dissolvent en une seule géométrie, potentiellement en plusieurs parties séparées.

### D'une commune à l'ensemble du pays

Ljubljana est traitée ; il reste à répéter l'opération pour chaque composante de chaque commune. Certaines communes comportent des parties séparées : normaliser en `MULTIPOLYGON` puis convertir en `POLYGON` permet de traiter ces composantes indépendamment, sans étendre automatiquement un code à une partie dépourvue de points.

L'identifiant et le nom de la commune s'appliquent à chaque composante ; ces attributs sont donc déclarés spatialement constants avant de scinder les géométries.

```r
components <- municipalities |>
  st_set_agr("constant") |>
  st_cast("MULTIPOLYGON") |>
  st_cast("POLYGON") |>
  mutate(component_id = row_number())
```

#### Pourquoi une marge intérieure ?

Dans le projet espagnol, on sélectionne d'abord les adresses à l'intérieur d'une marge de **200 m**. Si aucune n'est trouvée, on retente avec **50 m**. Cela réduit l'influence des points proches d'une frontière, où de petits décalages entre couches de données peuvent fausser leur affectation.

Il n'existe pas de règle universelle derrière ces valeurs : Goerlich décrit une marge de 20 m, tandis que les choix de 200 m et 50 m proviennent de l'implémentation de l'auteur. Ils sont repris ici pour illustrer ce flux de travail, bien que la faible densité des points postaux rende plus facile d'exclure par erreur de l'information utile. Comparer d'autres marges constituerait une prochaine étape intéressante.

```r
select_points <- function(component, postal_points) {
  for (margin in c(200, 50)) {
    interior <- st_buffer(st_geometry(component), -margin)
    if (all(st_is_empty(interior))) next
    selected_points <- st_filter(postal_points, interior,
      .predicate = st_within
    )
    if (nrow(selected_points) > 0) {
      return(selected_points)
    }
  }
  postal_points[0, ]
}
```

La marge ne sert qu'à sélectionner les points : les zones résultantes couvrent la composante **d'origine**, pas la géométrie réduite par la marge. Si les deux tentatives échouent, la composante reste non assignée — aucun point extérieur à la commune n'est emprunté pour la compléter.

#### Trois cas, une seule fonction

Trois cas doivent être gérés. Sans aucun point, la composante est conservée avec un code `NA`. Si tous les points sélectionnés partagent le même code, celui-ci est assigné à toute la composante. Voronoi n'est nécessaire que lorsque plusieurs codes sont présents : pas besoin de découper une zone qui possède déjà une affectation unique.

```r
build_areas <- function(component, postal_points) {
  selected_points <- select_points(component, postal_points)
  codes <- unique(selected_points$POSTCODE)
  if (length(codes) <= 1L) {
    component$POSTCODE <- if (length(codes)) codes else NA_character_
    return(component)
  }
  cells <- selected_points |>
    st_union() |>
    st_voronoi(envelope = st_as_sfc(st_bbox(component))) |>
    st_collection_extract("POLYGON") |>
    st_sf(geometry = _)
  point_matches <- st_intersects(cells, selected_points)
  cells$POSTCODE <- selected_points$POSTCODE[unlist(point_matches)]
  clipped_geometry <- st_intersection(
    st_geometry(cells),
    st_geometry(component)
  )
  result <- st_sf(
    POSTCODE = cells$POSTCODE[attr(clipped_geometry, "idx")[, 1]],
    geometry = clipped_geometry
  ) |>
    group_by(POSTCODE) |>
    summarise(.groups = "drop") |>
    st_make_valid()
  result$GISCO_ID <- component$GISCO_ID
  result$LAU_NAME <- component$LAU_NAME
  result$component_id <- component$component_id
  result
}
result <- lapply(seq_len(nrow(components)), function(i) {
  build_areas(components[i, ], postal_points)
}) |>
  bind_rows()
```

#### Traitement des zones non assignées

Peut-on combler certains vides ? Une composante sans point peut appartenir à une commune dont les autres composantes disposent d'information. Son code n'est récupéré que si la commune présente **un seul code recouvré distinct** — une imputation à partir des données disponibles, non une preuve que la commune n'a réellement qu'un seul code.

```r
unique_codes <- result |>
  st_drop_geometry() |>
  filter(!is.na(POSTCODE)) |>
  distinct(GISCO_ID, POSTCODE) |>
  add_count(GISCO_ID) |>
  filter(n == 1)
unassigned_before <- sum(is.na(result$POSTCODE))
index <- match(result$GISCO_ID, unique_codes$GISCO_ID)
recoverable <- is.na(result$POSTCODE) & !is.na(index)
result$POSTCODE[recoverable] <- unique_codes$POSTCODE[index[recoverable]]
```

Avant de dresser la carte finale, les géométries sont nettoyées pour ne garder que des surfaces : les réparations peuvent produire des collections contenant des lignes ou points résiduels, qui n'ont pas leur place dans une couche de zones. Dissoudre par code postal supprime aussi les limites communales entre zones partageant ce code.

```r
keep_surfaces <- function(x) {
  geometry <- st_make_valid(st_geometry(x))
  geometry <- lapply(geometry, function(part) {
    if (!inherits(part, c("POLYGON", "MULTIPOLYGON", "GEOMETRYCOLLECTION"))) {
      return(st_multipolygon())
    }
    surfaces <- suppressWarnings(st_collection_extract(st_sfc(part), "POLYGON"))
    if (length(surfaces) == 0L || all(st_is_empty(surfaces))) {
      return(st_multipolygon())
    }
    st_cast(st_union(surfaces), "MULTIPOLYGON", warn = FALSE)[[1]]
  })
  st_geometry(x) <- st_sfc(geometry, crs = st_crs(x))
  x[!st_is_empty(x), ]
}
unassigned <- result |>
  filter(is.na(POSTCODE)) |>
  keep_surfaces()
postal_areas <- result |>
  filter(!is.na(POSTCODE)) |>
  group_by(POSTCODE) |>
  summarise(.groups = "drop") |>
  keep_surfaces() |>
  st_cast("MULTIPOLYGON")
```

### La carte complète

Pour la vue nationale, les zones sont colorées selon le premier chiffre du code postal — ce qui garde la carte lisible sans prétendre valider une classification des régions postales. Le gris est réservé aux composantes non assignées, avec sa propre entrée de légende.

```r
postal_colours <- c(
  "1" = "#007F7F", "2" = "#E87500", "3" = "#3B6FB6", "4" = "#A64E9A",
  "5" = "#649A32", "6" = "#D9AF00", "8" = "#B94350", "9" = "#6255A4",
  "Unassigned" = "#727A80"
)
postal_groups <- sort(unique(substr(postal_areas$POSTCODE, 1, 1)))
ggplot() +
  geom_sf(data = municipalities, fill = "#d5d2ca", colour = NA) +
  geom_sf(
    data = postal_areas,
    aes(fill = substr(POSTCODE, 1, 1)), colour = background, linewidth = 0.15
  ) +
  geom_sf(
    data = unassigned, aes(fill = "Unassigned"),
    colour = background, linewidth = 0.15
  ) +
  scale_fill_manual(
    values = postal_colours, name = "Postal code group",
    breaks = c(postal_groups, "Unassigned"),
    labels = c(paste0(postal_groups, "xxx"), "Unassigned")
  ) +
  coord_sf(datum = NA) +
  labs(
    title = "Slovenia, point by point",
    subtitle = "Proximity areas clipped to municipal boundaries",
    caption = paste("Eurostat / GISCO, 2024 · Own elaboration",
      "Dark grey: unassigned areas · Estimated boundaries, not official",
      sep = "\n"
    )
  )
```

### Vérification du résultat

La carte est prête, mais il reste à vérifier la géométrie avant d'aller plus loin : les polygones sont-ils valides ? Les zones assignées et non assignées couvrent-elles bien le territoire ? Y a-t-il des recouvrements notables ? On tolère un mètre carré de différence pour les imprécisions numériques des opérations géométriques.

```r
territory <- st_union(st_geometry(municipalities))
coverage <- st_union(c(st_geometry(postal_areas), st_geometry(unassigned)))
difference_m2 <- as.numeric(sum(st_area(st_sym_difference(territory, coverage))))
overlap_m2 <- as.numeric(
  sum(st_area(postal_areas)) + sum(st_area(unassigned)) - sum(st_area(coverage))
)
knitr::kable(data.frame(
  Indicator = c(
    "Codes with an estimated area", "Components assigned by municipal recovery",
    "Unassigned records", "Unassigned area (km²)",
    "Coverage difference (m²)", "Overlap (m²)"
  ),
  Value = round(c(
    nrow(postal_areas), sum(recoverable), nrow(unassigned),
    as.numeric(sum(st_area(unassigned))) / 1e6, difference_m2,
    overlap_m2
  ), 4)
))
```

| Indicateur | Valeur |
|---|---|
| Codes avec une zone estimée | 468,0000 |
| Composantes assignées par recouvrement communal | 4,0000 |
| Enregistrements non assignés | 6,0000 |
| Zone non assignée (km²) | 150,2033 |
| Différence de couverture (m²) | 0,0000 |
| Recouvrement (m²) | -0,0002 |

Ces contrôles vérifient la géométrie, **pas l'exactitude postale**. On pourrait couvrir un pays entier avec des polygones parfaitement valides tout en obtenant une approximation médiocre de ses zones de livraison réelles.

### Retour à l'Espagne

L'auteur dispose désormais de la séquence complète : points, zones de proximité, découpage et fusion par code postal. Les mêmes étapes fonctionnent avec des adresses bien plus détaillées, comme les données CartoCiudad de son projet sur les codes postaux espagnols.

La donnée d'entrée compte autant que l'algorithme : avec un seul point représentatif par code, Voronoi cartographie surtout des distances entre représentants ; avec des points d'adresses, il peut mieux approximer où se concentrent les adresses de chaque code. Il ne sait toujours rien des itinéraires de livraison, des barrières physiques ou des limites officielles.

Ces résultats n'ont pas été comparés à une source postale indépendante pour la Slovénie. Avant toute utilisation analytique, il faudrait examiner la couverture, les coordonnées, la relation avec les communes et la sensibilité aux marges choisies. Pour l'instant, il s'agit d'un exemple de travail qui montre, étape par étape, comment ces polygones sont construits.

Le titre de l'article fait un clin d'œil à l'album de Muse *Black Holes and Revelations*.

### Références

- Goerlich, F. J. (2022). *Elaboración de un mapa de códigos postales de España con recursos libres: Cómo evitar pagar por disponer de información de referencia* (Working Paper n° 2022-3). Ivie. https://doi.org/10.12842/WPIVIE_0322 (version en ligne mise à jour)
- Hernangómez, D. (2026). *Códigos postales de España* (Version 1.0.0) [Jeu de données]. Zenodo. https://doi.org/10.5281/zenodo.23698418 (documentation du projet)
- Pokojski, W., & Pokojska, P. (2018). Voronoi diagrams – Inventor, method, applications. *Polish Cartographical Review, 50*(3), 141–150. https://doi.org/10.2478/pcr-2018-0009
- Sánchez, J. I. (2020, 13 novembre). Así hice el mapa de los códigos postales de España con SIG y datos abiertos. *Nosolosig*.

## Pourquoi ça compte

Cet article illustre de façon pédagogique et reproductible une technique géospatiale (Voronoi/sf en R) pour approximer des zones administratives à partir de points, tout en modélisant honnêtement ses limites — un cas d'école utile pour quiconque traite des données géospatiales ouvertes ou construit des pipelines data reproductibles.
