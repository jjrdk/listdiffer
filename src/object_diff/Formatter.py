from typing import TypeVar

from src.object_diff.DiffEntry import DiffEntry
from src.object_diff.Compared import Compared, Change
from src.object_diff.Delta import Delta
from src.object_diff.DiffCalculator import DiffCalculator

T = TypeVar('T')


class Formatter:
    @staticmethod
    def format(diffs: list[DiffEntry], source, other) -> list[Compared]:
        result_lines = []

        for x in range(len(diffs)):
            item = Formatter.add_untouched_lines(diffs, x, source, result_lines)
            Formatter.add_deleted_lines(item, source, result_lines)
            Formatter.add_inserted_lines(item, other, result_lines)

        return result_lines

    @staticmethod
    def create_delta(source: list[T], other: list[T]) -> list[Delta[T]]:
        span = DiffCalculator.diff(source, other)
        result: list[Delta[T]] = [None] * len(span)
        for i in range(len(span)):
            diff_entry = span[i]
            result[i] = Delta(diff_entry, other[diff_entry.start_compared: diff_entry.start_compared + diff_entry.inserted_compared])
        return result

    @staticmethod
    def apply_deltas(source: list[T], diff: list[Delta[T]]):
        position = 0
        output = []
        for delta in diff:
            take = (delta.diff.start_source - position)
            output.extend(source[position:take+position])
            output.extend(delta.added)
            position = delta.diff.start_source + delta.diff.deleted_source
        output.extend(source[position:])
        return output

    @staticmethod
    def add_untouched_lines(diffs: list[DiffEntry], x: int, lines: list[T], result_lines: list[Compared[T]]):
        item = diffs[x]
        offset = 0 if x == 0 else diffs[x - 1].start_source + diffs[x - 1].deleted_source
        count = item.start_source - offset
        span = lines[offset:offset + count]
        for t in span:
            result_lines.append(Compared(t, Change.UNCHANGED))
        return item

    @staticmethod
    def add_deleted_lines(diff_entry: DiffEntry, lines, result_lines):
        span = lines[diff_entry.start_source - 1: diff_entry.start_source - 1 + diff_entry.deleted_source]
        for t in span:
            result_lines.append(Compared(t, Change.REMOVED))

    @staticmethod
    def add_inserted_lines(diff_entry: DiffEntry, lines: list[T], result_lines: list[Compared[T]]):
        span = lines[diff_entry.start_compared - 1: diff_entry.start_compared - 1 + diff_entry.inserted_compared]
        for t in span:
            result_lines.append(Compared(t, Change.ADDED))
