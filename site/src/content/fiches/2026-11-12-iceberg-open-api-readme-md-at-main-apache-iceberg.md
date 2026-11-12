---
title: "iceberg/open-api/README.md at main · apache/iceberg"
date: 2026-11-12
url: "https://substack.com/redirect/3ae4d1d5-3c99-411d-aae9-80efe59dce50?j=eyJ1IjoiN3Y1bG1jIn0.HlvPOGYPdVknSYzEK1JIj6IFkAFn8zuyjtfU9Mbft9Q"
keywords: ["Apache Iceberg", "REST Catalog", "OpenAPI", "lakehouse", "tests de compatibilité"]
theme: "Data"
tone: "tutorial"
used_in: ["2026-11-12"]
---

## Résumé
Ce document est le README technique du module `open-api` du projet Apache Iceberg. Il décrit le fichier `rest-catalog-open-api.yaml`, qui spécifie l'interface du REST Catalog d'Iceberg, ainsi que les commandes permettant de valider (lint) et de régénérer le code à partir de cette spécification OpenAPI. Il détaille également le REST Compatibility Kit (RCK), un kit de tests de conformité (TCK) permettant de vérifier qu'un serveur REST tiers respecte bien la spécification REST Catalog d'Iceberg, avec sa configuration via variables d'environnement ou propriétés système Java et son exécution via Gradle.

## Points clés
- Le fichier `rest-catalog-open-api.yaml` définit l'interface du REST Catalog d'Iceberg.
- Les commandes `make install` + `make lint` valident la spécification OpenAPI ; `make install` + `make generate` régénèrent le code Python correspondant (`rest-catalog-open-api.py`) après une modification du YAML, bien que ce code généré ne soit pas utilisé en production — il sert uniquement à visualiser l'impact des changements.
- Le REST Compatibility Kit (RCK) est un TCK basé sur l'implémentation Java de référence du REST Catalog, exécutable contre n'importe quel serveur REST implémentant la spécification.
- La configuration du RCK se fait via des variables d'environnement préfixées `CATALOG_` (avec des règles de transformation du nom de clé) ou via des propriétés système Java préfixées `rck.`.
- Plusieurs comportements de test sont configurables (ex. : création obligatoire de namespace, support des retries côté serveur, support des points dans les noms, support des variants), car la spécification REST ne les impose pas tous strictement.
- Les tests de compatibilité se lancent via Gradle, avec un serveur HTTP local adossé à une base JDBC par défaut, ou contre un serveur REST externe via `-Drck.local=false`.

## Analyse approfondie
Le fichier `rest-catalog-open-api.yaml` définit l'interface du REST catalog.

Pour s'assurer que la définition open-api est valide, vous pouvez exécuter la commande `lint` :

```
make install
make lint
```

Lors de la mise à jour de `rest-catalog-open-api.yaml`, assurez-vous de mettre à jour `rest-catalog-open-api.py` avec les changements de la spécification en exécutant les commandes suivantes :

```
make install
make generate
```

Le code généré n'est pas utilisé dans le projet, mais il aide à visualiser les changements apportés dans le code généré par la définition de l'open-API.

Le REST Compatibility Kit (RCK) est une implémentation de Technology Compatibility Kit (TCK) pour la spécification REST d'Iceberg. Cela comprend une série de tests basés sur l'implémentation Java de référence du REST Catalog, qui peuvent être exécutés contre n'importe quel serveur REST implémentant la spécification.

Le RCK peut être configuré soit via des variables d'environnement, soit via des propriétés système Java, et permet de configurer à la fois les tests et le client REST. Les variables d'environnement préfixées par `CATALOG_` sont transmises à la configuration du catalogue avec les mutations suivantes :

1. Le préfixe `CATALOG_` est supprimé du nom de la clé
2. Un simple underscore (`_`) est remplacé par un point (`.`)
3. Un double underscore (`__`) est remplacé par un tiret (`-`)
4. Les noms de clés sont convertis en minuscules

Une configuration d'environnement de base ressemblerait à ceci :

```
CATALOG_URI=https://my_rest_server.io/                    ## -> uri=https://my_rest_server.io/
CATALOG_WAREHOUSE=test_warehouse                          ## -> warehouse=test_warehouse
CATALOG_IO__IMPL=org.apache.iceberg.aws.s3.S3FileIO       ## -> io-impl=org.apache.iceberg.aws.s3.S3FileIO
CATALOG_CREDENTIAL=<oauth_key>:<oauth_secret>             ## -> credential=<oauth_key>:<oauth_secret>
```

Les propriétés Java transmises au test doivent être préfixées par `rck.`, ce qui peut être utilisé pour configurer certaines configurations de test décrites ci-dessous, ainsi que toute propriété du client du catalogue.

Un exemple de la même configuration utilisant des propriétés système Java ressemblerait à ceci :

```
rck.uri=https://my_rest_server.io/                    ## -> uri=https://my_rest_server.io/
rck.warehouse=test_warehouse                          ## -> warehouse=test_warehouse
rck.io-impl=org.apache.iceberg.aws.s3.S3FileIO        ## -> io-impl=org.apache.iceberg.aws.s3.S3FileIO
rck.credential=<oauth_key>:<oauth_secret>             ## -> credential=<oauth_key>:<oauth_secret>
```

Certains comportements de test sont configurables selon les implémentations de catalogue. Tous les comportements ne sont pas strictement définis par la spécification REST. Les éléments suivants sont actuellement configurables :

| config | défaut |
|---|---|
| rck.requires-namespace-create | true |
| rck.supports-serverside-retry | true |
| rck.overrides-requested-location | false |
| rck.supports-names-with-dot | false |
| rck.supports-variant | false |

Les tests de compatibilité peuvent être invoqués via gradle avec la commande suivante :

Note : le comportement par défaut est d'exécuter un serveur http local avec un backend jdbc à des fins de test, donc `-Drck.local=false` doit être défini pour pointer vers un serveur REST externe.

```
./gradlew :iceberg-open-api:test --tests RESTCompatibilityKitSuite \
 -Drck.local=false \
 -Drck.requires-namespace-create=true \
 -Drck.uri=https://my_rest_server.io/ \
 -Drck.warehouse=test_warehouse \
 -Drck.credential=<oauth_key>:<oauth_secret>
```

## Pourquoi ça compte
Le REST Catalog est devenu le mécanisme d'interopérabilité central entre moteurs (Spark, Trino, Flink, Snowflake, etc.) autour du format de table Iceberg ; disposer d'un TCK officiel comme le RCK est donc un signal fort pour toute veille sur la standardisation du lakehouse et sur la fiabilité des intégrations multi-moteurs.
