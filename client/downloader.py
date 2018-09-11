#!/usr/bin/env python3


from client.tcpconnection import TcpConnection
from tools.timer import Timer
from tools.progress_bar import get_progress_bar


def download_data_from_connection(connection: TcpConnection, size=None):
    data = bytearray()
    timer = Timer()
    timer.start()

    while True:
        next_part = connection.receive(1024)

        if len(next_part) == 0:
            break
        downloaded = len(next_part) + len(data)

        speed = downloaded / (timer.get_elapsed() + 1e-6)

        percent_line = get_progress_bar(downloaded, speed, size)
        print('\r' + percent_line + '        ', end='')

        for b in next_part:
            data.append(b)

    print('\r')

    timer.kill()

    return data


def download_data(address, port, size=None):
    connection = TcpConnection(address, port)

    return download_data_from_connection(connection, size)


def download_file_from_connection(connection: TcpConnection, path, size=None):
    data = download_data_from_connection(connection, size)
    with open(path, 'wb') as file:
        file.write(data)


def download_file(address, port, path, size=None):
    data = download_data(address, port, size)
    with open(path, 'wb') as file:
        file.write(data)
