"""Authored adversarial controls, never independent study evidence."""
import copy
import json
import os
from unittest.mock import patch

from evaluation import planning_02, slicing_04
from intentline.errors import IntentlineError
from intentline.records import canonical, sha
from tests.test_slicing_coverage import CoverageCase


class StudyGuards05(CoverageCase):
    def studies(self):
        from tests.test_evaluation import Evaluation
        from tests.test_slicing_evaluation import SlicingEvaluation
        if not self.setup_split():
            return
        yield planning_02, Evaluation.fixture(self)
        yield slicing_04, SlicingEvaluation.fixture(self)

    def register(self, study):
        raw = canonical({k: study[k] for k in ('phase', 'registered_at', 'arms', 'tasks')})
        (self.root / study['registration']['path']).write_bytes(raw)
        study['registration']['sha256'] = sha(raw)

    def test_gold_alias_and_cross_task_instruction_leaks(self):
        for module, original in self.studies():
            for leak in ('alias', 'other_task', 'instructions', 'review_alias'):
                study = copy.deepcopy(original)
                task = study['tasks'][0]
                private = task['reference'] if leak != 'review_alias' else task['reviews'][0]['record'] if task['reviews'] else task['reference']
                alias = {'path': 'renamed-private.txt', 'sha256': private['sha256']}
                (self.root / alias['path']).write_bytes((self.root / private['path']).read_bytes())
                if leak == 'instructions':
                    study['arms'][module.ARMS[0]]['instructions'] = alias
                else:
                    if leak == 'other_task':
                        other = copy.deepcopy(task)
                        other['id'] = 'other'
                        other['reference'] = None
                        other['eligible'] = False
                        study['tasks'].append(other)
                        for run in copy.deepcopy(study['assignments']):
                            run.update(task='other', blind_id='other-' + run['blind_id'], state='not_run', output=None, scores=[])
                            study['assignments'].append(run)
                        study['blockers'] = ['Authored unexecuted controls']
                        task = other
                    task['context'].append(alias)
                    for run in study['assignments']:
                        if run['task'] == task['id']:
                            run['inputs'] = [task['request']] + task['context'] + ([task['parent']] if 'parent' in task else [])
                self.register(study)
                with self.subTest(evaluator=module.__name__, leak=leak), self.assertRaises(IntentlineError):
                    module.validate(study, self.root)

    def test_late_task_review_and_score_before_registration(self):
        for module, original in self.studies():
            # Add real-shaped review declarations to the development slicing fixture.
            if not original['tasks'][0]['reviews']:
                original['tasks'][0]['reviews'] = [
                    {'actor': 'task-reviewer', 'timestamp': '2026-10-12T00:00:00Z',
                     'conflicts': [], 'corrections': [], 'record': original['tasks'][0]['reference']}]
            for defect in ('late_review', 'early_score'):
                study = copy.deepcopy(original)
                if defect == 'late_review':
                    study['tasks'][0]['reviews'][0]['timestamp'] = '2026-10-13T00:00:00Z'
                else:
                    ref = study['assignments'][0]['scores'][0]
                    score = json.loads((self.root / ref['path']).read_bytes())
                    score['timestamp'] = '2026-10-11T00:00:00Z'
                    raw = canonical(score)
                    (self.root / ref['path']).write_bytes(raw)
                    ref['sha256'] = sha(raw)
                self.register(study)
                with self.subTest(evaluator=module.__name__, defect=defect), self.assertRaises(IntentlineError):
                    module.validate(study, self.root)

    def test_path_types_hashes_and_adverse_assignment_retention(self):
        for module, original in self.studies():
            for kind in ('missing', 'symlink', 'fifo', 'traversal', 'hash', 'failed_missing', 'fake_authentication'):
                study = copy.deepcopy(original)
                target = self.root / 'unsafe.txt'
                if target.exists() or target.is_symlink():
                    target.unlink()
                if kind == 'symlink':
                    target.symlink_to(self.root / study['tasks'][0]['request']['path'])
                elif kind == 'fifo':
                    os.mkfifo(target)
                if kind in ('missing', 'symlink', 'fifo'):
                    study['tasks'][0]['request']['path'] = target.name
                elif kind == 'traversal':
                    study['tasks'][0]['request']['path'] = '../outside'
                elif kind == 'hash':
                    study['tasks'][0]['reference']['sha256'] = '0' * 64
                elif kind == 'failed_missing':
                    study['assignments'][0].update(state='failed', scores=[], output=None)
                    study['assignments'].pop(0)
                else:
                    study['authentication'] = 'external_host_verified'
                self.register(study)
                with self.subTest(evaluator=module.__name__, kind=kind), self.assertRaises((IntentlineError, OSError)):
                    module.validate(study, self.root)

    def test_valid_controls_no_effects_and_not_run_unknowns(self):
        for module, study in self.studies():
            self.register(study)
            with patch('socket.socket', side_effect=AssertionError('network')), patch('subprocess.Popen', side_effect=AssertionError('dispatch')):
                self.assertEqual(module.assess(study, self.root)['authentication'], 'unverified')
                study['blockers'] = ['Authored no-run control']
                for run in study['assignments']:
                    run.update(state='not_run', output=None, scores=[])
                result = module.assess(study, self.root)
            for arm in result['arms'].values():
                self.assertIsNone(arm['adverse_counts'])
                self.assertIsNone(arm['clean_fraction'])
                self.assertTrue(all(value is None for value in arm['usage'].values()))
            study['assignments'][0]['metrics']['cost'] = 0
            with self.assertRaises(IntentlineError):
                module.validate(study, self.root)
