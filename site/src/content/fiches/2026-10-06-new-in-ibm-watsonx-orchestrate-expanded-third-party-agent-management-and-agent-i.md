---
title: "New in IBM watsonx Orchestrate: Expanded third-party agent management and Agent Identities"
date: 2026-10-06
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.ibm.com%2Fnew%2Fannouncements%2Fnew-in-ibm-watsonx-orchestrate-expanded-third-party-agent-management-and-agent-identities%3Futm_source=tldrit/1/010001a10c03b4ed-ebe552a3-143e-4c23-87f0-7bcca5a769cc-000000/xSSkA-GFDNvZM39BzZdd4JjadC0EbHvc5xHhgNOoQMs=452"
keywords: ["agents IA", "watsonx Orchestrate", "IBM", "gouvernance d'agents", "identité d'agent", "LLM-as-a-Judge"]
theme: "IA"
tone: "news"
used_in: ["2026-10-06"]
---

## Résumé
IBM annonce deux avancées majeures pour watsonx Orchestrate en septembre 2026 : l'AI Gateway peut désormais découvrir et importer des agents construits sur Microsoft Foundry et Google Gemini Enterprise Agent Platform (en plus d'Amazon Agentcore, intégré le mois précédent), et une fonctionnalité « Agent Identity » en préversion donne à chaque agent une identité vérifiable propre, rattachée aux fournisseurs d'identité existants (IBM Verify, Microsoft Entra). L'annonce inclut aussi six évaluateurs LLM-as-a-Judge prêts à l'emploi pour le suivi qualité en production, avec des taux d'échantillonnage configurables par les administrateurs, ainsi que des tableaux de bord personnalisables par utilisateur. L'ambition affichée est de faire de watsonx Orchestrate un plan de contrôle unifié au-dessus de tous les clouds d'agents d'une entreprise, avec une gouvernance de plus en plus fine (visibilité, identité, contrôle des coûts d'évaluation).

## Points clés
- L'AI Gateway de watsonx Orchestrate connecte désormais trois plateformes d'agents tierces : Amazon Agentcore (depuis août), Microsoft Foundry et Google Gemini Enterprise Agent Platform (nouveauté de septembre), permettant de scanner, découvrir et importer leurs agents dans un plan de contrôle unique.
- Six évaluateurs LLM-as-a-Judge prêts à l'emploi (toxicité, utilité, hallucination, concision, pertinence du contexte, pertinence de la réponse) surveillent désormais le trafic d'agents en production, applicables aux agents natifs comme aux agents externes importés.
- Le taux d'échantillonnage des évaluations est réglable par les administrateurs : 3 % par défaut au niveau du tenant, avec possibilité de monter jusqu'à 20 % par évaluateur individuel — un levier de coût explicite puisque chaque évaluation est un appel de modèle.
- « Agent Identity » (préversion, disponible pour IBM Verify et Microsoft Entra) attribue à chaque agent une identité distincte de celle de son créateur et de son utilisateur, afin de distinguer les actions humaines des actions agentiques et de limiter les accès aux seuls besoins de la tâche.
- Les tableaux de bord du plan de contrôle deviennent personnalisables, chaque équipe pouvant organiser l'affichage selon son propre rôle sans affecter l'expérience des autres utilisateurs.
- Cette annonce s'inscrit dans une trajectoire mensuelle engagée depuis juin 2026 (visibilité unifiée de l'estate agentique en juin, préversion de l'agent AgentOps en juillet, disponibilité générale et intégration d'Amazon Agentcore en août), avec l'ambition de couvrir vision, identité et gouvernance des comportements des agents.

## Analyse approfondie
**Extension de l'AI Gateway à Microsoft Foundry et Google Gemini Enterprise Agent Platform**
L'AI Gateway de watsonx Orchestrate, qui avait commencé en août à découvrir et importer les agents construits sur Amazon Agentcore, ajoute en septembre 2026 la prise en charge de deux nouvelles plateformes : Microsoft Foundry et Google Gemini Enterprise Agent Platform. Concrètement, il est désormais possible de scanner chacune de ces plateformes connectées, d'y repérer les agents en cours d'exécution, puis de les importer dans le même plan de contrôle que celui utilisé pour les agents natifs d'IBM.

L'article souligne que la plupart des grandes entreprises construisent leurs agents sur plus d'un cloud, et que l'outillage natif de chaque plateforme n'est conçu que pour gouverner les agents qui lui sont propres. watsonx Orchestrate se positionne au-dessus de ces trois plateformes : l'endroit où un agent a été construit ne détermine plus la capacité à le voir et à le gouverner de façon centralisée.

**Contrôle fin des évaluations LLM-as-a-Judge en production**
Six évaluateurs prêts à l'emploi — toxicité, utilité (helpfulness), hallucination, concision, pertinence du contexte et pertinence de la réponse — tournent désormais en continu sur le trafic réel des agents, et les équipes choisissent quels évaluateurs activer ainsi que leur fréquence d'échantillonnage.

En août, la fonctionnalité « Custom LLM-as-a-Judge » avait permis aux équipes de définir leurs propres critères qualité au moment de la construction de l'agent. La vraie difficulté se situe en production : évaluer en continu chaque exécution sur une multitude de métriques coûte cher, et un score qualité générique correspond rarement à ce qui compte réellement pour l'activité de l'entreprise. Les nouveaux contrôles permettent de décider où va le budget d'évaluation :
- **Six évaluateurs prêts à l'emploi** : toxicité, utilité, hallucination, concision, pertinence du contexte et pertinence de la réponse, disponibles sans avoir à écrire de critères sur mesure.
- **Contrôle des évaluateurs au niveau du tenant** : les administrateurs peuvent activer ou désactiver individuellement chaque évaluateur à l'échelle du tenant, pour ne faire tourner que les métriques pertinentes pour leurs cas d'usage.
- **Taux d'échantillonnage réglables** : le taux par défaut du tenant est de 3 % sur l'ensemble des évaluateurs ; les administrateurs peuvent le relever pour un évaluateur donné jusqu'à 20 %. Tout évaluateur sans taux propre hérite du taux par défaut du tenant.
Ces contrôles s'appliquent aussi bien aux agents natifs qu'aux agents externes importés.

Puisque chaque évaluation correspond à un appel de modèle, l'échantillonnage devient un levier de coût direct. L'exemple donné : une banque qui surveille un agent en contact avec la clientèle peut échantillonner la toxicité à un taux élevé, car le risque réputationnel y est concentré, tout en laissant la concision au taux par défaut. Résultat : une facture de supervision qui reflète le profil de risque de l'entreprise plutôt qu'un taux fixe appliqué uniformément à tout.

**Agent Identity : une identité vérifiable pour chaque agent**
En préversion, « Agent Identity » donne à chaque agent de watsonx Orchestrate une identité unique et vérifiable, distincte à la fois de la personne qui a construit l'agent et de celle qui l'utilise. Plutôt que de créer un nouveau magasin d'identités, watsonx Orchestrate connecte les identités d'agents au fournisseur d'identité déjà utilisé par l'organisation ; la préversion privée prend en charge IBM Verify et Microsoft Entra.

Aujourd'hui, beaucoup d'agents s'authentifient via des comptes de service partagés, des clés API statiques, ou les identifiants propres de l'utilisateur. Cela rend difficile de distinguer ce qu'un utilisateur a fait de ce qu'un agent a fait en son nom, et tend aussi à donner à l'agent plus d'accès que ce que la tâche exige réellement. Agent Identity vise à répondre à ce problème (l'article mentionne trois axes, sans tous les détailler explicitement dans le texte disponible), notamment en séparant clairement les identités humaines et agentiques et en limitant les droits d'accès au strict nécessaire.

**Tableaux de bord personnalisables**
Différentes équipes ont des priorités différentes lorsqu'elles surveillent la performance et l'usage de l'IA. De nouvelles améliorations des tableaux de bord offrent davantage de flexibilité, permettant à chaque utilisateur de se concentrer sur les informations les plus pertinentes pour son rôle. Les utilisateurs peuvent désormais personnaliser la disposition de leur tableau de bord selon leurs propres flux de travail et préférences. En organisant l'information de la manière qui correspond le mieux à leurs responsabilités, les équipes accèdent plus rapidement aux informations dont elles ont besoin, sans affecter l'expérience des autres utilisateurs.

**Une trajectoire mensuelle de gouvernance agentique**
L'article resitue cette annonce dans une progression mensuelle : en juin 2026, IBM a rendu visible l'ensemble du parc d'agents (« agentic estate ») dans un plan de contrôle unique ; en juillet, l'agent AgentOps a été présenté en préversion pour améliorer les agents une fois en production ; en août, AgentOps est passé en disponibilité générale et le parc s'est étendu aux agents construits sur Amazon Agentcore. Ce mois-ci (septembre), le parc couvre désormais trois grands clouds, et IBM commence à attribuer à chaque agent une identité propre.

La conclusion de l'article insiste sur une idée centrale : voir chaque agent n'est qu'une première étape. Une équipe sécurité a aussi besoin de savoir qui est chaque agent, ce qu'il est autorisé à faire, et ce qu'il a réellement fait, avant d'approuver son utilisation pour des tâches sensibles. IBM annonce vouloir continuer à construire dans cette direction et à rendre compte de ses progrès chaque mois, renvoyant vers les notes de version complètes pour le détail de toutes les nouveautés du mois.

## Pourquoi ça compte
Cette annonce illustre une tendance structurante de la veille IA 2026 : le passage d'une simple orchestration multi-agents à une véritable couche de gouvernance transversale (identité, coûts d'évaluation, conformité) au-dessus des plateformes cloud concurrentes — un enjeu clé pour toute entreprise qui déploie des agents IA à grande échelle sur plusieurs fournisseurs.
