---
title: "Can internal model transparency tame the AI race?"
date: 2026-09-22
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fblog.karthiktadepalli.com%2Fp%2Finternal-model-transparency%3Futm_source=tldrai/1/010001a0c42e94b8-7b241079-f6b5-4a4c-afea-c924ebe9e012-000000/iKeRQ2oxEeOXkdBdJpo5PBvOOFaCgfh3vlHddVCXSMQ=452"
authors: ["Karthik Tadepalli"]
keywords: ["gouvernance de l'IA", "course technologique", "auto-amélioration récursive", "transparence", "régulation", "laboratoires d'IA"]
theme: "IA"
tone: "opinion"
used_in: ["2026-09-22"]
---

## Résumé

Face à l'accélération de l'auto-amélioration récursive (RSI) des IA, portée par une pression concurrentielle intense entre laboratoires, l'auteur propose la « transparence des modèles internes » (IMT) : tout modèle déployé en interne par un laboratoire devrait aussi être fourni aux chercheurs des laboratoires concurrents. Il montre, via un exemple Anthropic/DeepMind, que ce mécanisme retire l'avantage compétitif de la RSI, incite les labos à moins investir dans les capacités de code de pointe, réduit le risque de concentration du pouvoir dans une seule entreprise, et permet des audits de sécurité par des tiers. L'auteur compare l'IMT aux réglementations de sécurité classiques et au projet « AI 2040 » de transparence totale de la recherche, la présentant comme plus légère à mettre en œuvre et à vérifier. Il reconnaît toutefois des limites : accélération à court terme du progrès agrégé, difficulté de faire respecter la règle, et persistance d'autres motivations (revenus, avantage de coût) à poursuivre la RSI.

## Points clés

- L'IMT oblige un laboratoire à partager tout modèle déployé en interne avec les chercheurs des laboratoires concurrents, ce qui supprime l'avantage compétitif tiré de la RSI.
- Exemple Anthropic (code) / DeepMind (science) : sous IMT, un labo ne peut plus transformer son avance dans un domaine en avance générale, ce qui décourage l'investissement massif dans l'automatisation de la R&D en IA.
- Deux bénéfices annexes : réduction du risque qu'un seul labo finisse par contrôler le modèle le plus puissant, et possibilité pour des tiers (autres labos, METR, Redwood Research) de tester la sécurité des modèles internes d'un concurrent — en référence à l'incident OpenAI-HuggingFace.
- L'IMT peut être mise en œuvre unilatéralement par les États-Unis, ou étendue à un accord Chine-États-Unis, avec une surface de vérification bien plus réduite que d'autres formes de coopération (ex. vérification du calcul).
- Comparée aux réglementations de sécurité classiques, l'IMT régule les incitations plutôt que les comportements ; comparée à la « transparence totale de la recherche » d'AI 2040, elle en est une version minimale et plus réalisable, limitée au modèle fini.
- Limites reconnues par l'auteur : risque d'accélération à court terme du progrès agrégé, difficulté de vérification pour un régulateur, et persistance d'autres motivations économiques (revenus, réduction des coûts) à développer des modèles de code avancés.

## Analyse approfondie

### Motivation

Alors que les laboratoires d'IA accélèrent l'automatisation de la recherche en IA elle-même (l'*auto-amélioration récursive*, ou RSI), la vitesse des progrès de l'IA devient préoccupante même pour les laboratoires de pointe eux-mêmes. 1400 employés de laboratoires de pointe ont signé la lettre « Pacing the Frontier », à l'appui de l'affirmation suivante :

> Pour réaliser le potentiel de l'IA, l'industrie, les gouvernements et la société dans son ensemble pourraient avoir besoin de la possibilité de gagner du temps afin de traiter les risques émergents, de développer des mesures de sécurité et de renforcer la supervision. **Mais chaque entreprise — et chaque pays — subit une pression concurrentielle intense qui l'empêche de ralentir unilatéralement cette accélération.** Et aujourd'hui, le monde manque des outils techniques et de gouvernance nécessaires pour rythmer délibérément les progrès à l'échelle de la frontière technologique.

Les incitations concurrentielles sont une motivation majeure qui pousse les laboratoires à développer l'IA bien plus vite et de façon plus imprudente qu'ils ne le souhaiteraient. Le problème est que la première entreprise à automatiser la recherche en IA peut prendre une avance décisive, concentrant un pouvoir énorme entre les mains d'une seule firme et forçant ses concurrents à entrer eux aussi dans la course. Nous avons donc besoin d'idées politiques qui découragent les entreprises de poursuivre la RSI, en atténuant leurs incitations concurrentielles.

Cet essai propose une telle idée : la transparence des modèles internes.

### La transparence des modèles internes

Une raison centrale pour laquelle les laboratoires poursuivent la RSI, malgré ses risques, est qu'elle leur donne une meilleure technologie de recherche que leurs concurrents. Imaginons que DeepMind se concentre sur la recherche scientifique tandis qu'Anthropic se concentre sur le code. Gemini obtient alors un A en recherche scientifique mais un B- en code. Anthropic peut battre DeepMind en rendant Claude A- en code, puis en utilisant ce Claude pour fabriquer un autre Claude qui obtient un A+ en recherche scientifique. En conséquence, la RSI procure aux laboratoires un avantage concurrentiel dans *tous* les domaines — ce qui signifie que les laboratoires qui ne poursuivent pas la RSI perdront nécessairement face à ceux qui le font. Ainsi, malgré les risques, la RSI est inévitablement attirante.

Cet avantage est suffisamment réel pour que les laboratoires cherchent à s'emparer des outils des autres. En août 2025, Anthropic a révoqué l'accès à son API pour OpenAI, car le personnel d'OpenAI utilisait Claude Code avant le lancement de GPT-5. Cette mesure est logique : donner à ses concurrents l'accès à ses meilleurs modèles annule l'intérêt même de posséder les meilleurs modèles.

C'est la motivation de la *transparence des modèles internes* (« internal model transparency », IMT), qui consiste en la proposition suivante : **dès qu'un laboratoire déploie un modèle à usage interne, il doit également le mettre à disposition des chercheurs des autres laboratoires.** Autrement dit, les entreprises ne peuvent pas utiliser leurs modèles internes comme source d'avantage concurrentiel dans la course à l'IA.

### Que ferait l'IMT ?

Pour voir l'effet que l'IMT aurait sur les laboratoires, il est utile d'imaginer d'abord que les laboratoires ne changent en rien leur comportement et continuent à se concentrer sur l'automatisation de la recherche en IA. Que se passerait-il alors ?

Dans l'exemple ci-dessus, la RSI a aidé Anthropic à battre DeepMind en recherche scientifique, car l'entreprise était accélérée par le fait que Claude était un meilleur outil que Gemini. Mais avec l'IMT, DeepMind aurait également accès à ce même Claude, si bien qu'Anthropic ne pourrait plus utiliser sa supériorité en code pour fabriquer un meilleur modèle que DeepMind. On peut même aller plus loin : DeepMind pourrait se spécialiser dans la collecte de compléments à un outil de code de pointe, comme de meilleures données de tâches sur la R&D scientifique que celles auxquelles Anthropic a accès. Avec ces données supplémentaires, DeepMind pourrait utiliser Claude pour produire un meilleur modèle scientifique d'IA qu'Anthropic ne pourrait en fabriquer avec Claude. Autrement dit, DeepMind peut profiter gratuitement de l'avantage d'Anthropic en code, mais Anthropic ne peut pas exploiter l'avantage de DeepMind en données. Ainsi, DeepMind bat Anthropic dans la fabrication d'une IA optimisée pour la science.

L'enseignement plus général est que, sous l'IMT, posséder un modèle vraiment excellent en R&D d'IA cesse d'être une source d'avantage concurrentiel. Cela réduit l'incitation concurrentielle à automatiser la R&D en IA, avec tous les risques que cela comporte.

En fait, l'exemple montre qu'il existe au moins une certaine incitation à profiter gratuitement des autres laboratoires : les laisser développer des capacités de code qui vous seront ensuite mises à disposition, pendant que vous consacrez votre argent et votre calcul à d'autres composantes de la pile d'entraînement de l'IA. L'équilibre qui en résulte est que chaque laboratoire investit beaucoup moins dans les capacités de code de pointe, et davantage dans d'autres sources d'avantage. Il devient ainsi possible de ralentir le développement de l'IA de pointe sans jamais l'imposer par une contrainte. Sous la transparence des modèles internes, un progrès plus lent émerge des incitations propres des laboratoires eux-mêmes.

Je considère que la désincitation à la RSI est la raison majeure d'adopter la transparence des modèles internes. Mais la proposition présente deux autres avantages substantiels :

1. **Elle rend beaucoup moins probable le scénario où une seule entreprise finit par contrôler le modèle le plus puissant.** Si tous les modèles intermédiaires qu'elle a dû construire pour y parvenir sont également accessibles à ses concurrents, il devient très difficile pour un seul laboratoire de conserver une avance sur tous les autres. Cela empêche une concentration du pouvoir au sein d'un seul laboratoire, dans les scénarios où la RSI se produit.
2. **Elle permet à des tiers de tester la sécurité des modèles internes.** L'incident HuggingFace a été provoqué par un modèle OpenAI déployé en interne, à usage « recherche uniquement ». Si ce modèle avait été accessible aux équipes de sécurité d'Anthropic ou de DeepMind, elles auraient pu découvrir des problèmes qu'OpenAI n'a pas identifiés. Ces risques seraient encore plus détectables si l'IMT était étendue à des enquêteurs tiers de confiance, comme METR ou Redwood Research, qui ont mené l'enquête sur l'incident OpenAI-HuggingFace. L'incident HuggingFace montre l'ampleur du risque que peuvent poser les modèles internes ; l'IMT pourrait offrir un moyen de mettre ces risques en lumière.

### Mettre en œuvre l'IMT

Une vertu de l'IMT est qu'elle n'a pas besoin d'être un accord international. Une réglementation ne couvrant que les laboratoires américains produit déjà le bénéfice de ralentissement du rythme, car la dynamique de course qu'elle vise est principalement une course entre laboratoires américains de pointe. Le principal coût de rester au niveau national est la fuite : les laboratoires chinois pourraient continuer à automatiser la R&D en IA sans contrainte, tandis que les États-Unis abandonneraient une partie de leur avance temporelle.

Si ce coût est intolérable, l'IMT s'étend naturellement à un accord entre les États-Unis et la Chine, où les laboratoires chinois seraient également parties à la réglementation. La Chine serait probablement d'accord, puisque l'IMT profite aux laboratoires suiveurs. Bien sûr, le défi consiste à vérifier la réciprocité de la coopération — s'assurer que les laboratoires chinois ne dissimulent pas leurs propres avancées vers la RSI.

Mais contrairement à d'autres formes de coopération internationale, la surface de vérification est minuscule. La seule chose que les États-Unis doivent vérifier est qu'un modèle disponible en interne pour les chercheurs d'un laboratoire chinois est également fourni aux laboratoires américains, ce qui est nettement plus simple à vérifier que d'autres formes de coopération internationale (par exemple la vérification du calcul).

Il reste quelques détails de mise en œuvre assez importants à régler. Quelle est la liste des entreprises incluses dans cette liste de transparence ? Comment est-elle décidée ? Comment s'assurer que les laboratoires ne servent pas des versions bridées de leurs modèles internes aux utilisateurs externes ? Comment empêcher les laboratoires de facturer des tarifs absurdement élevés lorsqu'ils fournissent leurs modèles internes à des concurrents, afin d'en restreindre effectivement l'usage ? Ces problèmes semblent solubles, mais ils doivent effectivement être résolus.

### Comment l'IMT se compare-t-elle aux autres réglementations sur l'IA ?

#### Réglementations de sécurité

Une manière directe de maîtriser la RSI serait d'imposer des règles directes sur le déploiement interne : inscrire dans la loi les politiques de sécurité déjà existantes des laboratoires, en exigeant des évaluations de sécurité avant qu'un modèle puisse être utilisé en interne. Cette formule — proposer des règles sur le développement/déploiement de l'IA que les laboratoires doivent suivre — est l'approche dominante de la gouvernance de l'IA.

Mais tandis que ces réglementations de sécurité régulent les comportements, l'IMT régule les incitations auxquelles font face les laboratoires. Une réglementation de sécurité doit préciser ce qui constitue une capacité dangereuse, maintenir cette définition à jour à mesure que la technologie évolue, et prendre en flagrant délit les laboratoires qui franchissent la limite. À l'inverse, l'IMT ne demande pas à un régulateur de juger si un modèle donné est sûr. Elle modifie la structure des gains de sorte que la course vers la RSI devienne moins rentable.

Rien de tout cela ne fait de l'IMT un substitut à une réglementation de sécurité directe. Mais cela signifie que l'IMT demande beaucoup moins aux régulateurs que les approches standards de la gouvernance de l'IA, tout en s'attaquant à l'incitation à la course qui est la cause profonde de progrès imprudents de l'IA.

#### Transparence totale de la recherche

AI 2040, le plan de gouvernance proposé par l'AI Futures Project, comprend un plan de coordination internationale fondé sur la « transparence totale de la recherche » : chaque innovation algorithmique jamais réalisée est immédiatement divulguée à l'ensemble du public. L'avantage de cette approche est qu'elle aide tout le monde à s'accorder sur la façon d'aligner l'IA, et décourage la course.

Mais la transparence totale de la recherche est une exigence lourde, avec une surface de contrôle immense. Elle s'articule avec d'autres caractéristiques d'AI 2040 — en particulier, la prémisse d'un accord international pour encadrer les centres de données et l'entraînement de l'IA. Mais la transparence totale de la recherche n'est pas applicable sans un accord international de grande ampleur.

La transparence des modèles internes est une forme minimale viable de transparence de la recherche : au lieu de partager chaque innovation, les laboratoires ne partagent que l'artefact final — le modèle lui-même. Et tandis qu'AI 2040 plaide pour que cette transparence soit totale, envers l'ensemble du public, je propose une version plus modeste où cette transparence est étendue principalement aux autres laboratoires, et éventuellement à des évaluateurs tiers de confiance.

Bien sûr, une forme internationale d'IMT nécessite encore un accord, et un certain degré de vérification. Mais la surface de cette vérification se limite à une API pour des modèles largement disponibles en interne dans un laboratoire. Il n'est pas nécessaire de surveiller les centres de données, les chercheurs, ou toute autre source d'avantage pour les laboratoires. Ainsi, l'IMT capture partiellement les bénéfices de la transparence totale de la recherche, tout en étant strictement plus facile à mettre en œuvre.

### Réserves

Il s'agit d'une idée encore brute, avec des limites claires :

1. À court terme, l'IMT accélère probablement le progrès agrégé de l'IA, en permettant aux entreprises retardataires de revenir dans la course. Cela pourrait être néfaste : il est beaucoup plus facile de coordonner un ralentissement entre laboratoires lorsqu'ils sont moins nombreux.
2. Réguler le déploiement interne est en général très difficile. Vérifier que les laboratoires respectent une quelconque règle sur leurs modèles déployés en interne exige une capacité technique bien supérieure à celle dont dispose actuellement le gouvernement américain.
3. Une meilleure technologie de recherche n'est pas la seule motivation à poursuivre des modèles de code avancés. Des modèles de code plus performants constituent une source de revenus considérable pour les laboratoires, comme le montre la croissance des revenus d'Anthropic. Les laboratoires voudront donc toujours fabriquer des modèles de code avancés ; l'IMT ne fait qu'atténuer une seule des motivations à la RSI.

**Réactions de lecteurs**

Excellent article, et c'est en réalité une idée très astucieuse. Il ne s'agit pas seulement de réduire l'incitation, comme vous le soulignez. Cela place même l'auto-amélioration dans une position légèrement désavantageuse par rapport à d'autres priorités, puisqu'elle bénéficiera aussi à votre concurrent. Bien sûr, comme vous le notez à la fin, l'incitation à poursuivre une telle recherche reste considérable, car elle constitue non seulement une source de revenus énorme, mais aussi, évidemment, la promesse d'un code futur bon marché. L'IA permettrait à ces laboratoires d'augmenter leur production et de réduire leurs coûts de main-d'œuvre, sans compter que la plupart des dirigeants de ces laboratoires semblent au moins un peu acquis à l'idée de la singularité, ce qui signifie qu'ils pourraient vouloir provoquer délibérément la RSI dans l'espoir que cela leur permette à l'avenir de produire des produits véritablement exceptionnels — même si, évidemment, il existe le risque qu'au moment où cela commence à produire des rendements aussi importants, on ne soit plus soi-même à la pointe. L'idée ici est qu'ils pourraient vouloir la singularité parce que, même si leurs concurrents se retrouvent sur un pied d'égalité, une telle révolution technologique augmenterait suffisamment la demande pour leurs produits pour que cela reste net bénéfique pour eux, avec une marge considérable.

Ma plus grande inquiétude à l'égard de la proposition est qu'elle repose sur l'existence de plusieurs laboratoires à la pointe ou proches de la pointe. Si les rendements d'échelle et d'autres dynamiques amènent l'industrie de l'IA à devenir très concentrée, au point qu'une seule entreprise domine quelque chose comme 80 à 90 % du marché, alors l'incitation se rapproche beaucoup du système antérieur à la divulgation. Même si cela abaisse la barrière à l'entrée, puisque n'importe quel concurrent pourra accéder à son modèle de pointe. Et bien sûr, selon la façon dont est fixée l'éligibilité au partage obligatoire, aucun concurrent ne pourrait en réalité y être éligible dans un scénario aussi concentré. Comme vous le soulignez également, l'autre grande source d'inquiétude est évidemment que, précisément parce que cela abaisse la barrière à l'entrée et réduit globalement les dynamiques favorisant la concentration du marché, cela peut rendre la coordination à l'échelle de l'industrie beaucoup plus difficile. Coordonner trois laboratoires est bien plus facile que coordonner 30 concurrents, et bien sûr, se débarrasser des dynamiques de RSI a pour effet secondaire que, alors qu'on pouvait auparavant s'attendre à ce qu'un laboratoire prenne l'avantage, la raison de s'y attendre a considérablement diminué si cette réforme est adoptée.

Cela dit, je pense qu'il s'agit surtout d'une raison d'être prudent sur les détails précis et de ne pas trop miser sur cette seule proposition ; dans l'ensemble, je pense que c'est une excellente idée, qui s'accorderait aussi bien avec les préoccupations de nombreuses personnes qui ne se soucient pas forcément de la sécurité de l'IA, mais qui s'inquiètent de choses comme les barrières à l'entrée, ou des entreprises à code fermé gardant leur recherche pour elles-mêmes, voire des personnes préoccupées par la concentration du marché. Pour peu que personne n'adopte cette mesure en la traitant comme un problème réglé sur l'IA — ce qui est, je pense, une inquiétude réelle avec certaines propositions moins ambitieuses qui cherchent à être incrémentales. Cela devrait être une excellente idée, capable de rassembler une large coalition de soutien. Et bien sûr, être trop ambitieux pose ses propres problèmes, car on pourrait tout simplement ne rien accomplir du tout si l'on se concentre uniquement sur ce type de propositions.

La transparence des modèles internes est un cadre percutant. Si la course est portée par l'avantage privé que chaque laboratoire tire de ce qu'il utilise en interne, forcer le partage de ces modèles avec la recherche réduit la récompense du secret, sans avoir à attendre une retenue volontaire. L'angle Anthropic-code contre DeepMind-science me convainc : une fois que ces outils circulent, une partie de la différenciation s'évapore. L'exemple OpenAI-Hugging Face rend également concret l'argument des tests par des tiers.

Lorsqu'un laboratoire déploie pour la première fois un modèle interne sous cette règle, à quoi devrait ressembler la transmission en pratique : les poids complets du modèle transmis aux laboratoires pairs, une API de recherche contrôlée, ou quelque chose de plus restreint qui permette néanmoins à des tiers de mener de véritables évaluations de sécurité ?

## Pourquoi ça compte

Cette proposition offre un angle de gouvernance de l'IA original — agir sur les incitations économiques plutôt que sur les interdictions techniques — et alimente le débat sur la course entre laboratoires, la concentration du pouvoir et la vérifiabilité des accords de sécurité en IA, des enjeux centraux pour toute veille sur la régulation de l'intelligence artificielle.
