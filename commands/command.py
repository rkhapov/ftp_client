#!/usr/bin/env python3
from abc import abstractmethod

from network.ftp import FtpConnection


class Command:
    @abstractmethod
    def execute(self, connection: FtpConnection):
        raise NotImplemented
