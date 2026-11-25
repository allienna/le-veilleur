---
title: "Speeding up code review with `small-change`"
date: 2026-11-25
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Flethain.com%2Fsmall-changes%2F%3Futm_source=tldrdev/1/010001a20d7d27e0-53e789d5-a97b-438e-8ffd-f9ea51c829a6-000000/z4UlmZ7Nyvyv7AP_2bocAaxsUZs4c9EDIrchMsh_1s8=452"
authors: ["Will Larson"]
keywords: ["revue de code", "IA générative", "CICD", "ingénierie logicielle", "automatisation", "pull request"]
theme: "Software"
tone: "opinion"
used_in: ["2026-11-25"]
---

## Résumé
Ce billet de blog (lethain.com) décrit comment l'entreprise Imprint fait face à une explosion du volume de pull requests (x4 en moyenne, jusqu'à x10-25 pour certaines équipes en deux ans), portée par l'adoption de harnais d'IA, tout en améliorant sa qualité logicielle (incidents en baisse de 42 %, incidents critiques en baisse de 78 %). Le temps médian de revue de PR a cependant plus que doublé (33 à 77 minutes), ce qui a poussé l'équipe à concevoir un dispositif appelé `small-change` : un mécanisme qui accélère l'approbation des changements de faible risque via des critères automatisés (taille, absence d'alertes d'un bot de revue IA, expérience de l'auteur, périmètre limité). L'auteur met aussi en garde contre le piège du « meat proxy review », où les commentaires générés par des harnais IA créent une illusion de revue sans réel partage de connaissances, et évoque brièvement `fleet`, leur harnais orchestré de façon centralisée pour écrire et vérifier du code.

## Points clés
- Le volume de PR fusionnées a été multiplié par 4 en moyenne sur deux ans chez Imprint, et jusqu'à 10-25 fois pour certaines équipes, avec une qualité en hausse (incidents -42 %, incidents critiques -78 %).
- Le temps médian de revue d'une PR est passé de 33 à 77 minutes, en corrélation directe avec la hausse du volume de PR — ce qui a motivé la recherche d'une solution.
- Les quatre raisons historiques de réviser du code (partage de connaissances, prévention des erreurs, prévention de comportements malveillants, obligations de conformité) doivent selon l'auteur être repensées à l'ère des harnais IA.
- Le dispositif `small-change` définit des critères objectifs et vérifiés automatiquement (moins de 1000 lignes, aucune alerte critique du bot `ai-code-review`, auteur expérimenté sur le service concerné, périmètre d'impact limité, exclusion des bibliothèques partagées) pour qualifier un changement à une approbation accélérée.
- Deux agents internes soutiennent le dispositif : `review-small-change` (qui approuve ou ignore, sans jamais commenter, pour éviter la dérive du « meat proxy review ») et `review-pr-cluster` (qui identifie des thèmes récurrents sur des lots de PR).
- Les premiers résultats montrent qu'environ 10 % des changements sont éligibles au `small-change` ; la réussite de l'initiative dépendra de la capacité à élargir ce taux en renforçant en parallèle les mécanismes de vérification automatisée.

## Analyse approfondie

### Pourquoi réviser les pull requests ?
L'auteur identifie quatre justifications traditionnelles à la revue de code, et explique comment chacune doit évoluer face au volume actuel :

1. **Le partage de connaissances entre auteur et relecteur** — l'ingénierie logicielle s'apprend historiquement par compagnonnage, la revue étant le principal vecteur de transmission des bonnes pratiques. Avec le volume actuel, ce partage devra se faire davantage au niveau de grappes de pull requests plutôt que PR par PR.
2. **La prévention des erreurs** — la revue a longtemps été un moyen coûteux de détecter des erreurs ; l'auteur estime que des pipelines CI/CD efficaces combinés à des techniques de vérification outillées (comme le `pstack` de l'outil « poteto ») sont aujourd'hui plus efficaces que la revue humaine pour cet objectif.
3. **La prévention des comportements malveillants** — selon l'auteur, même une revue de code attentive manque généralement les comportements malveillants *compétents* (heureusement, la plupart des comportements malveillants sont peu compétents). La meilleure protection combine des règles fixes (certains fichiers/objets sensibles exigent une revue obligatoire), des mécanismes anti-abus affinés via leurs expériences de support client basées sur des LLM, des audits et l'inspection des journaux d'audit.
4. **Les obligations de conformité** inscrites dans leurs contrôles documentés — ces règles pourraient être modifiées, mais exigent aujourd'hui qu'un humain indépendant revoie les changements sur un sous-ensemble de leurs dépôts.

L'auteur estime qu'il existe aujourd'hui de meilleures solutions pour chacun de ces quatre problèmes, mais que ces changements doivent être introduits avec prudence.

### Petits pas avec `small-change`
Imprint privilégie des changements progressifs et circonscrits pour valider de nouvelles pratiques. C'est dans cet esprit qu'a été conçu le concept de `small-change`, qui fonctionne ainsi :

1. Lorsqu'une pull request est marquée comme prête, le pipeline CI/CD détermine automatiquement si elle est éligible au statut `small-change`, matérialisé par un check GitHub qui passe (et non modifiable manuellement par un humain). Un label existe aussi pour la visibilité, mais seul le check — vérifié indépendamment — fait foi.
2. Un changement est qualifié de `small-change` s'il remplit tous les critères suivants :
   - moins de 1000 lignes de code ;
   - aucune alerte de priorité p1 ou p2 remontée par leur bot de revue automatisée `ai-code-review` ;
   - l'auteur a de « l'expérience » sur le service ou l'application concerné, définie comme au moins 10 pull requests précédentes fusionnées dans les répertoires de ce service — pour les changements traversant plusieurs services, l'auteur doit avoir cette expérience sur chacun d'eux ;
   - le changement impacte moins de `N` services ou applications distincts (`N` = 1 sur leur monorepo frontend, `N` = 3 sur le monorepo backend, où un changement typique touche à la fois un service gRPC et une passerelle HTTP commune) ;
   - les bibliothèques et utilitaires partagés sont exclus de l'éligibilité ;
   - chaque dépôt dispose d'un fichier `.small_change` permettant une personnalisation fine par chemin (par exemple, exclure un service lié aux mouvements d'argent) pendant que l'équipe continue d'ajuster les réglages.
3. Leur automatisation Slack étiquette chaque mention de pull request avec des réactions emoji indiquant son état (tests en échec, approuvée mais tests en cours, prête à fusionner, etc.). Une réaction `small-change` a été ajoutée pour signaler les PR remplissant ces critères.
4. Deux agents ont été créés dans leur dépôt interne de « skills », déployés sur différents harnais :
   - `review-small-change`, qui prend en entrée une liste de dépôts et passe en revue toutes les `small-change` ouvertes et non brouillons, en approuvant celles qui remplissent les critères (tous les checks passent, y compris celui de `small-change`, et le changement ne touche pas à des sujets sensibles comme les paiements ou la sécurité). Cet agent n'a que deux options possibles : approuver ou ignorer — il ne commente **jamais** la PR, afin d'éviter la prolifération du « meat proxy review », devenu sur certaines équipes un goulot d'étranglement se faisant passer pour une solution.
   - `review-pr-cluster`, qui passe en revue des lots de pull requests pour identifier des thèmes récurrents et suggérer des pistes de discussion ou de nouvelles vérifications à ajouter.
5. L'attente collective établie est que toute erreur causée par une `small-change` constitue un échec du système, à corriger au niveau systémique : amélioration de `ai-code-review`, des mécanismes de vérification, du CI/CD, du harnais, etc.

La mise en œuvre et le déploiement initial n'ont demandé qu'environ deux jours d'attention répartie, même si l'auteur imagine devoir continuer à ajuster les réglages pendant longtemps — peut-être indéfiniment.

### La revue par « proxy robotique » (meat proxy review)
L'auteur évoque ce piège mentionné au point 4.1 : le « meat proxy review » est devenu, pour de nombreuses équipes, un goulot d'étranglement particulièrement insidieux car il *ressemble* d'abord à une solution, alors qu'il aggrave la situation. Le schéma typique est le suivant :

1. L'équipe est submergée par les revues.
2. L'équipe décide de faire réviser les pull requests par son harnais IA local.
3. Les pull requests reçoivent un grand nombre de commentaires, dont certains sont pertinents et d'autres non — sans étude approfondie, il est difficile de distinguer les uns des autres, et on ne sait pas toujours si ces commentaires reflètent réellement le point de vue du relecteur humain. Il faut alors fournir un travail conséquent pour réfuter des commentaires avec lesquels le relecteur lui-même ne serait peut-être pas d'accord.
4. Ces équipes se mettent alors à utiliser leurs harnais pour répondre aux commentaires générés par d'autres harnais, transformant tout le processus de revue en une illusion qui ne favorise plus l'apprentissage et qui, surtout, pourrait se dérouler sans aucune implication des autres membres de l'équipe.

Dans tous les cas observés de « meat proxy review », l'équipe obtiendrait de meilleurs résultats en investissant plutôt dans un mécanisme de revue centralisé, dans la boucle de traitement des retours de ce mécanisme centralisé par le harnais, et en se contentant ensuite d'apposer son approbation.

### `fleet` : un harnais orchestré de façon centralisée
L'auteur mentionne brièvement leur autre approche pour réduire le volume de revue de code : `fleet`, leur harnais orchestré de façon centralisée (comparable aux « Minions » de Stripe, bien que sans suivre leur approche en un seul coup). Imprint s'appuie sur `fleet` pour implémenter et vérifier le logiciel dans un environnement hautement contrôlé fonctionnant dans le cloud, avec des mécanismes d'évaluation indépendants permettant de déterminer le nombre adéquat de relecteurs indépendants pour un changement donné. Ce nombre peut descendre jusqu'à un seul (`fleet` écrit, un humain relit) pour les changements évalués comme sûrs.

### Résultats, prochaines étapes et réception
L'auteur reconnaît qu'il est encore trop tôt pour tirer un bilan utile. D'après les premiers résultats, environ 10 % des changements se qualifient comme `small-change`. Ceux-ci sont désormais éligibles à une approbation très rapide, qu'ils obtiennent généralement sauf s'ils déclenchent une alerte, en général parce qu'ils touchent à un sujet lié à la sécurité ou à l'argent.

Même si 10 % reste un pourcentage modeste, le concept fonctionne sur le fond, et sa réussite dépendra en définitive de leur capacité à élargir ce pourcentage dans les mois à venir, en parallèle de l'élargissement de leurs mécanismes de vérification pour les rendre toujours plus complets. Tout cela réussira ou échouera selon leur capacité à améliorer leurs vérifications — un défi plus difficile à relever dans un contexte de faible complexité d'échelle mais de forte complexité métier, que dans les produits à forte complexité d'échelle mais faible complexité métier, où des techniques comme les déploiements incrémentaux sont exceptionnellement efficaces (elles restent utiles, mais couvrent moins de cas quand la plupart des utilisateurs ont des configurations et comportements différents).

L'accueil en interne n'a pas été uniformément enthousiaste : il s'agit d'un changement substantiel par rapport à la manière dont les équipes ont appris à être de bons ingénieurs, et il est inconfortable de devoir réévaluer si une bonne pratique de longue date n'est pas devenue un simple dogme. Ce qui est le plus stimulant dans le cycle actuel, c'est de pouvoir réévaluer chaque semaine ces pratiques avec lesquelles on a grandi ; ce qui est le plus difficile, c'est de savoir qu'ils risquent de prendre du retard s'ils cessent un jour de les réévaluer.

## Pourquoi ça compte
Ce témoignage concret montre comment une organisation d'ingénierie repense en temps réel ses processus de revue de code face à l'explosion de volume de PR générée par l'adoption des harnais d'IA — un sujet central pour toute veille sur l'impact opérationnel de l'IA générative dans le développement logiciel.
