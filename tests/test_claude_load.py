"""Offline Claude load-harness regressions; every CLI invocation is mocked."""
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent / 'load'))
import claude_load


INIT = {'type': 'system', 'subtype': 'init', 'session_id': 'mock'}
READ = {'type': 'assistant', 'message': {'content': [
    {'type': 'tool_use', 'id': 'read-1', 'name': 'Read',
     'input': {'file_path': '/mock/go-style/SKILL.md'}},
]}}
READ_OK = {'type': 'user', 'message': {'content': [
    {'type': 'tool_result', 'tool_use_id': 'read-1', 'content': '# Go style\nUse the house rules.'},
]}}
READ_ERROR = {'type': 'user', 'message': {'content': [
    {'type': 'tool_result', 'tool_use_id': 'read-1', 'is_error': True,
     'content': 'File does not exist.'},
]}}
DONE = {'type': 'result', 'subtype': 'success', 'is_error': False, 'result': 'Here is the code.'}
FAILED = {'type': 'result', 'subtype': 'error_during_execution', 'is_error': True,
          'result': 'simulated API failure after skill request'}


class ClaudeInstallTests(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.work = Path(scratch.name)
        root = self.work / 'repo'
        source = root / 'skills/python-style'
        (source / 'references').mkdir(parents=True)
        (source / 'agents').mkdir()
        (source / 'SKILL.md').write_text('# Mock Python skill\n')
        self.results = claude_load.Results('claude')
        self.failed_command = None
        self.outputs = {
            ('claude', 'plugin', 'marketplace', 'add', str(root)): 'Successfully added',
            ('claude', 'plugin', 'install', 'go@style-skills'): 'Successfully installed',
            ('claude', 'plugin', 'install', 'house-style@style-skills'): 'Successfully installed',
            ('claude', 'plugin', 'list'): 'go@style-skills\nhouse-style@style-skills',
            ('claude', 'plugin', 'details', 'go'): ', '.join(sorted(claude_load.GO_SKILLS)),
            ('claude', 'plugin', 'details', 'house-style'): 'Skills (14)',
        }
        for target, value in [('load_common.WORK', self.work), ('claude_load.ROOT', root),
                              ('claude_load.results', self.results), ('sys.stdout', io.StringIO()),
                              ('sys.argv', ['claude_load.py', 'install'])]:
            mock = patch(target, value)
            mock.start()
            self.addCleanup(mock.stop)
        for target, effect in [('claude_load.run', self.cli),
                               ('claude_load.model_checks', AssertionError('unexpected model check')),
                               ('subprocess.run', AssertionError('unexpected real CLI invocation'))]:
            mock = patch(target, side_effect=effect)
            mock.start()
            self.addCleanup(mock.stop)

    def cli(self, cmd, cwd, env):
        if cmd[:4] == ['npx', '-y', 'skills', 'add']:
            # Model only the installer's filesystem result; never run an installer.
            home = Path(env['HOME'])
            target = home / '.agents/skills/go-style'
            target.mkdir(parents=True)
            (target / 'SKILL.md').write_text('# Mock Go skill\n')
            link = home / '.claude/skills/go-style'
            link.parent.mkdir(parents=True)
            link.symlink_to(target, target_is_directory=True)
            return subprocess.CompletedProcess(cmd, 0, '', '')
        command = tuple(cmd)
        code = 1 if command == self.failed_command else 0
        return subprocess.CompletedProcess(cmd, code, self.outputs[command],
                                           'simulated probe failure' if code else '')

    def assert_install_result(self, failed_command=None):
        self.failed_command = tuple(failed_command.split()) if failed_command else None
        self.assertEqual(claude_load.main(), 1 if failed_command else 0)
        self.assertEqual(len(self.results.rows), 8)
        for row in self.results.rows:
            self.assertEqual(row['result'], 'fail' if row['command'] == failed_command else 'pass')
        saved = json.loads((self.work / 'results-claude-install.json').read_text())
        self.assertEqual(saved, self.results.rows)

    def test_failed_plugin_list_with_matching_stdout_fails_suite(self):
        self.assert_install_result('claude plugin list')

    def test_failed_house_style_details_with_matching_stdout_fails_suite(self):
        self.assert_install_result('claude plugin details house-style')

    def test_successful_install_probes_pass_suite(self):
        self.assert_install_result()


class ClaudeLoadTests(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.work = Path(scratch.name)
        self.results = claude_load.Results('claude')
        for target, value in [('claude_load.results', self.results), ('sys.stdout', io.StringIO())]:
            mock = patch(target, value)
            mock.start()
            self.addCleanup(mock.stop)
        home = patch.object(claude_load.Path, 'home', return_value=self.work)
        home.start()
        self.addCleanup(home.stop)
        cli = patch.object(claude_load, 'run')
        self.run = cli.start()
        self.addCleanup(cli.stop)

    def reply(self, events, returncode=0):
        self.run.return_value = subprocess.CompletedProcess(
            ['mocked-claude'], returncode, '\n'.join(json.dumps(e) for e in events),
            'simulated CLI failure' if returncode else '')

    def reply_with_history(self, history, transcript):
        path = self.work / '.claude/projects/mock/mock.jsonl'
        if transcript:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('\n'.join(json.dumps(e) for e in history))
            self.reply([INIT, DONE])
        else:
            path.unlink(missing_ok=True)
            self.reply([INIT, *history, DONE])

    def check(self, want=None, unwanted=None):
        return claude_load.check('mocked', 'model selection', self.work, 'Write code.',
                                 ['go-style'] if want is None else want, unwanted or [])

    def assert_failed(self):
        self.assertEqual([row['result'] for row in self.results.rows], ['fail'])
        with patch('load_common.WORK', self.work):
            self.assertEqual(self.results.save('mocked'), 1)

    def test_audit_skill_request_followed_by_failed_run_cannot_pass(self):
        self.reply([INIT, READ, FAILED], returncode=1)
        with patch.object(claude_load, 'verdict') as verdict:
            self.assertEqual(self.check(), '')
        verdict.assert_not_called()
        self.assert_failed()
        self.assertIn('exited 1', self.results.rows[0]['saw'])

    def test_model_requires_exit_success_terminal_success_and_nonempty_answer(self):
        cases = [
            (1, [INIT, READ, DONE]),
            (0, [INIT, READ, FAILED]),
            (0, [INIT, READ, {**DONE, 'is_error': True}]),
            (0, [INIT, READ, {**DONE, 'subtype': 'error_max_turns'}]),
            (0, [INIT, READ]),
            (0, []),
            *[(0, [INIT, READ, {**DONE, 'result': value}]) for value in ['', ' \n', None, 42, []]],
            *[(0, [INIT, READ, {k: v for k, v in DONE.items() if k != key}])
              for key in ['subtype', 'is_error', 'result']],
        ]
        for code, events in cases:
            with self.subTest(code=code, events=events):
                self.results.rows.clear()
                self.reply(events, code)
                with patch.object(claude_load, 'verdict') as verdict, \
                        patch.object(claude_load, 'skill_reads') as reads:
                    self.assertEqual(self.check(), '')
                verdict.assert_not_called()
                reads.assert_not_called()
                self.assert_failed()

    def test_success_before_failed_or_incomplete_result_cannot_pass(self):
        for tail in [[FAILED], [{'type': 'error', 'message': 'stream failed'}], [READ]]:
            with self.subTest(tail=tail):
                self.results.rows.clear()
                self.reply([INIT, READ, DONE, *tail])
                self.assertEqual(self.check(), '')
                self.assert_failed()

    def test_failed_result_before_success_cannot_pass(self):
        self.reply([INIT, READ, FAILED, DONE])
        self.assertEqual(self.check(), '')
        self.assert_failed()

    def test_malformed_event_json_records_failure(self):
        self.run.return_value = subprocess.CompletedProcess(['mocked-claude'], 0, '{invalid JSON', '')
        self.assertEqual(self.check(), '')
        self.assert_failed()

    def test_cli_startup_failure_and_timeout_are_recorded(self):
        for error in [FileNotFoundError('mocked missing CLI'),
                      subprocess.TimeoutExpired(['mocked-claude'], 600)]:
            with self.subTest(error=error):
                self.results.rows.clear()
                self.run.side_effect = error
                self.assertEqual(self.check(), '')
                self.assert_failed()

    def test_successful_model_still_requires_expected_skill_selection(self):
        self.reply([INIT, READ, READ_OK, DONE])
        self.assertEqual(self.check(), 'Here is the code.')
        self.assertEqual([row['result'] for row in self.results.rows], ['pass'])
        for want, unwanted in [(['python-style'], []), (['go-style'], ['go-style'])]:
            with self.subTest(want=want, unwanted=unwanted):
                self.results.rows.clear()
                self.check(want, unwanted)
                self.assert_failed()

    def test_failed_read_followed_by_successful_answer_fails_from_transcript(self):
        self.reply_with_history([READ, READ_ERROR], transcript=True)
        self.assertEqual(self.check(), DONE['result'])
        self.assert_failed()
        self.assertEqual(self.results.rows[0]['saw'], 'loaded: none')

    def test_failed_read_followed_by_successful_answer_fails_from_stdout(self):
        self.reply_with_history([READ, READ_ERROR], transcript=False)
        self.assertEqual(self.check(), DONE['result'])
        self.assert_failed()
        self.assertEqual(self.results.rows[0]['saw'], 'loaded: none')

    def test_uncompleted_or_unmatched_read_does_not_count_as_loaded(self):
        unmatched = {'type': 'user', 'message': {'content': [
            {**READ_OK['message']['content'][0], 'tool_use_id': 'other-read'},
        ]}}
        without_id = {'type': 'assistant', 'message': {'content': [
            {k: v for k, v in READ['message']['content'][0].items() if k != 'id'},
        ]}}
        for transcript in [False, True]:
            for history in [[], [READ], [READ, unmatched], [without_id, READ_OK], [READ_OK]]:
                with self.subTest(transcript=transcript, history=history):
                    self.results.rows.clear()
                    self.reply_with_history(history, transcript)
                    self.assertEqual(self.check(), DONE['result'])
                    self.assert_failed()
                    self.assertEqual(self.results.rows[0]['saw'], 'loaded: none')

    def test_successful_read_counts_as_loaded(self):
        for transcript in [False, True]:
            for suffix in ['SKILL.md', 'references/guide.md']:
                for status in [{}, {'is_error': False}]:
                    with self.subTest(transcript=transcript, suffix=suffix, status=status):
                        self.results.rows.clear()
                        read = {'type': 'assistant', 'message': {'content': [
                            {**READ['message']['content'][0], 'input': {'file_path': f'/mock/go-style/{suffix}'}},
                        ]}}
                        result = {'type': 'user', 'message': {'content': [
                            {**READ_OK['message']['content'][0], **status},
                        ]}}
                        self.reply_with_history([read, result], transcript)
                        self.assertEqual(self.check(), DONE['result'])
                        self.assertEqual(self.results.rows[0]['result'], 'pass')
                        self.assertEqual(self.results.rows[0]['saw'], 'loaded: go-style')

    def test_successful_retry_counts_as_loaded(self):
        retry = {'type': 'assistant', 'message': {'content': [
            {**READ['message']['content'][0], 'id': 'read-2'},
        ]}}
        for transcript in [False, True]:
            for first, second in [(READ_ERROR, READ_OK), (READ_OK, READ_ERROR)]:
                with self.subTest(transcript=transcript, first=first):
                    self.results.rows.clear()
                    result = {'type': 'user', 'message': {'content': [
                        {**second['message']['content'][0], 'tool_use_id': 'read-2'},
                    ]}}
                    self.reply_with_history([READ, first, retry, result], transcript)
                    self.assertEqual(self.check(), DONE['result'])
                    self.assertEqual(self.results.rows[0]['result'], 'pass')
                    self.assertEqual(self.results.rows[0]['saw'], 'loaded: go-style')

    def test_read_results_match_requests_by_id(self):
        requests = {'type': 'assistant', 'message': {'content': [
            READ['message']['content'][0],
            {'type': 'tool_use', 'id': 'read-2', 'name': 'Read',
             'input': {'file_path': '/mock/python-style/SKILL.md'}},
        ]}}
        responses = {'type': 'user', 'message': {'content': [
            {'type': 'tool_result', 'tool_use_id': 'read-2',
             'content': 'See also /mock/go-style/SKILL.md.'},
            READ_ERROR['message']['content'][0],
        ]}}
        for transcript in [False, True]:
            with self.subTest(transcript=transcript):
                self.results.rows.clear()
                self.reply_with_history([requests, responses], transcript)
                self.assertEqual(self.check(want=['python-style'], unwanted=['go-style']), DONE['result'])
                self.assertEqual(self.results.rows[0]['result'], 'pass')
                self.assertEqual(self.results.rows[0]['saw'], 'loaded: python-style')

    def test_explicit_injection_counts_as_loaded_despite_failed_read(self):
        injection = {'type': 'user', 'message': {
            'content': 'Base directory for this skill: /mock/go-style\n# Go style\nUse the house rules.',
        }}
        for transcript in [False, True]:
            for history in [[injection], [READ, READ_ERROR, injection]]:
                with self.subTest(transcript=transcript, history=history):
                    self.results.rows.clear()
                    self.reply_with_history(history, transcript)
                    self.assertEqual(self.check(), DONE['result'])
                    self.assertEqual(self.results.rows[0]['result'], 'pass')
                    self.assertEqual(self.results.rows[0]['saw'], 'loaded: go-style')

    def test_successful_model_preserves_transcript_skill_injection(self):
        transcript = self.work / '.claude/projects/mock/mock.jsonl'
        transcript.parent.mkdir(parents=True)
        transcript.write_text(json.dumps({'content': 'Base directory for this skill: /mock/go-style\n'}))
        self.reply([INIT, DONE])
        self.assertEqual(self.check(), 'Here is the code.')
        self.assertEqual([row['result'] for row in self.results.rows], ['pass'])
        self.assertEqual(self.results.rows[0]['saw'], 'loaded: go-style')

    def probe_checks(self):
        with patch.object(claude_load, 'project', return_value=self.work), \
                patch.object(claude_load, 'check', return_value=''), \
                patch.object(claude_load, 'commit_checks'):
            claude_load.model_checks()

    def test_failed_listing_and_description_probes_are_recorded_and_continue(self):
        init = {**INIT, 'skills': claude_load.ALL + [f'go:{s}' for s in claude_load.GO_SKILLS]}
        descriptions = '\n'.join(claude_load.yaml.safe_load(
            (claude_load.ROOT / 'skills' / s / 'SKILL.md').read_text().split('---')[1])['description']
            for s in claude_load.ALL)
        for code, ending in [(1, [{**DONE, 'result': descriptions}]), (0, [FAILED]), (0, [])]:
            with self.subTest(code=code, ending=ending):
                self.results.rows.clear()
                self.reply([init, *ending], code)
                self.probe_checks()
                self.assertEqual([row['check'] for row in self.results.rows],
                                 ['listing', 'listing', 'descriptions not cut'])
                self.assertEqual([row['result'] for row in self.results.rows], ['fail'] * 3)

    def test_successful_listing_and_description_probes_still_pass(self):
        init = {**INIT, 'skills': claude_load.ALL + [f'go:{s}' for s in claude_load.GO_SKILLS]}
        descriptions = '\n'.join(claude_load.yaml.safe_load(
            (claude_load.ROOT / 'skills' / s / 'SKILL.md').read_text().split('---')[1])['description']
            for s in claude_load.ALL)
        self.reply([init, {**DONE, 'result': descriptions}])
        self.probe_checks()
        self.assertEqual([row['result'] for row in self.results.rows], ['pass'] * 3)


if __name__ == '__main__':
    unittest.main()
