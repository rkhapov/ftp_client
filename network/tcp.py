#!/usr/bin/env python3
import socket

from network.address import Address
from network.connection import Connection
from network.server import Server


class TcpConnection(Connection):
    def __init__(self, address: Address=None, timeout=None, ipv6_mode=False, sock=None):
        if sock is not None:
            self.__socket = sock
            self.__timeout = sock.gettimeout()
            sockname = self.__socket.getsockname()
            self.__address = Address(sockname[0], sockname[1])
        else:
            self.__address = address
            self.__timeout = timeout
            self.__socket = socket.socket(socket.AF_INET if not ipv6_mode else socket.AF_INET6, socket.SOCK_STREAM)
            self.__socket.settimeout(self.__timeout)
            self.__socket.connect(address.as_tuple)

    @property
    def timeout(self):
        return self.__socket.gettimeout()

    @timeout.setter
    def timeout(self, t):
        self.__socket.settimeout(t)

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

    def close(self):
        self.__socket.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class TcpServer(Server):
    def __init__(self, address: Address=None, timeout=None, ipv6_mode=False):
        self.__address = address
        self.__timeout = timeout
        self.__ipv6_mode = ipv6_mode
        self.__socket = socket.socket(socket.AF_INET if not ipv6_mode else socket.AF_INET6, socket.SOCK_STREAM)
        self.__socket.settimeout(timeout)

    @property
    def socket(self):
        return self.__socket

    def listen(self, backlog=1) -> Address:
        if self.__address:
            self.__socket.bind(self.__address.as_tuple)
        self.__socket.listen(backlog)
        a = self.__socket.getsockname()

        return Address(host=a[0], port=a[1])

    def accept(self) -> (Connection, Address):
        con, address = self.__socket.accept()

        return TcpConnection(sock=con), Address(address[0], address[1])

    def close(self):
        self.__socket.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
