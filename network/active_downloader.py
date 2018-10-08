#!/usr/bin/env python3
from network.server import Server


BYTES_PER_RECV = 4096


def download_active_with_server(server: Server, size=None):
    if size:
        return _download_exactly(server, size)
    return _download_all(server)


def _download_exactly(server: Server, size:int):
    pass


def _download_all(server: Server):
    pass
