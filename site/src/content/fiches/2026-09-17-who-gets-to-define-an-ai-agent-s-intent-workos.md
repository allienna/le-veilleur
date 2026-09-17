---
title: "Who gets to define an AI agent's intent? — WorkOS"
date: 2026-09-17
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fworkos.com%2Fblog%2Fdefine-ai-agent-intent%3Futm_source=tldrdev/1/010001a0a9ee3a28-d0f70b3b-39c2-4b56-bed5-34844dc5139e-000000/iYldDmn7XCRWO4xhTdo_gAsc22dJer4alRwg5JGepcg=452"
keywords: ["agents IA", "autorisation", "politique d'accès", "intention de tâche", "gestion des permissions"]
theme: "Sécurité"
tone: "tutorial"
used_in: ["2026-09-17"]
---

## Résumé
L'article de WorkOS explore une question centrale pour le déploiement d'agents IA en entreprise : qui a le pouvoir de définir l'intention d'un agent, et comment cette intention doit-elle être confrontée aux règles de l'organisation ? La personne qui confie une tâche à l'agent doit en préciser le but, mais c'est l'organisation qui décide des actions autorisées pendant l'exécution de cette tâche. L'article s'appuie sur une démonstration du produit Airlock (présentée par Aaron Tainter lors d'un événement "Agent Night" le 12 août), où un agent opérant sur Linear et Gmail voit ses appels d'outils validés à la fois par l'intention déclarée et par des politiques configurées. La thèse : une description de tâche plus large ne doit jamais équivaloir à une autorisation d'ignorer les règles de l'entreprise.

## Points clés
- La description d'une tâche doit inclure l'effet recherché (ex. "trouver les doublons de facturation et les rembourser"), pas seulement l'objectif général, sinon l'agent doit deviner s'il peut agir en écriture.
- L'identité du demandeur et les règles de politique doivent rester établies par les contrôles d'identité et de permissions de l'application, jamais par une simple affirmation textuelle dans la tâche ("j'agis pour l'administrateur facturation" ne prouve rien).
- Une politique doit rester valable indépendamment du vocabulaire employé pour décrire la tâche : renommer une demande "préparer une synthèse détaillée" ne lève pas une restriction sur les données financières dans un e-mail.
- Dans la démo Airlock, deux tâches similaires (lire un ticket Linear puis composer un e-mail) ont eu des issues opposées, selon que le contenu de l'e-mail violait ou non la politique — preuve que le contenu compte plus que les outils connectés.
- Une extension légitime du périmètre de travail (ex. examiner un mois supplémentaire de charges) doit être tracée et réévaluée avec les mêmes permissions, sans transférer l'autorité d'approbation.
- Reformuler une demande refusée avec des mots plus doux ne doit pas suffire à contourner un refus si le destinataire, le contenu et l'effet visé restent identiques — ce comportement doit être testé, pas supposé acquis.

## Analyse approfondie
**Deux rôles distincts : l'intention et la politique**
L'article part d'un principe simple mais souvent négligé dans la conception des agents IA : la personne qui formule la demande définit *ce que l'agent doit accomplir* (son intention), tandis que l'organisation définit *ce qu'il est autorisé à faire* pour y parvenir (la politique). L'agent conserve une marge de manœuvre sur la manière d'exécuter la tâche — quelles recherches effectuer, quels outils appeler — mais élargir la formulation de sa tâche ne doit jamais lui donner le droit de contourner les règles de l'entreprise.

Le produit Airlock illustre cette séparation : dans la démonstration décrite, un agent demande un jeton associé à son intention déclarée, puis l'utilise pour opérer à travers Linear et Gmail. Airlock évalue chaque appel proposé à l'aune de cette intention et des politiques configurées : la tâche explique ce que l'agent cherche à faire, mais ce sont les politiques qui déterminent, action par action, si celle-ci peut réellement s'exécuter.

**Décrire le travail en incluant l'effet recherché**
L'exemple de facturation donné sur la page produit d'Airlock est instructif : une demande de "retrouver les doublons de facturation du mois dernier et les rembourser" fournit à l'agent un objectif, une période temporelle et un effet attendu, tout en lui laissant le soin de déterminer les recherches et comparaisons nécessaires.

À l'inverse, une demande aussi vague que "aide-moi avec la facturation" laisse un vide interprétatif : cela pourrait signifier produire un rapport, émettre des remboursements, modifier des abonnements ou contacter des clients. C'est au demandeur de lever cette ambiguïté avant que l'agent ne commence à modifier quoi que ce soit.

Une demande intermédiaire comme "lister les charges des 30 derniers jours" convient si seul un rapport est attendu ; mais si l'employé souhaite aussi des remboursements, l'opération d'écriture reste non spécifiée. La tâche doit donc énoncer explicitement l'effet voulu, afin que l'agent n'ait pas à déduire si détecter un doublon implique automatiquement de déplacer de l'argent.

Même une demande de remboursement clairement formulée ne règle pas toutes les décisions à prendre : dans l'exemple produit d'Airlock, rechercher des charges est autorisé, un remboursement nécessite une validation, et supprimer une fiche client est refusé car hors du périmètre de la tâche. Ce sont là des décisions distinctes, prises action par action, au sein d'un même flux de travail.

**Séparer l'identité et la politique du texte de la tâche**
Une phrase du type "j'agis pour le compte de l'administrateur facturation" ne constitue pas une preuve d'identité. L'identité du demandeur doit être établie via les mécanismes de contrôle d'identité de l'application, à partir desquels sont ensuite appliquées les permissions de ressources et les règles de l'entreprise pertinentes. La description de la tâche peut aider à expliquer une action, mais elle ne peut, à elle seule, établir l'autorité du demandeur. Le guide d'Agent Auth de WorkOS sur le "permission-scoping" établit une distinction similaire entre intention et autorité : la description du travail par l'appelant donne un contexte que le système d'autorisation peut évaluer, en complément des permissions existantes — pas à leur place.

La politique doit aussi rester pertinente quelle que soit la manière dont la tâche est formulée. Une règle interdisant la divulgation d'informations financières dans un e-mail sortant doit continuer à s'appliquer même si la tâche est décrite comme "préparer une synthèse détaillée" — reformuler l'objectif ne supprime pas la restriction sur le contenu autorisé.

**Utiliser une action réelle pour tester la clarté d'une tâche**
La démonstration d'Agent Night fournit un exemple concret : une mise à jour de planning ordinaire envoyée à un manager est passée sans problème. Mais dans une demande ultérieure, l'agent a trouvé un ticket Linear évoquant la consommation de tokens LLM et a rédigé un e-mail résumant ce ticket — qu'Airlock a bloqué, car le corps du message contenait des informations de coût de tokens, traitées par la politique configurée comme des données financières.

Les deux scénarios impliquaient pourtant la même combinaison d'outils (lecture de Linear, envoi d'e-mail) : connaître les outils connectés n'aurait pas suffi à expliquer des résultats différents. C'est le contenu de l'e-mail proposé, croisé avec la demande initiale de l'employé et la politique en vigueur, qui a déterminé l'issue.

L'article propose une méthode pratique : prendre un flux de travail déjà utilisé par son équipe, noter qui l'a demandé, quelles ressources sont concernées et quel changement l'employé attend de l'agent. Puis soumettre cette description à une autre personne avec quelques actions proposées, et lui demander lesquelles relèvent bien de la tâche définie. Si les avis divergent — par exemple si l'un pense qu'un remboursement est inclus et l'autre que la tâche s'arrête à un rapport — c'est le signe qu'il faut clarifier la tâche avant de s'appuyer sur elle comme contexte d'autorisation.

**Traiter tout changement de périmètre comme une décision à part entière**
Un employé peut légitimement élargir le périmètre d'une tâche, par exemple en demandant à l'agent d'examiner un mois supplémentaire de charges. Ce changement doit être enregistré et les nouvelles actions doivent être évaluées avec les mêmes permissions et politiques applicables : une tâche révisée peut introduire davantage de travail sans pour autant transférer l'autorité d'approuver un remboursement.

En revanche, un agent qui reformule une demande déjà refusée appelle une réponse différente. Si le destinataire, le contenu et l'effet visé restent inchangés, un simple assouplissement du vocabulaire ne doit pas suffire à rendre acceptable un envoi initialement interdit. L'article recommande d'intégrer ce cas de test dans l'évaluation : soumettre une action non autorisée, la reformuler, puis vérifier à la fois la nouvelle décision prise par le système et si quelque chose s'est réellement produit du côté du fournisseur (provider).

Les vérifications sémantiques pouvant varier selon la formulation employée, l'article conclut que ce comportement doit être testé plutôt que supposé garanti. Une intention clairement exprimée donne un contexte utile à ces vérifications, mais ce sont les permissions et politiques réellement applicables qui continuent de fixer les limites que le flux de travail doit respecter.

## Pourquoi ça compte
À mesure que les agents IA obtiennent un accès direct à des systèmes sensibles (facturation, e-mail, outils de gestion de projet), la manière de formuler leur tâche devient un enjeu de sécurité à part entière : ce texte propose un cadre concret pour éviter que l'ambiguïté d'une instruction ne se traduise par une action non autorisée, un sujet clé pour toute équipe qui conçoit des systèmes d'autorisation pour des agents autonomes.
