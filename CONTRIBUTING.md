# Contributing

Installing and using the skills and plugins needs nothing beyond this repository.

The sync and comparison workflow below is for maintainers: it reads the separate,
private source repository, where house rules and configurations are changed first.
Public contributors can propose changes to the bundled files here, and a maintainer
carries them into that source repository and regenerates. Maintainers then run these commands
from this repository:

```sh
python tools/sync.py
python tools/build.py
python tools/check.py
python -m unittest discover -s tests
```

Use Python 3.11 or later and install `tools/requirements.txt` in your environment.
The default upstream is the sibling repository; `sync.py --source PATH` and
`check.py --source PATH` select another checkout. Sync reads only its `code/`
and `configs/` trees, plus exactly `design/tokens.css` and `design/tokens.json`
through the reviewed `house-design-tokens-v1` filter. Design prose is authored
in `skills/design-style/references/`; its entrypoint uses `tools/templates/design-body.md`
and its provenance inventory uses `tools/bodies/design-sources.md`. Token changes
flow through sync; new token names require review of `tools/design-token-profile.json`.
The filter replaces metadata, uses generic system fonts, renames ownership slots,
and verifies CSS parity and unrounded contrast before emitting either token file.
The checker separately reads its private marker list,
which is never copied here. Set `--markers PATH` to select a list explicitly; a missing explicit list fails. With no default list, the checker prints `SKIP privacy: no marker list`. Forbidden working files are still checked. Set `STYLE_SKILLS_SOURCE` to select a checkout for both scripts without passing `--source`. A source archive without that checkout prints an explicit sync-check skip.

Edit descriptions, source metadata, build status, and source-page coverage in
[tools/catalog.json](tools/catalog.json). Edit generated presentation in
[tools/templates/](tools/templates/). Run the builder again to regenerate it.
The sync manifest records link relocations and omitted upstream-only references.
Only enabled catalog entries ship; planned source skills are not placeholders.

Keep canonical skill files in `skills/`. The builder copies them into isolated
`plugins/<name>/skills/` bundles, including dotfiles, references, and licenses.
Each bundle uses only Claude's default skill discovery and its own manifest.
All of `plugins/` is generated; the builder removes stale files and directories
there. Do not edit bundled copies. Language bundles contain their house skill
and their enabled sources; `design` contains the design house skill alone;
`house-style` contains all house skills, including design.

Source bodies live in `tools/bodies/` and support bare Markdown or `body_format: skill-markdown` for an
authored entrypoint whose frontmatter is regenerated. Link-only bodies come
from [the wrapper template](tools/templates/link-only-body.md) and catalog facts,
so the checker can compare them independently of the generated `SKILL.md`.
The template supplies an original-reading, offline-fallback, citation, and attribution workflow. [LICENSING.md](LICENSING.md) explains link-only treatments and unresolved source terms.

The checker caches each external page in the ignored `.cache/sources/` folder.
Use `--offline` to replay cached results, `--retry-failed` to retry only failed
requests, or `--refresh` to fetch everything again.
HTTP failures and missing cache entries fail validation. No check failure is
silently waived. Work notes and validation logs must stay outside the public tree. Claude validation is skipped with an explicit message only
when Claude Code is not installed.

The design examples also have an opt-in rendered check, separate from the default
unittest run. Use an existing Playwright module and Chromium executable; this
script installs nothing, starts no server, opens local files, and blocks network
requests. From the repository root:

```sh
PLAYWRIGHT_MODULE=/absolute/path/to/playwright \
CHROMIUM_PATH=/absolute/path/to/chrome \
node tests/design_browser.cjs
```

If either variable is unset or the Playwright module is unavailable, it exits
successfully with `skipped: Playwright not available`. A configured Chromium
launch failure or a failed assertion exits nonzero; a skip is not a browser pass.
The executable path must point to the Chromium binary, not its containing folder.
Run it with a short `TMPDIR` (for example `TMPDIR=$(mktemp -d /tmp/sk.XXXX)`): under a long
temp path, Chromium's profile socket path gets too long and the launch fails.
Run this on a host that permits Chromium subprocesses. The script launches once
and does not retry a sandbox denial.

Every catalog-listed design HTML example runs in system light and dark themes at
320x900 and 1440x900, plus 1100x640 for the compact rail. Checks cover page overflow,
every sequential tab stop in forward/reverse order using real Tab keys, computed
focus outlines and clipping, text (including placeholders/disabled labels),
control boundaries and icon contrast, hover/pressed colors, keyboard table
sorting and horizontal table scrolling. Thresholds are compared without rounding:
4.5:1 for text and 3:1 for essential indicators. Forced-colors runs check system
Highlight focus; reduced-motion runs check actual computed animation/transition
durations and delays. Unexpected translucent text/surfaces or background images
fail rather than escaping the contrast audit. These examples use opaque sRGB
colors; this is a targeted regression check, not a screen-reader or complete
accessibility audit. Static feedback snapshots do not simulate server requests.

For syntax and contrast-math checks without launching a browser:

```sh
node --check tests/design_browser.cjs
node tests/design_browser.cjs --self-test
```
