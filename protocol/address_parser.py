import re

from network.address import IPv4Address
from tools import parse_helpers

_address_regexp_4 = re.compile('\d{1,3},\d{1,3},\d{1,3},\d{1,3},\d{1,3},\d{1,3}', re.M)
_address_regexp_6 = re.compile('\|\|\|\d+\|', re.M)


def parse_address_from_string(address: str):
    tokens = [t for t in re.split('[ \t,]', address) if t.isnumeric()]
    if len(tokens) != 6:
        return None
    return IPv4Address('.'.join(tokens[0:4]), int(tokens[4]) * 256 + int(tokens[5]))


def extract_address_from_text(text: str) -> [str, None]:
    result = _address_regexp_4.search(text)

    if result is not None:
        address = result.group(0)
        return parse_address_from_string(address)

    return


def parse_address_from_string_6(a: str):
    tokens = [t for t in re.split('[ \t, \|]', a) if t != '']

    if len(tokens) != 1:
        return None

    s, p = parse_helpers.try_parse_int(tokens[0])

    if s:
        return p

    return None


def extract_address_from_text_6(text: str) -> [str, None]:
    result = _address_regexp_6.search(text)

    if result is not None:
        address = result.group(0)
        return parse_address_from_string_6(address)

    return
