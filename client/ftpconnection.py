#!/usr/bin/env python3

from client.tcpconnection import TcpConnection, Connection


class FtpConnection(Connection):
    def __init__(self, host: str, port: int, logfile: str = None):
        self._connection = TcpConnection(host, port, logfile)

    def send(self, data: str):
        if not data.endswith('\n'):
            data += '\n'

        self._connection.send(data)

    def receive(self, max_length: int = 1024):
        return self._connection.receive(max_length)

    def close(self):
        self._connection.close()
