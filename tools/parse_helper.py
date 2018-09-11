#!/usr/bin/env python3

import re


_address_regexp = re.compile('\(\d{1,3},\d{1,3},\d{1,3},\d{1,3},\d{1,3},\d{1,3}\)', re.M)
_size_regexp = re.compile('\d+ bytes')


def parse_address_from_string(address: str):
    tokens = re.split('[ \t,]', address)
    if len(tokens) != 6:
        return None
    return '.'.join(tokens[0:4]), int(tokens[4]) * 256 + int(tokens[5])


def extract_address_from_text(text: str) -> [str, None]:
    result = _address_regexp.search(text)

    if result is not None:
        address = result.group(0)
        trimed = address[1:len(address) - 1]
        return parse_address_from_string(trimed)

    return


def extract_size_from_text(text: str):
    result = _size_regexp.search(text)

    if result is not None:
        size = result.group(0)
        return int(size.split(' ')[0])

    return None
