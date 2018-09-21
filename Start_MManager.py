from wakeonlan import send_magic_packet
from fabric import Connection
import marshal
import types
import threading
from queue import Queue

import socket
import time

def starting_module(c_q):

    ##########################################
    ##########      VARIABLES       ##########
    ##########################################

    s = open('configs.pyc','rb')
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
    command = 'python3 Internal_MManager.py 1'

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
            print("Initializing Minecraft Server...")

            try:
                c_q.put(1)
                with server.cd('/usr/minecraft/'):
                    server.run(command)
                break
            except:
                print("Minecraft Server Failed to Initialize")
                c_q.put(2)
                break

        #IF PC IS TURNED OFF
        else:

            print('Looking up server info')
            try:
                i = socket.gethostbyname(d)
            except:
                print("Server info could not be retrieved")
                c_q.put(3)
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
                with server.cd('/usr/minecraft/'):
                    server.run(command)
                break
            except:
                print("Minecraft Server Failed to Initialize")
                c_q.put(5)
                break

##########################################
##########     MAIN ROUTINE     ##########
##########################################

def main():

    close_queue= Queue()

    thread_start_server = threading.Thread(name='Start_Server', target=starting_module, daemon=True, args=(close_queue,))
    thread_start_server.start()

    #WAITS FOR THREAD TO GIVE OUTPUT (BAD OR GOOD)
    while True:
        state = close_queue.get()
        if state == 1:
            time.sleep(5)
            print('Success! Server is now ON!')
            break
        else:
            print(state)
            break

if __name__ == '__main__':

    main()