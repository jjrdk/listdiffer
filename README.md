# List Differ

Version: 0.2.0

Calculates longest common sequence on text, lists of numbers or characters, or lists of objects.

When comparing objects, make sure that the objects are hashable, i.e. override the `__hash()__` method of the class.
It is also a good idea to override the `__eq()__` method if you have some custom logic for comparing items.
This could be the case if your business logic considers close values as similar.

If you want to compare two strings ignoring casing, then simply call `lower` on each string before passing as argument.

## Examples

### Example 1 - Strings

Calculate a diff between two strings

#### Same strings

```python
from listdiffer import differ

first = 'string'
second = 'string'
diff = differ.diff_text(first, second, False, False)

assert len(diff) == 0
```

#### Different strings

```python
from listdiffer import differ

first = 'first string'
second = 'second string'
diff = differ.diff_text(first, second, False, False)

assert len(diff) == 1
```

### Example 2 - List of integers

Calculate a diff between two strings

#### Same lists

```python
from listdiffer import differ

first = [1, 2, 3]
second = [1, 2, 3]
d = differ.diff(first, second)

assert len(d) == 0
```

#### Different lists

```python
from listdiffer import differ

first = [1, 2, 3]
second = [1, 2, 4]
d = differ.diff(first, second)

assert len(d) == 1
```

## Example 3 - Lists of objects

### Same lists

```python
from listdiffer import differ

@dataclass
class TestItem:
    text: str
    value: int

    def __eq__(self, other):
        return self.text == other.text and self.value == other.value

    def __hash__(self):
        return hash((self.text, self.value))

source = [TestItem('test', 1), TestItem('test', 2), TestItem('test', 3)]
compare = [TestItem('test', 1), TestItem('test', 2), TestItem('test', 3)]
result = differ.diff(source, compare)

assert len(result) == 0
```

### Different lists

```python
from listdiffer import differ

@dataclass
class TestItem:
    text: str
    value: int

    def __eq__(self, other):
        return self.text == other.text and self.value == other.value

    def __hash__(self):
        return hash((self.text, self.value))

source = [TestItem('test', 1), TestItem('test', 2), TestItem('test', 3)]
compare = [TestItem('test', 1), TestItem('test', 2), TestItem('test', 3), TestItem('test', 4)]
result = differ.diff(source, compare)

assert len(result) == 1
```
