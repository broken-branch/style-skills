"""Regression tests for public/private boundaries and packaging checks."""
from email.message import Message
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from common import markdown_links, quick_rules, read_catalog, ROOT, TAG, write
from sync import public_file, config_files, rewrite_markdown, sync_outputs
from build import build_outputs, bundle_outputs, examples_line, frontmatter, link_only_body, marketplace, source_body, source_examples, stale_bundle_paths
from check import Cache, Checks, marker_hits, overlap_lines, parse_frontmatter, protected_sources, readable, shingles


class GuardTests(unittest.TestCase):
    def test_sync_rejects_private_research_traversal_and_symlinks(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'code').mkdir()
            (root / 'private').mkdir()
            (root / 'private/secret.md').write_text('ZEBRA_SECRET')
            (root / 'code/secret.md').symlink_to(root / 'private/secret.md')
            for path in ['private/secret.md', 'research/note.md', 'code/../private/secret.md', '/tmp/data', 'code/secret.md']:
                with self.subTest(path=path), self.assertRaises(ValueError):
                    public_file(root, path)

    def test_config_discovery_includes_dotfiles_excludes_samples(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'configs/rust/sample').mkdir(parents=True)
            (root / 'configs/rust/.config').write_text('keep')
            (root / 'configs/rust/sample/file').write_text('omit')
            self.assertEqual(config_files(root, 'rust'), ['configs/rust/.config'])

    def test_markers_are_case_insensitive_words_and_never_echoed(self):
        self.assertEqual(marker_hits('one\nzEbRa_SeCrEt here\nprefixable', ['ZEBRA_SECRET', 'prefix']), [(2, 1)])
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            marker_file = root / 'external.txt'
            marker_file.write_text('ZEBRA_SECRET\n')
            content = root / 'output.md'
            content.write_text('A zebra_secret value')
            checks = Checks(root)
            checks.privacy([content], marker_file)
            self.assertEqual(len(checks.failures), 1)
            self.assertNotIn('zebra_secret', checks.failures[0].lower())
            checks.privacy([], root / 'absent')
            self.assertEqual(len(checks.failures), 2)

    def test_archive_scan_and_privacy_without_external_markers(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in ['README.md', 'HANDOFF.md', 'nested/REPORT.md',
                         'research/input.md', '.cache/page.json', 'review/changes.md']:
                write(root / name, 'content')
            checks = Checks(root)
            with patch('check.subprocess.run') as run:
                run.return_value.returncode = 128
                files = checks.public_files()
            self.assertIn(root / 'research/input.md', files)
            self.assertNotIn(root / '.cache/page.json', files)
            self.assertNotIn(root / 'review/changes.md', files)
            with patch('sys.stdout', new_callable=io.StringIO) as output:
                checks.privacy(files, None)
            self.assertIn('SKIP privacy: no marker list', output.getvalue())
            self.assertEqual(len(checks.failures), 3)

    def test_sync_excludes_run_logs_in_nested_config_roots(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in ['VALIDATION.md', 'nested/REPORT.md', 'nested/.lint',
                         'Test-Guide.ps1', 'accessibility.spec.mjs', 'sample/fixture']:
                write(root / 'configs/example' / name, 'content')
            self.assertEqual(config_files(root, 'example'), ['configs/example/nested/.lint'])

    def test_dotted_release_tags_and_reference_only_copy_sources(self):
        from common import TAG
        self.assertEqual(TAG.findall('[RUST-1.86]'), ['RUST-1.86'])
        sources = [{'id': 'manual', 'treatment': 'reference-only', 'license': 'GFDL-1.3-or-later'},
                   {'id': 'web', 'treatment': 'reference-only', 'license': 'CC-BY-SA-4.0'}]
        self.assertEqual(protected_sources({'sources': sources}), sources)

    def test_twelve_word_overlap_spans_lines_and_markdown(self):
        source = shingles('one two three four five six seven eight nine ten eleven twelve thirteen')
        self.assertEqual(overlap_lines('ONE **two** three four five six\nseven eight nine ten eleven twelve', source), [1])
        self.assertFalse(overlap_lines('one two three four five six seven eight nine ten eleven', source))
        html = '<p>one <em>two</em> three</p><script>ignore me</script>'
        self.assertEqual(readable(html, True).strip(), 'one two three')

    def test_yaml_duplicates_and_unsafe_tags_fail(self):
        for text in ['---\nname: a\nname: b\n---\nbody', '---\nname: !!python/object:bad {}\n---\nbody']:
            with self.subTest(text=text), self.assertRaises(Exception):
                parse_frontmatter(text)

    def test_quick_rules_limit(self):
        text = '## Quick rules\n\n' + '\n'.join('- MUST rule.' for _ in range(26)) + '\n\n## Tooling\n'
        with self.assertRaises(ValueError):
            quick_rules(text)

    def test_link_relocation_does_not_change_rule_text(self):
        mapping = {'code/rust.md': 'references/guide.md', 'code/shared.md': 'references/shared.md', 'configs/rust/rustfmt.toml': 'references/config/rustfmt.toml'}
        text = '- MUST keep this exact rule. [TAG]\n[shared](shared.md) [format](../configs/rust/rustfmt.toml) [sample](../configs/rust/sample/)'
        omissions = []
        output = rewrite_markdown(text, 'code/rust.md', 'references/guide.md', mapping, omissions)
        self.assertTrue(output.startswith('- MUST keep this exact rule. [TAG]\n'))
        self.assertIn('[shared](shared.md)', output)
        self.assertIn('[format](config/rustfmt.toml)', output)
        self.assertIn('sample (upstream-only; not bundled)', output)
        self.assertEqual(len(omissions), 1)

    def test_conflict_ids_removed_without_losing_positions_or_diagnostics(self):
        cases = [
            ('code/python.md',
             "- MUST resolve C01 (width) through Ruff: PEP 8 proposes 79/72, Google 80, and Ruff 88. [PEP8] [GOOGLE-PYTHON] [RUFF-FORMAT]",
             "- MUST resolve differences over width through Ruff: PEP 8 proposes 79/72, Google 80, and Ruff 88. [PEP8] [GOOGLE-PYTHON] [RUFF-FORMAT]"),
            ('code/python.md',
             "- PREFER direct imports under C05, as PEP 8 permits, instead of Google's module-only restriction.",
             "- PREFER direct imports, as PEP 8 permits, instead of Google's module-only restriction."),
            ('code/python.md',
             "- MUST use `type` for aliases in C21, choosing Python 3.12 and `UP040` over Google's `TypeAlias` spelling.",
             "- MUST use `type` for aliases, choosing Python 3.12 and `UP040` over Google's `TypeAlias` spelling."),
            ('code/python.md',
             "- MUST let Ruff's configured quote policy resolve C28, narrowing PEP 8's and Google's freedom without `Q000`.",
             "- MUST let Ruff's configured quote policy resolve the competing styles, narrowing PEP 8's and Google's freedom without `Q000`."),
            ('code/python.md',
             "- MUST allow package exports for C35, following PEP 8/257 instead of `RUF067`'s empty-initializer restriction.",
             "- MUST allow package exports, following PEP 8/257 instead of `RUF067`'s empty-initializer restriction."),
            ('code/python.md',
             "- PREFER cohesion review for C37, following Google over hard `C901` thresholds. Keep `SC2312` and `C100` intact.",
             "- PREFER cohesion review, following Google over hard `C901` thresholds. Keep `SC2312` and `C100` intact."),
            ('code/go.md',
             '- MUST use mixedCaps (C01: Google excludes underscores; Uber prefixes private globals). [GOOGLE-GO] [UBER-GO]',
             '- MUST use mixedCaps (Google excludes underscores; Uber prefixes private globals). [GOOGLE-GO] [UBER-GO]'),
        ]
        for relative, original, expected in cases:
            with self.subTest(relative=relative, original=original):
                omissions = []
                output = rewrite_markdown(original, relative, 'references/guide.md', {}, omissions)
                self.assertEqual(output, expected)
                self.assertEqual(omissions, [])

    def test_conflict_id_rewriting_is_limited_to_python_and_go_guides(self):
        text = 'Resolve C01 (width), choose imports under C05 and aliases in C21 for C35 (C02: both positions); keep `C901` and `SC2312`.'
        for relative in ['code/rust.md', 'code/shared.md', 'code/bash.md', 'configs/python/README.md']:
            with self.subTest(relative=relative):
                self.assertEqual(rewrite_markdown(text, relative, 'references/guide.md', {}, []), text)

    def test_markdown_links_handle_nested_parens_and_fences(self):
        links = list(markdown_links('[call](https://example.org/f(a))\n```\n[x](missing)\n```\n[ref][key]\n[key]: file.md#heading'))
        self.assertIn((1, 'https://example.org/f(a)'), links)
        self.assertIn((5, 'file.md#heading'), links)
        self.assertNotIn((3, 'missing'), links)

    def test_shared_alike_and_restricted_sources_are_all_selected(self):
        catalog = read_catalog()
        ids = {s['id'] for s in protected_sources(catalog)}
        self.assertTrue({'cpp-core', 'effective-rust', 'cube-css', 'gitlab-sql', 'node-practices', 'mdn-css', 'poshcode', 'holywell-sql', 'owasp', 'mdn-a11y', 'shellcheck-wiki', 'wcag22'} <= ids)

    def test_build_is_deterministic_and_marketplace_excludes_planned(self):
        catalog = read_catalog()
        outputs = build_outputs(ROOT, catalog)
        self.assertEqual(outputs, build_outputs(ROOT, catalog))
        for skill in catalog['skills']:
            if skill['status'] == 'enabled' and skill['kind'] != 'house':
                self.assertEqual(outputs[f"skills/{skill['name']}/LICENSE"], (ROOT / skill['license_path']).read_bytes())
        plugins = marketplace(catalog)['plugins']
        self.assertEqual(len(plugins), 14)
        for plugin in plugins:
            name = plugin['name']
            self.assertEqual(plugin['source'], './plugins/' + name)
            self.assertNotIn('skills', plugin)
            manifest = json.loads(outputs[f'plugins/{name}/.claude-plugin/plugin.json'])
            self.assertEqual(manifest['name'], name)
            self.assertNotIn('skills', manifest)
            actual = {p.split('/')[3] for p in outputs if p.startswith(f'plugins/{name}/skills/')}
            expected = {s['name'] for s in catalog['skills'] if s['status'] == 'enabled' and
                        (s['kind'] == 'house' if name == 'house-style' else s['language'] == name)}
            self.assertEqual(actual, expected)
        next(s for s in catalog['skills'] if s['name'] == 'rust-effective-style')['status'] = 'planned'
        self.assertFalse(any('/rust-effective-style/' in path for path in build_outputs(ROOT, catalog)))

    def test_authored_entrypoint_body_survives_repeated_builds(self):
        skill = next(s for s in read_catalog()['skills'] if s['name'] == 'rust-official-style')
        skill = dict(skill, examples=[])  # Preserve the original no-examples fixture.
        body = '# Source\n\nA rule.\n\n---\n\nAnother paragraph.\n'
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            entry = root / skill['body_path']
            write(entry, frontmatter(skill) + '\n' + body)
            for _ in range(3):
                extracted = source_body(root, skill)
                self.assertEqual(extracted, body)
                write(entry, frontmatter(skill) + '\n' + extracted)
            entry.write_text('No frontmatter\n')
            with self.assertRaises(ValueError):
                source_body(root, skill)

    def test_split_source_skills_are_explicit_and_single_source(self):
        import yaml
        expected = {
            'rust-official-style': 'rust-style', 'rust-api-style': 'rust-api',
            'go-official-style': 'effective-go', 'go-review-style': 'go-review',
            'react-official-style': 'react-rules', 'react-effects-style': 'react-effects',
            'python-pep8-style': 'pep8', 'python-pep257-style': 'pep257',
        }
        catalog = read_catalog()
        outputs = build_outputs(ROOT, catalog)
        sources = {s['id']: s for s in catalog['sources']}
        skills = {s['name']: s for s in catalog['skills']}
        for name, sid in expected.items():
            with self.subTest(skill=name):
                skill = skills[name]
                self.assertEqual(skill['source_ids'], [sid])
                self.assertEqual(skill['kind'], 'source')
                for field in ('url', 'version', 'credit_line', 'license', 'license_check_urls'):
                    self.assertEqual(skill[field], sources[sid][field])
                for prefix in ('', f"plugins/{skill['language']}/"):
                    base = f'{prefix}skills/{name}/'
                    front, _ = parse_frontmatter(outputs[base + 'SKILL.md'])
                    self.assertIs(front['disable-model-invocation'], True)
                    policy = yaml.safe_load(outputs[base + 'agents/openai.yaml'])['policy']
                    self.assertIs(policy['allow_implicit_invocation'], False)
                self.assertNotIn(f'plugins/house-style/skills/{name}/SKILL.md', outputs)

    def test_examples_are_linked_and_bundled_but_not_sync_owned(self):
        catalog = read_catalog()
        outputs = build_outputs(ROOT, catalog)
        manifest = json.loads((ROOT / 'tools/sync-manifest.json').read_text())
        synced = {record['skill']: set(record['inputs'].values()) for record in manifest['skills']}
        for skill in catalog['skills']:
            if skill['kind'] != 'house':
                continue  # Source contracts are covered independently below.
            examples = skill.get('examples', [])
            if not examples:
                continue
            with self.subTest(skill=skill['name']):
                self.assertTrue(3 <= len(examples) <= 4)
                base = f"skills/{skill['name']}/"
                self.assertIn(examples_line(ROOT, skill), outputs[base + 'SKILL.md'])
                for example in examples:
                    relative = example['path']
                    self.assertNotIn(relative, synced[skill['name']])
                    for tag in TAG.findall((ROOT / base / relative).read_text()):
                        self.assertIn(tag, catalog['source_tags'])
                        self.assertIn(f'`[{tag}]`', outputs[base + 'references/sources.md'])
                    plugins = ('house-style',) if skill['language'] == 'all' else ('house-style', skill['language'])
                    for plugin in plugins:
                        self.assertEqual(outputs[f'plugins/{plugin}/{base}{relative}'],
                                         (ROOT / base / relative).read_bytes())

    def test_source_examples_are_linked_tagged_and_bundled_but_not_sync_owned(self):
        catalog = read_catalog()
        outputs = build_outputs(ROOT, catalog)
        manifest = json.loads((ROOT / 'tools/sync-manifest.json').read_text())
        synced = {record['skill']: set(record['inputs'].values()) for record in manifest['skills']}
        for skill in catalog['skills']:
            if skill['kind'] == 'house' or skill['status'] != 'enabled':
                continue
            with self.subTest(skill=skill['name']):
                examples = skill.get('examples', [])
                self.assertTrue(2 <= len(examples) <= 3)
                self.assertEqual(len({e['path'] for e in examples}), len(examples))
                base = f"skills/{skill['name']}/"
                references = '\n'.join(p.read_text() for p in (ROOT / base / 'references').rglob('*.md')
                                       if 'examples' not in p.relative_to(ROOT / base).parts)
                self.assertIn(examples_line(ROOT, skill), outputs[base + 'SKILL.md'])
                self.assertEqual(outputs[base + 'SKILL.md'].count('<!-- BEGIN GENERATED EXAMPLES -->'), 1)
                for example in examples:
                    relative = example['path']
                    text = (ROOT / base / relative).read_text()
                    self.assertNotIn(relative, synced.get(skill['name'], set()))
                    tags = re.findall(r'\[([A-Za-z0-9][A-Za-z0-9:_.-]*)\]',
                                      '\n'.join(text.splitlines()[:8]))
                    self.assertTrue(tags, relative)
                    for tag in tags:
                        self.assertRegex(references, r'(?<![\w:.-])' + re.escape(tag) + r'(?![\w:.-])')
                    for tag in TAG.findall(text):
                        self.assertIn(tag, catalog['source_tags'])
                        self.assertIn(catalog['source_tags'][tag]['source_id'], skill['source_ids'])
                        self.assertIn(f'`[{tag}]`', references)
                    bundled = f"plugins/{skill['language']}/{base}{relative}"
                    self.assertEqual(outputs[bundled], (ROOT / base / relative).read_bytes())
                    self.assertNotIn(f'plugins/house-style/{base}{relative}', outputs)
                checks = Checks(ROOT)
                checks.source_examples(skill, catalog)
                self.assertEqual(checks.failures, [])

    def test_source_examples_survive_rebuilds_and_removal(self):
        body = '# Source\n\nA rule.\n\n---\n\nAnother paragraph.\n'
        for skill in read_catalog()['skills']:
            if skill['kind'] == 'house' or skill['status'] != 'enabled':
                continue
            with self.subTest(skill=skill['name']):
                once = source_examples(ROOT, skill, body)
                self.assertTrue(once.startswith(body))
                self.assertEqual(once.count('<!-- BEGIN GENERATED EXAMPLES -->'), 1)
                self.assertIn(examples_line(ROOT, skill), once)
                self.assertEqual(source_examples(ROOT, skill, once), once)
                self.assertEqual(source_examples(ROOT, dict(skill, examples=[]), once), body)
                if skill.get('body_format') == 'skill-markdown' and skill['kind'] == 'source':
                    with tempfile.TemporaryDirectory() as folder:
                        root = Path(folder)
                        entry = root / skill['body_path']
                        write(entry, frontmatter(skill) + '\n' + body)
                        for example in skill['examples']:
                            write(root / 'skills' / skill['name'] / example['path'], '// Fixture.\n')
                        for _ in range(3):
                            extracted = source_body(root, skill)
                            self.assertEqual(extracted, once)
                            write(entry, frontmatter(skill) + '\n' + extracted)
                        self.assertEqual(source_body(root, dict(skill, examples=[])), body)

    def test_source_example_checks_reject_invalid_counts_paths_and_tags(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            base = root / 'skills/demo-style/references'
            reference = '<!-- demo:1 -->\n# section-anchor\n[2.2 Item](https://example.test)\n`[DEMO]`\n`[FOREIGN]`\n'
            write(base / 'rules.md', reference)
            good = '// [demo:1] [section-anchor] [2.2] [DEMO]\n'
            for name in ('first.cc', 'second.cc', 'third.cc', 'fourth.cc'):
                write(base / 'examples' / name, good)
            skill = {'name': 'demo-style', 'source_ids': ['demo'], 'examples': [
                {'path': 'references/examples/first.cc', 'label': 'first'},
                {'path': 'references/examples/second.cc', 'label': 'second'}]}
            catalog = {'source_tags': {'DEMO': {'source_id': 'demo'},
                                       'FOREIGN': {'source_id': 'another'}}}
            for header, expected in [
                (good, None), ('// No citation\n', 'opening comment'),
                ('// [demo:12]\n', 'unknown reference tag'),
                ('// [section-anchors]\n', 'unknown reference tag'),
                ('// [2.20]\n', 'unknown reference tag'),
                ('// [UNKNOWN]\n', 'unregistered, foreign or uncredited'),
                ('// [FOREIGN]\n', 'unregistered, foreign or uncredited'),
                (good + '\n' * 8 + '// [FOREIGN]\n', 'unregistered, foreign or uncredited'),
                ('// No header tag\n' + '\n' * 8 + '// [DEMO]\n', 'opening comment'),
            ]:
                with self.subTest(header=header):
                    write(base / 'examples/first.cc', header)
                    checks = Checks(root)
                    checks.source_examples(skill, catalog)
                    if expected is None:
                        self.assertEqual(checks.failures, [])
                    else:
                        self.assertTrue(any(expected in f for f in checks.failures), checks.failures)
            write(base / 'examples/first.cc', good)
            write(base / 'rules.md', reference.replace('`[DEMO]`', 'DEMO'))
            checks = Checks(root)
            checks.source_examples(skill, catalog)
            self.assertTrue(any('uncredited' in f for f in checks.failures))
            write(base / 'rules.md', reference)
            examples = skill['examples'] + [
                {'path': 'references/examples/third.cc', 'label': 'third'},
                {'path': 'references/examples/fourth.cc', 'label': 'fourth'}]
            for count in (0, 1, 2, 3, 4):
                checks = Checks(root)
                checks.source_examples(dict(skill, examples=examples[:count]), catalog)
                self.assertEqual(bool(checks.failures), count not in (2, 3))
            checks = Checks(root)
            checks.source_examples(dict(skill, examples=[examples[0]] * 2), catalog)
            self.assertTrue(any('distinct' in f for f in checks.failures))
            for path in ('references/examples/missing.cc', '../outside.cc',
                         '/tmp/outside.cc', 'references/rules.md'):
                with self.subTest(path=path), self.assertRaises(ValueError):
                    Checks(root).source_examples(dict(skill, examples=[{'path': path, 'label': 'bad'}]), catalog)

    def test_link_only_examples_do_not_allow_unlisted_source_text(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'repo'
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(
                '.git', '.cache', '__pycache__', '*.py[cod]'))
            catalog = read_catalog(root)
            checks = Checks(root)
            checks.structure(catalog)
            self.assertEqual(checks.failures, [])
            extras = []
            for skill in catalog['skills']:
                if skill['kind'] != 'link-only' or skill['status'] != 'enabled':
                    continue
                for relative in ('references/upstream.md', 'references/examples/unlisted.txt'):
                    path = root / 'skills' / skill['name'] / relative
                    write(path, 'Unreviewed source material.\n')
                    extras.append(path.relative_to(root).as_posix())
            checks.structure(catalog)
            self.assertEqual(set(checks.failures), {
                f'FAIL link-only {path}: link-only skills may not bundle source text' for path in extras})

    def test_source_examples_and_link_only_indexes_are_copy_checked(self):
        phrase = 'one two three four five six seven eight nine ten eleven twelve'
        url = 'https://example.test/source'
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            skills = []
            expected = set()
            for kind in ('source', 'link-only'):
                skill = {'name': kind + '-style', 'kind': kind, 'status': 'enabled', 'examples': [
                    {'path': 'references/examples/original.txt', 'label': 'example'}]}
                skills.append(skill)
                base = root / 'skills' / skill['name']
                write(base / skill['examples'][0]['path'], phrase)
                write(base / 'references/sources.md', phrase)
                write(base / 'references/examples.md', phrase)
                paths = [base / skill['examples'][0]['path']]
                if kind == 'link-only':
                    paths.extend([base / 'references/sources.md', base / 'references/examples.md'])
                expected.update(f'FAIL copy {p.relative_to(root)}:1: 12+ words match restricted ({url})'
                                for p in paths)
            cache = Cache(root / '.cache', offline=True)
            cache.pages[url] = {'text': phrase}
            checks = Checks(root)
            checks.copies({'skills': skills, 'sources': [
                {'id': 'restricted', 'license': 'CC-BY-SA-4.0', 'treatment': 'share-alike', 'url': url}]}, cache)
            self.assertEqual(set(checks.failures), expected)

    def test_example_paths_must_exist_inside_references_examples(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            skill = {'name': 'demo-style', 'examples': []}
            self.assertEqual(examples_line(root, skill), '')
            for path in ('references/examples/missing.html', '../outside.html',
                         '/tmp/outside.html', 'references/guide.md'):
                skill['examples'] = [{'path': path, 'label': 'example'}]
                with self.subTest(path=path), self.assertRaises(ValueError):
                    examples_line(root, skill)

    def test_bundle_copies_preserve_bytes_and_use_fresh_generated_files(self):
        catalog = {'build_version': '1.0.0', 'skills': [
            {'name': 'rust-style', 'language': 'rust', 'kind': 'house', 'status': 'enabled'},
            {'name': 'go-style', 'language': 'go', 'kind': 'house', 'status': 'enabled'}]}
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            write(root / 'skills/rust-style/SKILL.md', 'old')
            write(root / 'skills/rust-style/references/.config', b'\xff\x00\r\n')
            write(root / 'skills/go-style/SKILL.md', 'go')
            outputs = bundle_outputs(root, catalog, {'skills/rust-style/SKILL.md': 'fresh'})
            for name in ('house-style', 'rust'):
                prefix = f'plugins/{name}/skills/rust-style/'
                self.assertEqual(outputs[prefix + 'SKILL.md'], 'fresh')
                self.assertEqual(outputs[prefix + 'references/.config'], b'\xff\x00\r\n')
            self.assertNotIn('plugins/go/skills/rust-style/SKILL.md', outputs)
            (root / 'skills/rust-style/leak').symlink_to(root / 'skills/go-style')
            with self.assertRaises(ValueError):
                bundle_outputs(root, catalog, {})

    def test_bytecode_exclusions_keep_unexpected_authored_files_checked(self):
        phrase = 'one two three four five six seven eight nine ten eleven twelve'
        url = 'https://example.test/source'
        catalog = {'build_version': '1.0.0', 'skills': [
            {'name': 'python-style', 'language': 'python', 'kind': 'house', 'status': 'enabled'}],
            'sources': [{'id': 'restricted', 'license': 'CC-BY-SA-4.0',
                         'treatment': 'share-alike', 'url': url}]}
        artifacts = ['__pycache__/payload', 'nested/__pycache__/notes.txt',
                     'module.pyc', 'nested/module.pyo', 'nested/module.pyd']
        authored = ['unexpected.data', '.hidden', 'nested/module.pyc.txt',
                    '__pycache__-notes/guide.txt']
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            base = root / 'skills/python-style'
            write(base / 'SKILL.md', '# Python\n')
            for relative in artifacts:
                write(base / 'references' / relative, b'\xff\x00')
            for relative in authored:
                write(base / 'references' / relative, phrase)
            outputs = bundle_outputs(root, catalog, {})
            for plugin in ('house-style', 'python'):
                prefix = f'plugins/{plugin}/skills/python-style/'
                self.assertEqual({p.removeprefix(prefix) for p in outputs if p.startswith(prefix)},
                                 {'SKILL.md'} | {'references/' + p for p in authored})
            checks = Checks(root)
            self.assertEqual(set(checks.public_files()),
                             {base / 'SKILL.md'} | {base / 'references' / p for p in authored})
            cache = Cache(root / '.cache/sources', offline=True)
            cache.pages[url] = {'text': phrase}
            checks.copies(catalog, cache)
            self.assertEqual(set(checks.failures), {
                f'FAIL copy skills/python-style/references/{p}:1: 12+ words match restricted ({url})'
                for p in authored})

    def test_python_examples_leave_bundle_outputs_and_checks_unchanged(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'repo'
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(
                '.git', '.cache', '.venv', 'review', '__pycache__', '*.py[cod]'))
            catalog = read_catalog(root)
            before = build_outputs(root, catalog)
            examples = root / 'skills/python-style/references/examples'
            # Exercise ordinary imports even when the outer test runner disables
            # bytecode or redirects its cache outside the example directory.
            env = {k: v for k, v in os.environ.items()
                   if k not in {'PYTHONDONTWRITEBYTECODE', 'PYTHONPYCACHEPREFIX'}}
            result = subprocess.run(
                [sys.executable, '-m', 'unittest', 'discover', '-s', str(examples)],
                cwd=root, env=env, capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(list(examples.rglob('*.pyc')), 'example imports must generate bytecode')
            self.assertEqual(build_outputs(root, catalog), before)
            checks = Checks(root)
            checks.structure(catalog)
            with patch('sys.stdout', new_callable=io.StringIO):
                checks.generated(catalog, root / 'missing-upstream')
            # A local source fixture exercises the real originality scan without
            # requiring the private checkout or downloaded source cache.
            url = 'https://example.test/source'
            cache = Cache(root / '.cache/sources', offline=True)
            cache.pages[url] = {'text': 'one two three four five six seven eight nine ten eleven twelve'}
            checks.copies({**catalog, 'sources': [
                {'id': 'restricted', 'license': 'CC-BY-SA-4.0',
                 'treatment': 'share-alike', 'url': url}]}, cache)
            self.assertEqual(checks.failures, [])

    def test_bundle_checks_reject_extra_skills_escaping_links_and_stale_files(self):
        catalog = {'build_version': '1.0.0', 'skills': [
            {'name': 'rust-style', 'language': 'rust', 'kind': 'house', 'status': 'enabled'}]}
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            write(root / 'skills/rust-style/SKILL.md', '# Rust\n')
            outputs = bundle_outputs(root, catalog, {})
            for path, content in outputs.items():
                write(root / path, content)
            checks = Checks(root)
            checks.bundles(catalog)
            self.assertEqual(checks.failures, [])
            self.assertEqual(stale_bundle_paths(root, outputs), [])
            extra = root / 'plugins/rust/skills/go-style/SKILL.md'
            write(extra, '# Go\n')
            entry = root / 'plugins/rust/skills/rust-style/SKILL.md'
            entry.write_text('[outside](../../../../skills/rust-style/SKILL.md)\n')
            checks.bundles(catalog)
            self.assertTrue(any('discovery differs' in f for f in checks.failures))
            self.assertTrue(any('escaping bundle reference' in f for f in checks.failures))
            self.assertIn(extra, stale_bundle_paths(root, outputs))
            (root / 'plugins/rust/escape').symlink_to(root / 'skills')
            with self.assertRaises(ValueError):
                stale_bundle_paths(root, outputs)

    def test_link_only_workflow_is_independent_of_authored_output(self):
        for skill in read_catalog()['skills']:
            if skill['kind'] != 'link-only':
                continue
            with self.subTest(skill=skill['name']):
                body = link_only_body(ROOT, skill)
                self.assertIn(skill['credit_line'], body)
                self.assertIn(skill['url'], body)
                install = skill['existing_skill']
                if install['status'] in {'found', 'found-related'}:
                    self.assertIn(install['install_line'], body)
                    self.assertIn(install['caveat'], body)
                else:
                    self.assertNotIn('missing:', body)
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            skill = next(s for s in read_catalog()['skills'] if s['name'] == 'sql-gitlab-style')
            shutil.copytree(ROOT / 'tools/templates', root / 'tools/templates')
            shutil.copytree(ROOT / 'skills/sql-gitlab-style', root / 'skills/sql-gitlab-style')
            shutil.copy(ROOT / 'LICENSE-CONTENT', root / 'LICENSE-CONTENT')
            entry = root / skill['body_path']
            write(entry, frontmatter(skill) + '\n' + link_only_body(root, skill) + '\nUnreviewed source text.\n')
            checks = Checks(root)
            checks.structure({'build_version': '1.0.0', 'skills': [skill],
                              'source_tags': read_catalog()['source_tags']})
            self.assertTrue(any('wrapper differs from reviewed' in f for f in checks.failures))

    def test_changed_license_and_invocation_settings_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            import shutil
            shutil.copytree(ROOT / 'skills/rust-style', root / 'skills/rust-style')
            shutil.copy(ROOT / 'LICENSE-CONTENT', root / 'LICENSE-CONTENT')
            catalog = read_catalog()
            catalog['skills'] = [s for s in catalog['skills'] if s['name'] == 'rust-style']
            (root / '.claude-plugin').mkdir()
            (root / '.claude-plugin/marketplace.json').write_text(json.dumps(marketplace(catalog)))
            entry = root / 'skills/rust-style/SKILL.md'
            entry.write_text(entry.read_text().replace('license: CC-BY-4.0', 'license: MIT\ndisable-model-invocation: true'))
            checks = Checks(root)
            checks.structure(catalog)
            self.assertTrue(any('FAIL license' in failure for failure in checks.failures))
            self.assertTrue(any('FAIL invocation' in failure for failure in checks.failures))

    def test_full_copy_check_detects_entrypoint_and_config_prose(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            base = root / 'skills/demo-style'
            (base / 'references/config').mkdir(parents=True)
            phrase = 'one two three four five six seven eight nine ten eleven twelve'
            (base / 'SKILL.md').write_text(phrase)
            (base / 'references/config/settings.toml').write_text('# ' + phrase)
            (base / 'references/sources.md').write_text(phrase)
            (base / 'references/config/LICENSE').write_text(phrase)
            catalog = {'skills': [{'name': 'demo-style', 'kind': 'house', 'status': 'enabled'}], 'sources': [{'id': 'restricted', 'license': 'CC-BY-SA-4.0', 'treatment': 'share-alike', 'url': 'https://example.test/source'}]}
            cache = Cache(root / 'cache', offline=True)
            cache.pages['https://example.test/source'] = {'text': '<p>' + phrase + '</p>', 'content_type': 'text/html'}
            checks = Checks(root)
            checks.copies(catalog, cache)
            self.assertEqual(len(checks.failures), 2)
            self.assertTrue(all('12+ words match restricted' in line for line in checks.failures))

    def test_sync_needs_only_public_input_trees(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder)
            (source / 'code').mkdir()
            (source / 'configs/rust/sample').mkdir(parents=True)
            (source / 'code/shared.md').write_text('shared')
            (source / 'code/rust.md').write_text('rust')
            (source / 'configs/.editorconfig').write_text('root = true')
            (source / 'configs/rust/rustfmt.toml').write_text('max_width = 100')
            (source / 'configs/rust/sample/omitted.rs').write_text('not shipped')
            catalog = {'skills': [{'name': 'rust-style', 'kind': 'house', 'status': 'enabled', 'language': 'rust', 'house_guide_path': 'code/rust.md', 'config_roots': ['rust']}]}
            outputs = sync_outputs(source, source, catalog)
            self.assertEqual(outputs['skills/rust-style/references/guide.md'], b'rust')
            self.assertEqual(outputs['skills/rust-style/references/shared.md'], b'shared')
            self.assertFalse(any('/sample/' in path for path in outputs))
            self.assertFalse((source / 'private').exists())
            self.assertFalse((source / 'research').exists())


class CacheTests(unittest.TestCase):
    def test_fetch_once_defragment_offline_and_failure_cache(self):
        calls = []
        base = 'https://example.test'
        def fetch(request, timeout):
            calls.append(request.full_url)
            if request.full_url.endswith('/missing'):
                raise HTTPError(request.full_url, 404, 'Not Found', {}, None)
            response = io.BytesIO(b'<p>source text</p>')
            response.status, response.url = 200, request.full_url
            response.headers = Message()
            response.headers['Content-Type'] = 'text/html; charset=utf-8'
            return response
        # Exercise real cache I/O and concurrent fetching without requiring a
        # listening socket, which restricted build sandboxes do not permit.
        with tempfile.TemporaryDirectory() as folder, patch('check.urlopen', side_effect=fetch):
            cache = Cache(Path(folder))
            cache.load({base + '/#one', base + '/#two', base + '/missing'})
            self.assertEqual(sorted(calls), [base + '/', base + '/missing'])
            self.assertEqual(cache.pages[base + '/']['text'], '<p>source text</p>')
            offline = Cache(Path(folder), offline=True)
            offline.load({base + '/', base + '/missing', base + '/absent'})
            self.assertEqual(len(calls), 2)
            self.assertEqual(offline.pages[base + '/'], cache.pages[base + '/'])
            self.assertIn('HTTP Error 404', offline.pages[base + '/missing']['error'])
            self.assertIn('error', offline.pages[base + '/absent'])


if __name__ == '__main__':
    unittest.main()
