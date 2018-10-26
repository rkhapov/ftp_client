from abc import abstractmethod

from infra.environment import Environment
from network import downloader
from network.connection import Connection
from network.tcp import TcpServer
from protocol.address_parser import extract_address_from_text, extract_address_from_text_6
from protocol.ftp import FtpClient
from protocol.status import StatusCode
from tools.parse_helpers import try_parse_int


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

        self.environment.writer.write(pasv_reply.text)
        return None

    def _entry_pasv_6(self, client: FtpClient):
        reply = client.execute("epsv")

        if reply.is_success_reply:
            port = extract_address_from_text_6(reply.text)
            addr = client.connection.peer_address.with_port(port)

            return addr

        self.environment.writer.write(reply.text)
        return None

    def _entry_port(self, client: FtpClient):
        mode = self.environment.reader.read_next_command('Do you want to use this machine as server(yes, no)[yes]:')

        if mode == '' or mode.lower() == 'yes':
            return self.__get_server_with_current_machine(client)
        return self.__get_external_server(client)

    def __get_server_with_current_machine(self, client: FtpClient):
        if self.environment.is_under_nat:
            self.environment.writer.write('Cant create server on machine under nat', is_error=True)
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
        self.environment.writer.write(f'port command returned code {reply.status_code} with text {reply.text}', is_error=True)
        return None

    def __get_external_server(self, client: FtpClient):
        address = self.environment.reader.read_next_command('Enter receiver address (in FTP format): ')

        if not self.environment.is_ipv6_mode:
            reply = client.execute(f'port {address}')
        else:
            reply = client.execute(f'eprt {address}')

        if reply.status_code != StatusCode.COMMAND_OK.value:
            self.environment.writer.write(f'port command returned code {reply.status_code} with text {reply.text}', is_error=True)
            return None

        return 'external'

    def _pasv_download(self, connection: Connection, client: FtpClient,
                       remote_name, local_name, start_offset=0, mode='I', cmd='retr'):
        set_type_reply = client.execute(f'type {mode}')

        if not set_type_reply.is_success_reply:
            self.environment.writer.write(set_type_reply.text, is_error=True)
            return

        if mode == 'I':
            self._pasv_download_binary(connection, client, remote_name, local_name, start_offset, cmd)
            return

        raise NotImplementedError(f'Downloading at mode {mode} are not supported')

    def _pasv_download_binary(self, connection: Connection, client: FtpClient, remote_name, local_name, start_offset, cmd):
        size = self._get_size(client, remote_name)

        if start_offset != 0:
            self._restore_download(client, connection, local_name, remote_name, size, start_offset, cmd)
            return

        self._download_from_connection(connection, client, remote_name, local_name, 'wb', size, start_offset, cmd)

    def _restore_download(self, client, connection, local_name, remote_name, size, start_offset, cmd):
        if not self._try_rest(client, start_offset):
            self.environment.writer.write('Cant restore downloading', is_error=True)
            return
        if size is not None and start_offset >= size:
            self.environment.writer.write('No any downloading needed', is_error=True)
            return

        self._download_from_connection(connection, client, remote_name, local_name, 'ab', size, start_offset, cmd)

    def _download_from_connection(self, connection: Connection, client: FtpClient,
                                  remote_name, local_name, file_mode, size, offset, cmd):
        def download(a):
            try:
                with connection, open(local_name, mode=file_mode) as file:
                    downloader.download(connection, size,
                                        part_callback=lambda x: file.write(x),
                                        start=offset,
                                        writer=self.environment.writer)
            except IOError as e:
                self.environment.writer.write("io error: {}".format(e.strerror), is_error=True)

        reply = client.execute(f'{cmd} {remote_name}', download)

        self.environment.writer.write(reply.text)

    def _get_size(self, client: FtpClient, filename):
        if client.has_size_command():
            text = client.execute("size {}".format(filename)).text.strip()
            parsed, value = try_parse_int(text)
            if parsed:
                return value
        return None

    def _try_rest(self, client: FtpClient, offset):
        reply = client.execute(f"rest {offset}")
        self.environment.writer.write(reply.text)

        return reply.status_code == StatusCode.REQUESTED_FILE_ACTION_PENDING_INFO.value
