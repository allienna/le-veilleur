---
title: "The state of the tech industry in 2026"
date: 2026-10-12
url: "https://open.substack.com/pub/pragmaticengineer/p/the-state-of-the-tech-industry-in?utm_source=multiple-personal-recommendations-email&utm_medium=email&token=eyJ1c2VyX2lkIjo0NzU1OTI2MjgsInBvc3RfaWQiOjIxOTEyNTgzMCwiaWF0IjoxNzkxNzUwODExLCJleHAiOjE3OTQzNDI4MTEsImlzcyI6InB1Yi00NTg3MDkiLCJzdWIiOiJwb3N0LXJlYWN0aW9uIn0.M3uBaBAQA77DNR6sXRsdsESRjxJIuHnw3xnqiehdonk"
authors: ["Gergely Orosz"]
keywords: ["agents IA", "revue de code", "migrations logicielles", "industrie tech", "ingénierie", "IDE"]
theme: "Leadership"
tone: "opinion"
used_in: ["2026-10-12"]
---

## Résumé
Dans ce numéro de The Pragmatic Engineer, Gergely Orosz dresse un état des lieux de l'industrie tech en 2026, à partir de son keynote à la conférence LDX3 et de visites chez OpenAI, Anthropic, Ramp, Uber, GitHub, Linear et Factory AI. Sa thèse centrale : l'ampleur et la vitesse du changement provoqué par l'IA générative sont sans précédent, dépassant même l'arrivée d'internet ou du mobile selon Martin Fowler. L'auteur distingue ce qui a radicalement changé (écriture de code à la main en voie de disparition, multiplication des agents en parallèle, essor des PR générées par IA, disparition progressive de l'IDE), ce qui est cassé (revues de code devenues du théâtre, qualité en baisse, pénurie d'infrastructure, épuisement des dirigeants techniques) et ce qui reste stable (importance des équipes, de la planification, des tests, et le fait que les non-ingénieurs ne déploient toujours pas en production). Il conclut par des projections sur l'avenir proche du métier d'ingénieur logiciel.

## Points clés
- La vitesse de transformation induite par l'IA est jugée inédite par des figures comme Martin Fowler, dépassant l'impact de l'internet ou de l'agilité.
- L'écriture de code à la main devient marginale chez les ingénieurs les plus productifs, qui pilotent désormais 5 à 10 agents en parallèle (Claude Code, agents sur le web, worktrees multiples).
- Les PR et issues générées par des agents dépassent désormais en volume celles créées par des humains sur GitHub et Linear, et les migrations techniques qui prenaient des années se font en semaines ou mois (Anthropic, OpenAI, Airbnb, Asana, Uber).
- Les revues de code humaines sont décrites comme devenues « théâtrales » (approbations automatiques faute de temps), avec une qualité et une fiabilité logicielle perçues en baisse malgré la hausse de productivité.
- Les fondamentaux (équipes, planification, tests, responsabilité de la mise en production réservée aux ingénieurs) restent largement inchangés, et les anciennes bonnes pratiques (tests unitaires, « tracer bullet », architecture amont) redeviennent pertinentes pour bien guider les agents.
- L'auteur anticipe une généralisation des agents de code dans le cloud, une diminution de la lecture du code par les ingénieurs, de nouvelles infrastructures internes agentiques, et une valorisation croissante de l'expertise métier (« wisdom ») face à une intelligence technique rendue banale par l'IA.

## Analyse approfondie
**1. La vitesse du changement.** Orosz rappelle les grandes ruptures technologiques passées (internet, mobile, cloud, nouveaux langages comme Go et Rust, frameworks comme React) pour souligner que l'impact actuel de l'IA leur est supérieur en ampleur et en rapidité. Martin Fowler, cité lors du Pragmatic Summit, affirme que rien n'a jamais eu un tel poids : contrairement à l'agilité ou à la programmation orientée objet, personne ne conteste aujourd'hui l'importance de l'IA. Pour Orosz, l'industrie entre dans une transformation technologique majeure qui va changer durablement la façon de construire des logiciels, même si certains aspects du métier perdureront.

**2. Ce qui a changé** (16 constats, dont les principaux) :
- *Plus personne n'écrit de code à la main* : tendance devenue massive depuis fin 2025, avec les modèles d'IA désormais très performants en code ; débat public relancé par le créateur de Ruby on Rails sur « la mort du codage manuel ».
- *Le travail en agents parallèles se généralise* : Boris Cherny (créateur de Claude Code) utilise 5 terminaux avec Claude Code en parallèle plus 5 à 10 instances sur le web ; Peter Mattis (Cockroach Labs) gère 5 à 10 sessions d'agents simultanées ; Dima Zaytsev (Linear, ex-Uber) alterne entre 5 à 10 worktrees locaux.
- *Explosion des PR générées par agent* : selon des données inédites de GitHub, les PR créées par des agents ont dépassé en volume celles créées par des humains dès août 2026, avec environ 75 millions de PR générées par IA par mois contre 25 millions de PR humaines fin 2023.
- *Les tickets générés par agents progressent aussi*, notamment via le support MCP de Linear pour la création agentique d'issues.
- *L'usage des « agent skills » devient courant*, avec des entreprises qui créent leurs propres répertoires de compétences partagées (donnée confirmée par Factory AI).
- *L'IDE s'efface* : Steve Yegge (podcast cité) juge que rester sur un IDE classique relève d'une « mauvaise pratique » d'ingénierie et décrit une échelle en huit niveaux d'usage de l'IA, du niveau zéro jusqu'à l'orchestration de dizaines, voire centaines, d'agents. Des exemples concrets : Antigravity (dernier IDE basé sur VS Code lancé en novembre 2025, puis abandonné dans sa version 2.0), Codex lancé hors format IDE en février 2026, Cursor qui a supprimé son interface IDE en avril 2026, JetBrains qui bascule vers des environnements agentiques avec JetBrains Air. Kent Beck estime que ce n'est pas le besoin de contexte qui a disparu, mais sa nature qui a changé.
- *Chaque entreprise construit son propre « harness » d'agents* : exemples cités chez Ramp (Inspect), Stripe (Minions), Uber (Minion), Block (Goose), Shopify (River), Google (Agent Smith), Meta (Devmate), Amazon (Kiro + Crew), Dropbox (Nova), Spotify (Honk), DoorDash (Flux), Grab (LLM-Kit), WorkOS (Horizon), Hubspot (Crucible), Monzo (Agent Chip), Sierra (Pinecone), Harvey (Spectre), Browserbase (bb).
- *Le développement démarre souvent dans Slack* (« @Codex, implémente ceci » chez OpenAI, « @Claude » chez Anthropic, « @Linear » chez Linear), avec des agents cloud déclenchés directement depuis la messagerie.
- *Des « usines logicielles agentiques » émergent* partout, intégrant l'IA au CI/CD, à la revue de code, au déploiement (exemple de l'« Agentic Deploy System » et de la « Perf Factory » chez OpenAI).
- *Les migrations ne prennent plus des années* : Bun migré de Zig à Rust en 11 jours chez Anthropic (contre ~1,5 an estimé), API d'OpenAI migrée de Python à Rust en ~5 mois, 3 500 fichiers de tests migrés d'Enzyme à React Testing Library chez Airbnb en 6 semaines, 4 000 fichiers chez Asana en 2 semaines, 600 000 tests JUnit 4 migrés vers JUnit 5 chez Uber (15 millions de lignes de code) en 4 mois.
- *Le coût de l'IA devient un sujet d'ingénierie central* : recours croissant à des modèles ouverts et au routage intelligent de modèles pour réduire les coûts de token de plus de 50 %, exemple d'Uber qui maintient ses coûts stables malgré une hausse d'usage.
- *Des projets entiers sont menés par seulement un ou deux ingénieurs*, chacun pilotant plusieurs agents (témoignage de Katelyn Lesse, Head of Engineering chez Claude Platform/Anthropic).
- Autres tendances listées : disparition des spécialisations (iOS, Android, frontend) au profit de profils généralistes ; réduction de la taille des équipes ; recrutement de juniors en baisse ; émergence de l'« infrastructure agentique » comme discipline à part entière.

**3. Ce qui est cassé.**
- L'hypothèse d'une croissance linéaire du volume de code est invalidée : lignes de code et nombre de commits croissent désormais de façon exponentielle (données GitHub).
- Les revues de code humaines sont qualifiées de « théâtre » : face au volume de changements, les ingénieurs valident massivement sans relecture approfondie (témoignage anonyme d'un ingénieur de startup), une situation confirmée par la réaction du public lors du keynote LDX3.
- Les revues effectuées uniquement par des agents IA progressent (donnée Linear).
- La qualité et la fiabilité logicielle perçues sont en baisse : Mario Zechner (créateur de Pi) évoque un « 98 % de disponibilité » devenu la norme et des bugs d'interface inattendus, un phénomène déjà discuté en mars dans un article sur le ralentissement potentiel causé par les agents IA.
- Pénurie d'infrastructure : au-delà du manque de GPU et de mémoire déjà connu, une pénurie de CPU se développe, rendant les réservations de capacité de plus en plus difficiles et coûteuses ; l'auteur recommande de sécuriser des capacités fixes dès maintenant.
- Impact sur la concentration et la charge de travail individuelle : Dima Zaytsev décrit une multiplication du « context switching » et un sentiment de charge de travail accrue malgré les gains de productivité individuels.
- Des cadres techniques (CTO, VP Engineering) démissionnent sans poste suivant pour retourner à des rôles de développeur individuel, motivés par l'envie de « reconstruire » avec les nouveaux outils (témoignage anonyme d'un CTO), phénomène développé dans un autre article de la newsletter.

**4. Ce qui reste identique.**
- Les équipes restent structurantes : Katelyn Lesse insiste sur le maintien du modèle des « two-pizza teams », même dans une organisation très avancée dans l'usage de l'IA.
- La planification demeure essentielle pour les projets complexes, comme l'illustre le processus de conception du produit « Managed Agents » chez Anthropic, construit sur des idées mûries pendant deux ans.
- Les tests et la validation gardent toute leur importance : Jarred Sumner (créateur de Bun, chez Anthropic) souligne que l'IA écrit le code et les tests, mais que le temps consacré à la fiabilisation reste comparable à l'ère pré-IA.
- Les non-ingénieurs ne déploient toujours pas en production : Orosz n'a trouvé aucune entreprise où des PM ou designers publient directement du code ; ils créent des correctifs ou prototypes relus ensuite par des développeurs.
- D'anciennes pratiques d'ingénierie refont surface pour mieux guider les agents : inspiré par Matt Pocock et le concept de « tracer bullet » issu de The Pragmatic Programmer, l'auteur observe un regain d'intérêt pour les tests unitaires, le « chemin critique » (golden path) et l'architecture amont, des pratiques pourtant anciennes.

**5. Et ensuite ?**
- Les agents de codage dans le cloud et les « harness » dédiés devraient devenir la norme plutôt que l'usage local, avec Ramp (Inspect) comme référence et une offensive attendue d'Anthropic, OpenAI et d'autres fournisseurs.
- Les ingénieurs liront de moins en moins le code produit par les agents : Charity Majors (Honeycomb) interpelle sur ce que signifierait livrer du code sans le comprendre, notant que les équipes Ops et QA ont déjà appris, depuis des décennies, à livrer du code qu'elles n'ont pas écrit.
- De nouveaux types d'infrastructures internes émergeront : CI/CD intégrant des évaluations agentiques, usines logicielles agentiques, agents impliqués dans le déploiement, l'observabilité et la gestion d'incidents, avec l'observabilité agentique comme nouvelle spécialité.
- On entre dans un « âge d'or » des migrations et refontes, désormais réalisables en semaines plutôt qu'en années, réduisant les excuses pour ne pas traiter la dette technique.
- La « positivité IA » devient un critère de recrutement dans certaines startups, au même titre que l'adhésion à une culture de croissance rapide.
- L'expertise métier (la « sagesse », selon Titus Winters, auteur principal de Software Engineering at Google) gagnera en valeur à mesure que l'intelligence technique brute, rendue accessible par l'IA, se banalise.
- L'auteur termine sur une note personnelle, relayant Peter Mattis (Cockroach Labs) qui invite chacun à se rappeler pourquoi il a choisi ce métier : construire, désormais plus vite et avec moins de compromis.

En commentaires, plusieurs lecteurs interrogent la méthodologie de l'article : s'agit-il surtout de nouveaux projets ou de maintenance ? la qualité du code a-t-elle été mesurée sur la durée (6 mois ou plus) ? les entreprises interrogées ont-elles intérêt à surestimer l'impact de l'IA ? existe-t-il des enquêtes de satisfaction des employés ? la productivité accrue se traduit-elle réellement en revenus ou en profits ? Un lecteur souligne aussi l'écart croissant entre praticiens et théoriciens de l'ingénierie logicielle, source de gaspillage (par exemple la demande de CPU), et s'interroge sur l'absence de mesure du « AI slop » (code produit en excès et de faible valeur) et sur la question de savoir si plus de code produit signifie réellement plus de valeur business.

## Pourquoi ça compte
Ce panorama, construit à partir d'entretiens directs avec Anthropic, OpenAI, GitHub, Linear et des praticiens de référence, offre un instantané daté et sourcé des mutations concrètes du métier d'ingénieur logiciel sous l'effet des agents IA — utile pour calibrer sa propre adoption d'outils agentiques et anticiper les débats (qualité, revue de code, organisation des équipes) qui touchent toute équipe tech en 2026.
