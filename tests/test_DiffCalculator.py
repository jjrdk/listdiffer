from unittest import TestCase

from src.object_diff.DiffCalculator import DiffCalculator


class TestDiffCalculator(TestCase):
    def test_equal_text(self):
        calc = DiffCalculator()
        source = "some text"
        compare = "some text"
        result = calc.diff_text(source, compare)
        self.assertEqual(0, len(result))

    def test_equal_text_except_ignored_space(self):
        calc = DiffCalculator()
        source = "some text"
        compare = "some      text"
        result = calc.diff_text(source, compare, True)
        self.assertEqual(0, len(result))

    def test_equal_array(self):
        calc = DiffCalculator()
        source = [1,2,3]
        compare = [1,2,3]
        result = calc.diff(source, compare)
        self.assertEqual(0, len(result))
