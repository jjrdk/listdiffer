# List Differ

Version: 0.2.0

## Description

Calculates longest common sequence on text, lists of numbers or characters, or lists of objects.

When comparing objects, make sure that the objects are hashable, i.e. override the `__hash()__` method of the class.
It is also a good idea to override the `__eq()__` method if you have some custom logic for comparing items.
This could be the case if your business logic considers close values as similar.

If you want to compare two strings ignoring casing, then simply call `lower` on each string before passing as argument.

## Patch String Generation

The `format_diff_text_as_patch`, or the companion `format_diff_as_patch`, function can be used to generate a patch string 
from the diff result.

The patch string can be used to patch the first string to the second string. It can also be persisted and used later to 
patch the original string, thereby serving as a change log.

The patch string can be read back to a `List[Delta[str]]` using the `parse_patch_text` function in the `patch_parser` module.

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

### Example 4 - Patch string generation

    ```python
text1 = """line1
line2
line3"""
        text2 = """line1
line2
lineX"""

        patch = format_diff_text_as_patch(text1, text2)

        assert """diff
@@ -2,1 +2,1 @@
    line1
    line2
+   lineX
-   line3
""" == patch
```