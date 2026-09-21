---
title: "Issue #70 – The Debt AI Creates"
date: 2026-09-21
url: "https://open.substack.com/pub/thedataecosystem/p/issue-70-the-debt-ai-creates?utm_source=multiple-personal-recommendations-email&utm_medium=email&token=eyJ1c2VyX2lkIjo0NzU1OTI2MjgsInBvc3RfaWQiOjIxNjE4Mjg3MSwiaWF0IjoxNzg5OTM3NjkyLCJleHAiOjE3OTI1Mjk2OTIsImlzcyI6InB1Yi0yNDg1MjQ2Iiwic3ViIjoicG9zdC1yZWFjdGlvbiJ9.fa-OAGH-zEJTbJAmZLTQE_j2ArOghlPZJKTB67IdyL4"
keywords: ["dette technique", "IA générative", "gouvernance IA", "context engineering", "AgenticOps"]
theme: "IA"
tone: "opinion"
used_in: ["2026-09-21"]
---

## Résumé
L'article définit la « dette IA » comme tout ce que les outils, agents et systèmes construits avec l'IA produisent sans que personne ne le relise, n'en soit responsable ou ne puisse l'expliquer plus tard. Elle provient de trois sources : la dette technique et contextuelle déjà existante que l'IA hérite, les productions générées à bas coût mais jamais vérifiées, et la « dette mémoire » accumulée par les assistants IA au fil des sessions. L'auteur soutient que la vitesse de construction avec l'IA dépasse largement notre capacité de relecture, créant une boucle où du contenu générique nourrit du contenu encore plus générique. Il propose cinq leviers pour limiter cette dette, à l'échelle individuelle, d'équipe et d'entreprise.

## Points clés
- La dette IA a trois origines : la dette contextuelle héritée (données et organisation déjà défaillantes), les productions IA bon marché jamais relues, et la dette mémoire (contexte qui dérive sans traçabilité entre sessions).
- Une étude Microsoft Research / Carnegie Mellon sur 319 travailleurs du savoir montre que plus la confiance envers l'IA augmente, moins l'esprit critique est mobilisé.
- 66 % des développeurs jugent que le code généré par IA est "presque bon mais pas tout à fait", et 45 % estiment que le débogage de ce code prend plus de temps.
- Les rôles techniques accumulent la dette dans des artefacts (code, agents, POC abandonnés) ; les rôles non techniques l'accumulent dans des documents et décisions (l'auteur compare cela à un fichier Excel qu'une seule personne sait expliquer).
- Cinq remèdes proposés : inventorier ce qui a été construit, intégrer la maintenance dès la conception ("AgenticOps"), organiser le contexte/la mémoire/les fichiers, nettoyer régulièrement l'existant, et s'assurer que quelqu'un peut toujours expliquer ce que l'IA a produit.
- L'auteur cite Animesh Kumar sur la dette mémoire (écart croissant entre ce que la mémoire d'un système IA contient et la capacité à l'inspecter, corriger, auditer ou transférer) et un sondage Stanford/BetterUp indiquant qu'environ 40 % des employés de bureau américains ont reçu du travail généré par IA de piètre qualité ("AI workslop") dans le mois précédent.

## Analyse approfondie
L'auteur part d'un constat : construire avec l'IA est devenu trivial et bon marché (il cite Lovable, valorisée 1,8 milliard de dollars huit mois après son lancement, et Base44, revendue 80 millions de dollars à Wix environ six mois après sa création par une seule personne). Mais la facilité de construction ne garantit pas la qualité : le développement rigoureux suppose normalement de concevoir, cadrer, collaborer, tester et itérer — un processus que la vitesse de l'IA court-circuite, créant ce que l'auteur appelle la "dette IA", en écho à la dette technique classique.

Il distingue trois sources de cette dette :

1. **La dette contextuelle héritée** : un agent IA branché sur une organisation hérite de définitions incohérentes, de dossiers mal organisés et de systèmes disparates. Comme le dit l'auteur, on ne peut pas "sortir de cette dette à coups de meilleurs prompts" — si le contexte sous-jacent n'est pas cartographié, un prompt plus habile ne produit qu'une version plus confiante d'une mauvaise réponse.

2. **La dette liée aux constructions bon marché** : les raccourcis pris lors de builds rapides (vibe coding) dégradent la qualité au fil des mises à jour. L'auteur relie cela à un problème de cadrage : la distinction entre "ce dont on a besoin" et "ce qu'on veut" s'efface quand produire un outil ne prend qu'une journée, et les parties prenantes ignorent souvent qu'un outil doit être testé, déployé, surveillé et maintenu.

3. **La dette mémoire**, propre à l'IA : les assistants conservent des informations d'une session à l'autre (rôle, préférences, contexte projet), ce qui évite de tout répéter, mais cette mémoire devient une dépendance mal comprise. L'auteur reprend d'Animesh Kumar quatre problèmes : dérive sans contrôle de version, savoir institutionnel sans sauvegarde (piégé chez un fournisseur), impossibilité de retracer la provenance d'une réponse erronée, et impossibilité d'intégrer de nouvelles personnes puisque le fonctionnement réel est enfermé dans la mémoire de l'agent plutôt que documenté. Il ajoute un cinquième problème : la discontinuité du contexte entre sessions, illustrée par son propre exemple où son IA a continué de croire qu'il vivait à Londres plusieurs mois après son retour à Toronto.

Sur les **coûts** de cette dette, l'auteur identifie trois effets : la relecture humaine ne suit plus le volume produit (les équipes cessent de relire, simulent la relecture, ou délèguent la relecture à d'autres agents) ; la perte de compréhension de ce qu'on construit, visible dans la production de contenu générique ("AI slop") ; et un effet cumulatif où du contenu générique nourrit la génération suivante, érodant la pensée critique jusqu'à créer une dépendance totale à l'IA pour fonctionner.

Pour **limiter la dette**, il propose cinq principes, déclinés à l'échelle individuelle, d'équipe et d'entreprise :
- **Savoir ce qui a été construit** : tenir un inventaire des agents, tâches planifiées et fichiers mémoire, jusqu'à une gouvernance formelle (propriété nommée, traçabilité des données) au niveau entreprise.
- **Intégrer la maintenance dès la conception ("AgenticOps")** : prioriser réellement les besoins, distinguer les prototypes jetables des produits qui doivent survivre sans leur créateur.
- **Organiser contexte, mémoire et fichiers** : consacrer du temps à structurer ses fichiers de contexte et à les corriger à la source ; à terme, viser une couche de contexte partagée et gouvernée (l'auteur recommande le livre de Jessica Talisman sur le sujet).
- **Réduire la dette existante** via des nettoyages réguliers (individuels, d'équipe trimestriels, ou une équipe dédiée en entreprise).
- **S'assurer que quelqu'un peut expliquer** ce que l'IA a produit — README automatiques, revues de spécifications, traçabilité en production — en évitant que la confiance envers l'IA ne remplace l'esprit critique, tendance confirmée par l'étude Microsoft Research/CMU citée plus haut.

Enfin, l'auteur note que cette dette touche différemment les métiers : les profils techniques ont déjà des réflexes (versioning, revue de code, tests, CI) mais sont dépassés par le volume ; les profils non techniques, dépourvus de ces réflexes, accumulent une dette purement documentaire et décisionnelle, illustrée par la comparaison avec un tableur Excel que seule une personne sait expliquer — un phénomène qui, selon lui, risque de se généraliser à mesure que davantage de non-techniciens construisent avec l'IA.

L'article conclut une trilogie sur la dette technique, la dette de données et la dette IA, en insistant sur le fait que comprendre l'origine, le coût et les leviers de réduction de chaque type de dette permet de construire de façon plus durable, sans prétendre les éliminer totalement.

## Pourquoi ça compte
Ce cadre conceptuel offre une grille de lecture utile pour la veille tech : à mesure que les organisations adoptent massivement les agents IA et le vibe coding, la question de la gouvernance, de la traçabilité et de la maintenabilité des outputs IA devient un enjeu opérationnel central, au même titre que la dette technique l'a été pour le développement logiciel classique.
