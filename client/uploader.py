#!/usr/bin/env python3

from client.tcpconnection import TcpConnection
from tools.progress_bar import get_progress_bar
from tools.timer import Timer


def upload_at_connection(connection: TcpConnection, data: bytes):
    uploaded_bytes = 0
    timer = Timer()
    timer.start()

    size = len(data)
    while uploaded_bytes < size:
        if size - uploaded_bytes >= 1024:
            l = 1024
            uploaded_bytes += 1024
        else:
            l = size - uploaded_bytes
            uploaded_bytes = size

        data_to_send = bytes(data[uploaded_bytes:uploaded_bytes+l])
        connection.send(data_to_send)

        speed = uploaded_bytes / (timer.get_elapsed() + 0.0001)
        bar = get_progress_bar(uploaded_bytes, speed, size)

        print('\r{}'.format(bar))

    timer.kill()


def upload_file_at_connection(connection: TcpConnection, path):
    with open(path, 'rb') as file:
        upload_at_connection(connection, file.read())
