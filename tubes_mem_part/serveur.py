#! /usr/bin/env python3
# _*_ coding: utf8 _*_
#
# Création d'un segment mémoire partagée et invocation du serveur secondaire
#
# Version 11/10/2022
#
import os, sys
from multiprocessing import shared_memory

_name = '012345'
_size = 10

def serveurPrincipal():
    print('Ouverture du tube1 en écriture... (serveur P)')
    # Ouverture en écriture est bloquante si pas de lecteur
    fifo1 = open(pathtube1, "w")

    print('Ouverture du tube2 en lecture... (serveur P)')
    # Ouverture en lecture est bloquante si pas de rédacteur
    fifo2 = open(pathtube2, "r")

    # TRAITEMENT SOUHAITE ICI
    for i in range(3):
        print('Processus principal prêt pour échanger des messages...')

        print('Écriture dans le tube1...')

        # 32 caractères
        fifo1.write(f"Message du processus principal : {i}!\n")
        fifo1.flush()

        print('Processus principal en attente de réception de messages...')

        line = fifo2.readline()
        print("Message recu : " + line)

    print('Fermeture du tube1...')
    fifo1.close()
    print('Fermeture du tube2...')
    fifo2.close()

    print ('Destruction des tubes...')

    os.unlink(pathtube1)
    os.unlink(pathtube2)

    shm_segment2.close()
    shm_segment1.close()
    shm_segment1.unlink()

def serveurSecondaire():
    # Création du segment mémoire partagée + accès à son "nom" (utilisé pour générer une clef)
    # (le nom peut être généré automatiquement, mais l'avantage de le fixer est que les n processus
    # qui accèdent au même segment ont "juste besoin de connaitre ce nom pour y accéder")
    shm_segment1 = shared_memory.SharedMemory(name=_name, create=False, size=_size)
    print ('Nom du segment mémoire partagée :', shm_segment1.name)

    # Accès + écriture de données via le premier accès au segment mémoire partagée
    print ('Taille du segment mémoire partagée en octets via premier accès :', len(shm_segment1.buf))
    shm_segment1.buf[:] = bytearray([74, 73, 72, 71, 70, 69, 68, 67, 66, 65])

    # Simuler l'attachement d'un second processus au même segment mémoire partagée
    # en utilisant le même nom que précédemment :
    shm_segment2 = shared_memory.SharedMemory(shm_segment1.name)

    # Accès + écriture de données via le second accès au MÊME segment mémoire partagée
    print ('Taille du segment mémoire partagée en octets via second accès :', len(shm_segment2.buf))
    print ('Contenu du segment mémoire partagée en octets via second accès :', bytes(shm_segment2.buf))

    print('Ouverture du tube1 en lecture... (serveur S)')
    # Ouverture en lecture est bloquante si pas de rédacteur
    fifo1 = open(pathtube1, "r")

    print('Ouverture du tube2 en écriture... (serveur S)')
    # Ouverture en écriture est bloquante si pas de lecteur
    fifo2 = open(pathtube2, "w")

    for i in range(3):
        print('Processus secondaire prêt pour échanger des messages...')

        print('Processus secondaire en attente de réception de messages...')

        line = fifo1.readline()
        print("Message recu : " + line)

        print('Écriture dans le tube2...')

        # 32 caractères
        fifo2.write(f"Message du process secondaire : {i}!\n")
        fifo2.flush()

    '''
    newpid = os.fork()
    if newpid < 0:
        print("fork() impossible")
        os.abort()
    if newpid == 0:
        # exécution d'une commande fille pour écrire sur la sortie standard
        os.execlp("ipcs", "ipcs", "-m")
    else:
        os.wait()
    '''

# Création du segment mémoire partagée + accès à son "nom" (utilisé pour générer une clef)
# (le nom peut être généré automatiquement, mais l'avantage de le fixer est que les n processus
# qui accèdent au même segment ont "juste besoin de connaitre ce nom pour y accéder")
try:
    shm_segment1 = shared_memory.SharedMemory(name=_name, create=True, size=_size)
except FileExistsError:
    shm_segment1 = shared_memory.SharedMemory(name=_name, create=False, size=_size)
print ('Nom du segment mémoire partagée :', shm_segment1.name)

# Accès + écriture de données via le premier accès au segment mémoire partagée
print ('Taille du segment mémoire partagée en octets via premier accès :', len(shm_segment1.buf))
shm_segment1.buf[:] = bytearray([74, 73, 72, 71, 70, 69, 68, 67, 66, 65])

# Simuler l'attachement d'un second processus au même segment mémoire partagée
# en utilisant le même nom que précédemment :
shm_segment2 = shared_memory.SharedMemory(shm_segment1.name)

# Accès + écriture de données via le second accès au MÊME segment mémoire partagée
print ('Taille du segment mémoire partagée en octets via second accès :', len(shm_segment2.buf))
print ('Contenu du segment mémoire partagée en octets via second accès :', bytes(shm_segment2.buf))

print ('Création des tubes...')

# Ci-dessous "0o" introduit un nombre en octal

pathtube1 = "/tmp/tubeNomme1.fifo"
pathtube2 = "/tmp/tubeNomme2.fifo"

# suppression des tubes nommés s'ils existent encore pour diverses raisons
if(os.path.exists(pathtube1)):
    os.unlink(pathtube1)

if(os.path.exists(pathtube2)):
    os.unlink(pathtube2)

# création concrète des tubes nommés
os.mkfifo(pathtube1, 0o0600)
os.mkfifo(pathtube2, 0o0600)

# création processus fils
newpid = os.fork()
if newpid < 0:
    print("fork() impossible")
    os.abort()
if newpid == 0: # processus fils
    # appel du serveur secondaire
    serveurSecondaire()
else: # processus courant 
    #os.wait()
    serveurPrincipal()
