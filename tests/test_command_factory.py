import unittest

from commands.command import *
from commands.command_factory import *


class CommandFactoryTests(unittest.TestCase):
    def test_from_string_unknown_command_should_throw_exception(self):
        cf = CommandFactory()

        self.assertRaises(CommandFactoryError, lambda: cf.from_string('unknown'))

    def test_from_string_invalid_arguments_count_should_throw_exception(self):
        cf = CommandFactory()

        self.assertRaises(CommandFactoryError, lambda: cf.from_string('help help help'))

    def test_from_string_empty_input_should_throw_exception(self):
        cf = CommandFactory()

        self.assertRaises(CommandFactoryError, lambda: cf.from_string('             '))

    def test_from_string_quit_command_should_return_quit_command(self):
        cf = CommandFactory()

        sut = cf.from_string('quit')

        self.assertTrue(isinstance(sut, Quit))

    def test_from_string_cd_command_should_return_change_directory_command(self):
        cf = CommandFactory()

        sut = cf.from_string('cd ..')

        self.assertTrue(isinstance(sut, ChangeDirectory))
        self.assertListEqual(sut.args, ['..'])

    def test_from_string_upload_command_should_return_upload_command(self):
        cf = CommandFactory()

        sut = cf.from_string('upload from')

        self.assertTrue(isinstance(sut, Upload))
        self.assertListEqual(sut.args, ['from'])

    def test_from_string_download_command_should_return_download_command(self):
        cf = CommandFactory()

        sut = cf.from_string('download from to')

        self.assertTrue(isinstance(sut, Download))
        self.assertListEqual(sut.args, ['from', 'to'])

    def test_from_string_rename_command_should_return_rename_command(self):
        cf = CommandFactory()

        sut = cf.from_string('rename from to')

        self.assertTrue(isinstance(sut, Rename))
        self.assertListEqual(sut.args, ['from', 'to'])

    def test_from_string_remove_command_should_return_rename_command(self):
        cf = CommandFactory()

        sut = cf.from_string('remove from')

        self.assertTrue(isinstance(sut, Remove))
        self.assertListEqual(sut.args, ['from'])

    def test_from_string_mkdir_command_should_return_make_directory_command(self):
        cf = CommandFactory()

        sut = cf.from_string('mkdir dir')

        self.assertTrue(isinstance(sut, MakeDirectory))
        self.assertListEqual(sut.args, ['dir'])

    def test_from_string_help_command_should_return_help_command(self):
        cf = CommandFactory()

        sut = cf.from_string('help')

        self.assertTrue(isinstance(sut, Help))
        self.assertListEqual(sut.args, [])

    def test_from_string_clear_command_should_return_clear_command(self):
        cf = CommandFactory()

        sut = cf.from_string('clear')

        self.assertTrue(isinstance(sut, Clear))
        self.assertListEqual(sut.args, [])

    def test_from_string_ls_command_should_return_ls_command(self):
        cf = CommandFactory()

        sut = cf.from_string('ls')

        self.assertTrue(isinstance(sut, List))
        self.assertListEqual(sut.args, [])

    def test_from_string_chelp_command_should_return_chelp_command(self):
        cf = CommandFactory()

        sut = cf.from_string('chelp help')

        self.assertTrue(isinstance(sut, CommandHelp))
        self.assertListEqual(sut.args, ['help'])

    def test_from_string_many_space_symbols_should_ignore_it(self):
        cf = CommandFactory()

        sut = cf.from_string('      help            ')

        self.assertTrue(isinstance(sut, Help))
        self.assertListEqual(sut.args, [])
