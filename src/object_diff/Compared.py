import typing
from enum import Enum

T = typing.TypeVar('T')


class Change(Enum):
    UNCHANGED = 0
    ADDED = 1
    REMOVED = 2


class Compared(typing.Generic[T]):
    def __init__(self, item: T, change: Change):
        self.item = item
        self.change = change
