---
title: "Microsoft Authenticator Flaw Let Permissionless Android Apps Steal Work Account Tokens"
date: 2026-10-29
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fthehackernews.com%2F2026%2F10%2Fmicrosoft-authenticator-flaw-let.html%3Futm_source=tldrit/1/010001a18276797c-740d9479-a7ac-4f58-b887-2d3068969a39-000000/I3WW69HZWAeU1AG7bj3xrsH1aNnsm6gWZlz0lt5Lxsw=452"
keywords: ["Microsoft Authenticator", "vulnérabilité Android", "vol de jetons", "CVE-2026-80097", "authentification mobile", "Enclave"]
theme: "Sécurité"
tone: "news"
used_in: ["2026-10-29"]
---

## Résumé
Microsoft a corrigé une faille dans son application Authenticator pour Android (CVE-2026-80097, score CVSS 8.6) qui permettait à une application malveillante sans aucune permission de se faire passer pour une application de confiance comme Teams et de récupérer les jetons de connexion d'un compte professionnel. Découverte par le chercheur Ofek Levin via un programme de la société de sécurité Enclave, la faille exploitait un composant exposé (AccountChooserActivity) dont la vérification de signature pouvait être contournée. Microsoft affirme que la faille n'a pas été exploitée dans la nature et nécessite une interaction de l'utilisateur, tandis qu'Enclave affirme que son preuve de concept fonctionnait sans aucune interaction. La correction est disponible dans la version 6.2606.4246 d'Authenticator pour Android.

## Points clés
- La faille CVE-2026-80097 touche Microsoft Authenticator pour Android et a été corrigée dans la version 6.2606.4246.
- Une application sans permission pouvait usurper l'identité d'une application de confiance (ex. Teams) pour obtenir des jetons Microsoft Graph donnant accès aux e-mails, fichiers et calendriers.
- La vérification de signature censée bloquer l'usurpation vérifiait la signature de l'application réellement installée, pas celle de l'application ayant réellement fait la demande.
- Désaccord notable entre Enclave (aucune interaction utilisateur nécessaire) et Microsoft (une étape de connexion dans Authenticator est requise).
- Microsoft juge l'exploitation "peu probable", la faille n'a pas été divulguée publiquement avant le correctif et n'est pas dans le catalogue CISA KEV au 26 octobre 2026.
- Le correctif ne précise pas si la mise à jour invalide les jetons déjà obtenus par une éventuelle application malveillante.

## Analyse approfondie
Microsoft a corrigé une faille dans son application Authenticator pour Android qui permettait à une application malveillante sans aucune permission de se faire passer pour une application Microsoft de confiance, comme Teams, et de collecter les jetons de connexion du compte professionnel d'une victime.

Microsoft référence la faille sous le nom CVE-2026-80097 et l'a corrigée dans la version 6.2606.4246 d'Authenticator pour Android ; toute personne utilisant l'application devrait donc la mettre à jour.

Dans les tests des chercheurs, les jetons donnaient un accès complet aux e-mails, fichiers et calendrier du compte. Microsoft indique que l'exploitation nécessite également que la victime complète une étape de connexion dans Authenticator, et que la faille n'a pas été utilisée dans des attaques.

La recherche provient d'Ofek Levin, qui travaillait dans le cadre d'un programme de fellowship auprès de la société de sécurité Enclave, laquelle a publié les détails techniques le 23 octobre 2026. Microsoft a attribué le CVE le 8 septembre et l'a noté 8.6 sur l'échelle CVSS, qu'elle qualifie d'« Important ».

Sur Android, Authenticator fait plus qu'afficher des codes à six chiffres. Il agit aussi comme un courtier (broker) : lorsque Teams, Outlook ou une autre application Microsoft doit connecter un utilisateur, elle le demande à Authenticator, et Authenticator renvoie un jeton, un laissez-passer numérique qui prouve que l'utilisateur est connecté. Parce que ce courtier contrôle l'accès à l'ensemble du compte, il devrait être prudent quant à l'application à laquelle il accorde un jeton.

La faille permettait à la mauvaise application d'en obtenir un. Authenticator expose un composant, une activité nommée **AccountChooserActivity**, que n'importe quelle application présente sur l'appareil peut démarrer. Lorsque l'application de l'attaquant démarrait cette activité, Authenticator construisait sa demande de jeton à partir des valeurs fournies par l'application de l'attaquant, y compris le nom de l'application qu'elle prétendait être. L'application affirmait être Teams, et le courtier la croyait.

Une vérification de signature était censée empêcher cela, mais elle n'y est pas parvenue. Cette vérification recherchait la signature réelle de l'application usurpée et confirmait que la demande correspondait à celle-ci. Comme Teams était réellement installée sur l'appareil, sa vraie signature était disponible pour être lue, et la vérification passait donc avec succès.

Authenticator pouvait également voir quelle application avait réellement effectué la demande, a constaté Enclave, mais elle n'utilisait pas cette information pour décider s'il fallait accorder un jeton.

Dans les tests d'Enclave, se faire passer pour Teams et demander des jetons Microsoft Graph renvoyait des permissions permettant de lire et d'envoyer des e-mails, de lire et d'écrire des fichiers, et de lire et d'écrire dans les calendriers, entre autres.

Microsoft décrit le résultat de manière plus générale : un attaquant qui réussirait pourrait s'authentifier en tant qu'utilisateur connecté et accéder aux ressources de cet utilisateur. Les jetons s'appliquent au compte professionnel connecté à Authenticator sur cet appareil, et non à d'autres comptes.

Les deux parties sont en désaccord sur un point que le lecteur devrait prendre en compte. Enclave a rapporté que sa preuve de concept renvoyait des jetons sans aucune interaction de l'utilisateur, autre que la présence d'un compte connecté.

L'avis de Microsoft indique que l'exploitation nécessite d'installer une application malveillante sur l'appareil et de convaincre l'utilisateur de compléter un flux d'authentification dans Authenticator. Son score CVSS indique également que la faille nécessite une interaction de l'utilisateur.

Microsoft affirme que la faille n'a pas été exploitée et n'a pas été divulguée publiquement avant le correctif, et évalue l'exploitation comme « peu probable ». Elle faisait partie du Patch Tuesday de septembre 2026 de l'entreprise et n'était pas l'une des deux failles Windows signalées ce mois-là comme déjà sous attaque active. La vulnérabilité ne figure pas dans le catalogue des vulnérabilités exploitées connues (Known Exploited Vulnerabilities) de la CISA américaine au 26 octobre 2026.

Le correctif consiste à mettre à jour Microsoft Authenticator pour Android vers la version 6.2606.4246 ou une version ultérieure, comme indiqué dans l'avis de Microsoft. Les organisations qui gèrent des appareils Android peuvent imposer cette version minimale via leur gestion des appareils. L'avis de Microsoft fournit le correctif mais ne précise pas si la mise à jour annule les jetons qu'une application malveillante aurait pu déjà obtenir, ce point reste donc flou dans les sources disponibles.

## Pourquoi ça compte
Ce cas illustre comment une faille de logique dans un mécanisme de confiance inter-applications (plutôt qu'une vulnérabilité classique) peut exposer des comptes professionnels entiers, et souligne l'importance de vérifier l'identité réelle de l'appelant plutôt que ses seules déclarations déclaratives, un point de vigilance pertinent pour toute équipe sécurité suivant l'écosystème Microsoft 365/Entra ID.
