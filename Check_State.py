from fabric2 import Connection
import marshal
import types

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
            server.open()
            verify = server.is_connected

        # SERVER IS OFF
        except:
            print("PC is turned off\nThe Server is Off...")
            break

        verify = server.is_connected
        #CHECKS IF PC IS ALREADY ON
        if verify:
            print("PC is turned ON")
            print("Checking if Server is Up...")

            # CHECK IF SERVER IS ALREADY ON
            try:
                a = server.run('pgrep -a java')
                if a != None:
                    print("Server is already running")
                    break

                # SERVER IS OFF
                else:
                    print("Server is Off\nTurn it on with Start_MManager!")
                    time.sleep(5)
                    break
            except:
                print("Error Connecting to PC, try again...")
                c_q.put(2)
                break

if __name__ == '__main__':

    main()