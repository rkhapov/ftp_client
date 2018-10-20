import argparse
import socket

from infra.environment import EnvironmentBuilder
from infra.factory import CommandFactory
from network.address import Address
from network.tcp import TcpConnection
from protocol.ftp import FtpClient


def parse_args():
    parser = argparse.ArgumentParser(description='Simple ftp client on python')
    parser.add_argument('address', help='address of ftp server', type=str)
    parser.add_argument('--port', '-p', help='port to connect, default is 21', type=int, default=21)
    parser.add_argument('--ipv6', help='enable ipv6 mode', action='store_true')

    args = parser.parse_args()

    return Address(args.address, args.port), args.ipv6


def get_client(timeout):
    address, is_ipv6 = parse_args()
    factory = CommandFactory()
    environment = EnvironmentBuilder().build(factory.commands, is_ipv6)
    tcp_connection = TcpConnection(address, timeout, is_ipv6)
    client = FtpClient(tcp_connection)

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
        print('Creating client...')
        client, environment, factory = get_client(15)

        print('Client created')
        print(f'IPv4 address: {environment.ipv4_address}')
        print(f'IPv6 address: {environment.ipv6_address}')
        print(f'Connection mode is {environment.connection_mode}')
        print(f'Used address: {environment.machine_address}')
        print(f'Is under NAT: {environment.is_under_nat}')
        print('Ready for work')
        print('------------------------------------------------------')

        # receive hello from server
        print(client.start().text)

        while not environment.closed:
            execute_next_command(client, environment, factory)

        client.connection.close()

    except socket.timeout:
        print('Network operation timeout, check if network is reachable')
    except socket.gaierror as e:
        print(e.strerror)
    except SyntaxError as e:
        print(e.text)
    except ConnectionResetError as e:
        print('server reset the connection: {}'.format(e.strerror))
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
