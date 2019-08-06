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
    print("##           RESET WORLD - V3.0          ##")
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
            print('\n')
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

        # CHECK IF SERVER IS ALREADY ON
        print('[STATE] Checking Active Session...')
        try:
            a = server.run('pgrep -f minecraft')
            if a is not None:
                print("[RESULT] Session active - cannot reset world")
                print('\n')
                c_q.put(1)
                break
        except Exception as err:
            error = err

        # TRY TO TRANSFER FILES TO PC
        # VANILLA - server.run("cd /opt/minecraft_vanilla; rm -r -f /world; mkdir world ")
        # MODDED - server.run("cd /opt/minecraft; rm -r -f /world; mkdir world ")
        print("[RESULT] Session inactive - Reseting World...")
        try:
            server.run("cd /opt/minecraft_vanilla; rm -r -f /world; mkdir world ")
            print("[RESULT] World was Reset Successfully")
            print('\n')
            c_q.put(1)
            break
        except:
            print("[RESULT] World could not be reset")
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
