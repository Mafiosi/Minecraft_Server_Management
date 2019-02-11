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

    ##########################################
    ##########      VARIABLES       ##########
    ##########################################

    print("Checking that configs.pyc is in the same folder....")
    try:
        s = open('configs.pyc', 'rb')
        print("It is... nice.")
    except:
        print("It is not... Move it to the same folder.")
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

    #CONNECTION VARIABLES
    server = Connection(host=d, user=u, port=22, connect_kwargs={"password": p})
    command = 'nohup screen -S mine -d -m python3 Internal_MManager.py &'

    #TIME PC TAKES TO TURN ON
    zzz = 50
    verify = False

    ##########################################
    ##########     MAIN PROGRAM     ##########
    ##########################################

    while True:
        print('Looking up server info and Checking if PC is ON...')
        try:
            time.sleep(1)
            i = socket.gethostbyname(d)
            time.sleep(1)
        except (Exception, ConnectionResetError, socket.timeout, paramiko.ssh_exception.SSHException) as err:
            print("Server info could not be retrieved")
            c_q.put(3)
            return


        # TELLS PC TO TURN ON
        try:
            send_magic_packet(m, ip_address=i, port=x)
        except (Exception, ConnectionResetError, socket.timeout, paramiko.ssh_exception.SSHException) as err:
            error = err
            print("PC cannot be turned ON")
            c_q.put(4)
            return

        #CHECKS IF PC IS ALREADY ON AND CONNECTS
        try:
            server.run('ls', hide=True)
            verify = server.is_connected
        except (Exception, ConnectionResetError, socket.timeout, paramiko.ssh_exception.SSHException) as err:
            print("PC is turned off --> Turning it ON...")

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
                    c_q.put(5)
                    return

            except (Exception, ConnectionResetError, socket.timeout, paramiko.ssh_exception.SSHException) as err:
                error = err
                print("PC cannot be turned ON")
                c_q.put(5)
                return

        else:
            print("PC is Turned ON")

        #CHECK IF SERVER IS ALREADY ON
        try:
            a = server.run('pgrep -f minecraft')
            if a is not None:
                c_q.put(1)
                print("Server is already running")
                break
        except Exception as err:
            error = err
            print("Initializing Minecraft Server...")

        # TURN SERVER ON
        try:
            with server.cd('/opt/scripts/'):
                server.run(command)
            c_q.put(1)
            print('Success! Server is now Turning ON.   ETA: ~60s')
        except:
            print("Minecraft Server Failed to Initialize")
            c_q.put(6)

        return

##########################################
##########     MAIN ROUTINE     ##########
##########################################


def main():

    sys.tracebacklimit = None
    close_queue= Queue()

    thread_start_server = threading.Thread(name='Start_Server', target=starting_module, daemon=True, args=(close_queue,))
    thread_start_server.start()

    #WAITS FOR THREAD TO GIVE OUTPUT (BAD OR GOOD)
    while True:
        state = close_queue.get()
        if state == 1:
            time.sleep(5)
            return
        else:
            print("ERROR: " + state)
            time.sleep(5)
            return


if __name__ == '__main__':

    main()
