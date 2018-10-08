from enum import Enum
from tools.get_ip import *


class ConnectionMode(Enum):
    PASSIVE = 1
    PORT = 2


class Environment:
    def __init__(self, connection_mode, closed, ipv4_address, ipv6_address, commands, ipv6_mode):
        self.connection_mode = connection_mode
        self.closed = closed
        self.__commands = commands
        self.__ipv4_address = ipv4_address
        self.__ipv6_address = ipv6_address
        self.__ipv6_mode = ipv6_mode

    @property
    def ipv6_mode(self):
        return self.__ipv6_mode

    @property
    def ipv4_address(self):
        return self.__ipv4_address

    @property
    def ipv6_address(self):
        return self.__ipv6_address

    @property
    def commands(self):
        return self.__commands

    @property
    def closed(self):
        return self.__closed

    @closed.setter
    def closed(self, value):
        self.__closed = value

    @property
    def connection_mode(self):
        return self.__connection_mode

    @connection_mode.setter
    def connection_mode(self, value: ConnectionMode):
        if not isinstance(value, ConnectionMode):
            raise ValueError('value of connection mode must be of type ConnectionMode')

        self.__connection_mode = value

    @property
    def machine_address(self):
        if self.__ipv6_mode:
            return self.__ipv6_address
        return self.__ipv4_address


class EnvironmentBuilder:
    def __init__(self):
        pass

    def build(self, commands, ipv6_mode):
        return Environment(connection_mode=ConnectionMode.PASSIVE,
                           closed=False,
                           commands=commands,
                           ipv4_address=get_ipv4(),
                           ipv6_address=get_ipv6(),
                           ipv6_mode=ipv6_mode)
