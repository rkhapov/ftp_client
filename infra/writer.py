#!/usr/bin/env python3
from abc import *


class Writer:
    @abstractmethod
    def write(self, s='', end=None, is_error=None):
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


class OnlyErrorsConsoleWriter(Writer):
    def write(self, s='', end=None, is_error=False):
        if is_error:
            print(s, end=end)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def close(self):
        pass


class ConsoleAllWriter(Writer):
    def write(self, s='', end=None, is_error=False):
        print(s, end=end)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def close(self):
        pass
