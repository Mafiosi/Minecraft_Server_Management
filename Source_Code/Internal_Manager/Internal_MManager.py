import os
import time
import threading
import marshal
import types
from queue import Queue
from subprocess import Popen, PIPE, STDOUT, call
from distutils.dir_util import copy_tree
import base64

#WRITES READS SERVER FUNCTIONS
def Server_Read(r_q,w_q,server):

    global message
    while True:
        #GETS SERVER MESSAGE
        output = server.stdout.readline()

        #Prints Without Conditions
        if output and flag is not True:
            print(output.decode("utf-8")[0:-1])
            server.stdout.flush()

        #Prints with a specific Condition
        elif output and flag is True:
            print("STARTING CYCLE READ PLAYERS")
            a = r_q.get()
            message = output
            #CHECKING ACTIVE PLAYERS
            if a == 1:
                while True:
                    try:
                        if int(message.decode("utf-8")[73]) is 2 and int(message.decode("utf-8")[74]) is 0:
                            break
                        else:
                            print(message.decode("utf-8")[0:-1])
                            server.stdout.flush()
                            message = server.stdout.readline()

                    except:
                        print(message.decode("utf-8")[0:-1])
                        server.stdout.flush()
                        message = server.stdout.readline()

                print(output.decode("utf-8")[0:-1])
                server.stdout.flush()
                w_q.put(1)
                time.sleep(1)
                print("READER BACK TO NORMAL")
            #SHUTTING DOWN SERVER
            if a == 2:
                print("READ ACCEPTED SHUTDOWN")
                print(output.decode("utf-8")[0:-1])
                server.stdout.flush()
                w_q.put(1)
                time.sleep(1)

        #EXIT WHEN SERVER TERMINATED
        elif output == b'' and server.poll() is not None:
            print("Exiting Reader")
            break
        #ERROR CONDITION
        else:
            print("Error reading server")
            break

#WRITES FUNCTIONS TO SERVER
def Server_Write(m_q,r_q,w_q,server):

    global flag
    while True:
        #WAITS FOR CONTROL TO SEND SOMETHING TO PRINT
        order = m_q.get()

        #CONDITION TO CHECK PLAYERS
        if order == 1:
            print("Checking Active Players")

            #FLAG INDICATES READ TO STOP FOR NO BUFFER INTERFERENCE
            flag = True
            time.sleep(1)
            server.stdout.flush()

            #WRITES MESSAGE
            server.stdin.write(bytes("list" + "\r", "ascii"))
            server.stdin.flush()

            #COMMUNICATION WITH READER TO CHECK IF SAFE
            r_q.put(1)
            w_q.get()
            m_q.put(1)
            flag = False
            time.sleep(1)
            print("WRITER BACK TO NORMAL")

        #CONDITION TO SHUT DOWN SERVER
        if order == 2:
            print("Shutting Down Server")

            #TELLS PLAYERS IF ACTIVE THE SERVER IS SHUTTING DOWN
            flag = True
            time.sleep(1)
            server.stdout.flush()
            # WRITES MESSAGE
            server.stdin.write(bytes("say The server will shutdown because there are no active players, if there are, too bad, reconnect again. x0x0" + "\r", "ascii"))
            server.stdin.flush()
            #COMMUNICATES WITH READER
            r_q.put(2)
            w_q.get()
            flag = False
            time.sleep(3)

            #ACTUALLY STOPS SERVER
            flag = True
            time.sleep(1)
            server.stdout.flush()
            # WRITES MESSAGE
            server.stdin.write(bytes("stop" + "\r", "ascii"))
            server.stdin.flush()
            # COMMUNICATES WITH READER
            r_q.put(2)
            w_q.get()
            m_q.put(1)
            flag = False
            time.sleep(1)
            print("Exiting Writer")
            break


##########################################
##########      VARIABLES       ##########
##########################################


#INITITALIZATION OF SERVER
server = Popen("java -Xms1G -Xmx5G -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=16M -jar /opt/minecraft_modded/forge-1.12.2-14.23.5.2854.jar nogui", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)

#INDICATES THAT'S SOMETHING IS GONNA BE WRITTEN
global flag
flag = False

#QUEUES FOR COMMUNICATION: MAIN-SERVER/WRITER
main_Queue = Queue()
read_Queue = Queue()
write_Queue = Queue()

#MESSAGE BETWEEN READER AND MAIN FUCNTION
global message

#SHUT DOWN MESSAGE
global shut
shut = False

#BACKUP DIRECTORY
origin = "/opt/minecraft_modded/world"
destination = "/opt/Backups/Server_World_Modded"

#tHREAD INITIALIZATION
thread_read = threading.Thread(name='Read_Server',target=Server_Read,args=(read_Queue,write_Queue,server,))
thread_write = threading.Thread(name='Write_Server',target=Server_Write,args=(main_Queue,read_Queue,write_Queue,server,))
thread_read.start()
thread_write.start()

# DECRYPTING INFO
s = open('configs.pyc', 'rb')
s.seek(12)
olives = marshal.load(s)

garden = types.ModuleType("Garden")
exec(olives, garden.__dict__)

p = base64.decodebytes(bytes(garden.pick(2)))
p = p.decode()

##########################################
##########     MAIN PROGRAM     ##########
##########################################
while True:
    #WILL ASK TO CHECK IF PLAYER ARE ON THE SERVER TIMEOUT - 7 MIN
    time.sleep(420)
    print("MAIN START CHECKING")
    x = 0
    main_Queue.put(1)
    time.sleep(1)
    main_Queue.get()
    try:
        a_p = int(message.decode("utf-8")[71])
    except:
        print("Error in data cycle. Waiting for the next one")
        a_p = 1

    #WILL CHECK 2 TIMES IF SERVER IS EMPLTY TIMEOUT - 1.5 MIN
    if a_p == 0:
        while x < 2:
            print("TRY: " + str(x))
            time.sleep(90)
            main_Queue.put(1)
            time.sleep(1)
            main_Queue.get()
            try:
                a_p = int(message.decode("utf-8")[71])
            except:
                print("Error in small data cycle. Waiting for the next one")
                x = 1
                a_p = 0

            if a_p == 0:
                x += 1
            else:
                print("MAIN BACK TO NORMAL")
                break

        #IF TWO CHECKS PASS SERVERS SHUTS DOWN
        if a_p == 0:
            print("Turning OFF")
            main_Queue.put(2)
            time.sleep(5)
            main_Queue.get()
            #WAITS FOR THREADS TO CLOSE
            thread_read.join()
            thread_write.join()
            #MAKES BACKUP
            print("Making a Backup....")
            copy_tree(origin, destination)
            print("Backup Done! The Computer will Shut down.")
            time.sleep(3)
            break

print("CYA")
os.system("sudo /sbin/shutdown -h now")
