---
title: "How the Claude Code team does code review / claude.dev Blog"
date: 2026-10-26
url: "https://leadershipintech.com/links/23569/3d78f33c-7ca0-4e03-9c70-68e56918a4cd/email"
keywords: ["revue de code", "agents IA", "Claude Code", "CI/CD", "ingénierie logicielle"]
theme: "Software"
tone: "news"
used_in: ["2026-10-26"]
---

## Résumé
L'article décrit comment l'équipe Claude Code a fait évoluer sa revue de code face à l'explosion du volume produit par les agents IA : Claude écrit désormais environ 90% du code de Claude Code lui-même. Entre juin et septembre, le nombre de pull requests fusionnées a plus que doublé tandis que le taux de reverts a chuté de plus de 40%. La stratégie n'est pas de supprimer la revue humaine mais de déplacer la majorité de la lecture vers des agents automatisés, en réservant l'attention humaine aux décisions à forte valeur ajoutée, et en investissant massivement dans la capacité à détecter et corriger rapidement les erreurs plutôt qu'à les prévenir à tout prix.

## Points clés
- La revue se déclenche désormais en continu avant même l'ouverture d'une PR (tests, builds, captures d'écran comparées au design), plutôt qu'en une seule étape finale.
- Chaque PR passe par une revue automatisée par Claude qui vérifie la cohérence avec l'intention et le reste du code, puis par un vote de plusieurs agents pour valider les anomalies détectées avant de les remonter à un humain.
- Un système de classification du risque (faible/moyen/élevé) détermine combien d'approbations humaines sont nécessaires ; les changements à faible risque peuvent fusionner sans validation humaine si les contrôles automatisés sont au vert.
- La personne qui a piloté l'agent reste responsable de la PR, au même titre que si elle avait écrit le code elle-même.
- L'équipe surveille le "bruit" généré par les revues automatisées (faux positifs, boucles de correction infinies entre agent auteur et agent relecteur) pour éviter de gaspiller du temps humain ailleurs.
- La connaissance du code ne passe plus par la lecture systématique des diffs, mais par des explications générées à la demande par Claude sur une portion précise du code.

## Analyse approfondie
L'article détaille l'architecture de revue mise en place par l'équipe Claude Code pour absorber la croissance massive du volume de changements de code induite par la génération assistée par IA (passant d'environ 2500 changements par jour en mai à plus de 30 000 en septembre dans le monorepo d'Anthropic).

Le principe directeur est de remplacer la question "un humain a-t-il lu le code ?" par "quel contrôle, automatisé ou humain, est le mieux placé pour détecter tel type de problème ?". Concrètement, plusieurs couches s'enchaînent :

1. **Avant la PR** : l'agent doit démontrer que son code fonctionne (tests, build, capture d'écran) plutôt que de simplement affirmer que c'est fait ; un sous-agent relit le diff avec un regard neuf ; des "skills" internes traquent les bugs, simplifient le diff et vérifient le comportement de bout en bout.
2. **Fichiers de configuration** : `CLAUDE.md` décrit le projet (stack, conventions, objectifs) et est chargé à chaque revue ; `REVIEW.md`, rédigé par les propriétaires du code, précise ce qui compte vraiment pour chaque zone du dépôt et ce qui doit être ignoré.
3. **Revue automatisée par PR** : chaque PR est examinée par Claude avant tout regard humain ; plusieurs agents cherchent des bugs en parallèle, puis un groupe distinct "vote" pour ne retenir que les signalements jugés suffisamment fiables, étiquetés par sévérité (Important, Nit, Pre-existing). Chaque signalement doit être traité (corrigé ou clos avec justification).
4. **Sécurité** : une revue de sécurité automatisée bloque la fusion tant qu'un signalement reste ouvert, avec un mécanisme équivalent disponible publiquement via une GitHub Action ou la commande `/security-review`.
5. **Contrôles classiques** : lint, vérification de types, tests multiplateformes et build, exécutés en grand nombre sur chaque PR.
6. **Gestion du risque** : un classifieur détermine le niveau de risque du changement (faible, moyen, élevé) et le nombre d'approbations humaines requises ; certains chemins sensibles (ex. fichiers de workflow CI) exigent toujours une validation humaine ; seuls les auteurs de confiance accèdent aux parcours allégés ; une approbation agent ne compte jamais comme une approbation humaine ; toute nouvelle validation de commit remet le compteur d'approbation à zéro.
7. **Après fusion** : une file de fusion re-teste chaque changement contre la branche principale ; les nouveautés sont d'abord déployées en interne chez Anthropic avant le grand public, avec des mécanismes de rollback rapide (flags désactivables sans déploiement) et une astreinte hebdomadaire.

L'équipe insiste sur une boucle d'amélioration continue : les incidents passés alimentent un jeu de test ("eval") quotidien pour le relecteur automatisé ; le bruit généré par les faux positifs est mesuré en observant comment les auteurs réagissent aux commentaires (correction, contestation, ou indifférence) ; et l'équipe a constaté qu'une majorité des signalements répétés concernaient du code déjà présent lors du premier passage, ce qui a conduit à revoir la fréquence des relectures successives plutôt que d'en multiplier les rounds par défaut.

Enfin, l'article aborde la question de la transmission de connaissance : sans lecture systématique des diffs par les humains, l'équipe compense en demandant à Claude de générer des explications ciblées sur une portion de code au moment où quelqu'un en a besoin, complétées par une culture de travail en canaux Slack ouverts qui permet à chacun de suivre ce que font les autres en temps réel.

## Pourquoi ça compte
Ce retour d'expérience illustre concrètement comment une organisation d'ingénierie repense ses processus de qualité et de gouvernance du code lorsque la production de code devient majoritairement assistée par IA, un enjeu central pour toute équipe tech qui voit croître la part de code généré par des agents.
