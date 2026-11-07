---
title: "AI just raised the interest rate on your technical debt"
date: 2026-11-07
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fhitesh.in%2F2026%2Fai-raised-the-interest-on-technical-debt%2F%3Futm_source=tldrit/1/010001a1b103aecf-7f6aba2a-9836-49b7-ba3c-81ff30300544-000000/DPRNYv6nV2pw_y_xudk0s-JCGTzDoG-x0w8jAAgVVuQ=452"
keywords: ["dette technique", "IA offensive", "vulnérabilités", "open source", "PHP", "gestion des risques"]
theme: "Sécurité"
tone: "opinion"
used_in: ["2026-11-07"]
---

## Résumé
L'article revient sur PHP2Shell, une faille critique de PHP corrigée en urgence fin octobre, née d'un bug de dépassement de mémoire signalé dès 2024 et classé "faible priorité" parce qu'il semblait inoffensif. Une recherche assistée par IA, financée par OpenAI via la société d'audit Calif, a transformé ce bug mineur en exécution de code arbitraire en deux semaines, tandis que le correctif a nécessité quatre ingénieurs pendant deux mois. L'auteur en tire une thèse plus large : les niveaux de gravité attribués aux vulnérabilités reposaient implicitement sur le coût humain requis pour les exploiter, coût que l'IA fait désormais chuter, rendant obsolètes des années de dettes techniques "acceptées". Il propose une liste d'actions concrètes pour que les dirigeants réévaluent leur exposition avant qu'un incident ne les y force.

## Points clés
- La faille PHP2Shell provient d'un bug connu depuis 2024, jugé bénin car il ne causait "que" des plantages par manque de mémoire.
- Des chercheurs utilisant l'IA ont transformé ce bug en exécution de code à distance en deux semaines seulement, alors que le correctif a mobilisé quatre ingénieurs pendant deux mois.
- La gravité d'une vulnérabilité a toujours été une estimation implicite du coût pour l'attaquant (temps, compétence) plutôt qu'une mesure intrinsèque du danger.
- L'IA fait chuter ce coût d'exploitation plus vite que la vitesse humaine de correction, créant une asymétrie croissante entre découverte et réparation.
- La dette technique se comporte comme un prêt à taux variable : le "taux" (coût d'exploitation) baisse grâce à l'IA, ce qui augmente le risque réel sans que le "principal" (code ancien non corrigé) ait changé.
- L'auteur recommande de prioriser la suppression des systèmes obsolètes et sans propriétaire plutôt que de les corriger, et de revoir trimestriellement les risques "acceptés".

## Analyse approfondie

### Le contexte : l'affaire PHP2Shell
Fin octobre, PHP a publié des correctifs d'urgence pour une faille baptisée PHP2Shell, qui exposait des sites allant d'installations WordPress à des pages gouvernementales. Selon IEEE Spectrum, le bug sous-jacent était une erreur de dépassement de mémoire signalée dès 2024. Ce type d'erreur ne provoque habituellement qu'un plantage du programme, elle avait donc été classée comme peu prioritaire et laissée de côté.

Une société de sécurité, Calif, a ensuite proposé d'auditer PHP avec le parrainage d'OpenAI. En deux semaines, un chercheur utilisant des outils d'IA a trouvé le moyen de transformer ce simple plantage en exécution de code arbitraire sur le serveur hôte. La correction a nécessité quatre ingénieurs pendant deux mois.

Matt Suiche, cité dans le même article, résume la situation sans détour : "C'est maintenant l'heure de payer la dette technique." L'auteur partage ce diagnostic, mais estime que la question utile pour un dirigeant (CEO ou CTO) est plus précise : lesquelles de vos propres décisions reposaient silencieusement sur la difficulté que les attaquants devaient surmonter ?

### La gravité n'a jamais été qu'un pari sur le coût de l'attaquant
Chaque étiquette "faible priorité" ou "ne sera pas corrigé" repose sur une hypothèse jamais formulée explicitement : transformer ce bug en attaque réelle demanderait plus de compétence, de temps et de patience que quiconque ne voudrait y consacrer. Pendant des décennies, ce pari était raisonnable. Enchaîner une corruption de mémoire jusqu'à une exécution de code fonctionnelle exigeait un spécialiste rare, menant un raisonnement très spécifique — et les spécialistes rares sont chers et occupés.

Suman Jana, de Columbia, également cité par Spectrum, décrit ce raisonnement comme "pas vraiment sorcier" mais exigeant "beaucoup de raisonnement très spécifique" pour déterminer quelles zones mémoire cibler et quels bits écraser — un exercice dans lequel l'IA excelle précisément. Dès que cette ressource rare devient bon marché, l'étiquette perd le sens qu'elle avait au moment où quelqu'un l'a saisie. L'auteur établit un parallèle avec les mots de passe : ce qui protégeait la plupart des entreprises n'était jamais leur robustesse intrinsèque, mais le coût du temps que l'attaquant devait y consacrer.

Il note un schéma récurrent : les registres de "risques acceptés" sont presque jamais révisés selon un calendrier régulier. On les relit après un incident — un peu comme ne vérifier son taux d'intérêt que lorsque la banque appelle.

### Le goulot d'étranglement s'est déplacé vers la correction
Trouver le bug a pris deux semaines. Le corriger a pris environ quatre fois plus de temps et quatre ingénieurs. C'est cette asymétrie que l'auteur mettrait devant un conseil d'administration : la découverte devient moins coûteuse mois après mois, tandis que la réparation reste à un rythme humain, et doit en plus éviter de casser tout ce qui dépend du code en question.

La dette technique se comporte comme un prêt à taux variable. Le principal, c'est l'ensemble du code ancien et des décisions reportées déjà accumulées. Le taux, c'est la facilité avec laquelle quelqu'un peut l'exploiter. La capacité de remboursement, c'est le nombre de semaines-ingénieur qu'on peut réaffecter à un correctif critique sans arrêter l'activité. La plupart des équipes dirigeantes ne suivent aucun des trois indicateurs. Elles savent que la dette existe, au sens vague où toute entreprise le sait, mais elles ne se sont jamais demandé à quelle vitesse elles pourraient rembourser une portion spécifique de cette dette.

Il existe aussi une version plus optimiste. Jana évoque une récente publication d'Anthropic où un modèle écrit un correctif tandis qu'un autre produit une preuve de correction, vérifiée par un outil formel, car, comme il le dit, "les LLM hallucinent". L'auteur juge que c'est la bonne direction, mais ne bâtirait pas encore un budget sur cette base : cela aide les équipes qui savent déjà déployer rapidement un correctif, mais n'apporte rien à celles dont la dernière mise à jour a pris un an.

### Supprimer avant de corriger
Chaque ligne de code est un passif, et on a toujours géré ce risque en décidant de ne pas construire certaines choses. Les assistants de codage, eux, ont tendance à ajouter tout ce qu'on leur demande. L'auteur ne considère pas cela comme acquis, mais y voit un levier d'action pour les dirigeants.

La vulnérabilité la moins chère à corriger est celle d'un code qu'on ne fait plus tourner. La plupart des entreprises matures conservent des services, des plugins, des bibliothèques et des sites entiers que personne ne possède ni n'utilise, et qui se trouvent pourtant dans la même surface d'attaque que les systèmes qui génèrent du revenu. Retirer un tel système coûte un projet ponctuel. Le défendre coûte une astreinte permanente tant qu'il existe. Si les attaquants sondent désormais tout à coût quasi nul, un système oublié sera la première cible, car personne ne le surveille.

Le même raisonnement s'applique à un niveau supérieur. Des projets open source comme PHP font fonctionner une grande partie du web, généralement sans ligne de revenu claire pour financer leur défense. Jana estime que les laboratoires d'IA devraient faire don de budgets de tokens pour aider. Qu'ils le fassent ou non, l'exposition de l'entreprise à ces projets lui appartient, et l'auteur voudrait savoir lesquels se trouvent sous ses systèmes critiques.

### Ce que l'auteur ferait ce trimestre
Si l'auteur conseillait une entreprise sur ce sujet, il garderait une liste courte, à suivre dans l'ordre :

1. Ressortir chaque ticket de sécurité marqué faible, reporté ou "ne sera pas corrigé" datant de plus de douze mois, et le réévaluer en supposant un attaquant doté d'une patience illimitée et d'un assistant IA compétent.
2. Commencer par tout ce qui est accessible depuis internet. Si la liste réévaluée compte plus qu'une poignée d'éléments, voilà la réponse sur l'ampleur de la dette portée.
3. Lister chaque système exposé à internet sans propriétaire désigné. En assigner un, ou planifier son retrait. Si personne ne veut en prendre la responsabilité, c'est le signe qu'il peut disparaître.
4. Mesurer le délai entre l'avis de sécurité et la mise en production du dernier correctif critique. S'il a fallu plus d'une semaine, comprendre où le temps a été perdu avant de budgétiser quoi que ce soit d'autre.
5. Compter le nombre de semaines-ingénieur qu'un correctif de l'ampleur de celui de PHP coûterait, et comparer ce chiffre à ce qu'on pourrait réellement libérer sans geler l'activité.
6. Identifier les trois projets open source dont dépendent le plus les systèmes critiques, et déterminer qui les maintient et comment ils sont financés.
7. Inscrire le registre des risques acceptés à l'agenda, pour une révision chaque trimestre, et non après un incident.

La question à ramener à son équipe est simple : quels risques avons-nous acceptés parce que les attaquants étaient lents, et quel est notre plan pour le jour où ils ne le seront plus ?

## Pourquoi ça compte
Ce texte recadre un sujet de veille sécurité classique (la dette technique) à l'aune de l'IA offensive : il montre concrètement, via un cas réel (PHP2Shell), que l'IA ne crée pas seulement de nouvelles menaces mais réévalue silencieusement tout un historique de risques jugés "acceptables", ce qui en fait un signal d'alerte actionnable pour toute organisation gérant du code legacy ou des dépendances open source.
