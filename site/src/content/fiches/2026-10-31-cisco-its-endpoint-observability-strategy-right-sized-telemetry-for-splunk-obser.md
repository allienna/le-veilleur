---
title: "Cisco IT’s Endpoint Observability Strategy: Right-Sized Telemetry for Splunk Observability Cloud"
date: 2026-10-31
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fblogs.cisco.com%2Fcisco-on-cisco%2Fcisco-its-endpoint-observability-strategy-right-sized-telemetry-for-splunk-observability-cloud%3Futm_source=tldrit/1/010001a18cc0296b-47ed0e76-3d7e-4e1d-a64c-db183e101824-000000/woCsUKgnXbRsI9pMFor1rFMEoambNalHd7WWq2OEjX4=452"
keywords: ["télémétrie", "observabilité", "Splunk", "Cisco IT", "OpenTelemetry", "endpoint"]
theme: "Software"
tone: "research"
used_in: ["2026-10-31"]
---

## Résumé
Cisco IT explique comment son équipe a repensé la collecte de télémétrie sur les postes de travail (endpoints) pour réduire de 75 % le volume de données tout en améliorant la visibilité sur la santé des appareils, des outils de collaboration et du réseau. Plutôt que de tout collecter en permanence, l'équipe a défini un modèle de télémétrie « juste dimensionnée » (right-sized) dans Splunk Observability Cloud, en évaluant chaque métrique selon son utilité réelle pour le support. L'article détaille huit stratégies concrètes issues de ce chantier, allant de l'ajustement de la fréquence de collecte à la gestion de la cardinalité des métriques. Le résultat est une base d'observabilité plus économique et plus durable, posée comme fondation pour une future automatisation du support.

## Points clés
- Réduction de 75 % du volume de télémétrie collectée sur les endpoints, avec à la clé une baisse des coûts de licence Splunk Observability Cloud.
- Environnement concerné : plus de 90 000 employés, postes macOS/Windows/Linux, VPN, proxy, applications de collaboration et destinations SaaS.
- Chaque métrique candidate est jugée selon quatre critères : son caractère actionnable, son utilité (évite-t-elle les doublons ?), son efficacité (métrique continue vs instantané en log) et sa portée (tout le parc ou seulement certains groupes d'appareils).
- Huit stratégies opérationnelles : fréquence adaptée à l'usage, conservation d'un socle de métriques essentielles, surveillance ciblée des process métier, profils de parc différenciés, collecte adaptative selon l'état de l'appareil, extension au chemin réseau, maîtrise de la cardinalité, et déploiement avec garde-fous.
- La démarche articule trois domaines habituellement cloisonnés : la santé de l'appareil, l'expérience de collaboration (ex. Webex) et le comportement du chemin réseau (DNS, VPN, proxy).

## Analyse approfondie

**Le défi : une visibilité complète sans sur-collecte**

Dans une entreprise distribuée comme Cisco, la résilience numérique commence au niveau du poste de travail de l'employé. Un problème ressenti sur ce poste peut en réalité provenir de plusieurs couches différentes : par exemple, une session Webex saccadée peut être causée par une surcharge du processeur, une mauvaise qualité de Wi-Fi, un état de VPN défaillant, ou encore un changement sur le chemin réseau.

Ce défi se pose à l'échelle de l'ensemble de l'environnement Cisco, qui compte plus de 90 000 employés, évolue en permanence, et couvre des postes macOS, Windows et Linux, de multiples états réseau, des applications de collaboration, des agents de sécurité, des VPN, des chemins de proxy, des destinations SaaS, ainsi que des utilisateurs travaillant depuis des lieux très variés.

Lorsqu'une dégradation survient sur l'une de ces couches sans être détectée, l'expérience de l'employé en souffre et la résilience numérique s'affaiblit — ce qui justifie l'importance de la télémétrie côté endpoint. Mais cela rend aussi la conception de cette télémétrie plus délicate : une seule métrique peut rapidement se démultiplier en de nombreuses séries temporelles (MTS) dès qu'on y ajoute des dimensions comme l'hôte, le système d'exploitation, le disque, le process, l'état, la direction, la cible ou le saut réseau. À l'échelle d'un parc entier et à haute fréquence de collecte, la courbe de coût peut grimper très vite.

L'observabilité des endpoints se heurte donc à un problème pratique : collecter chaque métrique de chaque appareil à haute fréquence peut générer plus de coûts, plus de bruit dans les données et plus de charge sur les appareils que de valeur réelle pour l'activité. Une approche différente était nécessaire.

**Une approche différente : dimensionner la télémétrie au juste niveau**

L'équipe a concentré sa stratégie d'observabilité des endpoints sur une seule question : quel est l'ensemble minimal mais suffisant de télémétrie permettant de comprendre la performance des appareils et d'accélérer la résolution des incidents, sans générer de coût, de bruit ou de charge inutiles ?

La réponse a pris la forme d'un modèle de télémétrie « juste dimensionnée », mis en œuvre dans Splunk Observability Cloud. Cette approche se caractérise par sa capacité à corréler des signaux provenant de domaines habituellement cloisonnés : la santé de l'appareil, l'expérience de collaboration et le comportement du chemin réseau. En analysant ces signaux dans une vue unifiée, les équipes de support peuvent aller au-delà des plaintes génériques sur une application. Par exemple, un problème signalé sur Webex est désormais immédiatement contextualisé : la télémétrie permet de distinguer une pression locale sur l'appareil (CPU, mémoire) d'une défaillance sur le chemin réseau (DNS, VPN, ou accessibilité du proxy).

Pour concrétiser cette approche, il a fallu passer de débats abstraits à un travail d'ingénierie concret. L'équipe a d'abord recensé l'ensemble des métriques produites par le Splunk OpenTelemetry Collector sur les environnements macOS, Windows et Linux. Cet inventaire a permis d'identifier les lacunes du jeu de données par défaut et de déterminer où des métriques personnalisées étaient nécessaires.

Chaque métrique candidate a ensuite été évaluée à travers un filtre rigoureux :
- **Caractère actionnable** : ce signal déclenche-t-il une réponse de support spécifique ?
- **Utilité** : fait-il doublon avec des données existantes, ou apporte-t-il un contexte unique ?
- **Efficacité** : doit-il s'agir d'une métrique continue, ou plutôt d'un instantané basé sur les logs pour éviter une cardinalité trop élevée ?
- **Portée** : l'ensemble du parc a-t-il besoin de cette métrique, ou seulement certains groupes d'appareils ?

Cette approche fondée sur la mesure a transformé la stratégie : d'un exercice consistant à « tout collecter », elle est devenue un cadre opérationnel précis, où chaque métrique est traitée comme un investissement.

**Huit stratégies pour une télémétrie d'endpoint juste dimensionnée**

Sur la base de l'expérience acquise en déployant le Splunk OpenTelemetry Collector à l'échelle de l'entreprise, l'équipe a identifié huit stratégies clés pour réussir un déploiement de collecte de télémétrie sur les endpoints :

1. **Adapter la fréquence au cas d'usage.** Un intervalle de collecte de 60 secondes suffit souvent pour les signaux liés à l'expérience employé et peut, selon leur modélisation, réduire le volume de points de données jusqu'à 75 % par rapport à l'intervalle par défaut du Collector (10 secondes).
2. **Conserver l'essentiel, éliminer le redondant.** Le jeu de métriques par défaut se concentre sur des signaux largement actionnables : CPU, mémoire, utilisation disque et entrées/sorties (I/O). Tout le reste doit justifier sa place.
3. **Traiter les métriques de processus comme à forte valeur mais à fort coût.** La surveillance des processus est limitée aux applications pertinentes pour l'activité, comme Webex, Duo et Cisco Collab Host, plutôt que de capturer chaque processus en cours d'exécution.
4. **Utiliser des profils de parc plutôt qu'un réglage global unique.** La profondeur de la télémétrie est hiérarchisée selon le besoin opérationnel, une collecte plus riche étant réservée au dépannage, aux appareils à risque élevé, ou à la réponse à incident.
5. **Rendre la collecte adaptative.** Les appareils en bon état fonctionnent de façon légère. Les appareils sous tension peuvent conserver le niveau de détail sur les processus et la performance nécessaire au dépannage, le système d'observabilité devenant ainsi plus attentif lorsque les conditions se dégradent.
6. **Étendre l'observabilité au chemin réseau.** Des contrôles fondés sur les domaines de défaillance permettent de distinguer si un problème provient de l'appareil, du réseau local, du VPN, du proxy ou de la périphérie SaaS — et pas seulement de savoir si un endpoint peut atteindre une destination.
7. **Maîtriser la cardinalité avant qu'elle ne prenne le dessus.** Les agrégations stables restent sous forme de métriques. Les instantanés de routes à forte cardinalité et les détails par échantillon sont déplacés vers les logs, où ils fournissent un contexte de dépannage sans alimenter l'explosion des séries temporelles.
8. **Déployer avec des garde-fous.** Des intervalles prudents, des limites strictes sur les cibles de sondage et les instantanés de route, une surveillance de la santé du Collector lui-même, ainsi que des boucles de retour avec les équipes de support, aident à faire tenir la stratégie à l'échelle sans créer de nouveaux problèmes de coût ou de fiabilité.

**Ce que l'équipe en retient**

La principale leçon est que l'observabilité des endpoints n'est pas un choix binaire entre tout collecter et accepter des angles morts. Il existe une voie intermédiaire plus efficace : capter les signaux actionnables lorsque les appareils ont besoin d'attention, tout en gardant une télémétrie légère sur le reste du parc.

En appliquant ces stratégies, Cisco IT a obtenu une réduction de 75 % du volume de données de télémétrie sur ses endpoints, ce qui diminue les coûts de licence Splunk Observability Cloud. Cette démarche s'inscrit dans le prolongement de la stratégie d'observabilité unifiée de Cisco IT, qui couvre le réseau, les plateformes et les opérations de service.

En réunissant les signaux d'endpoint, de collaboration et de chemin réseau dans Splunk Observability Cloud, l'équipe rapproche cette même fondation de résilience numérique de l'expérience employé. Les équipes de support peuvent désormais cibler plus tôt les domaines de défaillance probables, sans exiger que chaque endpoint envoie en permanence tous les signaux possibles — ce qui constitue une base plus solide pour une automatisation future.

Au niveau de l'endpoint, la résilience numérique dépend de la collecte des bonnes données, pas de toutes les données. Grâce à une télémétrie sélective, des garde-fous réfléchis et un focus sur les domaines de défaillance, les équipes peuvent dépanner plus efficacement, réduire le risque d'incidents non détectés affectant les employés, et le faire de manière pratique et durable.

**Ressources liées mentionnées dans l'article**
- La transformation de l'observabilité chez Cisco IT : de données fragmentées à une vision unifiée.
- Splunk Observability Cloud.
- Splunk OpenTelemetry Collector.

## Pourquoi ça compte
Ce retour d'expérience illustre une tension très actuelle en observabilité : le coût et le bruit croissants de la télémétrie face à la pression budgétaire, avec une méthode concrète (critères d'évaluation, profils différenciés, collecte adaptative) transposable à d'autres organisations IT qui cherchent à rationaliser leurs pipelines de monitoring sans sacrifier la capacité de diagnostic.
