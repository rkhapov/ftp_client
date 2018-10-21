from abc import abstractmethod


class Connection:
    @abstractmethod
    def receive(self, buff_size) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def send(self, data: bytes):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def address(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def peer_address(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def timeout(self):
        raise NotImplementedError

    @timeout.setter
    @abstractmethod
    def timeout(self, t):
        raise NotImplementedError
