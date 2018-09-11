#!/usr/bin/env python3
import enum

from network.tcp import TcpClient


END_OF_LINE = '\r\n'


class StatusCodePrefix(enum.Enum):
    IN_PROGRESS = 1
    SUCCESS = 2
    NEED_MORE_COMMAND = 3
    CANT_ACCEPT_NOW = 4
    FAILED = 5


class FtpAnswer:
    def __init__(self, body: str):
        self.__body = body

    @property
    def body(self):
        return self.__body

    @property
    def status_code(self):
        if self._body_has_code():
            return int(self.__body[0:3])

        raise ValueError('body doesnt contains status code')

    @property
    def is_multi_line_answer(self):
        return len(self.__body) >= 4 and self.__body[3] == '-'

    @property
    def is_in_progress_answer(self):
        return str(self.status_code).startswith(str(StatusCodePrefix.IN_PROGRESS))

    @property
    def is_success_answer(self):
        return str(self.status_code).startswith(str(StatusCodePrefix.SUCCESS))

    @property
    def is_need_more_command_answer(self):
        return str(self.status_code).startswith(str(StatusCodePrefix.NEED_MORE_COMMAND))

    @property
    def is_cant_accept_now_answer(self):
        return str(self.status_code).startswith(str(StatusCodePrefix.CANT_ACCEPT_NOW))

    @property
    def is_failed_answer(self):
        return str(self.status_code).startswith(str(StatusCodePrefix.FAILED))

    def _body_has_code(self):
        return len(self.__body) >= 3 and self.__body[0:3].isnumeric()


class FtpClient:
    def __init__(self, tcp_client: TcpClient):
        self.__tcp_client = tcp_client

    @property
    def tcp_client(self):
        return self.__tcp_client

    def send_command(self, command: str):
        if not command.endswith(END_OF_LINE):
            command += END_OF_LINE

        self.__tcp_client.send(bytes(command))

    def receive_answer(self) -> FtpAnswer:
        raise NotImplemented

    def receive_all(self) -> [FtpAnswer]:
        raise NotImplemented

    def _receive_line(self):
        line = ''

        while not line.endswith(END_OF_LINE):
            next_byte = self.__tcp_client.receive(1).decode('utf-8')
            line += next_byte

        return line
    
    def _is_multi_line_answer
