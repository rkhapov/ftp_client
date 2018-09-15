import unittest

from commands import *


class EnvironmentBuilderUnitTests(unittest.TestCase):
    def test_build__returns_right_initial_environment(self):
        from infra.environment import EnvironmentBuilder, ConnectionMode
        builder = EnvironmentBuilder()

        sut = builder.build()

        self.assertEqual(sut.connection_mode, ConnectionMode.PASSIVE)
        self.assertEqual(sut.port_address, '')
