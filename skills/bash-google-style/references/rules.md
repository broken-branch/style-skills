# Google Shell rules

Google Shell rules, including the Bash choice and its portability exception. Examples and the build-rule filename convention are omitted.

Source owner: Google. License: [CC-BY-3.0](../LICENSE). Changes by style-skills contributors: rules independently restated and shortened, examples dropped, and source-local policy excluded. Unofficial; no endorsement is implied.

## Tooling

- Run ShellCheck on shell scripts regardless of their length. — [Google: ShellCheck](https://google.github.io/styleguide/shellguide.html#s6.1-shellcheck). <!-- google-shell:59 -->

## Formatting

- Indent newly written shell code with two spaces per level. — [Google: Indentation](https://google.github.io/styleguide/shellguide.html#s5.1-indentation). <!-- google-shell:27 -->
- Match the indentation already used in a file being edited. — [Google: Indentation](https://google.github.io/styleguide/shellguide.html#s5.1-indentation). <!-- google-shell:28 -->
- Separate logical code blocks with empty lines. — [Google: Indentation](https://google.github.io/styleguide/shellguide.html#s5.1-indentation). <!-- google-shell:29 -->
- Reserve tab indentation for the body of a `<<-` heredoc. — [Google: Indentation](https://google.github.io/styleguide/shellguide.html#s5.1-indentation). <!-- google-shell:30 -->
- Limit normal source lines to 80 columns. — [Google: Line Length and Long Strings](https://google.github.io/styleguide/shellguide.html#s5.2-line-length-and-long-strings). <!-- google-shell:31 -->
- For a long string literal, prefer a heredoc or actual line breaks when feasible. — [Google: Line Length and Long Strings](https://google.github.io/styleguide/shellguide.html#s5.2-line-length-and-long-strings). <!-- google-shell:32 -->
- Allow indivisible words, paths, or URLs to exceed 80 columns; place them alone or in a variable where feasible, and wrap the surrounding code normally. — [Google: Line Length and Long Strings](https://google.github.io/styleguide/shellguide.html#s5.2-line-length-and-long-strings). <!-- google-shell:33 -->
- Leave a pipeline on one line when the complete expression fits. — [Google: Pipelines](https://google.github.io/styleguide/shellguide.html#s5.3-pipelines). <!-- google-shell:34 -->
- Wrap an overlong pipeline or `&&`/`||` chain into one command segment per line, starting continuation lines with the joining operator. — [Google: Pipelines](https://google.github.io/styleguide/shellguide.html#s5.3-pipelines). <!-- google-shell:35 -->
- Mark continuations consistently with backslashes and give subsequent pipeline segments a two-space indent. — [Google: Pipelines](https://google.github.io/styleguide/shellguide.html#s5.3-pipelines). <!-- google-shell:36 -->
- Place pipeline comments above the complete expression; move intricate operations into helpers when that makes the pipeline clearer. — [Google: Pipelines](https://google.github.io/styleguide/shellguide.html#s5.3-pipelines). <!-- google-shell:37 -->
- Keep `; then` beside the opening `if` and `; do` beside the opening loop header. — [Google: Control Flow](https://google.github.io/styleguide/shellguide.html#s5.4-control-flow). <!-- google-shell:38 -->
- Give `else`, `fi`, and `done` separate lines. — [Google: Control Flow](https://google.github.io/styleguide/shellguide.html#s5.4-control-flow). <!-- google-shell:39 -->
- Line up `fi` and `done` with the corresponding opening keyword. — [Google: Control Flow](https://google.github.io/styleguide/shellguide.html#s5.4-control-flow). <!-- google-shell:40 -->
- Include `in "$@"` explicitly when looping through the script's positional arguments. — [Google: Control Flow](https://google.github.io/styleguide/shellguide.html#s5.4-control-flow). <!-- google-shell:41 -->
- Indent `case` patterns one level inside the statement and their multiline bodies one further level. — [Google: Case statement](https://google.github.io/styleguide/shellguide.html#s5.5-case-statement). <!-- google-shell:42 -->
- Start each `case` alternative with its pattern rather than an opening parenthesis. — [Google: Case statement](https://google.github.io/styleguide/shellguide.html#s5.5-case-statement). <!-- google-shell:43 -->
- A readable, short `case` alternative may keep its pattern, action, and `;;` together on one line. — [Google: Case statement](https://google.github.io/styleguide/shellguide.html#s5.5-case-statement). <!-- google-shell:44 -->
- For longer `case` alternatives, give the pattern, body, and closing `;;` distinct lines. — [Google: Case statement](https://google.github.io/styleguide/shellguide.html#s5.5-case-statement). <!-- google-shell:45 -->
- In a one-line `case` alternative, leave a space after `)` and another before `;;`. — [Google: Case statement](https://google.github.io/styleguide/shellguide.html#s5.5-case-statement). <!-- google-shell:46 -->
- Avoid `;&` and `;;&` when ending `case` alternatives. — [Google: Case statement](https://google.github.io/styleguide/shellguide.html#s5.5-case-statement). <!-- google-shell:47 -->
- Follow a function name immediately with `()` in its definition. — [Google: Function Names](https://google.github.io/styleguide/shellguide.html#s7.1-function-names). <!-- google-shell:83 -->
- Open a function's body on the same line as its name. — [Google: Function Names](https://google.github.io/styleguide/shellguide.html#s7.1-function-names). <!-- google-shell:84 -->
- Either include or omit `function`, but make that choice uniform throughout the project. — [Google: Function Names](https://google.github.io/styleguide/shellguide.html#s7.1-function-names). <!-- google-shell:85 -->

## Naming

- Write function identifiers in lowercase, separating words with underscores. — [Google: Function Names](https://google.github.io/styleguide/shellguide.html#s7.1-function-names). <!-- google-shell:80 -->
- A library may namespace its functions with a library or package prefix followed by `::`; standalone functions need no namespace. — [Google: Function Names](https://google.github.io/styleguide/shellguide.html#s7.1-function-names). <!-- google-shell:81 -->
- Avoid colon-separated function namespaces where the calling context handles them poorly, including interactive completion. — [Google: Function Names](https://google.github.io/styleguide/shellguide.html#s7.1-function-names). <!-- google-shell:82 -->
- Use lowercase underscore-separated variable names, and name loop variables after the items they represent. — [Google: Variable Names](https://google.github.io/styleguide/shellguide.html#s7.2-variable-names). <!-- google-shell:86 -->
- Name constants and environment exports with uppercase words joined by underscores. — [Google: Constants, Environment Variables, and readonly Variables](https://google.github.io/styleguide/shellguide.html#s7.3-constants-and-environment-variable-names). <!-- google-shell:87 -->
- Use lowercase source filenames, joining words with underscores if needed; avoid hyphens. — [Google: Source Filenames](https://google.github.io/styleguide/shellguide.html#s7.4-source-filenames). <!-- google-shell:91 -->

## Files and layout

- Use Bash features freely; target plain Bourne shell only when the execution environment requires it. — [Google — Shell choice](https://google.github.io/styleguide/shellguide.html#s1.1-which-shell-to-use).

- Use Bash for executables, starting with `#!/bin/bash` and minimal interpreter flags. — [Google — Shell choice](https://google.github.io/styleguide/shellguide.html#s1.1-which-shell-to-use).

- Configure interpreter options through `set` inside the script so a direct Bash invocation retains them. — [Google: Which Shell to Use](https://google.github.io/styleguide/shellguide.html#s1.1-which-shell-to-use). <!-- google-shell:3 -->
- Choose shell for modest utilities and wrappers that mainly invoke other programs with little data processing. — [Google: When to use Shell](https://google.github.io/styleguide/shellguide.html#s1.2-when-to-use-shell). <!-- google-shell:5 -->
- Rewrite a script in a more structured language once it exceeds about 100 lines or needs complicated control flow. — [Google: When to use Shell](https://google.github.io/styleguide/shellguide.html#s1.2-when-to-use-shell). <!-- google-shell:7 -->
- Assess script complexity by how readily another maintainer could understand and change it. — [Google: When to use Shell](https://google.github.io/styleguide/shellguide.html#s1.2-when-to-use-shell). <!-- google-shell:8 -->
- Migrate a growing script before accumulated shell complexity makes the rewrite expensive. — [Google: When to use Shell](https://google.github.io/styleguide/shellguide.html#s1.2-when-to-use-shell). <!-- google-shell:9 -->
- Executable shell source may have a `.sh` suffix or no suffix. — [Google: File Extensions](https://google.github.io/styleguide/shellguide.html#s2.1-file-extensions). <!-- google-shell:10 -->
- Prefer extensionless executables when users run them directly from `PATH`. — [Google: File Extensions](https://google.github.io/styleguide/shellguide.html#s2.1-file-extensions). <!-- google-shell:12 -->
- Use `.sh` for shell libraries and keep their executable permission unset. — [Google: File Extensions](https://google.github.io/styleguide/shellguide.html#s2.1-file-extensions). <!-- google-shell:13 -->
- Keep constant definitions and exported environment declarations at the beginning of the file. — [Google: Constants, Environment Variables, and readonly Variables](https://google.github.io/styleguide/shellguide.html#s7.3-constants-and-environment-variable-names). <!-- google-shell:88 -->
- Collect the function definitions directly below the constants. — [Google: Function Location](https://google.github.io/styleguide/shellguide.html#s7.6-function-location). <!-- google-shell:94 -->
- Before the function block, restrict execution to sourcing dependencies, setting shell options, and initializing constants; do not scatter application logic among definitions. — [Google: Function Location](https://google.github.io/styleguide/shellguide.html#s7.6-function-location). <!-- google-shell:95 -->
- Give an executable script a `main` function once it defines any other function. — [Google: main](https://google.github.io/styleguide/shellguide.html#s7.7-main). <!-- google-shell:96 -->
- Make `main` the last function defined in a script. — [Google: main](https://google.github.io/styleguide/shellguide.html#s7.7-main). <!-- google-shell:97 -->
- End a script using `main` with a call that forwards `"$@"`, followed only by comments if necessary. — [Google: main](https://google.github.io/styleguide/shellguide.html#s7.7-main). <!-- google-shell:98 -->
- A brief script with only straight-line execution can omit `main`. — [Google: main](https://google.github.io/styleguide/shellguide.html#s7.7-main). <!-- google-shell:99 -->

## Types and data

- For variable expansions, prioritize the surrounding convention first, quotation second, and optional braces third. — [Google: Variable expansion](https://google.github.io/styleguide/shellguide.html#s5.6-variable-expansion). <!-- google-shell:48 -->
- Prefer brace-delimited expansion for ordinary named variables when the existing style leaves the choice open. — [Google: Variable expansion](https://google.github.io/styleguide/shellguide.html#s5.6-variable-expansion). <!-- google-shell:49 -->
- Leave one-character special and positional parameters unbraced unless braces are needed for parsing or clarity. — [Google: Variable expansion](https://google.github.io/styleguide/shellguide.html#s5.6-variable-expansion). <!-- google-shell:50 -->
- Brace-delimited variable expansion still needs double quotes where quoting is required. — [Google: Variable expansion](https://google.github.io/styleguide/shellguide.html#s5.6-variable-expansion). <!-- google-shell:51 -->
- Quote strings with variable or command expansions, spaces, or shell metacharacters, except for an intentional unquoted expansion or the source's internal-integer allowance. — [Google: Quoting](https://google.github.io/styleguide/shellguide.html#s5.7-quoting). <!-- google-shell:52 -->
- Keep argument sequences in arrays so each argument retains its quotation boundaries. — [Google: Quoting](https://google.github.io/styleguide/shellguide.html#s5.7-quoting). <!-- google-shell:53 -->
- Quoting the shell's readonly integer parameters `$?`, `$#`, `$$`, and `$!` is discretionary. — [Google: Quoting](https://google.github.io/styleguide/shellguide.html#s5.7-quoting). <!-- google-shell:54 -->
- Prefer quotes around named internal integer variables to keep their treatment consistent with other names. — [Google: Quoting](https://google.github.io/styleguide/shellguide.html#s5.7-quoting). <!-- google-shell:55 -->
- Prefer quotes for literal word strings; this preference does not require quoting ordinary options or pathnames. — [Google: Quoting](https://google.github.io/styleguide/shellguide.html#s5.7-quoting). <!-- google-shell:56 -->
- In `[[ … ]]`, quote literal comparison text while leaving intended pattern or regular-expression syntax active. — [Google: Quoting](https://google.github.io/styleguide/shellguide.html#s5.7-quoting). <!-- google-shell:57 -->
- Forward separate positional arguments with `"$@"`; use `"$*"` only when a single joined string is intended. — [Google: Quoting](https://google.github.io/styleguide/shellguide.html#s5.7-quoting). <!-- google-shell:58 -->
- Represent a sequence of strings or command arguments as an array. — [Google: Arrays](https://google.github.io/styleguide/shellguide.html#s6.7-arrays). <!-- google-shell:68 -->
- Expand an array as `"${array[@]}"` when each element must remain a separate argument. — [Google: Arrays](https://google.github.io/styleguide/shellguide.html#s6.7-arrays). <!-- google-shell:69 -->
- Avoid packing several command arguments, with embedded quoting, into a scalar string. — [Google: Arrays](https://google.github.io/styleguide/shellguide.html#s6.7-arrays). <!-- google-shell:70 -->
- Use another language when the data processing calls for structures more elaborate than simple shell arrays. — [Google: Arrays](https://google.github.io/styleguide/shellguide.html#s6.7-arrays). <!-- google-shell:71 -->
- For ordinary variable references inside arithmetic contexts, prefer the bare name when it improves readability. — [Google: Arithmetic](https://google.github.io/styleguide/shellguide.html#s6.9-arithmetic). <!-- google-shell:78 -->
- Prefer `readonly` and `export` for their respective declarations over equivalent `declare` options. — [Google: Constants, Environment Variables, and readonly Variables](https://google.github.io/styleguide/shellguide.html#s7.3-constants-and-environment-variable-names). <!-- google-shell:89 -->
- After computing a constant at runtime, mark it `readonly` immediately. — [Google: Constants, Environment Variables, and readonly Variables](https://google.github.io/styleguide/shellguide.html#s7.3-constants-and-environment-variable-names). <!-- google-shell:90 -->
- Declare a function's internal variables with `local` to limit their scope to that function and its children. — [Google: Use Local Variables](https://google.github.io/styleguide/shellguide.html#s7.5-use-local-variables). <!-- google-shell:92 -->

## Errors

- Write diagnostics for failures to standard error. — [Google: STDOUT vs STDERR](https://google.github.io/styleguide/shellguide.html#s3.1-stdout-vs-stderr). <!-- google-shell:16 -->
- Consider a shared diagnostic helper that adds context to each error message. — [Google: STDOUT vs STDERR](https://google.github.io/styleguide/shellguide.html#s3.1-stdout-vs-stderr). <!-- google-shell:17 -->
- Prefer to avoid standalone `(( … ))` commands and account for their unsuccessful status when the expression is zero, especially under `set -e`. — [Google: Arithmetic](https://google.github.io/styleguide/shellguide.html#s6.9-arithmetic). <!-- google-shell:77 -->
- When capturing command output in a local variable, declare it first and assign separately so the command's status remains available. — [Google: Use Local Variables](https://google.github.io/styleguide/shellguide.html#s7.5-use-local-variables). <!-- google-shell:93 -->
- Inspect command exit codes and choose return statuses that communicate the outcome. — [Google: Checking Return Values](https://google.github.io/styleguide/shellguide.html#s8.1-checking-return-values). <!-- google-shell:100 -->
- For a command outside a pipeline, test it directly with `if` or examine `$?` before another command replaces it. — [Google: Checking Return Values](https://google.github.io/styleguide/shellguide.html#s8.1-checking-return-values). <!-- google-shell:101 -->
- Use `PIPESTATUS` when the outcome of individual pipeline stages matters. — [Google: Checking Return Values](https://google.github.io/styleguide/shellguide.html#s8.1-checking-return-values). <!-- google-shell:102 -->
- If later handling distinguishes which pipeline stage failed, save `PIPESTATUS` immediately after the pipeline. — [Google: Checking Return Values](https://google.github.io/styleguide/shellguide.html#s8.1-checking-return-values). <!-- google-shell:103 -->

## Comments and docs

- Open every file with a short comment describing its contents; author details and copyright notices are optional. — [Google: File Header](https://google.github.io/styleguide/shellguide.html#s4.1-file-header). <!-- google-shell:18 -->
- Add a header comment to a function unless it is both brief and self-explanatory. — [Google: Function Comments](https://google.github.io/styleguide/shellguide.html#s4.2-function-comments). <!-- google-shell:19 -->
- Document every library function with a header comment, including trivial ones. — [Google: Function Comments](https://google.github.io/styleguide/shellguide.html#s4.2-function-comments). <!-- google-shell:20 -->
- Make the comments and any built-in help sufficient to understand how to use the program or library without studying its implementation. — [Google: Function Comments](https://google.github.io/styleguide/shellguide.html#s4.2-function-comments). <!-- google-shell:21 -->
- In function documentation, cover behavior, globals accessed or changed, parameters, stdout/stderr output, and return values that differ from the last command's default status. — [Google: Function Comments](https://google.github.io/styleguide/shellguide.html#s4.2-function-comments). <!-- google-shell:22 -->
- Explain significant or surprising implementation choices without commenting on every obvious operation. — [Google: Implementation Comments](https://google.github.io/styleguide/shellguide.html#s4.3-implementation-comments). <!-- google-shell:23 -->
- Mark provisional, incomplete, or temporary code with an uppercase `TODO` comment. — [Google: TODO Comments](https://google.github.io/styleguide/shellguide.html#s4.4-todo-comments). <!-- google-shell:24 -->
- Include in each TODO an identifier for a person who can explain the issue. — [Google: TODO Comments](https://google.github.io/styleguide/shellguide.html#s4.4-todo-comments). <!-- google-shell:25 -->
- Treat a TODO's named contact as a source of context, not a promise to implement the fix. — [Google: TODO Comments](https://google.github.io/styleguide/shellguide.html#s4.4-todo-comments). <!-- google-shell:26 -->

## Performance

- Use a language other than shell when execution performance is a requirement. — [Google: When to use Shell](https://google.github.io/styleguide/shellguide.html#s1.2-when-to-use-shell). <!-- google-shell:6 -->
- Prefer an equivalent Bash builtin or expansion over starting an external program. — [Google: Builtin Commands vs. External Commands](https://google.github.io/styleguide/shellguide.html#s8.2-builtin-commands-vs-external-commands). <!-- google-shell:104 -->

## Security

- Do not enable SUID or SGID permission bits on shell scripts. — [Google: SUID/SGID](https://google.github.io/styleguide/shellguide.html#s2.2-suid-sgid). <!-- google-shell:14 -->
- Use `sudo` when the script requires elevated access. — [Google: SUID/SGID](https://google.github.io/styleguide/shellguide.html#s2.2-suid-sgid). <!-- google-shell:15 -->
- Give filename globs an explicit directory prefix so a leading dash in a filename cannot become an option. — [Google: Wildcard Expansion of Filenames](https://google.github.io/styleguide/shellguide.html#s6.5-wildcard-expansion-of-filenames). <!-- google-shell:66 -->
- Avoid evaluating constructed shell code with `eval`. — [Google: Eval](https://google.github.io/styleguide/shellguide.html#s6.6-eval). <!-- google-shell:67 -->

## Language-specific pitfalls

- Capture command output with `$(…)` instead of backtick substitution. — [Google: Command Substitution](https://google.github.io/styleguide/shellguide.html#s6.2-command-substitution). <!-- google-shell:60 -->
- Prefer Bash's double-bracket conditional over single-bracket tests or the `test` command. — [Google: Test, &#91; … &#93;, and &#91;&#91; … &#93;&#93;](https://google.github.io/styleguide/shellguide.html#s6.3-tests). <!-- google-shell:61 -->
- Compare quoted string operands directly instead of adding protective filler characters. — [Google: Testing Strings](https://google.github.io/styleguide/shellguide.html#s6.4-testing-strings). <!-- google-shell:62 -->
- Express string emptiness explicitly with `-z` or `-n`. — [Google: Testing Strings](https://google.github.io/styleguide/shellguide.html#s6.4-testing-strings). <!-- google-shell:63 -->
- Prefer `==` for string equality in Bash conditionals. — [Google: Testing Strings](https://google.github.io/styleguide/shellguide.html#s6.4-testing-strings). <!-- google-shell:64 -->
- Compare numbers arithmetically or with numeric test operators; `<` and `>` inside `[[ … ]]` compare text. — [Google: Testing Strings](https://google.github.io/styleguide/shellguide.html#s6.4-testing-strings). <!-- google-shell:65 -->
- When loop assignments must persist, feed the loop with process substitution or read into an array instead of piping into the loop. — [Google: Pipes to While](https://google.github.io/styleguide/shellguide.html#s6.8-pipes-to-while). <!-- google-shell:72 -->
- Supply command output to `readarray` through process substitution so the populated array remains in the calling shell. — [Google: Pipes to While](https://google.github.io/styleguide/shellguide.html#s6.8-pipes-to-while). <!-- google-shell:73 -->
- Use a line-reading loop or `readarray` when command output must retain line boundaries; unquoted command substitution splits words. — [Google: Pipes to While](https://google.github.io/styleguide/shellguide.html#s6.8-pipes-to-while). <!-- google-shell:74 -->
- Perform integer calculations with `(( … ))` or `$(( … ))`, avoiding `let`, `$[ … ]`, and `expr`. — [Google: Arithmetic](https://google.github.io/styleguide/shellguide.html#s6.9-arithmetic). <!-- google-shell:75 -->
- Prefer `(( … ))` for numeric conditions over `[[ … ]]`. — [Google: Arithmetic](https://google.github.io/styleguide/shellguide.html#s6.9-arithmetic). <!-- google-shell:76 -->
- Implement reusable script operations as functions instead of aliases. — [Google: Aliases](https://google.github.io/styleguide/shellguide.html#s6.10-aliases). <!-- google-shell:79 -->

## Where the sources disagree

No unresolved source conflicts in this single-source adaptation; the source's consistency guidance follows.

- Use consistency to settle stylistic choices when neither a technical reason nor a long-term direction favors another choice. — [Google: When in Doubt: Be Consistent](https://google.github.io/styleguide/shellguide.html#s9-conclusion). <!-- google-shell:105 -->
- Before retaining an older convention, consider the benefits of a better style and the codebase's direction of change. — [Google: When in Doubt: Be Consistent](https://google.github.io/styleguide/shellguide.html#s9-conclusion). <!-- google-shell:106 -->

## Original worked examples

Original code under this skill's license: [literal prefixes and argument arrays](examples/filter_prefix.sh), [local declarations and command status](examples/command_status.sh).
