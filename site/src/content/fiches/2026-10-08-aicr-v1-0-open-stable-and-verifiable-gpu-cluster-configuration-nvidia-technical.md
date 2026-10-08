---
title: "AICR v1.0: Open, stable, and verifiable GPU cluster configuration | NVIDIA Technical Blog"
date: 2026-10-08
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fdeveloper.nvidia.com%2Fblog%2Faicr-v1-0-open-stable-and-verifiable-gpu-cluster-configuration%3Futm_source=tldrai/1/010001a1168ef748-df05ec07-7adb-4c74-853d-e820666ab336-000000/yacT9BW5rqZ8V0_Sr_PgRlgozKaFyqyMubsOvajeNFc=452"
keywords: ["GPU", "Kubernetes", "NVIDIA", "infrastructure", "validation", "open source"]
theme: "Tech"
tone: "news"
used_in: ["2026-10-08"]
---

## Résumé

NVIDIA annonce la version 1.0 d'AICR (AI Cluster Runtime), un outil open source qui fournit des recettes de configuration verrouillées par version pour les clusters Kubernetes accélérés par GPU. Cette version établit un contrat de compatibilité stable sur la CLI, l'API REST, le SDK Go, la structure des bundles et les schémas d'artefacts, permettant aux opérateurs, intégrateurs et contributeurs de s'appuyer durablement sur ces interfaces publiques. Le projet fournit un tableau de bord de validation permettant de trouver des recettes par service, GPU, système d'exploitation et intention de charge de travail, avec des preuves de validation signées. AICR compte désormais plus de 100 contributeurs distincts, dont près de la moitié extérieurs à NVIDIA.

## Points clés

- AICR propose quatre capacités indépendantes : Snapshot (état observé du cluster), Recipe (configuration souhaitée verrouillée par version), Bundle (artefacts de déploiement pour Helm, Argo CD, Flux ou Helmfile) et Validation (comparaison et vérification de conformité/performance).
- La v1.0 fige des règles de compatibilité pour la CLI `aicr`, l'API REST `aicrd`, le package Go `github.com/NVIDIA/aicr/pkg/client/v1`, ainsi que la structure des bundles et des schémas d'artefacts, avec des bases de référence vérifiées avant toute fusion de code.
- Chaque recette embarque des preuves de validation signées, consultables via la commande `aicr evidence verify`.
- Le modèle de recette est déjà intégré par l'écosystème : Pulumi Labs l'expose via un fournisseur infrastructure-as-code, et Mirantis l'intègre dans k0rdent pour la gestion multi-cluster.
- Le projet a grandi en six mois, passant de quelques recettes à une bibliothèque couvrant les principaux services Kubernetes et l'ensemble du portefeuille d'accélérateurs NVIDIA actuel.

## Analyse approfondie

Les clusters Kubernetes accélérés par GPU dépendent de versions compatibles entre des dizaines de composants, chacun suivant son propre cycle de publication : noyaux hôtes, pilotes GPU, runtimes de conteneurs, réseau, stockage, opérateurs et frameworks de charge de travail.

Une configuration qui fonctionne pour un service, une génération de GPU et une version de Kubernetes donnés peut échouer silencieusement pour une autre combinaison, et retracer les conflits de version après déploiement est lent et source d'erreurs.

NVIDIA AI Cluster Runtime (AICR) répond à ce problème avec des recettes validées et verrouillées par version pour la configuration des clusters GPU. Chaque recette fige les combinaisons de composants qui fonctionnent ensemble, génère les artefacts de déploiement pour Helm, Argo CD, Flux ou Helmfile, et porte des preuves de validation signées issues du matériel sur lequel elle a été testée.

La version 1.0 d'AICR établit un contrat de compatibilité stable à travers sa CLI, son API REST, son SDK Go, la structure de ses bundles et les schémas de ses artefacts, afin que les opérateurs, intégrateurs et contributeurs puissent s'appuyer sur les interfaces publiques d'AICR en toute confiance.

Le tableau de bord de validation permet aux opérateurs de trouver des recettes par service, GPU, système d'exploitation, intention de charge de travail et plateforme optionnelle, puis d'inspecter le statut de chaque recette ainsi que toute preuve publiée pour la configuration matérielle testée. Les intégrateurs peuvent développer en s'appuyant sur les interfaces publiques d'AICR sous la politique de compatibilité v1.x. Les contributeurs peuvent proposer des recettes pour des environnements que les mainteneurs ne peuvent pas tester, les valider sur leurs propres clusters, et soumettre des preuves signées pour relecture par les mainteneurs.

Ce modèle de recette trouve également des usages à travers l'écosystème. Pulumi Labs expose AICR via un fournisseur d'infrastructure-as-code, tandis que l'intégration k0rdent de Mirantis l'empaquète pour la gestion multi-cluster. Ensemble, ces initiatives démontrent l'intérêt de définir une configuration Kubernetes accélérée par GPU une seule fois et de la consommer via différents outils. Aujourd'hui, AICR compte plus de 100 contributeurs distincts, dont près de la moitié proviennent de l'extérieur de NVIDIA !

Les clusters Kubernetes accélérés par GPU dépendent de versions et de paramètres compatibles à travers les noyaux hôtes, les pilotes GPU, les runtimes de conteneurs, Kubernetes, le réseau, le stockage, les plugins de périphériques, les opérateurs, les ordonnanceurs et les frameworks de charge de travail. Ces composants suivent des cycles de publication différents ; mettre à jour l'un peut casser une combinaison qui fonctionnait auparavant. Une configuration validée pour un service, une génération de GPU, un type de fabric, une forme de machine et une version de Kubernetes donnés peut échouer pour une autre, et de petites différences de version peuvent être difficiles à retracer après déploiement.

Même si chaque composant s'installe avec succès, le cluster peut ne pas correspondre à la configuration prévue par la recette. L'installation ne confirme pas que les composants sont en bon état, que les capacités requises comme l'ordonnancement en groupe (gang scheduling) ou la découverte des accélérateurs fonctionnent, ni que les résultats mesurés atteignent les seuils de performance d'une recette.

La connaissance des combinaisons qui fonctionnent et de la manière dont elles ont été validées résidait jusque-là dans des systèmes de validation séparés, des scripts de déploiement et des procédures opérationnelles (runbooks). Cela rend difficile pour les équipes de découvrir, reproduire et mettre à jour des configurations fonctionnelles.

Au cours des six derniers mois, AICR est passé de quelques recettes à une bibliothèque couvrant les principaux services Kubernetes et le portefeuille actuel d'accélérateurs NVIDIA, restitués sous forme de bundles neutres vis-à-vis de l'outil de déploiement. Nous avons ajouté la validation sur cluster en direct, les preuves signées, l'agrégation publique des preuves et la vérification de la chaîne d'approvisionnement (supply-chain). Pour la v1.0, nous avons également ajouté des bases de référence de compatibilité validées et des contrôles bloquants à la fusion autour des surfaces d'intégration publiques.

AICR fournit quatre capacités fondamentales :

- **Snapshot** enregistre l'état observé du cluster, y compris les informations sur Kubernetes, le système d'exploitation, le noyau, le GPU et la topologie.
- **Recipe** décrit la configuration de composants souhaitée et verrouillée par version, ainsi que les contraintes et les phases de validation qui s'y appliquent.
- **Bundle** restitue la recette sous forme d'artefacts pour l'outil de déploiement préféré de l'opérateur.
- **Validation** compare la recette à l'état observé et, lorsque cela est déclaré, exécute des vérifications de déploiement, de conformité et de performance sur le cluster.

Ces quatre capacités sont délibérément indépendantes. Un snapshot enregistre l'état observé ; ce n'est pas une configuration souhaitée. Une recette décrit la configuration souhaitée ; elle ne réconcilie pas un cluster. Les outils CD open source courants comme Helm, Argo CD, Flux ou Helmfile appliquent ou réconcilient le bundle dans le cluster. AICR peut ensuite valider le cluster en cours d'exécution par rapport à la recette, et enregistrer une preuve signée du résultat.

Ces capacités peuvent être combinées selon plusieurs séquences. Les données de snapshot ou des critères cibles explicites peuvent produire une recette. Une recette peut produire un bundle pour un déployeur existant. La recette et l'état observé du cluster alimentent la validation. Un opérateur vérifie explicitement les bundles et les preuves lorsqu'il invoque la commande correspondante.

Par exemple, un opérateur peut sélectionner EKS, GB300, Ubuntu, l'entraînement (training), et Kubeflow ; résoudre ces critères vers une recette figée ; restituer la recette pour Argo CD ; la déployer via le flux de travail GitOps existant ; et valider le cluster en cours d'exécution par rapport à cette même recette. La configuration prévue ne change pas si l'opérateur la restitue à la place pour Helm, Flux ou Helmfile.

AICR v1.0 définit des règles de compatibilité pour sa CLI publique, son API REST, son SDK Go, la structure de ses bundles et les schémas de ses artefacts. Elle permet également aux opérateurs d'inspecter les preuves de validation publiées pour chaque recette « Supported » (prise en charge) : ce qui a été testé, quelles vérifications ont réussi, et qui a signé les résultats.

AICR v1.0 établit des règles de compatibilité pour :

- les commandes publiques, drapeaux (flags), sémantique de sortie et sortie structurée de la CLI `aicr`
- l'API REST `aicrd` et le contrat OpenAPI
- l'API exportée du package `github.com/NVIDIA/aicr/pkg/client/v1`
- la structure des bundles générés et les schémas d'artefacts AICR

Chaque interface publique dispose d'une base de référence validée, vérifiée avant toute fusion de modifications. La politique de publication définit également les changements cassants (breaking changes) sémantiques. Après la v1.0, retirer ou modifier de façon incompatible une interface publique stable nécessite une nouvelle version majeure.

Pour les intégrateurs Go, `pkg/client/v1` expose le flux de travail pris en charge sans nécessiter d'importations depuis les packages internes d'AICR. La CLI et le serveur REST utilisent la même façade, réduisant le risque qu'un point d'entrée public se comporte différemment d'un autre.

Essayez une recette pour votre environnement, inspectez son statut et toute preuve publiée, et exécutez la commande `aicr evidence verify` du tableau de bord lorsque des preuves sont disponibles. Les contributions sont particulièrement utiles pour les combinaisons matériel/cluster hors de la couverture actuelle du projet. Vous pouvez :

- Contribuer des fonctionnalités, intégrations ou documentation
- Proposer une recette pour du matériel, un OS ou un service non encore représenté dans AICR
- Valider une recette sur votre propre cluster et soumettre une preuve signée
- Signaler des bugs, partager des retours ou demander des fonctionnalités via GitHub Issues

Commencez par le dépôt du projet, le guide de contribution et le suivi des tickets (issue tracker).

## Pourquoi ça compte

AICR illustre une tendance de fond dans l'infrastructure IA : la standardisation open source de la configuration GPU/Kubernetes pour réduire la dette opérationnelle liée à la prolifération de versions incompatibles. C'est un signal à suivre pour quiconque opère ou prévoit d'opérer des clusters GPU à grande échelle, car la gouvernance de compatibilité v1.0 et l'adoption par des tiers (Pulumi, Mirantis) suggèrent une adoption plus large à venir.
