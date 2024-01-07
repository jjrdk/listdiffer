import re
from typing import List

from src.listdiffer.differ import Delta


def parse_patch(patch: str) -> List[Delta[str]]:
    regex = r'@@ -(?P<start_delete>\d+),(?P<lines_deleted>\d+) \+(?P<start_insert>\d+),(?P<lines_inserted>\d+) @@'
    patches = []
    delta: Delta[str] | None = None
    for line in patch.splitlines():
        if line.startswith('@@'):
            if delta:
                patches.append(delta)
            match = re.match(regex, line)
            if match:
                start_delete = int(match.group('start_delete'))
                lines_deleted = int(match.group('lines_deleted'))
                start_insert = int(match.group('start_insert'))
                lines_inserted = int(match.group('lines_inserted'))
                delta = Delta(start_delete, lines_deleted, start_insert, lines_inserted, [])
        elif line.startswith('+'):
            delta.added.append(line[4:])

    if delta:
        patches.append(delta)

    return patches
