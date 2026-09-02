---
title: "GitHub - volcengine/OpenViking: Self-evolving Context Database for AI Agents. Unify Agent Memory, Knowledge RAG and Skills."
date: 2026-09-02
url: "https://link.mail.beehiiv.com/ss/c/u001._d02Us3GR26SqbxiB_QNfVkmm2nD-5OvrFhY5asx5Z-Oud7n5DzMGJOEPnoQZviLg6pHGReSl2vGZAegfjl5R5NtkUgA0vPFl3faqSzb5LmWOXyZ0c4l61t7_V4LPksAp0YXvBEaLhbsrpYvM9ji7MaVKrlQrVl58vGCUpW8uBM/4to/J86wL3ZyRZKrMW8TS6n3xA/h21/h001.V6LcFacveYqnVX-MsVSsC95y0LJ1ixAkX8LckHvxKg0"
authors: ["Jiajie Fu", "Junwen Chen", "Mengzhao Wang", "Aoxiang He", "Maojia Sheng", "Xiangyu Ke", "Yifan Zhu", "Yunjun Gao"]
keywords: ["mémoire agent", "RAG", "base de contexte", "open-source", "protocole viking"]
theme: "IA"
tone: "news"
used_in: ["2026-09-02"]
---

## Résumé
OpenViking est une base de contexte open-source pour agents IA qui unifie mémoire, ressources documentaires (RAG) et compétences dans un unique système de fichiers virtuel adressé par le protocole `viking://`. Le contenu y est traité en trois niveaux de chargement — résumé, aperçu, détails — chargés à la profondeur nécessaire, avec une trajectoire de récupération observable à chaque requête. Le projet publie des résultats de benchmark (LoCoMo, tau2-bench) montrant une précision mémoire en forte hausse et une réduction importante des tokens consommés. Il est distribué sous licence AGPLv3, sans bridage de fonctionnalités par rapport à l'offre hébergée, et s'appuie sur les travaux du papier VikingMem accepté à VLDB 2026.

## Points clés
- Un système de fichiers virtuel unique (`viking://`) pour mémoires, ressources et compétences, navigable comme un vrai système de fichiers (`ls`, `tree`, `find`).
- Chargement à trois niveaux (L0 abstract, L1 overview, L2 details) qui réduit fortement la consommation de tokens en ne chargeant le détail complet qu'à la demande.
- Récupération récursive par dossier : la recherche vectorielle localise d'abord le dossier le plus pertinent, puis descend couche par couche pour préserver le contexte environnant.
- Chaque requête laisse une trajectoire de navigation observable, ce qui permet de déboguer un résultat inattendu en retraçant le chemin exact qui l'a produit.
- À la fin d'une session, les préférences utilisateur et l'expérience de l'agent sont extraites de manière asynchrone vers la mémoire long terme.
- Gains mesurés sur LoCoMo (précision de 80-83%, contre 24-57% en mémoire native) et sur tau2-bench (+6,87 points de succès en retail, +11,87 en aérien).

## Analyse approfondie
OpenViking est une base de contexte open-source pour agents IA. Elle stocke mémoires, ressources et compétences comme un seul système de fichiers virtuel sous le protocole `viking://`, si bien qu'un agent parcourt son propre contexte avec `ls`, `tree` et `find` plutôt que d'interroger une base vectorielle opaque. Le contenu est traité en trois niveaux — L0 abstract, L1 overview, L2 details — et chargé à la demande. Chaque récupération laisse une trajectoire que l'on peut observer et déboguer.

*Le playground OpenViking Studio — une démo en ligne accessible dans le navigateur, sans installation requise.*

- **Un seul système de fichiers pour tout le contexte.** Mémoires, ressources et compétences reçoivent chacune une URI `viking://`. Les agents localisent et manipulent le contexte de façon déterministe, comme un développeur travaillant avec des fichiers.
- **Le chargement par niveaux réduit la dépense en tokens.** Chaque entrée est traitée en L0 (résumé), L1 (aperçu) et L2 (détails) à l'écriture, puis chargée seulement à la profondeur requise par la tâche.
- **Récupération récursive par répertoire.** La recherche vectorielle localise d'abord le répertoire le mieux noté, puis descend couche par couche, si bien que les résultats arrivent avec leur contexte environnant intact.
- **Récupération observable.** Chaque requête conserve sa trajectoire de navigation dans les répertoires. Quand un résultat semble erroné, on peut voir exactement quel chemin l'a produit.
- **Les sessions deviennent de la mémoire.** Une fois une session validée, OpenViking extrait de manière asynchrone les préférences utilisateur et l'expérience de l'agent vers la mémoire long terme.

Comment les pièces s'assemblent : Architecture. La réflexion derrière la conception : Le paradigme de base de données pour l'ingénierie du contexte.

```
viking://
├── resources/              # Ressources : docs de projet, dépôts, pages web, etc.
│   └── my_project/
│       ├── docs/
│       │   ├── api/
│       │   └── tutorials/
│       └── src/
└── user/
    └── {user_id}/
        ├── memories/
        │   └── preferences/
        │       ├── writing_style
        │       └── coding_habits
        ├── resources/
        │   └── private_project/
        ├── skills/
        │   ├── search_code
        │   └── analyze_data
        └── peers/
            └── web-visitor-alice/
```

Les trois niveaux de chargement :

- **L0 (Résumé)** : une phrase de synthèse pour une vérification rapide de pertinence.
- **L1 (Aperçu)** : les informations centrales et les scénarios d'usage pour la planification.
- **L2 (Détails)** : la donnée originale complète, lue seulement en cas de besoin.

Chaque répertoire porte ses propres couches L0/L1, si bien que la pertinence peut être jugée avant la lecture d'un fichier complet :

```
viking://resources/my_project/
├── .abstract               # L0 : ~100 tokens - vérification rapide de pertinence
├── .overview               # L1 : ~2k tokens - structure et points clés
└── docs/
    ├── .abstract
    ├── .overview
    └── api/
        ├── auth.md         # L2 : contenu complet, chargé à la demande
        └── endpoints.md
```

OpenViking 0.3.22 a été évalué sur la mémoire utilisateur en conversation longue (LoCoMo) et sur des tâches d'agent multi-tours (tau2-bench). Les résultats complets et les détails de configuration, incluant le QA sur base de connaissances, figurent dans le rapport de benchmark ; les scripts de reproduction se trouvent dans `./benchmark`.

L'évaluation mémoire a utilisé Doubao 2.0 Pro comme VLM et Doubao-embedding-vision-251215 comme modèle d'embedding.

- **Mémoire utilisateur (LoCoMo)** : avec OpenViking, les trois intégrations d'agent atteignent toutes 80-83% de précision — contre 24-57% avec leur mémoire native — tandis que les tokens d'entrée chutent de 34,3 à 91,0% et la latence de requête de 58,45 à 66,10%.
- **Expérience agent (tau2-bench)** : la mémoire d'expérience augmente le taux de succès des tâches de +6,87 points (vente au détail) et +11,87 points (aérien) par rapport au même LLM sans mémoire.

💡 **Envie de voir ça en action d'abord ?** Essayez OpenViking Studio — une instance hébergée en direct avec un playground de contexte, une recherche sémantique et un hub multi-agent. Aucune installation requise.

Requiert Python 3.10 ou supérieur.

```
pip install openviking --upgrade
openviking-server init      # assistant interactif : fournisseurs, modèles, ov.conf
openviking-server doctor    # valider la configuration
openviking-server           # démarrer (arrière-plan : nohup openviking-server > openviking.log 2>&1 &)
```

`init` guide à travers la configuration du fournisseur et écrit `~/.openviking/ov.conf`. Il prend en charge Volcengine, OpenAI, Codex OAuth, Kimi, GLM, et Ollama en local — pour Ollama, il peut détecter et installer le runtime et télécharger des modèles adaptés au matériel. `doctor` vérifie le fichier de configuration, la version de Python, la connectivité au fournisseur et l'espace disque sans serveur en cours d'exécution. Modèles manuels de `ov.conf`, exemples par fournisseur, variables d'environnement et configuration Windows : guide de configuration · docs de démarrage rapide.

L'installation inclut déjà le CLI client `ov`. Avec le serveur en cours d'exécution :

```
ov status
ov add-resource https://github.com/volcengine/OpenViking # --wait
ov ls viking://resources/
ov tree viking://resources/volcengine -L 2
# attendre un peu pour le traitement sémantique si --wait n'est pas utilisé
ov find "what is openviking"
ov grep "openviking" --uri viking://resources/volcengine/OpenViking/docs/en
```

Prochaines étapes :

- Configuration client (`ov config`), installations CLI autonomes (npm / cargo), et usages avancés comme la reconstruction d'index : configuration du CLI
- Déploiement Docker et en production : guide de déploiement

Les intégrations injectent le rappel OpenViking dans le contexte de l'agent et valident automatiquement la mémoire de session :

Instructions de configuration pour chaque agent : aperçu des intégrations d'agent.

OpenViking Helper est une console de bureau, actuellement en bêta pour macOS et Windows x64 :

- **Configuration visuelle d'agent local** : détecte le CLI OpenViking, Claude Code, Codex, Cursor, Trae et OpenCode, puis configure les intégrations plugin, MCP, Hook et CLI supportées.
- **Inspection de trace de session** : analyse les sessions Claude Code, Codex et Trae pour afficher le rappel OpenViking, l'injection de prompt, les appels MCP, la capture et les événements de validation.
- **Gestion locale de mémoire et de compétences** : consulte les fichiers de mémoire / règles locaux et les compétences `SKILL.md`, puis les synchronise vers OpenViking.

VikingBot est un framework d'agent IA construit au-dessus d'OpenViking :

```
pip install "openviking[bot]"
openviking-server --with-bot
ov chat   # dans un autre terminal
```

L'image Docker officielle embarque VikingBot et le démarre par défaut avec le serveur et l'interface console. Détails : guide VikingBot.

Pour la production, faites tourner OpenViking comme un service HTTP autonome — voir déploiement serveur et le guide de déploiement.

**L'édition open source n'est pas bridée.** OpenViking dans ce dépôt est entièrement open source sous licence AGPLv3 : aucune fonctionnalité verrouillée, aucun compte requis, aucune clé d'activation. Suivez « Déployer en production » ci-dessus et faites-le tourner vous-même en production — et cela restera vrai.

Les deux éditions ci-dessous répondent à « qui l'exploite et où ça tourne », pas à « puis-je l'utiliser ».

Une édition est officiellement hébergée sur Volcano Engine, sans rien à installer ni à opérer ; les utilisateurs open source existants peuvent migrer avec l'outil de migration (l'hébergement mondial hors Chine arrive chez BytePlus). L'autre tourne dans votre propre environnement, les données n'en sortant jamais ; elle ajoute le déploiement distribué et le support officiel par rapport à l'édition open source, activés par clé de licence.

Vous voulez simplement faire tourner l'édition open source ? Allez-y — vous n'avez besoin de contacter personne. Direction le démarrage rapide.

OpenViking ouvre en open source un sous-ensemble des capacités centrales décrites dans le papier VikingMem :

**VikingMem : A Memory Base Management System for Stateful LLM-based Applications**
Jiajie Fu, Junwen Chen, Mengzhao Wang, Aoxiang He, Maojia Sheng, Xiangyu Ke, Yifan Zhu, et Yunjun Gao.
arXiv:2605.29640, 2026. Accepté à VLDB 2026.
📄 Lire le papier sur arXiv

OpenViking accueille les collaborations avec d'autres projets open source pour construire l'écosystème des données de contexte. Nos partenaires confirmés incluent :

- deer-flow - Harnais SuperAgent open source pour horizon long
- NoKV - Système de fichiers distribué natif IA
- loopx - Noyau d'état léger pour l'ingénierie de boucle
- Hermes Agent - L'agent qui grandit avec vous

Intéressé à rejoindre la liste des partenaires ? Merci de soumettre une issue à notre communauté pour candidater.

OpenViking est encore à ses débuts, et il reste beaucoup à construire.

- **Docs** : docs.openviking.ai · FAQ
- **Blog** : blog.openviking.ai
- **Équipe** : à propos de nous
- **Chat** : Groupe Lark · WeChat · Discord · X
- **Contribuer** : corrections de bugs et nouvelles fonctionnalités bienvenues — voir CONTRIBUTING.md

Ce projet prend la sécurité au sérieux. Pour signaler une vulnérabilité et connaître les versions supportées, voir SECURITY.md

Le projet OpenViking utilise des licences différentes selon les composants.

## Pourquoi ça compte
OpenViking illustre une tendance de fond dans l'écosystème agentique : traiter la mémoire et le RAG comme une base de données de contexte navigable et observable plutôt que comme une boîte noire vectorielle, avec des gains chiffrés significatifs sur la consommation de tokens et la précision — un signal à suivre pour quiconque construit des agents avec état.
