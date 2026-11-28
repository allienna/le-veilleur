---
title: "KubeCon + CloudNativeCon North America 2026: What we heard in Salt Lake City"
date: 2026-11-28
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fblog.nginx.org%2Fblog%2Fkubecon-cloudnativecon-north-america-2026-what-we-heard-in-salt-lake-city%3Futm_source=tldrit/1/010001a21d298e49-cc7c0e04-ed0d-4062-83ed-9b77549e5e84-000000/9wTrMY0R6LPhTJgs01cMhaU6Ze_QRbO2iQjQfIe5DzY=452"
keywords: ["Kubernetes", "Gateway API", "MCP", "Ingress", "Intelligence artificielle", "NGINX"]
theme: "Software"
tone: "news"
used_in: ["2026-11-28"]
---

## Résumé
Ce billet de NGINX/F5 revient sur KubeCon + CloudNativeCon North America 2026, qui s'est tenu à Salt Lake City jusqu'au 12 novembre, et où l'IA sur Kubernetes (routage d'inférence, passerelles IA, MCP, sandboxing d'agents) a dominé les échanges, des keynotes aux couloirs. Huit mois après la retraite du projet Ingress-NGINX, de nombreuses équipes n'ont toujours pas migré, alimentant un débat récurrent entre Ingress API et Gateway API ainsi qu'une forte affluence sur les sessions consacrées à ce sujet. F5 y a présenté des démonstrations de sécurisation du trafic MCP et de l'inférence IA via NGINX, ainsi qu'un rapport SlashData montrant que seules 38% des entreprises atteignent un niveau « enterprise-grade » sur Kubernetes, avec des lacunes marquées en observabilité et en gouvernance du trafic agentique. L'article souligne enfin l'explosion des CVE découvertes grâce à l'IA, qui pousse les éditeurs open source à revoir leurs cycles de correctifs.

## Points clés
- La migration hors d'Ingress-NGINX (project retiré en mars 2026, sans plus de releases ni de patchs de sécurité) reste largement inachevée huit mois après ; NGINX Ingress Controller et NGINX Gateway Fabric proposent des outils dédiés (mapping de plus de 130 annotations, outil ingress2gateway) pour basculer respectivement vers l'Ingress API ou la Gateway API.
- Le choix entre Ingress API (stable, spec figée depuis 2020, routage simple) et Gateway API (plus récente, orientée rôles, support HTTP/gRPC/TCP/UDP, extension dédiée à l'inférence IA) dépend surtout du besoin de portabilité et de séparation des responsabilités entre équipes plateforme et applicatives.
- Les discussions sur l'IA se sont concentrées sur les contrôles au niveau de la passerelle : routage par modèle, suivi des coûts et des tokens, authentification des agents, et application de politiques as-code (comme les patterns Kyverno présentés pour la Gateway API Inference Extension).
- Une démonstration NGINX a montré comment sécuriser le trafic MCP (authentification, quotas par outil, détection des échecs d'outils masqués derrière des réponses HTTP 200) sans nécessiter de cluster Kubernetes.
- Le rapport SlashData, basé sur 445 entreprises, montre que seules 38% des organisations atteignent un niveau « enterprise-grade » sur Kubernetes ; l'observabilité est le domaine le plus faible, et seulement 43% des entreprises inspectent le trafic agent/MCP malgré la montée en puissance de l'IA en production.
- La découverte de vulnérabilités assistée par IA a fait bondir le nombre de CVE en 2026 (37 contre seulement 2 en 2025 pour NGINX), poussant F5 à utiliser l'IA en interne pour corriger ses propres failles avant publication, avec un second modèle chargé de limiter les faux positifs.

## Analyse approfondie

### Un salon dominé par l'IA et la question d'Ingress
KubeCon + CloudNativeCon North America s'est terminé le 12 novembre à Salt Lake City. L'équipe NGINX remercie les visiteurs de son stand et les participants à ses sessions, ainsi que Nutanix, Red Hat et vCluster pour leurs « lightning talks » communs. Comme attendu, l'IA sur Kubernetes a traversé tout l'événement : routage d'inférence, passerelles IA, runtimes d'agents, Model Context Protocol (MCP) et sandboxing d'agents revenaient partout, des keynotes aux conversations informelles. Le sujet d'Ingress est revenu presque aussi souvent, de nombreuses équipes cherchant encore quelle solution adopter depuis la mise à la retraite d'Ingress-NGINX.

### La migration d'Ingress-NGINX reste en cours
Le projet communautaire Ingress-NGINX a été retiré en mars 2026 : plus de releases, plus de correctifs, plus de patchs de sécurité (voir l'annonce officielle sur le blog Kubernetes). Huit mois plus tard, l'équipe NGINX dit avoir été surprise du nombre d'équipes qui l'utilisent encore. Les sessions sur cette retraite et sur la Gateway API ont attiré parmi les plus grandes foules de la semaine, et le stand s'est rempli après le lightning talk consacré au chemin de migration le moins risqué.

Les noms se confondent facilement : Ingress-NGINX était un projet communautaire Kubernetes maintenu par le SIG Network, tandis que F5 maintient NGINX Open Source et NGINX Ingress Controller, une base de code distincte avec des releases depuis novembre 2016. La retraite d'Ingress-NGINX n'affecte ni l'un ni l'autre.

Pour les équipes qui planifient encore leur migration, deux chemins reviennent sans cesse :
- Conserver ses ressources Ingress et basculer vers NGINX Ingress Controller : l'outil de migration disponible sur kubernetes.nginx.org convertit plus de 130 annotations Ingress-NGINX, ainsi que les réglages de ConfigMap.
- Basculer vers la Gateway API avec NGINX Gateway Fabric : l'outil ingress2gateway convertit les ressources Ingress en ressources Gateway API, et son nouvel « émetteur » NGINX ajoute les politiques NGINX Gateway Fabric pour les réglages non couverts par la Gateway API.

kubernetes.nginx.org propose également des outils de migration pour le HAProxy Kubernetes Ingress Controller, et en version bêta pour Traefik Proxy.

### Ingress API ou Gateway API : comment choisir
La question « quelle API utiliser ? » est revenue fréquemment. Voici la version condensée de la présentation sur stand d'Alessandro Fael Garcia, intitulée « Ingress API or Gateway API : A decision guide for Kubernetes traffic ».

L'Ingress API est stable depuis 2020 et sa spécification est figée. Ses fonctionnalités avancées passent par des annotations propres à chaque éditeur et des ressources personnalisées, ce qui rend les configurations peu portables d'un contrôleur à l'autre. Elle reste adaptée :
- aux environnements de production historiques qui l'utilisent déjà ;
- aux nouveaux environnements de production où la stabilité à long terme prime ;
- au routage simple par hôte et par chemin.

La Gateway API, plus récente et organisée par rôles, est encore en développement actif. Elle prend en charge HTTP, gRPC, TCP et UDP, répartit la configuration entre opérateurs de cluster et développeurs d'applications, et standardise des fonctionnalités (comme le découpage de trafic) qu'Ingress ne gère que via des annotations. Elle est à privilégier pour :
- les nouveaux projets ;
- les clusters multi-tenants où les équipes plateforme et applicatives doivent avoir des rôles distincts ;
- les configurations que l'on souhaite garder portables entre différentes implémentations ;
- les charges de travail IA, via la Gateway API Inference Extension (voir le guide de NGINX Gateway Fabric).

Dans les deux cas, NGINX propose une implémentation : NGINX Ingress Controller pour l'Ingress API, et NGINX Gateway Fabric, pleinement conforme à la spécification Gateway API. En cas de doute, l'équipe renvoie vers le forum communautaire NGINX.

### Le trafic IA s'intègre à la passerelle
La majorité des échanges sur l'IA portaient sur des contrôles situés au niveau de la passerelle : routage des requêtes par modèle, suivi des tokens et des coûts d'inférence, authentification des agents et audit de leurs actions. Les équipes souhaitent aussi pouvoir écrire des politiques pour le trafic IA avec les mêmes outils de policy-as-code déjà utilisés pour le reste du cluster.

Les agents étaient omniprésents. Google a fait don d'Agent Substrate, un runtime pour agents IA sandboxés sur Kubernetes, à la CNCF en tant que projet Sandbox, un sujet largement discuté sur le salon.

Les trois sessions animées par NGINX portaient toutes sur l'IA. Le lundi, Scott McAllister a participé au panel « DevRel Unfiltered : What Developers Actually Build with Agents (and What Breaks) » lors du Distributed SQL Summit (événement co-localisé), pour discuter de ce que les développeurs construisent avec des agents et des points de rupture observés en production.

Le mardi, lors de KyvernoCon, Ciara Stacke et Alessandro Fael Garcia ont présenté « Who's Governing the GPU Lane? Policy as Code for AI Inference Traffic in Kubernetes ». Ils ont montré des patterns de politiques appliquées à l'admission pour les ressources de la Gateway API Inference Extension : isolation des tenants, failover sécurisé, contrôle d'accès aux modèles et routage GPU sensible aux coûts. Ces patterns fonctionnent avec n'importe quelle implémentation de Gateway API et n'importe quel moteur de politiques. L'enregistrement est disponible, ainsi qu'une démo exécutable depuis le dépôt nginx/nginx-demos, basée sur un cluster kind local et des modèles simulés, donc exécutable sur un simple laptop sans GPU.

Kyverno a aussi été évoqué sur le stand : après sa session KubeCon, Aurélie Vache est venue dédicacer son livre *Understanding Kyverno in a visual way*, et tous les exemplaires disponibles ont été distribués.

Le jeudi, Micheal Kingston et Ciara Stacke ont présenté « HTTP 200, Tool Failed: Taming MCP Agent Traffic with NGINX » au Demo Theater. Chaque appel d'outil MCP ressemble au même appel JSON-RPC POST vers /mcp, et un outil en échec peut malgré tout renvoyer un code HTTP 200. Dans la démo, NGINX Open Source se place devant un serveur MCP, authentifie chaque client et lit chaque requête pour identifier l'outil appelé, ce qui permet d'appliquer un contrôle d'accès par rôle et des limites de débit par outil. Il détecte aussi les échecs d'outils masqués dans des réponses 200 et les affiche dans Grafana. Cette démo, baptisée MCP Gateway Mission Control, est disponible dans le dépôt nginx/nginx-demos et fonctionne avec Docker Compose, sans besoin de cluster Kubernetes ; la détection des échecs d'outils provient du projet nginx/nginx-mcp-js, qui propose d'autres recettes et exemples exécutables.

Les démonstrations sur le stand ajoutaient également la sécurité F5 à NGINX Gateway Fabric : avec F5 AI Guardrails, NGINX Gateway Fabric envoie les prompts LLM pour inspection avant qu'ils n'atteignent le modèle, et les réponses avant qu'elles n'atteignent le client, bloquant ce que les politiques n'autorisent pas. F5 WAF for NGINX applique quant à lui des politiques WAF aux Gateways et aux routes. La documentation de NGINX Gateway Fabric couvre les deux cas (sécurisation du trafic LLM avec F5 AI Guardrails, et aperçu de F5 WAF for NGINX). F5 BIG-IP Next for Kubernetes disposait aussi de ses propres démonstrations.

### Kubernetes « enterprise-grade » : ce que disent les chiffres
Un des thèmes mis en avant par NGINX était le Kubernetes « enterprise-grade » : faire fonctionner chaque cluster comme un patrimoine gouverné de manière unifiée, avec une équipe plateforme qui l'opère, un responsable unique pour la sécurité et les politiques réseau, et une vue unique de la télémétrie. Le premier jour de KubeCon, F5 a publié un rapport de recherche réalisé par SlashData, *The State of Enterprise Kubernetes Strategy 2026* (PDF), dont les résultats ont été présentés par Marko Sluga et Buu Lam lors d'un lightning talk sur le stand.

SlashData a interrogé 445 entreprises de plus de 500 salariés exploitant Kubernetes en production, et a noté chacune sur 13 pratiques couvrant la gouvernance, la chaîne logistique logicielle, la résilience et l'observabilité. Selon leurs propres déclarations, 61% des entreprises appliquent à Kubernetes un standard équivalent ou supérieur au reste de leur parc IT. Mais une fois évaluées sur leurs pratiques réelles, seules 38% atteignent le niveau « enterprise-grade ». 51% sont qualifiées d'« établies, avec des lacunes », et 11% sont encore en phase de standardisation.

L'équipe NGINX en tire cinq recommandations :
- Séparer qui exploite Kubernetes de qui le gouverne. Lorsqu'une équipe de platform engineering gère Kubernetes au quotidien et qu'une équipe sécurité centrale distincte fixe les politiques, 66% des entreprises atteignent le niveau enterprise-grade, contre 32% pour toute autre organisation. Seules 19% des entreprises fonctionnent aujourd'hui ainsi.
- Exploiter Kubernetes comme une plateforme standard unique. Avec une plateforme unique à l'échelle de l'organisation, 53% des entreprises atteignent le niveau enterprise-grade, contre 25% lorsque Kubernetes reste cantonné à une seule équipe ou un seul projet. Au sommet du modèle de maturité, routage, accès et politiques de sécurité sont gérés depuis un point de contrôle unique, avec une politique de sortie (egress) commune à tous les clusters.
- Corriger la pratique manquante qui freine la progression. La moitié des entreprises (51%) obtiennent un score de 80 ou plus sur 100, mais le niveau supérieur suppose des prérequis, et 24% de ces entreprises bien notées manquent exactement une pratique clé — le plus souvent l'observabilité centralisée (36%), puis le contrôle d'admission automatisé (31%).
- Investir dans l'observabilité. C'est le domaine le plus faible des quatre : 48% atteignent le niveau supérieur, contre 67% pour la gouvernance. Seules 28% des entreprises prévoient d'y investir dans les 12 prochains mois, contre 42% pour la sécurité.
- Gouverner le trafic IA avant de faire monter en charge les agents. Parmi les entreprises qui exploitent des modèles IA, 77% les font tourner sur des clusters Kubernetes qu'elles opèrent elles-mêmes. La plupart (86%) ont étendu leur WAF et leur protection d'API à ce trafic, mais seules 43% inspectent le trafic des agents et des outils MCP.

Les autres sessions de NGINX répondaient directement à deux de ces lacunes : les patterns KyvernoCon apportent un contrôle d'admission automatisé pour les ressources d'inférence (l'un des deux prérequis les plus souvent manquants), et la démo MCP ajoute des métriques, une authentification et des limites de débit par outil aux appels d'agents, un point que seules 43% des entreprises surveillent actuellement. Le rapport complet détaille la méthodologie et les données derrière chaque résultat, et un billet de blog F5 en propose un résumé.

#### La sécurité de l'open source
La chaîne logistique logicielle constitue l'un des quatre domaines du rapport, et sur le stand, la question de l'open source est revenue souvent : comment l'industrie peut-elle suivre le rythme des correctifs de sécurité alors que de plus en plus de vulnérabilités sont découvertes ?

Les modèles d'IA de pointe trouvent désormais des vulnérabilités dans le code open source plus vite que jamais. Les déclarations de CVE ont bondi sur les principaux projets open source depuis que la découverte assistée par IA a pris son essor ce printemps, comme le montre VulnCheck dans son billet « The First CVE Wave ». NGINX n'est pas épargné : les avis de sécurité NGINX recensent déjà 37 CVE pour 2026, contre seulement deux sur l'ensemble de 2025. Les attaquants disposent des mêmes modèles, et un correctif de sécurité rendu public révèle où se trouvait la vulnérabilité, ce qui permet à un outil IA de transformer ce correctif en exploit avant que la plupart des équipes n'aient eu le temps de l'appliquer.

F5 affirme utiliser ces mêmes modèles sur son propre code, y compris NGINX Open Source, ce qui lui aurait permis de corriger toutes les CVE NGINX de l'année avant leur publication. Pour limiter les faux positifs, un second modèle est chargé de contester chaque détection, et un bug n'est qualifié de vulnérabilité qu'une fois démontré qu'un attaquant peut effectivement l'atteindre et le déclencher. Kunal Anand, Chief Product Officer de F5, détaille cette démarche dans deux billets : l'un sur la méthode de recherche de vulnérabilités en interne, l'autre sur l'accélération du rythme de publication des correctifs.

### Pour aller plus loin
- Visionner la session KyvernoCon et tester sa démo de policy-as-code ; le reste des enregistrements de la semaine est disponible sur la chaîne YouTube de la CNCF.
- Pour planifier une migration, démarrer sur kubernetes.nginx.org, qui regroupe les outils de migration et les présentations de NGINX Ingress Controller et NGINX Gateway Fabric ; pour basculer vers la Gateway API, utiliser ingress2gateway avec l'émetteur NGINX.
- Exécuter la démo MCP Gateway Mission Control sur son propre poste, puis utiliser nginx/nginx-mcp-js pour placer NGINX devant ses propres serveurs MCP.
- Adresser questions de migration, questions sur la Gateway API et demandes de fonctionnalités au forum communautaire NGINX, ou ouvrir un ticket sur les dépôts NGINX Gateway Fabric ou NGINX Ingress Controller.

L'article se termine sur une note légère : les visiteurs rentrés chez eux avec Jinx, la mascotte chat de NGINX (disponible en peluche et dans un livre pour enfants, *Jinx Takes the Helm*), ainsi que le T-shirt à motif Salt Lake City, ont visiblement apprécié ces goodies, plusieurs personnes le qualifiant de meilleur t-shirt du salon.

## Pourquoi ça compte
Ce billet offre un instantané utile pour la veille infra/cloud native : il confirme que la gouvernance du trafic IA (passerelles, MCP, policy-as-code) devient un axe central de l'écosystème Kubernetes, tout en chiffrant un retard concret des entreprises sur l'observabilité et le contrôle des agents IA en production. Il signale aussi une tendance à suivre de près : l'essor des CVE découvertes par IA, qui redéfinit l'urgence des cycles de correctifs pour les mainteneurs open source.
