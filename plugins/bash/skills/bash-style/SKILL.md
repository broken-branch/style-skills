---
name: bash-style
description: "Write, edit, or review .sh and Bash scripts using house Bash style unless another guide is requested."
license: CC-BY-4.0
metadata:
  kind: house
  language: bash
  version: "1.0.0"
  source-url: "references/sources.md"
  treatment: original-synthesis
---

# Bash style (house)

Our blend of the best Bash guides, in our own words. Every rule in the full guide names its source.

Scope: owned, noninteractive Bash scripts and sourced libraries on Linux, using Bash 5.2-compatible syntax and explicitly declared external utilities. Validation uses Bash 5.3.20. POSIX `sh`, interactive startup files, and macOS's system Bash 3.2 need separate profiles.

If the project declares older versions or its own formatter/linter settings, follow the project and say so.

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

## When to read more

- Before a change bigger than one function, read [references/guide.md](references/guide.md), the section for what you're doing.
- For naming basics, errors, tests, commits, secrets, and agent workflow, read [references/shared.md](references/shared.md).
- To set up tooling, copy or merge the files in [references/config/](references/config/) into your repository, then read the guide's Tooling section. Use the project's own source files and test fixtures.
- For worked controls, read [argument parsing and quoting](references/examples/render_args.sh), [negative results and failures](references/examples/match_lines.sh), [temporary-file cleanup](references/examples/sort_lines.sh).

## Sources

See [references/sources.md](references/sources.md) for sources, licenses, source tags, and changes. Unofficial: not affiliated with or endorsed by any source's owner.
