#!/usr/bin/env python3
from network.address import Address
from network.ftp import FtpConnection, FtpAnswer
from network.tcp import TcpConnection
from tools import parse_helper
from tools.progress_bar import get_progress_bar
from tools.timer import Timer


class Actions:
    def __init__(self, in_progress=None, success=None, failed=None, need_more=None, cant_execute_now=None):
        self.__in_progress = in_progress
        self.__success = success
        self.__failed = failed
        self.__need_more = need_more
        self.__cant_execute_now = cant_execute_now

    @property
    def in_progress(self):
        return self.__in_progress

    @property
    def success(self):
        return self.__success

    @property
    def failed(self):
        return self.__failed

    @property
    def need_more(self):
        return self.__need_more

    @property
    def cant_execute_now(self):
        return self.__cant_execute_now


def _print_body_of_answer(answers):
    for ans in answers:
        print(ans.body)


class FtpRequest:
    def __init__(self, command: str, actions: Actions = None):
        self.__command = command
        self.__actions = actions

    @property
    def command(self):
        return self.__command

    @property
    def actions(self):
        return self.__actions

    @property
    def in_progress(self):
        if self.__actions is None or self.__actions.in_progress is None:
            return _print_body_of_answer

        return self.__actions.in_progress

    @property
    def success(self):
        if self.__actions is None or self.__actions.success is None:
            return _print_body_of_answer

        return self.__actions.success

    @property
    def failed(self):
        if self.__actions is None or self.__actions.failed is None:
            return _print_body_of_answer

        return self.__actions.failed

    @property
    def need_more(self):
        if self.__actions is None or self.__actions.need_more is None:
            return _print_body_of_answer

        return self.__actions.need_more

    @property
    def cant_execute_now(self):
        if self.__actions is None or self.__actions.cant_execute_now is None:
            return _print_body_of_answer

        return self.__actions.cant_execute_now


class FtpResponse:
    def __init__(self, answers):
        self.__answers = answers

    @property
    def answers(self):
        return self.__answers

    @property
    def last_answer(self):
        return self.__answers[-1]


class FtpClient:
    def __init__(self, connection: FtpConnection, address: Address):
        if connection is None:
            tcp_connection = TcpConnection(address)
            ftp_connection = FtpConnection(tcp_connection)
            connection = ftp_connection

        self.__connection = connection

    @property
    def connection(self):
        return self.__connection

    def to_passive_mode(self) -> [Address, None]:
        self.__connection.send_command("PASV")
        answer = self.__connection.receive_answer()

        if answer.is_success_answer:
            return parse_helper.extract_address_from_text(answer.body)

        return None

    def execute(self, request: FtpRequest) -> FtpResponse:
        self.__connection.send_command(request.command)

        answer = self.__connection.receive_answer()

        if answer.is_multi_line_answer:
            answers = [answer, self.__connection.receive_answer()]
        else:
            answers = [answer]

        last_answer = answers[-1]

        if last_answer.is_in_progress_answer:
            request.in_progress(answers)
            answers.append(self.__connection.receive_answer())
        elif last_answer.is_success_answer:
            request.success(answers)
        elif last_answer.is_need_more_command_answer:
            request.need_more(answers)
        elif last_answer.is_cant_accept_now_answer:
            request.cant_execute_now(answers)
        else:
            request.failed(answers)

        return FtpResponse(answers)

    def download(self, connection: TcpConnection, size):
        data = bytearray()
        timer = Timer()
        timer.start()

        while True:
            next_part = connection.receive(1024)

            if len(next_part) == 0:
                break
            downloaded = len(next_part) + len(data)

            speed = downloaded / (timer.get_elapsed() + 1e-6)

            percent_line = get_progress_bar(downloaded, speed, size)
            print('\r' + percent_line + '        ', end='')

            for b in next_part:
                data.append(b)

        print('\r')

        timer.kill()

        return data
