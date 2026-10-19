---
title: "How to Use AI to Learn Faster"
date: 2026-10-19
url: "https://open.substack.com/pub/gregorojstersek/p/how-to-use-ai-to-learn-faster?utm_source=multiple-personal-recommendations-email&utm_medium=email&token=eyJ1c2VyX2lkIjo0NzU1OTI2MjgsInBvc3RfaWQiOjIxOTg0OTM1MywiaWF0IjoxNzkyMzU3NzkzLCJleHAiOjE3OTQ5NDk3OTMsImlzcyI6InB1Yi0xMTE1ODE1Iiwic3ViIjoicG9zdC1yZWFjdGlvbiJ9.e_u5umHPGiIFUXRX3m77Jcrq_CBEFIReX6YcUzizKbQ"
authors: ["Gregor Ojstersek"]
keywords: ["IA", "apprentissage continu", "onboarding codebase", "prompts", "Claude Code", "ingénierie logicielle"]
theme: "IA"
tone: "opinion"
used_in: ["2026-10-19"]
---

## Résumé
L'article soutient que l'IA n'est pas seulement un outil pour écrire du code plus vite, mais aussi un puissant levier d'apprentissage pour les ingénieurs. L'auteur distingue trois profils d'ingénieurs face à l'IA — les réfractaires, les sur-dépendants et les « multiplicateurs » — et affirme que seul ce dernier groupe en tire un impact réel. Il détaille ensuite des workflows concrets (prompts inclus) pour apprendre une nouvelle base de code, un nouveau langage/framework, construire des projets pratiques, et utiliser l'IA comme partenaire de réflexion. L'article est un extrait adapté du livre à paraître de l'auteur, « The Multiplier Mindset » (O'Reilly).

## Points clés
- Trois profils face à l'IA : les réfractaires (méfiance totale), les sur-dépendants (délèguent aussi leur jugement) et les multiplicateurs (délèguent les tâches répétitives, pas les décisions).
- Processus en 4 étapes pour onboarder une nouvelle base de code : /init avec un modèle haut de gamme, cartographie de l'architecture, identification de la stratégie de test, puis lancement de l'application — chaque étape accompagnée d'un prompt type.
- Apprendre un nouveau langage/framework en s'appuyant sur des connaissances déjà acquises (ex. Python → Java, FastAPI → Spring Boot) grâce à des prompts comparatifs.
- Construire des projets pratiques en mode « Plan » en questionnant activement les choix d'architecture proposés par l'IA plutôt qu'en générant tout le code d'un coup.
- Utiliser l'IA comme partenaire de réflexion : stress-tester une spec technique, préparer une conversation difficile, clarifier un problème, ou faire réviser son écrit.
- Message central : l'objectif n'a jamais été de tout faire soi-même ; les LLM sont des outils plus puissants mais aux résultats moins prévisibles.

## Analyse approfondie
Cette newsletter est sponsorisée par **CodeRabbit**.

**Moins de signalements. Seulement des risques réels.**

Le code généré par IA peut introduire des vulnérabilités faciles à manquer dans une pull request.

CodeRabbit Security relit en continu votre base de code pour détecter des bugs complexes et des risques de sécurité, en s'appuyant sur le contexte de l'ensemble de la base de code pour suivre les flux de données, les dépendances et les patterns au-delà du dernier diff.

Lancez CodeRabbit Security sur vos propres dépôts dès aujourd'hui.

Merci à CodeRabbit d'avoir sponsorisé cette newsletter. Revenons à la pensée du jour !

## Intro

L'IA transforme l'ingénierie plus vite que n'importe quel outil avant elle. En quelques années seulement, nous sommes passés d'écrire chaque ligne de code nous-mêmes à considérer l'ingénierie assistée par IA comme une façon standard de construire des logiciels.

Ce changement a créé beaucoup d'incertitude. Beaucoup de gens se demandent quelles compétences resteront précieuses, comment les rôles vont évoluer, et si s'appuyer sur l'IA va les aider à progresser ou les rendre trop dépendants d'elle.

Mais l'IA n'est pas seulement un outil pour écrire du code plus vite. Elle peut aussi être l'un des outils les plus puissants pour apprendre. La clé est de savoir comment l'utiliser efficacement.

Dans cet article, vous apprendrez comment les ingénieurs et responsables d'ingénierie les plus performants utilisent l'IA pour apprendre plus vite. Plus important encore, vous apprendrez l'état d'esprit derrière ces façons de travailler.

Commençons !

## Mon prochain livre « The Multiplier Mindset », publié par O'Reilly

Cet article est une version adaptée d'un des chapitres de mon prochain livre intitulé « The Multiplier Mindset », publié par O'Reilly. Le livre sortira bientôt et est disponible en précommande !

## Il existe 3 types de professionnels de l'ingénierie qui utilisent l'IA

Quand il s'agit d'utiliser l'IA, la plupart des ingénieurs et responsables d'ingénierie se répartissent en 3 camps :

- Les réfractaires

Ce sont les ingénieurs qui refusent complètement d'utiliser l'IA parce qu'ils ne lui font pas confiance. Ce sont souvent des personnes plus expérimentées qui ont vu de nombreux changements dans l'industrie.

Ils sont réticents au changement, préférant s'en tenir à ce qu'ils connaissent et maîtrisent. Leur état d'esprit est « ça a bien fonctionné pour moi pendant 15 ans, pourquoi changer ? ». Mais cette attitude peut empêcher les gens d'apprendre de nouvelles choses et d'améliorer leur métier.

- Les sur-dépendants

Ce sont les personnes qui s'appuient tellement sur les outils d'IA qu'elles arrêtent de réfléchir de façon critique et deviennent moins efficaces. Ce sont souvent des ingénieurs moins expérimentés qui maîtrisent bien le paysage des outils d'IA. Mais leur dépendance excessive à ces outils aboutit souvent à un travail médiocre.

Pire, certains ne vérifient même pas si le résultat produit par l'IA est conforme aux standards de l'équipe ! Cela force les relecteurs à faire le travail de trouver tous les problèmes, ce qui peut prendre beaucoup plus de temps que si les ingénieurs avaient fait la tâche correctement dès le départ.

- Les multiplicateurs

Ce sont les ingénieurs et responsables d'ingénierie qui voient l'IA comme un moyen de multiplier leurs efforts, et non de remplacer leur expertise. Ils l'utilisent pour éliminer le travail répétitif, apprendre plus vite, explorer davantage d'idées, et consacrer plus de temps aux problèmes où le jugement humain compte le plus. Ce sont aussi ceux qui ont le plus grand impact.

Vous voulez faire partie du **camp des multiplicateurs** : aborder ce « nouvel outil à la mode » avec curiosité, et non avec une confiance non méritée. Vous devez avoir envie d'essayer de nouvelles choses et d'apprendre, tout en gardant fermement les bonnes pratiques et fondamentaux de l'ingénierie. Vous devez déléguer vos tâches répétitives, pas vos décisions de jugement.

Vous devriez utiliser l'IA pour vous aider à penser à un niveau plus élevé, car c'est exactement ce qu'est devenir un multiplicateur en ingénierie. Les sections suivantes examinent comment multiplier votre impact sur les tâches importantes grâce à l'IA.

## Comment les multiplicateurs utilisent l'IA pour apprendre plus vite

Pour apprendre de nouvelles choses significativement plus vite, vous avez besoin d'une bonne compréhension des pratiques d'ingénierie et de la capacité à mobiliser différentes ressources pour obtenir ce dont vous avez besoin.

Les grands ingénieurs ne passent pas des heures à essayer de comprendre une base de code en la parcourant fichier par fichier ou en lisant chaque mot de la documentation. Ils utilisent l'IA pour comprendre rapidement les parties inconnues de la base de code et obtenir une vue d'ensemble de son architecture, de ses API et de tout autre élément pertinent. Voici quelques exemples.

### Intégration dans de nouvelles bases de code

Utiliser l'IA peut vous aider à comprendre une base de code en quelques heures. Jeff Morhous, ingénieur logiciel senior travaillant dans le secteur de la santé, a écrit un article invité sur la newsletter Engineering Leadership expliquant comment il utilise l'IA lorsqu'il doit travailler sur une nouvelle base de code.

Il a présenté un processus en quatre étapes, que je résume dans cette section.

**Étape 1 : utiliser /init pour obtenir la vue d'ensemble**

Si la base de code dispose déjà d'un fichier CLAUDE.md et/ou AGENTS.md, lisez-les. Sinon, lancez la commande /init de Claude Code. Elle va parcourir la base de code et documenter sa compréhension des fonctionnalités les plus importantes dans CLAUDE.md.

Utilisez un modèle de niveau supérieur quand vous lancez /init, même si cela vous coûte plus de tokens. Les tokens dépensés en raisonnement en amont sont des tokens bien dépensés.

Utiliser le Plan Mode avec un modèle moins cher comme Sonnet rend le plan plus susceptible de passer à côté d'une architecture critique ou de contenir des erreurs lourdes de conséquences. Les modèles davantage orientés raisonnement, en revanche, proposent souvent des choses à quoi vous n'auriez pas pensé seul.

**Étape 2 : cartographier l'architecture**

Il est judicieux de produire tôt une carte du dépôt pour vous aider à comprendre les composants majeurs du système, les frontières de responsabilité et les dépendances.

Voici un prompt que vous pouvez utiliser pour cela :

```
You are onboarding me to this repository.
Tasks:
- Identify the top-level architecture (apps/services/libraries) and what each does.
- Produce a directory map: top 10 directories with responsibilities.
- Identify key runtime boundaries: API layer, domain layer, persistence, async jobs, config.
- Show a dependency diagram (Mermaid) using the repo's actual module/package boundaries.
- Cite exact files for each claim (paths + brief evidence).
Constraints:
- Do not edit files.
- Prefer reading docs first (README, AGENTS.md, CLAUDE.md, docs/, CONTRIBUTING, ADRs) and then code.
- If the repo is a monorepo, explain the workspace/tooling setup.
Diagram:
Create a Mermaid diagram with your findings.
```

**Étape 3 : identifier la stratégie de test**

Si vous voulez comprendre la pyramide de tests de votre application et gagner rapidement en confiance, vous devez identifier dès le départ les patterns de test de votre application. Voici un prompt que vous pouvez utiliser pour cela :

```
Identify the testing strategy in this repo.
Output:
- Where tests live and how they're organized (unit/integration/e2e).
- The fastest local confidence loop: which commands to run before a PR.
- How fixtures/mocks/test containers are handled.
- Common failure modes in this repo's tests (if visible from config/docs).
If there is no testing strategy, propose a plan for one that follows the
testing pyramid (lots of unit tests, less e2e tests).
```

**Étape 4 : lancer l'application**

Si vous n'avez pas encore réussi à faire tourner l'application à ce stade, vous aurez besoin d'instructions. Demandez les étapes de configuration avec ce prompt :

```
Produce a repo-specific local setup checklist with commands.
Rules:
- Only include steps you can justify from files in the repo (README, Makefile, package/build files, scripts, devcontainer config).
- Include: required runtimes, dependency install, env vars, database setup,
migrations/seeds, and "run server / run worker / run UI".
- End with a smoke test of one key flow.
```

Cela devrait vous donner un seul « chemin heureux » de configuration qui se termine par un service fonctionnel et une étape de vérification.

### Apprendre un nouveau framework ou langage de programmation

De plus en plus d'ingénieurs avec qui je discute deviennent agnostiques en matière de technologie. La séparation entre frontend et backend continue de s'estomper.

Il en va de même pour les différents langages de programmation. Si vous êtes bon dans une certaine technologie, vous avez probablement une bonne compréhension de ses fondamentaux d'ingénierie et de ses patterns spécifiques.

Vous pouvez apprendre beaucoup plus facilement une nouvelle technologie en utilisant l'IA, car les concepts sont assez similaires, alors que la syntaxe diffère. Si vous êtes expert en Python, vous pouvez appliquer vos connaissances en combinaison avec l'IA pour devenir productif en Java et en PHP, et il en va de même pour beaucoup d'autres langages et frameworks.

Une fois que vous maîtrisez bien une technologie donnée, vous pouvez utiliser l'IA pour devenir bon dans d'autres si vous en avez besoin.

Par exemple, imaginez que vous êtes un ingénieur Python expérimenté qui doit travailler sur un projet Java. Vous commencez par donner à l'IA le contexte sur vous-même. Vous pouvez utiliser un prompt comme celui-ci :

```
I'm an experienced Python engineer and need to become productive in Java.
Explain the most important differences, using Python concepts I already
understand. Focus on the things most likely to surprise me or cause
mistakes.
```

Comme étape suivante, vous pouvez être plus précis sur le travail concret que vous effectuez. Si vous rejoignez un nouveau projet qui utilise Spring Boot, vous pourriez utiliser ce prompt :

```
I know how to build REST APIs with FastAPI. Show me how the same concepts
work in Spring Boot, including routing, dependency injection, validation,
database access, and error handling.
```

À partir de là, utilisez l'IA pendant que vous travaillez pour obtenir des explications sur du code inconnu et faire relire votre code afin de détecter d'éventuelles erreurs.

### Construire des projets pratiques

Depuis une dizaine d'années, regarder une vidéo tutoriel a été la méthode standard pour apprendre une nouvelle technologie. Essayez plutôt d'utiliser l'IA pour vous aider à comprendre certaines parties pendant que vous construisez.

Assurez-vous de demander pourquoi certaines choses sont ainsi faites. Vous pouvez commencer à peu près comme si vous appreniez un nouveau framework, sauf que cette fois votre objectif est d'apprendre en construisant. Disons que vous êtes un ingénieur React expérimenté et que vous voulez monter en compétence sur Angular. Vous pouvez commencer avec ce prompt :

```
I'm an experienced React developer learning Angular. I want to build a
simple TODO app with CRUD functionality. Create a plan that will help me
learn Angular while building it. Don't write the code yet.
```

C'est là que le mode plan de votre outil de codage IA préféré peut s'avérer utile. Passez en revue le plan et l'architecture proposés, puis commencez à poser des questions comme celle-ci :

```
Why would you structure the application this way? How is this different
from how I would typically structure a React application?
```

Ensuite, je vous conseille fortement de construire le projet une partie à la fois. Ne cherchez pas simplement à tout faire « en un coup » en espérant que ça marche. Utilisez l'IA comme un partenaire d'apprentissage.

Si vous voyez un pattern que vous ne reconnaissez pas, c'est le moment de demander pourquoi ce pattern est là, quelles pourraient être les alternatives possibles, et bien sûr, comment ce pattern se rattache aux concepts que vous connaissez déjà.

De plus, vous pouvez utiliser l'IA pour relire votre code. Un prompt pour cela pourrait ressembler à ceci :

```
Review this code as an experienced Angular engineer. What am I doing that
works but isn't a good practice in Angular? Explain why and show me how
an experienced Angular developer would approach it.
```

L'objectif est que vous compreniez et appreniez, donc n'essayez pas d'optimiser pour que l'IA écrive le plus de code possible. Concentrez-vous sur les décisions concernant POURQUOI tel code doit exister et COMMENT il affecte l'ensemble du système.

### Comment utiliser l'IA comme partenaire de réflexion

La loi de Conway nous dit que la structure d'un système logiciel reflète la structure de communication de l'organisation qui le construit.

C'est peut-être pour cela que les gens de l'industrie du logiciel doivent résoudre tant de problèmes difficiles impliquant à la fois la technique et les êtres humains.

Vous pouvez utiliser l'IA comme partenaire de réflexion en lui demandant de remettre en question vos hypothèses, de proposer des alternatives et d'identifier ce que vous avez manqué. Voici quelques façons de procéder :

- Partagez une spécification technique ou une décision d'architecture (ADR) avec un grand modèle de langage (LLM). Demandez-lui de mettre l'idée à l'épreuve.
- Préparez-vous à une conversation difficile avec des parties prenantes ou votre manager en rédigeant un script de ce que vous voulez dire, puis demandez au LLM de vous donner un retour et de vous aider à l'affiner. Une fois le script affiné, répétez-le à voix haute jusqu'à ce qu'il vous paraisse naturel !
- Partagez un problème précis, en l'expliquant le plus clairement possible, et demandez au LLM de proposer des pistes de solution. S'efforcer d'expliquer clairement le problème à un LLM produit non seulement de meilleures solutions, mais affine aussi votre propre compréhension.
- Demandez à l'IA de relire ce que vous écrivez. Appliquez ses modifications proposées manuellement afin de pouvoir y réfléchir et les adapter à votre propre style et à votre propre voix.

## Derniers mots

Terminons cet article avec ceci :

L'objectif de l'ingénierie n'a jamais été de tout faire soi-même. Les ingénieurs ont toujours utilisé des outils pour libérer du temps pour un travail à plus fort effet de levier, et les LLM ne sont que des outils plus puissants dont les résultats sont beaucoup moins prévisibles.

Alors, utilisez-les à votre avantage, en particulier pour apprendre quelque chose de nouveau plus rapidement ! Vous allez y arriver.

Cet article vous a plu ? Pensez à cliquer sur le bouton « j'aime ».

Un retour ou une suggestion ? Laissez un commentaire.

Vous connaissez quelqu'un que cela pourrait aider ? Partagez cet article.

## Dès que vous êtes prêt, voici comment je peux vous aider davantage

- Intéressé pour sponsoriser cette newsletter ? Consultez les options de sponsoring ici.
- Découvrez mon livre « The Multiplier Mindset », à paraître plus tard cette année, ici.
- Jetez un œil aux goodies de l'Engineering Leadership Store ici.
- Vous voulez travailler avec moi ? Vous pouvez voir toutes les options ici.

## Me contacter

Vous pouvez me trouver sur LinkedIn, X, YouTube, Bluesky, Instagram ou Threads.

Si vous souhaitez faire une demande sur un sujet particulier que vous aimeriez lire, vous pouvez m'envoyer un email à info@gregorojstersek.com.

Cette newsletter est financée par les abonnements payants de lecteurs comme vous.

Si vous ne l'êtes pas déjà, pensez à devenir abonné payant pour profiter de l'expérience complète !

Vous êtes plus que bienvenu pour explorer ce qui vous intéresse ici et l'essayer dans votre propre contexte. Faites-moi savoir comment ça s'est passé ! Les sujets traitent généralement de tout ce qui touche à l'ingénierie, au leadership, au management, au développement de produits scalables, à la construction d'équipes, etc.

## Pourquoi ça compte
Cet article dépasse le simple "tips & tricks" : il propose un cadre (réfractaires/sur-dépendants/multiplicateurs) et des prompts réutilisables pour transformer l'IA en accélérateur d'apprentissage plutôt qu'en béquille, un sujet central pour toute équipe tech qui adopte massivement les outils de codage IA. Il est particulièrement utile pour une veille sur les pratiques d'ingénierie et de management à l'ère des LLM.
