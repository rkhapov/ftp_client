import argparse
import re
import socket

from infra.environment import EnvironmentBuilder
from infra.factory import CommandFactory
from network.address import Address
from network.tcp import TcpConnection
from protocol.ftp import FtpClient


def parse_address(address: str):
    tokens = [t for t in re.split(':', address) if t != '']

    if len(tokens) == 1:
        return tokens[0], 21

    if len(tokens) != 2:
        raise SyntaxError('Address string should have one of formats:\n'
                          '<host>:<port>\n'
                          '<host> in case port 21 are used')

    return tokens[0], int(tokens[1])


def parse_address_from_args():
    parser = argparse.ArgumentParser(description='Simple ftp client on python')
    parser.add_argument('address', help='address of ftp server', type=str)

    args = parser.parse_args()

    address = parse_address(args.address)

    return Address(address[0], address[1])


def get_client(timeout):
    address = parse_address_from_args()
    tcp_connection = TcpConnection(address, timeout)
    client = FtpClient(tcp_connection)
    factory = CommandFactory()
    environment = EnvironmentBuilder().build(factory.commands)

    return client, environment, factory


def execute_next_command(client, environment, factory):
    try:
        command = factory.from_string(input("$> "), environment)

        command.execute(client)

    except NotImplementedError:
        print('Operation are not implemented yet')
    except ValueError as e:
        print('Error: {}'.format(e.args[0]))


def main():
    try:
        client, environment, factory = get_client(15)

        # receive hello from server
        print(client.start().text)

        while not environment.closed:
            execute_next_command(client, environment, factory)

        client.connection.close()

    except socket.timeout:
        print('Network operation timeout, check if network is reachable')
    except SyntaxError as e:
        print(e.text)
    except ConnectionResetError as e:
        print('server broke the connection: {}'.format(e.strerror))
    except ConnectionAbortedError as e:
        print('connection was aborted: {}'.format(e.strerror))
    except ConnectionError as e:
        print('connection error: {}'.format(e.strerror))
    except ImportError as e:
        if e.name == 'chardet':
            print('you need to install chardet package')
        else:
            raise


if __name__ == '__main__':
    main()
