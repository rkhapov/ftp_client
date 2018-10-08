import chardet


def decode_bytes(data: bytes) -> str:
    encoding = chardet.detect(data)['encoding']
    if encoding is None:
        encoding = input("Warning! Cant get encoding of content. Enter which encoding should be used(empty for utf-8):")

        if encoding == '':
            encoding = 'utf-8'

    try:
        return data.decode(encoding)
    except TypeError as e:
        print(e.args[0])
        return ''

