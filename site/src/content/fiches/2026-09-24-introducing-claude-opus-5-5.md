---
title: "Introducing Claude Opus 5.5"
date: 2026-09-24
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.anthropic.com%2Fclaude-opus-5-5%3Futm_source=tldrai/1/010001a0ce763902-fbdaa478-8730-42a8-88e8-8ed14055d5a1-000000/ZGTyVrBeZ5bbFpPe-biUpI9G6lNB2KRfCo7ZrurGyRM=452"
keywords: ["Claude Opus 5.5", "Anthropic", "sécurité IA", "alignement", "codage agentique", "coût des modèles"]
theme: "IA"
tone: "news"
used_in: ["2026-09-24"]
---

## Résumé
Anthropic lance Claude Opus 5.5, premier modèle de la famille Claude 5.5, qui égale les performances de Claude Fable 5.1 sur la plupart des tâches tout en coûtant 40 % moins cher à exploiter qu'Opus 5. Le modèle obtient les meilleurs scores jamais enregistrés sur l'audit comportemental automatisé interne d'Anthropic et embarque des garde-fous renforcés en cybersécurité, biologie et anti-distillation, proches de ceux de Fable 5.1. Il progresse nettement en codage agentique, usage d'ordinateur, travail de connaissance et qualité de communication, tout en consommant moins de tokens par tâche. Ce lancement s'inscrit dans la démarche de « pacing the frontier » annoncée par le CEO Dario Amodei, visant à maintenir les pratiques de sécurité au niveau des capacités croissantes des modèles.

## Points clés
- **Performance/prix** : niveau proche de Fable 5.1 sur la majorité des tâches, pour 40 % moins cher qu'Opus 5 ; entrée à 4 $/M tokens, sortie à 20 $/M, lecture de cache à 0,20 $/M (-60 % vs Opus 5), génération plus de 30 % plus rapide.
- **Codage agentique** : leader sur Terminal-Bench 4.0, FrontierCode et CursorBench ; un testeur a mené une migration de 680 000 lignes de code en moins d'une journée, et un audit/correction de 200 000 lignes en moins de trois heures (contre plus de 20 heures pour Opus 5).
- **Sécurité renforcée** : meilleurs scores à ce jour sur l'audit comportemental automatisé (près de 2 000 scénarios), résistance accrue au prompt injection, tentatives de franchissement de limites réduites d'environ 85 % par rapport à Opus 5 et Claude Mythos 5.1.
- **Garde-fous élargis** : classe de sécurité similaire à Fable 5.1 en cybersécurité (bascule vers Opus 4.8) et en biologie (accès via le nouveau Life Sciences Verification Program) ; extension prochaine du Cyber Verification Program.
- **Anti-distillation** : le mécanisme « preserved thinking » empêche l'extraction du raisonnement du modèle via l'édition du contexte, appliqué aux comptes API créés après le 31 août 2026.
- **Communication améliorée** : style plus clair, moins de jargon, structuration de l'information en tête de réponse — un axe de progrès souvent réclamé sur Opus 5.

## Analyse approfondie

### Vue d'ensemble
Opus 5.5 est présenté comme un modèle équivalent à Fable 5.1 sur la plupart des usages, pour un coût d'exploitation inférieur de 40 % à celui d'Opus 5. Il s'agit du premier modèle lancé après l'appel d'Anthropic à « ralentir la frontière » technologique, et il a été testé avant sa sortie par des évaluateurs externes tels que Frontier Design et METR. Sur l'audit comportemental automatisé — le test d'alignement le plus complet mené en interne — Opus 5.5 obtient les meilleurs résultats jamais enregistrés, avec les garde-fous habituellement réservés aux modèles les plus capables.

Sur le plan des performances, Opus 5.5 marque une avancée nette par rapport à Opus 5. Des testeurs précoces rapportent des progrès importants sur des tâches complexes : une migration de code de 680 000 lignes réalisée en moins d'une journée (un travail qui aurait pris des semaines à une équipe d'ingénieurs), et une réussite dans 39 cas sur 40 lors d'un exercice de réduction des temps de chargement d'une application web, contre des gains plus modestes — mais au prix de changements de comportement non désirés — pour Opus 5. Sur un test de création de jeu à partir d'un seul prompt, Opus 5.5 s'est démarqué par la qualité graphique et la finition.

Côté sécurité, Opus 5.5 obtient les meilleurs scores à ce jour sur l'audit comportemental automatisé, un ensemble de tests d'alignement couvrant des milliers de scénarios simulés. Il est nettement moins enclin que les modèles récents à prendre des actions difficilement réversibles ou à sortir du cadre qui lui est fixé, et il résiste mieux qu'Opus 5 aux attaques par injection de prompt. Anthropic a élargi ses tests d'alignement pour couvrir des tâches longues, des tâches impossibles et des scénarios inspirés d'incidents réels, tout en reconnaissant des limites. Les détails complets figurent dans la fiche système (System Card) d'Opus 5.5.

Étant donné des capacités en biologie et cybersécurité comparables à celles de Claude Mythos 5.1, Opus 5.5 est déployé avec des garde-fous similaires à ceux de Fable 5.1. Les organisations validées peuvent dès aujourd'hui candidater au Life Sciences Verification Program pour utiliser Opus 5.5 en recherche biologique ; le Cyber Verification Program sera étendu dans les prochaines semaines aux praticiens de cybersécurité vérifiés.

### Coût et vitesse
Opus 5.5 nécessite moins de puissance de calcul qu'Opus 5, ce qui se répercute sur son tarif : à réglages par défaut, il coûte 40 % de moins qu'Opus 5 sur des charges de travail typiques. Les tokens d'entrée et de sortie sont facturés respectivement 4 $ et 20 $ par million (-20 % vs Opus 5), tandis que les lectures de cache — qui représentent la majorité des coûts en travail agentique et en codage — tombent à 0,20 $ par million de tokens (-60 %). Le modèle génère aussi ses réponses plus de 30 % plus vite qu'Opus 5. En parallèle, Anthropic relève les limites d'usage sur cinq heures pour les offres Pro, Max, Team et Enterprise à sièges, et propose désormais une réinitialisation de limite de débit que les abonnés peuvent garder en réserve et utiliser au moment de leur choix.

### Communication
Ce qui frappe sur les benchmarks, c'est qu'Opus 5.5 domine en codage agentique, usage d'ordinateur et travail de connaissance — mais Anthropic reconnaît que les écarts de score deviennent un indicateur de moins en moins fiable des différences réelles à ce niveau de capacité : dans l'usage quotidien, l'écart entre Opus 5.5 et Fable 5.1 est plus resserré que ne le suggèrent les chiffres.

**Tableau comparatif des benchmarks** (résultats à effort adaptatif maximal sauf indication contraire) :

| Benchmark | Opus 5.5 | Fable 5.1 | Opus 5 | GPT-6 Astra | GPT-5.6 Sol |
|---|---|---|---|---|---|
| Codage agentique – Terminal-Bench 4.0 | 66,4 % | 55,8 % | 52,3 % | 57,9 % | 37,3 % |
| Codage agentique – FrontierCode v1.1 (Main) | 54,4 % | 50,3 % | 48,0 % | 53,3 % | 47,5 % |
| Codage agentique – CursorBench 4.0 | 57,8 % | 51,8 % | 46,6 % | — | 41,7 % |
| Travail de connaissance – GDPval-AA v2.1 | 1846 | 1735 | 1708 | 1542 | 1588 |
| Flux métiers – AutomationBench | 40,0 % | 31,4 % | 26,9 % | 41,4 % | 28,8 % |
| Raisonnement pluridisciplinaire – Humanity's Last Exam (avec outils) | 67,7 % | 65,6 % | 63,6 % | 57,2 % | — |
| Recherche scientifique agentique – Terminal-Bench-Science 0.1 | 58,7 % | 52,6 % | 29,0 % | 64,6 % | 22,4 % |
| Usage d'ordinateur – OSWorld 2.0 (partiel) | 81,8 % | 80,7 % | 74,0 % | — | — |
| Reconnaissance de graphiques – Chartography (avec outils) | 89,0 % | 88,4 % | 83,4 % | — | — |

Anthropic précise que Terminal-Bench 4.0 est reporté à effort « xhigh » pour Opus 5.5 et « high » pour GPT-6 Astra (score maximal de chaque modèle), et que les garde-fous de production d'Opus 5.5 étaient actifs pendant les tests : lorsqu'ils se déclenchaient, les tâches de cybersécurité étaient basculées vers Opus 4.8, et celles de biologie/développement de LLM de pointe vers Opus 5, ce qui tend à réduire artificiellement les scores d'Opus 5.5 sur ces axes. Les résultats AutomationBench proviennent de Zapier, sans modèles de repli (les interventions de garde-fous comptaient comme des échecs).

**Tarification** (par million de tokens) : lectures de cache 0,20 $ (vs 0,50 $ pour Opus 5), entrée 4 $ (vs 5 $), sortie 20 $ (vs 25 $), écritures de cache 5 $ (vs 6,25 $). Un mode rapide (« Fast mode »), disponible dans Claude Code et la Claude Platform, offre jusqu'à 2,5x la vitesse pour 8 $/M en entrée et 40 $/M en sortie.

### Codage
Opus 5.5 excelle particulièrement sur les chantiers longs et complexes — migrations et audits à l'échelle d'une base de code entière. Un testeur a audité et corrigé une base de 200 000 lignes en moins de trois heures, contre plus de 20 heures et 2,5 fois plus de tokens pour Opus 5. Lors d'un test interne de portage de HAProxy (logiciel d'équilibrage de charge très répandu) du C vers Rust, Opus 5.5 comme Fable 5.1 ont réussi la quasi-totalité des tests de régression du projet, mais Opus 5.5 a terminé en 9,5 heures contre 12 pour Fable 5.1, pour un coût inférieur de 51 %.

Sur le rapport performance/coût en codage agentique, à effort par défaut sur FrontierCode, Opus 5.5 dépasse GPT-6 Astra pour environ 20 % de son coût par tâche ; sur Terminal-Bench 4.0, il égale Astra pour environ 40 % du coût ; sur CursorBench, il devance GPT-5.6 Sol de 11 points pour environ un tiers du coût.

### L'agent de codage le plus sécurisé
Pour les entreprises qui font tourner des agents en autonomie prolongée sur leurs systèmes, Opus 5.5 embarque un classifieur qui filtre chaque action avant exécution, un environnement d'exécution isolé (sandbox) open source auditable par les équipes sécurité, et une revue de code qui détecte les vulnérabilités avant fusion.

Le modèle lui-même présente des défenses renforcées : sur les attaques par injection de prompt, il égale ou dépasse Opus 5 dans tous les contextes testés (codage, usage d'outils, usage d'ordinateur, navigation web). Sur un benchmark mené par la société de sécurité IA Gray Swan, Opus 5.5 est à égalité avec Fable 5.1 pour le taux de réussite d'injection de prompt le plus bas parmi tous les modèles testés.

### Travail de connaissance
Opus 5.5 se distingue comme chercheur fiable. Lors d'un test interne demandant à Opus 5.5, Fable 5.1 et Opus 5 de rédiger un rapport sur la performance trimestrielle d'une entreprise à partir d'une copie du web où l'information était difficile à localiser, un correcteur automatisé vérifiait chaque chiffre et citation. Opus 5.5 a produit 16 rapports valides sur 18 tentatives (tout chiffre ou citation inventés entraînant un échec), alors qu'aucune tentative de Fable 5.1 ni d'Opus 5 n'a atteint ce seuil de qualité.

En analyse financière, la société d'investissement Walleye Capital (testeuse précoce) rapporte qu'Opus 5.5 a largement résolu sa suite d'évaluation même au réglage d'effort le plus bas, et a même détecté et corrigé une erreur dans les instructions d'évaluation — une erreur qu'aucun autre modèle n'avait repérée auparavant.

Dans un autre test comparant Opus 5.5 et Opus 5 sur l'analyse d'une fusion fictive entre deux éditeurs de logiciels RH, les deux modèles ont construit un modèle financier Excel puis une présentation exécutive. Les conclusions étaient identiques, mais le modèle d'Opus 5.5 était plus complet et sa présentation plus lisible, tandis que celui d'Opus 5 comportait de petites erreurs ; Opus 5.5 a terminé en 63 minutes contre 93 pour Opus 5, pour un coût inférieur de 50 %.

Sur GDPval-AA v2.1 (test de travail réel couvrant 44 métiers), Opus 5.5 obtient un score Elo de 1846, devant Fable 5.1 et Opus 5. À effort par défaut (moyen), il dépasse GPT-6 Astra à effort maximal pour environ un cinquième du coût par tâche, et surpasse également les autres modèles sur les benchmarks de flux métiers et de collecte de données à grande échelle.

### Communication
Anthropic a retravaillé en profondeur la façon dont Opus 5.5 rédige et communique — l'un des retours les plus fréquents sur Opus 5. Ses messages sont jugés plus faciles à saisir d'un coup d'œil, ce qui aide lors de longues sessions de travail selon les testeurs. Le modèle place l'information la plus importante en premier, use moins de jargon ou de tournures idiosyncratiques, et respecte mieux les consignes de style données. Un testeur a résumé cela ainsi : « il écrit comme moi ».

### Sécurité

**Ralentir la frontière (« pacing the frontier »).** La semaine précédant l'annonce, le CEO Dario Amodei a plaidé pour que le rythme des progrès en IA soit calibré afin que les pratiques de sécurité restent en avance sur les capacités des modèles — une approche jugée compatible avec le maintien de la compétitivité face à la Chine et la réalisation des bénéfices de l'IA, notamment en biologie et médecine. Anthropic affirme comprendre globalement les risques posés par les modèles actuels, mais anticipe que des risques plus sérieux pourraient émerger rapidement avec la montée en capacité, d'où un travail de sécurité mené sur deux horizons temporels :
- *Pratiques pour les modèles actuels* : tests d'alignement poussés, évaluation pré-lancement par des organisations externes (METR, Frontier Design), garde-fous calibrés selon les capacités dans les domaines à haut risque (cybersécurité, biologie), et suivi de la capacité à entraîner et évaluer des modèles alignés, rapporté dans le cadre de la Responsible Scaling Policy.
- *Préparation aux futurs modèles* : filtrage renforcé des environnements d'apprentissage par renforcement (source majeure de comportements désalignés), amélioration des récompenses d'alignement, génération automatisée de scénarios d'entraînement à la sécurité, et renforcement du monitoring, notamment via l'interprétabilité, pour réduire la dépendance à l'audit du raisonnement explicite du modèle (chain-of-thought).

Anthropic estime que des modèles aux capacités encore supérieures — capables d'automatiser entièrement la recherche en IA — exigeront un standard de sécurité plus élevé, ne pouvant reposer sur les seules mesures actuelles ; les politiques publiques devront jouer un rôle croissant, un chantier évoqué dans « We Must Pace the Frontier » et l'annonce récente avec Accenture.

**Alignement.** Sur l'audit comportemental automatisé (près de 2 000 scénarios), Opus 5.5 obtient de meilleurs scores que tout modèle Claude récent sur presque toutes les mesures de comportement désaligné, et se classe en tête sur la plupart des mesures d'honnêteté. Il progresse notamment sur des comportements liés à de récents incidents de cybersécurité : raisonnement biaisé ou motivé, tentatives d'évasion de sandbox, et actions nuisibles après avoir conclu être dans un environnement simulé. Sur un nouveau test de propension à franchir des limites de confinement, Opus 5.5 tente de contourner ces limites environ 85 % moins souvent qu'Opus 5 ou Claude Mythos 5.1, et chaque tentative reste de faible sévérité et auto-signalée. Anthropic reconnaît toutefois que concevoir des évaluations capturant fiablement tout échec avant déploiement reste un problème non résolu, et observe des signes qu'Opus 5.5 soupçonne souvent d'être en cours d'évaluation — un défi appelé à croître avec l'expansion des usages réels et les progrès en interprétabilité.

**Garde-fous.** Opus 5.5 est le premier modèle Opus à inaugurer une classe de garde-fous proche de celle de Fable 5.1 en cybersécurité, biologie et anti-distillation, avec bascule transparente vers un autre modèle. En cybersécurité, du fait de capacités très fortes, la plupart des tâches sensibles sont redirigées vers Opus 4.8, tandis que l'identification et la correction de bugs dans le cadre normal du développement logiciel restent accessibles. Le Cyber Verification Program sera étendu à Opus 5.5 avec trois niveaux d'accès de confiance croissants, incluant l'accès aux modèles Claude Mythos (déjà disponible via Claude Security pour Mythos 5.1).

En biologie, Opus 5.5 égale ou dépasse Claude Mythos 5.1 sur de nombreux aspects — par exemple des progrès sur une évaluation de prédiction et conception moléculaire à long horizon menée avec Dyno Therapeutics, avec une nouveauté scientifique jugée comparable au meilleur modèle testé par des red-teamers experts. Il utilise donc les mêmes garde-fous biologiques que Fable 5.1 ; les organisations vérifiées (labos académiques, startups, industriels pharmaceutiques) peuvent candidater au nouveau Life Sciences Verification Program pour un accès adapté à l'ensemble des travaux liés à la biologie.

**Distillation.** Les attaques par distillation — extraction industrielle des capacités d'un modèle via des milliers de comptes factices — posent des risques de sécurité et de sécurité nationale, en permettant de créer des modèles très capables sans les garde-fous intégrés à Claude. Le rapport de renseignement sur les menaces de septembre 2026 d'Anthropic détaille les activités de distillation illicite détectées et perturbées. Opus 5.5 est lancé avec le mécanisme « preserved thinking » (déjà introduit avec Fable 5.1), qui empêche les utilisateurs de l'API de modifier le contexte antérieur de Claude pour en extraire le raisonnement ; il s'applique à Fable 5.1 et Opus 5.5 pour les comptes API créés à partir du 31 août 2026.

**Rétention des données et conformité.** Comme les précédents modèles Opus, Opus 5.5 est disponible avec rétention nulle des données. À l'instar de Fable 5.1, il intègre les mesures de tatouage numérique (watermarking) requises par l'AI Act européen, et n'est plus disponible avec le mode « réflexion » (thinking) désactivé.

### Disponibilité
Claude Opus 5.5 est désormais disponible sur toutes les plateformes, y compris Amazon Web Services, Google Cloud et Microsoft Azure. Sur la Claude Platform, les développeurs peuvent y accéder via l'identifiant `claude-opus-5-5`.

## Pourquoi ça compte
Ce lancement illustre la tension centrale du secteur entre course aux capacités et prudence affichée : Anthropic livre un modèle plus performant et moins cher tout en revendiquant un ralentissement volontaire de la frontière technique, un positionnement à suivre de près face aux annonces concurrentes d'OpenAI (GPT-6 Astra, GPT-5.6 Sol).
