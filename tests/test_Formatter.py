from unittest import TestCase

from src.objectdiff.formatter import *
from tests.TestItem import TestItem


class TestFormatter(TestCase):
    def test_format(self):
        source = [1, 2, 3, 6]
        compare = [1, 2, 4, 5]
        delta = diff(source, compare)
        result = [delta.change for delta in format_items(delta, source, compare)]
        self.assertEqual(
            [Change.UNCHANGED, Change.UNCHANGED, Change.REMOVED, Change.REMOVED,
             Change.ADDED, Change.ADDED],
            result)

    def test_create_delta(self):
        sequence1 = [1, 2, 3]
        sequence2 = [1, 2, 4, 6, 7, 8, 9]
        deltas = diff(sequence1, sequence2)

        self.assertEqual(1, len(deltas))

    def test_format_items(self):
        source = [TestItem(value=1, text='test'), TestItem(value=2, text='test'), TestItem(value=3, text='test'),
                  TestItem(value=6, text='test')]
        compare = [TestItem(value=1, text='test'), TestItem(value=2, text='test'), TestItem(value=4, text='test'),
                   TestItem(value=5, text='test')]
        delta = diff(source, compare)
        result = [compared.change for compared in format_items(delta, source, compare)]
        self.assertEqual(
            [Change.UNCHANGED, Change.UNCHANGED, Change.REMOVED, Change.REMOVED,
             Change.ADDED, Change.ADDED],
            result)

    def test_create_delta_item(self):
        sequence1 = [TestItem(value=1, text='test'), TestItem(value=2, text='test'), TestItem(value=3, text='test')]
        sequence2 = [TestItem(value=1, text='test'), TestItem(value=2, text='test'), TestItem(value=4, text='test'),
                     TestItem(value=6, text='test'), TestItem(value=7, text='test'), TestItem(value=8, text='test'),
                     TestItem(value=9, text='test')]
        deltas = diff(sequence1, sequence2)

        self.assertEqual(1, len(deltas))

    def test_html_text_formatting(self):
        text1 = """line1
line2
line3"""
        text2 = """line1
line2
lineX"""

        html = format_diff_text_as_html(text1, text2)

        self.assertEqual("line1<br/>line2<br/><del>line3</del><br/><b>lineX</b>", html)
