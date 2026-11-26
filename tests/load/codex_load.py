#!/usr/bin/env python3
"""Repeat the Codex load checks: install routes, then skill selection.

Install routes run in a scratch HOME (CODEX_HOME inside it) with no model call;
`codex debug prompt-input` shows the skill list the model would see. Model
checks use `codex exec -s read-only` in scratch projects under SK_LOAD_WORK.
"""
import json
from pathlib import Path
import re
import shutil
import sys

from load_common import (COMMIT_ASK, GO_ASK, GO_SKILLS, PY_ASK, PYTHON_SKILLS, ROOT,
                         Results, WORK, project, run, scratch_home, skill_reads,
                         staged_change, verdict)
import yaml

EFFORT = 'model_reasoning_effort="low"'
GO_MOD = {'go.mod': 'module example.com/demo\n\ngo 1.22\n'}
ALL = sorted(p.name for p in (ROOT / 'skills').iterdir() if (p / 'SKILL.md').exists())
PLUGINS = [p['name'] for p in json.loads((ROOT / '.claude-plugin/marketplace.json').read_text())['plugins']]
HOUSE = {s['name']: s['language'] for s in json.loads((ROOT / 'tools/catalog.json').read_text())['skills']
         if s['status'] == 'enabled' and s['kind'] == 'house'}
EXPECTED = set(HOUSE) | {f'{plugin}:{name}' for plugin in PLUGINS for name, language in HOUSE.items()
                         if plugin in {'house-style', language}}
LISTED = re.compile(r'^- ([a-z0-9:-]+): (.*) \(file: ', re.M)
results = Results('codex')


class LoadCheckError(RuntimeError):
    """A CLI or model failure that cannot produce a load verdict."""


def checked_run(cmd: list[str], cwd: Path, env: dict | None = None):
    out = run(cmd, cwd, env)
    if out.returncode != 0:
        detail = (out.stderr or out.stdout).strip()[-300:]
        raise LoadCheckError(f'{" ".join(cmd)} exited {out.returncode}: {detail}')
    return out


def description(name: str) -> str:
    return yaml.safe_load((ROOT / 'skills' / name / 'SKILL.md').read_text().split('---')[1])['description']


def listing(home: Path, env: dict) -> dict:
    """The skills list Codex would send the model, as {name: description}."""
    out = checked_run(['codex', 'debug', 'prompt-input', 'hi'], home / 'work', env)
    text = json.dumps(json.loads(out.stdout)).encode().decode('unicode_escape')
    return dict(LISTED.findall(text))


def install_routes() -> None:
    home, env = scratch_home()
    try:
        steps = [
            ('marketplace', ['codex', 'plugin', 'marketplace', 'add', str(ROOT)], 'Added marketplace'),
            ('plugin go', ['codex', 'plugin', 'add', 'go@style-skills'], 'Added plugin'),
            ('plugin house-style', ['codex', 'plugin', 'add', 'house-style@style-skills'], 'Added plugin'),
        ]
        for route, cmd, expect in steps:
            out = run(cmd, home / 'work', env)
            results.add(route, 'install', out.returncode == 0 and expect in out.stdout, ' '.join(cmd),
                        out.stdout.strip().splitlines()[0] if out.stdout.strip() else out.stderr[-200:])
        out = run(['codex', 'plugin', 'list'], home / 'work', env)
        ok = out.returncode == 0 and all(re.search(rf'{p}@style-skills\s+installed, enabled', out.stdout) for p in ('go', 'house-style'))
        results.add('plugin go + house-style', 'plugin list', ok, 'codex plugin list',
                    'read .claude-plugin/marketplace.json; go and house-style installed, enabled' if ok else out.stdout[-300:])
        seen = listing(home, env)
        names = sorted(n for n in seen if n.startswith(('go:', 'house-style:')))
        ok = {'go:go-style'} | {f'house-style:{name}' for name in HOUSE} <= seen.keys() \
            and not any('uber' in n for n in seen)
        results.add('plugin go + house-style', 'model-visible list', ok, 'codex debug prompt-input hi',
                    f'go:go-style plus {len(names) - 1} house-style:* entries; source skills hidden' if ok else ', '.join(names))
        cmd = ['npx', '-y', 'skills', 'add', str(ROOT), '--skill', 'go-style', '-a', 'claude-code', '-a', 'codex', '-g', '-y']
        out = run(cmd, home / 'work', env)
        ok = out.returncode == 0 and (home / '.agents/skills/go-style/SKILL.md').exists()
        results.add('npx skills add -g', 'install', ok, ' '.join(cmd), '~/.agents/skills/go-style (copy)')
        shutil.copytree(ROOT / 'skills/python-style', home / '.agents/skills/python-style')
        seen = listing(home, env)
        results.add('npx skills add -g', 'model-visible list', seen.get('go-style') == description('go-style'),
                    'codex debug prompt-input hi', 'go-style listed from ~/.agents/skills')
        results.add('folder copy', 'model-visible list', seen.get('python-style') == description('python-style'),
                    'cp -r skills/python-style ~/.agents/skills/ && codex debug prompt-input hi',
                    'python-style listed from ~/.agents/skills')
        script = home / '.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py'
        cmd = ['python3', str(script), '--url', f'file://{ROOT}/skills/go-style']
        out = run(cmd, home / 'work', env)
        results.add('$skill-installer local path', 'install', out.returncode == 0 and (home / '.codex/skills/go-style').exists(),
                    'python3 <skill-installer>/scripts/install-skill-from-github.py --url file://.../skills/go-style',
                    (out.stdout + out.stderr).strip()[-300:])
    except (LoadCheckError, ValueError) as exc:
        results.add('install routes', 'model-visible list', False, 'codex debug prompt-input hi', str(exc))
    finally:
        shutil.rmtree(home)


def many_installed() -> None:
    home, env = scratch_home()
    route = f'all {len(ALL)} skills + {len(PLUGINS)} plugins (scratch HOME)'
    try:
        for name in ALL:
            shutil.copytree(ROOT / 'skills' / name, home / '.agents/skills' / name)
        checked_run(['codex', 'plugin', 'marketplace', 'add', str(ROOT)], home / 'work', env)
        for name in PLUGINS:
            checked_run(['codex', 'plugin', 'add', f'{name}@style-skills'], home / 'work', env)
        seen = listing(home, env)
        missing = EXPECTED - seen.keys()
        if missing:
            raise LoadCheckError('missing advertised house skills: ' + ', '.join(sorted(missing)))
        ours = {n: d for n, d in seen.items() if n.split(':')[-1] in ALL}
        cut = [n for n, d in ours.items() if d != description(n.split(':')[-1])]
        results.add(route, 'descriptions not cut', not cut,
                    'codex debug prompt-input hi',
                    f'{len(ours)} entries, {len(ours) - len(cut)} unchanged; {len(seen)} skills listed in all')
    except (LoadCheckError, ValueError) as exc:
        results.add(route, 'descriptions not cut', False, 'codex debug prompt-input hi', str(exc))
    finally:
        shutil.rmtree(home)



def ask(path: Path, prompt: str) -> tuple[str, set]:
    out = checked_run(['codex', 'exec', '-s', 'read-only', '-C', str(path), '-c', EFFORT, '--json', prompt], path)
    events = [json.loads(l) for l in out.stdout.splitlines() if l.startswith('{')]
    failed = [e for e in events if e.get('type') in {'turn.failed', 'error'}]
    if failed:
        raise LoadCheckError('model failure: ' + json.dumps(failed[-1]))
    if not any(e.get('type') == 'turn.completed' for e in events):
        raise LoadCheckError('model did not complete a turn')
    thread = next((e['thread_id'] for e in events if e.get('type') == 'thread.started'), None)
    items = [e['item'] for e in events if e.get('type') == 'item.completed']
    commands = '\n'.join(i.get('command', '') for i in items
                         if i.get('type') == 'command_execution' and i.get('exit_code') == 0)
    final = '\n'.join(i.get('text', '') for i in items if i.get('type') == 'agent_message')
    if not final.strip():
        raise LoadCheckError('model completed without an answer')
    loaded = skill_reads(commands, ALL)
    # Explicit $skill mentions are injected into the session, not read by a command.
    for rollout in sorted((Path.home() / '.codex/sessions').rglob('rollout-*.jsonl'),
                          key=lambda p: p.stat().st_mtime)[-5:]:
        text = rollout.read_text()
        if thread and thread in text:
            loaded |= set(re.findall(r'<skill>(?:\\n|\n)<name>([a-z0-9-]+)</name>', text))
    return final, loaded


def check(route: str, name: str, path: Path, prompt: str, want: list[str], unwanted: list[str]) -> str:
    try:
        final, loaded = ask(path, prompt)
        ok, saw = verdict(loaded, want, unwanted)
    except (LoadCheckError, ValueError) as exc:
        final, ok, saw = '', False, str(exc)
    results.add(route, name, ok, f'codex exec -s read-only -C <proj> "{prompt[:60]}..."', saw)
    return final


def commit_checks() -> None:
    commit = project('codex-commit', ['code-style', 'go-style'], files=GO_MOD)
    staged_change(commit)
    final = check('project skills (.agents/skills)', 'commit message: code-style', commit, COMMIT_ASK, ['code-style'], [])
    (WORK / 'codex-commit-message.txt').write_text(final)


def model_checks() -> None:
    route = 'project skills (.agents/skills)'
    go_sources = [s for s in GO_SKILLS if s != 'go-style']
    go = project('codex-go', GO_SKILLS + ['code-style'], files=GO_MOD)
    check(route, 'default Go', go, GO_ASK, ['go-style'], go_sources)
    check(route, 'named: Uber in words', go, "Use Uber's Go style. " + GO_ASK, ['go-uber-style'], [])
    check(route, 'named: $go-uber-style', go, '$go-uber-style ' + GO_ASK, ['go-uber-style'], ['go-style'])

    py = project('codex-py', PYTHON_SKILLS + ['code-style'],
                 files={'pyproject.toml': '[project]\nname = "demo"\nversion = "0.1.0"\n'})
    py_sources = [s for s in PYTHON_SKILLS if s != 'python-style']
    check(route, 'default Python', py, PY_ASK, ['python-style'], py_sources)
    check(route, "named: Google's Python in words", py, "Use Google's Python style. " + PY_ASK, ['python-google-style'], [])
    check(route, 'named: $python-google-style', py, '$python-google-style ' + PY_ASK,
          ['python-google-style'], ['python-style'])

    commit_checks()

    every = project('codex-all', ALL, files=GO_MOD)
    check(f'all {len(ALL)} skills (project)', 'default Go', every, GO_ASK, ['go-style'], go_sources)



def main() -> int:
    if sys.argv[1:] == ['commit']:
        commit_checks()
        return results.save('commit')
    if 'model' not in sys.argv[1:]:
        install_routes()
        many_installed()
    if 'install' not in sys.argv[1:]:
        model_checks()
    return results.save('-'.join(sys.argv[1:]) or 'all')


if __name__ == '__main__':
    sys.exit(main())
