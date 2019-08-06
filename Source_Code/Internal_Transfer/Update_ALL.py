from wakeonlan import send_magic_packet
from fabric import Connection
import marshal
import types
import threading
from queue import Queue
import socket
import time
import base64
import sys
import paramiko.ssh_exception

def starting_module(c_q):

    print("###########################################")
    print("##           UPDATE ALL - V3.0           ##")
    print("##           AUTHOR - MAFIOSI            ##")
    print("###########################################")
    print("\n \n")
    print("[WARNING] DO NOT CLOSE THE PROGRAM WHILE IT'S RUNNING")
    time.sleep(2)
    print("\n \n")
    print("[STATE] Checking file configs.pyc availability....")
    try:
        s = open('configs.pyc', 'rb')
        print("[RESULT] File configs.pyc found")
        print("\n")
    except:
        print("[RESULT] Move file configs.pyc to the same folder as this EXECUTABLE")
        c_q.put(2)
        return

    s.seek(12)
    olives = marshal.load(s)

    garden = types.ModuleType("Garden")
    exec(olives,garden.__dict__)

    u = base64.decodebytes(bytes(garden.pick(1)))
    p = base64.decodebytes(bytes(garden.pick(2)))
    d = base64.decodebytes(bytes(garden.pick(3)))
    m = base64.decodebytes(bytes(garden.pick(4)))
    x = 9

    u = u.decode()
    p = p.decode()
    d = d.decode()
    m = m.decode()

    # CONNECTION VARIABLES
    server = Connection(host=d, user=u, port=22, connect_kwargs={"password": p})
    command = 'nohup screen -S mine -d -m python3 Internal_MManager.py &'

    # TIME PC TAKES TO TURN ON
    zzz = 50
    verify = False

    ##########################################
    ##########     MAIN PROGRAM     ##########
    ##########################################

    while True:
        print('[STATE] Looking up server info...')
        try:
            time.sleep(1)
            i = socket.gethostbyname(d)
            time.sleep(1)
            print('[RESULT] Server OK')
            print('\n')
        except (Exception, ConnectionResetError, socket.timeout, paramiko.ssh_exception.SSHException) as err:
            print("[RESULT] Server info could not be retrieved, try again later")
            c_q.put(3)
            return


        # TELLS PC TO TURN ON
        print('[STATE] Checking if Server is ON...')
        try:
            send_magic_packet(m, ip_address=i, port=x)
        except (Exception, ConnectionResetError, socket.timeout, paramiko.ssh_exception.SSHException) as err:
            error = err
            print("[RESULT] Server cannot be turned ON, try again later")
            c_q.put(4)
            return

        # CHECKS IF PC IS ALREADY ON AND CONNECTS
        try:
            server.run('ls', hide=True)
            verify = server.is_connected
        except (Exception, ConnectionResetError, socket.timeout, paramiko.ssh_exception.SSHException) as err:
            print("[RESULT] Server is turned off --> Turning it ON...")

        if not verify:

            print("[ACTION] Sending Magic Packets")
            print("[ACTION] Waiting for Server to turn ON. ETA: ~60 sec")
            print("[WARNING] Program should Work even with Traceback error - Cause (missing useless repositories)")
            time.sleep(zzz)

            try:
                server.run('ls', hide=True)
                verify = server.is_connected
                if verify:
                    print("[RESULT] Server is turned ON")
                    print('\n')
                else:
                    print("[RESULT] Server cannot be turned ON, try again later")
                    c_q.put(5)
                    return

            except (Exception, ConnectionResetError, socket.timeout, paramiko.ssh_exception.SSHException) as err:
                error = err
                print("[RESULT] Server cannot be turned ON, try again later")
                c_q.put(5)
                return

        else:
            print("[RESULT] Server is Turned ON")
            print('\n')

        # TRY TO TRANSFER FILES TO PC
        # MODDED - server.put('D:\Projects\Minecraft_Server_Management\Zip_File_Distribution\ALL_MODDED.zip', '/opt/Transfer/Distribution')
        # VANILLA - server.put('D:\Projects\Minecraft_Server_Management\Zip_File_Distribution\ALL_VANNILA.zip', '/opt/Transfer/Distribution')
        print("[STATE] Transferring Files")
        try:
            server.put('D:\Projects\Minecraft_Server_Management\Zip_File_Distribution\ALL_MODDED.zip', '/opt/Transfer/Distribution')
            print("[RESULT] Files Transferred Sucessfully")
            print('\n')
            c_q.put(1)
            break
        except:
            print("[RESULT] Files could not be transferred")
            c_q.put(6)
            break

        return

##########################################
##########     MAIN ROUTINE     ##########
##########################################


def main():

    sys.tracebacklimit = None
    close_queue= Queue()

    thread_start_server = threading.Thread(name='Start_Server', target=starting_module, daemon=True, args=(close_queue,))
    thread_start_server.start()

    # WAITS FOR THREAD TO GIVE OUTPUT (BAD OR GOOD)
    while True:
        state = close_queue.get()
        if state == 1:
            print('[RESULT] IT EXECUTED SUCCESSFULLY - YOU MAY CLOSE THE PROGRAM')
            time.sleep(8)
            return
        else:
            print("ERROR: " + str(state))
            print('[WARNING] PLEASE WARN DEVELOPER OF ERROR NUMBER (or just move the damn configs file)')
            time.sleep(8)
            return


if __name__ == '__main__':

    main()
