# PEP 257: condensed rules

PEP 257 describes documentation conventions, not additional Python syntax requirements. Preserve imperative summaries and the distinctions between one-line and multiline docstrings.

Source owner: David Goodger and Guido van Rossum. License: [LicenseRef-Public-Domain-PEP](../LICENSE). Changes: rules independently restated, shortened and grouped by topic; examples omitted. Unofficial; no endorsement is implied.

## Tooling

- When processing docstrings, strip all leading whitespace from their first line. — [PEP 257: Handling Docstring Indentation](https://peps.python.org/pep-0257/#handling-docstring-indentation). <!-- pep257:32 -->
- For later lines, remove the minimum shared indent of nonblank lines while retaining indentation relative to that baseline. — [PEP 257: Handling Docstring Indentation](https://peps.python.org/pep-0257/#handling-docstring-indentation). <!-- pep257:33 -->
- Trim empty lines from both ends of a processed docstring. — [PEP 257: Handling Docstring Indentation](https://peps.python.org/pep-0257/#handling-docstring-indentation). <!-- pep257:34 -->
- Expand tabs using Python's indentation rules before calculating docstring indentation. — [PEP 257: Handling Docstring Indentation](https://peps.python.org/pep-0257/#handling-docstring-indentation). <!-- pep257:35 -->

## Comments and docs

- Make an object's docstring the initial statement in its definition. — [PEP 257: What is a Docstring?](https://peps.python.org/pep-0257/#what-is-a-docstring). <!-- pep257:1 -->
- Normally supply docstrings for modules, exported functions and classes, and public methods, including `__init__`. — [PEP 257: What is a Docstring?](https://peps.python.org/pep-0257/#what-is-a-docstring). <!-- pep257:2 -->
- Document a package in the docstring of its `__init__.py` module when appropriate. — [PEP 257: What is a Docstring?](https://peps.python.org/pep-0257/#what-is-a-docstring). <!-- pep257:3 -->
- Delimit docstrings with three double quotes on each side. — [PEP 257: What is a Docstring?](https://peps.python.org/pep-0257/#what-is-a-docstring). <!-- pep257:4 -->
- Choose a raw triple-double-quoted docstring when its contents include backslashes. — [PEP 257: What is a Docstring?](https://peps.python.org/pep-0257/#what-is-a-docstring). <!-- pep257:5 -->
- Use the one-line form only when the behavior is obvious and the complete docstring fits on that line. — [PEP 257: One-line Docstrings](https://peps.python.org/pep-0257/#one-line-docstrings). <!-- pep257:6 -->
- Keep triple-quote delimiters even for a short docstring. — [PEP 257: One-line Docstrings](https://peps.python.org/pep-0257/#one-line-docstrings). <!-- pep257:7 -->
- Place a one-line docstring's opening and closing delimiters together on that line. — [PEP 257: One-line Docstrings](https://peps.python.org/pep-0257/#one-line-docstrings). <!-- pep257:8 -->
- Do not surround a simple function docstring with empty lines. — [PEP 257: One-line Docstrings](https://peps.python.org/pep-0257/#one-line-docstrings). <!-- pep257:9 -->
- Describe the effect as an imperative command ending with a period. — [PEP 257: One-line Docstrings](https://peps.python.org/pep-0257/#one-line-docstrings). <!-- pep257:10 -->
- Do not use a retrievable Python function signature as the entire docstring. — [PEP 257: One-line Docstrings](https://peps.python.org/pep-0257/#one-line-docstrings). <!-- pep257:11 -->
- State what kind of result the function returns when that information is needed. — [PEP 257: One-line Docstrings](https://peps.python.org/pep-0257/#one-line-docstrings). <!-- pep257:12 -->
- Include signature information when documenting a C function whose signature cannot be introspected. — [PEP 257: One-line Docstrings](https://peps.python.org/pep-0257/#one-line-docstrings). <!-- pep257:13 -->
- For a longer docstring, give a single summary line, an empty line, and then the detailed explanation. — [PEP 257: Multi-line Docstrings](https://peps.python.org/pep-0257/#multi-line-docstrings). <!-- pep257:14 -->
- Place the summary either immediately after the opening delimiter or on the next line. — [PEP 257: Multi-line Docstrings](https://peps.python.org/pep-0257/#multi-line-docstrings). <!-- pep257:15 -->
- Align the remaining docstring text with the indentation of its opening quotes. — [PEP 257: Multi-line Docstrings](https://peps.python.org/pep-0257/#multi-line-docstrings). <!-- pep257:16 -->
- Leave an empty line after a class docstring before its first method. — [PEP 257: Multi-line Docstrings](https://peps.python.org/pep-0257/#multi-line-docstrings). <!-- pep257:17 -->
- Write a script's docstring so it can serve as the script's usage message. — [PEP 257: Multi-line Docstrings](https://peps.python.org/pep-0257/#multi-line-docstrings). <!-- pep257:18 -->
- Explain the script's purpose, invocation, environment, files, options, and arguments for both first-time use and later reference. — [PEP 257: Multi-line Docstrings](https://peps.python.org/pep-0257/#multi-line-docstrings). <!-- pep257:19 -->
- In a module docstring, identify exported objects and briefly describe each one. — [PEP 257: Multi-line Docstrings](https://peps.python.org/pep-0257/#multi-line-docstrings). <!-- pep257:20 -->
- Extend a package's documentation to identify the modules and subpackages it exports. — [PEP 257: Multi-line Docstrings](https://peps.python.org/pep-0257/#multi-line-docstrings). <!-- pep257:21 -->
- Document callable behavior, relevant parameters, results, side effects, exceptions, and restrictions on when it may be called. — [PEP 257: Multi-line Docstrings](https://peps.python.org/pep-0257/#multi-line-docstrings). <!-- pep257:22 -->
- Identify optional parameters and state whether callers may rely on their keyword names. — [PEP 257: Multi-line Docstrings](https://peps.python.org/pep-0257/#multi-line-docstrings). <!-- pep257:23 -->
- Explain a class's behavior along with its public methods and instance attributes. — [PEP 257: Multi-line Docstrings](https://peps.python.org/pep-0257/#multi-line-docstrings). <!-- pep257:24 -->
- For an inheritable class, document the interface intended for subclasses separately from its ordinary public API. — [PEP 257: Multi-line Docstrings](https://peps.python.org/pep-0257/#multi-line-docstrings). <!-- pep257:25 -->
- Put constructor documentation on `__init__` and each method's documentation on that method. — [PEP 257: Multi-line Docstrings](https://peps.python.org/pep-0257/#multi-line-docstrings). <!-- pep257:26 -->
- When a subclass mostly inherits its parent, identify that relationship and describe the differences. — [PEP 257: Multi-line Docstrings](https://peps.python.org/pep-0257/#multi-line-docstrings). <!-- pep257:27 -->
- Call a method an override when it replaces parent behavior without calling it, and an extension when it also invokes the parent. — [PEP 257: Multi-line Docstrings](https://peps.python.org/pep-0257/#multi-line-docstrings). <!-- pep257:28 -->
- Preserve parameter-name capitalization in documentation instead of rendering names in all capitals. — [PEP 257: Multi-line Docstrings](https://peps.python.org/pep-0257/#multi-line-docstrings). <!-- pep257:29 -->
- Prefer a separate documentation line for each parameter. — [PEP 257: Multi-line Docstrings](https://peps.python.org/pep-0257/#multi-line-docstrings). <!-- pep257:30 -->
- For a docstring longer than one line, give the closing delimiter its own line. — [PEP 257: Multi-line Docstrings](https://peps.python.org/pep-0257/#multi-line-docstrings). <!-- pep257:31 -->

## Worked examples

Read [original worked examples and their source tags](examples.md) for small applications of this guide.
