---
title: "RRSI: Regularized Recursive Self-Improvement of Agent Harnesses"
date: 2026-09-24
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fregularized-rsi.com%2F%3Futm_source=tldrai/1/010001a0ce763902-fbdaa478-8730-42a8-88e8-8ed14055d5a1-000000/dcGujPIeQizYnCkpgNBoRBeUm8mM6G2Tf0rXS8PMRf4=452"
authors: ["Peng Xia", "Rujun Han", "Zifeng Wang", "Yanfei Chen", "Yufan Zhuang", "Yoonho Lee", "Chengsong Huang", "Han Yu", "Zhongying CuiZhu", "Yifei Ming", "Huaxiu Yao", "Burak Gokturk", "Tomas Pfister", "Chen-Yu Lee"]
keywords: ["auto-amélioration récursive", "harnais d'agents", "benchmark hors distribution", "régularisation", "Claude Opus 4.8", "overfitting"]
theme: "IA"
tone: "research"
used_in: ["2026-09-24"]
---

## Résumé
RRSI (Regularized Recursive Self-Improvement) est une méthode qui fait évoluer automatiquement des harnais d'agents IA tout en évitant le piège classique du sur-ajustement au benchmark d'entraînement. Contrairement aux méthodes antérieures, dont les gains obtenus sur le split d'évolution s'effondrent (voire deviennent négatifs) une fois testés hors distribution, RRSI est la seule approche dont les gains se maintiennent et même augmentent sur des benchmarks jamais vus. Le système repose sur une boucle d'édition contrainte — proposeur à budget décroissant, critique anti-fuite, porte de validation statistique et rentabilité en tokens — plutôt que sur une liberté totale d'édition du harnais. Testé avec Claude Opus 4.8 comme politique, RRSI dépasse la moyenne des méthodes antérieures de jusqu'à 22,9 % tout en produisant le harnais le plus économe en tokens.

## Points clés
- RRSI est la seule méthode testée dont le gain de performance croît hors distribution au lieu de s'effondrer une fois le benchmark changé.
- Le mécanisme central régularise la *recherche* (la boucle d'édition) plutôt que le harnais lui-même : budget d'édition décroissant, filtrage des fuites par un critique, et une porte qui n'admet un candidat que si le gain dépasse le bruit de mesure et reste rentable en tokens.
- Les éléments spécifiques au benchmark (noms de tâches, entités, réponses, logique ad hoc) sont rejetés avant même la notation, pour empêcher toute triche.
- Deux règles agissent directement sur le coût : refus de toute croissance non rentabilisée dès sa proposition, et élagage des composants devenus improductifs — deux garde-fous absents des méthodes antérieures.
- RRSI produit le harnais évolué le plus léger en tokens par essai, et le seul à dépasser le harnais de base (H0) de plus d'un point hors distribution.
- Chaque candidat est journalisé (hypothèse, diff, score, variation de coût), ce qui permet au proposeur de capitaliser sur les réussites et d'arrêter de retester les échecs.

## Analyse approfondie
### Les harnais évolués sur-ajustent au benchmark sur lequel ils sont notés. RRSI, lui, transfère.
RRSI améliore chaque benchmark hors distribution sans sur-ajuster au split sur lequel il évolue. Les méthodes antérieures font l'inverse : de larges gains sur l'ensemble d'évolution qui rétrécissent ou disparaissent dès que le benchmark change, deux d'entre elles terminant même en dessous du harnais dont elles sont parties.

**(a)** Gain sur le split d'évolution comparé au gain hors distribution, un point par méthode. RRSI est la seule méthode dont le gain augmente hors distribution.

**(b–d)** Scores de test pour le harnais non évolué H0, la moyenne des méthodes antérieures et RRSI. RRSI dépasse la moyenne antérieure de jusqu'à 22,9 %.

### Régulariser la recherche, pas le harnais
Chaque composant du harnais reste modifiable. RRSI contraint la boucle qui l'édite : l'ampleur autorisée pour une proposition, et quels gains mesurés ont le droit de rester.

**Un round de RRSI.** Le proposeur dépense un budget d'édition décroissant et lit le journal complet ; le critique filtre les fuites avant toute notation ; la porte n'admet un candidat que s'il dépasse le seuil de bruit et rentabilise ses tokens. Schématique ; les rounds réels se trouvent dans l'explorateur ci-dessous.

Les premiers rounds peuvent regrouper quelques éditions coordonnées pour identifier un mécanisme ; les rounds tardifs se limitent à un seul changement attribuable.

Chaque candidat est journalisé avec son hypothèse, son diff, son score et sa variation de coût, de sorte que le proposeur s'appuie sur ce qui a fonctionné et cesse de retester ce qui a échoué.

Quand la progression stagne dans la bande de bruit, le budget est redirigé vers les composants que le run n'a jamais touchés.

Les noms de tâches, entités, réponses ou toute logique spécifique au benchmark sont rejetés avant même qu'un candidat ne soit noté.

Un gain doit dépasser la variance mesurée sur le harnais de base inchangé.

Les tokens d'inférence supplémentaires doivent être compensés par un gain mesuré.

Les composants qui cessent de mériter leur place sont signalés pour suppression.

### Chaque benchmark de test s'améliore
Évoluer sur une suite par domaine, puis exécuter le harnais sans modification partout ailleurs. Mêmes outils, juge, essais et fenêtre que H0 ; la politique utilisée est Claude Opus 4.8.

**Moins cher, aussi.** Tokens de politique par essai pour chaque harnais final, comparés à sa moyenne hors distribution. RRSI est le harnais évolué le plus léger, et le seul à dépasser H0 de plus d'un point.

#### Deux règles agissent directement sur le coût
La règle de coût refuse toute croissance qui n'est pas rentabilisée au moment où elle est proposée ; l'élagage supprime la croissance qui a cessé d'être rentable depuis. Aucune méthode antérieure ne comporte l'une ou l'autre de ces règles.

### Observer le harnais évoluer, round par round
Quatre runs réels, chaque candidat : ce qu'il a proposé, ce qu'a dit le critique, pourquoi la porte l'a gardé ou rejeté, et le diff exact. Cliquez sur n'importe quel élément ; utilisez ← / → pour naviguer.

#### Comment le harnais s'est adapté, et ce que les régularisateurs ont bloqué entre-temps

### BibTeX
```
@article{xia2026rrsi,
  title={RRSI: Regularized Recursive Self-Improvement of Agent Harnesses},
  author={Xia, Peng and Han, Rujun and Wang, Zifeng and Chen, Yanfei and Zhuang, Yufan and Lee, Yoonho and Huang, Chengsong and Yu, Han and CuiZhu, Zhongying and Ming, Yifei and Yao, Huaxiu and Gokturk, Burak and Pfister, Tomas and Lee, Chen-Yu},
  journal={arXiv preprint arXiv:2609.24972},
  year={2026}
}
```

## Pourquoi ça compte
Ce travail apporte une réponse méthodologique concrète à un problème central de l'auto-amélioration récursive des agents IA : le sur-ajustement aux benchmarks d'évaluation. Pour la veille tech, c'est un signal important sur la manière dont les équipes de recherche commencent à outiller la fiabilité et la généralisation des systèmes d'agents auto-évolutifs, plutôt que de se contenter de scores impressionnants mais non transférables.
