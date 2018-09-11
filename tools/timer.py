#!/usr/bin/env python3

import threading
import time


class Timer:
    def __init__(self, interval=1.0 / 10):
        self._interval = interval
        self._thread = threading.Thread(target=self._thread_target, daemon=True)
        self._killed = False
        self._elapsed = 0.0

    def start(self):
        if not self._thread.is_alive():
            self._thread.start()

    def _thread_target(self):
        while not self._killed:
            time.sleep(self._interval)

            self._elapsed += self._interval

    def set_interval(self, interval):
        self._interval = interval

    def get_interval(self):
        return self._interval

    def kill(self):
        self._killed = True

    def get_elapsed(self):
        return self._elapsed
