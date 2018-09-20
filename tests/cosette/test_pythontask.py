'''Tests for the :mod:`~.pythontask` module.'''

import pytest

from ..context import valjean  # pylint: disable=unused-import

# pylint: disable=wrong-import-order
from valjean.cosette.task import TaskStatus
from valjean.cosette.pythontask import PythonTask


def test_return_value():
    '''Test that :class:`~.PythonTask` passes back the return value of the
    function.'''
    def task_func():
        return 42
    task = PythonTask('task', task_func)
    env_up, status = task.do({})
    assert env_up == {'task': {'result': 42}}
    assert status == TaskStatus.DONE


def test_pass_args():
    '''Test that positional args are correctly passed to the function in the
    task.'''
    def sum_args(i, j, k):
        return i + j + k
    i, j, k = 5, 6, 7
    task = PythonTask('task', sum_args, args=(i, j, k))
    env_up, status = task.do({})
    assert env_up == {'task': {'result': i + j + k}}
    assert status == TaskStatus.DONE


def test_pass_kwargs():
    '''Test that keyword args are correctly passed to the function in the
    task.'''
    def sum_kwargs(*, i=None, j=None, k=None):
        return i + j + k
    i, j, k = 5, 6, 7
    kwargs = {'i': i, 'j': j, 'k': k}
    task = PythonTask('task', sum_kwargs, kwargs=kwargs)
    env_up, status = task.do({})
    assert env_up == {'task': {'result': i + j + k}}
    assert status == TaskStatus.DONE


def test_pass_env():
    '''Test that the environment is correctly passed to the function in the
    task.'''
    def task_with_env(key, env):
        return env[key]
    key, value = 'tarapia', 'tapioco'
    task = PythonTask('task', task_with_env, args=(key,), env_kwarg='env')
    env = {key: value}
    env_up, status = task.do(env)
    assert env_up == {'task': {'result': value}}
    assert status == TaskStatus.DONE


def test_modify_env_raises():
    '''Test that the function in the task is not allowed to modify the
    environment.'''
    def task_modify_env(env):
        env['tarapia'] = 'tapioco'
    task = PythonTask('task', task_modify_env, env_kwarg='env')
    with pytest.raises(TypeError):
        task.do({})


def test_del_env_raises():
    '''Test that the function in the task is not allowed to delete keys from
    the environment.'''
    def task_del_env(env):
        del env['tarapia']
    task = PythonTask('task', task_del_env, env_kwarg='env')
    with pytest.raises(TypeError):
        task.do({'tarapia': 'tapioco'})
