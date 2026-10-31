---
title: "Chinese AI invasion gives enterprises a new way to control cost"
date: 2026-10-31
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Faibusiness.com%2Fgenerative-ai%2Fchinese-ai-invasion-gives-enterprises-new-way-control-cost%3Futm_source=tldrit/1/010001a18cc0296b-47ed0e76-3d7e-4e1d-a64c-db183e101824-000000/_ewN-agABnQ4uQjHBVP6u6_7xX9wC91HyNyai7UteGA=452"
keywords: ["modèles open-weight", "IA chinoise", "coûts d'inférence", "Anthropic", "Red Hat", "géopolitique"]
theme: "IA"
tone: "news"
used_in: ["2026-10-31"]
---

## Résumé

Les modèles d'IA en poids ouverts (open-weight) venus de Chine — DeepSeek, Qwen d'Alibaba, GLM de Z.ai — bousculent l'économie du secteur en offrant des performances jugées « suffisantes » pour une fraction du coût des modèles propriétaires américains. Des entreprises comme Red Hat pilotent déjà ces modèles en interne pour maîtriser l'explosion des dépenses en tokens, tandis qu'Anthropic reconnaît elle-même, dans son prospectus d'introduction en bourse, que les gains marginaux de performance des modèles de pointe ne justifient plus toujours leur surcoût. Mais l'adoption reste freinée par des limites d'infrastructure (latence, capacité) et par des craintes géopolitiques, qui alimentent une demande pour des alternatives open-weight occidentales.

## Points clés

- Les modèles chinois représentaient plus de la moitié du volume de tokens traité sur la plateforme OpenRouter pour la semaine du 25 octobre, contre un seul modèle chinois présent dans le classement un an plus tôt.
- Red Hat déploie en pilote le modèle GLM de Z.ai auprès d'environ 1 400 ingénieurs, qui y dirigent près de 70 % de leur trafic d'inférence, avec un quota de 300 $/mois par personne pour l'usage des modèles propriétaires.
- Anthropic admet dans son prospectus d'IPO que les clients pourraient estimer que les gains de performance des modèles de pointe ne valent plus le coût additionnel.
- Le principal frein aux modèles open-weight n'est plus la qualité mais l'infrastructure : latence et capacité insuffisantes pour certains fournisseurs.
- Les inquiétudes géopolitiques freinent l'adoption des modèles chinois (le Department of Homeland Security américain a interdit DeepSeek aux agences fédérales civiles), ce qui crée une demande pour des modèles ouverts occidentaux (Meta, Reflection AI).
- Des utilisateurs plus sceptiques (comme Xbow) notent que certains modèles chinois consomment davantage de tokens pour résoudre un problème donné, ce qui annule une partie de leur avantage tarifaire.

## Analyse approfondie

L'article part d'un constat simple : les modèles ouverts chinois, capables de tourner même sur un simple ordinateur portable, sont devenus assez puissants et assez demandés pour s'attaquer à un problème business central — le coût des tokens d'IA. Cela redessine l'économie des services d'IA et crée une pression concurrentielle sur les modèles dits « frontier » (de pointe).

Dans son prospectus d'introduction en bourse publié lundi, Anthropic reconnaît elle-même que, face à la diversité croissante des modèles disponibles, ses clients « pourraient conclure que les gains de performance incrémentaux à la frontière ne justifient pas le coût additionnel ».

Sur OpenRouter — une plateforme qui donne accès à plusieurs modèles d'IA via une seule API — les modèles chinois ont représenté plus de la moitié du volume mondial de tokens déclarés lors de la semaine se terminant le 25 octobre. Un an plus tôt, un seul modèle chinois figurait parmi les neuf modèles nommés dans le classement hebdomadaire d'usage du site.

Pour ses propres besoins internes, l'éditeur de logiciels open source Red Hat teste une version auto-hébergée de GLM, un modèle en poids ouverts développé par Z.ai à Pékin. Le modèle Qwen du géant technologique chinois Alibaba est également disponible, à plus petite échelle.

Selon Stephen Watt, ingénieur distingué et vice-président du bureau du CTO chez Red Hat, les ingénieurs étaient initialement inquiets de savoir si les modèles en poids ouverts seraient aussi performants que les modèles propriétaires de pointe. Mais ils ont découvert qu'ils étaient « suffisamment bons ». Watt affirme que les modèles en poids ouverts, principalement chinois, ont atteint un niveau d'efficacité comparable à celui d'Opus 4.6 d'Anthropic dans certains cas d'usage. Les ingénieurs avaient des réserves sur l'idée de s'éloigner des modèles de pointe, mais les données d'usage de Red Hat suggéraient que les modèles ouverts étaient adéquats pour de nombreuses tâches.

« On aurait tort de ne pas démarrer son parcours IA avec un modèle de pointe, mais après un certain temps, on aurait tort d'y rester, car cela dévore toute votre marge », dit Watt, en référence au coût comparativement élevé de la plupart des modèles fermés.

Les utilisateurs professionnels, ingénieurs et développeurs peuvent répartir leurs charges de travail selon les capacités des différents modèles. Ils peuvent héberger les modèles en interne, dans des environnements fermés. Mais certains restent prudents face aux modèles chinois, notamment pour des raisons géopolitiques, ce qui stimule l'intérêt pour des modèles développés aux États-Unis.

Cette hésitation, quand elle existe, repose généralement sur des préoccupations géopolitiques. Elle crée une demande latente pour des modèles occidentaux en poids ouverts, comme ceux développés par Meta et Reflection AI, selon Watt.

DataCamp, une plateforme d'apprentissage de l'IA utilisée par environ 6 000 organisations, a fait analyser par son tuteur IA près de 1,4 million d'heures d'apprentissage sur le dernier mois. L'entreprise évalue actuellement Gemma 4, un modèle en poids ouverts de Google destiné au tutorat. Selon Jonathan Cornelissen, cofondateur et PDG de DataCamp, les modèles chinois pourraient poser problème à certains gouvernements et utilisateurs d'entreprise.

Mais pour l'instant, la principale limite des modèles en poids ouverts reste l'infrastructure : les fournisseurs qui les font tourner ne peuvent pas les délivrer à la vitesse ou à l'échelle requises. La latence n'est pas compétitive, selon Cornelissen — certains fournisseurs ont la vitesse mais manquent de capacité, d'autres pêchent sur les temps de réponse. DataCamp est d'ailleurs en train de migrer d'Anthropic vers OpenAI, jugé moins coûteux, sans pour autant basculer son tuteur vers un modèle en poids ouverts.

Jonathan Steele, associé chez Beermann LLP à Chicago et fondateur du cabinet de cybersécurité Steele Fortress, utilise quant à lui un modèle Qwen localement sur un MacBook Pro pour la facturation et d'autres tâches sensibles, tout en recourant à Claude et ChatGPT pour d'autres travaux.

L'économie des modèles en poids ouverts peut sembler avantageuse, mais leur utilité dépend de l'infrastructure disponible et de la qualité des résultats produits. Comparer les coûts n'est d'ailleurs pas simple : un modèle open source peut mettre une demi-heure à produire un brouillon mais nécessiter ensuite cinq heures de relecture par un avocat, alors qu'un modèle de pointe peut rédiger en 15 minutes et ne demander que 30 minutes de révision — il est alors difficile de déterminer lequel est réellement le plus coûteux.

Malgré cela, certaines entreprises comme Red Hat parviennent à tirer de la valeur des modèles chinois. Son pilote avec Z.ai est utilisé par jusqu'à 1 400 ingénieurs, dont environ 70 % du trafic d'inférence est dirigé vers les modèles en poids ouverts. Les ingénieurs disposent d'un budget pour l'usage des modèles de pointe et répartissent leurs besoins entre modèles ouverts et propriétaires selon la nature du travail à accomplir.

Pour Red Hat, la maîtrise des coûts a été un moteur clé de cette démarche : les dépenses liées aux modèles de pointe augmentaient de façon incontrôlée. Avec l'arrivée des modèles en poids ouverts, chaque ingénieur dispose désormais d'un quota de 300 dollars par mois pour les modèles propriétaires, afin de l'inciter à choisir le modèle adapté à chaque tâche. Ces quotas restent expérimentaux et les ingénieurs peuvent demander des exceptions auprès de leurs managers. Selon Watt, le coût des modèles hébergés en externe est passé d'une croissance incontrôlée à une stagnation, puis à une baisse « radicale » aujourd'hui.

Sur le plan géopolitique, les tensions autour des modèles d'IA chinois pourraient s'intensifier. Le Department of Homeland Security américain a, ce mois-ci, interdit aux agences fédérales civiles l'usage de la technologie d'IA de DeepSeek, citant de « multiples vecteurs de menace », notamment un risque de transfert de données vers la Chine. L'ordonnance ne distingue toutefois pas entre les versions hébergées par DeepSeek et celles qu'une entreprise peut faire tourner sur son propre serveur local.

Albert Ziegler, responsable IA chez Xbow, une entreprise de sécurité offensive autonome, indique avoir testé GLM sans toutefois l'utiliser en production. Il n'exclut cependant pas les modèles en poids ouverts à l'avenir ; ses critères sont la performance relative au coût, les benchmarks de sécurité et l'acceptation par les clients. Dans les tests menés par Xbow, GLM nécessitait parfois sensiblement plus de tokens qu'un modèle fermé pour résoudre un même problème, ce qui annulait une bonne partie de son avantage tarifaire. Pour ses applications en production, Xbow a trouvé d'autres modèles fermés — notamment Grok, de la société d'Elon Musk — plus efficaces.

Ziegler exprime toutefois une inquiétude plus large concernant les dangers potentiels des modèles en poids ouverts. Selon lui, dans un an, les modèles ouverts seront meilleurs que les modèles fermés actuels, « et de façon assez nette ». Cette perspective, dit-il, peut être inquiétante : « Les gens pourront héberger un modèle de ce niveau sur leur propre cluster privé, sans aucune restriction. »

## Pourquoi ça compte

Cet article illustre un basculement structurel dans l'économie de l'IA d'entreprise : la montée en puissance des modèles open-weight chinois force les fournisseurs frontier (dont Anthropic, qui le reconnaît elle-même dans son prospectus d'IPO) à justifier leur prime de prix, tout en ajoutant une dimension géopolitique croissante aux choix d'infrastructure IA des entreprises.
