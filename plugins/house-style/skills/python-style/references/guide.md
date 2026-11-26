# Python style guide

Scope: Python 3.12+ applications and libraries; syntax and standard-library APIs target 3.12. Frameworks and older-runtime migrations need repository-specific additions.
Baseline: [shared rules](shared.md), including dependencies, commits, versioning, review, and AI agent workflow.
MUST means required; PREFER means the default, with a reason recorded for departures.
Source tags resolve in [source credits](sources.md#source-tags).

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

## Tooling

| Purpose | Tool and version | Config file | Repository command |
| --- | --- | --- | --- |
| Formatter | Ruff 0.17.3 | [pyproject.toml](config/pyproject.toml), `[tool.ruff.format]` | `ruff format --check .` |
| Linter | Ruff 0.17.3, explicit stable IDs below | Same file, `[tool.ruff.lint]` | `ruff check .` |
| Build / type checks | mypy 2.4.1, Python 3.12 target | Same file, `[tool.mypy]` | `mypy .` |
| Tests | CPython 3.14.8, standard-library `unittest` | Built-in discovery | `python -m unittest discover -s tests` |

Mechanical formatting: the formatter handles this.

Run these commands from the consuming project's root after merging the config. The TOML contains distributable tool blocks, not package metadata. After merging into a consuming project's root `pyproject.toml`, commands use that path and its application/test directories. Tool pins belong in that project's existing development environment and lock mechanism. Ruff rejects a version other than 0.17.3; mypy's pin is external to its config. `target-version` and `python_version` are both 3.12, independent of the interpreter running the tools.

Not yet run against Ruff 0.17.3 or mypy 2.4.1. Validate formatting, linting, and typing with those pinned tools after merging the tool blocks into the project’s `pyproject.toml`.

- MUST use Ruff's configured Python formatter and `I001` import ordering together, leaving conflicting layout linters disabled. Why: `ruff format` does not sort imports, and competing format policies can oscillate. [RUFF-FORMAT] [RUFF-CONFIG]
- MUST type-check Python implementation and tests with the strict mypy profile, without a global missing-import exemption. Why: skipped imports and untyped functions can hide unchecked values. [MYPY]
- MUST keep Python suppression comments diagnostic-specific, such as `# noqa: B019` or `# type: ignore[arg-type]`, and remove unused directives. Why: a targeted exception cannot hide unrelated future diagnostics. [RUFF] [MYPY]

- MUST install Python project dependencies and tools in an isolated project environment, never into the system interpreter or by bypassing its externally managed marker. Why: [PEP 668](https://peps.python.org/pep-0668/) protects distribution-owned Python packages. [PEP668]
- PREFER the repository's existing environment manager; for a new project use `uv`, dependencies in `pyproject.toml`, and a committed `uv.lock`, with `uv sync --locked` in CI. Why: a [locked project environment](https://docs.astral.sh/uv/concepts/projects/sync/) makes development and CI dependency resolution reproducible. [UV]

### Formatter and lint coverage

Formatter setting IDs: `line-length=88` (best-effort wrapping, not a hard line limit), `indent-width=4`, `format.indent-style=space`, `format.quote-style=double`, `format.line-ending=lf`, `format.skip-magic-trailing-comma=false`, and `format.docstring-code-format=true`. Continuations, statement layout, import spacing, quote normalization, and trailing commas are tool-owned. Docstring example formatting does not execute examples. [RUFF-FORMAT]

The following is the complete explicit Ruff selection, including `extend-select`. Each comma-separated ID is selected individually; no prefix group or implicit default profile is added. Descriptions identify diagnostic coverage, not proof that every instance of a semantic problem is detected. [RUFF] [RUFF-CONFIG]

| Rule IDs | Detected issue or configured policy |
| --- | --- |
| `A001`, `A002`, `A004`, `A006` | Builtin-shadowing variables, arguments, imports, and lambda arguments |
| `A005` | Modules shadowing standard-library names |
| `F401`, `F402`, `F403`, `F404`, `F405`, `F406`, `F407` | Unused/shadowed imports, wildcard ambiguity or scope, future-import placement and names |
| `F501`, `F502`, `F503`, `F504`, `F505`, `F506`, `F507`, `F508`, `F509` | Invalid percent-format strings, argument shapes, counts, or conversion characters |
| `F521`, `F522`, `F523`, `F524`, `F525`, `F541` | Invalid or mismatched `str.format` arguments; f-strings without interpolation |
| `F601`, `F602`, `F621`, `F622` | Repeated dictionary keys and invalid starred unpacking |
| `F631`, `F632`, `F633`, `F634` | Tuple assertions/conditions, literal identity, invalid print syntax |
| `F701`, `F702`, `F704`, `F706`, `F707`, `F722` | Invalid control-flow scope, handler ordering, and forward annotations |
| `F811`, `F821`, `F822`, `F823`, `F841`, `F842`, `F901` | Redefinitions, undefined/unbound/unused names, invalid exports, raising `NotImplemented` |
| `E401`, `E402`, `I001` | Import statement layout, module import placement, sorting and grouping |
| `TID252` | All relative imports, via `ban-relative-imports="all"` |
| `N801`, `N802`, `N803`, `N804`, `N805`, `N806`, `N807` | Class/function/argument/local names, `cls`/`self`, invalid dunder function naming |
| `N811`, `N812`, `N813`, `N814`, `N815`, `N816`, `N817`, `N818`, `N999` | Import alias casing, class/module variable casing, error suffix, module names |
| `E711`, `E712`, `E713`, `E714`, `E721`, `E722`, `E731` | Singleton/boolean comparisons, negative membership/identity, type comparisons, bare catches, assigned lambdas |
| `E741`, `E742`, `E743` | Ambiguous identifiers |
| `B002`, `B003`, `B004`, `B005` | Doubled unary signs, replacing `os.environ`, callable detection, misleading `strip` arguments |
| `B006`, `B007`, `B008`, `B011`, `B012` | Shared defaults, unused loop variables, default calls, `assert False`, escaping `finally` |
| `B013`, `B014`, `B015`, `B016`, `B017`, `B018`, `B019` | Exception tuples, useless expressions, literal raises, broad exception assertions, instance-retaining caches |
| `B020`, `B021`, `B022`, `B023`, `B025`, `B026`, `B028`, `B029` | Loop-name reuse, f-string docstrings, ineffective suppression, captured loop bindings, repeated/empty handlers, argument expansion, warning stacklevel |
| `B030`, `B031`, `B032`, `B033`, `B034`, `B035`, `B039` | Invalid caught types, reused group iterators, mistaken annotations, repeated set elements, regex positional arguments, constant comprehension keys, shared context defaults |
| `B904`, `B905` | Explicit exception chaining and explicit `zip(strict=...)` choice |
| `BLE001` | Broad catches except recognized reraising or traceback-logging cases |
| `SIM115` | Opened files outside a context manager; other resource lifetimes still need review |
| `TRY002`, `TRY004`, `TRY201` | Raising generic base exceptions, wrong exception for type validation, non-bare reraises |
| `RUF006`, `RUF008`, `RUF009`, `RUF012`, `RUF013` | Unretained asyncio tasks, mutable/call dataclass defaults, unmarked mutable class state, implicit optional annotations |
| `RUF018`, `RUF024`, `RUF032` | Assignment in assert, shared mutable `dict.fromkeys` values, Decimal from float literals |
| `ASYNC210`, `ASYNC212` | Known blocking HTTP APIs inside async functions |
| `ASYNC220`, `ASYNC221`, `ASYNC222` | Blocking process creation, execution, and waiting inside async functions |
| `ASYNC230`, `ASYNC240`, `ASYNC250`, `ASYNC251` | Blocking file/path operations, console input, and sleep inside async functions |
| `UP006`, `UP007`, `UP017`, `UP019`, `UP035`, `UP040`, `UP045` | Modern generics/unions/UTC/text/imports/aliases/nullable annotations for the selected Python target |
| `D100`, `D101`, `D102`, `D103`, `D104`, `D106`, `D107` | Missing public module/class/method/function/package/nested-class/constructor docstrings |
| `DTZ001`, `DTZ002`, `DTZ003`, `DTZ004`, `DTZ005`, `DTZ006`, `DTZ007` | Naive datetime construction, today/now/timestamp calls, and parsing without a timezone |
| `D200`, `D201`, `D202`, `D205`, `D207`, `D208`, `D209`, `D210`, `D211`, `D212`, `D214` | Formatter-compatible docstring structure, indentation, first-line summary, and section alignment |
| `D301`, `D400`, `D401`, `D402`, `D403` | Raw docstrings for backslashes, terminal period, imperative summaries, signature repetition, capitalization |
| `D405`, `D410`, `D411`, `D412`, `D414`, `D416`, `D417`, `D418`, `D419` | Google section names/separation/content/colons, argument documentation, overload docstrings, empty docstrings |
| `G001`, `G002`, `G003`, `G004`, `G010`, `G101`, `G201`, `G202` | Eager logger formatting, deprecated `warn`, reserved `extra` fields, exception-info usage |
| `S102`, `S110`, `S112` | `exec`, swallowed exceptions |
| `S301`, `S302`, `S306`, `S307` | Pickle/marshal loads, `mktemp`, `eval`; trusted uses still trigger review |
| `S323`, `S501`, `S506` | Unverified TLS contexts/requests and unsafe YAML loading |
| `S602`, `S604`, `S605`, `S608`, `PLW1510` | Shell-mediated process calls, interpolated SQL, and missing explicit subprocess failure policy |
| `PGH003`, `PGH004`, `RUF100`, `TD003` | Blanket type/lint ignores, unused suppressions, TODOs without issue context |

Per-file exceptions: `test_*.py` and `*_test.py` omit only the seven selected `D1xx` presence checks. Their existing docstrings still receive content checks. `.pyi` files omit those same presence checks because their implementation owns API prose. Ordinary helpers remain checked. Ruff's built-in `D102` exemption covers `@typing.override`; review still checks changed contracts. [RUFF] [RUFF-CONFIG]

Deliberately unselected: formatter conflicts `W191`, `E111`, `E114`, `E117`, `D203`, `D206`, `D300`, `Q000`–`Q004`, `COM812`, `COM819`, and `ISC002`; hard width checks `E501`/`W505`; competing `D213`/`D415`; `ANN401`; `TC001`–`TC008`; `TD002`/`FIX002`; `ISC001`/`ISC003`; `RUF067`; `PLR6301`; numerical complexity caps `C901`/`PLR0911`–`PLR0917`; blanket framework presets. `preview=false` and `unsafe-fixes=false` are explicit. [RUFF] [RUFF-FORMAT]

### Type-checker coverage

`strict=true` selects the pinned mypy profile. Its setting IDs are `disallow_any_generics`, `disallow_subclassing_any`, `disallow_untyped_calls`, `disallow_untyped_defs`, `disallow_incomplete_defs`, `check_untyped_defs`, `disallow_untyped_decorators`, `warn_redundant_casts`, `warn_unused_ignores`, `warn_return_any`, `implicit_reexport=false`, `strict_equality`, and `extra_checks`. Explicit additions preserve optional checks, reject missing-import `Any`, detect unreachable code, require coded ignores and override markers, and check unused awaitables. [MYPY]

| Diagnostic IDs | Coverage |
| --- | --- |
| `type-arg`, `no-untyped-def`, `no-untyped-call`, `untyped-decorator`, `no-any-return`, `redundant-cast`, `unused-ignore`, `comparison-overlap` | Strict-profile diagnostics |
| `no-any-unimported`, `unreachable`, `ignore-without-code`, `unused-awaitable`, `explicit-override` | Added by `disallow_any_unimported`, `warn_unreachable`, and `enable_error_code` |
| `attr-defined`, `union-attr`, `name-defined`, `used-before-def`, `has-type`, `no-redef` | Name/member availability and definite typing |
| `call-arg`, `arg-type`, `call-overload`, `return`, `return-value`, `empty-body`, `func-returns-value` | Calls and function results |
| `valid-type`, `nonetype-type`, `type-var`, `var-annotated`, `valid-newtype`, `literal-required`, `name-match` | Type declarations and inference |
| `assignment`, `method-assign`, `operator`, `index`, `list-item`, `dict-item`, `typeddict-item`, `typeddict-unknown-key`, `typeddict-readonly-mutated` | Assignments, operations, collections and TypedDicts |
| `metaclass`, `override`, `abstract`, `type-abstract`, `safe-super`, `exit-return`, `prop-decorator` | Class and context-manager contracts |
| `import`, `import-not-found`, `import-untyped` | Import availability and typed dependencies |
| `no-overload-impl`, `overload-overlap`, `overload-cannot-match` | Overload validity |
| `unused-coroutine`, `top-level-await`, `await-not-async`, `assert-type`, `truthy-function` | Async use and static checks |
| `str-format`, `str-bytes-safe`, `str-unpack` | Text and binary operations |
| `annotation-unchecked`, `syntax`, `narrowed-type-not-subtype`, `maybe-unrecognized-str-typeform`, `misc` | Remaining documented default diagnostics, including miscellaneous strict checks |

`strict_optional=true`, `implicit_optional=false`, and `strict_bytes=true` feed normal type diagnostics. `follow_imports="normal"` and `ignore_missing_imports=false` retain dependency checking. `warn_unused_configs` audits ineffective overrides when run with `--no-incremental`; output settings affect presentation only. Explicit `Any` remains possible; neither strict mode nor a cast validates external values at runtime. The table includes the documented default diagnostic IDs as well as enabled optional IDs. [MYPY]

`S101` and `S311` are deliberately unselected: review distinguishes removable assertions from runtime validation and non-security `random` use from required `secrets` use. `RUF018` still rejects assignment expressions in asserts. [RUFF]

Review-only or partial coverage: meaningful names and type-variable descriptions; safe import side effects; direct-symbol import clarity; metadata placement; runtime annotation resolution; docstring accuracy and return/raise completeness; isolation-boundary legitimacy; TODO link quality; loop mutation; general resource/task ownership; synchronization; real security trust; and useful complexity. Ruff and mypy recognize only some syntactic instances. [GOOGLE-PYTHON] [RUFF] [MYPY]

## Naming

- MUST use `snake_case` for modules, packages, functions, parameters, and variables, `CapWords` for classes, and `UPPER_SNAKE_CASE` for module constants. Why: Python readers recognize these roles immediately. [PEP8] [GOOGLE-PYTHON]
- MUST name instance and class receivers `self` and `cls`, end error exception names with `Error`, and avoid shadowing builtins or standard-library module names. Why: conventional roles and import resolution must stay unambiguous. [PEP8] [RUFF]
- PREFER a single leading underscore for internal members; reserve double-leading underscores for a demonstrated subclass-name collision. Why: ordinary internal names remain easy to inspect and test. [PEP8] [GOOGLE-PYTHON]
- PREFER descriptive type-parameter names, allowing short names only for private unconstrained parameters. Why: public generic relationships need meaningful names. [GOOGLE-PYTHON]
- MUST retain externally imposed names when implementing an existing protocol, such as unittest's `setUp`, instead of renaming the hook for style. Why: Python dispatch depends on the exact interface name. [PEP8] [PY-UNITTEST]

## Files and layout

- MUST use absolute imports and explicit imported names; declare intentional re-exports with `__all__` or a same-name import alias. Why: import origins and public exports stay statically visible. [PEP8] [GOOGLE-PYTHON] [MYPY]
- PREFER module-qualified references when direct symbol imports obscure ownership or collide; permit clear direct class, function, and typing imports. Why: concise names are useful when their origin remains obvious. [PEP8] [GOOGLE-PYTHON]
- MUST keep executable startup in `main()` behind `if __name__ == "__main__":`, without starting work during module import. Why: importing for tests or documentation must not launch the program. [GOOGLE-PYTHON]
- MUST place static module dunder metadata after the module docstring and future imports, before ordinary imports. Why: PEP 8 specifically defines the metadata exception to normal module layout. [PEP8]
- PREFER ordinary top-level imports and refactor cycles before using `TYPE_CHECKING`; use that guard only for dependencies absent from all runtime annotation consumers. Why: a type checker does not prove runtime introspection will resolve the names. [GOOGLE-PYTHON] [PY-TYPING]
- MUST keep package initializers limited to package documentation, intentional exports, and necessary lightweight setup. Why: importing a submodule also executes its package initializer. [PEP8] [PEP257] [GOOGLE-PYTHON]

## Types and data

- MUST represent instants with timezone-aware `datetime` values, using `datetime.now(tz=UTC)` or `datetime.fromtimestamp(value, tz=UTC)` and `zoneinfo.ZoneInfo` for local zones; never use `utcnow()` or `utcfromtimestamp()`. Why: [naive datetimes](https://docs.python.org/3/library/datetime.html#aware-and-naive-objects) do not identify an unambiguous instant. [RUFF]

- MUST annotate parameters and returns on application and test functions, including `-> None`; omit redundant `self` and `cls` annotations. Why: strict checking needs complete function boundaries. [GOOGLE-PYTHON] [MYPY]
- MUST use parameterized built-in containers, `X | None` for nullable values, and `type Alias = ...` for new annotation-only aliases. Why: the Python 3.12 baseline supports precise modern types. [GOOGLE-PYTHON] [PY-TYPING] [RUFF]
- PREFER `object` plus narrowing, a protocol, or a type parameter over `Any`; isolate any necessary `Any` to a documented adapter. Why: `Any` lets unchecked operations propagate. [PY-TYPING] [MYPY]
- PREFER `collections.abc` interfaces such as `Iterable`, `Sequence`, or `Mapping` in parameter annotations when mutation or a concrete container is unnecessary. Why: callers can supply suitable implementations without extra conversions. [GOOGLE-PYTHON]
- MUST create mutable function defaults per call and mutable dataclass fields with `default_factory`; use `None` or an immutable sentinel as the parameter default. Why: defaults are otherwise shared between calls or instances. [GOOGLE-PYTHON] [RUFF]
- MUST mark intentionally shared mutable class state with `ClassVar` and initialize per-instance state on the instance. Why: an ordinary class attribute is shared across instances. [PY-TYPING] [RUFF]
- MUST test optional values with `is None` or `is not None` when zero, empty text, or `False` remains valid. Why: truthiness would discard valid supplied values. [PEP8] [GOOGLE-PYTHON]
- MUST distinguish `str` text from `bytes` data and specify the intended encoding when opening text files or encoding and decoding. Why: implicit conversions and locale defaults change data. [GOOGLE-PYTHON] [MYPY]
- MUST mark overridden methods with `typing.override`, except `__init__` and `__new__`; document any contract change even when the base docstring is inherited. Why: static checking catches accidental mismatches and readers see changed behavior. [GOOGLE-PYTHON] [MYPY]
- PREFER plain attributes for simple data and cheap properties for access logic; use methods for expensive operations. Why: property syntax implies inexpensive, unsurprising access. [PEP8] [GOOGLE-PYTHON]

## Errors

- MUST catch specific exception types in narrow `try` blocks; use a broad catch only for reraising or a documented isolation boundary that records the traceback. Why: unrelated programming errors must remain visible. [PEP8] [GOOGLE-PYTHON] [RUFF]
- MUST use bare `raise` to propagate the current exception and `raise NewError(...) from error` when translating it. Why: traceback and cause information retain their intended meaning. [PEP8] [RUFF]
- MUST use explicit exceptions for runtime validation, usually `ValueError` or `TypeError`, and allow `assert` only for tests or non-critical invariants/type narrowing whose removal leaves required behavior intact. Why: optimized Python removes assertions; input validation and side effects must survive. [GOOGLE-PYTHON] [RUFF]
- MUST derive application exceptions from `Exception` or a more specific exception and avoid raising `Exception` or `BaseException` directly. Why: callers need a meaningful failure category without intercepting process-control exceptions. [PEP8] [RUFF]
- MUST use `with`, `async with`, or `try/finally` for owned resources and avoid `__del__` for required cleanup. Why: Python finalization does not guarantee timely resource release. [PEP8] [GOOGLE-PYTHON]
- MUST avoid `return`, `break`, or `continue` that exits `finally`, and explicitly return `None` on a missing-result path when other paths return values. Why: cleanup must not mask failures and return contracts must stay consistent. [PEP8] [RUFF]

## Comments and docs

- MUST write Python API docstrings with a period-ended imperative function summary and Google `Args`, `Returns` or `Yields`, and `Raises` sections when needed; describe classes and properties as values. Why: callers can find the contract in a consistent form. [PEP257] [GOOGLE-PYTHON] [RUFF]
- MUST document public Python modules, packages, classes, functions, methods, and explicit constructors, with constructor arguments on `__init__` and public data in `Attributes`. Why: Python's introspection and documentation tools use these docstrings. [PEP257] [GOOGLE-PYTHON] [RUFF]
- MUST document each parameter in `Args` when a function has a parameterized contract, and describe yielded items in `Yields`; omit `Returns` only for `None` or an adequate return summary. Why: section headings describe values rather than duplicate signatures. [GOOGLE-PYTHON] [RUFF]
- PREFER omitting docstrings on self-explanatory test modules, test classes, and test methods while documenting unusual setup or behavior. Why: repeating a test name provides no additional contract. [GOOGLE-PYTHON]
TODO syntax is defined once in [shared Comments and docs](shared.md#comments-and-docs). Python retains `TD003` for missing issue context, while the exact format and link quality remain review duties. [RUFF]

## Testing

- MUST name test modules `test_*.py` and test functions or methods `test_*`; keep exception assertions around only the operation expected to fail. Why: discovery and failure attribution stay reliable. [PY-UNITTEST] [GOOGLE-PYTHON] [RUFF]
- MUST use `TestCase` assertion helpers in unittest and ordinary `assert` in pytest, asserting a specific expected exception with `assertRaises` or `pytest.raises`. Why: framework diagnostics identify the actual mismatch. [PY-UNITTEST] [GOOGLE-PYTHON] [RUFF]
- MUST register unittest resource cleanup with `addCleanup`, `enterContext`, or a local context manager, including resources acquired before setup can fail. Why: `tearDown` alone does not cover unsuccessful setup. [PY-UNITTEST]
- MUST check Python cases where `None`, zero, empty containers, repeated calls, and captured loop values have distinct contract meanings. Why: truthiness, shared defaults, and late binding can pass ordinary happy-path tests. [PEP8] [GOOGLE-PYTHON]

## Performance

- PREFER comprehensions with one `for` and at most one filter; use ordinary loops for side effects or more complex control flow. Why: compact Python expressions still need an obvious execution order. [GOOGLE-PYTHON]
- PREFER iterators or generator expressions for one-pass consumption and `str.join` or `StringIO` for repeated text assembly. Why: unnecessary materialization and repeated string copying add memory and work. [PEP8] [GOOGLE-PYTHON]
- MUST pass a literal percent-style template and separate arguments to standard-library logging calls. Why: the logger can defer formatting until the message is needed. [GOOGLE-PYTHON] [RUFF]
- MUST await coroutines and keep spawned tasks under an owner that awaits completion, preferably `asyncio.TaskGroup`; propagate cancellation after cleanup. Why: discarded coroutines do no work and unmanaged tasks lose failures. [PY-ASYNCIO] [RUFF] [MYPY]
- MUST move blocking I/O off an asyncio event-loop thread and use thread synchronization or queues for shared threaded state. Why: `async def` and the GIL do not make blocking calls or compound updates safe. [PY-ASYNCIO] [GOOGLE-PYTHON]
- PREFER reviewing long functions for separable responsibilities without enforcing fixed line, branch, or parameter-count caps. Why: numerical size alone does not establish whether a Python function is understandable. [GOOGLE-PYTHON] [RUFF]

## Security

- MUST reject untrusted `pickle` or `shelve` data, avoid `eval` and `exec` on external text, and use `secrets` for security-sensitive randomness. Why: these Python APIs can execute data or produce predictable secrets. [PY-SECURITY] [RUFF]
- MUST call `subprocess.run` with separate arguments, `shell=False`, and an explicit `check` choice, using `check=True` unless failure is handled through the return code. Why: process syntax and failure handling must remain explicit. [PY-SECURITY] [RUFF]
- MUST use `tempfile.TemporaryFile`, `NamedTemporaryFile`, or `TemporaryDirectory` rather than `mktemp`. Why: securely creating the resource avoids a name-reservation race. [PY-SECURITY] [RUFF]
- MUST use safe YAML loading for external documents and keep TLS certificate verification enabled in Python HTTP clients. Why: unsafe constructors and disabled verification undermine otherwise typed interfaces. [RUFF]

## Language-specific pitfalls

- MUST avoid mutating a collection during traversal and bind loop values deliberately in closures that outlive the iteration. Why: iterator state and late-bound names can produce unexpected results. [GOOGLE-PYTHON] [RUFF]
- MUST pass `strict=True` to `zip` when inputs must have equal length and explicitly pass `strict=False` only when truncation is intentional. Why: the default truncation can silently lose unmatched data. [RUFF]
- MUST keep annotation-only `type` aliases out of runtime constructors and `isinstance` checks; use the actual class or supported runtime type expression there. Why: Python 3.12 aliases are not drop-in runtime class objects. [PY-TYPING] [RUFF]
- MUST account for Python 3.12 annotation evaluation with postponed annotations or quoted forward references where needed, while preserving names required by runtime introspection. Why: deferred evaluation and static-only imports do not supply missing runtime names. [GOOGLE-PYTHON] [PY-TYPING]
- PREFER module functions over `staticmethod` unless matching an external API, and reserve `classmethod` for alternate constructors or necessary class-wide behavior. Why: extra class scope should have a concrete purpose. [GOOGLE-PYTHON]
- PREFER f-strings for ordinary interpolation while retaining percent templates for lazy logging and literal translation templates. Why: the correct interpolation stage depends on the receiving API. [GOOGLE-PYTHON] [RUFF]
- MUST distinguish an intended adjacent string literal from a missing comma in a collection, and construct exact decimal quantities from strings or integers rather than float literals. Why: both errors can silently change data while remaining valid Python. [PEP8] [RUFF]

## Where the sources disagree

Where the sources disagree, the following house choices apply. Each choice states the adopted behavior and its reason.

- MUST resolve differences over width through the configured Ruff formatter: PEP 8 proposes 79/72, Google 80, and Ruff defaults to 88; this profile uses Ruff's 88 target without `E501` or `W505`. Why: one formatter owns wrapping, including lines it cannot shorten. [PEP8] [GOOGLE-PYTHON] [RUFF-FORMAT]
- MUST resolve differences over legacy tabs through Ruff's configured indentation, choosing Google's no-tab direction over PEP 8's existing-file allowance when formatting adopted files. Why: the formatter supplies a single mechanical result. [PEP8] [GOOGLE-PYTHON] [RUFF-FORMAT]
- MUST resolve differences over continuations with Ruff output rather than manually selecting among PEP 8's and Google's indentation alternatives. Why: layout is reproducible without prose exceptions. [PEP8] [GOOGLE-PYTHON] [RUFF-FORMAT]
- MUST resolve differences over backslash continuation with Ruff's parenthesized code continuation, following Google's direction over PEP 8's old-runtime exceptions. Why: the 3.12 baseline supports the formatter's syntax. [PEP8] [GOOGLE-PYTHON] [RUFF-FORMAT]
- PREFER clear direct symbol imports, as PEP 8 permits, while using module qualification when ownership is unclear instead of Google's module-only restriction. Why: explicit names remain readable without banning standard direct typing and class imports. [PEP8] [GOOGLE-PYTHON]
- MUST use absolute imports, choosing Google's uniform policy over PEP 8's relative-import allowance and setting `TID252` to ban all relatives. Why: one import policy is straightforward to check. [PEP8] [GOOGLE-PYTHON] [RUFF]
- MUST let `I001` resolve differences over import separators, choosing its PEP 8 grouping over Google's optional separators. Why: import sorting and grouping share one tool. [PEP8] [GOOGLE-PYTHON] [RUFF]
- MUST follow PEP 8's explicit static dunder-metadata placement rather than extrapolating Google's general imports-before-globals rule. Why: the specific rule resolves an apparent conflict without inventing a Google dunder ban. [PEP8] [GOOGLE-PYTHON]
- MUST use `snake_case` package names, allowing Google's underscores despite PEP 8's discouragement. Why: packages and modules share a readable naming convention. [PEP8] [GOOGLE-PYTHON]
- PREFER one internal underscore, following Google, with PEP 8's double-underscore collision protection available only for a demonstrated inheritance need. Why: the ordinary case stays inspectable without discarding the specialized mechanism. [PEP8] [GOOGLE-PYTHON]
- PREFER descriptive type-parameter names, following Google over PEP 8's short-name preference, with short private unconstrained names allowed. Why: public relationships deserve readable labels. [PEP8] [GOOGLE-PYTHON]
- MUST annotate and type-check functions, extending Google's checked-public-API requirement to implementation and tests instead of PEP 8's optional-tooling stance. Why: unchecked helpers can defeat checked interfaces. [PEP8] [GOOGLE-PYTHON] [MYPY]
- MUST use imperative function summaries, selecting PEP 257 and `D401` within Google's broader permission; class and property descriptions retain value-oriented prose. Why: a fixed function convention is automatically checkable. [PEP257] [GOOGLE-PYTHON] [RUFF]
- MUST end docstring summaries with periods, selecting PEP 257 and `D400` instead of Google's broader punctuation and `D415`. Why: one convention avoids overlapping alternative checks. [PEP257] [GOOGLE-PYTHON] [RUFF]
- PREFER meaningful test names without redundant docstrings, adopting Google's explicit test exemption over the PEPs' general public-object documentation rule. Why: tests can explain their contract through their names and assertions. [PEP8] [PEP257] [GOOGLE-PYTHON]
- MUST use explicit override markers and permit inherited docstrings only when the contract is unchanged, adopting Google's exception to PEP 257's per-method documentation rule. Why: the base remains authoritative while changed behavior gets new prose. [PEP257] [GOOGLE-PYTHON] [MYPY]
- MUST document the result, but permit Google's omission of a separate `Returns` section for `None` or an adequate summary rather than requiring redundant PEP 257-style detail. Why: content matters more than a duplicate heading. [PEP257] [GOOGLE-PYTHON]
- MUST follow the shared TODO convention, retaining Google's tracking context with the link after the colon rather than its parenthesized form; leave author-enforcing `TD002` off. Why: the shared spelling follows Ruff's documented link placement. [GOOGLE-PYTHON] [RUFF]
- MUST permit tracked, explained TODOs, following Google with `TD003` instead of enabling the universal `FIX002` ban. Why: incomplete work can be visible and actionable. [GOOGLE-PYTHON] [RUFF]
- PREFER ordinary imports, following Google and leaving `TC001`–`TC003` off; exceptional type-only guards still need runtime-evaluation review. Why: eager introspection may need the imported names. [GOOGLE-PYTHON] [RUFF] [PY-TYPING]
- MUST use `type` for new annotation-only aliases, choosing Python 3.12 and `UP040` over Google's older `TypeAlias` spelling. Why: the declared runtime baseline resolves the version mismatch. [GOOGLE-PYTHON] [RUFF] [PY-TYPING]
- PREFER precise types but allow documented adapter-local `Any`, following Google's escape hatch with strict mypy instead of enabling `ANN401`. Why: a blanket syntax ban cannot model every dynamic library boundary. [GOOGLE-PYTHON] [RUFF] [MYPY]
- MUST use specific built-in or domain exceptions; Google's `ValueError` advice and actual `TRY002` agree because the rule only rejects direct `Exception`/`BaseException` raises. Why: Ruff's TRY002 rejects raising bare `Exception` or `BaseException`, so it agrees with Google's built-in-exception advice. [GOOGLE-PYTHON] [RUFF]
- MUST allow assertions in tests and for removable non-critical invariants/type narrowing, following Google and leaving blanket `S101` off. Why: explicit runtime validation remains required while useful debug assertions can disappear under optimization. [GOOGLE-PYTHON] [RUFF]
- MUST avoid bare catches with `E722`, while permitting explicit broad catches only for reraising or documented traceback-recording isolation boundaries accepted by Google and `BLE001`. Why: explicit exception classes keep control-flow intent visible. [PEP8] [GOOGLE-PYTHON] [RUFF]
- MUST let Ruff formatting resolve differences over one-line suites, choosing expanded formatter output over Google's and PEP 8's limited one-line allowances. Why: the formatter handles statement layout without an extra prose policy. [PEP8] [GOOGLE-PYTHON] [RUFF-FORMAT]
- PREFER ordinary f-strings but preserve API-specific logging and translation templates allowed by Google; leave `UP031`/`UP032` off. Why: eager replacement can change when interpolation happens. [GOOGLE-PYTHON] [RUFF]
- MUST let Ruff's configured quote policy resolve the competing styles, narrowing PEP 8's and Google's freedom without selecting the competing `Q000` linter. Why: a single formatter controls escaping and quote choice. [PEP8] [GOOGLE-PYTHON] [RUFF-FORMAT]
- MUST let Ruff normalize multiline strings, choosing its policy over Google's optional triple-single convention and PEP 8's handwritten prescription. Why: multiline quote layout stays formatter-owned. [PEP8] [GOOGLE-PYTHON] [RUFF-FORMAT]
- MUST permit intentional adjacent literals, as PEP 8 and Google do, leaving `ISC001`/`ISC002`/`ISC003` unselected. Why: useful wrapping remains possible while reviewers check missing collection commas. [PEP8] [GOOGLE-PYTHON] [RUFF]
- MUST use formatter-compatible `D211` instead of `D203`, matching Google's class-docstring placement. Why: contradictory whitespace rules cannot both be satisfied. [GOOGLE-PYTHON] [RUFF] [RUFF-FORMAT]
- MUST select `D212` rather than `D213`, narrowing PEP 257's two allowed summary positions to one. Why: a single docstring layout is predictable. [PEP257] [RUFF]
- MUST let Ruff resolve trailing commas, following the guides' formatter-friendly direction with neither `COM812` nor `COM819` selected. Why: comma lint policies must not fight the formatter. [PEP8] [GOOGLE-PYTHON] [RUFF-FORMAT]
- MUST use unquoted expressions in annotation-only `type` statements and leave the legacy alias policies `TC007` and `TC008` off. Why: Python 3.12 alias values are lazy, and the opposing checks target other evaluation choices. [RUFF] [PY-TYPING]
- MUST allow lightweight documented package exports, following PEP 8/257 instead of `RUF067`'s empty-initializer restriction. Why: package APIs can legitimately provide documentation and deliberate re-exports. [PEP8] [PEP257] [RUFF]
- PREFER a module function when a method uses no instance state, following Google rather than `PLR6301`'s staticmethod alternative; existing external APIs remain exceptions. Why: extra class nesting needs a reason. [GOOGLE-PYTHON] [RUFF]
- PREFER review of function cohesion, following Google's flexible guidance over hard `C901` or `PLR` count thresholds. Why: arbitrary caps can encourage fragmentation without improving comprehension. [GOOGLE-PYTHON] [RUFF]
