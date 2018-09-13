from wakeonlan import send_magic_packet
from fabric import Connection

import socket
import time


def main():

    username = 'mafi'
    password = '#cenas1234'

    dns = 'belezamafiosi.ddns.net'
    mac = '1c:b7:2c:b0:28:61'
    port = 9

    command = 'cd /home/mafi/Desktop/scripts; Internal_MManager.py 1'

    print('Looking up server info:')

    ip = socket.gethostbyname(dns)

    print('DNS: {} -> IP: {}'.format(dns, ip))

    print('\nServer mac address:')
    print('MAC: {}'.format(mac))

    zzz = 60

    send_magic_packet(mac, ip_address=ip, port=port)

    print('\nSent magic packet to:\nIP: {}\nPORT: {}'.format(ip, port))

    print('\nWaiting for pc to turn on... \n(eta: ~{}s)'.format(zzz))
    time.sleep(zzz)

    print('\nRunning command: {}\n'.format(command))

    minecraft = Connection(host=dns, user=username, connect_kwargs={
                           "password": password}).run(command)

    print('\n' + str(minecraft))


if __name__ == '__main__':

    main()