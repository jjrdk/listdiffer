from enum import Enum
from typing import TypeVar, Generic
from src.object_diff.differ import diff, Delta

T = TypeVar('T')

START_DEL = "<del>"
END_DEL = "</del>"
START_BOLD = "<b>"
END_BOLD = "</b>"
LINEBREAK = "<br/>"


class Change(Enum):
    """Defines the different types of changes"""
    UNCHANGED = 0
    ADDED = 1
    REMOVED = 2


class Compared(Generic[T]):
    """Defines the comparison of an item against a base list"""
    def __init__(self, item: T, change: Change):
        self.item: T = item
        self.change: Change = change


def format_items(diffs: list[Delta], source: list[T], other: list[T]) -> list[Compared]:
    """
    Generates a list of comparisons of the items in the other list compared to the source list.

    :param diffs: The list of differences between the two lists.
    :param source: The source list.
    :param other: The compared list.
    :return: A list of Compared objects describing the differences.
    """
    result_lines = []

    for x in range(len(diffs)):
        item = _add_untouched_lines(diffs, x, source, result_lines)
        _add_deleted_lines(item, source, result_lines)
        _add_inserted_lines(item, other, result_lines)

    return result_lines


def format_diff_text_as_html(a: str, b: str,
                             add_formatter: lambda: (str, str) = None,
                             remove_formatter: lambda: (str, str) = None) -> str:
    text1_lines = list(map(lambda x: x.rstrip('\r'), a.split('\n')))
    text2_lines = list(map(lambda x: x.rstrip('\r'), b.split('\n')))

    return format_diff_as_html(text1_lines, text2_lines, add_formatter, remove_formatter)


def format_diff_as_html(source: list[T], compared: list[T],
                        add_formatter: lambda: (str, str) = None,
                        remove_formatter: lambda: (str, str) = None) -> str:
    """
    Outputs the difference between the lists as an HTML string.

    :param source: The source list
    :param compared: The comparison list
    :param add_formatter: A function producing the HTML tags for added items.
    :param remove_formatter: A function producing the HTML tags for removed items.
    :return: An HTML formatted string.
    """
    add_tuple: (str, str) = _emphasize() if add_formatter is None else add_formatter()
    remove_tuple: (str, str) = _delete() if remove_formatter is None else remove_formatter()
    deltas = diff(source, compared)
    result_lines = []

    for x in range(len(deltas)):
        item = _write_untouched_lines(deltas, x, source, result_lines)
        _write_deleted_lines(item, source, result_lines, remove_tuple)
        _write_inserted_lines(item, compared, add_tuple, result_lines)

    return ''.join(result_lines)


def _emphasize() -> (str, str):
    return START_BOLD, END_BOLD


def _delete() -> (str, str):
    return START_DEL, END_DEL


def _write_inserted_lines(diff_entry: Delta[T], text2_lines: list[T], add_formatting: (str, str),
                          result_lines: list[str]):
    if diff_entry.inserted_compared <= 0:
        return

    range_lines = text2_lines[diff_entry.start_compared: diff_entry.start_compared + diff_entry.inserted_compared]
    for line in range_lines:
        result_lines.append(add_formatting[0])
        result_lines.append("{}".format(line))
        result_lines.append(add_formatting[1])


def _write_untouched_lines(deltas: list[Delta[T]], x: int, text1_lines: list[T], result_lines: list[str]):
    item = deltas[x]
    offset = 0 if x == 0 else deltas[x - 1].start_source + deltas[x - 1].deleted_source
    count = item.start_source - offset
    untouched = text1_lines[offset:offset + count]
    for line in untouched:
        result_lines.append("{}".format(line))
        result_lines.append(LINEBREAK)
    return item


def _write_deleted_lines(diff_entry: Delta[T], text1_lines, result_lines, remove_formatting: (str, str)):
    for i in range(diff_entry.deleted_source):
        line = text1_lines[diff_entry.start_source + i]
        result_lines.append(remove_formatting[0])
        result_lines.append("{}".format(line))
        result_lines.append(remove_formatting[1])
    result_lines.append(LINEBREAK)


def _add_inserted_lines(diff_entry: Delta, lines: list[T], result_lines: list[Compared[T]]) -> None:
    span = lines[diff_entry.start_compared - 1: diff_entry.start_compared - 1 + diff_entry.inserted_compared]
    result_lines.extend(map(lambda t: Compared(t, Change.ADDED), span))


def _add_deleted_lines(diff_entry: Delta, lines: list[T], result_lines: list[Compared[T]]) -> None:
    span = lines[diff_entry.start_source - 1: diff_entry.start_source - 1 + diff_entry.deleted_source]
    result_lines.extend(map(lambda t: Compared(t, Change.REMOVED), span))


def _add_untouched_lines(diffs: list[Delta], x: int, lines: list[T], result_lines: list[Compared[T]]):
    item = diffs[x]
    offset = 0 if x == 0 else diffs[x - 1].start_source + diffs[x - 1].deleted_source
    count = item.start_source - offset
    span = lines[offset:offset + count]
    result_lines.extend(map(lambda t: Compared(t, Change.UNCHANGED), span))
    return item
