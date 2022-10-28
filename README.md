# projet_osps
Projet de système et programmation sécurisée
Langage : Python

## Etat d'avancement
- Constitution des 2 tubes nommés (SP vers SS et SS vers SP)
- Instanciation des 2 serveurs (principal et secondaire)
- Implémentation d'une première version de watchdog
- Vérification de la bonne utilisation de système d'exploitation
- Ajout d'une boucle infinie dans les serveurs pour des tests (arrêt brusque)

## Principe de fonctionnement
Le watchdog est le processus principal. Il lance le serveur principal, ainsi que le serveur secondaire.

## Bibliographie
SP : Serveur Principal
SS : Serveur Secondaire
Watchdog : chien de garde