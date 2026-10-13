---
title: "Do Agent Teams Pay Off? A Case Study on Vibe Code Bench | Vals AI"
date: 2026-10-13
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.vals.ai%2Fblogs%2Fmulti-agent-vibe-code-bench%3Futm_source=tldrai/1/010001a13050bbbb-35d29500-1e99-403b-8eda-fd880a962ed6-000000/ByMIpXJPco4XkraBiuS-NcbFqeL9fRrehBVvhtyI7tQ=452"
authors: ["Vals AI"]
keywords: ["agents IA", "multi-agent", "Claude Opus", "GPT-6", "benchmark", "génération de code"]
theme: "IA"
tone: "research"
used_in: ["2026-10-13"]
---

## Résumé
Vals AI a comparé, sur son benchmark Vibe Code Bench (50 applications web complètes à construire), des agents uniques à des équipes d'agents (un lead qui délègue à des sous-agents) pour GPT-6 Sol et Claude Opus 5.5, à effort de raisonnement moyen et maximal. Les équipes coûtent de 1,8 à 5,1 fois plus cher que les agents seuls, mais un seul des quatre écarts de score est statistiquement significatif : le gain de 7,3 points de Sol en effort moyen (p = 0,005). Pour Sol, augmenter l'effort de raisonnement a plus profité que de former une équipe ; pour Opus, ni l'un ni l'autre n'a d'effet significatif. Les deux leads orchestrent très différemment : Sol découpe vite et teste lui-même, Opus rédige d'abord un contrat d'interface puis délègue par vagues séquentielles.

## Points clés
- Sur 50 apps, les équipes d'agents coûtent 1,8 à 5,1 fois plus que l'agent seul, pour un gain de score significatif dans un seul cas sur quatre (Sol, effort moyen : +7,3 points, p = 0,005).
- Pour Sol, un effort de raisonnement plus élevé (max) rapporte davantage que le travail en équipe ; pour Opus, ni l'effort ni l'équipe ne changent significativement le score.
- Les équipes de Sol terminent plus vite (délégation en parallèle dès les premières minutes) ; celles d'Opus prennent jusqu'à 2,3 fois plus de temps (rédaction d'un contrat partagé puis délégation en vagues séquentielles).
- Le surcoût des équipes vient surtout des tokens en cache : chaque sous-agent réexpédie tout son contexte à chaque appel modèle (jusqu'à 224 millions de tokens en cache par app pour les sous-agents d'Opus en effort max).
- Le gain d'équipe de Sol en effort moyen se concentre sur les applications les plus difficiles (+15 points en moyenne), là où l'agent seul bâclait des fonctionnalités entières ; pour Opus, gains et pertes s'équilibrent sans corrélation avec la difficulté.
- Chaque configuration n'a été exécutée qu'une seule fois : les intervalles et p-values reflètent la variance entre applications, pas entre runs répétés, ce qui limite la portée des conclusions.

## Analyse approfondie
OpenAI et Anthropic proposent désormais un support natif du multi-agent : un agent "lead" peut créer des sous-agents, leur confier une partie d'une tâche, puis assembler leurs résultats. Vals AI a voulu mesurer ce que cela apporte, ce que cela coûte, et sur quels types de travaux cela aide, en utilisant des tâches proches de vrais projets logiciels.

Le test s'appuie sur Vibe Code Bench, le benchmark de Vals AI pour construire des applications web complètes à partir d'un cahier des charges produit. Chaque application est déployée via Docker Compose et notée par des agents navigateurs qui parcourent ses parcours utilisateurs. Le travail se répartit naturellement entre base de données, API, interface et déploiement, et les bugs aux points de jonction entre ces briques se répercutent directement sur le score. L'équipe a fait tourner GPT-6 Sol et Claude Opus 5.5 sur 50 applications, chacun en agent unique et en équipe, à effort de raisonnement moyen et maximal.

Dans une équipe, le lead peut confier des parties du projet à des sous-agents (jusqu'à cinq simultanément), lesquels ne peuvent pas créer leurs propres sous-agents. Les deux leads ont reçu la même consigne courte : découper le travail en parties indépendantes, les déléguer, puis intégrer et vérifier le résultat ; le prompt de tâche, le bac à sable et le correcteur étaient par ailleurs identiques. Le score correspond à la part des tests d'interface utilisateur réussis pour chaque application, moyennée sur les 50 apps. Chacune des huit configurations n'a tourné qu'une seule fois.

### Principaux résultats
- Les équipes coûtent de 1,8 à 5,1 fois plus cher que les agents seuls, et un seul écart de score est statistiquement significatif : l'équipe de Sol en effort moyen gagne 7,3 points par rapport à son agent seul (p = 0,005). Les trois autres écarts, de -0,3 à +3,4 points, ne sont pas significatifs.
- Pour Sol, un effort de raisonnement plus élevé augmente davantage le score qu'une équipe ; pour Opus, ni un effort plus élevé ni une équipe ne font de différence significative. Un effort plus élevé coûte cependant plus cher : l'agent seul de Sol en effort max coûte 1,6 fois le prix de son équipe en effort moyen (4,82 $ contre 3,07 $ par app) et prend trois fois plus de temps.
- Les équipes finissent plus vite pour Sol, mais pas pour Opus, et les deux leads orchestrent différemment. Le lead de Sol répartit l'application entre sous-agents parallèles dès les premières minutes et teste lui-même le résultat ; en effort max, sa durée d'exécution passe de 38 à 28 minutes. Le lead d'Opus commence généralement par rédiger un contrat partagé décrivant comment les parties de l'app s'articuleront, puis délègue par vagues séquentielles de constructeurs et de testeurs ; ses équipes prennent jusqu'à 2,3 fois plus de temps que ses agents seuls.

Ces observations proviennent d'un seul benchmark d'applications web complètes et ne se généralisent pas forcément à d'autres types de travaux.

### Coût, durée et score
Chaque paire a été comparée sur les mêmes 50 applications via un test t appairé. Seul le gain de 7,3 points de Sol en effort moyen est statistiquement significatif (p = 0,005 ; intervalle à 95 % de +2,3 à +12,4 points). Les trois autres écarts ne le sont pas (p = 0,16 à 0,81) : +1,4 point pour Sol en effort max, -0,3 pour Opus en effort moyen, et +3,4 pour Opus en effort max.

Tableau des scores, coûts et durées par modèle, effort et configuration :

| Modèle | Configuration | Score | Coût moyen par app | Durée médiane |
|---|---|---|---|---|
| GPT-6 Sol | effort moyen, agent seul | 77,6 % | 1,22 $ | 12,4 min |
| GPT-6 Sol | effort moyen, équipe | 84,9 % | 3,07 $ | 11,9 min |
| GPT-6 Sol | effort max, agent seul | 89 % | 4,82 $ | 38,4 min |
| GPT-6 Sol | effort max, équipe | 90,4 % | 8,54 $ | 27,6 min |
| Claude Opus 5.5 | effort moyen, agent seul | 91,5 % | 4,08 $ | 20,3 min |
| Claude Opus 5.5 | effort moyen, équipe | 91,2 % | 9,10 $ | 26,6 min |
| Claude Opus 5.5 | effort max, agent seul | 89,8 % | 23,77 $ | 74,7 min |
| Claude Opus 5.5 | effort max, équipe | 93,2 % | 122 $ | 174,1 min |

À effort moyen puis max, les équipes coûtent respectivement 2,5 et 1,8 fois plus que l'agent seul pour Sol, et 2,2 et 5,1 fois plus pour Opus. La majeure partie du surcoût vient des tokens d'entrée mis en cache : chaque sous-agent conserve son propre contexte (cahier des charges et état de travail) qui est réenvoyé à chaque appel au modèle. En effort max, les sous-agents d'Opus lisent une médiane de 224 millions de tokens en cache par app, contre 17 millions pour le lead et 55 millions pour l'agent seul. Une équipe d'Opus en effort max a dépassé le temps imparti alors qu'elle vérifiait encore son travail ; son coût d'environ 189 $ est estimé à partir de ses tokens et inclus dans la moyenne.

Le parallélisme fait gagner du temps à Sol dans les deux niveaux d'effort, légèrement en effort moyen : son équipe termine en 11,9 minutes contre 12,4 pour l'agent seul, et en 28 minutes contre 38 en effort max.

Les équipes d'Opus prennent plus de temps, jusqu'à 2,3 fois la durée de l'agent seul en effort max. Elles travaillent par vagues séquentielles, chaque vague attendant son membre le plus lent ; en effort max, le sous-agent médian tourne 46 minutes, contre 7 en effort moyen.

Ce temps supplémentaire correspond à du travail effectif des sous-agents, pas à de l'attente, et des exécutions plus longues ne donnent pas de meilleurs scores : la durée de l'équipe max d'Opus n'est pas corrélée à son gain par rapport à l'agent seul. Quatre de ses exécutions ont dépassé quatre heures, et une a atteint la limite de 5,25 heures.

**Effort plus élevé ou travail en équipe ?** Les deux leviers augmentent le coût, avec des effets différents sur le score. Pour Sol, l'effort max augmente le score de l'agent seul de 11,4 points (p < 0,001), davantage que les 7,3 points apportés par une équipe en effort moyen. L'agent seul en effort max dépasse aussi de 4,1 points l'équipe en effort moyen (89,0 % contre 84,9 %), un écart non significatif (p = 0,08), pour 1,6 fois le coût et trois fois la durée.

Pour Opus, l'effort max seul n'augmente pas le score : l'agent seul obtient 89,8 % pour 23,77 $, contre 91,5 % pour 4,08 $ en effort moyen (p = 0,48). La combinaison effort max et équipe produit le meilleur score de l'étude, 93,2 %, pour trente fois le coût de l'agent seul en effort moyen ; son avance de 1,6 point sur cet agent n'est pas significative (p = 0,36). Entre modèles, l'équipe max de Sol (90,4 %, 8,54 $) s'approche à environ un point de l'agent seul moyen d'Opus, pour le double du prix.

Aucune des deux options ne s'impose comme choix par défaut : un effort plus élevé apporte à Sol le gain le plus important, à un prix plus élevé, tandis que la configuration la moins chère d'Opus obtient un score comparable à sa configuration la plus chère sur cet ensemble de tâches.

### Comment les leads ont travaillé
Les deux leads ont reçu la même consigne mais ont réparti le travail différemment.

**Le lead de Sol découpe l'app et teste lui-même.** En effort moyen, le lead de Sol découpe le travail selon des lignes architecturales (base de données et données initiales, API, interface, déploiement) et crée tous ses sous-agents en environ une minute. En effort max, il découpe plus souvent l'interface en zones fonctionnelles distinctes (13 plans initiaux sur 50, contre 7 en effort moyen) et continue d'ajouter des sous-agents plus tard dans l'exécution. Il crée aussi légèrement plus de sous-agents (5,1 contre 4,2) et leur envoie presque deux fois plus de demandes de suivi (31 contre 18 par app).

Les journaux de Sol enregistrent les commandes du lead mais pas ses modifications de fichiers, donc on ne peut pas savoir combien de code il a écrit lui-même ; ses actions enregistrées relèvent surtout de la coordination, de la construction et des tests. Il pilote un navigateur sans interface graphique dans 46 exécutions sur 50 aux deux niveaux d'effort, effectuant environ deux fois plus de tests navigateur que l'agent seul, surtout sur l'URL publique de l'app plutôt qu'en local dans le bac à sable. En effort moyen, l'agent seul ne teste qu'en local dans 18 exécutions sur 50, contre 4 pour le lead d'équipe. Dans ses notes, le lead rapporte avoir détecté des bugs qui n'apparaissent qu'à la jonction des pièces construites séparément, comme une interface envoyant des champs ne correspondant pas au schéma de base de données, ou un total calculé différemment dans l'interface et dans la base. Chaque correction est renvoyée au sous-agent propriétaire du fichier concerné.

**Le lead d'Opus rédige un contrat puis délègue par vagues.** Avant de créer le moindre agent, le lead d'Opus rédige un document partagé, généralement nommé `CONTRACT.md`, décrivant le schéma, les routes API et la répartition des fichiers (42 exécutions sur 50 en effort moyen, 40 en effort max ; les agents seuls ne le font presque jamais). Il crée ses sous-agents par vagues. En effort moyen, il crée d'abord des constructeurs, puis, dans la plupart des cas, un sous-agent dédié aux tests de bout en bout. En effort max, il ajoute une vague : d'abord des sous-agents qui posent les fondations, puis des sous-agents qui construisent les fonctionnalités par-dessus, puis des sous-agents qui testent et relisent l'application. Il rédige lui-même les fichiers README dans la plupart des exécutions et modifie le code applicatif dans 10 exécutions sur 50 en effort moyen et 26 en effort max.

En effort max, l'équipe d'Opus est plus grande : 6,8 sous-agents par app au lieu de 4,2, un sous-agent de test dans les 50 exécutions, et environ 1 140 appels d'outils par sous-agent et par app, contre environ 270 pour l'agent seul en effort max. Ses sous-agents exécutent 36 tests navigateur par app, six fois plus que l'agent seul en effort max.

**Où est passé le temps.** Les équipes et les agents seuls atteignent leur premier déploiement (premier `docker compose up`) à des moments proches. En effort moyen, les équipes des deux modèles sont à moins d'une minute de leurs agents seuls. En effort max, l'équipe de Sol déploie environ cinq minutes plus tôt, celle d'Opus environ six minutes plus tard. L'équipe d'Opus en effort max passe ensuite les deux tiers de son exécution après ce premier déploiement, contre moins d'un tiers pour l'agent seul. Sur cette période, son lead et ses sous-agents consacrent une médiane de 68 agent-minutes (temps cumulé du lead et des sous-agents) aux tests, contre 10 pour l'agent seul.

Tableau des minutes médianes jusqu'au premier déploiement et jusqu'à la fin :

| Modèle et effort | Configuration | Premier déploiement | Fin | Agent-minutes de test après le premier déploiement |
|---|---|---|---|---|
| GPT-6 Sol, moyen | Agent seul | 5,1 min | 12,4 min | 3,1 min |
| GPT-6 Sol, moyen | Équipe | 5,7 min | 11,9 min | 3,5 min |
| GPT-6 Sol, max | Agent seul | 19,9 min | 38,4 min | 8 min |
| GPT-6 Sol, max | Équipe | 15,3 min | 27,6 min | 7 min |
| Claude Opus 5.5, moyen | Agent seul | 12,2 min | 20,3 min | 3,6 min |
| Claude Opus 5.5, moyen | Équipe | 12,5 min | 26,6 min | 6 min |
| Claude Opus 5.5, max | Agent seul | 51 min | 74,7 min | 9,6 min |
| Claude Opus 5.5, max | Équipe | 56,8 min | 174,1 min | 67,8 min |

Sur une application type (comptes utilisateurs, tenue de registres, tableau de bord d'usage, notifications par e-mail), les équipes de Sol obtiennent un score supérieur à ses agents seuls aux deux niveaux d'effort (62 % contre 50 %, puis 75 % contre 62 %), ce qui n'est pas le cas pour Opus (75 % contre 88 %, puis 75 % contre 75 %).

### D'où viennent les gains d'équipe
Pour vérifier si les équipes aident davantage sur les applications les plus difficiles, Vals AI a classé les apps à l'aide d'une exécution extérieure à chaque comparaison. Pour la comparaison en effort moyen, une app est considérée comme difficile si l'agent seul en effort max du même modèle y a obtenu moins de 90 % ; pour la comparaison en effort max, c'est l'agent seul en effort moyen qui sert de référence. Cela évite que des résultats dus au hasard dans les exécutions comparées ne déterminent le groupe d'une app.

- L'équipe de Sol en effort moyen gagne sur environ la moitié des apps, surtout les plus difficiles : score supérieur sur 24 apps, inférieur sur 11, identique sur 15. Sur les apps difficiles, le gain moyen est d'environ 15 points ; sur les plus faciles, d'environ 1 point. En effort max, le gain plus modeste de l'équipe de Sol se répartit également entre apps difficiles et faciles.
- Là où l'équipe de Sol en effort moyen gagne 20 points ou plus, elle construit et vérifie ce que l'agent seul avait laissé de côté. Sur ces neuf apps, les agents seuls déclaraient que les tests passaient alors que certaines fonctionnalités n'avaient jamais été construites, ni certains parcours jamais essayés. L'équipe couvre mieux le cahier des charges et vérifie plus soigneusement son travail : elle construit ces fonctionnalités, et son lead confronte les parties construites séparément, détectant des incohérences comme un formulaire ne correspondant pas au schéma de base de données ou une règle de permission bloquant une étape.
- Les gains et pertes d'Opus sont plus équilibrés et ne favorisent pas les apps difficiles. Son équipe obtient un score supérieur sur 14 apps et inférieur sur 15 en effort moyen, supérieur sur 13 et inférieur sur 8 en effort max. En effort moyen, elle perd environ quatre points sur les apps difficiles et en gagne environ deux sur les plus faciles ; en effort max, elle ajoute environ trois à quatre points dans les deux cas.
- Les autres caractéristiques testées n'ont pas d'effet homogène. Les apps avec davantage de rôles utilisateurs distincts gagnent 15 points avec l'équipe de Sol en effort moyen, mais aucune autre configuration ne montre cet effet. La longueur du cahier des charges, le nombre de tests d'interface, et le caractère mono- ou multi-utilisateur de l'app n'ont pas d'effet constant non plus.

### Travaux futurs
Sur ce benchmark, l'effet d'une équipe dépend du modèle, de l'effort de raisonnement et de l'application. La question ouverte est de savoir quelles tâches les équipes gèrent de façon fiablement meilleure que les agents seuls. Une équipe devrait gagner le plus quand le travail se divise en parties pouvant avancer en parallèle, et que le lead peut les recombiner sans consommer le temps ainsi économisé en coordination. Les tâches comportant de nombreuses parties indépendantes et de longues portions de travail séparables — grandes bases de code, questions de recherche larges, analyses portant sur de nombreux documents — sont les pistes à explorer en priorité.

### Méthodologie et limites
GPT-6 Sol a tourné via l'API Agents d'OpenAI, avec le mode `multi_agent` de l'API désactivé pour les agents seuls et activé pour les équipes, et des commandes exécutées dans un bac à sable Vals. Claude Opus 5.5 a tourné via la CLI Claude Code en mode headless, les outils de sous-agents étant retirés pour les agents seuls et disponibles pour les équipes. Les exécutions d'équipe d'Opus désactivaient aussi la limite de dix minutes de Claude Code pour les sous-agents en arrière-plan. L'effort de raisonnement, moyen ou max, était défini via le paramètre `reasoning.effort` d'OpenAI et la variable `CLAUDE_CODE_EFFORT_LEVEL` de Claude Code. Les apps étaient notées par la suite de tests d'interface standard de Vibe Code Bench.

Les décomptes comportementaux proviennent du flux d'événements de chaque lead, et des flux des sous-agents pour Opus. L'API Agents d'OpenAI émet deux événements `subagent.created` par sous-agent, donc les identifiants uniques de sous-agents ont été comptés pour Sol. Les tests navigateur comptent les commandes qui lancent ou font naviguer un navigateur sans interface graphique. La durée est le temps d'horloge murale de l'agent dans le bac à sable. Les harnais exposent des niveaux de détail différents : Claude Code enregistre tous les appels d'outils de chaque sous-agent, alors que le flux d'événements de l'API Agents d'OpenAI ne contient que les tours du lead — on peut donc voir quand le lead de Sol crée, envoie des messages et attend ses sous-agents, mais pas ce qu'il leur a dit ni ce qu'ils ont fait. Les coûts de Sol supposent que son usage de tokens rapporté inclut les sous-agents.

Les coûts de Sol appliquent les prix de liste du niveau de base d'OpenAI (2 $ par million de tokens en entrée, 0,20 $ en cache, 10 $ en sortie) à l'usage de tokens rapporté. Les requêtes au-delà du seuil de contexte long de 272 000 tokens sont facturées plus cher, ce qui n'a pas pu être évalué car l'usage est rapporté par exécution plutôt que par requête. Les coûts d'Opus correspondent aux totaux au prix de liste rapportés par Claude Code.

Comme chaque configuration n'a tourné qu'une seule fois, les intervalles et p-values de cette étude reflètent la variation entre applications, pas entre exécutions répétées. Les exécutions d'équipe ont aussi reçu la consigne de délégation, donc chaque comparaison oppose "des sous-agents plus un prompt de délégation" à l'absence des deux. Les deux modèles tournant sur des harnais différents, les comparaisons entre modèles mélangent l'effet du modèle avec celui de son harnais.

## Pourquoi ça compte
Cette étude chiffre un arbitrage rarement mesuré dans la pratique — coût et temps d'une architecture multi-agent contre le gain réel de qualité — et montre que ce gain dépend fortement du modèle sous-jacent et de son style d'orchestration, pas seulement du fait d'avoir des sous-agents. Pour une veille tech, elle offre un contrepoint factuel au discours "plus d'agents = mieux" très présent autour des outils agentiques actuels.
