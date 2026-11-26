# PEP 8: condensed rules

Six PEP 8 rules specific to CPython or its standard library are omitted. Preserve the normal 79-column code and 72-column prose limits and the team-agreement exception. An applicable project style guide takes precedence.

Source owner: Guido van Rossum, Barry Warsaw and Alyssa Coghlan. License: [LicenseRef-Public-Domain-PEP](../LICENSE). Changes: rules independently restated, shortened and grouped by topic; examples omitted. Unofficial; no endorsement is implied.

## Tooling

- Treat type checking as an optional, separate analysis step; annotations alone should not change interpreter behavior. — [PEP 8: Function Annotations](https://peps.python.org/pep-0008/#function-annotations). <!-- pep8:154 -->

## Naming

- For open-source projects serving an international audience, consider ASCII identifiers and English words where practical. — [PEP 8: Source File Encoding](https://peps.python.org/pep-0008/#source-file-encoding). <!-- pep8:34 -->
- Choose public API names to reflect what callers do with them, rather than how they work internally. — [PEP 8: Overriding Principle](https://peps.python.org/pep-0008/#overriding-principle). <!-- pep8:87 -->
- Preserve a library's established naming conventions where adopting these conventions would make its interface inconsistent. — [PEP 8: Naming Conventions](https://peps.python.org/pep-0008/#naming-conventions). <!-- pep8:88 -->
- In CapWords names, retain all capitals for an acronym. — [PEP 8: Descriptive: Naming Styles](https://peps.python.org/pep-0008/#descriptive-naming-styles). <!-- pep8:89 -->
- Use leading-and-trailing dunder names only where Python documents them. — [PEP 8: Descriptive: Naming Styles](https://peps.python.org/pep-0008/#descriptive-naming-styles). <!-- pep8:90 -->
- Avoid lone `l`, `O`, or `I` variable names because they resemble digits. — [PEP 8: Names to Avoid](https://peps.python.org/pep-0008/#names-to-avoid). <!-- pep8:91 -->
- Keep module names brief and lowercase, using underscores when they improve readability. — [PEP 8: Package and Module Names](https://peps.python.org/pep-0008/#package-and-module-names). <!-- pep8:92 -->
- Choose short lowercase package names, preferably without underscores. — [PEP 8: Package and Module Names](https://peps.python.org/pep-0008/#package-and-module-names). <!-- pep8:93 -->
- Prefix a C or C++ extension module with an underscore when a Python wrapper supplies its higher-level public API. — [PEP 8: Package and Module Names](https://peps.python.org/pep-0008/#package-and-module-names). <!-- pep8:94 -->
- Use CapWords as the usual class naming convention. — [PEP 8: Class Names](https://peps.python.org/pep-0008/#class-names). <!-- pep8:95 -->
- A class used chiefly as a callable interface may instead follow function naming conventions. — [PEP 8: Class Names](https://peps.python.org/pep-0008/#class-names). <!-- pep8:96 -->
- Respect established built-in naming conventions, including their exceptions for constants and exception classes. — [PEP 8: Class Names](https://peps.python.org/pep-0008/#class-names). <!-- pep8:97 -->
- Give type variables short names in CapWords form. — [PEP 8: Type Variable Names](https://peps.python.org/pep-0008/#type-variable-names). <!-- pep8:98 -->
- Append `_co` for covariant type variables and `_contra` for contravariant ones. — [PEP 8: Type Variable Names](https://peps.python.org/pep-0008/#type-variable-names). <!-- pep8:99 -->
- Name exception classes using the same casing as other classes. — [PEP 8: Exception Names](https://peps.python.org/pep-0008/#exception-names). <!-- pep8:100 -->
- Add `Error` to an exception name when the exception actually represents an error. — [PEP 8: Exception Names](https://peps.python.org/pep-0008/#exception-names). <!-- pep8:101 -->
- Apply function-style naming to global variables. — [PEP 8: Global Variable Names](https://peps.python.org/pep-0008/#global-variable-names). <!-- pep8:102 -->
- Write function and variable names as lowercase words joined by underscores. — [PEP 8: Function and Variable Names](https://peps.python.org/pep-0008/#function-and-variable-names). <!-- pep8:104 -->
- Keep mixedCase naming only where it preserves an existing interface's convention. — [PEP 8: Function and Variable Names](https://peps.python.org/pep-0008/#function-and-variable-names). <!-- pep8:105 -->
- Use `self` for the first parameter of an instance method. — [PEP 8: Function and Method Arguments](https://peps.python.org/pep-0008/#function-and-method-arguments). <!-- pep8:106 -->
- Use `cls` for the first parameter of a class method. — [PEP 8: Function and Method Arguments](https://peps.python.org/pep-0008/#function-and-method-arguments). <!-- pep8:107 -->
- Resolve a keyword collision with a trailing underscore or a suitable synonym instead of an obscure abbreviation. — [PEP 8: Function and Method Arguments](https://peps.python.org/pep-0008/#function-and-method-arguments). <!-- pep8:108 -->
- Apply function-style lowercase naming to methods and instance attributes. — [PEP 8: Method Names and Instance Variables](https://peps.python.org/pep-0008/#method-names-and-instance-variables). <!-- pep8:109 -->
- Mark nonpublic methods and attributes with a single initial underscore. — [PEP 8: Method Names and Instance Variables](https://peps.python.org/pep-0008/#method-names-and-instance-variables). <!-- pep8:110 -->
- Use double-leading-underscore mangling principally to avoid subclass name collisions in classes intended for inheritance. — [PEP 8: Method Names and Instance Variables](https://peps.python.org/pep-0008/#method-names-and-instance-variables). <!-- pep8:111 -->
- Normally define constants at module level and name them with uppercase words joined by underscores. — [PEP 8: Constants](https://peps.python.org/pep-0008/#constants). <!-- pep8:112 -->
- Do not prefix a public attribute's name with an underscore. — [PEP 8: Designing for Inheritance](https://peps.python.org/pep-0008/#designing-for-inheritance). <!-- pep8:115 -->
- Continue to prefix internal names with an underscore even when exports are controlled by `__all__`. — [PEP 8: Public and Internal Interfaces](https://peps.python.org/pep-0008/#public-and-internal-interfaces). <!-- pep8:124 -->

## Files and layout

- Use four spaces for each additional block level. — [PEP 8: Indentation](https://peps.python.org/pep-0008/#indentation). <!-- pep8:6 -->
- For continued expressions, align with the opening delimiter or use a clearly identifiable hanging indent. — [PEP 8: Indentation](https://peps.python.org/pep-0008/#indentation). <!-- pep8:7 -->
- With a hanging indent, start the arguments on the line after the opener. — [PEP 8: Indentation](https://peps.python.org/pep-0008/#indentation). <!-- pep8:8 -->
- Indent continuations enough to distinguish them from the following statement body. — [PEP 8: Indentation](https://peps.python.org/pep-0008/#indentation). <!-- pep8:9 -->
- Choose continuation indentation for clarity; it may differ from four spaces. — [PEP 8: Indentation](https://peps.python.org/pep-0008/#indentation). <!-- pep8:10 -->
- Align a multiline closing delimiter either with the items above it or with the start of its opening statement. — [PEP 8: Indentation](https://peps.python.org/pep-0008/#indentation). <!-- pep8:11 -->
- Choose a locally readable way to distinguish a wrapped `if` condition from its body; PEP 8 prescribes no single method. — [PEP 8: Indentation](https://peps.python.org/pep-0008/#indentation). <!-- pep8:12 -->
- Choose spaces as the normal indentation character. — [PEP 8: Tabs or Spaces?](https://peps.python.org/pep-0008/#tabs-or-spaces). <!-- pep8:13 -->
- Retain tabs only when matching existing code that already uses them for indentation. — [PEP 8: Tabs or Spaces?](https://peps.python.org/pep-0008/#tabs-or-spaces). <!-- pep8:14 -->
- Keep indentation free of mixed spaces and tabs. — [PEP 8: Tabs or Spaces?](https://peps.python.org/pep-0008/#tabs-or-spaces). <!-- pep8:15 -->
- Keep ordinary code lines within 79 characters. — [PEP 8: Maximum Line Length](https://peps.python.org/pep-0008/#maximum-line-length). <!-- pep8:16 -->
- A team agreement may raise the code limit to 99 characters while keeping prose at 72. — [PEP 8: Maximum Line Length](https://peps.python.org/pep-0008/#maximum-line-length). <!-- pep8:18 -->
- Wrap expressions within paired delimiters instead of using explicit continuation backslashes where possible. — [PEP 8: Maximum Line Length](https://peps.python.org/pep-0008/#maximum-line-length). <!-- pep8:20 -->
- Allow a continuation backslash when implicit joining is unavailable, including relevant older-runtime syntax for multiple context managers. — [PEP 8: Maximum Line Length](https://peps.python.org/pep-0008/#maximum-line-length). <!-- pep8:21 -->
- Make continuation lines recognizable through their indentation. — [PEP 8: Maximum Line Length](https://peps.python.org/pep-0008/#maximum-line-length). <!-- pep8:22 -->
- Breaking before or after a binary operator is acceptable when the surrounding code does so consistently. — [PEP 8: Should a Line Break Before or After a Binary Operator?](https://peps.python.org/pep-0008/#should-a-line-break-before-or-after-a-binary-operator). <!-- pep8:23 -->
- For new code, favor breaks that put binary operators before their operands on the next line. — [PEP 8: Should a Line Break Before or After a Binary Operator?](https://peps.python.org/pep-0008/#should-a-line-break-before-or-after-a-binary-operator). <!-- pep8:24 -->
- Leave two empty lines between module-level function or class definitions. — [PEP 8: Blank Lines](https://peps.python.org/pep-0008/#blank-lines). <!-- pep8:25 -->
- Leave one empty line between methods of a class. — [PEP 8: Blank Lines](https://peps.python.org/pep-0008/#blank-lines). <!-- pep8:26 -->
- Add blank lines sparingly to mark related groups of functions or distinct steps within a function. — [PEP 8: Blank Lines](https://peps.python.org/pep-0008/#blank-lines). <!-- pep8:27 -->
- Closely related one-line definitions may appear without separating blank lines. — [PEP 8: Blank Lines](https://peps.python.org/pep-0008/#blank-lines). <!-- pep8:28 -->
- Use a form-feed to mark a conceptual page only with awareness that some viewers display it poorly. — [PEP 8: Blank Lines](https://peps.python.org/pep-0008/#blank-lines). <!-- pep8:29 -->
- Limit non-ASCII literal data to cases that help readability; avoid distracting Unicode and byte-order marks. — [PEP 8: Source File Encoding](https://peps.python.org/pep-0008/#source-file-encoding). <!-- pep8:32 -->
- Give separate module imports separate lines in the usual case. — [PEP 8: Imports](https://peps.python.org/pep-0008/#imports). <!-- pep8:35 -->
- Names imported from a single module may be combined in one `from` statement. — [PEP 8: Imports](https://peps.python.org/pep-0008/#imports). <!-- pep8:36 -->
- Keep imports at the beginning of the module, following its documentation and preceding global declarations. — [PEP 8: Imports](https://peps.python.org/pep-0008/#imports). <!-- pep8:37 -->
- Arrange import groups in this order: standard library, external packages, then the project's own modules. — [PEP 8: Imports](https://peps.python.org/pep-0008/#imports). <!-- pep8:38 -->
- Leave an empty line between import groups. — [PEP 8: Imports](https://peps.python.org/pep-0008/#imports). <!-- pep8:39 -->
- Choose absolute import paths by default. — [PEP 8: Imports](https://peps.python.org/pep-0008/#imports). <!-- pep8:40 -->
- An explicit relative import is also reasonable within a complicated package hierarchy. — [PEP 8: Imports](https://peps.python.org/pep-0008/#imports). <!-- pep8:41 -->
- A class may ordinarily be imported by name from its defining module. — [PEP 8: Imports](https://peps.python.org/pep-0008/#imports). <!-- pep8:43 -->
- When imported class names collide, qualify their use with the module name. — [PEP 8: Imports](https://peps.python.org/pep-0008/#imports). <!-- pep8:44 -->
- Keep wildcard imports out of ordinary code; reserve them for justified republication of an existing public API. — [PEP 8: Imports](https://peps.python.org/pep-0008/#imports). <!-- pep8:45 -->
- Put module-level dunder metadata after the docstring and any future imports, but ahead of other imports. — [PEP 8: Module Level Dunder Names](https://peps.python.org/pep-0008/#module-level-dunder-names). <!-- pep8:46 -->
- Use a consistent choice of single or double string quotes; PEP 8 gives neither general priority. — [PEP 8: String Quotes](https://peps.python.org/pep-0008/#string-quotes). <!-- pep8:47 -->
- Change the outer quote character when doing so avoids escaping an embedded quote. — [PEP 8: String Quotes](https://peps.python.org/pep-0008/#string-quotes). <!-- pep8:48 -->
- Choose double-quote delimiters for triple-quoted strings. — [PEP 8: String Quotes](https://peps.python.org/pep-0008/#string-quotes). <!-- pep8:49 -->
- Keep the immediate interiors of parentheses, brackets, and braces unpadded. — [PEP 8: Pet Peeves](https://peps.python.org/pep-0008/#pet-peeves). <!-- pep8:50 -->
- When a trailing comma directly precedes a closing delimiter, leave no space between them. — [PEP 8: Pet Peeves](https://peps.python.org/pep-0008/#pet-peeves). <!-- pep8:51 -->
- Attach commas, semicolons, and nonslice colons to the text before them. — [PEP 8: Pet Peeves](https://peps.python.org/pep-0008/#pet-peeves). <!-- pep8:52 -->
- Treat slice colons symmetrically, giving both sides equal spacing when their operands need it. — [PEP 8: Pet Peeves](https://peps.python.org/pep-0008/#pet-peeves). <!-- pep8:53 -->
- Leave out the space adjacent to an absent slice bound or step. — [PEP 8: Pet Peeves](https://peps.python.org/pep-0008/#pet-peeves). <!-- pep8:54 -->
- Attach call parentheses and indexing or slicing brackets directly to the preceding expression. — [PEP 8: Pet Peeves](https://peps.python.org/pep-0008/#pet-peeves). <!-- pep8:55 -->
- Do not insert extra spaces around assignments merely to align nearby statements. — [PEP 8: Pet Peeves](https://peps.python.org/pep-0008/#pet-peeves). <!-- pep8:56 -->
- Strip whitespace from the ends of lines. — [PEP 8: Other Recommendations](https://peps.python.org/pep-0008/#other-recommendations). <!-- pep8:57 -->
- Surround assignment, comparison, and Boolean operators with one space on each side. — [PEP 8: Other Recommendations](https://peps.python.org/pep-0008/#other-recommendations). <!-- pep8:58 -->
- Optionally emphasize precedence by tightening spacing around higher-priority arithmetic while spacing lower-priority operators. — [PEP 8: Other Recommendations](https://peps.python.org/pep-0008/#other-recommendations). <!-- pep8:59 -->
- Use equal spacing on both sides of a binary operator, with no more than one space per side. — [PEP 8: Other Recommendations](https://peps.python.org/pep-0008/#other-recommendations). <!-- pep8:60 -->
- Apply normal colon spacing to annotations and place a space on each side of a return annotation's arrow. — [PEP 8: Other Recommendations](https://peps.python.org/pep-0008/#other-recommendations). <!-- pep8:61 -->
- Keep the equals sign unpadded in keyword arguments and unannotated parameter defaults. — [PEP 8: Other Recommendations](https://peps.python.org/pep-0008/#other-recommendations). <!-- pep8:62 -->
- Pad the equals sign with one space per side when the defaulted parameter has a type annotation. — [PEP 8: Other Recommendations](https://peps.python.org/pep-0008/#other-recommendations). <!-- pep8:63 -->
- Prefer a separate line for each statement. — [PEP 8: Other Recommendations](https://peps.python.org/pep-0008/#other-recommendations). <!-- pep8:64 -->
- Expand control statements with multiple clauses over multiple lines. — [PEP 8: Other Recommendations](https://peps.python.org/pep-0008/#other-recommendations). <!-- pep8:65 -->
- Do not wrap a compound statement merely to squeeze several statements into its continued line. — [PEP 8: Other Recommendations](https://peps.python.org/pep-0008/#other-recommendations). <!-- pep8:66 -->
- For multiline sequences likely to grow, consider putting each item on its own line with a trailing comma and a separate closing line. — [PEP 8: When to Use Trailing Commas](https://peps.python.org/pep-0008/#when-to-use-trailing-commas). <!-- pep8:68 -->
- Omit an unnecessary comma immediately before a same-line closer, except when it defines a singleton tuple. — [PEP 8: When to Use Trailing Commas](https://peps.python.org/pep-0008/#when-to-use-trailing-commas). <!-- pep8:69 -->
- Use `__all__` to declare wildcard exports, or hide internal globals behind a leading underscore. — [PEP 8: Global Variable Names](https://peps.python.org/pep-0008/#global-variable-names). <!-- pep8:103 -->
- Make it clear which parts of an API are public and which are internal. — [PEP 8: Public and Internal Interfaces](https://peps.python.org/pep-0008/#public-and-internal-interfaces). <!-- pep8:121 -->
- Consider documented interfaces public unless their documentation explicitly marks them internal or provisional. — [PEP 8: Public and Internal Interfaces](https://peps.python.org/pep-0008/#public-and-internal-interfaces). <!-- pep8:122 -->
- Declare the public API in `__all__`, using an empty sequence when the module exposes none. — [PEP 8: Public and Internal Interfaces](https://peps.python.org/pep-0008/#public-and-internal-interfaces). <!-- pep8:123 -->
- An interface remains internal if any containing namespace is internal. — [PEP 8: Public and Internal Interfaces](https://peps.python.org/pep-0008/#public-and-internal-interfaces). <!-- pep8:125 -->
- Rely on imported objects exposed by another module only when that module documents them as re-exports. — [PEP 8: Public and Internal Interfaces](https://peps.python.org/pep-0008/#public-and-internal-interfaces). <!-- pep8:126 -->
- In variable annotations, put one space after the colon and none before it. — [PEP 8: Variable Annotations](https://peps.python.org/pep-0008/#variable-annotations). <!-- pep8:156 -->
- Place one space on either side of the equals sign in an annotated assignment. — [PEP 8: Variable Annotations](https://peps.python.org/pep-0008/#variable-annotations). <!-- pep8:157 -->

## Types and data

- Include the required comma in a singleton tuple and normally write its parentheses as well. — [PEP 8: When to Use Trailing Commas](https://peps.python.org/pep-0008/#when-to-use-trailing-commas). <!-- pep8:67 -->
- Distinguish explicitly between public attributes, the subclass contract, and base-class internals. — [PEP 8: Designing for Inheritance](https://peps.python.org/pep-0008/#designing-for-inheritance). <!-- pep8:113 -->
- When an attribute's intended visibility is uncertain, start with a nonpublic interface. — [PEP 8: Designing for Inheritance](https://peps.python.org/pep-0008/#designing-for-inheritance). <!-- pep8:114 -->
- Expose uncomplicated public data as attributes instead of adding unnecessary getter and setter methods. — [PEP 8: Designing for Inheritance](https://peps.python.org/pep-0008/#designing-for-inheritance). <!-- pep8:116 -->
- Introduce a property when an attribute needs behavior while its existing access syntax must remain usable. — [PEP 8: Designing for Inheritance](https://peps.python.org/pep-0008/#designing-for-inheritance). <!-- pep8:117 -->
- Make property access inexpensive and generally avoid side effects beyond incidental work such as caching. — [PEP 8: Designing for Inheritance](https://peps.python.org/pep-0008/#designing-for-inheritance). <!-- pep8:118 -->
- Test singleton objects, including `None`, with identity comparisons. — [PEP 8: Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations). <!-- pep8:129 -->
- Distinguish a missing argument represented by `None` from a supplied value that happens to be falsey. — [PEP 8: Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations). <!-- pep8:130 -->
- Express negative identity directly with `is not`, rather than negating an `is` expression. — [PEP 8: Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations). <!-- pep8:131 -->
- Supply the full rich-comparison interface when implementing ordering; `functools.total_ordering` can fill in the related operations. — [PEP 8: Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations). <!-- pep8:132 -->
- Use `startswith` and `endswith` to recognize string prefixes and suffixes instead of comparing slices. — [PEP 8: Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations). <!-- pep8:145 -->
- Check type membership with `isinstance` rather than exact type-object comparison. — [PEP 8: Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations). <!-- pep8:146 -->
- Use a sequence's truth value to distinguish empty from nonempty. — [PEP 8: Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations). <!-- pep8:147 -->
- Evaluate Boolean values directly rather than comparing them with Boolean constants through equality or identity. — [PEP 8: Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations). <!-- pep8:149 -->
- Write function annotations using PEP 484's typing conventions rather than earlier experimental annotation styles. — [PEP 8: Function Annotations](https://peps.python.org/pep-0008/#function-annotations). <!-- pep8:151 -->
- If function annotations intentionally serve another purpose, mark them with an appropriate directive so a type checker does not misinterpret them. — [PEP 8: Function Annotations](https://peps.python.org/pep-0008/#function-annotations). <!-- pep8:153 -->
- Distribute type information through stubs when it should remain separate from the implementation. — [PEP 8: Function Annotations](https://peps.python.org/pep-0008/#function-annotations). <!-- pep8:155 -->
- Use variable-annotation syntax to express variable types in stub files. — [PEP 8: Variable Annotations](https://peps.python.org/pep-0008/#variable-annotations). <!-- pep8:158 -->

## Errors

- Base ordinary application exceptions on `Exception`, keeping `BaseException` for control-flow exceptions outside normal error handling. — [PEP 8: Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations). <!-- pep8:134 -->
- Organize exception types around the distinctions that error handlers need to recognize. — [PEP 8: Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations). <!-- pep8:135 -->
- When replacing an exception deliberately, retain its cause through explicit `raise ... from ...` chaining. — [PEP 8: Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations). <!-- pep8:136 -->
- If `from None` intentionally hides an exception chain, include the original details needed to understand the replacement error. — [PEP 8: Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations). <!-- pep8:137 -->
- Catch the narrowest suitable exception classes. — [PEP 8: Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations). <!-- pep8:138 -->
- Reserve a bare `except` for traceback reporting or cleanup followed by re-raising; prefer `finally` when it expresses cleanup more clearly. — [PEP 8: Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations). <!-- pep8:139 -->
- Catch the relevant `OSError` subclasses instead of manually branching on error numbers where possible. — [PEP 8: Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations). <!-- pep8:140 -->
- Limit the `try` suite to the operations whose failures the handler is meant to process. — [PEP 8: Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations). <!-- pep8:141 -->
- Manage a resource owned by the current scope with `with`, or use `try/finally` when appropriate. — [PEP 8: Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations). <!-- pep8:142 -->
- Name a context-manager factory explicitly when context entry performs work beyond acquiring and releasing a resource. — [PEP 8: Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations). <!-- pep8:143 -->
- Keep `return`, `break`, and `continue` from exiting a `finally` suite and silently replacing an active exception. — [PEP 8: Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations). <!-- pep8:150 -->

## Comments and docs

- Wrap flowing comment and docstring prose at 72 characters. — [PEP 8: Maximum Line Length](https://peps.python.org/pep-0008/#maximum-line-length). <!-- pep8:17 -->
- Revise associated comments whenever a code change makes them inaccurate. — [PEP 8: Comments](https://peps.python.org/pep-0008/#comments). <!-- pep8:70 -->
- Write clear, complete comment sentences without changing the capitalization of referenced identifiers. — [PEP 8: Comments](https://peps.python.org/pep-0008/#comments). <!-- pep8:71 -->
- Start comments with a capital letter unless their first word is an identifier that begins lowercase. — [PEP 8: Comments](https://peps.python.org/pep-0008/#comments). <!-- pep8:72 -->
- Finish sentences in block comments with a full stop. — [PEP 8: Comments](https://peps.python.org/pep-0008/#comments). <!-- pep8:73 -->
- Separate successive comment sentences with one or two spaces after their periods. — [PEP 8: Comments](https://peps.python.org/pep-0008/#comments). <!-- pep8:74 -->
- Use English for comments unless the code will certainly remain unread by people who do not know the chosen language. — [PEP 8: Comments](https://peps.python.org/pep-0008/#comments). <!-- pep8:75 -->
- Indent a block comment to the same level as the code it explains. — [PEP 8: Block Comments](https://peps.python.org/pep-0008/#block-comments). <!-- pep8:76 -->
- Prefix ordinary block-comment text with a hash and one space. — [PEP 8: Block Comments](https://peps.python.org/pep-0008/#block-comments). <!-- pep8:77 -->
- Divide block-comment paragraphs with a line consisting solely of a hash. — [PEP 8: Block Comments](https://peps.python.org/pep-0008/#block-comments). <!-- pep8:78 -->
- Add inline comments selectively. — [PEP 8: Inline Comments](https://peps.python.org/pep-0008/#inline-comments). <!-- pep8:79 -->
- Leave at least two spaces between a statement and its inline comment. — [PEP 8: Inline Comments](https://peps.python.org/pep-0008/#inline-comments). <!-- pep8:80 -->
- Place one space between an inline comment's hash and its text. — [PEP 8: Inline Comments](https://peps.python.org/pep-0008/#inline-comments). <!-- pep8:81 -->
- Use comments to explain unobvious intent rather than translating straightforward code into prose. — [PEP 8: Inline Comments](https://peps.python.org/pep-0008/#inline-comments). <!-- pep8:82 -->
- Provide docstrings for public modules, classes, functions, and methods. — [PEP 8: Documentation Strings](https://peps.python.org/pep-0008/#documentation-strings). <!-- pep8:83 -->
- For a private method, a comment immediately below its definition can serve instead of a docstring. — [PEP 8: Documentation Strings](https://peps.python.org/pep-0008/#documentation-strings). <!-- pep8:84 -->
- Close a multiline docstring with triple quotes on a line of their own. — [PEP 8: Documentation Strings](https://peps.python.org/pep-0008/#documentation-strings). <!-- pep8:85 -->
- Close a single-line docstring on the line containing its text. — [PEP 8: Documentation Strings](https://peps.python.org/pep-0008/#documentation-strings). <!-- pep8:86 -->

## Performance

- Expose costly calculations through operations rather than properties. — [PEP 8: Designing for Inheritance](https://peps.python.org/pep-0008/#designing-for-inheritance). <!-- pep8:119 -->
- For performance-sensitive string assembly, collect pieces for `join` instead of repeatedly concatenating them. — [PEP 8: Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations). <!-- pep8:128 -->

## Language-specific pitfalls

- Balance name mangling's collision protection against the inconvenience it causes debugging and advanced callers. — [PEP 8: Designing for Inheritance](https://peps.python.org/pep-0008/#designing-for-inheritance). <!-- pep8:120 -->
- Write portable Python rather than depending on optimizations or behavior specific to one implementation. — [PEP 8: Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations). <!-- pep8:127 -->
- Define a named function with `def` instead of binding a lambda to a name. — [PEP 8: Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations). <!-- pep8:133 -->
- Keep return paths consistent: when any path yields a value, use an explicit `None` return on other reachable paths. — [PEP 8: Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations). <!-- pep8:144 -->
- Do not encode essential string content as visually unobtrusive trailing spaces. — [PEP 8: Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations). <!-- pep8:148 -->

## Where the sources disagree

- Give the project's own style guide priority wherever it disagrees with PEP 8. — [PEP 8: Introduction](https://peps.python.org/pep-0008/#introduction). <!-- pep8:1 -->
- Favor consistency first inside the current function or module, then across the project, then with this guide. — [PEP 8: A Foolish Consistency is the Hobgoblin of Little Minds](https://peps.python.org/pep-0008/#a-foolish-consistency-is-the-hobgoblin-of-little-minds). <!-- pep8:2 -->
- Depart from a convention when applying it would make the code harder to read. — [PEP 8: A Foolish Consistency is the Hobgoblin of Little Minds](https://peps.python.org/pep-0008/#a-foolish-consistency-is-the-hobgoblin-of-little-minds). <!-- pep8:3 -->
- Preserve backward compatibility when making stylistic changes. — [PEP 8: A Foolish Consistency is the Hobgoblin of Little Minds](https://peps.python.org/pep-0008/#a-foolish-consistency-is-the-hobgoblin-of-little-minds). <!-- pep8:4 -->
- Allow justified exceptions for surrounding conventions, unchanged legacy code, or older supported interpreters. — [PEP 8: A Foolish Consistency is the Hobgoblin of Little Minds](https://peps.python.org/pep-0008/#a-foolish-consistency-is-the-hobgoblin-of-little-minds). <!-- pep8:5 -->

## Worked examples

Read [original worked examples and their source tags](examples.md) for small applications of this guide.
