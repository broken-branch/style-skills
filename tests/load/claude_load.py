#!/usr/bin/env python3
"""Repeat the Claude Code load checks: install routes, then skill selection.

Install routes run in a scratch HOME with no model call. Model checks use
`claude -p` in scratch projects under SK_LOAD_WORK (a temporary directory by default).
"""
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

from load_common import (COMMIT_ASK, GO_ASK, GO_SKILLS, PY_ASK, PYTHON_SKILLS, ROOT,
                         Results, WORK, project, run, scratch_home, skill_reads,
                         staged_change, verdict)
import yaml

MODEL = 'claude-sonnet-5-5'
GO_MOD = {'go.mod': 'module example.com/demo\n\ngo 1.22\n'}
ALL = sorted(p.name for p in (ROOT / 'skills').iterdir() if (p / 'SKILL.md').exists())
results = Results('claude')


class LoadCheckError(RuntimeError):
    """A CLI or model failure that cannot produce a load verdict."""


def install_routes() -> None:
    home, env = scratch_home()
    try:
        steps = [
            ('marketplace', ['claude', 'plugin', 'marketplace', 'add', str(ROOT)], 'Successfully added'),
            ('plugin go', ['claude', 'plugin', 'install', 'go@style-skills'], 'Successfully installed'),
            ('plugin house-style', ['claude', 'plugin', 'install', 'house-style@style-skills'], 'Successfully installed'),
        ]
        for route, cmd, expect in steps:
            out = run(cmd, home / 'work', env)
            results.add(route, 'install', out.returncode == 0 and expect in out.stdout, ' '.join(cmd),
                        out.stdout.strip().splitlines()[-1] if out.stdout.strip() else out.stderr[-200:])
        out = run(['claude', 'plugin', 'list'], home / 'work', env)
        ok = out.returncode == 0 and all(f'{p}@style-skills' in out.stdout for p in ('go', 'house-style'))
        results.add('plugin go + house-style', 'plugin list', ok, 'claude plugin list', 'both enabled' if ok else out.stdout[-300:])
        out = run(['claude', 'plugin', 'details', 'go'], home / 'work', env)
        ok = out.returncode == 0 and ', '.join(sorted(GO_SKILLS)) in out.stdout
        results.add('plugin go', 'plugin details', ok, 'claude plugin details go',
                    next((l.strip() for l in out.stdout.splitlines() if 'Skills (' in l), out.stdout[-200:]))
        out = run(['claude', 'plugin', 'details', 'house-style'], home / 'work', env)
        ok = out.returncode == 0 and 'Skills (14)' in out.stdout
        results.add('plugin house-style', 'plugin details', ok, 'claude plugin details house-style',
                    next((l.strip() for l in out.stdout.splitlines() if 'Skills (' in l), out.stdout[-200:]))
        cmd = ['npx', '-y', 'skills', 'add', str(ROOT), '--skill', 'go-style', '-a', 'claude-code', '-a', 'codex', '-g', '-y']
        out = run(cmd, home / 'work', env)
        target = home / '.claude/skills/go-style/SKILL.md'
        results.add('npx skills add -g', 'install', out.returncode == 0 and target.exists(), ' '.join(cmd),
                    f'~/.claude/skills/go-style -> {Path(home / ".claude/skills/go-style").readlink() if target.exists() else "missing"}')
        dest = home / '.claude/skills/python-style'
        shutil.copytree(ROOT / 'skills/python-style', dest)
        results.add('folder copy', 'install', (dest / 'SKILL.md').exists() and (dest / 'references').is_dir(),
                    'cp -r skills/python-style ~/.claude/skills/', 'SKILL.md, references/ and agents/ in place')
    finally:
        shutil.rmtree(home)


def successful_read_paths(events: list[dict]) -> list[str]:
    """Return paths from Read requests completed by a matching successful result."""
    pending = {}
    paths = []
    for event in events:
        content = event.get('message', {}).get('content', [])
        if not isinstance(content, list):
            continue
        for block in content:
            if block.get('type') == 'tool_use' and block.get('name') == 'Read' and block.get('id'):
                pending[block['id']] = block.get('input', {}).get('file_path')
            elif block.get('type') == 'tool_result':
                path = pending.pop(block.get('tool_use_id'), None)
                if isinstance(path, str) and block.get('is_error', False) is False:
                    paths.append(path)
    return paths


def ask(path: Path, prompt: str, plugins: list[str] = ()) -> tuple[dict, str, set]:
    # The prompt goes first: --allowedTools is variadic and would swallow a trailing prompt.
    cmd = ['claude', '-p', prompt, '--model', MODEL, '--output-format', 'stream-json', '--verbose',
           '--allowedTools', 'Bash(git diff:*)', 'Bash(git status:*)', 'Bash(git log:*)']
    for name in plugins:
        cmd += ['--plugin-dir', str(ROOT / 'plugins' / name)]
    out = run(cmd, path)
    if out.returncode != 0:
        detail = (out.stderr or out.stdout).strip()[-300:]
        raise LoadCheckError(f'claude exited {out.returncode}: {detail}')
    events = [json.loads(l) for l in out.stdout.splitlines() if l.startswith('{')]
    if not events or events[-1].get('type') != 'result':
        raise LoadCheckError('model did not complete with a terminal result')
    failed = [e for e in events if e.get('type') == 'error' or
              (e.get('type') == 'result' and
               (e.get('subtype') != 'success' or e.get('is_error') is not False))]
    if failed:
        raise LoadCheckError('model failure: ' + json.dumps(failed[-1]))
    final = events[-1].get('result')
    if not isinstance(final, str) or not final.strip():
        raise LoadCheckError('model completed without an answer')
    init = next((e for e in events if e.get('subtype') == 'init'), {})
    # The session transcript holds expanded slash commands as well as Skill tool loads.
    transcripts = list(Path.home().glob(f".claude/projects/*/{init.get('session_id')}.jsonl"))
    text = transcripts[0].read_text() if transcripts else out.stdout
    history = [json.loads(line) for line in text.splitlines() if line.startswith('{')] if transcripts else events
    loaded = {Path(m).name for m in re.findall(r'Base directory for this skill: ([^\\"\n]+)', text)}
    loaded |= skill_reads('\n'.join(successful_read_paths(history)), ALL)
    return init, final, loaded


def check(route: str, name: str, path: Path, prompt: str, want: list[str], unwanted: list[str],
          plugins: list[str] = ()) -> str:
    try:
        _, final, loaded = ask(path, prompt, plugins)
        ok, saw = verdict(loaded, want, unwanted)
    except (LoadCheckError, OSError, ValueError, subprocess.SubprocessError) as exc:
        final, ok, saw = '', False, str(exc)
    flags = ''.join(f' --plugin-dir plugins/{p}' for p in plugins)
    results.add(route, name, ok, f'claude -p --model {MODEL}{flags} "{prompt[:60]}..."', saw)
    return final


def commit_checks() -> None:
    commit = project('claude-commit', [], files=GO_MOD)
    staged_change(commit)
    final = check('plugin house-style (--plugin-dir)', 'commit message: code-style', commit, COMMIT_ASK,
                  ['code-style'], [], ['house-style'])
    (WORK / 'claude-commit-message.txt').write_text(final)
    commit = project('claude-commit-copy', ['code-style', 'go-style'], files=GO_MOD)
    staged_change(commit)
    check('project skills (npx/copy equivalent)', 'commit message: code-style', commit, COMMIT_ASK, ['code-style'], [])


def model_checks() -> None:
    plain = project('claude-plain', [], files=GO_MOD)
    go_sources = [s for s in GO_SKILLS if s != 'go-style']
    route = 'plugin go (--plugin-dir)'
    try:
        init, _, _ = ask(plain, 'Reply with OK.', ['go'])
        names = [s for s in init.get('skills', []) if s.startswith('go:')]
        ok, saw = set(names) == {f'go:{s}' for s in GO_SKILLS}, ', '.join(names)
    except (LoadCheckError, OSError, ValueError, subprocess.SubprocessError) as exc:
        ok, saw = False, str(exc)
    results.add(route, 'listing', ok, 'claude -p --plugin-dir plugins/go (init event skills)', saw)
    check(route, 'default Go', plain, GO_ASK, ['go-style'], go_sources, ['go'])
    check(route, 'named: Uber in words', plain, "Use Uber's Go style. " + GO_ASK, ['go-uber-style'], [], ['go'])
    check(route, 'named: /go:go-uber-style', plain, '/go:go-uber-style ' + GO_ASK, ['go-uber-style'], ['go-style'], ['go'])
    check(route, 'named: /go-uber-style', plain, '/go-uber-style ' + GO_ASK, ['go-uber-style'], ['go-style'], ['go'])
    check('plugin house-style (--plugin-dir)', 'default Go', plain, GO_ASK, ['go-style'], go_sources, ['house-style'])

    route = 'project skills (npx/copy equivalent)'
    go = project('claude-go', GO_SKILLS + ['code-style'], files=GO_MOD)
    check(route, 'default Go', go, GO_ASK, ['go-style'], go_sources)
    check(route, 'named: Uber in words', go, "Use Uber's Go style. " + GO_ASK, ['go-uber-style'], [])
    check(route, 'named: /go-uber-style', go, '/go-uber-style ' + GO_ASK, ['go-uber-style'], ['go-style'])

    route = 'plugin python (--plugin-dir)'
    py = project('claude-py', [], files={'pyproject.toml': '[project]\nname = "demo"\nversion = "0.1.0"\n'})
    py_sources = [s for s in PYTHON_SKILLS if s != 'python-style']
    check(route, 'default Python', py, PY_ASK, ['python-style'], py_sources, ['python'])
    check(route, "named: Google's Python in words", py, "Use Google's Python style. " + PY_ASK, ['python-google-style'], [], ['python'])
    check(route, 'named: /python:python-google-style', py, '/python:python-google-style ' + PY_ASK,
          ['python-google-style'], ['python-style'], ['python'])

    commit_checks()

    route = f'all {len(ALL)} skills (project)'
    every = project('claude-all', ALL, files=GO_MOD)
    try:
        init, _, _ = ask(every, 'Reply with OK.')
        missing = [s for s in ALL if s not in init.get('skills', [])]
        ok, saw = not missing, f'{len(ALL) - len(missing)}/{len(ALL)} listed'
    except (LoadCheckError, OSError, ValueError, subprocess.SubprocessError) as exc:
        ok, saw = False, str(exc)
    results.add(route, 'listing', ok, 'claude -p (init event skills)', saw)
    check(route, 'default Go', every, GO_ASK, ['go-style'], go_sources)
    probe = ['go-style', 'code-style', 'sql-style', 'typescript-style', 'vue-style']
    try:
        _, final, _ = ask(every, 'Without using tools, quote verbatim the description your available-skills list shows '
                          'for each of: ' + ', '.join(probe) + '. One line each as name: description. Then say '
                          'whether go-uber-style appears in that list.')
        descs = {s: yaml.safe_load((ROOT / 'skills' / s / 'SKILL.md').read_text().split('---')[1])['description'] for s in probe}
        cut = [s for s, d in descs.items() if d not in final]
        ok, saw = not cut, 'all quoted in full' if not cut else 'differs: ' + ', '.join(cut)
    except (LoadCheckError, OSError, ValueError, subprocess.SubprocessError) as exc:
        ok, saw = False, str(exc)
    results.add(route, 'descriptions not cut', ok, 'claude -p "quote verbatim the description ..."', saw)



def main() -> int:
    if sys.argv[1:] == ['commit']:
        commit_checks()
        return results.save('commit')
    if 'model' not in sys.argv[1:]:
        install_routes()
    if 'install' not in sys.argv[1:]:
        model_checks()
    return results.save('-'.join(sys.argv[1:]) or 'all')


if __name__ == '__main__':
    sys.exit(main())
