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
        mode = input('Do you want to use this machine as server(yes, no)[yes]:')

        if mode == '' or mode.lower() == 'yes':
            return self.__get_server_with_current_machine(client)
        return self.__get_external_server(client)

    def __get_server_with_current_machine(self, client: FtpClient):
        if self.environment.is_under_nat:
            print('Cant create server on machine under nat')
            return None

        server = TcpServer(ipv6_mode=self.environment.is_ipv6_mode, timeout=15)
        addr = server.listen()
        ftp_addr = Address(host=self.environment.machine_address, port=addr.port, type=addr.type)

        reply = client.execute(f'port {ftp_addr.ftp_address}')

        if reply.status_code == StatusCode.COMMAND_OK.value:
            return server

        print(reply.text)
        return None

    def __get_external_server(self, client: FtpClient):
        address = input('Enter receiver address (in FTP format): ')
        reply = client.execute(f'port {address}')

        if reply.status_code != StatusCode.COMMAND_OK.value:
            print(reply.text)
            return None

        return 'external'
