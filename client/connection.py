#!/usr/bin/env


# abstract class for network connection

from abc import *


class Connection:
    @abstractmethod
    def send(self, data: bytes):
        raise NotImplemented

    @abstractmethod
    def receive(self, max_length: int = None):
        raise NotImplemented

    @abstractmethod
    def close(self):
        raise NotImplemented
