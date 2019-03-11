'''Tests for the :mod:`~.cosette.use` module.'''

import pytest

from ..context import valjean  # pylint: disable=unused-import

# pylint: disable=wrong-import-order
from valjean.cosette.use import from_env


def test_missing_task_name_raises(caplog):
    '''Test that :func:`~.from_env` raises an exception if the required task
    name is not present.'''
    env = {}
    with pytest.raises(KeyError):
        from_env(env=env, task_name='task_name', key='key')
    assert "Task 'task_name' is required for argument injection" in caplog.text
    assert 'the task is not in the environment' in caplog.text


def test_missing_key_raises(caplog):
    '''Test that :func:`~.from_env` raises an exception if the required key is
    not present.'''
    env = {'task_name': {}}
    with pytest.raises(KeyError):
        from_env(env=env, task_name='task_name', key='key')
    assert "Task 'task_name' is required for argument injection" in caplog.text
    assert "I could not find the 'key' key" in caplog.text
