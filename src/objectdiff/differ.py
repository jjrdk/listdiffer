import typing
from dataclasses import dataclass

T = typing.TypeVar('T')


@dataclass(frozen=True)
class Delta(typing.Generic[T]):
    """Describes a difference between two compared items"""
    start_source: int
    """Indicates the start (0 based) of the difference in the source item."""
    start_compared: int
    """Indicates the start (0 based) of the difference in the compared item."""
    deleted_source: int
    """Indicates the amount of items are detected as deleted in the source item."""
    inserted_compared: int
    """Indicates the amount of items are detected as inserted in the compared item."""
    added: list[T]
    """Contains the added items at the diff location."""


class _DiffData:
    def __init__(self, data: list[int]):
        self.data: list[int] = data
        self.len: int = len(data)
        self.modified: list[bool] = [False] * (self.len + 2)


def diff_text(text_source: str, text_compared: str, trim_space: bool = False, ignore_space: bool = False) \
        -> list[Delta[chr]]:
    """
    Calculates the difference between two strings using the longest common sequence algorithm.

    :param text_source: The text to compare against
    :param text_compared: The text to compare
    :param trim_space: True if the texts should be trimmed
    :param ignore_space: True if the texts should be compared ignoring spaces in the text
    :return: A list of Delta[chr] describing the differences
    """
    def convert(text: str) -> list[int]:
        return [ord(c) for c in text if (True if c != ' ' else not ignore_space)]
    if trim_space:
        text_source = text_source.strip()
        text_compared = text_compared.strip()
    source_chars = convert(text_source)
    compare_chars = convert(text_compared)
    d: list[Delta[int]] = diff(source_chars, compare_chars)
    return list(map(lambda x: Delta(x.start_source,
                                    x.start_compared,
                                    x.deleted_source,
                                    x.inserted_compared,
                                    list(map(lambda y: chr(y), x.added))), d))


def diff(source: list[T], compared: list[T]) -> list[Delta[T]]:
    """
    Calculates the difference between two lists of objects using the longest common sequence algorithm.

    :param source: The list to compare against
    :param compared: The list to compare
    :return: A list of DiffEntry describing the differences
    """
    h: typing.Dict[T, int] = dict()
    diff_data1 = _DiffData(_diff_items(source, h))
    diff_data2 = _DiffData(_diff_items(compared, h))
    h.clear()
    num = diff_data1.len + diff_data2.len + 1
    down_vector = [0] * (2 * num + 2)
    up_vector = [0] * (2 * num + 2)
    _lcs(diff_data1, 0, diff_data1.len, diff_data2, 0, diff_data2.len, down_vector, up_vector)
    _optimize(diff_data1)
    _optimize(diff_data2)
    return _create_diffs(diff_data1, diff_data2, compared)


def apply_deltas(source: list[T], deltas: list[Delta[T]]) -> list[T]:
    """
    Applies deltas to a list of items to create an updated list.

    :param source: The source list to update with the deltas.
    :param deltas: The deltas to apply to the source list.
    :return: An updated list with the deltas applied.
    """
    position = 0
    output = []
    for delta in deltas:
        take = (delta.start_source - position)
        output.extend(source[position:take + position])
        output.extend(delta.added)
        position = delta.start_source + delta.deleted_source
    output.extend(source[position:])
    return output


def _optimize(data: _DiffData) -> None:
    index1 = 0
    while index1 < data.len:
        while index1 < data.len and not data.modified[index1]:
            index1 += 1

        index2 = index1
        while index2 < data.len and data.modified[index2]:
            index2 += 1

        if index2 < data.len and data.data[index1] == data.data[index2]:
            data.modified[index1] = False
            data.modified[index2] = True
        else:
            index1 = index2


def _sms(data_a: _DiffData, lower_a: int, upper_a: int, data_b: _DiffData, lower_b: int, upper_b: int,
         down_vector: list[int],
         up_vector: list[int]) -> tuple[int, int]:
    num1 = data_a.len + data_b.len + 1
    num2 = lower_a - lower_b
    num3 = upper_a - upper_b
    flag = (upper_a - lower_a - (upper_b - lower_b) & 1) > 0
    num4 = num1 - num2
    num5 = num1 - num3
    num6 = (upper_a - lower_a + upper_b - lower_b) // 2 + 1
    down_vector[num4 + num2 + 1] = lower_a
    up_vector[num5 + num3 - 1] = upper_a
    for index1 in range(num6 + 1):
        num7 = num2 - index1
        while num7 <= num2 + index1:
            if num7 == num2 - index1:
                index2 = down_vector[num4 + num7 + 1]
            else:
                index2 = down_vector[num4 + num7 - 1] + 1
                if num7 < num2 + index1 and down_vector[num4 + num7 + 1] >= index2:
                    index2 = down_vector[num4 + num7 + 1]

            index3 = index2 - num7
            while index2 < upper_a and index3 < upper_b and data_a.data[index2] == data_b.data[index3]:
                index2 += 1
                index3 += 1

            down_vector[num4 + num7] = index2
            if flag and num3 - index1 < num7 < num3 + index1 and up_vector[num5 + num7] <= down_vector[num4 + num7]:
                return down_vector[num4 + num7], down_vector[num4 + num7] - num7

            num7 += 2

        num8 = num3 - index1
        while num8 <= num3 + index1:
            if num8 == num3 + index1:
                num9 = up_vector[num5 + num8 - 1]
            else:
                num9 = up_vector[num5 + num8 + 1] - 1
                if num8 > num3 - index1 and up_vector[num5 + num8 - 1] < num9:
                    num9 = up_vector[num5 + num8 - 1]

            index2 = num9 - num8
            while num9 > lower_a and index2 > lower_b and data_a.data[num9 - 1] == data_b.data[index2 - 1]:
                num9 -= 1
                index2 -= 1

            up_vector[num5 + num8] = num9
            if not flag and num2 - index1 <= num8 <= num2 + index1 and up_vector[num5 + num8] <= down_vector[
                num4 + num8]:
                return down_vector[num4 + num8], down_vector[num4 + num8] - num8

            num8 += 2

    raise Exception("the algorithm should never come here.")


def _lcs(data_a: _DiffData, lower_a: int, upper_a: int, data_b: _DiffData, lower_b: int, upper_b: int,
         down_vector: list[int], up_vector: list[int]) -> None:
    while lower_a < upper_a and lower_b < upper_b and data_a.data[lower_a] == data_b.data[lower_b]:
        lower_a += 1
        lower_b += 1

    while lower_a < upper_a and lower_b < upper_b and data_a.data[upper_a - 1] == data_b.data[upper_b - 1]:
        upper_a -= 1
        upper_b -= 1

    if lower_a == upper_a:
        while lower_b < upper_b:
            data_b.modified[lower_b] = True
            lower_b += 1
    elif lower_b == upper_b:
        while lower_a < upper_a:
            data_a.modified[lower_a] = True
            lower_a += 1
    else:
        x, y = _sms(data_a, lower_a, upper_a, data_b, lower_b, upper_b, down_vector, up_vector)
        _lcs(data_a, lower_a, x, data_b, lower_b, y, down_vector, up_vector)
        _lcs(data_a, x, upper_a, data_b, y, upper_b, down_vector, up_vector)


def _create_diffs(data_a: _DiffData, data_b: _DiffData, other: list[T]) -> list[Delta[T]]:
    diff_entries = []
    index1 = 0
    index2 = 0
    while index1 < data_a.len or index2 < data_b.len:
        if index1 < data_a.len and not data_a.modified[index1] and index2 < data_b.len and not data_b.modified[index2]:
            index1 += 1
            index2 += 1
        else:
            num1 = index1
            num2 = index2
            while index1 < data_a.len and (index2 >= data_b.len or data_a.modified[index1]):
                index1 += 1
            while index2 < data_b.len and (index1 >= data_a.len or data_b.modified[index2]):
                index2 += 1
            if num1 < index1 or num2 < index2:
                inserted_compared = index2 - num2
                diff_entries.append(Delta(num1, num2, index1 - num1, inserted_compared,
                                          other[num2: num2 + inserted_compared]))
    return diff_entries


def _diff_items(source: list[T], h: typing.Dict[T, int]) -> list[int]:
    count = len(h)
    source_length = len(source)
    num_array = [0] * source_length
    for i in range(source_length):
        index2 = source[i]

        if index2 not in h:
            count += 1
            h[index2] = count
            num_array[i] = count
        else:
            num_array[i] = h[index2]

    return num_array
