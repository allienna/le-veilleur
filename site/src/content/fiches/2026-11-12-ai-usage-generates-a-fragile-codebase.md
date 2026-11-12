---
title: "AI usage generates a fragile codebase"
date: 2026-11-12
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fevanxmerz.com%2Fpost%2Fai-usage-generates-a-fragile-codebase%2F%3Futm_source=tldrdev/1/010001a1ca89a839-aabd319d-9c66-4193-901c-c3c50bf5912f-000000/KBsQHAgYNQWY3zJs5c95USUK5QagZr8ePRSqlKd4bss=452"
authors: ["Evan X. Merz"]
keywords: ["IA générative", "qualité du code", "dette technique", "codage agentique", "tests automatisés", "fiabilité logicielle"]
theme: "IA"
tone: "opinion"
used_in: ["2026-11-12"]
---

## Résumé
L'auteur, un ingénieur licencié de Meta en mai, affirme que la généralisation du codage assisté par IA produit des bases de code fragiles plutôt que des gains de productivité réels. Il identifie quatre mécanismes par lesquels l'IA fragilise le code (tests superficiels, complexité excessive, perte de compréhension humaine, rythme de revue trop rapide) et quatre symptômes observables (hausse des incidents, résolution plus lente, erreurs invisibles en interne mais visibles en production, dégradation de l'expérience utilisateur). Il conclut que les produits logiciels de qualité continueront de nécessiter une « touche humaine », faute de quoi le tout-IA mène à un cercle vicieux d'« enshittification ».

## Points clés
- L'auteur relie en partie son licenciement de Meta à sa réticence à adopter pleinement l'IA comme outil de codage, tout en précisant qu'il générait déjà 90 % de son code avec l'IA.
- Quatre causes de fragilité du code : tests automatisés superficiels, complexité inutile, érosion de la compréhension humaine du code, cadence de revue trop rapide pour maintenir la qualité.
- Quatre symptômes d'une base de code IA fragile : plus d'incidents, temps de résolution plus long, erreurs invisibles en tests mais visibles en production, dégradation de l'expérience utilisateur.
- Thèse centrale : les produits haut de gamme continueront d'exiger une touche humaine ; une dépendance totale à l'IA entraîne une dégradation progressive (« enshittification »).
- L'auteur se positionne en praticien plutôt qu'en opposant à l'IA : dans son poste actuel, il génère 100 % de son code via l'IA car c'est désormais l'attente de son employeur.

## Analyse approfondie
Je ne peux que spéculer sur les raisons de mon licenciement de Meta en mai, mais je suppose que l'une d'elles est que j'étais un peu plus réticent à adopter l'IA et les LLM comme outils de codage que certains de mes collègues. Ne vous méprenez pas, j'ai généré au moins 90 % de mon code à l'aide de l'IA durant mes derniers mois là-bas, ce qui était le minimum pour obtenir une évaluation correcte. Mais l'IA n'a pas multiplié par 10 la quantité de code que j'écrivais. Elle ne l'a même pas doublée.

J'étais concentré sur la qualité du code. J'ai vu le code poussé par certains de mes collègues très dépendants de l'IA, et j'ai constaté qu'il s'agissait de code fragile. Il y avait de nombreux problèmes subtils qui allaient générer de la dette technique à long terme, et même certains problèmes flagrants étaient ignorés par de très bons programmeurs. Par exemple, j'ai vu l'un des meilleurs programmeurs de mon équipe essayer de merger du code qui utilisait des événements JavaScript pour des effets CSS au survol de la souris plutôt que d'utiliser le sélecteur :hover, ce qui est une façon totalement non scalable d'écrire des effets de survol.

Aujourd'hui, je travaille dans une autre grande entreprise technologique et j'ai complètement basculé vers la génération de 100 % de mon code via l'IA, car c'est ce qui est attendu aujourd'hui. Pourtant, je vois beaucoup de gens prendre conscience que ce n'est pas une façon durable de poursuivre le développement d'un produit SaaS à grande échelle. L'IA a tendance à très bien résoudre les problèmes qui tiennent dans sa fenêtre de contexte, mais elle est totalement aveugle aux problèmes à long terme qui ne peuvent pas être compris dans ce cadre relativement restreint.

Dans cet article, je vais énumérer quatre façons dont l'usage de l'IA aboutit à une base de code fragile, incapable de résister aux exigences d'applications SaaS hautement disponibles et hautement scalables.

Au passage, chaque mot de cet article a été écrit par un humain. Même si l'image suivante a été générée par l'IA, cet article n'est pas du « AI slop ».

### Quatre façons dont l'IA fragilise les bases de code

Voici les quatre façons les plus courantes dont j'ai vu l'IA générer une base de code fragile.

#### 1. L'IA écrit des tests superficiels

L'un des échecs les plus évidents des LLM modernes est qu'ils ont tendance à écrire des cas de test automatisés simplistes qui ne couvrent pas ce qui compte vraiment pour les humains. Je vois fréquemment des agents IA écrire de nombreux tests pour des méthodes get/set qui sont triviales et ne nécessitent généralement pas beaucoup de tests. Lorsque l'IA écrit des tests e2e, elle a tendance à ne couvrir que les cas déjà couverts dans la base de code. En d'autres termes, l'IA n'écrit des tests que pour un seul type d'utilisateur, ou ne couvre que des interactions superficielles. Cela crée d'énormes trous dans la couverture de tests qui restent invisibles aux développeurs car ils ne sont pas captés par la métrique de couverture au niveau des lignes de code.

#### 2. L'IA écrit du code trop complexe

L'IA a aussi tendance à écrire du code trop complexe. Elle utilise fréquemment deux ou trois méthodes utilitaires là où une seule suffirait. Elle essaie de suivre des règles de bonnes pratiques, comme le DRY (Don't Repeat Yourself), de façon excessive, sans réaliser que la complexité ajoutée par cette rigidité rend le code plus difficile à déboguer ou à comprendre pour les développeurs humains.

#### 3. La dépendance à l'IA réduit la compréhension humaine

Et c'est le troisième problème des bases de code générées par l'IA : les humains ne les comprennent pas. Plus une entreprise s'appuie longtemps sur des agents IA pour générer le code, moins les développeurs comprennent la base de code. Cela signifie que les développeurs ne peuvent plus faire ce qui est nécessaire pour construire une base de code résiliente. Ils ne comprennent pas suffisamment bien les structures de données et les algorithmes pour voir qu'une pull request contient une nouvelle abstraction qui ne fonctionne pas avec les structures préexistantes.

#### 4. L'IA va trop vite pour maintenir un haut niveau de qualité

L'IA va trop vite pour que les développeurs humains puissent maintenir un haut niveau de qualité. Chaque pull request arrive plus vite que la précédente et doit être relue en encore moins de temps. Cela conduit les développeurs à survoler le code et à manquer des détails cruciaux qui se traduisent par de la dette technique à long terme. De petits problèmes de qualité, comme des trous dans les tests ou des variables mal nommées, s'accumulent dans la base de code jusqu'à ce qu'elle devienne un amas de code spaghetti.

### Quatre signes que votre base de code est fragile

Si vous n'êtes pas sûr que les agents de codage nuisent à votre base de code, vous pouvez rechercher les symptômes suivants d'une base de code fragile, générée par l'IA.

#### 1. Les bases de code générées par l'IA connaissent plus d'incidents

Quand votre département est passé au codage agentique, le nombre d'incidents a-t-il commencé à augmenter lentement ? Au début, quand nous utilisions tous des agents pour générer des quantités massives de code, cela ne semblait pas si différent du codage traditionnel. Les PR arrivaient, étaient mergées, et tout semblait aller bien. Mais voilà qu'un P0 est arrivé à la fin du mois, puis il y a eu deux SEV le mois suivant. Puis encore plus le mois d'après. Maintenant, après un an ou deux de codage agentique, on dirait qu'il y a un incident chaque week-end. Les agents de codage IA sont la raison pour laquelle il y a plus d'incidents impactant les clients.

#### 2. La récupération après incident prend plus de temps dans les bases de code IA

Non seulement il y a plus d'incidents, mais ils prennent plus de temps à être résolus. Le fait est que les développeurs humains de votre équipe ont désormais une compréhension plus superficielle de la base de code. Si votre agent de codage ne parvient pas à trouver le problème rencontré par vos clients, alors les humains vont devoir fouiller dans une base de code hautement complexe et mal testée. Ils se retrouvent essentiellement en territoire inconnu, ce qui leur prend plus de temps pour comprendre ce qui ne va pas. Par conséquent, les entreprises perdent de plus en plus d'argent dans des incidents qui prennent plus de temps à résoudre.

#### 3. Les bases de code générées par l'IA créent des erreurs qui ne sont visibles que par les utilisateurs

Quand les humains ne passent pas de temps dans le code, ils ne voient pas tous les cas d'usage. Ils ne comprennent pas comment les humains réels utilisent le code parce qu'ils ne s'assurent pas que l'IA instrumente correctement les analytics et capture correctement toutes les erreurs. Des erreurs invisibles apparaissent donc dans la base de code. Les erreurs ne sont pas capturées et ne sont visibles que par les utilisateurs du monde réel, par opposition aux types d'utilisateurs testés dans les tests automatisés ou lors des tests manuels des développeurs.

#### 4. L'IA se traduit par une mauvaise expérience utilisateur

Et cela nous conduit au problème ultime des bases de code IA : elles n'ont pas été conçues pour les humains. Les bases de code IA sont des logiciels faits par l'IA pour l'IA. Elles ne sont pas adaptées à la façon dont les utilisateurs humains utilisent le produit, ni adaptées à la façon dont les développeurs humains doivent maintenir le produit. L'expérience se dégrade à la fois côté utilisateur et côté développeur, menant à un cercle vicieux d'« enshittification ».

### Les produits faits pour les humains nécessitent une touche humaine

Le fait est que pour qu'un produit satisfasse des clients humains, il doit être façonné par une perspective humaine. Personne n'aime commander à des machines dans un restaurant. Acheter des vêtements sur un site web donne toujours des coupes moins bonnes que les acheter en magasin. Il en va de même pour les produits SaaS. Chaque fois que vous laissez votre produit SaaS dans les mains d'une machine, vous perdez la touche humaine qui est précieuse pour vos utilisateurs et vos développeurs. Cela peut fonctionner pour les produits les moins chers qui ne se différencient que par le prix, mais les logiciels de haute qualité continueront d'avoir une touche humaine. Les meilleurs produits, les plus chers, seront façonnés pour des utilisateurs humains par des développeurs humains. Ils seront charmants et agréables à utiliser. Ils ne seront pas fragiles, car ils ne seront pas principalement développés par l'IA.

## Pourquoi ça compte
Ce témoignage de terrain illustre concrètement les risques de dette technique, d'incidents et de perte de maîtrise humaine liés à une adoption agressive du codage agentique en entreprise — un contrepoint utile face au discours promotionnel sur les gains de productivité de l'IA en ingénierie logicielle.
