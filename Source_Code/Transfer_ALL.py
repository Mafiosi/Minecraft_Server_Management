from wakeonlan import send_magic_packet
from fabric2 import Connection
import marshal
import types
import socket
import time
import base64


def main():

    ##########################################
    ##########      VARIABLES       ##########
    ##########################################

    # DECRYPTING INFO
    s = open('configs.pyc', 'rb')
    s.seek(12)
    olives = marshal.load(s)

    garden = types.ModuleType("Garden")
    exec(olives, garden.__dict__)

    u = base64.decodebytes(bytes(garden.pick(1)))
    p = base64.decodebytes(bytes(garden.pick(2)))
    d = base64.decodebytes(bytes(garden.pick(3)))
    m = base64.decodebytes(bytes(garden.pick(4)))
    x = 9

    u = u.decode()
    p = p.decode()
    d = d.decode()
    m = m.decode()

    #CONNECTION VARIABLES
    server = Connection(host=d, user=u, connect_kwargs={
        "password": p})

    #TIME PC TAKES TO TURN ON
    zzz = 50
    verify = False

    ##########################################
    ##########     MAIN PROGRAM     ##########
    ##########################################

    while True:
        print('Looking up server info and Checking if PC is ON...')
        try:
            i = socket.gethostbyname(d)
        except:
            print("Server info could not be retrieved")
            print("Exiting")
            time.sleep(5)
            break

        # TELLS PC TO TURN ON
        try:
            send_magic_packet(m, ip_address=i, port=x)
        except:
            print("PC cannot be turned ON")
            print("Exiting")
            time.sleep(5)
            break

        #TRY CONNECTING TO PC
        try:
            server.run('ls', hide=True)
            verify = server.is_connected
        except:
            print("PC is turned off --> Turning it ON...")

        #CHECKS IF PC IS ALREADY ON
        if not verify:

            print("Magic Packets Sent")
            print("Waiting for PC to turn ON. ETA: ~60 sec")
            print("Program should Work even with Traceback error")
            time.sleep(zzz)

            try:
                server.run('ls', hide=True)
                verify = server.is_connected
                if verify:
                    print("PC is turned ON")
                else:
                    print("PC cannot be turned ON")
                    print("Exiting")
                    time.sleep(5)
                    break

            except:
                print("PC cannot be turned ON")
                print("Exiting")
                time.sleep(5)
                break


        # IF PC IS TURNED OFF
        else:
            print("PC is turned ON")

        #TRY TO TRANSFER FILES TO PC
        try:
            print("Initializing Files Transfer...")
            print("Folder: ALL.zip   Size: 512 MB   ETA: 3-5 min")
            print("DON'T CLOSE THE WINDOW! It will close automatically when done")
            server.get('/opt/Transfer/DISTRIBUTION/ALL.zip', None, True)
            print("Files Were Transfered Successfully!")
            break
        except:
            print("Couldn't Transfer Files TO PC, Check Connection.")
            break


if __name__ == '__main__':

    main()