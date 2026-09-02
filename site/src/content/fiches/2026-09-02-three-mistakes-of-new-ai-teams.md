---
title: "Three mistakes of new AI teams"
date: 2026-09-02
url: "https://link.mail.beehiiv.com/ss/c/u001.T-cngy-HiLjOztVyxmCjHAiI2yPEX7vUHq-Jru9d4NsPDrvi2oSHIGJZ4SD50HBaCmcgcWxHUsTVZOG5PtLneh5KoajT1zlLtroX9jXOZSeukuFc2HhCf5ItCQ7UGxhJ6LiMkRUmg-0LxE0-Vq_onZiK7lAB8Zi_dYb2YVST_cNgg8YrWXQYmvcdi7QPNzkq/4to/J86wL3ZyRZKrMW8TS6n3xA/h14/h001.Z6EBhIbPzGmAVMTOlpdAUMVYbSC_J4IgKPiHiaL5Uzc"
authors: ["Doug Turnbull"]
keywords: ["RAG", "retrieval", "évaluation", "recherche", "équipes IA"]
theme: "IA"
tone: "opinion"
used_in: ["2026-09-02"]
---

## Résumé
L'auteur, consultant spécialisé en recherche et RAG (retrieval-augmented generation), constate que les jeunes équipes IA reproduisent les erreurs commises par les équipes de recherche (search) des années 2010. Il identifie trois angles morts récurrents : l'absence d'évaluation rigoureuse, la sous-estimation de la complexité du retrieval, et une conception du "chunking" trop pauvre en métadonnées. Il plaide pour des équipes pluridisciplinaires mêlant ingénierie et data science plutôt que des silos séquentiels.

## Points clés
- Les organisations IA performantes consacrent une grande partie de leur effort à *comprendre* le problème (via des évaluations, ou "evals") plutôt qu'à le résoudre à l'aveugle.
- Se fier à son intuition ou à l'avis des product managers est risqué : seule une évaluation structurée révèle ce que "bon" signifie réellement pour l'utilisateur (exemple vécu chez Advanced Auto Parts, où la vraie intention de recherche différait de l'hypothèse initiale).
- Le retrieval n'est pas une simple case à cocher dans une architecture RAG standard : la qualité de la réponse d'un LLM dépend directement de la qualité du contexte récupéré, ce qui implique des choix complexes (découpage, ranking, diversité des résultats).
- Le "chunking" classique (découper le texte en passages) est insuffisant : ce qui compte, c'est d'enrichir les passages avec des métadonnées (titre, popularité, date de publication...) pour permettre au LLM d'évaluer la pertinence et la fiabilité d'une information.
- La compréhension de requête et la gestion des métadonnées constituent un "troisième pilier" caché du retrieval, au même niveau que la recherche lexicale et les embeddings.
- Les équipes IA gagnent à fusionner ingénierie et data science dans les mêmes personnes plutôt qu'à faire circuler des modèles entre silos, ce qui évite des cycles longs et coûteux de correction tardive.

## Analyse approfondie
**Sur les évaluations.** L'auteur insiste sur le fait qu'une organisation IA sérieuse ne peut pas avancer sans une méthodologie d'évaluation robuste — il cite le travail de Hamel Husain et Shreya Shankar, qui enseignent à mesurer le succès produit de bout en bout plutôt que des métriques génériques, puis à décomposer ce succès pour localiser les points faibles (retrieval, garde-fous, etc.). Il relie cette conviction à son expérience de fondateur de Quepid (outil d'évaluation de la recherche créé il y a douze ans), née du constat qu'il n'existe pas de réponse objectivement "juste" en recherche conversationnelle ou en IA. Il illustre par une anecdote : lors d'un projet pour la recherche interne d'Advanced Auto Parts, il avait supposé que les employés voulaient simplement retrouver le produit recherché, alors qu'en réalité ils voulaient surtout savoir quel produit leur rapporterait une prime de vente. La leçon : le rôle d'une équipe IA n'est pas seulement de construire, mais d'agir en scientifique — évaluer, formuler des hypothèses, tester, améliorer en boucle.

**Sur le retrieval.** L'auteur affirme que les équipes IA sont, de fait, des équipes de recherche (search teams), et que l'une des découvertes les plus robustes de la recherche académique est que la qualité du retrieval conditionne directement la qualité des réponses du LLM. Il évoque une étude où fournir le "bon" contexte au modèle améliore nettement la qualité des réponses, tout en soulignant que cela suppose déjà de disposer d'évaluations permettant de savoir ce qu'est un "bon" contexte. Il note que les choix techniques (stratégie de découpage, technologies de récupération, méthodes de ranking, diversité des résultats) sont nombreux et hétérogènes, et qu'il est facile de s'enfermer prématurément dans une approche par excès d'investissement (sunk cost). Il recommande d'expérimenter à moindre coût des solutions simples avant de basculer vers des architectures plus robustes et coûteuses — un arbitrage qui, selon lui, demande une véritable expérience du domaine de la recherche.

**Sur les métadonnées et le "vrai" RAG.** L'auteur remet en question la vision classique du RAG comme simple appariement question-passage par similarité d'embeddings. Pour lui, le RAG consiste avant tout à présenter à l'agent une information exploitable pour juger de sa pertinence et de sa fiabilité. Il prend l'exemple d'un chunk brut de son blog ("j'ai travaillé chez Shopify sur la pertinence de recherche") comparé à ce même contenu enrichi de métadonnées structurées (titre, popularité, date de publication) : la seconde version aide bien davantage le LLM à juger si l'information est récente, fiable, ou mérite une vérification supplémentaire. Il en tire une règle générale : il faut représenter une unité d'information avec sa provenance plutôt que de se focaliser sur la découpe littérale en paragraphes, et permettre aux LLM de naviguer dans cette architecture d'information. Il propose de considérer la compréhension de requête et la gestion des métadonnées comme un troisième pilier du retrieval, à côté du lexical et des embeddings.

**Sur l'organisation des équipes.** Enfin, l'auteur défend une approche pluridisciplinaire : les meilleures équipes de recherche/IA combinent dans les mêmes profils la capacité à construire des systèmes scalables et à raisonner en hypothèses scientifiques, plutôt que de séparer ingénierie et data science en silos qui se "lancent des modèles par-dessus le mur" avant de découvrir, des mois plus tard, qu'il fallait tout recommencer. Il relie cette conviction à son travail de formation (avec Hugo Bowne-Anderson) autour de la construction d'agents et de systèmes de retrieval.

## Pourquoi ça compte
Cet article condense des retours de terrain sur les pièges les plus coûteux des jeunes équipes IA/RAG — évaluation négligée, retrieval sous-estimé, métadonnées ignorées — des angles morts directement transposables à toute organisation qui déploie du RAG en production.
