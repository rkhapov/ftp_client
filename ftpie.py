import argparse
import socket
import sys

from infra.environment import EnvironmentBuilder
from infra.factory import CommandFactory
from network.address import IPv4Address, IPv6Address
from network.tcp import TcpConnection
from protocol.ftp import FtpClient


def parse_args():
    parser = argparse.ArgumentParser(description='Simple ftp client on python')
    parser.add_argument('address', help='address of ftp server', type=str)
    parser.add_argument('--port', '-p', help='port to connect, default is 21', type=int, default=21)
    parser.add_argument('--ipv6', help='enable ipv6 mode', action='store_true')
    parser.add_argument('--script', help='script to execute', type=str, default=None)

    args = parser.parse_args()

    if args.ipv6:
        return IPv6Address(args.address, args.port), args.ipv6, args.script
    return IPv4Address(args.address, args.port), args.ipv6, args.script


def get_client(timeout):
    address, is_ipv6, script = parse_args()
    factory = CommandFactory()
    environment = EnvironmentBuilder().build(factory.commands, is_ipv6, script)
    tcp_connection = TcpConnection(address, timeout)
    client = FtpClient(tcp_connection)

    return client, environment, factory


def execute_next_command(client, environment, factory):
    try:
        next_command = environment.reader.read_next_command('?>')

        if next_command is None:
            environment.closed = True
            return

        if (environment.is_pack_mode and next_command.strip().startswith('#')) or next_command == '':
            return

        command = factory.from_string(next_command, environment)

        command.execute(client)

    except NotImplementedError as e:
        print('Operation are not implemented yet', file=sys.stderr)
        print(e.args[0], file=sys.stderr)
    except ValueError as e:
        print('Error: {}'.format(e.args[0]), file=sys.stderr)


def main():
    try:
        client, environment, factory = get_client(15)

        with client.connection, environment.reader, environment.writer:
            if not environment.is_pack_mode:
                environment.writer.write('Client created')
                environment.writer.write(f'IPv4 address: {environment.ipv4_address}')
                environment.writer.write(f'IPv6 address: {environment.ipv6_address}')
                environment.writer.write(f'Used address: {environment.machine_address}')
                environment.writer.write(f'Is under NAT: {environment.is_under_nat}')
                environment.writer.write(f'Connection mode is IPv6: {client.connection.is_ipv6}')
                environment.writer.write('Ready for work')
                environment.writer.write('------------------------------------------------------')

            # receive hello from server
            environment.writer.write(client.start().text)

            while not environment.closed:
                execute_next_command(client, environment, factory)

    except socket.timeout:
        print('Network operation timeout, check if network is reachable', file=sys.stderr)
    except socket.gaierror as e:
        print(e.strerror, file=sys.stderr)
    except SyntaxError as e:
        print(e.text, file=sys.stderr)
    except ConnectionResetError as e:
        print('server reset the connection: {}'.format(e.strerror), file=sys.stderr)
    except ConnectionAbortedError as e:
        print('connection was aborted: {}'.format(e.strerror), file=sys.stderr)
    except ConnectionError as e:
        print('connection error: {}'.format(e.strerror), file=sys.stderr)
    except OSError as e:
        print("OSError:", e.strerror, file=sys.stderr)
    except ImportError as e:
        if e.name == 'chardet':
            print('you need to install chardet package', file=sys.stderr)
        else:
            raise
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
