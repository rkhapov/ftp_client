#!/usr/bin/env python3
from abc import abstractmethod

from protocol.ftp import FtpClient


class Command:
    def __init__(self):
        self.args = []

    @abstractmethod
    def execute(self, client: FtpClient):
        raise NotImplemented

    @abstractmethod
    @property
    def help(self):
        raise NotImplemented

    @abstractmethod
    @property
    def name(self):
        raise NotImplemented
