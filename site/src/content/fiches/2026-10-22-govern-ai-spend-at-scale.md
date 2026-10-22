---
title: "Govern AI Spend at Scale"
date: 2026-10-22
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Flinks.tldrnewsletter.com%2FF6MB03/1/010001a15ea72207-c55650dd-9a27-41e4-97cb-6d1d5a6b04bc-000000/VjKfVTbZtnLQfN6eWtsiJzrQGTetsz-83VvpWb6zJUc=452"
authors: ["Matei Zaharia", "Kasey Uhlenhuth"]
keywords: ["gouvernance IA", "FinOps", "Databricks", "Unity Gateway", "agents IA", "coûts cloud"]
theme: "Data"
tone: "news"
used_in: ["2026-10-22"]
---

## Résumé
Cette page présente un webinaire de Databricks consacré à la gouvernance des dépenses liées à l'IA à grande échelle, autour de deux outils : Unity Gateway, le plan de contrôle IA de l'entreprise, et Omnigent, son méta-harnais open-source pour agents de codage. Le contenu met en avant une approche en trois temps — « voir, montrer, agir » — pour piloter les coûts sans brider la productivité des développeurs, illustrée par une démonstration où Databricks a réduit ses propres coûts d'agents de codage d'environ 50 % sans perte de qualité. La fiche détaille aussi cinq leçons tirées de l'expérience interne de Databricks pour gérer les coûts IA.

## Points clés
- Unity Gateway centralise visibilité, budgets, routage de modèles et gouvernance des accès pour tout modèle, agent ou serveur MCP.
- Omnigent route les tâches vers le harnais d'agent de codage le plus adapté et permet d'appliquer des politiques de dépense par agent/sous-agent.
- Databricks a réduit ses coûts d'agents de codage d'environ 50 % en interne, sans compromis sur la qualité.
- Le concept de « tokenmaxxing » (surconsommation de tokens sans valeur ajoutée) est identifié comme un problème répandu, à remplacer par du « valuemaxxing ».
- Les politiques contextuelles et sensibles à la session sont présentées comme plus efficaces que les plafonds de dépense génériques pour prévenir les abus (ex. exfiltration de données).
- Plus d'un quadrillion de tokens ont été traités via Unity Gateway en un an, utilisé par des milliers de clients.

## Analyse approfondie
WEBINAIRE

# Comment gouverner les dépenses IA à grande échelle

Databricks gouverne les dépenses IA à grande échelle grâce à un modèle opérationnel piloté par la donnée. Unity Gateway, le plan de contrôle IA d'entreprise de Databricks, offre une visibilité centralisée, des contrôles budgétaires et une application de politiques contextuelles across les modèles et les agents. Omnigent, le méta-harnais open-source de Databricks, route les tâches vers le harnais d'agent de codage approprié et permet aux équipes d'appliquer des politiques de dépense à des agents individuels et à des sous-agents.

Unity Gateway aide à réduire les coûts IA tout en préservant la productivité des développeurs grâce à trois principes : **voir, montrer, agir**.

- **Visibilité centralisée :** connectez n'importe quel modèle, agent ou serveur MCP à la gateway, quel que soit le fournisseur. Suivez l'usage, la performance et le coût dans un tableau de bord unifié.
- **Budgets et plafonds de dépense en temps réel :** définissez des budgets par utilisateur ou par équipe qui se mettent à jour au fur et à mesure que les tokens sont consommés. Les ingénieurs peuvent visualiser leur propre consommation via la CLI d'Unity Gateway et mieux comprendre leur usage.
- **Routage intelligent des modèles :** faites correspondre automatiquement la complexité de la tâche au bon modèle et au bon harnais. De nombreuses requêtes peuvent être traitées sans recourir au modèle le plus coûteux.
- **Observabilité et traçabilité IA unifiées :** journalisez chaque requête avec son contexte complet dans des tables Unity Catalog gouvernées, incluant qui a fait la requête, quel modèle l'a traitée, combien de tokens elle a consommés et son coût.
- **Gouvernance Unity Catalog :** gouvernez les modèles IA, fournisseurs, agents et skills comme des objets avec des permissions fines. Cela étend le même cadre que celui déjà utilisé par votre équipe data.
- **Politiques contextuelles :** appliquez des garde-fous dynamiques et à état qui s'adaptent aux événements survenant pendant une session d'agent. Les politiques peuvent répondre au contexte de session en complément des règles statiques d'autorisation et de refus.

Regardez le webinaire pour voir ces capacités fonctionner ensemble dans une démonstration en direct. La démo montre notamment comment Databricks a réduit ses propres coûts d'agents de codage d'environ 50 % sans compromettre la qualité.

### Ce que vous allez apprendre dans ce webinaire

- Comment le CTO de Databricks **Matei Zaharia** et la Directrice Produit **Kasey Uhlenhuth** gouvernent les dépenses IA pour plus de 10 000 employés, et comment Unity Gateway apporte la même approche à votre organisation.
- Pourquoi les plafonds de dépense bruts et les politiques générales se retournent contre vous, et comment concevoir des contrôles plus efficaces.
- Le cadre **« voir, montrer, agir »** pour une gouvernance IA pilotée par la donnée.
- Comment Databricks a benchmarké des tâches de codage réelles pour identifier où les agents gaspillent le plus d'argent, et ce que les résultats ont révélé.
- Ce qu'est le **tokenmaxxing**, pourquoi il est répandu, et comment évoluer vers le **valuemaxxing**.
- Comment les **politiques contextuelles** adaptent l'application des règles aux données de session, aidant à prévenir l'exfiltration de données tout en permettant le travail légitime.
- Comment **Omnigent** orchestre plusieurs agents de codage et route automatiquement les tâches vers le bon modèle.

### À qui s'adresse ce contenu

- **CIO et dirigeants IT** gérant des portefeuilles IA en croissance qui ont besoin d'une vue unifiée des dépenses, de l'usage et des risques across les modèles et fournisseurs.
- **Équipes FinOps** qui étendent la discipline de coût cloud aux charges de travail IA, où la tarification au token et les agents autonomes mettent à l'épreuve les outils traditionnels.
- **Équipes plateforme et ingénierie** opérant des gateways de modèles qui doivent fournir un accès IA gouverné sans ralentir les développeurs.
- **Responsables sécurité et conformité** qui ont besoin de pistes d'audit, de politiques d'accès sensibles aux données, et de garde-fous qui s'adaptent à ce qu'un agent a vu pendant une session.

### Qu'est-ce qu'Unity Gateway ?

Unity Gateway est le plan de contrôle IA d'entreprise de Databricks. Il réunit FinOps, observabilité, permissions, routage, application de politiques et gestion des identités dans une couche unique qui se connecte à n'importe quel modèle, agent, serveur MCP ou skill.

Unity Gateway est disponible en version générale et déjà utilisé par des milliers de clients, avec plus d'un quadrillion de tokens traités via la gateway au cours de l'année passée.

### Qu'est-ce qu'Omnigent ?

Omnigent est le méta-harnais open-source de Databricks pour les agents de codage. Il fournit une couche commune across les harnais d'agents existants, permettant aux équipes de les combiner et de passer de l'un à l'autre pour différentes tâches plutôt que d'être enfermées dans une seule option.

Omnigent aide les équipes à gouverner le travail agentique de deux façons :

- **Routage intelligent :** diriger les requêtes simples vers des modèles plus économiques et les tâches complexes vers des modèles ou harnais plus capables.
- **Politiques de dépense :** fixer des limites pour des agents et sous-agents individuels, avec des notifications lorsqu'ils atteignent un seuil de dépense défini.

### 5 leçons pour gérer les coûts IA

- **Commencez par la visibilité :** on ne peut pas gérer ce qu'on ne voit pas. Centralisez l'instrumentation de l'usage et des coûts avant d'introduire des restrictions.
- **Mettez la visibilité des dépenses entre les mains des utilisateurs :** montrer les dépenses aux personnes qui les génèrent peut changer les comportements plus vite que l'imposition de plafonds descendants. Chez Databricks, la visibilité en temps réel dans les outils déjà utilisés par les ingénieurs s'est révélée plus efficace que de s'appuyer sur une seule limite mensuelle.
- **Benchmarkez le travail réel :** avant de supposer qu'un modèle plus grand ou un réglage à plus haut effort apportera plus de valeur, testez-le sur vos propres tâches. Les benchmarks internes de Databricks ont montré qu'un harnais plus simple et moins coûteux égalait ou dépassait la précision de la configuration par défaut.
- **Adaptez les contrôles au risque :** des contrôles bruts peuvent créer de la friction sans traiter le risque sous-jacent. Des politiques contextuelles, sensibles à la session, et des budgets par tâche peuvent distinguer les besoins légitimes des comportements problématiques plus efficacement que des plafonds de dépense uniformes ou des interdictions générales d'action.
- **Routez selon la complexité de la tâche :** un routage intelligent entre modèles ou harnais économiques et plus capables peut réduire les dépenses sans ralentir les équipes. La clé est d'adapter le routage à la complexité de la tâche plutôt que d'appliquer un réglage par défaut unique pour tous les cas.

### Ressources recommandées

## Intervenants

Matei Zaharia

Co-fondateur et CTO

Databricks

Kasey Uhlenhuth

Directrice Produit

Databricks

## Pourquoi ça compte
Ce contenu illustre une tendance de fond pour les organisations qui déploient des agents IA à grande échelle : le passage d'une consommation non maîtrisée de tokens à une gouvernance FinOps structurée, avec visibilité, routage intelligent et politiques contextuelles comme leviers concrets de réduction des coûts.
