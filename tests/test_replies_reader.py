import unittest

from network.connection import Connection
from protocol.replies_reader import RepliesReader
from protocol.reply import Reply


class FakeConnection(Connection):
    def __init__(self, text: str):
        self.__text = text
        self.__pointer = 0

    def receive(self, buff_size):
        if self.__pointer >= len(self.__text):
            raise IndexError('over reading from connection detected')

        data = self.__text[self.__pointer: self.__pointer + buff_size].encode('utf-8')
        self.__pointer += buff_size

        return data

    @property
    def address(self):
        raise ArithmeticError('address should not be called')

    @property
    def timeout(self):
        raise ArithmeticError('timeout should not be called')

    def send(self, data: bytes):
        raise ArithmeticError('send should not be called')


def get_reader(text):
    return RepliesReader(FakeConnection(text))


class RepliesReaderUnitTests(unittest.TestCase):
    def test_read_next_reply__single_line_at_connection__should_return_reply_with_all_text(self):
        reader = get_reader('123 Hello i am your reply!\r\n')
        expected = Reply(123, 'Hello i am your reply!\r\n')

        sut = reader.read_next_reply()

        self.assertEqual(sut, expected)

    def test_read_next_reply__invalid_first_line__should_raise_value_exception(self):
        reader = get_reader('invalid line lol\r\n')

        with self.assertRaises(ValueError):
            reader.read_next_reply()

    def test_read_next_reply__multi_line_data_at_connection__should_return_right_reply(self):
        reader = get_reader('123-First line\r\n' +
                            'Second line\r\n' +
                            ' 234 A line beginning with numbers\r\n' +
                            '123 The last line\r\n')
        expected = Reply(123, 'First line\r\nSecond line\r\n 234 A line beginning with numbers\r\nThe last line\r\n')

        sut = reader.read_next_reply()

        self.assertEqual(sut, expected)

    def test_read_next_reply__multi_line_data_contains_line_with_code__should_return_right_reply(self):
        reader = get_reader('123-First line\r\n' +
                            'Second line\r\n' +
                            '234 A line beginning with numbers\r\n' +
                            '123 The last line\r\n')
        expected = Reply(123, 'First line\r\nSecond line\r\n234 A line beginning with numbers\r\nThe last line\r\n')

        sut = reader.read_next_reply()

        self.assertEqual(sut, expected)
