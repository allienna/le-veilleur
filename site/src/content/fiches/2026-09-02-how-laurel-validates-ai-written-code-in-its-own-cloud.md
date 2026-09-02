---
title: "How Laurel Validates AI-Written Code in Its Own Cloud"
date: 2026-09-02
url: "https://link.mail.beehiiv.com/ss/c/u001.3a5P_SwQzY5x8USD2q4p0m895QuVtqvkW11dSkgIg8I7yY6GUJWSXHFbDSHBQ6GNuqYXUwDC32gA29Bi8V_NlU6RgC4T9tt54KGHciEU5y81VNls2F-KrTEKHhtz8Y9AJ3vM6gRkMTfbENO6FhSyLGRbKaVpdmsJ8JZEroO3u_9xI6uHad47QKqUIcc2yVHPsm2xBE_v6jiOHmsL6iI6G0DcZeZyeYKZwUl3F2H-OTdww3ve9WW4Y_uh5TasnHMoU6n7zEYiw0hp6fU0hCMl3W_e9uzTjosJkxQnBNVwqCbWSjPbck7C6gqTwhEFilPbrUkLQCg5vhAh0hVCQoRPC_hYRvz4_Mom4FdPb483IWs/4to/J86wL3ZyRZKrMW8TS6n3xA/h12/h001._X-C_JMD4DQJYmTt7HHYFcWdttZfSM-vfgQJ3VUvE-A"
authors: ["Naomi Klein"]
keywords: ["validation continue", "agents de codage IA", "Kubernetes", "environnements éphémères", "sandboxes par PR"]
theme: "Tech"
tone: "news"
used_in: ["2026-09-02"]
---

## Résumé
Laurel, éditeur de logiciels de suivi du temps et d'intelligence du travail pour les cabinets juridiques et comptables, voit désormais des agents IA rédiger 76 % de ses pull requests. Pour valider ce volume croissant de code sans faire sortir ni le code ni les données clients de son propre cloud AWS, l'équipe infrastructure a remplacé ses environnements de prévisualisation Vercel par des sandboxes éphémères par pull request, provisionnés directement sur son cluster Amazon EKS via l'outil Signadot. Résultat : malgré la montée en puissance du code généré par IA, le taux d'échec des changements est passé de 1,1 % à 0,2 % en trois mois.

## Points clés
- Sur ~60 ingénieurs, Laurel fusionne environ 9 pull requests par ingénieur et par semaine, avec 76 % du code désormais écrit par des agents IA (Claude Code, Codex, etc.).
- Les environnements de prévisualisation Vercel ne reproduisaient pas fidèlement la pile de production, ce qui générait des incidents récurrents.
- Contrainte de conformité forte : servant des cabinets juridiques et comptables, Laurel voulait éviter tout transfert de code ou de données clients vers un cloud tiers.
- Signadot crée, pour chaque PR, un sandbox ne dupliquant que les services modifiés, en routant le trafic pertinent via des « routing keys », le reste du trafic restant servi par un environnement partagé stable — tout cela sur le cluster EKS propre de Laurel.
- Une « routing key » unique, liée à un ticket Linear, permet de synchroniser les sandboxes à travers le monorepo front-end et les ~40 services backend concernés par un même changement.
- Sur une fenêtre de 30 jours, l'équipe a fusionné 2 873 PR (dont ~20 % d'automatisation), et le taux d'échec des changements est tombé de 1,1 % à 0,2 % alors que la part de code généré par agents grimpait de 55 % à 76 %.

## Analyse approfondie
**Le problème : valider un flot de changements générés par IA sans quitter son propre cloud**

Laurel exploite une stack Kubernetes sur Amazon EKS : une quarantaine de services backend (majoritairement Node.js, avec quelques services Python pour l'enrichissement de données) et un monorepo front-end de quatre services, qui constitue le plus gros cas d'usage de Signadot chez eux. Les données résident dans MongoDB Atlas et dans Postgres sur AWS Aurora, la messagerie repose sur Kafka, et l'observabilité s'appuie sur OpenTelemetry. L'équipe n'utilise pas de service mesh.

La demande de validation venait de trois directions à la fois : des ingénieurs souhaitant prévisualiser manuellement leurs changements, une volonté de faire tourner des tests de bout en bout automatisés en CI, et surtout le besoin de donner aux agents de codage une boucle de validation resserrée et réaliste. En tant qu'équipe d'ingénierie « AI-native » à l'avant-garde, Laurel générait plus de changements que ce qu'un dispositif de prévisualisation classique, divergent de la production, pouvait absorber sans risque.

Naomi Klein, Lead Infrastructure Engineer chez Laurel, résume : « Nous utilisions Vercel pour les environnements de prévisualisation, et c'était juste suffisamment différent de nos environnements de production, de staging et de développement pour causer des problèmes récurrents. »

Le vrai nœud du problème portait sur le lieu où cette validation pouvait s'exécuter. Servant des cabinets juridiques et comptables, Laurel garde les données clients à l'intérieur de son propre environnement AWS autant que possible, chaque fournisseur externe touchant à ces données ouvrant une nouvelle conversation de type « sous-traitant » que l'équipe préfère éviter. Les critères de sélection étaient donc stricts : fonctionner dans leur propre AWS, s'intégrer à GitOps, et se construire directement sur leur propre cluster Kubernetes de développement. Signadot répondait aux trois, ce qui en a fait le choix évident.

**La solution : des sandboxes par PR sur leur propre cluster EKS**

Plutôt que de dupliquer des environnements entiers, Signadot ne « forke » que les services modifiés dans un sandbox — un environnement éphémère léger — et utilise des clés de routage pour y diriger le trafic pertinent, tandis que toute autre dépendance est servie par un environnement partagé stable, le tout tournant dans le cluster propre de Laurel. Les sandboxes sont provisionnés par pull request, et l'ensemble fonctionne sur leur cluster EKS, détenu par l'équipe infrastructure et provisionné selon la même approche GitOps / infrastructure-as-code que le reste de leur plateforme.

N'ayant pas adopté de service mesh, Laurel a comblé ce vide directement grâce à DevMesh, le composant de Signadot dédié. Pour coordonner des changements qui traversent plusieurs dépôts, l'équipe associe une clé de routage à chaque ticket Linear, de sorte qu'une clé unique fait apparaître les sandboxes correspondants à la fois dans le monorepo front-end et dans les services backend concernés.

Naomi Klein : « Nous créons régulièrement des environnements Signadot sur presque chaque PR, pour presque chaque microservice. Nos ingénieurs peuvent construire et tester des changements à travers plusieurs services directement sur notre environnement de développement, en local comme via notre outillage CI. »

**Tests et agents de codage sur le même chemin**

Deux des plus gros cas d'usage de Laurel reposent sur cette fondation. Côté tests, Laurel a reconstruit sa suite de tests de bout en bout sur Signadot, en reprenant une partie de sa logique Playwright existante, grâce aux « Smart Tests » et aux clés de routage de Signadot.

Naomi Klein : « Nous avons construit une nouvelle suite de tests de bout en bout sur Signadot, un travail qui aurait été bien plus complexe autrement. Plusieurs ingénieurs ont rapporté à quel point Signadot les a beaucoup aidés à repérer des bugs dans leurs changements ou à valider leurs fonctionnalités. »

Côté agentique, Laurel voit affluer des PR entièrement générées par IA, aux côtés de PR assistées par IA et de PR entièrement humaines. Comme chaque PR reçoit automatiquement son propre sandbox proche de la production, les trois types de PR suivent le même chemin de validation. Les agents de codage — Claude Code, Codex et d'autres —, intégrés via l'outillage CLI et les « AI skills » propres à Laurel, reçoivent le même environnement isolé et réaliste qu'un ingénieur humain. C'est précisément l'objectif recherché : un seul endroit pour valider un changement, quel qu'en soit l'auteur, humain ou machine.

**Les résultats : plus de code écrit par IA, moins d'échecs**

Les gains qualitatifs sont arrivés en premier : des tests de bout en bout facilités, une nouvelle suite de tests construite sur Signadot, et des ingénieurs détectant bugs et validant fonctionnalités plus tôt qu'auparavant. Les chiffres viennent désormais confirmer ces gains.

Pour donner une idée de l'échelle que Signadot supporte aujourd'hui : sur une fenêtre récente de 30 jours, l'équipe de Laurel, forte d'environ 60 ingénieurs, a fusionné 2 873 pull requests. En excluant le trafic d'automatisation (environ 20 % du total), cela représente environ 2 300 PR d'ingénierie : 538 par semaine, soit environ 9 PR fusionnées par ingénieur et par semaine.

Le taux d'échec des changements est ce qui rend ce débit crédible. Sur ces mêmes trois mois, durant lesquels la part de PR d'ingénierie rédigées par des agents est passée de 55 % à 76 %, le taux d'échec des changements n'a pas simplement résisté à ce volume accru : il est tombé de 1,1 % à 0,2 %. C'était bien tout l'enjeu de cet investissement : absorber un volume croissant de changements de plus en plus générés par IA sans hausse correspondante des incidents. Laurel livre donc davantage de code écrit par IA tout en cassant moins souvent la production.

**Conclusion**

Pour une équipe « AI-native » soumise aux obligations de conformité liées à des clients juridiques et comptables, Signadot a offert à Laurel ce que les autres options ne pouvaient pas : une validation de qualité production qu'elle possède et exécute entièrement dans son propre AWS et Kubernetes, à l'échelle de chaque PR, couvrant la quasi-totalité des microservices de ses dépôts les plus critiques, et fournissant une surface de validation unique pour les ingénieurs comme pour les agents de codage.

Naomi Klein conclut : « Signadot facilite pour nos développeurs la construction et le test de microservices dans des déploiements extrêmement proches de la production. Cela a rendu le code, qu'il soit humain ou écrit par IA, plus facile à valider et à tester. »

## Pourquoi ça compte
Ce cas illustre un problème d'infrastructure qui va se généraliser dès que les agents de codage écrivent une part significative du code : la validation pré-merge doit devenir aussi rapide et fiable que la génération elle-même, sans sacrifier la conformité des données ni la fidélité à la production.
