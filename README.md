# Object Diff

Version: 0.1.0

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
from objectdiff import differ

first = 'string'
second = 'string'
diff = differ.diff_text(first, second, False, False)

assert len(diff) == 0
```

#### Different strings

```python
from objectdiff import differ

first = 'first string'
second = 'second string'
diff = differ.diff_text(first, second, False, False)

assert len(diff) == 1
```

### Example 2 - Array of integers

Calculate a diff between two strings

#### Same arrays

```python
from objectdiff import differ

first = [1, 2, 3]
second = [1, 2, 3]
d = differ.diff(first, second)

assert len(d) == 0
```

#### Different arrays

```python
from objectdiff import differ

first = [1, 2, 3]
second = [1, 2, 4]
d = differ.diff(first, second)

assert len(d) == 1
```
