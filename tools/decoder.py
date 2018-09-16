import chardet


def decode_bytes(data: bytes) -> str:
    encoding = chardet.detect(data)['encoding']

    return data.decode(encoding)
