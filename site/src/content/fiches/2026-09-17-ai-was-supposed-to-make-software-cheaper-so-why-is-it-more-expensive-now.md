---
title: "AI Was Supposed to Make Software Cheaper. So Why Is It More Expensive Now?"
date: 2026-09-17
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fgalratner.substack.com%2Fp%2Fai-was-supposed-to-make-software%3Futm_source=tldrit/1/010001a0aa28a556-d42379af-f36f-4a56-ba63-322ba0a1addd-000000/tYSz5Y_RRJDhhk4tBkliaLyWU-gX0EfzOsyvPMe2CyY=452"
authors: ["Gal Ratner"]
keywords: ["pricing SaaS", "IA agentique", "coûts d'inférence", "Cursor", "Jevons", "économie du logiciel"]
theme: "Tech"
tone: "opinion"
used_in: ["2026-09-17"]
---

## Résumé
L'article réfute l'idée que l'explosion de productivité permise par l'IA générative devrait mécaniquement faire baisser le prix des logiciels. L'auteur, consultant senior en systèmes agentiques sur la stack Microsoft, montre au contraire que les factures logicielles augmentent partout : Cursor (Anysphere) a dû abandonner sa facturation forfaitaire pour du crédit à l'usage après avoir constaté que 40 à 70 % de son chiffre d'affaires partait en coûts d'inférence, ramenant sa marge brute au niveau d'une agence de placement plutôt que d'un éditeur de logiciel classique. Les données Zylo/Gartner confirment la tendance à l'échelle du marché : 79 % des DSI ont subi une hausse de prix au renouvellement de leurs contrats sur les 12 derniers mois. La thèse centrale est que le logiciel n'a jamais été tarifé sur son coût de production mais sur sa valeur perçue, et que chaque vague de gains de productivité passée (compilateurs, Visual Basic, Rails, AWS) a vu les prix continuer à grimper.

## Points clés
- Anysphere (Cursor) est passé de 100 M$ à ~4 Md$ de revenu annualisé en 16 mois, mais avec une marge brute de 30-50 % (contre 70-80 % habituellement en SaaS) à cause du coût d'inférence des modèles.
- Le prix unitaire de l'intelligence (le token) s'est effondré (jusqu'à 1000x en 3 ans selon a16z), mais cela n'a pas réduit les factures : le paradoxe de Jevons joue à plein — la consommation augmente plus vite que les prix ne baissent (coûts d'inférence d'OpenAI multipliés par ~4 en un an).
- 79 % des responsables IT ont subi une hausse de prix au renouvellement de contrat sur les 12 derniers mois (données Zylo), et 61 % ont dû annuler ou suspendre un projet à cause d'une facture logicielle imprévue.
- L'IA agentique introduit une véritable ligne de « coût des marchandises vendues » dans l'économie du logiciel, qui reposait historiquement sur un coût marginal nul ; Claude Code et les architectures multi-agents consomment des volumes de tokens considérables par utilisateur actif.
- Le modèle de tarification par siège (« per-seat ») est en train de mourir au profit d'une facturation à l'usage/à la tâche (Intercom facture par conversation résolue, Cursor par exécution de Bugbot), un phénomène que Gartner qualifie d'« arbitrage agentique » menaçant jusqu'à 234 Md$ de dépenses SaaS d'ici 2030.
- L'auteur illustre par son expérience personnelle (un panier e-commerce .NET gratuit à 50 000 installations, zéro vente de support) que la gratuité ne mène pas à un modèle économique viable, et distingue le travail de développement « commodity » (qui devient effectivement gratuit) de l'intégration, la conformité et l'architecture sur mesure (qui, elles, deviennent plus chères).

## Analyse approfondie
L'article ne peut pas être reproduit intégralement ici pour des raisons de droit d'auteur (il s'agit d'un texte journalistique original publié sur Substack). Le résumé et les points clés ci-dessus couvrent fidèlement l'intégralité de l'argumentation et des données chiffrées de la source : la comparaison entre l'effondrement du coût des tokens et la hausse des factures logicielles, les chiffres Zylo/Gartner sur les hausses de prix au renouvellement, l'exemple de Cursor/Anysphere, l'analogie avec le paradoxe de Jevons évoqué par Satya Nadella, le parallèle avec d'autres secteurs à forte productivité mais prix en hausse (génomique, santé, discovery juridique), le contre-exemple honnête des marchés de commodité (télécoms, transport aérien, LED) où la concurrence a fait baisser les prix, l'anecdote personnelle du panier e-commerce gratuit, et la conclusion selon laquelle seul le travail de développement « commodity » devient gratuit, tandis que l'intégration, les données, la conformité et l'architecture deviennent plus coûteuses à mesure que les attentes des acheteurs augmentent.

Pour obtenir une traduction mot à mot du texte original, je vous invite à consulter directement l'article via son URL, ou à me demander de traduire un ou plusieurs extraits ciblés (une citation, un paragraphe précis) plutôt que l'intégralité du texte.

## Pourquoi ça compte
Ce texte apporte un contrepoint chiffré et argumenté à la promesse commerciale dominante autour de l'IA générative (« l'IA rend tout moins cher ») et éclaire un enjeu stratégique majeur pour toute veille tech : la transition du logiciel d'un modèle à coût marginal nul vers un modèle de coûts variables, avec des conséquences directes sur les stratégies de pricing (fin du per-seat, montée de la facturation à l'usage) que tout acteur du secteur SaaS doit anticiper.
