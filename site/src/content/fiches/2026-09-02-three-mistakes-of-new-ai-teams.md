---
title: "Three mistakes of new AI teams"
date: 2026-09-02
url: "https://link.mail.beehiiv.com/ss/c/u001.T-cngy-HiLjOztVyxmCjHAiI2yPEX7vUHq-Jru9d4NsPDrvi2oSHIGJZ4SD50HBaCmcgcWxHUsTVZOG5PtLneh5KoajT1zlLtroX9jXOZSeukuFc2HhCf5ItCQ7UGxhJ6LiMkRUmg-0LxE0-Vq_onZiK7lAB8Zi_dYb2YVST_cNgg8YrWXQYmvcdi7QPNzkq/4to/J86wL3ZyRZKrMW8TS6n3xA/h14/h001.Z6EBhIbPzGmAVMTOlpdAUMVYbSC_J4IgKPiHiaL5Uzc"
authors: ["Doug Turnbull"]
keywords: ["RAG", "évaluation", "recherche", "métadonnées", "équipes IA"]
theme: "IA"
tone: "opinion"
used_in: ["2026-09-02"]
---

## Résumé

L'auteur, consultant spécialisé en recherche et RAG (Retrieval-Augmented Generation), constate que les jeunes équipes IA reproduisent les mêmes erreurs que les équipes de recherche (search) des années 2010. Il identifie trois angles morts récurrents : l'absence d'évaluation rigoureuse (evals), la sous-estimation de la complexité du retrieval, et une conception trop restrictive de ce qu'est le "contexte" fourni au modèle. Il plaide pour des équipes pluridisciplinaires mêlant ingénierie et science des données plutôt que des silos séparés.

## Points clés

- Les organisations IA/search performantes consacrent environ 50% de leur effort à *comprendre* le problème (via des évaluations) plutôt qu'à le résoudre directement.
- Les évaluations doivent mesurer le succès du produit de bout en bout, pas des métriques génériques, et servir à localiser précisément les points faibles (retrieval, garde-fous, etc.).
- Le retrieval n'est pas une simple case à cocher : la qualité de la récupération d'information conditionne directement la qualité des réponses du LLM, et il existe de nombreuses architectures possibles à expérimenter, des plus simples aux plus complexes.
- Le "contexte" ne devrait pas se limiter à des chunks de texte brut : y ajouter des métadonnées structurées (titre, date, popularité, provenance) aide le LLM à juger de la pertinence et de la fiabilité d'une information.
- La compréhension de la requête et la gestion des métadonnées constituent un "troisième pilier" caché du retrieval, à côté du lexical et des embeddings.
- Les meilleures équipes IA sont multidisciplinaires : elles combinent ingénierie scalable et raisonnement scientifique par hypothèses, plutôt que de fonctionner en silos data science / engineering.

## Analyse approfondie

**Sur les évaluations.** L'auteur insiste sur le fait qu'on ne peut pas présumer savoir ce qu'est une "bonne" réponse. Il renvoie aux travaux de Hamel Hussain et Shreya Shankar, qui enseignent une méthodologie centrée sur la mesure du succès produit de bout en bout, puis sur la décomposition de cette mesure pour localiser les faiblesses (retrieval, garde-fous, etc.). Il partage son expérience personnelle : ayant créé l'outil Quepid il y a douze ans faute de vérité terrain objective en recherche conversationnelle, il a appris à ne pas se fier à son intuition. Il illustre ce point avec un projet mené pour la recherche interne d'Advanced Auto Parts, où l'hypothèse initiale (les employés cherchent le produit demandé) s'est révélée fausse : ce qu'ils voulaient réellement savoir, c'était quel produit leur rapporterait une prime de vente. Conclusion : le rôle d'une équipe IA n'est pas seulement de construire, mais de procéder comme des scientifiques — évaluer, formuler des hypothèses, tester, itérer.

**Sur le retrieval.** L'auteur affirme qu'une équipe IA est de fait une équipe de recherche (search), et que le retrieval déterminant la qualité de l'IA est l'un des résultats les mieux établis de la recherche académique : fournir le bon contexte à un LLM améliore radicalement la qualité de ses réponses (à condition, bien sûr, de disposer d'évaluations permettant de savoir ce qu'est le "bon" contexte). Les choix techniques — découpage en chunks, technologies de récupération, méthodes de ranking, diversité des réponses — sont nombreux et engendrent des architectures très différentes. Il met en garde contre le biais du coût irrécupérable (sunk cost) qui pousse à s'enfermer dans une seule approche, alors qu'il existe des moyens peu coûteux de tester des solutions simples avant d'investir dans des architectures robustes et complexes. Savoir naviguer entre le "rapide et sale" et le "robuste et coûteux" est, selon lui, une compétence qui s'acquiert avec l'expérience du search.

**Sur le contexte et les métadonnées.** L'auteur remet en question la vision classique du RAG comme simple pipeline de question-réponse (embedding des passages et de la requête, recherche de similarité, injection dans le contexte). Pour lui, le RAG consiste avant tout à présenter à l'agent une information exploitable, qui lui permette de juger de sa fiabilité et de sa pertinence par rapport à la requête. Il illustre cela avec un exemple tiré de son propre blog : un chunk de texte brut est bien moins utile à un LLM qu'un chunk enrichi de métadonnées structurées (titre, popularité, date de publication), car ces informations aident le LLM à évaluer si le contenu est récent, digne de confiance, ou mérite une investigation complémentaire. Un contenu peut être sémantiquement proche de la requête tout en étant une très mauvaise réponse pour l'utilisateur. L'auteur va plus loin : le retrieval ne se limite pas au lexical ou aux embeddings — représenter les bonnes métadonnées et permettre aux agents de s'appuyer sur elles peut compter davantage. Il propose de voir la compréhension de requête et les métadonnées comme un troisième pilier, caché, du retrieval. Sa recommandation : ne pas penser en termes de "chunks", mais réfléchir à la manière de représenter une unité d'information avec sa provenance, et à la façon de permettre aux LLM de naviguer dans cette architecture de l'information.

**Sur l'intersection ingénierie / data science.** Comme pour le search, les équipes IA prospèrent lorsqu'elles sont pluridisciplinaires. L'auteur plaide contre le cloisonnement entre ingénierie et data science, qui mène à un modèle "jeté par-dessus le mur", découvert inadapté trois mois plus tard, obligeant à tout recommencer. Il faut selon lui des profils capables de tenir les deux perspectives à la fois, pour arbitrer en temps réel les compromis de construction. Il mentionne à ce titre une formation qu'il co-anime avec Hugo Bowne-Anderson sur la construction d'agents et de systèmes de retrieval, destinée à ne pas éluder la dimension recherche/search dans l'apprentissage de l'IA.

## Pourquoi ça compte

Ce texte rappelle utilement, pour une veille tech IA, que les fondamentaux du search (évaluation rigoureuse, qualité du retrieval, structuration des métadonnées) restent le principal levier de qualité des systèmes RAG — un point souvent négligé au profit du choix du modèle ou du prompt.
