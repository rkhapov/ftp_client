import chardet

from infra.command_reader import CommandReader
from infra.writer import Writer


def decode_bytes(data: bytes, writer: Writer = None, reader: CommandReader = None) -> str:
    encoding = chardet.detect(data)['encoding']
    if encoding is None:
        if reader is None:
            return ''

        encoding = reader.read_next_command(
            "Warning! Cant get encoding of content. Enter which encoding should be used(empty for utf-8):")

        if encoding == '':
            encoding = 'utf-8'

    try:
        return data.decode(encoding)
    except TypeError as e:
        if writer is not None:
            writer.write(e.args[0], is_error=True)
        return ''
