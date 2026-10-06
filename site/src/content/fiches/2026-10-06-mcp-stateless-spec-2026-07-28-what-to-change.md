---
title: "MCP Stateless Spec 2026-07-28: What to Change"
date: 2026-10-06
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fimportstatic.com%2Fai%2Fmcp-stateless-spec-migration%3Futm_source=tldrit/1/010001a10c03b4ed-ebe552a3-143e-4c23-87f0-7bcca5a769cc-000000/a48klcmu9lNbhuXV7zBTq2_9O4aRJa16FgVNKWinRto=452"
keywords: ["MCP", "protocole sans état", "SDK Go", "API", "sécurité", "LLM"]
theme: "IA"
tone: "tutorial"
used_in: ["2026-10-06"]
---

## Résumé
La révision 2026-07-28 du Model Context Protocol (MCP) élimine la poignée de main `initialize` et les sessions côté serveur, rendant chaque requête autonome grâce aux métadonnées `_meta`, à de nouveaux en-têtes HTTP obligatoires (`Mcp-Method`, `Mcp-Name`) et à un système de versioning sans négociation. L'article, basé sur des tests concrets avec le SDK Go officiel (v1.8.0), détaille comment migrer les serveurs existants : remplacer l'état de session par des handles explicites, gérer les demandes d'entrée utilisateur (elicitation) via le nouveau mécanisme `input_required`/multi-round-trip, et activer l'option `Stateless` du SDK. Il couvre aussi la compatibilité avec les anciens clients, les dépréciations (roots, sampling, logging) garanties pendant douze mois, et fournit une checklist en sept points pour opérer la migration.

## Points clés
- Le MCP sans état supprime `initialize` et `Mcp-Session-Id` ; chaque requête porte sa version de protocole, l'identité et les capacités du client dans `_meta`.
- Les en-têtes HTTP `Mcp-Method` et `Mcp-Name` sont désormais obligatoires et vérifiés contre le corps JSON, sous peine d'erreur `-32020`.
- La négociation de version disparaît au profit de `server/discover` et de l'erreur `-32022` listant les versions supportées.
- Les interactions nécessitant une réponse de l'utilisateur (elicitation, sampling, roots) passent par un résultat `input_required` et un mécanisme de relance avec `requestState`, qui doit être signé car potentiellement manipulé par un attaquant.
- Le SDK Go active ce mode via l'option `StreamableHTTPOptions.Stateless` ; les anciens clients retombent automatiquement sur le protocole 2025-11-25.
- Roots, sampling et logging sont dépréciés (pas supprimés) avec une garantie de douze mois, tandis que `ping` et `logging/setLevel` sont déjà totalement retirés.

## Analyse approfondie
Testé avec Go 1.27.1 et go-sdk v1.8.0. Le JSON est copié depuis deux gestionnaires locaux.

La révision 2026-07-28 du Model Context Protocol (MCP) a supprimé les deux éléments autour desquels la plupart des serveurs étaient construits : la poignée de main (handshake) `initialize` et la session. La première requête HTTP d'un client peut désormais être un `tools/call`, et n'importe quelle instance derrière un répartiteur de charge peut y répondre. C'est toute l'idée derrière le MCP sans état (stateless). Il s'agit toujours de la version la plus récente du protocole, et le SDK Go officiel la prend en charge depuis la v1.7.0.

Pour l'auteur d'un serveur, le travail se divise en trois parties : arrêter de dépendre d'une session, envoyer les nouveaux champs requis, et réécrire tout outil qui demande quelque chose au client en plein milieu d'un appel. Voici chaque changement tel qu'il apparaît sur le fil (wire).

### Le MCP sans état signifie que chaque requête porte son propre contexte

Sous les versions 2025-11-25 et antérieures, un client ouvrait la connexion avec une poignée de main. Voici ce qu'un gestionnaire construit avec les valeurs par défaut du SDK Go a répondu à une requête POST `initialize` dans notre test :

```
200 OK
Content-Type: application/json
Mcp-Session-Id: P6RQHIL2JVW4X2IFODILDENZ6X
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "capabilities": { "tools": { "listChanged": true } },
    "protocolVersion": "2025-11-25",
    "serverInfo": { "name": "demo", "version": "1.0.0" }
  }
}
```
Le client devait ensuite envoyer `notifications/initialized` et joindre cet identifiant de session à chaque requête ultérieure, ce qui signifiait que chaque requête ultérieure devait atteindre une instance connaissant la session.

Le changelog du 2026-07-28 supprime les deux éléments. La version du protocole, l'identité du client et les capacités du client voyagent désormais dans `_meta` sur chaque requête. Voici la seule et unique requête que nous avons envoyée à un gestionnaire sans état :

```
POST /mcp HTTP/1.1
Content-Type: application/json
Accept: application/json, text/event-stream
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: add
{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{
  "name":"add","arguments":{"a":2,"b":40},
  "_meta":{
    "io.modelcontextprotocol/protocolVersion":"2026-07-28",
    "io.modelcontextprotocol/clientInfo":{"name":"probe","version":"0.1.0"},
    "io.modelcontextprotocol/clientCapabilities":{"elicitation":{"form":{}}}
  }}}
```
Et la réponse, sans en-tête de session :

```
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "_meta": {
      "io.modelcontextprotocol/serverInfo": { "name": "demo", "version": "1.0.0" }
    },
    "content": [ { "type": "text", "text": "{\"sum\":42}" } ],
    "structuredContent": { "sum": 42 },
    "resultType": "complete"
  }
}
```
Deux champs sont nouveaux dans la réponse. Le serveur s'identifie lui-même dans le `_meta` de chaque résultat, car il n'y a pas de poignée de main pour le faire. Et chaque résultat possède désormais un `resultType` obligatoire, qui est `"complete"` ici ; l'autre valeur apparaît plus loin.

Si votre serveur conservait quoi que ce soit par session, c'est la partie à repenser. La réponse du changelog est que les serveurs ayant besoin d'un état entre les appels doivent utiliser des handles explicites, générés par le serveur, transmis comme des arguments d'outil ordinaires. Un `cart_id` renvoyé par un outil et requis par le suivant fonctionne sur n'importe quelle instance, et il est également visible par le modèle.

### Les en-têtes HTTP sont vérifiés par rapport au corps de la requête

La requête ci-dessus répète la méthode et le nom de l'outil dans `Mcp-Method` et `Mcp-Name`. La page Streamable HTTP de la spécification les rend obligatoires afin que les passerelles (gateways) et les limiteurs de débit puissent router sur la base des en-têtes sans analyser le JSON, et elle exige que le serveur rejette une requête où l'en-tête et le corps sont en désaccord. Sans cela, un proxy pourrait autoriser un outil tout en laissant le serveur en exécuter un autre.

Le SDK Go applique cette règle. Nous avons envoyé `Mcp-Name: deploy` avec un corps appelant `add`, puis une requête sans aucun `Mcp-Method` :

```
400 Bad Request
{"jsonrpc":"2.0","id":4,"error":{"code":-32020,
 "message":"header mismatch: Mcp-Name header value 'deploy' does not match body value 'add'"}}
400 Bad Request
{"jsonrpc":"2.0","id":5,"error":{"code":-32020,"message":"missing required Mcp-Method header"}}
```
Si vous maintenez un client écrit à la main, c'est le point le plus facile à manquer : une requête du 2026-07-28 est refusée sans ces en-têtes, même si son corps est parfaitement correct. `Mcp-Name` est obligatoire pour `tools/call`, `resources/read` et `prompts/get`, et porte `params.name` ou `params.uri`.

La même page supprime le flux GET autonome et les flux reprenables (resumable). Un `GET` adressé à notre gestionnaire sans état a renvoyé `405 Method Not Allowed`. Un flux de réponse interrompu perd désormais la requête en vol, et le client doit la renvoyer avec un nouvel identifiant de requête. Les notifications de changement qui arrivaient autrefois sur le flux GET sont désormais délivrées en réponse à une requête `subscriptions/listen`, que le client ouvre lorsqu'il souhaite les recevoir.

### Les erreurs de version et `server/discover` remplacent la négociation

La page consacrée au versioning l'indique directement : « Il n'y a pas de poignée de main de négociation. Chaque requête porte sa propre version du protocole, et le serveur accepte ou rejette chaque requête indépendamment ». Un serveur qui n'implémente pas la version demandée répond avec l'erreur `-32022` et la liste des versions qu'il prend en charge. Nous avons demandé une version qui n'existe pas :

```
{
  "jsonrpc": "2.0",
  "id": 6,
  "error": {
    "code": -32022,
    "message": "unsupported protocol version",
    "data": {
      "supported": ["2026-07-28", "2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05"],
      "requested": "2027-01-01"
    }
  }
}
```
Un client qui veut cette information en amont appelle `server/discover`. Les serveurs doivent l'implémenter ; les clients sont libres de l'ignorer. La réponse du SDK dans notre test :

```
{
  "resultType": "complete",
  "_meta": { "io.modelcontextprotocol/serverInfo": { "name": "demo", "version": "1.0.0" } },
  "ttlMs": 0,
  "cacheScope": "public",
  "supportedVersions": ["2026-07-28", "2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05"],
  "capabilities": { "tools": { "listChanged": true } }
}
```
`ttlMs` et `cacheScope` sont également nouveaux, et obligatoires sur les résultats de `tools/list`, `prompts/list`, `resources/list`, `resources/templates/list` et `resources/read`. Ils indiquent à un client combien de temps il peut réutiliser la réponse et si un intermédiaire partagé peut la mettre en cache. La valeur par défaut du SDK, `0`, signifie « périmé immédiatement », donc un client n'en tire aucun bénéfice. La documentation du package décrit un hook `ServerOptions.SetCacheable` permettant de définir des valeurs réelles ; une liste d'outils qui ne change qu'au déploiement est une bonne candidate pour un TTL long.

### Dans le SDK Go, le nouveau protocole se cache derrière une seule option

Si vous avez suivi notre tutoriel de serveur MCP en Go, votre gestionnaire HTTP a été créé avec des options `nil`, et ce gestionnaire conserve des sessions. Dans go-sdk v1.8.0, un gestionnaire conservant des sessions ne parle pas le 2026-07-28. Le même `tools/call` moderne envoyé à ce gestionnaire nous a renvoyé :

```
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32022,
    "message": "protocol version \"2026-07-28\" is not supported by this server",
    "data": {
      "supported": ["2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05"],
      "requested": "2026-07-28"
    }
  }
}
```
Rien ne casse pour les clients du SDK, car ils retombent sur la poignée de main, mais vous restez alors sur l'ancien protocole. Le commutateur est `Stateless` :

```
// newHandler returns the Streamable HTTP handler. With stateless set, the
// handler accepts protocol version 2026-07-28 and keeps no session.
func newHandler(stateless bool) http.Handler {
	s := newServer()
	return mcp.NewStreamableHTTPHandler(func(*http.Request) *mcp.Server { return s }, &mcp.StreamableHTTPOptions{
		Stateless:    stateless,
		JSONResponse: true,
	})
}
```
Avec elle, le client du SDK a négocié `2026-07-28` ; sans elle, `2025-11-25`. Le code de l'outil était identique dans les deux cas.

Le gestionnaire sans état n'a pas exclu les anciens clients dans notre test. Il a répondu à un `initialize` ancien avec la version de protocole `2025-11-25` et sans `Mcp-Session-Id`, et il a répondu à un `tools/call` 2025-11-25 qui n'avait pas eu de poignée de main avant lui. C'est important, car la matrice de compatibilité de la spécification est sans détour sur l'alternative : un client ancien face à un serveur exclusivement moderne échoue, et les anciens clients n'ont aucun moyen de rattraper le protocole. Il y a toutefois un piège pour de tels clients, sur lequel la section suivante se heurte.

### Les outils qui demandent quelque chose à l'utilisateur renvoient `input_required`

L'élicitation (elicitation), l'échantillonnage (sampling) et les racines (roots) étaient auparavant des requêtes que le serveur envoyait au client pendant qu'un appel d'outil était ouvert. Cela nécessite un flux maintenu ouvert et une instance qui se souvient de l'appel. Le modèle des requêtes à plusieurs allers-retours (multi round-trip requests) inverse la logique : le serveur termine l'appel avec un résultat indiquant ce dont il a besoin, et le client relance la requête avec les réponses. Seuls `tools/call`, `prompts/get` et `resources/read` peuvent procéder ainsi.

Dans le SDK Go, le gestionnaire renvoie `InputRequests` lors du premier appel et lit `InputResponses` lors de la relance :

```
func deploy(_ context.Context, req *mcp.CallToolRequest, in DeployInput) (*mcp.CallToolResult, any, error) {
	if resp, ok := req.Params.InputResponses["confirm"].(*mcp.ElicitResult); ok && resp != nil {
		if !verifyState(req.Params.RequestState, in.Service, time.Now()) {
			return nil, nil, &jsonrpc.Error{Code: jsonrpc.CodeInvalidParams, Message: "invalid requestState"}
		}
		if resp.Action != "accept" || resp.Content["ok"] != true {
			return &mcp.CallToolResult{
				Content: []mcp.Content{&mcp.TextContent{Text: "deploy of " + in.Service + " cancelled"}},
			}, nil, nil
		}
		return &mcp.CallToolResult{
			Content: []mcp.Content{&mcp.TextContent{Text: "deployed " + in.Service}},
		}, nil, nil
	}
	return &mcp.CallToolResult{
		InputRequests: mcp.InputRequestMap{
			"confirm": &mcp.ElicitParams{
				Message: fmt.Sprintf("Deploy %s to production?", in.Service),
				RequestedSchema: &jsonschema.Schema{
					Type:       "object",
					Properties: map[string]*jsonschema.Schema{"ok": {Type: "boolean"}},
					Required:   []string{"ok"},
				},
			},
		},
		RequestState: signState(in.Service, time.Now().Add(5*time.Minute)),
	}, nil, nil
}
```
Le premier appel a renvoyé ce résultat (le bloc `_meta` est tronqué) :

```
{
  "content": null,
  "requestState": "ZGVwbG95fGJpbGxpbmd8MTc5MTEwMzk2MA.607524b40890a1bab45b5ad37e211a3ad2a40e7f9b08804f24efaf75f8223ab9",
  "resultType": "input_required",
  "inputRequests": {
    "confirm": {
      "method": "elicitation/create",
      "params": {
        "mode": "form",
        "message": "Deploy billing to production?",
        "requestedSchema": {
          "type": "object",
          "properties": { "ok": { "type": "boolean" } },
          "required": ["ok"]
        }
      }
    }
  }
}
```
La relance est un nouveau `tools/call` avec un nouvel `id`, les mêmes arguments, et deux paramètres supplémentaires :

```
"inputResponses": { "confirm": { "action": "accept", "content": { "ok": true } } },
"requestState": "ZGVwbG95fGJpbGxpbmd8MTc5MTEwMzk2MA.607524b4...ab9"
```
Elle a renvoyé `"deployed billing"` avec `resultType: "complete"`.

`requestState` est l'endroit où se loge la mémoire du serveur, et elle revient en passant par le client ; la spécification demande donc aux serveurs de la traiter comme contrôlée par un attaquant potentiel. Si elle influence l'autorisation ou la logique métier, elle doit être protégée en intégrité, et la page recommande de la lier au principal (l'identité appelante), à une expiration courte et à la requête d'origine. Notre fonction `signState` place l'outil, le nom du service et une expiration sous un HMAC-SHA256 avec une clé partagée par toutes les instances. Lorsque nous avons rejoué l'état de l'appel `billing` sur un appel pour `payments`, le serveur a répondu `-32602 invalid requestState`. La spécification avertit également que rien de tout cela ne rend un état à usage unique ; une action à usage unique nécessite toujours une vérification côté serveur.

Vous n'avez pas besoin d'écrire vous-même la boucle de relance côté client. Le client du SDK effectuait les deux allers-retours à l'intérieur d'un seul `CallTool`, en appelant notre `ElicitationHandler` entre les deux. Dans la v1.8.0, la boucle abandonne après 10 tours, et `MultiRoundTripOptions.Disabled` la désactive si vous voulez piloter vous-même les relances.

Le même gestionnaire servait aussi l'ancien protocole. Face au gestionnaire conservant les sessions, le SDK a négocié `2025-11-25`, a transformé les `InputRequests` en une élicitation classique initiée par le serveur, et `deploy` a renvoyé le même texte. Le piège concerne un client ancien face au gestionnaire sans état. Avec le client fixé sur `2025-11-25`, l'appel a échoué :

`calling "tools/call": multi-round-trip: fulfilling input request "confirm": client does not support elicitation`

Le SDK documente pourquoi : un gestionnaire sans état « utilise une session temporaire avec des paramètres d'initialisation par défaut pour chaque requête », si bien que les capacités déclarées par l'ancien client dans `initialize` ont disparu au moment où l'outil s'exécute. Les outils simples fonctionnent pour les anciens clients sur un gestionnaire sans état ; les outils qui ont besoin d'une entrée de leur part ne fonctionnent pas.

### Ce qu'il faut changer, dans l'ordre

1. Repérez ce que votre serveur conserve par session et déplacez-le vers des handles explicites transmis comme arguments d'outil, ou vers `requestState` pour un seul appel.
2. Réécrivez les outils qui appellent l'élicitation, l'échantillonnage ou les racines en plein milieu d'un appel pour qu'ils renvoient des demandes d'entrée (input requests), et signez tout état qu'ils envoient.
3. Mettez à jour le SDK et activez le gestionnaire sans état. En Go, cela correspond à go-sdk v1.7.0 ou ultérieur avec `Stateless: true`.
4. Décidez si les anciens clients comptent encore. Si c'est le cas et que vos outils ont besoin d'une entrée de leur part, conservez un point de terminaison conservant les sessions à côté de celui sans état jusqu'à leur mise à jour.
5. Dans les clients écrits à la main, ajoutez `_meta`, `MCP-Protocol-Version`, `Mcp-Method` et `Mcp-Name`, traitez un `resultType` manquant venant d'un ancien serveur comme `"complete"`, et gérez `-32022` en relançant avec une version tirée de `supported`.
6. Mettez à jour la gestion des erreurs : une ressource introuvable est désormais `-32602` au lieu de `-32002`, et une méthode inconnue sur HTTP renvoie un `404` avec un corps JSON-RPC `-32601`.
7. Définissez de vraies valeurs de `ttlMs` sur les résultats de liste, et renvoyez les outils dans un ordre déterministe, ce que le changelog demande afin que les clients et les caches de prompts LLM puissent réutiliser la liste.

Planifiez ensuite les dépréciations. Les racines, l'échantillonnage et la journalisation (logging) fonctionnent encore, et la politique de cycle de vie adoptée avec cette révision garantit aux fonctionnalités dépréciées une durée d'au moins douze mois, mais le changelog indique que les nouvelles implémentations ne devraient pas les ajouter. Les remplacements suggérés sont des paramètres d'outil ou des URI de ressource à la place des racines, un appel direct à votre fournisseur de LLM à la place de l'échantillonnage, et stderr ou OpenTelemetry à la place de la journalisation du protocole. `ping` et `logging/setLevel` sont déjà totalement supprimés, donc un mécanisme de keepalive basé sur `ping` doit disparaître lors de votre migration.

### Questions fréquentes

#### Le MCP est-il désormais sans état ?

Oui, depuis la version de protocole 2026-07-28, publiée le 28 juillet 2026. La poignée de main `initialize` et l'en-tête `Mcp-Session-Id` sont supprimés, et chaque requête porte désormais sa version de protocole, l'identité du client et les capacités du client dans `_meta`. Les serveurs qui souhaitent aussi accueillir d'anciens clients peuvent continuer à répondre à `initialize`.

#### Les clients MCP envoient-ils encore `initialize` ?

Pas sous le 2026-07-28. Un client peut envoyer `tools/call` comme première requête, ou appeler `server/discover` au préalable pour connaître les versions et capacités prises en charge. Un client qui prend en charge les deux époques retombe sur `initialize` lorsque le serveur ne répond pas avec une erreur moderne reconnue.

#### Comment un serveur MCP pose-t-il une question à l'utilisateur sans session ?

Il renvoie un résultat avec `resultType` égal à `input_required` et une carte `inputRequests`, au lieu d'envoyer sa propre requête. Le client recueille les réponses et relance l'appel d'origine avec `inputResponses`, en renvoyant le `requestState` opaque si le serveur en avait fourni un.

#### Comment activer MCP 2026-07-28 dans le SDK Go ?

Utilisez go-sdk v1.7.0 ou une version ultérieure, et définissez `StreamableHTTPOptions.Stateless` à `true`. Dans notre test sur la v1.8.0, un gestionnaire sans cette option rejetait les requêtes 2026-07-28 avec l'erreur `-32022`, et le client du SDK retombait sur le 2025-11-25.

#### L'échantillonnage, les racines et la journalisation MCP sont-ils supprimés ?

Non, ils sont dépréciés dans le 2026-07-28, pas supprimés. La politique de cycle de vie de la spécification garantit aux fonctionnalités dépréciées une fenêtre minimale de douze mois, et le changelog indique que les nouvelles implémentations ne devraient pas les adopter.

### Sources vérifiées pour cet article (8)

1. Spécification MCP 2026-07-28 : principaux changements – Suppression des sessions et de la poignée de main initialize, server/discover, subscriptions/listen, requêtes à plusieurs allers-retours, resultType, en-têtes obligatoires, ttlMs et cacheScope, dépréciations, renumérotation des codes d'erreur
2. La spécification du 2026-07-28, blog MCP, 28 juillet 2026 – Date de publication et résumé du modèle sans état
3. Spécification MCP 2026-07-28 : Streamable HTTP – En-têtes Mcp-Method et Mcp-Name, HeaderMismatch -32020, 404 pour méthode inconnue, suppression du GET et de la reprenabilité, règles de compatibilité ascendante
4. Spécification MCP 2026-07-28 : Versioning et compatibilité – Pas de poignée de main de négociation, UnsupportedProtocolVersionError -32022, matrice de compatibilité moderne, ancienne et mixte
5. Spécification MCP 2026-07-28 : Requêtes à plusieurs allers-retours – InputRequiredResult, inputRequests, inputResponses, règles d'intégrité et de rejeu de requestState, méthodes pouvant le renvoyer
6. Spécification MCP 2026-07-28 : Discovery – server/discover est obligatoire pour les serveurs et optionnel pour les clients ; champs de DiscoverResult
7. Documentation du package mcp, go-sdk v1.8.0 – StreamableHTTPOptions.Stateless, ServerOptions.SetCacheable et SupportedProtocolVersions, MultiRoundTripOptions, CallToolParams.InputResponses et RequestState
8. Versions go-sdk : v1.7.0 et v1.8.0 – v1.7.0 ajoute la version de protocole 2026-07-28 ; v1.8.0 est la dernière version et n'ajoute aucune version de protocole plus récente

## Pourquoi ça compte
Pour toute équipe développant ou intégrant des serveurs ou clients MCP (protocole utilisé pour relier les LLM à des outils externes), cette migration est incontournable à moyen terme : elle change la gestion d'état, le contrat HTTP et la sécurité des échanges, avec un impact direct sur l'architecture (scaling horizontal sans affinité de session) et la compatibilité des intégrations IA existantes.
