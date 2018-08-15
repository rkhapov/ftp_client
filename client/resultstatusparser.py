#!/usr/bin/env python3

from enum import Enum


# class Status(Enum):
#     IN_PROGRESS = 1
#     SUCCESS = 2
#     NEED_ONE_MORE_COMMAND = 3
#     CANT_EXECUTE_COMMAND_NOW = 4
#     CANT_BE_EXECUTED = 5


class ResultStatusParser:
    # @staticmethod
    # def get_command_code(command: str):
    #     return Status(ResultStatusParser.get_status_code(command) // 100)

    @staticmethod
    def get_status_code(result: str):
        try:
            return int(result[0:2])
        except:
            raise ValueError

    @staticmethod
    def is_success_code(code: int):
        return str(code).startswith('2')

    @staticmethod
    def is_need_more_command_code(code: int):
        return str(code).startswith('3')
