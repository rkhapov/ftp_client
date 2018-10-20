import threading
import time


class Timer:
    def __init__(self, interval=1.0 / 10):
        self._interval = interval
        self._thread = threading.Thread(target=self._thread_target, daemon=True)
        self._killed = False
        self._pause = True
        self._elapsed = 0.0

    def start(self):
        self._pause = False
        if not self._thread.is_alive():
            self._thread.start()

    def pause(self):
        self._pause = True

    def stop(self):
        self._pause = True
        self._elapsed = 0.0

    def kill(self):
        self._killed = True

    @property
    def interval(self):
        return self._interval

    @property
    def elapsed(self):
        return self._elapsed

    def _thread_target(self):
        while not self._killed:
            time.sleep(self._interval)

            if not self._pause:
                self._elapsed += self._interval

    def __enter__(self):
        self.stop()
        self.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.kill()
