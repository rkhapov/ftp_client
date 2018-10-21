#!/usr/bin/env python3

from abc import abstractmethod


class Address:
    @property
    @abstractmethod
    def host(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def port(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def as_tuple(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def ftp_address(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def ftp_extendend_address(self):
        raise NotImplementedError

    @abstractmethod
    def with_port(self, new_port):
        raise NotImplementedError

    @abstractmethod
    def with_host(self, new_host):
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other):
        raise NotImplementedError


class IPv4Address(Address):
    def __init__(self, host: str, port: int):
        if not isinstance(host, str):
            raise ValueError('host should be of type str')

        if not isinstance(port, int):
            raise ValueError('port should be of type int')

        self.__host = host
        self.__port = port

    @property
    def host(self):
        return self.__host

    @property
    def port(self):
        return self.__port

    @property
    def as_tuple(self):
        return self.__host, self.__port

    @property
    def ftp_address(self):
        return ','.join([*self.__host.split('.'),
                         *[str(int(b)) for b in self.__port.to_bytes(2, byteorder='big')]])

    @property
    def ftp_extendend_address(self):
        return '|' + '|'.join(['1', str(self.host), str(self.port)]) + '|'

    def __eq__(self, other):
        if not isinstance(other, IPv4Address):
            return False

        return self.__host == other.host and self.__port == other.port

    def with_port(self, new_port):
        return IPv4Address(host=self.__host, port=new_port)

    def with_host(self, new_host):
        return IPv4Address(host=new_host, port=self.__port)


class IPv6Address(Address):
    def __init__(self, host: str, port: int):
        self.__host = host
        self.__port = port

    @property
    def host(self):
        return self.__host

    @property
    def port(self):
        return self.__port

    @property
    def as_tuple(self):
        return self.__host, self.__port

    @property
    def ftp_address(self):
        return self.ftp_extendend_address

    @property
    def ftp_extendend_address(self):
        return '|' + '|'.join(['2', str(self.host), str(self.port)]) + '|'

    def __eq__(self, other):
        if not isinstance(other, IPv6Address):
            return False

        return self.__host == other.host and self.__port == other.port

    def with_port(self, new_port):
        return IPv6Address(host=self.__host, port=new_port)

    def with_host(self, new_host):
        return IPv6Address(host=new_host, port=self.__port)
