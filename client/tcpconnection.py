#!/usr/bin/env python3

import socket
import logging

from client.connection import Connection


def cut_to_len(data, l):
    return data if len(data) <= l else data[0:l]


class TcpConnection(Connection):
    def __init__(self, destination_address: str, destination_port: int, logfile: str = None):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((destination_address, destination_port))

        self._logfile = None
        if logfile is not None:
            self._enable_logging(logfile)

    def send(self, data: str):
        if not isinstance(data, bytes):
            if not isinstance(data, str):
                raise TypeError('Expected bytes or string data to send in connection')
            data = bytes(data, 'utf-8')

        if data[len(data) - 1] != b'\n':
            data += b'\n'

        if self._logfile is not None:
            logging.info('Sending, size={}: {}'.format(len(data), cut_to_len(data, 1024)))

        self._socket.sendall(data)

    def receive(self, max_length: int = 1024) -> str:
        data = self._socket.recv(max_length)

        if self._logfile is not None:
            logging.info('Received, size={}: {}'.format(len(data), cut_to_len(data, 1024)))

        return data.decode('utf-8')

    def close(self):
        self._socket.close()

    def get_logfile(self):
        return self._logfile

    def _enable_logging(self, filename: str):
        from time import gmtime, strftime
        logging.basicConfig(filename=filename, level=logging.DEBUG)
        logging.info('Logging enable, run at: {}'.format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
        self._logfile = filename
