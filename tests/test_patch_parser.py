from unittest import TestCase

from src.listdiffer.differ import apply_deltas
from src.listdiffer.patch_parser import parse_patch


class ParseTests(TestCase):
    def test_single_delta(self):
        patch = """diff
@@ -4,1 +4,1 @@
    line2
    line3
    line4
+   lineX
-   line5
    line6
    line7
    line8
"""
        deltas = parse_patch(patch)
        self.assertEqual(1, len(deltas))

    def test_multiple_deltas(self):
        patch = """diff
@@ -4,1 +4,1 @@
    line2
    line3
    line4
+   lineX
-   line5
    line6
    line7
    line8
@@ -8,1 +8,1 @@
    line6
    line7
    line8
+   lineY
-   line9
    line10
"""
        deltas = parse_patch(patch)
        self.assertEqual(2, len(deltas))

    def test_apply_delta(self):
        patch = """diff
@@ -2,1 +2,1 @@
    line1
    line2
+   lineX
-   line3
"""
        text1 = """line1
line2
line3"""
        text2 = """line1
line2
lineX"""

        deltas = parse_patch(patch)
        result = '\n'.join(apply_deltas(text1.split('\n'), deltas))

        self.assertEqual(text2, result)
