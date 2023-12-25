import typing

from src.object_diff.DiffData import DiffData
from src.object_diff.DiffEntry import DiffEntry

T = typing.TypeVar('T')


class DiffCalculator:
    @staticmethod
    def diff(text_source: list[T], text_compared: list[T]) -> list[DiffEntry]:
        h = dict()
        diff_data1 = DiffData(DiffCalculator.diff_items(text_source, h))
        diff_data2 = DiffData(DiffCalculator.diff_items(text_compared, h))
        h.clear()
        num = diff_data1.len + diff_data2.len + 1
        down_vector = [0] * (2 * num + 2)
        up_vector = [0] * (2 * num + 2)
        DiffCalculator.lcs(diff_data1, 0, diff_data1.len, diff_data2, 0, diff_data2.len, down_vector, up_vector)
        DiffCalculator.optimize(diff_data1)
        DiffCalculator.optimize(diff_data2)
        return DiffCalculator.create_diffs(diff_data1, diff_data2)

    @staticmethod
    def diff_text(text_source: str, text_compared: str, trim_space: bool = False, ignore_space: bool = False) -> list[DiffEntry]:
        if trim_space:
            text_source = text_source.strip()
            text_compared = text_compared.strip()
        source_chars = [ord(c) for c in text_source.strip() if c != ' ' and ignore_space]
        compare_chars = [ord(c) for c in text_compared if c != ' ' and ignore_space]
        return DiffCalculator.diff(source_chars, compare_chars)

    @staticmethod
    def diff_items(source: list[T], h: typing.Dict[T, int]) -> list[int]:
        count = len(h)
        num_array = [0] * len(source)
        for i in range(len(source)):
            index2 = source[i]

            if index2 not in h:
                count += 1
                h[index2] = count
                num_array[i] = count
            else:
                num_array[i] = h[index2]

        return num_array

    @staticmethod
    def optimize(data: DiffData) -> None:
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

    @staticmethod
    def sms(data_a: DiffData, lower_a: int, upper_a: int, data_b: DiffData, lower_b: int, upper_b: int,
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
                if not flag and num2 - index1 <= num8 <= num2 + index1 and up_vector[num5 + num8] <= down_vector[num4 + num8]:
                    return down_vector[num4 + num8], down_vector[num4 + num8] - num8

                num8 += 2

        raise Exception("the algorithm should never come here.")

    @staticmethod
    def lcs(data_a: DiffData, lower_a: int, upper_a: int, data_b: DiffData, lower_b: int, upper_b: int,
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
            x, y = DiffCalculator.sms(data_a, lower_a, upper_a, data_b, lower_b, upper_b, down_vector, up_vector)
            DiffCalculator.lcs(data_a, lower_a, x, data_b, lower_b, y, down_vector, up_vector)
            DiffCalculator.lcs(data_a, x, upper_a, data_b, y, upper_b, down_vector, up_vector)

    @staticmethod
    def create_diffs(data_a: DiffData, data_b: DiffData) -> list[DiffEntry]:
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
                    diff_entries.append(DiffEntry(num1, num2, index1 - num1, index2 - num2))
        return diff_entries
