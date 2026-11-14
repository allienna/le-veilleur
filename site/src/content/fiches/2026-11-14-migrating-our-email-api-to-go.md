---
title: "Migrating our Email API to Go"
date: 2026-11-14
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fresend.com%2Fblog%2Fmigrating-our-email-api-to-go%3Futm_source=tldrdev/1/010001a1d4d6d4f1-3f79bd2d-3bd3-45e7-9808-ba3d194e24a0-000000/DzlvsrnWR0BI6bkpTakZYo_cArIxTOT33zoFk-Lc1ZI=452"
authors: ["Derich Pacheco", "Fabio Kubo"]
keywords: ["Go", "migration API", "Node.js", "performance", "latence", "tests de régression"]
theme: "Software"
tone: "research"
used_in: ["2026-11-14"]
---

## Résumé

Resend, service d'envoi d'emails par API, a migré son service Node.js le plus critique (l'API email) vers Go, en sept semaines et environ 140 pull requests. L'objectif n'était pas seulement la performance, mais la compatibilité stricte avec le comportement existant (réponses, erreurs, idempotence, limites de débit, contenu des emails). Le déploiement progressif (50/50 entre Node et Go) a montré que le service Go consomme environ 62 % de CPU en moins, réduit la latence médiane d'environ 50 % et l'empreinte mémoire d'environ sept fois par rapport à Node. Deux ingénieurs, Derich Pacheco et Fabio Kubo, reviennent sur les défis techniques et organisationnels de cette réécriture.

## Points clés

- Migration complète de l'API email de Node.js vers Go en 7 semaines (~140 PR), avec un objectif de compatibilité comportementale totale plutôt que de simple parité fonctionnelle.
- Les problèmes de départ sur Node : des pics de requêtes volumineuses bloquaient la boucle d'événements (parsing/sérialisation synchrones et coûteux en CPU), et des timeouts S3 remontaient en erreurs 408/524 côté client.
- Un harnais de tests comparatifs envoie les mêmes requêtes aux deux implémentations et compare réponses, lignes en base de données, objets S3, idempotence et limites de débit — pas seulement le code HTTP retourné.
- La conversion HTML-vers-texte a nécessité un portage spécifique en Go pour reproduire exactement le comportement de la librairie Node (gestion des attributs `data-skip-in-text`, texte des liens), validé sur 60 cas de test.
- Résultats du rollout à 50 % : latence médiane de `POST /emails` passée de 58 ms à 31 ms, p99 de 498 ms à 420 ms, mémoire par tâche de ~1,3 Go à ~180 Mo, et nombre de tâches en pic réduit de 34 à 10.
- Les ingénieurs soulignent les difficultés liées au changement de paradigme (async par défaut vs sync par défaut, typage faible vs fort) et la suppression de code devenu inutile une fois le problème de boucle d'événements éliminé.

## Analyse approfondie

**Contexte et enjeu de la migration**

Reconstruire une API critique implique de préserver des années de décisions implicites, y compris celles jamais documentées. Pour Resend, cela signifiait faire correspondre exactement les réponses d'erreur, le comportement d'idempotence, les limites de débit, les données stockées et même le contenu des emails envoyés. Une implémentation plus rapide n'aurait de valeur que si les développeurs pouvaient continuer à s'appuyer sur le comportement qu'ils connaissaient déjà.

Sur sept semaines et environ 140 pull requests, l'équipe a fait passer un nouveau service Go d'un projet vide à la gestion du trafic de production. Dès octobre, Go gérait tout le trafic de l'API email. Pendant la phase où le trafic était partagé équitablement entre les deux services, Go affichait environ la moitié de la latence médiane et environ un septième de la consommation mémoire par tâche.

**Les limites du service Node existant**

Lors de pics de requêtes volumineuses, une tâche entière pouvait devenir non réactive. L'investigation a montré que le parsing et la sérialisation de corps de requêtes volumineux en étaient la cause — y compris pour des requêtes déjà rejetées par le limiteur de débit. En Node.js, le parsing et la sérialisation sont des opérations synchrones coûteuses en CPU qui bloquent la boucle d'événements jusqu'à leur achèvement : le traitement de requêtes vouées au rejet pouvait donc bloquer la tâche pour tout le reste du trafic.

Des timeouts S3 se traduisaient également par des erreurs 408 et 524 visibles côté client. Ces problèmes ont façonné les exigences du remplacement : un comportement plus prévisible sous charge, une consommation de ressources plus faible, et un meilleur contrôle de la durée des opérations individuelles. Changer d'implémentation impliquait aussi de revoir la gestion des requêtes, les timeouts, les pools de connexions et le dimensionnement — ces décisions sont devenues une part substantielle de la migration.

**La compatibilité comme problème de test**

La philosophie d'ingénierie de Resend exige un comportement prévisible et une compatibilité ascendante. Lors d'une réécriture, ce principe devient un problème de test : comment établir que deux implémentations se comportent de façon identique ?

L'équipe a construit un harnais qui envoie les mêmes requêtes à Node et à Go puis compare leur comportement, couvrant les réponses et erreurs, les lignes en base de données, les objets S3, l'idempotence et les limites de débit. Se contenter de vérifier la réponse HTTP aurait laissé trop de zones non testées : les deux services pouvaient renvoyer une réponse de succès identique tout en persistant des métadonnées différentes ou en produisant un contenu d'email différent.

L'implémentation existante est devenue la référence de compatibilité, et certaines bizarreries de Node ont été délibérément préservées : modifier un comportement inattendu peut casser une intégration qui en dépend.

**Le cas de la conversion HTML-vers-texte**

Cet exemple illustre bien la difficulté. Quand un utilisateur envoie un email avec seulement une partie HTML, Resend le convertit en texte pour les clients mail et destinataires préférant le texte brut. La librairie Go initialement choisie produisait un texte raisonnable, mais différent de celui de la librairie Node configurée : des éléments marqués `data-skip-in-text="true"` apparaissaient dans la sortie Go alors qu'ils devaient être omis, et les liens pouvaient récupérer un texte d'URL absent de la sortie Node. Ces différences auraient changé l'email reçu par le destinataire.

L'équipe a donc construit un portage Go reproduisant précisément le comportement HTML-vers-texte utilisé par leur API. Ce portage initial correspondait exactement aux 60 cas de test générés à partir de l'implémentation Node, offrant une preuve concrète pour les cas couverts et une base pour en ajouter d'autres.

**Déploiement en production**

Une fois le comportement de l'ancien système reproduit, le défi suivant était de déployer le nouveau système avec succès — ce qui a demandé davantage de réglages en production. Le nouveau service consommait moins de ressources par requête, mais l'équipe a néanmoins dû doubler deux fois la taille des tâches pendant le déploiement.

Plusieurs changements opérationnels ont été réalisés, chacun répondant à une contrainte différente : une consommation moyenne de ressources plus faible n'indiquait pas la capacité nécessaire pour absorber un pic, et un traitement plus rapide des requêtes ne supprimait pas le besoin de borner les opérations de stockage ou de tenir compte des connexions Redis. Le déploiement progressif a fourni les preuves de production nécessaires pour prendre ces décisions.

**Résultats chiffrés (rollout à 50 %)**

Les chiffres suivants proviennent de la phase où la moitié des requêtes allait vers Node et l'autre moitié vers Go, les deux services tournant avec la même taille de tâche. Le service Go consommait environ 62 % de CPU en moins par requête. La latence médiane des requêtes `POST /emails` a chuté d'environ 50 %, tandis que le p99 a baissé d'environ 16 %. Une grande partie de la traîne lente du temps de réponse est due à l'attente sur S3 et la base de données : améliorer le service API réduit une partie de la durée de la requête, mais une réduction supplémentaire de la traîne nécessiterait d'agir sur ces dépendances elles-mêmes.

| Métrique | Node | Go |
|---|---|---|
| `POST /emails` latence médiane | 58 ms | 31 ms |
| `POST /emails` latence p95 | 149 ms | 107 ms |
| `POST /emails` latence p99 | 498 ms | 420 ms |
| Batch latence médiane | 149 ms | 74 ms |
| Batch latence p99 | 1 721 ms | 1 363 ms |
| Tâches au pic | 34 | 10 |
| Mémoire par tâche | ~1,3 Go | ~180 Mo |
| CPU par requête (normalisé) | 1,00× | ~0,38× |

**Le regard des ingénieurs : Derich Pacheco et Fabio Kubo**

Derich décrit la difficulté principale comme celle des « inconnus inconnus » : ce n'était pas un simple portage entre deux runtimes similaires, mais un passage d'un environnement asynchrone par défaut à un environnement synchrone par défaut, d'un langage permissif à un langage strict, et de types qui disparaissent à l'exécution à des types qui persistent. Beaucoup du comportement de l'API vivait en réalité dans Node et ses packages npm, pas dans leur propre code — l'exemple des pièces jointes est frappant : leur SDK Node accepte un `Buffer`, que `JSON.stringify` transforme en objet `{"type":"Buffer","data":[...]}`, que Node reconvertit ensuite en octets via un simple appel `Buffer.from()`. Go n'ayant pas de `Buffer`, cette conversion a dû être reconstruite à la main, règles de coercition de JavaScript incluses.

Kubo insiste sur la complexité particulière de cette migration : l'envoi d'emails étant le flux le plus critique, chaque changement exigeait une revue minutieuse, avec un investissement important dans les tests, les métriques et le réglage de l'infrastructure. S'ajoute à cela le fait qu'il s'agit d'une API publique : Resend ne contrôle pas ce qui lui parvient, donc toute entrée qui fonctionnait avant devait continuer à fonctionner — un défi accru en passant d'un langage permissif (JavaScript) à un langage strict (Go). L'enjeu n'était donc pas seulement de renvoyer la même réponse HTTP, mais de garantir que l'email arrive exactement comme avant.

Derich évoque aussi le « code astucieux » qu'ils ont pu supprimer : une partie du service Node existait uniquement pour protéger la boucle d'événements, où une requête lente bloque toutes les requêtes suivantes. La vérification de la taille des emails, par exemple, comportait une astuce élaborée pour éviter de scanner des corps volumineux octet par octet. Go n'ayant pas ce problème, une fois le portage stabilisé, cette astuce a pu être réduite à la seule partie qui économise réellement du CPU — un gain invisible dans les graphiques, mais qui simplifie la tâche du prochain ingénieur.

Kubo mentionne avec satisfaction un petit widget affichant la répartition en pourcentage des codes de statut HTTP : comme le trafic était réparti aléatoirement entre les deux services, leurs distributions de codes de statut devaient être quasi identiques, ce qui a donné une confiance supplémentaire, en complément des tests de validation, que tout se comportait comme attendu pendant le déploiement.

Enfin, les deux ingénieurs reviennent sur la dimension humaine du projet : Derich souligne la vitesse et l'autonomie dont ils ont bénéficié sur un projet de cette ampleur — chacun pouvait s'approprier une partie, mener des expérimentations et abandonner celles qui ne fonctionnaient pas sans attendre l'autre ; quand l'équipe a décidé de migrer aussi l'endpoint batch vers Go, le projet est passé de la décision à la production en environ une semaine. Kubo, pour qui il s'agissait de son premier projet chez Resend et de la première collaboration avec Derich, décrit une entente immédiate et une dynamique de travail où chacun enrichissait les idées de l'autre, reflet selon lui de la culture de l'entreprise.

## Pourquoi ça compte

Ce cas documente de façon très concrète les coûts réels et les méthodes de validation (harnais de comparaison, portage comportemental) d'une migration Node→Go sur une API critique et publique — un retour d'expérience précieux pour toute équipe envisageant une réécriture de service à fort trafic sans régression fonctionnelle.
