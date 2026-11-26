"""Shared helpers for the Claude Code and Codex load checks.

Install routes run in a scratch HOME and never call a model. Model checks run
in scratch projects with project-level skill copies, under the real sign-in.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(os.environ['SK_LOAD_WORK']) if 'SK_LOAD_WORK' in os.environ else Path(tempfile.mkdtemp(prefix='style-load-'))
_SKILLS = json.loads((ROOT / 'tools/catalog.json').read_text())['skills']
GO_SKILLS = [s['name'] for s in _SKILLS if s['status'] == 'enabled' and s['language'] == 'go']
PYTHON_SKILLS = [s['name'] for s in _SKILLS if s['status'] == 'enabled' and s['language'] == 'python']
GO_ASK = 'Write a small Go function Reverse(s string) string for package demo, as it would go in strutil.go. Print the code; do not write files.'
PY_ASK = 'Write a small Python function slugify(text) for slug.py. Print the code; do not write files.'
COMMIT_ASK = 'Write a commit message for the staged change. Print it only; do not commit.'


class Results:
    def __init__(self, tool: str):
        self.tool = tool
        self.rows = []

    def add(self, route: str, check: str, ok: bool, command: str, saw: str) -> None:
        self.rows.append({'tool': self.tool, 'route': route, 'check': check,
                          'result': 'pass' if ok else 'fail', 'command': command, 'saw': saw})
        print(f"{'PASS' if ok else 'FAIL'} {self.tool} | {route} | {check} | {saw}", flush=True)

    def save(self, mode: str) -> int:
        path = WORK / f'results-{self.tool}-{mode}.json'
        path.write_text(json.dumps(self.rows, indent=1))
        print(f'wrote {path}')
        return sum(row['result'] == 'fail' for row in self.rows)


def run(cmd: list[str], cwd: Path, env: dict | None = None, timeout: int = 600) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, env=env, stdin=subprocess.DEVNULL, capture_output=True,
                          text=True, timeout=timeout)


def scratch_home() -> tuple[Path, dict]:
    """Return a scratch HOME and an environment that points both tools at it."""
    WORK.mkdir(parents=True, exist_ok=True)
    home = Path(tempfile.mkdtemp(prefix='scratchhome.', dir=WORK))
    env = dict(os.environ, HOME=str(home), CLAUDE_CONFIG_DIR=str(home / '.claude'),
               CODEX_HOME=str(home / '.codex'))
    (home / '.codex').mkdir()
    (home / 'work').mkdir()
    return home, env



def project(name: str, skills: list[str], files: dict | None = None) -> Path:
    """Create WORK/proj-<name> afresh with project-level copies for both tools."""
    path = WORK / f'proj-{name}'
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)
    run(['git', 'init', '-q'], path)
    for folder in ('.claude/skills', '.agents/skills'):
        (path / folder).mkdir(parents=True)
        for skill in skills:
            shutil.copytree(ROOT / 'skills' / skill, path / folder / skill)
    for rel, text in (files or {}).items():
        (path / rel).parent.mkdir(parents=True, exist_ok=True)
        (path / rel).write_text(text)
    return path


def staged_change(path: Path) -> None:
    """Commit a base file, then stage a small fix for the commit-message check."""
    git = ['git', '-c', 'user.name=load', '-c', 'user.email=load@example.invalid']
    (path / 'stack.go').write_text(
        'package demo\n\n// Pop removes the top item.\nfunc Pop(s []int) []int {\n\treturn s[:len(s)-1]\n}\n')
    run(git + ['add', 'stack.go'], path)
    run(git + ['commit', '-q', '-m', 'Add Pop'], path)
    (path / 'stack.go').write_text(
        'package demo\n\n// Pop removes the top item. It returns s unchanged when s is empty.\n'
        'func Pop(s []int) []int {\n\tif len(s) == 0 {\n\t\treturn s\n\t}\n\treturn s[:len(s)-1]\n}\n')
    run(git + ['add', 'stack.go'], path)


def skill_reads(text: str, names: list[str]) -> set[str]:
    """Names whose SKILL.md or references a command or tool call opened."""
    return {n for n in names if re.search(rf'/{re.escape(n)}/(SKILL\.md|references/)', text)}


def verdict(loaded: set[str], want: list[str], unwanted: list[str]) -> tuple[bool, str]:
    ok = all(n in loaded for n in want) and not any(n in loaded for n in unwanted)
    return ok, 'loaded: ' + (', '.join(sorted(loaded)) or 'none')
