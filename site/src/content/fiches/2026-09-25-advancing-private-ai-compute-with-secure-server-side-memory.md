---
title: "Advancing Private AI Compute with secure, server-side memory"
date: 2026-09-25
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fdeepmind.google%2Fblog%2Fadvancing-private-ai-compute-with-secure-server-side-memory%3Futm_source=tldrai/1/010001a0d39de058-f2e9d4a8-3e40-48b5-87bf-69a22915a201-000000/Aa0wv3rkshCHSWCsXw6MdSHjfh-ef8RqsuejpEzpXCw=452"
keywords: ["confidentialité", "mémoire IA", "Google DeepMind", "chiffrement", "cloud sécurisé", "enclave sécurisée"]
theme: "IA"
tone: "news"
used_in: ["2026-09-25"]
---

## Résumé
Google DeepMind annonce une évolution de son architecture Private AI Compute permettant une mémoire persistante et multi-appareils pour les assistants IA, tout en conservant des standards de confidentialité proches du traitement sur l'appareil. Le système repose sur un « coffre-fort numérique » chiffré dans le cloud, dont les clés de déchiffrement restent exclusivement sur les appareils de l'utilisateur. L'objectif est de résoudre un dilemme classique de l'IA moderne : offrir une continuité de mémoire à long terme entre appareils sans sacrifier la confidentialité des données. Techniquement, cela passe par un canal chiffré de bout en bout reliant l'appareil à une enclave sécurisée isolée dans le cloud.

## Points clés
- Google DeepMind introduit une couche de mémoire persistante côté serveur pour son architecture Private AI Compute.
- Les données utilisateur sont stockées de façon chiffrée dans le cloud, mais les clés de déchiffrement restent uniquement sur les appareils personnels de l'utilisateur.
- Même Google n'a pas accès aux données déchiffrées, selon l'article.
- Le mécanisme repose sur une « enclave sécurisée » : un environnement isolé qui déchiffre temporairement les données en mémoire pour traiter une requête, puis les re-chiffre immédiatement.
- L'objectif affiché est de permettre une continuité de l'assistant IA à travers plusieurs appareils, sans compromettre les standards de confidentialité habituellement réservés au traitement local.

## Analyse approfondie
Une mise à jour technique sur notre architecture Private AI Compute, qui permettra une mémoire IA persistante et multi-appareils avec des standards de confidentialité proches du traitement sur l'appareil.

L'IA devient de plus en plus capable et intuitive — se souvenant de ce qui compte, comprenant le monde qui vous entoure, et agissant selon vos directives. La confidentialité et la confiance sont au cœur de ce qui rend cela possible, garantissant que vos données restent privées et protégées à mesure que les systèmes d'IA évoluent pour offrir une assistance plus continue sur l'ensemble de vos appareils.

Aujourd'hui, nous partageons la manière dont nous allons apporter une mémoire privée, côté serveur, à notre plateforme Private AI Compute. Cette avancée résout un dilemme de longue date de l'IA moderne : comment offrir à un assistant une continuité à long terme entre les appareils tout en respectant les standards de confidentialité stricts, habituellement réservés au traitement sur l'appareil.

### Apporter la confidentialité de l'appareil à la mémoire à l'échelle du cloud

Avec cette nouvelle capacité technique, une nouvelle couche de mémoire persistante pourra fonctionner comme un coffre-fort numérique sécurisé dans le cloud. Selon ce modèle, les informations nécessaires pour vous assister sont scellées dans un espace de stockage dédié et chiffré, tandis que les clés cryptographiques nécessaires pour le déverrouiller sont détenues exclusivement sur vos appareils personnels — garantissant que vos données restent inaccessibles à quiconque, y compris Google.

Le schéma ci-dessous montre comment cette mise à jour de Private AI Compute fonctionnera. Lorsqu'un modèle d'IA a besoin d'accéder à des informations pour vous assister, un canal authentifié et chiffré de bout en bout relie votre appareil à un environnement protégé et isolé dans le cloud. Cet espace, ou « enclave sécurisée », déchiffre temporairement vos données en mémoire isolée pour traiter la requête, enregistre tout nouveau contexte, puis le chiffre immédiatement, préservant la confidentialité de vos informations comme si elles n'avaient jamais quitté votre appareil.

## Pourquoi ça compte
Cette annonce illustre une tendance de fond chez les grands acteurs de l'IA : concilier mémoire persistante multi-appareils et confidentialité renforcée, un enjeu clé pour l'adoption grand public des assistants IA de nouvelle génération.
