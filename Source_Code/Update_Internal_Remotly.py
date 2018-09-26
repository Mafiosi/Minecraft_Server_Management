from wakeonlan import send_magic_packet
from fabric2 import Connection
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
            server.run('ls',hide=True)
        except:
            print("PC is turned off\n Turning it ON...")

        verify = server.is_connected
        #CHECKS IF PC IS ALREADY ON
        if verify:
            print("PC is turned ON")
            print("Initializing Files Transfer...")

            #TRY TO TRANSFER FILES TO PC
            try:
                server.put('D:\Coding_Projects\Minecraft_Server_Management\Source_Code\Internal_MManager.py','/usr/minecraft')
                print("Files Were Transfered Successfully!")
                break
            except:
                print("Couldn't Transfer Files TO PC, Check Connection.")
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
                break

            print("Waiting for PC to turn ON. ETA: ~60 sec")
            time.sleep(zzz)

            #INITIALIZING MINECRAFT SERVER BY RUNNING SERVER MANAGER
            print("Initializing Files Transfer...")

            #TRY TO TRANSFER FILES TO PC
            try:
                server.put('D:\Coding_Projects\Minecraft_Server_Management\Source_Code\Internal_MManager.py', '/usr/minecraft')
                print("Files Were Transfered Successfully!")
                break
            except:
                print("Couldn't Transfer Files TO PC, Check Connection.")
                break

if __name__ == '__main__':

    main()