import unittest

from network.address import Address, IPv4Address
from protocol import address_parser


class AddressParserUnitTests(unittest.TestCase):
    def test_parse_address_from_string__string_are_not_address__returns_none(self):
        addr = address_parser.parse_address_from_string('not an addr lol')

        self.assertIsNone(addr)

    def test_parse_address_from_string__string_are_correct_address__returns_right_address(self):
        addr = address_parser.parse_address_from_string('192,168,1,4,4,6')
        expected = IPv4Address('192.168.1.4', 4 * 256 + 6)

        self.assertEqual(addr, expected)

    def test_extract_address_from_text__no_address_in_text__returns_none(self):
        addr = address_parser.extract_address_from_text('lol my text')

        self.assertIsNone(addr)

    def test_extract_address_from_text__there_is_address_in_text_but_without_brackets__should_return_right_address(self):
        addr = address_parser.extract_address_from_text('my text what do you want?? 192,1,1,1,4,6 loool')
        expected = IPv4Address('192.1.1.1', 4 * 256 + 6)

        self.assertEqual(addr, expected)

    def test_extract_address_from_text__there_is_address_but_in_brackets__should_return_right_address(self):
        addr = address_parser.extract_address_from_text('my text what do you want?? (192,1,1,1,4,6) loool')
        expected = IPv4Address('192.1.1.1', 4 * 256 + 6)

        self.assertEqual(addr, expected)

    def test_parse_address_from_string_6__string_are_not_valid_address__should_return_none(self):
        port = address_parser.parse_address_from_string_6('sdf fgdfgd not a valid 6')

        self.assertIsNone(port)

    def test_parse_address_from_string_6__string_are_valid_address__should_return_right_port(self):
        port = address_parser.parse_address_from_string_6("|||34234|")

        self.assertEqual(port, 34234)

    def test_extract_address_from_text__no_address__should_return_none(self):
        port = address_parser.extract_address_from_text_6('(sdafadfasdF)s dfasdf asdf sfad ')

        self.assertIsNone(port)

    def test_extract_address_from_text__string_contains_only_address__should_return_right_port(self):
        port = address_parser.extract_address_from_text_6("|||123123|")

        self.assertEqual(port, 123123)

    def test_extract_address_from_text__string_contains_not_only_adress__should_return_right_port(self):
        port = address_parser.extract_address_from_text_6("Entering passive mode (|||1234|)")

        self.assertEqual(port, 1234)
