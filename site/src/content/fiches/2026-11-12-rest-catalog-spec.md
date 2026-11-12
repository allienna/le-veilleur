---
title: "REST Catalog Spec"
date: 2026-11-12
url: "https://substack.com/redirect/fbbb710f-21d3-4028-913e-7d56332052be?j=eyJ1IjoiN3Y1bG1jIn0.HlvPOGYPdVknSYzEK1JIj6IFkAFn8zuyjtfU9Mbft9Q"
keywords: ["Apache Iceberg", "catalogue REST", "OpenAPI", "interopérabilité", "lakehouse", "métadonnées"]
theme: "Data"
tone: "tutorial"
used_in: ["2026-11-12"]
---

## Résumé
Ce document présente la spécification REST Catalog d'Apache Iceberg, une API standardisée (basée sur OpenAPI) permettant de gérer les métadonnées de table et les opérations de catalogue. Elle a été conçue par la communauté pour résoudre les problèmes de compatibilité posés par les catalogues enfichables, lorsque chaque langage ou moteur devait réimplémenter son propre client. Le protocole apporte une interopérabilité accrue entre langages et moteurs, une meilleure fiabilité via des commits basés sur les changements, une gestion simplifiée des métadonnées et des fonctionnalités avancées comme le partage sécurisé de tables. Une spécification OpenAPI YAML et une interface Swagger UI sont disponibles pour l'explorer de façon interactive.

## Points clés
- Le REST Catalog est une API commune, basée sur la spécification OpenAPI, pour interagir avec n'importe quel catalogue Iceberg.
- Il joue un rôle analogue au protocole thrift de Hive pour HMS, mais à l'échelle de l'écosystème Iceberg.
- Il améliore la compatibilité entre langages et moteurs : un seul client REST suffit pour supporter n'importe quel catalogue.
- Il renforce la fiabilité grâce aux commits basés sur les changements, permettant la déconfliction et les relances côté serveur.
- Il permet des fonctionnalités avancées : chargement paresseux des snapshots, commits multi-tables, mise en cache et partage sécurisé via credential vending ou remote signing.
- Des outils existent pour l'adoption : la classe `CatalogHandlers` pour la traduction vers les catalogues intégrés, et l'image Docker communautaire `iceberg-rest-fixture`.

## Analyse approfondie
### REST Catalog API Specification 🔗
Iceberg définit une API Catalog basée sur REST pour gérer les métadonnées de table et effectuer des opérations de catalogue. Vous pouvez trouver la spécification OpenAPI ici : REST Catalog OpenAPI YAML.

Vous pouvez également explorer l'API de manière interactive à l'aide de la Swagger UI.

### REST Catalog Protocol 🔗
À mesure que le projet Iceberg s'est développé pour prendre en charge davantage de langages et de moteurs, les catalogues enfichables (pluggable) ont commencé à poser des problèmes pratiques. Les catalogues devaient être implémentés dans plusieurs langages, et il s'est avéré difficile pour les offres commerciales de prendre en charge de nombreux catalogues et clients différents.

Pour résoudre les problèmes de compatibilité et ouvrir la voie à de nouvelles fonctionnalités, la communauté a créé le protocole REST catalog, une API commune (utilisant la spécification OpenAPI) pour interagir avec n'importe quel catalogue Iceberg. C'est l'équivalent du protocole thrift de Hive pour HMS.

Le protocole REST est important pour plusieurs raisons :

- **Compatibilité des langages et des moteurs** : les nouveaux langages et moteurs peuvent prendre en charge n'importe quel catalogue avec une seule implémentation client.
- **Fiabilité améliorée** : il utilise des commits basés sur les changements (change-based commits) pour permettre la déconfliction et les relances côté serveur — moins d'échecs !
- **Gestion simplifiée des métadonnées** : les mises à niveau de version des métadonnées sont plus simples car les métadonnées racines sont écrites par le service de catalogue.
- **Fonctionnalités avancées** : il permet de nouvelles fonctionnalités telles que le chargement paresseux des snapshots (lazy snapshot loading), les commits multi-tables et la mise en cache.
- **Sécurité** : le protocole prend en charge le partage sécurisé de tables via la distribution d'identifiants (credential vending) ou la signature à distance (remote signing).

Vous pouvez utiliser le protocole REST catalog avec n'importe quel catalogue intégré via la traduction dans la classe `CatalogHandlers`, ou en utilisant l'image Docker `iceberg-rest-fixture` maintenue par la communauté.

## Pourquoi ça compte
Le REST Catalog devient le standard de facto pour l'interopérabilité des catalogues dans l'écosystème data lakehouse (Iceberg, moteurs, outils commerciaux), un point clé à suivre pour quiconque évalue ou intègre des architectures de données modernes.
