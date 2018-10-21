#!/usr/bin/env python3
import socket

from network.address import Address, IPv4Address, IPv6Address
from network.connection import Connection
from network.server import Server


class TcpConnection(Connection):
    def __init__(self, address: Address = None, timeout=None, sock=None):
        if sock is not None:
            if sock.family != socket.AF_INET or sock.family != socket.AF_INET6:
                raise TypeError(f'Expected socket family to be AF_INET or AF_INET6, but {sock.family} found')
            self.__socket = sock
        else:
            family = socket.AF_INET if isinstance(address, IPv4Address) else socket.AF_INET6
            self.__socket = socket.socket(family, socket.SOCK_STREAM)
            self.__socket.settimeout(timeout)
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
        sockname = self.__socket.getsockname()

        if not self.is_ipv4:
            return IPv4Address(host=sockname[0], port=sockname[1])

        return IPv6Address(host=sockname[0], port=sockname[1])

    @property
    def peer_address(self):
        sockname = self.__socket.getpeername()

        if self.is_ipv4:
            return IPv4Address(host=sockname[0], port=sockname[1])

        return IPv6Address(host=sockname[0], port=sockname[1])

    @property
    def is_ipv6(self):
        return self.__socket.family == socket.AF_INET6

    @property
    def is_ipv4(self):
        return self.__socket.family == socket.AF_INET

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
    def __init__(self, address: Address = None, timeout=None, ipv6_mode=False):
        self.__address = address
        self.__timeout = timeout
        ipv6_mode = ipv6_mode or isinstance(address, IPv6Address)
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

        if self.is_ipv6:
            return IPv6Address(host=a[0], port=a[1])

        return IPv4Address(host=a[0], port=a[1])

    def accept(self) -> Connection:
        s, a = self.__socket.accept()
        print(s)
        return TcpConnection(sock=s)

    @property
    def is_ipv6(self):
        return self.__socket.family == socket.AF_INET6

    @property
    def is_ipv4(self):
        return self.__socket.family == socket.AF_INET

    def close(self):
        self.__socket.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
