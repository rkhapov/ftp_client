from infra.command import Command
from infra.environment import Environment, ConnectionMode
from network.downloader import download
from network.tcp import TcpConnection
from protocol.ftp import FtpClient


class DownloadCommand(Command):
    def __init__(self, environment: Environment):
        super().__init__(environment)

    def execute(self, client: FtpClient):
        if self.environment.connection_mode == ConnectionMode.PASSIVE:
            self._execute_passive(client)
        else:
            self._execute_port(client)

    @staticmethod
    def help():
        return 'download file <filename> to <outfilename>, if there is not <outfilename>, <filename> are used'

    @staticmethod
    def name():
        return 'download'

    @staticmethod
    def format():
        return 'download filename $outfilename'

    def _execute_port(self, client):
        filename = self.get_argument('filename')
        size = self._get_size(client, filename)
        entry = self._entry_port(client)

        if entry is None:
            return

        if entry == 'external':
            reply = client.execute(f'retr {filename}', lambda x: print(x.text))
            self.environment.writer.write(reply.text)
            return

        def download_file(a):
            with entry as server:
                con = server.accept()
                try:
                    with con, open(self._get_outputname(), 'wb') as file:
                        download(con, size, lambda x: file.write(x), writer=self.environment.writer)
                except IOError as e:
                    self.environment.writer.write(f'Cant create file: {e.strerror}', is_error=True)

        reply = client.execute(f'retr {filename}', download_file)

        self.environment.writer.write(reply.text)

    def _execute_passive(self, client):
        address = self._entry_pasv(client)

        if address is None:
            return

        connection = TcpConnection(address, 15)

        self._pasv_download(connection, client, self.get_argument('filename'), self._get_outputname(), cmd='retr')

    def _get_outputname(self):
        return self.get_argument('outfilename') if self.has_argument('outfilename') else self.get_argument('filename')
