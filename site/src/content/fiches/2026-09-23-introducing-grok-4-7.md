---
title: "Introducing Grok 4.7"
date: 2026-09-23
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Flinks.tldrnewsletter.com%2F0xk7iD/1/010001a0c94ac023-ce61b09e-2653-4bb7-99c9-33f88214b103-000000/Wm7YsJbP4CwurPPqv1ZXMf-_Ca5tP26TIH3YdaEplnI=452"
keywords: ["Grok 4.7", "xAI", "modèles de langage", "cybersécurité", "codage", "benchmarks"]
theme: "IA"
tone: "news"
used_in: ["2026-09-23"]
---

## Résumé
xAI annonce Grok 4.7, son modèle le plus performant à ce jour pour le codage et les tâches de connaissance, proposé au même prix et à la même vitesse que Grok 4.6. Construit sur une base plus large et entraîné plus longuement par renforcement sur des tâches complexes, il améliore la gestion de contexte long, la vérification de son propre travail et la production de documents professionnels. Le modèle intègre aussi une toute nouvelle pile de garde-fous, le rendant particulièrement résistant aux tentatives de jailbreak tout en conservant un faible taux de refus sur les usages légitimes, notamment en cybersécurité. Il est disponible dès aujourd'hui dans Cursor, Grok Build, l'API Grok et divers routeurs de modèles.

## Points clés
- Grok 4.7 est positionné à la frontière du rapport prix/performance sur CursorBench 4.0, un benchmark de tâches de codage longues.
- Le modèle repose sur une base plus grande que Grok 4.6, entraînée par un run de renforcement plus long sur des tâches difficiles, souvent longues de plusieurs heures.
- Il progresse sur GDPval et AA Briefcase (tâches professionnelles type avocats, infirmiers, analystes financiers), se rapprochant des autres modèles de pointe.
- Nouvelle pile de sécurité : meilleur modèle testé par xAI sur les refus et la résistance au jailbreak, en tête du benchmark de biosécurité LatchBio (62,4 %).
- Sur HackerBench v0.3, il ne laisse passer que 3,3 % des prompts cyber à risque tout en bloquant rarement le travail de sécurité légitime ; un accès red-team sur invitation est ouvert à des partenaires cybersécurité.
- Tarification : à partir de 2 $ par million de tokens en entrée et 6 $ par million en sortie, avec une variante rapide deux fois plus véloce au double du prix.

## Analyse approfondie
Grok 4.7 est notre modèle le plus performant pour le codage et le travail de connaissance. Il travaille plus longtemps sur les tâches difficiles, vérifie son propre travail avec plus de rigueur, et embarque nos meilleurs garde-fous à ce jour. Servi au même prix et à la même vitesse que Grok 4.6, il est très compétitif dans sa catégorie.

Sur CursorBench 4.0, qui met l'accent sur les tâches de codage de longue durée, Grok 4.7 se situe à la frontière du rapport prix/performance.

Grok 4.7 s'appuie sur un nouveau modèle de base, plus grand que celui de Grok 4.6. Il a été entraîné avec un run d'apprentissage par renforcement plus long, sur un mélange de tâches plus difficiles, avec une pondération en faveur de problèmes nécessitant de nombreuses heures à résoudre. Le modèle est meilleur pour vérifier son propre travail et gérer un contexte plus long. Nous avons également entraîné Grok 4.7 à comprendre nativement le harnais Grok Bot, ce qui le rend meilleur dans les tâches conversationnelles et le travail de connaissance générale.

Grok 4.7 est meilleur pour créer des documents et des présentations. Dans GDPval et AA Briefcase, l'IA est mise à l'épreuve sur des tâches réalisées par des professionnels tels que des avocats, des infirmiers et des analystes financiers. Grok 4.7 progresse par rapport à Grok 4.6 sur ces deux benchmarks et affiche des performances comparables à celles des autres modèles de pointe.

Grok 4.7 a été construit avec une toute nouvelle pile de garde-fous. C'est le modèle le plus solide que nous ayons testé en matière de refus et de résistance au jailbreak. Dans les domaines à double usage comme la cybersécurité et le travail biologique, il est en tête à la fois pour l'utilité sur les tâches bénignes et pour le refus sûr des tâches dangereuses, se plaçant en tête du benchmark de biosécurité de LatchBio avec un score de 62,4 %.

Grok 4.7 équilibre de solides capacités de défense cyber avec de faibles taux de refus pour les usages légitimes. Il affiche la meilleure sécurité sur HackerBench v0.3, notre benchmark pour les tâches cyber risquées et malveillantes, ne laissant passer que 3,3 % des prompts à double usage risqués tout en bloquant rarement le travail de sécurité légitime. Nous avons également commencé à donner à certains partenaires en cybersécurité un accès sur invitation aux capacités de red-team de Grok 4.7, à des fins de recherche défensive.

Grok 4.7 est disponible dès aujourd'hui dans Cursor et Grok Build. Il est également accessible via l'API Grok, des harnais de codage tiers, ainsi que des routeurs de modèles et des plateformes cloud.

Le modèle est tarifé à partir de 2 $ par million de tokens en entrée et 6 $ par million de tokens en sortie. Nous proposons également une variante rapide, deux fois plus véloce en sortie, au double du prix.

## Pourquoi ça compte
Cette annonce illustre la course continue entre laboratoires d'IA sur le rapport prix/performance en codage et sur la robustesse des garde-fous face aux usages malveillants, un enjeu clé pour la veille sécurité et IA appliquée aux outils professionnels.
