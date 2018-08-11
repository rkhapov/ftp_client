#!/usr/bin/env python3

from client.tcpconnection import TcpConnection, Connection

END_OF_LINE = '\r\n'


class FtpConnection(Connection):
    def __init__(self, host: str, port: int, logfile: str = None):
        self._tcp_connection = TcpConnection(host, port, logfile)

    def send(self, data: str):
        if not data.endswith(END_OF_LINE):
            data += END_OF_LINE

        self._tcp_connection.send(data)

    def receive(self, max_length: int = 1024):
        parts = []

        while True:
            parts.append(self._receive_next_line())
            last = parts[len(parts) - 1]

            if not FtpConnection._is_need_continue(last):
                break

        return END_OF_LINE.join(parts)

    def close(self):
        self._tcp_connection.close()

    def _receive_next_line(self) -> str:
        line = ''

        while not line.endswith(END_OF_LINE):
            line += self._tcp_connection.receive(1)

        return line

    @staticmethod
    def _is_need_continue(line):
        return not FtpConnection._is_first_line_of_answer(line) or\
               FtpConnection._is_multi_line_answer(line)

    @staticmethod
    def _is_multi_line_answer(line: str):
        return FtpConnection._is_first_line_of_answer(line) and len(line) >= 3 and line[3] == '-'

    @staticmethod
    def _is_first_line_of_answer(line: str) -> bool:
        if len(line) < 3:
            return False

        for i in range(3):
            if not line[i].isnumeric():
                return False

        return True
