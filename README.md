# style-skills

Coding and house UI design guides for Claude Code and Codex. For each language, choose a house style that combines the main guides, or select a source guide on its own.

The collection has 14 house skills that agents can select automatically and 32 source skills that run when invoked by name. Four source skills link to the original guide without including its text.

## Install

Choose either `house-style` or the language/design plugins. Installing both duplicates the house skills.

The commands below passed with a local repository path; installation from the published remote has not yet been tested.

Claude Code, a whole language:

```text
/plugin marketplace add broken-branch/style-skills
/plugin install go@style-skills
```

For house style in every language, use `/plugin install house-style@style-skills` instead of the language plugin.

Codex, a whole language:

```sh
codex plugin marketplace add broken-branch/style-skills
codex plugin add go@style-skills
```

For house style in every language, use `codex plugin add house-style@style-skills` instead.

One skill, in either tool:

```sh
npx skills add broken-branch/style-skills --skill go-style -a claude-code -a codex
```

Add `-g` to install for your user instead of this project. Or copy a folder from `skills/` into `~/.claude/skills/` (Claude Code) or `~/.agents/skills/` (Codex).

Available plugins: `house-style`, `rust`, `go`, `cpp`, `typescript`, `react`, `vue`, `html`, `css`, `python`, `bash`, `powershell`, `sql`, and `design`. Language plugins include their house skill and source guides. The `design` plugin contains only `design-style`; it is also included in `house-style`. Coding skills bundle shared coding rules; the design skill bundles visual and component contracts.

## Use

Use `design-style` for house UI appearance and interaction behavior. It complements language coding conventions and respects an existing project design system. Its three provisional defaults are marked in the skill. The new design skill has static packaging checks only; no model-selection result is claimed.

- Write code normally to let the agent select the language's house skill. Automatic selection is model-dependent; see [load results](tests/load/RESULTS.md).
- Type `/go-uber-style` in Claude Code (or `/go:go-uber-style` for the plugin) or `$go-uber-style` in Codex to select a source guide for the task. Plain words such as “use Uber's Go style” do not reliably load a source skill.

## Skills

<!-- BEGIN GENERATED SKILLS -->
| Language | Skill | Based on | License |
| --- | --- | --- | --- |
| all | [code-style](skills/code-style/SKILL.md) | Google Engineering Practices, EditorConfig, Conventional Commits, Semantic Versioning, Google developer documentation style guide, OWASP Cheat Sheet Series, C++ Core Guidelines, Effective Rust, Uber Go Style Guide, Google Go Style Guide, Google Python Style Guide, Ruff rules | CC-BY-4.0 |
| rust | [rust-style](skills/rust-style/SKILL.md) | Rust Style Guide, Rust API Guidelines, Google Rust Style Guide, Microsoft Pragmatic Rust Guidelines, Effective Rust, Clippy lint list | CC-BY-4.0 |
| go | [go-style](skills/go-style/SKILL.md) | Effective Go, Go Code Review Comments, Google Go Style Guide, Uber Go Style Guide, golangci-lint docs | CC-BY-4.0 |
| cpp | [cpp-style](skills/cpp-style/SKILL.md) | Google C++ Style Guide, Chromium C++ style, C++ Core Guidelines, clang-tidy checks | CC-BY-4.0 |
| typescript | [typescript-style](skills/typescript-style/SKILL.md) | Google TS/JS Style Guide (formerly the Google TypeScript Style Guide), Node.js Best Practices, TypeScript TSConfig reference, typescript-eslint shared configs, NestJS documentation, OWASP Cheat Sheet Series | CC-BY-4.0 |
| react | [react-style](skills/react-style/SKILL.md) | Rules of React, You Might Not Need an Effect, Airbnb React/JSX Style Guide, Bulletproof React, Node.js Best Practices, Google TS/JS Style Guide (formerly the Google TypeScript Style Guide), OWASP Cheat Sheet Series, TypeScript TSConfig reference, typescript-eslint shared configs, WCAG 2.2 Recommendation and quick reference | CC-BY-4.0 |
| vue | [vue-style](skills/vue-style/SKILL.md) | Vue Style Guide, eslint-plugin-vue, TypeScript TSConfig reference, typescript-eslint shared configs, WCAG 2.2 Recommendation and quick reference | CC-BY-4.0 |
| html | [html-style](skills/html-style/SKILL.md) | Google HTML/CSS Style Guide, web.dev Learn HTML, WCAG 2.2 Recommendation and quick reference, MDN accessibility guides, Google developer documentation style guide, OWASP Cheat Sheet Series, web.dev Learn CSS | CC-BY-4.0 |
| css | [css-style](skills/css-style/SKILL.md) | Google HTML/CSS Style Guide, Guidelines for writing CSS code examples, CUBE CSS, web.dev Learn CSS, stylelint-config-standard, OWASP Cheat Sheet Series, WCAG 2.2 Recommendation and quick reference | CC-BY-4.0 |
| python | [python-style](skills/python-style/SKILL.md) | PEP 8, PEP 257, Google Python Style Guide, Ruff rules | CC-BY-4.0 |
| bash | [bash-style](skills/bash-style/SKILL.md) | Google Shell Style Guide, ShellCheck wiki | CC-BY-4.0 |
| powershell | [powershell-style](skills/powershell-style/SKILL.md) | PowerShell Practice and Style, Strongly Encouraged Development Guidelines for PowerShell cmdlets, Microsoft Learn PSScriptAnalyzer documentation | CC-BY-4.0 |
| sql | [sql-style](skills/sql-style/SKILL.md) | SQL Style Guide, GitLab SQL style guide, PostgreSQL wiki Don't Do This, SQLFluff rules | CC-BY-4.0 |
| design | [design-style](skills/design-style/SKILL.md) | Original house visual rules; WCAG 2.2 reference | CC-BY-4.0 |
| rust | [rust-official-style](skills/rust-official-style/SKILL.md) | Rust Style Guide | MIT OR Apache-2.0 |
| rust | [rust-api-style](skills/rust-api-style/SKILL.md) | Rust API Guidelines | MIT OR Apache-2.0 |
| rust | [rust-google-style](skills/rust-google-style/SKILL.md) | Google Rust Style Guide | CC-BY-3.0 |
| rust | [rust-microsoft-style](skills/rust-microsoft-style/SKILL.md) | Microsoft Pragmatic Rust Guidelines | MIT |
| rust | [rust-effective-style](skills/rust-effective-style/SKILL.md) | Effective Rust | CC-BY-4.0 (our pointer text only; guide not included) |
| go | [go-official-style](skills/go-official-style/SKILL.md) | Effective Go | CC-BY-4.0 |
| go | [go-review-style](skills/go-review-style/SKILL.md) | Go Code Review Comments | CC-BY-4.0 |
| go | [go-google-style](skills/go-google-style/SKILL.md) | Google Go Style Guide | CC-BY-3.0 |
| go | [go-uber-style](skills/go-uber-style/SKILL.md) | Uber Go Style Guide | Apache-2.0 |
| cpp | [cpp-google-style](skills/cpp-google-style/SKILL.md) | Google C++ Style Guide | CC-BY-3.0 |
| cpp | [cpp-chromium-style](skills/cpp-chromium-style/SKILL.md) | Chromium C++ style, Google C++ Style Guide | BSD-3-Clause AND CC-BY-3.0 |
| cpp | [cpp-core-guidelines-style](skills/cpp-core-guidelines-style/SKILL.md) | C++ Core Guidelines | CC-BY-4.0 (our pointer text only; guide not included) |
| typescript | [typescript-google-style](skills/typescript-google-style/SKILL.md) | Google TS/JS Style Guide (formerly the Google TypeScript Style Guide) | CC-BY-3.0 |
| typescript | [typescript-node-best-practices-style](skills/typescript-node-best-practices-style/SKILL.md) | Node.js Best Practices | CC-BY-SA-4.0 |
| react | [react-official-style](skills/react-official-style/SKILL.md) | Rules of React | CC-BY-4.0 |
| react | [react-effects-style](skills/react-effects-style/SKILL.md) | You Might Not Need an Effect | CC-BY-4.0 |
| react | [react-airbnb-style](skills/react-airbnb-style/SKILL.md) | Airbnb React/JSX Style Guide | MIT |
| react | [react-bulletproof-style](skills/react-bulletproof-style/SKILL.md) | Bulletproof React | MIT |
| vue | [vue-official-style](skills/vue-official-style/SKILL.md) | Vue Style Guide | CC-BY-4.0 |
| html | [html-google-style](skills/html-google-style/SKILL.md) | Google HTML/CSS Style Guide | CC-BY-3.0 |
| css | [css-google-style](skills/css-google-style/SKILL.md) | Google HTML/CSS Style Guide | CC-BY-3.0 |
| css | [css-mdn-style](skills/css-mdn-style/SKILL.md) | Guidelines for writing CSS code examples | CC-BY-SA-4.0 |
| css | [css-cube-style](skills/css-cube-style/SKILL.md) | CUBE CSS | CC-BY-4.0 (our pointer text only; guide not included) |
| python | [python-pep8-style](skills/python-pep8-style/SKILL.md) | PEP 8 | LicenseRef-Public-Domain-PEP |
| python | [python-pep257-style](skills/python-pep257-style/SKILL.md) | PEP 257 | LicenseRef-Public-Domain-PEP |
| python | [python-google-style](skills/python-google-style/SKILL.md) | Google Python Style Guide | CC-BY-3.0 |
| bash | [bash-google-style](skills/bash-google-style/SKILL.md) | Google Shell Style Guide | CC-BY-3.0 |
| bash | [bash-omarchy-style](skills/bash-omarchy-style/SKILL.md) | Omarchy AGENTS.md Style section and .editorconfig | MIT |
| powershell | [powershell-poshcode-style](skills/powershell-poshcode-style/SKILL.md) | PowerShell Practice and Style | CC-BY-SA-4.0 |
| powershell | [powershell-microsoft-style](skills/powershell-microsoft-style/SKILL.md) | Strongly Encouraged Development Guidelines for PowerShell cmdlets | CC-BY-4.0 |
| sql | [sql-holywell-style](skills/sql-holywell-style/SKILL.md) | SQL Style Guide | CC-BY-SA-4.0 |
| sql | [sql-gitlab-style](skills/sql-gitlab-style/SKILL.md) | GitLab SQL style guide | CC-BY-4.0 (our pointer text only; guide not included) |
<!-- END GENERATED SKILLS -->

## Licenses

House skill text is CC BY 4.0. Source skills retain their applicable source licenses. See each skill's LICENSE file, [CREDITS.md](CREDITS.md), and [LICENSING.md](LICENSING.md). Tools and configs are MIT.

All skills are unofficial and unendorsed. The CC BY 4.0 license in a link-only skill covers its own pointer text; the original guide is not included.
