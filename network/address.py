#!/usr/bin/env python3


class Address:
    def __init__(self, host: str, port: int):
        if not isinstance(host, str):
            raise ValueError('host should be of type str')

        if not isinstance(port, int):
            raise ValueError('port should be of type int')

        self.__host = host
        self.__port = port

    @property
    def ip(self):
        return self.__host

    @property
    def port(self):
        return self.__port

    @property
    def as_tuple(self):
        return self.__host, self.__port
