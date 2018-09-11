#!/usr/bin/env python3

import socket

from network.address import Address


class TcpClient:
    def __init__(self, address: Address, timeout=None):
        self.__address = address
        self.__socket.settimeout(self.__timeout)
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect(address.as_tuple)
        self.__timeout = timeout

    @property
    def timeout(self):
        return self.__timeout

    @property
    def socket(self):
        return self.__socket

    @property
    def address(self):
        return self.__address

    def send(self, data: bytes):
        self.__socket.sendall(data)

    def receive(self, buf_size: int):
        return self.__socket.recv(buf_size)
