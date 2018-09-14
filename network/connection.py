#!/usr/bin/env python3
from abc import abstractmethod, abstractproperty


class Connection:
    @abstractmethod
    def receive(self, buff_size) -> bytes:
        raise NotImplemented

    @abstractmethod
    def send(self, data: bytes):
        raise NotImplemented

    @property
    @abstractmethod
    def address(self):
        raise NotImplemented

    @property
    @abstractmethod
    def timeout(self):
        raise NotImplemented
