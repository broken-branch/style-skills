# Rust Style Guide: condensed rules

Rust 2024 formatting is stable in rustfmt (`style_edition = "2024"`), although the Style Guide editions page still calls it nightly. Rules against breaking inside `()` and `func()` apply to the next style edition. Frontmatter rules apply only to unstable cargo-script frontmatter.

Source owner: The Rust Project Contributors. License: [MIT OR Apache-2.0](../LICENSE). Changes: rules independently restated, shortened and grouped by topic; examples omitted. Unofficial; no endorsement is implied.

## Tooling

- Start from Rust's default formatting, allowing explicit project configuration to override it. — [Rust Style Guide: The default Rust style](https://doc.rust-lang.org/style-guide/index.html#the-default-rust-style). <!-- RSG:001 -->
- Use spaces for indentation; tabs are not the default. — [Rust Style Guide: Indentation and line width](https://doc.rust-lang.org/style-guide/index.html#indentation-and-line-width). <!-- RSG:003 -->
- Indent code by four spaces per nesting level, excluding string and comment contents. — [Rust Style Guide: Indentation and line width](https://doc.rust-lang.org/style-guide/index.html#indentation-and-line-width). <!-- RSG:004 -->
- Limit ordinary source lines to 100 columns. — [Rust Style Guide: Indentation and line width](https://doc.rust-lang.org/style-guide/index.html#indentation-and-line-width). <!-- RSG:005 -->
- Use block indentation for continuations instead of aligning them with a preceding token. — [Rust Style Guide: Block indent](https://doc.rust-lang.org/style-guide/index.html#block-indent). <!-- RSG:006 -->
- Retain a final comma when a list ends on the following line. — [Rust Style Guide: Trailing commas](https://doc.rust-lang.org/style-guide/index.html#trailing-commas). <!-- RSG:007 -->
- Separate adjacent statements or items with no more than one blank line. — [Rust Style Guide: Blank lines](https://doc.rust-lang.org/style-guide/index.html#blank-lines). <!-- RSG:008 -->
- Strip trailing whitespace everywhere, preserving a string's value when adjusting its literal spelling. — [Rust Style Guide: Trailing whitespace](https://doc.rust-lang.org/style-guide/index.html#trailing-whitespace). <!-- RSG:009 -->
- Use version sorting unless a particular rule specifies another ordering. — [Rust Style Guide: Sorting](https://doc.rust-lang.org/style-guide/index.html#sorting). <!-- RSG:010 -->
- Compare ASCII digit sequences numerically and intervening text by Unicode lexical order. — [Rust Style Guide: Sorting](https://doc.rust-lang.org/style-guide/index.html#sorting). <!-- RSG:011 -->
- Defer equal-number leading-zero differences until all other comparisons tie, then put the first differing run with more zeroes first. — [Rust Style Guide: Sorting](https://doc.rust-lang.org/style-guide/index.html#sorting). <!-- RSG:012 -->
- Sort underscores after spaces but before every other character. — [Rust Style Guide: Sorting](https://doc.rust-lang.org/style-guide/index.html#sorting). <!-- RSG:013 -->
- Place non-lowercase characters before lowercase ones unless a more specific sorting rule applies. — [Rust Style Guide: Sorting](https://doc.rust-lang.org/style-guide/index.html#sorting). <!-- RSG:014 -->
- Put each attribute on a separate line aligned with its item. — [Rust Style Guide: Attributes](https://doc.rust-lang.org/style-guide/index.html#attributes). <!-- RSG:026 -->
- Indent inner attributes with the enclosing contents, using outer attributes where possible. — [Rust Style Guide: Attributes](https://doc.rust-lang.org/style-guide/index.html#attributes). <!-- RSG:027 -->
- Lay out attribute parameters using the function-argument conventions. — [Rust Style Guide: Attributes](https://doc.rust-lang.org/style-guide/index.html#attributes). <!-- RSG:028 -->
- Separate attribute assignments from their equals sign by one space on either side. — [Rust Style Guide: Attributes](https://doc.rust-lang.org/style-guide/index.html#attributes). <!-- RSG:029 -->
- Combine derive entries into one attribute without rearranging them. — [Rust Style Guide: Attributes](https://doc.rust-lang.org/style-guide/index.html#attributes). <!-- RSG:030 -->
- Let the formatter decide context-dependent thresholds for constructs described as small. — [Rust Style Guide: small items](https://doc.rust-lang.org/style-guide/index.html#small-items). <!-- RSG:031 -->
- Use the same item layout in nested scopes as at module scope. — [Rust Style Guide: Items](https://doc.rust-lang.org/style-guide/items.html). <!-- RSG:032 -->
- Keep `fn` beside the function's name so the declaration remains easy to search. — [Rust Style Guide: Function definitions](https://doc.rust-lang.org/style-guide/items.html#function-definitions). <!-- RSG:037 -->
- Order a function declaration's parts as visibility, safety, external ABI, `fn`, name and parameters, return type, and body. — [Rust Style Guide: Function definitions](https://doc.rust-lang.org/style-guide/items.html#function-definitions). <!-- RSG:038 -->
- When parameters wrap, break inside both parentheses and give each parameter an indented, comma-terminated line. — [Rust Style Guide: Function definitions](https://doc.rust-lang.org/style-guide/items.html#function-definitions). <!-- RSG:040 -->
- Lay out tuple types as parameter lists and tuple values as calls. — [Rust Style Guide: Tuples and tuple structs](https://doc.rust-lang.org/style-guide/items.html#tuples-and-tuple-structs). <!-- RSG:041 -->
- Put enum variants on separate lines one indentation level inside the enum. — [Rust Style Guide: Enums](https://doc.rust-lang.org/style-guide/items.html#enums). <!-- RSG:042 -->
- Format each variant according to whether it has named fields, positional fields, or no fields. — [Rust Style Guide: Enums](https://doc.rust-lang.org/style-guide/items.html#enums). <!-- RSG:043 -->
- A compact named-field variant may use one line with padded braces and no comma after its last field. — [Rust Style Guide: Enums](https://doc.rust-lang.org/style-guide/items.html#enums). <!-- RSG:044 -->
- If any named-field variant wraps, wrap the others too and consider moving their fields into dedicated structs. — [Rust Style Guide: Enums](https://doc.rust-lang.org/style-guide/items.html#enums). <!-- RSG:045 -->
- Keep the struct keyword and name together, adding the opening brace on that line when it fits. — [Rust Style Guide: Structs and Unions](https://doc.rust-lang.org/style-guide/items.html#structs-and-unions). <!-- RSG:046 -->
- Give struct fields one indentation level and trailing commas, aligning the closing brace with the declaration. — [Rust Style Guide: Structs and Unions](https://doc.rust-lang.org/style-guide/items.html#structs-and-unions). <!-- RSG:047 -->
- Break a field type onto a further-indented line only if the name and type cannot fit together. — [Rust Style Guide: Structs and Unions](https://doc.rust-lang.org/style-guide/items.html#structs-and-unions). <!-- RSG:048 -->
- Keep required empty braced or tuple struct delimiters adjacent. — [Rust Style Guide: Structs and Unions](https://doc.rust-lang.org/style-guide/items.html#structs-and-unions). <!-- RSG:050 -->
- Format union declarations with the struct layout rules. — [Rust Style Guide: Structs and Unions](https://doc.rust-lang.org/style-guide/items.html#structs-and-unions). <!-- RSG:051 -->
- Prefer a single-line tuple struct with comma-space field separators and no trailing comma. — [Rust Style Guide: Tuple structs](https://doc.rust-lang.org/style-guide/items.html#tuple-structs). <!-- RSG:052 -->
- Do not pad tuple-struct parentheses or separate their closer from the semicolon. — [Rust Style Guide: Tuple structs](https://doc.rust-lang.org/style-guide/items.html#tuple-structs). <!-- RSG:053 -->
- In a wrapped tuple struct, place each field on its own indented line with a comma. — [Rust Style Guide: Tuple structs](https://doc.rust-lang.org/style-guide/items.html#tuple-structs). <!-- RSG:055 -->
- Indent trait members once; keep an empty trait declaration on one line. — [Rust Style Guide: Traits](https://doc.rust-lang.org/style-guide/items.html#traits). <!-- RSG:056 -->
- Break after a nonempty trait's opening brace and before its closing brace. — [Rust Style Guide: Traits](https://doc.rust-lang.org/style-guide/items.html#traits). <!-- RSG:057 -->
- Add a space after a bound's colon and on both sides of each `+`. — [Rust Style Guide: Traits](https://doc.rust-lang.org/style-guide/items.html#traits). <!-- RSG:058 -->
- Prefer inline bounds or a `where` clause; otherwise break before each `+`, indent bounds, and place the brace separately. — [Rust Style Guide: Traits](https://doc.rust-lang.org/style-guide/items.html#traits). <!-- RSG:059 -->
- Indent `impl` members once and keep an empty implementation on one line. — [Rust Style Guide: Impls](https://doc.rust-lang.org/style-guide/items.html#impls). <!-- RSG:060 -->
- Keep an implementation header intact if possible; otherwise break before `for`, indent its type, and put the brace on its own line. — [Rust Style Guide: Impls](https://doc.rust-lang.org/style-guide/items.html#impls). <!-- RSG:061 -->
- Separate `extern crate` words normally and attach the terminating semicolon. — [Rust Style Guide: Extern crate](https://doc.rust-lang.org/style-guide/items.html#extern-crate). <!-- RSG:062 -->
- Use ordinary spacing between module keywords and names, a space before a body brace, and none before a semicolon. — [Rust Style Guide: Modules](https://doc.rust-lang.org/style-guide/items.html#modules). <!-- RSG:063 -->
- Use braces as the outer delimiter of a `macro_rules` definition. — [Rust Style Guide: macro_rules!](https://doc.rust-lang.org/style-guide/items.html#macro_rules). <!-- RSG:064 -->
- Keep generic parameters inline if possible, first wrapping other syntax or relocating bounds into `where`. — [Rust Style Guide: Generics](https://doc.rust-lang.org/style-guide/items.html#generics). <!-- RSG:065 -->
- Leave angle-bracket interiors unpadded; follow a closing bracket with a space only before a word or opening brace. — [Rust Style Guide: Generics](https://doc.rust-lang.org/style-guide/items.html#generics). <!-- RSG:066 -->
- Separate inline generic parameters with comma-space and omit a final comma. — [Rust Style Guide: Generics](https://doc.rust-lang.org/style-guide/items.html#generics). <!-- RSG:067 -->
- Wrap generic parameters inside the angle brackets, with one indented, comma-terminated parameter per line. — [Rust Style Guide: Generics](https://doc.rust-lang.org/style-guide/items.html#generics). <!-- RSG:068 -->
- Put spaces around associated-type assignment operators inside generic arguments. — [Rust Style Guide: Generics](https://doc.rust-lang.org/style-guide/items.html#generics). <!-- RSG:069 -->
- Attach `where` to a directly preceding closing delimiter; otherwise start it on a new line aligned with the declaration. — [Rust Style Guide: where clauses](https://doc.rust-lang.org/style-guide/items.html#where-clauses). <!-- RSG:071 -->
- Put each `where` predicate on an indented line with a comma, except where a semicolon ends the clause. — [Rust Style Guide: where clauses](https://doc.rust-lang.org/style-guide/items.html#where-clauses). <!-- RSG:072 -->
- After a `where` clause, begin the body or assignment on another line. — [Rust Style Guide: where clauses](https://doc.rust-lang.org/style-guide/items.html#where-clauses). <!-- RSG:073 -->
- Replace a tiny `where` clause with an inline parameter bound. — [Rust Style Guide: where clauses](https://doc.rust-lang.org/style-guide/items.html#where-clauses). <!-- RSG:074 -->
- When predicate bounds wrap, indent their continuations and start each with `+`. — [Rust Style Guide: where clauses](https://doc.rust-lang.org/style-guide/items.html#where-clauses). <!-- RSG:075 -->
- Keep a type alias inline when it fits; otherwise break before `=` and indent the assigned type. — [Rust Style Guide: Type aliases](https://doc.rust-lang.org/style-guide/items.html#type-aliases). <!-- RSG:076 -->
- For an alias with only a trailing `where`, indent the equals-and-type continuation and start `where` on the next line. — [Rust Style Guide: Type aliases](https://doc.rust-lang.org/style-guide/items.html#type-aliases). <!-- RSG:077 -->
- After a leading alias `where` clause, align `=` with the declaration; apply ordinary layout to any trailing clause. — [Rust Style Guide: Type aliases](https://doc.rust-lang.org/style-guide/items.html#type-aliases). <!-- RSG:078 -->
- Use alias layout for associated types and separate a bounds colon from its following bound. — [Rust Style Guide: Associated types](https://doc.rust-lang.org/style-guide/items.html#associated-types). <!-- RSG:079 -->
- For a wrapped import list, break inside its braces and indent comma-terminated entries. — [Rust Style Guide: Large list imports](https://doc.rust-lang.org/style-guide/items.html#large-list-imports). <!-- RSG:083 -->
- In a `let`, space after the type colon and around `=`, attaching the final semicolon. — [Rust Style Guide: Let statements](https://doc.rust-lang.org/style-guide/statements.html#let-statements). <!-- RSG:094 -->
- Keep declarations inline first, then try an indented break after `=`, and only then a break after the colon. — [Rust Style Guide: Let statements](https://doc.rust-lang.org/style-guide/statements.html#let-statements). <!-- RSG:095 -->
- Keep the beginning of a wrapped type after its colon when expression-combination rules allow it. — [Rust Style Guide: Let statements](https://doc.rust-lang.org/style-guide/statements.html#let-statements). <!-- RSG:096 -->
- Start a wrapped initializer beside `=` without extra indentation when it fits; otherwise indent the entire initializer. — [Rust Style Guide: Let statements](https://doc.rust-lang.org/style-guide/statements.html#let-statements). <!-- RSG:097 -->
- After a wrapped pattern or type, put a block initializer's opening brace on its own line at the declaration's indentation. — [Rust Style Guide: Let statements](https://doc.rust-lang.org/style-guide/statements.html#let-statements). <!-- RSG:098 -->
- Format the declaration before `else` using normal `let` conventions. — [Rust Style Guide: else blocks (let-else statements)](https://doc.rust-lang.org/style-guide/statements.html#else-blocks-let-else-statements). <!-- RSG:099 -->
- Keep `let-else` inline only when short, with a one-line declaration and exactly one uncommented expression in `else`. — [Rust Style Guide: else blocks (let-else statements)](https://doc.rust-lang.org/style-guide/statements.html#else-blocks-let-else-statements). <!-- RSG:100 -->
- In wrapped `let-else`, keep `else` beside its opening brace and put the closer on another line. — [Rust Style Guide: else blocks (let-else statements)](https://doc.rust-lang.org/style-guide/statements.html#else-blocks-let-else-statements). <!-- RSG:101 -->
- Append `else {` to a fitting one-line declaration, indent the body, and align its closer with `let`. — [Rust Style Guide: else blocks (let-else statements)](https://doc.rust-lang.org/style-guide/statements.html#else-blocks-let-else-statements). <!-- RSG:102 -->
- Start `else` on another line when appending it would exceed the width. — [Rust Style Guide: else blocks (let-else statements)](https://doc.rust-lang.org/style-guide/statements.html#else-blocks-let-else-statements). <!-- RSG:103 -->
- After a wrapped initializer, append `else` only to a delimiter-only line aligned with `let`; otherwise start it on a new aligned line. — [Rust Style Guide: else blocks (let-else statements)](https://doc.rust-lang.org/style-guide/statements.html#else-blocks-let-else-statements). <!-- RSG:104 -->
- Use parentheses or brackets for statement macros, joining the name, `!`, and opener and adding a final semicolon. — [Rust Style Guide: Macros in statement position](https://doc.rust-lang.org/style-guide/statements.html#macros-in-statement-position). <!-- RSG:105 -->
- Join an expression directly to its terminating semicolon. — [Rust Style Guide: Expressions in statement position](https://doc.rust-lang.org/style-guide/statements.html#expressions-in-statement-position). <!-- RSG:106 -->
- End expression statements with semicolons, except expressions ending in a block or supplying the enclosing block's result. — [Rust Style Guide: Expressions in statement position](https://doc.rust-lang.org/style-guide/statements.html#expressions-in-statement-position). <!-- RSG:107 -->
- Explicitly terminate unit-valued expressions instead of implicitly returning their unit result. — [Rust Style Guide: Expressions in statement position](https://doc.rust-lang.org/style-guide/statements.html#expressions-in-statement-position). <!-- RSG:108 -->
- Break inside block braces unless a specific single-line exception applies. — [Rust Style Guide: Blocks](https://doc.rust-lang.org/style-guide/expressions.html#blocks). <!-- RSG:109 -->
- Keep a block's preceding keyword and opening brace together with one space, then indent its contents. — [Rust Style Guide: Blocks](https://doc.rust-lang.org/style-guide/expressions.html#blocks). <!-- RSG:110 -->
- Place a block attribute on a separate line above the block. — [Rust Style Guide: Blocks](https://doc.rust-lang.org/style-guide/expressions.html#blocks). <!-- RSG:111 -->
- Render an empty block as adjacent braces. — [Rust Style Guide: Blocks](https://doc.rust-lang.org/style-guide/expressions.html#blocks). <!-- RSG:113 -->
- Allow a padded one-line block only for one uncommented expression with no statements, in expression position or an unsafe statement block. — [Rust Style Guide: Blocks](https://doc.rust-lang.org/style-guide/expressions.html#blocks). <!-- RSG:114 -->
- Do not pad before a closure's first pipe except after a keyword, and add one space after its final pipe. — [Rust Style Guide: Closures](https://doc.rust-lang.org/style-guide/expressions.html#closures). <!-- RSG:115 -->
- Use function-parameter layout for closures, leaving inferred types unwritten. — [Rust Style Guide: Closures](https://doc.rust-lang.org/style-guide/expressions.html#closures). <!-- RSG:116 -->
- Leave closure bodies unbraced where the syntax permits. — [Rust Style Guide: Closures](https://doc.rust-lang.org/style-guide/expressions.html#closures). <!-- RSG:117 -->
- Brace a closure body when it has a return annotation, statements, comments, or wrapped control flow. — [Rust Style Guide: Closures](https://doc.rust-lang.org/style-guide/expressions.html#closures). <!-- RSG:118 -->
- Keep small struct literals inline with spaces inside braces and no final field comma. — [Rust Style Guide: Struct literals](https://doc.rust-lang.org/style-guide/expressions.html#struct-literals). <!-- RSG:119 -->
- For larger struct literals, give every field a separate indented line ending with a comma. — [Rust Style Guide: Struct literals](https://doc.rust-lang.org/style-guide/expressions.html#struct-literals). <!-- RSG:120 -->
- Space after literal field colons and before the opening struct brace. — [Rust Style Guide: Struct literals](https://doc.rust-lang.org/style-guide/expressions.html#struct-literals). <!-- RSG:121 -->
- Lay out a struct-update tail like a field, but attach its `..` to the value and omit the final comma. — [Rust Style Guide: Struct literals](https://doc.rust-lang.org/style-guide/expressions.html#struct-literals). <!-- RSG:122 -->
- Under the documented next-style rule, never split the unit literal's parentheses, even at the width limit. — [Rust Style Guide: Unit literals](https://doc.rust-lang.org/style-guide/expressions.html#unit-literals). <!-- RSG:123 -->
- Prefer inline tuple literals with comma-space separators and unpadded parentheses. — [Rust Style Guide: Tuple literals](https://doc.rust-lang.org/style-guide/expressions.html#tuple-literals). <!-- RSG:124 -->
- Wrap tuple elements onto individual indented lines, retaining a comma after the last one. — [Rust Style Guide: Tuple literals](https://doc.rust-lang.org/style-guide/expressions.html#tuple-literals). <!-- RSG:125 -->
- Join a tuple-struct constructor to its opener and format its contents as a tuple literal. — [Rust Style Guide: Tuple struct literals](https://doc.rust-lang.org/style-guide/expressions.html#tuple-struct-literals). <!-- RSG:126 -->
- Use the corresponding struct-literal layout for enum values and normally qualify variants unless their enum is in the prelude. — [Rust Style Guide: Enum literals](https://doc.rust-lang.org/style-guide/expressions.html#enum-literals). <!-- RSG:127 -->
- Keep small arrays inline with comma-space separators and no bracket padding. — [Rust Style Guide: Array literals](https://doc.rust-lang.org/style-guide/expressions.html#array-literals). <!-- RSG:128 -->
- In an array repetition, put a space after its semicolon but not before it. — [Rust Style Guide: Array literals](https://doc.rust-lang.org/style-guide/expressions.html#array-literals). <!-- RSG:129 -->
- Use square brackets and array layout for `vec!` and other array-shaped macros. — [Rust Style Guide: Array literals](https://doc.rust-lang.org/style-guide/expressions.html#array-literals). <!-- RSG:130 -->
- Wrap an array repetition immediately after its semicolon. — [Rust Style Guide: Array literals](https://doc.rust-lang.org/style-guide/expressions.html#array-literals). <!-- RSG:131 -->
- Format other wrapped arrays like calls, breaking inside brackets with block-indented elements. — [Rust Style Guide: Array literals](https://doc.rust-lang.org/style-guide/expressions.html#array-literals). <!-- RSG:132 -->
- Attach indexing brackets directly to the indexed expression without a break before the opener. — [Rust Style Guide: Array accesses, indexing, and slicing](https://doc.rust-lang.org/style-guide/expressions.html#array-accesses-indexing-and-slicing). <!-- RSG:133 -->
- If an index must wrap, break inside its brackets and indent the index expression. — [Rust Style Guide: Array accesses, indexing, and slicing](https://doc.rust-lang.org/style-guide/expressions.html#array-accesses-indexing-and-slicing). <!-- RSG:134 -->
- Attach unary operators to operands, apart from the space required after `mut` in a mutable borrow. — [Rust Style Guide: Unary operations](https://doc.rust-lang.org/style-guide/expressions.html#unary-operations). <!-- RSG:135 -->
- Keep unary operators on the same line as their operands. — [Rust Style Guide: Unary operations](https://doc.rust-lang.org/style-guide/expressions.html#unary-operations). <!-- RSG:136 -->
- Separate binary and assignment operators from both operands with spaces. — [Rust Style Guide: Binary operations](https://doc.rust-lang.org/style-guide/expressions.html#binary-operations). <!-- RSG:137 -->
- Preserve parentheses that aid reading; formatters should neither insert nor remove them automatically. — [Rust Style Guide: Binary operations](https://doc.rust-lang.org/style-guide/expressions.html#binary-operations). <!-- RSG:139 -->
- Do not vary operator spacing to suggest precedence. — [Rust Style Guide: Binary operations](https://doc.rust-lang.org/style-guide/expressions.html#binary-operations). <!-- RSG:140 -->
- Wrap after assignment operators but before other binary operators, indenting continuation expressions. — [Rust Style Guide: Binary operations](https://doc.rust-lang.org/style-guide/expressions.html#binary-operations). <!-- RSG:141 -->
- Choose an assignment break before splitting another binary operation. — [Rust Style Guide: Binary operations](https://doc.rust-lang.org/style-guide/expressions.html#binary-operations). <!-- RSG:142 -->
- Space casts as binary operations; when wrapping, begin an indented continuation with `as` and its target type. — [Rust Style Guide: Casts (as)](https://doc.rust-lang.org/style-guide/expressions.html#casts-as). <!-- RSG:143 -->
- Keep a cast chain on one continuation when possible; otherwise break before every `as`. — [Rust Style Guide: Casts (as)](https://doc.rust-lang.org/style-guide/expressions.html#casts-as). <!-- RSG:144 -->
- Omit redundant parentheses enclosing an entire `if` or `while` condition. — [Rust Style Guide: Control flow](https://doc.rust-lang.org/style-guide/expressions.html#control-flow). <!-- RSG:145 -->
- Retain grouping parentheses that make logical or arithmetic relationships clearer. — [Rust Style Guide: Control flow](https://doc.rust-lang.org/style-guide/expressions.html#control-flow). <!-- RSG:146 -->
- Attach a call's opening parenthesis to its callee and each comma to the preceding argument, followed by one space. — [Rust Style Guide: Function calls](https://doc.rust-lang.org/style-guide/expressions.html#function-calls). <!-- RSG:147 -->
- Avoid wrapping the expression that identifies the callee. — [Rust Style Guide: Function calls](https://doc.rust-lang.org/style-guide/expressions.html#function-calls). <!-- RSG:148 -->
- Under the documented next-style rule, keep a zero-argument call's parentheses adjacent even past the width limit. — [Rust Style Guide: Function calls](https://doc.rust-lang.org/style-guide/expressions.html#function-calls). <!-- RSG:149 -->
- Use unpadded parentheses and no trailing comma for an inline call. — [Rust Style Guide: Single-line calls](https://doc.rust-lang.org/style-guide/expressions.html#single-line-calls). <!-- RSG:150 -->
- Wrap a call if it is large, too wide, or already contains a wrapped argument or callee. — [Rust Style Guide: Multi-line calls](https://doc.rust-lang.org/style-guide/expressions.html#multi-line-calls). <!-- RSG:151 -->
- For a wrapped call, break inside its parentheses and put each argument on an indented line with a final comma. — [Rust Style Guide: Multi-line calls](https://doc.rust-lang.org/style-guide/expressions.html#multi-line-calls). <!-- RSG:152 -->
- Apply function-call layout to method calls, leaving the joining dot unspaced. — [Rust Style Guide: Method calls](https://doc.rust-lang.org/style-guide/expressions.html#method-calls). <!-- RSG:153 -->
- Format recognizable Rust syntax inside a macro as the equivalent Rust construct. — [Rust Style Guide: Macro uses](https://doc.rust-lang.org/style-guide/expressions.html#macro-uses). <!-- RSG:154 -->
- Do not extend special standard-macro formatting conventions to unrelated third-party macros. — [Rust Style Guide: Macro uses](https://doc.rust-lang.org/style-guide/expressions.html#macro-uses). <!-- RSG:155 -->
- For small format-macro arguments, pack fitting groups on either side of a separately lined format string. — [Rust Style Guide: Format string macros](https://doc.rust-lang.org/style-guide/expressions.html#format-string-macros). <!-- RSG:156 -->
- Otherwise wrap format-macro arguments individually using call layout. — [Rust Style Guide: Format string macros](https://doc.rust-lang.org/style-guide/expressions.html#format-string-macros). <!-- RSG:157 -->
- Keep a short field or method chain inline if it fits. — [Rust Style Guide: Chains of fields and method calls](https://doc.rust-lang.org/style-guide/expressions.html#chains-of-fields-and-method-calls). <!-- RSG:158 -->
- In wrapped chains, break before dots and after `?`, with accesses and calls block-indented. — [Rust Style Guide: Chains of fields and method calls](https://doc.rust-lang.org/style-guide/expressions.html#chains-of-fields-and-method-calls). <!-- RSG:159 -->
- Join successive chain elements recursively when the first ends no wider than the next indentation and the joined line fits. — [Rust Style Guide: Chains of fields and method calls](https://doc.rust-lang.org/style-guide/expressions.html#chains-of-fields-and-method-calls). <!-- RSG:160 -->
- Once a chain element wraps internally, put it and every following element on separate lines. — [Rust Style Guide: Multi-line elements](https://doc.rust-lang.org/style-guide/expressions.html#multi-line-elements). <!-- RSG:161 -->
- Prefer spreading a chain of intact elements over needlessly wrapping an individual element. — [Rust Style Guide: Multi-line elements](https://doc.rust-lang.org/style-guide/expressions.html#multi-line-elements). <!-- RSG:162 -->
- Keep a control-flow keyword, condition, and opening brace together when width permits. — [Rust Style Guide: Control flow expressions](https://doc.rust-lang.org/style-guide/expressions.html#control-flow-expressions). <!-- RSG:163 -->
- Keep a closing brace, `else`, its optional condition, and the following brace together with normal spaces. — [Rust Style Guide: Control flow expressions](https://doc.rust-lang.org/style-guide/expressions.html#control-flow-expressions). <!-- RSG:164 -->
- In overlong control headers, prefer a break after a let-condition's `=` or before a loop's `in`. — [Rust Style Guide: Control flow expressions](https://doc.rust-lang.org/style-guide/expressions.html#control-flow-expressions). <!-- RSG:165 -->
- After a broken control header, place its opening brace on a separate line aligned with the expression. — [Rust Style Guide: Control flow expressions](https://doc.rust-lang.org/style-guide/expressions.html#control-flow-expressions). <!-- RSG:166 -->
- Allow an inline let-chain header only for two clauses: a literal or identifier with optional unary prefixes, then an inline let-clause. — [Rust Style Guide: Control flow expressions](https://doc.rust-lang.org/style-guide/expressions.html#control-flow-expressions). <!-- RSG:167 -->
- Keep the brace after a wrapped condition's final line if that line contains only closers and is no deeper than the control keyword. — [Rust Style Guide: Control flow expressions](https://doc.rust-lang.org/style-guide/expressions.html#control-flow-expressions). <!-- RSG:168 -->
- Use inline `if-else` only for a small value expression with exactly one `else` branch. — [Rust Style Guide: Single line if else](https://doc.rust-lang.org/style-guide/expressions.html#single-line-if-else). <!-- RSG:169 -->
- Keep the match value unbroken if possible and put indented arms between separately lined braces. — [Rust Style Guide: Match](https://doc.rust-lang.org/style-guide/expressions.html#match). <!-- RSG:170 -->
- Append a comma to a match arm precisely when its body is not a block. — [Rust Style Guide: Match](https://doc.rust-lang.org/style-guide/expressions.html#match). <!-- RSG:171 -->
- Do not prefix a match pattern with an initial `|`. — [Rust Style Guide: Match](https://doc.rust-lang.org/style-guide/expressions.html#match). <!-- RSG:172 -->
- Keep the pattern side of an arm on one line when possible. — [Rust Style Guide: Match](https://doc.rust-lang.org/style-guide/expressions.html#match). <!-- RSG:173 -->
- Do not place a nonempty arm block entirely beside its pattern. — [Rust Style Guide: Match](https://doc.rust-lang.org/style-guide/expressions.html#match). <!-- RSG:174 -->
- Brace an arm body containing multiple statements, line comments, control flow, or a first line too wide to follow the arrow. — [Rust Style Guide: Match](https://doc.rust-lang.org/style-guide/expressions.html#match). <!-- RSG:175 -->
- Retain a block around a macro-only arm to accommodate possible semicolons in its expansion. — [Rust Style Guide: Match](https://doc.rust-lang.org/style-guide/expressions.html#match). <!-- RSG:176 -->
- Indent an arm block's contents once relative to its braces. — [Rust Style Guide: Match](https://doc.rust-lang.org/style-guide/expressions.html#match). <!-- RSG:177 -->
- Begin a plain, uncommented expression body beside its arm pattern. — [Rust Style Guide: Match](https://doc.rust-lang.org/style-guide/expressions.html#match). <!-- RSG:178 -->
- Prefer bracing an arm body to splitting a pattern that need not wrap. — [Rust Style Guide: Line-breaking](https://doc.rust-lang.org/style-guide/expressions.html#line-breaking). <!-- RSG:179 -->
- Do not insert a newline after an arm arrow unless a block follows. — [Rust Style Guide: Line-breaking](https://doc.rust-lang.org/style-guide/expressions.html#line-breaking). <!-- RSG:180 -->
- For a wrapped guard, break before and indent `if`, then start a block body on a fresh line. — [Rust Style Guide: Line-breaking](https://doc.rust-lang.org/style-guide/expressions.html#line-breaking). <!-- RSG:181 -->
- Break alternation patterns before `|` without adding another indentation level. — [Rust Style Guide: Line-breaking](https://doc.rust-lang.org/style-guide/expressions.html#line-breaking). <!-- RSG:182 -->
- Append the guard to a wrapped pattern's last line when that line is narrower than the indentation. — [Rust Style Guide: Line-breaking](https://doc.rust-lang.org/style-guide/expressions.html#line-breaking). <!-- RSG:183 -->
- Pack wrapped alternatives into as few lines as possible only when they meet the source's small-pattern grammar. — [Rust Style Guide: Line-breaking](https://doc.rust-lang.org/style-guide/expressions.html#line-breaking). <!-- RSG:184 -->
- Combine a single-argument call with its wrapped argument's outer delimiters when it fits, repeating inward as appropriate. — [Rust Style Guide: Combinable expressions](https://doc.rust-lang.org/style-guide/expressions.html#combinable-expressions). <!-- RSG:185 -->
- Use the same delimiter-combination rules for analogous macros, tuple constructors, and parenthesized lists. — [Rust Style Guide: Combinable expressions](https://doc.rust-lang.org/style-guide/expressions.html#combinable-expressions). <!-- RSG:186 -->
- In a multi-argument call, combine a final block closure only if it is the sole closure and all earlier arguments plus its first line fit. — [Rust Style Guide: Combinable expressions](https://doc.rust-lang.org/style-guide/expressions.html#combinable-expressions). <!-- RSG:187 -->
- Keep range operators unspaced. — [Rust Style Guide: Ranges](https://doc.rust-lang.org/style-guide/expressions.html#ranges). <!-- RSG:188 -->
- When splitting a bounded range, break before the operator and indent the continuation. — [Rust Style Guide: Ranges](https://doc.rust-lang.org/style-guide/expressions.html#ranges). <!-- RSG:189 -->
- Parenthesize compound range endpoints so precedence is unambiguous. — [Rust Style Guide: Ranges](https://doc.rust-lang.org/style-guide/expressions.html#ranges). <!-- RSG:190 -->
- Choose uppercase or lowercase hexadecimal consistently for the project and never mix them within one literal. — [Rust Style Guide: Hexadecimal literals](https://doc.rust-lang.org/style-guide/expressions.html#hexadecimal-literals). <!-- RSG:191 -->
- Format patterns like corresponding expressions, adding the match-specific conventions when relevant. — [Rust Style Guide: Patterns](https://doc.rust-lang.org/style-guide/expressions.html#patterns). <!-- RSG:192 -->
- Leave slice and array-type brackets unpadded and add a space after an array-length semicolon. — [Rust Style Guide: Single line formatting](https://doc.rust-lang.org/style-guide/types.html#single-line-formatting). <!-- RSG:193 -->
- In raw-pointer types, attach `*` to `const` or `mut` and put a space before the pointee. — [Rust Style Guide: Single line formatting](https://doc.rust-lang.org/style-guide/types.html#single-line-formatting). <!-- RSG:194 -->
- Attach `&` to the following lifetime, `mut`, or type, separating any later words normally. — [Rust Style Guide: Single line formatting](https://doc.rust-lang.org/style-guide/types.html#single-line-formatting). <!-- RSG:195 -->
- In function types, space keywords and arrows normally, follow commas with spaces, and avoid delimiter padding or inline final commas. — [Rust Style Guide: Single line formatting](https://doc.rust-lang.org/style-guide/types.html#single-line-formatting). <!-- RSG:196 -->
- Space the never type as though it were a named type. — [Rust Style Guide: Single line formatting](https://doc.rust-lang.org/style-guide/types.html#single-line-formatting). <!-- RSG:197 -->
- Use comma-space in tuple types, retaining an inline final comma only for a one-element tuple. — [Rust Style Guide: Single line formatting](https://doc.rust-lang.org/style-guide/types.html#single-line-formatting). <!-- RSG:198 -->
- Leave path separators and generic brackets unpadded while spacing `as` inside a qualified path. — [Rust Style Guide: Single line formatting](https://doc.rust-lang.org/style-guide/types.html#single-line-formatting). <!-- RSG:199 -->
- Use normal spaces around type-bound `+` signs and after `impl`. — [Rust Style Guide: Single line formatting](https://doc.rust-lang.org/style-guide/types.html#single-line-formatting). <!-- RSG:200 -->
- Do not add padding inside type-grouping parentheses. — [Rust Style Guide: Single line formatting](https://doc.rust-lang.org/style-guide/types.html#single-line-formatting). <!-- RSG:201 -->
- Keep types unbroken when feasible and split their outermost syntax first when wrapping is necessary. — [Rust Style Guide: Line breaks](https://doc.rust-lang.org/style-guide/types.html#line-breaks). <!-- RSG:202 -->
- Wrap array types after the length-separating semicolon. — [Rust Style Guide: Line breaks](https://doc.rust-lang.org/style-guide/types.html#line-breaks). <!-- RSG:203 -->
- Use declaration layout for wrapped function types and generic-parameter layout for wrapped generic types. — [Rust Style Guide: Line breaks](https://doc.rust-lang.org/style-guide/types.html#line-breaks). <!-- RSG:204 -->
- For multiline type bounds, start each indented continuation with `+`. — [Rust Style Guide: Line breaks](https://doc.rust-lang.org/style-guide/types.html#line-breaks). <!-- RSG:205 -->
- Lay out precise-capture `use` bounds like path segments with ordinary generic arguments, without turbofish syntax. — [Rust Style Guide: Precise capturing bounds](https://doc.rust-lang.org/style-guide/types.html#precise-capturing-bounds). <!-- RSG:206 -->
- Use Rust's indentation and width conventions in Cargo manifests too. — [Rust Style Guide: Formatting conventions](https://doc.rust-lang.org/style-guide/cargo.html#formatting-conventions). <!-- RSG:213 -->
- Begin manifest keys at column one and surround `=` with single spaces. — [Rust Style Guide: Formatting conventions](https://doc.rust-lang.org/style-guide/cargo.html#formatting-conventions). <!-- RSG:218 -->
- Represent multiline manifest values with multiline strings rather than escaped newlines. — [Rust Style Guide: Formatting conventions](https://doc.rust-lang.org/style-guide/cargo.html#formatting-conventions). <!-- RSG:219 -->
- Keep a fitting manifest array beside its key; otherwise use indented comma-terminated entries and a separate closing bracket. — [Rust Style Guide: Formatting conventions](https://doc.rust-lang.org/style-guide/cargo.html#formatting-conventions). <!-- RSG:220 -->
- Use inline braced tables when they fit, promoting larger values to their own table section. — [Rust Style Guide: Formatting conventions](https://doc.rust-lang.org/style-guide/cargo.html#formatting-conventions). <!-- RSG:221 -->
- Introduce formatting changes through style editions to preserve existing formatting checks. — [Rust Style Guide: Rust style editions](https://doc.rust-lang.org/style-guide/editions.html). <!-- RSG:227 -->
- Default to the style edition matching the language edition, but permit choosing the formatter's edition independently. — [Rust Style Guide: Rust style editions](https://doc.rust-lang.org/style-guide/editions.html). <!-- RSG:228 -->
- When designing formatting, prioritize plain-text readability and accessibility, then appearance, diffs and space, then consistency and implementation simplicity. — [Rust Style Guide: Guiding principles and rationale](https://doc.rust-lang.org/style-guide/principles.html). <!-- RSG:234 -->

## Naming

- Favor a single letter for a generic type parameter's name. — [Rust Style Guide: Generics](https://doc.rust-lang.org/style-guide/items.html#generics). <!-- RSG:070 -->
- Name types and enum variants in `UpperCamelCase`. — [Rust Style Guide: Names](https://doc.rust-lang.org/style-guide/advice.html#names). <!-- RSG:208 -->
- Name fields, functions, methods, variables, and macros in `snake_case`. — [Rust Style Guide: Names](https://doc.rust-lang.org/style-guide/advice.html#names). <!-- RSG:209 -->
- Use `SCREAMING_SNAKE_CASE` for constants and immutable static values. — [Rust Style Guide: Names](https://doc.rust-lang.org/style-guide/advice.html#names). <!-- RSG:210 -->
- Resolve keyword collisions with a raw identifier or trailing underscore rather than distorted spelling. — [Rust Style Guide: Names](https://doc.rust-lang.org/style-guide/advice.html#names). <!-- RSG:211 -->

## Files and layout

- Lead a file with alphabetized `extern crate` declarations. — [Rust Style Guide: Items](https://doc.rust-lang.org/style-guide/items.html). <!-- RSG:033 -->
- Order file sections as imports, module declarations, then other items. — [Rust Style Guide: Items](https://doc.rust-lang.org/style-guide/items.html). <!-- RSG:034 -->
- Version-sort imports and modules, giving `self` and `super` precedence. — [Rust Style Guide: Items](https://doc.rust-lang.org/style-guide/items.html). <!-- RSG:035 -->
- Leave `macro_use` module declarations in place when reordering could affect behavior. — [Rust Style Guide: Items](https://doc.rust-lang.org/style-guide/items.html). <!-- RSG:036 -->
- Favor one-line `use` declarations without spaces just inside their braces. — [Rust Style Guide: Imports (use statements)](https://doc.rust-lang.org/style-guide/items.html#imports-use-statements). <!-- RSG:081 -->
- Prefer several imports to an oversized wrapped list, but require an explicit option before a formatter splits imports automatically. — [Rust Style Guide: Large list imports](https://doc.rust-lang.org/style-guide/items.html#large-list-imports). <!-- RSG:082 -->
- Sort each uninterrupted import group using version order. — [Rust Style Guide: Ordering of imports](https://doc.rust-lang.org/style-guide/items.html#ordering-of-imports). <!-- RSG:084 -->
- Keep existing import-group boundaries and the sequence of those groups. — [Rust Style Guide: Ordering of imports](https://doc.rust-lang.org/style-guide/items.html#ordering-of-imports). <!-- RSG:085 -->
- Treat an import attribute as a boundary so reordering preserves macro behavior. — [Rust Style Guide: Ordering of imports](https://doc.rust-lang.org/style-guide/items.html#ordering-of-imports). <!-- RSG:086 -->
- Recursively version-sort import lists with `self` and `super` leading and nested lists or globs at the end of their level. — [Rust Style Guide: Ordering list import](https://doc.rust-lang.org/style-guide/items.html#ordering-list-import). <!-- RSG:087 -->
- Simplify a trailing `self` import to the parent path itself. — [Rust Style Guide: Normalisation](https://doc.rust-lang.org/style-guide/items.html#normalisation). <!-- RSG:088 -->
- Delete import lists that contain no names. — [Rust Style Guide: Normalisation](https://doc.rust-lang.org/style-guide/items.html#normalisation). <!-- RSG:089 -->
- Remove list braces when they contain only one imported item. — [Rust Style Guide: Normalisation](https://doc.rust-lang.org/style-guide/items.html#normalisation). <!-- RSG:090 -->
- Leave other import merging, splitting, and glob rewrites disabled unless explicitly configured. — [Rust Style Guide: Normalisation](https://doc.rust-lang.org/style-guide/items.html#normalisation). <!-- RSG:091 -->
- Wrap an import list containing a nested group even if the entire list would fit inline. — [Rust Style Guide: Nested imports](https://doc.rust-lang.org/style-guide/items.html#nested-imports). <!-- RSG:092 -->
- Give nested imports separate lines while packing other entries into the fewest lines that fit. — [Rust Style Guide: Nested imports](https://doc.rust-lang.org/style-guide/items.html#nested-imports). <!-- RSG:093 -->
- Use conventional module files instead of `path` attributes when possible. — [Rust Style Guide: Modules](https://doc.rust-lang.org/style-guide/advice.html#modules). <!-- RSG:212 -->
- Separate manifest sections by one blank line, keeping headers and consecutive entries together. — [Rust Style Guide: Formatting conventions](https://doc.rust-lang.org/style-guide/cargo.html#formatting-conventions). <!-- RSG:214 -->
- Version-sort manifest keys except for the prescribed package-metadata ordering. — [Rust Style Guide: Formatting conventions](https://doc.rust-lang.org/style-guide/cargo.html#formatting-conventions). <!-- RSG:215 -->
- Put `[package]` first, beginning with `name` and `version`, then other sorted keys, and ending with `description`. — [Rust Style Guide: Formatting conventions](https://doc.rust-lang.org/style-guide/cargo.html#formatting-conventions). <!-- RSG:216 -->
- Keep standard manifest keys unquoted and avoid unusual keys that require quoting. — [Rust Style Guide: Formatting conventions](https://doc.rust-lang.org/style-guide/cargo.html#formatting-conventions). <!-- RSG:217 -->
- When supplying authors, pair names with angle-bracketed email addresses; a mailing-list address may stand alone. — [Rust Style Guide: Metadata conventions](https://doc.rust-lang.org/style-guide/cargo.html#metadata-conventions). <!-- RSG:222 -->
- Declare a valid SPDX license expression; this source also accepts the historical slash-separated spelling. — [Rust Style Guide: Metadata conventions](https://doc.rust-lang.org/style-guide/cargo.html#metadata-conventions). <!-- RSG:223 -->
- Set `homepage` to one absolute URL with an explicit scheme. — [Rust Style Guide: Metadata conventions](https://doc.rust-lang.org/style-guide/cargo.html#metadata-conventions). <!-- RSG:224 -->

## Types and data

- Represent a fieldless struct with the unit form when possible. — [Rust Style Guide: Structs and Unions](https://doc.rust-lang.org/style-guide/items.html#structs-and-unions). <!-- RSG:049 -->
- Use a named-field struct when positional fields become numerous or need wrapping. — [Rust Style Guide: Tuple structs](https://doc.rust-lang.org/style-guide/items.html#tuple-structs). <!-- RSG:054 -->
- For comparisons, prefer dereferencing a borrowed operand to adding a reference to its counterpart when this avoids extra references cheaply. — [Rust Style Guide: Binary operations](https://doc.rust-lang.org/style-guide/expressions.html#binary-operations). <!-- RSG:138 -->
- Prefer constructing values through expressions when that improves clarity. — [Rust Style Guide: Expressions](https://doc.rust-lang.org/style-guide/advice.html#expressions). <!-- RSG:207 -->

## Comments and docs

- Choose line comments in preference to block comments. — [Rust Style Guide: Comments](https://doc.rust-lang.org/style-guide/index.html#comments). <!-- RSG:015 -->
- Insert one space between a line-comment marker and its text. — [Rust Style Guide: Comments](https://doc.rust-lang.org/style-guide/index.html#comments). <!-- RSG:016 -->
- Pad both ends of a single-line block comment's contents with one space. — [Rust Style Guide: Comments](https://doc.rust-lang.org/style-guide/index.html#comments). <!-- RSG:017 -->
- Put multiline block-comment content on lines between its opening and closing delimiters. — [Rust Style Guide: Comments](https://doc.rust-lang.org/style-guide/index.html#comments). <!-- RSG:018 -->
- Usually dedicate a line to a comment; when it follows code, insert one separating space. — [Rust Style Guide: Comments](https://doc.rust-lang.org/style-guide/index.html#comments). <!-- RSG:019 -->
- Space an embedded block comment as though it were another token. — [Rust Style Guide: Comments](https://doc.rust-lang.org/style-guide/index.html#comments). <!-- RSG:020 -->
- Capitalize and punctuate comment sentences; brief inline annotations may omit full-sentence punctuation. — [Rust Style Guide: Comments](https://doc.rust-lang.org/style-guide/index.html#comments). <!-- RSG:021 -->
- Keep comment text within 80 columns before indentation and the whole line within the code limit. — [Rust Style Guide: Comments](https://doc.rust-lang.org/style-guide/index.html#comments). <!-- RSG:022 -->
- Favor line-form rustdoc comments over block-form documentation. — [Rust Style Guide: Doc comments](https://doc.rust-lang.org/style-guide/index.html#doc-comments). <!-- RSG:023 -->
- Document items with outer comments and enclosing crates or modules with inner comments. — [Rust Style Guide: Doc comments](https://doc.rust-lang.org/style-guide/index.html#doc-comments). <!-- RSG:024 -->
- Put an item's documentation ahead of its attributes. — [Rust Style Guide: Doc comments](https://doc.rust-lang.org/style-guide/index.html#doc-comments). <!-- RSG:025 -->
- Keep comments out of function signatures. — [Rust Style Guide: Function definitions](https://doc.rust-lang.org/style-guide/items.html#function-definitions). <!-- RSG:039 -->
- Keep comments off a block's brace-only opening and closing lines. — [Rust Style Guide: Blocks](https://doc.rust-lang.org/style-guide/expressions.html#blocks). <!-- RSG:112 -->
- Start the package description with its purpose instead of its name and wrap it at 80 columns. — [Rust Style Guide: Metadata conventions](https://doc.rust-lang.org/style-guide/cargo.html#metadata-conventions). <!-- RSG:225 -->
- For a multi-sentence description, keep the opening summary sentence on its own line. — [Rust Style Guide: Metadata conventions](https://doc.rust-lang.org/style-guide/cargo.html#metadata-conventions). <!-- RSG:226 -->

## Testing

- Check formatter changes on existing projects to catch accidental large-scale churn. — [Rust Style Guide: Bugs](https://doc.rust-lang.org/style-guide/index.html#bugs). <!-- RSG:002 -->

## Security

- Specify the ABI explicitly on external functions and blocks. — [Rust Style Guide: extern items](https://doc.rust-lang.org/style-guide/items.html#extern-items). <!-- RSG:080 -->

## Language-specific pitfalls

- For new syntax missing from an archived guide, apply its earliest later style rules without adopting unrelated edition-wide changes. — [Rust Style Guide: Rust style editions](https://doc.rust-lang.org/style-guide/editions.html). <!-- RSG:229 -->
- Only when using the unstable frontmatter feature, place it before comments and attributes, without a leading blank line or a gap after a shebang. — [Rust Style Guide: Frontmatter](https://doc.rust-lang.org/style-guide/nightly.html#frontmatter). <!-- RSG:230 -->
- For unstable frontmatter, leave at most one blank line after the block. — [Rust Style Guide: Frontmatter](https://doc.rust-lang.org/style-guide/nightly.html#frontmatter). <!-- RSG:231 -->
- For unstable frontmatter, use at least three fence dashes and exceed the content's longest leading dash run by one. — [Rust Style Guide: Frontmatter](https://doc.rust-lang.org/style-guide/nightly.html#frontmatter). <!-- RSG:232 -->
- For unstable frontmatter, separate an optional fence info string by one space and remove fence-line trailing whitespace. — [Rust Style Guide: Frontmatter](https://doc.rust-lang.org/style-guide/nightly.html#frontmatter). <!-- RSG:233 -->

## Original worked examples

See [sources.md](sources.md) for original code, source tags and reading pointers.
