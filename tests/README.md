# Tests

Run `python3 -m unittest discover -s tests` for tooling regressions and
`python3 tests/load/check_entrypoints.py` for isolated packaging checks.

Current inventory: 46 skills (14 house, 28 source, 4 link-only), 14 plugins.
The design tests exercise metadata/font filtering, ownership renaming, token
change propagation, input allowlisting, CSS/JSON parity, and unrounded contrast
in both themes. No private source fixture or network request is required.

Run `python3 tools/check.py --offline` with the source checkout and external
marker list available for generation, privacy, cached-link and originality checks.
See [load/README.md](load/README.md) for installation/model checks and their limits.
