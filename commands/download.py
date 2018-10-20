from infra.command import Command
from infra.environment import Environment, ConnectionMode
from network.downloader import download
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
        size = self._get_size(client)
        filename = self.get_argument('filename')
        entry = self._entry_port(client)

        if entry is None:
            return

        if entry == 'external':
            reply = client.execute(f'retr {filename}', lambda x: print(x.text), timeout=None)
            print(reply.text)
            return

        server = entry

        def download_file(a):
            with server:
                con, addr = server.accept()
                try:
                    with con, open(self._get_outputname(), 'wb') as file:
                        download(con, size, lambda x: file.write(x))
                except IOError as e:
                    print(f'Cant create file: {e.strerror}')

        reply = client.execute(f'retr {filename}', download_file, timeout=None)

        print(reply.text)

    def _execute_passive(self, client):
        size = self._get_size(client)
        address = self._entry_pasv(client)

        if address is None:
            return

        connection = TcpConnection(address, 15)

        def download_file(a):
            with connection:
                try:
                    with open(self._get_outputname(), 'wb') as file:
                        download(connection, size, lambda p: file.write(p))
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
