---
title: "Cisco, Palo Alto Networks, NTT rally after PHP2Shell crisis"
date: 2026-10-29
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.sdxcentral.com%2Fnews%2Fcisco-palo-alto-networks-ntt-rally-after-php2shell-crisis%2F%3Futm_source=tldrit/1/010001a18276797c-740d9479-a7ac-4f58-b887-2d3068969a39-000000/CJHf2ZS9-kA2TK1ssyQ-epIO1ewp3cQroIB_LiEwTz0=452"
keywords: ["PHP2Shell", "vulnérabilités", "cybersécurité", "patchs", "NTT", "infrastructure critique"]
theme: "Sécurité"
tone: "news"
used_in: ["2026-10-29"]
---

## Résumé
La crise mondiale de cybersécurité surnommée « PHP2Shell » continue de produire des effets en cascade, touchant notamment Palo Alto Networks, Cisco et le groupe japonais NTT. Deux vulnérabilités critiques découvertes dans PHP, le langage côté serveur qui fait tourner une grande partie du web, ont exposé un nombre considérable de sites, d'applications et de produits d'entreprise à des risques d'exécution de code malveillant et de prise de contrôle. Les éditeurs concernés publient des correctifs à des rythmes variables, tandis que des services publics japonais ont dû être suspendus par précaution. Un dirigeant de NTT souligne que ce type d'incident devient la norme à l'ère des découvertes de failles assistées par l'IA.

## Points clés
- Deux failles critiques dans PHP, découvertes par des chercheurs utilisant des modèles d'OpenAI et de Google, ont un impact radius exceptionnellement large.
- Palo Alto Networks confirme un impact de sévérité élevée sur PAN-OS (pare-feux PA-Series et VM-Series, Panorama), via l'interface de gestion HTTPS et l'API XML ; des correctifs sont déployés jusqu'au 30 octobre.
- Cisco indique que l'essentiel de ses produits réseau et sécurité n'est pas concerné, mais que certains produits (Ultra-Reliable Wireless Backhaul, gamme Expressway, Duo Access Gateway) le sont ; seul Duo Access Gateway a reçu un correctif pour l'instant.
- NTT DoCoMo a suspendu temporairement plusieurs services publics d'alerte d'urgence au Japon (J-Alert, crues, évacuations municipales), tout en maintenant les alertes séismes et tsunamis ; tout a été restauré le 25 octobre.
- NTTPC Communications a désactivé par précaution les interfaces de gestion de ses services cloud (portails clients, consoles VM, API), sans interrompre le fonctionnement des VM existantes ; un retour n'est pas attendu avant début novembre.
- La stratège en cybersécurité de NTT, Mihoko Matsubara, estime que l'IA accélère la découverte de vulnérabilités au point de submerger les équipes de défense.

## Analyse approfondie
Les retombées de la crise mondiale de cybersécurité PHP2Shell se poursuivent, touchant des acteurs de l'infrastructure comme Palo Alto Networks et Cisco, ainsi que les services de virtualisation et de télécommunications du géant japonais NTT.

Des chercheurs travaillant avec des modèles d'IA d'OpenAI et de Google ont découvert la semaine dernière des vulnérabilités critiques dans PHP, le langage de programmation côté serveur qui soutient une grande partie du web. Ces failles pouvaient exposer les serveurs vulnérables à du code malveillant, donnant potentiellement aux attaquants un accès à des informations sensibles ainsi qu'un contrôle sur les systèmes concernés. Bien que le nombre de failles critiques se limite à deux, leur rayon d'impact a couvert un ensemble considérable de sites web, d'applications et de produits d'entreprise.

Palo Alto Networks a rapidement confirmé, après la découverte, que les vulnérabilités affectaient plusieurs versions de son logiciel PAN-OS, y compris les pare-feux des gammes PA-Series et VM-Series ainsi que les systèmes de gestion Panorama. L'interface de gestion HTTPS et l'API XML étaient particulièrement exposées, l'entreprise qualifiant l'impact sur ses produits de sévérité élevée.

Palo Alto a publié la semaine dernière des correctifs pour ses services Cortex XCore SaaS et WildFire Cloud. L'éditeur a également commencé à déployer des hotfixes pour PAN-OS, les publications restantes étant prévues jusqu'au 30 octobre.

Cisco, de son côté, a confirmé que si certaines de ses familles de produits étaient concernées (Ultra-Reliable Wireless Backhaul, Expressway Series, Expressway Select Series et Duo Access Gateway), la majorité de ses produits majeurs de réseau et de sécurité n'était pas vulnérable. Plusieurs autres produits, dont certains composants SD-WAN et de cœur de réseau mobile, restaient en cours d'investigation.

L'entreprise a publié un correctif pour Duo Access Gateway, mais les patchs pour les autres produits affectés restent en attente.

### NTT et PHP2Shell

Au Japon, le géant des télécommunications NTT DoCoMo a temporairement suspendu plusieurs de ses services publics d'alerte d'urgence par précaution face aux failles PHP2Shell. Cette interruption a touché le système d'alerte national J-Alert, les prévisions de crues fluviales, ainsi que les notifications municipales de catastrophe et d'évacuation. Les alertes précoces de séismes et de tsunamis, en revanche, sont restées opérationnelles pendant toute la période de 48 heures. DoCoMo a confirmé que tous les services concernés avaient été restaurés le 25 octobre.

Une autre entité du groupe NTT, NTTPC Communications, a suspendu les interfaces de gestion de l'ensemble de ses services cloud. Cette mise à l'arrêt préventive a désactivé les portails d'administration client, les consoles de contrôle des machines virtuelles (VM) ainsi que l'API destinée aux clients. Si cela a empêché les utilisateurs de gérer leurs instances VM, les VM existantes ont continué de fonctionner normalement.

Selon ce fournisseur cloud et IT, une division de NTT DoCoMo Business, les interfaces concernées ne devraient pas être rétablies avant début novembre.

Avant même ces incidents, la stratège en chef de la cybersécurité chez NTT, Mihoko Matsubara, avait expliqué que la découverte de la faille PHP illustrait la manière dont les équipes de sécurité du monde entier doivent désormais composer avec un flux quotidien de nouvelles vulnérabilités et de correctifs découverts grâce à l'IA.

« Même avant l'IA de pointe, les défenseurs informatiques, en particulier dans les entreprises d'infrastructures critiques, avaient déjà du mal à suivre le rythme des correctifs, car nous devons nous assurer qu'il n'y a pas d'interruption de service pour continuer à fournir des services essentiels à tous », a déclaré Matsubara.

Interrogée sur la question de savoir si PHP2Shell restera dans les mémoires comme le plus grand drame de sécurité de 2026, la dirigeante a répondu : « Je ne mettrais pas d'argent sur cette hypothèse, car grâce à l'IA, nous risquons d'en voir d'autres. »

## Pourquoi ça compte
Cet épisode illustre comment une faille unique dans une brique logicielle largement répandue peut déclencher une onde de choc touchant simultanément des fournisseurs de sécurité réseau et des infrastructures critiques nationales, tout en révélant un nouveau facteur structurel : la découverte de vulnérabilités assistée par l'IA accélère le rythme des crises de sécurité au point de dépasser la capacité de réponse des équipes de défense.
