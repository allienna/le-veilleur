---
title: "Introducing n8n Assistant"
date: 2026-09-12
url: "https://elinkb7e.mail.aiwithremy.com/ss/c/u001.adqTTuWyYZbGGgTYNnclIbQ6avlxysmPsHbcWa_zh0Gf_WCn0p8ckE4OmKlFTX3s_D9ADYQOp_xTBWNCk7cbzkjN13ZfDiiqxtryK-nT618gxF7DujkCIQvK_Fg8N8QhoK1HkacywDQbVqoE6Okk74LzLl-kdpnKumAQOcxYf8kwF9GiHvVCVTYpZDYjNdtOALiXDV2Z1KdD-mRTak2eMXGTzv2ANX8ovizJKf0vQ0drwSom3KGe4hzAkcoWiPJ3GzPEnY6geG732cPLEVu0cw/4ty/Ec8DQ3QNSNKGyluF4vXnuQ/h10/h001.wsSftMO3jopYg7NdhjNDKGDL7QoZ-y7CYrbzid4Ajxo"
keywords: ["n8n", "automatisation", "assistant IA", "workflow", "no-code", "agent"]
theme: "IA"
tone: "news"
used_in: ["2026-09-12"]
---

## Résumé
n8n lance « n8n Assistant », un agent IA capable de construire, exécuter, déboguer et itérer sur des workflows d'automatisation directement sur le canvas n8n à partir d'une simple description en langage naturel. Contrairement aux outils qui génèrent du code ou exécutent une tâche ponctuelle sans rien laisser derrière eux, le résultat est un workflow n8n standard : visible, éditable, journalisé et appartenant à l'équipe plutôt qu'à la personne ayant rédigé le prompt. L'outil est disponible en preview, activé par défaut sur n8n Cloud (hors instances Enterprise Cloud), et consomme le crédit IA déjà alloué au plan de l'utilisateur. Il remplace l'ancien « AI Workflow Builder », avec une différence clé : il ne se contente pas de générer, il exécute, observe les résultats et corrige.

## Points clés
- Décrit en langage naturel, l'assistant planifie le workflow, le construit sur le canvas, demande les identifiants nécessaires, l'exécute et corrige les erreurs en itérant avec l'utilisateur.
- Il pose des questions de clarification avant de construire si la demande est ambiguë, plutôt que de deviner et de produire un résultat erroné.
- Toute action sensible (accès aux identifiants, activation du workflow) requiert une confirmation explicite de l'utilisateur.
- Le workflow produit est un workflow n8n natif et standard : pas de code séparé à héberger, sécuriser ou maintenir ailleurs.
- Disponible par défaut sur n8n Cloud (hors Enterprise Cloud) et en auto-hébergement Docker (n8n ≥ 2.36 avec clés propres) ; non supporté en self-hosted npm ; l'offre Enterprise arrive prochainement.
- Remplace l'« AI Workflow Builder » précédent, qui générait un workflow une seule fois sans l'exécuter ni le corriger.

## Analyse approfondie
Si vous avez déjà construit quoi que ce soit dans n8n, vous connaissez ce fossé : vous pouvez décrire en une phrase ce que vous voulez automatiser, mais ce n'est pas la même chose que de savoir quels nœuds utiliser, dans quel ordre, comment les configurer, et à quels comptes les connecter. Et quand la première exécution échoue avec une erreur que vous n'avez jamais vue, vous voilà de retour dans la documentation et sur le forum.

Cette étape de traduction est l'endroit où la plupart des projets d'automatisation s'enlisent. Non pas parce que la plateforme ne peut pas le faire, mais parce que comprendre comment faire prend un après-midi que vous n'aviez pas prévu d'y consacrer.

Avec n8n Assistant, vous décrivez l'automatisation que vous voulez en langage naturel, et il planifie le workflow, le construit sur votre canvas, demande les identifiants dont il a besoin, l'exécute, détermine ce qui a cassé, et itère sur la correction avec vous.

Ce que vous obtenez au final est un workflow n8n standard : visible sur le canvas, modifiable à la main, journalisé à chaque exécution, et appartenant à votre équipe plutôt qu'à celui qui a écrit le prompt.

Vous obtiendrez quelque chose de fonctionnel en quelques minutes, puis vous l'affinerez : remplacer un nœud, ajuster un filtre, ajouter une gestion d'erreurs, décider ce qui nécessite une étape de confirmation. Si vous préférez l'assembler vous-même, rien ne vous en empêche. C'est le même canvas, et les workflows sont les mêmes workflows.

Les outils IA capables de produire une automatisation à partir d'une phrase ne manquent pas, et plusieurs d'entre eux s'en sortent plutôt bien. Mais les problèmes apparaissent plus tard, quand une équipe doit dépendre du résultat :

- **Rien à inspecter.** Demandez à un agent de codage une intégration et vous obtenez du code, que quelqu'un doit désormais héberger, sécuriser, surveiller et maintenir. C'est très bien si vous êtes développeur et que vous automatisez votre propre travail. C'est plus difficile à justifier quand le résultat n'a de sens que pour la personne qui l'a demandé par prompt.
- **Rien qui persiste.** Demandez à un assistant en tâche ouverte d'aller accomplir la tâche, et il se peut bien qu'il le fasse. Mais l'exécution se termine, et le travail disparaît avec elle. Il ne reste rien à transmettre ou à relancer la semaine suivante.
- **Rien pour expliquer.** Quand une automatisation fait quelque chose de surprenant, quelqu'un doit l'expliquer à une personne qui ne l'a pas construite. « Le modèle a décidé de » ne suffit pas.

La question n'est donc pas de savoir si vous pouvez générer une automatisation. C'est de savoir si elle fonctionnera encore le mois prochain, si vous pouvez voir ce qu'elle a fait, et si un collègue peut la reprendre.

### Ce que fait n8n Assistant

Vous commencez par décrire le résultat que vous voulez plutôt que les étapes pour y parvenir :

- **Il demande avant de supposer.** Si votre requête est ambiguë, il pose une question de clarification plutôt que de construire la mauvaise chose. « Envoyer les nouvelles réponses au formulaire à mon équipe » entraîne une question sur quel formulaire et quel canal.
- **Il construit sur votre canvas.** Les nœuds apparaissent dans votre workflow, connectés entre eux, prêts à être ouverts. Il n'y a ni script ni fichier de configuration à héberger ailleurs.
- **Il demande les identifiants quand il en a besoin.** Pas de liste de vérification préalable avant d'avoir vu quoi que ce soit fonctionner. Quand il atteint un nœud nécessitant un compte connecté, il le demande à ce moment-là et vous guide dans le processus.
- **Il exécute le workflow.** n8n Assistant exécute ce qu'il a construit, observe ce qui se passe, et lit les mêmes données d'exécution que vous consulteriez vous-même.
- **Il débogue.** Si un nœud échoue, il détermine pourquoi, propose une correction, puis l'applique et relance l'exécution. Pas de copier-coller entre outils ni de téléchargement de fichiers JSON à examiner manuellement.
- **Il demande avant toute action conséquente.** L'accès aux identifiants et l'activation du workflow nécessitent votre confirmation explicite.

### Vos workflows restent les vôtres

Rien de tout cela ne se produit dans une surface produit séparée. Le workflow que n8n Assistant construit est le workflow que vous auriez construit à la main, dans le même projet, avec les mêmes nœuds et le même historique d'exécution.

Voici un exemple typique. Quelqu'un veut trier les soumissions entrantes de formulaire : enrichir les données de l'entreprise, vérifier si elle est déjà cliente, puis soit la router vers les ventes, soit envoyer une réponse type. Cette personne connaît tout cela sous forme de phrase, mais rien sous forme de graphe de nœuds. n8n Assistant le planifie, le construit, demande l'identifiant CRM quand il atteint le nœud qui en a besoin, l'exécute sur une soumission de test, et découvre que l'étape d'enrichissement renvoie un tableau vide pour les entrepreneurs individuels. Il corrige cela, relance l'exécution, et livre un workflow de huit nœuds avec une exécution propre.

Une semaine plus tard, les règles de routage changent. Quelqu'un qui n'était pas impliqué ouvre le workflow, le lit, et modifie un nœud. Il n'a pas besoin de savoir ce que quelqu'un a tapé pour que ce workflow soit construit.

### Exécuter, examiner, améliorer

Générer le workflow n'est que la première étape. Voici ce que vous obtenez ensuite :

- **Il s'exécute.** n8n Assistant exécute le workflow et lit le résultat au lieu de simplement déclarer un succès.
- **Les échecs sont visibles.** Les journaux d'exécution montrent les entrées, sorties et erreurs par nœud, la même vue que vous utiliseriez pour déboguer à la main.
- **Les corrections sont appliquées et relancées.** La boucle continue jusqu'à ce que le workflow se termine, ou jusqu'à ce que le blocage soit quelque chose que seul vous pouvez résoudre, comme un compte qui n'existe pas encore.
- **Les points de confirmation restent de votre ressort.** L'accès aux identifiants et l'activation attendent votre approbation.
- **Examinez avant de vous y fier.** Lisez le workflow, vérifiez les identifiants, regardez les journaux, puis activez. Surtout pour tout ce qui est critique pour l'activité.

### Ce que coûte une construction

n8n Assistant puise dans l'allocation de crédits IA de votre plan. Les utilisateurs existants conservent l'allocation qu'ils avaient déjà, et l'usage est comptabilisé séparément de l'ancien générateur de workflow IA, de sorte que rien de ce que vous dépensez ici ne change ce que vous aviez avant.

Une construction qui nécessite plusieurs cycles de débogage coûte plus cher qu'une construction qui réussit du premier coup. Les crédits sont alloués par plan, et nous ajouterons dans les semaines à venir des moyens de les recharger.

### Disponibilité

- **n8n Cloud :** activé par défaut pour les nouvelles instances. Les instances Enterprise Cloud sont pour l'instant exclues de ce paramètre par défaut.
- **Auto-hébergé (Docker) :** vous fournissez vos propres clés, configurez des variables d'environnement supplémentaires, et faites tourner une version de n8n à partir de la 2.36. Voir https://docs.n8n.io/deploy/host-n8n/install-options/one-line-setup pour plus de détails.
- **Auto-hébergé (npm) :** non supporté.
- **Enterprise :** sur notre feuille de route, à venir prochainement.

Notez que n8n Assistant est encore livré derrière un flag de preview. Cela ne limite pas qui peut l'utiliser : c'est en développement actif, avec davantage de fonctionnalités à venir.

Certaines choses ne sont pas encore là, mais nous y travaillons pour l'avenir :

- Le premier workflow n'est pas garanti prêt pour la production. Il vous amène à quelque chose qui fonctionne. L'examiner reste votre travail.
- La configuration des identifiants et des tiers n'a pas disparu. n8n Assistant demande au bon moment et vous guide, mais il ne peut pas créer un compte sur un service que vous n'avez pas.
- Il n'est pas proactif. Il ne surveille pas votre instance, n'apprend pas vos préférences au fil du temps, et ne suggère pas d'automatisations que vous n'avez pas demandées.
- Il fonctionne sur une seule instance. Il n'y a aucune capacité multi-instance dans ce lancement.
- Il ne pilote pas votre ordinateur ou votre navigateur. La configuration des identifiants assistée par navigateur est quelque chose que nous explorons, et cela ne fait pas partie de cette version.

Par ailleurs, n8n Assistant remplace l'**AI Workflow Builder**. Là où l'ancien générateur produisait un workflow une fois puis s'arrêtait, n8n Assistant le construit, l'exécute, et trouve des améliorations.

### Pour commencer

Ouvrez n8n Assistant sur votre instance et décrivez une automatisation que vous remettez à plus tard depuis un moment. Quelque chose de réel, avec deux ou trois intégrations et au moins une étape qui pourrait plausiblement mal tourner.

Voici quelques idées pour commencer :

- Router les soumissions entrantes de formulaire vers le bon destinataire
- Synchroniser une feuille de calcul avec un CRM selon un planning
- Publier un résumé quotidien des exécutions échouées de la veille sur un canal
- Transformer un rapport manuel récurrent en workflow
- Réparer un workflow existant qui échoue silencieusement

Consultez la documentation de n8n Assistant ici : https://docs.n8n.io/build/ways-of-building-workflows/n8n-assistant

Tant que n8n Assistant est derrière le flag de preview, le retour le plus utile est celui qui est précis : ce que vous avez demandé, ce qu'il a construit, et où cela a échoué. Nous suivons attentivement le forum de la communauté.

Nous avons hâte de voir ce que vous allez construire avec.

## Pourquoi ça compte
Ce lancement illustre une tendance de fond dans l'outillage no-code/low-code : le passage d'assistants IA qui génèrent du code ou des artefacts jetables à des agents qui construisent, exécutent et corrigent des objets natifs de la plateforme, pérennes et transmissibles à une équipe — un enjeu clé pour l'adoption de l'IA agentique en entreprise.
