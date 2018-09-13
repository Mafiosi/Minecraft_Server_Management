from wakeonlan import send_magic_packet
from fabric import Connection
import marshal
import types

import socket
import time


def main():

    s = open('configs.pyc','rb')
    s.seek(12)
    olives = marshal.load(s)

    garden = types.ModuleType("Garden")
    exec(olives,garden.__dict__)

    u = garden.pick(1)
    p = garden.pick(2)

    d = garden.pick(3)
    m = garden.pick(4)
    po = 9

    command = 'cd /home/mafi/Desktop/scripts; Internal_MManager.py 1'

    print('Looking up server info:')

    ip = socket.gethostbyname(d)

    print('DNS: {} -> IP: {}'.format(d, ip))

    print('\nServer mac address:')
    print('MAC: {}'.format(m))

    zzz = 60

    send_magic_packet(m, ip_address=ip, port=po)

    print('\nSent magic packet to:\nIP: {}\nPORT: {}'.format(i, po))

    print('\nWaiting for pc to turn on... \n(eta: ~{}s)'.format(zzz))
    time.sleep(zzz)

    print('\nRunning command: {}\n'.format(command))

    minecraft = Connection(host=d, user=u, connect_kwargs={
                           "password": p}).run(command)

    print('\n' + str(minecraft))


if __name__ == '__main__':

    main()