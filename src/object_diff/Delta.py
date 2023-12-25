from dataclasses import dataclass
from typing import TypeVar, Generic

from src.object_diff import DiffEntry

T = TypeVar('T')


@dataclass
class Delta(Generic[T]):
    diff: DiffEntry
    added: list[T]
