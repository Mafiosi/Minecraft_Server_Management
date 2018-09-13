from fabric import Connection


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

    command = 'systemctl poweroff'

    print('\nRunning command: {}\n'.format(command))

    shutdown = Connection(host=d, user=u, connect_kwargs={
        "password": p}).run(command)

    print('\n' + str(shutdown))


if __name__ == '__main__':

    main()
