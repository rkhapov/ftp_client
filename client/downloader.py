#!/usr/bin/env python3


from client.tcpconnection import TcpConnection


def _get_percent_line(percent, length=40):
    if length <= 2:
        raise ValueError('percent line length must be greater than 2')

    true_length = length - 2
    filled_count = int(percent / 100 * true_length)

    return '[{}{}] {:.1f}%'.format('#' * filled_count, ' ' * (true_length - filled_count), percent)


def download__data_from_connection(connection: TcpConnection, percent_func=None):
    data = bytearray()

    while True:
        next_part = connection.receive(1024)

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


def download_data(address, port, percent_func=None):
    connection = TcpConnection(address, port)

    return download__data_from_connection(connection, percent_func)


def download_file_from_connection(connection: TcpConnection, path, percent_func=None):
    data = download__data_from_connection(connection, percent_func)
    with open(path, 'wb') as file:
        file.write(data)


def download_file(address, port, path, percent_func=None):
    data = download_data(address, port, percent_func)
    with open(path, 'wb') as file:
        file.write(data)
