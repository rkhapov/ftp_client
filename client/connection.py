#!/usr/bin/env


# abstract class for network connection

from abc import *


class Connection:
    @abstractmethod
    def send(self, data: str):
        raise NotImplemented

    @abstractmethod
    def receive(self, max_length: int = 1024):
        raise NotImplemented

    @abstractmethod
    def close(self):
        raise NotImplemented
