def try_parse_int(s):
    if s.isnumeric():
        return True, int(s)
    return False, 0
