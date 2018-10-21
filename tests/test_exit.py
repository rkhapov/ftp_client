import unittest

from commands.exit import ExitCommand
from infra.environment import EnvironmentBuilder
from tests.fake_client import FakeClient
from tests.fake_connection import FakeConnection


class ExitCommandUnitTests(unittest.TestCase):
    def test_execute__set_closed_at_environment(self):
        environment = EnvironmentBuilder().build(None, ipv6_mode=False)
        cmd = ExitCommand(environment)

        cmd.execute(FakeClient(FakeConnection('lol', '200 Goodbay\r\n', -1)))

        self.assertEqual(environment.closed, True)
