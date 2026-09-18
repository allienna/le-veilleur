---
title: "6-7 loops we use every day to make PostHog self-driving"
date: 2026-09-18
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fposthog.com%2Fblog%2Fself-driving-loops%3Futm_source=tldrdev/1/010001a0af146874-dc9a6ee3-a5dc-4222-8676-ccbdd199480a-000000/dNE34Dqzm-_6hLEqrkxtpWzeEzGbouSs2z4Q7P3aNRM=452"
keywords: ["agents IA", "automatisation", "PostHog", "boucles de rétroaction", "veille produit", "self-driving"]
theme: "IA"
tone: "opinion"
used_in: ["2026-09-18"]
---

## Résumé
L'auteur, membre de l'équipe « self-driving » de PostHog, explique que ce qui compte vraiment dans les usages de l'IA agentique au quotidien tient en trois choses : les outils, les skills et surtout les « boucles » (loops). Il détaille six à sept boucles concrètes utilisées en interne, où des agents (« scouts ») détectent des problèmes (retours MCP, messages Slack, logs, alertes métriques, enregistrements de sessions, issues GitHub), rédigent des rapports, déclenchent des PR correctives, puis reviennent vérifier que le correctif a bien tenu. L'humain garde la main sur la décision finale (relecture, merge) mais délègue la détection, le tri et une bonne partie de l'implémentation. Plusieurs exemples réels (PR, délais, métriques d'erreur) illustrent la rapidité et la fiabilité de ce système.

## Points clés
- Trois piliers retenus dans l'usage quotidien de l'IA : les outils (tools), les compétences (skills) et les boucles (loops) — ces dernières ayant le plus changé la façon de travailler de l'auteur.
- Une bonne boucle repère les problèmes, absorbe le travail fastidieux (triage, dédoublonnage, une partie de l'implémentation) et reste transparente : l'humain peut lire ce qui a été fait et intervenir à tout moment.
- Sept boucles sont décrites : retours MCP (« agent-feedback »), veille du canal Slack de l'équipe, tri des issues GitHub prêtes à implémenter, alertes sur le taux d'erreur des outils MCP, analyse des enregistrements de session via « Replay Vision », surveillance des logs runtime, et un mécanisme transversal d'auto-vérification (« self-validation »).
- Des exemples chiffrés illustrent la rapidité du cycle : une plainte utilisateur transformée en rapport en ~5 minutes, une PR ouverte 8 minutes après, et un correctif en production en moins d'une journée de travail.
- Les « scouts » ne se contentent pas de signaler un problème : ils reviennent vérifier après coup si le correctif a réellement fonctionné (environ un run de scout sur dix inclut une passe d'auto-vérification).
- Le rôle humain se déplace : moins de détection et de tri manuels, plus de rédaction de spécifications claires (issues GitHub), de relecture de rapports/PR et de décision finale sur ce qui est mis en production.

## Analyse approfondie

**Trois piliers : outils, skills, boucles**
L'auteur dit avoir renoncé à suivre en détail toutes les tendances autour des agents IA ; il préfère régulièrement se demander ce qui lui apporte une utilité réelle. Trois éléments reviennent systématiquement : les outils, les compétences (skills — il mentionne au passage le « PostHog skills store », en soulignant qu'on manque quelque chose si on l'ignore) et les boucles. Ce sont ces dernières qui ont le plus transformé son quotidien.

Selon lui, une bonne boucle remplit trois fonctions : elle repère ce qui mérite d'être regardé (elle surveille à sa place ce qui lui importe) ; elle lui retire les tâches ingrates — le tri, le dédoublonnage, la question « est-ce le même problème que la semaine dernière ? », et, de plus en plus, une part importante du travail d'implémentation lui-même ; enfin, elle le garde informé (« keeps me in the loop », jeu de mots assumé) : il peut lire précisément ce que la boucle a fait et pourquoi, et intervenir à tout moment pour la réorienter. Il ajoute être encore incertain de vouloir garder ce niveau de contrôle indéfiniment, mais que pour l'instant il aime encore décider de ce qui part réellement en production.

Son rôle au sein de l'équipe self-driving consiste justement à construire ces boucles qui permettent, à terme, de se passer de ce troisième point si on le souhaite.

**Boucle 1 — Retours MCP des agents (« agent-feedback »)**
Quand un agent ou un humain rencontre une friction en utilisant le MCP de PostHog, il peut soumettre un retour structuré, sans intervention humaine, directement depuis la session concernée, via l'outil `agent-feedback`. Ces retours alimentent un flux d'événements unique, `mcp feedback submitted`.

Plutôt que de faire relire ces retours manuellement par un humain, un scout nommé `signals-scout-agent-feedback` a été mis en place. Il regroupe les soumissions négatives ou bloquantes (`task_completed=false`) par thèmes de friction récurrents, en s'appuyant sur la convergence de plusieurs signalements vers le même problème. Il route chaque thème vers le bon propriétaire (MCP, une équipe produit, la documentation, ou l'équipe signals elle-même), et corrobore les thèmes liés au MCP avec les taux d'erreur réels des appels d'outils (`mcp_tool_call`) avant de se manifester. Une fois un seuil de confiance dépassé, il rédige un rapport dans une boîte de réception dédiée. Une tâche PostHog peut ensuite reprendre ce rapport pour ouvrir une PR, ou l'escalader vers l'équipe compétente pour arbitrage humain.

Ce qui en fait une boucle, c'est que le scout revient vérifier les éléments qu'il pense avoir été corrigés : il conserve des notes dans un bloc-notes interne sur ce qui a été signalé, ce qui a été livré, et valide que le correctif tient avant de considérer un thème comme clos.

Exemple donné : le 28 août à 11h28 UTC, un agent travaillant dans le projet d'un client soumet un retour de type `missing_tool` (`task_completed=false`) : il voulait définir des événements de catalogue avant qu'aucun n'ait été ingéré. Le MCP disposait d'un outil `event-definition-update` mais pas de création, si bien que l'agent contournait le problème en envoyant une capture anonyme « seed » par événement avant d'appeler la mise à jour — une solution jugée peu élégante. Environ cinq minutes plus tard, le scout émet un rapport après avoir vérifié l'absence de rapports préexistants, de PR ouvertes ou d'issues déjà assignées. Huit minutes après, la PR #90832 est ouverte : le point de terminaison REST de création existait déjà, il ne manquait qu'un outil pour l'appeler côté MCP.

La première version du correctif n'était pas parfaite : la PR est passée par plusieurs cycles de relecture assistée par agent, via ReviewHog (l'outil interne de revue de code) et Codex. La PR finale incluait des changements backend et des tests, en plus du nouvel outil. L'auteur l'a approuvée à 14h22, a déclenché le merge (`/trunk merge`) à 17h27, et elle était en production à 18h56 — moins d'une journée de travail entre la plainte initiale et le correctif, l'essentiel du temps humain se limitant à la relecture et à quelques instructions de pilotage.

Rôle de l'auteur dans cette boucle : relire les rapports et les PR. La détection, le tri, le dédoublonnage et l'analyse des causes racines se font en amont, avant même qu'il n'intervienne ; il pilote au besoin, mais la boucle capte régulièrement des correctifs utiles, petits ou plus importants, à mesure que les API, outils, skills et clients évoluent.

Schéma résumé : un agent client se plaint d'un problème MCP → un scout observe et synthétise le retour → il en fait un rapport → un agent self-driving reprend le rapport et crée une PR → intervention humaine ponctuelle → le scout vérifie que la PR a effectivement résolu le problème.

**Boucle 2 — Veille du canal Slack de l'équipe**
Certains des meilleurs signalements de bugs démarrent par un simple « est-ce que ça arrive à quelqu'un d'autre ? » lancé dans Slack : des soucis mineurs, assez gênants pour être mentionnés, mais pas assez prioritaires pour figurer sur une liste de tâches.

Le scout `signals-scout-team-self-driving` a été mis en place pour surveiller précisément ce type de signaux dans le canal de l'équipe : bugs, idées de fonctionnalités, retours clients qui se perdent dans les fils de discussion. Il regroupe par fil, ignore les échanges informels et les blagues, et fait remonter les éléments utiles dans la boîte de réception self-driving.

Exemple : le 25 août, un collègue (Dylan) partage dans le canal un lien vers une tâche, à propos d'un problème d'intégration GitHub. En cliquant sur le lien, l'auteur obtient un message « Task not found » et interroge l'assistant (`@PostHog`) directement dans le fil pour comprendre pourquoi. Il s'avère que la tâche existait bien, mais que la page utilisait un contrôle de visibilité différent qui rejetait la requête avant le chargement de la page. Le scout `signals-scout-team-self-driving` récupère ce bug évoqué dans le fil, rédige un rapport dans la boîte de réception, ce qui déclenche une tâche aboutissant à la PR #88912 corrigeant le problème. L'auteur ajoute deux relecteurs (Vojta et Georgiy), Vojta approuve, et la PR est fusionnée le 4 septembre. Un bug découvert par hasard en discutant d'un autre bug a ainsi été corrigé.

Rôle de l'auteur : reproduire les problèmes, relire les rapports, et impliquer les bonnes personnes pour la relecture du correctif. Parfois, comme ici, l'investigation démarre directement dans le fil Slack.

Schéma résumé : l'équipe remarque un bug → le partage sur Slack → un scout le récupère → mène l'investigation → crée une PR → l'équipe relit et fusionne.

**Boucle 3 — Tri des issues GitHub prêtes à implémenter**
Cette boucle est celle qui a le plus changé la façon de travailler de l'auteur. Il passe désormais davantage de temps en amont à rédiger des spécifications, sous forme d'issues GitHub décrivant le comportement attendu d'un changement de code. L'équipe dispose d'un scout, `signals-scout-self-driving-github-issues`, qui balaie régulièrement les issues GitHub de l'équipe et juge si elles sont prêtes à être implémentées (périmètre clair, absence de blocage, personne déjà en train d'y travailler).

Lorsqu'une issue est jugée prête, elle devient un rapport dans la boîte de réception et peut passer en implémentation. Une issue nécessitant encore une décision produit revient, elle, vers un humain. Le scout vérifie également l'existence de rapports correspondants pour éviter les PR en doublon.

Exemple : le 4 septembre, l'auteur rédige l'issue #94896 expliquant le besoin de pouvoir renommer un skill sans en perdre l'historique. Le contournement existant — dupliquer le skill puis archiver l'ancien — ne préservait ni les versions ni la propriété (ownership) du skill. Le scout d'issues récupère cette issue le matin même, ce qui déclenche la PR #95499 : ajout d'une boîte de dialogue « Rename » dans le menu du skill et d'un outil MCP `skill-rename`, tout en conservant les versions existantes, les fichiers associés et la propriété du skill. L'auteur approuve la PR le 7 septembre, et elle est fusionnée le matin même — une fonctionnalité qu'il souhaitait, issue d'une issue qu'il a lui-même rédigée, avec un résultat concret à évaluer en bout de chaîne.

Il souligne pouvoir faire avancer davantage de ces chantiers en parallèle puisqu'il n'a plus besoin de surveiller chaque agent au travail : rédiger une bonne issue et vérifier le résultat prennent toujours du temps, mais c'est un temps qu'il juge mieux employé.

Rôle de l'auteur : rédiger l'issue et vérifier le résultat avant fusion.

Schéma résumé : un humain rédige la spécification → un scout balaie régulièrement pour repérer ce qui est prêt → déclenche des tâches et des PR pour les spécifications prêtes → un humain relit et fusionne.

**Boucle 4 — Alertes sur le taux d'erreur des outils MCP**
Des alertes surveillent des métriques jugées importantes, notamment le taux d'erreur des outils MCP utilisés par l'équipe self-driving, et déclenchent une investigation en cas d'anomalie. Ces alertes sont postées dans le canal Slack de l'équipe, via l'intégration PostHog-Slack, ce qui permet de poser rapidement des questions de suivi et d'orienter l'agent vers un correctif.

Exemple : le 5 septembre, l'alerte sur le taux d'erreur MCP se déclenche à environ 9,9 %, contre une base habituelle de 0,3 % à 1,2 % sur les deux semaines précédentes. L'investigation cible l'outil `scout-project-profile-get` : 88 erreurs en une heure, réparties sur environ 44 projets. L'auteur répond dans le fil : « cherchons la cause racine ». L'agent relie les échecs à un déploiement ayant accordé aux scouts des permissions d'écriture supplémentaires optionnelles. En creusant, l'équipe identifie une incohérence entre deux workers déployés séparément : le planificateur envoyait désormais un dictionnaire décrivant les permissions, mais un worker sandbox plus ancien attendait encore l'ancien format de préréglage (preset).

L'auteur ouvre, avec l'aide d'un agent, la PR #95623 pour que les scouts sans permission supplémentaire réutilisent la chaîne de préréglage compatible ; elle est fusionnée l'après-midi même. Il ouvre également la PR #95621 pour corriger le filtre de déploiement ayant exclu le worker de tâches lors d'un changement de code OAuth partagé — cette PR restait ouverte au moment de la rédaction de l'article.

L'auteur note que, cette fois, l'alerte n'a pas corrigé la production toute seule pendant qu'il prenait un café : ce cas a demandé davantage de pilotage humain que les autres. Mais elle a permis de détecter le problème, de fournir un point de départ pour l'investigation, et d'aboutir à un correctif de compatibilité fusionné — ce qu'il considère comme un résultat satisfaisant.

Rôle de l'auteur : poser des questions de suivi, vérifier le diagnostic, et faire fusionner le bon correctif.

Schéma résumé : une métrique bouge → une alerte Slack se déclenche → l'équipe pose des questions d'investigation → un scout déclenche un correctif → l'équipe relit et fusionne la PR → le scout continue de surveiller la métrique et signale si le correctif n'a pas fonctionné.

**Boucle 5 — Analyse des enregistrements de session via Replay Vision**
Cette boucle part directement des utilisateurs réels du produit, sans qu'ils aient besoin de signaler quoi que ce soit. Elle s'appuie sur « Replay Vision », qui regarde les enregistrements de sessions et transforme ce qu'il observe en observations structurées.

L'équipe fait tourner un « monitor scanner » baptisé « Desktop onboarding friction » sur les enregistrements de PostHog Desktop, avec pour consigne approximative de repérer les utilisateurs visiblement bloqués. Un jour, un enregistrement montre un utilisateur rencontrant une erreur de fournisseur (provider error) dans PostHog Desktop, puis échouant à envoyer un message de relance.

Le rapport relie ces échecs visibles à une investigation, qui révèle une lacune dans la gestion des erreurs : une première erreur de fournisseur était déjà reconnue, mais une seconde contournait la gestion de nouvelle tentative (retry) et exposait le texte brut du fournisseur. Une télémétrie existait pour les échecs de tâches liés, mais le rejet du message de relance en lui-même laissait la session active sans générer son propre événement d'échec — un problème que seul l'enregistrement vidéo a permis de mettre au jour, là où le flux d'événements seul restait aveugle.

La PR #93181 fait correspondre cette erreur à la famille des erreurs de type « content block », rend le message de relance éligible à la gestion de nouvelle tentative, remplace le texte brut du fournisseur par un message plus lisible, et maintient la session desktop active pour ce type de rejet. Le correctif est fusionné le 2 septembre. L'auteur juge la PR elle-même peu spectaculaire, mais souligne l'intérêt de la manière dont le problème a été découvert : un utilisateur bloqué, et un enregistrement devenu point de départ d'un correctif.

Rôle de l'auteur : il a pris connaissance de ce rapport après la fusion du correctif ; un autre ingénieur a relu l'implémentation. Il inclut cet exemple car il illustre une nouvelle façon de détecter des problèmes que le reste de la télémétrie peut manquer.

Schéma résumé : Replay Vision observe les utilisateurs → enregistre les points de friction → nous les signale → déclenche une PR → l'équipe relit et fusionne.

**Boucle 6 — Surveillance des logs runtime**
Un autre dispositif s'appuie sur un scout planifié, `signals-scout-self-driving-logs`, chargé de repérer les problèmes dans les portions des logs runtime liées à self-driving. Il détermine ce qui a provoqué chaque log, si des lignes répétées correspondent à une seule boucle de nouvelle tentative ou à des échecs distincts, et si quelqu'un est déjà en train de corriger le problème.

Un run a ainsi détecté qu'une tâche ne parvenait pas à démarrer son sandbox Hogland (un service de VM interne) parce qu'un de ses tags de métadonnées était trop long. Ce tag incluait un identifiant de workflow composé d'un préfixe et de deux UUID. Des métadonnées qui fonctionnaient avec un fournisseur précédent se heurtaient désormais à une limite chez un fournisseur différent. La PR #92909 borne la longueur des chaînes de tags envoyées à Hogland et ajoute des tests sur cette longueur, tout en conservant les identifiants de tâche et d'exécution comme tags séparés.

Ce que l'auteur apprécie particulièrement, c'est ce qui s'est passé pendant que cette PR attendait en relecture : le scout a continué de vérifier, et chaque nouvelle exécution a ajouté des preuves du même échec au rapport existant, plutôt que d'ouvrir une investigation concurrente. L'auteur a demandé la fusion le 7 septembre, effective le matin même à 10h00 UTC.

Mais une fusion n'équivaut pas à une vérification en production : le harnais (harness) indique aux scouts de laisser des notes de suivi et de revérifier les preuves de ce qu'ils ont signalé, afin de confirmer que le problème est réellement résolu. Lors de son run suivant après la fusion, le scout constate que le dernier échec correspondant s'est produit à 10h06 et ne s'est plus reproduit ensuite — ce qui lui permet d'affirmer que « la salve d'erreurs Hogland s'est arrêtée après la fusion du correctif », sans avoir besoin de rédiger de nouveau rapport.

Ce mécanisme est appelé « auto-validation » (self-validation) en interne. Sur le mois écoulé, environ un run de scout sur dix a inclus une passe d'auto-validation : revérifier d'anciens constats fait partie intégrante du travail habituel.

Rôle de l'auteur : juger si le diagnostic et le correctif sont pertinents, puis faire fusionner le changement.

Schéma résumé : un scout planifié repère des éléments dans les logs → investigue les causes des problèmes → vérifie si c'est déjà corrigé → complète les rapports existants grâce à sa mémoire. Les scouts planifiés suivants continuent de surveiller les logs et d'enrichir les mêmes rapports plutôt que d'en créer de nouveaux.

**Conclusion et contexte produit**
L'article renvoie vers un « guide de mise en place self-driving » pour reproduire ce type de boucles sur son propre produit. L'auteur mentionne avoir rédigé cet article au moment de la sortie de « GPT 6 Astra », ce qui l'a incité à ajouter un mini-jeu en 3D à la page. Il termine sur une présentation de PostHog comme plateforme de référence pour construire des produits « self-driving », combinant observabilité IA, analytics produit, replay de sessions, feature flags, expérimentation, suivi d'erreurs et logs, le tout unifié par un data warehouse et un CDP, pilotable depuis Slack, le web app, l'application desktop ou son propre éditeur via le MCP.

## Pourquoi ça compte
Cet article illustre de façon très concrète, avec délais et références de PR à l'appui, comment une équipe produit fait évoluer le rôle de l'ingénieur d'exécutant vers superviseur/décideur en s'appuyant sur des agents qui détectent, corrigent et vérifient eux-mêmes leurs correctifs — un signal utile pour toute veille sur l'évolution des workflows de développement assistés par IA.
