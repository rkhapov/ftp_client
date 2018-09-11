import unittest
import tools.sizeparser


class ExtractSizeFromTextTests(unittest.TestCase):
    def test_no_size_in_text_should_return_none(self):
        sut = tools.sizeparser.extract_size_from_text('105 my text lol')

        self.assertIsNone(sut)

    def test_returns_right_size(self):
        sut = tools.sizeparser.extract_size_from_text('105 my text lol (1488 bytes)')

        self.assertEqual(sut, 1488)
