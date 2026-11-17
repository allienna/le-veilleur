---
title: "PyPI's redesigned project pages with clearer security signals are now live - The Python Package Index Blog"
date: 2026-11-17
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fblog.pypi.org%2Fposts%2F2026-11-06-ui-updates-complete%2F%3Futm_source=tldrdata/1/010001a1e4102a7f-1707763f-bcae-44fd-9622-7435fac8cdc6-000000/We4BgUGsJ8VNY3Egxq-QLY_MYg5To3d5hcjl5VlBwk8=452"
keywords: ["PyPI", "provenance", "attestations", "sécurité logicielle", "chaîne d'approvisionnement", "SLSA"]
theme: "Sécurité"
tone: "news"
used_in: ["2026-11-17"]
---

## Résumé
PyPI a achevé la refonte de ses pages de projet afin de rendre les signaux de sécurité, notamment la provenance et les attestations, plus visibles et compréhensibles pour les utilisateurs. Un nouvel onglet « Sécurité » indique désormais l'état de provenance de chaque version (complète ou absente) et affiche des avertissements lorsque les métadonnées sont incohérentes, ce qui peut signaler une compromission de compte ou de pipeline. Le projet, mené avec l'agence Kabu Creative et financé par l'OpenSSF, s'appuie sur l'OpenSSF Attestations Style Guide et s'accompagne d'une refonte des onglets « fichiers de version » et « historique des versions », ainsi que d'une politique, en vigueur depuis juillet 2026, rejetant les fichiers téléversés plus de 14 jours après la version initiale.

## Points clés
- Nouvel onglet « Sécurité » affichant l'état de provenance de chaque version (complète ou absente) et les attestations par fichier.
- Deux types d'attestations supportés : PyPI Publish (confirmant une publication via un Trusted Publisher) et SLSA Build Provenance (lien vers le commit source, la plateforme et les instructions de build).
- Système d'avertissements de provenance détectant des incohérences entre fichiers d'une même version ou des changements de dépôt/workflow par rapport aux versions précédentes, signes possibles de prise de contrôle de compte.
- Page de détail du projet repensée avec bannières de statut hiérarchisées (la quarantaine prime sur tout le reste) et métadonnées reclassées par utilité.
- Nouvelle politique depuis juillet 2026 : rejet des fichiers téléversés plus de 14 jours après l'horodatage de la version initiale, avec signalement des fichiers tardifs antérieurs à cette date.
- Initiative financée par l'OpenSSF et mise en œuvre par Kabu Creative, en s'appuyant sur l'OpenSSF Attestations Style Guide.

## Analyse approfondie
En juillet, PyPI avait annoncé une série de mises à jour prévues pour son interface utilisateur. Façonnées par des recherches menées auprès de membres de la communauté Python, ces mises à jour visent à améliorer la manière dont PyPI présente les signaux de sécurité et affiche les détails des paquets. Ce travail est désormais terminé et déployé sur PyPI.

### Contexte
Avec la croissance rapide de l'écosystème Python, PyPI est devenu une cible de plus en plus attractive pour les acteurs malveillants. En réponse, l'équipe PyPI a déployé de nombreuses fonctionnalités de sécurité tout en jouant un rôle plus actif pour aider les utilisateurs à évaluer et comprendre la sécurité des paquets.

Les attestations numériques, introduites en 2024, illustrent cet effort : elles fournissent un enregistrement vérifiable de la *provenance* d'un fichier de version (d'où il vient). Cependant, la provenance et les attestations restent des concepts peu familiers pour de nombreux utilisateurs de PyPI, et l'interface communiquait mal leur signification, leur importance ou leurs limites.

Pour y remédier, PyPI s'est associé à Kabu Creative afin d'apporter des signaux de sécurité plus clairs à l'interface, en mettant en œuvre les recommandations de l'OpenSSF Attestations Style Guide.

#### Le nouvel onglet Sécurité
Le nouvel **onglet sécurité** communique les états de provenance des versions et affiche les attestations par fichier, offrant un espace dédié pour vérifier d'où proviennent les fichiers de version.

##### États de provenance
PyPI calcule l'état de provenance de chaque version en vérifiant si chaque fichier possède une attestation. En général, une version se trouve dans l'un des deux états suivants :

**Provenance complète** — Cela signifie que 100 % des fichiers de la version possèdent des attestations, portant l'un ou l'autre (ou les deux) des types d'attestation pris en charge :

Les **attestations PyPI Publish** confirment que le fichier a été publié par un Trusted Publisher PyPI.

Les **attestations SLSA Build Provenance** relient le fichier à son commit source exact, à sa plateforme de build et à ses instructions de build.

Les métadonnées d'attestation peuvent être consultées directement dans l'interface, avec un lien vers le journal de transparence pour plus d'informations.

**Aucune provenance** — Cela signifie simplement qu'aucun fichier de la version ne possède d'attestation. C'est typique des versions plus anciennes ou des projets qui n'ont pas encore configuré le Trusted Publishing. **L'absence de provenance n'indique pas nécessairement qu'une version ou un fichier est malveillant ; cela signifie seulement que l'origine du fichier ne peut pas être vérifiée cryptographiquement.**

En l'absence de provenance, il est recommandé de s'appuyer sur les signaux de confiance environnants pour évaluer la sécurité, tels que l'historique du mainteneur, les schémas de publication et l'activité du dépôt. Les mainteneurs sont encouragés à utiliser le Trusted Publishing avec un publisher qui génère des attestations pour leur prochaine version.

#### Avertissements de provenance
Les avertissements de provenance sont conçus pour aider à identifier quand un fichier pourrait ne pas provenir des mainteneurs du projet, par exemple si un attaquant a pris le contrôle d'un compte ou d'un workflow de publication.

Lorsque les métadonnées de provenance semblent inhabituelles ou entrent en conflit avec l'historique d'un projet, PyPI affiche un avertissement bien visible. De nombreux avertissements ont des explications légitimes, mais chacun mérite d'être vérifié avant installation :

- Certains fichiers portent des attestations tandis que d'autres non (par exemple, des wheels publiées via Trusted Publishing, mais une archive source téléversée à l'aide d'un jeton d'API). Dans ce cas, il convient de vérifier les notes de version pour d'éventuels problèmes de build, ou de poser la question dans le gestionnaire de tickets du projet avant d'installer.
- Les fichiers d'une même version proviennent de systèmes de build ou de dépôts source différents. Il convient alors de vérifier les métadonnées d'attestation pour confirmer que tous les fichiers proviennent bien de sources contrôlées par les mainteneurs.
- Les fichiers de version proviennent d'un dépôt ou d'un workflow différent de celui de la version précédente. Bien que souvent légitime (changement de nom d'organisation, migration de dépôt), cela peut aussi indiquer un pipeline compromis ou une prise de contrôle de compte ; il convient de consulter les notes de version ou les canaux officiels pour confirmer qu'une migration d'infrastructure était planifiée.
- Un projet qui publiait auparavant avec des attestations est passé à un téléversement de fichiers sans attestation. Il convient de vérifier si les mainteneurs ont intentionnellement modifié leur processus de publication (par exemple en revenant à des jetons d'API) ; si ce changement est inattendu, la version doit être traitée avec scepticisme jusqu'à vérification.

La documentation utilisateur de PyPI détaille davantage la provenance, les attestations et ces avertissements.

### Page de détail du projet repensée
Pour accompagner ces changements, la page de détail du projet a également été mise à jour :

- Les avertissements de provenance apparaissent désormais en haut de la page, aux côtés des bannières de statut pour les versions retirées (yanked), les projets archivés et les pré-versions. Si un projet ou une version est mis en quarantaine, seule la bannière de quarantaine est affichée, car elle prime sur tous les autres avertissements et bannières.
- Lorsqu'une version a une provenance complète ou des avertissements de provenance, son état de provenance est affiché dans la barre latérale, avec un lien vers l'onglet sécurité pour plus d'informations.
- Les métadonnées sont désormais classées par utilité et étiquetées « PyPI data » ou « Data verified by PyPI », remplaçant l'ancienne présentation où les données étaient regroupées et classées par statut de vérification.

### Fichiers de version et historique des versions
L'onglet **fichiers de version** repensé aide à trouver le bon fichier en recherchant et en filtrant de longues listes. Il permet aussi de consulter l'état de provenance de chaque fichier dans le tableau, et de repérer rapidement les fichiers tardifs, signalés par une icône d'avertissement orange.

Les avertissements de fichier tardif apparaissent lorsqu'un ou plusieurs fichiers ont été téléversés plus de 14 jours après l'horodatage de la version initiale. Ces avertissements n'apparaissent que sur les versions antérieures à juillet 2026, date à laquelle une politique a été introduite pour rejeter les nouveaux fichiers après 14 jours.

L'onglet **historique des versions** fournit désormais également plus de détails sur chaque version, en exposant le nombre de fichiers, l'état de provenance et le statut de la version (mise en quarantaine, retirée, archivée ou pré-version).

### Obtenir de l'aide
Parallèlement aux mises à jour de l'interface, la documentation utilisateur de PyPI a été enrichie pour aider à mieux naviguer dans la sécurité des paquets, via un guide de sécurité des paquets.

### Perspectives et remerciements
Le nouvel onglet sécurité donne à PyPI un espace dédié pour les futurs types d'attestation et avis de sécurité. Pour permettre à l'ensemble de l'écosystème open source de bénéficier de ce travail, une étude de cas a également été publiée dans l'OpenSSF Attestations Style Guide, détaillant les modèles de conception et les avertissements développés au cours de ce projet.

Cette initiative a été financée par l'Open Source Security Foundation et mise en œuvre par Kabu Creative. L'équipe PyPI remercie Dustin Ingram, Zach Steindler, et les membres de l'OpenSSF Securing Software Repositories Working Group pour avoir porté cet effort. Un remerciement particulier est adressé à Mike Fiedler, Jacob Coffee, et aux membres de l'équipe PyPI pour leurs retours de conception et leurs revues de code, à @cofiem pour ses contributions au nouvel onglet des fichiers de version, ainsi qu'aux participants aux entretiens utilisateurs et aux testeurs de la communauté pour avoir aidé à façonner la conception finale.

Enfin, l'équipe remercie l'OpenSSF pour son financement et son partenariat continu dans la sécurisation de l'écosystème de packaging Python.

## Pourquoi ça compte
Ces évolutions renforcent la capacité des développeurs à détecter des compromissions de la chaîne d'approvisionnement logicielle (supply chain) dans l'écosystème Python, un vecteur d'attaque en forte croissance ; elles illustrent aussi comment les standards de l'OpenSSF (attestations, SLSA) se traduisent concrètement dans l'UX d'un registre de paquets majeur.
