import unittest

from tools.addressparser import AddressParser


class AddressParserTests(unittest.TestCase):
    def test_parse_returns_tuple_of_size2(self):
        sut = AddressParser.parse('192,168,78,14,65,32')

        self.assertIsInstance(sut, tuple)
        self.assertEqual(len(sut), 2)

    def test_parse_input_string_are_not_valid_raise_value_exception(self):
        with self.assertRaises(ValueError):
            AddressParser.parse('lol')

    def test_parse_input_string_are_correct_should_return_right_address(self):
        sut = AddressParser.parse('192,168,78,14,65,32')

        self.assertTupleEqual(sut, ('192.168.78.14', 65 * 256 + 32))
