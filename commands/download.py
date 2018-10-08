from infra.command import Command
from infra.environment import Environment, ConnectionMode
from network.downloader import download_data_from_connection
from network.tcp import TcpConnection
from protocol.ftp import FtpClient
from tools.parse_helpers import try_parse_int


class DownloadCommand(Command):
    def __init__(self, environment: Environment):
        super().__init__(environment)

    def execute(self, client: FtpClient):
        if self.environment.connection_mode == ConnectionMode.PASSIVE:
            self._execute_passive(client)
        else:
            raise NotImplementedError

    @staticmethod
    def help():
        return 'download file <filename> to <outfilename>, if there is not <outfilename>, <filename> are used'

    @staticmethod
    def name():
        return 'download'

    @staticmethod
    def format():
        return 'download filename $outfilename'

    def _execute_passive(self, client):
        size = self._get_size(client)
        address = self._entry_pasv(client)

        if address is None:
            return

        connection = TcpConnection(address, 15)

        def download_file(a):
            with connection:
                try:
                    outname = self._get_outputname()
                    with open(outname, 'wb') as file:
                        data = download_data_from_connection(connection, size)
                        file.write(data)
                except IOError as error:
                    print('Cant create output file: {}'.format(error.strerror))

        reply = client.execute('retr {}'.format(self.get_argument('filename')), download_file)

        print(reply.text)

    def _get_size(self, client: FtpClient):
        if client.has_size_command():
            text = client.execute("size {}".format(self.get_argument('filename'))).text.strip()
            parsed, value = try_parse_int(text)
            if parsed:
                return value
        return None

    def _get_outputname(self):
        return self.get_argument('outfilename') if self.has_argument('outfilename') else self.get_argument('filename')
