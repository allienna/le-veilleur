---
title: "Horrible public key tricks:"
date: 2026-11-16
url: "https://leadershipintech.com/links/23743/3d78f33c-7ca0-4e03-9c70-68e56918a4cd/email"
authors: ["maurycyz"]
keywords: ["TLS/SSL", "RSA", "certificats", "cryptographie", "ACME", "clé publique"]
theme: "Sécurité"
tone: "opinion"
used_in: ["2026-11-16"]
---

## Résumé
Frustré par la complexité et les apparentes incohérences du système ACME/TLS (expiration périodique des certificats, autorités de certification validant des exposants publics aussi absurdes que « 4 »), l'auteur conçoit un « certificat de protestation » : il cache un message en clair dans le module RSA de sa clé publique tout en obtenant un certificat parfaitement valide, signé par une autorité de certification reconnue (Let's Encrypt). L'article détaille le fonctionnement mathématique de RSA, la méthode permettant d'injecter un message lisible en base64 dans le module n sans rompre sa structure (n = p × q), ainsi que la procédure concrète via openssl et certbot pour obtenir le certificat signé. Il conclut que l'astuce réduit l'entropie de la clé privée mais reste sans danger réel pour un site web public : la confidentialité persistante (forward secrecy) du TLS moderne protège contre l'espionnage même si la clé privée venait à être compromise.

## Points clés
- Le système ACME/TLS impose un renouvellement récurrent perçu comme une complexité superflue pour un simple site public ; l'auteur note qu'une autorité de certification a même validé un certificat avec l'exposant « 4 », illustrant selon lui le laxisme du système.
- Puisque seul le module RSA (n) est « contrôlé par l'utilisateur », l'auteur l'utilise pour y cacher un message humoristique encodé en base64, directement lisible dans le certificat PEM.
- La technique : choisir un nombre premier p au hasard, fabriquer un n « de complaisance » contenant le message voulu, puis redéfinir q comme le nombre premier le plus proche de n/p pour reconstituer une paire (p, q) valide.
- Le certificat obtenu est un certificat TLS tout à fait légitime, signé par Let's Encrypt via les commandes openssl/certbot standards, et renouvelable normalement.
- La manipulation réduit l'entropie de la clé mais s'apparente à des techniques connues de compression partielle de clé RSA (fixer une partie du module), jugées globalement sûres bien que largement abandonnées en pratique au profit d'autres cryptosystèmes.
- Risques résiduels non vérifiés par le script : proximité excessive entre p et q (facilitant la factorisation de n) ou valeur de d trop faible — jugés peu probables et sans conséquence grave pour un site public grâce au forward secrecy.

## Analyse approfondie
J'ai toujours été quelque peu agacé par SSL/TLS. Il oblige tout le monde à passer par une danse complexe appelée « ACME » juste pour mettre en ligne un site web public. Pire encore, les certificats expirent tous les quelques mois : ce n'est donc pas une opération ponctuelle. Même avec l'automatisation, maintenir un certificat exige de la vigilance pour s'assurer que le client ACME a toujours accès aux enregistrements DNS ou au serveur web.

... et, pour ne rien arranger, tout le système ne fonctionne même pas vraiment : les certificats sont délivrés via des connexions en clair, et des autorités de certification de confiance utilisent des clés aussi « sécurisées » que le nombre « 4 ».

*Il existe des précédents* d'implémentations SSL « de protestation », mais je souhaite réellement chiffrer le trafic web. L'écoute passive est un risque réel... mais s'en protéger ne nécessite pas tout l'attirail des certificats : la meilleure option est donc un certificat de protestation.

La seule partie du certificat que je contrôle directement est la clé publique. La façon la plus simple d'obtenir un mauvais certificat est donc d'utiliser une clé privée « vanity » (de complaisance), comme 313333333337 (l'un des nombres premiers les plus « eleet »). Cependant, même si la clé publique qui en résulterait serait faible, personne ne le saurait à moins d'essayer de la casser.

Une bonne protestation doit être visible :

```
openssl s_client -connect maurycyz.com:443 </dev/null 2>/dev/null \
  | sed -n '/BEGIN/,/END/p' | grep -zE '////.*////' --color=yes

-----BEGIN CERTIFICATE-----
[... données base64 du certificat ...]
////You+dont+actually+have+to+pick+random+private+keys//No+one+checks+these+things//A+certificate+authority+got+away+with+the+number+4+for+a+year/////
[... données base64 du certificat ...]
-----END CERTIFICATE-----
```

(message caché, traduit : « Vous n'êtes en réalité pas obligé de choisir des clés privées aléatoires // Personne ne vérifie ce genre de choses // Une autorité de certification s'en est tirée avec le nombre 4 pendant un an »)

*Commençons par examiner le cadre mathématique* de RSA. Pour générer une clé, on choisit deux grands nombres premiers (p et q) qu'on multiplie pour obtenir le module (n). On choisit un petit nombre e comme exposant public.

La clé publique RSA est composée du module (n) et de l'exposant public :

```
Chiffrement (nécessite de connaître e, public) :
texte_chiffré = texte_clair^e mod n
```

La clé privée contient le module ainsi que l'exposant privé (d), choisi comme étant l'inverse multiplicatif de e modulo n. La façon exacte de trouver d n'a pas d'importance ici, mais le procédé nécessite de connaître p et q.

```
Déchiffrement (nécessite de connaître d, privé) :
texte_clair = texte_chiffré^d mod n
            = texte_clair^(e*d) mod n
            = texte_clair^1 mod n
            = texte_clair
```

*Bon, revenons-en aux clés de complaisance.* La valeur standard pour e est 65537 (0x10001), car son faible nombre de bits à 1 rend le chiffrement plus rapide. D'ailleurs, l'autorité de certification que j'ai utilisée refuse de signer des clés dont l'exposant public n'est pas standard : impossible donc de s'amuser de ce côté-là.

Le module n, lui, compte 2048 ou 4096 bits « contrôlés par l'utilisateur » : c'est donc l'endroit idéal pour y cacher un message. Cependant, pour que le certificat soit utilisable, il faut trouver deux grands nombres premiers dont le produit donne exactement ce module de complaisance.

Ma méthode commence par choisir deux nombres premiers aléatoires et calculer la valeur de n qui en résulte. Les octets de n sont ensuite modifiés pour introduire le message dans l'encodage base64. Bien sûr, le n modifié n'est alors plus le produit de p et q, mais on peut corriger cela en redéfinissant q comme n/p.

La valeur de q ainsi obtenue n'a presque aucune chance d'être un nombre premier (ni même un entier) : je l'arrondis donc et cherche le nombre premier suivant après ce q idéal, ce qui ne nécessite en général qu'un ajustement de quelques centaines d'unités. Comme p et q sont de taille similaire, une petite variation de q n'affecte que la moitié la moins significative du produit :

```
58174124 * 918491824 = 53432457262362176
(on incrémente jusqu'au premier suivant...)
58174124 * 918491843 = 53432458367670532
```

Tant que le message est inséré dans la moitié haute de n, il a de bonnes chances de rester intact. Le p original et le nouveau q sélectionné permettent alors de construire une clé privée RSA fonctionnelle, de façon tout à fait classique.

À partir de là, il ne reste plus qu'à faire signer la clé par une autorité de certification :

```
# Domaine unique
openssl req -new -key priv.pem -subj '/C=US/CN=example.com' > cert_request
certbot certonly --manual --csr cert_request

# Domaine générique (wildcard)
cat > config <<EOF
[ req ]
req_extensions = req_ext
[ req_ext ]
subjectAltName = @alt_names
[ alt_names ]
DNS.1 = *.example.com
DNS.2 = example.com
EOF
openssl req -new -key priv.pem -config config -subj '/C=US/CN=example.com' > cert_request
certbot certonly --manual --csr cert_request
```

Le résultat est un certificat fonctionnel et reconnu par les navigateurs, avec un message assez long caché dans la clé publique. Le renouvellement se fait en soumettant à nouveau la CSR et en répétant le défi ACME, ce qui peut être automatisé.

Le base64 ne dispose pas de la plupart des signes de ponctuation, mais il offre l'alphabet ASCII complet, et les ~150 caractères disponibles (pour du RSA-2048) ou ~320 (pour du RSA-4096) laissent largement de la place pour des blagues. Une autre option consisterait à viser le base16 affiché dans le visualiseur de certificats de la plupart des navigateurs : cela offrirait beaucoup plus d'espace (2 caractères par octet au lieu de 0,75), mais exigerait un choix de mots plus minutieux.

*Côté sécurité*, cette astuce réduit évidemment l'entropie de la clé privée. Elle devrait néanmoins rester sûre : des méthodes presque identiques ont déjà été envisagées comme une forme de compression. Si la moitié haute du module est fixée à une valeur bien connue, elle n'a pas besoin d'être transmise ni stockée avec la clé.

Une réduction d'environ moitié peut être obtenue par simple division, mais l'état de l'art permet de fixer jusqu'aux deux tiers de la clé, ramenant sa taille au tiers de celle d'un RSA standard tout en conservant un niveau de sécurité comparable... bien que je doive préciser que ce genre d'astuces a largement été abandonné au profit d'autres cryptosystèmes capables d'utiliser directement des clés plus petites.

La manipulation de q peut produire des nombres premiers très proches l'un de l'autre, ce qui permettrait de factoriser n et de récupérer la clé privée. Une valeur de d trop petite peut également poser problème. Ces deux cas sont peu probables, mais mon script ne vérifie pas l'absence de valeurs non sécurisées.

Quoi qu'il en soit, indépendamment de la sécurité de la clé, cela devrait parfaitement convenir pour un site web public : le TLS moderne offre la confidentialité persistante (forward secrecy), si bien qu'espionner le trafic nécessite une attaque de type « homme du milieu » même si la clé privée est compromise.

*Pour aller plus loin* :
- https://tom7.org/httpv/httpv.pdf : ⭐ Le pire serveur TLS du monde
- /projects/badcert/gen.py : script permettant de générer une clé de complaisance
- https://rya.nc/cert-tricks.html : d'autres certificats de complaisance
- https://doi.org/10.1007/978-3-540-79104-1_9 : l'avis de véritables cryptographes sur le fait de fixer une partie du module n

## Pourquoi ça compte
Cet article illustre de façon ludique mais rigoureuse comment la structure mathématique de RSA laisse une marge de manipulation exploitable (ici à des fins humoristiques), tout en questionnant implicitement la rigueur réelle des contrôles exercés par les autorités de certification dans l'écosystème TLS actuel.
