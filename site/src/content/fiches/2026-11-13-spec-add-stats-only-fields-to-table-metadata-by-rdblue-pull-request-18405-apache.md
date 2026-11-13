---
title: "Spec: Add stats-only fields to table metadata by rdblue · Pull Request #18405 · apache/iceberg"
date: 2026-11-13
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fgithub.com%2Fapache%2Ficeberg%2Fpull%2F18405%3Futm_source=tldrdata/1/010001a1cf75fe31-ac9c430c-f0af-42e8-b127-f520ccf5a92f-000000/5N3nGmDBPfqeptMVzDylSfwYPWtzWyPATZjUOPx0CJk=452"
authors: ["rdblue", "pvary"]
keywords: ["Apache Iceberg", "métadonnées de table", "stats-only fields", "collation", "partitionnement", "schéma"]
theme: "Data"
tone: "research"
used_in: ["2026-11-13"]
---

## Résumé
Cette source est une discussion de pull request sur le dépôt Apache Iceberg (PR #18405) proposant d'ajouter des « champs stats-only » aux métadonnées de table. L'idée est de permettre le suivi de statistiques (bornes min/max) pour des valeurs dérivées non matérialisées, comme `to_lower_case(name)` ou des valeurs de partitionnement par bucket, sans avoir à créer une véritable colonne dans le schéma. La discussion porte notamment sur la distinction entre ce mécanisme et les colonnes générées/virtuelles, ainsi que sur la gestion spécifique des bornes liées à la collation (ordre de tri linguistique) des chaînes de caractères. La proposition a été initialement présentée sur la liste de diffusion des développeurs d'Iceberg.

## Points clés
- Ajout de « stats-only fields » aux métadonnées de table Apache Iceberg pour suivre des statistiques sur des valeurs dérivées non matérialisées.
- Deux cas d'usage visés : les champs de partition issus du bucket partitioning, et les expressions de valeur (ex. `to_lower_case(str)`).
- Débat sur la différence avec les colonnes générées/virtuelles : ces dernières nécessitent un field ID dans le schéma, ce que la proposition veut éviter.
- Introduction d'un champ `collation-value` par version de collation (avec `source-id`, `collation`, `version`) pour gérer les bornes sensibles à la collation.
- Ajout de nouvelles fonctions `min_code_point` et `max_code_point` dans la spec des expressions pour encadrer la plage de points de code.
- Suppression des champs de collation précédemment logés dans `content_stats` au profit de ce nouveau mécanisme stats-only.

## Analyse approfondie
### Conversation

| @rdblue : Nous avons discuté des index secondaires à l'ApacheCon, et vous avez suggéré d'utiliser des colonnes dérivées pour ce cas d'usage. J'ai vérifié le document et la colonne dérivée virtuelle pourrait aussi résoudre ce cas d'usage. Devrions-nous plutôt nous concentrer sur cette discussion ? |

| @pvary, ceci est indépendant des expressions de colonnes dérivées ou générées. Cela couvre des valeurs qui ne sont représentées que dans les stats, comme des bornes inférieures/supérieures alternatives (`to_lower_case(str)`) ou des valeurs de partition par bucket. Les colonnes générées ressembleraient davantage à des expressions de valeur par défaut, où l'expression est directement intégrée au schéma. J'ai envisagé de généraliser cela, mais les colonnes générées doivent figurer dans le schéma, ce qui signifie qu'elles ont déjà des field IDs. Mélanger ce travail avec elles ne ferait que complexifier cette fonctionnalité. |

| Ça me semble logique, j'aime bien « stats-only », c'est plus clair que c'est pour des stats basées sur des expressions. La colonne virtuelle proposée (expression de colonne générée non stockée) pourrait être une approximation de pauvre pour ce besoin, mais l'inconvénient est qu'elle occupe une colonne réelle. C'est probablement plus propre si le cas d'usage visé est bien des stats basées sur des expressions. |

| Pourquoi ne pas les mettre dans le schéma comme colonne optionnelle ? Cela supprimerait toutes les préoccupations liées à la génération d'ID et au maintien des stats. |

### Message de commit associé

Déplace les bornes sensibles à la collation hors de `content_stats` vers des champs stats-only (apache#18405), et clarifie la prose sur les collations.
- Les bornes de collation forment un champ stats-only `collation-value` par version de collation, avec `source-id`, `collation` et `version`. Les bornes sont des valeurs originales ordonnées selon la collation ; elles doivent être valides mais ne sont pas nécessairement strictes (tight).
- La plage de points de code (code-point range) est constituée de deux champs stats-only `expr-value` par champ collationné, utilisant les nouvelles fonctions `min_code_point` et `max_code_point` de la spec des expressions.
- Un lecteur peut utiliser les bornes d'une autre version de collation lorsque les deux versions ordonnent la plage de points de code du fichier de la même manière.
- Suppression des champs de collation de `content_stats` (offsets 8, 9, et 18-22) et de l'exemple de stats de collation.
Dépend de apache#18405.

### Description de la PR

Ceci ajoute des « champs stats-only » aux métadonnées de table. Un champ stats-only sert à suivre les statistiques d'une valeur dérivée non matérialisée. Par exemple, on pourrait en utiliser un pour suivre les stats de `to_lower_case(name)`.

Cela introduit deux cas : les champs de partition pour le résultat du bucket partitioning, et les expressions de valeur pour des cas d'usage comme celui ci-dessus.

Ceci a été discuté sur la liste de diffusion des développeurs dans le fil « [DISCUSS] Field ID tracking for non-materialized columns in v4 ».

## Pourquoi ça compte
Cette PR illustre l'évolution du format de table Apache Iceberg (en vue de la v4) pour mieux exploiter des statistiques sur des expressions dérivées sans alourdir le schéma, un enjeu clé pour l'optimisation des requêtes dans les lakehouses modernes.
