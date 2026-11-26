# Google Python Style Guide: condensed rules

Google Python rules, grouped by topic. Examples and internal BUILD-file bookkeeping are omitted. Keep source alternatives and recommendation strength.

## Quick rules

Read the sections relevant to the task below; the complete rules are kept in one place.

## Tooling

- Run pylint with Google's published pylintrc unless the project already specifies its own configuration. — [Google — Lint](https://google.github.io/styleguide/pyguide.html#lint).

- Suppress an unsuitable pylint diagnostic when leaving it visible would obscure useful warnings. — [Google Python: 2.1 Lint](https://google.github.io/styleguide/pyguide.html#lint). <!-- google-python:2 -->
- Target pylint suppressions to individual lines using symbolic diagnostic names, adding a reason when it is not self-evident. — [Google Python: 2.1 Lint](https://google.github.io/styleguide/pyguide.html#lint). <!-- google-python:3 -->
- Spell new pylint suppressions with `disable`, not the obsolete `disable-msg` option. — [Google Python: 2.1 Lint](https://google.github.io/styleguide/pyguide.html#lint). <!-- google-python:4 -->
- Handle unused formal parameters by deleting them at the beginning of the function and commenting on why they are unused. — [Google Python: 2.1 Lint](https://google.github.io/styleguide/pyguide.html#lint). <!-- google-python:5 -->
- Naming an unused parameter `_` or using an `unused_` prefix, or assigning it to `_`, remains allowed but is discouraged in favor of deletion. — [Google Python: 2.1 Lint](https://google.github.io/styleguide/pyguide.html#lint). <!-- google-python:6 -->
- Strongly consider static type analysis when changing existing Python code. — [Google Python: 2.21 Type Annotated Code](https://google.github.io/styleguide/pyguide.html#typed-code). <!-- google-python:76 -->
- Add annotations to new or modified public APIs and include type checking in the build process. — [Google Python: 2.21 Type Annotated Code](https://google.github.io/styleguide/pyguide.html#typed-code). <!-- google-python:77 -->
- Suppress `invalid-name` narrowly for mathematical identifiers that need the exception. — [Google Python: 3.16.5 Mathematical Notation](https://google.github.io/styleguide/pyguide.html#math-notation). <!-- google-python:213 -->
- Suppress an unsuitable type diagnostic on its line with `type: ignore` or a suitable checker-specific directive. — [Google Python: 3.19.7 Ignoring Types](https://google.github.io/styleguide/pyguide.html#typing-ignore). <!-- google-python:239 -->

## Naming

- End exception names with `Error` and avoid repeating information already supplied by their module name. — [Google Python: 2.4 Exceptions](https://google.github.io/styleguide/pyguide.html#exceptions). <!-- google-python:19 -->
- When mutable globals are necessary, make them internal and prefix their names with an underscore. — [Google Python: 2.5 Mutable Global State](https://google.github.io/styleguide/pyguide.html#global-variables). <!-- google-python:24 -->
- Use module-level constants where useful and name them with uppercase words joined by underscores. — [Google Python: 2.5 Mutable Global State](https://google.github.io/styleguide/pyguide.html#global-variables). <!-- google-python:27 -->
- Follow normal function naming and import conventions for decorators too. — [Google Python: 2.17 Function and Method Decorators](https://google.github.io/styleguide/pyguide.html#decorators). <!-- google-python:61 -->
- Use `get_` and `set_` prefixes for getter and setter methods. — [Google Python: 3.15 Getters and Setters](https://google.github.io/styleguide/pyguide.html#getters-and-setters). <!-- google-python:192 -->
- Choose informative names for files and code entities. — [Google Python: 3.16 Naming](https://google.github.io/styleguide/pyguide.html#naming). <!-- google-python:194 -->
- Avoid obscure abbreviations and names shortened by dropping letters. — [Google Python: 3.16 Naming](https://google.github.io/styleguide/pyguide.html#naming). <!-- google-python:195 -->
- Use lowercase words separated by underscores for modules, packages, functions, attributes, parameters, and variables. — [Google Python: 3.16 Naming](https://google.github.io/styleguide/pyguide.html#naming). <!-- google-python:196 -->
- Name classes and exception types with CapWords. — [Google Python: 3.16 Naming](https://google.github.io/styleguide/pyguide.html#naming). <!-- google-python:197 -->
- Use uppercase words with underscores for constants. — [Google Python: 3.16 Naming](https://google.github.io/styleguide/pyguide.html#naming). <!-- google-python:198 -->
- Use one-letter names only for familiar local loop, exception, or file variables, private type parameters without constraints, or established mathematical notation. — [Google Python: 3.16 Naming](https://google.github.io/styleguide/pyguide.html#naming). <!-- google-python:199 -->
- Make names more descriptive as the scope in which they are used grows. — [Google Python: 3.16 Naming](https://google.github.io/styleguide/pyguide.html#naming). <!-- google-python:200 -->
- Keep names free of dashes, invented dunders, offensive language, and unnecessary type labels. — [Google Python: 3.16 Naming](https://google.github.io/styleguide/pyguide.html#naming). <!-- google-python:201 -->
- Prefer a single leading underscore for internal members over double-underscore name mangling. — [Google Python: 3.16 Naming](https://google.github.io/styleguide/pyguide.html#naming). <!-- google-python:202 -->
- Preserve an acronym's uppercase letters within a CapWords name. — [Google Python: 3.16 Naming](https://google.github.io/styleguide/pyguide.html#naming). <!-- google-python:205 -->
- Match a foreign interface's naming when close integration with that interface makes consistency necessary. — [Google Python: 3.16 Naming](https://google.github.io/styleguide/pyguide.html#naming). <!-- google-python:207 -->
- Name Python files with a `.py` suffix and avoid hyphens. — [Google Python: 3.16.3 File Naming](https://google.github.io/styleguide/pyguide.html#file-naming). <!-- google-python:208 -->
- Use established mathematical notation for identifiers in mathematically intensive implementation code. — [Google Python: 3.16.5 Mathematical Notation](https://google.github.io/styleguide/pyguide.html#math-notation). <!-- google-python:210 -->
- Keep public API names descriptive where practical, even when the implementation uses mathematical notation. — [Google Python: 3.16.5 Mathematical Notation](https://google.github.io/styleguide/pyguide.html#math-notation). <!-- google-python:212 -->
- Give type aliases CapWords names and add a leading underscore when an alias is internal to its module. — [Google Python: 3.19.6 Type Aliases](https://google.github.io/styleguide/pyguide.html#type-aliases). <!-- google-python:236 -->
- Name type variables descriptively unless they are both private and unconstrained. — [Google Python: 3.19.10 Type variables](https://google.github.io/styleguide/pyguide.html#typevars). <!-- google-python:243 -->
- Keep names supplied by `typing` and `collections.abc` free from unrelated application definitions. — [Google Python: 3.19.12 Imports For Typing](https://google.github.io/styleguide/pyguide.html#typing-imports). <!-- google-python:249 -->

## Files and layout

- In programs using Abseil, invoke the entry point through `app.run`. — [Google — Main](https://google.github.io/styleguide/pyguide.html#317-main).

- Import packages or modules instead of their individual classes, types, or functions, subject to the static-analysis exceptions. — [Google Python: 2.2 Imports](https://google.github.io/styleguide/pyguide.html#imports). <!-- google-python:7 -->
- Use a plain module import or import a module from its containing package, as appropriate to its location. — [Google Python: 2.2 Imports](https://google.github.io/styleguide/pyguide.html#imports). <!-- google-python:8 -->
- Alias a module imported with `from` when its name collides or is excessively long or generic. — [Google Python: 2.2 Imports](https://google.github.io/styleguide/pyguide.html#imports). <!-- google-python:9 -->
- Use an alias on a direct module import only for a widely established abbreviation. — [Google Python: 2.2 Imports](https://google.github.io/styleguide/pyguide.html#imports). <!-- google-python:10 -->
- Specify the complete package path in imports instead of a relative path. — [Google Python: 2.2 Imports](https://google.github.io/styleguide/pyguide.html#imports). <!-- google-python:11 -->
- Allow direct symbol imports from `typing`, `collections.abc`, and `typing_extensions` when they support static analysis. — [Google Python: 2.2 Imports](https://google.github.io/styleguide/pyguide.html#imports). <!-- google-python:12 -->
- In new code, identify imported modules through their full package paths. — [Google Python: 2.3 Packages](https://google.github.io/styleguide/pyguide.html#packages). <!-- google-python:13 -->
- Normally nest a class or function only when it captures a local binding other than `self` or `cls`. — [Google Python: 2.6 Nested/Local/Inner Classes and Functions](https://google.github.io/styleguide/pyguide.html#nested-classes-functions). <!-- google-python:28 -->
- Hide a helper with a leading underscore at module level instead of nesting it solely to conceal it. — [Google Python: 2.6 Nested/Local/Inner Classes and Functions](https://google.github.io/styleguide/pyguide.html#nested-classes-functions). <!-- google-python:29 -->
- Replace a lambda with a named function when it spans lines or grows beyond roughly 60–80 characters. — [Google Python: 2.10 Lambda Functions](https://google.github.io/styleguide/pyguide.html#lambdas). <!-- google-python:41 -->
- Keep each of a conditional expression's two results and its condition on a single physical line, though the three parts may span lines. — [Google Python: 2.11 Conditional Expressions](https://google.github.io/styleguide/pyguide.html#conditional-expressions). <!-- google-python:44 -->
- Prefer a module-level function to `staticmethod`, except when an existing external interface requires the latter. — [Google Python: 2.17 Function and Method Decorators](https://google.github.io/styleguide/pyguide.html#decorators). <!-- google-python:66 -->
- Leave semicolons off statement endings. — [Google Python: 3.1 Semicolons](https://google.github.io/styleguide/pyguide.html#semicolons). <!-- google-python:80 -->
- Do not join several statements onto a line with semicolons. — [Google Python: 3.1 Semicolons](https://google.github.io/styleguide/pyguide.html#semicolons). <!-- google-python:81 -->
- Keep lines within 80 characters except for the source's stated exceptions. — [Google Python: 3.2 Line length](https://google.github.io/styleguide/pyguide.html#line-length). <!-- google-python:82 -->
- Allow longer imports, URLs or paths or flags in comments, whitespace-free module string constants that are inconvenient to split, and pylint suppression comments. — [Google Python: 3.2 Line length](https://google.github.io/styleguide/pyguide.html#line-length). <!-- google-python:83 -->
- Do not continue code with an explicit backslash; this restriction does not forbid escaped newlines inside string literals. — [Google Python: 3.2 Line length](https://google.github.io/styleguide/pyguide.html#line-length). <!-- google-python:84 -->
- Use paired delimiters to continue expressions implicitly across lines. — [Google Python: 3.2 Line length](https://google.github.io/styleguide/pyguide.html#line-length). <!-- google-python:85 -->
- Split an overlong literal into adjacent string pieces inside parentheses when practical. — [Google Python: 3.2 Line length](https://google.github.io/styleguide/pyguide.html#line-length). <!-- google-python:86 -->
- Break at the highest suitable syntax level and keep repeated breaks at that same level. — [Google Python: 3.2 Line length](https://google.github.io/styleguide/pyguide.html#line-length). <!-- google-python:87 -->
- Other lines may exceed 80 characters if Black or Pyink cannot shorten them; improve the breaks manually when it is sensible. — [Google Python: 3.2 Line length](https://google.github.io/styleguide/pyguide.html#line-length). <!-- google-python:90 -->
- Avoid unnecessary parentheses. — [Google Python: 3.3 Parentheses](https://google.github.io/styleguide/pyguide.html#parentheses). <!-- google-python:91 -->
- Leave conditions and return expressions unparenthesized unless a tuple or implicit continuation needs the delimiters. — [Google Python: 3.3 Parentheses](https://google.github.io/styleguide/pyguide.html#parentheses). <!-- google-python:92 -->
- Use an indentation increment of four spaces for blocks. — [Google Python: 3.4 Indentation](https://google.github.io/styleguide/pyguide.html#indentation). <!-- google-python:93 -->
- Use spaces exclusively for indentation. — [Google Python: 3.4 Indentation](https://google.github.io/styleguide/pyguide.html#indentation). <!-- google-python:94 -->
- Align a continuation with the opening delimiter or give it a four-space hanging indent. — [Google Python: 3.4 Indentation](https://google.github.io/styleguide/pyguide.html#indentation). <!-- google-python:95 -->
- When a closing delimiter occupies its own line, align it with the line that contains the opening delimiter. — [Google Python: 3.4 Indentation](https://google.github.io/styleguide/pyguide.html#indentation). <!-- google-python:96 -->
- Prefer a trailing comma when the closing delimiter is on another line, and include the required comma in a singleton tuple. — [Google Python: 3.4.1 Trailing commas in sequences of items?](https://google.github.io/styleguide/pyguide.html#trailing-comma). <!-- google-python:97 -->
- A trailing comma may intentionally ask Black or Pyink to keep a sequence vertically expanded. — [Google Python: 3.4.1 Trailing commas in sequences of items?](https://google.github.io/styleguide/pyguide.html#trailing-comma). <!-- google-python:98 -->
- Separate module-level definitions with two empty lines. — [Google Python: 3.5 Blank Lines](https://google.github.io/styleguide/pyguide.html#blank-lines). <!-- google-python:99 -->
- Leave one empty line between methods and after a class docstring. — [Google Python: 3.5 Blank Lines](https://google.github.io/styleguide/pyguide.html#blank-lines). <!-- google-python:100 -->
- Begin the function body immediately after its `def` header without an intervening blank line. — [Google Python: 3.5 Blank Lines](https://google.github.io/styleguide/pyguide.html#blank-lines). <!-- google-python:101 -->
- Use individual blank lines inside a function to separate logical steps. — [Google Python: 3.5 Blank Lines](https://google.github.io/styleguide/pyguide.html#blank-lines). <!-- google-python:102 -->
- Do not insert whitespace just inside paired delimiters. — [Google Python: 3.6 Whitespace](https://google.github.io/styleguide/pyguide.html#whitespace). <!-- google-python:104 -->
- Put commas, semicolons, and nonslice colons directly after the preceding text. — [Google Python: 3.6 Whitespace](https://google.github.io/styleguide/pyguide.html#whitespace). <!-- google-python:105 -->
- Normally follow those punctuation marks with one space, except when they end a line. — [Google Python: 3.6 Whitespace](https://google.github.io/styleguide/pyguide.html#whitespace). <!-- google-python:106 -->
- Attach call, indexing, and slicing delimiters directly to their target expression. — [Google Python: 3.6 Whitespace](https://google.github.io/styleguide/pyguide.html#whitespace). <!-- google-python:107 -->
- Remove whitespace left at the ends of lines. — [Google Python: 3.6 Whitespace](https://google.github.io/styleguide/pyguide.html#whitespace). <!-- google-python:108 -->
- Give assignment, comparison, and Boolean operators one space on either side. — [Google Python: 3.6 Whitespace](https://google.github.io/styleguide/pyguide.html#whitespace). <!-- google-python:109 -->
- Choose arithmetic-operator spacing according to readability. — [Google Python: 3.6 Whitespace](https://google.github.io/styleguide/pyguide.html#whitespace). <!-- google-python:110 -->
- Keep equals signs unpadded in keyword arguments and defaults for unannotated parameters. — [Google Python: 3.6 Whitespace](https://google.github.io/styleguide/pyguide.html#whitespace). <!-- google-python:111 -->
- Surround an annotated parameter's default equals sign with spaces. — [Google Python: 3.6 Whitespace](https://google.github.io/styleguide/pyguide.html#whitespace). <!-- google-python:112 -->
- Do not add padding to line up tokens across neighboring lines. — [Google Python: 3.6 Whitespace](https://google.github.io/styleguide/pyguide.html#whitespace). <!-- google-python:113 -->
- Give a directly executable Python file a shebang that selects Python 3. — [Google Python: 3.7 Shebang Line](https://google.github.io/styleguide/pyguide.html#shebang-line). <!-- google-python:114 -->
- Leave the shebang out of ordinary modules that are only imported. — [Google Python: 3.7 Shebang Line](https://google.github.io/styleguide/pyguide.html#shebang-line). <!-- google-python:115 -->
- Keep ordinary string quotes consistent within a file, changing the delimiter when it avoids an escape. — [Google Python: 3.10 Strings](https://google.github.io/styleguide/pyguide.html#strings). <!-- google-python:161 -->
- Normally delimit multiline strings with triple double quotes. — [Google Python: 3.10 Strings](https://google.github.io/styleguide/pyguide.html#strings). <!-- google-python:162 -->
- A file that consistently uses single quotes may also use triple single quotes for multiline text that is not a docstring. — [Google Python: 3.10 Strings](https://google.github.io/styleguide/pyguide.html#strings). <!-- google-python:163 -->
- Write each import on its own line except for the permitted combined static-typing symbol imports. — [Google Python: 3.13 Imports formatting](https://google.github.io/styleguide/pyguide.html#imports-formatting). <!-- google-python:181 -->
- Place imports after module documentation or comments and before global variables and constants. — [Google Python: 3.13 Imports formatting](https://google.github.io/styleguide/pyguide.html#imports-formatting). <!-- google-python:182 -->
- Group imports in order of future features, standard library, third-party packages, and repository subpackages. — [Google Python: 3.13 Imports formatting](https://google.github.io/styleguide/pyguide.html#imports-formatting). <!-- google-python:183 -->
- Treat same-top-level application imports like other repository subpackage imports; do not add the deprecated extra group. — [Google Python: 3.13 Imports formatting](https://google.github.io/styleguide/pyguide.html#imports-formatting). <!-- google-python:184 -->
- Sort imports within each group by full package path in case-insensitive lexicographic order. — [Google Python: 3.13 Imports formatting](https://google.github.io/styleguide/pyguide.html#imports-formatting). <!-- google-python:185 -->
- Separate import groups with blank lines if desired; the guide does not require them. — [Google Python: 3.13 Imports formatting](https://google.github.io/styleguide/pyguide.html#imports-formatting). <!-- google-python:186 -->
- Normally give each statement a line of its own. — [Google Python: 3.14 Statements](https://google.github.io/styleguide/pyguide.html#statements). <!-- google-python:187 -->
- A complete, simple `if` statement may share its line with its body when it has no `else`. — [Google Python: 3.14 Statements](https://google.github.io/styleguide/pyguide.html#statements). <!-- google-python:188 -->
- Keep control statements with several clauses expanded over multiple lines. — [Google Python: 3.14 Statements](https://google.github.io/styleguide/pyguide.html#statements). <!-- google-python:189 -->
- Put related functions and classes together in modules rather than requiring a separate file for every class. — [Google Python: 3.16 Naming](https://google.github.io/styleguide/pyguide.html#naming). <!-- google-python:204 -->
- Provide a launcher or symbolic link when an executable needs a name without a file extension. — [Google Python: 3.16.3 File Naming](https://google.github.io/styleguide/pyguide.html#file-naming). <!-- google-python:209 -->
- Place a program's executable work in a `main` function. — [Google Python: 3.17 Main](https://google.github.io/styleguide/pyguide.html#main). <!-- google-python:214 -->
- Guard the entrypoint with the `__name__` check so the module can be imported without starting the program. — [Google Python: 3.17 Main](https://google.github.io/styleguide/pyguide.html#main). <!-- google-python:215 -->
- Favor small functions with a focused purpose. — [Google Python: 3.18 Function length](https://google.github.io/styleguide/pyguide.html#function-length). <!-- google-python:218 -->
- Reassess a function near 40 lines, treating that size as a prompt for review rather than a fixed limit. — [Google Python: 3.18 Function length](https://google.github.io/styleguide/pyguide.html#function-length). <!-- google-python:219 -->
- Extract reusable or hard-to-change and hard-to-debug parts when doing so makes the design clearer. — [Google Python: 3.18 Function length](https://google.github.io/styleguide/pyguide.html#function-length). <!-- google-python:220 -->
- Break a long signature between parameters before separating a parameter name from its type. — [Google Python: 3.19.2 Line Breaking](https://google.github.io/styleguide/pyguide.html#typing-line-breaking). <!-- google-python:226 -->
- For an overlong signature, place parameters and usually the return annotation on separate lines using normal hanging indentation. — [Google Python: 3.19.2 Line Breaking](https://google.github.io/styleguide/pyguide.html#typing-line-breaking). <!-- google-python:227 -->
- Align a multiline signature's closing delimiter with its `def` keyword. — [Google Python: 3.19.2 Line Breaking](https://google.github.io/styleguide/pyguide.html#typing-line-breaking). <!-- google-python:228 -->
- Keep a type or constituent subtype together on one line when possible. — [Google Python: 3.19.2 Line Breaking](https://google.github.io/styleguide/pyguide.html#typing-line-breaking). <!-- google-python:229 -->
- Try a type alias before splitting an overlong parameter-and-type pair immediately after the colon. — [Google Python: 3.19.2 Line Breaking](https://google.github.io/styleguide/pyguide.html#typing-line-breaking). <!-- google-python:230 -->
- Space the equals sign around a default value when the parameter is annotated. — [Google Python: 3.19.4 Default Values](https://google.github.io/styleguide/pyguide.html#typing-default-values). <!-- google-python:232 -->
- For static analysis, import needed symbols directly from `typing` and `collections.abc`. — [Google Python: 3.19.12 Imports For Typing](https://google.github.io/styleguide/pyguide.html#typing-imports). <!-- google-python:247 -->
- Several static-typing symbols from one of those modules may share a `from` import line. — [Google Python: 3.19.12 Imports For Typing](https://google.github.io/styleguide/pyguide.html#typing-imports). <!-- google-python:248 -->
- Alias an imported typing name if it conflicts with an identifier already used in the module. — [Google Python: 3.19.12 Imports For Typing](https://google.github.io/styleguide/pyguide.html#typing-imports). <!-- google-python:250 -->
- Reserve `TYPE_CHECKING` imports for exceptional runtime-import constraints; prefer refactoring toward ordinary top-level imports. — [Google Python: 3.19.13 Conditional Imports](https://google.github.io/styleguide/pyguide.html#typing-conditional-imports). <!-- google-python:253 -->
- Limit the conditional typing block to entities used exclusively for annotations, including any aliases it defines. — [Google Python: 3.19.13 Conditional Imports](https://google.github.io/styleguide/pyguide.html#typing-conditional-imports). <!-- google-python:254 -->
- Place a conditional typing-import block directly after the regular imports. — [Google Python: 3.19.13 Conditional Imports](https://google.github.io/styleguide/pyguide.html#typing-conditional-imports). <!-- google-python:256 -->
- Sort conditional typing imports by the ordinary import rules and keep their list free of blank lines. — [Google Python: 3.19.13 Conditional Imports](https://google.github.io/styleguide/pyguide.html#typing-conditional-imports). <!-- google-python:257 -->
- Leave one blank line between the final import and aliases used to break a typing dependency cycle. — [Google Python: 3.19.14 Circular Dependencies](https://google.github.io/styleguide/pyguide.html#typing-circular-deps). <!-- google-python:260 -->

## Types and data

- Keep mutable state out of module globals where possible. — [Google Python: 2.5 Mutable Global State](https://google.github.io/styleguide/pyguide.html#global-variables). <!-- google-python:23 -->
- Provide functions or class methods for external access to necessary shared mutable state. — [Google Python: 2.5 Mutable Global State](https://google.github.io/styleguide/pyguide.html#global-variables). <!-- google-python:25 -->
- Choose comprehensions for straightforward transformations whose meaning remains easy to read. — [Google Python: 2.7 Comprehensions & Generator Expressions](https://google.github.io/styleguide/pyguide.html#comprehensions). <!-- google-python:30 -->
- Keep a comprehension or generator expression to one `for` clause and at most one filtering expression. — [Google Python: 2.7 Comprehensions & Generator Expressions](https://google.github.io/styleguide/pyguide.html#comprehensions). <!-- google-python:31 -->
- Favor a readable transformation over saving characters. — [Google Python: 2.7 Comprehensions & Generator Expressions](https://google.github.io/styleguide/pyguide.html#comprehensions). <!-- google-python:32 -->
- Use the container's built-in iteration protocol and membership operators directly. — [Google Python: 2.8 Default Iterators and Operators](https://google.github.io/styleguide/pyguide.html#default-iterators-operators). <!-- google-python:33 -->
- Use a generator when incremental production fits the problem. — [Google Python: 2.9 Generators](https://google.github.io/styleguide/pyguide.html#generators). <!-- google-python:36 -->
- Limit lambdas to uncomplicated expressions that fit on one line. — [Google Python: 2.10 Lambda Functions](https://google.github.io/styleguide/pyguide.html#lambdas). <!-- google-python:39 -->
- Favor a generator expression over passing a lambda to `map` or `filter`. — [Google Python: 2.10 Lambda Functions](https://google.github.io/styleguide/pyguide.html#lambdas). <!-- google-python:40 -->
- Use an appropriate function from `operator` instead of wrapping an ordinary operator in a lambda. — [Google Python: 2.10 Lambda Functions](https://google.github.io/styleguide/pyguide.html#lambdas). <!-- google-python:42 -->
- Use a conditional expression for simple choices only. — [Google Python: 2.11 Conditional Expressions](https://google.github.io/styleguide/pyguide.html#conditional-expressions). <!-- google-python:43 -->
- Use an `if` statement when the choice is too involved for a readable conditional expression. — [Google Python: 2.11 Conditional Expressions](https://google.github.io/styleguide/pyguide.html#conditional-expressions). <!-- google-python:45 -->
- Use default parameter values where they make the interface useful. — [Google Python: 2.12 Default Argument Values](https://google.github.io/styleguide/pyguide.html#default-arguments). <!-- google-python:46 -->
- Restrict property access to simple, inexpensive behavior that callers would expect from an attribute. — [Google Python: 2.13 Properties](https://google.github.io/styleguide/pyguide.html#properties). <!-- google-python:48 -->
- Expose stored data directly instead of adding a property that does nothing but forward access. — [Google Python: 2.13 Properties](https://google.github.io/styleguide/pyguide.html#properties). <!-- google-python:49 -->
- Define ordinary properties with `@property` rather than writing a custom descriptor. — [Google Python: 2.13 Properties](https://google.github.io/styleguide/pyguide.html#properties). <!-- google-python:50 -->
- Avoid making a property out of computation that subclasses may need to override and extend. — [Google Python: 2.13 Properties](https://google.github.io/styleguide/pyguide.html#properties). <!-- google-python:51 -->
- Use implicit truth-value testing when it captures the intended condition. — [Google Python: 2.14 True/False Evaluations](https://google.github.io/styleguide/pyguide.html#truefalse-evaluations). <!-- google-python:52 -->
- Distinguish `None` with an identity comparison. — [Google Python: 2.14 True/False Evaluations](https://google.github.io/styleguide/pyguide.html#truefalse-evaluations). <!-- google-python:53 -->
- Negate a Boolean value directly instead of comparing it with `False`. — [Google Python: 2.14 True/False Evaluations](https://google.github.io/styleguide/pyguide.html#truefalse-evaluations). <!-- google-python:54 -->
- Test explicitly when the distinction between `False` and `None` affects behavior. — [Google Python: 2.14 True/False Evaluations](https://google.github.io/styleguide/pyguide.html#truefalse-evaluations). <!-- google-python:55 -->
- Check sequence emptiness through its truth value instead of measuring its length. — [Google Python: 2.14 True/False Evaluations](https://google.github.io/styleguide/pyguide.html#truefalse-evaluations). <!-- google-python:56 -->
- For a known integer, a direct comparison with zero is acceptable when it avoids confusing zero with `None`. — [Google Python: 2.14 True/False Evaluations](https://google.github.io/styleguide/pyguide.html#truefalse-evaluations). <!-- google-python:57 -->
- Apply a decorator only when its advantage is clear. — [Google Python: 2.17 Function and Method Decorators](https://google.github.io/styleguide/pyguide.html#decorators). <!-- google-python:60 -->
- Reserve `classmethod` for named constructors and necessary operations on state belonging to the class as a whole. — [Google Python: 2.17 Function and Method Decorators](https://google.github.io/styleguide/pyguide.html#decorators). <!-- google-python:67 -->
- Standard-library abstractions remain acceptable even when their implementations use otherwise discouraged advanced features. — [Google Python: 2.19 Power Features](https://google.github.io/styleguide/pyguide.html#power-features). <!-- google-python:72 -->
- Prefer annotations in implementation files, using stubs when suitable for external packages or extension modules. — [Google Python: 2.21 Type Annotated Code](https://google.github.io/styleguide/pyguide.html#typed-code). <!-- google-python:78 -->
- Choose f-strings, percent interpolation, or `format` for string formatting. — [Google Python: 3.10 Strings](https://google.github.io/styleguide/pyguide.html#strings). <!-- google-python:157 -->
- A single uncomplicated concatenation is acceptable; use formatting instead of assembling a pattern from many `+` fragments. — [Google Python: 3.10 Strings](https://google.github.io/styleguide/pyguide.html#strings). <!-- google-python:158 -->
- Use adjacent literals or `textwrap.dedent` when source indentation would otherwise become unwanted string content. — [Google Python: 3.10 Strings](https://google.github.io/styleguide/pyguide.html#strings). <!-- google-python:165 -->
- Use accessor methods when reading or writing a value performs substantial logic or has noticeable cost. — [Google Python: 3.15 Getters and Setters](https://google.github.io/styleguide/pyguide.html#getters-and-setters). <!-- google-python:190 -->
- Expose a simple field directly rather than wrapping an ordinary read or assignment in accessor methods. — [Google Python: 3.15 Getters and Setters](https://google.github.io/styleguide/pyguide.html#getters-and-setters). <!-- google-python:191 -->
- Usually omit annotations for `self` and `cls`; use `Self` when it adds necessary precision. — [Google Python: 3.19.1 General Rules](https://google.github.io/styleguide/pyguide.html#typing-general). <!-- google-python:221 -->
- An explicit `None` return annotation on `__init__` is optional under this guide. — [Google Python: 3.19.1 General Rules](https://google.github.io/styleguide/pyguide.html#typing-general). <!-- google-python:222 -->
- Use `Any` when the type is intentionally left unspecified. — [Google Python: 3.19.1 General Rules](https://google.github.io/styleguide/pyguide.html#typing-general). <!-- google-python:223 -->
- Annotate public APIs at a minimum. — [Google Python: 3.19.1 General Rules](https://google.github.io/styleguide/pyguide.html#typing-general). <!-- google-python:224 -->
- Prioritize annotations for confusing code, code prone to type mistakes, and mature stable interfaces. — [Google Python: 3.19.1 General Rules](https://google.github.io/styleguide/pyguide.html#typing-general). <!-- google-python:225 -->
- Use postponed annotation evaluation or a quoted reference when an annotation names a class that is not yet defined. — [Google Python: 3.19.3 Forward Declarations](https://google.github.io/styleguide/pyguide.html#forward-declarations). <!-- google-python:231 -->
- Include `None` explicitly in the type of every parameter that accepts it. — [Google Python: 3.19.5 NoneType](https://google.github.io/styleguide/pyguide.html#none-type). <!-- google-python:233 -->
- Prefer the `X | None` spelling for nullable types in new code targeting Python 3.10 or later. — [Google Python: 3.19.5 NoneType](https://google.github.io/styleguide/pyguide.html#none-type). <!-- google-python:234 -->
- Do not treat a default value of `None` as an implicit nullable annotation. — [Google Python: 3.19.5 NoneType](https://google.github.io/styleguide/pyguide.html#none-type). <!-- google-python:235 -->
- Mark aliases with `typing.TypeAlias` to distinguish them from ordinary global values, as this source prescribes. — [Google Python: 3.19.6 Type Aliases](https://google.github.io/styleguide/pyguide.html#type-aliases). <!-- google-python:237 -->
- Do not turn a type alias into a workaround for forbidden symbol imports; a private shortening of an inconvenient type name may remain outside the public API. — [Google Python: 3.19.6 Type Aliases](https://google.github.io/styleguide/pyguide.html#type-aliases). <!-- google-python:238 -->
- Add an annotated assignment when a local implementation variable's type cannot be inferred clearly. — [Google Python: 3.19.8 Typing Variables](https://google.github.io/styleguide/pyguide.html#typing-variables). <!-- google-python:240 -->
- Do not introduce the older end-of-line type-comment syntax. — [Google Python: 3.19.8 Typing Variables](https://google.github.io/styleguide/pyguide.html#typing-variables). <!-- google-python:241 -->
- Use one shared type variable for related arguments and results that must consistently choose either `str` or `bytes`. — [Google Python: 3.19.10 Type variables](https://google.github.io/styleguide/pyguide.html#typevars). <!-- google-python:242 -->
- Represent textual content with `str` and binary content with `bytes`. — [Google Python: 3.19.11 String types](https://google.github.io/styleguide/pyguide.html#typing-strings). <!-- google-python:244 -->
- Avoid the compatibility alias `typing.Text` in newly written code. — [Google Python: 3.19.11 String types](https://google.github.io/styleguide/pyguide.html#typing-strings). <!-- google-python:245 -->
- Express a required common string type across multiple positions with a suitable shared type variable. — [Google Python: 3.19.11 String types](https://google.github.io/styleguide/pyguide.html#typing-strings). <!-- google-python:246 -->
- Prefer abstract container interfaces in function parameter annotations. — [Google Python: 3.19.12 Imports For Typing](https://google.github.io/styleguide/pyguide.html#typing-imports). <!-- google-python:251 -->
- When a concrete generic is necessary, use the built-in type rather than its older alias in `typing`. — [Google Python: 3.19.12 Imports For Typing](https://google.github.io/styleguide/pyguide.html#typing-imports). <!-- google-python:252 -->
- Prefer refactoring when type annotations introduce a circular module dependency. — [Google Python: 3.19.14 Circular Dependencies](https://google.github.io/styleguide/pyguide.html#typing-circular-deps). <!-- google-python:258 -->
- For a remaining typing cycle, the source permits a meaningfully named module alias bound to `Any`, sacrificing static precision to avoid the import. — [Google Python: 3.19.14 Circular Dependencies](https://google.github.io/styleguide/pyguide.html#typing-circular-deps). <!-- google-python:259 -->
- Write generic type arguments explicitly instead of leaving them to become implicit `Any` values. — [Google Python: 3.19.15 Generics](https://google.github.io/styleguide/pyguide.html#generics). <!-- google-python:261 -->
- Spell out `Any` when it is the intended generic argument. — [Google Python: 3.19.15 Generics](https://google.github.io/styleguide/pyguide.html#generics). <!-- google-python:262 -->
- Consider a type variable when it can express a relationship more accurately than `Any`. — [Google Python: 3.19.15 Generics](https://google.github.io/styleguide/pyguide.html#generics). <!-- google-python:263 -->

## Errors

- Choose an existing built-in exception when it accurately represents a failure or violated precondition. — [Google Python: 2.4 Exceptions](https://google.github.io/styleguide/pyguide.html#exceptions). <!-- google-python:15 -->
- Keep validation and required application behavior independent of assertions; an assertion must be removable without breaking correctness. — [Google Python: 2.4 Exceptions](https://google.github.io/styleguide/pyguide.html#exceptions). <!-- google-python:16 -->
- Derive a custom exception from an exception class that already exists. — [Google Python: 2.4 Exceptions](https://google.github.io/styleguide/pyguide.html#exceptions). <!-- google-python:18 -->
- Catch all exceptions only to re-raise them or at a deliberate boundary that records and suppresses failures. — [Google Python: 2.4 Exceptions](https://google.github.io/styleguide/pyguide.html#exceptions). <!-- google-python:20 -->
- Keep a `try` suite small enough that its handler cannot accidentally conceal unrelated failures. — [Google Python: 2.4 Exceptions](https://google.github.io/styleguide/pyguide.html#exceptions). <!-- google-python:21 -->
- Put cleanup required after both successful and failing execution in a `finally` clause. — [Google Python: 2.4 Exceptions](https://google.github.io/styleguide/pyguide.html#exceptions). <!-- google-python:22 -->
- Arrange explicit cleanup for expensive resources retained by a generator, using a context manager when suitable. — [Google Python: 2.9 Generators](https://google.github.io/styleguide/pyguide.html#generators). <!-- google-python:38 -->
- Make decorator application succeed whenever its arguments satisfy the decorator's contract. — [Google Python: 2.17 Function and Method Decorators](https://google.github.io/styleguide/pyguide.html#decorators). <!-- google-python:65 -->
- Write error text that identifies the condition that actually failed. — [Google Python: 3.10.2 Error Messages](https://google.github.io/styleguide/pyguide.html#error-messages). <!-- google-python:168 -->
- Delimit substituted values clearly so readers can separate them from the surrounding error message. — [Google Python: 3.10.2 Error Messages](https://google.github.io/styleguide/pyguide.html#error-messages). <!-- google-python:169 -->
- Keep diagnostic messages easy to locate and process with simple tools. — [Google Python: 3.10.2 Error Messages](https://google.github.io/styleguide/pyguide.html#error-messages). <!-- google-python:170 -->
- Release owned files, sockets, mappings, database connections, and other closeable resources promptly. — [Google Python: 3.11 Files, Sockets, and similar Stateful Resources](https://google.github.io/styleguide/pyguide.html#files). <!-- google-python:171 -->
- Prefer a `with` statement to delimit resource ownership. — [Google Python: 3.11 Files, Sockets, and similar Stateful Resources](https://google.github.io/styleguide/pyguide.html#files). <!-- google-python:173 -->
- Use `contextlib.closing` when an appropriate closeable resource lacks context-manager support. — [Google Python: 3.11 Files, Sockets, and similar Stateful Resources](https://google.github.io/styleguide/pyguide.html#files). <!-- google-python:174 -->

## Comments and docs

- Include the file header required by the project's license. — [Google — Comments and docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

- Explain the need for global mutable state in a comment or linked design document. — [Google Python: 2.5 Mutable Global State](https://google.github.io/styleguide/pyguide.html#global-variables). <!-- google-python:26 -->
- Describe generated values in a `Yields` section rather than under `Returns`. — [Google Python: 2.9 Generators](https://google.github.io/styleguide/pyguide.html#generators). <!-- google-python:37 -->
- Identify a decorator as such in its docstring. — [Google Python: 2.17 Function and Method Decorators](https://google.github.io/styleguide/pyguide.html#decorators). <!-- google-python:62 -->
- Move a lengthy URL in a comment onto a line of its own when needed. — [Google Python: 3.2 Line length](https://google.github.io/styleguide/pyguide.html#line-length). <!-- google-python:88 -->
- Keep a docstring's summary line within the 80-character limit. — [Google Python: 3.2 Line length](https://google.github.io/styleguide/pyguide.html#line-length). <!-- google-python:89 -->
- Keep definition-specific comments attached to that definition, considering a docstring when it would be a better home. — [Google Python: 3.5 Blank Lines](https://google.github.io/styleguide/pyguide.html#blank-lines). <!-- google-python:103 -->
- Use triple-double-quote delimiters for docstrings. — [Google Python: 3.8.1 Docstrings](https://google.github.io/styleguide/pyguide.html#docstrings). <!-- google-python:116 -->
- Open a docstring with a single summary line of at most 80 characters. — [Google Python: 3.8.1 Docstrings](https://google.github.io/styleguide/pyguide.html#docstrings). <!-- google-python:117 -->
- Terminate the summary with a period, exclamation mark, or question mark. — [Google Python: 3.8.1 Docstrings](https://google.github.io/styleguide/pyguide.html#docstrings). <!-- google-python:118 -->
- Put an empty line between the summary and any further explanation. — [Google Python: 3.8.1 Docstrings](https://google.github.io/styleguide/pyguide.html#docstrings). <!-- google-python:119 -->
- Indent the remaining description to align with the opening quote position. — [Google Python: 3.8.1 Docstrings](https://google.github.io/styleguide/pyguide.html#docstrings). <!-- google-python:120 -->
- Start a module with a docstring explaining what it contains and how it is used. — [Google Python: 3.8.2 Modules](https://google.github.io/styleguide/pyguide.html#module-docs). <!-- google-python:122 -->
- Give each public, nontrivial, or non-obvious callable a docstring, including generators and properties. — [Google Python: 3.8.3 Functions and Methods](https://google.github.io/styleguide/pyguide.html#function-docs). <!-- google-python:127 -->
- Provide enough interface detail for someone to call the function without inspecting its body. — [Google Python: 3.8.3 Functions and Methods](https://google.github.io/styleguide/pyguide.html#function-docs). <!-- google-python:128 -->
- Describe mutations and other effects observable by callers. — [Google Python: 3.8.3 Functions and Methods](https://google.github.io/styleguide/pyguide.html#function-docs). <!-- google-python:129 -->
- Place implementation rationale that does not affect callers in code comments instead of the API contract. — [Google Python: 3.8.3 Functions and Methods](https://google.github.io/styleguide/pyguide.html#function-docs). <!-- google-python:130 -->
- Choose either descriptive or imperative docstring summaries and apply that choice consistently within each file. — [Google Python: 3.8.3 Functions and Methods](https://google.github.io/styleguide/pyguide.html#function-docs). <!-- google-python:131 -->
- Describe a property's value as an attribute, without a sentence announcing that it returns something. — [Google Python: 3.8.3 Functions and Methods](https://google.github.io/styleguide/pyguide.html#function-docs). <!-- google-python:132 -->
- When a concise summary cannot cover the contract, use `Args`, `Returns` or `Yields`, and `Raises` sections with colon-ended headings. — [Google Python: 3.8.3 Functions and Methods](https://google.github.io/styleguide/pyguide.html#function-docs). <!-- google-python:133 -->
- Use a consistent hanging indent of either two or four spaces for docstring section contents. — [Google Python: 3.8.3 Functions and Methods](https://google.github.io/styleguide/pyguide.html#function-docs). <!-- google-python:134 -->
- List argument names exactly as declared in `Args`, retaining `*` and `**` on variadic parameters and separating descriptions with a colon. — [Google Python: 3.8.3 Functions and Methods](https://google.github.io/styleguide/pyguide.html#function-docs). <!-- google-python:135 -->
- Document parameter types when corresponding annotations are absent. — [Google Python: 3.8.3 Functions and Methods](https://google.github.io/styleguide/pyguide.html#function-docs). <!-- google-python:136 -->
- Explain the returned value's meaning and any type information not already expressed by its annotation. — [Google Python: 3.8.3 Functions and Methods](https://google.github.io/styleguide/pyguide.html#function-docs). <!-- google-python:137 -->
- Omit `Returns` for a `None`-only result, or when an adequate opening sentence beginning with Return, Returns, Yield, or Yields describes the result. — [Google Python: 3.8.3 Functions and Methods](https://google.github.io/styleguide/pyguide.html#function-docs). <!-- google-python:138 -->
- Describe a tuple result as one tuple with meaningful components, rather than as several independently returned values. — [Google Python: 3.8.3 Functions and Methods](https://google.github.io/styleguide/pyguide.html#function-docs). <!-- google-python:139 -->
- For a generator, document the value produced by each advance in `Yields`, rather than the generator object itself. — [Google Python: 3.8.3 Functions and Methods](https://google.github.io/styleguide/pyguide.html#function-docs). <!-- google-python:140 -->
- List exceptions that belong to the interface, without making failures from violating its preconditions part of the promised contract. — [Google Python: 3.8.3 Functions and Methods](https://google.github.io/styleguide/pyguide.html#function-docs). <!-- google-python:141 -->
- Document the callable's behavior as seen after its decorators have taken effect. — [Google Python: 3.8.3 Functions and Methods](https://google.github.io/styleguide/pyguide.html#function-docs). <!-- google-python:142 -->
- A method marked `@override` may rely on the inherited documentation when its contract is unchanged. — [Google Python: 3.8.3.1 Overridden Methods](https://google.github.io/styleguide/pyguide.html#overridden-method-docs). <!-- google-python:143 -->
- Document changes to the inherited contract, additional effects, or material refinements even when the method uses `@override`. — [Google Python: 3.8.3.1 Overridden Methods](https://google.github.io/styleguide/pyguide.html#overridden-method-docs). <!-- google-python:144 -->
- Put a class's docstring immediately inside its definition. — [Google Python: 3.8.4 Classes](https://google.github.io/styleguide/pyguide.html#class-docs). <!-- google-python:145 -->
- Start a class docstring by explaining what an instance represents. — [Google Python: 3.8.4 Classes](https://google.github.io/styleguide/pyguide.html#class-docs). <!-- google-python:146 -->
- List public attributes other than properties in an `Attributes` section formatted like `Args`. — [Google Python: 3.8.4 Classes](https://google.github.io/styleguide/pyguide.html#class-docs). <!-- google-python:147 -->
- Describe the meaning of an exception object instead of only saying when code might raise it. — [Google Python: 3.8.4 Classes](https://google.github.io/styleguide/pyguide.html#class-docs). <!-- google-python:148 -->
- Avoid wasting class documentation on the fact that the object is a class. — [Google Python: 3.8.4 Classes](https://google.github.io/styleguide/pyguide.html#class-docs). <!-- google-python:149 -->
- For a decorated class, describe the behavior that remains after decoration. — [Google Python: 3.8.4 Classes](https://google.github.io/styleguide/pyguide.html#class-docs). <!-- google-python:150 -->
- Explain complicated intent before the relevant operation, or briefly alongside it when that suffices. — [Google Python: 3.8.5 Block and Inline Comments](https://google.github.io/styleguide/pyguide.html#comments). <!-- google-python:151 -->
- Leave at least two spaces before an inline comment's hash. — [Google Python: 3.8.5 Block and Inline Comments](https://google.github.io/styleguide/pyguide.html#comments). <!-- google-python:152 -->
- Put at least one space between the comment marker and its text. — [Google Python: 3.8.5 Block and Inline Comments](https://google.github.io/styleguide/pyguide.html#comments). <!-- google-python:153 -->
- Explain purpose rather than narrating Python operations the reader can already understand. — [Google Python: 3.8.5 Block and Inline Comments](https://google.github.io/styleguide/pyguide.html#comments). <!-- google-python:154 -->
- Write comments with readable spelling, grammar, capitalization, and punctuation. — [Google Python: 3.8.6 Punctuation, Spelling, and Grammar](https://google.github.io/styleguide/pyguide.html#punctuation-spelling-grammar). <!-- google-python:155 -->
- Short end-of-line comments may use a less formal style, provided nearby comments remain consistent. — [Google Python: 3.8.6 Punctuation, Spelling, and Grammar](https://google.github.io/styleguide/pyguide.html#punctuation-spelling-grammar). <!-- google-python:156 -->
- Retain triple double quotes for docstrings regardless of the file's ordinary string convention. — [Google Python: 3.10 Strings](https://google.github.io/styleguide/pyguide.html#strings). <!-- google-python:164 -->
- Explain how a resource's lifetime ends when using a context manager is impractical. — [Google Python: 3.11 Files, Sockets, and similar Stateful Resources](https://google.github.io/styleguide/pyguide.html#files). <!-- google-python:175 -->
- Mark deliberately temporary or incomplete work with `TODO`. — [Google Python: 3.12 TODO Comments](https://google.github.io/styleguide/pyguide.html#todo). <!-- google-python:176 -->
- Follow `TODO` with a context link in parentheses, then a colon and an explanation. — [Google Python: 3.12 TODO Comments](https://google.github.io/styleguide/pyguide.html#todo). <!-- google-python:177 -->
- Prefer linking a tracked issue so the TODO has a place for follow-up discussion. — [Google Python: 3.12 TODO Comments](https://google.github.io/styleguide/pyguide.html#todo). <!-- google-python:178 -->
- Use a contextual resource instead of an individual's or team's name in a new TODO. — [Google Python: 3.12 TODO Comments](https://google.github.io/styleguide/pyguide.html#todo). <!-- google-python:179 -->
- For deferred cleanup, name a precise date or an event that future maintainers can recognize. — [Google Python: 3.12 TODO Comments](https://google.github.io/styleguide/pyguide.html#todo). <!-- google-python:180 -->
- Cite the source of mathematical notation or explain it in comments or documentation. — [Google Python: 3.16.5 Mathematical Notation](https://google.github.io/styleguide/pyguide.html#math-notation). <!-- google-python:211 -->

## Testing

- Use pytest assertions to express the outcomes a test expects. — [Google Python: 2.4 Exceptions](https://google.github.io/styleguide/pyguide.html#exceptions). <!-- google-python:17 -->
- Test the behavior supplied by decorators. — [Google Python: 2.17 Function and Method Decorators](https://google.github.io/styleguide/pyguide.html#decorators). <!-- google-python:63 -->
- A module containing tests may omit its module docstring. — [Google Python: 3.8.2.1 Test modules](https://google.github.io/styleguide/pyguide.html#test-docs). <!-- google-python:123 -->
- Docstrings are optional on `unittest.TestCase` subclasses and their `test_` methods. — [Google Python: 3.8.2.1 Test modules](https://google.github.io/styleguide/pyguide.html#test-docs). <!-- google-python:124 -->
- Leave out test docstrings that merely rephrase the test's name. — [Google Python: 3.8.2.1 Test modules](https://google.github.io/styleguide/pyguide.html#test-docs). <!-- google-python:125 -->
- Document test-specific information that helps a reader, such as unusual setup, required dependencies, or execution details. — [Google Python: 3.8.2.1 Test modules](https://google.github.io/styleguide/pyguide.html#test-docs). <!-- google-python:126 -->
- Tests may read protected constants from the module they exercise. — [Google Python: 3.16 Naming](https://google.github.io/styleguide/pyguide.html#naming). <!-- google-python:203 -->
- Use snake_case for new test names; retain the source's allowed combinations with legacy method names where applicable. — [Google Python: 3.16 Naming](https://google.github.io/styleguide/pyguide.html#naming). <!-- google-python:206 -->

## Performance

- Choose iteration instead of materializing a list when the list is unnecessary. — [Google Python: 2.8 Default Iterators and Operators](https://google.github.io/styleguide/pyguide.html#default-iterators-operators). <!-- google-python:34 -->
- Favor `queue.Queue` for communication between threads. — [Google Python: 2.18 Threading](https://google.github.io/styleguide/pyguide.html#threading). <!-- google-python:69 -->
- Use `threading` synchronization for other coordination, choosing conditions over lower-level locks where they fit. — [Google Python: 2.18 Threading](https://google.github.io/styleguide/pyguide.html#threading). <!-- google-python:70 -->
- Avoid repeated `+` or `+=` operations to grow a string inside a loop. — [Google Python: 3.10 Strings](https://google.github.io/styleguide/pyguide.html#strings). <!-- google-python:159 -->
- Collect text fragments for `join`, or write them to `StringIO`. — [Google Python: 3.10 Strings](https://google.github.io/styleguide/pyguide.html#strings). <!-- google-python:160 -->
- For a logger supporting deferred percent interpolation, pass a literal format pattern and its arguments separately. — [Google Python: 3.10.1 Logging](https://google.github.io/styleguide/pyguide.html#logging). <!-- google-python:166 -->
- Do not pre-interpolate an f-string for a logging API that supports deferred formatting. — [Google Python: 3.10.1 Logging](https://google.github.io/styleguide/pyguide.html#logging). <!-- google-python:167 -->
- When access becomes costly, replace property syntax with explicit method calls so the extra work is visible. — [Google Python: 3.15 Getters and Setters](https://google.github.io/styleguide/pyguide.html#getters-and-setters). <!-- google-python:193 -->

## Language-specific pitfalls

- Do not assume the executable script's directory will be present in `sys.path`. — [Google Python: 2.3 Packages](https://google.github.io/styleguide/pyguide.html#packages). <!-- google-python:14 -->
- Avoid changing a container while iterating through it. — [Google Python: 2.8 Default Iterators and Operators](https://google.github.io/styleguide/pyguide.html#default-iterators-operators). <!-- google-python:35 -->
- Exclude mutable values from function and method defaults. — [Google Python: 2.12 Default Argument Values](https://google.github.io/styleguide/pyguide.html#default-arguments). <!-- google-python:47 -->
- Check a NumPy array's size for emptiness; do not rely on its ambiguous Boolean conversion. — [Google Python: 2.14 True/False Evaluations](https://google.github.io/styleguide/pyguide.html#truefalse-evaluations). <!-- google-python:58 -->
- Closures are allowed, but remember that they capture bindings whose later values may be shared by several closures. — [Google Python: 2.16 Lexical Scoping](https://google.github.io/styleguide/pyguide.html#lexical-scoping). <!-- google-python:59 -->
- Keep decorator evaluation independent of external resources and environmental prerequisites. — [Google Python: 2.17 Function and Method Decorators](https://google.github.io/styleguide/pyguide.html#decorators). <!-- google-python:64 -->
- Use explicit synchronization instead of assuming built-in operations or assignments are atomic. — [Google Python: 2.18 Threading](https://google.github.io/styleguide/pyguide.html#threading). <!-- google-python:68 -->
- Avoid metaclasses, bytecode manipulation, dynamic compilation or inheritance, import tricks, modifications to interpreter internals, and custom `__del__` cleanup. — [Google Python: 2.19 Power Features](https://google.github.io/styleguide/pyguide.html#power-features). <!-- google-python:71 -->
- Use future imports when they safely provide desired behavior on older supported Python versions. — [Google Python: 2.20 Modern Python: from __future__ imports](https://google.github.io/styleguide/pyguide.html#modern-python). <!-- google-python:73 -->
- Remove a future import only after every supported runtime already provides the semantics it enables. — [Google Python: 2.20 Modern Python: from __future__ imports](https://google.github.io/styleguide/pyguide.html#modern-python). <!-- google-python:74 -->
- Keep a future import that guards later edits against older behavior even if it currently appears unnecessary. — [Google Python: 2.20 Modern Python: from __future__ imports](https://google.github.io/styleguide/pyguide.html#modern-python). <!-- google-python:75 -->
- Do not depend on object destruction or finalizers for cleanup with externally visible effects. — [Google Python: 3.11 Files, Sockets, and similar Stateful Resources](https://google.github.io/styleguide/pyguide.html#files). <!-- google-python:172 -->
- Keep import-time behavior safe for documentation tools and test discovery. — [Google Python: 3.17 Main](https://google.github.io/styleguide/pyguide.html#main). <!-- google-python:217 -->
- Quote references to conditionally imported types when supporting the older eager-annotation runtimes discussed by the source. — [Google Python: 3.19.13 Conditional Imports](https://google.github.io/styleguide/pyguide.html#typing-conditional-imports). <!-- google-python:255 -->

## Where the sources disagree

- Use the surrounding code's conventions when the guide leaves a decision open. — [Google Python: 4 Parting Words](https://google.github.io/styleguide/pyguide.html#consistency). <!-- google-python:264 -->
- Do not let local consistency alone preserve a poor old idiom or override updated guidance for the wider codebase. — [Google Python: 4 Parting Words](https://google.github.io/styleguide/pyguide.html#consistency). <!-- google-python:265 -->

## Worked examples

Read [original worked examples and their source tags](examples.md) for small applications of this guide.
