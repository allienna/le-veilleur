---
title: "What Decision Models Change for Data Engineers"
date: 2026-11-09
url: "https://open.substack.com/pub/thepipeandtheline/p/what-decision-models-change-for-data-engineers?utm_source=multiple-personal-recommendations-email&utm_medium=email&token=eyJ1c2VyX2lkIjo0NzU1OTI2MjgsInBvc3RfaWQiOjIyMjM3MjAzMSwiaWF0IjoxNzk0MTYzMTYxLCJleHAiOjE3OTY3NTUxNjEsImlzcyI6InB1Yi0xMTk2MjI5Iiwic3ViIjoicG9zdC1yZWFjdGlvbiJ9.hvQPK63z8cP2NZ-MAveMazt14MWVdJoSlemlEl26chQ"
authors: ["Alejandro Aboy"]
keywords: ["decision models", "OpenAI Decisions API", "data engineering", "LLM", "classification multimodale", "pipeline de données"]
theme: "IA"
tone: "tutorial"
used_in: ["2026-11-09"]
---

## Résumé
L'article présente les "Decision Models", une nouvelle catégorie d'outils dérivés des LLM mais conçus pour renvoyer des réponses typées (booléen, choix fermé, score) plutôt que du texte libre, à l'image des anciens classifieurs comme XGBoost. L'auteur illustre le concept avec un pipeline de démonstration utilisant l'API Decisions d'OpenAI pour détecter des incidents criminels dans des images de vidéosurveillance synthétiques, en posant trois questions typées par image. Un benchmark comparatif oppose cette API à un LLM classique (Responses API) sur 47 images : les Decision Models sont environ sept fois plus rapides, mais peuvent manquer des cas ambigus que le LLM généraliste détecte mieux. L'article conclut sur des recommandations concrètes indiquant quand privilégier ce type de modèle plutôt qu'un LLM classique dans une architecture de traitement de données.

## Points clés
- Les "Decision Models" (ex. OpenAI Decisions API) sont une évolution des classifieurs traditionnels adaptée à l'ère des LLM : ils renvoient des valeurs typées (vrai/faux, score, choix) avec une probabilité, sans génération de texte.
- Trois types de questions sont supportés : `predicate` (oui/non), `choice` (sélection dans une liste fermée) et `score` (niveau sur une échelle), combinables en un seul appel API multimodal (image + questions).
- Dans la démo (détection de scènes criminelles sur images CCTV synthétiques), les réponses coïncident généralement entre les trois types de questions, mais un cas de vol à l'étalage montre que la question oui/non peut rater un incident que la question de catégorie détecte correctement.
- Le benchmark sur 47 images montre que les Decision Models sont environ 7 fois plus rapides qu'un LLM classique interrogé avec les mêmes questions, avec zéro token de sortie généré (coût ~667 tokens d'entrée par image en détail "low").
- Les LLM génériques restent supérieurs sur les cas ambigus à haute confiance erronée, ce qui suggère de combiner les types de questions pour compenser ces angles morts plutôt que de se fier à un seuil unique.
- L'auteur recommande les Decision Models pour des verdicts rapides et bon marché sur des catégories fermées et bien définies, et déconseille leur usage quand une explication, une localisation spatiale dans l'image, ou une garantie de fiabilité par item sont nécessaires.

## Analyse approfondie
L'auteur, Alejandro Aboy (ingénieur passé du marketing digital au tracking web, puis à l'analytics, l'ingénierie de données et l'ingénierie IA), signe son retour sur sa newsletter *The Pipe & The Line* après une pause depuis juin. Il situe le contexte : l'arrivée de l'IA comme "consommatrice" de données bouleverse les usages classiques de l'ingénierie de données. Alors que les data engineers passaient traditionnellement leur temps sur des besoins ETL classiques (déplacer des données via API ou des outils comme Fivetran), les deux cas d'usage historiques — le BI pour l'analytique interne et les données non structurées pour l'entraînement de pipelines ML — se fondent désormais dans un flux hétérogène d'entrées multimodales qui remet en question les architectures établies. Les besoins de traitement de données doivent devenir plus flexibles et plus rapides que jamais.

**Que sont les Decision Models ?**
Les équipes data utilisent depuis des années des classifieurs comme XGBoost dans leurs pipelines : un petit modèle qui prend une ligne de données en entrée et renvoie une étiquette avec une probabilité. Les "Decision Models" reprennent cette même logique, mais adaptée à l'ère des LLM. Le concept a été introduit par TypeSafe sous le nom de "System One Decision Models" (avec Jev), et l'API Decisions d'OpenAI en est une implémentation équivalente, utilisée dans la suite de l'article. Le principe : on envoie une entrée et des questions ; on reçoit en retour des valeurs typées — vrai/faux, un score, ou un choix parmi des options disponibles. Le modèle ne peut pas rédiger de paragraphe explicatif. En contrepartie, la latence est extrêmement faible, ce qui le rend adapté à des flux de traitement de données exigeant de la rapidité et de la flexibilité.

**Le pipeline de démonstration : détecter des crimes sur des images de caméra**
Le pipeline simule un flux de caméra de vidéosurveillance : chaque image reçue est envoyée à l'API Decisions d'OpenAI avec trois questions, et les réponses déterminent si une alerte doit être déclenchée. Les images utilisées sont des illustrations synthétiques de style CCTV (sans personnes réelles), générées avec un modèle de génération d'image, et chaque exemple présenté correspond à une réponse réelle obtenue lors de l'exécution du pipeline.

L'API Decisions propose trois types de questions :
- `predicate` (oui/non)
- `choice` (un choix parmi une liste fermée d'options)
- `score` (un niveau sur une échelle)

Les images sont transmises en tant qu'`input_image` via une URL de données encodée en base64, avec un paramètre optionnel `detail` (`low`, `high`, `auto` ou `original`). L'auteur fournit un extrait de requête de test, qui définit trois questions : une question booléenne pour savoir si la scène montre un crime ou un incident violent en cours ; une question à choix fermé pour catégoriser la scène parmi "normal" (activité ordinaire), "theft" (vol), "fight" (violence physique) ou "vandalism" (dégradation de bien) ; et une question de score pour évaluer la gravité de la situation sur une échelle allant de "aucune" à "critique". La requête est envoyée au modèle via le point de terminaison `/v1/decisions`. En réponse, chaque question obtient une probabilité par option — par exemple, pour la question de catégorie, le modèle peut renvoyer "theft" avec une confiance de 0,89, accompagnée des probabilités associées à chaque option possible (dont 0,92 pour "theft" et 0,08 pour "normal" dans l'exemple donné). Un point notable : le nombre de tokens de sortie générés est nul à chaque appel, et chaque image coûte environ 667 tokens d'entrée en mode `detail: low`.

*Passage en revue de chaque scène :*
1. **Une scène normale** : rien à signaler, donc le pipeline la stocke et poursuit — pas d'incident, catégorie normale, gravité à 0.
2. **Une bagarre devant un bar** : les trois réponses concordent, donc l'alerte se déclenche — incident confirmé, catégorie "bagarre", gravité de niveau 2.
3. **Un acte de vandalisme sur le rideau d'une boutique** : même constat, les réponses concordent et l'alerte se déclenche — incident, catégorie "vandalisme", gravité de niveau 2.
4. **Un voleur à l'étalage glissant des écouteurs dans un sac à dos** : la question oui/non reste silencieuse et aurait raté l'incident, mais la question de catégorie identifie correctement un vol.

**Comparaison des Decision Models avec des LLM classiques**
Pour évaluer l'intérêt réel du modèle de décision, l'auteur a soumis les mêmes 47 images deux fois : une fois via l'API Decisions, une fois via l'API Responses en tant que LLM classique, avec les mêmes trois questions et une sortie au format JSON. Le second lot d'images comportait des scènes normales plus ambiguës, comme une personne courant pour attraper un bus ou un ouvrier repeignant un passage piéton. L'auteur précise avoir examiné ce second lot seulement après avoir fixé la règle d'alerte sur le premier lot, pour éviter tout biais. Une alerte est déclenchée dès que la réponse à la question de catégorie diffère de "normal".

Les résultats du benchmark :
- **Vitesse** : le modèle de décision est environ sept fois plus rapide, ce qui le rend exploitable dans un flux en temps réel.
- **Précision** : le LLM classique peut surpasser le modèle de décision sur certains cas limites. Les erreurs du modèle de décision concernent des scènes discrètes classées avec une confiance élevée (donc erronée), ce qui signifie qu'un simple ajustement de seuil ne suffirait pas à corriger le problème.
- **Combinaison des types de questions** : le cas de vol manqué par la question oui/non a été correctement détecté par le LLM, mais la vraie clé réside dans la combinaison de plusieurs types de questions au sein d'un même appel, afin de compenser les angles morts via une sortie composite.

**Quand l'utiliser, quand l'éviter**
*À utiliser quand :*
- Un verdict rapide et typé par élément est nécessaire (routage, signalement, notation).
- Les catégories forment une liste fermée courte, descriptible en une phrase.
- Une erreur de triage a un coût faible, car un humain ou une étape ultérieure réexamine les éléments signalés.
- Aucun jeu de données labellisé n'est disponible pour entraîner un modèle de vision dédié.

*À éviter quand :*
- Une explication est nécessaire, car le modèle ne fournit que des probabilités, sans raisonnement.
- La localisation d'un élément dans l'image est requise (pour des entrées multimodales), car aucune question de type "localisation" n'existe.
- Une garantie de fiabilité par élément est exigée, car les réponses restent probabilistes et les appels les plus lents peuvent prendre plusieurs secondes.

L'auteur conclut en se présentant brièvement : parti du marketing digital, il est passé par le tracking web, l'analytique, l'ingénierie analytique, l'ingénierie de données puis l'ingénierie IA, et explore encore aujourd'hui l'évolution de son propre rôle. Il remercie également Hoyt Emerson pour l'avoir encouragé à reprendre la publication de sa newsletter.

## Pourquoi ça compte
Ce retour d'expérience illustre une tendance concrète en ingénierie de données : l'émergence d'une couche de décision légère et rapide, intermédiaire entre les classifieurs ML traditionnels et les LLM généralistes, pour traiter des flux multimodaux à grande échelle sans la latence ni le coût d'un LLM complet. C'est un signal utile pour la veille sur l'évolution des architectures de pipelines data/IA et sur les nouveaux produits d'API orientés décision structurée (comme l'API Decisions d'OpenAI).
