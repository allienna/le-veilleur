---
title: "Data is the application"
date: 2026-10-01
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fma.ttias.be%2Fdata-is-the-application%2F%3Futm_source=tldrdev/1/010001a0f208073c-63569086-f574-47c6-82a4-201c8b273824-000000/IaR835YB92yTNzbAlLAx5K8C9TIzAZSDVOjCiQvUxgc=452"
authors: ["Mattias Geniar"]
keywords: ["codage agentique", "migrations de données", "event sourcing", "portes à sens unique", "confidentialité", "architecture de données"]
theme: "Tech"
tone: "opinion"
used_in: ["2026-10-01"]
---

## Résumé

L'auteur explique comment le codage agentique a rendu la quasi-totalité de ses décisions de développement réversibles et peu coûteuses — ce que Jeff Bezos appelle des "portes à double sens" — lui permettant d'itérer très vite, même depuis son téléphone. Il soutient que la couche de données constitue l'exception : les migrations, les choix de stockage et de format sont des "portes à sens unique" qui exigent réflexion lente et délibérée, un bureau et une tête reposée. Des techniques comme le soft delete, les migrations réversibles ou l'event sourcing n'offrent qu'une illusion d'annulation, car une donnée jamais enregistrée ou réellement perdue ne peut être reconstituée. Sa conclusion : les données sont la véritable application, le reste (UI, infrastructure, serveurs) pouvant être reconstruit rapidement, mais pas les données que les utilisateurs ont confiées.

## Points clés

- Le codage agentique transforme presque toutes les décisions produit (UI, fonctionnalités, traductions) en "portes à double sens" réversibles à très faible coût.
- La couche de données reste une "porte à sens unique" : migrations, formats de stockage, structures de données et sauvegardes exigent une réflexion lente et délibérée, à l'opposé de la vitesse du reste du développement.
- Les mécanismes classiques (soft delete, migration avec `down()`, backups) n'annulent qu'un changement de code, pas la perte réelle de la donnée elle-même.
- L'event sourcing se rapproche d'un vrai bouton d'annulation (on peut rejouer les événements dans une nouvelle table), mais déplace le problème : le journal append-only conserve pour toujours un événement mal conçu, et complique le droit à l'oubli.
- La confidentialité et la rétention des données (durée de conservation, suppression de compte, contenu des sauvegardes) restent des décisions lentes que la génération rapide de code par IA ne simplifie en rien.
- Thèse centrale : "les données sont l'application" — tout le reste peut être reconstruit en un après-midi, mais des données utilisateur perdues laissent une coquille vide.

## Analyse approfondie

Le codage agentique me permet d'avancer *très* vite. Une fonctionnalité est construite en quelques jours. Un design est implémenté en quelques heures. Changer une mise en page, mettre à jour un template, retravailler un flux : tout cela se passe à une vitesse que je n'aurais pas pu imaginer il y a un an.

Il y a une partie de la stack où rien de cette vitesse ne s'applique à moi : les données.

### Tout le reste a un bouton d'annulation

La majeure partie de mon travail se fait aujourd'hui depuis un téléphone, en discutant avec un environnement de développement distant. Une grande partie de ce travail est de l'itération, et l'itération est bon marché quand un changement peut être annulé.

- Une mise en page qui ne fonctionne pas vraiment une fois que les gens l'utilisent ? La version suivante n'est qu'à un déploiement.
- Un bug ? Corrigé, déployé, disparu.
- Des traductions erronées ? Redéployé, corrigé.
- Une refonte qui rend une partie de l'interface moins confuse, mais plus difficile à utiliser ? Redéployé, corrigé.
- Une fonctionnalité commencée dont je n'aime pas la direction ? Annulée. La branche reste là, inoffensive.

Rien de tout cela ne part sans être testé. Chaque changement passe toujours par la suite de tests, et je lis toujours le diff avant qu'il ne soit fusionné. Ce qui a changé, c'est le coût d'une mauvaise décision : si un écran s'avère confus une fois utilisé par de vraies personnes, la correction est à quelques minutes. C'est pour ça que je suis à l'aise de faire ce genre de travail depuis le canapé.

Donc j'avance vite, j'itère, je pivote, je change d'avis en plein milieu, je déploie et redéploie, j'annule des choses que je n'ai même pas finies... C'est pour ça que je prends désormais plus de temps pour réfléchir aux fonctionnalités : *générer* une nouvelle version est si bon marché qu'en essayer trois est devenu la façon normale de travailler.

### Les données, non

Chaque fois que je dois toucher la couche de données, je m'arrête.

Je ne peux pas le faire depuis un téléphone. J'ai besoin d'être à un bureau, devant un ordinateur, en mode réflexion, sans distractions. Parce que c'est la couche où une erreur n'est pas annulée par le déploiement suivant.

Il existe des patterns de code qui atténuent le choc, certes. Des suppressions douces (soft deletes), une migration avec un `down()` adéquat, une sauvegarde de la nuit précédente. Mais ceux-ci annulent un *changement de code*, pas la perte elle-même. Si une migration a tronqué une colonne, le `down()` remet la colonne en place. Vide.

L'event sourcing s'en approche le plus. On ne stocke pas l'état actuel, on stocke chaque changement comme un événement (`OrderPlaced`, `AddressChanged`, ...) et on construit ses tables à partir de ces événements. Une table cassée par une mauvaise migration ? On la jette et on relit les événements dans une nouvelle. Le package d'event sourcing de Spatie a une commande `event-sourcing:replay` pour ça. C'est un véritable bouton d'annulation pour la couche de données.

Mais la porte à sens unique est toujours là, elle s'est juste déplacée vers les événements. Le journal est en ajout uniquement (append-only), donc un événement mal conçu y reste pour toujours. Un événement qu'on n'a jamais enregistré ne peut pas être relu. Et un journal en ajout uniquement de tout ce qu'un utilisateur a jamais fait est la dernière chose que l'on souhaite quand cet utilisateur demande la suppression de son compte.

Les données sont les données. Si vous ne les avez pas, vous ne pouvez pas les reproduire.

Prenez Snapkin. Quand vous lui dites une fois que le blob blanc sur votre assiette de petit-déjeuner est du skyr et non du yaourt, elle s'en souvient et l'utilise à partir de ce moment. Je peux reconstruire l'écran qui posait la question en un après-midi. Je ne peux pas reconstruire la réponse. Seule la personne qui a mangé le skyr le sait, et elle l'a dit à l'application exactement une fois.

### Les portes à sens unique

Jeff Bezos a un nom pour ça. Dans sa lettre aux actionnaires d'Amazon de 2015, il divise les décisions en deux types :

> Certaines décisions sont conséquentes et irréversibles, ou presque irréversibles – des portes à sens unique – et ces décisions doivent être prises méthodiquement, avec soin, lentement, avec une grande délibération et concertation. Si vous passez la porte et que vous n'aimez pas ce que vous voyez de l'autre côté, vous ne pouvez pas revenir à l'endroit où vous étiez avant. [...] Mais la plupart des décisions ne sont pas comme ça – elles sont changeables, réversibles – ce sont des portes à double sens.

Le codage agentique a transformé presque tout ce que je construis en porte à double sens. Une mise en page, une fonctionnalité, une traduction : on passe la porte, on n'aime pas, on revient en arrière.

Bezos mettait en garde contre le fait de traiter des portes à double sens avec la prudence d'une porte à sens unique, parce que ça rend une entreprise lente. Avec les agents, c'est l'erreur inverse qui m'inquiète : franchir une porte à sens unique à la vitesse d'une porte à double sens, parce que tout autour bouge à cette vitesse-là.

Et la couche de données, c'est là que se trouvent les portes à sens unique :

- Les migrations.
- Ce que vous stockez, et dans quel format.
- Les structures de données.
- Les sauvegardes.
- La récupération.

Chaque migration de données, et chaque moment dans l'application où je dois décider *si* je dois stocker quelque chose et, si oui, *comment*, me fait faire une pause. C'est là que vont la majeure partie de mon temps et de ma réflexion aujourd'hui. Pas l'UI, pas l'UX, pas les fonctionnalités, pas ce qui vient après dans la liste. Tout cela peut rester fluide. Ça change, et je l'adapte à ce que les utilisateurs disent ou veulent.

Les données sont sacrées.

Cela ne rend pas pour autant une décision sur les données permanente. Je peux changer le type d'une colonne, scinder une table ou déplacer un champ ailleurs plus tard. Mais chacun de ces changements touche des lignes qui existent déjà, donc cela demande beaucoup plus d'effort et de réflexion pour s'assurer que rien n'est perdu et que chaque changement apporté aux données est intentionnel. Un changement de mise en page, c'est un nouveau déploiement. Un changement de données, c'est un plan : ce qui arrive à chaque ligne existante, comment je vérifie que ça a fonctionné, et comment je reviens en arrière si ça n'a pas fonctionné.

Un champ que je décide de stocker est un champ que je dois désormais protéger, sauvegarder, et finir par supprimer à nouveau. Un champ que je décide de *ne pas* stocker est perdu pour de bon. Je ne peux pas revenir en arrière et demander aux gens ce qu'ils ont fait mardi dernier.

### La confidentialité et la rétention des données ne se bâclent pas non plus

Il y a ensuite la confidentialité et la rétention des données. Combien de temps est-ce que je garde quelque chose ? Qui peut le voir ? Que se passe-t-il quand quelqu'un supprime son compte, et est-ce que ça couvre aussi les sauvegardes ? Que signifie même une sauvegarde si elle contient des données que j'ai promis de détruire ?

Aucune de ces questions n'a de réponse rapide, et aucune ne devient plus facile parce qu'un agent peut écrire la migration en 30 secondes. Écrire la migration n'a jamais été la partie lente. Réfléchir à ce qu'elle fait aux données déjà existantes, ça l'est.

### Les données sont l'application

Retirez tout d'une application : l'UI, le site web, l'application mobile, les serveurs, l'infrastructure. Vous pouvez tout reconstruire, et avec les outils dont nous disposons aujourd'hui, plus vite que jamais.

Vous ne pouvez pas faire ça avec les données que vos utilisateurs vous ont confiées. Perdez-les, et tout ce que vous reconstruirez ne sera qu'une coquille vide avec un écran de connexion.

Donc je vais continuer à itérer joyeusement sur une mise en page depuis mon téléphone. La migration, elle, attendra que je sois à mon bureau.

## Pourquoi ça compte

Alors que l'IA générative accélère radicalement le cycle de développement logiciel, cet article pointe un angle mort crucial de la gouvernance technique : la vitesse ne doit jamais s'appliquer aux décisions irréversibles sur les données, sous peine de dommages permanents et de pertes de confiance des utilisateurs.
