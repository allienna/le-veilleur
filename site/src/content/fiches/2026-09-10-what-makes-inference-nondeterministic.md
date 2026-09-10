---
title: "What Makes Inference Nondeterministic?"
date: 2026-09-10
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Ftheaiengineer.substack.com%2Fp%2Fwhat-makes-inference-nondeterministic%3Futm_source=tldrdev/1/010001a085e345e0-e4ed8295-36b0-4db1-9ad1-88297af62686-000000/71oXrM_S3vhDn4Iz8rrgR_7Yt-S2sWfZodSqk9ct-I0=452"
keywords: ["inférence", "nondéterminisme", "GPU", "vLLM", "virgule flottante", "batch"]
theme: "IA"
tone: "research"
used_in: ["2026-09-10"]
---

## Résumé
L'article explique pourquoi un même prompt envoyé au même modèle, à température zéro, peut produire des réponses différentes d'une exécution à l'autre. La cause n'est ni le seed aléatoire ni un bug du modèle, mais l'arithmétique en virgule flottante : l'ordre dans lequel le GPU additionne les nombres varie selon la charge du serveur au moment de la requête, ce qui change le résultat final. Thinking Machines Lab a mesuré 80 complétions différentes sur 1000 requêtes strictement identiques. Des « kernels » dits batch-invariant, disponibles dans vLLM et SGLang, corrigent ce problème mais coûtent environ 38 % de débit en moins.

## Points clés
- 1000 requêtes identiques à température zéro ont produit 80 réponses différentes (expérience de Thinking Machines Lab), avec une divergence apparaissant au 103e mot.
- Fixer un seed ou activer les flags de déterminisme de PyTorch ne règle rien : le problème se situe une couche plus bas, dans l'addition flottante elle-même, avant même que le modèle ne « choisisse » un mot.
- L'addition en virgule flottante n'est pas associative : additionner les mêmes nombres dans un ordre différent donne un total différent (l'article illustre cela avec l'exemple `(0.1 + 1e20) - 1e20` qui donne 0, contre `0.1 + (1e20 - 1e20)` qui donne 0.1).
- Le GPU découpe les longues additions en groupes (« chunks ») traités par différents cœurs ; la taille de ces groupes dépend du nombre de requêtes traitées simultanément par le serveur (le batch), donc du trafic des autres utilisateurs au même instant.
- Des kernels « batch-invariant » (proposés par vLLM et SGLang) figent ce découpage quelle que soit la charge, ce qui restaure la reproductibilité au prix d'environ 38 % de débit en moins (SGLang mesure de 24 à 55 % de latence supplémentaire selon l'implémentation d'attention utilisée).
- Recommandation pratique : activer ce mode déterministe uniquement pour les evals, la RL, les audits de sécurité et les suites de régression ; le laisser désactivé en production sur le trafic conversationnel où la vitesse prime.

## Analyse approfondie

### Température zéro et pourtant deux résultats différents
On relance le même eval trois fois : même prompt, même modèle, même commit, température à zéro — ce qui est censé forcer le modèle à toujours choisir le mot le plus probable. Pourtant, un cas donné passe deux fois puis échoue une fois. En comparant les deux sorties, un seul mot diffère au 40e mot, et tout ce qui suit dérive à partir de là. Fixer un seed ne change rien de stable : le test repasse, puis rééchoue à la cinquième tentative. Le réflexe classique est alors d'étiqueter le test comme « flaky » et de le relancer automatiquement.

Thinking Machines Lab a reproduit ce phénomène à grande échelle : 1000 requêtes, un seul prompt, température zéro, sur une infrastructure de serving ordinaire. Résultat : 80 complétions différentes. Les 1000 réponses concordaient mot pour mot jusqu'au 102e token, puis divergeaient au 103e.

### Pourquoi le seed et les flags de déterminisme n'y changent rien
Deux solutions semblent évidentes mais échouent, car aucune des deux n'agit sur la véritable cause. Le seed est la valeur de départ du générateur aléatoire du modèle : au-dessus de température zéro, le modèle tire au sort parmi ses meilleurs mots, et le seed rend ce tirage reproductible. Mais à température zéro, il n'y a plus de tirage à reproduire.

Les flags de déterminisme de PyTorch sont la deuxième tentative : ils garantissent qu'une même opération, relancée dans les mêmes conditions, redonne le même résultat. Or les deux exécutions comparées n'ont justement pas eu lieu dans les mêmes conditions : l'une sur un serveur peu chargé, l'autre sur un serveur très sollicité. Rien dans ces flags n'oblige deux conditions différentes à converger vers le même résultat.
La cause véritable se situe une couche plus bas : dans l'arithmétique elle-même.

### L'addition en virgule flottante n'a pas d'ordre fixe
Un ordinateur stocke un nombre avec un nombre fixe de chiffres, comme une balance de cuisine n'affiche qu'un nombre fixe de décimales. Poser deux kilos de farine sur une balance à trois chiffres affiche 2,00. Ajouter une pincée de sel laisse toujours 2,00 affiché, car le chiffre que le sel ferait bouger n'existe pas sur cet affichage. Le sel n'a pas disparu : il n'a simplement nulle part où apparaître à côté d'un nombre aussi grand.

En code, avec 1e20 (un 1 suivi de vingt zéros) jouant le rôle de la farine et 0.1 celui du sel :
```
(0.1 + 1e20) - 1e20   # 0.0
0.1 + (1e20 - 1e20)   # 0.1
```
Dans la première ligne, on ajoute le sel à la farine puis on retire la farine : on obtient zéro, car le sel a disparu au moment même où il a rencontré un nombre aussi grand. Dans la seconde ligne, on soustrait d'abord la farine à elle-même, et le sel reste intact. Mêmes trois nombres, seul l'ordre des opérations change le résultat.

En poussant l'exemple plus loin : huit nombres qui s'annulent exactement (1, 0.01, 0.00001, 0.0000000001 et leurs opposés) devraient toujours donner zéro quel que soit l'ordre d'addition. Or, sur les 40 320 ordres possibles, on obtient 102 totaux différents. L'auteur a reproduit l'expérience à l'échelle d'un modèle : en prenant un vecteur de 4096 nombres (la taille typique d'un vecteur additionné à chaque couche d'un modèle) et en le sommant 255 fois, en variant à chaque fois la taille des groupes utilisés pour le découpage, on obtient non pas un seul total identique, mais dix-sept totaux différents — sur un simple ordinateur portable, sans rien changer d'autre que le découpage. Un modèle réel effectue ce type d'addition des milliers de fois pour chaque mot généré, et un serveur chargé modifie ce découpage à chaque fois.

### Comment le GPU découpe l'addition
Un GPU n'additionne jamais une longue colonne de nombres de haut en bas. Il découpe la colonne en groupes, confie chaque groupe à un ensemble de cœurs différents, puis additionne les totaux partiels à la fin. Une puce à 100 cœurs qui additionnerait 4096 nombres un par un laisserait 99 cœurs inactifs.

Le code responsable du découpage choisit le nombre de groupes de façon à occuper tous les cœurs disponibles ; ce nombre de groupes dépend donc de la quantité de travail à traiter à cet instant. Dix requêtes simultanées ne donnent pas le même découpage que trente, et un découpage différent signifie un ordre d'addition différent.

Or cette opération d'addition constitue l'essentiel du travail d'un modèle : les multiplications de matrices de poids, la normalisation entre les couches et le mécanisme d'attention sont tous de longues additions, chacune alimentant la suivante. Une différence infime sur la dernière décimale à la couche 1 se propage en entrée de la couche 2, et s'amplifie ainsi de couche en couche. À la dernière couche, les deux mots les mieux notés sont souvent plus proches l'un de l'autre que l'écart introduit par ce découpage.

Empêcher cela suppose un kernel — le petit programme GPU qui exécute une opération donnée — qui garde le même découpage quel que soit le trafic. Un tel kernel est dit « batch-invariant » lorsqu'il découpe les nombres de la même façon indépendamment du nombre d'autres requêtes partageant la machine. Or la quasi-totalité des kernels utilisés en production ne le sont pas, précisément parce que faire varier le découpage selon la charge est ce qui permet de garder tous les cœurs occupés.

### La charge du serveur fait varier la taille de vos batches
Une requête n'est jamais traitée seule. Un « serving engine » regroupe toutes les requêtes arrivées au même moment et les traite ensemble comme un seul batch, car charger les poids du modèle depuis la mémoire GPU coûte le même prix, que ce soit pour une requête ou pour trente.

Plus il y a d'appelants, plus le batch est grand ; plus le batch est grand, plus le découpage de l'addition change ; un découpage différent change l'ordre d'addition ; un ordre différent change le total ; et un total différent peut faire basculer le mot choisi. Sur une API hébergée, on ne voit ni ne contrôle la taille de son propre batch, qui varie minute par minute selon le trafic. Sur un serveur auto-hébergé, le paramètre `--max-num-seqs` plafonne le nombre de requêtes par batch, mais ne fixe qu'une limite haute : le batch reste rempli de tout ce qui arrive, jusqu'à ce plafond.

L'article cite l'issue GitHub 9567 de vLLM comme démonstration : avec un Llama 3 quantifié, à température zéro, une taille de batch fixée manuellement et sans variation de trafic, la sortie change malgré tout d'une taille de batch à l'autre — preuve que la cause se situe bien dans la pile logicielle de serving, indépendamment du code de l'utilisateur.

### Le coût des kernels batch-invariant
Le mode déterministe est un simple flag disponible dans vLLM et SGLang. Il remplace les kernels habituels par des kernels qui découpent toujours une colonne de nombres en un nombre fixe de groupes, quel que soit le nombre de requêtes dans le batch.

Ce découpage figé a un coût : le kernel normal ajuste la taille de ses groupes pour occuper tous les cœurs disponibles, tandis que le kernel figé applique le même découpage à un batch de 2 comme à un batch de 30 — ce qui laisse une grande partie de la puce inactive sur les petits batches. Thinking Machines Lab a mesuré une baisse d'environ 38 % du nombre de requêtes traitées par heure ; SGLang a mesuré un surcoût de latence de 24 à 55 % selon l'implémentation d'attention utilisée. Ces chiffres restent propres à chaque équipe, son modèle et son matériel.

Ni vLLM ni SGLang ne couvrent encore les modèles Mixture-of-Experts (qui routent chaque mot vers une sous-partie différente du réseau). TensorRT-LLM, de son côté, ne propose aucun mode de ce type : la reproductibilité n'y est garantie qu'à une taille de batch de 1.

### Reproductibilité pour les evals, vitesse en production
Le consensus des personnes ayant étudié la question : activer ce mode là où reproduire l'exécution est le produit lui-même, et le laisser désactivé là où la vitesse prime.

Reproduire l'exécution est le produit dans les evals, l'apprentissage par renforcement, les audits de sécurité, les suites de régression et la reproduction de bugs — une suite de régression incapable de reproduire ses propres échecs ne rapporte que du bruit, et un run d'entraînement non rejouable est un run qu'on ne peut pas déboguer. La vitesse est le produit sur le trafic conversationnel, la rédaction, le code, et partout où plusieurs bonnes réponses conviennent également.

Un piège à éviter : le moteur de serving applique ce mode à l'échelle du batch entier ; si un seul appelant demande de la reproductibilité, tous ceux qui partagent le même endpoint en paient la latence. Il faut donc dédier un endpoint séparé au trafic reproductible.

### Ce qu'il faut retenir
Le déterminisme n'a jamais été une propriété du modèle lui-même : c'était une propriété du fait d'être seul sur la machine. Toute exécution reproductible obtenue par le passé l'était uniquement parce que rien d'autre ne partageait le batch au même moment. Une machine vide donne le déterminisme gratuitement ; une machine chargée non, et le racheter coûte environ 38 % de la vitesse.

### FAQ
**La température 0 rend-elle un LLM déterministe ?** Non. Elle force le modèle à toujours prendre le mot le mieux noté, ce qui est différent de la question de savoir si les scores eux-mêmes sont stables. Ces scores proviennent d'additions dont l'ordre varie selon le nombre de requêtes partageant la machine, donc le mot le mieux noté peut changer même si le choix est parfaitement figé.

**Pourquoi mon modèle donne-t-il des réponses différentes avec le même seed ?** Le seed contrôle l'aléatoire du modèle, inutilisé à température 0. La variation vient d'en dessous : la requête est regroupée avec d'autres, la taille de ce groupe détermine le découpage de l'addition sur GPU, et l'ordre d'addition change le résultat.

**Le nondéterminisme de l'inférence est-il un bug ?** C'est un compromis assumé et documenté : vLLM et SGLang laissent le serving nondéterministe par défaut et rendent la reproductibilité optionnelle, car l'activer coûte environ 38 % de vitesse.

**Comment rendre l'inférence LLM reproductible ?** Activer les kernels batch-invariant du moteur de serving, figer l'implémentation d'attention utilisée (car elles se comportent différemment entre elles), et isoler le trafic reproductible sur son propre endpoint.

**Un endpoint dédié suffit-il à rendre l'inférence reproductible ?** Non à lui seul : il empêche les requêtes d'autres clients d'entrer dans votre batch, mais vos propres requêtes concurrentes continuent de se regrouper entre elles, donc le découpage continue de varier. Il faut combiner endpoint dédié et kernels batch-invariant.

L'auteur ajoute une inquiétude personnelle : l'impact de ce phénomène sur les pipelines d'évaluation. Si un même prompt peut produire des complétions différentes d'une exécution à l'autre, toute suite de tests reposant sur des assertions déterministes peut être silencieusement trompeuse — un problème que beaucoup d'équipes ne découvrent que lorsqu'un agent ayant passé la CI la veille échoue en production le lendemain matin. Mettre en cache les logits aide pour le replay, mais dès qu'on ajoute de l'usage d'outils ou du raisonnement en chaîne avec des embranchements, le nondéterminisme s'accumule d'une façon qu'un simple flag température=0 ne peut pas masquer.

## Pourquoi ça compte
Ce texte révèle une source de nondéterminisme dans l'inférence LLM largement méconnue et invisible depuis l'application cliente, avec un impact direct sur la fiabilité des evals, des tests de régression et des pipelines agentiques — un sujet clé pour quiconque opère des LLM en production ou construit des systèmes d'évaluation fiables.
