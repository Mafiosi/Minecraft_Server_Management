import sys
import threading
from threading import Thread
from threading import Timer
from subprocess import Popen, PIPE, STDOUT

##########    MAIN PROGRAM    ##########

def Server(flag):

    server = Popen("cd /opt/minecraft/server_1; java -Xms1024M -Xmx6144M -jar /opt/minecraft/server_1/forge-1.12.2-14.23.4.2759-universal.jar nogui",stdin=PIPE, stdout=PIPE, stderr=STDOUT)

    while True:
        output = server.stdout.readline()
        if output == '':
            break
        if output:
            print (output.strip())
        else:
            print("Error reading server")
            break





##########    MAIN PROGRAM    ##########

thread_server = threading.Thread(name='Init_Server',target=Server,args=(flag,))
thread_status = threading.Thread(name='Verify_Status',target=Status,args=(flag,))

thread_server.start()
thread_status.start()

thread_server.join()
thread_status.join()