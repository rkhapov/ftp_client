import unittest

from commands.exit import ExitCommand
from infra.environment import EnvironmentBuilder


class ExitCommandUnitTests(unittest.TestCase):
    def test_execute__set_closed_at_environment(self):
        environment = EnvironmentBuilder().build()
        cmd = ExitCommand(environment)

        cmd.execute(None)

        self.assertEqual(environment.closed, True)
