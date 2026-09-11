---
title: "You don't have ICs anymore, you have managers (Emilie Schario)"
date: 2026-09-11
url: "https://substack.com/app-link/post?publication_id=370988&post_id=214955808&utm_source=post-email-title&utm_campaign=email-post-title&isFreemail=true&r=7v5lmc&token=eyJ1c2VyX2lkIjo0NzU1OTI2MjgsInBvc3RfaWQiOjIxNDk1NTgwOCwiaWF0IjoxNzg5MDQ1Nzk5LCJleHAiOjE3OTE2Mzc3OTksImlzcyI6InB1Yi0zNzA5ODgiLCJzdWIiOiJwb3N0LXJlYWN0aW9uIn0.-xTtAv7o9yWbp3y_5rf1SbQYiuQU5zWPtkQ7pOOKyC0"
authors: ["Emilie Schario", "Tristan Handy"]
keywords: ["agents IA", "model-agnostic", "management d'équipe", "ingénierie produit", "recrutement junior", "dbt Labs"]
theme: "IA"
tone: "opinion"
used_in: ["2026-09-11"]
---

## Résumé

Emilie Schario, cofondatrice de Kilo Code (plateforme d'agents de codage open source et model-agnostic, rachetée par Anaconda en juillet 2026), explique dans cet entretien comment son équipe d'une vingtaine d'ingénieurs fonctionne sans quasiment aucun poste "produit" dédié : chaque ingénieur possède son périmètre de bout en bout et pilote en parallèle une flotte d'agents IA, ce qui, selon elle, transforme mécaniquement le métier d'individual contributor en métier de manager. Elle défend aussi le choix stratégique de Kilo de rester compatible avec plus de 500 modèles plutôt que de parier sur un seul fournisseur, un choix motivé non par la peur du lock-in mais par la volonté de garder la liberté de choisir le bon modèle au bon moment. L'échange aborde également le problème non résolu du recrutement des profils juniors dans une organisation entièrement distante et "AI-native", et se termine par un retournement : selon elle, ce sont les "data people", habitués depuis longtemps à jongler entre des demandes multiples (marketing, finance, direction), qui seraient mieux préparés que les développeurs classiques à ce futur où chacun gère un portefeuille d'agents.

## Points clés

- Chez Kilo, ~20 ingénieurs et une seule personne avec "produit" dans son titre : chacun possède sa feuille de route, son support et ses bugs, ce qui ne fonctionne, selon Emilie Schario, que parce que chaque ingénieur encadre aussi une équipe d'agents IA.
- Thèse centrale : le rôle d'individual contributor est en train de disparaître au profit d'un rôle de manager, que l'on encadre des humains, des agents, ou les deux.
- Kilo mise sur le "model-agnostic" (500+ modèles supportés, relations directes et anticipées avec les labs) pour préserver la liberté de choisir l'outil adapté à chaque tâche, plutôt que par crainte d'un verrouillage fournisseur.
- Le virage du secteur, de la maximisation de la consommation de tokens vers un ROI IA mesuré et une dépense plus efficace, conforte selon elle la pertinence du multi-modèle.
- Le recrutement de profils juniors reste un problème non résolu dans une organisation entièrement distante et composée uniquement de seniors (10 à 15 ans d'expérience minimum chez Kilo).
- Argument final : les professionnels de la data, habitués à être "multi-threaded" entre des demandes contradictoires depuis des années, seraient mieux préparés à gérer plusieurs agents en parallèle que les développeurs logiciels classiques.

## Analyse approfondie

### Qui est Emilie Schario

Emilie Schario a fait ses débuts dans la donnée chez GitLab, où elle a occupé plusieurs postes au sein de l'équipe data engineering, avant de diriger l'organisation data de Netlify. Elle a ensuite passé un an chez Amplify Partners comme "data-strategist-in-residence", conseillant les startups du portefeuille sur leurs premières embauches et stack data, avant de fonder Turbine, une startup ERP rachetée par la suite par Settle. Elle a rejoint Kilo initialement pour dépanner temporairement en tant que CEO, à la demande de Sid Sijbrandij (président exécutif de GitLab), avant de s'engager durablement comme cofondatrice, responsable produit et ingénierie. Kilo a été racheté par Anaconda deux à trois semaines avant l'enregistrement de cet épisode.

### "Kilo speed" : une discipline culturelle délibérée

Emilie décrit "kilo speed" comme la sensation d'un trajet vers le travail sans jamais tomber sur un feu rouge : tout avance sans friction, sans process inutile, sans checklist qui existerait juste pour exister. Elle insiste sur le fait que ce n'est pas un sous-produit naturel du fait d'être une entreprise IA, mais une décision prise en continu par l'équipe, aussi bien dans la façon de gérer un canal Slack ou un email que dans la façon de livrer une fonctionnalité. C'est un critère de recrutement autant qu'une valeur affichée.

### Un modèle d'organisation inhabituel : le "product engineer" généralisé

L'organisation compte environ 20 ingénieurs et une seule personne portant le mot "produit" dans son titre, en charge d'une brique d'infrastructure partagée. Chaque autre ingénieur possède entièrement son périmètre : c'est lui qui définit la feuille de route, répond aux retours utilisateurs sur Discord, gère les tickets de support et les bugs remontés. Ce que d'autres entreprises appelleraient un poste réparti entre quatre à dix personnes (PM, support, ingénierie, etc.) est ici tenu par une seule, précisément parce que cette personne dispose en permanence d'une équipe d'agents IA travaillant avec elle. Emilie résume ce changement en disant qu'on ne "finit plus sa journée avec un joli nœud" comme au début de sa carrière : on termine désormais la journée en lançant des agents pour la nuit, on en relance d'autres le matin, et on passe son temps à réviser ce que les précédents ont produit. D'où sa formule : "vous n'avez plus des ICs, vous avez des managers", que l'on gère des personnes, des agents, ou les deux.

### Le pari model-agnostic : une question d'optionalité, pas de peur du lock-in

Plutôt que de construire sur la pile technologique d'un seul laboratoire, Kilo prend en charge plus de 500 modèles et entretient des relations directes avec la plupart des grands labs, testant parfois des modèles non publiés pendant plusieurs semaines, ajustant le prompt système de Kilo pour chacun, et renvoyant des retours d'usage réels avant leur sortie publique. Quand l'argument est comparé à la thèse de dbt Labs en faveur d'une infrastructure data ouverte et indépendante du compute, Emilie nuance : pour la donnée, la crainte porte sur un verrouillage à la Oracle. Pour les modèles, le sujet est différent : personne ne sait quel sera le meilleur modèle, ou le meilleur rapport qualité-prix, dans trois mois, donc rester ouvert vise avant tout à préserver la liberté de choisir le bon outil pour la bonne tâche, à mesure que la frontière technologique avance. Elle illustre cela avec l'Agent Manager de Kilo, qui permet de donner exactement le même prompt à plusieurs modèles en parallèle, chacun tournant dans un git worktree séparé pour éviter les collisions, uniquement pour observer leurs différences de performance. Elle relève aussi un changement de climat sectoriel : plus tôt dans l'année, la conversation portait sur la maximisation de la consommation de tokens ; au moment de l'entretien, elle a basculé vers une dépense IA efficace et la mesure d'un vrai retour sur investissement, ce qu'elle lit comme une validation de la thèse multi-modèle plutôt que comme une contradiction.

### Le problème non résolu des profils juniors

Tous les ingénieurs de Kilo ont au moins dix ans d'expérience professionnelle (la moyenne est de 15 ans), dans une organisation entièrement distante. Emilie reconnaît ouvertement ne pas savoir comment intégrer des profils juniors dans une organisation distribuée et "AI-native" : les apprentissages informels qui se transmettent en présentiel (elle cite l'exemple d'avoir appris ce qu'était une window function lors d'un échange en personne) sont beaucoup plus difficiles à transmettre à distance. Elle se dit optimiste quant à la capacité du secteur à résoudre ce problème, sans prétendre l'avoir déjà résolu elle-même, et cite des initiatives comme Ember Fellows (héritier de Venture for America, fermé depuis) qui réintroduisent volontairement une composante en présentiel.

### Parcours : Netlify, Amplify Partners, Turbine

Sur Netlify, elle évoque son inquiétude quant à la suite de sa carrière après avoir dirigé une équipe data impactante, dont plusieurs membres ont ensuite rejoint dbt Labs ou Brooklyn Data Co. Chez Amplify Partners, son rôle de conseil transverse au portefeuille (aide au recrutement des premiers profils data, structuration de la stack, retours produits pour des startups comme Hex ou Hightouch) lui a beaucoup plu mais lui a aussi fait prendre conscience de son besoin d'appartenir à une équipe et de construire un produit au quotidien. Sur son expérience de fondatrice d'ERP avec Turbine, elle tire une leçon dure : concurrencer NetSuite exige des moyens considérables, et la bataille est autant culturelle que technologique — convaincre des acteurs installés depuis longtemps que NetSuite n'est pas une fatalité s'est révélé, dans son propre aveu, un problème qu'elle n'a jamais résolu.

### L'histoire de Kilo

Kilo a été fondée par JP Posma, qui a dû s'effacer pour des raisons familiales alors qu'il travaillait sur le Vesuvius Challenge avec Nat Friedman et Sid Sijbrandij. Sid a alors demandé à Emilie, qui venait de quitter Settle, de prendre temporairement la direction de l'entreprise. Ce qui devait être un dépannage court est devenu un engagement permanent après qu'elle a fait venir Scott Breitenother comme CEO permanent — les deux dirigeants échangent depuis, dit-elle, une dizaine de fois par jour. Scott a fait passer l'entreprise d'un projet open source avec quelques fonctionnalités commerciales à une véritable plateforme d'ingénierie agentique, jusqu'au rachat par Anaconda.

### Origines open source et différenciation face à Claude Code ou Codex

À ses débuts, Kilo était un fork d'un fork : Cline (agent de codage open source qui n'acceptait pas les contributions communautaires) a été forké par Roo pour construire une vraie communauté, puis Kilo a lui-même forké Roo. Kilo n'est aujourd'hui plus un fork de Roo et s'appuie en partie sur l'open code server depuis février de la même année. La différence avec Claude Code (Anthropic) ou Codex, selon Emilie, est que ces outils sont liés aux modèles de leur propre laboratoire : changer de labo oblige à changer de logiciel. Kilo, disponible en extension VS Code, JetBrains, en interface web, CLI, application mobile et extension navigateur, vise à rendre ce changement de modèle transparent pour l'utilisateur.

### Modèle économique

L'usage individuel de Kilo est gratuit ; les équipes et entreprises paient un prix par poste et par mois pour les fonctionnalités logicielles. Pour l'usage des modèles eux-mêmes, l'utilisateur peut apporter sa propre clé (Anthropic, OpenRouter, etc.), payer à l'usage, ou souscrire un "Kilo Pass" mensuel avec des crédits bonus.

### Conclusion : le parallèle avec les "data people"

Interrogée sur ce que les développeurs logiciels font aujourd'hui que les professionnels de la donnée n'ont pas encore rattrapé, Emilie retourne la question : ce sont selon elle les data people qui ont, depuis des années, l'habitude d'être sollicités simultanément par le marketing, la direction et la finance, une situation dont les développeurs ont longtemps été protégés. Si gérer plusieurs agents en parallèle est fondamentalement un problème de management, les analytics engineers — "managers d'eux-mêmes" depuis toujours, sans PM ni designer pour absorber les sollicitations extérieures — pourraient être mieux préparés à ce nouveau monde que les développeurs qui construisent aujourd'hui les outils IA.

## Pourquoi ça compte

Ce témoignage illustre concrètement comment l'adoption d'agents IA reconfigure déjà l'organisation du travail d'ingénierie (fusion des rôles produit/ingénierie, disparition du poste d'IC classique) et pose la question, encore ouverte, de la formation des profils juniors dans des équipes entièrement distantes et orientées IA — deux signaux utiles à suivre pour toute veille sur l'impact organisationnel de l'IA générative.
