import unittest

from network.connection import Connection
from protocol.command_sender import CommandSender


buffer = bytearray()


class FakeConnection(Connection):
    def receive(self, buff_size) -> bytes:
        raise ArithmeticError('receive should not be called')

    def send(self, data: bytes):
        for b in data:
            buffer.append(b)

    @property
    def address(self):
        raise ArithmeticError('address should not be called')

    @property
    def timeout(self):
        raise ArithmeticError('timeout should not be called')


def get_sender():
    buffer.clear()
    return CommandSender(FakeConnection())


class CommandSenderUnitTests(unittest.TestCase):
    def test_send_command__command_are_ended_by_eof__should_send_all_text(self):
        sender = get_sender()

        sender.send_command('cmd arg1 arg2\r\n')

        self.assertEqual(bytes(buffer), b'cmd arg1 arg2\r\n')

    def test_send_command__command_are_not_ended_by_eof__should_add_eof_and_send(self):
        sender = get_sender()

        sender.send_command('cmd arg1 arg2')

        self.assertEqual(bytes(buffer), b'cmd arg1 arg2\r\n')
