---
title: "dbt State — Build only what's changed, skip the rest | dbt Labs"
date: 2026-10-16
url: "https://substack.com/redirect/551c1021-270e-45cf-9d00-95e796724244?j=eyJ1IjoiN3Y1bG1jIn0.HlvPOGYPdVknSYzEK1JIj6IFkAFn8zuyjtfU9Mbft9Q"
keywords: ["dbt State", "orchestration", "warehouse", "data build tool", "coûts cloud"]
theme: "Data"
tone: "news"
used_in: ["2026-10-16"]
---

## Résumé
dbt Labs présente « dbt State », une fonctionnalité qui analyse les métadonnées et le code SQL à chaque exécution pour ne reconstruire que les modèles réellement modifiés par les données amont ou le code. En évitant les reconstructions inutiles grâce à la réutilisation, au clonage ou au déferrement automatique vers la production, dbt State promet de réduire le coût de calcul de l'entrepôt de données de 15 à 30 % en moyenne. Le produit s'adresse aussi bien aux environnements orchestrés sur la plateforme dbt, en local, qu'avec un orchestrateur externe, et vise à simplifier la gestion de la fraîcheur des données directement dans le code plutôt que dans le planificateur.

## Points clés
- Détection automatique des changements (code ou données amont) à chaque run pour décider de construire ou non un modèle.
- Trois mécanismes d'évitement de reconstruction : réutilisation (coût et risque nuls), clonage (coût minimal), et déferrement automatique vers l'état de production en développement.
- Compatible avec les modèles complets, les modèles incrémentaux, les snapshots, les seeds et les tests.
- Déclaration de la fraîcheur et des règles de dépendance directement dans le code du projet (ex. `lag_tolerance`), remplaçant l'orchestration impérative par une configuration déclarative versionnée.
- Tarification à l'usage basée sur les « Daily Active Target Tables » (DATT), c'est-à-dire le nombre de tables cibles distinctes bénéficiant d'une opération de skip, de clone ou de réutilisation de test par jour.
- Témoignage client : Virgin Media O2 rapporte 25 % d'économies sur le temps d'exécution des jobs et les coûts de calcul de l'entrepôt.

## Analyse approfondie
### Arrêtez de reconstruire. Commencez à économiser.

Que vous orchestriez sur la plateforme dbt, que vous exécutiez dbt en local, ou que vous utilisiez un orchestrateur externe, dbt State rend chaque exécution plus intelligente : moins de calcul, une orchestration plus simple et une itération plus rapide.

**Simplifier l'orchestration**
Appliquez la fraîcheur sur le modèle dans le code, pas dans le planificateur. Exécutez aussi souvent que l'entreprise en a besoin. Pas de workflows personnalisés, pas d'orchestration manuelle.

**Développer plus vite avec des garde-fous**
Commencez à construire en quelques secondes sans aucun rituel de configuration complexe. Itérez librement et plus rapidement sans craindre les erreurs coûteuses ou les changements cassants.

**Optimiser la performance**
Réduisez le calcul de l'entrepōt de données de 15 à 30 % en moyenne en ne construisant les modèles que lorsque les données ou le code amont ont réellement changé. Arrêtez de payer pour reconstruire ce qui n'a pas changé.

> dbt State a été un changement de paradigme dans notre façon de travailler. Avec la fraîcheur codifiée, une orchestration plus simple, et au final, une capacité de développement libérée, nous consacrons plus de temps aux initiatives qui apportent de la valeur à notre entreprise. Et cela s'ajoute aux 25 % d'économies à la fois sur le temps d'exécution des jobs et sur les coûts de calcul de l'entrepôt.
> — Gordon Curzon, Head of Analytics Engineering chez Virgin Media O2

### De l'intelligence intégrée à chaque exécution.

À chaque exécution, dbt State vérifie vos métadonnées et le SQL de vos modèles pour voir ce qui a changé. Lorsque les données ou le code amont ont changé, il **construit** le modèle. Sinon, il **ignore** la construction en :

- **Réutilisant** l'état existant — calcul nul, risque nul
- **Clonant** l'état existant avec un coût de calcul minimal
- **Déférant automatiquement** (en développement) vers l'état de production

Cela fonctionne pour les modèles complets, les modèles incrémentaux, les snapshots, les seeds et les tests.

### Orchestration plus simple, données plus fraîches, exécutions plus efficaces.

Éliminez les heures passées à maintenir des workflows personnalisés et une orchestration manuelle. Activez simplement dbt State, configurez la fraîcheur, et exécutez vos jobs aussi souvent que nécessaire. Cela signifie des données plus fraîches, moins de complexité, et des économies significatives sur l'entrepôt sans changer votre façon de travailler.

**Configurations ajustées.** Déclarez les règles de fraîcheur et de dépendance directement dans le code de votre projet. Définissez une fenêtre maximale d'obsolescence via `lag_tolerance` pour que les modèles ne se reconstruisent que lorsqu'ils en ont besoin — pas à chaque exécution. Faites passer la logique d'orchestration d'une planification impérative à des configurations déclaratives et versionnées.

### Itérer plus vite dans des environnements de développement gouvernés.

Non seulement dbt State ignore et clone les modèles en développement, mais il peut aussi déférer automatiquement vers l'état de production, ce qui permet aux analytics engineers de commencer à construire immédiatement — sans surcharge manuelle et sans crainte d'erreurs coûteuses.

Le clonage automatique depuis la production et le déferrement automatique vous permettent de commencer à construire en quelques secondes. Vous n'exécutez que la partie du DAG sur laquelle vous travaillez. Pas de macros de clonage, pas de gestion manuelle de l'obsolescence. Aucune expertise de la syntaxe de sélection n'est requise ; dbt State constitue un garde-fou structurel contre l'explosion des coûts de développement, peu importe qui — ou quel agent IA — exécute la commande.

### La confiance des équipes data

### Réutilisez plus, économisez plus.

La tarification de dbt State est basée sur l'usage. Vous payez en fonction du bénéfice tiré de la réutilisation des modèles. Le coût de dbt State est mesuré via les « Daily Active Target Tables » (DATT). Les daily active target tables sont mesurées comme le nombre de tables cibles distinctes pour lesquelles dbt State effectue une opération unique de skip ou de clone, ainsi que des opérations uniques de réutilisation de test, au cours d'une journée calendaire donnée.

**Consultez la page tarifaire pour en savoir plus.**

## Pourquoi ça compte
Cette fonctionnalité illustre une tendance de fond dans l'outillage data : déplacer la logique de fraîcheur et d'orchestration du planificateur vers le code versionné, afin de réduire les coûts cloud et la complexité opérationnelle des pipelines analytiques — un sujet clé pour toute équipe data confrontée à l'explosion des coûts d'entrepôt.
