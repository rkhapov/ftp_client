from network.connection import Connection
from tools.timer import Timer
from tools.progress_bar import get_progress_bar


def download_data_from_connection(connection: Connection, size: int=None):
    if size is None:
        return bytes(_download_all_from_connection(connection))

    return bytes(_download_exact_amount_from_connection(connection, size))


def _download_exact_amount_from_connection(connection, size):
    timer = Timer()
    timer.start()
    data = bytearray()

    max_len = 1
    while len(data) != size:
        next_part = connection.receive(4096 if len(data) + 4096 < size else size - len(data))

        for b in next_part:
            data.append(b)

        speed = len(data) / (timer.elapsed + 1e-6) / 1024 * 1000

        bar = get_progress_bar(len(data), speed, size)
        print('\r{}{}'.format(bar, ' ' * (max_len - len(bar))), end='')
        max_len = max((max_len, len(bar)))
    ss = 'Downloaded {:.2f} Kbytes by {:.2f} sec'.format(len(data) / 1024, timer.elapsed)
    print('\r{}{}'.format(ss, ' ' * (max_len - len(ss))))
    timer.kill()

    return data


def _download_all_from_connection(connection):
    timer = Timer()
    timer.start()
    data = bytearray()

    max_len = 1
    while True:
        next_part = connection.receive(4096)

        if len(next_part) == 0:
            break

        for b in next_part:
            data.append(b)

        speed = len(data) / (timer.elapsed + 1e-6) / 1024 * 1000

        bar = get_progress_bar(len(data), speed)
        print('\r{}{}'.format(bar, ' ' * (max_len - len(bar))), end='')
        max_len = max((max_len, len(bar)))
    ss = 'Downloaded {:.2f} Kbytes by {:.2f} sec'.format(len(data) / 1024, timer.elapsed)
    print('\r{}{}'.format(ss, ' ' * (max_len - len(ss))))
    timer.kill()

    return data
