'''Tests for the :mod:`~.eval_test_task` module.'''

import pytest

# pylint: disable=wrong-import-order,no-value-for-parameter
from ..context import valjean  # pylint: disable=unused-import
from valjean.cosette.task import TaskStatus
from valjean.gavroche.test import TestResult
from valjean.gavroche.eval_test_task import EvalTestTask


def test_valid_test_eval(valid_tests):
    '''Test that :class:`~.EvalTestTask` correctly evaluates :class:`~.Test`
    objects.'''
    eval_test_task = EvalTestTask('eval-test_task', 'test_task')
    env = {'test_task': {'result': valid_tests}}
    env_up, status = eval_test_task.do(env=env, config=None)
    assert status == TaskStatus.DONE
    assert 'eval-test_task' in env_up
    env_result = env_up['eval-test_task']
    assert 'result' in env_up['eval-test_task']
    test_results = env_result['result']
    for test_result in test_results:
        assert isinstance(test_result, TestResult)


def test_wrong_type_fails(invalid_tests):
    '''Test that :class:`~.EvalTestTask` raises the correct exceptions when the
    task that is supposed to produce the tests actually produced garbage.'''
    eval_test_task = EvalTestTask('eval-test_task', 'test_task')
    env = {'test_task': {'result': invalid_tests}}
    with pytest.raises(TypeError):
        eval_test_task.do(env=env, config=None)
