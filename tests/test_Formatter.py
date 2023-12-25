from unittest import TestCase

from src.object_diff.Compared import Change
from src.object_diff.DiffCalculator import DiffCalculator
from src.object_diff.Formatter import Formatter
from tests.TestItem import TestItem


class TestFormatter(TestCase):
    def test_format(self):
        source = [1, 2, 3, 6]
        compare = [1, 2, 4, 5]
        delta = DiffCalculator.diff(source, compare)
        result = [compared.change for compared in Formatter.format(delta, source, compare)]
        self.assertEqual(
            [Change.UNCHANGED, Change.UNCHANGED, Change.REMOVED, Change.REMOVED,
             Change.ADDED, Change.ADDED],
            result)

    def test_create_delta(self):
        sequence1 = [1, 2, 3]
        sequence2 = [1, 2, 4, 6, 7, 8, 9]
        deltas = Formatter.create_delta(sequence1, sequence2)

        self.assertEqual(1, len(deltas))

    def test_apply_deltas(self):
        sequence1 = [1, 2, 3, 5, 6, 8, 9]
        sequence2 = [1, 2, 4, 6, 7, 8, 9]
        deltas = Formatter.create_delta(sequence1, sequence2)
        applied = Formatter.apply_deltas(sequence1, deltas)

        self.assertEqual(sequence2, applied)

    def test_format_item(self):
        source = [TestItem(value=1, text='test'), TestItem(value=2, text='test'), TestItem(value=3, text='test'),
                  TestItem(value=6, text='test')]
        compare = [TestItem(value=1, text='test'), TestItem(value=2, text='test'), TestItem(value=4, text='test'),
                   TestItem(value=5, text='test')]
        delta = DiffCalculator.diff(source, compare)
        result = [compared.change for compared in Formatter.format(delta, source, compare)]
        self.assertEqual(
            [Change.UNCHANGED, Change.UNCHANGED, Change.REMOVED, Change.REMOVED,
             Change.ADDED, Change.ADDED],
            result)

    def test_create_delta_item(self):
        sequence1 = [TestItem(value=1, text='test'), TestItem(value=2, text='test'), TestItem(value=3, text='test')]
        sequence2 = [TestItem(value=1, text='test'), TestItem(value=2, text='test'), TestItem(value=4, text='test'),
                     TestItem(value=6, text='test'), TestItem(value=7, text='test'), TestItem(value=8, text='test'),
                     TestItem(value=9, text='test')]
        deltas = Formatter.create_delta(sequence1, sequence2)

        self.assertEqual(1, len(deltas))

    def test_apply_deltas_item(self):
        sequence1 = [TestItem(value=1, text='test'), TestItem(value=2, text='test'), TestItem(value=3, text='test'),
                     TestItem(value=5, text='test'), TestItem(value=6, text='test'), TestItem(value=8, text='test'),
                     TestItem(value=9, text='test')]
        sequence2 = [TestItem(value=1, text='test'), TestItem(value=2, text='test'), TestItem(value=4, text='test'),
                     TestItem(value=6, text='test'), TestItem(value=7, text='test'), TestItem(value=8, text='test'),
                     TestItem(value=9, text='test')]
        deltas = Formatter.create_delta(sequence1, sequence2)
        applied = Formatter.apply_deltas(sequence1, deltas)

        self.assertEqual(sequence2, applied)
