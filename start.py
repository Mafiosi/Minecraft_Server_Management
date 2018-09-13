import sys
import time
import threading
from threading import Thread
from threading import Timer
from queue import Queue
from subprocess import Popen, PIPE, STDOUT
from distutils.dir_util import copy_tree

##########    MAIN PROGRAM    ##########

def Server_Read(r_q,w_q,server):
    global message
    while True:
        output = server.stdout.readline()

        #Prints Without Conditions
        if output and flag is not True:
            print(output.decode("utf-8"))
            server.stdout.flush()
        #Prints with a specific Condition
        elif output and flag is True:
            r_q.get()
            message = output
            print(output.decode("utf-8"))
            server.stdout.flush()
            w_q.put(1)
        elif output == b'' and server.poll() is not None:
            print("Exiting Reader")
            break
        else:
            print("Error reading server")
            break



def Server_Write(m_q,r_q,w_q,server):

    global flag
    while True:
        order = m_q.get()

        #Cicle to Check if there are Active Players
        if order == 1:
            print("Checking Active Players")
            flag = True
            time.sleep(1)
            server.stdin.write(bytes("list" + "\r", "ascii"))
            server.stdin.flush()

            r_q.put(1)
            w_q.get()
            m_q.put(1)
            flag = False
            time.sleep(1)

        #WILL SHUT-DOWN SERVER
        if order == 2:
            print("Shutting Down Server")

            #TELLS PLAYERS IF ACTIVE THE SERVER IS SHUTTING DOWN
            flag = True
            time.sleep(1)
            server.stdin.write(bytes("say The server will shutdown because there are no active players, if there are, too bad, reconnect again. x0x0" + "\r", "ascii"))
            server.stdin.flush()

            r_q.put(1)
            w_q.get()
            flag = False
            time.sleep(1)

            #ACTUALLY STOPS SERVER
            flag = True
            time.sleep(1)
            server.stdin.write(bytes("stop" + "\r","ascii"))
            server.stdin.flush()

            r_q.put(1)
            w_q.get()
            m_q.put(1)
            flag = False
            time.sleep(1)
            break


##########    MAIN PROGRAM    ##########

#INITITALIZATION OF SERVER
server = Popen("cd /opt/minecraft/server_1; java -Xms1024M -Xmx6144M -jar /opt/minecraft/server_1/forge-1.12.2-14.23.4.2759-universal.jar nogui",shell=True,stdin=PIPE, stdout=PIPE, stderr=STDOUT)

#INDICATES THAT'S SOMETHING IS GONNA BE WRITTEN
global flag
flag = False

#INDICATES ERROR AND SHUTS DOWN SERVER
error = False


main_Queue = Queue()
read_Queue = Queue()
write_Queue = Queue()

#MESSAGE BETWEEN READER AND MAIN FUCNTION
global message

#SHUT DOWN MESSAGE
global shut
shut = False

#BACKUP DIRECTORY
origin = "/opt/minecraft/server_1/world"
destination = "/opt/minecraft/Backup/Server_World"


thread_read = threading.Thread(name='Read_Server',target=Server_Read,args=(read_Queue,write_Queue,server,))
thread_write = threading.Thread(name='Write_Server',target=Server_Write,args=(main_Queue,read_Queue,write_Queue,server,))

thread_read.start()
thread_write.start()

while True:
    #WILL ASK TO CHECK IF PLAYER ARE ON THE SERVER TIMEOUT - 5 MIN
    time.sleep(30)
    main_Queue.put(1)
    time.sleep(1)
    main_Queue.get()
    a_p = int(message.decode("utf-8")[71])

    #WILL CHECK 2 TIMES IF SERVER IS EMPLTY TIMEOUT - 1 MIN
    if a_p == 0:
        for x in range(0,2):
            if a_p == 0:
                time.sleep(30)
                print("Vai 1")
                main_Queue.put(1)
                time.sleep(1)
                main_Queue.get()
                a_p = int(message.decode("utf-8")[71])

        #IF Two CHECKS PASS SERVERS SHUTS DOWN
        if a_p == 0:
            main_Queue.put(2)
            time.sleep(1)
            main_Queue.get()
            thread_read.join()
            thread_write.join()
            copy_tree(origin,destination)
            break


