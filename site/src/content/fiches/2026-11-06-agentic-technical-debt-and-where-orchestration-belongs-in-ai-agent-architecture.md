---
title: "Agentic Technical Debt and Where Orchestration Belongs in AI Agent Architecture"
date: 2026-11-06
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.kai-waehner.de%2Fblog%2F2026%2F11%2F03%2Fagentic-technical-debt-and-where-orchestration-belongs-in-ai-agent-architecture%2F%3Futm_source=tldrdev/1/010001a1abacb0ca-2f786ad4-8d6e-4c43-9b3e-cd5994e35b49-000000/YM2altatFRynNt_j7WKT-vDfP7WHjQx4UadhkMFyKX4=452"
authors: ["Kai Waehner"]
keywords: ["agents IA", "dette technique", "orchestration", "durable execution", "gouvernance IA"]
theme: "IA"
tone: "opinion"
used_in: ["2026-11-06"]
---

## Résumé
L'article compare la « dette technique des agents IA » à la dette technique du ML décrite par Google en 2015 (NeurIPS) : le modèle n'est qu'une petite partie d'un système bien plus vaste (prompts, outils, mémoire, retries, approbations, budgets, audit). L'auteur affirme que cette dette provient surtout d'un mauvais placement de ces responsabilités dans la mauvaise couche architecturale, et propose une matrice des couches (modèle, harness d'agent, exécution durable, plan de contrôle d'orchestration) avec la responsabilité qui revient à chacune. Il illustre son propos avec un cas concret de litige de facture fournisseur et l'outil open source Kestra.

## Points clés
- Gartner anticipe que 40% des applications d'entreprise intégreront des agents IA spécialisés fin 2026 (contre moins de 5% en 2025), mais prévoit aussi l'annulation de plus de 40% des projets d'agents IA d'ici fin 2027 (coûts, valeur métier floue, contrôles de risque insuffisants).
- Chez Camunda (sondage 2026, 1150 décideurs IT/métier/architectes), 71% utilisent déjà des agents IA mais seulement 11% des cas d'usage agentiques ont atteint la production en un an.
- Quatre couches architecturales à distinguer : le modèle (LLM/decision model), le harness de l'agent (boucle de contrôle, outils, mémoire, sandbox), l'exécution durable (type Temporal, pour survivre aux pannes/redémarrages), et le plan de contrôle d'orchestration unifié (approbations, budgets, audit, compensation inter-systèmes).
- Les erreurs de placement les plus fréquentes : règles d'approbation cachées dans un prompt, retries sur des effets de bord dans la boucle de l'agent (double envoi de documents), audit limité aux traces d'un seul framework, gouvernance dupliquée dans chaque outil vendeur.
- Exemple détaillé : un litige de facture fournisseur orchestré avec Kestra, où l'agent LLM ne fait qu'une étape bornée (proposition de résolution) sous contrôle humain et traçabilité complète.
- À mesure que les modèles se banalisent, la valeur se déplace vers les couches qui détiennent l'état du processus, les approbations et le journal d'audit — plus difficiles à remplacer une fois le processus construit autour d'elles.

## Analyse approfondie

**Le point de départ : l'héritage du papier Google de 2015**
L'auteur part du constat établi par des ingénieurs de Google dans « Hidden Technical Debt in Machine Learning Systems » (NeurIPS 2015) : le code ML proprement dit n'est qu'une petite boîte au sein d'un système bien plus large consacré à la collecte de données, la configuration, le service et la supervision. L'essentiel du coût de la mise en production se trouve hors de cette boîte. Pour les agents IA, le même schéma se répète : l'appel au modèle est la nouvelle « petite boîte », entourée de prompts, d'outils, de mémoire, de retries, d'approbations, de permissions, de budgets et de pistes d'audit.

**Définition de la dette technique agentique**
Elle correspond au coût cumulé des raccourcis pris autour des agents IA, lorsque prompts, câblage d'outils, mémoire, logique de contrôle et règles de gouvernance sont assemblés plus vite que les équipes ne peuvent les tester, les standardiser et les auditer. Plusieurs publications de 2026 (équipes de plateforme comme travaux académiques) cataloguent ces types de dette, mais la vraie question architecturale est de savoir où chaque responsabilité doit vivre pour éviter qu'elle ne s'accumule.

Les agents accumulent cette dette plus vite que les modèles de ML classiques, pour quatre raisons : sortie non déterministe (même entrée, résultats différents, rendant les tests et la non-régression plus difficiles) ; actions sur des systèmes réels (ERP, emails, infrastructure — une erreur a des effets de bord concrets) ; état de longue durée (le travail s'étale de quelques minutes à plusieurs jours, avec redémarrages et attentes humaines) ; multiplicité des propriétaires (chaque équipe et chaque éditeur d'application livre ses propres agents avec ses propres règles).

**Les couches d'une architecture d'agent IA en production**
L'article détaille quatre couches, chacune avec son rôle propre :
- *Modèle* : raisonne ou décide. Selon la tâche, il peut s'agir d'un LLM, d'un modèle de décision, d'un modèle ML entraîné ou de simples règles. Les LLM viennent d'Anthropic, OpenAI, Mistral (Europe), DeepSeek et Qwen d'Alibaba (Chine), entre autres ; les modèles de décision viennent de fournisseurs comme TypeSafe AI.
- *Harness d'agent* : l'environnement d'exécution autour du modèle pour un seul agent. Il exécute la boucle de contrôle, appelle les outils, assemble le contexte, gère la mémoire et isole l'exécution (sandbox). Le raccourci « Agent = Modèle + Harness », popularisé par LangChain, est devenu courant. Des frameworks comme LangGraph, l'OpenAI Agents SDK, Google ADK et AWS Strands fournissent les briques de base.
- *Exécution durable* : persiste chaque étape pour qu'une exécution longue survive aux pannes, redémarrages et attentes au sein d'une même application. Temporal en est l'exemple le plus connu, et fait tourner des graphes LangGraph ainsi que plusieurs SDK d'agents comme des workflows durables.
- *Plan de contrôle d'orchestration unifié* : un seul plan de contrôle pour les données, l'infrastructure, les applications et les processus métier. L'IA agentique est gouvernée à travers ces quatre domaines. Ce plan de contrôle démarre le travail à partir d'événements et de plannings, séquence les étapes à travers systèmes et équipes, et possède les approbations, les échéances, la compensation et la piste d'audit. Kestra est cité comme exemple.

Au-dessus de cette pile se trouve le « portail de décision » de l'intelligence des processus (process intelligence), qui décide quels processus méritent un agent et mesure l'impact après coup.

L'auteur insiste : un harness appartient à un seul agent, alors qu'un processus métier traverse agents, personnes et systèmes pendant des heures ou des jours. Chaque couche est utile ; la dette apparaît quand une couche empiète sur le rôle d'une autre. Les frontières entre couches bougent constamment car chaque fournisseur étend son territoire vers la couche voisine : les laboratoires de modèles ajoutent des fonctionnalités de harness à leurs SDK d'agents, les fournisseurs d'exécution durable ajoutent des intégrations d'agents, et les plateformes d'orchestration comme Kestra ajoutent des capacités d'exécution durable. Mais la question de la propriété de chaque responsabilité reste la même, quel que soit le produit qui héberge la couche.

**Où doit vivre chaque responsabilité**
L'article propose une matrice assignant les responsabilités courantes à la couche qui devrait les porter, indépendamment des produits choisis :
- *Choix du modèle* : l'étape d'orchestration décide du type de modèle nécessaire pour une tâche, le harness route l'appel (« décider en haut, router en bas »).
- *Permissions des outils et identité* : le harness les applique à chaque appel ; le plan de contrôle définit quelle identité et quels secrets une étape de workflow peut utiliser.
- *Retries et timeouts* : le harness relance les appels modèle/outil sans effet de bord. Les étapes qui modifient un système métier sont relancées par l'exécution durable ou le plan de contrôle, avec une clé d'identifiant métier pour qu'un retry ne puisse pas poster deux fois la même réservation.
- *État après panne* : l'exécution durable récupère l'état au sein d'une application ; le plan de contrôle récupère l'état à travers les systèmes.
- *Approbation humaine* : le plan de contrôle la possède comme une étape explicite, avec délai, chemin d'escalade et enregistrement de qui a approuvé quoi.
- *Budgets de coût et de tokens* : le harness plafonne une exécution unique ; le plan de contrôle applique des budgets par processus, équipe ou locataire. Les budgets limitent aussi les dégâts en cas de vol d'identifiants — dans les incidents de « LLMjacking » enquêtés par Mandiant en 2026, des attaquants ont généré plus de 100 000 dollars de frais de modèle en une seule journée.
- *Compensation à travers les systèmes* : le plan de contrôle la possède, car seul lui voit tous les systèmes touchés par le processus.
- *Déclencheurs événementiels et planifiés* : le plan de contrôle, par exemple en réagissant à des topics Kafka.
- *Audit et traçabilité (lineage)* : le plan de contrôle enregistre entrées, sorties, décisions et approbations de chaque étape à travers les quatre domaines.

**Les erreurs de placement les plus courantes créatrices de dette**
- Règles d'approbation dans le prompt : « Demander avant les remboursements de plus de 1000 euros » fonctionne dans un prompt système la plupart du temps, mais personne ne peut prouver que ça a fonctionné à chaque fois.
- Retries dans la boucle de l'agent autour d'effets de bord : un timeout sur un appel ERP pousse l'agent à réessayer, et le fournisseur reçoit deux notes de crédit.
- Audit limité aux traces d'un seul framework : chaque équipe voit son propre agent, mais personne ne peut reconstituer le processus de bout en bout pour un auditeur.
- Gouvernance dupliquée dans chaque boîte fournisseur : l'ERP, le CRM et le service desk livrent chacun des agents avec leurs propres garde-fous, mais le processus traverse tous ces outils et aucun jeu de règles unique ne le couvre.

**Étude de cas : litige de facture fournisseur**
L'article détaille un flux complet où chaque couche joue son rôle :
- Un événement de non-concordance de facture venu de l'ERP arrive sur un topic Kafka et démarre le workflow.
- Un rapprochement déterministe à trois voies (facture, bon de commande, réception) résout la plupart des cas sans IA.
- Un modèle de décision classe les litiges restants par type (prix, quantité, livraison manquante).
- Un agent LLM, dans son harness, dispose d'outils en lecture seule sur les contrats et l'historique des commandes ; il rédige une proposition de résolution et un message au fournisseur.
- Au-delà d'un certain montant, une personne du service comptabilité-fournisseurs approuve ou modifie la proposition ; sans réponse avant l'échéance, le cas est escaladé.
- La note de crédit part vers l'ERP et le message vers le portail fournisseur en parallèle ; si la mise à jour du portail échoue malgré les retries, le workflow annule la note de crédit et ouvre un dossier.
- Chaque étape, entrée, décision du modèle et approbation atterrit dans un seul enregistrement d'audit.

L'idée centrale : l'agent exécute une étape bornée au milieu d'un processus gouverné, et ne décide jamais seul si de l'argent doit bouger.

**Faire tourner le plan de contrôle avec Kestra**
Kestra, plateforme d'orchestration open source, rend cela concret : le flux est du YAML déclaratif versionné dans Git. L'agent tourne comme une tâche « AI Agent » unique avec une liste d'outils explicite, un plafond d'appels d'outils, un budget de tokens pour toute l'exécution et un timeout. L'approbation est une tâche « Pause » qui attend une personne et reprend avec sa décision. Un déclencheur Kafka démarre le flux. Les workers tournent près de l'ERP et des données, tandis que le plan de contrôle peut tourner n'importe où.

La plupart des équipes démarrent Kestra sur un seul domaine, souvent un pipeline de données ou une tâche d'infrastructure, parce que le noyau est léger, événementiel et sous licence Apache 2.0. Un processus comme celui décrit ici est généralement le deuxième ou troisième flux, une fois le premier domaine opérationnel.

D'autres orchestrateurs peuvent remplir des parties de ce rôle, et de nombreuses entreprises en font tourner plusieurs côte à côte, en se faisant appel mutuellement lorsqu'un processus traverse des domaines. Camunda est fort quand les équipes métier modélisent le processus en BPMN. Temporal convient quand les développeurs écrivent tout le processus en code applicatif. Airflow et Dagster couvrent bien les pipelines de données, et des services cloud comme AWS Step Functions fonctionnent au sein d'un seul cloud. Chacun est un bon choix dans son domaine. Kestra couvre les quatre domaines avec un seul plan de contrôle, de sorte que la même piste d'audit inclut aussi le pipeline qui rafraîchit les données maîtres fournisseurs et la tâche qui fait tourner les identifiants ERP.

**Quand un agent seul et son harness suffisent**
Tous les agents n'ont pas besoin d'un plan de contrôle. Un assistant de code, un agent de recherche ou un résumé de support au sein d'une seule application est bien servi par son harness. Si un agent tourne longtemps au sein de l'application d'une seule équipe, l'exécution durable est l'ajout approprié.

Un plan de contrôle se justifie dès qu'au moins une de ces conditions s'applique : le processus traverse plusieurs systèmes ou équipes ; une action de l'agent déplace de l'argent, modifie des systèmes de production ou atteint des clients ; un auditeur ou un régulateur a besoin d'un enregistrement de bout en bout ; des agents de différents fournisseurs travaillent sur le même processus.

**Où se déplace la valeur quand les modèles se banalisent**
La couche modèle se banalise le plus vite — les modèles de décision ont montré ce schéma, plusieurs fournisseurs ayant proposé des offres compatibles en quelques semaines après le premier lancement. La valeur se déplace vers les couches qui détiennent l'état du processus, les approbations et le journal d'audit, car elles sont difficiles à remplacer une fois qu'un processus en dépend.

Plusieurs groupes se disputent cette couche : les hyperscalers regroupent des runtimes d'agents managés ; les fournisseurs d'exécution durable ajoutent des intégrations d'agents ; les éditeurs d'applications intègrent des agents dans l'ERP, le CRM et la gestion de services ; les plateformes d'orchestration gouvernent les processus à travers tous ces outils. La question pratique pour tout projet d'agent est de savoir quelle couche possède les approbations, les budgets et l'audit — il vaut mieux y répondre tôt, car déplacer ces responsabilités plus tard implique de reconstruire le processus autour d'elles.

L'article conclut en faisant le lien avec le papier Google de 2015 : de même que ce papier plaidait pour concevoir le système autour du modèle, les agents ont besoin de la même discipline. Une orchestration unifiée donne à chaque responsabilité autour de l'agent un propriétaire clair, ce qui garde la dette technique agentique visible et sous contrôle.

## Pourquoi ça compte
Ce texte offre un cadre de décision concret pour les équipes qui déploient des agents IA en production, à un moment où le taux d'échec des projets agentiques (selon Gartner et Camunda) reste élevé faute de gouvernance claire des responsabilités comme l'approbation, le budget et l'audit.
