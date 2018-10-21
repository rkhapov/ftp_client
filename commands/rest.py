from infra.command import Command
from infra.environment import Environment, ConnectionMode
from network.downloader import download
from network.tcp import TcpConnection
from protocol.ftp import FtpClient
from protocol.status import StatusCode
from tools.parse_helpers import try_parse_int


class RestCommand(Command):
    def __init__(self, environment: Environment):
        super().__init__(environment)

    def execute(self, client: FtpClient):
        r = client.execute('type i')

        if not r.is_success_reply:
            print(r.text)
            return

        if self.environment.connection_mode == ConnectionMode.PASSIVE:
            self._execute_passive(client)
        else:
            self._execute_port(client)

    @staticmethod
    def help():
        return 'restore downloading file <filename> to <outfilename>, if there is not <outfilename>, <filename> are used'

    @staticmethod
    def name():
        return 'restore'

    @staticmethod
    def format():
        return 'restore filename $outfilename'

    def _execute_port(self, client):
        offset = self._get_offset()

        if offset is None:
            print('Cant get offset to download')
            return

        size = self._get_size(client)

        if offset >= size:
            print('No downloading needed')
            return

        filename = self.get_argument('filename')
        entry = self._entry_port(client)

        if entry is None:
            return

        if not self._try_rest(client, offset):
            print('Cant restore download')
            return

        if entry == 'external':
            reply = client.execute(f'retr {filename}', lambda x: print(x.text), timeout=None)
            print(reply.text)
            return

        server = entry

        def download_file(a):
            with server:
                con = server.accept()
                try:
                    with con, open(self._get_outputname(), 'wb+') as file:
                        download(con, size, lambda x: file.write(x))
                except IOError as e:
                    print(f'Cant create file: {e.strerror}')

        reply = client.execute(f'retr {filename}', download_file, timeout=None)

        print(reply.text)

    def _execute_passive(self, client):
        address = self._entry_pasv(client)
        offset = self._get_offset()

        if address is None:
            return

        if offset is None:
            print('Cant get offset')
            return

        connection = TcpConnection(address, 15)

        self._pasv_download(connection, client, self.get_argument('filename'), self._get_outputname(), offset)

    def _get_offset(self):
        try:
            import os
            return os.path.getsize(self._get_outputname())
        except:
            return None

    def _get_outputname(self):
        return self.get_argument('outfilename') if self.has_argument('outfilename') else self.get_argument('filename')
