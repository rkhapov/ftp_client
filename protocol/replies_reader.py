from network.connection import Connection
from protocol.reply import Reply
from tools.parse_helpers import try_parse_int

END_OF_LINE = '\r\n'
READ_BLOCK_SIZE = 1


class RepliesReader:
    def __init__(self, connection: Connection):
        self.__connection = connection

    @property
    def connection(self):
        return self.__connection

    def read_next_reply(self) -> Reply:
        code, is_multi, text, all_text = self._read_next_line()

        if code is None:
            raise ValueError('Unexpected data at connection for the first line: {}'.format(text))

        if not is_multi:
            return Reply(code, text)

        return self._read_to_line_with_code(code, text)

    def _read_to_line_with_code(self, expected_code, first_line_text):
        lines = [first_line_text]

        while True:
            code, is_multi, text, all_text = self._read_next_line()

            if code == expected_code:
                lines.append(text)
                break
            lines.append(all_text)

        return Reply(expected_code, ''.join(lines))

    def _read_next_line(self):
        line = self._read_to_end_of_line()

        have_code, code = try_parse_int(line[0:3])

        if have_code:
            is_multi = line[3] == '-' if len(line) >= 4 else False
            text = line[4:]

            return code, is_multi, text, line

        return None, None, line, line

    def _read_to_end_of_line(self) -> str:
        line = ''

        while not line.endswith(END_OF_LINE):
            line += self.__connection.receive(READ_BLOCK_SIZE).decode()

        return line
