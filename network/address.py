class Address:
    def __init__(self, host: str, port: int, type='ipv4'):
        if not isinstance(host, str):
            raise ValueError('host should be of type str')

        if not isinstance(port, int):
            raise ValueError('port should be of type int')

        self.__host = host
        self.__port = port
        self.__type = type

    @property
    def type(self):
        return self.__type

    @property
    def host(self):
        return self.__host

    @property
    def port(self):
        return self.__port

    @property
    def as_tuple(self):
        return self.__host, self.__port

    @property
    def ftp_address(self):
        t = self.__type

        if t == 'ipv4':
            return self._convert_to_ftp_ipv4()

        raise NotImplementedError(f'converting to ftp address of type {t} are not supported')

    def __eq__(self, other):
        if other is None:
            return False

        if not isinstance(other, Address):
            return False

        return self.__host == other.host and self.__port == other.port

    def _convert_to_ftp_ipv4(self):
        return ','.join([
            *self.__host.split('.'),
            *[str(int(b)) for b in self.__port.to_bytes(2, byteorder='big')]])
