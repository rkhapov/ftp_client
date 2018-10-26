from infra.command import Command
from infra.environment import Environment, ConnectionMode
from network import uploader
from network.tcp import TcpConnection
from protocol.ftp import FtpClient


class UploadCommand(Command):
    def __init__(self, environment: Environment):
        super().__init__(environment)

    def execute(self, client: FtpClient):
        r = client.execute('type i')

        if not r.is_success_reply:
            self.environment.writer.write(r.text, is_error=True)
            return

        if self.environment.connection_mode == ConnectionMode.PASSIVE:
            self._upload_passive(client)
        else:
            self._upload_port(client)

    @staticmethod
    def help():
        return 'upload filename as outfilename, if there is no outfilename, filename are used'

    @staticmethod
    def name():
        return 'upload'

    @staticmethod
    def format():
        return 'upload filename $outfilename'

    def _get_data_to_upload(self):
        try:
            with open(self.get_argument('filename'), 'rb') as file:
                return file.read()
        except:
            self.environment.writer.write('Cant open file {}'.format(self.get_argument('filename')), is_error=True)
            return None

    def _get_out_file_name(self):
        if self.has_argument('outfilename'):
            return self.get_argument('outfilename')
        return self.get_argument('filename')

    def _upload_port(self, client: FtpClient):
        data = self._get_data_to_upload()
        out_file_name = self._get_out_file_name()

        if data is None:
            return

        address = self._entry_port(client)

        if address is None:
            return

        if address == 'external':
            reply = client.execute(f'stor {out_file_name}', lambda x: self.environment.writer.write(x.text), timeout=None)
            self.environment.writer.write(reply.text)
            return

        server = address

        def upload(a):
            with server, server.accept() as con:
                uploader.upload(con, data, writer=self.environment.writer)

        reply = client.execute(f'stor {out_file_name}', upload, timeout=None)
        self.environment.writer.write(reply.text)

    def _upload_passive(self, client: FtpClient):
        data = self._get_data_to_upload()
        out_file_name = self._get_out_file_name()

        if data is None:
            return

        address = self._entry_pasv(client)

        if address is None:
            return

        connection = TcpConnection(address, 15)

        def upload_file(a):
            with connection:
                uploader.upload(connection, data, writer=self.environment.writer)

        reply = client.execute("STOR {}".format(out_file_name), upload_file)

        self.environment.writer.write(reply.text)
