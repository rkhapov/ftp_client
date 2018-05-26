#!/usr/bin/env python3

import argparse
import sys
import re

from commands.command_factory import CommandFactory, CommandFactoryError
from client.tcpconnection import *


def parse_address(address: str):
    tokens = re.split(':', address)

    if len(tokens) == 1:
        return tokens[0], 21

    if len(tokens) != 2:
        raise SyntaxError('Address string should have one of formats:\n'
                          'host:port\n'
                          'host in case port 21 are used')

    return tokens[0], int(tokens[1])


def parse_args():
    parser = argparse.ArgumentParser(description='Simple ftp client on python')
    parser.add_argument('address', help='address of ftp server', type=str)
    parser.add_argument('-l', '--logfile', help='log file for all network  low-level operations',
                        type=str, default=None)

    args = parser.parse_args()

    return args.address, args.logfile


def process_next_command(connection: Connection, factory: CommandFactory):
    try:
        command = factory.from_string(input('$> '))
        command.execute(connection)
    except CommandFactoryError as e:
        print(e.args[0])
    except KeyboardInterrupt:
        print('\nKeyboard interrupt received: ending session...')
        factory.from_string('quit').execute(connection)
        sys.exit(0)


def create_ftp_client():
    try:
        address, logfile = parse_args()
        address, port = parse_address(address)
        connection = None  # TcpConnection(address, port, logfile)
        command_factory = CommandFactory()

        return connection, command_factory

    except Exception as e:
        print('Error creating ftp client: ', e.__class__.__name__, e.args[0])
        sys.exit(1)


def main():
    connection, factory = create_ftp_client()

    while True:
        process_next_command(connection, factory)


if __name__ == '__main__':
    main()
