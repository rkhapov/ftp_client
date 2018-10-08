from infra.command import Command
from infra.environment import Environment, ConnectionMode
from network import uploader
from network.tcp import TcpConnection
from protocol.ftp import FtpClient


class UploadCommand(Command):
    def __init__(self, environment: Environment):
        super().__init__(environment)

    def execute(self, client: FtpClient):
        if self.environment.connection_mode == ConnectionMode.PASSIVE:
            self._upload_passive(client)
        else:
            raise NotImplementedError

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
            print('Cant open file {}'.format(self.get_argument('filename')))
            return None

    def _get_out_file_name(self):
        if self.has_argument('outfilename'):
            return self.get_argument('outfilename')
        return self.get_argument('filename')

    def _upload_passive(self, client: FtpClient):
        data = self._get_data_to_upload()
        out_file_name = self._get_out_file_name()

        if data is None:
            return

        address = self._entry_pasv(client)

        if address is None:
            return

        with TcpConnection(address, 15) as connection:
            def upload_file(a):
                uploader.upload_data_at_connection(connection, data)

            reply = client.execute("STOR {}".format(out_file_name), upload_file)

        print(reply.text)
