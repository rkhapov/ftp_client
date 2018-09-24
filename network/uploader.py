from network.connection import Connection
from tools.progress_bar import get_progress_bar
from tools.timer import Timer


def upload_data_at_connection(connection: Connection, data: bytes):
    timer = Timer()
    timer.start()

    uploaded_bytes = 0
    max_len = 1

    while uploaded_bytes < len(data):
        if uploaded_bytes + 1024 < len(data):
            uploaded_bytes += 1024
            connection.send(data[uploaded_bytes:uploaded_bytes + 1024])
        else:
            uploaded_bytes += len(data) - uploaded_bytes
            connection.send(data[uploaded_bytes:uploaded_bytes + len(data) - uploaded_bytes])

        speed = uploaded_bytes / (timer.elapsed + 1e-6)

        bar = get_progress_bar(uploaded_bytes, speed, len(data))
        print('\r{}{}'.format(bar, ' ' * (max_len - len(bar))), end='')
        max_len = max((max_len, len(bar)))
    result = '\rUploaded {:.2f} Kbytes by {} seconds'.format(uploaded_bytes / 1024, timer.elapsed)
    print('\r{}{}'.format(result, ' ' * (max_len - len(result))))

    timer.kill()
