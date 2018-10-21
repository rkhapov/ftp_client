from network.connection import Connection
from tools.progress_bar import ProgressBar


def download(connection: Connection, size=None, part_callback=None, bytes_per_recv=4096, start=0):
    with ProgressBar(size) as bar:
        data = bytearray()

        bar.append(start)

        try:
            part = connection.receive(bytes_per_recv)

            while len(part) != 0:
                data.extend(part)

                if part_callback is not None:
                    part_callback(part)

                bar.append(len(part))
                bar.print_with_clearing()

                part = connection.receive(bytes_per_recv)

            print()
            print(f'Downloaded {bar.statistic}')

            return data

        except KeyboardInterrupt:
            print()
            print(f'Downloading aborted at {len(data)} bytes')
            print(f'Downloaded {bar.statistic}')
            return data
