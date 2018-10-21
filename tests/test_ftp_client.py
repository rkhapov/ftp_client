import unittest

from network.address import IPv4Address
from network.connection import Connection
from protocol.ftp import FtpClient
from protocol.reply import Reply

send_buffer = bytearray()


class FakeConnection(Connection):
    def close(self):
        pass

    @property
    def peer_address(self):
        return IPv4Address('127.0.0.1', 1337)

    def __init__(self, text: str):
        self.__text = text
        self.__pointer = 0

    def receive(self, buff_size) -> bytes:
        if self.__pointer >= len(self.__text):
            raise IndexError('over reading from connection detected')

        data = self.__text[self.__pointer: self.__pointer + buff_size].encode('utf-8')
        self.__pointer += buff_size

        return data

    def send(self, data: bytes):
        for b in data:
            send_buffer.append(b)

    @property
    def address(self):
        raise ArithmeticError('address was called')

    @property
    def timeout(self):
        return 5

    @timeout.setter
    def timeout(self, v):
        pass


def get_client(text):
    send_buffer.clear()
    return FtpClient(FakeConnection(text))


class FtpClientUnitTests(unittest.TestCase):
    def test_execute__simple_command_with_no_preliminary__should_send_and_receive_right_text(self):
        client = get_client("200 OK\r\n")
        expected_reply = Reply(200, "OK\r\n")

        sut = client.execute("size lol")

        self.assertEqual(send_buffer, b'size lol\r\n')
        self.assertEqual(sut, expected_reply)

    def test_execute__reply_with_preliminary_but_handler_not_specified__should_raise_value_exception(self):
        client = get_client("123 OK\r\n200 OK\r\n")

        with self.assertRaises(ValueError):
            client.execute("cmd")

    def test_execute__reply_contains_preliminary__should_call_handler_with_it(self):
        client = get_client("123 preliminary text\r\n200 OK\r\n")
        called = False
        def handler(reply):
            nonlocal called
            called = True
            self.assertEqual(reply, Reply(123, "preliminary text\r\n"))

        client.execute("cmd", handler)

        self.assertTrue(called)

    def test_execute__reply_contains_preliminary__should_return_reply_after_preliminary(self):
        client = get_client("123 preliminary text\r\n200 OK\r\n")
        expeted_reply = Reply(200, "OK\r\n")

        sut = client.execute("cmd", lambda x: x)

        self.assertEqual(sut, expeted_reply)
