from infra.command import Command
from infra.environment import Environment
from network.downloader import download
from network.tcp import TcpConnection
from protocol.ftp import FtpClient
from tools import decoder


class ListCommand(Command):
    def __init__(self, environment: Environment):
        super().__init__(environment)

    def execute(self, client: FtpClient):
        # executing always in passive mode
        # because there is no obvious reason to do it in port mode
        self._execute_passive(client)

    def _execute_passive(self, client):
        address = self._entry_pasv(client)

        if address is None:
            return

        connection = TcpConnection(address, 15, ipv6_mode=self.environment.is_ipv6_mode)

        def download_list(a):
            with connection:
                print(decoder.decode_bytes(download(connection)))

        reply = client.execute('list', download_list)

        print(reply.text)

    @staticmethod
    def help():
        return 'print directory content'

    @staticmethod
    def name():
        return 'ls'

    @staticmethod
    def format():
        return 'ls $dir'
