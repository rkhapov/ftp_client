from network.connection import Connection
from protocol.ftp import FtpClient


class FakeClient(FtpClient):
    def __init__(self, connection: Connection):
        super().__init__(connection)

    def execute(self, cmd: str, positive_preliminary_handler=None):
        return super().execute(cmd, positive_preliminary_handler)
