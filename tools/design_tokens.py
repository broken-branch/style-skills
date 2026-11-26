"""Filter the reviewed house token schema without exporting source prose."""
from __future__ import annotations

import json
from pathlib import Path
import re

from common import json_text

FONTS = {'font-body': 'ui-sans-serif, system-ui, sans-serif',
         'font-mono': 'ui-monospace, monospace'}


def public_name(value: str) -> str:
    # Only the four reviewed ownership slots cross the public boundary.
    return re.sub(r'color-[a-z]+-(blue|purple|green|brown)-(surface|text)',
                  r'color-owner-\1-\2', value)


def rename(value):
    if isinstance(value, dict):
        result = {public_name(k): rename(v) for k, v in value.items()}
        if len(result) != len(value):
            raise ValueError('colliding public token names')
        return result
    if isinstance(value, list):
        return [rename(v) for v in value]
    return public_name(value) if isinstance(value, str) else value


def css_body(data: dict) -> str:
    def block(selector, values, scheme=None):
        rows = [selector + ' {'] + [f'  --{k}: {v};' for k, v in values.items()]
        if scheme:
            rows.append(f'  color-scheme: {scheme};')
        return '\n'.join(rows + ['}'])

    def media(condition, content):
        return f'@media ({condition}) {{\n' + '\n'.join('  ' + line for line in content.splitlines()) + '\n}'

    dark = data['themes']['dark']
    return '\n\n'.join([
        block(':root', data['shared']),
        block(':root,\n:root[data-theme="light"]', data['themes']['light'], 'light'),
        media('prefers-color-scheme: dark', block(':root:not([data-theme="light"]):not([data-theme="dark"])', dark, 'dark')),
        block(':root[data-theme="dark"]', dark, 'dark'),
        media('prefers-reduced-motion: reduce', block(':root', data['reducedMotion'])),
    ]) + '\n'


def contrast(first: str, second: str) -> float:
    def luminance(color):
        rgb = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in rgb]
        return sum(v * w for v, w in zip(linear, (.2126, .7152, .0722)))
    low, high = sorted((luminance(first), luminance(second)))
    return (high + .05) / (low + .05)


def validate(data: dict, profile: dict) -> None:
    def require(condition, message):
        if not condition:
            raise ValueError('design tokens: ' + message)

    require(set(data) == {'meta', 'shared', 'themes', 'reducedMotion', 'breakpoints', 'colorRoles', 'textPairs', 'nonTextPairs'}, 'schema changed; review filter')
    require(set(data['shared']) == set(profile['shared']), 'shared names changed; review filter')
    require(set(data['themes']) == {'light', 'dark'}, 'expected both themes')
    for values in data['themes'].values():
        require(set(values) == set(profile['theme']), 'theme names changed; review filter')
        for key, value in values.items():
            pattern = r'#[0-9a-fA-F]{6}' if key.startswith('color-') else r'[\d.]+(?:px)? [\d.]+px [\d.]+px rgb\(0 0 0 / [\d.]+%\)'
            require(isinstance(value, str) and re.fullmatch(pattern, value), 'unsupported color or shadow')
    for key, value in data['shared'].items():
        require(value == FONTS[key] if key in FONTS else isinstance(value, str) and re.fullmatch(r'(?:-?[\d.]+(?:rem|px|ms|em)?|none|ease)', value), 'unsupported shared value')
    require(set(data['breakpoints']) == {'compact', 'split', 'wide', 'short'}, 'breakpoints changed')
    require(all(isinstance(v, str) and re.fullmatch(r'[\d.]+rem', v) for v in data['breakpoints'].values()), 'invalid breakpoint')
    require(data['reducedMotion'] == {'duration-fast': '0ms', 'duration-panel': '0ms'}, 'reduced motion changed')
    roles = data['colorRoles']
    require(set(roles) == {'foreground', 'background', 'indicator', 'decorative'}, 'color roles changed')
    colors = {k for k in profile['theme'] if k.startswith('color-')}
    require(all(isinstance(v, list) for v in roles.values()), 'invalid role lists')
    listed = [k for names in roles.values() for k in names]
    require(set(listed) == colors and len(listed) == len(colors), 'missing or duplicate color role')
    for field, role, threshold in [('textPairs', 'foreground', 4.5), ('nonTextPairs', 'indicator', 3.0)]:
        pairs = data[field]
        require(isinstance(pairs, list) and pairs, 'empty pair registry')
        seen, fronts, backs = set(), set(), set()
        for pair in pairs:
            require(set(pair) == {'foreground', 'backgrounds'}, 'unexpected pair fields')
            fg = pair['foreground']
            require(fg in roles[role] and isinstance(pair['backgrounds'], list) and pair['backgrounds'], 'invalid foreground or backgrounds')
            fronts.add(fg)
            for bg in pair['backgrounds']:
                require(bg in roles['background'] and (fg, bg) not in seen, 'invalid or duplicate pair')
                seen.add((fg, bg))
                backs.add(bg)
                for theme in data['themes'].values():
                    require(contrast(theme[fg], theme[bg]) >= threshold, 'contrast below unrounded minimum')
        require(fronts == set(roles[role]), 'uncovered foreground role')
        if field == 'textPairs':
            require(backs == set(roles['background']), 'uncovered background role')


def filtered_tokens(root: Path, raw_json: bytes, raw_css: bytes) -> tuple[bytes, bytes]:
    data = rename(json.loads(raw_json))
    # Source metadata is intentionally discarded wholesale, including new fields.
    data['meta'] = {'name': 'House design', 'version': 1,
                    'format': 'Semantic CSS custom properties; use only registered color pairs.',
                    'textContrastMinimum': 4.5, 'nonTextContrastMinimum': 3}
    data['shared'].update(FONTS)
    validate(data, json.loads((root / 'tools/design-token-profile.json').read_text()))
    # Keep the upstream CSS behavior; fail if JSON/CSS or supported selectors drift.
    css = public_name(re.sub(r'/\*.*?\*/', '', raw_css.decode(), flags=re.S)).strip()
    for key, value in FONTS.items():
        css = re.sub(r'--' + key + r':[^;]*;', f'--{key}: {value};', css)
    if re.sub(r'\s+', '', css) != re.sub(r'\s+', '', css_body(data)):
        raise ValueError('design tokens: CSS differs from supported JSON contract')
    header = '/* Filtered by tools/sync.py. See sources.md for transformations and token licensing. */\n\n'
    return json_text(data).encode(), (header + css + '\n').encode()
