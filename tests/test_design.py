"""Exercise the design sync boundary and token propagation without private fixtures."""
import copy
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import unquote, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from common import ROOT, read_catalog, write
from design_tokens import contrast, css_body, filtered_tokens, rename
from sync import public_file, sync_outputs


class DesignSyncTests(unittest.TestCase):
    def setUp(self):
        self.tokens = json.loads((ROOT / 'skills/design-style/references/tokens.json').read_text())

    def filtered(self, data, css=None):
        return filtered_tokens(ROOT, json.dumps(data).encode(), (css if css is not None else css_body(data)).encode())

    def test_metadata_fonts_comments_and_ownership_are_filtered(self):
        data = json.loads(json.dumps(self.tokens).replace('color-owner-', 'color-internal-'))
        data['meta'] = {'name': 'ZEBRA_SECRET', 'extra': {'path': '/example/ZEBRA_SECRET'}}
        data['shared']['font-body'] = 'ZEBRA_SECRET, sans-serif'
        data['shared']['font-mono'] = 'ZEBRA_SECRET, monospace'
        output, css = self.filtered(data, '/* ZEBRA_SECRET */\n' + css_body(data))
        for payload in (output, css):
            self.assertNotIn(b'ZEBRA_SECRET', payload)
            self.assertNotIn(b'color-internal-', payload)
            self.assertIn(b'color-owner-blue-surface', payload)
        self.assertEqual(json.loads(output)['textPairs'], self.tokens['textPairs'])
        self.assertIn(b'--font-body: ui-sans-serif, system-ui, sans-serif;', css)

    def test_sync_propagates_changed_values_and_records_only_token_inputs(self):
        data = copy.deepcopy(self.tokens)
        data['shared']['space-4'] = '1.125rem'
        data['themes']['light']['color-text'] = '#111111'
        skill = next(s for s in read_catalog()['skills'] if s['name'] == 'design-style')
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder)
            write(source / 'design/tokens.json', json.dumps(data))
            write(source / 'design/tokens.css', css_body(data))
            write(source / 'design/our-look.md', 'ZEBRA_SECRET')
            outputs = sync_outputs(ROOT, source, {'skills': [skill]})
        output = json.loads(outputs['skills/design-style/references/tokens.json'])
        self.assertEqual(output['shared']['space-4'], '1.125rem')
        self.assertEqual(output['themes']['light']['color-text'], '#111111')
        css = outputs['skills/design-style/references/tokens.css']
        self.assertIn(b'--space-4: 1.125rem;', css)
        self.assertIn(b'--color-text: #111111;', css)
        manifest = json.loads(outputs['tools/sync-manifest.json'])['skills'][0]
        self.assertEqual(set(manifest['inputs']), {'design/tokens.css', 'design/tokens.json'})
        self.assertEqual(manifest['filter'], 'house-design-tokens-v1')
        self.assertEqual(len(outputs), 3)
        self.assertNotIn(b'ZEBRA_SECRET', b''.join(outputs.values()))

    def test_new_fields_names_and_css_injection_require_review(self):
        mutations = [
            lambda d: d.update(extra='ZEBRA_SECRET'),
            lambda d: d['shared'].update({'unknown-name': '1rem'}),
            lambda d: d['shared'].update({'space-1': '1rem; content: "ZEBRA_SECRET"'}),
            lambda d: d['textPairs'][0].update(note='ZEBRA_SECRET'),
            lambda d: d['themes']['dark'].update({'color-text': 'url(example.test)'}),
        ]
        for mutate in mutations:
            data = copy.deepcopy(self.tokens)
            mutate(data)
            with self.subTest(mutation=mutate), self.assertRaises(ValueError):
                self.filtered(data)

    def test_css_drift_extra_rules_and_missing_theme_fail(self):
        original = css_body(self.tokens)
        for css in (original.replace('140ms', '141ms'), original + '\nbody { color: red; }',
                    original.replace('prefers-color-scheme: dark', 'prefers-color-scheme: light')):
            with self.subTest(css=css[-50:]), self.assertRaises(ValueError):
                self.filtered(self.tokens, css)

    def test_contrast_uses_unrounded_thresholds_for_both_roles(self):
        self.assertEqual(contrast('#000000', '#ffffff'), 21)
        self.assertLess(contrast('#777777', '#ffffff'), 4.5)
        for ratio in (4.499999, 2.999999):
            self.assertIn(round(ratio, 2), (4.5, 3.0))
            # First run fails text; second lets text pass then fails indicators.
            text_count = sum(len(p['backgrounds']) for p in self.tokens['textPairs']) * 2
            values = [ratio] if ratio > 3 else [21] * text_count + [ratio]
            with patch('design_tokens.contrast', side_effect=values), self.assertRaises(ValueError):
                self.filtered(self.tokens)

    def test_both_themes_and_color_role_coverage_are_required(self):
        cases = []
        data = copy.deepcopy(self.tokens)
        data['themes']['dark']['color-text'] = data['themes']['dark']['color-sheet']
        cases.append(data)
        data = copy.deepcopy(self.tokens)
        data['nonTextPairs'].pop()
        cases.append(data)
        data = copy.deepcopy(self.tokens)
        data['textPairs'][0]['backgrounds'].append(data['textPairs'][0]['backgrounds'][0])
        cases.append(data)
        for data in cases:
            with self.assertRaises(ValueError):
                self.filtered(data)

    def test_only_allowlisted_design_inputs_and_no_symlinks(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder)
            for relative in ('design/our-look.md', 'design/company.md', 'design/tokens.css', 'private/value'):
                write(source / relative, 'fixture')
            for relative in ('design/our-look.md', 'design/company.md', 'design/../private/value'):
                with self.subTest(path=relative), self.assertRaises(ValueError):
                    public_file(source, relative)
            (source / 'design/tokens.json').symlink_to(source / 'private/value')
            with self.assertRaises(ValueError):
                public_file(source, 'design/tokens.json')

    def test_public_name_collisions_fail(self):
        with self.assertRaises(ValueError):
            rename({'color-internal-blue-text': 'one', 'color-owner-blue-text': 'two'})

    def test_example_css_uses_defined_tokens_and_current_breakpoints(self):
        css = (ROOT / 'skills/design-style/references/examples/examples.css').read_text()
        names = set(self.tokens['shared']) | set(self.tokens['themes']['light'])
        self.assertLessEqual(set(re.findall(r'var\(--([\w-]+)\)', css)), names)
        for key in ('compact', 'split', 'wide', 'short'):
            self.assertIn(self.tokens['breakpoints'][key], css)
        lengths = set(re.findall(r'\b\d+(?:\.\d+)?rem\b', css))
        self.assertLessEqual(lengths, set(self.tokens['breakpoints'].values()))


class Element:
    def __init__(self, tag, attrs, parent=None):
        self.tag, self.attrs, self.parent = tag, dict(attrs), parent
        self.children, self.text = [], ''

    def descendants(self):
        return [child for item in self.children for child in [item, *item.descendants()]]

    def content(self):
        return self.text + ''.join(child.content() for child in self.children)


class ExampleHTML(HTMLParser):
    """Small tree for local HTML contracts; no browser or extra dependency."""
    void = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.root = Element('document', [])
        self.stack = [self.root]
        self.feed(text)
        self.nodes = self.root.descendants()
        self.ids = {e.attrs['id']: e for e in self.nodes if 'id' in e.attrs}

    def handle_starttag(self, tag, attrs):
        item = Element(tag, attrs, self.stack[-1])
        self.stack[-1].children.append(item)
        if tag not in self.void:
            self.stack.append(item)

    def handle_endtag(self, tag):
        if self.stack[-1].tag != tag:
            raise ValueError(f'mismatched end tag: {tag}')
        self.stack.pop()

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.void:
            self.handle_endtag(tag)

    def handle_data(self, data):
        self.stack[-1].text += data


class DesignExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = ROOT / 'skills/design-style'
        skill = next(s for s in read_catalog()['skills'] if s['name'] == 'design-style')
        cls.listed = [cls.base / example['path'] for example in skill['examples']]
        cls.pages = {p: ExampleHTML(p.read_text()) for p in cls.listed if p.suffix == '.html'}

    def test_catalog_covers_all_local_html_and_shared_styles(self):
        self.assertEqual(set(self.pages), set((self.base / 'references/examples').glob('*.html')))
        for path, page in self.pages.items():
            with self.subTest(page=path.name):
                self.assertEqual(len(page.stack), 1)
                self.assertEqual({e.attrs.get('href') for e in page.nodes if e.tag == 'link'},
                                 {'../tokens.css', 'examples.css'})
                self.assertFalse(any('style' in e.attrs or e.tag == 'style' for e in page.nodes))

    def test_ids_labels_aria_and_local_destinations(self):
        for path, page in self.pages.items():
            with self.subTest(page=path.name):
                ids = [e.attrs['id'] for e in page.nodes if 'id' in e.attrs]
                self.assertEqual(len(ids), len(set(ids)), 'duplicate IDs')
                for element in page.nodes:
                    attrs = element.attrs
                    for key in ('aria-labelledby', 'aria-describedby', 'aria-controls', 'aria-activedescendant', 'for', 'headers'):
                        for target in attrs.get(key, '').split():
                            self.assertIn(target, page.ids, f'{element.tag} {key}={target}')
                    if 'tabindex' in attrs:
                        self.assertIn(attrs['tabindex'], ('-1', '0'))
                    if element.tag in {'input', 'select', 'textarea'} and attrs.get('type') != 'hidden':
                        self.assertTrue(any(e.tag == 'label' and e.attrs.get('for') == attrs.get('id')
                                            and e.content().strip() for e in page.nodes), 'visible field label')
                    if element.tag in {'a', 'button'}:
                        self.assertTrue(attrs.get('aria-label') or attrs.get('aria-labelledby') or element.content().strip())
                    if element.tag == 'button':
                        self.assertEqual(attrs.get('type'), 'button')
                    if attrs.get('role') == 'region':
                        self.assertTrue(attrs.get('aria-label') or attrs.get('aria-labelledby'))
                    if 'aria-current' in attrs:
                        self.assertEqual(element.tag, 'a')
                        self.assertEqual(attrs['aria-current'], 'page')
                    for key in ('href', 'src'):
                        if key not in attrs:
                            continue
                        url = urlsplit(attrs[key])
                        self.assertFalse(url.scheme or url.netloc, 'remote dependency or destination')
                        self.assertTrue(url.path or url.fragment, 'empty link')
                        target = (path.parent / unquote(url.path)).resolve() if url.path else path.resolve()
                        self.assertTrue(target.is_relative_to(self.base.resolve()))
                        self.assertTrue(target.is_file(), str(target))
                        if url.fragment:
                            target_page = self.pages.get(target) or ExampleHTML(target.read_text())
                            self.assertIn(unquote(url.fragment), target_page.ids)

    def test_every_banner_kind_has_its_paired_tokens_and_inherited_link_ink(self):
        css = (self.base / 'references/examples/examples.css').read_text()
        page = self.pages[self.base / 'references/examples/feedback.html']
        for kind in ('success', 'caution', 'warning', 'error'):
            with self.subTest(kind=kind):
                block = re.search(r'\.notice-' + kind + r'\s*\{([^}]+)\}', css)[1]
                self.assertIn(f'color: var(--color-{kind}-text)', block)
                self.assertIn(f'background: var(--color-{kind}-surface)', block)
                banners = [e for e in page.nodes if f'notice-{kind}' in e.attrs.get('class', '').split()]
                self.assertTrue(banners)
                for banner in banners:
                    self.assertTrue(any(e.tag == 'a' for e in banner.descendants()))
                    self.assertFalse(any(e.tag == 'button' or 'muted' in e.attrs.get('class', '').split()
                                         for e in banner.descendants()))
        self.assertRegex(css, r'\.notice a\s*\{\s*color: inherit;\s*\}')
        self.assertRegex(css, r'\.notice\s*\{[^}]*border: var\(--border-width\) solid currentColor;')

    def test_each_empty_state_situation_has_explanation_and_recovery(self):
        page = self.pages[self.base / 'references/examples/feedback.html']
        situations = {e.attrs['data-situation']: e for e in page.nodes if 'data-situation' in e.attrs}
        self.assertEqual(set(situations), {'first-use', 'filtered-zero', 'no-permission', 'loading', 'failed-load'})
        for name, section in situations.items():
            children = section.descendants()
            with self.subTest(situation=name):
                self.assertTrue(any(e.tag == 'h2' and e.content().strip() for e in children))
                self.assertTrue(any(e.tag == 'p' and e.content().strip() for e in children))
                if name == 'loading':
                    self.assertTrue(any(e.attrs.get('role') == 'status' and 'Loading' in e.content() for e in children))
                else:
                    self.assertTrue(any(e.tag == 'a' and e.attrs.get('href') for e in children))
        self.assertTrue(any(e.tag == 'input' and e.attrs.get('value') for e in situations['filtered-zero'].descendants()))
        retry = next(e for e in situations['failed-load'].descendants() if e.content().strip() == 'Try again')
        self.assertEqual(retry.parent, situations['failed-load'], 'boxed retry stays outside the tint')

    def test_table_headers_sort_state_and_named_keyboard_region(self):
        tables = []
        for page in self.pages.values():
            for table in (e for e in page.nodes if e.tag == 'table'):
                tables.append(table)
                descendants = table.descendants()
                self.assertTrue(any(e.tag == 'caption' and e.content().strip() for e in descendants))
                sorted_headers = [e for e in descendants if 'aria-sort' in e.attrs]
                self.assertLessEqual(len(sorted_headers), 1)
                for header in sorted_headers:
                    self.assertEqual(header.tag, 'th')
                    self.assertIn(header.attrs['aria-sort'], ('ascending', 'descending'))
                    self.assertTrue(any(e.tag == 'button' for e in header.descendants()))
                for header in (e for e in descendants if e.tag == 'th'):
                    self.assertIn(header.attrs.get('scope'), ('row', 'col'))
                self.assertEqual(table.parent.attrs.get('role'), 'region')
                self.assertEqual(table.parent.attrs.get('tabindex'), '0')
                self.assertTrue(table.parent.attrs.get('aria-labelledby'))
        self.assertTrue(tables)


if __name__ == '__main__':
    unittest.main()
