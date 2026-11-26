"""Offline load-harness regressions; every CLI invocation is mocked."""
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent / 'load'))
import codex_load
import load_common


def completed(returncode=0, stdout='', stderr=''):
    return subprocess.CompletedProcess(['mocked-codex'], returncode, stdout, stderr)


def prompt_listing(entries):
    return json.dumps({'prompt': '\n' + '\n'.join(
        f'- {name}: {description} (file: /mock/{name}/SKILL.md)'
        for name, description in entries.items())})


READ = {'type': 'item.completed', 'item': {
    'type': 'command_execution', 'command': 'cat .agents/skills/go-style/SKILL.md', 'exit_code': 0}}
ANSWER = {'type': 'item.completed', 'item': {'type': 'agent_message', 'text': 'Here is the code.'}}
DONE = {'type': 'turn.completed'}
FAILED = {'type': 'turn.failed', 'error': {'message': 'simulated model failure'}}


class CodexLoadTests(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.work = Path(scratch.name)
        self.results = codex_load.Results('codex')
        self.entries = {name: codex_load.description(name.split(':')[-1])
                        for name in codex_load.EXPECTED}
        for target, value in [('load_common.WORK', self.work), ('codex_load.WORK', self.work),
                              ('codex_load.results', self.results), ('sys.stdout', io.StringIO())]:
            mock = patch(target, value)
            mock.start()
            self.addCleanup(mock.stop)
        home = patch.object(codex_load.Path, 'home', return_value=self.work)
        home.start()
        self.addCleanup(home.stop)
        cli = patch.object(codex_load, 'run', side_effect=self.successful_cli)
        self.run = cli.start()
        self.addCleanup(cli.stop)

    def successful_cli(self, cmd, *args):
        return completed(stdout=prompt_listing(self.entries) if cmd[1:3] == ['debug', 'prompt-input'] else '')

    def assert_failed(self):
        self.assertEqual([row['result'] for row in self.results.rows], ['fail'])
        self.assertEqual(self.results.save('mocked'), 1)

    def test_audit_failed_installs_and_empty_listing_cannot_pass(self):
        self.run.side_effect = None
        self.run.return_value = completed(1, stderr='simulated CLI failure')
        with patch.object(codex_load, 'listing', return_value={}) as listing:
            codex_load.many_installed()
        self.assert_failed()
        listing.assert_not_called()
        self.assertIn('exited 1', self.results.rows[0]['saw'])

    def test_each_install_failure_rejects_an_otherwise_complete_listing(self):
        for failed_command in range(len(codex_load.PLUGINS) + 1):
            with self.subTest(failed_command=failed_command):
                self.results.rows.clear()
                self.run.reset_mock()
                def cli(cmd, *args):
                    if self.run.call_count == failed_command + 1:
                        return completed(1, stderr='simulated install failure')
                    return self.successful_cli(cmd, *args)
                self.run.side_effect = cli
                codex_load.many_installed()
                self.assert_failed()
                self.assertEqual(self.run.call_count, failed_command + 1)

    def test_empty_or_partial_successful_listing_cannot_pass(self):
        complete = self.entries.copy()
        for omitted in (set(complete), {'go-style'}, {'house-style:go-style'}, {'go:go-style'}):
            with self.subTest(omitted=sorted(omitted)):
                self.results.rows.clear()
                self.entries = {name: desc for name, desc in complete.items() if name not in omitted}
                codex_load.many_installed()
                self.assert_failed()
                self.assertIn('missing advertised house skills:', self.results.rows[0]['saw'])

    def test_failed_listing_with_valid_output_cannot_pass(self):
        def cli(cmd, *args):
            out = self.successful_cli(cmd, *args)
            if cmd[1:3] == ['debug', 'prompt-input']:
                out.returncode = 1
            return out
        self.run.side_effect = cli
        codex_load.many_installed()
        self.assert_failed()

    def test_invalid_listing_json_cannot_pass(self):
        self.run.side_effect = None
        self.run.return_value = completed(stdout='not JSON')
        codex_load.many_installed()
        self.assert_failed()

    def test_complete_listing_passes_and_changed_description_fails(self):
        self.entries['unrelated-system-skill'] = 'An unrelated tool.'
        codex_load.many_installed()
        self.assertEqual([row['result'] for row in self.results.rows], ['pass'])
        self.assertEqual(self.results.save('mocked'), 0)
        self.results.rows.clear()
        self.entries['house-style:go-style'] = 'truncated'
        codex_load.many_installed()
        self.assert_failed()

    def model_check(self, events, returncode=0, want=None, unwanted=None):
        self.run.side_effect = None
        self.run.return_value = completed(returncode, '\n'.join(json.dumps(e) for e in events),
                                          'simulated model failure' if returncode else '')
        return codex_load.check('mocked', 'model selection', self.work, 'Write code.',
                                ['go-style'] if want is None else want, unwanted or [])

    def test_audit_skill_read_followed_by_failed_turn_cannot_pass(self):
        with patch.object(codex_load, 'verdict') as verdict:
            answer = self.model_check([READ, FAILED], returncode=1)
        self.assertEqual(answer, '')
        verdict.assert_not_called()
        self.assert_failed()

    def test_model_requires_process_completion_turn_success_and_answer(self):
        cases = [
            (1, [READ, ANSWER, DONE]),
            (0, [READ, FAILED]),
            (0, [READ, ANSWER]),
            (0, [READ, DONE]),
            (0, [READ, ANSWER, FAILED, DONE]),
            (0, [READ, ANSWER, DONE, {'type': 'error', 'message': 'stream failed'}]),
            (0, []),
        ]
        for code, events in cases:
            with self.subTest(code=code, events=events):
                self.results.rows.clear()
                with patch.object(codex_load, 'verdict') as verdict:
                    self.assertEqual(self.model_check(events, code), '')
                verdict.assert_not_called()
                self.assert_failed()

    def test_completed_model_turn_still_requires_expected_skill_selection(self):
        self.assertEqual(self.model_check([READ, ANSWER, DONE]), 'Here is the code.')
        self.assertEqual([row['result'] for row in self.results.rows], ['pass'])
        for want, unwanted in [(['python-style'], []), (['go-style'], ['go-style'])]:
            with self.subTest(want=want, unwanted=unwanted):
                self.results.rows.clear()
                self.model_check([READ, ANSWER, DONE], want=want, unwanted=unwanted)
                self.assert_failed()

    def test_audit_failed_skill_read_followed_by_successful_turn_cannot_pass(self):
        read = {'type': 'item.completed', 'item': {
            **READ['item'], 'exit_code': 1, 'aggregated_output': 'No such file or directory'}}
        self.assertEqual(self.model_check([read, ANSWER, DONE]), 'Here is the code.')
        self.assert_failed()
        self.assertEqual(self.results.rows[0]['saw'], 'loaded: none')

    def test_skill_reads_require_an_explicit_zero_exit_code(self):
        for status in [{'exit_code': -9}, {'exit_code': None}, {}]:
            with self.subTest(status=status):
                self.results.rows.clear()
                read = {'type': 'item.completed', 'item': {
                    'type': 'command_execution',
                    'command': 'cat .agents/skills/go-style/references/guide.md', **status}}
                self.model_check([read, ANSWER, DONE])
                self.assert_failed()
                self.assertEqual(self.results.rows[0]['saw'], 'loaded: none')

    def test_failed_unwanted_read_does_not_pollute_successful_skill_evidence(self):
        read = {'type': 'item.completed', 'item': {
            'type': 'command_execution', 'exit_code': 1,
            'command': 'cat .agents/skills/python-style/SKILL.md'}}
        self.model_check([READ, read, ANSWER, DONE], unwanted=['python-style'])
        self.assertEqual([row['result'] for row in self.results.rows], ['pass'])
        self.assertEqual(self.results.rows[0]['saw'], 'loaded: go-style')

    def test_explicit_skill_injection_survives_a_failed_command_read(self):
        rollout = self.work / '.codex/sessions/rollout-mock.jsonl'
        rollout.parent.mkdir(parents=True)
        rollout.write_text(json.dumps({'thread_id': 'mock-thread',
                                       'text': '<skill>\n<name>go-style</name>\n</skill>'}))
        read = {'type': 'item.completed', 'item': {**READ['item'], 'exit_code': 1}}
        for thread, expected in [('mock-thread', 'pass'), ('different-thread', 'fail')]:
            with self.subTest(thread=thread):
                self.results.rows.clear()
                self.model_check([{'type': 'thread.started', 'thread_id': thread}, read, ANSWER, DONE])
                self.assertEqual([row['result'] for row in self.results.rows], [expected])


if __name__ == '__main__':
    unittest.main()
