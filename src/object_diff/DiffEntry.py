from dataclasses import dataclass


@dataclass
class DiffEntry:
    start_source: int
    start_compared: int
    deleted_source: int
    inserted_compared: int
