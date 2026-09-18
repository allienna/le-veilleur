---
title: "Stricter enterprise policy enforcement for chrome.debugger in Chrome 155 | Chrome for Developers"
date: 2026-09-18
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fdeveloper.chrome.com%2Fblog%2Fdebugger-enterprise-policy-restrictions%3Futm_source=tldrit/1/010001a0af4cf319-1031fadd-7514-4e10-a19f-5ad4018bc42d-000000/UYHZbUUvgeerfiXiQABV0E6OaUM3h1oeF1yuSVF7QLw=452"
keywords: ["Chrome 155", "chrome.debugger", "extensions", "politique d'entreprise", "DLP", "CDP"]
theme: "Sécurité"
tone: "news"
used_in: ["2026-09-18"]
---

## Résumé
À partir de Chrome 155, Google durcit l'application des politiques d'entreprise sur l'API `chrome.debugger` utilisée par les extensions. Le changement ne concerne que les navigateurs gérés dont l'administrateur a configuré des restrictions d'hôtes (`runtime_blocked_hosts`), désactivé les captures d'écran (`DisableScreenshots`) ou mis en place des règles DLP. Dans ces cas, `chrome.debugger.attach()` est désormais rejeté en bloc plutôt que filtré finement, selon un modèle « tout ou rien », car le protocole CDP opère en dessous du modèle d'origine du web et ne peut pas être restreint de façon sûre par origine. Le déploiement est prévu en bêta le 16 septembre 2026 et en stable le 6 octobre 2026, avec un flag de contournement temporaire disponible jusqu'à Chrome 160.

## Points clés
- Le changement ne s'applique qu'aux navigateurs gérés en entreprise avec des politiques spécifiques configurées ; les profils personnels et environnements non gérés ne sont pas affectés.
- Si `runtime_blocked_hosts` est configuré (même partiellement, même avec des exceptions dans `runtime_allowed_hosts`), `chrome.debugger.attach()` est rejeté sur toutes les cibles.
- Si les captures d'écran sont désactivées via `DisableScreenshots` ou des règles DLP, l'attachement du debugger échoue également.
- Le modèle choisi est « tout ou rien » car le CDP donne un accès trop puissant (exécution de scripts arbitraires, interception réseau) pour être filtré de façon fiable par origine.
- Un flag de ligne de commande (`--disable-features=ExtensionDebuggerStrictPolicyRestrictions`) permet un contournement temporaire, supprimé à partir de Chrome 160.
- Google recommande aux développeurs de migrer vers des API de plus haut niveau (`chrome.scripting`, `chrome.declarativeNetRequest`, `chrome.cookies`) si un accès CDP complet n'est pas strictement nécessaire.

## Analyse approfondie
À partir de Chrome 155, Chrome modifie la façon dont les restrictions de politique d'entreprise s'appliquent aux extensions utilisant l'API `chrome.debugger`.

Ce changement n'affecte que les extensions s'exécutant sur des navigateurs gérés pour lesquels un administrateur a explicitement configuré `runtime_blocked_hosts`, `DisableScreenshots`, ou des règles de prévention des pertes de données (DLP, Data Loss Prevention).

Si une extension s'exécute sur un navigateur non géré, ou dans un environnement d'entreprise sans ces restrictions de politique spécifiques, `chrome.debugger` continue de fonctionner normalement, sans changement.

### Calendrier et déploiement

- **Chrome 155 Beta :** 16 septembre 2026
- **Déploiement stable de Chrome 155 :** 6 octobre 2026

### Principaux changements dans Chrome 155

Les changements suivants n'affectent que les navigateurs gérés en entreprise :

- **Restrictions d'hôtes :** Si une politique d'entreprise (`ExtensionSettings`) configure une liste non vide d'hôtes bloqués (`runtime_blocked_hosts`) pour une extension, `chrome.debugger.attach()` est rejeté sur toutes les cibles avec le message : « Host access is restricted by policy. » (Accès à l'hôte restreint par la politique.) C'est le cas même si des origines spécifiques sont incluses dans `runtime_allowed_hosts`.
- **Restrictions liées aux captures d'écran et au DLP :** Si la capture d'écran est désactivée par une politique d'entreprise (`DisableScreenshots` ou des règles de prévention des pertes de données (DLP)), `chrome.debugger.attach()` échoue avec le message : « Screenshot capture is restricted by policy. » (Capture d'écran restreinte par la politique.)

Les profils personnels et les environnements non gérés continuent d'avoir un accès sans restriction à `chrome.debugger`, comme auparavant.

L'API `chrome.debugger` donne un accès direct au Chrome DevTools Protocol (CDP), offrant des capacités puissantes telles que l'évaluation arbitraire de scripts et l'interception du trafic réseau. Comme le CDP opère en dessous du modèle d'origine de la plateforme web, un filtrage basé sur l'origine ne peut pas le restreindre de manière sûre. Chrome 155 résout ce problème avec un modèle *tout ou rien*, en validant les politiques d'entreprise en amont, dès l'appel à `chrome.debugger.attach()`.

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

#### Envisager des API de plus haut niveau alternatives

Si votre extension n'a pas strictement besoin d'un accès direct au CDP, envisagez de migrer vers des API d'extension de plus haut niveau qui prennent en charge des permissions d'hôtes granulaires et fonctionnent avec les listes d'autorisation et de blocage d'hôtes définies par l'entreprise :

- Utilisez l'API `chrome.scripting` pour exécuter des scripts et insérer des styles dans les pages autorisées.
- Utilisez l'API `chrome.declarativeNetRequest` pour inspecter, modifier ou bloquer des requêtes réseau de manière déclarative.
- Utilisez l'API `chrome.cookies` avec les permissions d'hôtes standard.

### Recommandations pour les administrateurs d'entreprise

Les administrateurs d'entreprise qui gèrent les politiques d'extensions doivent noter que les extensions nécessitant la permission debugger ne peuvent pas fonctionner avec des restrictions d'hôtes partielles (`runtime_blocked_hosts`). Si une extension a besoin de `chrome.debugger`, elle ne doit avoir aucun hôte bloqué configuré dans `ExtensionSettings`.

Si la capture d'écran est désactivée via `DisableScreenshots` ou des règles de prévention des pertes de données (DLP), `chrome.debugger.attach()` échouera.

Les organisations qui ont besoin de listes de blocage d'hôtes ou de restrictions sur les captures d'écran devraient vérifier si leurs extensions internes ou approuvées peuvent migrer vers des API de plus haut niveau telles que `chrome.scripting` ou `chrome.declarativeNetRequest`.

Si un délai supplémentaire est nécessaire pour migrer les extensions concernées, les administrateurs peuvent temporairement revenir au comportement antérieur à Chrome 155 en lançant Chrome avec l'option de ligne de commande `--disable-features=ExtensionDebuggerStrictPolicyRestrictions`. Notez qu'il s'agit d'une solution de contournement temporaire et que ce flag sera supprimé dans Chrome 160.

### Partager vos retours

Pour plus de détails, consultez la documentation de l'API `chrome.debugger`. Pour toute question ou retour, contactez le groupe Google Chromium Extensions.

## Pourquoi ça compte
Ce changement impose aux équipes de sécurité et aux développeurs d'extensions d'entreprise d'anticiper des ruptures fonctionnelles dès octobre 2026 et de revoir leur dépendance au CDP au profit d'API plus granulaires, un signal clair du durcissement continu du modèle de sécurité des extensions Chrome.
