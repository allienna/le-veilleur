---
title: "Stripe evals: Measuring real-world coding agent performance"
date: 2026-11-21
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fstripe.dev%2Fblog%2Fstripe-integration-evals-methodology%3Futm_source=tldr%26utm_medium=community/1/010001a1f8e20cf0-04c1a8d2-b096-40a7-9fd6-0fd535581342-000000/52m-WVlAhcnisQTAdYIjP3NNWg2JjwZ4DHeBebqKjJ8=452"
keywords: ["agents de codage", "Stripe", "benchmark", "MCP", "intégration API", "LLM"]
theme: "IA"
tone: "research"
used_in: ["2026-11-21"]
---

## Résumé
Stripe a conçu « Stripe evals », un benchmark mesurant la qualité des intégrations Stripe produites par des agents de codage (Claude Code, Codex, OpenCode) sur 69 scénarios réalistes de paiements, abonnements et Connect, via un agent qui simule un développeur humain. Les résultats montrent que le plugin agent Stripe améliore le score moyen de tous les modèles testés de 3 à 8 points, réduit les recherches web de 96 % et diminue l'usage de paramètres d'API obsolètes. Toutefois, une notation stricte exigeant la validation de tous les critères obligatoires fait chuter le taux de réussite moyen de 78,1 % à 29,4 %, révélant que la plupart des intégrations restent presque correctes mais échouent sur des détails critiques. Stripe publie en open source ce benchmark ainsi que son harnais d'évaluation Forge, qu'elle compte enrichir et maintenir dans le temps.

## Points clés
- Benchmark de 69 scénarios (paiements ponctuels, abonnements, Connect) testés sur 14 paires modèle/harnais (Claude Code, Codex, OpenCode), avec et sans le plugin agent Stripe.
- Le plugin Stripe améliore systématiquement les scores (+3 à +8 points), réduit les recherches web de 96 % et les références à des paramètres d'API obsolètes de 7 % à 1,3 %.
- Sous notation stricte (tous les critères MUST requis), le taux de réussite moyen s'effondre de 78,1 % à 29,4 %, révélant des erreurs sur le « dernier kilomètre » des intégrations.
- Les performances varient fortement selon le modèle, le harnais et le type de scénario : les meilleurs sur paiements/abonnements ne sont pas forcément les meilleurs sur Connect.
- L'évaluation utilise un agent-joueur de rôle doté de besoins latents privés pour simuler un développeur réel, et des juges LLM (GPT 6.1 Sol) notant chaque critère séparément.
- Stripe publie en open source le benchmark et le harnais Forge, avec un engagement à l'enrichir et à publier régulièrement de nouveaux résultats.

## Analyse approfondie
Les choix d'intégration déterminent la valeur qu'une entreprise retire de Stripe. Opter pour les schémas d'intégration actuels permet aux entreprises d'accéder à de nouvelles fonctionnalités avec moins de code sur mesure et peut réduire le travail de migration futur. Bien construire une intégration implique aussi de gérer les échecs de paiement, les changements d'abonnement et les événements webhook.

Lorsque les développeurs construisent avec des agents de codage, nous avons observé que ces agents ont tendance à privilégier des API plus anciennes, plus présentes dans leur corpus de pré-entraînement, qu'ils passent à côté de fonctionnalités clés et qu'ils hallucinent. Les benchmarks de codage existants ne détectent pas ce problème : ils vérifient si le code passe des tests déterministes, pas si l'intégration de l'API est correcte. Nous voulons que les développeurs qui construisent avec des agents démarrent sur la meilleure configuration Stripe possible, ce qui commence par identifier où les agents sont aujourd'hui en défaut. C'est pourquoi nous avons créé Stripe evals, pour mesurer cela et identifier des moyens d'orienter les agents vers de meilleures intégrations, via des fonctionnalités comme le plugin agent Stripe.

Stripe evals mesure la capacité des agents de codage à construire des intégrations de haute qualité dans des scénarios réalistes et bien spécifiés, pilotés par un agent jouant un rôle (roleplaying agent). Nous avons exécuté 69 scénarios couvrant les paiements ponctuels, les abonnements et Connect (marketplaces et plateformes), sur 14 paires modèle/harnais, à la fois avec et sans le plugin agent Stripe. Les scénarios incluent des tâches telles que la construction d'un checkout hébergé, l'implémentation d'une facturation à l'usage (metered billing), la gestion d'abonnements par poste (per-seat) et la répartition des paiements de marketplace.

Le plugin aide. Les 14 agents de codage ont tous obtenu un meilleur score avec lui, avec un gain d'environ 3 à 8 points de pourcentage, et les recherches web ont chuté de 96 % à mesure que les modèles s'appuyaient sur des indications fiables. Les modèles se comportent aussi différemment les uns des autres : Fable 5.1 a effectué 53 % d'appels d'outils supplémentaires avec le plugin, tandis que Gemini 3.8 Flash en a effectué 26 % de moins. Si les chiffres globaux sont élevés, un taux de réussite strict, exigeant que tous les critères nécessaires soient validés, fait chuter le score moyen de l'ensemble des agents de 78,1 % à 29,4 %.

Nous publions également notre benchmark Stripe et notre framework d'évaluation. Nous maintiendrons le harnais d'évaluation et mettrons à jour les résultats de façon continue, avec de nouveaux modèles, cas et fonctionnalités.

## Résultats détaillés

Les résultats ci-dessous évaluent les agents de codage sur nos 69 cas publics (19 Connect, 24 paiements et 26 abonnements) sur 2 exécutions.

### Tableau 1 : Résultats détaillés des scores

| Modèle | Harnais | Score moyen : sans plugin → avec plugin | Variation du score | Taux de réussite strict : sans plugin → avec plugin | Coût par exécution ($) : sans plugin → avec plugin | Minutes par évaluation : sans plugin → avec plugin |
|---|---|---|---|---|---|---|
| Haiku 5.5 | Claude Code | 73,5% → 76,2% | +2,7% | 23,5% → 30,9% | 0,08 → 0,09 | 8,3 → 7,8 |
| Sonnet 5.5 | Claude Code | 78,0% → 82,6% | +4,6% | 29,4% → 33,1% | 1,07 → 1,16 | 8,1 → 7,3 |
| Opus 5.5 | Claude Code | 83,5% → 86,2% | +2,7% | 35,3% → 36,0% | 2,77 → 3,15 | 12,4 → 12,4 |
| Fable 5.1 | Claude Code | 79,5% → 84,6% | +5,1% | 25,4% → 36,4% | 5,02 → 6,13 | 15,7 → 19,6 |
| Fable 5.2 | Claude Code | 81,1% → 85,2% | +4,1% | 28,4% → 43,2% | 5,76 → 5,35 | 15,2 → 15,1 |
| GPT-6 Luna | Codex | 72,0% → 79,1% | +7,1% | 17,3% → 29,1% | 0,05 → 0,07 | 7,2 → 8,8 |
| GPT-6.1 Sol | Codex | 85,6% → 89,6% | +4,0% | 39,0% → 50,7% | 0,51 → 0,61 | 6,1 → 6,5 |
| GPT-6 Astra | Codex | 85,5% → 90,0% | +4,5% | 41,9% → 52,9% | 2,93 → 3,63 | 6,2 → 7,8 |
| Gemini 4 Argon | OpenCode | 74,3% → 77,6% | +3,3% | 20,6% → 31,6% | 1,64 → 3,86 | 8,1 → 9,3 |
| Gemini 3.8 Flash | OpenCode | 64,8% → 72,7% | +7,9% | 11,2% → 21,6% | 2,21 → 2,67 | 11,6 → 9,9 |
| Grok 4.7 | OpenCode | 72,0% → 75,8% | +3,8% | 21,3% → 26,5% | 0,70 → 1,37 | 5,1 → 5,3 |
| Kimi K3 | OpenCode | 69,2% → 75,0% | +5,8% | 21,1% → 25,0% | 1,83 → 1,99 | 14,8 → 13,3 |
| GLM 5.3 | OpenCode | 68,1% → 72,6% | +4,5% | 18,5% → 21,8% | 2,26 → 2,42 | 15,7 → 14,7 |
| Minimax M3.1 Flash | OpenCode | 73,4% → 80,8% | +7,4% | 21,5% → 28,6% | 0,49 → 0,65 | 28,2 → 27,9 |

*Il s'agit d'une agrégation des cas Paiements, Connect et Abonnements, qui présentent des performances de modèle différentes ; les comparaisons entre modèles doivent donc être contextualisées avec le tableau 3.*

#### Le plugin améliore la performance des modèles

Dans nos évaluations, les 14 paires modèle/harnais ont toutes obtenu un meilleur score avec le plugin, avec une amélioration globale d'environ 3 à 8 points de pourcentage. Le plugin a également permis de réduire les références à des paramètres obsolètes, de 7 % à 1,3 % des paramètres dans les appels d'API. Par exemple, sans le plugin, GPT 6.1 Sol sur le scénario payments-mobile-physical-goods utilisait un paramètre récemment supprimé, `payment_method_types: ['card']`, alors qu'avec le plugin, le modèle écrit correctement `automatic_payment_methods: { enabled: true }`, activant les Dynamic Payment Methods.

#### Baisse du volume de tests grâce au plugin

Avec le plugin, les agents de codage ont écrit environ 40 % de lignes de test en moins et ont exécuté des tests dans 42 % des évaluations contre 53 % sans le plugin. Cela ne signifie pas que moins de tests améliore la performance, mais plutôt que des informations plus fiables fournies par le plugin réduisent le besoin de vérifications excessives du code écrit.

### Tableau 2 : Appels d'outils

| Modèle | Harnais | Recherches web/éval : sans → avec plugin | Variation | Récupérations de pages/éval : sans → avec plugin | Variation | Total appels d'outils/éval : sans → avec plugin | Variation |
|---|---|---|---|---|---|---|---|
| Tous les agents (regroupés) | Tous | 1,26 → 0,05 | −96% | 4,84 → 1,78 | −63% | 59,4 → 61,4 | +3% |
| Opus 5.5 | Claude Code | 0,36 → 0,07 | −82% | 4,14 → 1,92 | −54% | 59,9 → 61,3 | +2% |
| Sonnet 5.5 | Claude Code | 0,82 → 0,02 | −97% | 4,67 → 1,28 | −73% | 39,0 → 42,8 | +10% |
| Haiku 5.5 | Claude Code | 1,35 → 0,11 | −92% | 4,22 → 1,37 | −68% | 45,4 → 45,0 | −1% |
| Fable 5.1 | Claude Code | 0,40 → 0,03 | −92% | 7,26 → 2,74 | −62% | 35,8 → 54,8 | +53% |
| Fable 5.2 | Claude Code | 0,66 → 0,03 | −95% | 8,99 → 4,13 | −54% | 55,6 → 60,7 | +9% |
| GPT-6.1 Sol | Codex | 1,31 → 0,01 | −99% | 3,99 → 0,17 | −96% | 28,8 → 33,6 | +17% |
| GPT-6 Astra | Codex | 1,28 → 0,05 | −96% | 4,44 → 0,33 | −92% | 28,5 → 33,5 | +17% |
| GPT-6 Luna | Codex | 4,06 → 0,11 | −97% | 3,49 → 0,00 | −100% | 52,4 → 52,8 | +1% |
| Gemini 4 Argon | OpenCode | non mesuré | non mesuré | 0,17 → 1,99 | ×12 | 18,7 → 33,7 | +80% |
| Gemini 3.8 Flash | OpenCode | non mesuré | non mesuré | 0,17 → 0,12 | −31% | 47,1 → 34,6 | −26% |
| Grok 4.7 | OpenCode | non mesuré | non mesuré | 3,01 → 3,13 | +4% | 40,7 → 57,7 | +42% |
| Kimi K3 | OpenCode | non mesuré | non mesuré | 1,62 → 0,71 | −56% | 79,6 → 75,9 | −5% |
| GLM 5.3 | OpenCode | non mesuré | non mesuré | 4,01 → 1,29 | −68% | 117,0 → 106,4 | −9% |
| Minimax M3.1 Flash | OpenCode | non mesuré | non mesuré | 22,92 → 8,77 | −62% | 236,1 → 239,5 | +1% |

*OpenCode utilisait la recherche web via OpenRouter, que nous ne pouvons pas observer directement.*

#### Les agents remplacent la recherche web par le plugin

Le plugin inclut des appels d'outils MCP (comme la recherche documentaire, le planificateur d'implémentation) et des skills. En général, le plugin réduit le besoin d'environ 1,2 recherche web par évaluation. Les récupérations web (la façon dont les agents extraient du contenu web depuis une URL) diminuent également d'environ 3 récupérations par évaluation.

Pourtant, tous les modèles ne se comportent pas de la même façon. Il est intéressant de noter qu'Argon et Grok effectuent davantage de récupérations lorsqu'ils utilisent le plugin. Ils ont tendance à récupérer des pages particulières référencées dans les résultats d'outils ou dans les skills.

#### Une notation stricte réduit drastiquement les métriques d'évaluation

Pour mesurer si une intégration satisfait toutes les exigences clés de qualité, nous rapportons également le taux de réussite strict pour les critères requis (détails dans la section notation et reporting ci-dessous). Dans ce mode de calcul, la performance moyenne des modèles chute de façon spectaculaire, de 78,1 % à 29,4 %, pour les mêmes critères requis. Cela indique que de nombreux modèles produisent des implémentations presque correctes mais rencontrent des difficultés sur le dernier kilomètre. Par exemple, dans le scénario payments-radar-review-fulfillment, Opus 5.5 ne vérifie pas si une commande est éligible à l'expédition, se contentant de vérifier `PaymentIntent.status === 'succeeded'`, ce qui peut permettre l'expédition de commandes après un remboursement ou un litige (dispute).

### Tableau 3 : Catégories de scénarios

| Modèle | Harnais | Paiements : sans → avec plugin | Abonnements : sans → avec plugin | Connect : sans → avec plugin |
|---|---|---|---|---|
| Fable 5.2 | Claude Code | 88% → 90% | 69% → 73% | 89% → 97% |
| Fable 5.1 | Claude Code | 84% → 87% | 71% → 73% | 85% → 97% |
| Opus 5.5 | Claude Code | 87% → 89% | 76% → 78% | 89% → 94% |
| Sonnet 5.5 | Claude Code | 84% → 90% | 68% → 70% | 85% → 91% |
| Haiku 5.5 | Claude Code | 82% → 86% | 62% → 63% | 78% → 82% |
| GPT-6 Astra | Codex | 90% → 96% | 82% → 83% | 85% → 92% |
| GPT-6.1 Sol | Codex | 90% → 94% | 80% → 84% | 87% → 91% |
| GPT-6 Luna | Codex | 80% → 89% | 62% → 67% | 75% → 83% |
| Minimax M3.1 Flash | OpenCode | 79% → 88% | 60% → 66% | 88% → 92% |
| Gemini 4 Argon | OpenCode | 77% → 79% | 63% → 64% | 86% → 95% |
| Gemini 3.8 Flash | OpenCode | 70% → 78% | 51% → 57% | 77% → 88% |
| Grok 4.7 | OpenCode | 76% → 81% | 60% → 60% | 83% → 90% |
| Kimi K3 | OpenCode | 76% → 80% | 55% → 59% | 80% → 91% |
| GLM 5.3 | OpenCode | 75% → 77% | 55% → 56% | 77% → 89% |

*Des différences significatives de performance ont été observées entre les catégories de scénarios : paiements ponctuels, abonnements et Connect. Les agents de codage les plus performants sur les paiements ponctuels et les abonnements n'étaient pas les meilleurs sur Connect. Les scénarios Connect, qui impliquent davantage de décisions d'intégration spécifiques au scénario, ont aussi bénéficié d'un gain plus important grâce au plugin, comparé aux autres catégories.*

## Méthodologie

### Agents de codage

Nous avons choisi trois harnais de codage : Claude Code, Codex et OpenCode, ainsi qu'un échantillon de modèles incluant des modèles à poids ouverts (open-weight).

### Le plugin agent Stripe

Le plugin agent Stripe donne aux agents de codage des skills rédigés par Stripe et un accès à des outils via notre serveur Model Context Protocol (MCP). Les skills fournissent les meilleures pratiques d'intégration, tandis que des outils comme `stripe_implementation_planner` et `search_stripe_documentation` fournissent des conseils d'implémentation et la documentation à jour. Des outils de recherche et de détails d'API aident les agents à consulter les opérations et paramètres pris en charge.

### Recherche web

Pour simuler au mieux l'expérience du développeur, nous avons fourni la recherche web native la plus proche disponible pour chaque harnais de codage. Pour tous les modèles Claude Code et Codex, nous avons utilisé la recherche web fournie par les harnais eux-mêmes. Pour OpenCode, nous avons utilisé l'outil serveur OpenRouter Web Search, qui tente d'utiliser la recherche native du fournisseur si elle est disponible, sinon se replie sur Exa.

### Utiliser un LLM pour simuler un humain aux besoins latents

Les développeurs partent généralement d'un objectif, pas d'exigences complètes, et guident les agents de codage via des retours itératifs et des décisions clés. Pour évaluer ces interactions, nous utilisons un agent secondaire qui joue le rôle du développeur, sans jamais enseigner à l'agent de codage comment réussir le benchmark.

Cet agent-joueur de rôle reçoit pour instruction d'orienter l'agent de codage vers le résultat produit souhaité, sans présupposer d'expertise sur les API Stripe. Il demande à l'agent de codage d'investiguer et de prendre lui-même toutes les décisions d'intégration. Il lui est également interdit d'écrire du code, de répéter la réponse de l'agent, ou de s'étendre sur des considérations applicatives génériques.

Tout comme un développeur humain a un ensemble latent de besoins en abordant l'agent de codage, notre agent-joueur de rôle dérive un ensemble figé et privé de besoins à partir du prompt initial et du contexte, avant même le début de la conversation. Par exemple, un utilisateur construisant une plateforme qui facture 0,50 $ fixe par paiement pourrait vouloir comprendre l'économie unitaire (unit economics) même sans le demander explicitement. À la fin de chaque tour, l'agent-joueur de rôle détermine si tous les besoins sont satisfaits. Il identifie généralement deux à quatre besoins, avec un maximum de six. À chaque tour, il sélectionne un besoin non résolu et le transforme en question de suivi. Il ne révèle jamais la liste complète.

L'agent-joueur de rôle ne s'arrête, en fonctionnement normal, que lorsqu'il ne reste plus aucun besoin ou qu'une limite de tours préétablie est atteinte. Cela maintient l'agent concentré, comme le serait un développeur focalisé, tout en permettant une flexibilité naturelle si un petit détour est nécessaire pour accomplir la tâche. Le harnais enregistre les besoins et leur progression à des fins d'auditabilité, mais cet état privé n'est jamais transmis à l'agent de codage ni aux juges.

### Évaluer les agents dans une boucle réaliste

Les agents de codage ont été exécutés en mode headless dans un espace de travail isolé, avec accès à leurs outils de codage habituels et à la recherche web. Ils pouvaient inspecter le dépôt, écrire des fichiers, exécuter des commandes et réviser leur implémentation sur plusieurs tours d'interaction avec l'agent-joueur de rôle.

Nous avons exécuté chaque scénario avec des configurations appariées :
- Sans le plugin Stripe
- Avec le plugin Stripe

La tâche, le message d'ouverture, le harnais de codage et le modèle étaient fixes.

### Juger sur la base de preuves observables

Les preuves sont évaluées selon une grille spécifique à chaque scénario, comportant plusieurs critères. Tous les critères n'ont pas la même importance. Pour en tenir compte, nous reprenons la terminologie de la RFC 2119 : un critère est soit un MUST (obligatoire pour toute intégration valide), soit un SHOULD (une recommandation).

Nous notons chaque critère séparément plutôt que de demander à un seul juge de les évaluer tous ensemble, afin d'éviter qu'un critère n'influence le score des autres. Cela rend les échecs plus faciles à interpréter et les jugements plus simples, ce qui permet à des modèles relativement plus faibles de juger de façon fiable et sans dégradation lorsque l'on augmente le nombre de critères.

Chaque jugement s'appuie sur deux sources de preuves :
- La transcription visible. Il s'agit d'une trajectoire native analysée (les étapes de l'utilisateur et de l'agent directement issues des sessions de l'agent), sans horodatages, métadonnées supplémentaires, sessions de sous-agents, etc. En cas d'erreur d'analyse, nous nous reposons sur un enregistrement de la conversation produit par le runner.
- L'espace de travail résultant. Les fichiers écrits pendant l'exécution restent dans le répertoire hôte monté dans l'environnement de l'agent. Le juge inspecte un instantané (snapshot) de ce que l'agent a produit.

Ce qui est exclu :
- La collecte de l'espace de travail est bornée et exclut les dépendances, les répertoires générés, les métadonnées du dépôt et les fichiers binaires.
- Le raisonnement du modèle : l'évaluation repose sur le comportement observable et les artefacts produits, pas sur le raisonnement privé.

Les juges ont rendu des jugements structurés, en utilisant un échantillonnage verbalisé à cinq candidats pour faire apparaître des lectures alternatives de chaque critère. Un critère n'est validé que lorsque la réponse de l'agent de codage ou l'espace de travail fournit la preuve requise.

### Notation et reporting

L'évaluation exécute 69 cas x 2 répétitions x 2 bras = 276 exécutions totales par agent de codage. Les résultats sont regroupés en trois catégories comportant chacune un nombre variable de scénarios (24 paiements ponctuels, 26 abonnements et 19 plateformes Connect).

La métrique phare rapportée — le taux de réussite d'intégration — est le taux de réussite moyen des critères (à la fois MUST et SHOULD). Un scénario comportant 7 critères MUST et 1 SHOULD, pour lequel une exécution en satisfait 6, obtient un score de 75 %. Le taux de réussite strict, qui exige la validation de tous les critères MUST (binaire par cas), est plus représentatif du succès du développeur, mais il est sensible à toute erreur de données ou de jugement. C'est ce qui est à l'origine de conclusions erronées autour de phénomènes émergents.

Nous avons utilisé GPT 6.1 Sol à la fois comme modèle jouant le rôle du développeur et comme modèle juge pour toutes les évaluations, afin de garantir la cohérence du jugement. Pour mesurer un éventuel biais du juge (par exemple, Sol favorisant potentiellement les modèles OpenAI), nous avons mené un test avec Opus comme juge, mais les résultats n'ont montré aucun biais. Les scores ont évolué de façon synchrone, Opus se montrant simplement un juge uniformément plus indulgent. Tous les modèles ont été exécutés avec le réglage d'effort par défaut.

En pratique, un délai d'expiration de 45 minutes par cas est appliqué, et traité comme une erreur. Les erreurs ne sont pas incluses dans le calcul du score, car il est plausible que certains modèles, avec davantage de temps, auraient réussi à résoudre les cas.

### Ce que ce benchmark ne mesure pas

Nous prévoyons de combler les lacunes suivantes dans nos travaux futurs :
- La vérification à l'exécution (runtime). Une intégration bien formée mais non fonctionnelle peut obtenir la note maximale. Le benchmark valide la spécification correcte, pas l'exécution correcte.
- La qualité de la recommandation produit. Nous ne vérifions pas si un agent recommande le bon produit.
- La maintenance à long terme. Le benchmark mesure la qualité de l'intégration initiale, pas la façon dont le code vieillit ou s'adapte aux évolutions de l'API.

## Conclusion et travaux futurs

Ce travail montre que le comportement des agents dépend fortement du modèle qui les pilote et des outils disponibles. Les harnais de codage, associés à des modèles de pointe (frontier models), peuvent produire des intégrations Stripe fonctionnelles de bout en bout, sans pour autant suivre nécessairement toutes les meilleures pratiques. Les agents se comportent mieux lorsqu'ils sont guidés par notre plugin, bien que leurs performances ne soient pas uniformes selon les modèles économiques (paiements ponctuels vs abonnements vs paiements de marketplace). Ce premier benchmark nous aide à comprendre comment différents agents et modèles de codage intègrent Stripe, et nous donne des pistes pour mieux les orienter afin d'obtenir de meilleurs résultats pour les entreprises qui utilisent Stripe.

Dans notre démarche de développement ouvert (build in the open), nous publions ce benchmark ainsi que le harnais d'évaluation Forge. Conscients qu'il reste toujours du travail à accomplir, nous ajouterons bientôt davantage de cas de test, explorerons un éventail plus large de harnais et de modèles, mettrons continuellement à jour Forge, et publierons périodiquement de nouveaux résultats.

Si vous souhaitez comprendre ce qui est possible avec les applications d'IA, nous recrutons ! Consultez nos offres d'emploi en ingénierie.

## Pourquoi ça compte
Ce travail illustre concrètement les limites actuelles des agents de codage sur des tâches d'intégration réelles (API obsolètes, hallucinations, approximations sur les derniers détails critiques) et montre comment un fournisseur peut combler ce fossé via des outils/skills dédiés (MCP) plutôt que de compter sur les capacités génériques du modèle — une approche transposable à d'autres écosystèmes d'API suivis en veille IA/dev tools.
