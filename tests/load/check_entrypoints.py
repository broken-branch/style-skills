#!/usr/bin/env python3
"""Check each skill's entrypoint and links in isolation; installs nothing."""
import json
from pathlib import Path
import sys
import tempfile
import shutil

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from common import ROOT, local_target, markdown_links, enabled, read_catalog
from check import parse_frontmatter, StrictLoader
from build import plugin_skills
import yaml

failures = []
catalog = read_catalog()
skills = enabled(catalog)


def check_folder(root, label):
    for entry in root.rglob('SKILL.md'):
        parse_frontmatter(entry.read_text())
        yaml.load((entry.parent / 'agents/openai.yaml').read_text(), Loader=StrictLoader)
    for path in root.rglob('*.md'):
        for line, url in markdown_links(path.read_text()):
            if '://' in url or url.startswith('mailto:'):
                continue
            target, _ = local_target(path, url)
            if not target.is_relative_to(root) or not target.exists():
                failures.append(f'FAIL {label}/{path.relative_to(root)}:{line}: {url}')


for skill in skills:
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder) / skill['name']
        shutil.copytree(ROOT / 'skills' / skill['name'], root)
        check_folder(root, skill['name'])
plugins = plugin_skills(catalog)
for name, members in plugins.items():
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder) / name
        shutil.copytree(ROOT / 'plugins' / name, root)
        manifest = json.loads((root / '.claude-plugin/plugin.json').read_text())
        if manifest['name'] != name or 'skills' in manifest:
            failures.append(f'FAIL {name}: unexpected plugin manifest or custom skill paths')
        actual = {p.name for p in (root / 'skills').iterdir()}
        if actual != {s['name'] for s in members}:
            failures.append(f'FAIL {name}: unexpected skills in default discovery directory')
        check_folder(root, name)
for failure in failures:
    print(failure)
print(f'{"FAIL" if failures else "PASS"}: {len(skills)} isolated skill folders and {len(plugins)} isolated plugin bundles; metadata and local references')
raise SystemExit(bool(failures))
