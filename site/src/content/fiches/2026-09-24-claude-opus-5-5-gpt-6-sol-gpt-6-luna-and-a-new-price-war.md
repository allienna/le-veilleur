---
title: "Claude Opus 5.5, GPT-6 Sol, GPT-6 Luna, and a new price war"
date: 2026-09-24
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fsimonwillison.net%2F2026%2FSep%2F22%2Fopus-and-sol-and-luna%2F%3Futm_source=tldrnewsletter/1/010001a0cddf5dd6-4a4eb42a-5617-4663-8713-76298d163470-000000/IIubHB7MCtSlsyRCMT0at6C6raVomJuTdUC8JfelXXs=452"
authors: ["Simon Willison"]
keywords: ["Claude Opus", "GPT-6", "guerre des prix", "LLM", "Anthropic", "OpenAI"]
theme: "IA"
tone: "opinion"
used_in: ["2026-09-24"]
---

## Résumé
Dans ce billet du 22 septembre 2026, Simon Willison analyse la sortie quasi simultanée de Claude Opus 5.5 (Anthropic) et de GPT-6 Sol / GPT-6 Luna (OpenAI), deux annonces qui déclenchent une nouvelle guerre des prix sur le marché des grands modèles de langage. GPT-6 Sol et Luna voient leur tarif divisé par deux par rapport à leurs équivalents GPT-5.6, tandis qu'Opus 5.5 bénéficie d'une baisse de 20 % et d'un style de communication amélioré. L'auteur note toutefois un problème notable : au niveau de réflexion « max », Opus 5.5 a échoué à produire une réponse sur son test habituel du pélican à vélo, épuisant sa limite de tokens en pleine réflexion.

## Points clés
- GPT-6 Luna et GPT-6 Sol coûtent environ deux fois moins cher que leurs prédécesseurs GPT-5.6, avec Luna à 0,10 $/M (entrée) et 0,50 $/M (sortie), l'un des tarifs les plus bas jamais proposés par OpenAI.
- Claude Opus 5.5 passe de 5 $/25 $ par million de tokens à 4 $/20 $, avec une baisse de 60 % sur les tokens en cache, un point important pour les usages agentiques à contexte long.
- Grok 4.7 (xAI), initialement très compétitif, se retrouve désormais aligné sur les prix de GPT-6 Sol.
- Au niveau de réflexion « max », Opus 5.5 a échoué deux fois de suite à terminer le test du pélican à vélo, épuisant sa limite de 128 000 tokens de sortie en pleine phase de raisonnement, chaque tentative coûtant 2,56 $ et près de 20 minutes.
- Anthropic annonce l'arrivée prochaine de Sonnet 5.5 et Haiku 5.5, avec une interrogation sur la capacité de Haiku à rester compétitif face à un GPT-6 Luna dix fois moins cher.
- L'auteur adopte déjà GPT-6 Sol et Claude Opus 5.5 comme modèles par défaut dans Codex et Claude Code, et bascule sa démo Datasette Agent vers GPT-6 Luna.

## Analyse approfondie
**Contexte.** La veille de cette publication avait déjà vu sortir Grok 4.7 et MiMo v2.6 (Flash/Pro). Le jour même, Anthropic publie Claude Opus 5.5, suivi environ une heure plus tard par GPT-6 Sol et GPT-6 Luna chez OpenAI. Willison précise qu'il est encore tôt pour juger pleinement ces modèles, mais livre ses premières impressions.

**Des tarifs GPT-6 Sol et Luna divisés par deux.** GPT-5.6 Luna était déjà le modèle préféré de l'auteur pour développer des applications, grâce à un excellent rapport performance/prix. GPT-6 Luna coûte pourtant encore deux fois moins cher, et GPT-6 Sol bénéficie d'une réduction comparable par rapport à GPT-5.6 Sol.

Tableau comparatif des tarifs (en dollars par million de tokens) :

| Modèle | Entrée | Entrée en cache | Sortie |
|---|---|---|---|
| GPT-6 Luna | 0,10 $/M | 0,01 $/M | 0,50 $/M |
| GPT-5.6 Luna | 0,20 $/M | 0,02 $/M | 1,20 $/M |
| Grok 4.7 | 2 $/M | 0,50 $/M | 6 $/M |
| GPT-6 Sol | 2 $/M | 0,20 $/M | 10 $/M |
| GPT-5.6 Terra | 2 $/M | 0,20 $/M | 12 $/M |
| Claude Opus 5.5 | 4 $/M | 0,20 $/M | 20 $/M |
| GPT-5.6 Sol | 4 $/M | 0,40 $/M | 20 $/M |
| Claude Fable 5.1 | 10 $/M | 0,25 $/M | 50 $/M |
| GPT-6 Astra | 10 $/M | 1 $/M | 50 $/M |

Willison souligne qu'une hausse de prix de 25 % est déjà prévue pour GPT-5.6 en novembre : GPT-6 revient donc à moitié prix même par rapport au tarif promotionnel actuel de GPT-5.6. Il remarque aussi qu'avec GPT-5.6 Terra désormais au même prix que GPT-6 Sol, les raisons de continuer à utiliser Terra ont pratiquement disparu.

Cette agressivité tarifaire est frappante : Grok 4.7 s'était positionné à 2 $/6 $, soit moins de la moitié du prix de GPT-5.6 Sol à l'époque, mais se retrouve maintenant à parité côté entrée et proche côté sortie avec GPT-6 Sol. À 0,10 $/0,50 $, GPT-6 Luna devient l'un des modèles les moins chers jamais publiés par OpenAI, devancé seulement par le bien plus faible GPT-4.1 Nano (0,10 $/0,40 $, avril 2025) et GPT-5 Nano (0,05 $/0,40 $, août 2025).

Pour tester les nouveaux modèles, l'auteur a généré des rendus de pélicans avec GPT-6 Luna et GPT-6 Sol, puis les a rassemblés dans une grille comparative incluant aussi les pélicans de GPT-5.6. Il observe que la famille 5.6 avait choisi des couleurs plus vives et audacieuses, tandis que la famille 6 est nettement plus sobre. Selon lui, c'est toujours GPT-6 Astra en mode « max » qui produit le meilleur pélican.

**Claude Opus 5.5 : baisse de prix et style amélioré.** Opus 5.5 semble répondre aux principales critiques adressées au style de communication d'Opus. Thariq Shihipar (Anthropic) est cité expliquant qu'Opus 5.5 est le fruit des retours utilisateurs : le modèle communique plus clairement, coûte moins cher par token qu'Opus 5.0 tout en offrant l'intelligence de Fable 5.1, se montre très économe en tokens, et fonctionne à tous les niveaux d'effort. Il serait également meilleur sur Blender, un point que l'auteur compte tester.

Les versions Opus 4.5, 4.6, 4.7, 4.8 et 5 partageaient toutes le même tarif : 5 $/million en entrée et 25 $/million en sortie. La version 5.5 introduit une baisse de 20 %, à 4 $ et 20 $. Le prix des lectures en cache chute quant à lui de 60 %, un changement significatif pour les conversations agentiques longues, où plus de 90 % des tokens d'entrée sont traités au tarif « cache ».

Le nouveau tarif d'Opus 5.5 rejoint celui de GPT-5.6 Sol — mais c'était avant qu'OpenAI ne divise par deux les prix de Sol. GPT-6 Astra et Claude Fable 5.1 restent tous deux à 10 $/million en entrée et 50 $/million en sortie : la guerre des prix touche pour l'instant surtout le palier de modèles situé juste en dessous.

Anthropic annonce également l'arrivée prochaine de Sonnet 5.5 et Haiku 5.5. Willison s'interroge sur la capacité de Haiku à retrouver sa compétitivité tarifaire sur l'entrée de gamme : le Haiku 4.5 actuel est à 1 $/5 $, alors que le tout nouveau GPT-6 Luna coûte dix fois moins cher, à 0,10 $/0,50 $.

**Le mode « max » d'Opus 5.5 sur-réfléchit jusqu'à planter.** Pour la première fois dans son test habituel consistant à générer un SVG représentant « un pélican faisant du vélo », Claude Opus 5.5 en niveau de réflexion « max » n'est pas parvenu à produire de réponse. Le modèle a qualifié la requête de « demande de test classique », puis s'est lancé dans un raisonnement extrêmement détaillé et minutieux sur l'anatomie du pélican, la géométrie du vélo, le placement des éléments SVG, les proportions des pattes, le rendu du panier avec un poisson, l'expression du visage, la superposition des calques, jusqu'aux attributs de dimension du SVG final.

L'auteur explique que si l'enthousiasme était réel, la génération s'est arrêtée net : Opus 5.5, comme les autres modèles Claude, est limité à 128 000 tokens de sortie maximum, une limite atteinte alors que le modèle était encore en train de raisonner sur le SVG. Une seconde tentative a donné le même résultat. Willison en conclut que le mode « max » est probablement inutilisable en l'état : si un modèle sur-réfléchit jusqu'à l'échec sur une requête aussi simple qu'un SVG de pélican, il n'a pas confiance dans sa capacité à bien se comporter sur des tâches plus complexes. Chacun des deux échecs lui a coûté 2,56 $ et près de 20 minutes.

À titre de comparaison, Fable 5.1 en mode « max » n'a pas connu ce problème de sur-réflexion et a produit, selon l'auteur, le meilleur pélican qu'il ait vu de la part d'un modèle Anthropic. Il partage les pélicans générés par Opus 5.5 (hors mode max), ainsi qu'une grille comparative incluant Opus 5, Fable 5.1 et Sonnet 5. Il conclut que comparer différents fournisseurs de modèles sur ce test précis a de moins en moins de sens, mais que l'exercice reste utile pour comparer une même famille de modèles à différents niveaux de raisonnement.

**Adoption personnelle.** Willison indique utiliser désormais GPT-6 Sol et Claude Opus 5.5 comme modèles par défaut dans Codex et Claude Code, et avoir mis à jour sa démo Datasette Agent (agent.datasette.io) pour utiliser GPT-6 Luna, qu'il trouve rapide et compétent aussi bien pour les requêtes SQL que pour la génération de HTML et JavaScript dans les Datasette Apps.

## Pourquoi ça compte
Cette actualité illustre une intensification rapide de la guerre des prix entre Anthropic, OpenAI et xAI sur les LLM, avec des baisses de tarifs de 20 à 50 % en quelques mois, tout en révélant une limite concrète des modes de raisonnement « max » (dépassement de la limite de tokens de sortie) à surveiller pour tout usage agentique en production.
