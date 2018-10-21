class Reply:
    def __init__(self, status_code: int, text: str):
        self.__status_code = status_code
        self.__text = text

    @property
    def status_code(self):
        return self.__status_code

    @property
    def text(self):
        return self.__text

    @property
    def is_success_reply(self):
        return str(self.__status_code).startswith('2')

    def __eq__(self, other):
        if not isinstance(other, Reply):
            return False

        return self.__status_code == other.status_code and self.__text == other.text
