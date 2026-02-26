---
name: python-patterns
version: 0.1.0
user-invocable: true
description: >-
  This skill should be used when the user asks to "write idiomatic Python",
  "review Python code", "refactor Python", "follow PEP 8", "use type hints",
  "write Pythonic code", or when writing, reviewing, designing, or refactoring
  Python applications. Provides patterns for readability, correctness, and
  maintainability.
---

# Python Development Patterns

Idiomatic Python patterns and best practices for building robust, efficient, and maintainable applications.

## When to Activate

- Writing new Python code
- Reviewing Python code for quality and idioms
- Refactoring existing Python code
- Designing Python packages or modules

## Core Principles

### 1. Readability Counts

Prioritize clarity. Code should be obvious to the next reader.

```python
# Good: Clear and readable
def get_active_users(users: list[User]) -> list[User]:
    return [user for user in users if user.is_active]

# Bad: Clever but confusing
def get_active_users(u):
    return [x for x in u if x.a]
```

### 2. Explicit Over Implicit

Avoid magic; make intent clear.

```python
# Good: Explicit configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Bad: Hidden side effects
some_module.setup()  # What does this do?
```

### 3. EAFP — Easier to Ask Forgiveness than Permission

Prefer exception handling over precondition checks.

```python
# Good: EAFP style
try:
    return dictionary[key]
except KeyError:
    return default_value

# Bad: LBYL (Look Before You Leap)
if key in dictionary:
    return dictionary[key]
return default_value
```

## Quick Reference: Python Idioms

| Idiom | Description |
|-------|-------------|
| EAFP | Easier to ask forgiveness than permission |
| Context managers | Use `with` for resource management |
| List comprehensions | For simple transformations |
| Generators | For lazy evaluation and large datasets |
| Type hints | Annotate function signatures |
| Dataclasses | For data containers with auto-generated methods |
| `__slots__` | For memory optimization |
| f-strings | For string formatting (Python 3.6+) |
| `pathlib.Path` | For path manipulation (Python 3.4+) |
| `enumerate` | For index-element pairs in loops |

## Anti-Patterns to Avoid

```python
# Bad: Mutable default arguments
def append_to(item, items=[]):  # Shared across calls!
    items.append(item)
    return items

# Good: Use None sentinel
def append_to(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

```python
# Bad: Bare except
try:
    risky_operation()
except:
    pass  # Silent failure!

# Good: Specific exception
try:
    risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
```

```python
# Bad: type() for type checking    # Bad: Comparing to None with ==
if type(obj) == list: ...           if value == None: ...

# Good: isinstance / identity       # Good: Use is
if isinstance(obj, list): ...       if value is None: ...
```

```python
# Bad: Wildcard imports
from os.path import *

# Good: Explicit imports
from os.path import join, exists
```

## Reference Documentation

Detailed patterns and examples for each topic:

- **Type Hints** — [references/type-hints.md](references/type-hints.md) — Basic, modern 3.9+, TypeVar, Protocol
- **Error Handling** — [references/error-handling.md](references/error-handling.md) — Specific exceptions, chaining, custom hierarchies
- **Context Managers** — [references/context-managers.md](references/context-managers.md) — Resource management, @contextmanager, class-based
- **Comprehensions & Generators** — [references/comprehensions-generators.md](references/comprehensions-generators.md) — List comps, generator expressions, generator functions
- **Dataclasses & NamedTuples** — [references/dataclasses-namedtuples.md](references/dataclasses-namedtuples.md) — Validation, immutability, NamedTuple
- **Decorators** — [references/decorators.md](references/decorators.md) — Function, parameterized, class-based
- **Concurrency** — [references/concurrency.md](references/concurrency.md) — Threads, multiprocessing, async/await
- **Package Organization** — [references/package-organization.md](references/package-organization.md) — Project layout, imports, __init__.py
- **Performance** — [references/performance.md](references/performance.md) — __slots__, generators, string optimization
- **Tooling & Configuration** — [references/tooling-config.md](references/tooling-config.md) — black, ruff, mypy, pytest, pyproject.toml

**Remember**: Python code should be readable, explicit, and follow the principle of least surprise. When in doubt, prefer clarity over cleverness.
