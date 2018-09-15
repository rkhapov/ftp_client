from abc import abstractmethod

from infra.environment import Environment
from protocol.ftp import FtpClient


class Command:
    def __init__(self, environment: Environment):
        self.__arguments = {}
        self.__environment = environment

    @property
    def environment(self):
        return self.__environment

    @property
    def arguments(self):
        return self.__arguments

    def add_argument(self, name: str, value: str):
        if name in self.__arguments:
            raise LookupError('Argument with name {} already exists'.format(name))

        self.__arguments[name] = value

    def get_argument(self, name: str) -> str:
        name = name.lower()
        if name not in self.__arguments:
            raise LookupError('No argument with name {}'.format(name))

        return self.__arguments[name]

    def has_argument(self, name):
        return name.lower() in self.__arguments

    @abstractmethod
    def execute(self, client: FtpClient):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def help():
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def name():
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def format():
        raise NotImplementedError
