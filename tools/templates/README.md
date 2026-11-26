# style-skills

Coding and house UI design guides for Claude Code and Codex. For each language, choose a house style that combines the main guides, or select a source guide on its own.

The collection has {house_count} house skills that agents can select automatically and {source_count} source skills that run when invoked by name. Four source skills link to the original guide without including its text.

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

<!-- table made by tools/build.py: language, skill, based on, license -->

## Licenses

House skill text is CC BY 4.0. Source skills retain their applicable source licenses. See each skill's LICENSE file, [CREDITS.md](CREDITS.md), and [LICENSING.md](LICENSING.md). Tools and configs are MIT.

All skills are unofficial and unendorsed. The CC BY 4.0 license in a link-only skill covers its own pointer text; the original guide is not included.
