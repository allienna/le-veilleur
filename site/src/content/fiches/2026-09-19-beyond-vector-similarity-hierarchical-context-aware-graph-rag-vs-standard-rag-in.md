---
title: "Beyond Vector Similarity: Hierarchical Context-Aware Graph RAG vs Standard RAG in Enterprise Code Migration"
date: 2026-09-19
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Farxiv.org%2Fabs%2F2609.12464%3Futm_source=tldrit/1/010001a0b47533a3-741ea328-68ec-45bd-9bd6-b85eb11d154b-000000/28IY7uZMDiWtbK3fdUclKm8wjCC84cc9cADUNleqX5c=452"
keywords: ["RAG", "graphe de connaissances", "migration de code", "LLM", "hallucination", "microservices"]
theme: "IA"
tone: "research"
used_in: ["2026-09-19"]
---

## Résumé
Cet article de recherche (arXiv) compare deux approches de Retrieval-Augmented Generation (RAG) pour automatiser la traduction de code lors de la modernisation de systèmes monolithiques vers des microservices : le RAG vectoriel classique et une nouvelle méthode nommée Hierarchical Context-Resident Graph (HCRG), un « Graph RAG ». Les auteurs montrent que le RAG standard, en récupérant des fragments de code isolés, brise les chaînes d'héritage et provoque un fort taux d'échec de compilation, un problème masqué par des métriques traditionnelles comme CodeBLEU. Leur pipeline s'appuie sur tree-sitter pour extraire l'arbre syntaxique abstrait (AST), un Property Graph sur Google Cloud Spanner pour cartographier les relations architecturales, et un Gemini Context Cache pour sérialiser cette structure. Résultat empirique clé : le Graph RAG réduit fortement les hallucinations d'API et améliore la cohérence des dépendances, au prix d'une complexité de code légèrement accrue.

## Points clés
- Le RAG vectoriel classique fragmente le code et casse les relations topologiques (héritage, dépendances), entraînant des échecs de compilation.
- La métrique CodeBLEU (91 % pour les deux méthodes) masque ces défaillances structurelles derrière un code syntaxiquement plausible mais cassé — d'où la création d'un cadre d'évaluation maison à 7 métriques de génie logiciel.
- Le pipeline HCRG combine tree-sitter (extraction d'AST), un Property Graph sur Google Cloud Spanner, et un Gemini Context Cache pour une traduction de code topologique et « parent-first ».
- Le taux d'hallucination d'API chute de 56,4 % à 16,2 % avec le Graph RAG ; la qualité de résolution des dépendances passe de 34,8 % à 65,9 % ; la cohérence parent-enfant grimpe de 26,7 % à 45,5 %.
- Contrepartie : le contexte global dense pousse le LLM vers une sur-ingénierie défensive, faisant chuter la cohérence de complexité cyclomatique de 71,6 % à 46,7 %, et dégradant légèrement la préservation des docstrings (67,0 % à 61,0 %).
- Conclusion des auteurs : malgré ce compromis sur la complexité du code, le Graph RAG offre une voie nettement plus viable et architecturalement solide pour la modernisation automatisée de bases de code d'entreprise.

## Analyse approfondie
**Titre : Au-delà de la similarité vectorielle : RAG hiérarchique et contextuel par graphe contre RAG standard dans la migration de code en entreprise**

Résumé : Alors que les entreprises modernisent leurs systèmes monolithiques hérités vers des microservices, les grands modèles de langage (LLM) sont massivement utilisés pour la traduction automatisée de code. Cependant, la génération augmentée par récupération (RAG) basée sur des vecteurs traditionnelle peine à capturer les relations topologiques. Elle récupère des fragments isolés qui rompent les chaînes d'héritage, entraînant des taux élevés d'échec de compilation. Cet article introduit une méthodologie de graphe hiérarchique contextuel (Hierarchical Context-Resident Graph, HCRG) pour résoudre ces limitations. Notre pipeline utilise tree-sitter pour l'extraction d'arbre syntaxique abstrait (AST), cartographie les relations architecturales dans un Property Graph Google Cloud Spanner, et sérialise cette structure dans un Gemini Context Cache pour une traduction de code topologique et « parent d'abord » (parent-first). Nous déplaçons l'évaluation d'un simple chevauchement textuel vers un cadre personnalisé de génie logiciel à 7 métriques. Les métriques traditionnelles comme CodeBLEU (qui obtenait un score de 91 % pour les deux méthodes) masquaient efficacement les défaillances structurelles du RAG standard derrière un code syntaxiquement plausible mais cassé. Empiriquement, le Graph RAG atténue de manière décisive la perte de dépendances : les taux d'hallucination d'API sont passés de 56,4 % à 16,2 %, la qualité de résolution des dépendances s'est améliorée de 34,8 % à 65,9 %, et la cohérence parent-enfant est passée de 26,7 % à 45,5 %. Cependant, le Graph RAG introduit des compromis spécifiques. Le contexte global dense provoque une sur-ingénierie défensive de la part du LLM, réduisant la cohérence de complexité cyclomatique de 71,6 % à 46,7 %, et dégrade légèrement la préservation des docstrings (de 67,0 % à 61,0 %). En définitive, tout en échangeant de la complexité de code contre une réduction des hallucinations, le Graph RAG offre une voie substantiellement plus viable et architecturalement saine pour la modernisation automatisée de bases de code d'entreprise.

## Pourquoi ça compte
Ce papier illustre une limite concrète des architectures RAG vectorielles classiques pour des tâches nécessitant une compréhension structurelle (code, dépendances), et propose une piste concrète — le Graph RAG couplé à un cache de contexte — pertinente pour toute veille sur l'usage des LLM en migration ou modernisation de systèmes d'entreprise.
