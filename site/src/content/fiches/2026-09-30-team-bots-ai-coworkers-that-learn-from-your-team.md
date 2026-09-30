---
title: "Team Bots: AI coworkers that learn from your team"
date: 2026-09-30
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Flinks.tldrnewsletter.com%2FD8PDTY/1/010001a0ed56b287-90a62935-8940-46d3-9a4e-6d8f51356728-000000/WbRu6QZPzVPfjwOVOGc1DR4IPe7ddpcoXtEiwtxlfUk=452"
keywords: ["agents IA", "Grok", "xAI", "productivité", "automatisation", "entreprise"]
theme: "IA"
tone: "news"
used_in: ["2026-09-30"]
---

## Résumé
xAI lance Team Bots, une nouvelle catégorie de Grok Bots partagés qui travaillent et apprennent aux côtés d'une équipe entière tout en conservant des conversations privées par utilisateur. En interne, l'entreprise les déploie pour briefer les équipes commerciales chaque matin, trier les bugs et coordonner l'ingénierie, faire respecter la charte de marque en marketing, et répondre aux questions de données à partir d'un entrepôt de plus de 45 000 tables. La fonctionnalité est disponible dès aujourd'hui en bêta publique sur les forfaits Teams et Enterprise, avec des bots préconfigurés pour les ventes, le produit, le marketing et la data.

## Points clés
- Un Team Bot se construit autour d'un rôle ou d'un workflow partagé par toute une équipe, avec compétences et mémoire communes, mais des conversations individuelles restant privées.
- Chaque Team Bot dispose d'un identifiant Slack dédié, ce qui permet de l'inviter dans un canal pour que toute l'équipe interagisse avec lui.
- Quatre cas d'usage internes illustrent le concept : un bot de comptes commerciaux (briefing matinal), un bot d'ingénierie (triage de bugs, tickets, Cloud Agents), un bot marketing (revue de marque et publication SEO) et un bot de données (requêtes en lecture seule sur l'entrepôt).
- Un exemple client externe est cité : Harper, une compagnie d'assurance, utilise un bot pour repérer les polices expirées et aider à leur réactivation.
- Les bots mémorisent les corrections et décisions au fil du temps, ce que l'un apprend améliore les réponses données à toute l'équipe.
- Lancement en bêta publique, réservé aux forfaits payants Teams et Enterprise.

## Analyse approfondie
Aujourd'hui, nous lançons Team Bots, des Grok Bots qui travaillent et apprennent aux côtés de votre équipe. Donnez-en un accès aux fichiers, applications et expertises dont il a besoin, puis partagez-le afin que chacun puisse travailler à partir du même contexte.

Chez SpaceXAI, les Team Bots briefent chaque matin les équipes en charge des comptes clients, coordonnent des projets d'ingénierie et répondent à des questions sur les données à travers toute l'entreprise. Voici comment ils fonctionnent, comment nous les utilisons, et comment en créer un pour votre propre flux de travail.

Vous construisez un Team Bot autour d'un rôle ou d'un flux de travail partagé par votre équipe. Tout le monde a accès au même Bot et à son expertise, tout en pouvant continuer à travailler avec lui individuellement.

Chaque Team Bot réunit quatre éléments qui l'aident à accomplir sa mission :

Bien que le Bot soit partagé, les conversations de chaque personne avec lui restent privées. Le Bot conserve un contexte et des souvenirs distincts pour chaque utilisateur, tout en s'appuyant sur les compétences partagées au sein de l'équipe.

Les équipes peuvent également collaborer avec un Team Bot dans Slack. Chaque Team Bot possède son propre identifiant, ce qui permet de l'inviter dans un canal où chacun peut poser des questions, apporter du contexte et voir ses réponses.

Chez SpaceXAI, nous utilisons les Team Bots dans certains de nos flux de travail les plus riches en contexte. Voici quatre exemples issus des Ventes et de la Réussite client, du Produit et de l'Ingénierie, du Marketing, et de l'Analyse de données.

Chez SpaceXAI, chaque grand compte commercial dispose d'un Team Bot dédié. Chaque Bot est partagé par l'account executive, le customer success manager, l'architecte solutions et le responsable des ventes.

Chaque nuit, le Bot passe en revue l'actualité de l'entreprise, les appels Gong récents, les documents Notion et les fils Slack pertinents. Chaque matin, il publie un briefing dans le canal Slack du compte, indiquant ce qui a changé et ce que chaque personne doit faire ensuite, avec des brouillons adaptés à son rôle.

Tout au long de la journée, les équipes en charge des comptes utilisent le Bot dans Slack pour évaluer leur stratégie, confronter son raisonnement aux données du compte et planifier les prochaines étapes. Le Bot se souvient des décisions prises par les équipes et bâtit un contexte riche au fil du temps. Lorsque des personnes arrivent ou quittent le compte, il devient le système de référence et peut rapidement mettre à niveau les nouveaux membres de l'équipe.

Harper, une compagnie d'assurance au service des petites entreprises, a créé un Team Bot pour identifier les clients dont les polices ont expiré et les aider à rétablir leur couverture, réduisant ainsi le travail manuel de son équipe et permettant aux clients de récupérer des économies substantielles.

**Customer Bot**
Un bot partagé pour un compte client donné. Il maintient l'AE, le CSM, le SA et le responsable des ventes alignés, publie un briefing chaque matin de semaine, et rédige le prochain geste de chaque personne.

Notre Engineering Team Bot travaille à partir du canal Slack d'un projet et se connecte à Notion, Linear, Hex, Datadog et Cursor. Il suit les décisions produit, trie les rapports de bugs, crée des tickets et lance des Cloud Agents pour traiter les correctifs bien définis.

Nous avons enseigné au Bot notre processus de mise en production via des compétences (« skills »). Il sait comment gérer les revues de pull requests, quand demander de l'aide à l'équipe, et quelles preuves un changement doit apporter avant d'être considéré comme terminé. Il coordonne le travail entre les outils et les agents, puis rend compte de l'avancement et des blocages dans Slack.

Nous avons utilisé ce dispositif pendant le développement de Team Bots. Le Bot a piloté un Cursor Project qui orchestrait des centaines de Cloud Agents, aidant une équipe de cinq personnes à livrer plus de 100 pull requests par jour et à lancer Team Bots en quelques semaines.

**EPD Teammate**
Le coordinateur du projet ou de la fonctionnalité de votre équipe EPD (Engineering, Product, Design). Il suit les canaux Slack du projet, dépose des bugs clairement documentés dans Linear, et exécute des Cursor cloud agents qui renvoient des pull requests vertes et vérifiées, afin que toute l'équipe reste synchronisée.

Les grandes équipes marketing consacrent un temps considérable à préserver la cohérence de leur marque, de leurs messages et de leur ton. Nous avons créé Marketing Bot pour faciliter ce travail.

Nous avons donné au Bot accès à notre charte de marque, à nos articles de blog et à nos textes pour les réseaux sociaux. Chaque fois que quelqu'un partage un brouillon pour approbation dans Slack, il évalue le travail au regard de notre ton et de nos derniers messages. Les équipes régionales peuvent ainsi obtenir des retours et avancer selon leur propre fuseau horaire, sans attendre un cycle de validation au siège.

Pour les modifications du site web et du référencement (SEO), Marketing Bot prend en charge le travail, de la relecture jusqu'à la mise en ligne. Une fois qu'une mise à jour de contenu passe la relecture, le Bot effectue la modification et publie un lien de prévisualisation dans Slack pour validation finale. Toute personne de l'équipe marketing peut ainsi déployer des mises à jour du site sans ouvrir de ticket ni attendre l'ingénierie, et chaque changement passe par les mêmes vérifications de marque et de SEO.

**Marketing Bot**
Maintient votre équipe marketing fidèle à la marque. Il évalue tout support au regard de votre charte de marque et de vos derniers messages, et prend en charge les changements approuvés du site web et du SEO, de la relecture jusqu'à la prévisualisation et la validation, afin que chaque région puisse publier selon son propre calendrier.

Notre équipe d'analyse de données reçoit chaque jour des dizaines de demandes d'analyses ponctuelles. Elle a créé Data Bot afin que n'importe qui chez SpaceXAI puisse obtenir des réponses sans attendre un analyste ou sans avoir à configurer un accès à l'entrepôt de données.

Data Bot utilise des identifiants partagés, en lecture seule, pour interroger les tables approuvées dans Databricks. Il se connecte également à Datadog, Hex et Statsig pour investiguer les questions et présenter les résultats.

L'équipe d'analyse de données avait déjà passé deux ans à constituer une bibliothèque de compétences pour travailler avec plus de 45 000 tables. Elle a transmis cette bibliothèque existante à Data Bot, avec notamment des instructions pour trouver les bonnes données, analyser l'utilisation des fonctionnalités à des fins de détection de fraude, respecter les standards graphiques de SpaceXAI, et mettre à jour en toute sécurité les tableaux de bord utilisés dans toute l'entreprise. Data Bot se souvient également des corrections apportées à ses requêtes, si bien que ce qu'il apprend d'une personne améliore les réponses qu'il donne à tout le monde.

**Data Bot**
Répond aux questions ponctuelles de votre équipe sur les données de votre entrepôt, avec des requêtes en lecture seule, des définitions de métriques claires et des graphiques. Il se souvient de chaque correction et confirmation, si bien que les réponses s'améliorent pour tout le monde au fil du temps.

Team Bots est disponible dès aujourd'hui en bêta publique sur les forfaits Teams et Enterprise. Prenez vos Grok Bots favoris et partagez-les avec votre équipe. Pour commencer, essayez l'un de nos Team Bots préconfigurés pour les ventes, la gestion de produit, le marketing ou l'analyse de données.

## Pourquoi ça compte
Ce lancement illustre une tendance de fond dans l'IA d'entreprise : le passage d'assistants individuels à des agents collectifs dotés de mémoire et de compétences partagées, intégrés directement dans les outils de collaboration (Slack, Notion, Linear). C'est un signal à surveiller pour quiconque suit la concurrence entre plateformes d'agents IA en contexte professionnel (Copilot, Claude, ChatGPT Enterprise, Grok).
