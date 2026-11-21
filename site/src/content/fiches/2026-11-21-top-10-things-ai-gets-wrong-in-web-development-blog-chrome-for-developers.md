---
title: "Top 10 things AI gets wrong in web development | Blog | Chrome for Developers"
date: 2026-11-21
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fdeveloper.chrome.com%2Fblog%2Ftop-10-things-ai-gets-wrong-in-web-dev%3Futm_source=tldrdev/1/010001a1f8e20cf0-04c1a8d2-b096-40a7-9fd6-0fd535581342-000000/2CmPA2RCHsTIVqKkR1uEGy6hf_d7ookHrL_MceJhBPc=452"
keywords: ["agents de codage IA", "accessibilité web", "sécurité web", "performance web", "bonnes pratiques web", "Modern Web Guidance"]
theme: "IA"
tone: "research"
used_in: ["2026-11-21"]
---

## Résumé
Chrome for Developers a publié la version 1.0 de Modern Web Guidance, un ensemble de compétences qui injectent l'expertise de la plateforme web, les bonnes pratiques et les données de compatibilité navigateur directement dans les agents de codage IA. Leurs évaluations comparatives montrent que même les modèles de pointe les plus récents ne suivent pas, par défaut, les bonnes pratiques du développement web moderne : les agents non guidés ne réussissent qu'environ 50 % des vérifications, contre environ 90 % lorsque Modern Web Guidance est installé. L'article détaille 10 domaines d'erreurs récurrentes couvrant l'accessibilité, l'expérience utilisateur, la performance et la sécurité, avec des exemples concrets observés lors des tests. L'équipe invite la communauté à signaler d'autres lacunes via le dépôt GitHub du projet.

## Points clés
- Les agents de codage IA non guidés ne réussissent qu'environ 50 % des vérifications de bonnes pratiques web, contre 90 % avec Modern Web Guidance installé.
- Les lacunes d'accessibilité les plus fréquentes concernent la gestion du focus clavier et de `inert`, le `prefers-reduced-motion`, et la validation des formulaires.
- En expérience utilisateur, les modèles recourent souvent à du JavaScript impératif fait main (gestes tactiles, dialogues modaux, mode sombre) au lieu des fonctionnalités CSS/HTML natives modernes.
- En performance, les agents appliquent les bonnes pratiques classiques de temps de chargement mais échouent sur la réactivité du thread principal et les décalages de mise en page (CLS).
- En sécurité, les modèles n'ajoutent quasiment jamais de Content Security Policy ou d'assainissement HTML robuste sans qu'on le leur demande explicitement, et échouent sur plus de la moitié des vérifications liées aux passkeys.
- Modern Web Guidance vise à combler ces lacunes via une commande d'installation (`npx modern-web-guidance@latest install`) disponible pour les agents de codage.

## Analyse approfondie
Cette semaine, nous avons publié la version 1.0 de Modern Web Guidance, un ensemble de compétences (skills) qui intègrent l'expertise de la plateforme web, les bonnes pratiques et les données de compatibilité des navigateurs directement dans vos agents de codage. L'objectif de Modern Web Guidance est d'aider les développeurs qui utilisent des agents de codage IA à tirer pleinement parti de la puissance et des capacités de la plateforme web moderne, et in fine d'améliorer les expériences web pour les utilisateurs.

Depuis que nous avons présenté pour la première fois un aperçu anticipé de Modern Web Guidance en mai dernier, les agents de codage n'ont cessé de s'améliorer, et de nombreux nouveaux modèles de pointe (frontier models) impressionnants ont été publiés. L'une des questions que l'on nous pose le plus souvent est : ces nouveaux modèles de pointe ne suivent-ils pas déjà les bonnes pratiques du développement web ?

Malheureusement, la réponse est « non » — et nous savons que la réponse est « non » parce que nous le testons.

Chaque guide de Modern Web Guidance définit un ensemble d'attentes (expectations) qui doivent être vérifiées si les bonnes pratiques du guide ont été correctement suivies. Notre suite d'évaluations (eval suite) teste ensuite ces guides en soumettant le même prompt à un agent exécuté avec Modern Web Guidance installé (l'agent « guidé ») et à un autre agent exécuté sans Modern Web Guidance (l'agent « non guidé »). Le résultat des deux exécutions est ensuite comparé aux attentes définies par le guide.

En comparant les taux de réussite des agents guidés et non guidés, on constate que les modèles d'IA — même les derniers modèles de pointe — ne suivent pas de manière fiable les bonnes pratiques du développement web moderne lorsqu'ils sont laissés à eux-mêmes.

En moyenne, les agents de codage non guidés ne réussissent qu'environ 50 % des vérifications de notre suite d'évaluations, contre environ 90 % lorsque Modern Web Guidance est utilisé.

Vous pouvez consulter notre tableau de bord d'évaluation pour voir la liste complète des vérifications spécifiques que nous effectuons pour chaque guide, ainsi que les scores obtenus par chaque modèle.

Mais pour donner une vue d'ensemble, cet article couvre 10 des domaines les plus problématiques dans lesquels nous constatons que les modèles d'IA se trompent de manière systématique, dans des disciplines clés que les développeurs web sont le plus susceptibles de rencontrer dans leur travail quotidien, comme l'accessibilité, l'expérience utilisateur, la performance et la sécurité.

### 1. Accessibilité : gestion du focus clavier et de inert

Pour les personnes qui naviguent au clavier ou avec un lecteur d'écran, un ordre de focus prévisible est ce qui rend les interfaces interactives utilisables. Sans cela, le focus peut errer dans du contenu d'arrière-plan masqué ou se retrouver bloqué dans des dizaines d'arrêts de tabulation supplémentaires.

La gestion du focus et de inert est l'une des plus grandes lacunes d'accessibilité observées dans nos évaluations, et l'un des domaines qui s'améliore le plus avec Modern Web Guidance. Les erreurs les plus courantes sont les suivantes :

- Ne pas déplacer le focus vers les nouvelles vues ouvertes, et oublier de restaurer le focus sur l'élément déclencheur lors du retour en arrière.
- S'appuyer sur des pièges de tabulation (tab traps) JavaScript manuels et sur `aria-modal="true"` pour des modales personnalisées, au lieu d'utiliser un `<dialog>` modal ou de marquer le contenu d'arrière-plan comme `inert`.
- Exposer chaque élément d'une barre d'outils ou d'une grille directionnelle comme un arrêt de tabulation distinct, au lieu d'utiliser un seul arrêt de tabulation avec un `tabindex` itinérant (roving tabindex).
- Créer des contours `:focus-visible` personnalisés qui n'atteignent pas un ratio de contraste de 3:1 par rapport aux arrière-plans adjacents.

### 2. Accessibilité : prise en charge de la réduction des animations (reduced motion)

Les mouvements de page inattendus et les animations à grande échelle ne sont pas seulement une source de distraction — pour les personnes souffrant de troubles vestibulaires ou de sensibilité au mouvement, ils peuvent provoquer des vertiges, des nausées ou des maux de tête.

Les modèles d'IA pensent généralement à vérifier `prefers-reduced-motion` lors de l'ajout de transitions CSS standards ou d'animations par images clés (keyframe). En revanche, lorsqu'ils utilisent des fonctionnalités plus récentes comme le défilement fluide (smooth scrolling), les view transitions ou les animations pilotées par le défilement (scroll-driven animations), ils oublient souvent la réduction des animations, ou commettent des erreurs lors de sa mise en œuvre :

- Définir `scroll-behavior:smooth` de manière globale et inconditionnelle sur l'élément racine.
- Utiliser des animations CSS pilotées par le défilement sans vérification de la réduction des animations.
- Supprimer les durées de `transition` sur les éléments d'un carrousel pour activer la réduction des animations pendant le défilement, mais oublier de supprimer également les propriétés `transform`, ce qui fait que les éléments changent brusquement de taille pendant le défilement.
- Appliquer une réinitialisation globale de la durée à 0,01 ms sur `*`, `*::before` et `*::after` lorsque la réduction des animations est active, ce qui supprime aussi toutes les transitions essentielles non liées au mouvement (nécessaires pour communiquer les changements d'état de l'interface).
- Activer les view transitions entre documents de manière inconditionnelle et surcharger les animations `::view-transition-*` lorsque la réduction des animations est active, plutôt que de simplement conditionner la règle `@view-transition` à une vérification de la réduction des animations.

### 3. Accessibilité : validation de formulaire, indices de format et états d'autofill

Les formulaires sont la pierre angulaire de la plupart des parcours utilisateurs critiques sur le web. Un simple accroc dans un formulaire de paiement peut avoir un impact majeur sur le chiffre d'affaires d'une entreprise.

Lors de la création de formulaires, les modèles d'IA font bien les choses de base dans l'ensemble. Cependant, ils échouent souvent sur des détails à la fois petits et critiques, comme les erreurs de validation, le bon positionnement des placeholders et des indices de format, ou l'intégration correcte avec les gestionnaires de mots de passe et les fonctionnalités d'autofill :

- Réimplémenter `:user-invalid` en CSS avec une validation JavaScript personnalisée sur `blur`, qui signale souvent comme invalides des champs `required` non touchés dès que l'utilisateur les quitte par tabulation.
- Laisser `aria-invalid` se désynchroniser des erreurs visibles, soit en définissant prématurément `aria-invalid="true"` sur `blur`, soit en stylant `:user-invalid` en CSS sans synchroniser `aria-invalid` en JavaScript.
- S'appuyer sur un texte `placeholder` qui disparaît pour indiquer les formats requis (comme `MM/AA` pour un champ de date d'expiration de carte) au lieu d'afficher un indice persistant lié via `aria-describedby`.
- Placer les indices de format et les règles de mot de passe sous le `<input>` (au lieu de les placer au-dessus), là où ils peuvent être masqués par le clavier mobile et les popovers d'autofill, précisément au moment où l'utilisateur a besoin de les lire.
- Mettre en évidence les champs `:autofill` en changeant uniquement la couleur de la bordure, au lieu d'associer la couleur à un indice non chromatique qui ne modifie pas la mise en page (comme un `box-shadow` en inset).

### 4. Expérience utilisateur : gestes de glissement et tactiles (swipe et touch)

Les agents savent bien implémenter les gestes tactiles en JavaScript impératif et en écrivant leur propre logique physique personnalisée. Ces implémentations fonctionnent ; cependant, les interactions tactiles pilotées par JavaScript donnent rarement la sensation de fluidité à laquelle les utilisateurs sont habitués avec leurs équivalents en application native.

Bon nombre de ces interactions peuvent être implémentées avec CSS et les API de défilement natives, ce qui permet au navigateur d'exécuter la physique des gestes hors du thread principal (main thread). Pourtant, dans nos évaluations, les modèles d'IA négligent souvent ces fonctionnalités :

- Implémenter des gestes de type swipe-to-dismiss ou swipe-to-reveal avec des écouteurs `pointermove` ou `touchmove` au lieu d'utiliser CSS Scroll Snap.
- Omettre `overscroll-behavior-x:none` sur les interfaces à onglets avec swipe, ce qui peut déclencher accidentellement une navigation retour ou avant du navigateur lors d'un over-swipe.
- Piloter les effets de progression du swipe sur le thread principal via des callbacks JavaScript, au lieu d'utiliser des animations pilotées par le défilement (scroll-driven animations).
- Ne pas prendre en charge correctement le focus clavier sur les panneaux d'action à swipe basés sur le défilement.

### 5. Expérience utilisateur : dialogues, popovers et transitions de la top layer

Dans nos évaluations, les modèles recourent souvent à des solutions de contournement JavaScript impératives pour animer, fermer ou contenir le défilement autour des dialogues modaux et des popovers.

Au lieu de s'appuyer sur les fonctionnalités HTML et CSS modernes conçues pour les overlays de la top layer, les agents codent fréquemment à la main des machines à états d'entrée et de sortie, des hooks sur l'historique, et des verrous de défilement sur `body`, plus difficiles à maintenir et propices à des bugs d'interface subtils.

Lorsque ces interactions sont bien réalisées, elles peuvent transformer une expérience qui semble fragile en une expérience soignée à laquelle les utilisateurs font confiance. Voici les erreurs les plus courantes que nous observons :

- Construire des overlays personnalisés en `position:fixed` avec des gestionnaires manuels de clic à l'extérieur pour la fermeture légère (light dismiss), au lieu d'utiliser simplement `popover`.
- Créer des animations d'entrée et de sortie en basculant des classes de transition CSS et en se synchronisant avec `requestAnimationFrame()` et des écouteurs `transitionend` (avec des solutions de repli `setTimeout()`), au lieu de le faire en CSS pur avec `@starting-style` et `transition-behavior`.
- Verrouiller le défilement de la page derrière une modale ouverte en définissant `overflow:hidden` sur `<html>`, au lieu d'utiliser un élément `<dialog>` pour contenir l'overscroll.
- Ajouter des écouteurs `popstate` pour détecter les gestes de retour Android et fermer les modales ouvertes, plutôt que d'utiliser la fonctionnalité native de fermeture au bouton retour d'un élément `<dialog>` modal.

### 6. Expérience utilisateur : mode sombre et contrôles adaptatifs au thème

Les utilisateurs activent le mode sombre pour réduire la fatigue oculaire et l'éblouissement ; un flash blanc vif au chargement de la page, des contrôles de formulaire non thématisés, ou un interrupteur qui se désynchronise de la préférence du système d'exploitation nuisent donc immédiatement à l'expérience.

Un interrupteur de mode sombre peut sembler simple à mettre en place, pourtant les modèles non guidés, dans nos évaluations, manquent systématiquement des détails clés de la plateforme nécessaires pour bien gérer le changement de thème et les contrôles de formulaire natifs :

- Omettre `<meta name="color-scheme" content="light dark">` dans le `<head>`, ce qui provoque, pour les utilisateurs en mode sombre, un flash de toile blanche pendant le chargement des feuilles de style externes.
- Styliser des thèmes sombres ou des composants à surface sombre avec des couleurs personnalisées sans définir `color-scheme`, ce qui laisse les barres de défilement et les contrôles de formulaire natifs bloqués en mode clair.
- Négliger la fonction CSS `light-dark()` lors de la définition de tokens de couleur adaptatifs au thème qui suivent automatiquement le `color-scheme` actif.
- Ne proposer qu'un interrupteur binaire clair/sombre qui définit une surcharge explicite dans `localStorage`, sans option pour revenir au réglage par défaut du système.
- Oublier d'ajouter un écouteur d'événement `storage`, ce qui laisse les autres onglets ouverts désynchronisés lorsque l'utilisateur change de thème.

### 7. Performance : réactivité et fluidité à l'exécution

Les utilisateurs passent la plus grande partie de leur temps sur une page web une fois que celle-ci a fini de se charger ; des interactions lentes et des transitions saccadées peuvent donc nuire à l'expérience utilisateur tout autant qu'un chargement initial lent.

Dans nos évaluations, les modèles suivent généralement les bonnes pratiques classiques en matière de temps de chargement, promues depuis des années par des outils comme Lighthouse, et ils savent généralement décharger les boucles lourdes évidentes vers un Web Worker. Là où ils rencontrent des difficultés constantes, c'est sur la réactivité du thread principal, pourtant essentielle pour optimiser l'INP : isoler le travail de mise en page (layout), planifier les tâches par priorité, et tirer parti des nouvelles fonctionnalités HTML et CSS qui déportent le travail de rendu hors du thread principal.

Par exemple, nous constatons souvent que les agents :

- Créent des files d'attente `setTimeout()` personnalisées pour le travail en arrière-plan ou à faible priorité, au lieu de prioriser les tâches visibles par l'utilisateur avec `scheduler.postTask()` ou de tirer parti de la poursuite de tâche (task continuation) avec `scheduler.yield()` lorsque le navigateur le prend en charge.
- Construisent des mises en page complexes (comme des grilles de données denses) sans appliquer `content-visibility:auto` et `contain-intrinsic-size`, ce qui fait que les mises à jour après les interactions utilisateur déclenchent un reflow de la page entière.
- Masquent les vues inactives d'une SPA avec `display:none` (ou les détruisent) au lieu d'utiliser `content-visibility:hidden` (associé à `inert`). La première approche détruit l'état de rendu mis en cache, de sorte que le retour sur cette vue déclenche un layout et un paint complets.
- Mettent en pause les animations `<canvas>` hors écran et les boucles en arrière-plan via des callbacks Intersection Observer plutôt que d'associer `content-visibility:auto` à l'événement `contentvisibilityautostatechange` (lorsqu'il est disponible), ce qui fait manquer la marge de pré-rendu du navigateur avant que les éléments n'entrent dans la zone visible.
- Construisent des indices d'interface signalant la possibilité de défilement à l'aide d'écouteurs d'événement `scroll` qui forcent des calculs de mise en page continus, plutôt que d'utiliser les requêtes CSS scroll-state lorsqu'elles sont disponibles (avec Intersection Observer en repli).

### 8. Performance : décalages de mise en page et scintillement visuel

Les décalages de mise en page inattendus brisent la concentration du lecteur et peuvent amener les utilisateurs à cliquer sur des boutons inattendus — parfois avec des conséquences irréversibles !

Les modèles ajoutent bien, de manière fiable, les attributs `width` et `height` aux éléments `<img>` standards pour se protéger des décalages de mise en page, mais ils ratent systématiquement d'autres sources courantes de décalages de mise en page et de flashs avant le rendu (pre-paint), provenant des éléments `<video>`, des changements de polices web (font swap), des barres d'outils des navigateurs mobiles, et des expériences côté client — autant d'éléments qui peuvent impacter le CLS.

- Omettre les attributs explicites `width` et `height` sur les éléments `<video>` (si bien que les lecteurs non chargés prennent par défaut une taille de 300×150 et décalent la mise en page une fois les métadonnées chargées), ou styliser les éléments conteneurs des médias au lieu de définir `aspect-ratio` et `object-fit` directement sur les éléments médias.
- Associer des polices web à des polices système de repli sans `font-size-adjust`, ce qui provoque un reflow visible des paragraphes et des titres lorsque les polices web se substituent aux polices de repli.
- Dimensionner les sections hero et les mises en page plein écran avec des unités `vh` statiques au lieu des unités de viewport dynamiques ou petites (`dvh`, `svh`), ce qui fait sauter le contenu lorsque les barres d'outils des navigateurs mobiles apparaissent ou se replient.
- Masquer le contenu avec d'anciens scripts anti-scintillement en `opacity:0` ou `visibility:hidden` et des timeouts de plusieurs secondes pour les tests A/B côté client (ce qui retarde le LCP et laisse des éléments invisibles cliquables), au lieu d'utiliser des scripts avec `blocking="render"` lorsque c'est disponible.
- Déclencher des view transitions entre documents avant que le balisage critique situé au-dessus de la ligne de flottaison n'ait été analysé, au lieu de retenir le premier rendu avec `rel="expect"` et `blocking="render"`, ce qui fait apparaître brusquement des éléments à moitié analysés en pleine transition.

### 9. Sécurité : défenses contre le XSS DOM et assainissement du HTML (sanitization)

Une seule faille de cross-site scripting (XSS) permet à un attaquant d'exécuter du code arbitraire dans le navigateur de vos utilisateurs, de voler des données de session ou d'agir à leur place. C'est pourquoi les défenses imposées par le navigateur, comme l'assainissement sûr du HTML, Trusted Types et des CSP strictes, sont si importantes.

Les modèles traitent rarement ces problématiques de sécurité de manière proactive. Par exemple, sur l'ensemble des tâches de notre suite d'évaluations complète, les modèles n'ont ajouté ni Content Security Policy (CSP) ni en-tête d'isolation cross-origin sans qu'on le leur demande explicitement.

Même lorsque les prompts demandent explicitement de la sécurité, les modèles non guidés continuent d'échouer à plus de la moitié de nos vérifications de sécurité, en se rabattant sur des solutions de repli personnalisées fragiles ou des politiques incomplètes. Cela se voit clairement dans la défense contre le XSS DOM :

- Écrire à la main des assainisseurs (sanitizers) basés sur une allowlist avec `DOMParser` — soit comme solution de repli pour `setHTML()`, soit à l'intérieur d'une politique Trusted Types — au lieu d'utiliser une bibliothèque éprouvée comme DOMPurify lorsque l'assainissement natif n'est pas disponible.
- Inclure systématiquement DOMPurify dans le bundle à chaque chargement de page, au lieu d'utiliser `setHTML()` natif lorsqu'il est pris en charge et de ne charger DOMPurify que de façon différée (lazy), en solution de repli.
- Enregistrer des politiques Trusted Types permissives de type passthrough `(input) => input`, qui sapent l'application des contrôles au niveau des sinks.
- Associer Trusted Types sur des pages statiques à des CSP `script-src 'self'` basées sur une allowlist d'hôtes, au lieu de verrouiller les scripts inline avec des hachages SHA-256.
- Omettre `'strict-dynamic'` et `'report-sample'` lors de la configuration de Content Security Policies `script-src` basées sur un nonce.

### 10. Sécurité : connexion par passkey, réauthentification et cycle de vie des identifiants

Les passkeys améliorent la sécurité pour les utilisateurs et les taux de conversion à la connexion pour les entreprises, mais leur implémentation (même avec l'aide d'agents) reste un défi.

WebAuthn dispose d'API spécifiques de sérialisation, de détection des capacités et de signalement, que les modèles non guidés manquent presque entièrement dans nos évaluations. Si l'on demande à un modèle d'IA d'ajouter la connexion par passkey, sa gestion, ou une réauthentification renforcée (step-up), il écrit souvent des assistants d'encodage d'octets manuels, omet les vérifications de capacités sur l'interface de gestion, ou laisse les identifiants se désynchroniser des gestionnaires de mots de passe :

- Coder à la main des assistants de conversion Base64URL avec `atob()` et `btoa()` — soit comme méthode principale, soit comme code de repli redondant — au lieu de s'appuyer sur les méthodes de sérialisation intégrées comme `parseCreationOptionsFromJSON()`, `parseRequestOptionsFromJSON()` et `credential.toJSON()`.
- Omettre `PublicKeyCredential.signalUnknownCredential()` lors de la connexion lorsque le serveur signale un identifiant d'identification (credential ID) inconnu, laissant ainsi des passkeys supprimées ou révoquées dans les gestionnaires de mots de passe des utilisateurs.
- Omettre `PublicKeyCredential.getClientCapabilities()` avant d'afficher l'interface de création et de gestion des passkeys.
- Omettre un `AbortController` et un `AbortSignal` lors du démarrage des requêtes de réauthentification renforcée par passkey.
- Passer l'option obsolète `mediation:"immediate"` au lieu de `uiMode:"immediate"` pour des invites de connexion simplifiées.

### Combler ces lacunes

Ces 10 domaines sont loin d'être une liste exhaustive, et nous nous attendons à ce que les lacunes spécifiques évoluent avec le temps. Les modèles rattraperont leur retard, et la plateforme web continuera elle-même d'évoluer.

La bonne nouvelle, c'est que Modern Web Guidance comble déjà toutes ces lacunes, et continuera d'évoluer en même temps que la plateforme.

Pour commencer avec Modern Web Guidance, exécutez la commande suivante, ou recherchez-la dans la marketplace de plugins de votre agent :

```
npx modern-web-guidance@latest install
```

Avez-vous observé des modèles se tromper sur d'autres tâches de développement web ? Nous aimerions le savoir. Ouvrez une issue dans le dépôt GitHub de Modern Web Guidance, ou aidez-nous à combler ces lacunes pour d'autres développeurs en contribuant au projet.

## Pourquoi ça compte
Cet article quantifie, avec des données d'évaluation concrètes, l'écart persistant entre les capacités des modèles d'IA de pointe et les exigences réelles du développement web (accessibilité, sécurité, performance), ce qui est directement utile pour toute veille sur les limites actuelles des agents de codage IA et les outils (comme Modern Web Guidance) conçus pour les combler.
