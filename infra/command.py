from abc import abstractmethod

from infra.environment import Environment, ConnectionMode
from network.address import Address
from network.tcp import TcpServer
from protocol.address_parser import extract_address_from_text, extract_address_from_text_6
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
        if self.environment.is_ipv6_mode:
            return self._entry_pasv_6(client)

        pasv_reply = client.execute('pasv')

        if pasv_reply.status_code == StatusCode.ENTERING_PASSIVE_MODE.value:
            return extract_address_from_text(pasv_reply.text)

        print(pasv_reply.text)
        return None

    def _entry_pasv_6(self, client: FtpClient):
        reply = client.execute("epsv")

        if reply.is_success_reply:
            port = extract_address_from_text_6(reply.text)
            addr = client.connection.peer_address.with_port(port)

            return addr

        print(reply.text)
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
        ftp_addr = addr.with_host(self.environment.machine_address)

        if server.is_ipv4:
            reply = client.execute(f'port {ftp_addr.ftp_address}')
        else:
            reply = client.execute(f'eprt {ftp_addr.ftp_extendend_address}')

        if reply.status_code == StatusCode.COMMAND_OK.value:
            return server

        server.close()
        print(f'port command returned code {reply.status_code} with text {reply.text}')
        return None

    def __get_external_server(self, client: FtpClient):
        address = input('Enter receiver address (in FTP format): ')

        if not self.environment.is_ipv6_mode:
            reply = client.execute(f'port {address}')
        else:
            reply = client.execute(f'eprt {address}')

        if reply.status_code != StatusCode.COMMAND_OK.value:
            print(f'port command returned code {reply.status_code} with text {reply.text}')
            return None

        return 'external'
