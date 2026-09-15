---
title: "Building a Robust Harness for agent in production: Feed agent case-study - monday AI engineering"
date: 2026-09-15
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fengineering.monday.com%2Fbuilding-a-robust-harness-for-agent-in-production-feed-agent-case-study%2F%3Futm_source=tldrdev/1/010001a09fa17143-b67cfd13-fe03-4346-b4e7-d376aac736e3-000000/fVrIHVgclFNNWVvVcG9DcgvXDo3G7LoJI3x8WCAuL1w=452"
keywords: ["agents IA", "LangChain", "production", "observabilité", "hallucinations", "évaluation LLM"]
theme: "IA"
tone: "research"
used_in: ["2026-09-15"]
---

## Résumé
Dans cet article, l'équipe ingénierie de monday.com décrit le « harness » (garde-fou opérationnel) construit autour de feedAgent, un agent qui génère un flux d'activité personnalisé pour chaque membre d'un espace de travail. La thèse centrale : un LLM seul ne garantit rien en production — c'est l'ensemble des mécanismes qui l'entourent (préparation des données, limites d'exécution, vérification des sorties, observabilité, mémoire, évaluation) qui transforme un agent capable en un agent fiable. L'équipe a construit ce harness au-dessus de l'architecture d'agent de LangChain, en l'enrichissant de règles métier spécifiques. L'article détaille la méthode utilisée (« walk the flow ») et les techniques concrètes mises en œuvre à chaque étape, de la récupération des données jusqu'à la boucle de feedback.

## Points clés
- Un agent en production échoue à trois niveaux possibles : les données/contexte en entrée, le flux d'exécution lui-même, et la boucle de feedback qui permet de s'améliorer.
- Avant l'appel au modèle : un préprocesseur d'activité réduit le volume de tokens, supprime les données personnelles (PII) et un système d'alias remplace les identifiants bruts pour détecter les hallucinations.
- Pendant l'exécution : schéma de sortie validé par outil, retry sur échec de schéma, limite du nombre d'appels au modèle et limite de récursion du graphe encadrent le comportement de l'agent.
- En sortie : filtrage des hallucinations (citations d'alias invalides) et déduplication des activités entre les éléments du flux.
- La boucle de feedback repose sur trois piliers : traçabilité (LangSmith, événements de synthèse), mémoire du flux (règles explicites de l'utilisateur et observations inférées de son comportement), et évaluations offline/online avec LLM-juge.
- Conclusion de l'équipe : les défaillances ne viennent généralement pas du modèle lui-même, mais des hypothèses implicites faites autour de lui — d'où l'importance du harness.

## Analyse approfondie
### Qu'est-ce qu'un « harness » ?
Les auteurs filent la métaphore du bowling : le modèle de langage est la boule, et le harness correspond aux barrières latérales de la piste. Sans elles, une mauvaise trajectoire finit dans la gouttière — une citation hallucinée, une sortie malformée, une boucle incontrôlée qui consomme le budget. Le harness est ce qui garde la boule dans la piste. On peut jouer sans filet et parfois atteindre la cible, mais rien ne le garantit ; en production, on veut transformer cette possibilité en quasi-certitude.

En construisant feedAgent — un agent profond qui curate un flux d'activité personnalisé pour chaque membre d'un espace de travail — l'équipe de monday.com a identifié trois zones de risque récurrentes : (1) les données et le contexte fournis à l'agent, (2) le flux de l'agent et ses limites, (3) la boucle de feedback qui permet son amélioration continue. Leur conviction : adopter un harness existant ne suffit pas, il faut le connaître en profondeur et l'enrichir avec les spécificités du domaine métier. Ils se sont appuyés sur l'architecture d'agent de LangChain et son harness intégré, puis ont construit par-dessus leur propre couche spécifique à leur métier.

### Étude de cas : FeedAgent
Un espace de travail (« workspace ») est un lieu partagé où humains et agents collaborent. FeedAgent décide, parmi tout ce qui s'y passe, ce qui mérite d'être remonté à chaque utilisateur, en visant un flux précis, actionnable, à jour et fiable. Ce cas d'usage cumule plusieurs contraintes : l'agent raisonne en boucle, appelle des outils, décide seul quand il a terminé ; il récupère des données réelles issues de sources multiples ; sa sortie doit être structurée et ancrée dans les faits — chaque élément du flux doit citer les activités précises qui le justifient et rester actionnable ; enfin, cette sortie est directement vue et utilisée par les utilisateurs. L'un des principaux défis consiste à extraire uniquement ce qui compte vraiment parmi un volume massif de données (activité sur les tableaux, documents, exécutions d'agents, etc.).

### La méthode : parcourir le flux
L'équipe a choisi de construire le harness en parcourant chaque phase du cycle d'exécution de l'agent, en se demandant systématiquement : « Que peut-il mal se passer ici, et que fait le harness pour y remédier ? » Cette méthode part du principe qu'un agent n'est pas un pipeline linéaire mais une boucle complexe, différente pour chaque flux spécifique construit.

### Récupération des données — avant l'invocation de l'agent
La première phase consiste à récupérer les données et construire le prompt. Le prompt système pose le contexte général (tâche, flux, définition du succès), puis viennent les données propres au flux à générer : activité des utilisateurs sur différents objets, activité des agents, éléments de flux existants, etc. Le modèle ne voit que ce que le harness choisit de lui exposer. La question du harness ici est de garantir une entrée précise, de taille limitée et sans données personnelles :

1. **Préprocesseur d'activité (taille limitée et sans PII)** : réduit les tokens en entrée tout en conservant l'information utile, à la fois pour la gestion du contexte et pour les coûts. Il agrège les rafales d'événements en événements uniques, ne conserve que les changements agrégés importants, et élimine le bruit de configuration. Cette étape est déterministe — le modèle ne voit jamais le flux brut — et retire toute donnée personnelle avant que le LLM n'y ait accès.
2. **Système d'alias (lutte contre l'hallucination)** : les identifiants bruts du prompt sont remplacés par des alias courts, créant une surface de détection des hallucinations — toute référence inventée par le modèle plutôt que réellement récupérée est repérée et écartée. Le modèle cite ces alias comme preuves pour chaque élément du flux, puis toute activité hallucinée est filtrée.
3. **Mise en cache du prompt** : le prompt système, chargé à chaque génération de flux, est mis en cache au niveau de la passerelle IA (AI gateway), ce qui réduit fortement le coût des appels répétitifs.

### Flux de l'agent — exécuter l'agent avec des limites
**1) Initialisation** : au moment où l'agent est créé, le modèle est instancié avec sa configuration (nom du modèle, température, limites de tokens), les outils sont branchés, le prompt système est attaché, et la pile de middleware est appliquée. La question du harness : l'agent démarre-t-il avec les bons outils, les bonnes limites, et un contrat clair sur ce qu'il doit produire ?

1. **Schéma de sortie** : le schéma force le modèle à émettre sa réponse via un appel d'outil validé, plutôt que d'espérer un JSON libre valide.
2. **Retry en cas d'échec de schéma** : en cas d'échec, l'erreur de validation est réinjectée dans le contexte pour permettre au modèle de se corriger.
3. **Limite d'appels au modèle** : l'équipe utilise le middleware `modelCallLimitMiddleware` de LangChain avec `exitBehavior: 'end'`, garantissant un arrêt maîtrisé plutôt qu'un échec non géré.

**2) À l'intérieur de l'exécution** — divisée en deux volets.

- *2.1 L'exécution* : l'agent raisonne, appelle des outils, raisonne à nouveau, et finit par émettre (ou non) sa sortie structurée.
  - **Limite de récursion**, distincte de la limite d'appels au modèle : elle plafonne le nombre d'itérations de boucle que le graphe peut exécuter, créant un second plafond indépendant.
  - **Gestion de l'absence de réponse structurée / des exceptions** : chaque exécution se termine proprement, soit avec une sortie validée, soit avec un échec capturé et journalisé.

- *2.2 Les outils* : chaque outil est un point de défaillance potentiel. Quelques patterns appliqués :
  - Ne pas laisser l'agent choisir un outil indispensable — l'ajouter séparément plus tard dans le flux pour garantir son exécution, et restreindre les outils/permissions aux seules actions requises.
  - Fournir des messages d'erreur actionnables (une instruction plutôt qu'un simple signal d'échec).
  - Garantir un cycle de fermeture défini pour les outils qui maintiennent des connexions.

**3) Sortie** : l'agent retourne une liste de nouveaux éléments de flux et de mises à jour, chacun citant les alias utilisés comme preuve.

1. **Filtrage des hallucinations** : tout ce qui ne correspond pas à un identifiant d'activité valide est écarté et journalisé.
2. **Déduplication** : une même activité ne peut apparaître dans deux éléments de flux ; un système de priorité et un ensemble d'identifiants résolus garantissent l'unicité.

### La boucle de feedback
**1) Observabilité** : après l'exécution, la question devient celle de la visibilité.

1. **Traçage LangSmith** : toute l'invocation est enveloppée dans `traceable()`, capturant appels d'outils, réponses du modèle, comptage de tokens et chaînes de raisonnement.
2. **Événements** : un événement de synthèse est émis à chaque exécution, portant des métriques (durée, nombre d'activités, nombre d'éléments de flux, modèle utilisé, trajectoire des appels d'outils, décomposition du prompt, etc.).

**2) Boucle d'apprentissage** : la « Feed Memory » referme la boucle en réinjectant les signaux comportementaux des utilisateurs dans l'entrée de l'agent lors de l'exécution suivante.

1. **Règles explicites** : converties depuis les propos directs de l'utilisateur, de haute autorité, appliquées de façon déterministe avant la curation.
2. **Observations inférées** : motifs détectés dans les dismissals, clics et temps passé, de plus faible autorité, informant les décisions ambiguës sans jamais primer sur les règles explicites.

Dès la phase 1, l'agent relit ces règles et observations accumulées avant de curer le flux suivant.

**3) Évaluations** : l'agent n'étant pas déterministe, l'équipe combine deux niveaux d'évaluation :

1. **Offline** : un jeu de données enrichi en continu, évalué par un LLM-juge selon des métriques spécifiques, exécuté en intégration continue pour éviter les régressions.
2. **Online** : analyse continue des données de production en temps réel, avec des métriques similaires.

### En résumé
Les barrières ne garantissent pas un strike, mais elles garantissent que la boule reste dans la piste — à chaque exécution, pour chaque utilisateur. Le constat récurrent de l'équipe : les défaillances ne se situent pas dans le modèle lui-même, mais dans les hypothèses implicites faites autour de lui. Ce qui entre dans le prompt, ce qui borne l'exécution, ce qui est vérifié avant mise en production, ce qui est mémorisé pour la prochaine fois — tout cela relève du harness, pas du modèle.

## Pourquoi ça compte
Ce retour d'expérience de monday.com donne un vocabulaire et des patterns concrets — gestion du contexte, bornage de l'exécution, vérification anti-hallucination, mémoire comportementale, évaluation offline/online — directement réutilisables pour qui conçoit des agents LLM en production, au-delà du cas LangChain.
