# Projet de système et programmation sécurisée (OSPS)
Langage utilisé : Python (version 3)

### <b> Remarque préalable : </b> le code a été commenté afin d'expliquer le principe de chaque instruction

## Etat d'avancement final
- Constitution des 2 tubes nommés (SP vers SS et SS vers SP)
- Instanciation des 2 serveurs (principal et secondaire)
- Implémentation d'un watchdog planifié (toutes les 2 secondes)
- Vérification de l'utilisation du bon système d'exploitation (Linux)
- Ajout d'une boucle infinie dans les serveurs pour des tests (arrêt brusque d'un des serveurs) et une meilleure visualisation du fonctionnement

## Principe de fonctionnement
Le watchdog est le processus principal, parent de tous les autres. Il lance le serveur principal, ainsi que le serveur secondaire. \
Il vérifie toutes les 2 secondes si ses processus fils sont en vie. Si ce n'est pas le cas, il tente de les relancer. Il affiche aussi les 3 identifiants (ou PID) des processus, respectivement du watchdog, du SP et du SS, à intervalle régulier.
Les 2 serveurs peuvent communiquer grâce aux tubes nommés, pour savoir si l'un des 2 est en train d'utiliser la mémoire partagée par exemple.
La mémoire partagée est commune aux serveurs. Elle permet d'avoir des informations centralisées.

## Exécution du programme
Utiliser la commande `./serveur.py` afin de lancer le processus principal (ou `python3 serveur.py`).
* [WSL] Si l'erreur `/usr/bin/env: ‘python3\r’: No such file or directory` apparaît, utiliser la commande `dos2unix serveur.py` afin de convertir l'arborescence.
* Si l'erreur `-bash: ./serveur.py: Permission denied` s'affiche, appliquer les droits d'exécution sur le fichier en utilisant ` sudo chmod u+x serveur.py`.

## Suggestions d'amélioration du code
<table>
    <tr>
        <th>Proposition</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>Gestion des erreurs améliorée</td>
        <td>Ajouter plus d'exceptions durant l'exécution du programme principal (ex : lors de la création/destruction des tubes)</td>
    </tr>
    <tr>
        <td>Gestion d'un arrêt brutal du watchdog</td>
        <td>L'interruption du processus principal est gérée par l'exception `KeyBoardInterrupt` mais pas lorsqu'on tue le processus avec `kill`</td>
    </tr>
</table>

## Bibliographie
SP : Serveur Principal \
SS : Serveur Secondaire \
Watchdog : chien de garde/surveillance

## Documentation externe
Librairie multiprocessing : [docs.python.org](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Process.daemon)