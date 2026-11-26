"""Shared deterministic metadata and Markdown helpers."""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = Path(os.environ.get('STYLE_SKILLS_SOURCE', ROOT.parent / 'style-source'))
NAME = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')
# Destinations may have nested parentheses (e.g. documentation method names).
LINK = re.compile(r'(?<!!)\[([^\]\n]*)\]\((<[^>]+>|(?:[^()\s]|\([^()]*\))+)(?:\s+"[^"]*")?\)')
TAG = re.compile(r'\[([A-Z][A-Z0-9.-]+)\]')


def read_catalog(root: Path = ROOT) -> dict:
    catalog = json.loads((root / 'tools/catalog.json').read_text())
    names = [s['name'] for s in catalog['skills']]
    if len(names) != len(set(names)):
        raise ValueError('catalog: duplicate skill name')
    ids = [s['id'] for s in catalog['sources']]
    if len(ids) != len(set(ids)):
        raise ValueError('catalog: duplicate source ID')
    for skill in catalog['skills']:
        if not NAME.fullmatch(skill['name']) or len(skill['name']) > 64:
            raise ValueError('catalog: invalid skill name')
        if skill['kind'] not in {'house', 'source', 'link-only'}:
            raise ValueError(f"catalog: unsupported kind for {skill['name']}")
        if skill.get('status') not in {'enabled', 'planned'}:
            raise ValueError(f"catalog: missing build status for {skill['name']}")
        for sid in skill['source_ids']:
            if sid not in ids:
                raise ValueError(f"catalog: unknown source {sid}")
    return catalog


def enabled(catalog: dict) -> list[dict]:
    return [s for s in catalog['skills'] if s['status'] == 'enabled']


def write(path: Path, data: str | bytes) -> None:
    content = data.encode() if isinstance(data, str) else data
    if path.is_symlink() or any(p.is_symlink() for p in path.parents):
        raise ValueError(f'refusing symlink output: {path.name}')
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_bytes() != content:
        path.write_bytes(content)


def json_text(value: object) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + '\n'


def quick_rules(text: str) -> str:
    match = re.search(r'^## Quick rules\s*\n(.*?)(?=^## |\Z)', text, re.M | re.S)
    if not match:
        raise ValueError('guide has no Quick rules section')
    block = match.group(1).strip('\n')
    if not 1 <= len(block.splitlines()) <= 25:
        raise ValueError('quick rules exceed 25 lines or are empty')
    if not all(line.startswith(('- MUST ', '- PREFER ')) for line in block.splitlines()):
        raise ValueError('quick rules must be one rule per line')
    return block


def markdown_links(text: str):
    """Return line, destination for inline, reference, and autolinks, outside fences."""
    fence = False
    definitions = {}
    lines = text.splitlines()
    for line in lines:
        m = re.match(r'^\s*\[([^\]]+)\]:\s*<?(\S+?)>?(?:\s+".*")?$', line)
        if m:
            definitions[m[1].casefold()] = m[2]
    for number, line in enumerate(lines, 1):
        if line.lstrip().startswith(('```', '~~~')):
            fence = not fence
            continue
        if fence:
            continue
        line = re.sub(r'`+[^`]*`+', '', line)
        for m in LINK.finditer(line):
            yield number, m[2].strip('<>')
        for m in re.finditer(r'<(https?://[^<>\s]+)>', line):
            yield number, m[1]
        for m in re.finditer(r'\[([^\]]+)\]\[([^\]]*)\]', line):
            key = (m[2] or m[1]).casefold()
            if key in definitions:
                yield number, definitions[key]
            else:
                yield number, 'missing-reference:' + key
        if re.match(r'^\s*\[[^\]]+\]:', line):
            key = re.search(r'\[([^\]]+)\]', line)[1].casefold()
            if key in definitions:
                yield number, definitions[key]


def heading_ids(text: str) -> set[str]:
    ids, counts = set(), {}
    for line in text.splitlines():
        if not re.match(r'^#{1,6} ', line):
            continue
        slug = re.sub(r'[^\w\- ]', '', re.sub(r'^#+ ', '', line).lower()).replace(' ', '-')
        n = counts.get(slug, 0)
        counts[slug] = n + 1
        ids.add(slug if not n else f'{slug}-{n}')
    ids.update(re.findall(r'(?:id|name)=["\']([^"\']+)["\']', text))
    return ids


def local_target(path: Path, url: str) -> tuple[Path, str]:
    parts = urlsplit(url)
    return (path.parent / unquote(parts.path)).resolve(), unquote(parts.fragment)
