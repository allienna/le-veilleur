---
title: "Can AI Agents Answer Your Data Questions? A Benchmark for Data Agents"
date: 2026-10-24
url: "https://substack.com/redirect/226dda21-579d-4626-bb9f-477408bd966e?j=eyJ1IjoiN3Y1bG1jIn0.HlvPOGYPdVknSYzEK1JIj6IFkAFn8zuyjtfU9Mbft9Q"
keywords: ["benchmark", "agents IA", "données d'entreprise", "text-to-SQL", "LLM", "SGBD"]
theme: "Data"
tone: "research"
used_in: ["2026-10-24"]
---

## Résumé
Cet article présente DAB (Data Agent Benchmark), un nouveau benchmark destiné à évaluer les agents LLM sur des questions portant sur des données d'entreprise réelles. Contrairement aux benchmarks existants, qui ne testent que des sous-tâches isolées comme le text-to-SQL sur une seule base de données, DAB couvre le workflow complet auquel sont confrontés les agents en conditions réelles : données fragmentées, dupliquées, incohérentes, et informations clés enfouies dans du texte non structuré. Construit à partir d'une étude menée auprès d'entreprises déployant des agents de données en production dans six secteurs, DAB comprend 104 requêtes réparties sur 17 jeux de données et 4 systèmes de gestion de bases de données. Le meilleur agent de l'état de l'art n'atteint que 57 % de réussite (pass@1), ce qui souligne les limites actuelles de ces systèmes.

## Points clés
- DAB comprend 104 requêtes couvrant 17 jeux de données et 4 systèmes de gestion de bases de données (SGBD) différents.
- Les benchmarks existants ne testent que des fragments isolés du workflow (ex. text-to-SQL sur une seule base) et sont de plus en plus saturés et contaminés.
- Les données d'entreprise réelles sont fragmentées entre systèmes hétérogènes, dupliquées, incohérentes, avec des informations clés cachées dans du texte non structuré.
- Les agents doivent aller au-delà de la simple écriture de requêtes SQL ou de scripts de data science pour répondre aux questions.
- Le meilleur agent état de l'art n'atteint que 57 % de pass@1 sur ce benchmark.
- Les auteurs analysent les modes d'échec des agents et en tirent des enseignements pour orienter le développement futur des agents de données.

## Analyse approfondie
# Informatique > Bases de données

# Titre : Les agents IA peuvent-ils répondre à vos questions sur les données ? Un benchmark pour les agents de données

Voir le PDF HTML (expérimental)

Résumé : Construire des agents de données fiables reste difficile, car les données d'entreprise réelles sont fragmentées entre de nombreux systèmes de bases de données hétérogènes, avec des données dupliquées et incohérentes, et des informations clés souvent enfouies dans du texte non structuré, ce qui exige des agents qu'ils aillent au-delà de la simple écriture de SQL ou de scripts de data science pour répondre aux questions. Les benchmarks existants ne couvrent que des fragments isolés de ce workflow de bout en bout (par exemple, le text-to-SQL sur une seule base de données) et sont de plus en plus saturés et contaminés. Nous présentons un nouveau benchmark pour les agents LLM, le Data Agent Benchmark (DAB), fondé sur une étude d'entreprises construisant des agents de données en production dans six secteurs d'activité. DAB comprend 104 requêtes couvrant 17 jeux de données et 4 systèmes de gestion de bases de données. Sur DAB, le meilleur agent de l'état de l'art n'atteint que 57 % de pass@1. Nous analysons les modes d'échec des agents et en tirons des enseignements pour le développement futur des agents de données. Notre benchmark et le code de nos expériences sont publiés à cette adresse URL.

# Outils bibliographiques et de citation

# Code, données et médias associés à cet article

# Démonstrations

# Outils de recommandation et de recherche

# arXivLabs : projets expérimentaux avec des collaborateurs de la communauté

arXivLabs est un cadre permettant à des collaborateurs de développer et de partager de nouvelles fonctionnalités arXiv directement sur notre site web.

Les individus et organisations qui travaillent avec arXivLabs ont adopté et accepté nos valeurs d'ouverture, de communauté, d'excellence et de respect de la vie privée des données des utilisateurs. arXiv s'engage à respecter ces valeurs et ne travaille qu'avec des partenaires qui y adhèrent.

Vous avez une idée de projet qui apporterait de la valeur à la communauté d'arXiv ? **En savoir plus sur arXivLabs**.

## Pourquoi ça compte
Ce benchmark expose un écart important entre les démonstrations d'agents IA sur des cas simplifiés et la réalité complexe des systèmes de données d'entreprise, ce qui en fait une référence utile pour évaluer de façon réaliste la maturité des agents de données avant tout déploiement en production.
