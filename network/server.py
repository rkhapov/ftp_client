#!/usr/bin/env python3
from abc import abstractmethod

from network.address import Address
from network.connection import Connection


class Server:
    @abstractmethod
    @property
    def socket(self):
        raise NotImplementedError

    @abstractmethod
    def listen(self, n) -> Address:
        raise NotImplementedError

    @abstractmethod
    def accept(self) -> (Connection, Address):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError
