---
title: "Harness affects cost more than correctness"
date: 2026-09-18
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Farena.ai%2Fblog%2Fcoding-agents-harness-tax%3Futm_source=tldrai/1/010001a0af8f638d-dcc57c6a-1a9b-4a37-be52-1a8f5d78e44e-000000/TDH-pKFkluvepNoNbYToNK_qtaaRpWfn1MDGTKC-kUk=452"
keywords: ["agents de codage", "harnais logiciel", "benchmark", "coût", "open source", "Claude Code"]
theme: "IA"
tone: "research"
used_in: ["2026-09-18"]
---

## Résumé
Cet article de blog (Arena.ai, relayé par la newsletter TLDR AI) évalue 21 combinaisons modèle-harnais (7 modèles x 3 harnais : Claude Code, Codex CLI, Pi) sur les benchmarks SWE-bench Lite et Terminal-Bench 2.0. Il montre que le choix du harnais a un effet marginal sur le taux de réussite des tâches mais peut faire varier le coût jusqu'à un facteur 5 pour un même modèle. Pi, un harnais minimaliste et open source limité à quatre outils, se révèle aussi performant que des harnais propriétaires plus complexes comme Claude Code, et les modèles obtiennent parfois de meilleurs résultats en dehors du harnais de leur propre fournisseur. Les auteurs baptisent ce surcoût caché la « harness tax » (taxe du harnais) et appellent à des harnais capables de s'adapter automatiquement plutôt qu'à un choix manuel.

## Points clés
- Le choix du harnais fait peu varier le taux de réussite (±2 % sur SWE-bench Lite, ±5 % sur Terminal-Bench 2.0) mais peut multiplier le coût par un facteur allant jusqu'à 5 pour un même modèle.
- Claude Code coûte environ 1,5 à 2 fois plus cher que Pi ou Codex pour des performances globalement équivalentes sur les deux benchmarks testés.
- Pi, un harnais open source minimal (seulement quatre outils : read, write, edit, bash), atteint la frontière de Pareto coût/performance sur les deux benchmarks.
- Le contexte initial de Claude Code est plus de 10 fois supérieur à celui de Pi, ce qui alourdit le coût dès le tout premier appel au modèle.
- Dans 9 comparaisons sur 12, un harnais alternatif au harnais du fournisseur du modèle obtient le meilleur taux de réussite (ex. : Sonnet 4.6 performe mieux sous Codex que sous Claude Code).
- Les résultats se limitent à deux benchmarks open source potentiellement vus pendant l'entraînement des modèles ; ils pourraient ne pas se généraliser à tous les flux de travail réels.

## Analyse approfondie

### Contexte et question de recherche
Les auteurs partent du constat que les modèles de langage transforment le développement logiciel, mais que ce sont les agents de codage qui mettent cette intelligence au travail, par l'intermédiaire d'un « harnais » (harness) : le système logiciel qui orchestre les outils, le contexte et l'exécution des tâches autour du modèle. Si le modèle fournit l'intelligence brute, le harnais détermine de plus en plus l'efficacité avec laquelle cette intelligence est réellement exploitée. Choisir un agent de codage revient donc toujours à choisir un couple modèle + harnais, même quand on croit ne comparer que des modèles. Or, alors que des millions de personnes utilisent déjà des agents de codage au quotidien, l'effet propre du harnais reste mal documenté. C'est la question posée par l'étude : à modèle égal, un harnais différent permettrait-il de résoudre davantage de tâches, ou de réduire les coûts ?

Pour y répondre, les auteurs testent 21 paires modèle-harnais (7 modèles croisés avec Claude Code, Codex CLI et Pi) sur deux benchmarks open source de référence, SWE-bench Lite et Terminal-Bench 2.0, et en tirent trois constats principaux, détaillés ci-dessous.

### 1. Le harnais pèse surtout sur le coût, peu sur la réussite
Premier constat : un même modèle atteint souvent un taux de réussite comparable quel que soit le harnais utilisé, mais à des coûts très différents. Sur les deux benchmarks, GPT-5.6 Luna est le moins coûteux, Claude Fable 5 obtient le meilleur taux de réussite sur SWE-bench Lite, et le modèle à poids ouverts Kimi K3 se situe proche de la frontière de Pareto. Mais pour un modèle donné, la variation entre harnais reste faible : Claude Fable 5 résout 97,8 % des tâches sous Claude Code contre 96,7 % sous Codex et sous Pi — un écart de réussite négligeable — alors que Claude Code coûte environ deux fois plus cher que Pi pour ce même modèle (1,33 $ contre 0,67 $ par tâche en moyenne).

Cet écart de coût se retrouve systématiquement : en moyenne géométrique sur l'ensemble des modèles partagés entre harnais, Claude Code coûte environ 2 fois plus cher que Pi et 1,6 fois plus cher que Codex sur SWE-bench Lite, et 1,5 fois plus cher que Pi sur Terminal-Bench 2.0. Dans le même temps, l'effet moyen du harnais sur le taux de réussite reste contenu (±2 % sur SWE-bench Lite, ±5 % sur Terminal-Bench 2.0). Les auteurs résument ce surcoût, payé pour une qualité quasiment identique, par l'expression « harness tax » (taxe du harnais) : une dépense cachée que l'on accepte implicitement en utilisant le harnais par défaut d'un agent de codage sans le comparer à des alternatives. Leur recommandation : toute évaluation de modèle devrait systématiquement comparer coût et taux de réussite à travers plusieurs harnais, et pas seulement à travers plusieurs modèles.

### 2. Un harnais simple peut suffire
Deuxième constat : Pi, un harnais open source réduit à quatre outils seulement (lecture, écriture, édition de fichiers et exécution de commandes shell), atteint la frontière de Pareto coût/performance sur les deux benchmarks — preuve qu'une architecture minimale peut rivaliser avec des harnais bien plus riches en fonctionnalités.

En creusant le nombre de tours d'interaction, les auteurs montrent que des agents peuvent produire un nombre de tours quasi identique pour des coûts très différents : sur SWE-bench Lite, Fable 5 met en moyenne 15,4 tours sous Pi contre 15,3 sous Claude Code, mais ce dernier coûte environ deux fois plus cher pour un gain de réussite de seulement 1,1 point — donc une dépense bien plus élevée par tour, même si la définition d'un « tour » diffère selon les harnais.

Une part de cet écart se joue dès le premier appel : sur les sept modèles testés, le contexte initial moyen envoyé par Claude Code est plus de dix fois supérieur à celui de Pi, du fait d'instructions système plus longues et de schémas d'outils plus volumineux. Ce contexte plus lourd renchérit directement le coût, même si la facture totale dépend aussi de la mise en cache, du volume de tokens générés et des appels suivants. Pour les auteurs, ces résultats ouvrent un espace de recherche pour des harnais open source : on peut égaler l'état de l'art sans disposer d'un harnais propriétaire ni co-entraîner le modèle avec lui, la complexité d'un harnais devant être vue comme un compromis à arbitrer empiriquement plutôt que comme une qualité en soi.

### 3. Un modèle performe parfois mieux hors du harnais de son propre fournisseur
Troisième constat, le plus contre-intuitif : être optimisé par son fournisseur ne garantit pas le meilleur résultat. OpenAI présente par exemple GPT-5-Codex comme spécifiquement optimisé pour l'ingénierie logicielle dans Codex. Pourtant, sur les six modèles Anthropic et OpenAI testés et les deux benchmarks, c'est un harnais tiers qui obtient le meilleur taux de réussite observé dans neuf comparaisons sur douze.

Le phénomène ne se limite pas aux modèles haut de gamme : Sonnet 4.6 résout 68,9 % des tâches sous Codex contre 66,7 % sous Claude Code sur SWE-bench Lite, à coût comparable. GPT-5.6 Sol fait de même hors de son propre harnais : sur Terminal-Bench 2.0, il atteint 83,3 % de réussite sous Pi contre 78,9 % sous Codex, pour environ moitié moins cher (0,42 $ contre 0,76 $). Les auteurs en concluent que les capacités d'un modèle sont largement transférables d'un harnais à l'autre, et qu'appartenir au même fournisseur que le modèle n'est pas un gage de meilleure compatibilité. La question qui compte reste, selon eux, purement empirique : quel harnais offre le meilleur équilibre coût/réussite pour un modèle et une tâche donnés.

### Limites et perspectives
Les auteurs rappellent que leurs conclusions portent sur deux benchmarks open source que les modèles ont pu croiser pendant leur entraînement, et pourraient ne pas se généraliser à d'autres charges de travail. Ils relient ce travail à leurs recherches antérieures sur le choix conjoint de modèles et de configurations système, et estiment que la sélection du harnais devient un enjeu d'autant plus pressant que l'usage des agents de codage se généralise. La suite logique, selon eux, est d'évaluer et d'automatiser ce choix de harnais directement dans des flux de développement réels, où les besoins évoluent, où les développeurs donnent leur avis, et où les tâches s'étalent sur plusieurs sessions.

Plus largement, ils distinguent deux régimes d'usage. Pour les tâches courantes, l'agent de codage n'est qu'une interface vers l'intelligence du modèle (gestion du contexte, accès aux outils, exécution) ; à mesure que les modèles progressent, il pourrait avoir besoin de moins d'échafaudage, ce qui plaide pour des harnais généralistes priorisant coût et fiabilité plutôt que des fonctionnalités superflues. Pour les problèmes les plus difficiles, en revanche — à la frontière des capacités du modèle, comme la découverte scientifique — un harnais plus structuré, capable de guider l'exploration d'idées, l'évaluation de candidats et l'apprentissage par le retour, garde tout son intérêt. Leur conclusion : l'utilisateur ne devrait pas avoir à arbitrer lui-même entre ces configurations — l'objectif final est un harnais capable de s'adapter à la tâche en cours tout en restant généraliste.

### Méthode, remerciements et sources
L'étude, publiée sous le nom de projet « HarnessTax », a bénéficié de crédits de calcul AWS (Amazon AI Fellowship), d'un accès API sponsorisé par Arena Intelligence et de crédits API Anthropic fournis par Laude, ainsi que du soutien de plusieurs partenaires industriels du laboratoire (Accenture, AMD, Anyscale, Broadcom, Google, IBM, Intel, Intesa Sanpaolo, Lambda, Mibura, Samsung SDS, SAP). L'article s'appuie sur quinze références, notamment des travaux d'Anthropic et d'OpenAI sur leurs propres agents de codage (Claude Code, Codex), les benchmarks SWE-bench Lite et Terminal-Bench 2.0, et un billet de Portkey qui a popularisé l'expression « harness tax ».

## Pourquoi ça compte
Cette étude invite les équipes qui construisent ou évaluent des agents de codage à comparer plusieurs harnais plutôt que d'accepter par défaut l'outillage du fournisseur du modèle, car la « taxe du harnais » peut doubler les coûts sans gain de performance mesurable. C'est un signal utile pour toute veille sur les outils IA de développement : la vraie différenciation se joue autant sur l'ingénierie du harnais que sur le modèle sous-jacent.
