---
title: "GitHub - ucbepic/DataAgentBench: Benchmark for data agents"
date: 2026-10-24
url: "https://substack.com/redirect/dfbaa0de-4813-48f9-8598-60cf363edf26?j=eyJ1IjoiN3Y1bG1jIn0.HlvPOGYPdVknSYzEK1JIj6IFkAFn8zuyjtfU9Mbft9Q"
authors: ["Ruiying Ma", "Shreya Shankar", "Ruiqi Chen", "Yiming Lin", "Sepanta Zeighami", "Rajoshi Ghosh", "Abhinav Gupta", "Anushrut Gupta", "Tanmai Gopal", "Aditya G. Parameswaran"]
keywords: ["benchmark", "agents de données", "leaderboard", "SQL multi-bases", "UC Berkeley", "LLM"]
theme: "Data"
tone: "research"
used_in: ["2026-10-24"]
---

## Résumé

DataAgentBench (DAB) est un benchmark développé conjointement par UC Berkeley et Hasura PromptQL pour évaluer des agents de données sur des tâches réalistes et complexes, orientées données d'entreprise. Il couvre quatre dimensions clés — intégration multi-bases, jointures de clés mal formées, transformation de texte non structuré et connaissance du domaine — sur 12 jeux de données, 54 requêtes, 9 domaines et 4 SGBD (PostgreSQL, MongoDB, SQLite, DuckDB). Un leaderboard public, alimenté par des soumissions communautaires via Pull Request, classe les agents selon leur score Pass@1 moyenné sur 5 exécutions ; les meilleurs agents actuels (Datasage, Camber v2) dépassent 95 %, tandis que des modèles nus comme Gemini-2.5-Flash ou Kimi-K2 plafonnent sous les 30 %. Le dépôt fournit également toute l'infrastructure nécessaire (agent de référence, environnement Docker sécurisé, scripts de validation) pour exécuter et soumettre ses propres résultats.

## Points clés

- DAB est présenté comme le premier benchmark pour agents de données sur des tâches d'entreprise réalistes, par opposition aux benchmarks SQL ou mono-base existants.
- Quatre propriétés testées : intégration multi-bases, jointures de clés mal formées, transformation de texte non structuré, connaissance du domaine.
- Couverture : 12 jeux de données, 54 requêtes, 9 domaines, 4 SGBD (PostgreSQL, MongoDB, SQLite, DuckDB).
- Leaderboard public et ouvert aux contributions via Pull Request, classé par Pass@1 (moyenne de 5 essais), avec des options "prompt ajusté" et "indices".
- Les agents en tête combinent des LLM de pointe (GLM-5.3, Claude-Opus-5) avec des outils spécifiques aux tâches (résolution floue d'entités, filtres d'horaires, outils de conformité).
- Infrastructure complète fournie : agent de référence (`DataAgent.py`), sandbox Docker pour l'exécution Python, scripts d'agrégation de précision et de validation des réponses.

## Analyse approfondie

🌐 **Site web & Leaderboard : ucbepic.github.io/DataAgentBench**

📄 **Article : arxiv.org/abs/2603.20576**

🔥 **DAB est le premier benchmark pour évaluer les agents de données sur des tâches réalistes et complexes, orientées données. C'est un effort collaboratif entre UC Berkeley et Hasura PromptQL.**

🤝 **Nous accueillons les contributions au leaderboard ! Soumettez une Pull Request en suivant les instructions ci-dessous pour partager les résultats de votre agent et les voir classés sur DAB.**

DAB capture **quatre propriétés essentielles** des charges de travail de données d'entreprise réelles, à travers différents secteurs :

- **Intégration multi-bases de données**
- **Jointures de clés mal formées**
- **Transformation de texte non structuré**
- **Connaissance du domaine**

Contrairement aux benchmarks précédents limités au SQL ou à une seule base de données, DAB soumet les agents à une **complexité de données d'entreprise réaliste**.

**Prompt ajusté** ✓ = le prompt initial est spécifique à DAB, construit à partir d'une étude approfondie des conventions de tâches de DAB (règles du domaine, choix d'analyse et d'interprétation, et formats de réponse attendus).

**Indices** ✓ = utilisation de `db_description_withhint.txt`.

| Rang | Modèle | Prompt ajusté | Pass@1 ¹ | Essais | Indices | Date | Soumission |
|---|---|---|---|---|---|---|---|
| 1 | Datasage (GLM-5.3 + Jev-1.13.0) ⁸ | ✓ | 0,9628 | 5 | ✓ | 2026-10-01 | #115 |
| 2 | Camber v2 (Claude-Opus-5, effort élevé) | ✓ | 0,9542 | 5 | ✓ | 2026-09-22 | #111 |
| 3 | Permute EQ (Claude-Opus-5) | ✓ | 0,9467 | 5 | ✓ | 2026-09-11 | #95 |
| 4 | Scout (OceanBase Lab) (GLM-5.2) | ✓ | 0,9062 | 5 | ✓ | 2026-09-08 | #96 |
| 5 | Camber (Claude-Opus-5, effort élevé) | ✓ | 0,8790 | 5 | ✓ | 2026-08-27 | #92 |
| 6 | DVIndex (GPT-6-Astra, effort élevé + Jev-1.13.0) | ✓ | 0,8768 | 5 | ✓ | 2026-09-23 | #113 |
| 7 | Phoenix-CLI (Claude-Opus-5.5) | | 0,8621 | 5 | ✓ | 2026-09-26 | #114 |
| 8 | Sentinel (Actioneer) (Fable-5 + Claude-Opus-4.7) | ✓ | 0,8617 | 5 | ✓ | 2026-07-20 | #73 |
| 9 | Permute Core (Claude-Opus-5) | ✓ | 0,8413 | 5 | ✓ | 2026-08-05 | #85 |
| 10 | Alkera (Fable-5 + Claude-Opus-4.8) | ✓ | 0,8411 | 5 | ✓ | 2026-07-14 | #70 |
| 11 | Sarvam Code v0.36 (GLM-5.2) | ✓ | 0,8208 | 5 | ✓ | 2026-07-28 | #75 |
| 12 | DataTrail v1 (Muse-Spark-1.3, effort moyen) | ✓ | 0,8201 | 5 | ✓ | 2026-09-13 | #104 |
| 13 | SCRIBE (Actioneer) (Claude-Opus-4.7) | ✓ | 0,8185 | 5 | ✓ | 2026-06-26 | #67 |
| 14 | Stela (DeepSeek-V4.1-Flash, effort maximal) | ✓ | 0,8114 | 5 | ✓ | 2026-09-13 | #103 |
| 15 | Alkera (Claude-Opus-4.8) | ✓ | 0,8044 | 5 | ✓ | 2026-07-15 | #69 |
| 16 | LabRat (Claude-Opus-5 + Cartographer) ⁶ | ✓ | 0,8018 | 5 | ✓ | 2026-08-03 | #84 |
| 17 | DataGallery (Qwen3.8-Max) | | 0,7932 | 5 | ✓ | 2026-10-12 | #120 |
| 18 | Spacedock (Recce) (GPT-5.5) | | 0,7850 | 5 | ✓ | 2026-06-23 | #63 |
| 19 | DG (GLM-5.3) ⁷ | ✓ | 0,7828 | 5 | ✓ | 2026-09-19 | #108 |
| 20 | Sarvam Code v0.35 (GLM-5.2) | ✓ | 0,7812 | 5 | ✓ | 2026-07-27 | #74 |
| 21 | LabRat (GPT-5.6-Luna-Max + Cartographer) | | 0,7751 | 5 | ✓ | 2026-07-16 | #72 |
| 22 | Altimate Code (GPT-5.5 + Claude Sonnet 4.6) | | 0,7588 | 5 | ✓ | 2026-06-01 | #53 |
| 23 | Phoenix-CLI (Claude-Opus-5) | | 0,7556 | 5 | ✓ | 2026-09-04 | #94 |
| 24 | AgenDA (Claude-Opus-4.8) | | 0,7244 | 5 | ✓ | 2026-07-10 | #68 |
| 25 | Qwen3.8-Flash-Next | | 0,7087 | 5 | ✓ | 2026-09-12 | #99 |
| 26 | fabric-rlm (GPT-5.6-Luna-Max) ⁵ | | 0,6956 | 5 | ✓ | 2026-07-31 | #76 |
| 27 | Altimate Code (Claude-Sonnet-4.6) | | 0,6822 | 5 | ✓ | 2026-05-10 | #44 |
| 28 | Spacedock (Recce) (Claude-Opus-4.8) | | 0,6804 | 5 | ✓ | 2026-06-08 | #55 |
| 29 | MinusX (Claude Sonnet 4.6 + GPT5.5-mini + Claude Haiku 4.5) | | 0,6601 | 5 | ✓ | 2026-05-21 | #50 |
| 30 | DataBridge (GLM-5.2) | ✓ | 0,6137 | 6 | ✓ | 2026-06-22 | #61 |
| 31 | Pi Coding Agent (Claude-Opus-4.6) | | 0,6103 | 5 | ✓ | 2026-04-21 | #31 |
| 32 | LabRat (Claude-Sonnet-4.6 + Cartographer) | | 0,6088 | 5 | ✓ | 2026-06-24 | #65 |
| 33 | PromptQL (Gemini-3.1-Pro) | | 0,6000 | 5 | ✓ | 2026-03-18 | #24 |
| 34 | PromptQL (Claude-Opus-4.6) | | 0,5933 | 5 | ✓ | 2026-03-02 | #23 |
| 35 | Spacedock (Recce) (Claude-Opus-4.6) | | 0,5828 | 5 | | 2026-05-08 | #47 |
| 36 | Claude-Opus-4.6 | | 0,5551 | 5 | ✓ | 2026-03-18 | #22 |
| 37 | LabRat (Claude-Sonnet-4.6) ² | | 0,5138 | 5 | | 2026-06-01 | #54 |
| 38 | Oracle Forge — Team PaLM (Gemini-3.1-Pro-Preview) ³ | | 0,4721 | 5 | ✓ | 2026-05-10 | #37 |
| 39 | Gemini-3-Pro | | 0,4663 | 50 | ✓ | 2026-03-02 | — |
| 40 | nQuery (gpt-oss-safeguard-120b) NGENUX SOLUTIONS PVT LTD | | 0,4547 | 5 | ✓ | 2026-07-02 | #56 |
| 41 | Oracle Forge — Tenacious Intelligence (Claude-Sonnet-4.6) ⁴ | | 0,4464 | 5–7 | | 2026-04-21 | #32 |
| 42 | GPT-5-mini | | 0,3663 | 50 | ✓ | 2026-03-02 | — |
| 43 | GPT-5.2 | | 0,2991 | 50 | ✓ | 2026-03-02 | — |
| 44 | Kimi-K2 | | 0,2925 | 50 | ✓ | 2026-03-02 | — |
| 45 | Oracle Forge — Team Cohere (Gemini-2.0-Flash) | | 0,1671 | 5 | ✓ | 2026-04-21 | #38 |
| 46 | Gemini-2.5-Flash | | 0,1049 | 50 | ✓ | 2026-03-02 | — |

**¹ Méthodologie.** La requête 1 de DEPS_DEV_V1 a été réévaluée le 2026-08-18 en relançant son `validate.py` contre un validateur révisé (acceptant n'importe lequel des 95 paquets ex-aequo à la cinquième place avec 57779 étoiles, plutôt que le seul paquet ex-aequo enregistré dans `ground_truth.csv`, voir l'issue #86), à partir des mêmes JSON de soumission, sans autre changement de requête. Tous les scores Pass@1 ont été recalculés le 2026-06-12 en relançant le `validate.py` de chaque requête contre les validateurs actuels (y compris les vérités terrain PATENTS régénérées), à partir des JSON de soumission stockés dans ce dépôt (`submissions/`, `leaderboard_submissions/`) ou dans les branches PR de soumission correspondantes (`refs/pull/<N>/head`). Pass@1 est la moyenne, sur l'ensemble des jeux de données, du taux de réussite moyen par requête de chaque jeu de données.

**²** LabRat (#54) comptait 21 essais contaminés comptabilisés comme échecs.

**³** Team PaLM (#37) couvre 49 des 54 requêtes (les requêtes manquantes sont notées 0).

**⁴** Tenacious Intelligence (#32) a 5 à 7 essais par requête (dénominateurs par requête utilisés).

**⁵** fabric-rlm (#76) comptait 8 essais agnews comptabilisés comme échecs : 4 ont chargé des étiquettes de référence externes, et 4 ont soumis la valeur de référence sans dérivation dans les traces fournies.

**⁶** LabRat (#84) manque 2 des 270 essais (requête 4 d'agnews, délais d'infrastructure dépassés), comptabilisés comme échecs ; en les excluant, le score serait de 0,8102.

**⁷** DG (#108) utilise des indices dérivés par les auteurs. Pour la requête 1 de GITHUB_REPOS, l'indice fixe le dénominateur : « 4 lignes README au total ; ... ne jamais utiliser de comptages basés sur contents.sample_path », ce qui fait que l'agent compte les 3 fichiers README donnant la référence 1/3 plutôt que la centaine qu'il trouverait autrement. Pour la requête 1 de PANCANCER_ATLAS, l'indice fixe la clé de réponse : « les lignes de sortie sont indexées par le code ICD-O », ce qui fait que l'agent rapporte des codes d'histologie (9382/3) comme la référence l'exige, plutôt que des noms (Astrocytome), ce que la question seule ne précise pas.

**⁸** Datasage (#115) fournit à l'agent des outils spécifiques à la tâche, par exemple un assistant de moyenne mobile exponentielle qui renvoie l'année du premier pic (requêtes 1 et 2 de PATENTS), un filtre d'horaires d'ouverture (requête 3 de googlelocal), un outil de décision de conformité aux politiques (requêtes 2, 6 et 7 de crmarenapro) et un outil de résolution floue d'entités (music_brainz_20k).

Pour contribuer les résultats de votre agent au leaderboard DAB :

1. Collectez les résultats de **5 exécutions** sur **toutes les requêtes** à travers **tous les jeux de données**.
2. Organisez tous vos résultats d'exécution dans un **unique** fichier JSON suivant cette structure :
```
[
  {
    "dataset": "<dataset_name>",   // ex. : "bookreview"
    "query": "<query_id>",         // ex. : "1"
    "run": "<run_number>",         // 0–4 pour 5 exécutions
    "answer": "<agent_generated_answer>"
  },
  ...
  // Inclure une entrée pour chaque exécution de chaque requête de tous les jeux de données
]
```
3. Soumettez une **Pull Request** à ce dépôt incluant :
   - Le fichier JSON de résultats
   - Les **traces d'exécution** de vos exécutions (les journaux/transcriptions étape par étape de l'agent), afin que les résultats puissent être vérifiés indépendamment
   - Une brève description de la configuration de votre agent, incluant :
     - Le nom de votre agent
     - Le(s) nom(s) et la version du ou des modèle(s) LLM de base
     - Si des indices de jeu de données ont été utilisés
     - Toute note additionnelle ou configuration particulière à souligner
4. Nous validerons chaque soumission — voir SUBMISSION_RUBRIC.md, que nous recommandons de vérifier localement pendant vos exécutions.

Ce benchmark contient **12** jeux de données et **54** requêtes à travers **9** domaines et **4** SGBD :

| Jeu de données | #BDD | SGBD | #Tables | #Requêtes |
|---|---|---|---|---|
| agnews | 2 | MongoDB, SQLite | 3 | 4 |
| bookreview | 2 | PostgreSQL, SQLite | 2 | 3 |
| crmarenapro | 6 | DuckDB, PostgreSQL, SQLite | 27 | 13 |
| deps_dev_v1 | 2 | DuckDB, SQLite | 3 | 2 |
| github_repos | 2 | DuckDB, SQLite | 6 | 4 |
| googlelocal | 2 | PostgreSQL, SQLite | 2 | 4 |
| music_brainz_20k | 2 | DuckDB, SQLite | 2 | 3 |
| pancancer_atlas | 2 | DuckDB, PostgreSQL | 3 | 3 |
| patents | 2 | PostgreSQL, SQLite | 2 | 3 |
| stockindex | 2 | DuckDB, SQLite | 2 | 3 |
| stockmarket | 2 | DuckDB, SQLite | 2754 | 5 |
| yelp | 2 | DuckDB, MongoDB | 5 | 7 |

Avant d'exécuter DAB, veuillez terminer les étapes de configuration suivantes.

De nombreux jeux de données de DAB contiennent des fichiers de base de données volumineux dépassant 50 Mo et sont suivis avec Git LFS. Si vous voulez que ces fichiers soient téléchargés dès le clonage, activez Git LFS **avant** de cloner :

`git lfs install`

Puis clonez et exécutez le script de téléchargement :
```
git clone https://github.com/ucbepic/DataAgentBench.git
cd DataAgentBench
bash download.sh
```
`download.sh` a deux objectifs :

- **Télécharger les gros jeux de données qui ne sont pas sur GitHub.** La base de données `PATENTS` d'environ 5 Go (`patent_publication.db`) est trop volumineuse pour le dépôt ; elle est donc récupérée depuis le miroir Hugging Face.
- **Réparer les pulls Git LFS échoués.** Si Git LFS n'a pas été activé avant le clonage ou a rencontré une erreur, certains fichiers suivis se retrouvent manquants ou sous forme de pointeurs. Le script vérifie chaque fichier listé dans `dataset_manifest.tsv` par rapport à son sha256 et retélécharge toute discordance depuis le miroir du Hugging Face Hub.

Les fichiers déjà corrects ne sont pas modifiés.

Nous recommandons d'utiliser un environnement virtuel dédié pour garantir la reproductibilité.

**Avec Conda (recommandé) :**
```
sudo apt-get install libpq-dev
conda env create -f environment.yaml
conda activate dabench
```
Ceci installera toutes les dépendances requises spécifiées dans environment.yaml.

- **Installer Docker.** Suivez le guide officiel. Version utilisée dans nos expériences : **28.4.0**
- **Construire l'image Docker :** l'image inclut **Python 3.12**, **pandas** et **PyArrow** préinstallés : `docker build -t python-data:3.12 .`

DAB évalue les agents sur plusieurs systèmes de bases de données ; vous devez donc installer et configurer les bases de données suivantes localement.

- **PostgreSQL** : installez PostgreSQL depuis le site officiel et démarrez le serveur.
  - **Version minimale requise** : 17.5
  - Version utilisée dans nos expériences : 17.7 (Ubuntu 17.7-3.pgdg24.04+1)
- **MongoDB** : installez MongoDB Community Edition depuis le site officiel et démarrez le serveur.
  - Version utilisée dans nos expériences : v8.2.1
- **SQLite & DuckDB** : ils opèrent directement sur des fichiers de base de données et ne nécessitent pas de serveur en cours d'exécution.

Après avoir installé toutes les bases de données, vous devez configurer les paramètres de connexion pour correspondre à votre installation locale.

Valeurs de configuration par défaut (définies dans db_config.py) :

| **Paramètre** | **Valeur par défaut** |
|---|---|
| PG_CLIENT | "psql" |
| PG_HOST | "127.0.0.1" |
| PG_PORT | 5432 |
| PG_USER | "postgres" |
| PG_PASSWORD | "" |
| PG_DB | "test" |
| MONGO_URI | "mongodb://localhost:27017/" |
| SQLITE_PATH | "data/mydb.sqlite" |
| DUCKDB_PATH | "data/mydb.duckdb" |

**Option 1** : Créez un fichier `.env` à la racine du projet. Par ex. :
```
# PostgreSQL
PG_PASSWORD=your_password
PG_DB=mydb
# MongoDB (si authentification requise)
MONGO_URI=mongodb://username:password@localhost:27017/?authSource=admin
```
**Option 2** : Modifiez les valeurs par défaut dans db_config.py.

Créez un fichier `.env` à la racine du projet et ajoutez vos clés API :
```
AZURE_API_BASE=
AZURE_API_KEY=
AZURE_API_VERSION=
GEMINI_API_KEY=
TOGETHER_API_KEY=
```
Actuellement, nous prenons en charge :

- l'API Microsoft Azure (pour les modèles GPT)
- l'API Google Gemini (pour les modèles Gemini)
- l'API Together.AI (pour les modèles Kimi)

Si vous souhaitez utiliser un modèle non pris en charge par défaut, vous pouvez l'enregistrer dans DataAgent.py :
```
# DataAgent.py (à partir de la ligne 76)
if "gpt" in deployment_name.lower():
      self.client = AzureOpenAI(
          api_key=os.getenv("AZURE_API_KEY"),
          api_version=os.getenv("AZURE_API_VERSION"),
          azure_endpoint=os.getenv("AZURE_API_BASE")
      )
  # ajoutez un nouveau modèle ici comme branche `elif`
  else:
      raise ValueError(f"Unsupported deployment name: {deployment_name}")
```
et un prompt personnalisé pour s'adapter au format d'ID d'appel d'outil de votre modèle dans prompt_builder.py.

DAB fournit un agent intégré. Vous pouvez l'exécuter sur une requête spécifique comme suit :

**Exemple :** exécuter un seul essai de GPT-5-mini sur `query1` du jeu de données `bookreview`, avec jusqu'à 100 itérations d'agent et les indices de jeu de données activés :
```
python run_agent.py \
    --dataset bookreview \
    --query_id 1 \
    --llm gpt-5-mini \
    --iterations 100 \
    --use_hints \
    --root_name run_0
```
Les journaux de cette exécution seront enregistrés sous :
```
query_bookreview/query1/logs/data_agent/run_0
```
Le répertoire de journaux a la structure suivante :
```
run_0/
├─ exec_tool_work_dir/     <- Répertoire de travail pour l'outil `execute_python` (Docker)
├─ final_agent.json        <- Trajectoire complète de l'agent et statistiques d'exécution
├─ llm_calls.jsonl         <- Tous les appels API LLM effectués par l'agent
└─ tool_calls.jsonl        <- Tous les appels d'outils effectués par l'agent
```
DAB fournit des utilitaires pour calculer à la fois la **précision Pass@1 agrégée d'un jeu de données** et la **correction d'une seule exécution**.

Nous fournissons un script `avg_accuracy.py` pour calculer la **précision Pass@1** sur **50 exécutions par requête** d'un jeu de données.

Avant d'exécuter le script, assurez-vous que vos journaux d'exécution sont organisés sous la structure de répertoire suivante (vous devrez peut-être d'abord les déplacer du dossier du jeu de données vers le répertoire `results-<model_name>/`) :
```
results-gpt-5-mini/
└─ query_bookreview/
   └─ query1/
      └─ data_agent/
         ├─ run_0/
         ├─ run_1/
         ├─ ...
         └─ run_49/
```
Calculez ensuite Pass@1 comme suit :
```
from python_script.avg_accuracy import avg_acc
print(avg_acc("bookreview", "gpt-5-mini"))
```
Ceci agrégera les résultats de validation sur toutes les exécutions et requêtes et rapportera la précision Pass@1 finale pour le jeu de données.

Une fois qu'une exécution d'agent est terminée, vous pouvez valider sa réponse finale par rapport à la vérité terrain :
```
from pathlib import Path
import json
run_dir = Path("query_bookreview/query1/logs/data_agent/run_0")
with open(run_dir / "final_agent.json", encoding="utf-8") as f:
    llm_json = json.load(f)
llm_answer = llm_json["final_result"]
term_reason = llm_json["terminate_reason"]
if term_reason == "no_tool_call":
    validation_result = {"is_valid": False}
else:
    validation_result = validate(query_dir, llm_answer, term_reason)
```
Le résultat de validation suit cette structure :
```
{
  "timestamp": "YYYYMMDD_HHMMSS",
  "query_name": "query1",
  "is_valid": True/False,   # Si la réponse de l'agent correspond à la vérité terrain
  "reason": "...",          # Explication du succès ou de l'échec
  "ground_truth": "...",    # La réponse de référence
  "llm_answer": "...",      # La réponse finale de l'agent
}
```
Un jeu de données dans DAB est organisé comme un dossier à la racine du projet. Par exemple, pour le jeu de données `bookreview` :
```
query_bookreview/
├─ query_dataset/                  <- Tous les fichiers de base de données
│  ├─ books_info.sql
│  └─ review_query.db
├─ query1/                         <- Chaque requête stockée dans un dossier séparé
├─ db_config.yaml                   <- Configuration de connexion à la base de données
├─ db_description.txt               <- Description des schémas de base de données
└─ db_description_with_hint.txt     <- Indices optionnels pour les requêtes
```
Chaque requête est stockée dans son dossier de jeu de données correspondant :
```
query_1/
├─ query.json           <- La requête sous forme de chaîne entre guillemets doubles
├─ ground_truth.csv     <- La réponse de référence en texte brut
└─ validate.py          <- Script Python pour valider la sortie d'un agent
```
`validate.py` définit une fonction `validate` avec la signature suivante :
```
def validate(llm_output: str):
    """
    Valide si la vérité terrain est présente dans la réponse de l'agent.
    Renvoie :
        (True, "OK")   – si la réponse correspond à la vérité terrain
        (False, reason) – si elle ne correspond pas
    """
```
DAB vous permet d'**implémenter et d'exécuter vos propres agents** tout en exploitant des outils intégrés pour l'interrogation de bases de données et l'exécution Python. Ces utilitaires, situés sous `tools/`, fournissent :

- **🔗 Connexion automatique à la base de données**
  - Charge les configurations de base de données depuis `db_config.yaml` pour chaque jeu de données.
  - Pas besoin de se connecter manuellement à PostgreSQL, MySQL, MongoDB, SQLite ou DuckDB — toutes les connexions sont gérées automatiquement via `db_utils`.
- **🛡️ Interrogation de base de données en lecture seule**
  - Garantit que les requêtes sont en lecture seule, évitant les écritures accidentelles qui pourraient polluer les données.
- **🐳 Environnement d'exécution Python sécurisé**
  - Exécute du code Python avec un délai d'expiration de 600 secondes dans un environnement Docker avec Python 3.12, `pandas` et `pyarrow` préinstallés.
  - Protège votre machine locale des opérations non sécurisées de l'agent.
- **📄 Implémentation de référence de l'agent**
  - `DataAgent.py` est un agent intégré pleinement fonctionnel.
  - Utilisez-le comme modèle pour implémenter et tester votre propre agent.

Si vous utilisez DAB dans vos recherches, veuillez citer notre article :
```
@article{ma2026can,
  title={Can AI Agents Answer Your Data Questions? A Benchmark for Data Agents},
  author={Ma, Ruiying and Shankar, Shreya and Chen, Ruiqi and Lin, Yiming and Zeighami, Sepanta and Ghosh, Rajoshi and Gupta, Abhinav and Gupta, Anushrut and Gopal, Tanmai and Parameswaran, Aditya G},
  journal={arXiv preprint arXiv:2603.20576},
  year={2026}
}
```

## Pourquoi ça compte

DAB fixe une référence commune et exigeante pour mesurer la maturité réelle des agents de données face à des scénarios d'entreprise (bases hétérogènes, données mal structurées), un signal utile pour suivre la course entre labos et startups sur les agents LLM appliqués aux données.
