#!/usr/bin/env python3
import enum

from network.tcp import TcpConnection


END_OF_LINE = '\r\n'

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
