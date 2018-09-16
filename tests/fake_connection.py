from network.connection import Connection


class FakeConnection(Connection):
    def __init__(self, address, recv_data, timeout, raise_over_reading=False):
        self.recv_data = recv_data
        self.recv_pointer = 0
        self.send_data = bytearray()
        self.__address = address
        self.__timeout = timeout
        self.closed = False
        self.raise_over_reading = raise_over_reading

    def receive(self, buff_size) -> bytes:
        if self.recv_pointer >= len(self.recv_data) and self.raise_over_reading:
            raise IndexError('over reading from connection')

        if self.recv_pointer >= len(self.recv_data):
            return b''

        data = self.recv_data[self.recv_pointer: self.recv_pointer + buff_size].encode('utf-8')
        self.recv_pointer += buff_size

        return data

    def send(self, data: bytes):
        for b in data:
            self.send_data.append(b)

    def close(self):
        self.closed = True

    @property
    def address(self):
        return self.__address

    @property
    def timeout(self):
        return self.__timeout
