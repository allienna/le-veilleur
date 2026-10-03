---
title: "Introducing Grok 4.7"
date: 2026-10-03
url: "https://elinkb7e.mail.aiwithremy.com/ss/c/u001.MqKIjgh6BgBZ0egqqBw0s9sHnkwHhYskVveBugIh2oB7ZCImlf2dfy1jxOIr5QApHlLOKC9SLq-v-PyKjlQXb4RH3gDoCLMgXyj_lE_1V-omy99DlbV89M9EtZmd7oa9QdcmEE5UFHosw0QKBGfSQXqFd6hAStaC4LT1upImOgvL5K9Nf-XEaZCWGlTdmDVhJy5cS7T7Xkc6GcbjFeQ_A2duj1PKuYAqKGthVqOmL3vhGiOcNm-W812SG0flBQ22l5JAL37yMUwS4z4rweRE8g/4uj/iyYzyNEMQwKDJINrvZRz6g/h7/h001.g6d7hEUGfRB_Eje170eKIYy2b7DLCUBJX1-Uq1Tp9WE"
authors: ["xAI"]
keywords: ["Grok 4.7", "xAI", "sécurité IA", "codage", "cybersécurité", "benchmarks"]
theme: "IA"
tone: "news"
used_in: ["2026-10-03"]
---

## Résumé
xAI annonce Grok 4.7, son modèle le plus performant à ce jour pour le code et le travail de connaissance, capable de travailler plus longtemps sur des tâches difficiles et de mieux vérifier son propre travail. Proposé au même prix et à la même vitesse que Grok 4.6, il progresse sur les benchmarks de codage (CursorBench 4.0) et de productivité professionnelle (GDPval, AA Briefcase). Le modèle inaugure aussi une toute nouvelle pile de sécurité, affichant les meilleurs résultats de xAI en matière de résistance au jailbreak et de refus sûr des requêtes dangereuses en cybersécurité et en biologie. Il est disponible dès aujourd'hui dans Cursor, Grok Build, l'API Grok et diverses plateformes tierces, à partir de 2$/M tokens en entrée et 6$/M en sortie.

## Points clés
- Modèle de base nouveau et plus volumineux, entraîné avec un cycle de reinforcement learning plus long sur des tâches plus difficiles, pondérées vers des problèmes prenant plusieurs heures.
- Meilleure autovérification et meilleure gestion de contextes longs ; compréhension native du harness Grok Bot pour des échanges conversationnels plus fluides.
- À la frontière du rapport qualité-prix sur CursorBench 4.0 (tâches de codage longues) et progrès sur GDPval/AA Briefcase (tâches de type avocat, infirmier, analyste financier).
- Nouvelle pile de garde-fous : meilleur score de xAI sur les refus et la résistance au jailbreak, avec 62,4% sur le benchmark de biosécurité de LatchBio.
- Sur HackerBench v0.3 (tâches cyber risquées), ne laisse passer que 3,3% des prompts à double usage dangereux tout en bloquant rarement le travail de sécurité légitime.
- Accès anticipé, sur invitation, aux capacités de red-team du modèle pour des partenaires cybersécurité sélectionnés ; variante rapide disponible à vitesse double pour un prix double.

## Analyse approfondie
Grok 4.7 est notre modèle le plus performant pour le code et le travail de connaissance. Il travaille plus longtemps sur les tâches difficiles, vérifie son propre travail avec plus de soin, et s'accompagne de nos garde-fous les mieux calibrés à ce jour. Proposé au même prix et à la même vitesse que Grok 4.6, il est hautement compétitif dans sa catégorie.

Sur CursorBench 4.0, qui met l'accent sur des tâches de codage de plus longue durée, Grok 4.7 se situe à la frontière en matière de rapport qualité-prix (price-performance).

Grok 4.7 repose sur un modèle de base nouveau et plus volumineux que celui de Grok 4.6. Il a été entraîné au moyen d'un cycle de reinforcement learning plus long, sur un ensemble de tâches plus difficiles, pondéré en faveur de problèmes nécessitant de nombreuses heures pour être résolus. Le modèle est meilleur pour vérifier son propre travail et gérer des contextes plus longs. Nous avons également entraîné Grok 4.7 à comprendre nativement le harness Grok Bot, ce qui le rend meilleur pour les tâches conversationnelles et le travail de connaissance générale.

Grok 4.7 est plus performant pour la création de documents et de présentations. Dans GDPval et AA Briefcase, l'IA est chargée de réaliser des tâches effectuées par des professionnels tels que des avocats, des infirmiers et des analystes financiers. Grok 4.7 progresse par rapport à Grok 4.6 sur ces deux benchmarks et obtient des performances comparables à celles des autres modèles de pointe (frontier models).

Grok 4.7 a été construit avec une pile de garde-fous (safeguard stack) entièrement nouvelle. C'est le modèle le plus solide que nous ayons testé en matière de refus et de résistance au jailbreak. Dans les domaines à double usage (dual-use) comme la cybersécurité et le travail biologique, il arrive en tête à la fois pour l'utilité sur les tâches bénignes et pour le refus sûr des tâches dangereuses, se classant premier sur le benchmark de biosécurité de LatchBio avec un score de 62,4%.

Grok 4.7 concilie de solides capacités de cyberdéfense avec de faibles taux de refus pour les usages légitimes. Il affiche le meilleur niveau de sécurité sur HackerBench v0.3, notre benchmark pour les tâches cyber risquées et malveillantes, en ne laissant passer que 3,3% des prompts à double usage risqués, tout en bloquant rarement le travail de sécurité légitime. Nous avons également commencé à donner à certains partenaires en cybersécurité, sur invitation uniquement, un accès aux capacités de red-team de Grok 4.7 pour la recherche en défense.

Grok 4.7 est disponible dès aujourd'hui dans Cursor et Grok Build. Il est également accessible via l'API Grok, des harnesses de codage tiers, ainsi que des routeurs de modèles et des plateformes cloud.

Le modèle est tarifé à partir de 2$ par million de tokens en entrée et 6$ par million de tokens en sortie. Nous proposons également une variante rapide, deux fois plus rapide en sortie, pour un prix deux fois plus élevé.

## Pourquoi ça compte
Cette annonce illustre la course continue entre laboratoires d'IA sur le couple performance/sécurité, avec un accent marqué de xAI sur la calibration des refus en contexte dual-use (cybersécurité, biologie) — un signal à suivre pour quiconque évalue le positionnement concurrentiel de Grok face à OpenAI, Anthropic ou Google sur les usages professionnels et le codage.
