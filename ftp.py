import argparse

from commands.command_factory import CommandFactory
from client.tcpconnection import TcpConnection
from commands.command import Help


def parse_args():
    parser = argparse.ArgumentParser(description='Simple ftp client on python')
    parser.add_argument('-a', '--address', help='address of ftp server', type=str, required=True)
    parser.add_argument('-p', '--port', help='port of connection', type=int, default=21)
    parser.add_argument('-l', '--logfile', help='log file for all network operations', type=str, default=None)
    parser.add_argument('-s', '--script', help='script file for automatization', type=str, default=None)

    args = parser.parse_args()

    return args.address, args.port, args.logfile, args.script


def main():
    address, port, logfile, script = parse_args()
    connection = TcpConnection(address, port, logfile)
    command_factory = CommandFactory()

    while True:
        print(connection.receive(2048))
        # command = command_factory.from_string(input())
        # command.execute(connection)
        connection.send(input('$ '))


if __name__ == '__main__':
    main()
