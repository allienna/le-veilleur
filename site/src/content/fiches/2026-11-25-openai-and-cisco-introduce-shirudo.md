---
title: "OpenAI and Cisco introduce Shirudo"
date: 2026-11-25
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Flinks.tldrnewsletter.com%2FiCVEif/1/010001a20d7d27e0-53e789d5-a97b-438e-8ffd-f9ea51c829a6-000000/FfKhyHbd2E14UX0LpqR4dIQOLGBXbl9mvg7yBt5k3AY=452"
authors: ["OpenAI", "Cisco"]
keywords: ["eBPF", "Linux", "vulnérabilités", "open-source", "OpenAI", "Cisco"]
theme: "Sécurité"
tone: "news"
used_in: ["2026-11-25"]
---

## Résumé
OpenAI et Cisco lancent Shirudo, un runtime open-source qui permet de protéger des systèmes Linux en production contre des exploits connus, sans attendre l'application d'un correctif ni redémarrer les services. Le projet s'appuie sur eBPF pour déployer des « shields » (bliter des chemins de code vulnérables) de manière ciblée, signée et vérifiable matériellement via TPM. Une démonstration a montré qu'un shield généré par Codex bloquait une exploitation de type Java4Shell contre un service Elasticsearch actif, sans interruption. Le code est publié en licence BSD 2-Clause (programmes BPF en double licence BSD/GPL) pour inviter la communauté sécurité à contribuer.

## Points clés
- Shirudo (« bouclier » en japonais) utilise eBPF pour appliquer des protections temporaires ciblées sur des systèmes Linux déjà en production, en attendant un correctif définitif.
- Une preuve de concept a bloqué une attaque Java4Shell visant Elasticsearch grâce à un shield généré par Codex, ajoutant une vérification sur le décodeur Base64 de Java, sans arrêter le service.
- Le projet repose sur quatre piliers : protection à chaud sans redémarrage, défense assistée par des agents IA à vitesse machine, déploiement de confiance (shields signés et vérifiés par le vérificateur eBPF du noyau), et attestation matérielle via TPM pour tracer les protections appliquées.
- OpenAI et Cisco veulent à terme renforcer les fondations du système (durcissement du noyau, limitation des permissions des workloads, mises à jour et restauration plus sûres) et combiner IA de pointe et recherche en sécurité pour détecter vulnérabilités et tester des défenses réalistes.
- Le code est publié en open-source (licence BSD 2-Clause, composants BPF en double licence BSD/GPL) afin que développeurs, chercheurs et opérateurs infra puissent l'inspecter, le tester et contribuer.
- L'ambition affichée est de livrer des shields testés en même temps que les annonces de vulnérabilités, pour donner aux opérateurs une protection temporaire pendant la préparation des correctifs permanents.

## Analyse approfondie
Shirudo part d'un problème opérationnel classique en sécurité : entre la découverte d'une vulnérabilité et le déploiement effectif d'un correctif, il peut s'écouler des jours, voire des semaines. Pendant cette fenêtre, bloquer purement et simplement l'opération système exploitée par l'attaquant risque aussi de couper l'accès à des requêtes légitimes qui utilisent le même mécanisme — d'où la difficulté de « protéger sans casser le service ».

La réponse proposée consiste à créer des protections temporaires et réversibles, appelées « shields », que les équipes de sécurité peuvent tester avant de les activer. Un shield cible précisément le comportement qui rend le système vulnérable, laissant passer le trafic légitime. Une fois validé par un opérateur humain, il peut être déployé sur un service qui continue de tourner, sans interruption.

Techniquement, Shirudo repose sur eBPF, la technologie Linux qui permet d'exécuter de petits programmes à des points précis du noyau pour observer un comportement suspect et y réagir de façon ciblée. Le projet s'organise autour de quatre capacités :

- **Protection à chaud** : les shields eBPF peuvent neutraliser un chemin de code vulnérable sans redémarrage, et les équipes peuvent d'abord observer leur effet en mode supervision avant de les appliquer réellement.
- **Défense à la vitesse de la machine** : des agents (IA) disposent de contrôles programmables pour investiguer une vulnérabilité, concevoir un shield ciblé, puis valider son efficacité face à de vrais exploits et de vraies charges de travail — tout en laissant aux équipes humaines le contrôle final sur ce qui est effectivement déployé.
- **Déploiement de confiance** : chaque shield est signé cryptographiquement et vérifié avant chargement ; le vérificateur eBPF du noyau Linux contrôle sa conformité aux règles de sécurité, et des contrôles noyau empêchent les modifications non autorisées.
- **Vérification matérielle** : un module TPM (Trusted Platform Module) permet de conserver une trace vérifiable des protections appliquées ou retirées, ce qui donne aux opérateurs un moyen de prouver la conformité de leurs systèmes.

Une démonstration présentée lors de la Linux Plumbers Conference illustre concrètement l'application d'un shield et sa vérification sur une machine cible. L'exemple phare concerne la vulnérabilité « Java4Shell » : l'équipe a utilisé Codex (le modèle de génération de code d'OpenAI) pour produire un shield ajoutant un contrôle d'entrée sur le décodeur Base64 de Java, puis l'a attaché directement à un processus Elasticsearch en cours d'exécution. Lors de la tentative d'exploitation, le shield a rejeté l'entrée malveillante, bloquant l'attaque tout en laissant Elasticsearch continuer de fonctionner normalement.

Au-delà de ce cas d'usage, OpenAI et Cisco présentent Shirudo comme une première étape vers une infrastructure capable de s'adapter aux menaces émergentes sans sacrifier la fiabilité. Les deux entreprises affichent l'ambition de renforcer les fondations des systèmes d'exploitation nécessaires pour déployer ce type de protection à grande échelle : durcissement du noyau et des services critiques, réduction des permissions accordées aux workloads, et sécurisation des processus de mise à jour et de restauration.

L'objectif à long terme est de permettre à des défenseurs humains comme à des agents IA d'identifier rapidement les systèmes affectés par une faille, de valider des protections, puis de déployer des shields eBPF qui bloquent les exploits sans perturber les charges de travail en cours. Les applications devraient, à terme, ne disposer que des permissions strictement nécessaires, régies par des politiques générées et maintenues automatiquement. OpenAI et Cisco entendent combiner recherche en IA de pointe et recherche en sécurité/infrastructure pour découvrir des vulnérabilités et tester des défenses contre des attaques réalistes, afin de faciliter la détection et le confinement des compromissions, d'empêcher les attaquants de se déplacer latéralement entre systèmes, et de restaurer les services dans un état connu et vérifié. L'attestation matérielle et des contrôles réseau indépendants doivent apporter une garantie supplémentaire même si certains systèmes individuels sont compromis.

Enfin, le projet est publié en open-source : le code de Shirudo est disponible pour que développeurs, chercheurs en sécurité et opérateurs d'infrastructure puissent l'examiner, le tester et y contribuer. Il est distribué sous licence BSD 2-Clause, les programmes BPF étant eux en double licence BSD et GPL. L'ambition affichée par OpenAI et Cisco est de pouvoir, à l'avenir, publier des shields déjà testés en parallèle des annonces de vulnérabilités, offrant ainsi aux opérateurs un moyen d'évaluer et de déployer une protection temporaire pendant la préparation du correctif permanent.

## Pourquoi ça compte
Shirudo illustre une tendance de fond en sécurité défensive : l'usage d'agents IA pour générer et valider des contre-mesures à la vitesse des attaques, combiné à des mécanismes noyau (eBPF, TPM) pour garantir la confiance dans ces protections déployées à chaud. C'est un signal fort de la convergence entre acteurs IA (OpenAI) et acteurs infrastructure/sécurité (Cisco) sur la défense « virtual patching », un sujet clé pour toute veille sécurité ou infrastructure cloud.
