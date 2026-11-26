#!/usr/bin/env python3
"""Validate packaging, licenses, privacy, text originality, links, and Claude."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import threading
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urldefrag, urlsplit
from urllib.request import Request, urlopen

try:
    import yaml
except ImportError:
    print('FAIL dependency: install tools/requirements.txt (PyYAML is required)')
    raise SystemExit(1)

from common import DEFAULT_SOURCE, LINK, NAME, ROOT, TAG, enabled, heading_ids, local_target, markdown_links, quick_rules, read_catalog
from build import build_outputs, examples_line, link_only_body, marketplace, plugin_skills, stale_bundle_paths
from sync import sync_outputs


EXAMPLE_INDEXES = ('references/sources.md', 'references/examples.md')


class StrictLoader(yaml.SafeLoader):
    """Reject duplicate keys instead of accepting a silent last-value override."""


def mapping(loader, node, deep=False):
    pairs = loader.construct_pairs(node, deep=deep)
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate YAML key: {key}')
        result[key] = value
    return result


StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    match = re.match(r'\A---\n(.*?)\n---\n(.*)\Z', text, re.S)
    if not match:
        raise ValueError('missing or malformed YAML frontmatter')
    data = yaml.load(match[1], Loader=StrictLoader)
    if not isinstance(data, dict):
        raise ValueError('frontmatter must be a mapping')
    return data, match[2]


class PageText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.parts = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        if tag in {'script', 'style', 'noscript', 'svg'}:
            self.skip += 1
        for key, value in attrs:
            if key in {'id', 'name'} and value:
                self.ids.add(value)
        if tag in {'p', 'div', 'br', 'li', 'pre', 'section', 'h1', 'h2', 'h3', 'h4', 'tr'}:
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag in {'script', 'style', 'noscript', 'svg'} and self.skip:
            self.skip -= 1
        if tag in {'p', 'div', 'li', 'pre', 'section', 'h1', 'h2', 'h3', 'h4', 'tr'}:
            self.parts.append('\n')

    def handle_data(self, text):
        if not self.skip:
            self.parts.append(text)


def readable(text: str, html: bool = False) -> str:
    if html:
        parser = PageText()
        parser.feed(text)
        return ''.join(parser.parts)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    # Keep labels and code text, not Markdown destination syntax.
    text = LINK.sub(lambda m: m[1], text)
    return unescape(text)


def words(text: str) -> list[str]:
    return re.findall(r"[^\W_]+(?:['’][^\W_]+)?", text.casefold(), re.UNICODE)


def shingles(text: str) -> set[tuple[str, ...]]:
    tokens = words(text)
    return {tuple(tokens[i:i + 12]) for i in range(len(tokens) - 11)}


def overlap_lines(text: str, source: set[tuple[str, ...]]) -> list[int]:
    tokens, positions = [], []
    for line, content in enumerate(readable(text).splitlines(), 1):
        current = words(content)
        tokens.extend(current)
        positions.extend([line] * len(current))
    return sorted({positions[i] for i in range(len(tokens) - 11) if tuple(tokens[i:i + 12]) in source})


def marker_hits(text: str, markers: list[str]) -> list[tuple[int, int]]:
    hits = []
    for number, line in enumerate(text.splitlines(), 1):
        for index, marker in enumerate(markers, 1):
            if re.search(r'(?<!\w)' + re.escape(marker) + r'(?!\w)', line, re.I):
                hits.append((number, index))
    return hits


class Cache:
    """One GET per distinct defragmented URL, cached even when fetching fails."""
    def __init__(self, path: Path, offline: bool = False, refresh: bool = False, retry_failed: bool = False):
        self.path, self.offline, self.refresh = path, offline, refresh
        self.retry_failed = retry_failed
        self.path.mkdir(parents=True, exist_ok=True)
        self.pages = {}
        self.host_locks = {}

    def fetch(self, url: str) -> dict:
        url = urldefrag(url)[0]
        key = hashlib.sha256(url.encode()).hexdigest()
        path = self.path / (key + '.json')
        if path.exists() and not self.refresh:
            data = json.loads(path.read_text())
            if data.get('url') != url:
                raise ValueError('cache URL mismatch')
            if not (self.retry_failed and data.get('error')):
                return data
        if self.offline:
            return {'url': url, 'error': 'not cached; offline mode', 'text': ''}
        page = {'url': url, 'fetched_at': int(time.time()), 'text': ''}
        try:
            request = Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; style-skills-link-check/1.0)', 'Accept': 'text/html,text/plain,application/json;q=0.9,*/*;q=0.5'})
            with urlopen(request, timeout=25) as response:
                body = response.read(16 * 1024 * 1024 + 1)
                if len(body) > 16 * 1024 * 1024:
                    raise ValueError('response exceeds 16 MiB')
                page.update(status=response.status, final_url=response.url, content_type=response.headers.get_content_type(), text=body.decode(response.headers.get_content_charset() or 'utf-8', errors='replace'))
                if not 200 <= response.status < 300:
                    page['error'] = f'HTTP {response.status}'
                elif not page['text'].strip():
                    page['error'] = 'empty response'
        except (HTTPError, URLError, OSError, ValueError) as exc:
            page['error'] = str(exc)
            if isinstance(exc, HTTPError):
                exc.close()
        temporary = path.with_suffix('.tmp')
        temporary.write_text(json.dumps(page, ensure_ascii=False))
        temporary.replace(path)
        return page

    def load(self, urls: set[str]) -> None:
        urls = sorted({urldefrag(u)[0] for u in urls})
        self.host_locks = {urlsplit(u).netloc: threading.Semaphore(2) for u in urls}
        def bounded_fetch(url):
            with self.host_locks[urlsplit(url).netloc]:
                return self.fetch(url)
        with ThreadPoolExecutor(max_workers=12) as pool:
            for url, result in zip(urls, pool.map(bounded_fetch, urls)):
                self.pages[url] = result


class Checks:
    def __init__(self, root: Path):
        self.root = root
        self.failures = []

    def fail(self, kind: str, location: str | Path, message: str) -> None:
        if isinstance(location, Path):
            location = location.relative_to(self.root).as_posix()
        self.failures.append(f'FAIL {kind} {location}: {message}')

    def public_files(self) -> list[Path]:
        result = subprocess.run(['git', '-C', str(self.root), 'rev-parse', '--show-toplevel'], capture_output=True, text=True)
        if result.returncode == 0 and Path(result.stdout.strip()).resolve() == self.root.resolve():
            listing = subprocess.run(['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'], cwd=self.root, capture_output=True, check=True)
            return sorted({self.root / p.decode() for p in listing.stdout.split(b'\0')
                           if p and ((self.root / p.decode()).is_file() or (self.root / p.decode()).is_symlink())})
        # Source archives have no Git index. Match the repository's ignored
        # build/cache/review directories, but never skip unknown public files.
        excluded = {'.git', '.cache', '__pycache__', '.venv', 'review'}
        return sorted(p for p in self.root.rglob('*') if (p.is_file() or p.is_symlink())
                      and not excluded.intersection(p.relative_to(self.root).parts)
                      and p.suffix not in {'.pyc', '.pyo', '.pyd'})

    def structure(self, catalog: dict) -> None:
        active = {s['name']: s for s in enabled(catalog)}
        actual = {p.name for p in (self.root / 'skills').iterdir() if p.is_dir()}
        for name in sorted(actual ^ active.keys()):
            self.fail('catalog', 'skills/' + name, 'enabled catalog and skill folders differ')
        allowed = {'name', 'description', 'license', 'metadata'}
        for name, skill in active.items():
            base = self.root / 'skills' / name
            try:
                text = (base / 'SKILL.md').read_text()
                front, body = parse_frontmatter(text)
                if front.get('name') != name or not NAME.fullmatch(name) or len(name) > 64:
                    self.fail('name', base, 'invalid name or folder mismatch')
                description = front.get('description')
                if not isinstance(description, str) or not 1 <= len(description) <= 150:
                    self.fail('description', base, 'must be a string of 1–150 characters')
                if len(text.splitlines()) > 80:
                    self.fail('length', base, 'SKILL.md exceeds 80 lines')
                fields = allowed | ({'disable-model-invocation'} if skill['kind'] != 'house' else set())
                if set(front) != fields:
                    self.fail('frontmatter', base, 'missing or unapproved fields')
                metadata = front.get('metadata', {})
                if not isinstance(metadata, dict) or set(metadata) != {'kind', 'language', 'version', 'source-url', 'treatment'}:
                    self.fail('metadata', base, 'unsupported or missing metadata fields')
                else:
                    for key in ('kind', 'language', 'treatment'):
                        if metadata[key] != skill[key]:
                            self.fail('metadata', base, key + ' differs from catalog')
                if front.get('license') != skill['license']:
                    self.fail('license', base, 'frontmatter differs from catalog')
                expected_license = self.root / ('LICENSE-CONTENT' if skill['kind'] in {'house', 'link-only'} else skill['license_path'])
                if (base / 'LICENSE').read_bytes() != expected_license.read_bytes():
                    self.fail('license', base, 'LICENSE does not match its declared license text')
                agent = yaml.load((base / 'agents/openai.yaml').read_text(), Loader=StrictLoader)
                if not isinstance(agent, dict) or not isinstance(agent.get('interface', {}).get('display_name'), str):
                    self.fail('openai', base, 'display name missing')
                policy = agent.get('policy', {})
                if skill['kind'] == 'house':
                    if 'disable-model-invocation' in front or policy.get('allow_implicit_invocation', True) is not True:
                        self.fail('invocation', base, 'house skills must allow implicit invocation')
                    guide = (base / 'references/guide.md').read_text()
                    if quick_rules(guide) != quick_rules(body):
                        self.fail('quick-rules', base, 'entrypoint differs from the guide')
                    if len(guide.splitlines()) > 600:
                        self.fail('guide', base, 'guide exceeds 600 lines')
                    credits = (base / 'references/sources.md').read_text()
                    guide_paths = [base / 'references/guide.md']
                    if skill['language'] == 'design':
                        guide_paths.append(base / 'references/components.md')
                    else:
                        guide_paths.append(base / 'references/shared.md')
                    guide_paths.extend((base / 'references/related').glob('*.md'))
                    for guide_path in guide_paths:
                        for number, line in enumerate(guide_path.read_text().splitlines(), 1):
                            if not line.startswith(('- MUST ', '- PREFER ')):
                                continue
                            tags = set(TAG.findall(line)) & catalog['source_tags'].keys()
                            provenance = re.findall(r'\[source: ([^\]]+)\]', line)
                            if skill['language'] == 'design':
                                for group in provenance:
                                    for tag in group.split('; '):
                                        if tag not in skill['provenance_tags'] or f'`{tag}`' not in credits:
                                            self.fail('source-tag', f'{guide_path.relative_to(self.root)}:{number}', 'unregistered design provenance tag')
                            citations = [url for _, url in markdown_links(line) if url in catalog.get('citation_pages', {})]
                            if not tags and not citations and not (skill['language'] == 'design' and provenance):
                                self.fail('source-tag', f'{guide_path.relative_to(self.root)}:{number}', 'rule has no registered source tag or direct citation')
                            for tag in tags:
                                if f'`[{tag}]`' not in credits:
                                    self.fail('source-tag', f'{guide_path.relative_to(self.root)}:{number}', f'{tag} is not credited')
                            for url in citations:
                                if url not in credits:
                                    self.fail('source-tag', f'{guide_path.relative_to(self.root)}:{number}', 'direct citation is not credited')
                elif front.get('disable-model-invocation') is not True or policy.get('allow_implicit_invocation') is not False:
                    self.fail('invocation', base, 'both explicit-only settings are required')
                if skill['kind'] != 'house':
                    self.source_examples(skill, catalog)
                if skill['kind'] == 'link-only':
                    allowed_paths = {'SKILL.md', 'agents/openai.yaml', 'LICENSE'}
                    if skill.get('examples'):
                        # Paths were validated above. Only declared original code and
                        # its pointer index are allowed; source text remains forbidden.
                        allowed_paths.update(example['path'] for example in skill['examples'])
                        allowed_paths.update(EXAMPLE_INDEXES)
                    for path in base.rglob('*'):
                        if path.is_file() and path.relative_to(base).as_posix() not in allowed_paths:
                            self.fail('link-only', path, 'link-only skills may not bundle source text')
                    if body.removeprefix('\n') != link_only_body(self.root, skill):
                        self.fail('link-only', base, 'wrapper differs from reviewed link-only body')
                # All explicitly named bundled paths, including backtick references.
                for target in re.findall(r'`(references/[^`]+|agents/[^`]+|LICENSE)`', body):
                    path = (base / target).resolve()
                    if not path.is_relative_to(base.resolve()) or not path.exists():
                        self.fail('reference', base, f'missing or escaping file {target}')
            except (OSError, ValueError, TypeError, KeyError, yaml.YAMLError) as exc:
                self.fail('skill', base, str(exc))
        try:
            actual_market = json.loads((self.root / '.claude-plugin/marketplace.json').read_text())
            if actual_market != marketplace(catalog):
                self.fail('marketplace', '.claude-plugin/marketplace.json', 'plugin membership or metadata differs from catalog')
        except (OSError, ValueError) as exc:
            self.fail('marketplace', '.claude-plugin/marketplace.json', str(exc))
        self.bundles(catalog)

    def source_examples(self, skill: dict, catalog: dict) -> None:
        base = self.root / 'skills' / skill['name']
        examples_line(self.root, skill)  # Reject traversal and missing files first.
        examples = skill.get('examples', [])
        if not 2 <= len(examples) <= 3:
            self.fail('examples', base, 'source skills need two or three examples')
        if len({example['path'] for example in examples}) != len(examples):
            self.fail('examples', base, 'example paths must be distinct')
        references = '\n'.join(path.read_text() for path in (base / 'references').rglob('*.md')
                               if 'examples' not in path.relative_to(base).parts)
        for example in examples:
            path = base / example['path']
            text = path.read_text()
            header = '\n'.join(text.splitlines()[:8])
            tags = re.findall(r'\[([A-Za-z0-9][A-Za-z0-9:_.-]*)\]', header)
            if not tags:
                self.fail('example-tag', path, 'opening comment has no source rule tag')
            # Registered tags anywhere in the example retain the house credit
            # contract and must also belong to this source skill.
            for tag in set(TAG.findall(text)):
                info = catalog['source_tags'].get(tag)
                if not info or info['source_id'] not in skill['source_ids'] or f'`[{tag}]`' not in references:
                    self.fail('example-tag', path, f'unregistered, foreign or uncredited source tag: {tag}')
            # Local rule IDs, section anchors and numbered items resolve in the
            # containing skill's references, never in another source's index.
            for tag in tags:
                if not re.search(r'(?<![\w:.-])' + re.escape(tag) + r'(?![\w:.-])', references):
                    self.fail('example-tag', path, f'unknown reference tag: {tag}')

    def bundles(self, catalog: dict) -> None:
        for name, skills in plugin_skills(catalog).items():
            base = self.root / 'plugins' / name
            try:
                actual = {p.name for p in (base / 'skills').iterdir()}
                expected = {s['name'] for s in skills}
                if actual != expected:
                    self.fail('bundle', base, 'default skills/ discovery differs from catalog membership')
                for path in base.rglob('*'):
                    if path.is_symlink():
                        self.fail('bundle', path, 'bundles must contain real files and directories')
                    elif path.is_file() and path.suffix == '.md':
                        for line, url in markdown_links(path.read_text()):
                            if urlsplit(url).scheme:
                                continue
                            target, _ = local_target(path, url)
                            if not target.is_relative_to(base.resolve()) or not target.exists():
                                self.fail('bundle', f'{path.relative_to(self.root)}:{line}', 'missing or escaping bundle reference: ' + url)
            except (OSError, ValueError) as exc:
                self.fail('bundle', base, str(exc))

    def generated(self, catalog: dict, source: Path) -> None:
        for name, producer in [('sync', lambda: sync_outputs(self.root, source, catalog)), ('build', lambda: build_outputs(self.root, catalog))]:
            try:
                if name == 'sync' and not source.exists():
                    print('SKIP sync: no source checkout; use --source PATH to verify synced guides')
                    continue
                outputs = producer()
                for relative, expected in outputs.items():
                    content = expected.encode() if isinstance(expected, str) else expected
                    path = self.root / relative
                    if not path.exists() or path.read_bytes() != content:
                        self.fail('generated', relative, f'out of date; rerun {name}.py')
                if name == 'build':
                    for path in stale_bundle_paths(self.root, outputs):
                        self.fail('generated', path, 'unexpected bundle content; rerun build.py')
            except (OSError, ValueError, KeyError) as exc:
                self.fail('generated', name, str(exc))

    def privacy(self, files: list[Path], marker_file: Path | None) -> None:
        forbidden = {'HANDOFF.md', 'QUESTIONS.md', 'SOURCES-addition.md', 'VALIDATION.md', 'REPORT.md'}
        for path in files:
            relative = path.relative_to(self.root)
            if path.name in forbidden or any(part in {'private', 'research', '.cache'} for part in relative.parts):
                self.fail('private-path', path, 'forbidden working material in public file set')
            if path.is_symlink():
                self.fail('symlink', path, 'public files must not escape through symlinks')
        if marker_file is None:
            print('SKIP privacy: no marker list; use --markers PATH for private-marker checks')
            return
        try:
            markers = [line.strip() for line in marker_file.read_text().splitlines() if line.strip() and not line.lstrip().startswith('#')]
            if not markers:
                raise ValueError('marker list is empty')
        except (OSError, ValueError) as exc:
            self.fail('privacy', 'external marker list', str(exc))
            return
        for path in files:
            relative = path.relative_to(self.root)
            if path.is_symlink():
                continue
            for _, index in marker_hits(relative.as_posix(), markers):
                self.fail('private-marker', path, f'filename matches external marker #{index}')
            text = path.read_bytes().decode('utf-8', errors='replace')
            for line, index in marker_hits(text, markers):
                # Do not echo the external marker itself into logs or artifacts.
                self.fail('private-marker', f'{relative}:{line}', f'matches external marker #{index}')

    def links(self, files: list[Path]) -> dict[str, list[str]]:
        external = {}
        for path in files:
            if path.suffix != '.md' or path.parent in {self.root / 'tools/templates', self.root / 'tools/bodies'}:
                continue
            text = path.read_text()
            for line, target in markdown_links(text):
                where = f'{path.relative_to(self.root)}:{line}'
                scheme = urlsplit(target).scheme
                if scheme in {'http', 'https'}:
                    external.setdefault(target, []).append(where)
                    continue
                if scheme == 'mailto':
                    continue
                if scheme:
                    self.fail('link', where, f'unsupported or missing link: {target}')
                    continue
                destination, fragment = local_target(path, target)
                if not destination.is_relative_to(self.root) or not destination.exists():
                    self.fail('link', where, f'missing or external local destination: {target}')
                elif fragment and destination.is_file() and destination.suffix == '.md' and fragment not in heading_ids(destination.read_text()):
                    self.fail('link', where, f'missing local heading: {target}')
        return external

    def web(self, external: dict[str, list[str]], cache: Cache) -> None:
        for url, locations in sorted(external.items()):
            page = cache.pages[urldefrag(url)[0]]
            if page.get('error'):
                self.fail('web-link', locations[0], f"{url}: {page['error']} ({len(locations)} reference(s))")
                continue
            fragment = unquote(urlsplit(url).fragment)
            if fragment and not fragment.startswith(':~:text='):
                if page.get('content_type') == 'text/html':
                    parsed = PageText()
                    parsed.feed(page['text'])
                    anchors = parsed.ids
                else:
                    anchors = heading_ids(page['text'])
                if fragment not in anchors and 'user-content-' + fragment not in anchors:
                    self.fail('web-fragment', locations[0], f'{url}: fragment not found in fetched page ({len(locations)} reference(s))')

    def copies(self, catalog: dict, cache: Cache) -> None:
        houses = []
        for skill in enabled(catalog):
            base = self.root / 'skills' / skill['name']
            if skill['kind'] != 'house':
                examples_line(self.root, skill)
                houses.extend(base / example['path'] for example in skill.get('examples', []))
                if skill['kind'] == 'link-only' and skill.get('examples'):
                    houses.extend(base / path for path in EXAMPLE_INDEXES if (base / path).is_file())
                continue
            houses.append(base / 'SKILL.md')
            houses.extend(p for p in (base / 'references').rglob('*')
                          if p.is_file() and p.name not in {'sources.md', 'LICENSE'}
                          and '__pycache__' not in p.relative_to(self.root).parts
                          and p.suffix not in {'.pyc', '.pyo', '.pyd'})
        # Identical shared/related copies still report every affected file.
        bycontent = {}
        for path in houses:
            bycontent.setdefault(path.read_text(), []).append(path)
        # Build house runs once; large wiki and cheat-sheet collections then
        # compare by set intersection instead of repeatedly tokenizing the guides.
        index = {}
        contents = list(bycontent)
        for content_id, text in enumerate(contents):
            tokens, positions = [], []
            for line, content in enumerate(readable(text).splitlines(), 1):
                current = words(content)
                tokens.extend(current)
                positions.extend([line] * len(current))
            for i in range(len(tokens) - 11):
                key = tuple(tokens[i:i + 12])
                index.setdefault(key, set()).add((content_id, positions[i]))
        house_runs = set(index)
        for source in protected_sources(catalog):
            for url in source.get('copy_check_urls', [source['url']]):
                page = cache.pages[urldefrag(url)[0]]
                if page.get('error'):
                    self.fail('copy-source', source['id'], f"{url}: {page['error']}")
                    continue
                source_text = readable(page['text'], page.get('content_type') == 'text/html')
                runs = shingles(source_text)
                if not runs:
                    self.fail('copy-source', source['id'], f'{url}: insufficient readable source text')
                    continue
                hits = set()
                for run in house_runs & runs:
                    hits.update(index[run])
                for content_id, line in sorted(hits):
                    for path in bycontent[contents[content_id]]:
                        self.fail('copy', f'{path.relative_to(self.root)}:{line}', f'12+ words match {source["id"]} ({url})')


def protected_sources(catalog: dict) -> list[dict]:
    return [s for s in catalog['sources'] if s['treatment'] in {'share-alike', 'link-only'} or 'BY-SA' in s['license'] or 'GFDL' in s['license'] or s['id'] in {'shellcheck-wiki', 'wcag22'}]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=DEFAULT_SOURCE)
    parser.add_argument('--markers', type=Path, help='external privacy marker list; an explicitly supplied missing list fails')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--offline', action='store_true', help='require cached pages; never fetch')
    group.add_argument('--refresh', action='store_true', help='replace cached results with a fresh GET per page')
    group.add_argument('--retry-failed', action='store_true', help='retry cached fetch errors once; preserve successful cache entries')
    args = parser.parse_args()
    checks = Checks(ROOT)
    try:
        catalog = read_catalog()
        files = checks.public_files()
        checks.structure(catalog)
        checks.generated(catalog, args.source.resolve())
        default_markers = args.source / 'private/markers.txt'
        checks.privacy(files, args.markers if args.markers is not None else default_markers if default_markers.exists() else None)
        external = checks.links(files)
        urls = set(external)
        for source in protected_sources(catalog):
            urls.update(source.get('copy_check_urls', [source['url']]))
        cache = Cache(ROOT / '.cache/sources', args.offline, args.refresh, args.retry_failed)
        print(f'Checking {len(enabled(catalog))} skills and {len({urldefrag(u)[0] for u in urls})} distinct source/link pages...', flush=True)
        cache.load(urls)
        checks.web(external, cache)
        checks.copies(catalog, cache)
        claude = shutil.which('claude')
        if not claude:
            print('SKIP claude: Claude Code is not installed')
        else:
            for target in ['.'] + [p['source'] for p in marketplace(catalog)['plugins']]:
                result = subprocess.run([claude, 'plugin', 'validate', target], cwd=ROOT, capture_output=True, text=True, timeout=60)
                if result.returncode:
                    checks.fail('claude', target, 'plugin validate failed: ' + ' '.join((result.stdout + result.stderr).split()))
                else:
                    print('PASS claude: plugin validate ' + target)
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        checks.fail('check', '.', str(exc))
    for failure in checks.failures:
        print(failure)
    print(f'{"FAIL" if checks.failures else "PASS"}: {len(checks.failures)} failure(s)')
    return int(bool(checks.failures))


if __name__ == '__main__':
    sys.exit(main())
