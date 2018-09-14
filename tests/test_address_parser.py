import unittest

from network.address import Address
from protocol import address_parser


class AddressParserUnitTests(unittest.TestCase):
    def test_parse_address_from_string__string_are_not_address__returns_none(self):
        addr = address_parser.parse_address_from_string('not an addr lol')

        self.assertIsNone(addr)

    def test_parse_address_from_string__string_are_correct_address__returns_right_address(self):
        addr = address_parser.parse_address_from_string('192,168,1,4,4,6')
        expected = Address('192.168.1.4', 4 * 256 + 6)

        self.assertEqual(addr, expected)

    def test_extract_address_from_text__no_address_in_text__returns_none(self):
        addr = address_parser.extract_address_from_text('lol my text')

        self.assertIsNone(addr)

    def test_extract_address_from_text__there_is_address_in_text_but_without_brackets__should_return_right_address(self):
        addr = address_parser.extract_address_from_text('my text what do you want?? 192,1,1,1,4,6 loool')
        expected = Address('192.1.1.1', 4 * 256 + 6)

        self.assertEqual(addr, expected)

    def test_extract_address_from_text__there_is_address_but_in_brackets__should_return_right_address(self):
        addr = address_parser.extract_address_from_text('my text what do you want?? (192,1,1,1,4,6) loool')
        expected = Address('192.1.1.1', 4 * 256 + 6)

        self.assertEqual(addr, expected)
