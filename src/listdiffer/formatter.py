from enum import Enum
from typing import TypeVar, Generic, List, Tuple
from listdiffer.differ import diff, Delta

T = TypeVar('T')

START_DEL = "<del>"
END_DEL = "</del>"
START_BOLD = "<ins>"
END_BOLD = "</ins>"
LINEBREAK = "<br/>"


class Change(Enum):
    """Defines the different types of changes"""
    UNCHANGED = 0
    """Item is unchanged between the two Lists."""
    ADDED = 1
    """Item is added to the compared List."""
    REMOVED = 2
    """Item is removed from the source List."""


class Compared(Generic[T]):
    """Defines the comparison of an item against a base List"""

    def __init__(self, item: T, change: Change):
        self.item: T = item
        self.change: Change = change


def format_items(diffs: List[Delta], source: List[T], other: List[T]) -> List[Compared]:
    """
    Generates a List of comparisons of the items in the other List compared to the source List.

    :param diffs: The List of differences between the two Lists.
    :param source: The source List.
    :param other: The compared List.
    :return: A List of Compared objects describing the differences.
    """
    result_lines: List[Compared[T]] = []

    for x in range(len(diffs)):
        item = _add_untouched_lines(diffs, x, source, result_lines)
        _add_deleted_lines(item, source, result_lines)
        _add_inserted_lines(item, other, result_lines)

    return result_lines


def format_diff_text_as_patch(source: str, comparison: str, comment: str | None = None, padding: int = 3) -> str:
    """
    Outputs the difference between the strings as a patch string.

    :param source: The source string
    :param comparison: The comparison string
    :param comment: A comment to add to the patch.
    :param padding: The number of lines to include before and after the change.
    :return: A patch formatted string.
    """
    text1_lines = source.split('\n')
    text2_lines = comparison.split('\n')

    return format_diff_as_patch(text1_lines, text2_lines, comment, padding)


def format_diff_as_patch(source: List[T], compared: List[T], comment: str | None = None, padding: int = 3) -> str:
    """
    Outputs the difference between the Lists as a patch string.

    :param source: The source List
    :param compared: The comparison List
    :param comment: A comment to add to the patch.
    :param padding: The number of lines to include before and after the change.
    :return: A patch formatted string.
    """
    padding = max(0, padding)
    deltas = diff(source, compared)
    result = 'Subject: [PATCH] {}\n---\n'.format(comment) if comment is not None else ''
    result += 'diff\n'

    for delta in deltas:
        start = max(0, delta.start_source - padding)
        result += '@@ -{},{} +{},{} @@\n'.format(delta.start_source,
                                                 delta.deleted_source,
                                                 delta.start_compared,
                                                 delta.inserted_compared)
        result += '\n'.join(map(lambda s: '    {}'.format(s), source[start:delta.start_source]))
        result += '\n'
        result += '\n'.join(map(lambda s: '+   {}'.format(s), delta.added))
        result += '\n'
        deleted_rows = delta.start_source + delta.deleted_source
        result += '\n'.join(
            map(lambda s: '-   {}'.format(s),
                source[delta.start_source: deleted_rows]))
        result += '\n'
        trailing_start = delta.start_source + delta.deleted_source
        trailing_rows = min(padding, len(source) - deleted_rows)
        if trailing_rows > 0:
            result += '\n'.join(
                map(lambda s: '    {}'.format(s), source[trailing_start:trailing_start + trailing_rows]))
            result += '\n'

    return result


def format_diff_text_as_html(source: str, compared: str,
                             add_formatter: Tuple[str, str] = (START_BOLD, END_BOLD),
                             remove_formatter: Tuple[str, str] = (START_DEL, END_DEL)) -> str:
    """
        Outputs the difference between the strings as an HTML string.

        :param source: The source List
        :param compared: The comparison List
        :param add_formatter: A function producing the HTML tags for added items.
        :param remove_formatter: A function producing the HTML tags for removed items.
        :return: An HTML formatted string.
        """

    def clean(x):
        return x.rstrip('\r')

    text1_lines = List(map(clean, source.split('\n')))
    text2_lines = List(map(clean, compared.split('\n')))

    return format_diff_as_html(text1_lines, text2_lines, add_formatter, remove_formatter)


def format_diff_as_html(source: List[T], compared: List[T],
                        add_formatter: Tuple[str, str] = (START_BOLD, END_BOLD),
                        remove_formatter: Tuple[str, str] = (START_DEL, END_DEL)) -> str:
    """
    Outputs the difference between the Lists as an HTML string.

    :param source: The source List
    :param compared: The comparison List
    :param add_formatter: A function producing the HTML tags for added items.
    :param remove_formatter: A function producing the HTML tags for removed items.
    :return: An HTML formatted string.
    """
    deltas = diff(source, compared)
    result_lines: List[str] = []

    for x in range(len(deltas)):
        item = _write_untouched_lines(deltas, x, source, result_lines)
        _write_deleted_lines(item, source, result_lines, remove_formatter)
        _write_inserted_lines(item, compared, add_formatter, result_lines)

    return '\n'.join(result_lines)


def _emphasize() -> Tuple[str, str]:
    return START_BOLD, END_BOLD


def _delete() -> Tuple[str, str]:
    return START_DEL, END_DEL


def _write_inserted_lines(diff_entry: Delta[T], text2_lines: List[T], add_formatting: Tuple[str, str],
                          result_lines: List[str]):
    (start, end) = add_formatting
    if diff_entry.inserted_compared <= 0:
        return

    range_lines = text2_lines[diff_entry.start_compared: diff_entry.start_compared + diff_entry.inserted_compared]
    for line in range_lines:
        result_lines.append(start)
        result_lines.append("{}".format(line))
        result_lines.append(end)


def _write_untouched_lines(deltas: List[Delta[T]], x: int, text1_lines: List[T], result_lines: List[str]):
    item = deltas[x]
    offset = 0 if x == 0 else deltas[x - 1].start_source + deltas[x - 1].deleted_source
    count = item.start_source - offset
    untouched = text1_lines[offset:offset + count]
    for line in untouched:
        result_lines.append("{}".format(line))
        result_lines.append(LINEBREAK)
    return item


def _write_deleted_lines(diff_entry: Delta[T], text1_lines, result_lines, remove_formatting: Tuple[str, str]):
    (start, end) = remove_formatting
    for i in range(diff_entry.deleted_source):
        line = text1_lines[diff_entry.start_source + i]
        result_lines.append(start)
        result_lines.append("{}".format(line))
        result_lines.append(end)
    result_lines.append(LINEBREAK)


def _add_inserted_lines(diff_entry: Delta, lines: List[T], result_lines: List[Compared[T]]) -> None:
    span = lines[diff_entry.start_compared - 1: diff_entry.start_compared - 1 + diff_entry.inserted_compared]
    result_lines.extend(map(lambda t: Compared(t, Change.ADDED), span))


def _add_deleted_lines(diff_entry: Delta, lines: List[T], result_lines: List[Compared[T]]) -> None:
    span = lines[diff_entry.start_source - 1: diff_entry.start_source - 1 + diff_entry.deleted_source]
    result_lines.extend(map(lambda t: Compared(t, Change.REMOVED), span))


def _add_untouched_lines(diffs: List[Delta], x: int, lines: List[T], result_lines: List[Compared[T]]):
    item = diffs[x]
    offset = 0 if x == 0 else diffs[x - 1].start_source + diffs[x - 1].deleted_source
    count = item.start_source - offset
    span = lines[offset:offset + count]
    result_lines.extend(map(lambda t: Compared(t, Change.UNCHANGED), span))
    return item
