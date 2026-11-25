---
title: "Claude Ship - Claude Code Docs"
date: 2026-11-25
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fcode.claude.com%2Fdocs%2Fen%2Fclaude-ship%3Futm_source=tldrai/1/010001a20df2eb5b-9b2d6378-b8a0-4ed3-b906-b3c3c735d4f3-000000/yIbAwxP4G098RmidmKrMQse8WHfTXJP_wkL4EMCFWZw=452"
keywords: ["Claude Ship", "revue de code automatisée", "CI/CD", "GitHub", "politique d'approbation", "agents IA"]
theme: "IA"
tone: "tutorial"
used_in: ["2026-11-25"]
---

## Résumé
Claude Ship est une suite de trois agents IA intégrés aux pull requests (Code Review, PR Steward, Claude Approvals) destinée à automatiser la revue de code, le traitement des retours et l'application de politiques d'approbation. Réservée aux organisations sous plans Team et Enterprise, elle s'active agent par agent par un Owner, Code Review étant disponible en version stable (GA) tandis que PR Steward et Claude Approvals restent en bêta publique. La facturation se fait séparément via les crédits d'usage de l'organisation, en fonction de la consommation de tokens, et certaines configurations de sécurité (Zero Data Retention, HIPAA, clés de chiffrement gérées par le client) en excluent l'usage.

## Points clés
- Trois agents distincts : Code Review (détecte erreurs de logique, failles de sécurité, cas limites cassés), PR Steward (traite les retours de revue et les checks en échec), Claude Approvals (évalue les pull requests selon une politique écrite par l'organisation).
- Activation recommandée un agent à la fois, dans l'ordre : Code Review, puis PR Steward (en commençant en mode manuel via `@claude steward`), puis Claude Approvals.
- La politique Claude Approvals est définie dans un fichier `.claude/approvals.yml` du dépôt ; un mode observation (facturé) permet de voir les décisions de la politique sans les appliquer.
- Disponible uniquement pour les organisations sous plans Team et Enterprise, exclue pour celles en Zero Data Retention, configuration HIPAA ou avec clés de chiffrement gérées par le client.
- Facturation séparée du plan de base, par agent, sur la consommation de tokens ; Approvals facture en plus les exécutions de classificateur.
- Désactiver Approvals avant Code Review, car une politique active peut déclencher des revues facturées même si Code Review est éteint.

## Analyse approfondie
- Code Review : recherche des problèmes tels que des erreurs de logique, des vulnérabilités de sécurité et des cas limites défaillants
- PR Steward : traite les retours de revue et les checks en échec
- Claude Approvals : vérifie les pull requests par rapport à une politique d'approbation que vous rédigez

Claude Ship utilise l'IA et peut passer à côté de bugs, de vulnérabilités de sécurité ou d'autres problèmes.

**Paramètres de l'organisation > Claude Ship** pour les réglages de Claude Ship. Un rôle Owner est nécessaire. Activez un agent à la fois, sur un seul dépôt, dans cet ordre :

1. Configurez Code Review
2. Configurez PR Steward. Pour le réglage qui choisit quand PR Steward démarre, commencez par **Manuel (@claude steward)**. PR Steward n'a pas de limite de dépense propre jusqu'à ce que vous en définissiez une.
3. Configurez Claude Approvals. Un fichier de politique dans le dépôt le déclenche, donc vérifiez qui peut l'activer. Commencez en mode observation, où le check **Claude Approvals** rapporte ce que votre politique déciderait. Le mode observation est facturé. Consultez le coût d'Approvals.

**Paramètres de l'organisation > Claude Ship**. Un fichier de politique Claude Approvals,

`.claude/approvals.yml`, modifie quelles pull requests Code Review examine automatiquement. Une fois le fichier présent sur la branche par défaut, en mode observation ou appliqué, les revues automatiques s'arrêtent normalement là où aucune règle correspondante ne nomme `claude/code_review`. Pour les conserver, ajoutez `claude/code_review` à une règle.
Claude Ship est destiné aux organisations sous plans Team et Enterprise.
Code Review est disponible en version générale (GA). PR Steward et Claude Approvals sont en bêta publique. Les agents ne sont pas disponibles pour les organisations ayant activé la Zero Data Retention, la configuration HIPAA, ou des clés de chiffrement gérées par le client. Approvals comporte davantage de limites.
Chaque agent est facturé selon l'usage de tokens via les crédits d'usage de votre organisation, séparément de l'usage inclus dans votre plan. Approvals facture les exécutions du classificateur ainsi que les Code Reviews que la politique demande.
**Paramètres de l'organisation > Usage** : un agent activé continue de fonctionner et de facturer votre organisation. Pour arrêter ces frais, suivez la procédure pour désactiver Claude Ship. Consultez les coûts de chaque agent : désactivez Approvals avant Code Review, car une politique peut déclencher des revues facturées alors même que Code Review est désactivé. Ces étapes laissent actives les

commandes `/ship` et `/steward`. Consultez comment les désactiver.
- GitHub Actions et GitLab CI/CD : exécutez Claude Code dans votre propre CI
- Revue de code en local : obtenez une revue dans votre terminal avant de pousser

## Pourquoi ça compte
Ce document illustre la montée en puissance des agents IA directement intégrés aux workflows de pull request (revue, suivi des retours, politiques d'approbation), un axe clé de la veille sur l'automatisation DevOps assistée par IA. Il est aussi révélateur des contraintes de gouvernance (facturation séparée, exclusions pour ZDR/HIPAA) que les organisations doivent anticiper avant d'adopter ces outils.
