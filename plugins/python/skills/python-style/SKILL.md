---
name: python-style
description: "Write, edit, or review .py, .pyi, and pyproject.toml using house Python style unless another guide is requested."
license: CC-BY-4.0
metadata:
  kind: house
  language: python
  version: "1.0.0"
  source-url: "references/sources.md"
  treatment: original-synthesis
---

# Python style (house)

Our blend of the best Python guides, in our own words. Every rule in the full guide names its source.

Scope: Python 3.12+ applications and libraries; syntax and standard-library APIs target 3.12. Frameworks and older-runtime migrations need repository-specific additions.

If the project declares older versions or its own formatter/linter settings, follow the project and say so.

## Quick rules

- MUST install Python project dependencies and tools in an isolated project environment, never into the system interpreter or by bypassing its externally managed marker. Why: [PEP 668](https://peps.python.org/pep-0668/) protects distribution-owned Python packages. [PEP668]
- MUST use `snake_case` for modules, packages, functions, parameters, and variables, `CapWords` for classes, and `UPPER_SNAKE_CASE` for module constants. Why: Python readers recognize these roles immediately. [PEP8] [GOOGLE-PYTHON]
- MUST use absolute imports and explicit imported names; declare intentional re-exports with `__all__` or a same-name import alias. Why: import origins and public exports stay statically visible. [PEP8] [GOOGLE-PYTHON] [MYPY]
- MUST keep executable startup in `main()` behind `if __name__ == "__main__":`, without starting work during module import. Why: importing for tests or documentation must not launch the program. [GOOGLE-PYTHON]
- MUST annotate parameters and returns on application and test functions, including `-> None`; omit redundant `self` and `cls` annotations. Why: strict checking needs complete function boundaries. [GOOGLE-PYTHON] [MYPY]
- MUST use parameterized built-in containers, `X | None` for nullable values, and `type Alias = ...` for new annotation-only aliases. Why: the Python 3.12 baseline supports precise modern types. [GOOGLE-PYTHON] [PY-TYPING] [RUFF]
- PREFER `object` plus narrowing, a protocol, or a type parameter over `Any`; isolate any necessary `Any` to a documented adapter. Why: `Any` lets unchecked operations propagate. [PY-TYPING] [MYPY]
- MUST create mutable function defaults per call and mutable dataclass fields with `default_factory`; use `None` or an immutable sentinel as the parameter default. Why: defaults are otherwise shared between calls or instances. [GOOGLE-PYTHON] [RUFF]
- MUST test optional values with `is None` or `is not None` when zero, empty text, or `False` remains valid. Why: truthiness would discard valid supplied values. [PEP8] [GOOGLE-PYTHON]
- MUST distinguish `str` text from `bytes` data and specify the intended encoding when opening text files or encoding and decoding. Why: implicit conversions and locale defaults change data. [GOOGLE-PYTHON] [MYPY]
- MUST use `with`, `async with`, or `try/finally` for owned resources and avoid `__del__` for required cleanup. Why: Python finalization does not guarantee timely resource release. [PEP8] [GOOGLE-PYTHON]
- MUST catch specific exception types in narrow `try` blocks; use a broad catch only for reraising or a documented isolation boundary that records the traceback. Why: unrelated programming errors must remain visible. [PEP8] [GOOGLE-PYTHON] [RUFF]
- MUST use bare `raise` to propagate the current exception and `raise NewError(...) from error` when translating it. Why: traceback and cause information retain their intended meaning. [PEP8] [RUFF]
- MUST use explicit exceptions for runtime validation, usually `ValueError` or `TypeError`, and allow `assert` only for tests or non-critical invariants/type narrowing whose removal leaves required behavior intact. Why: optimized Python removes assertions; input validation and side effects must survive. [GOOGLE-PYTHON] [RUFF]
- MUST write Python API docstrings with a period-ended imperative function summary and Google `Args`, `Returns` or `Yields`, and `Raises` sections when needed; describe classes and properties as values. Why: callers can find the contract in a consistent form. [PEP257] [GOOGLE-PYTHON] [RUFF]
- MUST mark overridden methods with `typing.override`, except `__init__` and `__new__`; document any contract change even when the base docstring is inherited. Why: static checking catches accidental mismatches and readers see changed behavior. [GOOGLE-PYTHON] [MYPY]
- MUST name test modules `test_*.py` and test functions or methods `test_*`; keep exception assertions around only the operation expected to fail. Why: discovery and failure attribution stay reliable. [PY-UNITTEST] [GOOGLE-PYTHON] [RUFF]
- PREFER comprehensions with one `for` and at most one filter; use ordinary loops for side effects or more complex control flow. Why: compact Python expressions still need an obvious execution order. [GOOGLE-PYTHON]
- MUST avoid mutating a collection during traversal and bind loop values deliberately in closures that outlive the iteration. Why: iterator state and late-bound names can produce unexpected results. [GOOGLE-PYTHON] [RUFF]
- MUST pass a literal percent-style template and separate arguments to standard-library logging calls. Why: the logger can defer formatting until the message is needed. [GOOGLE-PYTHON] [RUFF]
- MUST await coroutines and keep spawned tasks under an owner that awaits completion, preferably `asyncio.TaskGroup`; propagate cancellation after cleanup. Why: discarded coroutines do no work and unmanaged tasks lose failures. [PY-ASYNCIO] [RUFF] [MYPY]
- MUST move blocking I/O off an asyncio event-loop thread and use thread synchronization or queues for shared threaded state. Why: `async def` and the GIL do not make blocking calls or compound updates safe. [PY-ASYNCIO] [GOOGLE-PYTHON]
- MUST reject untrusted `pickle` or `shelve` data, avoid `eval` and `exec` on external text, and use `secrets` for security-sensitive randomness. Why: these Python APIs can execute data or produce predictable secrets. [PY-SECURITY] [RUFF]
- MUST call `subprocess.run` with separate arguments, `shell=False`, and an explicit `check` choice, using `check=True` unless failure is handled through the return code. Why: process syntax and failure handling must remain explicit. [PY-SECURITY] [RUFF]
- MUST keep annotation-only `type` aliases out of runtime constructors and `isinstance` checks; use the actual class or supported runtime type expression there. Why: Python 3.12 aliases are not drop-in runtime class objects. [PY-TYPING] [RUFF]

## When to read more

- Before a change bigger than one function, read [references/guide.md](references/guide.md), the section for what you're doing.
- For naming basics, errors, tests, commits, secrets, and agent workflow, read [references/shared.md](references/shared.md).
- To set up tooling, copy or merge the files in [references/config/](references/config/) into your repository, then read the guide's Tooling section. Use the project's own source files and test fixtures.
- For worked controls, read [validated dataclass](references/examples/batch_plan.py), [exception hierarchy and reader](references/examples/plan_reader.py), [reader tests](references/examples/test_plan_reader.py).

## Sources

See [references/sources.md](references/sources.md) for sources, licenses, source tags, and changes. Unofficial: not affiliated with or endorsed by any source's owner.
