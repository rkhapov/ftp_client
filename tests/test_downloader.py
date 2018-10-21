import random
import string
import unittest

from network.downloader import download
from tests.fake_connection import FakeConnection


def get_connetion(text):
    return FakeConnection('my_addr', text, -1)


def get_random_data(size):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=size))


class DownloaderUnitTests(unittest.TestCase):
    def test_download_data_from_connection__should_not_call_send_from_connection(self):
        connection = get_connetion('lol connection')

        download(connection)

        self.assertEqual(len(connection.send_data), 0)

    def test_download_data_from_connection__size_are_none__should_download_all_data_from_connection(self):
        data = get_random_data(5234)
        connection = get_connetion(data)

        downloaded_data = download(connection)

        self.assertSequenceEqual(downloaded_data, data.encode())
