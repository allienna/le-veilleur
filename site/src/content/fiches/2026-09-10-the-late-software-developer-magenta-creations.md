---
title: "The late Software Developer - Magenta Creations"
date: 2026-09-10
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fmg-crea.com%2Fblog%2Fthe-late-software-developer%2F%3Futm_source=tldrdev/1/010001a085e345e0-e4ed8295-36b0-4db1-9ad1-88297af62686-000000/OHhYR4Pfis8UeZzc4Xf0rXrn6htaiRzL0XiXo_-od_s=452"
keywords: ["agents IA", "développement logiciel", "MCP", "productivité", "automatisation", "codage assisté"]
theme: "IA"
tone: "opinion"
used_in: ["2026-09-10"]
---

## Résumé
L'auteur, développeur depuis dix ans, raconte comment son métier a basculé du codage en profondeur et en solitaire vers la supervision simultanée de plus de 20 sessions d'agents IA travaillant en parallèle. Ce changement, à la fois grisant et déstabilisant, lui a permis de développer une dizaine d'applications natives macOS/iOS en quelques mois seulement — des projets qu'il jugeait auparavant trop coûteux en temps pour être lancés. Il en tire une conclusion structurelle : dans le logiciel comme dans toute industrie, « l'usine devient le produit », et le développeur humain devient le goulot d'étranglement qu'il faut désormais chercher à éliminer. Il présente enfin deux outils qu'il a publiés pour faire tourner cette « usine » d'agents : Bastion et Cupertino.

## Points clés
- Le travail quotidien est passé de sessions de codage focalisées à la gestion parallèle de plus de 20 agents IA, ce qui change fondamentalement la charge cognitive.
- L'attention se déplace : au lieu de préserver le "flow", il s'agit désormais de débloquer les agents en continu et d'arbitrer les limites de débit (rate limits) des API.
- Ce nouveau mode de travail a rendu viables des projets personnels auparavant abandonnés faute de temps, avec une dizaine d'apps macOS/iOS livrées en quelques mois.
- Constat central : "l'usine est le produit" — l'enjeu n'est plus de coder, mais de construire et d'optimiser le système qui fait coder les agents à sa place.
- Le développeur humain devient le principal frein à la mise à l'échelle ; l'objectif assumé est de "se retirer de l'équation" le plus vite possible.
- Deux outils open source sont proposés pour opérer cette usine d'agents : Bastion (exécution mutualisée des serveurs MCP avec identifiants stockés dans le Keychain et journalisation de tous les appels) et Cupertino (accès sécurisé des agents à l'ensemble des données de l'écosystème Apple) ; le code est public, la licence payante ne fait que lever une limite d'essai dans le temps, et l'auteur cherche des retours d'utilisateurs.

## Analyse approfondie
L'article prend la forme d'un billet personnel où l'auteur décrit la transformation radicale de son métier de développeur. Après une décennie passée à coder en sessions longues et concentrées, il se retrouve désormais à jongler en permanence avec plus de vingt sessions d'agents IA fonctionnant en parallèle — une bascule qu'il juge à la fois excitante et anxiogène.

Sur le plan cognitif, il note que la stimulation n'est plus la même : autrefois, il évitait toute distraction pour préserver son état de "flow" ; aujourd'hui, il change constamment de contexte pour débloquer ses agents et les orienter vers l'étape suivante, tout en apprenant à gérer au mieux les limites de débit des API (rate limits), une contrainte qu'il qualifie de nouvelle discipline critique.

Cette évolution a toutefois un effet très concret : elle lui a permis de développer une dizaine d'applications natives macOS/iOS en quelques mois seulement — des idées qu'il avait mises de côté auparavant parce qu'elles ne justifiaient pas l'investissement en temps qu'elles auraient demandé. Ce n'est plus le cas.

S'il maintient ce rythme, il estime qu'il gérera des centaines d'applications d'ici l'an prochain. Il en tire un constat plus général, à la manière de tout secteur industrialisé : "l'usine est le produit", et il est lui-même le goulot d'étranglement de cette usine. Son rôle consiste donc, littéralement, à chercher à se retirer de l'équation aussi vite que possible — une démarche qu'il trouve, malgré son caractère contre-intuitif, source de plaisir dans un paysage professionnel profondément redessiné.

Pour faire tourner cette "usine" d'agents, il indique avoir publié des dizaines de MCP (Model Context Protocol) ainsi que deux outils :
- **Bastion**, qui exécute chaque serveur MCP une seule fois pour l'ensemble des clients sur le Mac, avec les identifiants stockés dans le Keychain et chaque appel journalisé.
- **Cupertino**, qui permet à tout agent d'accéder de façon sécurisée à l'ensemble des données de l'écosystème Apple.

Le code source de ces outils est public ; la version payante se contente de lever une limite de durée d'essai. L'auteur précise offrir des licences à des utilisateurs afin de recueillir des retours précoces, et invite les personnes intéressées à le contacter.

## Pourquoi ça compte
Ce témoignage illustre concrètement comment l'essor des agents IA autonomes redéfinit le quotidien des développeurs, en déplaçant leur valeur ajoutée du code lui-même vers l'orchestration et l'industrialisation de flottes d'agents — une tendance clé à suivre pour anticiper l'évolution du métier.
