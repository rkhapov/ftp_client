import unittest

from commands.pasv import PasvCommand
from infra.environment import EnvironmentBuilder, ConnectionMode


class PasvCommandUnitTests(unittest.TestCase):
    def test_execute__should_set_connection_mode_to_passive(self):
        environment = EnvironmentBuilder().build(None)
        environment.connection_mode = ConnectionMode.PORT
        cmd = PasvCommand(environment)

        cmd.execute(None)

        self.assertEqual(environment.connection_mode, ConnectionMode.PASSIVE)
