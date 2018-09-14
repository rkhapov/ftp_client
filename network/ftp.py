#!/usr/bin/env python3
import enum

from network.tcp import TcpConnection


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

    def __str__(self):
        return self.__body

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


def _is_first_line_of_multi_line_answer(line):
    return len(line) >= 4 and line[3] == '-'


def _is_answer_line(line):
    return len(line) >= 3 and line[0:3].isnumeric()


class FtpConnection:
    def __init__(self, tcp_connection: TcpConnection):
        self.__tcp_connection = tcp_connection
        self.__buffer = []

    @property
    def tcp_connection(self):
        return self.__tcp_connection

    def send_command(self, command: str):
        if not command.endswith(END_OF_LINE):
            command += END_OF_LINE

        self.__tcp_connection.send(bytes(command, 'utf-8'))

    def receive_answer(self) -> FtpAnswer:
        if not self._buffer_is_empty():
            return self.__buffer.pop(0)

        first_line = self._receive_line()

        if not _is_first_line_of_multi_line_answer(first_line):
            return FtpAnswer(first_line)

        return self._receive_multi_line_answer(first_line)

    def receive_all(self) -> [FtpAnswer]:
        answers = []

        while not self._buffer_is_empty():
            answers.append(self.__buffer.pop(0))

        answers.append(self.receive_answer())

        while not self._buffer_is_empty():
            answers.append(self.__buffer.pop(0))

        return answers

    def _receive_multi_line_answer(self, first_line):
        parts = [first_line]
        current_line = self._receive_line()

        while not _is_answer_line(current_line):
            parts.append(current_line)
            current_line = self._receive_line()

        self.__buffer.append(FtpAnswer(current_line))

        return FtpAnswer(END_OF_LINE.join(parts))

    def _receive_line(self):
        line = ''

        while not line.endswith(END_OF_LINE):
            next_byte = self.__tcp_connection.receive(1).decode('utf-8')
            line += next_byte

        return line

    def _buffer_is_empty(self):
        return len(self.__buffer) == 0
