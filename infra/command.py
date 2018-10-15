from abc import abstractmethod

from infra.environment import Environment, ConnectionMode
from network.address import Address
from network.tcp import TcpServer
from protocol.address_parser import extract_address_from_text
from protocol.ftp import FtpClient
from protocol.status import StatusCode


class Command:
    def __init__(self, environment: Environment):
        self.__arguments = {}
        self.__environment = environment

    @property
    def environment(self):
        return self.__environment

    @property
    def arguments(self):
        return self.__arguments

    def add_argument(self, name: str, value: str):
        if name in self.__arguments:
            raise LookupError('Argument with name {} already exists'.format(name))

        self.__arguments[name] = value

    def get_argument(self, name: str) -> str:
        name = name.lower()
        if name not in self.__arguments:
            raise LookupError('No argument with name {}'.format(name))

        return self.__arguments[name]

    def has_argument(self, name):
        return name.lower() in self.__arguments

    @abstractmethod
    def execute(self, client: FtpClient):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def help():
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def name():
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def format():
        raise NotImplementedError

    def _entry_pasv(self, client: FtpClient):
        if self.environment.connection_mode != ConnectionMode.PASSIVE:
            raise ValueError('entering into passive mode not in passive mode of environment')

        pasv_reply = client.execute('pasv')

        if pasv_reply.status_code == StatusCode.ENTERING_PASSIVE_MODE.value:
            return extract_address_from_text(pasv_reply.text)

        print(pasv_reply.text)
        return None

    def _entry_port(self, client: FtpClient):
        if self.environment.connection_mode != ConnectionMode.PORT:
            raise ValueError('entering into port mode not in port mode of environment')

        if self.environment.is_under_nat:
            print('Current machine are under NAT')
            print('Please, enter address which should be used as receiver')

            if self.environment.is_ipv6_mode:
                print('Please, dont forget that current mode is IPv6')
            else:
                print('Please, dont forget that current mode is IPv4')

            address_string = input(">")

            reply = client.execute(f"port {address_string}")

            if reply.status_code != StatusCode.COMMAND_OK.value:
                print(reply.text)
                return None

            return 'NAT'
        else:
            address_string = self.environment.machine_address
            server = TcpServer(timeout=15)
            addr = server.listen()
            connection_address = Address(host=address_string,
                                         port=addr.port,
                                         type='ipv6' if self.environment.is_ipv6_mode else 'ipv4')

            reply = client.execute(f"port {connection_address.ftp_address}")
            connection, address = server.accept()

            if reply.status_code != StatusCode.COMMAND_OK.value:
                print(reply.text)
                return None

            return server, connection, address
