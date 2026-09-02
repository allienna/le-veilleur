---
title: "GitHub - jeffhajewski/latticedb: Embedded single-file knowledge graph database with vector search and full-text search for AI/RAG apps"
date: 2026-09-02
url: "https://elink56e.dataelixir.com/ss/c/u001.Dt8L-Y0jq6TkmYqlU8wlZM7Wgh8ux-hPslUUIPQJ3xXXxW52jH-bDhBx-qLtpsVT-UOFQUgiWGZ79GGR2aSFXp4YDnu92uhRXAjcTmK2VP6c71SToUeQsLLnU_U_Qkg8y61AcdAsvl3kd-ekmdKS6vS1M9BFU2Af0p2os2k-2J-l4zSGUrw9l2mmwinZ0gvz9yNn9G7ubvcmeMJd2w1_Ug/4to/fP9g9RI3QPmrGoOJ8JMNAQ/h11/h001.l7y9IE4rTbHeBBiNFkxi2YfGxWPRBWr7dD7HaERkXuE"
authors: ["Jeff Hajewski"]
keywords: ["base de données graphe", "recherche vectorielle", "embarqué", "RAG", "full-text", "HNSW"]
theme: "Tech"
tone: "tutorial"
used_in: ["2026-09-02"]
---

## Résumé
LatticeDB est une base de données de graphe embarquée, mono-fichier, écrite en Zig, qui combine dans un seul moteur et un seul langage de requête : traversée de graphe, recherche vectorielle par similarité (HNSW) et recherche plein texte (BM25). Elle vise les charges de travail locales, mono-processus, riches en relations — RAG, mémoire d'agent, outils de connaissance locaux — sans serveur ni configuration. Le projet met en avant des benchmarks agressifs (0,13 µs pour une lecture de nœud, 0,83 ms pour une recherche vectorielle à 1M de vecteurs avec 100% de rappel) et se positionne comme une alternative légère à SQLite, Neo4j ou des bases vectorielles dédiées pour le prototypage sur une seule machine. Des bindings existent pour Python, TypeScript/Node.js, Go et Java, avec un langage de requête proche de Cypher.

## Points clés
- Un seul fichier, un seul moteur : traversée de graphe (Cypher-like), recherche vectorielle HNSW et recherche plein texte BM25 dans le même langage de requête.
- Modèle mono-écrivain embarqué, local-first, avec journal WAL pour la durabilité et la reprise après crash.
- Benchmarks internes revendiquant des performances supérieures à SQLite, RocksDB, FAISS, Neo4j, Weaviate ou Qdrant sur des opérations comparables.
- Ne convient pas aux cas nécessitant plusieurs écrivains concurrents, du multi-nœud/sharding, des données purement tabulaires, ou l'intégralité du langage Cypher (pas de `OPTIONAL MATCH` ni de procédures `CALL`).
- Écosystème jeune et minimal comparé à Neo4j ou PostgreSQL (peu d'outillage, pas de dashboards, pas de drivers matures dans tous les langages).
- Fonctionnalités opérationnelles notables : sauvegarde continue, sauvegarde à chaud, sérialisation en mémoire, flux nommés durables et changefeed de graphe.

## Analyse approfondie
**Base de données propriété-graphe avec indexation vectorielle et plein texte native.**

LatticeDB est une base de données locale mono-fichier pour des données connectées, sémantiques et textuelles. Elle permet de parcourir des relations, d'exécuter une recherche par similarité vectorielle et de faire une recherche plein texte BM25 sur le même jeu de données, dans un seul moteur et une seule couche de requête. Elle est conçue pour des charges de travail riches en relations sur une seule machine, avec un fonctionnement sans configuration et un modèle embarqué mono-écrivain.

LatticeDB est une base de données de graphe embarquée, mono-fichier, qui permet aux applications locales d'interroger les mêmes données par relation, sémantique et texte, puis de consommer des événements durables de graphe et d'application depuis ce même fichier. Des charges de travail comme le Graph RAG, la mémoire d'agent et les outils de connaissance locaux en sont des exemples construits sur ces primitives, pas la définition du moteur.

- **Un seul fichier.** Toute la base de données est un fichier unique et portable. Pas de serveur, pas de configuration.
- **Une seule couche de requête.** Traversée de graphe, similarité vectorielle HNSW et plein texte BM25 — dans le même langage de requête.
- **Un seul journal d'événements.** Des flux nommés durables et un changefeed de graphe intégré partagent le même chemin de transaction/WAL que les écritures du graphe.
- **Local-first.** Conçue pour un seul processus propriétaire sur une seule machine, avec durabilité assurée par le WAL.
- **Rapide.** Lecture de nœud en 0,13 µs. Recherche vectorielle en 0,83 ms sur 1M de vecteurs avec 100% de rappel.

```
// Trouver des chunks similaires à une requête, remonter au document puis à l'auteur
MATCH (chunk:Chunk)-[:PART_OF]->(doc:Document)-[:AUTHORED_BY]->(author:Person)
WHERE chunk.embedding <=> $query_vector < 0.3
  AND doc.content @@ "neural networks"
RETURN doc.title, chunk.text, author.name
ORDER BY chunk.embedding <=> $query_vector
LIMIT 10
```

**CLI** : `curl -fsSL https://raw.githubusercontent.com/jeffhajewski/latticedb/main/dist/install.sh | bash`

**Python** : `pip install latticedb`. Les wheels publiées sont censées embarquer `liblattice` sur les plateformes supportées. Les installations depuis les sources peuvent aussi embarquer une bibliothèque native pré-construite via `LATTICE_BUNDLE_LIB_DIR=/path/to/lib`.

**TypeScript / Node.js** : `npm install @hajewski/latticedb`. Les tarballs publiées sont censées embarquer `liblattice` sur les plateformes supportées. Les checkouts depuis les sources peuvent intégrer la bibliothèque native dans le package avec `LATTICE_BUNDLE_LIB_DIR=/path/to/lib npm run bundle:native`.

**Java** : nécessite JDK 21+. Voir bindings/java/README.md pour la construction Maven, qui compile le pont JNI et intègre `liblattice` depuis `zig-out/lib`. Un exemple exécutable de graphe de connaissance se trouve dans bindings/java/src/main/java/io/latticedb/examples.

**Go** : voir bindings/go/README.md pour le workflow cgo actuel. Le chemin consommateur par défaut utilise les métadonnées `pkg-config` installées ; le développement dans le dépôt peut utiliser `-tags repolocal` contre `zig-out/lib`. Il existe aussi un exemple exécutable de récupération graphe/vecteur/texte dans examples/go.

Des nettoyages récents de la surface des bindings ont déplacé les helpers d'embedding vers des modules et sous-packages dédiés. Voir docs/client_api_migration.md pour les imports préférés et les alias de compatibilité actuels.

- Le guide « Getting Started » propose le chemin le plus court pour CLI, Python, TypeScript, Go et Java.
- Le « CLI Quickstart » est le plus petit exemple copier-coller du dépôt.
- La vue d'ensemble des exemples couvre les démonstrations plus larges de récupération graphe/vecteur/texte.

Un exemple complet : créer un petit graphe de connaissance avec des documents et des auteurs, stocker des embeddings, indexer du texte, puis interroger les trois modes de recherche à la fois.

Les exemples utilisent le helper intégré `hash_embed` / `hashEmbed` / `HashEmbed` afin de fonctionner sans service externe. C'est un substitut déterministe, pas un embedding sémantique réel : un texte similaire ne produit pas des vecteurs proches, donc un seuil de distance est arbitraire et une requête de similarité peut ne rien trouver. Utilisez un vrai modèle d'embedding dès que le résultat doit avoir un sens — voir « Working with Embeddings ».

[Suivent des exemples de code identiques en Python, TypeScript, Go et Java, illustrant la création d'un graphe (Person, Document, Chunk), le stockage de vecteurs, l'indexation plein texte et une requête combinant traversée de graphe, recherche vectorielle et agrégations.]

Benchmarks réalisés sur Apple M1, mono-thread, avec pool de buffers auto-dimensionné. Exécuter `zig build benchmark` pour reproduire. Pour la charge d'indexation FTS à termes répétés qui avait révélé un comportement quadratique, exécuter `zig build fts-benchmark`.

| Opération | Latence | Débit | Cible | Statut |
|---|---|---|---|---|
| Lecture de nœud | 0,13 µs | 7,9M ops/s | < 1 µs | PASS |
| Création de nœud | 0,65 µs | 1,5M ops/s | — | — |
| Traversée d'arête | 9 µs | 111K ops/s | — | — |
| Recherche plein texte (100 docs) | 19 µs | 53K ops/s | — | — |
| 10-NN vectoriel (1M vecteurs) | 0,83 ms | 1,2K ops/s | < 10 ms @ 1M | PASS |

Vecteurs cosinus à 128 dimensions, M=16, ef_construction=200, ef_search=64, k=10. Exécuter `zig build vector-benchmark` pour reproduire.

| Échelle | Latence moyenne | Latence P99 | Rappel@10 | Mémoire |
|---|---|---|---|---|
| 1 000 | 65 µs | 70 µs | 100% | 1 Mo |
| 10 000 | 174 µs | 695 µs | 99% | 10 Mo |
| 100 000 | 438 µs | 1,2 ms | 99% | 101 Mo |
| 1 000 000 | 832 µs | 1,8 ms | 100% | 1 040 Mo |

La latence de recherche croît de façon sous-linéaire (O(log N)) avec un rappel@10 de 99-100%. Utilise une sélection heuristique de voisins (Algorithme 4 du papier HNSW) pour une connectivité de graphe diversifiée, un compactage des pages de connexion pour une réduction mémoire d'environ 4,5x, et un produit scalaire pré-normalisé pour une distance cosinus rapide.

**Sensibilité à ef_search (1M vecteurs)**

| ef_search | Latence moyenne | Rappel@10 |
|---|---|---|
| 16 | 506 µs | 57% |
| 32 | 1,9 ms | 79% |
| 64 | 990 µs | 100% |
| 128 | 3,2 ms | 100% |
| 256 | 11,6 ms | 100% |

Comparaisons annoncées : sur la latence de lecture de nœud, LatticeDB (0,13 µs) se situe au niveau de RocksDB en mémoire (0,14 µs) et devance SQLite sur disque de 23x. Sur la recherche vectorielle 10-NN à 1M, LatticeDB (0,83 ms, 100% de rappel) devance FAISS HNSW mono-thread (0,5-3 ms) et reste compétitive face à Weaviate et Qdrant, serveurs qui ajoutent une latence réseau en pratique. Sur la traversée à 2 sauts (100K nœuds), LatticeDB affiche 39 µs contre 548 µs pour une CTE récursive SQLite — seules ces deux lignes sont mesurées sur la même machine avec le même harnais ; les chiffres Kuzu et Neo4j viennent de sources tierces et ne sont donc qu'indicatifs.

**LatticeDB vs SQLite** — graphe de réseau social à distribution en loi de puissance, cache d'adjacence préchargé :

À petite échelle (10K nœuds, 50K arêtes), LatticeDB est 23x plus rapide sur une traversée à 1 saut, 13x à 2 sauts, 9x à 3 sauts, et 52x sur un chemin de longueur variable (1..5). À échelle moyenne (100K nœuds, 500K arêtes), les gains vont de 6x à 75x selon l'opération. Sur une traversée à profondeur limitée, l'écart se creuse fortement avec la profondeur : de 390x à une profondeur de 10 jusqu'à 2 819x à une profondeur de 50. LatticeDB utilise un parcours BFS avec cache d'adjacence et suivi de visite par bitset ; SQLite utilise une CTE récursive avec déduplication `UNION`. Les deux calculent le même ensemble de nœuds atteignables (~8K nœuds) ; l'écart s'élargit aux profondeurs importantes car le coût de la CTE croît à chaque niveau de récursion.

Sur la recherche plein texte, l'index inversé à score BM25 de LatticeDB (19 µs) est annoncé environ 300x plus rapide que SQLite FTS5 (< 6 ms) et compétitif avec Tantivy, une bibliothèque de recherche Rust dédiée.

**Fonctionnalités**

*Graphe* : nœuds et arêtes avec labels et propriétés arbitraires ; index d'égalité durables sur des propriétés ciblées ; traversée multi-sauts et chemins de longueur variable (`*1..3`) ; transactions ACID avec commit/rollback et reprise après crash ; `MERGE`, `WITH`, `UNWIND`, agrégations (`count`, `sum`, `avg`, `min`, `max`, `collect`).

*Recherche vectorielle* : plus proches voisins approximatifs HNSW (M, ef configurables) ; embeddings par hachage intégrés ou client HTTP pour Ollama/OpenAI ; insertion en masse de nœuds vectoriels pour une ingestion rapide.

*Recherche plein texte* : index inversé à score BM25 avec tokenisation et racinisation (stemming) ; recherche floue avec distance de Levenshtein configurable.

*Langage de requête (proche de Cypher)* : `MATCH`, `WHERE`, `RETURN`, `CREATE`, `DELETE`, `SET`, `REMOVE`, `ORDER BY`, `LIMIT`, `SKIP`, `DETACH DELETE` ; opérateur de distance vectorielle `<=>` ; opérateur de recherche plein texte `@@` ; paramètres `$name`.

*Opérations* : stockage mono-fichier avec journal d'écriture anticipée (WAL) pour la reprise après crash ; sauvegarde continue vers un répertoire avec restauration à un point dans le temps ; sauvegarde à chaud via `lattice backup`, sans fermer la base ; sérialisation d'une base en octets et ouverture depuis des octets, pour stocker de nombreuses petites bases dans du stockage objet ; bases en mémoire avec `:memory:`, sans toucher au disque ; flux nommés durables avec offsets de consommateur explicites, purge manuelle et changefeeds de graphe ; réutilisation de freelist en ligne plus `lattice compact` pour une récupération physique sûre de la queue ; zéro configuration ; modèle embarqué mono-écrivain pour applications locales ; API C propre, avec bindings Python, TypeScript, Go et Java.

**Cas d'usage visés** : données locales connectées (notes, documents, catalogues, graphes de citations et d'entités) ; graphe plus récupération (traversée relationnelle, recherche sémantique et lexicale sur le même jeu de données) ; outils de connaissance locaux embarqués sans serveur séparé ; mémoire d'agent et pipelines RAG comme exemple de charge construite sur le substrat graphe/vecteur/texte ; développement local comme alternative légère à Neo4j ou Weaviate pour le prototypage sur une machine.

**Quand ne pas utiliser LatticeDB** : si plusieurs applications doivent écrire simultanément dans la même base (modèle mono-écrivain, préférer Neo4j ou PostgreSQL) ; si les données sont fondamentalement tabulaires (une base relationnelle comme SQLite ou PostgreSQL sera plus simple et tout aussi rapide) ; si le besoin dépasse une seule machine (LatticeDB peut répliquer les changements d'un fichier en continu — c'est de la sauvegarde, pas du clustering ; pour du sharding ou des requêtes distribuées sur des milliards de nœuds, voir Neo4j cluster, Dgraph ou un service managé comme Neptune) ; si le langage Cypher complet est requis (pas encore de `OPTIONAL MATCH` ni de procédures `CALL` — Neo4j reste l'implémentation complète) ; si un outillage et un écosystème mûrs sont nécessaires (Neo4j dispose d'outils de visualisation, de dashboards d'administration, de monitoring et de drivers dans tous les langages ; PostgreSQL a des décennies d'outillage ; LatticeDB est jeune et léger, un atout pour l'embarqué mais une faiblesse pour un écosystème opérationnel riche).

Écrit en Zig, sans dépendances. Construction : `git clone ... && cd latticedb && zig build && zig build test`. La documentation complète vit sur docs.latticedb.org (référence Cypher, API C/Python/TypeScript/Go, guides, internals du moteur de stockage) ; latticedb.org est le site du projet.

## Pourquoi ça compte
LatticeDB illustre la tendance à unifier graphe, recherche vectorielle et plein texte dans un seul moteur embarqué mono-fichier, une architecture directement pertinente pour les pipelines RAG et la mémoire d'agent qui, jusqu'ici, empilaient souvent trois systèmes séparés (base relationnelle, base vectorielle, moteur de recherche).
