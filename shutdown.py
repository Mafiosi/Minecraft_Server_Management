from fabric import Connection


def main():

    dns = 'belezamafiosi.ddns.net'

    username = 'mafi'
    password = '#cenas1234'

    command = 'systemctl poweroff'

    print('\nRunning command: {}\n'.format(command))

    shutdown = Connection(host=dns, user=username, connect_kwargs={
        "password": password}).run(command)

    print('\n' + str(shutdown))


if __name__ == '__main__':

    main()
