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
    print("##     TRANSFER TEXTURES ONLY - V3.0     ##")
    print("##         MODDED SERVER - 1.12.2        ##")
    print("##           AUTHOR - MAFIOSI            ##")
    print("###########################################")
    print()
    print("[WARNING] DO NOT CLOSE THE PROGRAM WHILE IT'S RUNNING")
    time.sleep(2)
    print()
    print("[STATE] Checking file configs.pyc availability....")
    try:
        s = open('configs.pyc', 'rb')
        print("[RESULT] File configs.pyc found")
        print()
    except:
        print("[RESULT] Move file configs.pyc to the same folder as this EXECUTABLE")
        c_q.put(2)
        return

    s.seek(12)
    olives = marshal.load(s)

    garden = types.ModuleType("Garden")
    exec(olives,garden.__dict__)

    alpha = base64.decodebytes(bytes(garden.pick(1)))
    beta = base64.decodebytes(bytes(garden.pick(2)))
    gamma = base64.decodebytes(bytes(garden.pick(3)))
    delta = base64.decodebytes(bytes(garden.pick(4)))
    x = 9

    alpha = alpha.decode()
    beta = beta.decode()
    gamma = gamma.decode()
    delta = delta.decode()

    # CONNECTION VARIABLES
    server = Connection(host=gamma, user=alpha, port=22, connect_kwargs={"password": beta})
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
            i = socket.gethostbyname(gamma)
            time.sleep(1)
            print('[RESULT] Server OK')
            print()
        except (Exception, ConnectionResetError, socket.timeout, paramiko.ssh_exception.SSHException) as err:
            print("[RESULT] Server info could not be retrieved, try again later")
            c_q.put(3)
            return


        # TELLS PC TO TURN ON
        print('[STATE] Checking if Server is ON...')
        try:
            send_magic_packet(delta, ip_address=i, port=x)
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
                    print()
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
            print()

        # TRY TO TRANSFER FILES TO PC
        print("[STATE] Initializing File Transfer")
        print("[SPECIFICATIONS] Folder: TEXTURES_ONLY_MODDED.zip   Size: 88 MB   ETA: 1-3 min")
        print("[CONTENTS]   1 - TEXTURES")
        print()

        answer = None
        i = 0
        while answer not in ("y", "n"):
            answer = input(" DO YOU WANT TO PROCEED?  y/n \n ANSWER: ")
            if answer == "y":
                try:
                    print()
                    print("[STATE] Transferring Files to this Executable's Folder")
                    print("[WARNING] DO NOT CLOSE THE WINDOW! It will close automatically when done")
                    server.get('/opt/Transfer/Modded/Distribution/Textures_Only_Modded.zip', None, True)
                    print("[RESULT] Files Were Transferred Successfully!")
                    print()
                    c_q.put(1)
                    break
                except:
                    print("[RESULT] Couldn't Transfer Files TO PC, Check Internet Connection or try again later")
                    c_q.put(6)
                    break
            elif answer == "n":
                print("[RESULT] Exiting Program")
                c_q.put(1)
                break
            else:
                i = i + 1
                if i == 3:
                    print()
                    print("[RESULT] Alright ya douche I'm closing the program")
                    c_q.put(1)
                    break
                print("\n[RESULT] That answer is not y(es) or n(o), care to change?")
                answer = None

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