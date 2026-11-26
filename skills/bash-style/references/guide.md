# Bash style guide

Scope: owned, noninteractive Bash scripts and sourced libraries on Linux, using Bash 5.2-compatible syntax and explicitly declared external utilities. Validation uses Bash 5.3.20. POSIX `sh`, interactive startup files, and macOS's system Bash 3.2 need separate profiles.
Baseline: [shared rules](shared.md), including dependencies, commits, versioning, review, and AI agent workflow.
MUST means required; PREFER means the default, with a reason recorded for departures.
Source tags resolve in [source credits](sources.md#source-tags).

## Quick rules

- MUST give executable Bash scripts a Bash shebang and invoke them directly or with `bash`, never `sh`; prefer `#!/bin/bash` on this Linux baseline, using `#!/usr/bin/env bash` only with a controlled PATH resolving the required runtime. Why: the interpreter determines whether Bash syntax works. [GOOGLE-SHELL] [BASH-MANUAL] [SHELLCHECK]
- PREFER shell for short command wrappers; reconsider the language around 100 lines or when control flow or data structures become complicated. Why: shell scales poorly as an application language. [GOOGLE-SHELL]
- MUST double-quote data expansions in command arguments and redirections, including nested command substitutions; leave only intended pattern syntax unquoted. Why: unquoted expansion can split data or expand filenames. [GOOGLE-SHELL] [SHELLCHECK]
- MUST store argument lists in arrays and forward them with `"${args[@]}"` or `"$@"`. Why: a string cannot preserve empty arguments and argument boundaries. [GOOGLE-SHELL] [SHELLCHECK]
- MUST use `[[ ... ]]` for Bash string/file tests, quote a literal equality operand on the right, and distinguish it from an intentional glob or regex. Why: test syntax changes expansion and matching behavior. [GOOGLE-SHELL] [SHELLCHECK]
- MUST use `IFS= read -r` for literal text lines and NUL-delimited records for arbitrary filenames. Why: whitespace, backslashes, and newlines can be data. [SHELLCHECK] [BASH-MANUAL]
- MUST iterate filenames with guarded globs, arrays, `find -exec`, or NUL-delimited streams, never parsed `ls` output or `for item in $(command)`. Why: display text and word splitting cannot preserve filenames. [SHELLCHECK]
- MUST test command status directly with `if command; then` or `if ! command; then`, rather than a later test of `$?`. Why: intervening commands can overwrite the result. [SHELLCHECK]
- PREFER explicit status handling with `set -u -o pipefail` in standalone scripts; add `errexit` only as a tested extra guard. Why: nounset and pipefail expose common mistakes while errexit has context-dependent exceptions. [SHELLCHECK] [BASH-MANUAL]
- MUST separate `local`, `readonly`, or `export` declarations from assignments that capture command output. Why: declaration builtins can mask a failed substitution. [GOOGLE-SHELL] [SHELLCHECK]
- MUST handle fallible commands inside functions explicitly even when callers enable `set -e`. Why: condition-invoked functions and command substitutions can suppress errexit. [SHELLCHECK] [BASH-MANUAL]
- MUST check meaningful pipeline failures with `pipefail` or an immediately saved `PIPESTATUS` array, and account for consumers that close the pipe early. Why: the final command alone can hide upstream failure or SIGPIPE. [GOOGLE-SHELL] [BASH-MANUAL]
- MUST declare function scratch variables with `local`, and pass inputs explicitly instead of relying on a caller's locals. Why: Bash locals have dynamic scope and remain visible to called functions. [GOOGLE-SHELL] [BASH-MANUAL]
- MUST use `return` for library/function failures, reserve `exit` for the executable boundary, and send diagnostics to stderr. Why: sourcing executes inside the caller and stdout may carry data. [GOOGLE-SHELL] [BASH-MANUAL]
- MUST validate or default environment inputs and optional positional parameters before expansion, using forms such as `${INPUT:?message}` and `${1-}` deliberately. Why: unset and empty are distinct states, especially under nounset. [SHELLCHECK] [BASH-MANUAL]
- MUST keep sourced libraries from changing caller options, traps, working directory, or IFS on load; explicitly scope any needed changes. Why: sourcing shares the caller's execution environment. [BASH-MANUAL]
- MUST allocate temporary paths with `mktemp`, check creation, and arrange `EXIT` cleanup that preserves the original failure status. Why: predictable names and cleanup that hides failure make shell workflows unsafe. [SHELLCHECK] [BASH-MANUAL]
- MUST avoid `eval` in owned Bash code; use arrays, explicit dispatch, or validated Bash indirection. Why: reevaluating strings destroys the separation between data and shell syntax. [GOOGLE-SHELL] [SHELLCHECK]
- MUST pass data to a fixed `printf` format, such as `printf '%s\n' "$value"`. Why: data used as the format can interpret percent sequences and escapes. [SHELLCHECK]
- MUST protect filename operands with `--` where supported and explicit paths such as `./` for globs or commands without an option terminator. Why: quoting alone does not stop dash-leading names from becoming options. [GOOGLE-SHELL] [SHELLCHECK]
- MUST validate external numbers as bounded decimal digits before arithmetic or indexed-array use; apply `10#` only after validation when leading zeros are allowed. Why: Bash evaluates arithmetic expressions recursively and leading zero means octal. [BASH-MANUAL] [SHELLCHECK]
- MUST redirect input into loops whose assignments must survive; separately collect failures from process substitutions or background jobs. Why: pipeline loops can run in subshells and asynchronous failures do not become the consumer's status. [GOOGLE-SHELL] [BASH-MANUAL] [SHELLCHECK]
- MUST guard `cd` before dependent commands and check a destructive target's nonempty value and intended location before removal. Why: a failed directory change or empty path can redirect an operation. [SHELLCHECK]
- MUST put executable flow in `main` when there are other functions, place its definition last, and finish with `main "$@"`. Why: shell definitions execute in order and argument forwarding must remain explicit. [GOOGLE-SHELL]
- MUST test Bash scripts with empty, spaced, wildcard, newline, and dash-leading arguments, plus command failures and distinct stdout/stderr expectations. Why: ordinary-looking input misses shell expansion and status bugs. [SHELLCHECK] [BASH-MANUAL]

## Tooling

For your project, merge the bundled EditorConfig settings, copy `.shellcheckrc` into the scripts' ancestor directory, and run `shfmt -d`, `shellcheck --check-sourced --severity=style`, and `bash -n` against your own shell files.

| Purpose | Tool and version | Config file | Repository command |
| --- | --- | --- | --- |
| Formatter | shfmt 3.14.1 | [.editorconfig](config/.editorconfig) | `shfmt -d <owned-shell-files>` |
| Linter | ShellCheck 0.11.0 | [.shellcheckrc](config/.shellcheckrc) | `SHELLCHECK_OPTS='' shellcheck --rcfile=.shellcheckrc --check-sourced --severity=style <owned-shell-files>` |
| Build / type checks | Bash 5.3.20; syntax only, no type checker | Bash interpreter | `bash -n <owned-script>` |
| Tests | Bash 5.3.20 and existing Linux utilities | Project's shell test suite | Project's declared shell test command |

Mechanical formatting: the formatter handles this.

Run these commands from the consuming repository after merging the Bash EditorConfig settings and placing `.shellcheckrc` above the scripts. Replace placeholders with explicit owned files, including sourced libraries and extensionless commands. Not yet run against shfmt 3.14.1; rerun formatting and ShellCheck 0.11.0 after adoption.

- MUST declare Bash via a shebang or `# shellcheck shell=bash` in a shebang-free library, and preserve ShellCheck's dialect detection. Why: a global Bash override would conceal a mistaken `sh` declaration. [SHELLCHECK-MANUAL]
- MUST keep `--check-sourced` in the lint command and identify resolvable library paths with a `source=` directive where needed. Why: following includes and reporting their diagnostics are separate settings. [SHELLCHECK-MANUAL]
- MUST run shfmt with the shipped EditorConfig and without parser/printer flags such as `-ln`, `-i`, `-s`/`--simplify`, or `-mn`/`--minify`; give stdin a real `--filename`. Why: those flags bypass EditorConfig formatting and unnamed stdin cannot locate it. [SHFMT]
- PREFER retaining surrounding discretionary expansion bracing; in new Bash files use `"$var"` unless braces are required, leaving optional `require-variable-braces` disabled. Why: optional bracing adds no data-boundary protection. [GOOGLE-SHELL] [SHELLCHECK]
- MUST keep lint exceptions adjacent to the affected command using a reason comment and a specific `# shellcheck disable=SCxxxx` directive. Why: ShellCheck directives apply to the following command or compound block. [SHELLCHECK-MANUAL]

Optional SC2312 and SC2310/SC2311 are unselected: ordinary process substitutions and explicitly checked function conditions are permitted. Producer failures that matter still require explicit collection; `set -e` is never a substitute. [SHFMT] [SHELLCHECK]

### Enforcement map

The RC enables default diagnostics and eight named optional checks, with no disabled codes. The command includes `style` severity, so any reported diagnostic fails it. The following table maps the guide's semantic rules to diagnostics; most checks detect patterns rather than establish the full contract. Syntax diagnostics remain enabled as well. [SHELLCHECK-MANUAL] [SHELLCHECK-SOURCE]

| Optional setting | Diagnostic ID | Coverage |
| --- | --- | --- |
| `add-default-case` | `SC2249` | Missing fallback in `case`; the fallback's behavior needs review. |
| `avoid-negated-conditions` | `SC2335` | Inverted comparisons with a direct opposite operator. |
| `avoid-nullary-conditions` | `SC2244` | Implicit nonempty-string tests. |
| `check-unassigned-uppercase` | `SC2154` | Extends the normal unassigned-variable check to uppercase names. |
| `deprecate-which` | `SC2230` | `which` in place of `command -v`. |
| `quote-safe-variables` | `SC2248` | Unquoted argument expansions even when current inferred values look safe. |
| `require-double-brackets` | `SC2292` | Single-bracket tests in Bash/Ksh. |
| `useless-use-of-cat` | `SC2002` | Avoidable `cat` processes. |

| Default diagnostic IDs | Mapped behavior |
| --- | --- |
| `SC1008`, `SC1071`, `SC2148`, `SC2239`, `SC2246` | Unknown/unsupported or malformed interpreter declarations; minimum Bash version needs review. |
| `SC1090`, `SC1091`, `SC1092`, `SC1094` | Dynamic, unresolved, recursive, or unparsable includes. |
| `SC2046`, `SC2048`, `SC2068`, `SC2086`, `SC2089`, `SC2090`, `SC2124`, `SC2145`, `SC2206`, `SC2207`, `SC2231` | Splitting, argument forwarding, quoted array elements, and strings mistaken for argument lists. |
| `SC2010`, `SC2011`, `SC2012`, `SC2013`, `SC2035`, `SC2038`, `SC2044`, `SC2045`, `SC2144`, `SC2162`, `SC2202` | Fragile filename/line loops, raw reads, glob operands, and dash-leading names; delimiter choice needs review. |
| `SC2049`, `SC2053`, `SC2071`, `SC2076`, `SC2236`, `SC2237`, `SC2254`, `SC2295` | Literal versus pattern comparisons, lexical/numeric confusion, and explicit emptiness tests. |
| `SC2034`, `SC2153`, `SC2154`, `SC2165`, `SC2167`, `SC2168`, `SC2318` | Unused/unassigned variables, nested loop variable reuse, invalid `local`, and dependent declarations. |
| `SC2015`, `SC2155`, `SC2181`, `SC2251`, `SC2319`, `SC2320` | Misleading AND/OR chains, masked declarations, indirect status tests, and overwritten statuses. |
| `SC2030`, `SC2031`, `SC2094`, `SC2095`, `SC2106`, `SC2259`, `SC2260`, `SC2261` | Lost subshell state, reading an overwritten file, consumed loop input, and conflicting stream routing. |
| `SC2064`, `SC2069`, `SC2172`, `SC2173`, `SC2186` | Early trap expansion, redirection ordering, signal names, untrappable signals, and obsolete temp-file tools. |
| `SC2114`, `SC2115`, `SC2156`, `SC2164`, `SC2294` | Dangerous removal patterns, unchecked `cd`, interpolation into shell code, and array arguments to `eval`. |
| `SC2059`, `SC2151`, `SC2152`, `SC2182`, `SC2183`, `SC2241`, `SC2242` | Dynamic printf formats, conversion counts, and invalid return/exit values. |
| `SC2003`, `SC2006`, `SC2007`, `SC2072`, `SC2079`, `SC2080`, `SC2219`, `SC2309` | Obsolete command/arithmetic syntax, unsupported decimals, octal mistakes, and text used numerically. |
| `SC2119`, `SC2120`, `SC2142`, `SC2213`, `SC2214`, `SC2218`, `SC2220`, `SC2221`, `SC2222`, `SC2262`, `SC2263`, `SC2317`, `SC2329` | Missing function arguments, aliases, option/case inconsistencies, definition order, and apparent unreachable/uncalled code. |

shfmt has option names rather than diagnostic IDs. The config selects `shell_variant=bash`, `indent_style=space`, `indent_size=2`, `binary_next_line=true`, `switch_case_indent=true`, `space_redirects=false`, `function_next_line=false`, and `keep_padding=false`. The `[[bash]]` section is a shfmt extension covering Bash shebangs, including extensionless files; ordinary editors need explicit filename globs. shfmt does not enforce an 80-column limit, naming, function-keyword choice, or discretionary expansion braces. [SHFMT]

Manual review covers script complexity; names; `main` structure; local declarations on every scratch variable; docs; the full no-`eval` policy; source-path trust; integer validation/overflow; exact error propagation; pipeline and asynchronous exit handling; cleanup ownership; libraries' caller state; test completeness; and actual Bash 5.2 compatibility. `SC2294` is not a blanket `eval` ban, `SC2186` does not require `mktemp` everywhere, and passing ShellCheck does not establish injection safety. [SHELLCHECK] [BASH-MANUAL]



## Naming

- PREFER `lower_snake_case` for Bash functions, ordinary variables, and source filenames, with `UPPER_SNAKE_CASE` for constants and exported environment variables. Why: casing distinguishes shell-local state from the environment contract. [GOOGLE-SHELL]
- PREFER a library-specific function prefix such as `files_read` when functions are sourced. Why: Bash libraries share one function namespace; the underscore spelling is a house departure from Google. [GOOGLE-SHELL] [BASH-MANUAL]
- MUST avoid repurposing special shell variables such as `PATH`, `IFS`, `HOME`, or `RANDOM` as application scratch storage. Why: assignment can silently change shell behavior. [SHELLCHECK] [BASH-MANUAL]

## Files and layout

- MUST give executable Bash scripts a Bash shebang and invoke them directly or with `bash`, never `sh`; prefer `#!/bin/bash` on this Linux baseline, using `#!/usr/bin/env bash` only with a controlled PATH resolving the required runtime. Why: the interpreter determines whether Bash syntax works. [GOOGLE-SHELL] [BASH-MANUAL] [SHELLCHECK]
- PREFER shell for short command wrappers; reconsider the language around 100 lines or when control flow or data structures become complicated. Why: shell scales poorly as an application language. [GOOGLE-SHELL]
- PREFER `.sh` for repository script sources and nonexecutable libraries, and extensionless installed commands. Why: source files and public command names serve different consumers. [GOOGLE-SHELL]
- MUST put executable flow in `main` when there are other functions, place its definition last, and finish with `main "$@"`. Why: shell definitions execute in order and argument forwarding must remain explicit. [GOOGLE-SHELL]
- PREFER constants, imports, and shell setup before function definitions, with application execution confined to the entry point. Why: top-level shell statements execute immediately. [GOOGLE-SHELL]
- PREFER defining functions with `name()` and omitting the `function` keyword. Why: one definition grammar is sufficient and remains recognizable across shell dialects. [GOOGLE-SHELL] [SHELLCHECK]
- MUST keep sourced libraries from changing caller options, traps, working directory, or IFS on load; explicitly scope any needed changes. Why: sourcing shares the caller's execution environment. [BASH-MANUAL]

## Types and data

- MUST double-quote data expansions in command arguments and redirections, including nested command substitutions; leave only intended pattern syntax unquoted. Why: unquoted expansion can split data or expand filenames. [GOOGLE-SHELL] [SHELLCHECK]
- MUST store argument lists in arrays and forward them with `"${args[@]}"` or `"$@"`. Why: a string cannot preserve empty arguments and argument boundaries. [GOOGLE-SHELL] [SHELLCHECK]
- MUST declare function scratch variables with `local`, and pass inputs explicitly instead of relying on a caller's locals. Why: Bash locals have dynamic scope and remain visible to called functions. [GOOGLE-SHELL] [BASH-MANUAL]
- MUST validate or default environment inputs and optional positional parameters before expansion, using forms such as `${INPUT:?message}` and `${1-}` deliberately. Why: unset and empty are distinct states, especially under nounset. [SHELLCHECK] [BASH-MANUAL]
- PREFER `readonly` for constants and `export` only for intended child-process inputs. Why: these builtins express separate immutability and environment contracts. [GOOGLE-SHELL]
- MUST use `[[ ... ]]` for Bash string/file tests, quote a literal equality operand on the right, and distinguish it from an intentional glob or regex. Why: test syntax changes expansion and matching behavior. [GOOGLE-SHELL] [SHELLCHECK]
- MUST express empty/nonempty checks with `-z`/`-n`, and use arithmetic comparisons for validated integers. Why: strings such as `false` and `0` are nonempty, not Boolean false. [GOOGLE-SHELL] [SHELLCHECK]
- PREFER a direct opposite comparison such as `!=` over negating equality. Why: one operator makes the condition easier to interpret. [SHELLCHECK]
- MUST use `IFS= read -r` for literal text lines and NUL-delimited records for arbitrary filenames. Why: whitespace, backslashes, and newlines can be data. [SHELLCHECK] [BASH-MANUAL]
- MUST handle the final unterminated text line when the input contract allows it, for example with `while IFS= read -r line || [[ -n "$line" ]]`. Why: `read` can assign text while returning failure at EOF. [BASH-MANUAL]
- MUST keep NUL-bearing data in files or streams and account for trailing-newline removal by `$(...)`. Why: shell variables and command capture are not byte-preserving binary containers. [BASH-MANUAL]

## Errors

- MUST test command status directly with `if command; then` or `if ! command; then`, rather than a later test of `$?`. Why: intervening commands can overwrite the result. [SHELLCHECK]
- MUST capture `$?` immediately in the `else` branch of an unnegated command test when its exact failure status matters. Why: logging and `!` replace that status. [SHELLCHECK]
- MUST separate `local`, `readonly`, or `export` declarations from assignments that capture command output. Why: declaration builtins can mask a failed substitution. [GOOGLE-SHELL] [SHELLCHECK]
- MUST handle fallible commands inside functions explicitly even when callers enable `set -e`. Why: condition-invoked functions and command substitutions can suppress errexit. [SHELLCHECK] [BASH-MANUAL]
- PREFER explicit status handling with `set -u -o pipefail` in standalone scripts; add `errexit` only as a tested extra guard. Why: nounset and pipefail expose common mistakes while errexit has context-dependent exceptions. [SHELLCHECK] [BASH-MANUAL]
- MUST check meaningful pipeline failures with `pipefail` or an immediately saved `PIPESTATUS` array, and account for consumers that close the pipe early. Why: the final command alone can hide upstream failure or SIGPIPE. [GOOGLE-SHELL] [BASH-MANUAL]
- MUST distinguish a command's documented negative-result status from execution failure, such as `grep` status 1 versus 2. Why: treating every nonzero result as absence conceals operational errors. [GOOGLE-SHELL] [BASH-MANUAL]
- MUST use `return` for library/function failures, reserve `exit` for the executable boundary, and send diagnostics to stderr. Why: sourcing executes inside the caller and stdout may carry data. [GOOGLE-SHELL] [BASH-MANUAL]
- MUST include a fallback in `case` statements and reject invalid CLI options explicitly. Why: an unmatched input otherwise silently performs no branch. [SHELLCHECK]
- MUST allocate temporary paths with `mktemp`, check creation, and arrange `EXIT` cleanup that preserves the original failure status. Why: predictable names and cleanup that hides failure make shell workflows unsafe. [SHELLCHECK] [BASH-MANUAL]
- MUST register cleanup as a function or literal trap command, keep referenced state alive until it runs, and define INT/TERM behavior when cleanup depends on orderly exit. Why: early interpolation, expired function locals, and signal exits can invalidate cleanup; SIGKILL cannot be trapped. [SHELLCHECK] [BASH-MANUAL]

Capturing output and the original failure status, without a masked declaration:

```bash
read_version() {
  local version status
  if version=$(tool --version); then
    printf '%s\n' "$version"
  else
    status=$?
    printf 'tool --version failed (status %s)\n' "$status" >&2
    return "$status"
  fi
}
```

## Comments and docs

- MUST document every library function and nontrivial script function with its arguments, globals read/changed, stdin/stdout/stderr use, and meaningful statuses. Why: shell has no signature syntax for these interfaces. [GOOGLE-SHELL]
- PREFER a brief file header identifying executable versus sourced use, required Bash version, and external commands. Why: a useful header exposes shell dependencies; making it optional departs from Google. [GOOGLE-SHELL] [BASH-MANUAL]

## Testing

- MUST test Bash scripts with empty, spaced, wildcard, newline, and dash-leading arguments, plus command failures and distinct stdout/stderr expectations. Why: ordinary-looking input misses shell expansion and status bugs. [SHELLCHECK] [BASH-MANUAL]
- MUST test scripts on their declared minimum Bash and required utility variants, including sourced-library behavior under caller options. Why: a newer interpreter and ShellCheck cannot establish older-runtime or GNU/BSD compatibility. [BASH-MANUAL] [SHELLCHECK-MANUAL]
- MUST test cleanup on successful completion, failure, and supported interruption paths when the script owns temporary resources. Why: traps and signal handling execute outside the normal path. [BASH-MANUAL]
- MUST compare NUL-delimited or exact-byte output through files or byte-aware tools rather than command substitution. Why: Bash cannot retain NUL bytes and strips trailing newlines in captures. [BASH-MANUAL]

## Performance

- PREFER Bash builtins and parameter expansion for simple string/length operations, and `command -v` once per required command for availability checks. Why: these avoid unnecessary processes and use the shell's actual command lookup. [GOOGLE-SHELL] [SHELLCHECK]
- PREFER direct file arguments or input redirection over an unnecessary `cat` pipeline, and batched external tools over one subprocess per record. Why: process startup can dominate small shell operations. [GOOGLE-SHELL] [SHELLCHECK]

## Security

- MUST avoid `eval` in owned Bash code; use arrays, explicit dispatch, or validated Bash indirection. Why: reevaluating strings destroys the separation between data and shell syntax. [GOOGLE-SHELL] [SHELLCHECK]
- MUST source only trusted code from known locations; pass values as positional arguments to a fixed `bash -c` program instead of interpolating them into its text. Why: both sourcing and command-string execution parse shell code. [SHELLCHECK] [BASH-MANUAL]
- MUST pass data to a fixed `printf` format, such as `printf '%s\n' "$value"`. Why: data used as the format can interpret percent sequences and escapes. [SHELLCHECK]
- MUST protect filename operands with `--` where supported and explicit paths such as `./` for globs or commands without an option terminator. Why: quoting alone does not stop dash-leading names from becoming options. [GOOGLE-SHELL] [SHELLCHECK]
- MUST validate external numbers as bounded decimal digits before arithmetic or indexed-array use; apply `10#` only after validation when leading zeros are allowed. Why: Bash evaluates arithmetic expressions recursively and leading zero means octal. [BASH-MANUAL] [SHELLCHECK]
- MUST guard `cd` before dependent commands and check a destructive target's nonempty value and intended location before removal. Why: a failed directory change or empty path can redirect an operation. [SHELLCHECK]
- MUST avoid SUID/SGID shell scripts and keep `set -x` off around sensitive operations. Why: shell privilege and argument tracing expose execution context and expanded values. [GOOGLE-SHELL] [BASH-MANUAL]

## Language-specific pitfalls

- MUST iterate filenames with guarded globs, arrays, `find -exec`, or NUL-delimited streams, never parsed `ls` output or `for item in $(command)`. Why: display text and word splitting cannot preserve filenames. [SHELLCHECK]
- MUST handle unmatched globs deliberately, with a per-result existence guard or scoped `nullglob`/`failglob`. Why: the default leaves an unmatched pattern as a literal filename. [SHELLCHECK] [BASH-MANUAL]
- MUST redirect input into loops whose assignments must survive; separately collect failures from process substitutions or background jobs. Why: pipeline loops can run in subshells and asynchronous failures do not become the consumer's status. [GOOGLE-SHELL] [BASH-MANUAL] [SHELLCHECK]
- MUST save each background PID and inspect its `wait` result when its success matters. Why: bare `wait` reports zero after all jobs and does not aggregate their failures. [BASH-MANUAL]
- PREFER a checked temporary-file producer followed by a redirected consumer when a process-substitution producer's failure matters. Why: this makes both statuses explicit without asynchronous descriptor management. [SHELLCHECK] [BASH-MANUAL]
- MUST use `$(...)` for command capture and `$((...))` or `((...))` for integer arithmetic rather than backticks, `expr`, `let`, or `$[...]`. Why: supported syntax has clearer expansion and nesting rules. [GOOGLE-SHELL] [SHELLCHECK]
- MUST account for arithmetic-command status when enabling errexit; use `count=$((count + 1))` for an unconditional increment. Why: `((count++))` returns failure when its previous value was zero. [GOOGLE-SHELL] [BASH-MANUAL]
- MUST use `if` for true success/failure branches instead of assuming `first && second || third` is an if/else expression. Why: failure in `second` also runs `third`. [SHELLCHECK]
- PREFER functions over aliases in scripts. Why: alias expansion happens while parsing and cannot express ordinary positional-argument interfaces. [GOOGLE-SHELL] [SHELLCHECK]
- MUST avoid reading a file in a pipeline that simultaneously redirects output back to that file. Why: the shell can truncate the input before the reader opens it. [SHELLCHECK]

## Where the sources disagree

Where Google and ShellCheck differ, the house picks below apply. Additional house choices on file headers and library names follow.

- MUST test command status directly, choosing ShellCheck SC2181 over Google's allowance for an immediate separate `$?` test; capture a needed numeric status immediately inside an unnegated test's failure branch. Why: the check remains attached to the operation and lint catches the fragile alternative. [GOOGLE-SHELL] [SHELLCHECK]
- PREFER surrounding variable bracing in existing code and `"$var"` in new files unless braces are required, leaving SC2250 off; this follows Google's consistency priority but departs from its new-code `"${var}"` preference. Why: braces alone do not prevent splitting and the formatter owns mechanical style. [GOOGLE-SHELL] [SHELLCHECK]
- MUST avoid `eval` in owned Bash code, adopting Google's avoidance over the wiki's conditional POSIX indirection alternatives in SC1067/SC2271/SC2298; SC1067 is historical and removed. Why: Bash arrays and validated indirection remove that portability justification. [GOOGLE-SHELL] [SHELLCHECK]
- MUST use the Bash dialect for this guide, adopting Google's Bash baseline while applying the wiki's SC3001/SC3010/SC3030 restrictions only to separately declared `sh` code. Why: these are interpreter constraints, not a disagreement about valid Bash. [GOOGLE-SHELL] [SHELLCHECK]
- PREFER `name()` definitions without `function`, narrowing Google's optional keyword while respecting the wiki's Ksh SC2111 and sh SC2112/SC2113 constraints as dialect-specific. Why: one simple house form is sufficient; those diagnostics do not enforce this preference in Bash. [GOOGLE-SHELL] [SHELLCHECK]

- PREFER a brief file header when it adds deployment or usage context, departing from Google's mandatory header on every file. Why: a trivial helper should not need a comment that only repeats its filename. [GOOGLE-SHELL] [BASH-MANUAL]
- PREFER underscore-separated library prefixes such as `files_read` over Google's `files::read`. Why: one lower_snake_case naming scheme keeps functions recognizable to ordinary shell and editor tooling. [GOOGLE-SHELL] [BASH-MANUAL]
