---
title: "Four PostgreSQL arguments that came out even"
date: 2026-10-16
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fexplainmeasured.com%2Fposts%2Farguments-that-came-out-even%3Futm_source=tldrdata/1/010001a13f0d59fd-c7dedc25-842c-4848-902e-7af2e182448b-000000/MxiWtkyeMCDp8P6a0V4IuJ3Tk5OWkDwYs44aq2cEdow=452"
keywords: ["PostgreSQL", "benchmark", "requêtes SQL", "optimisation", "types de données", "performance"]
theme: "Data"
tone: "research"
used_in: ["2026-10-16"]
---

## Résumé
L'auteur a testé empiriquement quatre conseils récurrents de revue de code PostgreSQL (IN vs ANY vs VALUES, type de colonne pour un statut, colonnes souvent vides, count(DISTINCT) vs GROUP BY) sur PostgreSQL 18.6 avec une table de 2 millions de lignes. Contrairement à son attente de trouver au moins deux conseils clairement validés, il obtient trois égalités et un résultat qui contredit la sagesse commune. Il conclut que la plupart de ces "bonnes pratiques" doivent être vérifiées avec EXPLAIN sur ses propres données plutôt qu'appliquées par défaut.

## Points clés
- IN, ANY et une jointure VALUES pour 1 000 ids lisent exactement les mêmes pages et ont des temps d'exécution équivalents (à la variance de mesure près) ; ANY garde un texte de requête stable, ce qui aide les requêtes préparées et `pg_stat_statements`.
- Stocker un statut en text, smallint ou enum produit des tables et des index de taille quasiment identique, à cause du padding des lignes et de la déduplication des B-tree.
- Les colonnes NULL ne coûtent presque rien (juste un bit dans le bitmap de nullité), donc des colonnes optionnelles majoritairement vides sont quasi gratuites en espace.
- `count(DISTINCT x)` a été plus rapide que l'équivalent réécrit en `count(*)` sur un GROUP BY, à l'inverse du conseil habituel de réécriture.
- L'auteur insiste sur le fait que ces résultats dépendent du plan choisi, de `work_mem`, de la version de PostgreSQL et du matériel — ce ne sont pas des règles universelles.

## Analyse approfondie
# Quatre débats PostgreSQL qui se sont terminés à égalité

Certains conseils reviennent sans cesse en revue de code parce qu'ils semblent importants. J'en ai choisi quatre que j'ai vus débattus, et je les ai mesurés. Je m'attendais à au moins deux résultats nets. J'ai obtenu trois égalités et un résultat qui va dans le sens inverse du conseil habituel.

## Configuration

PostgreSQL 18.6, paramètres par défaut. MacBook Pro 13 pouces de 2020, Intel i5-8257U, 8 Go de RAM. Une table `u` de 2 000 000 lignes avec un id, un email, un statut et un timestamp. Les temps sont des temps d'exécution issus de `EXPLAIN (ANALYZE, TIMING OFF)`, cache chaud, premier run écarté, médiane des suivants.

## IN, ANY ou une jointure VALUES pour 1 000 ids

|  | médiane | runs | buffers |
|---|---|---|---|
| `id IN (1999, 3998, ...)` | 26 ms | 15 à 54 ms | 3 001 |
| `id = ANY('{...}'::bigint[])` | 19 ms | 15 à 20 ms | 3 001 |
| `JOIN (VALUES ...) v(i) ON id = i` | 20 ms | 16 à 21 ms | 3 001 |

Les trois lisent exactement les mêmes pages. Les médianes diffèrent, mais un run en IN a pris 54 ms et un autre 15 ms, donc je ne tirerais aucune conclusion de cet écart. Utilisez la forme que votre driver rend la plus simple. ANY a un avantage pratique quand le tableau est passé comme un unique paramètre : le texte de la requête reste identique quel que soit le nombre d'ids, ce qui est plus favorable aux requêtes préparées et à `pg_stat_statements`.

## text, smallint ou enum pour une colonne de statut

Trois valeurs, deux millions de lignes, chacune stockée de trois façons dans sa propre table à une colonne.

|  | table | index |
|---|---|---|
| text | 72,6 Mo | 13,9 Mo |
| smallint | 73,0 Mo | 13,9 Mo |
| enum | 72,7 Mo | 13,9 Mo |

Chaque ligne a un en-tête de 24 octets et est alignée sur 8 octets, donc un smallint de 2 octets et un `'active'` de 7 octets finissent par occuper la même taille. Les index sont identiques car la déduplication des B-tree stocke chaque valeur une seule fois avec une liste de pointeurs de lignes. Dans une table plus large, l'ordre des colonnes peut changer l'alignement, mais le type d'une courte colonne de statut n'est pas l'endroit où l'espace se perd. Choisissez-le pour ce qu'il permet de vérifier.

## Colonnes habituellement vides

Un million de lignes avec un id et dix autres colonnes entières. Dans une table, les dix colonnes sont toutes NULL ; dans l'autre, toutes remplies.

|  | table | par ligne |
|---|---|---|
| dix colonnes NULL | 44 Mo | 36 octets |
| dix colonnes remplies | 77 Mo | 68 octets |

Un NULL ne prend aucune place dans la ligne. Il coûte un seul bit dans le bitmap de nullité de la ligne. Les colonnes optionnelles qui sont majoritairement vides sont presque gratuites, ce qui est bon à savoir avant de découper une table pour économiser de l'espace.

## count(DISTINCT) contre GROUP BY

Le conseil que j'ai vu le plus souvent : `count(DISTINCT x)` est lent, il faut le réécrire en count sur une sous-requête GROUP BY. Sur deux millions d'emails uniques :

|  | médiane |
|---|---|
| `count(DISTINCT email)` | 1,95 s |
| `count(*) FROM (SELECT email FROM u GROUP BY email)` | 3,12 s |

La réécriture était plus lente. Je ne prétends pas qu'elle l'est toujours. Lequel des deux gagne dépend du plan que choisit le GROUP BY et de `work_mem`, et les deux changent selon les versions et les paramètres. C'est bien là le propos : c'est un conseil à vérifier avec EXPLAIN sur ses propres données, pas à appliquer tel quel.

## Ce que je n'ai pas testé

- Des listes IN de dizaines de milliers de valeurs.
- Des colonnes de statut à l'intérieur d'une ligne plus large, où l'alignement peut différer.
- `count(DISTINCT)` avec plus de `work_mem`, ou sur des colonnes à peu de valeurs distinctes.
- D'autre matériel. Comparez les ratios, pas les secondes.

## Le reproduire

run2.py et results2.json. Sections 1, 9, 10 et 12 du script.

## Pourquoi ça compte
Ce billet rappelle qu'en ingénierie de données, les "bonnes pratiques" répétées sans mesure peuvent être fausses ou sans objet selon la version et la configuration ; il encourage une culture de vérification empirique (EXPLAIN ANALYZE) plutôt que l'application mécanique de règles héritées en revue de code.
