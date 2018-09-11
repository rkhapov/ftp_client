#!/usr/bin/env python3

import re

_size_regexp = re.compile('\d+ bytes')


def extract_size_from_text(text: str):
    result = _size_regexp.search(text)

    if result is not None:
        size = result.group(0)
        return int(size.split(' ')[0])

    return None
