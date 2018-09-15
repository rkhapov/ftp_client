from enum import Enum


class ConnectionMode(Enum):
    PASSIVE = 1
    PORT = 2


class Environment:
    def __init__(self, connection_mode, port_address):
        self.connection_mode = connection_mode
        self.port_address = port_address

    @property
    def connection_mode(self):
        return self.__connection_mode

    @connection_mode.setter
    def connection_mode(self, value: ConnectionMode):
        if not isinstance(value, ConnectionMode):
            raise ValueError('value of connection mode must be of type ConnectionMode')

        self.__connection_mode = value

    @property
    def port_address(self):
        return self.__port_address

    @port_address.setter
    def port_address(self, value: str):
        if not isinstance(value, str):
            raise ValueError('value of port address must be of type str')

        self.__port_address = value


class EnvironmentBuilder:
    def __init__(self):
        pass

    def build(self):
        return Environment(ConnectionMode.PASSIVE, '')
