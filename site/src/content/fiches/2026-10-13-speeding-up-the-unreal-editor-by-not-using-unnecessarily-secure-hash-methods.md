---
title: "Speeding up the Unreal editor by… not using unnecessarily secure hash methods"
date: 2026-10-13
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Flarstofus.com%2F2026%2F10%2F11%2Fspeeding-up-the-unreal-editor-by-not-using-unnecessarily-secure-hash-methods%2F%3Futm_source=tldrnewsletter/1/010001a12fb84000-1b548899-3bbf-451e-b2e7-159af658a1db-000000/e6H4QwcMR9S_yZSBeqZgSUepbl-2iEhvYCd33i7BlwI=452"
keywords: ["optimisation", "Unreal Engine", "hachage", "SHA1", "xxHash", "performance"]
theme: "Software"
tone: "research"
used_in: ["2026-10-13"]
---

## Résumé
L'auteur raconte comment il a repéré un goulot d'étranglement caché dans l'éditeur Unreal Engine : l'algorithme cryptographique SHA1 (conçu par la NSA) était utilisé pour hacher le code source des shaders, une opération qui ne nécessite aucune sécurité cryptographique. En le remplaçant par xxHash, déjà présent dans le moteur, il réduit le temps CPU consacré à cette opération de 12,90 à 1,59 secondes, soit un gain de 8x, mesuré sur le projet de démonstration Electric Dreams. Sa pull request a été acceptée en quelques jours par Epic Games, qui l'a même améliorée en encapsulant le nouveau hachage dans une struct dédiée (FShaderHash) pour faciliter de futures évolutions.

## Points clés
- SHA1, algorithme cryptographique conçu par la NSA, servait à hacher le code source des shaders dans Unreal Engine, sans aucune justification de sécurité.
- Le remplacement par xxHash (déjà implémenté dans le moteur) a fait chuter le temps CPU de hachage de 12,90 s à 1,59 s, soit 8 fois plus rapide.
- Effet secondaire bénéfique : la taille des hachages stockés est passée de 20 à 8 octets.
- La pull request a été acceptée par Epic Games en quelques jours, qui l'a enrichie d'une struct FShaderHash pour simplifier de futurs changements d'algorithme.
- La démarche illustre une stratégie d'optimisation efficace : chercher les angles morts du profilage plutôt que les zones déjà bien optimisées (ex. compilation des shaders).
- Un oubli de test sur les builds hors éditeur a nécessité une correction, rappel que les tests doivent couvrir toutes les configurations de build.

## Analyse approfondie
Une bonne astuce lorsqu'on cherche des pistes d'optimisation d'un logiciel consiste à éviter les zones qui sont déjà très probablement bien optimisées, et à se concentrer plutôt sur celles qui ont pu être négligées, soit parce qu'elles sont trop obscures, soit parce qu'elles n'apparaissent pas lors des sessions de profilage habituelles. Cette tactique a déjà bien fonctionné dans le passé, comme l'ont montré mon optimisation de la création des tooltips, ou celle du chargement des fichiers de localisation de l'éditeur.

C'est pourquoi, en profilant (encore une fois) le lancement de l'éditeur, j'ai pour habitude d'ignorer la plupart des fonctions contenant des mots comme « Shader Compilation » ou « Shader Source » lorsque je tombe sur elles dans mon profileur. La compilation des shaders est un processus notoirement long et élaboré, et je suis à peu près certain que des gens très compétents chez Epic ont déjà passé beaucoup de temps à optimiser ces zones. C'est pour cette raison que j'ignorais, par exemple, la fonction « Compile Global Shader Map », même si son temps d'exécution se chiffrait typiquement en plusieurs secondes :

Cela, du moins, était vrai jusqu'au jour où je l'ai survolée avec un niveau de zoom inhabituellement élevé et où j'ai aperçu une des fonctions qu'elle appelait :

Je ne suis certainement pas un expert des algorithmes de hachage, mais SHA1 est l'un des (très rares) algorithmes de hachage que même moi je connais. Et voir cet algorithme utilisé pour hacher des shaders m'a semblé étrange. C'est parce que SHA1 ~~est~~ était un algorithme de hachage cryptographiquement sûr, développé à l'origine par la NSA (oui, celle-là). Et même s'il a été cryptographiquement cassé il y a des années et ne devrait plus être utilisé pour des données sensibles, cette origine signifie que – pour le dire poliment – il n'est pas particulièrement rapide.

Qu'est-ce que « pas rapide » signifie dans ce contexte ? Eh bien, jugez-en par vous-même dans ce test comparatif d'un ensemble d'algorithmes de hachage couramment utilisés, réalisé il y a quelques années par Aras Pranckevičius (en fait, c'était il y a 10 ans – je commence à vieillir). SHA1 n'était même pas inclus comme un véritable concurrent, mais seulement, comme le note le début de l'article, « pour illustrer les différences de performance ». Aïe.

C'est d'autant plus gênant que les données hachées sont le code source du shader, y compris tous les commentaires et la mention de copyright :

Cela signifie à la fois que nous devons hacher beaucoup de données (les fichiers source peuvent être assez volumineux) et qu'il n'y a aucune raison de les hacher avec un hachage cryptographiquement sûr, puisqu'il ne s'agit pas de données sensibles.

Dès lors, renoncer à un hachage cryptographiquement sûr au profit d'un algorithme rapide devrait être un gain facile, non ? Et l'article cité proposait déjà une bonne alternative, dont j'ai même trouvé une implémentation existante dans la base de code d'Unreal : xxHash.

Précision avant qu'on me pose la question : xxHash n'est pas forcément le hachage le plus rapide qui existe. D'autres hachages, potentiellement encore plus rapides, existent, mais pour l'instant, utiliser un hachage plus rapide déjà employé et testé au sein du moteur sur lequel nous travaillons est une option bien plus simple.

Changer le hachage utilisé n'a pas été trop compliqué, même si j'ai dû modifier plus d'endroits du code que prévu, puisque tous les endroits où le hachage produit était stocké ou transmis devaient aussi être mis à jour. Un effet secondaire agréable de ce changement est que les hachages stockés sont devenus un peu plus petits qu'avant (8 octets au lieu de 20).

Mais bien sûr, l'effet recherché par ce changement ne concernait pas la mémoire, mais le temps CPU. Pour mes tests, j'ai ouvert dans l'éditeur l'un des propres projets d'exemple d'Unreal, Electric Dreams, 5 fois avec et 5 fois sans le changement, soit 10 exécutions au total. Le profilage a été réalisé avec Superluminal.

Pour mettre les chiffres suivants en perspective, précisons que je parlerai surtout du temps CPU total, cumulé sur tous les threads, et non seulement du temps passé sur le thread de jeu. Ce n'est pas pour gonfler artificiellement les chiffres, mais pour les rendre plus cohérents et plus faciles à comparer. L'effet réel sur le temps de démarrage de l'éditeur correspond (très approximativement) au temps mesuré divisé par le nombre de cœurs.

Dans la version standard du moteur, pas moins de 12,90 secondes étaient passées dans FSHA1::Update. Dans la version modifiée utilisant xxHash, ce temps est tombé à seulement 1,59 seconde passée dans FXxHash64Builder::Update. C'est huit fois plus rapide ! Mission accomplie.

Normalement, cet article se terminerait maintenant par un lien vers une pull request, pour que toute personne intéressée par ce changement puisse l'intégrer dans sa propre version du moteur, en attendant et en espérant que quelqu'un chez Epic la remarque et la fusionne dans la branche principale.

Eh bien, cette fois j'ai une meilleure nouvelle encore : le changement a déjà été accepté ! (pas encore fusionné cependant, cela semble devoir prendre encore quelques jours)

J'ai soumis la pull request quelques jours seulement avant d'écrire cet article, et ces quelques jours ont déjà suffi à quelqu'un chez Epic non seulement pour relire mon changement, mais aussi pour le peaufiner. Jetons donc un œil à certaines des modifications apportées à ma proposition :

Une astuce très maligne à laquelle je n'avais pas pensé consistait à envelopper le xxHash dans une autre struct, FShaderHash. Cela ne change rien au comportement actuel, mais facilitera un futur changement d'algorithme de hachage, si un algorithme encore plus rapide s'avérait nécessaire, sans avoir à modifier le code à de nombreux endroits différents.

Correction d'une erreur de compilation pour les builds hors éditeur : c'était un oubli de ma part. Je n'avais testé mon changement que sur un build éditeur, principalement parce que mon profilage initial avait aussi été effectué dans l'éditeur. Je devrais sans doute ajouter les builds hors éditeur à ma liste, déjà longue, de vérifications à faire avant une future pull request.

Et voilà, c'était tout. Si cet article vous a plu et que vous souhaitez lire d'autres contenus sur l'optimisation de jeux à l'avenir, pensez à me suivre sur BlueSky, Mastodon ou LinkedIn, où je publie tous mes articles. Ou abonnez-vous directement à mon blog, juste en dessous de l'article.

## Pourquoi ça compte
Ce cas concret illustre comment un choix technique par défaut (un hachage cryptographique utilisé sans raison de sécurité) peut coûter cher en performance dans un moteur aussi utilisé qu'Unreal Engine, et propose une méthode de profilage reproductible — explorer les angles morts plutôt que les zones déjà optimisées — transposable à d'autres bases de code volumineuses.
