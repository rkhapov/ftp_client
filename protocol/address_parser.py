import re

from network.address import Address

_address_regexp = re.compile('\d{1,3},\d{1,3},\d{1,3},\d{1,3},\d{1,3},\d{1,3}', re.M)


def parse_address_from_string(address: str):
    tokens = [t for t in re.split('[ \t,]', address) if t != '' and t.isnumeric()]
    if len(tokens) != 6:
        return None
    return Address('.'.join(tokens[0:4]), int(tokens[4]) * 256 + int(tokens[5]))


def extract_address_from_text(text: str) -> [str, None]:
    result = _address_regexp.search(text)

    if result is not None:
        address = result.group(0)
        return parse_address_from_string(address)

    return
