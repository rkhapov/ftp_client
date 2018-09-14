from network.tcp import TcpConnection
from protocol.replies_reader import RepliesReader


class FtpRequest:
    pass


class FtpResponse:
    pass


class FtpClient:
    def __init__(self, tcp_connection: TcpConnection):
        self.__tcp_connection = tcp_connection
        self.__replies_reader = RepliesReader(self.__tcp_connection)

    @property
    def tcp_connection(self):
        return self.__tcp_connection

    @property
    def replies_reader(self):
        return self.__replies_reader

    def execute(self, request: FtpRequest) -> FtpResponse:
        pass
