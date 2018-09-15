class Address:
    def __init__(self, host: str, port: int):
        if not isinstance(host, str):
            raise ValueError('host should be of type str')

        if not isinstance(port, int):
            raise ValueError('port should be of type int')

        self.__host = host
        self.__port = port

    @property
    def host(self):
        return self.__host

    @property
    def port(self):
        return self.__port

    @property
    def as_tuple(self):
        return self.__host, self.__port

    def __eq__(self, other):
        if other is None:
            return False

        if not isinstance(other, Address):
            return False

        return self.__host == other.host and self.__port == other.port
