import unittest

from commands.port import PortCommand
from infra.environment import EnvironmentBuilder, ConnectionMode


class PortCommandUnitTests(unittest.TestCase):
    def test_execute__with_correct_address__should_change_environment_right(self):
        environment = EnvironmentBuilder().build(None, ipv6_mode=True)
        cmd = PortCommand(environment)

        cmd.execute(None)

        self.assertEqual(environment.connection_mode, ConnectionMode.PORT)

