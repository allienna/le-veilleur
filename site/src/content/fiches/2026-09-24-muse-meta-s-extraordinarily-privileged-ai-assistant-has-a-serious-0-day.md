---
title: "Muse, Meta's extraordinarily privileged AI assistant, has a serious 0-day"
date: 2026-09-24
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Farstechnica.com%2Fsecurity%2F2026%2F09%2Fmuse-metas-extraordinarily-privileged-ai-assistant-has-a-serious-0-day%2F%3Futm_source=tldrit/1/010001a0ce34a143-103c6133-f4c1-4425-9a6a-d84b86c1254a-000000/BUzDF_Xs1PKy_p-hua6F7Pu5UkkQASV6SEgEaQRs5o8=452"
keywords: ["IA", "Meta", "zero-day", "macOS", "confidentialité", "assistant IA"]
theme: "Sécurité"
tone: "news"
used_in: ["2026-09-24"]
---

## Résumé
Meta a vanté la sécurité de Muse, son nouvel assistant IA pour macOS, comme étant « conçu dès l'origine pour la confidentialité et la sécurité ». Or une faille zero-day découverte dans l'application permet à n'importe quelle application locale ou commande de terminal de prendre le contrôle total de l'agent, contournant les protections système d'Apple. La vulnérabilité expose le jeton d'authentification du compte Muse en détournant le point de terminaison de transcription vers un serveur contrôlé par l'attaquant. Amazon a d'ailleurs commencé à bloquer Muse sur son site dimanche, alimentant les doutes sur la sécurité réelle du produit.

## Points clés
- Muse est un assistant IA macOS de Meta capable de réserver des rendez-vous, remplir des formulaires, faire des achats, générer des images et se connecter à WhatsApp, l'e-mail, le calendrier et les réseaux sociaux.
- Pour fonctionner, Muse doit obtenir des autorisations système étendues sur macOS (micro, caméra, localisation, fichiers), contournant des protections qu'Apple a mis des années à développer.
- Une faille zero-day permet à n'importe quelle app ou commande locale, quelles que soient ses permissions macOS, de modifier des réglages non documentés de Muse.
- Un de ces réglages permet de rediriger le point de terminaison de transcription vers un serveur contrôlé par un attaquant, exposant ainsi le jeton d'authentification du compte.
- Ce jeton donne un contrôle total sur le compte Muse de la victime.
- Amazon a commencé à bloquer Muse sur son site le dimanche précédent la publication, ce qui alimente les interrogations sur la sécurité du produit.

## Analyse approfondie
Mark Zuckerberg, fondateur et PDG de Meta, s'est donné beaucoup de mal pour vanter la sécurité de son nouvel assistant IA, Muse, affirmant qu'il est « conçu dès l'origine pour la confidentialité et la sécurité ». Une vulnérabilité zero-day qui donne aux applications exécutées localement et aux commandes de terminal un contrôle total sur l'agent soulève de sérieux doutes. Autre élément qui alimente les interrogations : Amazon a commencé dimanche à bloquer Muse sur son site.

Meta a lancé Muse il y a quelques semaines. L'assistant « prend des rendez-vous, remplit des formulaires et gère le service client », « retire proactivement des tâches de votre liste », et peut « effectuer des achats, générer des images, créer des documents, et se connecter à vos applications et services préférés ». L'application macOS (curieusement, il n'existe pas de version Windows) fonctionne aussi avec le compte WhatsApp, l'e-mail, le calendrier et les réseaux sociaux de l'utilisateur. Lorsqu'une tâche nécessite un outil qui n'existe pas, Muse le crée à la volée.

### Meta en fait trop sur la sécurité de Muse

Bien sûr, pour que Muse puisse accomplir toutes ces tâches, les utilisateurs doivent d'abord lui donner accès à leurs comptes. Cela implique d'authentifier l'assistant auprès de chaque service et, comme l'application tourne sous macOS, de lui accorder des autorisations sur un large éventail de ressources de l'appareil restreintes par le système d'exploitation, comme l'écriture de fichiers sur le disque, l'accès au micro et à la caméra, ou la surveillance de la localisation et des calendriers. Apple a passé des années à développer ces défenses pour empêcher les applications installées ou les commandes saisies dans le terminal d'accéder à ces ressources, de toute évidence parce que l'entreprise les considère comme une menace pour la sécurité. Muse annule complètement ces mesures par défaut.

La faille zero-day permet à n'importe quelle application ou commande de terminal d'accéder au jeton qui authentifie les utilisateurs auprès de leur compte Muse. Les développeurs de Meta ont conçu l'assistant de telle sorte que toute application installée localement ou tout code exécuté, quelles que soient les permissions macOS dont il dispose, peut modifier une longue liste de réglages non documentés. La plupart sont plutôt anodins, comme le contrôle du mode sombre. L'un de ces réglages, en revanche, n'a rien d'anodin. Il permet à des processus de modifier le point de terminaison où s'effectue la transcription. Normalement, il s'agit d'une adresse de serveur exploitée par Meta. Les attaquants peuvent exploiter cette faille en remplaçant cette adresse par leur propre point de terminaison. Une fois cela fait, les attaquants obtiennent le jeton qui donne un contrôle total sur le compte Muse.

## Pourquoi ça compte
Ce cas illustre un risque structurel des assistants IA « agentiques » très privilégiés : plus un agent obtient d'autorisations système et d'accès à des comptes tiers, plus une faille unique peut avoir des conséquences catastrophiques, malgré un discours marketing rassurant sur la sécurité.
