import unittest

from commands.cd import CdCommand
from commands.download import DownloadCommand
from commands.help import HelpCommand
from commands.list import ListCommand
from commands.login import LoginCommand
from commands.pasv import PasvCommand
from commands.port import PortCommand
from commands.pwd import PwdCommand
from commands.upload import UploadCommand
from infra.environment import EnvironmentBuilder
from infra.factory import CommandFactory


class CommandFactoryUnitTests(unittest.TestCase):
    def setUp(self):
        self.factory = CommandFactory()
        self.environment = EnvironmentBuilder().build(self.factory.commands)

    def test_from_string__no_any_tokens__should_raise_value_exception(self):
        with self.assertRaises(ValueError):
            self.factory.from_string('  \t  ', self.environment)

    def test_from_string__unexisting_command__should_raise_value_exception(self):
        with self.assertRaises(ValueError):
            self.factory.from_string('my_command my_argument', self.environment)

    def test_from_string__cd_command_without_arguments__should_raise_value_error(self):
        with self.assertRaises(ValueError):
            self.factory.from_string('cd', self.environment)

    def test_from_string__valid_cd_command__should_return_right_command(self):
        sut = self.factory.from_string('cd ..', self.environment)

        self.assertIsInstance(sut, CdCommand)
        self.assertEqual(sut.arguments, {'directory': '..'})

    def test_from_string__download_without_parameters__should_raise_value_error(self):
        with self.assertRaises(ValueError):
            self.factory.from_string('download', self.environment)

    def test_from_string__download_with_one_argument__should_return_right_command(self):
        sut = self.factory.from_string('download file.txt', self.environment)

        self.assertIsInstance(sut, DownloadCommand)
        self.assertEqual(sut.arguments, {'filename': 'file.txt'})

    def test_from_string__download_with_two_arguments__should_return_right_command(self):
        sut = self.factory.from_string('download file.txt outfile.txt', self.environment)

        self.assertIsInstance(sut, DownloadCommand)
        self.assertEqual(sut.arguments, {'filename': 'file.txt', 'outfilename': 'outfile.txt'})

    def test_from_string__help_command_withoud_args__should_return_right_command(self):
        sut = self.factory.from_string('help', self.environment)

        self.assertIsInstance(sut, HelpCommand)
        self.assertEqual(sut.arguments, {})

    def test_from_string__help_command_with_arg__should_return_right_command(self):
        sut = self.factory.from_string('help cmd', self.environment)

        self.assertIsInstance(sut, HelpCommand)
        self.assertEqual(sut.arguments, {'command': 'cmd'})

    def test_from_string__ls_command_without_args__should_return_right_command(self):
        sut = self.factory.from_string('ls', self.environment)

        self.assertIsInstance(sut, ListCommand)
        self.assertEqual(sut.arguments, {})

    def test_from_string__ls_command_with_one_arg__should_return_right_command(self):
        sut = self.factory.from_string('ls directory', self.environment)

        self.assertIsInstance(sut, ListCommand)
        self.assertEqual(sut.arguments, {'dir': 'directory'})

    def test_from_string__login_command_without_args__should_return_right_command(self):
        sut = self.factory.from_string('login', self.environment)

        self.assertIsInstance(sut, LoginCommand)
        self.assertEqual(sut.arguments, {})

    def test_from_string__login_command_with_only_user_arg__should_return_right_command(self):
        sut = self.factory.from_string('login myuser', self.environment)

        self.assertIsInstance(sut, LoginCommand)
        self.assertEqual(sut.arguments, {'user': 'myuser'})

    def test_from_string__login_command_with_user_and_pass__should_return_right_command(self):
        sut = self.factory.from_string('login myuser pass', self.environment)

        self.assertIsInstance(sut, LoginCommand)
        self.assertEqual(sut.arguments, {'user': 'myuser', 'password': 'pass'})

    def test_from_string__pasv_command__should_return_right_command(self):
        sut = self.factory.from_string('pasv', self.environment)

        self.assertIsInstance(sut, PasvCommand)
        self.assertEqual(sut.arguments, {})

    def test_from_string__port_command_without_address__should_raise_value_exception(self):
        with self.assertRaises(ValueError):
            self.factory.from_string('port  ', self.environment)

    def test_from_string__port_command__should_return_right_command(self):
        sut = self.factory.from_string('port 197,123,14,1,2,4', self.environment)

        self.assertIsInstance(sut, PortCommand)
        self.assertEqual(sut.arguments, {'address': '197,123,14,1,2,4'})

    def test_from_string__pwd_command__should_return_right_command(self):
        sut = self.factory.from_string('pwd', self.environment)

        self.assertIsInstance(sut, PwdCommand)
        self.assertEqual(sut.arguments, {})

    def test_from_string__upload_without_args__should_raise_value_error(self):
        with self.assertRaises(ValueError):
            self.factory.from_string('upload', self.environment)

    def test_from_string__upload_command_with_one_arg__should_return_right_command(self):
        sut = self.factory.from_string('upload file.txt', self.environment)

        self.assertIsInstance(sut, UploadCommand)
        self.assertEqual(sut.arguments, {'filename': 'file.txt'})

    def test_from_string__upload_command_with_two_args__should_return_right_command(self):
        sut = self.factory.from_string('upload file.txt outfile.txt', self.environment)

        self.assertIsInstance(sut, UploadCommand)
        self.assertEqual(sut.arguments, {'filename': 'file.txt', 'outfilename': 'outfile.txt'})











