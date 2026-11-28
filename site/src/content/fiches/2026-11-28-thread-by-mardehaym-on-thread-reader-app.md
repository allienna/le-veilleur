---
title: "Thread by @mardehaym on Thread Reader App"
date: 2026-11-28
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fthreadreaderapp.com%2Fthread%2F2125913331915784509.html%3Futm_source=tldrdev/1/010001a21cf08720-a1a3e8d5-31b1-49de-837d-f0489d0b4604-000000/S-DeAURMoCyYpHhh3ufahYM9xb_eQ36lDU5tMuKbh7o=452"
authors: ["@mardehaym"]
keywords: ["agents IA", "architecture LLM", "conseil en IA", "code graph", "gouvernance", "production"]
theme: "IA"
tone: "opinion"
used_in: ["2026-11-28"]
---

## Résumé

Ce thread (compilé via Thread Reader App / newsletter TLDR) rassemble plusieurs réflexions pratiques d'un praticien de l'IA en entreprise. Il affirme que les échecs en production viennent rarement du choix du modèle LLM, mais des six couches d'infrastructure qui l'entourent (déclencheurs métier, orchestration, outils déterministes, contexte, évaluation/contrôle humain, runtime). Il enchaîne avec des mises en garde contre les cabinets de conseil en IA, les erreurs organisationnelles les plus fréquentes lors des transformations IA, une technique concrète (le « code graph ») pour réduire la consommation de tokens des agents de codage, et un playbook en 12 semaines pour industrialiser un workflow IA.

## Points clés

- Les échecs de production d'agents IA viennent des six couches qui entourent le modèle (déclencheur métier, orchestration/état, outils déterministes, contexte de confiance, évaluation/contrôle humain, runtime/control plane), pas du modèle lui-même.
- Les cabinets de conseil en IA posent un risque structurel : les conseils ne garantissent pas une implémentation réelle, et la phase de « discovery » peut devenir un centre de coûts sans livrable clair.
- Les transformations IA échouent souvent pour des raisons organisationnelles — mesurer l'activité (pull requests) plutôt que la valeur livrée, ou distribuer des licences sans workflow cible ni baseline.
- Un « code graph » (nœuds = fonctions/classes/types, arêtes = appels/imports) réduit d'environ 25 % la consommation de tokens d'un agent de codage en évitant l'exploration à l'aveugle du repo.
- Un playbook en 12 semaines pour industrialiser un workflow IA commence par désigner un owner unique et poser un jalon de validation à chaque phase, avant même de choisir un modèle.

## Analyse approfondie

La plupart des entreprises passent leur temps à débattre du modèle à choisir. Or le modèle s'inscrit dans un système d'exploitation plus large, et presque chaque échec en production se produit dans les six couches qui l'entourent.

> Couche un : expérience et déclencheur. Arrêtez de vous rabattre systématiquement sur une interface de chat. Les véritables agents métier se déclenchent sur un événement : l'arrivée d'un fichier, une facture entrante, un changement de statut de ticket, ou une planification. Quand l'agent a besoin d'un humain, il route vers une file d'exceptions ou une boîte de réception, pas vers une transcription de chat brute que personne dans l'équipe des opérations n'a le temps de lire.

> Couche deux : orchestration et état. Arrêtez de traiter les agents comme des scripts qui traînent sur l'ordinateur portable de quelqu'un. La définition d'un agent doit être versionnée, bornée et gouvernée comme n'importe quel autre artefact de code, avec possibilité de rollback. Stockez l'historique d'exécution et les points de contrôle (checkpoints) dans une base de données comme Postgres, afin qu'une exécution interrompue reprenne là où elle s'est arrêtée plutôt que de repartir de zéro.

> Couche trois : outils et logique déterministe. Les garanties résident dans du code simple, testé unitairement, pas dans le prompt. Encapsulez votre logique métier éprouvée et vos API de systèmes de référence (systems of record) derrière un unique service connecteur, sous forme d'outils nommés avec des interfaces stables. Laissez les règles déterministes gérer les étapes fixes, et n'appelez le modèle que là où un jugement est réellement nécessaire.

> Couche quatre : contexte de confiance. Ne déversez pas tout votre wiki ou votre repo dans un prompt géant. Donnez à chaque domaine son propre knowledge graph ou catalogue de données, délimité, que l'agent interroge en cours d'exécution comme un outil. Quand la documentation s'éloigne de la réalité, les agents hallucinent. La solution n'est pas un prompt plus long. C'est un contexte faisant autorité et sensible aux permissions.

> Couche cinq : évaluation et contrôle humain. Avant qu'un agent ne touche à un client ou ne déplace de l'argent, constituez un golden set de cas réels passés que vos experts du domaine valident comme corrects. Exécutez des contrôles déterministes et des évaluations de type LLM-as-a-judge sur chaque changement, et conservez une étape de validation humaine pour toute action à fort impact ou irréversible. Les opérateurs cessent d'appuyer sur des boutons et commencent à juger.

> Couche six : runtime et plan de contrôle. Chaque appel au modèle passe par une passerelle LLM (LLM gateway) unique, à l'intérieur de votre propre périmètre cloud. Les appels directs à l'API d'un fournisseur sont un défaut de production. Imposez des clés virtuelles par tenant et par service, des plafonds de dépenses stricts, des garde-fous contre l'injection de prompt, une traçabilité complète, et des alias de modèles internes, afin que changer de fournisseur soit un simple changement de configuration, pas une réécriture.

Les modèles et les frameworks continueront de changer. Les actifs durables sont vos règles de workflow, vos jeux d'évaluation, vos périmètres de contexte, et la responsabilité opérationnelle.

Évitez d'embaucher un cabinet de conseil en IA.
Évitez d'embaucher un cabinet de conseil en IA.
Évitez d'embaucher un cabinet de conseil en IA.
Évitez d'embaucher un cabinet de conseil en IA.
Évitez d'embaucher un cabinet de conseil en IA.
Évitez d'embaucher un cabinet de conseil en IA.

LA PREMIÈRE RAISON EST :

1. Les conseils laissent toujours quelqu'un d'autre faire la construction

Si vous avez besoin d'un logiciel fonctionnel, vérifiez que l'implémentation fait réellement partie de la mission.

Demandez un projet similaire qu'ils ont livré : ce que leur équipe a construit, ce qui est passé en production et qui en a assuré le support ensuite.

Une feuille de route seule ne prouve pas qu'ils sont capables de l'exécuter.

2. La phase de « discovery » peut devenir un projet à part entière

Un dirigeant d'agence nous a raconté que des cabinets d'ingénierie lui avaient demandé 50 000 $ juste pour explorer son problème de système legacy.

Il n'était pas prêt à dépenser autant pour obtenir un simple scope.

Avant de payer pour une phase de discovery, mettez-vous d'accord sur les questions auxquelles elle répondra, ce que vous recevrez, et comment cela vous rapproche d'une construction concrète.

J'ai passé ce trimestre à échanger avec des CFO, des operating partners et des responsables de l'innovation qui ont déjà dépensé de l'argent réel sur l'IA.

Les mêmes 6 erreurs reviennent sans cesse, souvent dans leurs propres mots :

Erreur 1 : Mesurer l'activité.

Le CFO d'une société de logiciels de soins à domicile soutenue par un fonds de private equity — le genre de plateforme qui doit garder chaque visite Medicaid prête pour un audit — m'a dit que l'équipe ouvre et ferme désormais plus de pull requests que jamais.

Les incendies sont éteints plus vite, mais la base de code ne s'améliore pas.

Plus de pull requests n'est pas synonyme de progrès.

Mesurez le travail de la roadmap qui a réellement été livré.

Erreur 2 : Traiter les licences comme une stratégie.

Un directeur chez un administrateur de fonds de private markets a donné Claude à environ un tiers de l'entreprise. Interrogé sur les économies réalisées, il n'avait pas encore de réponse. La facture continue d'augmenter.

Pendant ce temps, dans l'administration de fonds, les avis d'appel de capital (capital call notices) sont encore saisis manuellement par un analyste et vérifiés par un second, et le nouveau modèle ILPA arrive en 2027.

Choisissez ce workflow précis et mettez-vous d'accord sur une base de référence avant que quiconque n'obtienne une licence.

18 raisons pour lesquelles les transformations IA échouent, même dans des entreprises qui réussissent par ailleurs :

1. Cartographier la procédure (SOP) plutôt que le processus réel. Le document dit une chose, les systèmes en disent une autre. Asseyez-vous avec la personne qui fait réellement le travail.

2. Des données qui ne sont pas prêtes. Un agent n'est jamais meilleur que les données auxquelles il peut accéder. Obtenez les accès, les permissions et un schéma utilisable avant que quiconque n'écrive un prompt.

La majorité des tokens consommés par un agent de code servent à une seule tâche : comprendre comment la base de code s'assemble.

Un graphe de code (code graph) a réduit cela d'environ 25 % pour nous.

Comment ça fonctionne, et six règles pour en faire tourner un à l'échelle d'une équipe :

Un agent de code démarre chaque ticket sans rien connaître de la base de code.

Il cherche et ouvre des fichiers jusqu'à en savoir assez pour faire la modification. Cela consomme la majorité des tokens d'une session, et une grande partie de ce qu'il lit s'avère sans importance.

Nous avons donc donné à nos agents une carte à consulter avant d'ouvrir le moindre fichier : un graphe de code.

Chaque fonction, classe et type est un nœud. Chaque appel et import entre eux est une arête (edge).

Sur le repo pour lequel nous l'avons construit, cela représente 6 477 nœuds et 16 011 arêtes. Une construction complète prend 16 secondes.

Comment nous faisons passer un workflow IA de l'idée à la production en 12 semaines, étape par étape :

Nous ne commençons pas par un modèle. Nous commençons par un workflow, un owner, et un jalon de validation (gate) à la fin de chaque phase. Voici le playbook.

1. Cadrage — frame (semaines 1-2)

Désignez un seul owner qui contrôle les priorités, la validation et l'escalade. Choisissez un workflow dont les clients se plaignent, pour lequel ils attendent, ou à cause duquel ils partent, et remontez-le en amont et en aval pour trouver où se situe réellement le délai.

→ livrables : brief d'opportunité, cartographie du workflow, cartographie des systèmes, registre des outils, baseline, charte de preuve (proof charter)
→ point clé : les opérateurs expérimentés définissent ce à quoi ressemble une bonne réponse avant que quiconque ne commence à ajuster quoi que ce soit
→ jalon : le sponsor confirme le workflow, son owner, et ce qui est hors périmètre

## Pourquoi ça compte

Ce thread condense des leçons de terrain rarement formalisées sur la mise en production d'agents IA en entreprise — architecture en couches, pièges du conseil, erreurs organisationnelles récurrentes — utiles pour quiconque évalue un projet d'agents IA ou un prestataire externe.
