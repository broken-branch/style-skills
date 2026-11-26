# Omarchy Bash rules

Restated from the AGENTS.md Style section and `.editorconfig` at commit `abe42d9c`. Examples and the install/migration layout rule are omitted; other AGENTS.md sections are outside this skill’s scope.

Source owner: David Heinemeier Hansson and Omarchy contributors. License: [MIT](../LICENSE), including the upstream copyright notice. Changes by style-skills contributors: style rules independently restated and shortened; examples and repository-specific instructions omitted. Unofficial; no endorsement is implied.

## Tooling

- Make the project's root EditorConfig the boundary for inherited editor settings with `root = true`. — [Omarchy: .editorconfig, root](https://github.com/omacom/omarchy/blob/abe42d9c81af6c6839548a039064c79d19abf93c/.editorconfig). <!-- omarchy-editorconfig:root -->
- Use spaces for indentation under the all-files EditorConfig policy. — [Omarchy: .editorconfig, indent_style](https://github.com/omacom/omarchy/blob/abe42d9c81af6c6839548a039064c79d19abf93c/.editorconfig). <!-- omarchy-editorconfig:indent_style -->
- Set the all-files indentation width to two spaces. — [Omarchy: .editorconfig, indent_size](https://github.com/omacom/omarchy/blob/abe42d9c81af6c6839548a039064c79d19abf93c/.editorconfig). <!-- omarchy-editorconfig:indent_size -->
- End each text file with a newline. — [Omarchy: .editorconfig, insert_final_newline](https://github.com/omacom/omarchy/blob/abe42d9c81af6c6839548a039064c79d19abf93c/.editorconfig). <!-- omarchy-editorconfig:insert_final_newline -->
- Remove whitespace left at the ends of lines. — [Omarchy: .editorconfig, trim_trailing_whitespace](https://github.com/omacom/omarchy/blob/abe42d9c81af6c6839548a039064c79d19abf93c/.editorconfig). <!-- omarchy-editorconfig:trim_trailing_whitespace -->
- Store line endings as LF. — [Omarchy: .editorconfig, end_of_line](https://github.com/omacom/omarchy/blob/abe42d9c81af6c6839548a039064c79d19abf93c/.editorconfig). <!-- omarchy-editorconfig:end_of_line -->
- Encode text files in UTF-8. — [Omarchy: .editorconfig, charset](https://github.com/omacom/omarchy/blob/abe42d9c81af6c6839548a039064c79d19abf93c/.editorconfig). <!-- omarchy-editorconfig:charset -->
- Indent with two spaces; do not use tabs. — [Omarchy: Style](https://github.com/omacom/omarchy/blob/abe42d9c81af6c6839548a039064c79d19abf93c/AGENTS.md#style). <!-- omarchy-style:2 -->

## Files and layout

- Start executable shebangs with `#!/bin/bash`; never use `#!/usr/bin/env bash`. The narrowly scoped privileged-mode exception below still applies. — [Omarchy: Style](https://github.com/omacom/omarchy/blob/abe42d9c81af6c6839548a039064c79d19abf93c/AGENTS.md#style). <!-- omarchy-style:8a -->

## Types and data

- Target Bash 5 conditional syntax: `[[ … ]]` for file and string checks, and `(( … ))` for numeric checks. — [Omarchy: Style](https://github.com/omacom/omarchy/blob/abe42d9c81af6c6839548a039064c79d19abf93c/AGENTS.md#style). <!-- omarchy-style:3 -->
- Within `[[ … ]]`, leave variable expansions unquoted and quote string literals used for value comparisons. — [Omarchy: Style](https://github.com/omacom/omarchy/blob/abe42d9c81af6c6839548a039064c79d19abf93c/AGENTS.md#style). <!-- omarchy-style:4 -->
- Prefer an arithmetic conditional to numeric comparison operators inside double brackets. — [Omarchy: Style](https://github.com/omacom/omarchy/blob/abe42d9c81af6c6839548a039064c79d19abf93c/AGENTS.md#style). <!-- omarchy-style:5 -->
- Protect strings and paths containing spaces with quotes instead of backslash-escaping each space. — [Omarchy: Style](https://github.com/omacom/omarchy/blob/abe42d9c81af6c6839548a039064c79d19abf93c/AGENTS.md#style). <!-- omarchy-style:7 -->

## Comments and docs

- In Markdown documentation, break lines at structural boundaries such as headings and list entries instead of hard-wrapping prose at 80 columns. — [Omarchy: Style](https://github.com/omacom/omarchy/blob/abe42d9c81af6c6839548a039064c79d19abf93c/AGENTS.md#style). <!-- omarchy-style:1 -->

## Testing

The regression requirement for the privileged-mode exception appears under Security.

## Security

- Use `#!/bin/bash -p` only at a security-sensitive entrypoint that must block `BASH_ENV` and exported-function injection before any command; document the boundary and add a regression test rejecting an ordinary Bash invocation with a misleading script argument of `-p`. — [Omarchy: Style](https://github.com/omacom/omarchy/blob/abe42d9c81af6c6839548a039064c79d19abf93c/AGENTS.md#style). <!-- omarchy-style:8b -->

## Language-specific pitfalls

- For a simple two-way decision, prefer an explicit `if`/`else` structure over leaving the second path after a branch that calls `exec` or `exit`. — [Omarchy: Style](https://github.com/omacom/omarchy/blob/abe42d9c81af6c6839548a039064c79d19abf93c/AGENTS.md#style). <!-- omarchy-style:6 -->

## Where the sources disagree

The selected Style section and EditorConfig agree on indentation; no unresolved conflict occurs within this adaptation.

## Original worked examples

Original code under this skill's license: [test quoting and explicit alternatives](examples/choose_label.sh), [path tests and quoted output](examples/path_kind.sh).
