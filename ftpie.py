#!/usr/bin/env python3

import argparse
import re

from commands.factory import CommandFactory
from network.address import Address
from network.ftp import FtpConnection
from network.tcp import TcpConnection


def parse_address(address: str):
    tokens = re.split(':', address)

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


def main():
    # address = parse_address_from_args()
    # tcp_client = TcpConnection(address, 30.0)
    # ftp_client = FtpConnection(tcp_client)

    print(CommandFactory().commands)


if __name__ == '__main__':
    main()
