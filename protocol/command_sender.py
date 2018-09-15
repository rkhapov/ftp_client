from network.connection import Connection
from protocol.constants import END_OF_LINE


class CommandSender:
    def __init__(self, connection: Connection):
        self.__connection = connection

    @property
    def connection(self):
        return self.__connection

    def send_command(self, cmd: str):
        if not cmd.endswith(END_OF_LINE):
            cmd += END_OF_LINE

        self.__connection.send(cmd.encode())
