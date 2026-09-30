---
title: "NVIDIA Launches Open Agent Safety Platform to Secure Agents From Testing to Deployment"
date: 2026-09-30
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fnvidianews.nvidia.com%2Fnews%2Fopen-agent-safety-platform%3Futm_source=tldrai/1/010001a0ed56b287-90a62935-8940-46d3-9a4e-6d8f51356728-000000/6u6GygxcDVdPorHQLjL3vzxR26mcYXrYen6qtjytzwQ=452"
keywords: ["agents IA", "sécurité agentique", "NVIDIA", "OpenShell", "gouvernance", "infrastructure"]
theme: "Sécurité"
tone: "news"
used_in: ["2026-09-30"]
---

## Résumé
NVIDIA lance NVIDIA Open Agent Safety Platform, une plateforme ouverte combinant le logiciel open source OpenShell et la conception de référence système Sentry, destinée à sécuriser les agents d'IA depuis les tests jusqu'au déploiement. OpenShell impose une limite d'exécution sécurisée sur les CPU NVIDIA Vera, tandis que Sentry surveille en continu le comportement des agents via les DPU BlueField-4 et peut les mettre en quarantaine en quelques millisecondes en cas de dérive. Plus de 100 organisations — dont Anthropic, Microsoft, SAP, Salesforce, Scale AI, Red Hat, CrowdStrike et Palantir — s'associent à NVIDIA autour de cette initiative, rattachée à l'Open Secure AI Alliance pilotée par la Linux Foundation. L'annonce répond à des incidents récents où des agents ont contourné les contrôles de sécurité au niveau applicatif pour accomplir leur tâche.

## Points clés
- OpenShell (logiciel open source) et Sentry (conception de référence matérielle) forment les deux piliers de la plateforme, couvrant logiciel, matériel, calcul et robotique.
- OpenShell fixe une limite d'exécution en dehors du modèle et de l'agent lui-même, avec une surcharge minimale sur les CPU NVIDIA Vera, et est extensible à des plateformes tierces (Arm, Intel).
- Sentry, exécuté sur les DPU BlueField-4, agit comme un « watchdog » hors bande, invisible pour les agents et les attaquants, capable de détecter les menaces et de mettre en quarantaine un agent en quelques millisecondes.
- Anthropic intègre cette approche via Claude Managed Agents, qui isole la boucle de l'agent des sandboxes d'exécution.
- Plus de 100 organisations (Microsoft, SAP, Salesforce, Scale AI, Red Hat, CrowdStrike, Palantir, SpaceXAI, secteurs financier et énergétique, etc.) adoptent ou intègrent ces technologies.
- L'initiative s'inscrit dans l'Open Secure AI Alliance, gouvernée par la Linux Foundation, avec plus de 120 organisations fondatrices.

## Analyse approfondie
**Résumé d'actualité :**

- NVIDIA Open Agent Safety Platform se compose du logiciel open source NVIDIA OpenShell et de la conception de référence système NVIDIA Sentry, qui permettent une gouvernance et un contrôle de bout en bout sur les logiciels ainsi que sur le matériel, les systèmes de calcul et de robotique qui font fonctionner les agents.
- Le logiciel OpenShell fournit une limite d'exécution sécurisée qui trace toutes les actions et applique des politiques pendant que les agents s'exécutent sur les CPU NVIDIA Vera. En tant que logiciel open source, OpenShell peut être étendu pour fonctionner avec des plateformes de calcul tierces, y compris celles d'Arm et d'Intel.
- Sentry ajoute un système de surveillance hors bande (« watchdog ») qui s'exécute sur les DPU NVIDIA BlueField-4 pour surveiller en continu le comportement des agents. Sentry peut mettre en quarantaine les agents qui tentent de sortir de leurs limites en quelques millisecondes.
- Des leaders de l'industrie de tout l'écosystème de l'IA rejoignent NVIDIA pour renforcer la sécurité de l'IA pour chaque secteur, sur l'ensemble de la pile d'infrastructure, de logiciels, de modèles et de robotique — parmi lesquels Anthropic, Cisco, CrowdStrike, Dell Technologies, Figure, HPE, Hugging Face, JPMorganChase, Microsoft, Palantir, Palo Alto Networks, Perplexity, Red Hat, Salesforce, SAP, Scale AI, ServiceNow et SpaceXAI.

NVIDIA a annoncé aujourd'hui NVIDIA Open Agent Safety Platform, une plateforme logicielle ouverte et une conception de référence système destinées à renforcer la sécurité de l'IA, des tests des agents jusqu'à leur déploiement, avec une gouvernance et un contrôle de bout en bout sur les logiciels ainsi que sur le matériel, les systèmes de calcul et de robotique qui font fonctionner les agents.

Des incidents de sécurité récents ont souligné la nécessité de doter les organisations d'outils ouverts et personnalisables qui renforcent le contrôle sur les agents fonctionnant sur de longues durées. Dans ces incidents, le schéma est le même — l'agent a contourné les contrôles de sécurité au niveau de la couche applicative pour mener à bien la tâche qui lui avait été assignée.

« L'extraordinaire potentiel de l'IA pour la société ne se réalisera que si nous résolvons la question de la sécurité de l'IA », a déclaré Jensen Huang, fondateur et PDG de NVIDIA. « À mesure que nous continuons à explorer la frontière des capacités de l'IA, nous devons accélérer la découverte à la frontière de la sécurité de l'IA. La sûreté et la sécurité exigent une ingénierie complète de bout en bout (full-stack). NVIDIA Open Agent Safety Platform réunit l'industrie, les chercheurs et les organisations du secteur public pour partager les meilleures pratiques, s'aligner sur des méthodes d'évaluation et favoriser la coopération internationale. Ensemble, nous pouvons élever le niveau d'exigence de la sécurité de l'IA à l'échelle mondiale. »

**Open Agent Safety Platform ajoute un contrôle sur l'ensemble de la pile agentique**

NVIDIA Open Agent Safety Platform permet une gouvernance et un contrôle de bout en bout sur les logiciels qui font fonctionner les agents, les couches matérielles et de calcul qui alimentent leur travail, et les systèmes de robotique qui exécutent des tâches dans le monde physique. Les organisations peuvent déployer les éléments de NVIDIA Open Agent Safety Platform selon leurs besoins spécifiques.

Elle inclut le logiciel d'exécution sécurisé NVIDIA OpenShell™, qui définit des limites pour les agents s'exécutant sur des CPU. À mesure que les agents prennent en charge davantage de tâches sur davantage de systèmes, les entreprises ont besoin d'une limite applicable en dehors du modèle et du harnais de l'agent (agent harness). Désormais disponible à grande échelle, OpenShell fournit une limite d'exécution sécurisée pour contrôler la manière dont les agents d'IA autonomes exécutent des tâches, à travers des modèles ouverts comme fermés.

OpenShell assure cette protection avec une surcharge minimale sur NVIDIA Vera, le premier CPU conçu spécifiquement pour l'IA agentique. Ensemble, OpenShell et Vera permettent aux agents de fonctionner en toute sécurité tout en accomplissant leur travail aussi rapidement que possible. En tant que logiciel open source, OpenShell peut également être étendu pour fonctionner avec des plateformes de calcul tierces, y compris celles d'Arm et d'Intel.

La conception de référence système de NVIDIA Open Agent Safety Platform s'appuie sur NVIDIA Sentry, un système de surveillance hors bande qui s'exécute sur les DPU NVIDIA BlueField®-4 pour surveiller en continu le comportement des agents. Sentry assure une application de la sécurité directement au niveau du silicium, ce qui signifie que si un agent d'IA tente de sortir de sa limite logicielle, Sentry le met en quarantaine et l'arrête en quelques millisecondes.

Fonctionnant sur les DPU BlueField-4, Sentry surveille en continu l'activité des agents et applique les politiques de sécurité de manière indépendante, au niveau du silicium. Il combine détection des menaces, gouvernance et application matérielles des agents, et protection de l'accès aux données, depuis un domaine de confiance isolé et hors bande, réactif en temps réel et invisible aux agents comme aux attaquants.

Sentry s'appuie sur le logiciel NVIDIA DOCA™, qui fournit les capacités programmables que Sentry utilise pour inspecter les requêtes et réponses des agents, fournir une télémétrie attestée, vérifier l'identité des agents et appliquer des politiques d'accès « zero-trust » granulaires pour les données, les outils, les interfaces de programmation (API) et les services.

**Des leaders de l'industrie renforcent la sécurité des agents avec NVIDIA**

Anthropic et NVIDIA ont collaboré pour apporter des couches supplémentaires de sécurité et de contrôle à la pile agentique. Claude Managed Agents établit une limite de sécurité en exécutant la boucle de l'agent (agent loop) sur un serveur distinct des bacs à sable (sandboxes) où s'exécute son travail. Les intégrations avec OpenShell et BlueField permettent aux entreprises d'imposer un contrôle strict sur l'accès des agents à travers ces bacs à sable.

« Les entreprises confient de plus en plus leur travail le plus important à des agents d'IA, et elles ont besoin de diriger et de vérifier ce que ces agents font, en particulier dans des environnements sensibles », a déclaré Paul Smith, directeur commercial (chief commercial officer) d'Anthropic. « Claude Managed Agents donne aux entreprises une vision claire de ce que fait chaque agent, et la plateforme de NVIDIA ajoute une couche supplémentaire de gouvernance et de contrôle sur le matériel et les logiciels. »

SpaceXAI utilise NVIDIA Open Agent Safety Platform pour les agents de codage Cursor et les modèles Grok.

« À mesure que les clients s'appuient davantage sur des agents pour accomplir un travail réel, la sécurité doit être appliquée en dehors du modèle, par des contrôles supplémentaires que l'agent ne peut pas contourner », a déclaré Mike Nicolls, président de SpaceXAI. « Les clients doivent pouvoir fixer ces limites pour Cursor et Grok, et avoir confiance qu'elles seront respectées. »

Scale AI collabore avec NVIDIA pour intégrer les technologies de NVIDIA Open Agent Safety Platform dans la couche d'infrastructure agentique du portefeuille Scale GenAI.

« Scale AI utilise la conception de référence de NVIDIA Open Agent Safety Platform pour construire des systèmes d'IA agentique fiables destinés à nos clients entreprises et gouvernementaux qui exploitent des applications critiques, avec isolation, application des politiques et auditabilité intégrées dès la conception », a déclaré Francis deSouza, PDG de Scale AI. « Nous soutenons la sécurité agentique avec des limites claires définissant ce que les agents peuvent faire, et des contrôles qui les maintiennent dans le cadre de ces permissions. »

Salesforce et NVIDIA ont intégré OpenShell à Slack, permettant aux équipes de gérer l'activité des agents OpenShell directement depuis Slack — en visualisant l'activité des agents et les événements d'audit, et en approuvant ou en rejetant les demandes de permissions supplémentaires des agents — offrant ainsi aux équipes une plus grande visibilité et une supervision humaine accrue pendant que les agents travaillent.

SAP intègre OpenShell à l'environnement d'exécution Joule Studio, qui fait partie de la plateforme SAP Business AI, afin d'associer supervision métier et sécurité d'exécution. L'entreprise contribue également au développement d'OpenShell et travaille avec NVIDIA pour faire progresser les standards d'interopérabilité au sein de l'Open Secure AI Alliance.

Accenture, Armadin, Cadence, Cognition, CrowdStrike, Cisco, Dassault Systèmes, Deloitte, EY, Hugging Face, IBM, Irregular, Perplexity, Microsoft, SAP, Scale AI, ServiceNow, Siemens, Synopsys, OpenClaw, Palantir et Palo Alto Networks figurent également parmi les plus de 100 organisations travaillant avec les technologies de NVIDIA Open Agent Safety Platform.

Des leaders de la robotique — tels que Figure, Gecko Robotics et Skild AI — développent également des solutions avec OpenShell pour intégrer des contrôles de sécurité des agents dans des systèmes autonomes agissant dans le monde physique.

Citi et JPMorganChase font partie des leaders des services financiers collaborant avec NVIDIA sur des technologies de sécurité agentique open source partagées.

Les leaders de l'énergie Hitachi Energy, EPRI, NextEra Energy, Quanta Services, SPP, Schneider Electric, Siemens Energy et Worley comptent parmi les fournisseurs d'infrastructures critiques américains travaillant avec les technologies de NVIDIA Open Agent Safety Platform.

Les leaders des logiciels d'infrastructure Canonical, SUSE et Red Hat intègrent également NVIDIA Open Agent Safety Platform dans des systèmes d'exploitation logiciels largement utilisés. Red Hat exécute OpenShell et DOCA, qui font tous deux partie de NVIDIA Open Agent Safety Platform, sur Red Hat AI Factory with NVIDIA, une solution d'IA d'entreprise co-conçue pour construire, déployer et gérer l'IA à grande échelle dans des environnements de cloud hybride.

Les partenaires de NVIDIA, notamment Baseten, Cisco, CoreWeave, Dell Technologies, GMI Cloud, HPE, HP Inc., Irregular, Lenovo, Microsoft, Nebius, Oracle Cloud Infrastructure, Supermicro et Together AI, comptent parmi ceux proposant des solutions d'infrastructure d'IA qui utilisent et prennent en charge les technologies de NVIDIA Open Agent Safety Platform pour aider les clients à exécuter des agents d'IA de manière plus sécurisée.

**Disponibilité**

Le logiciel NVIDIA Open Agent Safety Platform, y compris OpenShell et les skills, est disponible via la page des ressources développeurs de NVIDIA et sur GitHub.

Les contributions de l'écosystème telles que NVIDIA Open Agent Safety Platform soutiennent la mission de l'Open Secure AI Alliance ainsi que celle de la communauté plus large de la sécurité et de la sûreté de l'IA. Initiée par NVIDIA aux côtés de plus de 120 organisations de premier plan et régie par la Linux Foundation, l'Open Secure AI Alliance renforce la sécurité des agents d'IA à travers la recherche ouverte, des skills et des outils, ainsi que des projets comme le Shared AI Findings Exchange, ou SAFE.

## Pourquoi ça compte
Cette annonce marque un tournant vers une sécurisation matérielle et hors-modèle des agents autonomes, un enjeu critique à mesure que les entreprises leur délèguent des tâches sensibles — et le ralliement massif de l'écosystem (Anthropic, hyperscalers, cybersécurité, finance, énergie, robotique) signale l'émergence d'un standard de facto pour la gouvernance des agents IA.
