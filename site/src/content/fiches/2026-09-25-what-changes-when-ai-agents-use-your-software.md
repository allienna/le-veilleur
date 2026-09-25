---
title: "What changes when AI agents use your software"
date: 2026-09-25
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Farize.com%2Fblog%2Fbuilding-tools-for-ai-agents%2F%3Futm_source=tldrdev/1/010001a0d31fd935-16efbac0-b8da-49bc-8c1b-f0db54f4a6a6-000000/biiDk3Z5rL6BPtAFcJTpEplkxuEUDFPeC6c3GnU42BI=452"
keywords: ["agents IA", "autorisation déléguée", "fiabilité", "outils pour agents", "sécurité", "ingénierie IA"]
theme: "IA"
tone: "news"
used_in: ["2026-09-25"]
---

## Résumé
Ivan Burazin, cofondateur et PDG de Daytona, estime que la prochaine étape clé de l'ingénierie IA consiste à construire des outils fiables pour les agents, pas seulement à améliorer les modèles. Il pointe deux frustrations concrètes : la confusion entre son identité et celle de ses agents (illustrée par son refus de leur donner accès à son compte bancaire sous ses propres identifiants), et des échecs récurrents liés à l'accès aux outils, qu'il juge plus fréquents que les limites du modèle lui-même. L'article, tiré d'un entretien pour la série « Rise of the AI Engineer » d'Arize, traduit ces frustrations en questions d'ingénierie concrètes : gestion des identités déléguées, conception de retries sûrs face aux échecs d'outils, et évaluation rigoureuse de la fiabilité des agents sur des essais répétés. Il conclut que concevoir de bons outils pour agents est un métier d'ingénieur IA à part entière.

## Points clés
- Les agents doivent avoir une identité distincte de celle de l'utilisateur, avec des permissions précises et révocables, plutôt qu'un accès hérité intégralement de l'utilisateur.
- Des standards comme l'échange de jetons OAuth permettent de distinguer le « sujet » d'un jeton de l'« acteur » qui exécute le travail délégué.
- Les échecs d'agents surviennent souvent à la frontière entre le modèle et les outils : mauvais choix d'outil, arguments invalides, timeouts ambigus, réponses peu exploitables.
- Pour des opérations comme les exports de données, il faut des contrats de récupération clairs (vérification de statut, idempotence appliquée côté serveur, fenêtres de validité) pour permettre des nouvelles tentatives sûres.
- Un succès passé ne garantit pas un succès futur : il faut évaluer les agents sur des essais répétés, dans des environnements réinitialisables, en distinguant la réussite de la tâche client du simple respect du workflow.
- Concevoir des outils pour agents implique un arbitrage entre richesse d'information (contexte) et simplicité d'usage pour le modèle.

## Analyse approfondie
Cet article, publié sur le blog d'Arize, relaie un entretien avec Ivan Burazin, cofondateur et PDG de Daytona (éditeur de sandboxes d'exécution de code), réalisé dans le cadre de la série « Rise of the AI Engineer ». Burazin y expose ses frustrations vis-à-vis des agents IA qu'il utilise, et l'article en tire une série de questions d'ingénierie concrètes pour les équipes produit.

### Identité de l'agent IA et accès délégué
Burazin résume sa frustration en une phrase : il ne veut pas que ses agents accèdent à son compte bancaire sous sa propre identité. Les agents avec lesquels il travaille ont tendance à se comporter comme s'ils étaient lui. Traduire cette frustration en exigence technique revient à définir précisément ce que le système autorisera, indépendamment de la façon dont le modèle se présente lui-même.

Plusieurs approches permettent de représenter cette relation entre utilisateur et agent : accès utilisateur délégué, identité de service dédiée, ou combinaison des deux. Le standard d'échange de jetons OAuth, par exemple, permet de distinguer le « sujet » d'un jeton (l'utilisateur pour le compte de qui l'action est menée) de l'« acteur » qui exécute réellement le travail délégué. L'implémentation appropriée dépend des services concernés et des permissions qu'ils supportent.

Donner à un agent un compte séparé ne résout pas à lui seul les décisions d'autorisation centrales. Un utilisateur pourrait autoriser un rapport sur un projet donné sans autoriser des exports portant sur le reste de l'organisation. L'intégration doit préserver cette frontière même si le modèle demande un jeu de données plus large.

Un « harness » d'agent — l'environnement d'exécution qui coordonne les appels au modèle et l'exécution des outils — peut aider à transporter le contexte pertinent et à filtrer les appels d'outils. Mais les services qui exécutent ces requêtes doivent eux aussi appliquer les règles d'autorisation. Le code d'intégration de confiance peut détenir les identifiants et n'exposer que les opérations permises, sans jamais placer les secrets eux-mêmes dans le contexte du modèle.

Les questions pratiques à trancher sont concrètes : quelle application agit pour quel utilisateur, à quelles ressources peut-elle accéder, et comment l'accès expire-t-il ou est-il révoqué ? Un journal d'audit doit permettre de reconstituer cette relation après coup. Ces décisions relèvent aussi de la spécification produit : si compléter un rapport nécessite une permission supplémentaire, l'équipe doit décider si l'agent doit demander une validation, renvoyer un résultat partiel clairement identifié comme tel, ou s'arrêter. Chaque choix engage une promesse différente vis-à-vis du client.

### Gérer les échecs d'outils et les retries sûrs
La frustration de Burazin concernant l'accès aux outils invite à regarder de plus près la frontière où le plan d'un agent rencontre le reste du système. Comme il le formule, « ces agents doivent réellement aller faire ces choses ».

Un échec à cette frontière peut avoir plusieurs causes : le modèle peut choisir le mauvais outil ou construire des arguments invalides ; une requête correctement formée peut être refusée, ou le service peut échouer pendant son traitement ; même une réponse réussie peut laisser le modèle incertain sur la marche à suivre. Ce sont des cas qui appellent des investigations différentes.

Prenons l'exemple d'un agent préparant un rapport : il demande à un service d'exporter un jeu de données, mais la réponse expire (timeout). Le service a pu rejeter la requête, démarrer l'export, ou le terminer avant que la connexion n'échoue — le simple timeout ne permet pas à l'appelant de savoir ce qui s'est réellement passé.

Pour une API d'export, le contrat de récupération doit préciser comment vérifier le statut d'une opération et dans quelles conditions un nouvel essai est sûr. Si le backend supporte des requêtes idempotentes, l'appelant peut réutiliser la même clé et les mêmes paramètres selon les règles documentées de ce service. C'est au serveur d'appliquer la déduplication : ajouter un identifiant à une requête ne crée pas cette garantie en soi. La fenêtre de validité de la clé compte également.

Lorsque le résultat reste inconnu, le système a besoin d'un chemin défini de réconciliation ou d'escalade : relancer un nouvel export peut ajouter du coût ou produire des résultats contradictoires sans pour autant résoudre ce qu'il est advenu du premier.

Ces problématiques sont familières à quiconque a maintenu une API. Ce qui mérite un test supplémentaire avec un LLM, c'est la façon dont le modèle choisit une opération et interprète les informations qui lui sont renvoyées. Les travaux d'Anthropic sur la conception d'outils soulignent l'intérêt de descriptions explicites, de contenus de réponse pertinents et d'erreurs exploitables.

Pour le workflow de rapport, l'outil doit permettre de distinguer une requête acceptée d'un export effectivement terminé. Il doit exposer un moyen de vérifier le job, préciser si un nouvel essai est possible, et distinguer clairement un échec de permission d'une simple indisponibilité temporaire. Une API ou un CLI existant fournit parfois déjà tout ce qu'il faut.

### Évaluer la fiabilité des agents sur des essais répétés
Ce qui surprend le plus Burazin, ce sont les échecs survenant sur des tâches que l'agent a déjà réussies par le passé. En décrivant des tests de Daytona portant sur la concurrence et le timing, il note que certaines tentatives échouent purement et simplement. Son exemple — neuf succès suivis d'un échec — illustre la frustration sans pour autant établir un taux d'échec mesuré.

Un succès antérieur montre seulement que le système pouvait accomplir la tâche dans ces conditions précises. Lors d'une tentative ultérieure, le modèle peut choisir une séquence d'actions différente, tandis que l'environnement peut lui aussi avoir changé : un jeton périmé, un jeu de données différent, ou un service sous charge peuvent modifier le résultat. Ces hypothèses doivent être investiguées séparément.

Pour l'équipe qui construit le workflow de rapport, une investigation utile commencerait par une tâche reproductible et une définition claire du succès : le fichier attendu doit contenir les données demandées, être accessible à l'utilisateur prévu, et arriver dans le budget de temps convenu. L'évaluation doit aussi vérifier l'absence d'accès non autorisé et d'opérations dupliquées involontaires — un fichier correct peut très bien coexister avec une erreur grave ailleurs dans l'exécution.

Pour comparer deux implémentations d'outils, il faut fixer le modèle, les instructions, le harness et les budgets d'exécution, et enregistrer leurs versions. Chaque variante doit être exécutée plusieurs fois à partir d'états de départ équivalents, dans un environnement de test réinitialisable — des exports résiduels ou des résultats mis en cache peuvent sinon fausser les tentatives suivantes. Les recommandations d'Anthropic sur l'évaluation des agents mettent explicitement en garde contre la distorsion des résultats causée par un état partagé.

Il faut ensuite tester délibérément la récupération, avec des scénarios comme une réponse perdue après que le serveur a accepté l'export, ou un changement de permission avant la reprise de la tâche. Ces tests répondent à une question différente de celle du scénario de référence : comment le système se comporte-t-il quand une dépendance cesse de coopérer ?

Une évaluation d'agent doit aussi distinguer le fait d'accomplir la tâche du client du simple respect du workflow. Un test peut réussir parce que l'agent arrête correctement un export non autorisé, même si aucun rapport n'est produit au final. Une approbation requise doit être comptabilisée séparément d'un sauvetage humain imprévu.

Pour les décisions produit, la réussite de la tâche doit être considérée conjointement avec le temps et le coût nécessaires pour y parvenir. Moins de tentatives peut être un signe positif si cela élimine du travail inutile, ou au contraire refléter un agent qui abandonne plus vite. Il faut donc rapporter le nombre d'essais et les circonstances des échecs avant de considérer qu'une petite amélioration de la moyenne constitue un progrès réel.

### Construire des outils pour agents, un métier d'ingénieur IA
Burazin insiste particulièrement sur le rôle des ingénieurs qui construisent des outils pour les agents, car ce travail exige de comprendre comment les modèles utilisent les interfaces qu'on leur donne. Sa prévision — voir les agents devenir les utilisateurs dominants des logiciels — reste une prévision, mais tester un produit existant avec un agent ne nécessite pas d'accepter d'emblée cette échelle.

Une équipe qui maintient un service d'export pourrait commencer par une tâche que ses clients délèguent déjà. Elle pourrait tester si des états d'opération plus clairs réduisent le nombre de jobs abandonnés, ou si un chemin de récupération documenté réduit le besoin d'intervention humaine. Le résultat constituerait une preuve concrète sur ce workflow précis, suffisante pour éclairer une décision produit.

Il existe un arbitrage à gérer : une réponse d'outil plus riche peut expliquer davantage tout en consommant plus de contexte et en noyant l'information dont l'agent a réellement besoin. Une opération conçue de façon trop étroite peut simplifier une tâche tout en compliquant l'expression d'autres workflows. Les améliorations doivent justifier leur place au regard des tâches que le produit est censé soutenir.

Pour Burazin, l'erreur stratégique a été d'hésiter à investir dans ce travail. En revenant sur les choix de Daytona, il déclare : « nous avons aussi couvert nos paris, et à cause de ça, nous avons été plus lents que nous n'aurions dû l'être. »

Ces améliorations doivent, in fine, profiter à la personne qui a délégué la tâche et s'attendait à passer à autre chose. Si l'agent a besoin de quelqu'un devant son clavier pour expliquer chaque résultat ambigu, le produit a laissé à son client une part substantielle du travail.

L'entretien complet avec Ivan Burazin est disponible dans la série « Rise of the AI Engineer ».

## Pourquoi ça compte
La fiabilité et la sécurité des agents IA en production — identités déléguées, retries sûrs, évaluation rigoureuse sur essais répétés — deviennent un axe d'ingénierie à part entière, distinct des progrès du modèle lui-même. C'est un signal utile pour toute équipe qui envisage de déployer des agents en conditions réelles plutôt qu'en démo.
