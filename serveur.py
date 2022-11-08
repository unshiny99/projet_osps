#! /usr/bin/env python3
# _*_ coding: utf8 _*_
#
# Création d'un segment mémoire partagée et invocation du serveur secondaire
# Fonctionnalité basique du watchdog (surveillance d'état des serveurs conjoints)
#
# Version 08/11/2022
# Réalisé par Maxime Frémeaux & Khalil Bedjaoui
#
import multiprocessing
import os, sys
import platform
import time
from multiprocessing import shared_memory, process
from threading import Timer

# classe utilisée pour la boucle de répétition du watchdog
class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

# déclaration variables et initialisation
_name = '012345'
_size = 10
processes = {}

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
        fifo1.flush() # vider le buffer

        print('Processus principal en attente de réception de messages...')

        line = fifo2.readline()
        print("Message recu : " + line)

    while True:
        continue

    print('Fermeture du tube1...')
    fifo1.close()
    print('Fermeture du tube2...')
    fifo2.close()

    print ('Destruction des tubes...')

    os.unlink(pathtube1)
    os.unlink(pathtube2)

    # fermeture mémoire partagée et destruction objet
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
        fifo2.flush() # vider le buffer

    while True:
        continue

# chien de garde qui permet de vérifier l'état des processus fils
def watchdog():
    print("pid du watchdog : " + str(os.getpid()))
    print("pid de SP : " + str(processes[0].pid))
    print("pid de SS : " + str(processes[1].pid))

    # print(processes[0].is_alive())
    # print(processes[0].exitcode)
    # print(processes[1].is_alive())
    # print(processes[1].exitcode)

    # si SS est kill mais SP en vie, tenter de relancer SS
    if(processes[0].is_alive() and not processes[1].is_alive()):
        print("Relancement du serveur secondaire")
        processes[1] = multiprocessing.Process(target=serveurSecondaire)
        processes[1].start()

    # si SP est kill mais SS en vie, tuer SP -- et le watchdog
    # tue le processus courant (et son fils serveur secondaire) et en relance un (ainsi que le fils)
    if(not processes[0].is_alive() and processes[1].is_alive()):
        print("Relancement du serveur principal")
        processes[0] = multiprocessing.Process(target=serveurPrincipal)
        processes[0].start()
        print("Relancement du serveur secondaire")
        processes[1].kill()
        processes[1] = multiprocessing.Process(target=serveurSecondaire)
        processes[1].start()

    # attente conjointe processus
    processes[0].join(1)
    processes[1].join(1)

# programme conçu pour les distributions Linux
if(platform.system() == 'Linux'):
    # Création du segment mémoire partagée + accès à son "nom" (utilisé pour générer une clef)
    try:
        shm_segment1 = shared_memory.SharedMemory(name=_name, create=True, size=_size)
    except FileExistsError:
        shm_segment1 = shared_memory.SharedMemory(name=_name, create=False, size=_size)

    print ('Nom du segment mémoire partagée :', shm_segment1.name)

    # Accès + écriture de données via le premier accès au segment mémoire partagée
    print ('Taille du segment mémoire partagée en octets via premier accès :', len(shm_segment1.buf))
    shm_segment1.buf[:_size] = bytearray([74, 73, 72, 71, 70, 69, 68, 67, 66, 65])

    # Simuler l'attachement d'un second processus au même segment mémoire partagée
    # en utilisant le même nom que précédemment
    shm_segment2 = shared_memory.SharedMemory(shm_segment1.name)

    # Accès + écriture de données via le second accès au MÊME segment mémoire partagée
    print ('Taille du segment mémoire partagée en octets via second accès :', len(shm_segment2.buf))
    print ('Contenu du segment mémoire partagée en octets via second accès :', bytes(shm_segment2.buf))

    # chemin de destination pour les tubes nommés
    pathtube1 = "/tmp/tubeNomme1.fifo"
    pathtube2 = "/tmp/tubeNomme2.fifo"

    # suppression des tubes nommés s'ils existent encore pour diverses raisons 
    # (ex: crash inattendu de l'application)
    if(os.path.exists(pathtube1)):
        os.unlink(pathtube1)

    if(os.path.exists(pathtube2)):
        os.unlink(pathtube2)

    print ('Création des tubes...')
    # création concrète des tubes nommés
    # Note : "0o" introduit un nombre en octal
    os.mkfifo(pathtube1, 0o0600)
    os.mkfifo(pathtube2, 0o0600)

    # création des processus en multiprocessing
    p1 = multiprocessing.Process(target=serveurPrincipal)
    p2 = multiprocessing.Process(target=serveurSecondaire)
    processes[0] = p1
    processes[1] = p2

    # démarrage processus serveur
    processes[0].start()
    processes[1].start()

    # lancement boucle watchdog
    timer = RepeatTimer(1, watchdog) #  , args=("bar",) # si besoin d'argument à passer
    timer.start()
    time.sleep(2)
else:
    print(platform.system() + " n'est pas (encore) supporté :/")