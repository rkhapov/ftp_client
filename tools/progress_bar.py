#!/usr/bin/env python3


def get_progress_bar(current_length, speed, size=None, length=40):
    if size is not None:
        percent = current_length / size * 100
        if length <= 2:
            raise ValueError('percent line length must be greater than 2')

        true_length = length - 2
        filled_count = int(percent / 100 * true_length)

        return '[{}] {:.1f}% Speed: {:.2f} KB/s'.format(
            '#' * filled_count + ' ' * (true_length - filled_count),
            percent,
            speed / 1024)

    return 'Transferring with speed {:.2f} KB/s...'.format(speed / 1024)
