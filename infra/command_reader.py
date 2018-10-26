#!/usr/bin/env python3
from abc import *


class CommandReader:
    @abstractmethod
    def read_next_command(self):
        raise NotImplementedError
