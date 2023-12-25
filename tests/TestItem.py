from dataclasses import dataclass


@dataclass
class TestItem:
    text: str
    value: int

    def __eq__(self, other):
        return self.text == other.text and self.value == other.value

    def __hash__(self):
        return hash(self.text + self.value.__str__())
