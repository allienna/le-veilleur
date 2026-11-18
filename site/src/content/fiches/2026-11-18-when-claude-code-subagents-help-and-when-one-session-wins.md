---
title: "When Claude Code Subagents Help and When One Session Wins"
date: 2026-11-18
url: "https://substack.com/app-link/post?publication_id=3009345&post_id=225055710&utm_source=post-email-title&utm_campaign=email-post-title&isFreemail=true&r=7v5lmc&token=eyJ1c2VyX2lkIjo0NzU1OTI2MjgsInBvc3RfaWQiOjIyNTA1NTcxMCwiaWF0IjoxNzk0OTI0MzExLCJleHAiOjE3OTc1MTYzMTEsImlzcyI6InB1Yi0zMDA5MzQ1Iiwic3ViIjoicG9zdC1yZWFjdGlvbiJ9.ZywDxNREG6CzWwXdK7uoz9cWbDASUJcdAxw7dYCoSPw"
authors: ["Nir"]
keywords: ["sous-agents", "Claude Code", "multi-agent", "orchestration LLM", "tokens", "benchmarking"]
theme: "IA"
tone: "opinion"
used_in: ["2026-11-18"]
---

## Résumé
Cet article s'appuie sur une expérience menée par un chercheur d'Anthropic (16 agents Claude chargés d'écrire un compilateur C, pour un coût de près de 20 000 dollars) afin d'examiner quand les architectures multi-agents dans Claude Code apportent réellement un gain, et quand elles ne font qu'ajouter du coût sans valeur. L'auteur retrace le désaccord public de 2025 entre Cognition (qui met en garde contre le multi-agent) et Anthropic (qui défend ses systèmes de recherche parallèle), et montre qu'une partie des gains attribués aux équipes d'agents s'explique en réalité par un surcroît de tokens consommés plutôt que par une meilleure architecture. Il propose une méthode, le « control run », pour comparer à budget égal une session unique et une équipe de sous-agents avant de choisir une approche, et résume où en sont Cognition et Anthropic sur ce sujet en 2026.

## Points clés
- L'expérience du compilateur C a montré que 16 agents travaillant sur le même bug s'écrasaient mutuellement ; le problème s'est résolu en redécoupant la tâche en fichiers indépendants, chaque agent traitant un cas distinct.
- La métaphore du chantier : une équipe d'artisans ne bat un contractant seul que lorsque les tâches sont véritablement séparées (pièces différentes) ; sur une tâche séquentielle (un seul tuyau qui fuit), elle se gêne et coûte plus cher.
- En juin 2025, Cognition a publié « Don't Build Multi-Agents » (illustré par un clone de Flappy Bird raté, divisé entre deux sous-agents incohérents entre eux), tandis qu'Anthropic a défendu son système de recherche multi-agent, affichant +90 % sur son propre benchmark interne.
- Sur un benchmark de navigation web cité par Anthropic, 80 % des écarts de performance s'expliquaient par le nombre de tokens dépensés, pas par la qualité de l'architecture — ce qui remet en question une partie des gains attribués au multi-agent.
- En 2026, les deux entreprises convergent : Cognition réserve le multi-agent à la relecture de code par un agent « frais » sans le contexte du codeur ; Anthropic recommande de replier les sous-agents dans l'agent principal, sauf pour trois cas précis (contexte volumineux à isoler, travaux parallèles réellement indépendants, séparation d'outils ou d'instructions contradictoires).
- L'auteur propose une méthode de vérification, le « control run » : exécuter la même tâche en session unique et en équipe de sous-agents, à budget de tokens comparable et au moins deux fois chacune, avant de décider quelle architecture conserver.

## Analyse approfondie

### Le compilateur C et la logique du chantier
En février (2026 implicite), un chercheur d'Anthropic a confié à 16 agents Claude la tâche d'écrire un compilateur C capable, à terme, de compiler un noyau Linux fonctionnel. Au bout de deux semaines et près de 20 000 dollars de calcul, l'objectif a été atteint — mais pas sans accroc : à un moment donné, les 16 agents se sont tous heurtés au même bug, et chacun a tenté de le corriger à sa façon, écrasant sans cesse les correctifs des autres. Pendant cette phase, l'équipe de 16 agents n'a pas fait mieux qu'un seul agent, tout en coûtant bien plus cher.

L'auteur compare cette dynamique à une rénovation de maison : une équipe de plusieurs corps de métier (peintre, électricien, plombier) est efficace quand chacun travaille dans une pièce différente, sans dépendre des autres. Mais si on envoie toute l'équipe réparer une seule fuite, ils se gênent et annulent le travail des autres. C'est exactement ce qui s'est produit avec le compilateur : lorsque les tests qui échouaient étaient nombreux et indépendants, répartir un test par agent fonctionnait bien ; mais lorsque le problème touchait le noyau dans son ensemble (une tâche unique), chaque agent corrigeait le même point à sa manière et écrasait le travail des autres.

La solution a consisté à changer la forme du problème : une nouvelle configuration compilait la majeure partie du noyau avec GCC (un compilateur de référence, fiable) et ne confiait au nouveau compilateur qu'un sous-ensemble aléatoire de fichiers. Comme si on gardait l'ancienne plomberie dans la plus grande partie de la maison, et qu'on ne posait de nouveaux tuyaux que dans quelques pièces tirées au hasard : en cas de fuite, on sait où chercher, et chaque plombier peut prendre une pièce différente.

### Le débat de 2025 entre Cognition et Anthropic
Cette tension a opposé publiquement deux entreprises d'agents IA en 2025. En juin, Cognition (éditeur de l'agent de codage Devin) a publié un billet intitulé « Don't Build Multi-Agents » (« Ne construisez pas de systèmes multi-agents »). Leur exemple : un clone de Flappy Bird réparti entre deux sous-agents, l'un ayant produit un décor qui ressemblait à Super Mario, l'autre un oiseau qui ne ressemblait ni ne se comportait comme celui du jeu. Chaque sous-agent a fait quelque chose de raisonnable avec ce qu'il pouvait voir, mais les deux parties ne s'accordaient pas. C'est là que l'analogie du chantier atteint sa limite : un peintre peut entrer dans la cuisine et poser une question à l'électricien, alors qu'un sous-agent ne voit que les instructions qu'on lui a données. Tout ce qui n'a pas été écrit, le sous-agent doit le deviner.

Le lendemain, Anthropic a décrit son propre système de recherche, dans lequel un agent « principal » envoie des sous-agents effectuer des recherches en parallèle. Sur le benchmark de recherche interne d'Anthropic, cette équipe d'agents a surpassé un agent unique de 90 %.

Mais le même billet d'Anthropic contenait un résultat beaucoup moins repris : sur un benchmark de navigation web, le nombre de tokens dépensés par le système expliquait 80 % des écarts de performance observés. Autrement dit, la question se pose : l'équipe d'agents est-elle réellement plus intelligente, ou dépense-t-elle simplement davantage de ressources de calcul ?

### Le biais des tokens supplémentaires
Une équipe de sous-agents consomme presque toujours plus de tokens que l'agent unique auquel on la compare. Selon la documentation de Claude Code, une équipe d'agents utilise environ 7 fois plus de tokens qu'une session normale lorsque les coéquipiers fonctionnent en mode plan. Or, davantage de tokens peut améliorer la qualité d'une réponse à lui seul, ce qui rend facile d'attribuer à tort ce gain à l'architecture multi-agent plutôt qu'au simple surcroît de calcul.

L'auteur compare cela à un essai clinique : un nouveau médicament doit être comparé au meilleur traitement existant, sur des patients comparables, avec les mêmes critères de mesure. Si le groupe recevant le nouveau médicament bénéficie aussi de deux fois plus de visites d'infirmières, il devient impossible de savoir ce qui a réellement aidé. Avec les agents IA, ces « visites d'infirmières » supplémentaires, ce sont les tokens.

En janvier (2026), Anthropic a reconnu que certaines équipes avaient passé des mois à construire des systèmes multi-agents, pour finalement découvrir qu'un meilleur prompt sur un agent unique obtenait un résultat équivalent. En avril, une étude a mené cet essai « à budget égal », avec la même enveloppe de raisonnement de chaque côté : sur des questions nécessitant plusieurs étapes de raisonnement, testées sur trois familles de modèles différentes, l'agent unique a systématiquement égalé ou dépassé l'équipe de sous-agents.

### Où en sont les deux entreprises en 2026
Depuis, les deux entreprises ont convergé vers une position intermédiaire. En avril, Cognition a réaffirmé que son avertissement de 2025 restait valable pour les essaims d'agents qui écrivent du code simultanément. Ce qui fonctionne chez eux est plus restreint : plusieurs agents peuvent contribuer à la réflexion, mais un seul écrit le code final. Leur agent de relecture lit chaque modification sans disposer du contexte de l'agent codeur, et détecte environ deux bugs par pull request — à l'image d'un bon relecteur éditorial, qui repère les trous qu'un auteur ne voit pas dans son propre texte, parce que l'auteur sait ce qu'il voulait dire, alors que le relecteur ne voit que la page.

En octobre, Anthropic a publié un guide expliquant comment replier des sous-agents dans l'agent principal. Dans les cas qu'ils décrivent, un agent unique doté de « compétences » (skills) bat souvent les architectures à sous-agents en qualité, et le fait souvent à moindre coût et avec une latence réduite. Le guide conserve néanmoins trois usages légitimes pour les sous-agents : garder le contexte principal propre, exécuter des travaux séparés dans des contextes neufs, et isoler des outils ou des instructions qui, combinés, embrouilleraient un agent unique.

### Quand recourir aux sous-agents
En reprenant l'image du chantier, une équipe ne justifie son coût que lorsque les « pièces » du travail sont séparées. Dans Claude Code, cela correspond à trois cas :

- **Utiliser un sous-agent** quand la tâche inonderait la session principale d'informations inutiles par la suite, comme une recherche large dans une grosse base de code, de longs logs ou une pile de documentation. Le sous-agent travaille dans sa propre fenêtre de contexte et ne renvoie que ses conclusions, ce qui garde le bruit hors de la session principale.
- **Exécuter des sous-agents en parallèle** quand les parties du travail sont véritablement indépendantes : questions distinctes, modules séparés, ou échecs de tests sans rapport entre eux.
- **Ajouter un relecteur « frais »** quand on veut un second regard sur une modification, avec une consigne du type : « Relis ce diff comme si tu n'avais jamais vu la tâche. Liste tout ce qui pourrait casser, avec le fichier et la ligne. »
- **Rester en session unique** quand chaque étape dépend de la précédente : traquer un bug, ou refactoriser à travers des fichiers partagés. C'est le cas du tuyau qui fuit. La documentation de Claude Code elle-même déconseille les équipes d'agents pour le travail séquentiel, les qualifiant encore d'expérimentales.

### Le test de contrôle avant de diviser une tâche
L'ouvrage auquel renvoie l'article appelle cette vérification le « control run » (test de contrôle) : exécuter la même tâche une fois avec un agent unique, une fois avec une équipe, au même budget. Dans Claude Code, la méthode se déroule ainsi :

1. Choisir une tâche déjà réalisée avec des sous-agents la semaine précédente, avec un critère de réussite clair (les tests passent, et le diff serait mergé).
2. L'exécuter d'abord en session unique, avec une consigne du type : « Fais cette tâche toi-même, sans sous-agents. Lis les fichiers nécessaires, fais la modification, et lance les tests. » Noter le temps pris et ce qu'indique la commande /usage.
3. Exécuter ensuite la version avec sous-agents, dans la même limite de temps. Sur un abonnement, /usage indique la part de tokens consommée par les sous-agents — il faut la compter intégralement.
4. Compter tout ce qui a dû être corrigé manuellement pour que le résultat fusionné fonctionne réellement. Cet effort est imputé au score de l'équipe.
5. Répéter chaque version au moins deux fois : dans un exemple cité du guide d'octobre d'Anthropic, une modification a cassé une étape qui fonctionnait jusque-là, et cette régression n'est apparue que sur une exécution sur deux.

Si l'équipe de sous-agents l'emporte par une marge supérieure à l'écart entre ses deux propres exécutions, on la conserve. Si une session unique obtient un résultat équivalent, on revient à la session unique en conservant les bonnes instructions rédigées pour l'équipe. Si l'équipe gagne mais consomme beaucoup plus de ressources, on peut donner à la session unique ce même budget supplémentaire (par exemple une seconde passe où elle relit son propre diff) et comparer à nouveau.

### Les limites de cette méthode
L'auteur reconnaît que les preuves disponibles restent limitées : les résultats « à budget égal » proviennent surtout de tâches de raisonnement et de recherche, et peu d'études testent de longues tâches de codage impliquant de nombreux appels d'outils. On ne peut donc ni supposer qu'une session unique gagnera toujours sur sa propre tâche, ni l'inverse.

La réponse est aussi amenée à évoluer dans le temps : le guide d'octobre d'Anthropic a constaté que des configurations multi-agents rigides empêchaient souvent les modèles les plus récents de faire eux-mêmes une plus grande partie du travail. Une répartition qui était rentable avec le modèle de l'an dernier peut perdre face à une session unique avec le modèle d'aujourd'hui — d'où la nécessité de refaire le test de contrôle à chaque changement de modèle.

L'auteur conclut que la plupart du travail de codage ressemble à un long tuyau où chaque étape dépend de la précédente, plutôt qu'à des pièces séparées d'un chantier — et invite à donner, avant toute division en sous-agents, le même budget à une session unique pour voir ce qu'elle produit seule. L'article se termine par une offre commerciale sur les livres et le cours de l'auteur, qui sort du champ de cette analyse technique.

## Pourquoi ça compte
Ce texte offre un cadre méthodologique concret (le « control run ») pour trancher un débat récurrent en veille IA — multi-agents vs agent unique — en mettant en évidence un biais de mesure fréquent (le surcroît de tokens) qui fausse beaucoup de comparaisons publiées sur le sujet.
