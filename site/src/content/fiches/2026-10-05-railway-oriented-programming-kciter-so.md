---
title: "Railway-Oriented Programming | kciter.so"
date: 2026-10-05
url: "https://programmingdigest.net/links/23397/8e384055-4ef6-4411-8656-1644e3ae163f/email"
authors: ["kciter"]
keywords: ["programmation fonctionnelle", "gestion des erreurs", "monades", "Railway-Oriented Programming", "Kotlin", "Rust"]
theme: "Tech"
tone: "tutorial"
used_in: ["2026-10-05"]
---

## Résumé
L'article présente le Railway-Oriented Programming (ROP), une méthodologie issue de la programmation fonctionnelle proposée par Scott Wlaschin (F# for Fun and Profit) pour gérer les effets de bord et les erreurs de façon prévisible. Il part des approches classiques — LBYL, EAFP, fonctions pures, guard clauses, try-catch — pour en montrer les limites, puis construit pas à pas les notions de functor et de monade (via les types `Option` et `Result` en Kotlin) qui permettent de représenter l'échec comme une valeur plutôt que comme une exception. ROP en découle : chaque fonction est vue comme un aiguillage ferroviaire qui bascule entre une voie de succès et une voie d'échec, avec une voie de récupération optionnelle, ce qui rend le flux du programme séquentiel et lisible. L'article conclut sur les limites pratiques (imbrication des monades, absence de Higher-Kinded Types dans certains langages) et recommande un usage ciblé plutôt que systématique.

## Points clés
- Les effets de bord (I/O, erreurs internes à une fonction) rendent le comportement d'un programme imprévisible ; les approches LBYL (vérifier avant) et EAFP (agir puis rattraper) sont deux façons classiques de les gérer, sans que l'une soit supérieure à l'autre.
- Les fonctions pures et les guard clauses réduisent l'imprévisibilité mais ne résolvent pas les I/O externes ni les erreurs non anticipées ; try-catch reste utile mais nuit à la lisibilité (flux non séquentiel, erreurs à connaître à l'avance).
- Un functor est une "boîte" paramétrée qui permet d'appliquer une fonction à une valeur tout en gérant un cas particulier (ex. `Option` pour le null, `Result`/`Either` pour l'erreur) via une méthode `map`.
- Une monade résout le problème d'empilement de boîtes (`Result<Result<...>>`) grâce à `flatMap`, qui aplatit directement la valeur retournée par la fonction imbriquée.
- Le Railway-Oriented Programming modélise le programme comme une voie ferrée à trois rails : succès, échec, et récupération (`recover`/`rescue`), avec trois principes — exécution séquentielle, bifurcation succès/échec à chaque étape, et absence de panique du programme.
- Les limites pratiques existent : sans Monad Comprehension (ex. `for/yield` en Scala) ou Higher-Kinded Types (Monad Transformers), combiner plusieurs monades imbriquées complexifie le code ; l'auteur recommande de réserver `Result` aux fonctions qui en ont réellement besoin.

## Analyse approfondie

### Les effets de bord, racine du problème
Tout programme accumule, au fil de son évolution, des problèmes imprévus et de la dette technique. Un effet de bord est ce qui se produit à l'intérieur d'une fonction et affecte le monde extérieur à celle-ci : manipulation d'une variable externe, données corrompues reçues via le réseau, ou simplement une erreur survenant à l'intérieur d'une fonction et se répercutant sur le reste du programme. Ce dernier cas est souvent négligé par les développeurs — y compris dans du code très simple, comme une fonction qui récupère le premier élément d'une liste et qui échoue si la liste est vide.

### Deux philosophies : LBYL et EAFP
Au-delà du simple branchement conditionnel, deux grandes familles de gestion des effets de bord existent :
- **LBYL (Look Before You Leap)** : on vérifie explicitement les conditions avant d'exécuter la logique (ex. tester si une liste est vide avant d'y accéder).
- **EAFP (Easier to Ask for Forgiveness than Permission)** : on exécute la logique directement et on rattrape l'exception si elle survient (ex. bloc try/catch autour de l'accès à la liste).

Python privilégie l'EAFP, mais aucune des deux approches n'est intrinsèquement meilleure : chacune convient à des situations différentes.

### Fonctions pures et guard clauses
Quand il n'y a pas d'I/O externe à gérer, écrire des fonctions pures — qui renvoient toujours la même sortie pour les mêmes entrées — permet de rendre le résultat prévisible (mais pas nécessairement mathématiquement exact : les limites des nombres flottants en sont un exemple classique, où `0.0 + 1.0/3 * 10` répété en boucle peut différer de `1.0/3*10` calculé directement, bien que la fonction reste pure). Le choix d'une spécification d'implémentation adaptée (arrondi, calcul exact via chaînes de caractères, etc.) permet de traiter ce genre d'écart.

Le guard clause consiste à placer les conditions défensives en tout début de logique, évitant les `if` imbriqués et améliorant la lisibilité. Swift intègre même une instruction `guard` dédiée, où le bloc s'exécute quand la condition n'est *pas* remplie.

### try-catch : utile mais limité en lisibilité
Le try-catch, supporté depuis longtemps par de nombreux langages, isole le code pouvant lever une exception dans un bloc `try` et le traitement de l'erreur dans un bloc `catch`. Il est généralement utilisé dans la logique appelante plutôt que dans la fonction appelée elle-même. Son principal défaut est que le flux de contrôle n'est plus séquentiel : lors d'une exception, l'exécution bascule abruptement vers le `catch`, et un bloc `finally` oblige à vérifier d'où l'on provient. De plus, le développeur doit connaître à l'avance la liste des erreurs qu'une fonction peut lever, ce qui devient coûteux quand les erreurs personnalisées se multiplient. Cela dit, pour un programme qui ne doit jamais s'arrêter brutalement (comme un serveur), try-catch reste très utile.

### Functors : encapsuler une valeur pour gérer un cas particulier
Avant d'aborder les functors et les monades, l'article rappelle la notion de type comme ensemble de départ (domaine) et d'arrivée (image) d'une fonction. Une fonction comme la division entière n'est pas pure si elle peut lever une erreur de division par zéro : son image ne couvre alors pas tout l'ensemble `Int`. Pour représenter l'erreur comme faisant partie du résultat, il faut créer un nouveau type — c'est l'idée du **functor** : une "boîte" qui contient une valeur, que l'on peut extraire, transformer via une fonction, puis réinsérer dans la boîte. La méthode qui réalise cette opération est généralement nommée `map`.

Exemple générique :
```kotlin
class Functor<T>(private val value: T) {
  fun <R> map(f: (T) -> R): Functor<R> = Functor(f(this.value))
}
```

En appliquant cette idée, on peut construire un type `Option` qui distingue `Some` (valeur présente) de `None` (valeur absente), ce qui permet de prévenir les erreurs de type NullPointerException, avec un filtrage par pattern matching garantissant qu'aucun cas n'est oublié.

De la même manière, un type `Result<V, E>` (avec les variantes `Success` et `Failure`) permet d'encapsuler soit une valeur de succès, soit une erreur, en remplaçant le try-catch classique par une valeur manipulable. Toutefois, enchaîner des fonctions qui renvoient chacune un `Result` via `map` provoque un problème d'empilement : on obtient un `Result<Result<Int, Throwable>, Throwable>`, ce qui casse la cohérence des types.

### Monades : aplatir l'empilement de boîtes
La **monade** résout précisément ce problème d'imbrication. De nombreux développeurs en utilisent déjà sans le savoir, via la fonction `flatMap` : là où `map` sur une `List<Int>` produirait une `List<List<Int>>`, `flatMap` restitue directement une `List<Int>`, car la valeur renvoyée par la fonction est utilisée telle quelle plutôt que réemballée dans une nouvelle boîte.

Appliqué à `Result` :
```kotlin
fun <V, R, E> Result<V, E>.flatMap(f: (V) -> Result<R, E>): Result<R, E> =
  when (this) {
    is Result.Success -> f(this.value)
    is Result.Failure -> this
  }
```
Ainsi, enchaîner `sum(...).flatMap { divide(it, 0) }` conserve des types cohérents et permet de traiter proprement l'erreur de division par zéro.

### Le Railway-Oriented Programming proprement dit
ROP est une méthodologie fonctionnelle de contrôle des effets de bord introduite par Scott Wlaschin. Bien que peu connue sous ce nom, elle est partiellement suivie par Rust, qui ne dispose pas de try-catch et s'appuie sur un type `Result` associé à un filtrage par motif (`match`) pour traiter les erreurs.

L'idée centrale : la logique du programme se scinde en succès ou en échec à chaque étape, et chaque chemin possède sa propre "voie". ROP repose sur trois principes :
- chaque fonction s'exécute de façon séquentielle ;
- chaque fonction se divise en succès ou en échec ;
- le programme ne doit jamais paniquer (planter brutalement).

En abstrayant la logique comme une voie ferrée, on découpe naturellement les fonctionnalités en unités pouvant être scindées en succès/échec, ce qui facilite l'implémentation, le refactoring et la lisibilité, puisque le flux reste séquentiel.

### Les trois voies : succès, échec, récupération
ROP distingue :
- la **voie de succès**, où la logique se déroule comme prévu ;
- la **voie d'échec**, où une étape échoue en cours de route ;
- la **voie de récupération**, qui permet, après un échec récupérable, de revenir sur la voie de succès.

Cette récupération s'implémente via une fonction `recover` (ou `rescue`) :
```kotlin
fun <V, E> Result<V, E>.recover(f: (E) -> V): Result.Success<V> =
  when (this) {
    is Result.Success -> this
    is Result.Failure -> Result.Success(f(error))
  }
```
En typant précisément les erreurs possibles via une `sealed class`, on peut distinguer chaque cause d'échec (ex. `DivideByZero`, `TooBig`, `TooSmall`) et les traiter spécifiquement dans un `recover`, le compilateur garantissant l'exhaustivité du traitement.

### Limites pratiques : imbrication et Higher-Kinded Types
Même avec `flatMap`, certains cas restent imbriqués — par exemple quand une étape ultérieure a besoin d'une valeur produite par une étape antérieure. Des langages comme Scala ou Haskell résolvent cela via la **Monad Comprehension** (syntaxe `for ~ yield` en Scala), que Kotlin ne supporte pas nativement (on peut l'approcher avec les Context Receivers, via des bibliothèques comme Arrow).

Lorsqu'on doit combiner plusieurs monades différentes (par exemple `Result` et `Option` ensemble, ou dans un contexte réactif avec Mono/Flux ou une bibliothèque de la famille Rx), le code peut nécessiter un dépaquetage manuel par pattern matching, ce qui devient rapidement complexe. La solution générale passe par les **Higher-Kinded Types (HKT)**, peu supportés par les langages courants (absents de Kotlin, présents en Scala), qui permettent d'implémenter un **Monad Transformer** (ex. `OptionT` dans la bibliothèque cats) pour composer proprement plusieurs monades sans imbrication.

### Conclusion de l'auteur
ROP permet d'écrire du code plus sûr et plus intuitif, mais son adoption dépend fortement de l'environnement technique (support ou non des HKT, de la Monad Comprehension). L'auteur déconseille d'utiliser `Result` pour absolument toutes les fonctions, au risque de nuire à la lisibilité : il recommande de le réserver aux fonctions qui en ont réellement besoin.

## Pourquoi ça compte
ROP offre un vocabulaire et des patterns concrets (Option, Result, flatMap, recover) pour remplacer les exceptions par des valeurs typées, une tendance de fond dans les langages modernes (Rust, Swift, Kotlin) ; comprendre ses principes et ses limites (imbrication, HKT) aide à juger quand l'adopter dans une base de code sans sacrifier la lisibilité.
