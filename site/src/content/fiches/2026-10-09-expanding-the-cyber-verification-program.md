---
title: "Expanding the Cyber Verification Program"
date: 2026-10-09
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.anthropic.com%2Fnews%2Fcyber-verification-program%3Futm_source=tldrit/1/010001a11b7250a7-b7916d03-b70d-47ff-a4c5-2d892d3249b6-000000/1mzIvrj2rIAJJSpL0CjYSmHVU3hglumItTVhiwwv9VU=452"
keywords: ["cybersécurité", "Claude", "vulnérabilités", "red team", "vérification d'identité", "sécurité offensive"]
theme: "Sécurité"
tone: "news"
used_in: ["2026-10-09"]
---

## Résumé

Anthropic annonce l'extension de son Cyber Verification Program (CVP), qui donne aux professionnels de la sécurité vérifiés un accès à des capacités cyber avancées de Claude avec des garde-fous (classifieurs de blocage) assouplis. Le programme fusionne désormais deux initiatives précédentes (Project Glasswing et l'ancien CVP) en trois paliers d'accès — Defense Access, Red Team Access et Specialized Access — correspondant à des usages et des niveaux de vérification croissants. Anthropic présente des tests internes (CyScenarioBench) montrant l'efficacité différenciée des garde-fous selon les paliers, ainsi que des résultats chiffrés de Project Glasswing : plus de 129 000 vulnérabilités logicielles identifiées par des partenaires entre avril et juillet 2026, et 5 500 supplémentaires via les propres efforts de scan open-source d'Anthropic.

## Points clés

- Trois nouveaux paliers d'accès : **Defense Access** (défense, SOC, réponse à incident, rétro-ingénierie de malware), **Red Team Access** (pentest et red teaming autorisés, réservé aux organisations), et **Specialized Access** (quasi sans restriction, réservé à un nombre limité d'organisations vérifiées en lien avec le gouvernement américain, pour les systèmes critiques comme les réseaux électriques ou les systèmes de vol).
- Les modèles grand public (Claude Opus 5.5, Sonnet 5.5, Fable 5.1) conservent des garde-fous cyber conservateurs par défaut, car les capacités offensives et défensives sont intrinsèquement duales.
- Test interne CyScenarioBench : sans CVP, 100 % des tâches sont bloquées dès le premier prompt ; en palier Defense Access, 46 tâches sur 50 restent bloquées à un moment donné ; en palier Red Team Access, aucun blocage et un taux de réussite de 34/50 (proche du taux sans aucun garde-fou, 67,6 %).
- Project Glasswing a permis d'identifier au moins 129 000 vulnérabilités vérifiées (avril-juillet 2026) chez les partenaires, plus 5 500 via les scans open-source propres d'Anthropic ; plus de 33 000 sont classées critiques ou de sévérité élevée, et ce chiffre est jugé probablement sous-estimé (potentiellement x5).
- La conservation des données est obligatoire pour les organisations du programme (pour surveiller les usages malveillants), en attendant la solution Enterprise Frontier Safeguards (EFS) prévue à l'automne, qui combinera confidentialité « zero data retention » et garde-fous robustes.
- Le CVP est disponible sur la Claude Platform, Google Cloud Vertex AI et Microsoft Foundry ; sur Amazon Bedrock, il n'est accessible qu'aux clients éligibles à l'EFS.

## Analyse approfondie

### Extension du Cyber Verification Program

Anthropic lance une version élargie de son Cyber Verification Program (CVP), qui rend disponibles des capacités cyber avancées et des classifieurs de blocage réduits aux professionnels de la sécurité qualifiés. Le programme comprend désormais trois paliers d'accès, permettant aux équipes de sécurité de demander le niveau correspondant le mieux à leurs besoins. Chaque palier donne accès aux modèles les plus capables d'Anthropic, dont Claude Opus 5.5, Claude Sonnet 5.5, Claude Mythos 5.1, et les futurs modèles à venir.

La cybersécurité est par nature à double usage : les capacités qui permettent à une équipe de sécurité de trouver et corriger une vulnérabilité peuvent tout autant permettre à un acteur malveillant de l'exploiter. C'est pourquoi les modèles disponibles au grand public (Opus 5.5, Fable 5.1, Sonnet 5.5) appliquent des garde-fous cyber conservateurs qui bloquent la majorité des tâches offensives, afin de limiter les usages malveillants, tout en travaillant à réduire les faux positifs pour le code sécurisé légitime.

Mais les défenseurs ont eux aussi besoin d'accéder aux outils les plus puissants pour sécuriser leurs systèmes. Depuis six mois, Anthropic donnait un accès de confiance via deux programmes distincts : Project Glasswing, qui donnait à un groupe d'organisations protégeant les logiciels les plus critiques un accès à Claude Mythos ; et l'ancien CVP, qui donnait à des équipes de sécurité vérifiées un accès à des garde-fous réduits sur Opus et Sonnet. Ces deux programmes sont désormais fusionnés en une offre élargie unique, destinée à toucher davantage d'organisations de sécurité.

### Les nouveaux paliers d'accès

Chaque palier correspond à un périmètre de travail cyber spécifique, avec ses propres exigences de vérification et contrôles de sécurité.

**Defense Access** couvre le travail défensif : opérations de centre de sécurité (SOC), réponse à incident, rétro-ingénierie de malware, analyse et validation de vulnérabilités. Les organisations éligibles incluent les équipes de sécurité d'entreprises, d'associations, d'universités et d'organismes publics défendant leurs propres systèmes ; les opérateurs d'infrastructures critiques de toute taille (hôpitaux régionaux, services publics municipaux) ; les petites sociétés de sécurité ; les mainteneurs open-source ; et les chercheurs indépendants ayant un historique de signalement de vulnérabilités. Anthropic s'attend à ce que beaucoup d'organisations défensives soient éligibles à ce palier, avec un délai de réponse visé de quelques jours.

**Red Team Access** ajoute aux usages défensifs ci-dessus le pentesting et le red teaming autorisés. Sont concernés les équipes red team internes, les red teams gouvernementales, et les sociétés de sécurité/pentest. Ces organisations ne peuvent mener des tests offensifs que contre des systèmes qu'elles sont explicitement autorisées à tester, y compris des systèmes informatiques d'industries critiques. Des blocages en temps réel subsistent pour les actions pouvant causer un dommage physique ou une perturbation massive, comme le déploiement de ransomware, l'endommagement de systèmes physiques, ou le pentest de systèmes de sécurité à haut risque. En raison d'exigences d'éligibilité et de contrôles de sécurité renforcés, Anthropic prévoit un délai d'examen de quelques semaines pour ce palier ; les organisations éligibles sont placées en Defense Access pendant l'examen de leur candidature Red Team Access. Ce palier est actuellement réservé aux organisations, les chercheurs individuels n'y étant pas éligibles.

**Specialized Access**, qui comporte le moins de restrictions cyber, est réservé à un nombre limité d'organisations vérifiées autorisées à tester des systèmes de sécurité pouvant affecter des vies humaines ou perturber des marchés : systèmes de pilotage aérien, réseaux électriques, réseaux télécoms, infrastructures interbancaires, réseaux administratifs gouvernementaux. Pour ce palier, chaque organisation est examinée en profondeur en collaboration avec le gouvernement américain. Les membres existants de Project Glasswing basculent automatiquement vers ce palier, sans nouvelle validation nécessaire pour les modèles actuels.

Les modèles grand public restent utilisables pour des tâches comme la revue de code, le correctif de problèmes connus, la recherche de vulnérabilités dans du code source possédé par l'utilisateur, et le tri des alertes de sécurité.

La conservation des données est obligatoire pour les organisations inscrites au programme, afin de permettre la surveillance des usages malveillants. Une fois disponible cet automne, Enterprise Frontier Safeguards (EFS) — une nouvelle solution combinant la confidentialité du « zero data retention » avec des garde-fous robustes — permettra aux organisations éligibles de stocker leurs données dans une infrastructure cloud qu'elles contrôlent. En attendant l'EFS, les organisations ayant déjà accès à Claude Fable 5.1 ou Claude Mythos 5.1 en zero data retention peuvent aussi utiliser le CVP en zero data retention. Un formulaire permet de s'inscrire pour être tenu informé de l'arrivée de l'EFS.

### Mesurer l'efficacité des paliers

Pour évaluer l'efficacité des protections de chaque palier, Anthropic a fait passer Claude Opus 5.5 au test CyScenarioBench — une évaluation mesurant la capacité d'un modèle à planifier et exécuter des opérations cyber multi-étapes dans des conditions réalistes — avec les garde-fous propres à chaque palier CVP. S'agissant de scénarios offensifs complexes et interactifs, Anthropic attendait des blocages significatifs à la fois sur le modèle grand public et sur le palier Defense Access, et aucun blocage sur les paliers Red Team Access et Specialized Access.

Sur cinq tentatives pour chacun des 10 défis CyScenarioBench, par palier :
- Sans accès CVP, chaque tâche a été bloquée dès le premier prompt ;
- En palier Defense Access, 46 des 50 essais ont été bloqués à un moment donné, les 4 tâches restantes ayant réussi ;
- En palier Red Team Access, aucun blocage ne s'est produit, et Claude Opus 5.5 a réussi 34 des 50 tâches — un résultat équivalent au taux de réussite de 67,6 % obtenu par le modèle sans aucun garde-fou (représentatif du palier Specialized Access).

Ces résultats donnent à Anthropic la confiance nécessaire pour rendre des capacités cyber avancées disponibles en toute sécurité à un plus grand nombre de défenseurs, en élargissant les efforts défensifs initiés avec Project Glasswing. L'entreprise indique continuer à affiner ses classifieurs par palier au fil du temps.

### Donner l'avantage aux défenseurs

Via Project Glasswing, Anthropic a constaté que les modèles Claude Mythos augmentaient significativement la vitesse à laquelle les organisations identifiaient des vulnérabilités dans leurs systèmes. Grâce au programme, les partenaires ont découvert au moins 129 000 vulnérabilités logicielles vérifiées entre avril et juillet 2026. Par ses propres efforts de scan open-source, Anthropic a identifié 5 500 vulnérabilités vérifiées additionnelles entre avril et octobre 2026. Sur l'ensemble de ces vulnérabilités vérifiées, plus de 33 000 ont jusqu'ici été classées critiques ou de sévérité élevée. Ce chiffre est probablement sous-estimé, car il repose sur des données déclaratives d'un sous-ensemble seulement des partenaires de Glasswing ; Anthropic estime que l'impact réel pourrait être au moins cinq fois supérieur.

Interrogés sur le temps qu'il leur aurait fallu pour trouver le même nombre de vulnérabilités sans Claude Mythos, plusieurs partenaires ont indiqué que les modèles avaient accéléré leur rythme de découverte de vulnérabilités de plusieurs mois, voire plusieurs années. Des témoignages de partenaires de Booz Allen et Comcast sont disponibles sur le sujet.

Les changements apportés aujourd'hui au Cyber Verification Program visent à étendre l'impact de Project Glasswing à un bien plus grand nombre de défenseurs cyber. Anthropic poursuit également ses efforts pour sécuriser les logiciels open-source et les infrastructures critiques, et prévoit de partager prochainement davantage d'informations sur ces travaux.

### Candidater au programme

Les organisations intéressées peuvent candidater au CVP via un formulaire dédié. Dans le cadre du processus, Anthropic vérifie tous les candidats et demande une preuve des contrôles de sécurité requis pour le palier concerné. Les membres existants du CVP conservent leurs paramètres actuels pour les modèles précédents et seront automatiquement évalués pour un accès à Claude Opus 5.5, Claude Sonnet 5.5 et Claude Mythos 5.1 dans le cadre du programme mis à jour. Les administrateurs devront attribuer l'accès à des espaces de travail spécifiques en suivant une procédure documentée.

Le CVP est disponible sur la Claude Platform, sur Vertex AI de Google Cloud, et sur Microsoft Foundry. Sur Amazon Bedrock, il n'est disponible que pour les clients éligibles à l'Enterprise Frontier Safeguards. Les utilisateurs bloqués sur un travail qu'ils estiment couvert par leur palier peuvent le signaler ; le détail complet de chaque palier est disponible dans le centre d'aide d'Anthropic.

## Pourquoi ça compte

Ce mouvement illustre comment les éditeurs de modèles d'IA ajustent finement leurs garde-fous pour arbitrer entre la sécurité offensive/défensive à grande échelle (dual-use) ; à suivre pour la veille sur la gouvernance des capacités IA sensibles et sur l'évolution du marché de la cybersécurité assistée par IA.
