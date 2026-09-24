---
title: "GPT-6 Astra Breaks an Old Enigma Message - Schneier on Security"
date: 2026-09-24
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.schneier.com%2Fblog%2Farchives%2F2026%2F09%2Fgpt-6-astra-breaks-an-old-enigma-message.html%3Futm_source=tldrai/1/010001a0ce763902-fbdaa478-8730-42a8-88e8-8ed14055d5a1-000000/bsBATZ0mHlDAE15C4Zx2uS9JK0eUk9ygh0nCOOnYLwc=452"
authors: ["Bruce Schneier"]
keywords: ["intelligence artificielle", "cryptanalyse", "Enigma", "GPT-6", "traçabilité des données"]
theme: "Sécurité"
tone: "news"
used_in: ["2026-09-24"]
---

## Résumé
GPT-6 Astra, une IA, est parvenue seule à déchiffrer un message Enigma non résolu (Nr. 172, MVUEH) publié sur le site Crypto Cellar Research, après avoir simplement reçu pour consigne de tenter de casser l'un des messages non résolus du site. Elle a identifié un lien probable avec un second message (Nr. 173, SIPVX) et utilisé le nom de lieu répété « ROSENOW ROSENOW » comme crib, développant elle-même un simulateur Enigma et une Bombe en Python et C++ pour retrouver la clé et le texte en clair corrects. Les chercheurs analysent encore les journaux d'exécution pour comprendre précisément sa méthode. Un commentaire pointe une zone d'ombre : l'origine de certaines références de fichiers citées par l'IA reste indéterminée, alors qu'elle devrait, en théorie, être traçable dans les logs.

## Points clés
- GPT-6 Astra a cassé seule le message Enigma non résolu Nr. 172 (MVUEH), sans intervention humaine dans le processus de déchiffrement.
- Carter Leffer s'est limité à lui demander de tenter de casser un message non résolu du site Crypto Cellar Research.
- L'IA a soupçonné un lien entre le message MVUEH et le message Nr. 173 (SIPVX).
- Elle a utilisé le nom de lieu répété « ROSENOW ROSENOW » comme crib (mot probable).
- Elle a développé de son propre chef un simulateur Enigma et une Bombe Enigma en Python et C++.
- Un commentaire soulève une interrogation non résolue sur l'origine de certaines références de fichiers mentionnées par l'IA.

## Analyse approfondie
## GPT-6 Astra déchiffre un ancien message Enigma

C'est assez stupéfiant :

Cependant, ce qu'il y a de plus étonnant dans ce déchiffrement, c'est que GPT6 Astra l'a réalisé entièrement par lui-même. Carter Leffer s'est contenté de demander à GPT6 Astra de voir s'il pouvait casser l'un des messages Enigma non résolus publiés sur le site web de Crypto Cellar Research. Après avoir analysé les messages non résolus du site, il a estimé que le message le plus prometteur était le Nr. 172, MVUEH, et il a également rapidement soupçonné que le texte en clair du message Nr. 173, SIPVX, pourrait être lié au texte en clair du message non résolu MVUEH. Après avoir essayé de nombreuses approches différentes, GPT6 Astra s'est concentré sur l'utilisation du nom de lieu répété ROSENOW ROSENOW comme crib (mot probable). Après avoir développé les logiciels Python et C++ nécessaires pour un simulateur Enigma et une Bombe Enigma, GPT6 Astra a entamé un déchiffrement approfondi à partir du crib ROSENOW, ce qui a finalement permis de trouver la clé correcte et le texte en clair du message MVUEH.

Nous sommes encore en train d'analyser les journaux (logs) de GPT6 Astra pour comprendre exactement comment il a exécuté ce déchiffrement. Et nous découvrons des détails stupéfiants.

Plus de détails au lien indiqué.

Michael Donnelly • 22 septembre 2026, 9h47

« Les références de fichiers que mentionne GPT‑6 Astra… sont correctes, mais elles ne sont pas disponibles sur le site web de Crypto Cellar Research. GPT‑6 Astra mentionne une collection privée, mais on ne sait pas clairement de quoi il s'agit, ni s'il a réussi à accéder aux collections numérisées du Bundesarchiv, ni s'il a trouvé ces fichiers ailleurs. »

Comment se fait-il qu'ils n'arrivent pas à déterminer d'où proviennent ces références de fichiers ? Cela semble être le genre d'information qui devrait figurer dans les logs. Du moins pour les collections numérisées du Bundesarchiv, dont l'accès n'impliquerait aucun piratage.

## Pourquoi ça compte
Cet épisode illustre de façon concrète les capacités émergentes des IA agentiques en cryptanalyse autonome, un signal important pour la veille IA/sécurité sur les usages offensifs comme défensifs de ces modèles. Il souligne aussi un enjeu de traçabilité et de gouvernance des données : même les concepteurs peinent à retracer l'origine de sources utilisées par une IA agissant de façon autonome.
