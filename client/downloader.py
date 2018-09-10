#!/usr/bin/env python3


from client.tcpconnection import TcpConnection


def _get_percent_line(percent, length=20):
    if length <= 2:
        raise ValueError('percent line length must be greater than 2')

    true_length = length - 2
    filled_count = percent / 100 * true_length

    return '[{}{}] {:.1}'.format('#' * filled_count, ' ' * (true_length - filled_count), percent)


def download_data(address, port, percent_func=None):
    connection = TcpConnection(address, port)

    data = bytearray()

    while True:
        next_part = connection.receive()

        if len(next_part) == 0:
            break

        if percent_func is not None:
            percent = percent_func(len(data) + len(next_part))
            percent_line = _get_percent_line(percent)
            print('\r' + percent_line, end='')

        for b in next_part:
            data.append(b)

    if percent_func is not None:
        print('\r')

    return data


def download_file(address, port, path, percent_func=None):
    data = download_data(address, port, percent_func)
    with open(path, 'rw') as file:
        file.write(data)


if __name__ == '__main__':
    import sys
    download_file(sys.argv[0], sys.argv[1], sys.argv[2])
