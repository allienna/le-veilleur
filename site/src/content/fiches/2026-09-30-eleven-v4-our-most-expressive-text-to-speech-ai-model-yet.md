---
title: "Eleven v4: Our most expressive text-to-speech AI model yet"
date: 2026-09-30
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Felevenlabs.io%2Fblog%2Feleven-v4%3Futm_source=tldrai/1/010001a0ed56b287-90a62935-8940-46d3-9a4e-6d8f51356728-000000/N1Pesz3SjUd3yP4DFndfr_nkruXj4BLOX5owKPjoWzU=452"
keywords: ["synthèse vocale", "intelligence artificielle", "clonage vocal", "agents conversationnels", "multilingue", "ElevenLabs"]
theme: "IA"
tone: "news"
used_in: ["2026-09-30"]
---

## Résumé
ElevenLabs lance Eleven v4 et sa variante rapide Eleven v4 Turbo, deux modèles de synthèse vocale (text-to-speech) présentés comme les plus expressifs de la marque à ce jour, classés n°1 par Artificial Analysis et préférés par environ 75 % des auditeurs lors de tests en aveugle face à des concurrents comme Cartesia, Inworld ou Google Gemini. Bâtis sur une nouvelle architecture, ces modèles interprètent le ton, le rythme, l'émotion et le contexte, prennent en charge plus de 90 langues avec un accent natif fidèle, et améliorent nettement le clonage vocal (dès 10 secondes d'audio) ainsi que la cohérence des voix sur de longs contenus. Eleven v4 Turbo cible spécifiquement les usages à faible latence (~100-150 ms), pensé pour fonctionner main dans la main avec la plateforme d'agents conversationnels ElevenAgents. Les deux modèles sont disponibles immédiatement via ElevenAgents, ElevenCreative et l'API d'ElevenLabs.

## Points clés
- Eleven v4 est classé n°1 sur le classement Provider Voice Arena d'Artificial Analysis et préféré à ~75 % en tests en aveugle contre des concurrents (Cartesia, Inworld, Google Gemini).
- Eleven v4 Turbo offre une latence médiane d'environ 100-150 ms, la rendant adaptée aux agents vocaux temps réel.
- Contrôle fin de la livraison via des balises inline en langage naturel (émotion, effets sonores, prononciation IPA).
- Prise en charge de plus de 90 langues avec un transfert d'accent natif fidèle et sans dérive vers l'accent d'origine.
- Clonage vocal amélioré : identité vocale préservée dès 10 secondes d'audio, plus de cohérence sur les contenus longs, ajout du clonage professionnel (PVC).
- Disponible dès maintenant dans ElevenAgents, ElevenCreative et via l'API ElevenLabs.

## Analyse approfondie
Une même phrase peut changer radicalement selon la manière dont elle est prononcée. « Il faut que tu restes calme » ne devrait pas sonner pareil selon qui la dit : un médecin s'adressant avec douceur à un patient effrayé, ou un personnage de jeu vidéo la criant à son escouade avant de se lancer dans la bataille.

Aujourd'hui, nous lançons Eleven v4, notre modèle de synthèse vocale le plus expressif à ce jour, ainsi que sa variante à faible latence, Eleven v4 Turbo.

Classé n°1 par Artificial Analysis¹, et préféré par environ 75 % des auditeurs lors de tests comparatifs en aveugle face à des modèles concurrents², Eleven v4 a été conçu pour interpréter le ton, le rythme, l'émotion, le personnage et le contexte. Il génère une parole qui peut sonner dramatique, tendre, urgente, comique ou conversationnelle, tout en conservant l'identité du locuteur. Une dynamique multi-locuteurs plus naturelle rend les conversations plus réactives, au lieu de donner l'impression de répliques assemblées séparément. Les locuteurs répondent au contexte de la conversation, produisant un dialogue et des interactions de personnages plus naturels.

### Une nouvelle architecture conçue pour la performance
Construit sur une architecture entièrement nouvelle, Eleven v4 est notre modèle de synthèse vocale le plus expressif, classé n°1 par Artificial Analysis¹. Eleven v4 Turbo apporte cette même technologie aux usages à faible latence comme les agents. Avec une latence d'inférence médiane d'environ 100 ms, il peut répondre plus vite que la pause moyenne entre deux prises de parole dans une conversation.

Les deux modèles peuvent générer une parole qui semble empreinte d'émotion plutôt que mécanique. La fidélité audio sous-jacente est également plus élevée sur tous les plans, avec un rendu plus propre et plus naturel.

Les générations précédentes de modèles de synthèse vocale savaient lire un texte à voix haute, mais Eleven v4 apporte à la parole une profondeur émotionnelle qui la rend bien plus naturelle. Le modèle est capable d'interpréter le ton voulu, le rythme à adopter, le caractère du texte, et le contexte, afin de produire une parole émotionnellement juste.

Les utilisateurs disposent également d'un contrôle fin sur les résultats, et peuvent décrire en langage naturel la manière dont une réplique doit être livrée. Ils peuvent aussi ajouter des instructions précises sur la façon de prononcer certaines phrases, l'émotion qu'elles doivent transmettre, et même des effets sonores, à l'aide de balises intégrées telles que [laughs] (rires), [said angrily in French accent] (dit avec colère avec un accent français), [light rain] (pluie légère), ou [phone buzzing] (téléphone qui vibre). Eleven v4 suit ces balises audio et ces instructions de mise en scène avec plus de précision que les modèles précédents, si bien que la livraison décrite correspond réellement au résultat obtenu. Cela facilite la direction de la narration, l'approfondissement des personnages ou de leurs dialogues, et tous les cas où l'interprétation compte.

La documentation développeur d'ElevenLabs détaille l'intégralité de la syntaxe des balises et la façon de les appliquer via l'API. La prise en charge de l'alphabet phonétique international (IPA) a elle aussi été nettement améliorée, ce qui rend les prononciations personnalisées plus fiables.

Eleven v4 apporte également des améliorations en matière de cohérence et de dynamique dans les conversations entre plusieurs locuteurs. Grâce à une nouvelle méthode de capture de l'identité des locuteurs, Eleven v4 préserve les qualités propres à chaque voix. Il est capable de maintenir la cohérence de la parole tout au long de conversations avec des agents, de livres audio ou de publicités. Parce que le modèle comprend le contexte de toute une scène, il génère un dialogue naturel où les locuteurs réagissent à ce qui vient d'être dit, plutôt que d'assembler des répliques isolées.

### Un modèle Turbo pour les usages à faible latence
Les modèles vocaux de haute qualité ont eu tendance à être plus lents à générer la parole, ce qui obligeait les utilisateurs à choisir entre des agents rapides ou expressifs. Beaucoup ont opté pour des agents compétents mais monotones, pouvant sembler robotiques face à un client agacé qui cherche simplement à résoudre son problème.

Eleven v4 Turbo combine vitesse et émotion, avec un délai médian avant la première parole d'environ 150 ms³, rendant possible le déploiement d'agents puissants dans d'innombrables secteurs : des agents chaleureux et rassurants capables de prononcer avec exactitude des termes médicaux dans le domaine de la santé, jusqu'à des agents au débit rapide et au langage familier pour divertir les joueurs dans le jeu vidéo.

Le modèle Eleven v4 Turbo est conçu pour fonctionner avec la plateforme d'agents conversationnels d'ElevenLabs, ElevenAgents. D'autres créateurs d'agents assemblent des modèles et logiciels provenant de différents fournisseurs, ce qui laisse les utilisateurs sans moyen d'affiner ou d'améliorer les résultats du modèle pour leurs cas d'usage spécifiques. Les équipes de recherche et d'ingénierie d'ElevenLabs ont optimisé Eleven v4 Turbo et ElevenAgents ensemble, comme un seul et même système, pour offrir des agents plus expressifs, plus fiables et à faible latence.

### Une voix, une myriade de langues
La manière dont nous communiquons varie selon le contexte, le lieu, et même l'heure de la journée. Construire une parole expressive qui reflète cela, à travers les langues, reste l'un des défis les plus difficiles de l'IA audio.

Eleven v4 marque un progrès sur tous ces aspects, et les améliorations vont au-delà de la simple prononciation des phrases. Eleven v4 capture mieux le rythme, l'émotion et la livraison à travers les langues, aidant les créateurs à produire une parole qui semble naturelle dans sa langue et son contexte. La façon de s'adresser à une personne âgée inconnue au Japon est ainsi très différente de la façon de s'adresser à une personne âgée inconnue en Italie, par exemple.

Eleven v4 et Eleven v4 Turbo prennent tous deux en charge plus de 90 langues. Désormais, une voix enregistrée dans une langue en parle couramment n'importe quelle autre, en adoptant l'accent d'un locuteur natif tout en conservant l'identité de la voix d'origine. Cette adhérence à l'accent est nettement plus forte qu'auparavant, si bien que la voix ne dérive plus vers son accent d'origine au fil d'une génération.

*Exemples audio originaux : catalan, espagnol.*

Pour le doublage et la localisation, cela signifie que la voix de marque que vous avez choisie — qu'il s'agisse d'un acteur célèbre avec lequel vous travaillez ou d'un ton qui correspond le mieux au style de votre entreprise — sonnera très bien dans n'importe quelle langue prise en charge par Eleven v4.

### Un clonage vocal plus authentique et plus cohérent
Le clonage vocal est plus authentique, plus puissant et plus cohérent avec Eleven v4 et Eleven v4 Turbo, avec une similarité vocale nettement meilleure par rapport à la voix source d'origine. Les clones vocaux instantanés (Instant Voice Clones) peuvent désormais capturer des voix avec une haute fidélité à partir de seulement 10 secondes d'audio.

*Exemples audio originaux : voix réelle, Eleven v4.*

Eleven v4 préserve également l'identité du locuteur de manière plus fiable à travers les générations, les dialogues, la narration et les répliques régénérées. Cela signifie que, pour les projets de longue durée, les personnages, narrateurs et voix clonées restent cohérents tout au long d'une production. Eleven v4 ajoute également la prise en charge des clones vocaux professionnels (Professional Voice Clones, PVC), pour les usages de clonage nécessitant la plus haute fidélité.

Le « request stitching » — l'enchaînement de générations pour produire un contenu de plus longue durée — est également nettement plus fiable dans Eleven v4, ce qui améliore l'expérience de travail dans ElevenLabs Studio et l'application ElevenLabs Reader.

### Entendez la différence par vous-même
Eleven v4 et Eleven v4 Turbo sont l'aboutissement de nos dernières recherches en génération de parole expressive. Ils sont conçus pour les contenus où l'interprétation compte autant que les mots eux-mêmes, qu'il s'agisse de livres audio, de performances de personnages, de voix off, de doublage, ou de la localisation d'agents conversationnels.

Les deux modèles sont disponibles dès maintenant dans ElevenAgents, ElevenCreative, et via ElevenAPI. Créez un compte gratuit pour commencer à générer avec Eleven v4 ou Eleven v4 Turbo dès aujourd'hui.

---
1. Artificial Analysis, classement Provider Voice Arena, septembre 2026.
2. Basé sur des tests de préférence utilisateur en aveugle, en face-à-face, contre Cartesia Sonic 3.6, Inworld TTS-2, Google Gemini 3.8 Flash-Lite TTS, et Google Gemini 3.8 Flash TTS, septembre 2026. Pour chaque paire, les évaluateurs ont écouté la même réplique produite par Eleven v4 et par un concurrent, présentées en aveugle, et ont jugé laquelle était la plus expressive et laquelle semblait la plus naturelle ; les égalités comptaient pour moitié.
3. Délai médian entre la requête et l'audition de la parole. Mesuré en septembre 2026 avec des scripts identiques et des réglages par défaut, face à Cartesia Sonic 3.6, xAI TTS, Google Gemini 3.8 Flash-Lite TTS, et OpenAI GPT-4o mini TTS ; la latence réseau a été mesurée puis retirée pour tous les systèmes. Eleven v4 Turbo via streaming WebSocket.

## Pourquoi ça compte
Ce lancement illustre la course à l'expressivité et à la faible latence dans la synthèse vocale, un terrain où ElevenLabs cherche à se différencier des géants (Google, OpenAI, xAI) en intégrant verticalement modèle et plateforme d'agents ; à suivre pour toute veille sur les agents vocaux, le doublage automatisé et le clonage de voix, notamment sous l'angle des enjeux éthiques et de consentement liés à la voix.
