---
title: "The Path to Rails 8.1: From Vue and jQuery to Stimulus"
date: 2026-11-14
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fblog.dnsimple.com%2F2026%2F11%2Frails-8-1-vue-and-jquery-to-stimulus%3Futm_source=tldrdev/1/010001a1d4d6d4f1-3f79bd2d-3bd3-45e7-9808-ba3d194e24a0-000000/2GUH4UbpJp2TtXDMv8AVnIceotT-sDCpglcptqI6ZU8=452"
authors: ["Dallas Read"]
keywords: ["Rails", "Stimulus", "Vue.js", "jQuery", "Turbo", "migration frontend"]
theme: "Software"
tone: "tutorial"
used_in: ["2026-11-14"]
---

## Résumé
DNSimple a achevé la migration de son application Rails vers les valeurs par défaut de Rails 8.1 en supprimant l'intégralité de ses composants Vue (environ 50) et de son code jQuery. L'article détaille, à travers l'exemple concret d'une vérification pré-vol de la résolution DNS, comment une méthode en trois questions (HTML natif ? rendu serveur ? sinon, JavaScript minimal) a permis de remplacer un composant Vue de 350 lignes par une Turbo Frame couplée à un contrôleur Stimulus. Le résultat est une logique métier centralisée côté serveur en Ruby, un nombre de requêtes réduit par page, et un seul pattern JavaScript (Stimulus) à maintenir pour toute l'application.

## Points clés
- DNSimple a supprimé la totalité de ses ~50 composants Vue et de son code jQuery lors de sa migration vers les défauts de Rails 8.1.
- jQuery posait problème car Turbo Drive ne déclenche pas `DOMContentLoaded` à chaque visite, cassant les scripts de page attachés à ce hook.
- Vue posait problème car les importmaps ne peuvent pas compiler des single-file components, obligeant à garder une étape de build JavaScript.
- Méthode de décision en trois questions : HTML natif possible ? sinon rendu serveur possible ? sinon, JavaScript minimal via Stimulus.
- Le composant Vue de 350 lignes (17 props, 6 états) gérant la vérification DNS a été remplacé par une Turbo Frame rendue serveur + un contrôleur Stimulus de 192 lignes, supprimant au passage 3 requêtes redondantes par page.
- La prochaine étape de la série migrera le CSS (Bootstrap/Tachyons vers Tailwind) via des ViewComponents.

## Analyse approfondie

L'article est le deuxième d'une série consacrée à la migration de DNSimple vers les conventions par défaut de Rails 8.1. Le premier épisode avait remplacé rails-ujs par Turbo Drive, révélant au passage des effets de bord que l'ancien JavaScript masquait depuis des années. Celui-ci s'attaque au JavaScript lui-même : où est-il parti ?

Le point de départ est une question laissée en suspens dans l'article précédent : comment supprimer autant de code sans rien perdre ? La réponse concrète porte sur la pop-up de vérification DNS préalable à certaines actions (ajout d'enregistrements, transfert d'e-mail, commande de certificat) : ce composant Vue de 350 lignes a été déplacé côté serveur et transformé en Turbo Frame pilotée par un contrôleur Stimulus. Plus largement, l'application comptait une cinquantaine de composants Vue et une quantité importante de jQuery ; elle n'en a aujourd'hui plus aucun. Le bénéfice mis en avant n'est pas seulement la suppression de lignes de code, mais la centralisation de la logique métier : ce qui était auparavant dupliqué entre Ruby (serveur) et JavaScript (navigateur) vit désormais uniquement côté serveur, et le JavaScript restant suit un unique pattern (Stimulus), facilitant le débogage et l'ajout de fonctionnalités.

**Pourquoi abandonner Vue et jQuery.** Les deux technologies ont échoué pour des raisons différentes. Vue nécessitait une étape de build dédiée car les importmaps ne savent pas compiler des composants « single-file » — ce build se dressait entre DNSimple et l'objectif d'une application Rails sans bundler JavaScript. jQuery, de son côté, s'appuyait majoritairement sur des scripts de page attachés à des sélecteurs `js-*` via l'événement `DOMContentLoaded`. Or Turbo Drive ne redéclenche pas cet événement à chaque navigation : dès qu'une page passait sous Turbo, ces scripts cessaient simplement de fonctionner.

**La méthode de migration.** Pour chaque composant à migrer, l'équipe s'est posé systématiquement trois questions, dans cet ordre : un élément HTML natif peut-il suffire, sans JavaScript ? Sinon, le serveur peut-il directement rendre le HTML plutôt que de laisser le navigateur récupérer du JSON et le transformer lui-même en HTML ? Et seulement si aucune des deux options ne convient, quel est le plus petit bout de JavaScript capable de gérer ce qui reste ? L'article souligne qu'en partant directement de la troisième question, on aboutit à un portage mécanique « un composant Vue = un contrôleur Stimulus », alors que l'essentiel de ce que faisaient les composants Vue n'était pas de la logique de navigateur : ils se contentaient de transformer en HTML des données que le serveur possédait déjà. Selon les cas, la solution retenue a donc varié : l'élément natif `<dialog>` a remplacé la modale Vue, certains widgets sont devenus des Web Components légers, d'autres de simples Turbo Frames sans JavaScript du tout.

**Pourquoi Stimulus pour le JavaScript restant.** Lorsque du JavaScript reste nécessaire, Stimulus est le choix retenu. Un contrôleur Stimulus se connecte quand son élément apparaît dans la page et se déconnecte quand il la quitte — un cycle de vie indispensable puisque Turbo remplace l'intégralité du `<body>` à chaque navigation. Sans ce mécanisme, chaque composant devrait retrouver et réinitialiser ses éléments à chaque visite, et prendre soin de retirer les écouteurs d'événements qu'il aurait ajoutés au document.

**Étude de cas : la vérification de résolution DNS.** Avant toute action nécessitant que le DNS du domaine pointe bien vers DNSimple, l'application vérifie plusieurs conditions : expiration de l'enregistrement, délégation vers un autre fournisseur, zone inactive. En cas de problème, une boîte de dialogue explique quoi corriger.

Dans l'ancienne version, ce contrôle était un composant Vue de 350 lignes recevant 17 props et gérant six états internes. Il récupérait les résultats via une requête JSON et construisait lui-même le HTML des cinq états d'échec possibles. Chaque page intégrant ce composant exécutait en plus, à chaque rendu, une requête de domaine, une vérification de permission et une recherche de prix, uniquement pour alimenter ces props. Lorsque la vérification passait, le composant simulait un clic sur un lien caché pour poursuivre l'action initiale ; l'URL cible et la méthode HTTP de ce lien transitaient elles-mêmes par des props, comme l'illustre cet extrait du code original :

```
this.ajax(this.dnsResolutionCheckDomainUrl)
  .then((response) => {
    const checks = response.getAt('response', []);
    const isPass = checks.length === 0;
    if (isPass)
      this.clicker(this.$refs.iUnderstand);
    else {
      this.checks = checks;
      this.isLoading = false;
    }
  })
```

Dans la nouvelle version, c'est le serveur qui rend chaque état : l'endpoint renvoie du HTML (destiné à une Turbo Frame) plutôt que du JSON. En cas de succès, la frame ne contient qu'un marqueur vide ; en cas d'échec, elle contient directement le message complet, avec permissions, prix et liens déjà calculés côté serveur. Le contrôleur Stimulus associé ne porte plus qu'une seule valeur, l'URL de la vérification, et se limite à ce qu'une Turbo Frame seule ne peut pas faire : intercepter le clic sur l'élément protégé par la vérification, ouvrir la boîte de dialogue et charger la frame, rejouer le clic d'origine une fois l'utilisateur prêt à continuer, et poser un cookie lorsque l'utilisateur demande à ne plus être contrôlé pendant 24 heures. Plutôt que de dupliquer l'URL et la méthode dans des props comme le faisait Vue, le nouveau contrôleur garde simplement une référence vers l'élément (lien ou bouton) effectivement cliqué, et le reclique lui-même :

```
intercept (event) {
  const action = event.target.closest('a, button, [role="button"]') || event.currentTarget;
  if (action === this.bypassedAction) {
    this.bypassedAction = null;
    return;
  }
  event.preventDefault();
  event.stopPropagation();
  this.pendingAction = action;
  this._open();
  this._load();
}
continue (event) {
  event?.preventDefault();
  this._close();
  if (!this.pendingAction) return;
  const action = this.pendingAction;
  this.pendingAction = null;
  this.bypassedAction = action;
  action.click();
}
```

Un drapeau de contournement (`bypassedAction`) empêche le contrôleur d'intercepter son propre clic rejoué. Lorsque l'utilisateur clique sur « Rafraîchir », le contrôleur appelle simplement `frame.reload()`, Turbo se chargeant d'annuler toute requête encore en cours — là où la version Vue nécessitait une garde explicite via un état `isLoading`.

En termes de volume de code, l'opération n'a pas drastiquement réduit le nombre de lignes : la version Vue totalisait environ 430 lignes (composant principal, composant enfant, partial et helper), contre environ 400 pour la nouvelle version (un contrôleur de 192 lignes et deux partials). Le gain n'est donc pas tant dans le nombre de lignes que dans la nature du changement : c'est désormais le serveur qui décide de ce qui doit être affiché, permissions et prix compris, et les pages n'exécutent plus les trois requêtes redondantes qu'elles exécutaient auparavant uniquement pour nourrir les props du composant Vue.

**Conclusion et suite de la série.** Pour l'auteur, l'apport principal de cette migration n'est pas la suppression de lignes de code en elle-même, mais le fait d'avoir ramené toute la logique métier à un seul endroit et dans un seul langage, repérable aussi bien par un humain que par un agent logiciel. La recommandation pour qui envisage une migration similaire reste la même grille à trois questions (HTML natif ? rendu serveur ? sinon, JavaScript minimal ?), avec ce critère de succès : mesurer non pas le nombre de lignes supprimées, mais la quantité d'information que le navigateur n'a plus besoin de connaître.

L'article annonce la suite de la série : la migration du CSS, où DNSimple a abandonné Bootstrap et Tachyons au profit de Tailwind, sous-application par sous-application, en s'appuyant sur des ViewComponents pour garder un balisage cohérent — avec en exemple un ancien helper d'alerte comptant 106 points d'appel, aujourd'hui unifiés derrière un seul ViewComponent.

L'article est signé Dallas Read, et se termine par la signature habituelle du blog DNSimple sur sa mission (« nous pensons que la gestion de domaine devrait être simple »).

## Pourquoi ça compte
Ce retour d'expérience illustre une tendance de fond dans l'écosystème Rails/Hotwire : remplacer les frameworks JS côté client (Vue, React) par du rendu serveur + JavaScript minimal (Turbo/Stimulus), ce qui simplifie la maintenance et réduit la dette technique liée aux bundlers.
