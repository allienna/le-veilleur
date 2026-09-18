---
title: "Stricter enterprise policy enforcement for chrome.debugger in Chrome 155 | Chrome for Developers"
date: 2026-09-18
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fdeveloper.chrome.com%2Fblog%2Fdebugger-enterprise-policy-restrictions%3Futm_source=tldrit/1/010001a0af4cf319-1031fadd-7514-4e10-a19f-5ad4018bc42d-000000/UYHZbUUvgeerfiXiQABV0E6OaUM3h1oeF1yuSVF7QLw=452"
keywords: ["Chrome extensions", "chrome.debugger", "politique d'entreprise", "DLP", "Chrome DevTools Protocol", "administration navigateur"]
theme: "Sécurité"
tone: "news"
used_in: ["2026-09-18"]
---

## Résumé
À partir de Chrome 155, Google renforce l'application des politiques d'entreprise sur l'API `chrome.debugger` utilisée par les extensions. Le changement ne concerne que les navigateurs gérés (managed browsers) dont l'administrateur a configuré `runtime_blocked_hosts`, `DisableScreenshots` ou des règles de prévention de perte de données (DLP) ; les environnements non gérés ne sont pas affectés. Concrètement, dès qu'une de ces restrictions est active, tout appel à `chrome.debugger.attach()` sera purement et simplement rejeté, selon un modèle « tout ou rien », car l'API CDP sous-jacente ne peut pas être filtrée finement par origine. Le déploiement se fait en bêta le 16 septembre 2026 et en stable le 6 octobre 2026, avec un mécanisme de contournement temporaire via un flag jusqu'à Chrome 160.

## Points clés
- Chrome 155 impose un rejet total de `chrome.debugger.attach()` dès qu'une politique `ExtensionSettings` définit une liste non vide de `runtime_blocked_hosts`, même si certaines origines figurent dans `runtime_allowed_hosts`.
- Si la capture d'écran est désactivée par `DisableScreenshots` ou par des règles DLP, `chrome.debugger.attach()` échoue également, avec un message d'erreur dédié.
- Le comportement des profils personnels et des environnements non managés reste inchangé.
- Google recommande de gérer explicitement ces rejets dans le code des extensions et d'envisager une migration vers des API de plus haut niveau (`chrome.scripting`, `chrome.declarativeNetRequest`, `chrome.cookies`) qui respectent les listes d'autorisation/blocage d'hôtes.
- Un flag de contournement temporaire (`--disable-features=ExtensionDebuggerStrictPolicyRestrictions`) est disponible pour les administrateurs le temps de migrer leurs extensions, mais il sera supprimé dans Chrome 160.
- Calendrier : bêta Chrome 155 le 16 septembre 2026, déploiement stable le 6 octobre 2026.

## Analyse approfondie
À partir de Chrome 155, Chrome modifie la façon dont les restrictions de politique d'entreprise s'appliquent aux extensions utilisant l'API `chrome.debugger`.

Ce changement ne concerne que les extensions s'exécutant sur des navigateurs gérés, pour lesquels un administrateur a explicitement configuré `runtime_blocked_hosts`, `DisableScreenshots`, ou des règles de prévention de perte de données (Data Loss Prevention, DLP).

Si une extension s'exécute sur un navigateur non géré, ou dans un environnement d'entreprise sans ces restrictions de politique spécifiques, `chrome.debugger` continue de fonctionner normalement, sans aucun changement.

### Calendrier et déploiement
- **Bêta Chrome 155 :** 16 septembre 2026
- **Déploiement stable de Chrome 155 :** 6 octobre 2026

### Changements clés dans Chrome 155
Les changements suivants n'affectent que les navigateurs gérés en entreprise :

- **Restrictions d'hôtes :** si une politique d'entreprise (`ExtensionSettings`) configure une liste non vide d'hôtes bloqués (`runtime_blocked_hosts`) pour une extension, `chrome.debugger.attach()` est rejeté sur toutes les cibles avec le message : « Host access is restricted by policy. » C'est le cas même si des origines spécifiques figurent dans `runtime_allowed_hosts`.
- **Restrictions liées aux captures d'écran et au DLP :** si la capture d'écran est désactivée par une politique d'entreprise (`DisableScreenshots`) ou par des règles de prévention de perte de données (DLP), `chrome.debugger.attach()` échoue avec le message : « Screenshot capture is restricted by policy. »

Les profils personnels et les environnements non gérés continuent de bénéficier d'un accès sans restriction à `chrome.debugger`, comme auparavant.

L'API `chrome.debugger` donne un accès direct au Chrome DevTools Protocol (CDP), offrant des capacités puissantes, notamment l'évaluation arbitraire de scripts et l'interception réseau. Comme le CDP opère en dessous du modèle d'origine de la plateforme web, un filtrage basé sur l'origine ne peut pas le restreindre de manière sûre. Chrome 155 résout ce problème avec un modèle « tout ou rien », en validant les politiques d'entreprise en amont, dès l'appel à `chrome.debugger.attach()`.

### Actions recommandées pour les développeurs

#### Gérer proprement les rejets d'attachement
Gérez toujours les rejets d'attachement dans le code de votre extension afin de fournir un retour clair aux utilisateurs en entreprise :

```
// Basé sur les promesses (Manifest V3)
try {
  await chrome.debugger.attach({ tabId }, "1.3");
} catch (error) {
  if (error.message.includes("Host access is restricted by policy")) {
    console.warn("Debugger attach blocked: Extension has host restrictions configured by enterprise policy.");
  } else if (error.message.includes("Screenshot capture is restricted by policy")) {
    console.warn("Debugger attach blocked: Screenshots or DLP restrictions are enforced by enterprise policy.");
  } else {
    console.warn("Debugger attach failed:", error.message);
  }
}
// Basé sur les callbacks
chrome.debugger.attach({ tabId }, "1.3", () => {
  if (chrome.runtime.lastError) {
    console.warn("Debugger attach failed:", chrome.runtime.lastError.message);
  }
});
```

#### Envisager des API alternatives de plus haut niveau
Si votre extension n'a pas strictement besoin d'un accès direct au CDP, évaluez une migration vers des API d'extension de plus haut niveau qui prennent en charge des permissions d'hôtes granulaires et qui fonctionnent en cohérence avec les listes d'autorisation et de blocage d'hôtes de l'entreprise :

- Utilisez l'API `chrome.scripting` pour exécuter des scripts et injecter des styles sur les pages autorisées.
- Utilisez l'API `chrome.declarativeNetRequest` pour inspecter, modifier ou bloquer des requêtes réseau de façon déclarative.
- Utilisez l'API `chrome.cookies` avec des permissions d'hôtes standard.

### Recommandations pour les administrateurs d'entreprise
Les administrateurs d'entreprise qui gèrent les politiques d'extensions doivent noter que les extensions nécessitant la permission de débogage ne peuvent pas fonctionner avec des restrictions d'hôtes partielles (`runtime_blocked_hosts`). Si une extension a besoin de `chrome.debugger`, elle ne doit pas avoir d'hôtes bloqués configurés dans `ExtensionSettings`.

Si la capture d'écran est désactivée via `DisableScreenshots` ou des règles de prévention de perte de données (DLP), `chrome.debugger.attach()` échouera.

Les organisations qui ont besoin de listes de blocage d'hôtes ou de restrictions de capture d'écran devraient vérifier si leurs extensions internes ou approuvées peuvent migrer vers des API de plus haut niveau telles que `chrome.scripting` ou `chrome.declarativeNetRequest`.

Si un délai supplémentaire est nécessaire pour migrer les extensions concernées, les administrateurs peuvent revenir temporairement au comportement antérieur à Chrome 155 en lançant Chrome avec le flag en ligne de commande `--disable-features=ExtensionDebuggerStrictPolicyRestrictions`. Notez qu'il s'agit d'une solution de contournement temporaire et que ce flag sera supprimé dans Chrome 160.

### Partager un retour
Pour plus de détails, consultez la documentation de l'API `chrome.debugger`. Pour toute question ou retour, adressez-vous au groupe Google Chromium Extensions.

## Pourquoi ça compte
Ce changement illustre la tension croissante entre les capacités puissantes offertes aux extensions de navigateur et les impératifs de sécurité/conformité en entreprise (DLP, contrôle des hôtes) ; les équipes qui développent ou déploient des extensions internes doivent anticiper dès maintenant une possible rupture de fonctionnalité avec Chrome 155.
