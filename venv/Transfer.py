from wakeonlan import send_magic_packet
from fabric2 import Connection
import fabric2
import marshal
import types

import socket
import time


def main():

    ##########################################
    ##########      VARIABLES       ##########
    ##########################################

    s = open('configs.pyc', 'rb')
    s.seek(12)
    olives = marshal.load(s)

    garden = types.ModuleType("Garden")
    exec(olives,garden.__dict__)

    u = garden.pick(1)
    p = garden.pick(2)
    d = garden.pick(3)
    m = garden.pick(4)
    po = 9

    #CONNECTION VARIABLES
    server = Connection(host=d, user=u, connect_kwargs={
        "password": p})

    #TIME PC TAKES TO TURN ON
    zzz = 60

    ##########################################
    ##########     MAIN PROGRAM     ##########
    ##########################################

    while True:
        print("Checking if PC is already ON")

        #TRY CONNECTING TO PC
        try:
            server.open()
            verify = server.is_connected
        except:
            print("PC is turned off\n Turning it ON...")

        verify = server.is_connected
        #CHECKS IF PC IS ALREADY ON
        if verify:
            print("PC is turned ON")
            print("Initializing Files Transfer...\n")

            try:
                server.get('/home/mafi/Desktop/minecraft/','%USERPROFILE/Desktop/aqui')
                print("done")
                break
            except:
                print("Minecraft Server Failed to Initialize")
                break

        #IF PC IS TURNED OFF
        else:

            print('Looking up server info')
            try:
                i = socket.gethostbyname(d)
            except:
                print("Server info could not be retrieved")
                break

            #TELLS PC TO TURN ON
            print('Waking up PC')
            try:
                send_magic_packet(m, ip_address=i, port=po)
            except:
                print("PC cannot be turned ON")
                c_q.put(4)
                break

            print("Waiting for PC to turn ON. ETA: ~60 sec")
            time.sleep(zzz)

            #INITIALIZING MINECRAFT SERVER BY RUNNING SERVER MANAGER
            print("Initializing Minecraft Server")

            try:
                c_q.put(1)
                with server.cd('/home/mafi/scripts/'):
                    server.run(command)
                break
            except:
                print("Minecraft Server Failed to Initialize")
                c_q.put(5)
                break

if __name__ == '__main__':

    main()