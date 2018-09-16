import re


def split_without_escaped(s):
    return [f for f in re.split(r'(?<!\\)[ \t]', s) if f != '']
