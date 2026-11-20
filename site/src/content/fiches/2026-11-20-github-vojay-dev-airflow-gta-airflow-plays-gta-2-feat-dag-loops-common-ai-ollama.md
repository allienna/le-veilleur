---
title: "GitHub - vojay-dev/airflow-gta: Airflow plays GTA 2 🚗, feat. Dag Loops, Common AI, Ollama, Nimble (local decision model), Plugins, and more"
date: 2026-11-20
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fgithub.com%2Fvojay-dev%2Fairflow-gta%3Futm_source=tldrdata/1/010001a1f382eb1c-813c2c29-0e67-4fcb-a679-689a5eec2cc8-000000/JUGqvaSbQQGa6IKnv-hMuL8mKYHk8PndJ_rs0pgFe74=452"
authors: ["vojay-dev"]
keywords: ["Apache Airflow", "Ollama", "LLM local", "orchestration", "Dag", "jeu vidéo"]
theme: "Data"
tone: "tutorial"
used_in: ["2026-11-20"]
---

## Résumé

« airflow-gta » est un projet démo créé par le développeur GitHub vojay-dev qui détourne Apache Airflow 3.4 pour faire jouer un Dag à Grand Theft Auto 2 dans le navigateur. Chaque mouvement de la voiture correspond à une itération d'une boucle de tâches Airflow, pilotée par un petit modèle de décision local (Ollama / `nimble`) qui choisit parmi huit actions possibles. Un « bridge » Python (FastAPI + Playwright) pilote le jeu via son API développeur, calcule les distances par l'algorithme de Dijkstra sur la carte du jeu, et un plugin React affiche en direct et en relecture le déroulé de la partie dans l'UI Airflow. L'objectif est de démontrer trois fonctionnalités récentes d'Airflow : les boucles de tâches, les tâches LLM à sortie typée (Common AI `@task.llm`) et les plugins d'UI personnalisés.

## Points clés

- Démonstration ludique mais technique des boucles de tâches Airflow 3.4 (`.loop()` + porte `LoopDecision`), où l'état du jeu est transmis d'une itération à l'autre.
- Utilisation d'une tâche `@task.llm` avec sortie Pydantic typée (`Drive`) pour contraindre un modèle local (Ollama, `nimble`) à choisir parmi huit mouvements possibles.
- Un « bridge » FastAPI/Playwright pilote un port navigateur de GTA2 en WebAssembly, lit le fichier de carte du jeu et calcule les trajets optimaux avec l'algorithme de Dijkstra.
- Un plugin d'UI Airflow (React) offre un tableau de bord « GTA2 Dashcam » avec relecture, carte de la ville, télémétrie et affichage du prompt envoyé au modèle.
- Projet entièrement local (Docker, Astro CLI, Ollama, Chrome), sans fichiers de jeu redistribués, pour des raisons de licence freeware non librement redistribuable.
- Mission de livraison personnalisée (hors missions natives du jeu) avec conditions de victoire/défaite claires : 3 livraisons, 3 voitures perdues, ou 300 mouvements.

## Analyse approfondie

**Un Dag Apache Airflow 3.4 qui joue à Grand Theft Auto 2.**

Chaque déplacement de la voiture correspond à une itération d'une boucle de tâches. Un petit modèle de décision local choisit le mouvement, et un plugin montre ce qui s'est passé, en direct, dans l'UI Airflow.

*L'onglet GTA2 Dashcam après une partie gagnée : 3 colis sur 3 livrés en 99 mouvements, aucune voiture perdue.*

Cette démo illustre les capacités des fonctionnalités Airflow suivantes :

- **Boucles de tâches** (`.loop(...)` avec une porte `LoopDecision`) : un mouvement de jeu par itération, l'état du jeu étant transmis d'une itération à l'autre.
- **Common AI `@task.llm`** avec un `output_type` Pydantic : le modèle ne peut répondre qu'avec un des huit mouvements possibles.
- **Plugins d'UI Airflow** (`react_apps` avec `destination: "dag_run"`) : un onglet « GTA2 Dashcam » sur chaque run, en direct et en relecture.

GTA2 a ses propres missions (cabines téléphoniques, jobs de gang). Ce projet ne les utilise pas. Il joue à la place une mission de livraison personnalisée, que le « bridge » (voir plus bas) met en place et dont il tient le score depuis l'extérieur :

1. Le jeu démarre normalement (« start play in area 1 », Downtown). Le bridge téléporte alors le joueur sur la route la plus longue et la plus droite du quartier.
2. **Obtenir une voiture :** le bridge fait apparaître une voiture près du joueur via l'API développeur du port navigateur. Le joueur y monte avec la touche Entrée du jeu et son animation habituelle, donc il n'y a pas de vol de voiture à proprement parler.
3. **Livrer trois colis :**
   - Chaque point de livraison est un pâté de maisons aléatoire situé entre 35 et 70 blocs par la route. Le paramètre `seed` du Dag détermine quel point est choisi.
   - Il apparaît comme un point de passage sur le radar. Ce marqueur appartient à la surcouche cartographique du port navigateur, qui ne fait pas partie du jeu original.
   - Les noms des colis (« le pager d'astreinte », « une clé USB intitulée 'prod_dump_final_v2' », etc.) ne sont que des éléments narratifs.
4. Chaque point de livraison est un pâté de maisons aléatoire situé entre 35 et 70 blocs par la route.
5. **Livré :** quand la voiture se trouve à moins de 2,5 blocs du point de livraison par la route, le bridge valide la livraison et verse +1000 $ au compteur d'argent du jeu. Il définit ensuite le point de livraison suivant.
6. **Voitures :** si le joueur se retrouve hors de la voiture ou meurt, cette voiture est perdue et le bridge en fait apparaître une nouvelle. Après trois voitures perdues, la partie se termine.
7. **Temps :** le Dag autorise au maximum 300 mouvements.

*Mouvement 79 : deuxième livraison. Le camion de glaces ne faisait pas partie du plan.*

**Conditions de fin :**

| Résultat | Quand |
|---|---|
| Gagné | 3 colis livrés |
| Perdu | 3 voitures perdues |
| Temps écoulé | 300 mouvements |

*Le Dag en vue Graph : le groupe `turn` a bouclé 99 fois sur un maximum de 300.*

**Un mouvement :**

1. **`decide` :** une tâche `@task.llm` reçoit un court texte issu de l'itération précédente. Ce texte indique le point de livraison, la direction dans laquelle la voiture est orientée, et ce que ferait chacun des huit mouvements. Le modèle répond avec un objet `Drive` : l'un de `forward`, `forward_left`, `forward_right`, `reverse`, `reverse_left`, `reverse_right`, `handbrake_left` ou `handbrake_right`.
2. **`drive` :** envoie le mouvement au bridge. Le bridge relance le jeu, maintient les touches correspondant à ce mouvement pendant 700 ms de temps de jeu, remet en pause, enregistre une capture d'écran et renvoie le nouvel état.
3. **`game_over` :** la porte de boucle. Elle renvoie `LoopDecision(stop=..., reason=...)`.

**D'où vient le texte :**

- Le bridge lit le fichier de carte de GTA2 (`wil.gmp`) sous forme d'une grille 256 × 256 au niveau de la rue (route, trottoir, terrain ou bloqué).
- Il calcule les distances par la route jusqu'au point de livraison avec l'algorithme de Dijkstra et simule chaque mouvement comme un arc sur la grille.
- Par exemple :
```
Le point de livraison est à 27 blocs par la route, à l'est. Vous êtes orienté vers l'est.
forward : dégagé, rapproche de 5 blocs du point de livraison.
forward_right : DANGER, percute un mur après 2,5 blocs, éloigne de 2 blocs du point de livraison.
```
- La carte ne montre pas les poteaux ni les voitures en stationnement. Un mouvement qui échoue simplement à déplacer la voiture reste donc classé DANGER jusqu'à ce que la voiture bouge à nouveau.

| Élément | Chemin | Notes |
|---|---|---|
| GTA2 dans le navigateur | `site/` | Le port préconstruit M1sterMo/gta2 : la décompilation `gta2_re` compilée en WebAssembly. Une ligne de `site/gamefiles.js` est modifiée pour charger l'installeur depuis le bridge plutôt que depuis Internet Archive. |
| Bridge | `bridge/bridge.py` | FastAPI et Playwright sur la machine hôte. Il exécute votre Chrome installé avec un profil persistant et pilote le jeu via l'API développeur du port (`?devdata`). Il gère aussi la mission. |
| Lecteur de carte | `bridge/gmp.py` | Lit le chunk DMAP d'un fichier `.gmp` de GTA2. |
| Anticipation (Lookahead) | `bridge/driver.py` | Distances par la route, simulation des mouvements et texte destiné au modèle. |
| Dag | `airflow/dags/airflow_plays_gta2.py` | Boucle `insert_coin` → `turn` (`decide`, `drive`, `game_over`) → `high_score` |
| Client du bridge | `airflow/include/gta2/bridge.py` | Client HTTP de la bibliothèque standard |
| Plugin GTA2 Dashcam | `airflow/plugins/` | Application React présente sur chaque run d'un Dag taggé `gta2` |
| Flux terminal | `scripts/feed.py` | Une ligne par mouvement, lue depuis les XCom du run |
| Vérification du bridge | `scripts/play_test.py` | Un joueur scripté effectue 60 mouvements, sans Airflow |

Ouvrez un run, puis l'onglet **GTA2 Dashcam**.

*Mouvement 30 : cinq mouvements provoqueraient un accident (💥). Le modèle choisit le `forward` qui brille, et qui rapproche de 4 blocs.* / *La carte de la ville : une couleur de trace par livraison, ✓ pour chaque point de livraison.*

- **Dashcam :** la capture d'écran du jeu pour chaque mouvement, avec le mouvement, les blocs restants et des bannières d'événements.
- **Volant :** les huit mouvements autour de la voiture, colorés selon l'anticipation. Vert rapproche, rouge 💥 provoque un accident, gris éloigne. Le mouvement choisi par le modèle brille.
- **Carte de la ville :** la grille des routes, la trace par livraison, les points de livraison effectués et en cours, et la voiture avec son orientation.
- **Télémétrie :** mouvement, colis, voitures, blocs restants, une sparkline de distance de route et la fréquence de sélection de chaque mouvement.
- **Le prompt :** le texte exact reçu par le modèle pour ce mouvement.
- **Contrôles :** mode direct pendant qu'un run est en cours, relecture avec un curseur temporel après coup.

*Mode direct pendant un run : l'onglet suit la dernière itération de la boucle.*

Les données du run proviennent des XCom (`insert_coin`, et `turn.drive` pour chaque itération) via l'API REST d'Airflow. Les captures d'écran et la grille des routes proviennent du bridge à l'adresse `http://127.0.0.1:8765`, donc l'onglet fonctionne dans un navigateur sur la machine qui exécute le bridge.

**Prérequis :**

- macOS ou Linux, avec Docker (Docker Desktop ou Rancher Desktop) et l'Astro CLI
- Ollama 0.35 ou plus récent, pour son API de décisions (`/v1/systemone`)
- uv, Python 3, et Google Chrome
- Les données du jeu GTA2 (voir plus bas)
- Environ 1 Go d'espace disque pour les données du jeu et le cache du navigateur, plus l'image Airflow

Développé et testé sur macOS (Apple Silicon) avec Chrome 157, Astro Runtime `runtime-dev:3.4-1-alpha8` et Ollama 0.40.

Le port navigateur nécessite l'installeur freeware original de GTA2, `GTA2INSTALLER.exe`. Il doit être placé dans `game-data/`.

- Rockstar a publié GTA2 en freeware en 2004, mais ne le propose plus au téléchargement.
- Le port navigateur original télécharge l'installeur depuis l'item `gta2_rockstar-classics` d'Internet Archive. `make game-data` télécharge le même fichier et vérifie sa taille. Cet item a été mis en ligne par un utilisateur privé, et sa provenance ne peut pas être vérifiée.
- Si vous possédez votre propre copie, placez-la à `game-data/GTA2INSTALLER.exe`.
- GTA2 est freeware mais n'est pas librement redistribuable. Ce dépôt ne contient aucun fichier du jeu. Gardez `game-data/`, `.chrome-profile/` et `frames/` en local. Ils sont dans le .gitignore, et l'image Airflow ne les contient jamais, car `airflow/` est son propre contexte de build Docker.

```
make game-data   # une seule fois
make start       # Ollama + modèle, le bridge (ouvre une fenêtre Chrome), Airflow
make trigger     # démarre un run ; make trigger SEED=11 pour d'autres points de livraison
make stop
```

1. Observez la fenêtre Chrome : c'est le jeu.
2. Dans l'UI Airflow à l'adresse http://localhost:8080/dags/airflow_plays_gta2 (admin / admin), ouvrez le run puis son onglet **GTA2 Dashcam**.
3. Utilisez `localhost:8080`, pas l'URL du proxy affichée par `astro dev start` ; le proxy bloque les bundles de plugins.

Le premier démarrage décompresse l'installeur dans le navigateur, ce qui prend environ une minute. Ensuite, le jeu est mis en cache dans `.chrome-profile/`, et une partie démarre en environ 15 secondes.

Une partie prend environ 80 à 110 mouvements, à raison d'environ 5 secondes par mouvement. La majeure partie de ce temps est due à l'ordonnancement des tâches ; une décision prend moins d'une seconde sur un ordinateur portable M-series.

| Cible | Ce qu'elle fait |
|---|---|
| `make` / `make help` | Liste les cibles |
| `make start` | Ollama + modèle, bridge + Chrome, Airflow |
| `make stop` | Airflow, le bridge et son Chrome, et Ollama si `make start` l'a démarré |
| `make status` | Ce qui est en cours d'exécution |
| `make trigger` | Démarre un run (`SEED=`, 7 par défaut) |
| `make feed` | Une ligne par mouvement du dernier run, en direct |
| `make bridge` / `make bridge-stop` | Seulement le bridge. L'arrêt force l'arrêt s'il est bloqué |
| `make play-test` | Vérifie le bridge avec un joueur scripté, sans Airflow |
| `make logs` | Suit le journal du bridge |
| `make game-data` | Télécharge l'installeur et vérifie sa taille |
| `make clean-frames` | Supprime les captures d'écran enregistrées |

`airflow/.env` contient la configuration côté Airflow et ne contient aucun secret. `make start` le crée à partir de `airflow/.env.example` au premier lancement.

| Paramètre | Où | Valeur par défaut |
|---|---|---|
| Modèle de décision | `MODEL` dans le `Makefile`, et `extra.model` de `AIRFLOW_CONN_OLLAMA_DECISIONS` dans `airflow/.env` | `nimble` (`system-one:nimble`) |
| URL du bridge pour Airflow | `GTA2_BRIDGE_URL` dans `airflow/.env` | `http://host.docker.internal:8765` |
| Port du bridge | variable d'environnement `BRIDGE_PORT` | `8765` |
| Afficher la barre d'outils du port | `SHOW_TOOLS=1` au démarrage du bridge | masquée |
| Livraisons pour gagner, voitures, distance d'arrivée, modèle de voiture, durée d'un mouvement | constantes en haut de `bridge/bridge.py` | 3, 3, 2,5 blocs, modèle 10, 700 ms |
| Distance du point de livraison | `pick_target(near, far)` dans `bridge/driver.py` | 35 à 70 blocs |
| Mouvements maximum | `MAX_MOVES` dans le Dag | 300 |
| Points de livraison | paramètre `seed` du Dag | 7 |

La connexion au modèle utilise le type de connexion `pydanticai` du fournisseur Common AI. D'autres modèles pris en charge par cette connexion devraient fonctionner tant qu'ils renvoient le type de sortie `Drive`, mais seul `nimble` a été testé.

| Endpoint | Ce qu'il fait |
|---|---|
| `POST /api/start` `{"seed": 7}` | Nouvelle page, démarrage du jeu, voiture, premier point de livraison. Renvoie l'état du jeu |
| `POST /api/act` `{"action": "forward", "ms": 700}` | Un mouvement. Renvoie le nouvel état, incluant `look` (le texte pour le modèle) et `options` |
| `GET /api/state` | L'état actuel |
| `GET /api/actions` | Les mouvements disponibles |
| `GET /api/grid/{level}` | La grille des routes (256 chaînes de 256 caractères) |
| `POST /api/eval` `{"js": "..."}` | Debug uniquement : exécute une fonction JavaScript dans la page du jeu |

Le bridge n'est accessible que sur 127.0.0.1.

**Coordonnées :**

- Les blocs de la carte vont de 0 à 255. `x` augmente vers l'est et `y` augmente vers le sud.
- `rot` va de 0 à 1440 pour un cercle complet : 0 fait face au sud, 360 à l'est, 720 au nord, 1080 à l'ouest.

**Crédits :**

- **GTA2** est © Rockstar Games / Take-Two Interactive. Il s'agit d'un projet non officiel et non commercial, qui n'est ni affilié ni approuvé par eux. Aucun fichier du jeu n'est inclus.
- **Le port navigateur :** M1sterMo/gta2 et gta2-browser, sous licence MIT pour leur propre code. Il est vendored dans `site/`.
- **Le moteur :** la décompilation `gta2_re` par les contributeurs de CriminalRETeam. Leurs conditions s'appliquent.
- **Construit avec :** Apache Airflow, l'Astro CLI, Ollama, Playwright et FastAPI.

## Pourquoi ça compte

Ce projet est un exemple concret et pédagogique d'intégration d'un LLM local dans un pipeline d'orchestration de données (Airflow), au-delà des cas d'usage data classiques : il illustre de façon ludique les boucles de tâches, les sorties structurées de type LLM et les plugins UI personnalisés, utile pour quiconque suit l'évolution d'Airflow vers des workflows plus dynamiques et agentiques.
