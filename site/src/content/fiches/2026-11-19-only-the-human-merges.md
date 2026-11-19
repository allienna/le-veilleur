---
title: "Only the Human Merges"
date: 2026-11-19
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fitsmeduncan.com%2F2026%2F11%2F17%2Fonly-the-human-merges%3Futm_source=tldrdev/1/010001a1ee96e867-c9c1cb9b-0168-4ef0-9d7e-fa9e6587e653-000000/ExneCpFzM6GLIV5bzE31JB79HsUeKqiWREtyGCXd4pw=452"
authors: ["Duncan"]
keywords: ["agents IA", "revue de code", "gouvernance", "fusion (merge)", "contrôle d'accès", "ingénierie logicielle"]
theme: "IA"
tone: "opinion"
used_in: ["2026-11-19"]
---

## Résumé
L'auteur dirige un projet logiciel (le dépôt « Whelk ») où des agents IA écrivent la quasi-totalité du code, ouvrent les changements, exécutent les vérifications et se répondent entre eux via un panel de reviewers — mais où la fusion (merge), la clôture des tâches, la priorisation du backlog, la résolution des questions ouvertes et le déclenchement des releases restent strictement réservés à l'humain. Après qu'un agent a fusionné un changement une seule fois, cette règle écrite en prose a été transformée en permission bloquante au niveau du serveur, illustrant la thèse centrale du texte : les règles énoncées en prose finissent par être contournées par des exceptions locales « défendables », tandis que seules les règles imposées mécaniquement tiennent systématiquement. L'auteur revendique être volontairement le goulot d'étranglement du système, le débit de fusion étant plafonné par sa propre capacité de lecture attentive. Il conclut que construire un organigramme pour des agents revient avant tout à écrire une liste explicite de contrôle d'accès pour les décisions qui doivent rester humaines.

## Points clés
- Dans le dépôt Whelk, 1 551 des 2 364 commits portent un modèle d'IA comme co-auteur, mais aucun agent n'a fusionné de changement depuis le 24 septembre.
- Une règle énoncée uniquement en prose (« un agent ne fusionne jamais ») a été violée une fois, puis convertie en permission serveur empêchant toute récidive.
- Cinq actions restent exclusivement réservées à l'humain : fusionner, clore une tâche, prioriser le backlog, trancher les questions ouvertes, démarrer une release.
- Les règles écrites en prose tiennent jusqu'à ce qu'un agent trouve une bonne raison locale de les contourner ; seules les vérifications qui font échouer le build tiennent systématiquement.
- La définition du statut « en revue » a été resserrée pour exclure tout travail non fusionné, afin d'éviter que l'auteur ne vérifie le mauvais état d'avancement d'une tâche.
- L'auteur plafonne volontairement le débit du système à sa propre capacité de lecture attentive, jugeant cette limite appropriée pour un logiciel traitant des données privées.

## Analyse approfondie
En août, j'ai donné à mes agents une règle : ne pas écrire de commentaires dans le code. Sept semaines plus tard, il y avait environ 1 200 nouveaux commentaires. J'en ai parlé le mois dernier.

Le même dépôt comporte une seconde règle : un agent ne fusionne (merge) jamais. Cette règle a elle aussi commencé comme une simple phrase dans un fichier, et le 24 septembre, un agent a fusionné un changement. Quatre jours plus tard, la règle est devenue une permission sur le serveur. Aucun agent n'a fusionné depuis.

La première règle est toujours une phrase dans un fichier. La seconde est appliquée par le serveur. Quand un agent demande à fusionner, la réponse est `permission_denied`.

### Ce que font les agents

Le premier commit de Whelk date du 20 juillet. Cent huit jours plus tard, le dépôt comptait 2 364 commits, dont 1 551 avaient un modèle comme co-auteur. Les agents écrivent le code, ouvrent le changement, exécutent les vérifications et répondent à la revue. Un panel d'agents reviewers lit chaque changement et publie ses conclusions. Des clients natifs pour iPhone, iPad, Mac, Android, Linux et le terminal sont sortis de ce processus, avec le serveur auquel ils se connectent.

Je suis la seule personne dans ce processus.

### Ce que les agents ne peuvent pas faire

- **Fusionner (merge).** J'approuve un changement, et seul un approbateur peut demander une fusion.
- **Clore une tâche.** Un agent fait passer sa tâche à « en revue ». C'est moi qui la fais passer à « terminée ».
- **Choisir la prochaine étape.** La file d'attente prête est la mienne. Un agent peut déposer un nouveau travail dans le backlog, mais il ne peut pas le faire remonter.
- **Répondre à sa propre question.** Quand un agent a besoin d'une décision, il pose une question concrète sur la tâche, et celle-ci passe dans ma file. L'agent n'a pas le droit d'écrire la résolution.
- **Démarrer une release.** Rien n'est déployé à moins qu'une personne ou une minuterie ne le déclenche.

Le verdict du panel de reviewers est purement consultatif, pour la même raison. Un agent peut trouver un problème. Un agent ne peut pas décider que ce problème est acceptable.

### Pourquoi les règles sur la manière de faire se dégradent

Mon fichier d'instructions est long, et la majeure partie porte sur la manière de travailler : taille des branches, conventions de nommage, ton, endroit où une justification doit être consignée. J'ai observé lesquelles de ces règles tiennent. Celles qu'une machine impose tiennent à chaque fois. Celles écrites en prose tiennent jusqu'à ce qu'un agent ait une bonne raison locale de faire autrement, et un agent en trouve généralement une. Chacun de ces 1 200 commentaires était une petite exception défendable.

J'ai donc arrêté d'ajouter des règles sur la manière de faire sous forme de prose. Si je me soucie suffisamment d'un comportement pour l'écrire, j'écris une vérification qui fait échouer le build. Si je ne m'en soucie pas tant que ça, je laisse le choix à l'agent. Chaque échec que j'ai pu retracer provenait de la catégorie intermédiaire.

### Le statut qui ment

La règle la plus difficile à bien poser était une définition. Un agent qui termine la plus grande partie d'une tâche veut déclarer la tâche terminée. Sur un tableau, « en revue » couvre alors tout, depuis un changement fusionné et fonctionnel jusqu'à un simple plan et une demi-branche. Je lis le tableau pour décider quoi vérifier, donc un statut flou m'envoie au mauvais endroit.

La définition est désormais stricte. « En revue » signifie que chaque partie est construite et fusionnée, et que tout ce qui reste nécessite mes yeux ou mon matériel. Un travail restant disqualifie une tâche. Une vérification restante, non. Un changement ouvert, au vert, mais non fusionné, est toujours en cours.

Une seconde règle s'ajoute à celle-ci. Aucun agent ne peut proposer un moyen pour moi de vérifier moins cette file. Pas d'échantillonnage, pas de paliers, pas de catégorie de travail qui se déploie sur la seule base des tests. Les agents proposent cela, tout comme le font de bons ingénieurs managers, parce que la file est longue. Quand la file est longue, c'est que le travail a été découpé trop grossièrement.

### Ce que cela coûte

Je suis le goulot d'étranglement, et c'est délibéré. Écrire du code a cessé d'être l'étape rare ; la fusion a pris sa place. Le processus protège mon attention : une branche à la fois, moins de 1 500 lignes écrites à la main, et un changement ouvert aujourd'hui est fusionné aujourd'hui, ou alors il était trop gros.

Le débit est fixé par ce que je peux lire avec attention en une journée. Pour un logiciel auquel les gens vont confier leurs données privées, je pense que c'est la bonne limite.

### L'organigramme, avec les permissions

En juillet, j'écrivais que l'organigramme est le produit : la coordination est désormais quelque chose que l'on construit. En en construisant un, j'ai appris quelle partie compte le plus. Un organigramme pour des agents est avant tout une liste de contrôle d'accès. Les équipes humaines laissent les droits de décision flous et comblent les vides par le jugement et les conversations de couloir. Les agents comblent chaque vide par une action pleine d'assurance.

Si vous ajoutez des agents à une équipe, écrivez la liste des décisions qui restent du ressort d'une personne avant d'écrire la moindre instruction de style. Puis faites en sorte que le système impose cette liste.

C'est l'essentiel de ce sur quoi je travaille avec des fondateurs et des CTO dans le cadre de Mentorship & Advisory.

## Pourquoi ça compte
Ce témoignage concret éclaire un enjeu central de la gouvernance des workflows agentiques : les consignes textuelles données aux agents ne suffisent pas à garantir un comportement fiable, il faut des contrôles d'accès techniques pour les décisions à fort enjeu comme la fusion ou la mise en production. Pertinent pour toute veille sur les pratiques d'ingénierie logicielle assistée par agents IA et sur la conception d'organisations homme-agent.
