from wakeonlan import send_magic_packet
from fabric import Connection
import marshal
import types
import threading
from queue import Queue

import socket
import time

def starting_module():


    #DECRYPTING INFO
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
    c = Connection(host=d, user=u, connect_kwargs={
        "password": p})
    command = 'python3 Internal_MManager.py'

    #TIME PC TAKES TO TURN ON
    zzz = 60

    # MAIN PROGRAM
    print("Checking if PC is already ON")
    c.open()
    a = c.is_connected

    #IF PC IS ALREADY ON
    if a:
        print("PC is turned ON")
        print("Initializing Minecraft Server...")

        try:
            with c.cd('/home/mafi/scripts/'):
                c.run(command)

            print('Success! Server is now ON!')
            c_q.put(1)
        except:
            print("Minecraft Server Failed to Initialize")
            c_q.put(1)

    #IF PC IS TURNED OFF
    else:

        print('Looking up server info')
        try:
            i = socket.gethostbyname(d)
        except:
            print("Server info could not be retrieved")
            c_q.put(1)


        print('Waking up PC')
        try:
            send_magic_packet(m, ip_address=i, port=po)
        except:
            print("PC cannot be turned ON")
            c_q.put(1)

        print("Waiting for PC to turn ON. ETA: ~60 sec")
        time.sleep(zzz)

        print("Initializing Minecraft Server")

        try:
            with c.cd('/home/mafi/scripts/'):
                c.run(command)

            print('Success! Server is now ON!')
            c_q.put(1)
        except:
            print("Minecraft Server Failed to Initialize")
            c_q.put(1)
def main():

    close_queue= Queue()

    thread_start_server = threading.Thread(name='Start_Server', target=starting_module, args=(close_queue,))
    thread_start_server.start()

    while True:
        close_queue.get()
        break


if __name__ == '__main__':

    main()