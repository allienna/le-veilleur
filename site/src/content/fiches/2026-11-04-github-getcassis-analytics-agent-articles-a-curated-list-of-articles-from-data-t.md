---
title: "GitHub - GetCassis/analytics-agent-articles: A curated list of articles from data teams building analytics agents."
date: 2026-11-04
url: "https://elink56e.dataelixir.com/ss/c/u001.Dt8L-Y0jq6TkmYqlU8wlZHAAch_peQXCBamlelfZNvT1blwGGeg1orn216O-FWrFjg4YrvnCiE4qVXyusUlIswt0h2x8MRgB_wfz71RJBofAdd_zOHiTdbalqWHdX2UJeaZZYFOVm_0a8d4WVdvLi2R7WvintC5sZY6SXUBZcOq0GbVwn4B3wSlf-eWuZOswZjvuqcA1wFUSubKepjH3r6uytJ71RJG7oIrrFTfcd_jlmUS3olW8339Inf4KRrxZZF-8YtrJQ1MoqGxR9z9vYw/4vf/9_2zRaPmRUOeF_YxJ4YDRg/h12/h001.UFc86A_ahQlyJGCPnl3ZrQjK7WCbLYvtKogckWhyZ1c"
keywords: ["agents analytiques", "context engineering", "data", "IA", "dbt", "benchmark"]
theme: "Data"
used_in: ["2026-11-04"]
---

## Résumé
Ce dépôt GitHub « analytics-agent-articles » est une liste organisée d'articles publiés par des équipes data (Anthropic, OpenAI, Ramp, Cloudflare, DoorDash, Meta, Uber, LinkedIn, entre autres) qui documentent la construction d'agents analytiques internes. La ressource classe les lectures par problème pratique rencontré (donner du contexte à l'agent, tester les réponses, corriger les erreurs, réduire coût et latence, favoriser l'adoption) et met en avant trois lectures prioritaires : Anthropic, OpenAI et Ramp. Elle recense également des implémentations côté éditeurs (Cube, Omni, Cassis, Lyft), des benchmarks publics (ClickHouse, Benchouse) et un compte-rendu du dbt Summit 2026. Le dépôt est collaboratif : les contributions externes (nouveaux liens, corrections) y sont explicitement encouragées.

## Points clés
- Ressource agrégée sur GitHub recensant les retours d'expérience de nombreuses équipes data construisant des agents analytiques internes.
- Trois lectures prioritaires identifiées : Anthropic (self-service analytics, juin 2026), OpenAI (agent de données interne, janvier 2026), Ramp (agent construit autour d'un projet dbt existant, octobre 2025).
- Classement thématique par problème concret : contexte, tests des réponses/modèles, correction d'erreurs, coût/latence, adoption par les utilisateurs.
- Présence de benchmarks publics comparatifs, dont le ClickHouse Agentic Analytics Benchmark (201 questions réelles, notation par jury de modèles) et Benchouse.
- Implémentations détaillées côté éditeurs (Cube, Omni, Cassis, Lyft) couvrant l'ingénierie de contexte et le passage en production.
- Dépôt ouvert aux contributions communautaires pour ajouter ou corriger des liens.

## Analyse approfondie
Une liste organisée d'articles d'équipes data qui construisent des agents analytiques.

Lectures recommandées en premier · Constructions internes · Parcourir par problème · Lectures complémentaires · Contribuer

1. **Anthropic — Comment une équipe fait fonctionner l'analytique en self-service.** Skills, définitions de métriques, documentation et évaluations (juin 2026), incluant comment l'équipe les maintient à jour à mesure que les modèles de données évoluent.
2. **OpenAI — À l'intérieur d'un agent de données interne.** L'architecture derrière la préparation du contexte, la récupération, les permissions et les évaluations (janvier 2026).
3. **Ramp — En construire un autour d'un projet dbt existant.** Exemples SQL et Jinja pour les tables de contexte et la documentation métier (octobre 2025).

Lisez un article directement depuis la colonne de droite, ou cliquez sur une entreprise pour accéder à ses notes de lecture complètes. Les dates sont les dates de publication ; les stacks reflètent ce que les auteurs utilisaient à l'époque.

- **Donner du contexte à l'agent :** Ramp, Gorgias, AngelList, Astronomer, Bitrise, BlaBlaCar, Cloudflare, DoorDash, incident.io, Meta, OpenAI.
- **Tester les réponses et les changements de modèle :** Gorgias, Anthropic, ClickHouse, DoorDash, Ramp, LinkedIn, Meta, Uber.
- **Corriger les erreurs et maintenir le contexte à jour :** Bitrise, DoorDash, GitHub, Gorgias, incident.io, Meta, Replit, Astronomer.
- **Réduire le coût et la latence :** Cloudflare, DoorDash, Gorgias, Vercel.
- **Favoriser l'adoption par les utilisateurs :** Alan, Astronomer, Bitrise, Faire, incident.io, Ramp, LinkedIn, Meta.

Ingénierie produit, études techniques, benchmarks et comptes-rendus de conférences qui complètent les retours d'expérience internes.

- Cube : Construire un harnais d'analytique agentique · `Implémentation éditeur`. Erreurs, limites de résultats et outils respectant les permissions. Stack et notes.
- Omni : Benchmarker le harnais d'analytique agentique d'Omni · `Implémentation éditeur`. Tester la qualité, la latence et le coût sur une charge de travail analytique d'un éditeur. Stack et notes.
- Cassis : Votre contexte de données doit être débogable · `Implémentation éditeur`. Organiser le contexte en arbre de domaines métier afin qu'une règle manquante puisse être retracée jusqu'au tour qui l'a omise. Stack et notes.
- Cassis : Comment assembler le contexte des agents analytiques à partir de vos actifs existants · `Implémentation éditeur`. Construire le premier contexte à partir des actifs de données existants, avec un kit de démarrage open source. Stack et notes.
- Cassis : L'ingénierie du contexte pour les agents analytiques · `Implémentation éditeur`. Comment structurer les tables, métriques et règles métier pour qu'un agent puisse trouver ce dont il a besoin. Stack et notes.
- Lyft : Du jour 1 à la production · `Ingénierie de production`. Faire passer un agent analytique existant d'un prototype Streamlit à une application interne authentifiée et observable. Stack et notes.
- ClickHouse : Le benchmark de l'analytique agentique · `Benchmark`. Un harnais réutilisable construit à partir de 201 questions réelles, avec notation par jury de modèles, mesure du coût et de la latence, et contrôles de contamination. Code · Notes.
- Benchouse : Le benchmark des agents analytiques · `Benchmark`. Comparer la précision, l'exhaustivité, la retenue et le coût par question entre agents analytiques. Notes.
- Cassis : Les agents analytiques au dbt Summit 2026 · `Compte-rendu de conférence`. Où les 40 sessions du sommet sur les agents analytiques et le contexte se sont accordées, où les équipes diffèrent encore, et ce que les présentations ont laissé en suspens. Notes.

Vous connaissez une équipe qui a documenté sa construction interne ? Ouvrez une issue ou une pull request avec le lien et une phrase expliquant ce qui la rend utile. Consultez le guide de contribution pour le format. Les corrections et signalements de liens cassés sont également bienvenus.

## Pourquoi ça compte
Cette ressource offre une cartographie rapide de l'état de l'art en matière d'agents analytiques d'entreprise (ingénierie du contexte, évaluation, coûts, adoption), un point d'entrée précieux pour toute veille sur l'IA appliquée à la donnée en 2026.
