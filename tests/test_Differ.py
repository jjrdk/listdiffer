from unittest import TestCase
from src.listdiffer.differ import diff, diff_text, apply_deltas
from tests.TestItem import TestItem


class TestDiffer(TestCase):
    def test_equal_text(self):
        source = "some text"
        compare = "some text"
        result = diff_text(source, compare)
        self.assertEqual(0, len(result))

    def test_not_equal_text(self):
        source = "some text"
        compare = "text"
        result = diff_text(source, compare)
        self.assertEqual(1, len(result))

    def test_equal_text_except_ignored_space(self):
        source = "some text"
        compare = "some      text"
        result = diff_text(source, compare, False, True)
        self.assertEqual(0, len(result))

    def test_not_equal_text_because_space(self):
        source = "some text"
        compare = "some      text"
        result = diff_text(source, compare, False, False)
        self.assertEqual(1, len(result))

    def test_equal_array(self):
        source = [1, 2, 3]
        compare = [1, 2, 3]
        result = diff(source, compare)
        self.assertEqual(0, len(result))

    def test_equal_object_array(self):
        source = [TestItem('test', 1), TestItem('test', 2), TestItem('test', 3)]
        compare = [TestItem('test', 1), TestItem('test', 2), TestItem('test', 3)]
        result = diff(source, compare)
        self.assertEqual(0, len(result))

    def test_not_equal_array(self):
        source = [1, 2, 3]
        compare = [1, 2, 3, 4]
        result = diff(source, compare)
        self.assertEqual(1, len(result))

    def test_not_equal_object_array(self):
        source = [TestItem('test', 1), TestItem('test', 2), TestItem('test', 3)]
        compare = [TestItem('test', 1), TestItem('test', 2), TestItem('test', 3), TestItem('test', 4)]
        result = diff(source, compare)
        self.assertEqual(1, len(result))

    def test_apply_deltas(self):
        sequence1 = [1, 2, 3, 5, 6, 8, 9]
        sequence2 = [1, 2, 4, 6, 7, 8, 9]
        deltas = diff(sequence1, sequence2)
        applied = apply_deltas(sequence1, deltas)

        self.assertEqual(sequence2, applied)

    def test_apply_deltas_item(self):
        sequence1 = [TestItem(value=1, text='test'), TestItem(value=2, text='test'), TestItem(value=3, text='test'),
                     TestItem(value=5, text='test'), TestItem(value=6, text='test'), TestItem(value=8, text='test'),
                     TestItem(value=9, text='test')]
        sequence2 = [TestItem(value=1, text='test'), TestItem(value=2, text='test'), TestItem(value=4, text='test'),
                     TestItem(value=6, text='test'), TestItem(value=7, text='test'), TestItem(value=8, text='test'),
                     TestItem(value=9, text='test')]
        deltas = diff(sequence1, sequence2)
        applied = apply_deltas(sequence1, deltas)

        self.assertEqual(sequence2, applied)
