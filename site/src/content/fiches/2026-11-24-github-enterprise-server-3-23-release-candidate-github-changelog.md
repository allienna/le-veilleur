---
title: "GitHub Enterprise Server 3.23 release candidate - GitHub Changelog"
date: 2026-11-24
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fgithub.blog%2Fchangelog%2F2026-11-20-github-enterprise-server-3-23-release-candidate%2F%3Futm_source=tldrit/1/010001a2089020f9-043233d8-eb54-4687-9c0f-67a02ba30045-000000/4qDt7M0dhpymRMaBB-lOY-2Xpq5fmfSCD4i3WQrY3ew=452"
keywords: ["GitHub Enterprise Server", "DevOps", "sécurité des dépendances", "OAuth", "Dependabot", "release candidate"]
theme: "Software"
tone: "news"
used_in: ["2026-11-24"]
---

## Résumé
GitHub publie la release candidate de GitHub Enterprise Server (GHES) 3.23, qui introduit plusieurs nouveautés touchant les Projects, la sécurité des dépendances et l'infrastructure du cluster. Parmi les points forts figurent des filtres de projet plus expressifs, une détection de secrets par IA fonctionnant entièrement en local (y compris en environnement air-gapped), une couverture élargie de la base de données d'advisories GitHub à de nouveaux écosystèmes de paquets, un délai de prudence pour les mises à jour Dependabot, l'expiration des tokens OAuth, et la possibilité de dédier un nœud au primaire Redis dans un cluster GHES. Plusieurs de ces fonctionnalités sont en preview publique et peuvent encore évoluer avant la disponibilité générale.

## Points clés
- Les vues de projet GitHub Projects supportent désormais des filtres combinant `OR`, `AND` et parenthèses pour un regroupement plus précis.
- Détection de secrets non structurés par IA, exécutée localement sur le CPU de l'appliance, sans GPU ni LLM hébergé, compatible air-gapped (preview publique).
- La GitHub Advisory Database couvre désormais les paquets malveillants sur PyPI, Maven, RubyGems, NuGet, Go, Rust et Composer, en plus de npm, via l'ingestion automatique des advisories du dépôt malicious-packages d'OpenSSF.
- Dependabot applique par défaut un délai de trois jours avant d'ouvrir une pull request de mise à jour, laissant le temps de détecter des versions compromises ou buguées.
- Les tokens OAuth peuvent désormais expirer après huit heures avec des refresh tokens pour le renouvellement ; opt-in pour les apps existantes, activé par défaut pour les nouvelles (preview publique).
- Possibilité de déplacer le primaire Redis vers un nœud dédié dans un cluster GHES, sans partager les ressources avec d'autres services comme MySQL.

## Analyse approfondie
GitHub Enterprise Server (GHES) 3.23 est désormais disponible et introduit de nouvelles capacités sur l'ensemble de la plateforme. Voici quelques points forts de la version 3.23 :

- Lorsque vous travaillez dans GitHub Projects, vous pouvez créer des vues de projet plus précises en combinant des filtres avec des `OR` logiques, des `AND` explicites, et des parenthèses pour le regroupement. Par exemple, `(status:Done OR status:Todo) is:issue` affiche les issues ayant l'un ou l'autre statut.
- Si votre entreprise utilise GitHub Secret Protection, vous pouvez détecter des secrets non structurés entièrement au sein de votre réseau grâce à la détection de secrets par IA sur GHES, y compris dans des environnements air-gapped. Un modèle autonome et affiné tourne sur le CPU de l'appliance, sans GPU, sans LLM hébergé, et sans connexion sortante. Cette fonctionnalité est en preview publique et sujette à modification.
- En tant que développeur, vous pouvez identifier les paquets malveillants connus sur PyPI, Maven, RubyGems, NuGet, Go, Rust et Composer grâce à la GitHub Advisory Database, en plus de npm. La base de données ingère automatiquement les advisories de malware du dépôt malicious-packages d'OpenSSF afin d'étendre la couverture à ces écosystèmes.
- Par défaut, Dependabot attend qu'une version de paquet soit disponible sur son registre depuis au moins trois jours avant d'ouvrir une pull request de mise à jour de version. Ce délai de prudence donne aux mainteneurs et à la communauté plus de temps pour détecter et signaler des versions compromises ou buguées avant que les utilisateurs ne fusionnent les mises à jour.
- En tant que développeur d'applications OAuth, vous pouvez limiter la durée de vie des tokens en utilisant des access tokens qui expirent après huit heures, avec des refresh tokens pour obtenir de nouveaux access tokens. L'expiration des tokens est optionnelle pour les applications OAuth existantes et activée par défaut pour les applications nouvellement créées. Vous pouvez demander des tokens expirants avec `scope=offline_access` lors de l'autorisation, pour des tests et un déploiement progressif, ou exiger l'expiration dans l'enregistrement de votre application. Avant d'exiger l'expiration, vous devez mettre à jour tous les clients pour qu'ils demandent, stockent et utilisent les refresh tokens, afin d'éviter de casser la connexion des clients qui ne les supportent pas. Cette fonctionnalité est en preview publique et sujette à modification.
- Dans votre cluster GHES, vous pouvez désormais déplacer le primaire Redis d'un nœud qui exécute aussi d'autres services, comme MySQL, vers un nœud dédié. Redis utilise alors les ressources et le volume de données du nœud dédié plutôt que de les partager avec ces services. Cette procédure n'attache pas un nouveau disque à un nœud existant et n'utilise pas de service Redis externe.

Les release candidates permettent d'essayer les dernières fonctionnalités en avant-première et de partager vos retours avant la disponibilité générale. Pour en savoir plus, consultez « About upgrades to new releases » ainsi que les notes de version de GHES 3.23. Pour commencer, téléchargez la release candidate de GHES 3.23.

Si vous avez des retours ou des questions concernant la release candidate, contactez le support GitHub.

## Pourquoi ça compte
Cette version illustre la tendance des plateformes DevOps à intégrer directement la sécurité de la chaîne d'approvisionnement logicielle (détection de secrets par IA, couverture élargie des advisories, délai de prudence Dependabot) et un contrôle plus fin des accès (expiration des tokens OAuth), des signaux utiles pour toute équipe suivant l'évolution des pratiques de sécurité et d'infrastructure chez les grands éditeurs d'outils de développement.
