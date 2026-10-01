---
title: "Getting the most out of Opus 5.5 in Claude and Claude Code / claude.dev Blog"
date: 2026-10-01
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fclaude.dev%2Fblog%2Fgetting-the-most-out-of-opus-5-5%2F%3Futm_source=tldrdev/1/010001a0f208073c-63569086-f574-47c6-82a4-201c8b273824-000000/2Z1tbo_d0RnfT3aS-W4-aZI22nq4ChIboQa_Z3HVZNY=452"
keywords: ["Opus 5.5", "Claude Code", "prompting", "agents autonomes", "sécurité IA", "subagents"]
theme: "IA"
tone: "tutorial"
used_in: ["2026-10-01"]
---

## Résumé
Ce billet de blog d'Anthropic explique comment tirer le meilleur parti d'Opus 5.5 dans les applications Claude et Claude Code. Le modèle se distingue par sa capacité à travailler plus longtemps en autonomie, à rendre compte clairement de ce qu'il a fait, et à toujours réfléchir avant de répondre. L'article propose des conseils concrets de prompting (donner la tâche complète, nommer une « ligne d'arrivée », utiliser des subagents, tenir une liste de tâches dans un fichier) ainsi que des explications sur les nouveaux garde-fous de sécurité bio/cyber introduits avec ce modèle.

## Points clés
- Donner la tâche entière en un seul message avec un critère de fin clair (« les tests passent ») permet à Opus 5.5 de travailler en autonomie pendant de longues périodes, parfois plusieurs heures.
- Il n'est plus nécessaire de demander à Opus 5.5 de « réfléchir étape par étape » : le modèle réfléchit toujours avant de répondre et calibre lui-même l'effort nécessaire.
- Pour les audits ou migrations sur une grande base de code, on peut demander au modèle de répartir le travail entre plusieurs subagents et de vérifier chaque résultat rapporté.
- Sur les tâches longues, consigner une checklist dans un fichier (ex. TASKS.md) permet de suivre l'avancement même après un résumé de contexte.
- Opus 5.5 lit mieux les graphiques, diagrammes et captures d'écran, et produit des fichiers (tableurs, documents) directement utilisables.
- Le modèle inaugure des garde-fous de sécurité biologique/cyber de niveau Fable : certains messages sont basculés automatiquement vers un modèle plus ancien, sans bloquer la conversation.

## Analyse approfondie
Comment bien prompter Opus 5.5, piloter une exécution longue, et vérifier vos résultats dans les applications Claude et Claude Code.

Opus 5.5 fonctionne bien avec la façon dont vous utilisez déjà Claude. Certaines choses se comportent toutefois différemment : il travaille plus longtemps de façon autonome, il indique clairement ce qu'il a fait, et il réfléchit avant chaque réponse. Ce guide explique comment travailler avec Opus 5.5 dans les applications Claude et dans Claude Code, notamment comment prompter le modèle, piloter une exécution longue, et vérifier vos résultats.

**Trois choses à essayer lors de votre première session avec Opus 5.5**

**Quoi faire.** Donnez la tâche entière en un seul message. Nommez la ligne d'arrivée, par exemple « les tests passent » ou « chaque endpoint est migré ». Puis laissez-le travailler.

**Pourquoi c'est important avec Opus 5.5.** Opus 5.5 persévère mieux sur des travaux longs et à plusieurs étapes que ne le faisait Opus 5. Comparé aux modèles Opus précédents, ses plus gros progrès concernent le travail multi-étapes, comme faire aboutir une modification à travers un grand dépôt de code jusqu'à ce que les tests passent. Les premiers testeurs l'ont fait tourner sur des tâches de code longues, pendant des heures, avec peu de supervision. Avec une ligne d'arrivée claire, il sait quand il a terminé.

**Comment.** Dans Claude Code, par exemple :

Migrez les endpoints de paiement de l'ancien client vers le nouveau.
C'est terminé quand : chaque endpoint utilise le nouveau client, l'ancien client est supprimé, et la suite de tests passe.
Arrêtez-vous et demandez-moi uniquement si un test échoue pour une raison que vous ne pouvez pas expliquer.

**Quoi faire.** Retirez les formulations « réfléchis bien », « réfléchis étape par étape » et autres lignes similaires de vos prompts et de vos instructions enregistrées.

**Pourquoi c'est important avec Opus 5.5.** Opus 5.5 réfléchit toujours avant de répondre, et il décide lui-même de la quantité de réflexion nécessaire. Vous n'avez pas besoin de lui demander de réfléchir. Dans nos tests sur un produit de chat, retirer une ligne « réfléchis bien » a permis d'obtenir des réponses plus rapides, sans baisse de qualité perceptible.

**Comment.** Supprimez la ligne. Pour une réponse rapide à une question simple, dites-le explicitement : « Réponds directement. » Pour modifier la quantité de réflexion dans Claude Code, changez le niveau d'effort (« effort »).

**Quoi faire.** Si quelque chose vous revient en tête en cours d'exécution, vous pouvez taper un message de suivi pendant qu'il travaille.

**Pourquoi c'est important avec Opus 5.5.** Les exécutions sont désormais plus longues, donc un redémarrage coûte plus cher.

**Comment faire.** Dans Claude Code, tapez le message et appuyez sur Entrée pendant que Claude travaille, par exemple : « Garde aussi les anciens noms d'endpoints comme alias. »

**Quoi faire.** Lorsque vous demandez une page, une application ou un artefact, listez les habitudes de design que vous voulez exclure.

**Pourquoi c'est important avec Opus 5.5.** Sans direction de design, Opus 5.5 retombe sur quelques styles par défaut. Une instruction générale comme « évite un look générique » ne fait essentiellement qu'échanger un défaut contre un autre. Une liste de motifs précis fonctionne bien mieux.

**Comment.** Nommez les motifs :

Construisez un site web personnel avec du contenu provisoire.
N'utilisez pas de fond crème ou blanc cassé, de mots d'accent en italique dans les titres, de libellés de section numérotés « 01 / 02 / 03 », de libellés en police monospace, ou de boutons en forme de pilule.

Regardez ensuite ce qu'il a choisi à la place. Si cela ne vous plaît pas non plus, ajoutez-le à la liste et redemandez.

**Quoi faire.** Mettez une règle courte dans votre fichier CLAUDE.md précisant quand s'arrêter pour demander, et quand continuer.

**Pourquoi c'est important avec Opus 5.5.** Opus 5.5 vous tient informé pendant qu'il travaille. Sur une tâche longue, il s'arrête parfois pour faire un rapport plutôt que de continuer : un résumé qui nomme la prochaine étape sans l'exécuter, une proposition de continuer, ou une liste de choix qui ne bloquent pas réellement le travail. Il suit les instructions qui nomment ces points d'arrêt. Nommez vous aussi les arrêts que vous souhaitez.

**Comment.** Ajoutez ceci à CLAUDE.md, et adaptez-le à votre projet :

Quand une étape ne nécessite pas mon avis, continue. Mets les notes de statut dans le même message que ta prochaine action.
Arrête-toi et demande uniquement quand tu ne peux pas continuer sans moi, ou avant toute action destructrice : supprimer des données, faire un push forcé, ou modifier quelque chose hors de ce dépôt.

Si une exécution s'arrête avec « Voulez-vous que je continue ? », répondez « continue ». Si cela arrive souvent, la règle ci-dessus vous aidera.

Une règle de type « continue » signifie moins d'arrêts, donc gardez votre propre garde-fou avant toute action risquée ou difficile à annuler. La dernière ligne de la règle ci-dessus s'en charge. Gardez les invites de permission actives pour les commandes destructrices également.

Pour le pair programming, vous voudrez peut-être l'inverse : un plan en une ligne avant de commencer et un bref récapitulatif à la fin. Dites-le dans votre CLAUDE.md à la place. Opus 5.5 suit l'une ou l'autre approche.

**Quoi faire.** Pour un audit, une migration, ou une revue sur une grande base de code, demandez à Opus 5.5 de répartir le travail entre des subagents et de vérifier chaque résultat.

**Pourquoi c'est important avec Opus 5.5.** Les premiers testeurs ont fait coordonner par Opus 5.5 des subagents en parallèle sur des audits et migrations longs, avec peu de supervision.

**Comment.**

Auditez chaque service dans services/ pour le bug de retry mentionné dans le ticket lié.
Confiez chaque service à son propre subagent. Quand un subagent rapporte un résultat, vérifiez ses preuves avant de les accepter.
Terminez avec un seul tableau : service, affecté oui ou non, et la preuve.

**Quoi faire.** Pour une exécution qui va prendre du temps, demandez à Opus 5.5 de tenir sa liste de tâches dans un fichier et de la mettre à jour au fil de l'avancement. Lisez ensuite le fichier, pas le défilement de la conversation, pour voir où en est l'exécution.

**Pourquoi c'est important avec Opus 5.5.** Les exécutions sont plus longues désormais. Une exécution longue remplit la fenêtre de contexte, et Claude Code résume alors les tours de conversation les plus anciens. Une liste dans un fichier survit à cela, et elle montre d'un coup d'œil ce qui est fait et ce qu'il reste à faire.

**Comment.** « Tiens une checklist dans TASKS.md. Coche chaque élément une fois terminé, et ajoute tout nouvel élément que tu trouves. »

**Quoi faire.** Quand une exécution longue se termine, cherchez d'abord ce que Claude attend de vous, comme une décision qu'il a laissée ouverte ou une modification qu'il souhaite que vous approuviez. Lisez ensuite le reste du résumé de Claude.

**Pourquoi c'est important avec Opus 5.5.** Opus 5.5 rend compte de son travail plus clairement qu'Opus 5. Ses mises à jour et son résumé final indiquent ce qu'il a fait, ce qu'il a trouvé, et ce dont il a besoin de vous, en langage clair.

**Comment.** Pour modifier le format du résumé, indiquez-le dans CLAUDE.md, par exemple : « Termine chaque exécution avec trois titres : Bloqué en attente de moi, Modifié, Trouvé. »

**Quoi faire.** Demandez à Opus 5.5 de relire un diff ou une pull request avant qu'une personne ne le fasse.

**Pourquoi c'est important avec Opus 5.5.** Un testeur précoce a rapporté qu'Opus 5.5 au niveau d'effort le plus bas détectait plus de bugs qu'Opus 5 au niveau d'effort élevé, avec moins de fausses alertes. Il explique aussi ses modifications en langage clair, ce qui rend ses descriptions de pull requests plus faciles à relire.

**Comment.** Donnez ce prompt à Claude :

Relis le diff de cette branche par rapport à main.
Liste uniquement les problèmes pour lesquels tu bloquerais la fusion. Pour chacun, indique le fichier et la ligne, pourquoi c'est faux, et comment démontrer que ça échoue.

**Quoi faire.** Pour de la recherche et de l'analyse, demandez-lui d'indiquer ce qu'il n'a pas pu trouver ou vérifier.

**Pourquoi c'est important avec Opus 5.5.** « Je n'ai pas pu trouver ceci » vaut la peine d'être lu, et le demander explicitement permet de le repérer facilement.

**Comment.** Ajoutez « Signale tout ce que tu n'as pas pu confirmer, et indique où tu as cherché » à la demande. Cela fonctionne à la fois dans un rapport de recherche Claude et dans Claude Code.

Vérifiez d'abord que le sélecteur de modèle affiche bien Opus 5.5.

**Quoi faire.** Joignez le graphique, le diagramme, la capture d'écran ou la diapositive. Ne retapez pas les chiffres.

**Pourquoi c'est important avec Opus 5.5.** Opus 5.5 lit les graphiques, diagrammes et captures d'écran plus précisément qu'Opus 5, et n'a besoin d'aucune étape supplémentaire pour le faire. Il est aussi meilleur sur le sens qui dépend de la position des éléments dans l'image : quelles cases une flèche relie, ce qui a changé entre deux versions d'un diagramme, ou quand une réunion commence et se termine sur une capture de calendrier.

**Comment.** Joignez l'image et posez une question précise : « Lesquels de ces services appellent directement l'API de facturation ? »

**Quoi faire.** Donnez-lui un plan long, un rapport, ou un deck, et demandez-lui de trouver les erreurs.

**Pourquoi c'est important avec Opus 5.5.** Opus 5.5 porte plus d'attention aux détails que les modèles Opus précédents. Dans nos tests, il a repéré une date tombant sur le mauvais jour de la semaine dans un long fil de planification, et un graphique qui ne correspondait pas aux chiffres d'un deck.

**Comment.** Soumettez le prompt : « Vérifie ce deck pour tout ce qui se contredit : chiffres, dates et noms. Cite chaque problème et indique où il se trouve. »

**Quoi faire.** Quand vous voulez un tableur ou un document, demandez le fichier, pas un plan.

**Pourquoi c'est important avec Opus 5.5.** Les tableurs et documents que produit Opus 5.5 nécessitent moins de retouches que ceux d'Opus 5 avant de pouvoir être partagés.

**Comment.** « Fais-en un tableur que je peux partager : une ligne par fournisseur, avec des colonnes pour le coût, la date de fin de contrat et le responsable. »

**Quoi faire.** Si les questions de suivi dans une longue conversation semblent lentes, ajoutez une instruction indiquant que les réponses précédentes sont considérées comme actées.

**Pourquoi c'est important avec Opus 5.5.** Dans une longue conversation, Opus 5.5 revient parfois sur une réponse précédente en réfléchissant à un court suivi. Cela ralentit la réponse.

**Comment.** Ajoutez ceci aux instructions du projet :

« Une fois que tu as répondu à quelque chose, considère cette réponse comme actée. Concentre-toi sur ce que je demande maintenant, et ne reviens pas sur une réponse précédente sauf si je t'interroge à ce sujet ou que je signale un problème avec elle. »
Laissez cette instruction de côté pour les projets d'analyse longue, où une étape ultérieure peut révéler une erreur dans une étape antérieure.

Opus 5.5 est le premier modèle Opus à être lancé avec des garde-fous de sécurité bio et cyber de niveau Fable. Dans les applications Claude et Claude Code, la plupart des messages signalés basculent vers un modèle plus ancien, et votre travail continue sur celui-ci. Trouver des vulnérabilités de sécurité dans du code source est autorisé, et les questions courantes de santé et d'éducation devraient continuer à fonctionner normalement. Ces garde-fous peuvent parfois signaler à tort du travail légitime, et nous les ajustons pour réduire les signalements incorrects. Si vous êtes basculé, voici ce que vous verrez et ce qu'il faut faire.

**Ce que vous voyez.** Une notification qui commence par « Basculé vers » suivi du nom d'un modèle plus ancien. Claude répond sur ce modèle, et la conversation y reste.

**Quoi faire.**

La vérification couvre tout le contenu de la conversation, y compris les fichiers et les résultats de recherche. Un signalement peut donc provenir d'un contenu antérieur, pas seulement de votre dernier message.

**Ce que vous voyez.** Une notification qui nomme le modèle plus ancien. La session continue sur ce modèle.

**Quoi faire.** Retirez de vos prompts et instructions les demandes visant à reproduire son raisonnement interne dans la réponse.

**Pourquoi c'est important avec Opus 5.5.** Une demande de reproduire son raisonnement interne dans la réponse peut être refusée. C'est l'une des catégories de signalement.

**Comment.** Demandez à Claude ce dont vous avez besoin autrement, par exemple : « Explique en trois phrases pourquoi tu as choisi cette approche. »

**Quoi faire.** Dans Claude Code, utilisez le mode rapide pour les échanges où vous lisez chaque réponse avant d'envoyer le message suivant.

**Pourquoi c'est important avec Opus 5.5.** Le mode rapide est disponible pour Opus 5.5 dès le lancement, en aperçu de recherche (research preview). Vous obtenez le même modèle, et le texte arrive plus vite. Il nécessite d'activer un usage supplémentaire, et il coûte plus cher par token que le mode standard.

**Comment.** Tapez /fast dans Claude.

Parcourez ceci avant votre prochaine tâche longue.

**Demander**

**Exécutions longues dans Claude Code**

**Vérifier**

**Signalements**

Commencez à construire avec Opus 5.5 !

*Avec nos remerciements à Molly Vorwerck pour sa relecture.*

## Pourquoi ça compte
Ce guide donne des indications concrètes et actionnables pour adapter ses pratiques de prompting et de supervision à un modèle plus autonome, ce qui est directement utile pour quiconque intègre Opus 5.5 dans des workflows de développement ou d'analyse ; il éclaire aussi les nouveaux garde-fous de sécurité, un point sensible pour le suivi de l'évolution des pratiques de safety chez les fournisseurs de LLM.
