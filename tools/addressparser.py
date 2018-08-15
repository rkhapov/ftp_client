#!/usr/bin/env python3
import re


class AddressParser:
    @staticmethod
    def parse(address: str):
        tokens = re.split('[ \t,]', address)

        if len(tokens) != 6:
            raise ValueError('incorrect format of address')

        return '.'.join(tokens[0:4]), int(tokens[4]) * 256 + int(tokens[5])
