---
title: "Hunger beats tenure: Advice for junior engineers"
date: 2026-11-04
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Ffelixrieseberg.com%2Fhunger-beats-tenure-advice-for-junior-engineers%2F%3Futm_source=tldrdev/1/010001a1a1565131-99f227e0-edaf-4364-84ac-c8357cefdb86-000000/yiFF1GKXal8Vae0xyBW98P-qPXLqT1P0t30600S3pds=452"
authors: ["Felix Rieseberg"]
keywords: ["ingénieurs juniors", "entretien de codage", "IA générative", "Anthropic", "Claude Code", "prototypage"]
theme: "Leadership"
tone: "opinion"
used_in: ["2026-11-04"]
---

## Résumé
Felix Rieseberg, responsable de recrutement chez Anthropic, explique avoir abandonné l'entretien de codage traditionnel : Claude résout désormais ces petits défis techniques mieux que les candidats humains, rendant l'exercice obsolète. Il observe que l'essor de l'IA générative supprime le principal obstacle à l'impact des ingénieurs juniors — le coût élevé de l'exécution — et que des profils peu expérimentés dépassent désormais des ingénieurs plus chevronnés. Il formule cinq conseils concrets pour les ingénieurs sans statut ni capital social, et illustre sa thèse par la genèse de Claude Code, prototypé en un week-end par deux ingénieurs récemment arrivés chez Anthropic.

## Points clés
- Anthropic a cessé d'utiliser l'entretien de codage classique : Claude surpasse désormais les humains sur ces exercices, qui ont perdu leur valeur prédictive.
- Thèse centrale : « la faim l'emporte sur l'ancienneté » — l'impact professionnel n'est plus borné par le nombre d'années d'expérience accumulées.
- Le regard neuf des nouveaux arrivants (exemples chez Stripe et Notion) permet de repérer des frictions et de remettre en cause des « impossibilités » que les anciens ne questionnent plus.
- Historiquement, le vrai frein n'était pas le manque d'idées mais le coût élevé de l'exécution et les couches hiérarchiques nécessaires pour obtenir un feu vert ; l'IA réduit fortement ce coût.
- Cinq conseils pratiques : viser l'impact business plutôt que le backlog, choisir une idée ambitieuse, la prototyper en un week-end, se concentrer sur une seule idée forte, et exploiter sa perspective d'outsider.
- Claude Code comme preuve par l'exemple : un prototype construit en un week-end par deux ingénieurs juniors (Anthony Morris et Alice Zhao) a donné naissance à un produit public lancé environ huit jours plus tard.

## Analyse approfondie
L'auteur ouvre son billet en annonçant qu'il a mis fin, ce mois-ci, à la pratique de l'entretien de codage classique. En tant que responsable de recrutement chez Anthropic, il a cessé de demander aux candidats de les réaliser. Il reconnaît que cet exercice a eu son utilité : savoir définir rapidement un problème et trouver une solution élégante était un indicateur faible mais utile de la réussite future d'un candidat dans ses équipes. Les petits défis de code en conditions réelles révélaient quelque chose de significatif.

Ce n'est plus le cas aujourd'hui. Il n'y a pas plus de sens à soumettre quelqu'un à un petit défi React qu'à l'interroger sur l'assembleur : Claude est désormais meilleur que l'humain sur les deux exercices. Les profils qui ont le plus d'impact chez Anthropic réussissent indépendamment de leur performance à ces tests.

Malgré son omniprésence, l'entretien de codage n'a jamais été populaire, et l'auteur s'attend à ce que des ingénieurs expérimentés réagissent fortement à sa disparition, ne serait-ce que pour ce que cela dit de l'évolution de leur métier. Beaucoup a été écrit sur le fait que l'IA représente un défi pour les développeurs juniors, notamment pour trouver un emploi. Mais après avoir observé des juniors travailler avec l'IA, l'auteur se dit plus optimiste : l'impact dépend désormais moins du nombre d'années d'expérience accumulées sur des frameworks et des bibliothèques.

Il constate que des ingénieurs relativement nouveaux dépassent des personnes qui sont probablement de meilleurs codeurs mais qui sont en poste depuis bien plus longtemps. D'où l'idée que « la faim l'emporte sur l'ancienneté ». Ce billet se veut son meilleur conseil aux ingénieurs juniors — bien que « junior » soit un terme inapproprié : il s'adresse en réalité à ceux qui n'ont ni capital social, ni statut, ni pouvoir.

### Tout voir, mais ne pas être écouté
L'auteur invite d'abord à connaître à la fois son avantage et son handicap.

Un regard neuf, même naïf, a longtemps été considéré comme une force. Lorsqu'il a rejoint Stripe, le fondateur Patrick Collison demandait aux nouveaux venus de prêter une attention particulière à ce qui leur semblait étrange, pariant que les nouveaux repéreraient des frictions et des opportunités que les anciens avaient depuis longtemps cessé de remarquer.

En 1991, James March écrivait que les organisations dépendent du maintien d'un afflux de personnes « naïves et ignorantes ». Interrogé sur la confiance nécessaire pour tenter des plans de caméra que personne n'avait essayés, Orson Welles répondait : « L'ignorance, la pure ignorance — il n'y a pas de confiance qui l'égale. Ce n'est que lorsqu'on connaît bien un métier qu'on devient timide ou prudent. »

L'auteur raconte qu'à son arrivée chez Notion, un entretien portait sur la conception d'une architecture de mode hors ligne. Il fut surpris d'apprendre que c'était considéré comme une question « piège », un mode hors ligne étant jugé impossible : le modèle de données était trop complexe pour synchroniser un espace de travail Notion entier, et télécharger des pages individuelles aurait constitué une expérience utilisateur que le PDG Ivan Zhao n'aurait jamais acceptée. La complexité du modèle de données s'est révélée réelle ; la résistance du fondateur, non. Tout le monde considérait cela comme une évidence, si bien que personne n'avait vérifié. Lui, nouvel arrivant ignorant, n'a simplement pas su qu'il ne fallait pas poser la question.

Il est facile, avec de tels exemples, de juger que des gens ont pris de mauvaises décisions — mais l'auteur insiste sur la difficulté de repérer ces erreurs lorsqu'on les commet soi-même. Peu après son arrivée chez Notion, il avait voulu équiper les équipes de grands écrans pour afficher des tableaux de bord en direct ; il s'est heurté à des obstacles organisationnels, a échoué, et n'a pas eu l'énergie de se battre davantage.

Un an plus tard, un nouvel employé, Ji Pei, est arrivé avec la même idée. L'auteur l'a d'abord découragé, lui disant qu'il avait déjà essayé sans succès. Mais Ji Pei avait déjà posé la question, et les écrans sont arrivés dès le lendemain. Quelque part durant cette année, l'auteur était devenu, à son tour, l'ancien du cru.

Le seul problème de ce pouvoir de l'ignorance : personne ne se soucie de ce que l'on pense. La plupart des entreprises technologiques comportent des strates de management intermédiaire chargées de traduire les objectifs business en exécution. Structurellement, les entreprises sont souvent organisées autour de l'idée que quelques personnes valident ou bloquent les idées individuelles. Dans un monde où l'exécution est coûteuse, il faut généralement gravir patiemment les échelons du statut social avant que l'organisation entière ne « parie » sur une idée. Les organigrammes évoluent à un rythme glacial, si bien que même les entreprises convaincues par l'IA s'attendent encore souvent à ce que les juniors exécutent simplement leurs tâches plus vite, plutôt que de poursuivre ambitieusement les objectifs de l'entreprise.

Bonne nouvelle, cependant : l'exécution n'est plus coûteuse.

### Que faire
1. **Privilégier l'impact business plutôt que le backlog** : en 2011, avant l'ère du codage assisté par IA, Patrick McKenzie écrivait que « les ingénieurs sont embauchés pour créer de la valeur business, pas pour programmer des choses ». Il conseillait de se rattacher aux parties de l'entreprise qui génèrent des revenus. Il faut d'abord comprendre ce que l'entreprise cherche réellement à accomplir (ou, dans une grande structure, ce que vise son groupe ou son département), puis trouver le bon niveau — comprendre les objectifs du responsable de son responsable est souvent un bon indicateur.
2. **Choisir une idée radicale** : élaborer quelques idées qui, si elles réussissent, amélioreraient radicalement les chances que l'organisation atteigne ces objectifs. Il faut être ambitieux.
3. **La construire en un week-end** : l'auteur a vu de petits groupes ou des ingénieurs solos dépasser le processus classique — rédaction de documents d'exigences produit (PRD), recherche d'adhésion, lobbying pour obtenir du temps de designers ou de product managers — en construisant directement un prototype fonctionnel.
4. **Se concentrer sur une seule bonne idée** : selon l'auteur, les juniors commettent souvent l'erreur d'entasser plusieurs idées dans un même prototype, noyant trois excellentes idées parmi vingt mauvaises. Un prototype qui inclut la création d'un nouveau langage de programmation, un backend, et aussi des applications mobiles n'a aucune chance de réussir. L'objectif d'un prototype fonctionnel est de communiquer une idée si clairement que la direction en saisit immédiatement l'opportunité — et comprend que son auteur est la bonne personne pour la mener.
5. **Exploiter sa perspective neuve** : sur un produit destiné aux utilisateurs, un junior dispose d'une empathie unique et d'une meilleure intuition de ce qui fonctionne ou non pour eux. Les collègues de l'auteur chez Slack et Notion avaient du mal à se mettre dans la peau d'un utilisateur externe de Slack ou de Notion. Sur l'infrastructure ou l'outillage, l'avantage est de ne pas avoir appris toutes les raisons pour lesquelles certaines choses sont jugées « impossibles ».

### L'avenir est prometteur
L'auteur ne pense pas que l'entretien de codage reviendra. Il est facile de ressentir une pointe de nostalgie en pensant au nombre d'exemplaires du livre « Algorithms and Data Structures » achetés dans l'espoir de décrocher un bon emploi et un avenir meilleur — ou de voir la disparition de l'entretien de codage comme une nouvelle étape dans l'élévation du niveau d'abstraction de l'ingénierie logicielle.

Dans le même temps, lui qui déteste depuis longtemps les promotions à l'ancienneté, se dit optimiste : il a déjà vu sa part d'applications et de produits populaires construits de cette façon.

Chez Anthropic, les équipes s'étaient tellement habituées à utiliser Claude Code en ligne de commande (CLI) qu'il a fallu seulement deux ingénieurs relativement nouveaux — Anthony Morris et Alice Zhao — pour concevoir un prototype fonctionnel en un seul week-end. La première version publique a été lancée environ huit jours plus tard. Il n'est pas surprenant qu'une bonne interface graphique pour Claude Code soit devenue un produit très demandé.

L'auteur n'est probablement pas le seul manager à chercher comment recruter des personnes qui savent bien construire avec l'IA. Il n'a pas encore trouvé la méthode idéale, mais il dit scruter les CV et portfolios à la recherche de petits prototypes qui révèlent du goût, de l'empathie et une pensée rigoureuse. Il invite d'ailleurs toute personne ayant trouvé une meilleure méthode à la lui partager.

L'image accompagnant ce billet est une œuvre de J. M. W. Turner, « The Fighting Temeraire » (1839).

## Pourquoi ça compte
Ce témoignage, venant d'un hiring manager d'Anthropic, illustre concrètement comment l'IA générative redéfinit les critères de recrutement et de progression en ingénierie logicielle, en déplaçant la valeur de l'expérience technique accumulée vers la capacité à prototyper vite et à viser l'impact business — un signal utile pour toute veille sur l'évolution des métiers tech face à l'IA.
