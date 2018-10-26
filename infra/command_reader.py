#!/usr/bin/env python3
import re
from abc import *
from getpass import getpass


class CommandReader:
    @abstractmethod
    def read_next_command(self, promt):
        raise NotImplementedError

    @abstractmethod
    def read_hide(self, promt):
        raise NotImplementedError

    @property
    @abstractmethod
    def supports_hide(self):
        raise NotImplementedError

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError


class ConsoleCommandReader(CommandReader):
    def read_next_command(self, promt='?>'):
        try:
            return input(promt)
        except KeyboardInterrupt:
            raise
        except:
            return None

    def read_hide(self, promt):
        return getpass(promt)

    @property
    def supports_hide(self):
        return True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def close(self):
        pass


class FileCommandReader(CommandReader):
    def __init__(self, script_path, cmd_line_split='|'):
        self.__file = open(script_path, 'r')
        self.__buff = []
        self.__cmd_line_split = '[' + cmd_line_split + ']'

    def read_next_command(self, promt=None):
        if len(self.__buff) != 0:
            return self.__buff.pop()

        line = self.__file.readline()

        if line == '':
            return None

        if line.strip() == '':
            return ''

        tokens = list(filter(lambda x: x != '', map(lambda x: x.strip(), re.split(self.__cmd_line_split, line))))

        if len(tokens) == 0:
            return None

        self.__buff.extend(tokens[1:])

        return tokens[0]

    def read_hide(self, promt):
        raise TypeError('Hided reading are not valid on scripts!')

    @property
    def supports_hide(self):
        return False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.__file.close()
