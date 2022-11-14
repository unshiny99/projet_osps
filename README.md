# projet_osps
Projet de système et programmation sécurisée \
Langage : Python

## Etat d'avancement
- Constitution des 2 tubes nommés (SP vers SS et SS vers SP)
- Instanciation des 2 serveurs (principal et secondaire)
- Implémentation d'un watchdog planifié (toutes les 2 secondes)
- Vérification de l'utilisation du bon système d'exploitation (Linux)
- Ajout d'une boucle infinie dans les serveurs pour des tests (arrêt brusque d'un des serveurs) et une meilleure visualisation du fonctionnement

## Principe de fonctionnement
Le watchdog est le processus principal, parent de tous les autres. Il lance le serveur principal, ainsi que le serveur secondaire. \
Il vérifie toutes les 2 secondes si ses processus fils sont en vie. Si ce n'est pas le cas, il tente de les relancer.
Les 2 serveurs peuvent communiquer grâce aux tubes nommés, pour savoir si l'un des 2 est en train d'utiliser la mémoire partagée par exemple.
La mémoire partagée est commune aux serveurs. Elle permet d'avoir des informations centralisées.

## Bibliographie
SP : Serveur Principal \
SS : Serveur Secondaire \
Watchdog : chien de garde/surveillance

## Documentation externe
Librairie multiprocessing : [docs.python.org](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Process.daemon)