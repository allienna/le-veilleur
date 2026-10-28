---
title: "Four-Step Dimensional Design Process"
date: 2026-10-28
url: "https://substack.com/redirect/5a1ec009-6655-494d-9eef-262a073a4674?j=eyJ1IjoiN3Y1bG1jIn0.HlvPOGYPdVknSYzEK1JIj6IFkAFn8zuyjtfU9Mbft9Q"
keywords: ["modélisation dimensionnelle", "méthode Kimball", "grain", "dimensions et faits", "gouvernance des données"]
theme: "Data"
tone: "tutorial"
used_in: ["2026-10-28"]
---

## Résumé
Ce texte présente le processus de conception dimensionnelle en quatre étapes, un cadre méthodologique classique utilisé en modélisation de données décisionnelles. Il décrit les quatre décisions fondamentales à prendre lors de la conception d'un modèle dimensionnel : choisir le processus métier, déclarer le grain, identifier les dimensions, puis identifier les faits. Le texte souligne que ces décisions doivent concilier les besoins métier et les contraintes réelles des données sources, dans le cadre de sessions de modélisation collaboratives. Il insiste enfin sur le rôle des représentants de la gouvernance des données métier dans la validation des détails de conception.

## Points clés
- Le processus de conception dimensionnelle repose sur quatre décisions clés : processus métier, grain, dimensions, faits.
- Ces décisions doivent résulter d'un compromis entre les besoins business et les réalités des données source.
- La conception se déroule lors de sessions de modélisation collaboratives impliquant plusieurs parties prenantes.
- Après ces quatre déclarations, l'équipe définit les noms de tables et de colonnes, des exemples de valeurs de domaine, et les règles métier.
- La participation des représentants de la gouvernance des données métier est jugée indispensable pour obtenir l'adhésion ( buy-in ) du métier.

## Analyse approfondie
Les quatre décisions clés prises lors de la conception d'un modèle dimensionnel sont :

1. Sélectionner le processus métier.
2. Déclarer le grain.
3. Identifier les dimensions.
4. Identifier les faits.

Les réponses à ces questions sont déterminées en tenant compte des besoins du métier ainsi que des réalités des données source sous-jacentes, au cours des sessions de modélisation collaboratives. Une fois les déclarations de processus métier, de grain, de dimensions et de faits effectuées, l'équipe de conception détermine les noms de tables et de colonnes, des exemples de valeurs de domaine, et les règles métier. Les représentants de la gouvernance des données métier doivent participer à cette activité de conception détaillée afin de garantir l'adhésion du métier (business buy-in).

## Pourquoi ça compte
Ce rappel méthodologique reste une référence incontournable pour toute équipe data qui conçoit des modèles dimensionnels (data warehouse, data marts), en particulier pour structurer le dialogue entre équipes techniques et parties prenantes métier.
