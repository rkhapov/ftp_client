from network.connection import Connection
from tools.progress_bar import ProgressBar


def upload(connection: Connection, data: bytes, part_callback=None, bytes_per_send=4096):
    with ProgressBar(len(data)) as bar:
        try:
            offset = 0

            while offset < len(data):
                send_data = data[offset:offset + bytes_per_send]
                connection.send(send_data)
                offset += bytes_per_send

                if part_callback is not None:
                    part_callback(send_data)

                bar.append(len(send_data))
                bar.print_with_clearing()

            print()
            print(f'Sent {bar.statistic}')

        except KeyboardInterrupt:
            print()
            print(f'Uploading aborted at {offset} bytes')
            print(f'Sent {bar.statistic}')
