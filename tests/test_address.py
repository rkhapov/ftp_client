#!/usr/bin/env python3
import unittest

from network.address import Address


class AddressUnitTests(unittest.TestCase):
    def test_ftp_address__ipv4_address_withoud_high_byte__should_return_right_string(self):
        address = Address('123.123.56.54', 123)

        sut = address.ftp_address

        self.assertEqual(sut, '123,123,56,54,0,123')

    def test_ftp_address__ipv4_address_with_high_byte__should_return_right_string(self):
        address = Address('192.168.1.1', 0xA566)

        sut = address.ftp_address

        self.assertEqual(sut, '192,168,1,1,' + str(0xA5) + ',' + str(0x66))
