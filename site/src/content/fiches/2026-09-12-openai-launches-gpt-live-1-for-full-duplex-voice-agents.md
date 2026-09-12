---
title: "OpenAI launches GPT-Live-1 for full-duplex voice agents"
date: 2026-09-12
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.testingcatalog.com%2Fopenai-launches-gpt-live-1-for-full-duplex-voice-agents%2F%3Futm_source=tldrai/1/010001a090aa182a-d18dee2c-9abe-499b-abe2-6b2b9843ff74-000000/IovTzFtV-m9BviPmP-S5xFEbczjUanvXNIb4NYHJSGI=452"
keywords: ["OpenAI", "agents vocaux", "full-duplex", "API", "voix synthétique", "latence"]
theme: "IA"
tone: "news"
used_in: ["2026-09-12"]
---

## Résumé
OpenAI a lancé GPT-Live-1 dans son API, un modèle vocal full-duplex capable d'écouter et de parler simultanément, sans passer par la chaîne traditionnelle reconnaissance vocale → raisonnement → synthèse vocale. Les premiers retours font état d'une forte baisse des interruptions et de gains mesurés sur des benchmarks dédiés, avec des clients comme Speak, Yelp Host, Fin d'Intercom et Devin de Cognition. Le modèle est facturé 0,05$ par minute, propose 12 voix au lancement, et s'inscrit dans une stratégie où OpenAI sépare la couche vocale de la pile de raisonnement.

## Points clés
- Traitement audio simultané (full-duplex) plutôt qu'un enchaînement classique ASR → LLM → TTS
- Speak rapporte près de 80% d'interruptions en moins qu'avec les systèmes précédents basés sur les tours de parole
- +30 points de pourcentage sur le Full Duplex Bench face à GPT-Realtime-2.1 ; premier rang sur Tau3 avec GPT-6 Astra
- Un client a réduit sa base de code vocale de 80% (23 000 lignes en moins) pour des conversations patients en temps réel
- Tarification à 0,05$/minute, 12 voix disponibles, voix personnalisées sur demande commerciale
- OpenAI dirige les cas d'usage entreprise plus complexes vers son offre Presence

## Analyse approfondie
OpenAI a lancé GPT-Live-1 dans son API, apportant aux développeurs qui construisent des applications vocales et des workflows métier le modèle vocal naturel introduit pour la première fois dans ChatGPT. Le modèle écoute et parle en même temps, gère les interruptions et les accusés de réception au fur et à mesure qu'ils se produisent, et peut maintenir une conversation fluide pendant qu'un raisonnement plus poussé ou des actions s'exécutent via des modèles et outils associés tels que GPT-6 Astra, Codex et ChatGPT Work.

Contrairement aux agents vocaux traditionnels qui enchaînent reconnaissance vocale, modèle de raisonnement et synthèse vocale, GPT-Live-1 traite conjointement l'audio entrant et sortant. Selon OpenAI, cela évite la latence et les transitions fragiles susceptibles de faire perdre le timing, le contexte et le rythme conversationnel. Les développeurs peuvent contrôler le ton, le rythme et le style via le system prompt, choisir leur propre modèle backend et leur propre agent harness, et utiliser les transcriptions ASR, le texte de réponse, le biaisage par mots-clés (keyword biasing), la reconnaissance alphanumérique et la détection native des tours de parole (turn detection). La prise en charge de la téléphonie vise les réservations, le suivi de commandes et le service client, le modèle étant conçu pour gérer le bruit de fond et les silences sans parler par-dessus les utilisateurs ni narrer chaque étape.

Les premiers résultats indiquent un changement net dans la gestion des tours de parole. Speak rapporte près de 80% d'interruptions en moins par rapport aux systèmes précédents basés sur les tours de parole, laissant plus de temps de réflexion aux apprenants de langues. Selon OpenAI, GPT-Live-1 a gagné 30 points de pourcentage par rapport à GPT-Realtime-2.1 sur le Full Duplex Bench et s'est classé premier sur Tau3 lorsqu'il est associé à GPT-6 Astra avec un effort de raisonnement moyen. Parmi les premiers utilisateurs figurent Yelp Host, Speak, Fin d'Intercom et Devin de Cognition. Un client a indiqué que le passage d'un système en cascade à GPT-Live-1 avait réduit sa base de code vocale de 80%, supprimant 23 000 lignes utilisées pour les conversations en temps réel avec des patients.

Ce lancement dote OpenAI d'une couche vocale en façade (front-end) qui peut venir se greffer au-dessus d'une pile de raisonnement choisie et facturée séparément. GPT-Live-1 coûte 0,05$ par minute dans l'API, les frais du modèle backend et de l'agent harness étant facturés à part. Il est lancé avec 12 voix couvrant différents accents, dialectes et langues, l'accès à des voix personnalisées nécessitant de contacter les équipes commerciales. OpenAI prévoit d'ajouter davantage de voix et de langues, et oriente les entreprises vers Presence pour les workflows en temps réel capables d'utiliser les systèmes de l'entreprise, d'entreprendre des actions approuvées et d'escalader vers des humains.

## Pourquoi ça compte
Ce lancement illustre la course d'OpenAI pour s'imposer sur la couche d'interaction vocale des agents IA, un segment stratégique pour les usages d'entreprise (service client, téléphonie, réservations) où la latence et le naturel conversationnel deviennent des facteurs de différenciation concurrentielle.
