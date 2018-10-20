from infra.command import Command
from infra.environment import Environment, ConnectionMode
from network.downloader import download
from network.tcp import TcpConnection
from protocol.ftp import FtpClient
from tools import decoder


class ShortListCommand(Command):
    def __init__(self, environment: Environment):
        super().__init__(environment)

    def execute(self, client: FtpClient):

        if self.environment.connection_mode == ConnectionMode.PASSIVE:
            self._execute_passive(client)
        else:
            raise NotImplementedError

    def _execute_passive(self, client):
        address = self._entry_pasv(client)

        if address is None:
            return

        connection = TcpConnection(address, 15)

        def download_list(a):
            with connection:
                print(' '.join(decoder.decode_bytes(download(connection)).split()))

        reply = client.execute('nlst', download_list)

        print(reply.text)

    @staticmethod
    def help():
        return 'print directory content in short format'

    @staticmethod
    def name():
        return 'sls'

    @staticmethod
    def format():
        return 'sls $dir'
