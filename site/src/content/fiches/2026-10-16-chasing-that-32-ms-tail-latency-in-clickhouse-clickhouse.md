---
title: "Chasing that 32 ms tail latency in ClickHouse | ClickHouse"
date: 2026-10-16
url: "https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fclickhouse.com%2Fblog%2Fchasing-32ms-tail-latency-clickhouse%3Futm_source=tldrit/1/010001a13f7fa0c2-9c38a2c3-bf45-4497-a828-511fbe85a9da-000000/gFGP0X-88R3_gyI_Ovl8rLoaxrWiCz48_Amfk9U6SGU=452"
keywords: ["ClickHouse", "latence réseau", "TCP", "protocole natif", "congestion window"]
theme: "Software"
tone: "research"
used_in: ["2026-10-16"]
---

## Résumé
L'équipe ClickHouse a enquêté sur une latence additionnelle mystérieuse de ~32 ms observée par un client sur de simples requêtes SELECT via le protocole natif TCP. La cause : après une période d'inactivité de la connexion, le noyau Linux réinitialise la fenêtre de congestion TCP (`cwnd`) à sa valeur initiale (`initcwnd`), et les multiples petits paquets de métadonnées envoyés par ClickHouse (`Logs`, `Progress`, `ProfileEvents`) avant le paquet final `EndOfStream` dépassent alors cette fenêtre réduite, forçant un aller-retour réseau supplémentaire. En regroupant ces paquets de métadonnées au niveau applicatif en une seule écriture socket, l'équipe a réduit de moitié le nombre de paquets TCP et supprimé entièrement cette latence de queue (« tail latency »).

## Points clés
- Le protocole natif de ClickHouse exige que le client attende un paquet `EndOfStream` pour considérer une requête terminée, après avoir reçu les données puis des paquets de métadonnées (`Logs`, `Progress`, `ProfileEvents`).
- Après ~2 secondes d'inactivité (le délai de retransmission, ou RTO), Linux réinitialise la fenêtre de congestion TCP (`cwnd`) à sa valeur initiale (`initcwnd`, souvent 10 MSS, 8 dans le cas du client).
- `TCP_NODELAY` (désactivation de l'algorithme de Nagle), utilisé par ClickHouse pour la faible latence, fait que chaque petite écriture socket devient un segment TCP distinct sur le réseau.
- Si le nombre de segments dépasse la fenêtre de congestion réduite, le serveur doit attendre un accusé de réception (ACK) du client avant d'envoyer le reste, ce qui ajoute un aller-retour complet (~32 ms dans ce cas).
- La reproduction du bug a été faite de façon déterministe avec des network namespaces Linux, `tc` (traffic control) et une fenêtre de congestion initiale fixée à 8 MSS.
- Le correctif regroupe les paquets de métadonnées non sensibles au temps en une seule écriture applicative, réduisant de moitié le nombre de paquets TCP et éliminant la latence supplémentaire, sans retarder les paquets `Progress` qui doivent rester en temps réel.

## Analyse approfondie
En résumé : dans le protocole natif de ClickHouse, les clients doivent attendre un paquet `EndOfStream` pour qu'une requête soit considérée comme terminée. Entre les paquets de résultats (`Data`) et `EndOfStream`, ClickHouse envoie plusieurs paquets de métadonnées (`Logs`, `Progress`, `ProfileEvents`). Combinés à `TCP_NODELAY` et à une fenêtre de congestion TCP (`cwnd`) réinitialisée après une période d'inactivité, ces paquets non groupés peuvent dépasser la fenêtre, forçant un aller-retour supplémentaire. Nous avons reproduit ce problème de façon déterministe à l'aide de network namespaces Linux, et réduit la latence de queue en regroupant ces paquets de métadonnées au niveau applicatif.

### Le problème

Un de nos clients a observé une latence supplémentaire d'environ 32 ms sur de simples requêtes SELECT entre le client et le serveur.

Dans la configuration de ce client, le client et le serveur sont séparés d'environ 32 ms (en sortie réseau). Lorsqu'une connexion restait inactive pendant 2 secondes ou plus, la requête suivante prenait environ 64 ms de bout en bout : 2× le temps d'aller-retour (RTT) au lieu du ~32 ms attendu (1× RTT).

Nous avons dû déterminer ce qui causait exactement cet aller-retour supplémentaire.

Cette investigation a mené à des enseignements intéressants, à la fois sur la pile TCP de Linux et sur le protocole natif de ClickHouse.

### Le protocole natif de ClickHouse 101

Le serveur ClickHouse prend en charge un large éventail de protocoles. HTTP et TCP natif sont les deux principaux moyens de communiquer avec le serveur ClickHouse. Le problème du client concerne le protocole natif TCP, c'est donc notre objet d'étude. Il est important de comprendre un peu le fonctionnement du protocole natif de ClickHouse pour saisir le problème du client.

Le protocole natif de ClickHouse est un protocole à état construit au-dessus du protocole de transport TCP. Le client et le serveur échangent différents messages protocolaires selon les phases (Handshake, INSERT ou SELECT). La spécification officielle du protocole natif TCP en décrit le fonctionnement en détail.

Voici une version simplifiée du fonctionnement des requêtes SELECT au niveau du protocole.

1. Le client envoie `Query` (contient le SQL, les paramètres, les drapeaux, etc.).
2. Le serveur diffuse des paquets `Data` contenant les lignes de résultat réelles.
3. Le serveur envoie également des paquets de métadonnées intermédiaires (`ProfileEvents`, `Progress`, `Logs`).
4. Le serveur envoie `EndOfStream` (EOS) pour signaler que cette requête particulière est terminée.

Cela signifie que le client doit continuer à lire depuis la connexion jusqu'à ce qu'il reçoive le paquet `EndOfStream` pour cette requête, avant que celle-ci ne soit considérée comme terminée.

### La fenêtre de congestion TCP 101

TCP est le protocole de transport bien connu, et son fonctionnement dépasse le cadre de cet article. Ici, nous nous concentrons principalement sur deux caractéristiques du protocole TCP nécessaires pour comprendre précisément le problème du client.

1. La fenêtre de congestion
2. TCP_NODELAY (l'algorithme de Nagle)

#### La fenêtre de congestion

La fenêtre de congestion (contrairement à la fenêtre de réception) n'est configurée ni du côté client ni du côté serveur. C'est une valeur qui démarre généralement petite (basée sur `initcwnd`, la valeur initiale de la fenêtre de congestion sous Linux) et qui augmente continuellement tant que le réseau entre le client et le serveur ne rencontre aucun problème de congestion (par exemple, le serveur peut envoyer ce nombre de paquets TCP avant d'attendre un ACK du client). C'est ce qu'on appelle communément le démarrage lent TCP (« slow start »).

En substance, TCP limite la quantité de données non acquittées en transit à l'aide de cette fenêtre de congestion (`cwnd`).

La valeur `initcwnd` est généralement de 10 MSS (Maximum Segment Size), mais elle diffère parfois. Dans le cas du client, elle était de 8 MSS.

Un point crucial à noter sur la fenêtre de congestion est qu'elle continue de croître, et si la connexion est inactive pendant un certain temps (par exemple 2 secondes dans le cas du client), la pile TCP de Linux réinitialise la taille actuelle de la fenêtre de congestion à la valeur `initcwnd`. Ce délai d'inactivité est appelé le délai de retransmission (Retransmission Timeout, RTO), et il est calculé dynamiquement en fonction du RTT du réseau, avec des bornes inférieure (200 millisecondes) et supérieure (120 secondes) dans la pile TCP de Linux.

#### TCP_NODELAY (l'algorithme de Nagle)

Étant donné son ancienneté, l'un des comportements par défaut de TCP est de regrouper les écritures socket avant de les transmettre sur le réseau, afin de réduire la surcharge réseau. C'est ce qu'on appelle souvent l'algorithme de Nagle, qui s'exécute à l'intérieur de la pile TCP de Linux, là où l'application n'a presque aucun contrôle.

Les systèmes modernes à faible latence (comme ClickHouse) désactivent ce comportement en activant `TCP_NODELAY=1`, demandant au noyau d'envoyer immédiatement les écritures socket.

Le piège ici est que si `TCP_NODELAY` est activé et qu'une application émet plusieurs écritures socket pour ces paquets de métadonnées (`ProfileEvents`, `Log`, `Progress`), chacune de ces écritures devient un segment TCP individuel sur le réseau.

Si le serveur émet plus de petites écritures que ce que la fenêtre `cwnd` réduite peut contenir, le noyau doit s'arrêter et attendre un ACK du client avant d'envoyer les paquets restants, ce qui entraîne une pénalité d'aller-retour supplémentaire.

### Reproduire exactement le problème du client

Reproduire le problème du client nécessite de simuler le même RTT réseau entre le client et le serveur (~32 ms) pour rendre le problème visible. Par simplicité, nous exécutons toutes les requêtes (avec une période d'inactivité de 2 secondes) sur une seule connexion TCP via le protocole natif entre le client et le serveur.

Deux éléments sont impliqués ici :

1. Un programme Go qui exécute de vraies requêtes pour observer le problème rencontré par le client (latence de queue supplémentaire d'environ 32 ms)
2. Un serveur ClickHouse dans un network namespace avec les conditions réseau du client appliquées (simulant un délai de sortie réseau d'environ 32 ms).

#### Configuration réseau

Nous aurions pu utiliser Docker ou Podman pour créer le network namespace. Cependant, nous l'avons délibérément configuré manuellement avec `netns` pour rendre la simulation réseau plus facile à comprendre.

Nous avons ensuite utilisé `tc` (traffic control) pour simuler un délai WAN de 32 ms entre le client et le serveur. Nous avons également configuré la fenêtre de congestion TCP initiale à 8 MSS (`initcwnd 8`).

1. Disposer d'un binaire ClickHouse (< 26.9) (celui que nous utilisons pour reproduire le problème)

```
mkdir -p ~/chbin && cd ~/chbin
wget https://builds.clickhouse.com/26.8/amd64/clickhouse && chmod +x ./clickhouse
```

1. Créer un réseau pour simuler l'infrastructure du client (client et serveur à ~32 ms de distance).

```
# Créer un network namespace dédié pour ClickHouse
sudo ip netns add chsrv
# Créer une paire veth virtuelle
sudo ip link add veth-host type veth peer name veth-ch
sudo ip link set veth-ch netns chsrv
# Assigner les adresses IP
sudo ip addr add 10.99.0.1/24 dev veth-host
sudo ip link set veth-host up
sudo ip netns exec chsrv ip addr add 10.99.0.2/24 dev veth-ch
sudo ip netns exec chsrv ip link set veth-ch up
sudo ip netns exec chsrv ip link set lo up
# Ajouter un délai de sortie de 32ms et fixer la cwnd initiale à 8
sudo ip netns exec chsrv tc qdisc add dev veth-ch root netem delay 32ms
sudo ip netns exec chsrv ip route change 10.99.0.0/24 dev veth-ch \
    proto kernel scope link src 10.99.0.2 initcwnd 8
```

1. Vérifier le réseau simulé (vous devriez voir ~32 ms)

`ping -c 5 10.99.0.2`
```
PING 10.99.0.2 (10.99.0.2) 56(84) bytes of data.
64 bytes from 10.99.0.2: icmp_seq=1 ttl=64 time=32.0 ms
64 bytes from 10.99.0.2: icmp_seq=2 ttl=64 time=32.1 ms
64 bytes from 10.99.0.2: icmp_seq=3 ttl=64 time=32.0 ms
64 bytes from 10.99.0.2: icmp_seq=4 ttl=64 time=32.0 ms
64 bytes from 10.99.0.2: icmp_seq=5 ttl=64 time=32.1 ms
```

#### Programme client

Ce programme Go exécute des requêtes simples sur une connexion établie avec une période d'inactivité de 2 secondes entre les requêtes. Nous séparons également la latence globale de la requête et la latence de queue (le temps entre le dernier paquet `Data` et le paquet `EndOfStream`) pour observer plus clairement la latence de queue (avant et après le correctif).

Le programme Go exécute N requêtes identiques `SELECT max(id)` sur une connexion réutilisée et divise la latence de chaque requête en :

1. `first_row` (le résultat de la requête lui-même) et
2. `tail` (de la première ligne à la fin du flux).

`tail` est la clé ici : en bonne santé ≈ 0 ms ; bloqué = exactement 1× RTT.

#### Exécuter le test

1. Exécuter le serveur dans le réseau simulé

```
mkdir -p /tmp/chdata
cd ~/chbin
sudo ip netns exec chsrv sudo -u "$USER" \
    ./clickhouse server -- --listen_host=0.0.0.0 --path=/tmp/chdata/
```

1. Créer une table et des lignes pour les expériences

```
cd ~/chbin
./clickhouse client --host 10.99.0.2 -q \
  "CREATE TABLE IF NOT EXISTS benchmark_test (id UInt64) ENGINE=MergeTree ORDER BY id"
./clickhouse client --host 10.99.0.2 -q \
  "INSERT INTO benchmark_test SELECT number FROM numbers(939)"
```

1. Exécuter le programme Go pour observer le problème en action

`go run issue.go`
Vous devriez voir des résultats similaires à ceux-ci :

```
addr=10.99.0.2:9000  sleep=2s  profile_events=true
query: SELECT max(id) FROM benchmark_test
query  1: first_row=  33.17ms  eos=  65.31ms  tail=  32.13ms  (rows=1)
query  2: first_row=  33.65ms  eos=  65.19ms  tail=  31.54ms  (rows=1)
query  3: first_row=  33.44ms  eos=  65.02ms  tail=  31.57ms  (rows=1)
query  4: first_row=  33.30ms  eos=  65.10ms  tail=  31.80ms  (rows=1)
query  5: first_row=  33.19ms  eos=  65.11ms  tail=  31.92ms  (rows=1)
```

**Observation :** La première ligne est arrivée en ~33 ms (1× RTT), mais la connexion s'est bloquée pendant encore **~32 ms (latence de queue)** en attendant le train de paquets `EndOfStream`.

### Cause racine

Le RTT supplémentaire (~32 ms) vient du fait qu'une fois la fenêtre de congestion réinitialisée (d'une grande valeur à `initcwnd`, qui était de 8 dans le cas du client) après une période d'inactivité de 2 secondes, le serveur ne peut pas envoyer tous les paquets restants (Data + ces paquets de métadonnées) en un seul aller-retour.

Le serveur a envoyé 8 segments TCP, a épuisé l'espace `cwnd` disponible et s'est mis en pause jusqu'à ce que le client acquitte le premier lot, coûtant un aller-retour complet supplémentaire de 32 ms.

### Le correctif et les résultats

Il existe des solutions de contournement pour rendre ce problème moins susceptible de se produire :

1. Désactiver `ProfileEvents` côté serveur (les paquets `ProfileEvents` sont l'une des causes du grand nombre de paquets TCP sur le réseau)
2. Désactiver la réinitialisation de la fenêtre de congestion de la connexion (`cwnd`) à sa valeur initiale (`initcwnd`) après une période d'inactivité (`tcp_slow_start_after_idle=0`) sur le nœud serveur (GKE dans le cas du client ; c'est également recommandé pour le TCP haute performance par Google Cloud)
3. Augmenter `initcwnd` (par défaut 10, 8 dans le cas du client) sur le nœud serveur
4. Améliorer le protocole natif de ClickHouse pour créer moins de paquets TCP grâce à un regroupement au niveau applicatif.
5. Utiliser l'option `TCP_CORK` au lieu de `TCP_NODELAY`

Malheureusement, dans ce cas, le client avait peu de contrôle sur les solutions (1), (2) et (3), donc les seules options viables étaient (4) et (5). L'option 5 (`TCP_CORK`) semblait intéressante, mais elle présente quelques inconvénients :

- La pile TCP du noyau garde un contrôle total sur le remplissage de ces segments TCP
- Elle est spécifique au noyau Linux

L'option (4) semblait également être une bonne amélioration côté serveur de toute façon. Nous avons donc décidé de faire en sorte que le protocole natif de ClickHouse crée moins de paquets TCP grâce à un regroupement au niveau applicatif.

Le correctif est simple : nous regroupons ces paquets de métadonnées au niveau applicatif en une seule écriture socket (donc potentiellement moins de paquets TCP), qui peut ensuite être envoyée en un nombre minimal d'allers-retours même lorsque la fenêtre de congestion est réinitialisée.

Il y a un piège : nous ne pouvons pas regrouper aveuglément tous les paquets de métadonnées, car certains paquets comme `Progress` sont sensibles au temps et doivent être livrés immédiatement au client (imaginez que le client veuille connaître la progression réelle de la requête, et que le regroupement côté serveur la retarde, communiquant un état de progression erroné).

Nous pouvons valider que notre regroupement fonctionne en examinant les paquets TCP capturés : le nombre total de paquets TCP que le serveur crée pour la même requête est presque divisé par deux. Cela supprime les ~32 ms de latence de queue supplémentaire que nous avions initialement observée.

#### Validation

En supposant que le serveur ClickHouse fonctionne sur le port 9000.

##### Avant le correctif

Si vous exécutez le même script Go en capturant les paquets TCP PUSH (`PSH`, ceux où les données applicatives réelles sont transférées) via `tshark` :

`tshark -i veth-host -f 'tcp port 9000 and greater 60 and tcp[tcpflags] & tcp-push != 0' -w capture.pcap`
```
Capturing on 'veth-host'
50
```

Même avant d'examiner les fichiers pcap capturés, nous pouvons voir qu'un total de 50 paquets TCP de ce type ont été capturés, du serveur vers le client.

Remarquez également les nombreux minuscules segments TCP :

```
tshark -r capture.pcap -Y 'tcp.flags.push == 1 && tcp.len > 0' -T fields -e tcp.len |
 sort -n | uniq -c | awk 'BEGIN {print "COUNT\tTCP_PACKET_SIZE_BYTES"} {print $1 "\t" $2}'
```
```
COUNT	TCP_PACKET_SIZE_BYTES
7	1
5	8
6	9
4	10
5	12
5	28
6	36
1	62
5	164
1	475
1	2261
2	2328
1	2357
1	2896
```

##### Après le correctif

Le même script Go, capturant sur le serveur corrigé avec le regroupement :

`tshark -i veth-host -f 'tcp port 9000 and greater 60 and tcp[tcpflags] & tcp-push != 0' -w patched-capture.pcap`
```
Capturing on 'veth-host'
25
```

Vous pouvez clairement voir que le nombre de paquets TCP transférés est réduit de moitié par rapport à avant.

L'examen des paquets capturés montre clairement que les paquets `PSH` sont bien plus « remplis » par rapport aux nombreux petits paquets précédents.

`tshark -r patched-capture.pcap -Y 'tcp.flags.push == 1 && tcp.len > 0' -T fields -e tcp.len | sort -n | uniq -c | awk 'BEGIN {print "COUNT\tTCP_PACKET_SIZE_BYTES"} {print $1 "\t" $2}'`
```
COUNT	TCP_PACKET_SIZE_BYTES
3	1
1	36
1	62
5	164
2	2363
2	2417
1	2516
```

#### Vérifier que la latence de queue disparaît dans la même configuration client

L'exécution du même script avec exactement la même configuration que celle décrite pour reproduire le problème exact du client montre comment la latence de queue de ~32 ms a disparu :

```
query  1: first_row=  34.53ms  eos=  35.65ms  tail=   1.12ms  (rows=1)
query  2: first_row=  34.79ms  eos=  35.58ms  tail=   0.79ms  (rows=1)
query  3: first_row=  35.23ms  eos=  36.12ms  tail=   0.90ms  (rows=1)
query  4: first_row=  34.72ms  eos=  35.95ms  tail=   1.23ms  (rows=1)
query  5: first_row=  34.98ms  eos=  36.26ms  tail=   1.27ms  (rows=1)
```

Notez qu'aucun aller-retour supplémentaire n'est désormais nécessaire pour que le serveur envoie `EndOfStream` (eos) au client.

### Résumé (de l'article source)

Une latence de queue élevée n'est pas toujours causée par des moteurs de base de données lents ou des requêtes de longue durée ; parfois, le coupable se cache dans l'interaction entre les vidages au niveau applicatif et le comportement TCP au niveau du noyau.

- **Les connexions TCP inactives se réinitialisent :** Après une période d'inactivité RTO, la pile TCP de Linux réduit `cwnd` à `initcwnd`, limitant le nombre de paquets non acquittés pouvant tenir dans un seul aller-retour.
- **`TCP_NODELAY` a un compromis :** Désactiver l'algorithme de Nagle rend les écritures individuelles rapides, mais émettre plusieurs petits appels `write()` peut créer un nombre inattendu de segments TCP qui peuvent rapidement épuiser une petite fenêtre de congestion.
- **Regrouper au niveau applicatif :** Regrouper les paquets de métadonnées (`ProfileEvents`, `Logs`, `Progress`) en une seule écriture tampon avant de les vidanger réduit considérablement le nombre de segments TCP, maintenant une latence de queue prévisible même sur des connexions inactives à RTT élevé.

## Pourquoi ça compte
Ce cas illustre comment des optimisations bas niveau (désactivation de Nagle, interaction protocole applicatif/pile TCP) peuvent créer des latences invisibles mais reproductibles à grande échelle ; une méthodologie de diagnostic (namespaces réseau, `tc`, `tshark`) directement réutilisable pour diagnostiquer des problèmes de latence similaires dans d'autres systèmes distribués.
