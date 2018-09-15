import unittest

from commands.port import PortCommand
from infra.environment import EnvironmentBuilder, ConnectionMode


class PortCommandUnitTests(unittest.TestCase):
    def test_execute__with_correct_address__should_change_environment_right(self):
        environment = EnvironmentBuilder().build()
        cmd = PortCommand(environment)
        cmd.add_argument('address', '192,168,1,1,6,7')

        cmd.execute(None)

        self.assertEqual(environment.connection_mode, ConnectionMode.PORT)
        self.assertEqual(environment.port_address, '192,168,1,1,6,7')

    def test_execute__with_incorrect_address__should_raise_value_error(self):
        environment = EnvironmentBuilder().build()
        cmd = PortCommand(environment)
        cmd.add_argument('address', 'not_an_address_lol')

        with self.assertRaises(ValueError):
            cmd.execute(None)
