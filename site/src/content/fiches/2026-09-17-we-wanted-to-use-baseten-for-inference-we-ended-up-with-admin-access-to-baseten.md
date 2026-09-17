---
title: "We wanted to use Baseten for inference. We ended up with admin access to Baseten GitHub repos - Strix"
date: 2026-09-17
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.strix.ai%2Fblog%2Fbaseten-harbor-github-pat-takeover%3Futm_source=tldrdev/1/010001a0a9ee3a28-d0f70b3b-39c2-4b56-bed5-34844dc5139e-000000/NqvmAJx-eXuhsZHwFU4tjEq-7FtuBvt1ECLW1E_d6Yc=452"
keywords: ["sécurité", "agent IA autonome", "fuite d'identifiants", "Docker", "GitHub", "pentest"]
theme: "Sécurité"
tone: "research"
used_in: ["2026-09-17"]
---

## Résumé
Strix, un agent de hacking autonome développé par la société du même nom, a scanné le domaine du fournisseur d'inférence Baseten (valorisé 13 milliards de dollars) avant qu'ils n'en deviennent clients, et a découvert en environ 25 minutes un jeton d'accès personnel GitHub actif offrant des droits d'administrateur sur des dépôts internes critiques de Baseten. Ce jeton, oublié depuis un build Docker de mars 2023, était exposé dans l'historique de build d'une image accessible publiquement via un registre Harbor mal configuré. Baseten a réagi rapidement et de façon professionnelle, sécurisant le registre et révoquant le jeton en moins de 24 heures. L'article détaille la méthodologie de découverte de Strix ainsi que des recommandations concrètes pour éviter ce type de fuite dans les pipelines Docker/CI.

## Points clés
- Strix a repéré, sans identifiants ni accès au code source, un registre Harbor public exposant une image `baseten/baseten-app`.
- Un jeton GitHub personnel (`basetenbot`) datant de mars 2023 était resté visible dans l'historique de build (`history[].created_by`) de l'image, et fonctionnait toujours plus de trois ans plus tard.
- Ce jeton donnait un accès admin/push sur le dépôt produit principal, le dépôt GitOps pilotant les clusters, le tap Homebrew, ainsi qu'un accès lecture/écriture à plusieurs dépôts clients privés.
- Cause racine : un jeton passé en argument de build Docker (`ARG GITHUB_TOKEN`) puis injecté dans la configuration Git via `git config --global`, ce qui persiste sa valeur dans les métadonnées et l'historique de l'image.
- Baseten a confirmé la criticité du problème et corrigé (registre rendu privé, jeton révoqué) en moins de 24 heures, une réponse saluée comme exemplaire par les auteurs.
- L'article recommande d'auditer les anciennes images, d'utiliser des montages de secrets BuildKit, et de limiter la portée et la durée de vie des jetons de build.

## Analyse approfondie
Avant de confier ses données et celles de ses clients à Baseten pour de l'inférence, l'équipe de Strix — un agent de hacking autonome — a décidé de tester la sécurité du fournisseur par précaution, comme elle le fait avec la plupart de ses prestataires. Baseten est un produit reconnu, valorisé 13 milliards de dollars, sur lequel s'appuient de nombreuses entreprises sérieuses ; mais en tant qu'entreprise de sécurité, les auteurs préfèrent systématiquement scanner un tiers avant d'en dépendre, plutôt que de découvrir un problème après coup.

Strix a été pointé vers `*.baseten.co` sans identifiants ni accès au code source. En sortie, il a remonté un jeton d'accès personnel GitHub actif appartenant au compte `basetenbot`, avec des droits admin et push sur le dépôt produit principal de Baseten, sur le dépôt GitOps pilotant leurs clusters, sur leur tap Homebrew, ainsi qu'un accès en lecture/écriture à d'autres dépôts privés, y compris des dépôts spécifiques à certains clients. L'image dans laquelle ce jeton avait été capturé datait de mars 2023 ; le jeton, lui, était toujours valide lorsqu'il a été découvert en juillet 2026. Les auteurs soulignent le professionnalisme de l'équipe sécurité de Baseten, qui a confirmé la criticité du problème, verrouillé le registre concerné et fait tourner le jeton dès le lendemain après-midi — une réactivité qu'ils jugent rare dans ce type de situation.

### Méthodologie : comment Strix a trouvé la faille

Strix a procédé comme n'importe quel bon test d'intrusion commence : par une phase de reconnaissance. Les auteurs rappellent que la vulnérabilité la plus grave se cache souvent sur un sous-domaine oublié, d'où l'intérêt de combiner tests en boîte noire et tests avec accès au code. En énumérant les hôtes et en parcourant les journaux de certificats, Strix a cartographié la surface d'attaque et découvert un registre Harbor à l'adresse `gcp-us-east4-zlw.registry.baseten.co`.

Harbor organise les images de conteneurs en projets, et l'un de ces projets s'est avéré public : sans authentification, Strix pouvait lister les dépôts, obtenir des jetons de pull anonymes et télécharger manifestes et blobs, dont une image nommée `baseten/baseten-app`. Plutôt que de s'arrêter au simple constat d'un registre exposé — certaines entreprises publient volontairement des images, et l'agent cherche à éviter tout faux positif — Strix a choisi de vérifier l'impact réel en inspectant le contenu de l'image. Une première piste, une paire de clés AWS, s'est révélée sans valeur : un appel en lecture seule `sts:GetCallerIdentity` a renvoyé une erreur `InvalidClientTokenId`, signe que la clé était déjà révoquée.

L'agent a poursuivi en récupérant les couches de l'image, en exécutant l'outil open source TruffleHog, puis en inspectant directement la configuration de l'image. C'est là qu'il a mis la main sur un jeton d'accès personnel GitHub, présent dans le champ `history[].created_by` — un champ qui enregistre la commande ayant produit chaque étape de build. En l'occurrence, une commande `RUN` contenait la valeur du `GITHUB_TOKEN` directement injectée en clair. Une requête `GET /user` en lecture seule vers l'API GitHub a confirmé la validité du jeton, associé au compte `basetenbot`. Le point important, selon les auteurs, est que même en purgeant un fichier de credentials du système de fichiers final, l'historique de build téléchargeable avec l'image peut encore contenir une copie du secret — ce qui explique qu'un jeton vieux de plus de trois ans fonctionnait toujours.

### L'étendue des permissions

Un jeton actif n'est dangereux que par les droits qu'il porte. Strix a donc vérifié, toujours via des appels en lecture seule, le scope OAuth (`repo`) et l'appartenance du compte à l'organisation `basetenlabs`, puis le détail des permissions par dépôt :

| Dépôt | Accès |
|---|---|
| `basetenlabs/b***` | **admin: true**, push: true |
| `basetenlabs/f***` | **admin: true**, push: true |
| `basetenlabs/h***` | **admin: true**, push: true |
| `basetenlabs/r***` | Privé, lecture/écriture |
| `basetenlabs/b***` | Privé, lecture/écriture |
| `basetenlabs/t***` | Privé, lecture/écriture |
| `basetenlabs/b***` | Privé, lecture/écriture |

Les auteurs qualifient ce niveau d'accès, laissé accessible dans une image téléchargeable publiquement, d'insensé. Une fois cette confirmation obtenue, l'équipe a jugé disposer de suffisamment d'éléments pour signaler le problème sans risquer un faux positif : aucun dépôt client n'a été cloné, aucune modification n'a été poussée ni aucune configuration altérée. L'e-mail de divulgation a été rédigé immédiatement.

### Origine du problème

L'étape de build contenant le jeton remontait précisément au 3 mars 2023. L'erreur à l'origine de la fuite est classique : pour récupérer des dépendances privées depuis GitHub pendant un build, quelqu'un avait passé un jeton en argument de build selon un motif de ce type :

```
ARG GITHUB_TOKEN
RUN GITHUB_TOKEN=${GITHUB_TOKEN} bash -c '\
if [[ "${GITHUB_TOKEN}" != "" ]]; then \
git config --global --add \
url."https://${GITHUB_TOKEN}@github.com/".insteadOf "git@github.com:"; \
fi'
```

Ce réflexe est compréhensible : le jeton permet à Git de s'authentifier et le build fonctionne. Mais Docker peut enregistrer cet argument de build dans les métadonnées et l'historique de l'image — ce qui s'est produit ici, malgré les avertissements explicites de Docker à ce sujet. Un second problème s'ajoute : la commande `git config --global` écrit l'URL authentifiée, jeton inclus, dans le fichier de configuration Git lui-même, qui peut à son tour se retrouver dans l'image. La correction recommandée consiste à utiliser un montage de secret BuildKit avec une authentification temporaire qui ne persiste pas dans l'image, à inspecter systématiquement couches et historique de build, et surtout à révoquer les anciens jetons — modifier le Dockerfile n'a aucun effet sur les images déjà publiées et téléchargées.

### Ce que révèle l'autonomie de l'agent

Les auteurs insistent sur le fait que Baseten dispose pourtant d'une équipe de sécurité réactive et utilise déjà des outils de sécurité basés sur l'IA ; cela n'a pas empêché un jeton de build de 2023 de conserver un accès admin à des dépôts critiques pendant plus de trois ans. Le risque, selon eux, tient au fait qu'on se concentre naturellement sur l'application et les dépôts source, en oubliant les anciennes images de conteneurs — et que scanner les fichiers d'une image ne suffit pas si l'on ignore son historique de build.

Ce qui les frappe dans ce scan, c'est la façon dont Strix a enchaîné les étapes de façon autonome, sans indication préalable sur Harbor ou sur l'existence d'un jeton : découverte du registre, vérification de la possibilité de récupérer une image, test d'un premier identifiant mort, découverte d'un second identifiant dans l'historique de build, puis vérification complète de ses droits — le tout en environ 25 minutes. Les auteurs y voient une illustration de la raison d'être de Strix : face à la montée des attaques assistées par IA, ils estiment que la seule défense efficace consiste à s'auto-attaquer en continu pour détecter ces failles avant des acteurs malveillants.

### Chronologie de la divulgation

La gestion de l'incident par Baseten est présentée comme exemplaire :

- 13 juillet, 23h10 : signalement du jeton `basetenbot` actif, du projet Harbor public et du détail des permissions sur les dépôts.
- 14 juillet, matin : Baseten rend le projet Harbor privé ; les auteurs signalent que le jeton fonctionne toujours.
- 14 juillet, 16h34 : un membre de l'équipe sécurité de Baseten confirme la criticité, indique que le projet Harbor a été rendu privé et le jeton révoqué, et demande la suppression sécurisée des images récupérées par Strix.
- 14 juillet, 17h05 : confirmation de la suppression, accompagnée de deux constats supplémentaires de sévérité moindre issus du même scan.
- 17 juillet : Baseten clôture les constats restants.
- Septembre : les auteurs informent Baseten de leur intention de publier cette découverte et leur transmettent un brouillon de l'article.

Baseten a également remercié l'équipe avec des t-shirts et des sweats.

### Recommandations pratiques

L'article conclut par une checklist destinée à toute organisation utilisant conteneurs et GitHub :

1. Identifier ce qui peut être récupéré sans authentification, y compris d'anciens tags et projets oubliés.
2. Examiner l'historique de build (`docker history --no-trunc`, ou les champs `history[].created_by` du blob de configuration) ainsi que les couches de l'image.
3. Sortir les secrets des arguments de build, en utilisant des montages de secrets et en s'assurant que les commandes qui les consomment ne les réécrivent pas dans l'image.
4. Limiter précisément ce que les jetons de build peuvent faire : un accès en lecture à une dépendance suffit, un accès admin sur les dépôts produit et déploiement aggrave fortement l'impact d'une fuite ; ajouter systématiquement une date d'expiration.

Les auteurs terminent en invitant les lecteurs à tester leurs propres systèmes avec un outil équivalent à Strix, rappelant que toute cette découverte est partie d'une simple intention d'évaluer un fournisseur d'inférence — et que des attaquants dotés d'IA peuvent suivre exactement le même chemin.

## Pourquoi ça compte
Ce cas illustre concrètement comment des agents IA autonomes peuvent accélérer massivement la découverte de vulnérabilités critiques (25 minutes pour toute la chaîne, de la reconnaissance à l'exploitation de credentials), un signal utile pour la veille sécurité sur les risques liés aux anciennes images Docker et à la gestion des secrets dans les pipelines CI/CD.
