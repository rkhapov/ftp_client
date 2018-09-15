import unittest
from protocol.status import is_positive_preliminary_code, is_positive_completion_code, \
    is_positive_intermediate_completion_code, is_transient_negative_completion_code, \
    is_permanent_negative_completion_code


class StatusUnitTests(unittest.TestCase):
    def test_is_positive_preliminary_code__code_are_not__should_return_false(self):
        self.assertFalse(is_positive_preliminary_code(223))

    def test_is_positive_preliminary_code__code_are__should_return_true(self):
        self.assertTrue(is_positive_preliminary_code(123))

    def test_is_positive_completion_code__code_are_not__should_return_false(self):
        self.assertFalse(is_positive_completion_code(123))

    def test_is_positive_completion_code__code_are__should_return_true(self):
        self.assertTrue(is_positive_completion_code(223))

    def test_is_positive_intermediate_code__code_are_not__should_return_false(self):
        self.assertFalse(is_positive_intermediate_completion_code(123))

    def test_is_positive_intermediate_code__code_are__should_return_true(self):
        self.assertTrue(is_positive_intermediate_completion_code(300))

    def test_is_transient_negative_completion_code__code_are_not__should_return_false(self):
        self.assertFalse(is_transient_negative_completion_code(345))

    def test_is_transient_negative_completion_code__code_are__should_return_true(self):
        self.assertTrue(is_transient_negative_completion_code(455))

    def test_is_permanent_negative_completion_code__code_are_not__should_return_false(self):
        self.assertFalse(is_permanent_negative_completion_code(123))

    def test_is_permanent_negative_completion_code__code_are__should_return_true(self):
        self.assertTrue(is_permanent_negative_completion_code(543))
