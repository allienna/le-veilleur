---
title: "Building Git infrastructure for agent-scale development"
date: 2026-10-09
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fgithub.blog%2Fengineering%2Farchitecture-optimization%2Fbuilding-git-infrastructure-for-agent-scale-development%2F%3Futm_source=tldrit/1/010001a11b7250a7-b7916d03-b70d-47ff-a4c5-2d892d3249b6-000000/QcjEJ8JD6d338HFmRYgP4CKkMO3WDy0tFKxAIal6kLo=452"
authors: ["Brian"]
keywords: ["GitHub", "infrastructure Git", "agents IA", "scalabilité", "architecture distribuée"]
theme: "Tech"
tone: "news"
used_in: ["2026-10-09"]
---

## Résumé
GitHub annonce une refonte profonde de son infrastructure Git pour répondre à l'explosion de l'activité générée par le développement "agentique", où des agents IA commitent et poussent du code en continu aux côtés des développeurs humains. L'article, écrit par un Principal Software Engineer de GitHub, détaille comment l'architecture actuelle (Spokes, avec cinq copies complètes par dépôt et un protocole de commit en trois phases) atteint ses limites quand la durabilité et la scalabilité reposent sur le même mécanisme : ajouter des répliques pour absorber les lectures ralentit les écritures. La nouvelle architecture vise à découpler le stockage durable (Azure Blob Storage) du calcul qui sert les requêtes, et à minimiser la coordination nécessaire lors d'un push, avec des gains mesurés en interne allant jusqu'à 35x en débit d'écriture.

## Points clés
- L'activité Git globale sur GitHub a plus que doublé entre septembre 2025 et août 2026 (de 218,2 à 473,3 milliards d'événements par mois), avec 7,38 milliards de commits en un seul mois de septembre (x5 en un an).
- Les pushes ont été multipliés par 4,9 en un an (0,69 à 3,35 milliards/mois) et les fusions de pull requests par environ 4, tandis que GitHub Actions a tourné 3,26 milliards de fois en septembre (x4+).
- L'architecture actuelle (Spokes) fait reposer durabilité et scalabilité sur le même mécanisme : chaque réplique participe à chaque écriture, donc un push est aussi lent que la réplique la plus lente, et ajouter des répliques pour les lectures ralentit les écritures.
- La nouvelle architecture repose sur deux principes : minimiser la coordination (ne synchroniser que la mise à jour de la référence, paralléliser le reste) et découpler le stockage (Azure Blob Storage comme source durable) du calcul (workers légers avec cache pour servir les lectures).
- Les benchmarks internes montrent un débit d'écriture jusqu'à 35 fois supérieur, avec une capacité de lecture qui s'ajuste élastiquement à la demande.
- GitHub promet de préserver les workflows et contrôles existants (branches protégées, revues obligatoires, logs d'audit) malgré la montée en échelle.

## Analyse approfondie

### Le contexte : une croissance tirée par les agents
Chaque jour, des millions de développeurs utilisent GitHub pour construire des produits, contribuer à l'open source et mener des projets personnels. L'architecture de GitHub a évolué au fil des années pour suivre cette demande croissante. Aujourd'hui, c'est le développement agentique qui pousse ce prochain changement architectural : développeurs et agents travaillent désormais simultanément dans des dépôts qui reçoivent des millions de commits par jour, ce qui exige une architecture Git différente.

Les charges de travail les plus intenses d'aujourd'hui donnent un aperçu de l'échelle visée. L'écart entre un dépôt typique et les dépôts les plus actifs est bien plus large qu'on ne l'imagine : en août 2026, le dépôt le plus sollicité de GitHub a reçu environ un milliard de requêtes. Au-delà de ces cas extrêmes, l'activité Git globale croît très vite : entre septembre 2025 et août 2026, elle a plus que doublé, passant de 218,2 à 473,3 milliards d'événements par mois. En septembre seul, développeurs et agents ont réalisé 7,38 milliards de commits sur GitHub, soit plus de cinq fois plus qu'un an auparavant.

Les dépôts en tête de cette courbe illustrent ce à quoi ressemble le développement agentique à la pointe : de grandes équipes d'ingénierie faisant tourner des pipelines CI intenses, en parallèle de flottes d'agents grandissantes. Soutenir ces équipes signifie construire une infrastructure Git capable de lectures et écritures concurrentes et soutenues, à une échelle que peu de dépôts atteignent aujourd'hui. GitHub investit donc massivement dans cette infrastructure pour répondre aux exigences du développement logiciel agentique.

Construire pour cette échelle soulève plusieurs défis architecturaux :
- **Le temps de traitement d'un commit devient un goulot d'étranglement par agent.** Un agent en boucle serrée commite ou enregistre un point de contrôle après presque chaque action. Sa vitesse est donc bornée par la rapidité d'un push unique — une latence qu'un humain ne remarquerait jamais devient le facteur limitant pour un agent.
- **La demande en débit d'écriture augmente de plusieurs ordres de grandeur.** Les pushes ont été multipliés par 4,9 en un an, passant de 0,69 à 3,35 milliards par mois. Des milliers d'agents travaillant sur leurs propres branches dans un même dépôt produisent un débit d'écriture soutenu qui converge vers un seul point de l'architecture.
- **Les fusions se disputent une référence unique.** Le développement en "trunk-based", les trains de versions et les files de fusion (merge queues) canalisent tout ce travail vers une seule référence qui doit absorber chaque fusion. Le volume de fusions de pull requests a crû de près de 4x en un an.
- **Chaque push se démultiplie en milliers de lectures.** Par exemple, la CI et l'analyse de code clonent ou récupèrent la même pointe de branche des milliers de fois par minute, et cette diffusion doit rester peu coûteuse. GitHub Actions a lui seul tourné 3,26 milliards de fois en septembre, plus de 4 fois plus qu'un an plus tôt.
- **Les opérations sur un dépôt doivent rester rapides.** Pour cela, GitHub compacte en continu les données du dépôt et nettoie les objets devenus inutiles. Chaque nouvelle écriture ajoute à ce travail, et le coût s'accumule avec le volume.

C'est pourquoi des clones rapides ne résolvent qu'une partie du problème. Les lectures sont relativement faciles à faire évoluer : on ajoute des caches, des répliques, et on sert les mêmes octets à plus de clients. Mais ces charges de travail exigent davantage. Les écritures sont bien plus difficiles : chaque push doit être stocké de manière durable et rendu visible de façon cohérente avant que l'agent ou le job CI suivant ne puisse s'appuyer dessus.

### Là où l'architecture actuelle rencontre de nouvelles exigences
L'architecture actuelle a bien servi les développeurs pendant des années. Chaque dépôt est stocké par Spokes, qui conserve une copie complète sur les disques locaux de plusieurs serveurs de fichiers — cinq par défaut. Ces disques locaux rapides permettent aux opérations Git de lire les données natives du dépôt avec une faible latence, et les copies supplémentaires apportent de la redondance tout en répartissant les lectures entre serveurs. Lorsqu'un push met à jour une référence, un protocole de commit en trois phases utilise un quorum pour garantir que la CI, l'interface web et les clients API voient un état cohérent du dépôt. Ce couple de mécanismes sert aujourd'hui un milliard de dépôts.

Cependant, le mécanisme utilisé pour la durabilité est le même que celui utilisé pour la scalabilité. Les copies sur disque constituent la source de vérité, donc ajouter de la capacité de lecture signifie ajouter une réplique durable supplémentaire. Chaque réplique participe à chaque écriture, donc un push n'est jamais plus rapide que la réplique la plus lente de son ensemble. Résultat net : ajouter des répliques pour absorber la charge de lecture ralentit les écritures.

Pour la plupart des dépôts, ce compromis fonctionne bien. Mais aux niveaux d'activité les plus élevés, il devient un plafond : ajouter des répliques de lecture ajoute de la surcharge aux écritures, perdre une réplique réduit la capacité de lecture, et perdre le quorum arrête complètement les écritures. Pour répondre aux exigences d'un monde "agent-first", il faut séparer la durabilité de la scalabilité sans perdre ce sur quoi les équipes comptent aujourd'hui.

### Construit pour les plus sollicités, meilleur pour tous
GitHub reconstruit cette infrastructure alors que la plateforme continue de fonctionner. Il n'y a pas de fenêtre de maintenance où le code du monde s'arrêterait de bouger, ni de version de ce travail qui demanderait aux utilisateurs de changer leur façon de développer pendant la transition.

Cette refonte vise les charges de travail les plus exigeantes de GitHub : une entreprise livrant sous des contraintes réglementaires strictes, une équipe qui fait atterrir un changement dans un dépôt qui construit un système d'exploitation, ou une organisation faisant tourner des milliers d'agents sur une seule base de code. Concevoir pour cette échelle élève le niveau pour tout le monde : le mainteneur qui relit les contributions de bénévoles répartis sur tous les fuseaux horaires, et l'étudiant qui ouvre sa première pull request, bénéficient tous deux de la même fondation, plus rapide et plus résiliente.

La nouvelle architecture doit aussi préserver les contrôles que les équipes utilisent déjà. Un mainteneur a besoin de protections de branche et de revues obligatoires pour qu'un changement non relu n'atteigne jamais la branche par défaut. Une équipe sécurité a besoin de logs d'audit et de visibilité sur le dépôt pour enquêter sur un accès suspect. Un ingénieur d'astreinte a besoin d'automatisation fiable et d'une observabilité suffisante pour comprendre pourquoi un déploiement a échoué.

Pour continuer à servir tout le monde tout en montant en échelle pour les charges les plus intenses, GitHub retient ces principes directeurs :
- **Construire sur les workflows auxquels les développeurs font déjà confiance.** Les équipes s'appuient sur des workflows comme le branchement, la revue, la fusion et l'historique pour construire, livrer et gouverner le logiciel à grande échelle. La nouvelle infrastructure est conçue pour prendre en charge ces mêmes workflows à des volumes d'activité bien plus élevés.
- **Donner la priorité à la fiabilité.** Chaque décision est mesurée à l'aune de la fiabilité attendue par les développeurs et les organisations. C'est cette confiance dans la plateforme qui permet à une organisation d'ingénierie de construire de l'automatisation, de livrer selon un calendrier, de répondre à des obligations de conformité et de comprendre le logiciel qu'elle produit. Ce travail améliorera sensiblement le débit et l'échelle, en prolongeant une fondation de confiance déjà existante.
- **Garder les gens en contrôle de leur code.** Si le système n'aide pas les personnes et organisations qui l'utilisent, et n'est pas sous leur contrôle, il ne vaut pas la peine d'être construit. Même si les agents prennent en charge une part croissante du travail, les propriétaires du code doivent toujours pouvoir le relire, le comprendre et l'approuver.

### L'approche
GitHub construit une nouvelle architecture capable de monter en échelle de façon beaucoup plus efficace, fondée sur des principes de conception de systèmes distribués appliqués à la concurrence et à l'échelle du développement logiciel agentique. L'objectif est de maintenir l'élan des communautés open source et des entreprises qui ont construit leurs projets sur Git et GitHub, tout en adaptant les fonctionnalités et contrôles existants aux besoins de l'ère agentique.

**Minimiser la coordination**
Un dépôt qui reçoit de nombreux pushes doit accepter et publier les mises à jour rapidement. La coordination a de la valeur quand elle protège la correction des données, mais trop de coordination limite le débit d'écriture et peut transformer un dépôt actif en goulot d'étranglement. L'architecture actuelle de GitHub est fortement couplée à des endroits où ce n'est pas nécessaire, ce qui limite la capacité à monter en échelle sur les lectures et les écritures sans compromis difficiles. GitHub redessine le système pour préserver la coordination requise par la sémantique de Git, tout en laissant tout le reste progresser indépendamment.
- **Ne coordonner que ce qui exige un accord.** La seule partie d'un push qui nécessite réellement un accord est la mise à jour de la référence elle-même. Stocker les objets sous-jacents, valider la connectivité des objets et scanner les secrets représentent un travail bien plus important, mais la majeure partie peut se dérouler en parallèle d'autres écritures. Cela réduit le chemin critique d'un push à la petite étape qui exige réellement une coordination, si bien que le reste du travail ne retarde plus l'accusé de réception.
- **Déplacer la maintenance hors du chemin de service.** La compaction et le ramassage des objets inutiles (garbage collection) comptent parmi les tâches les plus lourdes d'un dépôt, et aujourd'hui elles tournent sur les mêmes machines qui répondent aux requêtes Git en direct. Dans la nouvelle architecture, des workers séparés gèrent la maintenance directement sur le stockage durable. Un dépôt très actif peut ainsi être optimisé en continu en arrière-plan, sans ralentir les pushes et les fetches.

**Découpler le stockage du calcul**
Aujourd'hui, les copies complètes du dépôt sur disques locaux servent à la fois de stockage durable et de couche répondant aux requêtes Git. Séparer les deux permet de faire évoluer chacune indépendamment.
- **Faire évoluer les lectures sans ajouter de copies durables.** Dans la nouvelle architecture, la capacité de lecture provient de workers légers qui mettent les données en cache pour servir les requêtes. La copie de référence du dépôt réside dans une couche de stockage durable sous-jacente. Ainsi, la plateforme peut absorber de gros pics de lecture provenant de la diffusion CI, des flottes d'agents et des clones massifs, sans ajouter de travail à chaque push.
- **Laisser chaque couche faire un seul métier.** Les données de référence du dépôt résident dans Azure Blob Storage, qui fournit déjà durabilité et réplication à l'échelle d'Azure. La couche de calcul est optimisée pour un débit maximal à la plus faible latence possible.
- **Récupérer plus vite après une panne.** Quand stockage et calcul sont couplés, perdre une machine réduit à la fois la capacité et la durabilité, et la récupération implique de reconstruire une copie complète du dépôt. Quand ils sont séparés, perdre un worker de calcul se rapproche d'un simple cache miss : un worker de remplacement peut commencer à servir les requêtes immédiatement et remplir son cache depuis le stockage durable au fil du trafic.
- **Ajuster la capacité à la demande.** Les workers de calcul peuvent être ajoutés ou retirés selon les variations de trafic, plutôt que de provisionner à l'avance pour la charge de pointe. Un dépôt traversant un pic d'activité — comme une sortie de version ou l'arrivée d'une nouvelle flotte d'agents — peut obtenir une capacité supplémentaire pour la durée du pic, puis la relâcher une fois celui-ci passé.

Ensemble, ces principes permettent de supporter un débit plus élevé et davantage de travail concurrent, sans sacrifier la fiabilité et les contrôles dont les utilisateurs ont besoin.

### Et la suite ?
GitHub construit une architecture conçue pour offrir le débit et la fiabilité les plus élevés possibles : lectures et écritures évoluent indépendamment, et le système récupère sans accroc après une panne. Dans des benchmarks internes, cette architecture a déjà livré un débit d'écriture jusqu'à 35 fois supérieur, avec une capacité de lecture qui s'ajuste d'elle-même à la demande.

Alors que le développement automatisé augmente la fréquence et la concurrence des changements logiciels, GitHub fera évoluer ses fondations sans sacrifier la gouvernance et le contrôle sur lesquels les équipes s'appuient. Cette fondation est déjà en cours de mise en place. Un prochain article de cette série reviendra plus en détail sur l'architecture future de GitHub et le chemin qui y a mené.

## Pourquoi ça compte
Ce billet illustre comment l'essor des agents IA codant en autonomie oblige les plateformes d'infrastructure historiques (Git, CI/CD) à repenser des architectures vieilles de plusieurs années, avec des gains de débit (jusqu'à 35x) qui deviennent un avantage compétitif pour attirer les organisations qui déploient des flottes d'agents à grande échelle.
