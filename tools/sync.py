#!/usr/bin/env python3
"""One-way public guide/config sync and filtered house tokens. No research inputs."""
from __future__ import annotations

import argparse
import os
import re
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

from common import DEFAULT_SOURCE, LINK, ROOT, enabled, json_text, read_catalog, write
from design_tokens import filtered_tokens

DESIGN_INPUTS = {'design/tokens.json': 'references/tokens.json',
                 'design/tokens.css': 'references/tokens.css'}

EXCLUDED = {'sample', 'samples', '.git', '__pycache__', 'node_modules', 'target'}
# Config manifests run upstream samples; they are not project adoption templates.
EXCLUDED_FILES = {'VALIDATION.md', 'REPORT.md', 'Test-Guide.ps1', 'accessibility.spec.mjs', 'package.json'}
EXCLUDED_CONFIG_PATHS = {
    'configs/html/playwright.config.mjs',
    'configs/html/run-browser-tests.mjs',
    # Keep the sample SQL and its safety README together upstream.
    'configs/sql/migrations',
}


def public_file(source: Path, relative: str) -> Path:
    path = PurePosixPath(relative)
    if path.is_absolute() or '..' in path.parts or not path.parts or (path.parts[0] not in {'code', 'configs'} and relative not in DESIGN_INPUTS):
        raise ValueError(f'not a public input: {relative}')
    current = source
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f'symlink input refused: {relative}')
    if not current.is_file():
        raise ValueError(f'missing public input: {relative}')
    return current


def config_files(source: Path, language: str) -> list[str]:
    if not re.fullmatch(r'[a-z]+', language):
        raise ValueError('invalid config directory')
    base = source / 'configs' / language
    if base.is_symlink():
        raise ValueError('symlink config directory refused')
    result = []
    for directory, dirs, files in os.walk(base, followlinks=False):
        for name in dirs:
            if (Path(directory) / name).is_symlink():
                raise ValueError('symlink config subtree refused')
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDED
                         and (Path(directory) / d).relative_to(source).as_posix() not in EXCLUDED_CONFIG_PATHS)
        for name in sorted(files):
            relative = (Path(directory) / name).relative_to(source).as_posix()
            if name in EXCLUDED_FILES or relative in EXCLUDED_CONFIG_PATHS:
                continue
            public_file(source, relative)
            result.append(relative)
    return result


def plan_skill(source: Path, skill: dict) -> dict[str, str]:
    """Map only public inputs to self-contained destinations for one skill."""
    guide = skill['house_guide_path']
    public_file(source, guide)
    mapping = {guide: 'references/guide.md'}
    # All skills, including the shared skill, receive shared.md.
    if guide != 'code/shared.md':
        mapping['code/shared.md'] = 'references/shared.md'
    pending = [guide, 'code/shared.md']
    seen = set()
    while pending:
        relative = pending.pop()
        if relative in seen:
            continue
        seen.add(relative)
        text = public_file(source, relative).read_text()
        for m in LINK.finditer(text):
            url = urlsplit(m[2].strip('<>'))
            if url.scheme or not url.path:
                continue
            linked = Path(os.path.normpath(str(Path(relative).parent / unquote(url.path)))).as_posix()
            if linked.startswith('code/') and linked.endswith('.md') and linked not in mapping:
                public_file(source, linked)
                mapping[linked] = 'references/related/' + Path(linked).name
                pending.append(linked)
    languages = set(skill.get('config_roots', []))
    languages.update(Path(p).stem for p in mapping if p.startswith('code/') and p != 'code/shared.md')
    for language in sorted(languages):
        for relative in config_files(source, language):
            tail = Path(relative).relative_to('configs/' + language).as_posix()
            folder = 'references/config/' if language == skill['language'] else f'references/config/{language}/'
            mapping[relative] = folder + tail
    # Root configs are dependencies of shared and web guides. Do not replace a
    # language-specific .editorconfig with the root's different settings.
    common = {'.editorconfig'}
    if languages & {'html', 'css', 'react', 'vue', 'typescript'}:
        common.add('.prettierrc.json')
    for name in sorted(common):
        destination = 'references/config/' + name
        if destination in mapping.values():
            destination = 'references/config/common/' + name
        mapping['configs/' + name] = destination
    return mapping


def rewrite_markdown(text: str, relative: str, destination: str, mapping: dict[str, str], omissions: list, link_rewrites: dict | None = None) -> str:
    # The conflict inventory is not bundled. Keep the choices and source
    # comparisons readable without its IDs; diagnostic codes stay intact.
    if relative == 'code/python.md':
        text = re.sub(r'\bC[0-9]{2}\b \(([^)\n]+)\)', r'differences over \1', text)
        text = re.sub(r'\bresolve C[0-9]{2}\b', 'resolve the competing styles', text)
        text = re.sub(r' (?:for|under|in) C[0-9]{2}\b', '', text)
    elif relative == 'code/go.md':
        text = re.sub(r'\(C[0-9]{2}: ', '(', text)

    # Explain how to adopt the bundled configs in the consuming project.
    adoption = {
        'code/bash.md': "For your project, merge the bundled EditorConfig settings, copy `.shellcheckrc` into the scripts' ancestor directory, and run `shfmt -d`, `shellcheck --check-sourced --severity=style`, and `bash -n` against your own shell files.",
        'code/html.md': 'For your project, copy the bundled HTML Validate profiles and root Prettier config, then run `html-validate --config .htmlvalidate.json path/to/your-page.html` and `prettier --config .prettierrc.json --check path/to/your-page.html`, replacing the example input with your own authored or assembled HTML files.',
    }
    if relative in adoption:
        text = text.replace('## Tooling\n\n', '## Tooling\n\n' + adoption[relative] + '\n\n', 1)
        text = re.sub(r"Commands run from this (?:repository|repo)'s root(?: and exercise the sample)?\. ", '', text)

    def replace(m):
        label, raw = m[1], m[2].strip('<>')
        if raw in (link_rewrites or {}):
            return f'[{label}]({link_rewrites[raw]})'
        parts = urlsplit(raw)
        if parts.scheme or raw.startswith('#'):
            return m[0]
        target = Path(os.path.normpath(str(Path(relative).parent / unquote(parts.path)))).as_posix()
        anchor = parts.fragment
        if target in mapping:
            output = mapping[target]
        elif target == 'research/SOURCES.md':
            output, anchor = 'references/sources.md', 'source-tags'
        elif target.startswith('research/') and target.endswith('conflicts.md'):
            output, anchor = 'references/guide.md', 'where-the-sources-disagree'
        else:
            omissions.append({'file': destination, 'target': target, 'label': label})
            return f'{label} (upstream-only; not bundled)'
        url = os.path.relpath(output, Path(destination).parent)
        if anchor:
            url += '#' + anchor
        return f'[{label}]({url})'
    return LINK.sub(replace, text)


def sync_outputs(root: Path, source: Path, catalog: dict) -> dict[str, bytes]:
    outputs, records = {}, []
    for skill in enabled(catalog):
        if skill['kind'] != 'house':
            continue
        if skill.get('sync_profile') == 'house-design-tokens-v1':
            base = 'skills/' + skill['name'] + '/'
            data, css = filtered_tokens(root,
                public_file(source, 'design/tokens.json').read_bytes(),
                public_file(source, 'design/tokens.css').read_bytes())
            outputs[base + 'references/tokens.json'] = data
            outputs[base + 'references/tokens.css'] = css
            records.append({'skill': skill['name'], 'inputs': DESIGN_INPUTS,
                            'filter': 'house-design-tokens-v1', 'omitted_links': [],
                            'transformations': ['replace source metadata', 'generic system font stacks',
                                                'public ownership token names', 'remove CSS comments',
                                                'validate schema, CSS parity and unrounded contrast']})
            continue
        mapping = plan_skill(source, skill)
        omissions = []
        base = 'skills/' + skill['name'] + '/'
        for relative, destination in sorted(mapping.items()):
            data = public_file(source, relative).read_bytes()
            if relative.endswith('.md'):
                data = rewrite_markdown(data.decode(), relative, destination, mapping, omissions, catalog.get('link_rewrites')).encode()
            elif relative.endswith(('.js', '.mjs')):
                text = data.decode()
                # Relocate relative config imports alongside their bundled dependency.
                def replace_import(m):
                    target = Path(os.path.normpath(str(Path(relative).parent / m[2]))).as_posix()
                    if target not in mapping:
                        return m[0]
                    path = os.path.relpath(mapping[target], Path(destination).parent)
                    if not path.startswith('.'):
                        path = './' + path
                    return m[1] + path + m[3]
                text = re.sub(r"(from\s+['\"])(\.[^'\"]+)(['\"])", replace_import, text)
                data = text.encode()
            outputs[base + destination] = data
        if skill['house_guide_path'] == 'code/shared.md':
            outputs[base + 'references/shared.md'] = outputs[base + 'references/guide.md']
        records.append({'skill': skill['name'], 'inputs': mapping, 'omitted_links': omissions})
    outputs['tools/sync-manifest.json'] = json_text({'version': 1, 'skills': records}).encode()
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=DEFAULT_SOURCE)
    args = parser.parse_args()
    try:
        outputs = sync_outputs(ROOT, args.source.resolve(), read_catalog())
        # Remove stale generated files only; never delete unrelated skill work.
        manifest = ROOT / 'tools/sync-manifest.json'
        if manifest.exists():
            import json
            old = json.loads(manifest.read_text())
            for record in old['skills']:
                for destination in set(record['inputs'].values()) | {'references/shared.md'}:
                    relative = 'skills/' + record['skill'] + '/' + destination
                    path = ROOT / relative
                    if relative not in outputs and path.is_file():
                        if not path.resolve().is_relative_to(ROOT / 'skills') or path.is_symlink():
                            raise ValueError('unsafe stale output path')
                        path.unlink()
        for relative, data in outputs.items():
            write(ROOT / relative, data)
    except (OSError, ValueError, KeyError) as exc:
        print(f'FAIL sync: {exc}')
        return 1
    print(f'PASS sync: {len(outputs) - 1} public files; public inputs only')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
