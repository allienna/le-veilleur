---
title: "GitHub - mitdbg/pgvectorfast: Postgres extension for vector search with performance enhancements built on Calico buffer pool."
date: 2026-11-20
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fgithub.com%2Fmitdbg%2Fpgvectorfast%3Futm_source=tldrdata/1/010001a1f382eb1c-813c2c29-0e67-4fcb-a679-689a5eec2cc8-000000/wZN53G65LQD9HTyfZ71ppneFb7DYxAHNcoUiq9To1RA=452"
authors: ["Xinjing Zhou", "Jinming Hu", "Andrew Pavlo", "Michael Stonebraker"]
keywords: ["PostgreSQL", "pgvector", "recherche vectorielle", "buffer pool", "HNSW", "performance"]
theme: "Data"
tone: "tutorial"
used_in: ["2026-11-20"]
---

## Résumé
pgvectorfast est une extension PostgreSQL qui accélère la recherche de similarité vectorielle et les requêtes analytiques en remplaçant le gestionnaire de buffer standard de PostgreSQL par un nouveau buffer pool nommé Calico. Construit comme une surcouche compatible de pgvector (mêmes types de données, opérateurs de distance et index HNSW/IVFFlat), il cible le goulot d'étranglement créé par la traduction de pages via table de hachage partitionnée et les verrous/pins atomiques lors des parcours de graphes HNSW. L'extension combine trois techniques : traduction de pages par tableaux avec cache de chemins, lectures optimistes sans verrou, et préchargement groupé adapté à la charge de travail. Le projet est distribué via Docker, paquets APT (Debian), PGXN ou compilation depuis les sources, et s'appuie sur des travaux de recherche publiés par des membres du MIT (groupe de bases de données).

## Points clés
- Remplace le gestionnaire de buffer partagé de PostgreSQL par le buffer pool Calico, tout en conservant une compatibilité SQL et sur disque complète avec pgvector (types `vector`, `halfvec`, `bit`, `sparsevec`, index `hnsw`/`ivfflat`).
- Trois techniques combinées : traduction de pages par tableaux à deux niveaux avec cache préfixe par backend, lectures optimistes sans verrou (`calico.optimistic_reads`) pour les parcours HNSW, et préchargement groupé des voisins (`hnsw.enable_prefetch`) tirant parti du cache CPU et de l'AIO/`io_uring`.
- Fonctionne sur PostgreSQL 18 et 19, Linux x86-64 uniquement, avec plusieurs modes d'installation : image Docker prête à l'emploi, paquets APT PGDG pour Debian, installation via PGXN, ou compilation depuis les sources.
- Contrainte notable : incompatible avec les builds PostgreSQL compilés avec LTO (`-flto=auto`), comme ceux des paquets PGDG Ubuntu, car Calico nécessite des symboles de debug non-LTO du serveur.
- Nécessite l'activation explicite après chaque redémarrage de PostgreSQL via `CALL calico.activate();`.
- S'appuie sur un travail de recherche académique (« Calico ») cité dans un article arXiv signé par des chercheurs du MIT, dont Andrew Pavlo et Michael Stonebraker.

## Analyse approfondie
**pgvectorfast est une amélioration haute performance, drop-in, de pgvector qui accélère la recherche de similarité vectorielle et les requêtes analytiques dans PostgreSQL grâce à un buffer pool partagé rapide.**

Basé sur pgvector, pgvectorfast est une extension PostgreSQL standard fonctionnant sur des serveurs PostgreSQL 18 et 19 non modifiés, pour une recherche de similarité vectorielle rapide. Il préserve une compatibilité SQL et sur disque complète avec tous les types de données `pgvector` (`vector`, `halfvec`, `bit`, `sparsevec`), les opérateurs de distance et les types d'index (`hnsw`, `ivfflat`). Voir la documentation pgvector pour l'API SQL complète, les paramètres d'index et le guide d'utilisation.

Voir les résultats détaillés de benchmark pour les mesures de rappel, les décompositions de latence et les configurations expérimentales.

Le gestionnaire de buffer par défaut de PostgreSQL traduit chaque référence de page via une table de hachage partagée et partitionnée, et acquiert des pins atomiques ainsi que des verrous de contenu de page à chaque lecture de page. Lors des recherches par index vectoriel et des scans/jointures analytiques — et en particulier lors du parcours de graphe HNSW, qui effectue des milliers de recherches de voisins irrégulières par requête — la traduction de pages, le trafic atomique de pin/unpin et les entrées-sorties aléatoires synchrones deviennent des goulots d'étranglement majeurs.

pgvectorfast remplace le gestionnaire de buffer partagé de PostgreSQL par le buffer pool **Calico** (*Making Array-Based Translation Practical for Modern, High-Performance Buffer Management*), qui combine trois techniques :

1. **Traduction de pages par tableaux et cache de chemins** : remplace la table de hachage de recherche de buffer partagé de PostgreSQL et les verrous de partition sur les chemins critiques par une indexation directe par tableaux à deux niveaux, adossée à des régions de mémoire virtuelle allouées de manière différée, associée à un cache préfixe de relation par backend (taux de succès proche de 100 % sur les index HNSW).
2. **Lectures optimistes sans verrou (`calico.optimistic_reads`)** : encode l'état de verrou et de version dans chaque entrée de traduction de 64 bits, afin que le parcours HNSW lise les vecteurs voisins et calcule les distances L2 ou produit scalaire (y compris la recherche cosinus normalisée) de manière spéculative, sans opérations atomiques de pin/unpin ni verrous de contenu, avec un repli transparent vers des lectures avec pin dès qu'une écriture concurrente ou une éviction survient.
3. **Préchargement groupé adapté à la charge de travail (`hnsw.enable_prefetch`)** : regroupe les recherches de pages voisines à chaque saut du graphe HNSW pour émettre des chargements de traduction parallèles et des préchargements CPU ciblés (`__builtin_prefetch`) pour les pages résidentes (parallélisme au niveau mémoire), ainsi que des lectures asynchrones groupées via PostgreSQL AIO/`io_uring` pour les pages non résidentes (parallélisme au niveau E/S).

Téléchargez et exécutez une image prête à l'emploi pour x86-64 (`linux/amd64`) avec PostgreSQL 18, les symboles de debug correspondants (`postgresql-18-dbgsym`), et `shared_preload_libraries = 'vectorfast'` préconfiguré :

```
docker run -d \
  --name pgvectorfast \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  zxjcarrot/pgvectorfast:pg18
```
Tags disponibles : `pg18` / `latest` (`postgres:18-trixie`), `pg18-trixie`, `pg18-bookworm`, et `<version>-pg18` sur les tags de release.

Pour construire l'image localement :

`docker build --build-arg PG_MAJOR=18 -t pgvectorfast .`

Des paquets `postgresql-18-pgvectorfast` précompilés pour Linux x86-64 (`amd64`) sont publiés pour Debian 12 (`bookworm`) et Debian 13 (`trixie`) contre le dépôt APT PGDG de PostgreSQL. Ils déclarent `Conflicts`/`Replaces`/`Provides` pour `postgresql-18-pgvector` et dépendent des symboles `postgresql-18-dbgsym` correspondants. (Les paquets PGDG Ubuntu compilent PostgreSQL avec `-flto=auto`, que Calico rejette au démarrage car la LTO intègre en ligne les routines internes du gestionnaire de buffer ; sous Ubuntu, utilisez l'image Docker ou compilez depuis les sources contre un build PostgreSQL sans LTO.)

1. Assurez-vous que le dépôt APT PostgreSQL (PGDG) est activé (par exemple via `postgresql-common`/`/usr/share/postgresql-common/pgdg/apt.postgresql.org.sh`).
2. Ajoutez la clé de signature APT et le dépôt `pgvectorfast`, puis installez :

```
sudo install -d -m 0755 /etc/apt/keyrings
curl -fsSL https://mitdbg.github.io/pgvectorfast/pgvectorfast.asc | sudo tee /etc/apt/keyrings/pgvectorfast.asc >/dev/null
echo "deb [signed-by=/etc/apt/keyrings/pgvectorfast.asc] https://mitdbg.github.io/pgvectorfast $(. /etc/os-release && echo "$VERSION_CODENAME") main" | sudo tee /etc/apt/sources.list.d/pgvectorfast.list
sudo apt-get update
sudo apt-get install -y postgresql-18-pgvectorfast
```
1. Poursuivez avec le guide de démarrage rapide pour précharger `vectorfast` et activer l'extension.

Installez via PGXN en utilisant `pgxnclient`. Comme PGXN compile depuis les sources contre votre installation PostgreSQL, assurez-vous d'abord de disposer des en-têtes de développement PostgreSQL 18 ou 19 (`pg_config`), des symboles serveur non-LTO (comme `postgresql-18-dbgsym` sur Debian PGDG, ou un build source non dépouillé), de `libcapstone-dev` (ou de Python `pip`), d'un compilateur C et de GNU Make :

```
sudo apt-get update
sudo apt-get install -y pgxnclient build-essential libcapstone-dev postgresql-server-dev-18 postgresql-18-dbgsym
sudo pgxn install pgvectorfast
```
Si votre `pg_config` cible n'est pas en premier dans le `PATH` (ou si vous compilez en tant qu'utilisateur non privilégié), passez `--pg_config` et `--sudo` :

`pgxn install --sudo --pg_config /path/to/pg_config pgvectorfast`

Poursuivez avec le guide de démarrage rapide pour précharger `pgvectorfast` dans `postgresql.conf` et activer Calico.

- Linux x86-64
- PostgreSQL 18 ou 19 avec en-têtes de développement serveur (`pg_config`) et symboles serveur non-LTO : soit un build source non dépouillé, soit un build packagé avec les symboles de debug correspondants installés (par ex. `postgresql-18-dbgsym`)
- Compilateur C (GCC ou Clang) et GNU Make
- Capstone (`libcapstone-dev` 4.x/5.x via les paquets système, ou amorcé automatiquement comme `capstone==5.0.6` dans `~/.cache/pgvectorfast/python-deps` via `pip` Python pendant `make` ; à surcharger avec `CAPSTONE_PREFIX=/path/to/capstone` ; doit rester disponible au moment de l'exécution)

```
git clone https://github.com/mitdbg/pgvectorfast.git
cd pgvectorfast
make
make install # peut nécessiter sudo
```
Si votre installation PostgreSQL cible n'est pas en premier dans le `PATH`, passez `PG_CONFIG` :

```
make PG_CONFIG=/path/to/pg_config
make PG_CONFIG=/path/to/pg_config install
```
1. Ajoutez `vectorfast` à `shared_preload_libraries` dans `postgresql.conf` et redémarrez PostgreSQL :

`shared_preload_libraries = 'vectorfast'`
1. Activez pgvector et le buffer pool Calico en utilisant l'une des deux approches (en tant que superutilisateur, hors d'un bloc de transaction) :

En une seule commande :

`CREATE EXTENSION vectorfast;`

Ou créez les extensions et activez Calico explicitement :

```
CREATE EXTENSION vector;
CREATE EXTENSION calico;
CALL calico.activate();
```
Après chaque redémarrage ultérieur de PostgreSQL, exécutez `CALL calico.activate();` pour réactiver le buffer pool.

1. Créez un index HNSW et exécutez des requêtes de similarité en utilisant le SQL pgvector standard :

```
CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(128));
CREATE INDEX ON items USING hnsw (embedding vector_l2_ops);
SELECT * FROM items ORDER BY embedding <-> '[...]' LIMIT 10;
```
Voir l'exemple exécutable de démarrage rapide et la documentation complète de pgvector pour tous les types vectoriels, opérateurs de distance, scans itératifs et options d'indexation.

| Paramètre | Contexte | Défaut | Description |
|---|---|---|---|
| `calico.optimistic_reads` | Session / Utilisateur | `on` | Active les lectures de tuples optimistes sans verrou pendant le parcours HNSW pour `vector_l2_ops`, `vector_ip_ops` et `vector_cosine_ops`. |
| `hnsw.enable_prefetch` | Session / Utilisateur | `on` | Active le préchargement groupé des voisins (préchargement CPU + regroupement des lectures asynchrones) pendant la recherche HNSW. |

Si vous utilisez pgvectorfast, veuillez citer notre travail comme suit :

```
@misc{zhou2026calico,
  title         = {Making Array-Based Translation Practical for Modern, High-Performance Buffer Management},
  author        = {Xinjing Zhou and Jinming Hu and Andrew Pavlo and Michael Stonebraker},
  year          = {2026},
  eprint        = {2604.00423},
  archivePrefix = {arXiv},
  primaryClass  = {cs.DB},
  url           = {https://arxiv.org/abs/2604.00423}
}
```

## Pourquoi ça compte
Ce projet illustre une tendance de fond en bases de données : réécrire les couches internes (gestion mémoire/buffer) pour exploiter le matériel moderne (AIO, io_uring, cache CPU) plutôt que d'optimiser uniquement les algorithmes applicatifs, une piste à surveiller pour qui suit l'évolution de l'infrastructure de recherche vectorielle en production.
