#!/usr/bin/env python3

from client.tcpconnection import TcpConnection

END_OF_LINE = '\r\n'


class FtpConnection(TcpConnection):
    def __init__(self, host: str, port: int, logfile: str = None):
        super().__init__(host, port, logfile)

    def send(self, data: str):
        if not data.endswith(END_OF_LINE):
            data += END_OF_LINE

        super().send(data)

    def receive(self, max_length: int = 1024) -> str:
        parts = []

        while True:
            next_line = self.receive_next_line()
            parts.append(next_line)

            if not FtpConnection._is_need_continue(next_line):
                break

        return END_OF_LINE.join(parts)

    def close(self):
        super().close()

    def receive_next_line(self) -> str:
        line = ''

        while not line.endswith(END_OF_LINE):
            next_byte = super().receive(1).decode('utf-8')
            line += next_byte

        return line

    @staticmethod
    def _is_need_continue(line):
        return not FtpConnection._is_first_line_of_answer(line) or \
               FtpConnection._is_multi_line_answer(line) or \
               FtpConnection._is_command_in_process_answer(line)

    @staticmethod
    def _is_command_in_process_answer(line):
        return len(line) >= 1 and line[0] == '1'

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
