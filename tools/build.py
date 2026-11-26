#!/usr/bin/env python3
"""Generate skill metadata, credits, marketplace, and README deterministically."""
from __future__ import annotations

from pathlib import Path
import re

from common import ROOT, TAG, enabled, json_text, markdown_links, quick_rules, read_catalog, write


def frontmatter(skill: dict) -> str:
    import json
    quote = json.dumps
    fields = ['---', f"name: {skill['name']}", f"description: {quote(skill['description'])}", f"license: {skill['license']}"]
    if skill['kind'] != 'house':
        fields.append('disable-model-invocation: true')
    fields.extend(['metadata:', f"  kind: {skill['kind']}", f"  language: {skill['language']}", f"  version: {quote(skill.get('skill_version', '1.0.0'))}", f"  source-url: {quote(skill['url'] if skill['kind'] != 'house' else 'references/sources.md')}", f"  treatment: {skill['treatment']}", '---', ''])
    return '\n'.join(fields)


def openai_yaml(skill: dict) -> str:
    import json
    text = 'interface:\n  display_name: ' + json.dumps(skill['display_name']) + '\n'
    if skill['kind'] == 'house':
        short = 'Commit messages, code review, and shared code rules' if skill['language'] == 'all' else 'House style for ' + {'cpp': 'C++', 'typescript': 'TypeScript', 'powershell': 'PowerShell', 'html': 'HTML', 'css': 'CSS', 'sql': 'SQL'}.get(skill['language'], skill['language'].title()) + ' code and reviews'
        if skill['language'] == 'design':
            short = 'House UI tokens, layout, states, and keyboard behavior'
        text += '  short_description: ' + json.dumps(short) + '\n'
    implicit = 'true' if skill['kind'] == 'house' else 'false'
    text += 'policy:\n  allow_implicit_invocation: ' + implicit + '\n'
    return text


def plugin_skills(catalog: dict) -> dict[str, list[dict]]:
    skills = enabled(catalog)
    languages = sorted({s['language'] for s in skills} - {'all'})
    return {name: [s for s in skills if (s['kind'] == 'house' if name == 'house-style' else s['language'] == name)]
            for name in ['house-style'] + languages}


def marketplace(catalog: dict) -> dict:
    # Each default skills/ scan is confined to a self-contained plugin root.
    plugins = [{'name': name, 'source': './plugins/' + name,
                'description': 'House coding and UI design style (used automatically)' if name == 'house-style' else 'House UI design: tokens, layout, and component behavior' if name == 'design' else {'cpp': 'C++', 'typescript': 'TypeScript', 'powershell': 'PowerShell', 'html': 'HTML', 'css': 'CSS', 'sql': 'SQL'}.get(name, name.title()) + ': house style plus source guides (sources run only when named)',
                'version': catalog['build_version']}
               for name in plugin_skills(catalog)]
    return {'name': 'style-skills', 'owner': {'name': 'style-skills contributors'}, 'metadata': {'description': 'Coding and house UI design guides as skills', 'version': catalog['build_version']}, 'plugins': plugins}


def source_body(root: Path, skill: dict) -> str:
    body = (root / skill['body_path']).read_text()
    body_format = skill.get('body_format', 'markdown')
    if body_format == 'skill-markdown':
        match = re.fullmatch(r'---\n.*?\n---\n(.*)', body, re.S)
        if not match:
            raise ValueError(f"{skill['name']}: missing or malformed YAML frontmatter")
        body = match[1].removeprefix('\n')
    elif body_format != 'markdown':
        raise ValueError(f"{skill['name']}: unsupported body_format {body_format}")
    return source_examples(root, skill, body)


def examples_line(root: Path, skill: dict) -> str:
    """Route to authored examples without making them sync inputs."""
    links = []
    base = root / 'skills' / skill['name']
    for example in skill.get('examples', []):
        path = Path(example['path'])
        if path.is_absolute() or '..' in path.parts or path.parts[:2] != ('references', 'examples'):
            raise ValueError(f"{skill['name']}: invalid example path {path}")
        if not (base / path).is_file():
            raise ValueError(f"{skill['name']}: missing example {path}")
        links.append(f"[{example['label']}]({path.as_posix()})")
    return '\n- For worked controls, read ' + ', '.join(links) + '.' if links else ''


def source_examples(root: Path, skill: dict, body: str) -> str:
    """Refresh example links even when SKILL.md is its own authored body."""
    body = re.sub(r'\n<!-- BEGIN GENERATED EXAMPLES -->\n.*?\n<!-- END GENERATED EXAMPLES -->\n?',
                  '', body, flags=re.S)
    links = examples_line(root, skill)
    if not links:
        return body
    if skill['kind'] == 'link-only':
        body = body.replace("covers only this skill's original pointer text.",
                            "covers this skill's original pointer text and original worked examples.")
    return (body + '\n<!-- BEGIN GENERATED EXAMPLES -->\n## When to read more\n'
            + links + '\n\nOriginal examples use this skill\'s [license](LICENSE).\n'
            + '<!-- END GENERATED EXAMPLES -->\n')


def link_only_body(root: Path, skill: dict) -> str:
    """Render the reviewed reading workflow independently of its output SKILL.md."""
    existing = skill.get('existing_skill', {})
    if existing.get('status') in {'found', 'found-related'}:
        installation = (f"For a related third-party skill, see [{existing['name']}]({existing['skill_url']}). "
                        f"Its recorded install line is `{existing['install_line']}`.\n\n"
                        + existing['caveat'])
    else:
        installation = 'Use the original guide directly; no verified guide-specific skill is linked here.'
    url = skill['url']
    citation = 'section title and link to the exact section you read'
    if skill['name'] == 'cpp-core-guidelines-style':
        url += 'CppCoreGuidelines'
        citation = 'guideline ID (for example R.11) and link to the exact guideline you read'
    elif skill['name'] == 'rust-effective-style':
        citation = 'item number (for example Item 1) and link to the exact item you read'
    body = (root / 'tools/templates/link-only-body.md').read_text().format(
        title=skill['display_name'], house_skill=skill['language'] + '-style',
        language=skill['display_name'].split(' style:', 1)[0],
        source_title=skill['source_title'], source_url=url,
        license_summary=skill['license_summary'],
        source_license=skill['source_license'], installation=installation,
        citation=citation, credit_line=skill['credit_line'])
    return source_examples(root, skill, body)


def bundle_outputs(root: Path, catalog: dict, generated: dict[str, str | bytes]) -> dict[str, str | bytes]:
    outputs = {}
    market = marketplace(catalog)
    entries = {p['name']: p for p in market['plugins']}
    for name, skills in plugin_skills(catalog).items():
        prefix = f'plugins/{name}/'
        manifest = {k: v for k, v in entries[name].items() if k != 'source'}
        manifest['author'] = market['owner']
        outputs[prefix + '.claude-plugin/plugin.json'] = json_text(manifest)
        for skill in skills:
            base = 'skills/' + skill['name'] + '/'
            # Copy bytes, including dotfiles and licenses. Prefer this build's
            # outputs so a single run never bundles stale generated metadata.
            files = {}
            skill_root = root / base
            if skill_root.is_symlink():
                raise ValueError(f'refusing symlink bundle input: {base}')
            for path in sorted(skill_root.rglob('*')):
                if path.is_symlink():
                    raise ValueError(f'refusing symlink bundle input: {path.relative_to(root)}')
                if (path.is_file() and '__pycache__' not in path.relative_to(root).parts
                        and path.suffix not in {'.pyc', '.pyo', '.pyd'}):
                    files[path.relative_to(root).as_posix()] = path.read_bytes()
            files.update((p, content) for p, content in generated.items() if p.startswith(base))
            outputs.update((prefix + p, content) for p, content in files.items())
    return outputs


def stale_bundle_paths(root: Path, outputs: dict[str, str | bytes]) -> list[Path]:
    """plugins/ is wholly generated; catch extra files, directories and symlinks."""
    bundle_root = root / 'plugins'
    if bundle_root.is_symlink():
        raise ValueError('refusing symlink bundle root: plugins')
    expected = {root / p for p in outputs if p.startswith('plugins/')}
    directories = {parent for path in expected for parent in path.parents if parent.is_relative_to(bundle_root)}
    stale = []
    for path in sorted(bundle_root.rglob('*'), key=lambda p: (-len(p.parts), p.as_posix())):
        if path.is_symlink():
            raise ValueError(f'refusing symlink bundle output: {path.relative_to(root)}')
        if path not in (directories if path.is_dir() else expected):
            stale.append(path)
    return stale


def cell(value: str) -> str:
    return value.replace('|', '\\|').replace('\n', ' ')


def source_row(source: dict, house: bool = False) -> str:
    treatment = 'reference-only' if house and source['treatment'] != 'adapt' else source['treatment']
    return f"| [{cell(source['title'])}]({source['url']}) | {cell(source['owner'])} | {source['license']} | {treatment} |"


def reference_credit(source: dict) -> str:
    owner = source['owner'].rstrip('.')
    return (f"{source['title']}, {source['owner']}, {source['license']}, {source['url']}. "
            f"Referenced in original house wording; no source sentences or examples reproduced. Unofficial, not endorsed by {owner}.")


def sources_text(root: Path, skill: dict, catalog: dict) -> str:
    if skill['language'] == 'design':
        return (root / 'tools/bodies/design-sources.md').read_text()
    reference = root / 'skills' / skill['name'] / 'references'
    tags = set()
    cited_pages = set()
    paths = list(reference.rglob('*.md'))
    paths.extend(root / 'skills' / skill['name'] / example['path']
                 for example in skill.get('examples', []))
    for path in paths:
        if path.name != 'sources.md':
            tags.update(TAG.findall(path.read_text()))
            cited_pages.update(url for _, url in markdown_links(path.read_text()) if url in catalog.get('citation_pages', {}))
    tags &= catalog['source_tags'].keys()
    ids = set(skill['source_ids']) | {catalog['source_tags'][tag]['source_id'] for tag in tags}
    for tag in tags:
        ids.update(catalog['source_tags'][tag].get('additional_source_ids', []))
    ids.update(catalog['citation_pages'][url]['source_id'] for url in cited_pages)
    sources = [s for s in catalog['sources'] if s['id'] in ids]
    lines = ['# Sources and changes', '', 'House text: CC-BY-4.0, style-skills contributors. Configurations: MIT (see config/LICENSE).', '', 'Changes: independently worded rules combined, conflicts settled, and project-specific scope kept explicit. Source wording and examples are not bundled. Link-only, share-alike, WCAG, and ShellCheck references supply links and attribution only; their licenses do not become the house license.', '', 'Related guides and shared rules are included where linked. Local link destinations and config import paths are adjusted for packaging. ', '', 'Unofficial: not affiliated with or endorsed by any source owner. NOASSERTION means the license was not established; it is not a reuse grant.', '', '| Source | Owner | Source license | Treatment |', '| --- | --- | --- | --- |']
    lines.extend(source_row(s, house=True) for s in sources)
    lines.extend(['', '## Source tags', '', '| Tag | Reference | Source license |', '| --- | --- | --- |'])
    byid = {s['id']: s for s in sources}
    for tag in sorted(tags):
        info = catalog['source_tags'][tag]
        source = byid[info['source_id']]
        links = ', '.join(f'[source {i}]({url})' for i, url in enumerate(info['urls'], 1))
        licenses = '; '.join(f'{license} ({host})' for host, license in info.get('licenses', {}).items()) or source['license']
        lines.append(f"| `[{tag}]` | {links} | {licenses} |")
    lines.extend(['', '## Direct citations', '', '| Page | Source license |', '| --- | --- |'])
    for url in sorted(cited_pages):
        page = catalog['citation_pages'][url]
        lines.append(f"| [{cell(page['title'])}]({url}) | {byid[page['source_id']]['license']} |")
    lines.extend(['', '## Attribution notices', ''])
    for source in sources:
        lines.append(f"- {source.get('credit_line', source['title']) if source['treatment'] == 'adapt' else reference_credit(source)}")
        notice = source.get('attribution_wording', '')
        if notice and not notice.startswith('not applicable:'):
            lines.append('  Source notice (applies to the linked work): ' + notice)
    return '\n'.join(lines) + '\n'


def build_outputs(root: Path, catalog: dict) -> dict[str, str | bytes]:
    content_license = (root / 'LICENSE-CONTENT').read_text()
    software_license = (root / 'LICENSE').read_text()
    body_template = (root / 'tools/templates/house-body.md').read_text()
    outputs = {}
    for skill in enabled(catalog):
        base = 'skills/' + skill['name'] + '/'
        if skill['kind'] == 'house':
            guide = (root / base / 'references/guide.md').read_text()
            scope = next((line for line in guide.splitlines() if line.startswith('Scope:')), 'Scope: shared rules for code in every language.')
            # Execution history is not part of the language baseline.
            scope = re.sub(r',?\s*(?:with )?the sample executed on CPython \d+\.\d+\.\d+', '', scope)
            scope = re.sub(r' The sample uses [^.]+(?:\.\d+)*\.', '', scope)
            template = (root / 'tools/templates/design-body.md').read_text() if skill['language'] == 'design' else body_template
            body = template.format(title=skill['display_name'], language='coding' if skill['language'] == 'all' else skill['display_name'].split(' style')[0], scope=scope, quick_rules=quick_rules(guide), examples=examples_line(root, skill))
            outputs[base + 'references/sources.md'] = sources_text(root, skill, catalog)
            outputs[base + ('references/TOKENS-LICENSE' if skill['language'] == 'design' else 'references/config/LICENSE')] = software_license
            license_text = content_license
        else:
            body = link_only_body(root, skill) if skill['kind'] == 'link-only' else source_body(root, skill)
            license_text = (root / skill['license_path']).read_bytes()
        text = frontmatter(skill) + '\n' + body
        if len(text.splitlines()) > 80 or len(skill['description']) > 150:
            raise ValueError(f"{skill['name']}: entrypoint or description too long")
        outputs[base + 'SKILL.md'] = text
        outputs[base + 'agents/openai.yaml'] = openai_yaml(skill)
        outputs[base + 'LICENSE'] = license_text
    outputs['.claude-plugin/marketplace.json'] = json_text(marketplace(catalog))
    credits = ['# Credits', '', 'House prose is CC-BY-4.0. Tools, tests, and configurations are MIT. Original worked examples follow the containing house skill\'s CC-BY-4.0 license. The table records upstream terms; those terms do not relicense the original house wording. Source skills retain their declared licenses; link-only wrappers contain no source text.', '', 'Changes: rules independently restated and combined, conflicts resolved, source examples omitted. Worked examples are original code. Restricted sources are linked only. All skills are unofficial and unendorsed. NOASSERTION entries need a further license review before any source adaptation.', '', '| Source | Owner | Source license | Treatment |', '| --- | --- | --- | --- |']
    credits.extend(source_row(s) for s in catalog['sources'])
    byid = {s['id']: s for s in catalog['sources']}
    credits.extend(['', '## Directly cited pages', '', '| Page | Source license |', '| --- | --- |'])
    for url, page in sorted(catalog.get('citation_pages', {}).items()):
        credits.append(f"| [{cell(page['title'])}]({url}) | {byid[page['source_id']]['license']} |")
    credits.extend(['', '## Source-specific notices', ''])
    for source in catalog['sources']:
        notice = source.get('attribution_wording', '')
        if notice and not notice.startswith('not applicable:'):
            credits.append(f"- [{source['title']}]({source['url']}): {notice}")
    outputs['CREDITS.md'] = '\n'.join(credits) + '\n'
    readme = (root / 'tools/templates/README.md').read_text()
    readme = readme.replace('{house_count}', str(sum(s['kind'] == 'house' for s in enabled(catalog))))
    readme = readme.replace('{source_count}', str(sum(s['kind'] != 'house' for s in enabled(catalog))))
    table = ['<!-- BEGIN GENERATED SKILLS -->', '| Language | Skill | Based on | License |', '| --- | --- | --- | --- |']
    byid = {s['id']: s for s in catalog['sources']}
    for skill in enabled(catalog):
        # Main guides in this compact table; every supplementary citation is in credits.
        names = ', '.join(byid[sid]['title'] for sid in skill['source_ids'] if not sid.startswith('citation-'))
        if skill['language'] == 'design':
            names = 'Original house visual rules; WCAG 2.2 reference'
        license_label = skill['license'] + (' (our pointer text only; guide not included)' if skill['kind'] == 'link-only' else '')
        table.append(f"| {skill['language']} | [{skill['name']}](skills/{skill['name']}/SKILL.md) | {cell(names)} | {license_label} |")
    table.append('<!-- END GENERATED SKILLS -->')
    readme = readme.replace('<!-- table made by tools/build.py: language, skill, based on, license -->', '\n'.join(table))
    installs = []
    for skill in enabled(catalog):
        if skill['kind'] == 'link-only' and skill.get('existing_skill', {}).get('status') in {'found', 'found-related'}:
            existing = skill['existing_skill']
            installs.append(f"- [{existing['name']}]({existing['skill_url']}), related to {skill['source_title']}: `{existing['install_line']}`. {existing['caveat']}")
    readme = readme.replace('<!-- related link-only skill installs -->', '\n'.join(installs))
    outputs['README.md'] = readme
    outputs.update(bundle_outputs(root, catalog, outputs))
    return outputs


def main() -> int:
    try:
        outputs = build_outputs(ROOT, read_catalog())
        stale = stale_bundle_paths(ROOT, outputs)
        for relative, text in outputs.items():
            write(ROOT / relative, text)
        for path in stale:
            path.rmdir() if path.is_dir() else path.unlink()
    except (OSError, ValueError, KeyError) as exc:
        print(f'FAIL build: {exc}')
        return 1
    print(f'PASS build: {len(outputs)} generated files')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
