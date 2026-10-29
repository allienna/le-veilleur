---
title: "How Meta Built Forum With AI-Native Engineering"
date: 2026-10-29
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fengineering.fb.com%2F2026%2F10%2F15%2Fml-applications%2Fhow-meta-built-forum-ai-native-engineering%2F%3Futm_source=tldrdev/1/010001a18238e1f8-ddd7e87c-e55b-4c81-83eb-9084da787664-000000/tDPyN3Kb8iZshz6BWxtlkVk4XTiggvZNz0bLF89KUVk=452"
keywords: ["IA agentique", "ingénierie logicielle", "Meta", "automatisation des tests", "vérification continue"]
theme: "IA"
tone: "research"
used_in: ["2026-10-29"]
---

## Résumé
Meta détaille comment son équipe a construit Forum, une nouvelle application dérivée des Groupes Facebook, en intégrant un agent IA comme véritable participant au cycle d'ingénierie plutôt que comme simple outil d'autocomplétion. L'équipe est passée d'un modèle human-in-the-loop à un modèle human-on-the-loop, où l'agent exécute lui-même les cycles de planification, implémentation, test et correction, sous la supervision d'un ingénieur qui fixe les objectifs et valide les résultats. Cette transition a nécessité d'adapter le code, les outils et l'environnement de test (isolation des builds, outils d'introspection de l'interface, tests de charge automatisés) plutôt que de simplement améliorer les prompts. Résultat : Forum a atteint la parité fonctionnelle avec Facebook Groups en huit semaines, avec une détection précoce d'un bug mémoire significatif et un gain de vélocité durable après le lancement.

## Points clés
- Passage du human-in-the-loop (l'IA assiste chaque étape pilotée par l'ingénieur) au human-on-the-loop (l'agent exécute la boucle complète, l'ingénieur supervise et valide le résultat).
- La vérification automatisée (statut de build, tests unitaires, correspondance avec les specs UI) est présentée comme le véritable multiplicateur de force, plus que la génération de code elle-même.
- Un modèle opérationnel à cinq composants — Rules, Skills, Agents, Commands, Hooks — structure l'intervention de l'agent dans le cycle d'ingénierie.
- Donner aux agents des outils d'introspection (hiérarchie de vues, état réel de l'écran) plutôt que des descriptions textuelles a fortement réduit les erreurs de localisation dans l'app.
- Un build séparé de type « bac à sable », qui partage le code et le design system de la production mais en exclut le code prototype, permet de prototyper avec l'IA sans risque pour les utilisateurs réels.
- Des agents de tests de charge ont détecté et corrigé un bug mémoire significatif avant le lancement, et Forum a atteint la parité fonctionnelle avec Facebook Groups en 8 semaines.

## Analyse approfondie
- Forum, la toute nouvelle application de Meta, s'adresse à tous ceux qui souhaitent aller plus loin dans les conversations de leurs groupes Facebook.
- Pour construire Forum, les ingénieurs de Meta ont adopté une toute nouvelle façon de travailler en intégrant un agent IA dans le cycle de développement.
- Nous partageons ici les enseignements tirés de la construction de Forum avec de l'IA agentique : comment nous avons adapté la base de code, testé des frameworks et des outils internes pour l'exécution agentique, ce qui a fonctionné, et ce qui n'a pas fonctionné.

Forum est une application autonome de Groupes, construite de zéro par une petite équipe. C'est aussi là que nous avons testé une façon différente de travailler : traiter un agent IA comme un participant au processus d'ingénierie plutôt que comme un moyen plus rapide de taper du code.

Cette expérimentation avait besoin d'une définition du succès, et la nôtre n'était pas le volume de code. Nous avons mesuré des résultats vérifiés, prêts pour la production — des changements qui compilent, passent les tests et survivent à la revue.

### Du human-in-the-loop au human-on-the-loop

Pointer l'IA uniquement sur l'étape de codage ne change pas grand-chose. Nos résultats se sont amplifiés lorsque nous avons étendu l'approche aux étapes entourant l'implémentation — planification, construction, test et vérification. La façon la plus claire de voir ce changement est de regarder qui possède chaque étape.

Avec le **human-in-the-loop**, l'ingénieur pilote chaque étape et l'IA l'assiste à l'intérieur de celle-ci en complétant automatiquement une fonction, en suggérant un correctif, ou en répondant à une question. Chaque itération avance au rythme de la personne qui la pilote.

Avec le **human-on-the-loop**, l'agent exécute lui-même l'itération — planifier, implémenter, construire, tester, corriger, répéter — tandis que l'ingénieur fixe l'objectif, observe l'exécution, intervient en cas de dérive, et approuve le résultat. Le rôle de la personne passe de l'exécution des étapes à la responsabilité du résultat et au maintien du niveau de qualité. C'est la cible vers laquelle nous nous dirigeons, pas un état achevé : certaines étapes s'exécutent aujourd'hui de façon autonome, tandis que d'autres maintiennent encore un ingénieur à chaque itération.

Lorsque l'ingénieur supervise, le travail cesse d'être strictement séquentiel. Des cycles qui s'exécutaient auparavant un par un peuvent désormais se superposer, et le temps de l'ingénieur est consacré à la direction et au jugement plutôt qu'à attendre que la boucle se termine. Mais cela ne tient que si ce qui revient peut être digne de confiance. Sans vérification, le code généré par l'IA crée un problème familier — une sortie plausible que personne n'a confirmée comme fonctionnelle, que l'ingénieur doit alors lire, déboguer et souvent jeter. Des signaux faibles ne suppriment pas la contrainte ; ils la déplacent de l'écriture de code vers la revue de code qui semble terminé et ne l'est pas.

Nous avons donc placé la barre au niveau de la vérification plutôt qu'à celui de la compilation. Compiler n'est pas la ligne d'arrivée — une tâche n'est complète qu'une fois que les tests automatisés et les contrôles visuels sont passés. Les agents vérifient leur propre travail avant qu'un ingénieur ne le voie, ce qui signifie que ce qui arrive en revue est un ensemble plus restreint de résultats à plus forte confiance plutôt qu'un tas de sorties à trier. Moins de choses sont générées, et moins de choses sont jetées. Chaque résultat livré porte toujours la validation d'un ingénieur ; notre effort a consisté à rendre cette validation rapide et bien étayée, avec les résultats de build, les résultats de tests et les sessions de vérification enregistrées jointes au changement.

Avec l'ingénieur hors de chaque cycle, la boucle doit pouvoir s'exécuter en toute sécurité par elle-même. Quatre capacités rendent cela possible :

**La planification comme spécification technique :** L'exécution agentique exige une précision extrême. Une ambiguïté qu'un ingénieur pourrait résoudre par intuition entraîne l'échec de l'agent. Nous avons investi dans une décomposition amont rigoureuse et un contexte lisible par la machine, ce qui a resserré la boucle d'ingénierie à la fois pour les ingénieurs et pour les agents.

**La vérification automatisée à l'intérieur de la boucle est le multiplicateur de force :** Nous avons intégré des signaux automatisés de réussite/échec — statut de build, tests unitaires, et correspondance avec les spécifications d'interface — directement dans la boucle de l'agent. Cela a permis un développement asynchrone produisant des pull requests prêtes à être revues, avec des plans de test pré-remplis et des sessions de vérification enregistrées. La vérification est la partie la plus difficile à bien faire, et la quantité que nous pouvons confier à la boucle en toute sécurité est déterminée par le niveau de confiance que nous pouvons accorder aux vérificateurs.

**Des tests utilisateurs simulés avec des agents :** Nous avons déployé des agents de navigation qui interagissent avec l'application en direct exactement comme le ferait une personne. Ces agents effectuent des actions, lisent l'écran et signalent les régressions. Les agents de navigation sont capables d'exécuter continuellement les mêmes chemins de vérification.

**Des opérations de production agentiques :** Après le lancement, des agents aident à automatiser l'analyse des causes racines. Lorsqu'un utilisateur de Forum envoie un retour, les agents utilisent ce retour pour enquêter sur d'éventuelles régressions. Les agents transmettent ensuite l'analyse aux ingénieurs, qui décident de la suite à donner.

### Le modèle opérationnel

Ce modèle de responsabilité nécessite une mécanique comportant cinq composants clés :

- **Les règles (Rules)** sont des instructions permanentes du projet. Lorsque l'agent répète une erreur plus de deux fois, nous encodons la correction une fois, pour tout le monde.
- **Les skills** transforment les conventions de l'équipe en étapes chargeables que l'agent peut invoquer.
- **Les agents** automatisent des vérifications qui nécessitaient auparavant un passage manuel.
- **Les commandes (Commands)** enchaînent des skills et des agents en workflows. Elles évaluent la complexité, reproduisent un bug, planifient et implémentent un correctif, créent la pull request, et exécutent une revue à plusieurs étapes.
- **Les hooks** sont des déclencheurs automatisés, comme l'exécution d'un linter après chaque tour de l'agent, la vérification de la connectivité au simulateur avant l'installation, et la validation des tests avant la création d'une pull request.

### Adapter l'environnement aux modèles

Les plus grands gains sont venus de la modification de notre code et de nos outils, pas de nos prompts.

**La lisibilité architecturale plutôt que la complexité héritée :** Nous avons travaillé à garder la base de code de Forum aussi simple que possible et avons choisi de modulariser les éléments clés de l'architecture afin de bénéficier d'une infrastructure éprouvée tout en permettant aux agents de s'y brancher facilement. Là où nous ne pouvions pas le faire facilement, nous avons reconstruit à partir de zéro, sacrifiant la réutilisation au profit du débit agentique, ce qui s'est révélé payant en vitesse de développement. Les agents apprennent des patterns à partir du code qu'ils lisent. Corrigez un pattern faible une fois, et chaque future session d'agent hérite de l'amélioration ; laissez-le tel quel, et le même raccourci réapparaît dans tout ce que l'agent écrit par la suite.

**Donner aux agents des outils, pas des descriptions :** Notre principal mode d'échec était que l'agent perdait la trace de l'endroit où il se trouvait dans l'application — modifiant le fil d'actualité principal alors qu'on lui demandait de changer l'écran d'accueil d'un groupe, ou devinant les coordonnées d'un écran. Nous avons donc, au lieu de décrire l'application à l'agent, lui donné des outils pour vérifier : lire la hiérarchie de vues en direct depuis le simulateur, lister les éléments réellement présents à l'écran, et rechercher le chemin vers une vue cible — tout cela avant d'agir. Les modifications mal dirigées ont fortement chuté. Nous avons appliqué la même approche partout où les agents touchaient à nos systèmes : donner à l'agent un moyen de vérifier l'état directement plutôt qu'une description à partir de laquelle raisonner.

**L'isolation au niveau du build pour un prototypage IA sûr :** À mesure que Forum mûrissait vers la production, nous avons voulu que les prototypes en phase précoce et les expérimentations générées par agent aient de la place pour s'exécuter, tout en maintenant l'application de production strictement limitée au travail terminé et revu. Nous voulions une garantie plus forte que le simple feature gating, où le code de prototype existe toujours à l'intérieur du build de production. Notre solution a été un **flavor de build séparé**, une application bac à sable qui partage exactement la même base de code, les mêmes frameworks et le même design system que la production, mais qui compile le code de prototype *hors* du build de production entièrement, via une architecture de type plugin/socket.

Cela nous a apporté trois choses à la fois :

- Les designers et les partenaires transverses pouvaient prototyper librement avec des outils IA sans avoir besoin d'un ingénieur dans la boucle pour chaque changement.
- Tout ce qui était construit dans le bac à sable pouvait être porté directement en production sans reconstruction.
- Aucun code de prototype ne pouvait faire planter l'application de production car il n'existait physiquement pas dans ce build.

Ce pattern nous a permis de conserver une itération IA rapide *après* avoir eu de vrais utilisateurs sur l'application à protéger.

### Trouver de vrais bugs grâce aux tests de charge par IA

Adapter l'environnement a fait plus que rendre l'agent plus rapide à construire — cela a fait de l'agent un testeur. Nous ne l'avons pas pointé vers un défaut spécifique. Nous avons plutôt mis en place des scénarios de stress reproductibles qui imitent le comportement réel des utilisateurs (défilement agressif, navigation aléatoire dans les groupes, navigation rapide, chargement répété de médias) et les avons exécutés de façon routinière sur l'ensemble des builds. Parce que ces exécutions produisent des signaux cohérents (plantages, croissance de la mémoire, défauts de page, régressions d'interface), l'agent peut trier les anomalies, les restreindre à la séquence qui les déclenche, puis enquêter sur la cause racine.

Une de ces exécutions a mis en évidence un problème de mémoire. L'agent a isolé une reproduction, proposé un correctif, et l'a vérifié — tout cela pendant le développement, avant que l'application n'atteigne les utilisateurs. Le correctif a réduit de façon significative la croissance de la mémoire sur l'appareil et les défauts de page lors de sessions de stress répétées.

Pendant que les ingénieurs prenaient les décisions architecturales, la détection et le suivi des régressions étaient automatisés et reproductibles ; une fois une anomalie détectée, l'agent pouvait reproduire → isoler → proposer un correctif → vérifier avec le même harnais.

### Appliquer la même discipline au fil d'actualité de Forum

Nous avons appliqué l'approche human-on-the-loop à deux endroits :

**Construire la stack :** Les agents ont cartographié les options architecturales et leurs compromis ; les ingénieurs les ont ensuite évaluées et choisies. Ce que nous avons délibérément gardé humain, c'est la cible — décider à quoi ressemble un bon résultat est un jugement produit, pas quelque chose que le système devrait définir lui-même.

**Faire fonctionner la stack :** Les questions qui nécessitaient auparavant l'ingénieur connaissant le chemin de code concerné vont désormais à un agent d'investigation qui réunit ce dont il a besoin et publie un compte-rendu avec des correctifs suggérés. Après avoir noté manuellement un lot d'investigations réelles, nous sommes arrivés à un workflow où l'agent condense le travail mécanique et livre un compte-rendu structuré à un ingénieur, qui valide ensuite si une découverte est un véritable bug ou un compromis intentionnel.

Ce qui a amélioré la qualité n'était pas un meilleur prompting. C'était le contexte. Une catégorie récurrente d'investigations restait faible jusqu'à ce que nous donnions à l'agent les mêmes repères vers le code pertinent, des exemples de requêtes, et des documents de conception que nous donnerions à tout nouvel ingénieur le premier jour. La qualité de cette catégorie a bondi. La différence avec l'onboarding humain, c'est qu'on entraîne une seule fois, et que chaque future session démarre à partir de cela.

### Est-ce que ça a fonctionné ?

Au-delà d'expédier plus vite, nous avons expédié plus proprement. La vérification continue a mis en évidence des problèmes systémiques — comme le goulot d'étranglement mémoire mentionné plus haut — pendant le développement plutôt qu'après le lancement. Les résultats se retrouvent dans le profil de performance :

- **Une qualité détectée tôt :** La boucle de tests de charge autonome a détecté et corrigé le problème de mémoire mentionné précédemment pendant le développement plutôt qu'après le lancement, réduisant de près de moitié l'utilisation de la mémoire et les défauts de page.
- **Vélocité :** Forum a atteint la parité fonctionnelle de base avec Facebook Groups en huit semaines, l'IA prenant en charge une grande partie de l'implémentation de routine, ce qui a permis aux ingénieurs de se concentrer sur l'architecture, les décisions produit et la qualité.
- **Un effet de levier qui a duré :** Après le lancement, l'investigation pilotée par agent a aidé les ingénieurs à trier et à identifier la cause racine des retours utilisateurs.

L'IA a fait plus que générer du code. Elle a resserré notre boucle de qualité, aidant une petite équipe à livrer une application de haute qualité avec moins de retouches continues.

### Ce qui a fonctionné, et ce qui n'a pas fonctionné

### Remerciements

Nous remercions Neeharika Sinha, Jane Kou, Gang Yang, Guohao Zhang, Zeya Zhang, Kinnary Jangla, et Yonghui Lu pour leurs contributions précieuses.

## Pourquoi ça compte
Ce retour d'expérience de Meta offre un cas concret et chiffré de l'IA agentique appliquée à un cycle de développement logiciel complet, au-delà du simple assistant de code — un signal utile pour quiconque évalue comment structurer l'autonomie des agents en ingénierie.
