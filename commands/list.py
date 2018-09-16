from infra.command import Command
from infra.environment import Environment, ConnectionMode
from network.downloader import download_data_from_connection
from network.tcp import TcpConnection
from protocol.ftp import FtpClient
from tools import decoder


class ListCommand(Command):
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
            print(decoder.decode_bytes(download_data_from_connection(connection)))
            connection.close()

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
