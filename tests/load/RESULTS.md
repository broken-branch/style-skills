# Load test results

> Historical record: these results are from `95af068` (41 skills, 13 plugins). The release tree has 46 skills and 14 plugins; `tests/load/check_entrypoints.py` covers the current packaging, and a Claude Code plugin load (`rust:rust-style`) passed on 2026-11-17.

Run on 2026-10-31 with Claude Code 2.1.312 and codex-cli 0.165.0, against the working tree at `95af068`. Claude model checks used `claude-sonnet-5-5`; Codex used its configured model with `model_reasoning_effort="low"`.

## How this was run

A scratch HOME has no sign-in for either tool, and existing credentials were not copied. So:

- **Install routes** ran with `HOME`, `CLAUDE_CONFIG_DIR` and `CODEX_HOME` pointing into a fresh `mktemp -d` folder. No model was called there. Each check covers what can be seen without a model: the command succeeds, the files land where the README says, `claude plugin list` / `claude plugin details`, and `codex plugin list`. For Codex, `codex debug prompt-input` also shows the exact skill list the model would get, again with no model call.
- **Model checks** ran in scratch projects under `<work>/proj-*`, using the real sign-in. Claude Code loaded the plugins with `claude -p --plugin-dir plugins/<name>` and the single-skill routes from project copies in `.claude/skills/`. Codex loaded project copies from `.agents/skills/` with `codex exec -s read-only -C <proj>`. These are the project-level equivalents of the user-level routes; model loading for the user-level routes was not tested directly.
- **Detecting which skill loaded.** Claude Code: the session transcript records `Base directory for this skill: …` for both Skill tool loads and expanded slash commands, and Read/Bash calls show any file opened under a skill folder. Codex: `--json` command events show a `SKILL.md` or `references/` file being read, and the session rollout shows `<skill><name>…` injected for `$name` mentions.
- Nothing was installed into `~/.claude`, `~/.codex` or `~/.agents`. All scratch HOMEs were removed.

`/skills` is interactive in both tools, so the listing check used each tool's non-interactive view instead. For Claude Code that is the `skills` field of the `-p` init event, plus `claude plugin list` / `details`. For Codex it is `codex debug prompt-input`.

## Summary

| Area | Claude Code | Codex |
| --- | --- | --- |
| Plugin marketplace from local path (go, house-style) | pass | pass (CLI `codex plugin add`; no `.agents/plugins/marketplace.json` needed) |
| `npx skills add <local path> -g` | pass | pass |
| Folder copy | pass | pass |
| `$skill-installer` with a local path | n/a | **fail**: GitHub URLs only |
| Listing | pass | pass |
| Default: house skill loads, source skill doesn't (Go, Python) | pass | pass |
| Named with `/…` or `$…` | pass | pass |
| Named in plain words ("Use Uber's Go style") | **fail** (by design, see below) | **fail** (by design) |
| code-style when writing a commit message | pass (4 of 4 after the description change; 0 of 5 before) | pass |
| Many installed: descriptions not cut | pass (41 project skills) | pass (41 flat skills + 13 plugins, 42 skills in the list) |

## Failures and what worked instead

1. **`$skill-installer` does not take a local path.** Its script (`install-skill-from-github.py`) accepts only `--repo owner/repo` or a `github.com` URL. `--url file://…` fails with "Only GitHub URLs are supported for download mode." The README's GitHub URL form cannot be tested until a remote exists. What worked instead: `npx skills add <path> -g`, or copying the folder into `~/.agents/skills/`.
2. **A source guide named in plain words doesn't load, in either tool.** "Use Uber's Go style." and "Use Google's Python style." load nothing in Claude Code. In Codex they load the house skill (`go-style` / `python-style`). This follows from the source skills' own metadata: `disable-model-invocation: true` (Claude Code) and `allow_implicit_invocation: false` (Codex) remove them from the list the model chooses from. The README only promises selection by `/go:go-uber-style` or `$go-uber-style`, and both of those pass. Plain-word selection is not supported by these explicit-only settings.
3. **Claude Code does not load code-style for a commit message.** The prompt "Write a commit message for the staged change" loaded no skill in 5 of 5 runs: twice in the scripted check (once through the house-style plugin, once through project copies), plus 3 repeats through the house-style plugin, one of which asked it to commit. Codex loaded code-style on the first try. The description, "Write, edit, or review source files (.rs, .go, .py, .ts), tests, and commits using shared house rules.", leads with source files and ends with "commits". A description that names commit messages up front would probably fix this; that is not tested.

### README install steps

| README step | Result | What worked |
| --- | --- | --- |
| `/plugin marketplace add <owner>/style-skills`, `/plugin install go@style-skills` | Works from a local path. | `claude plugin marketplace add /path/to/style-skills`, then `claude plugin install go@style-skills` and `claude plugin install house-style@style-skills` |
| `codex plugin marketplace add <owner>/style-skills`, then `codex plugin add go@style-skills` | Works from a local path, entirely in the CLI. | `codex plugin marketplace add /path/to/style-skills`, then `codex plugin add go@style-skills` and `codex plugin add house-style@style-skills`. Codex reads `.claude-plugin/marketplace.json` and the bundles' `.claude-plugin/plugin.json`, and copies them to `$CODEX_HOME/plugins/cache/style-skills/<plugin>/1.0.0/`. It needs no `.agents/plugins/marketplace.json` and no `.codex-plugin/` manifest. |
| `npx skills add <owner>/style-skills --skill go-style -a claude-code -a codex` | Works with a local path. Without `-g` it installs into the current project; with `-g` it writes to `~/.agents/skills/go-style` and symlinks `~/.claude/skills/go-style` to it. | `npx -y skills add /path/to/style-skills --skill go-style -a claude-code -a codex -g -y` |
| `$skill-installer install https://github.com/<owner>/…/skills/go-style` | Not testable without a remote; a local path fails (failure 1). | `npx skills add` or a folder copy |
| Copy a folder into `~/.claude/skills/` or `~/.agents/skills/` | Works. | `cp -r skills/python-style ~/.agents/skills/` (Codex lists it); same for `~/.claude/skills/` |

### Other observations

- **Duplicate house skills.** Installing `go` and `house-style` together gives two copies of go-style in both tools: `go:go-style` and `house-style:go-style`. With all 13 plugins installed, Codex listed 38 style entries (13 flat, 13 house-style, 12 per-language). Nothing broke, but the README could say to install either `house-style` or the language plugins.
- **Claude Code short names.** In Claude Code, `/go-uber-style` without the plugin prefix also worked for the plugin copy.
- **Token cost.** `claude plugin details go` reports about 122 always-on tokens for the go plugin.
- **Codex reads extra skills.** Codex often read code-style alongside the language skill. That is harmless and does not count against the default check.
- **No injected instructions.** No guide or reference file tried to give instructions during these runs.

## All rows

Claude Code (`tests/load/claude_load.py`):

| Route | Check | Result | Command | Saw |
| --- | --- | --- | --- | --- |
| marketplace | install | pass | `claude plugin marketplace add <repo>` | Successfully added marketplace: style-skills |
| plugin go | install | pass | `claude plugin install go@style-skills` | Successfully installed plugin: go@style-skills (scope: user) |
| plugin house-style | install | pass | `claude plugin install house-style@style-skills` | Successfully installed plugin: house-style@style-skills (scope: user) |
| plugin go + house-style | plugin list | pass | `claude plugin list` | both enabled, read from `plugins/go` and `plugins/house-style` |
| plugin go | plugin details | pass | `claude plugin details go` | Skills (4) go-google-style, go-official-style, go-style, go-uber-style |
| plugin house-style | plugin details | pass | `claude plugin details house-style` | Skills (13) bash-style … vue-style |
| npx skills add -g | install | pass | `npx -y skills add <repo> --skill go-style -a claude-code -a codex -g -y` | `~/.claude/skills/go-style -> ../../.agents/skills/go-style` |
| folder copy | install | pass | `cp -r skills/python-style ~/.claude/skills/` | SKILL.md, references/, agents/ in place |
| plugin go (--plugin-dir) | listing | pass | `claude -p --plugin-dir plugins/go` (init event) | go:go-google-style, go:go-official-style, go:go-style, go:go-uber-style |
| plugin go (--plugin-dir) | default Go | pass | `claude -p "Write a small Go function Reverse…" --plugin-dir plugins/go` | loaded: go-style |
| plugin go (--plugin-dir) | named: Uber in words | fail | `claude -p "Use Uber's Go style. Write…" --plugin-dir plugins/go` | loaded: none |
| plugin go (--plugin-dir) | named: /go:go-uber-style | pass | `claude -p "/go:go-uber-style Write…" --plugin-dir plugins/go` | loaded: go-uber-style |
| plugin go (--plugin-dir) | named: /go-uber-style | pass | `claude -p "/go-uber-style Write…" --plugin-dir plugins/go` | loaded: go-uber-style |
| plugin house-style (--plugin-dir) | default Go | pass | `claude -p "Write a small Go function…" --plugin-dir plugins/house-style` | loaded: go-style |
| project skills (npx/copy equivalent) | default Go | pass | `claude -p "Write a small Go function…"` | loaded: go-style |
| project skills (npx/copy equivalent) | named: Uber in words | fail | `claude -p "Use Uber's Go style. Write…"` | loaded: none |
| project skills (npx/copy equivalent) | named: /go-uber-style | pass | `claude -p "/go-uber-style Write…"` | loaded: go-uber-style |
| plugin python (--plugin-dir) | default Python | pass | `claude -p "Write a small Python function slugify…" --plugin-dir plugins/python` | loaded: python-style |
| plugin python (--plugin-dir) | named: Google's Python in words | fail | `claude -p "Use Google's Python style. Write…" --plugin-dir plugins/python` | loaded: none |
| plugin python (--plugin-dir) | named: /python:python-google-style | pass | `claude -p "/python:python-google-style Write…" --plugin-dir plugins/python` | loaded: python-google-style |
| plugin house-style (--plugin-dir) | commit message: code-style | fail | `claude -p "Write a commit message for the staged change…" --plugin-dir plugins/house-style` | loaded: none (3 more repeats: none) |
| project skills (npx/copy equivalent) | commit message: code-style | fail | `claude -p "Write a commit message for the staged change…"` | loaded: none |
| all 41 skills (project) | listing | pass | `claude -p` (init event) | 41/41 listed |
| all 41 skills (project) | default Go | pass | `claude -p "Write a small Go function…"` | loaded: go-style |
| all 41 skills (project) | descriptions not cut | pass | `claude -p "quote verbatim the description…"` | go-style, code-style, sql-style, typescript-style, vue-style quoted in full |

Codex (`tests/load/codex_load.py`):

| Route | Check | Result | Command | Saw |
| --- | --- | --- | --- | --- |
| marketplace | install | pass | `codex plugin marketplace add <repo>` | Added marketplace `style-skills` |
| plugin go | install | pass | `codex plugin add go@style-skills` | Added plugin `go` from marketplace `style-skills` |
| plugin house-style | install | pass | `codex plugin add house-style@style-skills` | Added plugin `house-style` from marketplace `style-skills` |
| plugin go + house-style | plugin list | pass | `codex plugin list` | read `.claude-plugin/marketplace.json`; both installed, enabled |
| plugin go + house-style | model-visible list | pass | `codex debug prompt-input hi` | go:go-style plus 13 house-style:* entries; source skills hidden |
| npx skills add -g | install | pass | `npx -y skills add <repo> --skill go-style -a claude-code -a codex -g -y` | `~/.agents/skills/go-style` (copy) |
| npx skills add -g | model-visible list | pass | `codex debug prompt-input hi` | go-style listed from `~/.agents/skills` |
| folder copy | model-visible list | pass | `cp -r skills/python-style ~/.agents/skills/` | python-style listed from `~/.agents/skills` |
| $skill-installer local path | install | fail | `python3 <skill-installer>/scripts/install-skill-from-github.py --url file://<repo>/skills/go-style` | Error: Only GitHub URLs are supported for download mode. |
| all 41 skills + 13 plugins (scratch HOME) | descriptions not cut | pass | `codex debug prompt-input hi` | 38 style entries, all 38 descriptions unchanged; 42 skills listed in all |
| project skills (.agents/skills) | default Go | pass | `codex exec -s read-only -C <proj> "Write a small Go function Reverse…"` | loaded: code-style, go-style |
| project skills (.agents/skills) | named: Uber in words | fail | `codex exec … "Use Uber's Go style. Write…"` | loaded: code-style, go-style |
| project skills (.agents/skills) | named: $go-uber-style | pass | `codex exec … "$go-uber-style Write…"` | loaded: code-style, go-uber-style |
| project skills (.agents/skills) | default Python | pass | `codex exec … "Write a small Python function slugify…"` | loaded: code-style, python-style |
| project skills (.agents/skills) | named: Google's Python in words | fail | `codex exec … "Use Google's Python style. Write…"` | loaded: code-style, python-style |
| project skills (.agents/skills) | named: $python-google-style | pass | `codex exec … "$python-google-style Write…"` | loaded: code-style, python-google-style |
| project skills (.agents/skills) | commit message: code-style | pass | `codex exec … "Write a commit message for the staged change…"` | loaded: code-style |
| all 41 skills (project) | default Go | pass | `codex exec … "Write a small Go function…"` | loaded: code-style, go-style |

## Repeating

```sh
cd tests/load
python3 claude_load.py install   # scratch HOME, no model call
python3 claude_load.py model     # about 20 small Sonnet calls in <work>/proj-claude-*
python3 codex_load.py install
python3 codex_load.py model      # 9 codex exec runs in <work>/proj-codex-*
```

With no argument, each script runs both parts. `SK_LOAD_WORK` moves the work folder. Rows are printed and saved as `results-<tool>-<mode>.json` in the work folder; the exit status is the number of failed rows. The scripts expect the plain-words checks (three in Claude Code, two in Codex) and Claude's commit-message checks to fail until the decisions above are made.

## Review update, 2026-10-31

The code-style description now leads with commit messages, code review, and shared rules in any language. The older commit-message results above describe the old description; the 4-of-4 commit-only rerun below validates the new description.

Commit-only rerun, 2026-10-31, new description: **pass, 4 of 4 runs** (`claude_load.py commit`, run twice; claude-sonnet-5-5). Both routes, the house-style plugin via `--plugin-dir` and project skill copies, loaded code-style each time. Codex already passed.
