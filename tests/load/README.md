# Load checks

Run `python tests/load/check_entrypoints.py` to check metadata and references after copying each skill and plugin bundle into its own temporary directory. It does not install skills, invoke a model, or change user configuration.

The current inventory is 46 skills (14 house, 28 source, 4 link-only) across 14
plugin bundles. `design-style` appears in both `design` and `house-style`.
The design addition has isolated packaging checks; historical model/load results
in RESULTS.md describe their recorded revision and do not validate design selection.

`python tools/check.py` also validates the marketplace and all plugin bundles with Claude Code when it is installed.

`claude_load.py` and `codex_load.py` exercise installation and skill selection. Their `install` mode uses a temporary HOME and makes no model calls. Their `model` mode uses project skill copies and the existing sign-in; it requires signed-in tools and network access. Set `SK_LOAD_WORK` to the directory for scratch projects and results; otherwise a temporary directory is created.

To repeat only the commit-message checks after changing code-style:

```sh
SK_LOAD_WORK=/path/to/scratch python tests/load/claude_load.py commit
SK_LOAD_WORK=/path/to/scratch python tests/load/codex_load.py commit
```

Model mode uses the tools' normal session storage. Run it only where that storage is writable; never copy credentials or run model checks in the temporary HOME used for installation tests. See [RESULTS.md](RESULTS.md) for observed behavior and limits.
