from network.connection import Connection
from protocol.command_sender import CommandSender
from protocol.replies_reader import RepliesReader
from protocol.reply import Reply
from protocol.status import is_positive_preliminary_code, StatusCode


class FtpClient:
    def __init__(self, connection: Connection):
        self.__replies_reader = RepliesReader(connection)
        self.__command_sender = CommandSender(connection)

    def start(self) -> Reply:
        return self.__replies_reader.read_next_reply()

    @property
    def connection(self):
        return self.__replies_reader.connection

    @property
    def replies_reader(self):
        return self.__replies_reader

    @property
    def command_sender(self):
        return self.__command_sender

    def execute(self, cmd: str, positive_preliminary_handler=None, timeout=-1) -> Reply:
        timeout_backup = self.connection.timeout
        if timeout != -1:
            self.connection.timeout = timeout

        self.__command_sender.send_command(cmd)

        reply = self.__replies_reader.read_next_reply()

        if not is_positive_preliminary_code(reply.status_code):
            self.connection.timeout = timeout_backup
            return reply

        if positive_preliminary_handler is None:
            self.connection.timeout = timeout_backup
            raise ValueError('positive preliminary handler are None, but reply with code {} are received'
                             .format(reply.status_code))
        positive_preliminary_handler(reply)

        end_reply = self.__replies_reader.read_next_reply()

        self.connection.timeout = timeout_backup
        return end_reply

    def has_size_command(self):
        return self.execute('size myfile').status_code != StatusCode.COMMAND_UNRECOGNIZED.value
