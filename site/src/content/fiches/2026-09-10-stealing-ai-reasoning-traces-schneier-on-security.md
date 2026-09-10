---
title: "Stealing AI Reasoning Traces - Schneier on Security"
date: 2026-09-10
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.schneier.com%2Fblog%2Farchives%2F2026%2F09%2Fstealing-ai-reasoning-traces.html%3Futm_source=tldrai/1/010001a0865dff15-ab1e96d3-e50a-4858-9290-c463567f08de-000000/fiLzFhqoeIm8V_1LTWZVmpy8wWhxbwc5dcXs6dxXTg8=452"
authors: ["Bruce Schneier"]
keywords: ["chain-of-thought", "jailbreak", "extraction de données", "API LLM propriétaires", "chiffrement"]
theme: "Sécurité"
tone: "news"
used_in: ["2026-09-10"]
---

## Résumé
L'article de Bruce Schneier relaie une recherche montrant que les blocs de raisonnement chiffrés (chain-of-thought) renvoyés par les API de LLM propriétaires sont interchangeables entre sessions, utilisateurs et modèles d'un même fournisseur. Les chercheurs exploitent cette faille architecturale pour forcer un modèle plus faible à déchiffrer et afficher en clair la trace de raisonnement d'un modèle plus puissant, sans jamais attaquer directement ce dernier. La vulnérabilité a été démontrée chez Anthropic, OpenAI et Google, et a permis d'extraire des centaines de PII et d'identifiants depuis des journaux de sessions publiés publiquement. Schneier conclut sur une note ironique : des chatbots eux-mêmes accusés de s'être construits sur de la propriété intellectuelle volée s'inquiètent qu'on vole la leur.

## Points clés
- Les fournisseurs de LLM chiffrent les traces de chain-of-thought côté client (plutôt que de les stocker côté serveur) pour protéger leur IP et limiter les fuites, mais le client doit les renvoyer à chaque requête suivante.
- Ces blocs chiffrés sont compatibles et interchangeables entre sessions, utilisateurs et modèles d'un même fournisseur — une faille architecturale exploitable.
- En injectant la trace chiffrée d'un modèle puissant dans un modèle plus faible et moins protégé, les chercheurs le forcent à décoder et exposer le raisonnement en clair : un « jailbreak de déchiffrement » scalable, démontré chez Anthropic, OpenAI et Google.
- Quatre vecteurs d'attaque identifiés : contournement de l'anti-distillation, extraction massive de données privées, révélation d'informations dangereuses masquées même quand la réponse finale refuse la requête, et injections de prompt invisibles dans des rollouts agentiques publics.
- En décodant 315 320 blocs de raisonnement récupérés dans des dépôts publics, les chercheurs ont retrouvé 367 éléments de PII et 182 identifiants.
- Les auteurs ont suivi une procédure de divulgation responsable et proposent des mitigations cryptographiques et systémiques.

## Analyse approfondie
**Stealing AI Reasoning Traces**

Recherche intéressante : « Stealing Reasoning Traces from Proprietary LLM APIs ».

**Résumé (abstract) :** Les principaux fournisseurs de grands modèles de langage dissimulent désormais le raisonnement étape par étape de leurs modèles, ou chaîne de pensée (chain-of-thought), afin de protéger leur propriété intellectuelle et de limiter les fuites d'informations. Plutôt que de stocker ces traces côté serveur, les fournisseurs les renvoient au client sous forme de blocs de texte chiffré, que le client renvoie ensuite avec chaque requête suivante. En nous appuyant sur des recherches antérieures, nous identifions une vulnérabilité architecturale : ces blocs chiffrés sont entièrement compatibles et interchangeables entre différentes sessions, utilisateurs et modèles au sein de l'écosystème d'un même fournisseur. Nous exploitons cette compatibilité pour développer un jailbreak de déchiffrement scalable. En injectant une trace de raisonnement chiffrée provenant d'un modèle donné dans un modèle plus faible et moins protégé du même fournisseur, nous le forçons à décoder et à afficher la trace mot pour mot en clair, sans jamais avoir à jailbreaker directement le modèle le plus performant. Cette vulnérabilité permet quatre vecteurs d'attaque distincts. Premièrement, elle contourne les mécanismes anti-distillation, permettant à des adversaires d'extraire le raisonnement d'un modèle propriétaire, comme nous le démontrons chez Anthropic, OpenAI et Google. Deuxièmement, elle permet une extraction de données privées à grande échelle. Les développeurs partagent souvent publiquement des journaux de sessions, sans savoir ce que contiennent les blocs chiffrés. En décodant 315 320 blocs de raisonnement collectés dans des dépôts publics, nous avons récupéré 367 éléments d'information personnelle identifiable (PII) et 182 identifiants (credentials). Troisièmement, elle révèle par inadvertance des informations dangereuses dissimulées dans le processus de raisonnement, y compris dans les cas où la sortie finale visible du modèle rejette de façon sûre une requête malveillante. Quatrièmement, des attaquants peuvent exploiter cette faille pour exécuter des injections de prompt invisibles, en intégrant des charges utiles malveillantes entièrement dans les blocs chiffrés afin d'empoisonner des exécutions agentiques publiques. À la suite d'une divulgation responsable, nous proposons des mesures d'atténuation concrètes, tant cryptographiques que systémiques, pour sécuriser le raisonnement côté client.

Michael • 8 septembre 2026, 10 h 48

Donc les chatbots dominants, largement construits sur de la propriété intellectuelle volée, s'inquiètent qu'on leur vole la leur. Fascinant.

## Pourquoi ça compte
Cette faille touche au cœur de la promesse de confidentialité des API de raisonnement des grands fournisseurs de LLM (Anthropic, OpenAI, Google) : elle transforme un mécanisme pensé pour protéger l'IP et la sécurité en un vecteur d'extraction de secrets, de PII et d'attaques par injection à grande échelle, ce qui en fait un signal important à suivre pour toute veille sécurité IA.
