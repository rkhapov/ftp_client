#!/usr/bin/env python3
import unittest

from network.address import Address
from protocol import address_parser


class AddressUnitTests(unittest.TestCase):
    def test_ftp_address__ipv4_address_withoud_high_byte__should_return_right_string(self):
        address = Address('123.123.56.54', 123)

        sut = address.ftp_address

        self.assertEqual(sut, '123,123,56,54,0,123')

    def test_ftp_address__ipv4_address_with_high_byte__should_return_right_string(self):
        address = Address('192.168.1.1', 0xA566)

        sut = address.ftp_address

        self.assertEqual(sut, '192,168,1,1,' + str(0xA5) + ',' + str(0x66))

    def test_ftp_address__ipv4_after_parsing__should_return_origin_address(self):
        origin = Address('192.168.1.1', 45321)
        ftp = origin.ftp_address

        sut = address_parser.parse_address_from_string(ftp)

        self.assertEqual(sut, origin)
