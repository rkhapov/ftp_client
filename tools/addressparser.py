#!/usr/bin/env python3
import re

_address_regexp = re.compile('\(\d{1,3},\d{1,3},\d{1,3},\d{1,3},\d{1,3},\d{1,3}\)', re.M)


class AddressParser:
    @staticmethod
    def parse(address: str):
        tokens = re.split('[ \t,]', address)

        if len(tokens) != 6:
            raise ValueError('incorrect format of address')

        return '.'.join(tokens[0:4]), int(tokens[4]) * 256 + int(tokens[5])

    @staticmethod
    def extract_address_from_text(text: str) -> [str, None]:
        result = _address_regexp.search(text)

        if result is not None:
            addr = result.group(0)
            return addr[1:len(addr) - 1]

        return
