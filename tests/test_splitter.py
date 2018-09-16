import unittest

from tools.splitter import split_without_escaped


class SplitterUnitTests(unittest.TestCase):
    def test_split_without_escape__without_any_escaped__should_return_right_tokens(self):
        sut = split_without_escaped('this is\tmy   string')

        self.assertSequenceEqual(sut, ['this', 'is', 'my', 'string'])

    def test_split_without_escape__with_escaped__shoult_return_right_tokens(self):
        sut = split_without_escaped(r'this is         m\ y \\string')

        self.assertSequenceEqual(sut, ['this', 'is', r'm\ y', r'\\string'])
