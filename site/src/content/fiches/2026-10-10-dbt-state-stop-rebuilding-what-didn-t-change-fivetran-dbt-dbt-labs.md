---
title: "dbt State: stop rebuilding what didn't change | Fivetran/dbt | dbt Labs"
date: 2026-10-10
url: "https://substack.com/redirect/cc2840fb-d715-4122-a5ce-3d9c54f99def?j=eyJ1IjoiN3Y1bG1jIn0.HlvPOGYPdVknSYzEK1JIj6IFkAFn8zuyjtfU9Mbft9Q"
keywords: ["dbt State", "orchestration de données", "optimisation des coûts", "pipelines data", "dbt Labs", "data warehouse"]
theme: "Data"
tone: "news"
used_in: ["2026-10-10"]
---

## Résumé
dbt Labs annonce la disponibilité générale (GA) de dbt State, un moteur de décision qui évite de reconstruire un modèle dbt lorsque ni sa logique ni les données amont n'ont changé. Sur une plateforme où plus de 22 millions de modèles s'exécutent chaque jour, la majorité sont aujourd'hui reconstruits inutilement ; dbt State choisit entre réutiliser, cloner depuis un autre schéma, ou reconstruire, selon le principe de « l'action valide la moins coûteuse ». Plusieurs clients (CarGurus, Fanatics Betting and Gaming, Virgin Media O2, Joe & The Juice, RxBenefits, Obie) rapportent des réductions de coûts de calcul à deux chiffres et des gains de temps significatifs. La tarification est de 0,094 $ par table cible active et par jour, et un outil « Cost Insights » offre une visibilité complète sur les dépenses et économies réalisées.

## Points clés
- dbt State compare la logique SQL compilée de chaque modèle et la fraîcheur des données amont par rapport au dernier build réussi, et choisit entre trois actions : réutiliser, cloner depuis un autre schéma, ou reconstruire.
- La configuration repose sur des paramètres par modèle (`lag_tolerance`, `require_fresh_data_from`, `compare_unrendered_code`) ; la commande `dbt state explain` permet de comprendre chaque décision prise.
- Certains cas restent toujours reconstruits : vues avec `select *`, Jinja non déterministe (ex. `dbt_utils.get_relations_by_pattern` avec `union_relations`), et sources externes BigQuery sans `loaded_at_field`/`loaded_at_query`.
- Des clients rapportent des gains concrets : CarGurus (-9 % de calcul, -35 % de modèles construits, -15 % de coûts de backfill Snowflake), RxBenefits (-59 % de coûts sur les jobs planifiés, plus de 700 000 modèles réutilisés, deux semaines de temps de requête économisées sur 60 jours).
- La tarification est de 0,094 $ par table cible active réutilisée et par jour, chaque test comptant comme une table cible distincte.
- dbt Cost Insights (GA sur Snowflake, BigQuery, Databricks ; en preview sur Redshift) donne une estimation journalière des dépenses et des économies liées à dbt State.

## Analyse approfondie
**Le principe : ne plus reconstruire ce qui n'a pas changé**

L'article part d'une comparaison concrète entre deux jobs dbt horaires exécutant exactement les mêmes modèles dans le même projet. L'un reconstruit tout à chaque exécution, l'autre produit le même résultat, à jour, mais à un coût bien plus faible : c'est la promesse de dbt State, désormais en disponibilité générale. Le service suit, pour chaque modèle, si sa logique ou les données amont ont changé, et réutilise le résultat précédent si ce n'est pas le cas. Sur l'ensemble de la plateforme dbt, plus de 22 millions de modèles sont construits chaque jour, et la plupart sont reconstruits même quand rien n'a changé en amont.

**Démonstration côte à côte**

En comparant deux jobs horaires identiques — un avec dbt State activé, un sans — la différence est visible : sans dbt State, chaque modèle et chaque test s'exécute à chaque run. Avec dbt State, presque tous les modèles sont marqués comme « réutilisés », et les tests ne sont pas relancés sur les modèles réutilisés puisqu'ils ont déjà été validés précédemment. Pour le modèle `stg_suppliers`, l'interface indique explicitement qu'il est réutilisé car aucune de ses sources amont n'a de changement de données. Cette logique s'applique au niveau du modèle : un troisième job utilisant également `stg_suppliers` réutiliserait le dernier run valide, tant que les sources de données n'ont pas changé — ce qui en fait un levier puissant pour optimiser l'ensemble des pipelines dbt.

**Trois actions possibles, pas une seule**

dbt State fonctionne en comparant la logique SQL compilée de chaque nœud et la fraîcheur des données amont par rapport au dernier build réussi. Selon le résultat, il choisit l'une des trois actions suivantes :

- **Réutiliser depuis le même schéma** : si l'objet existe déjà dans le schéma cible, que la logique n'a pas changé et que les sources amont n'ont pas changé dans la limite du `lag_tolerance` défini, dbt laisse l'objet tel quel et réutilise les résultats du dernier build, pour tous les jobs concernés.
- **Cloner depuis un autre schéma** : si dbt trouve un objet identique (même logique, données fraîches) dans un autre schéma — par exemple construit lors d'un run de développement ou de CI avant d'arriver en production — il le clone plutôt que de le reconstruire.
- **Construire** : si aucun modèle réutilisable n'est trouvé, dbt reconstruit le modèle.

Le principe sous-jacent est celui de « l'action valide la moins coûteuse » : la validité prime, le coût vient ensuite.

**Configuration et points de vigilance**

dbt State fonctionne bien avec sa configuration par défaut, mais reste ajustable modèle par modèle. Parmi les options clés :

- `lag_tolerance` : le délai qui doit s'écouler depuis le dernier changement de données amont avant qu'une reconstruction soit déclenchée. On peut l'augmenter si les besoins sont alignés sur un cycle précis (par exemple un rapport analytique rafraîchi seulement chaque semaine).
- `require_fresh_data_from` : contrôle si une reconstruction se déclenche dès qu'une seule source se met à jour, ou seulement une fois que toutes les sources ont été mises à jour.
- `compare_unrendered_code` : indique s'il faut comparer le code non rendu d'un modèle avec le dernier build pour décider d'une reconstruction. *(Note de l'éditeur : l'article d'annonce de la GA fait référence à `compare_unrendered_code`, alors que ce brouillon mentionnait initialement `evaluate_volatile_sql`.)*

Pour comprendre précisément pourquoi dbt a pris telle ou telle décision sur un run donné, la commande `dbt state explain` indique quels nœuds ont été construits, ignorés, clonés ou différés, et pourquoi.

Le passage à dbt State ne nécessite que des ajustements mineurs de configuration. Les équipes utilisant auparavant la fonctionnalité d'orchestration sensible à l'état (« state-aware orchestration ») doivent faire correspondre l'ancienne valeur `build_after` aux nouvelles valeurs `lag_tolerance` et `require_fresh_data_from`. Si `build_after` n'existe pas, dbt applique ses valeurs par défaut : `lag_tolerance: 45m` et `require_fresh_data_from: any`.

Côté tarification, dbt State facture 0,094 $ par table cible active quotidienne, chaque test étant comptabilisé comme une table cible distincte. Ainsi, un modèle unique avec des tests `not_null` et `unique` sur une même colonne coûte au total 0,282 $ par jour de réutilisation, quel que soit le nombre de runs qui réutilisent ce modèle ce jour-là.

**Les limites de dbt State**

Certains cas d'usage ne bénéficient pas de dbt State : les modèles sont alors systématiquement reconstruits, faute de pouvoir fiabiliser la mise en cache :

- **Les vues utilisant `select *`**, car dbt ne peut pas résoudre les noms de colonnes sans exécuter de requête. Il est possible de contourner ce problème en excluant les vues du build via `dbt build --exclude config.materialized:view`.
- **Le Jinja non déterministe** (le langage de template utilisé par les modèles dbt), par exemple `dbt_utils.get_relations_by_pattern` combiné à `union_relations`, qui renvoie les relations dans un ordre variable et change donc le hash à chaque exécution.
- **Les sources externes BigQuery**, sauf si `loaded_at_field` ou `loaded_at_query` est configuré.

Dans la plupart des cas, de légères modifications de code suffisent à rendre ces schémas compatibles avec la mise en cache de dbt State. Si les gains de performance attendus ne se matérialisent pas, ces trois cas sont les premiers points à vérifier.

**Les économies constatées chez les clients**

Avec un nombre suffisant de clients utilisant dbt State en production, des résultats concrets émergent, et ils sont substantiels.

Parag Shah, vice-président data chez CarGurus, rapporte que la simple activation de dbt State a permis une réduction de 9 % du calcul, avec 35 % de modèles construits en moins, ce qui s'est traduit par une baisse de 15 % des coûts de backfill sur Snowflake.

Chez Fanatics Betting and Gaming, Alvin Chai, ingénieur analytique senior, indique qu'un projet pilote est passé d'un taux de réutilisation de 0,2 % à environ 15 %, atteignant jusqu'à 25 % sur certains projets, avec des économies de calcul à deux chiffres dès le premier projet.

Chez Virgin Media O2, la responsable de l'ingénierie analytique résume : dbt State a créé un changement de paradigme dans la façon de travailler de l'équipe — avec de la capacité libérée, une fraîcheur des données codifiée et une orchestration plus simple et plus intelligente, l'équipe peut désormais se concentrer sur les initiatives créatrices de valeur pour l'entreprise. Les gains de vitesse se mesurent aussi au niveau du modèle : chez Joe & The Juice, l'itération sur une table de faits de 400 millions de lignes est passée de 15-25 minutes à quelques secondes, éliminant le besoin de clonage ou de report manuel.

Chez RxBenefits, Chris Shepherd, ingénieur data principal, rapporte une réduction de 59 % des coûts sur les jobs planifiés de la plateforme dbt fonctionnant sur un entrepôt Snowflake adaptatif. En réutilisant plus de 700 000 modèles plutôt que de les reconstruire, l'équipe a également économisé deux semaines de temps d'exécution de requêtes sur une période de 60 jours.

Ces économies permettent aux équipes d'aller plus vite : Obie a réalisé suffisamment d'économies pour faire passer ses pipelines de données clés d'une fréquence quotidienne à une fréquence toutes les deux heures, offrant ainsi aux parties prenantes des données fraîches tout au long de la journée et des décisions business plus rapides et plus précises.

**Visibilité sur la facturation**

Une critique fréquente des plateformes cloud est le manque de transparence sur les coûts. dbt Cost Insights offre une visibilité complète sur ce que coûte dbt State et sur les économies réalisées. Une fois les coûts de l'entrepôt de données configurés, Cost Insights fournit une estimation des dépenses journalières. Cost Insights est en disponibilité générale pour Snowflake, BigQuery et Databricks, et encore en preview pour Redshift.

**Où dbt State s'exécute**

Étant un service distinct, dbt State fonctionne quelle que soit la façon d'utiliser dbt : sur la plateforme dbt ou via son propre système d'orchestration. Il opère également sur l'ensemble des environnements — typiquement trois : un environnement de développement local par développeur, un environnement de staging isolé orchestré en intégration continue (CI) qui exécute les tests et valide le fonctionnement avant mise en production, et l'environnement de production où vivent le code de release et les données réelles. dbt State fonctionne sur ces trois environnements, générant des économies de temps et d'argent à chaque exécution de pipeline : depuis les machines de développement lors de tests ad hoc, depuis les environnements de CI isolés à chaque pull request approuvée, et depuis la production lors des runs planifiés ou déclenchés par événement. Au-delà de la réduction des coûts, cela réduit le temps d'attente des producteurs de données à chaque étape, accélérant ainsi la mise en production des changements.

**Conclusion**

dbt State est présenté comme un moteur de décision : à chaque exécution, il détermine s'il faut reconstruire un modèle ou réutiliser les résultats du run le plus récent. Parce que cette décision est prise modèle par modèle, tout job utilisant un modèle donné peut bénéficier de temps d'exécution plus rapides sans sacrifier l'exactitude des données.

## Pourquoi ça compte
dbt State illustre une tendance de fond dans l'outillage data : la bascule d'une logique de reconstruction systématique vers une orchestration incrémentale et consciente des coûts, un enjeu central pour toute équipe data confrontée à l'explosion des coûts de calcul cloud (Snowflake, BigQuery, Databricks).
