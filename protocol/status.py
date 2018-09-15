import enum


class FirstDigit(enum.Enum):
    POSITIVE_PRELIMINARY = 1
    POSITIVE_COMPLETION = 2
    POSITIVE_INTERMEDIATE_COMPLETION = 3
    TRANSIENT_NEGATIVE_COMPLETION = 4
    PERMANENT_NEGATIVE_COMPLETION = 5


def _get_first_digit(code: int):
    d = code // 100

    return d


def is_positive_preliminary_code(code: int):
    return _get_first_digit(code) == FirstDigit.POSITIVE_PRELIMINARY.value


def is_positive_completion_code(code: int):
    return _get_first_digit(code) == FirstDigit.POSITIVE_COMPLETION.value


def is_positive_intermediate_completion_code(code: int):
    return _get_first_digit(code) == FirstDigit.POSITIVE_INTERMEDIATE_COMPLETION.value


def is_transient_negative_completion_code(code: int):
    return _get_first_digit(code) == FirstDigit.TRANSIENT_NEGATIVE_COMPLETION.value


def is_permanent_negative_completion_code(code: int):
    return _get_first_digit(code) == FirstDigit.PERMANENT_NEGATIVE_COMPLETION.value


class SecondDigit(enum.Enum):
    SYNTAX = 0
    INFORMATION = 1
    CONNECTIONS = 2
    AUTHENTICATION_AND_ACCOUNTING = 3
    UNSPECIFIED = 4
    FILE_SYSTEM = 5


class StatusCode(enum.Enum):
    RESTART_MARKER_REPLY = 110
    SERVICE_READY_IN_MINUTES = 120
    TRANSFER_STARTING = 125
    FILE_STATUS_OK = 150

    COMMAND_OK = 200
    COMMAND_SUPERFLUOUS = 202
    SYSTEM_STATUS = 211
    DIRECTORY_STATUS = 212
    FILE_STATUS = 213
    HELP = 214
    SYSTEM_TYPE = 215
    READY_FOR_NEW_USER = 220
    CLOSING_CONTROL_CONNECTION = 221
    DATA_CONNECTION_OPEN = 225
    CLOSING_DATA_CONNECTION = 226
    ENTERING_PASSIVE_MODE = 227
    USER_LOGGED_IN = 230
    REQUESTED_FILE_ACTION_OKAY = 250
    PATHNAME_CREATED = 257

    USER_OKAY_NEED_PASSWORD = 331
    NEED_ACCOUNT_FOR_LOGIN = 332
    REQUESTED_FILE_ACTION_PENDING_INFO = 350

    SERVICE_NOT_AVAILABLE_CONTROL_CONNECTION_CLOSING = 421
    CANT_OPEN_DATA_CONNECTION = 425
    CONNECTION_CLOSED = 426
    FILE_BUSY = 450
    LOCAL_ERROR = 451
    INSUFFICIENT_STORAGE_SPACE = 452

    COMMAND_UNRECOGNIZED = 500
    PARAMETERS_ERROR = 501
    COMMAND_NOT_IMPLEMENTED = 502
    BAD_SEQUENCE_OF_COMMANDS = 503
    NOT_IMPLEMENTED_FOR_PARAMETER = 504
    NOT_LOGGED_IN = 530
    NEED_ACCOUNT_FOR_STORING = 532
    FILE_UNAVAILABLE = 550
    PAGE_TYPE_UNKNOWN = 551
    EXCEEDED_STORAGE_ALLOCATION = 552
    FILE_NAME_NOT_ALLOWED = 553
