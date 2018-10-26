from infra.writer import Writer
from tools.timer import Timer


class ProgressBar:
    def __init__(self, size, length=40):
        if length <= 2:
            raise ValueError('percent line length must be greater than 2')

        self.__size = size
        self.__current = 0
        self.__timer = Timer()
        self.__max_len = 1
        self.__length = length

    @property
    def length(self):
        return self.__length

    @property
    def timer(self):
        return self.__timer

    @property
    def elapsed_time(self):
        return self.__timer.elapsed

    def append(self, size):
        self.__current += size

    @property
    def current_size(self):
        return self.__current

    @property
    def size(self):
        return self.__size

    @property
    def bar(self):
        speed = self.__current / (self.elapsed_time + 1e-6)

        if self.__size is not None:
            percent = self.__current / self.__size * 100

            true_length = self.__length - 2
            filled_count = int(percent / 100 * true_length)

            bar = '[{}] {:.1f}% Speed: {:.2f} KB/s'.format(
                '#' * filled_count + ' ' * (true_length - filled_count),
                percent,
                speed / 1024)
        else:
            bar = 'Progressing with speed {:.2f} KB/s...'.format(speed / 1024)
        self.__max_len = max((self.__max_len, len(bar)))

        return bar

    @property
    def clearing_string(self):
        return ' ' * self.__max_len

    @property
    def statistic(self):
        if self.__size:
            return '{} of {} bytes from {:.2f} seconds'.format(self.__current, self.__size, self.elapsed_time)

        return '{} bytes from {:.2f} second'.format(self.__current, self.elapsed_time)

    def print_with_clearing(self, writer: Writer=None):

        if writer is None:
            return

        space = ' ' * self.__max_len
        bar = self.bar
        writer.write(f'\r{space}\r{bar}', end='')

    def __enter__(self):
        self.__timer.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__timer.kill()
