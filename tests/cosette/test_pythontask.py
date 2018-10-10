'''Tests for the :mod:`~.pythontask` module.'''

import pytest

from ..context import valjean  # pylint: disable=unused-import

# pylint: disable=wrong-import-order
from valjean.config import Config
from valjean.cosette.pythontask import PythonTask


def test_return_value():
    '''Test that :class:`~.PythonTask` passes back the return value of the
    function.'''
    def task_func():
        return 42
    name = 'task'
    task = PythonTask(name, task_func)
    ret = task.do(env={}, config=None)
    assert ret == 42


def test_pass_args():
    '''Test that positional args are correctly passed to the function in the
    task.'''
    def sum_args(i, j, k):
        return i + j + k
    i, j, k = 5, 6, 7
    name = 'task'
    task = PythonTask(name, sum_args, args=(i, j, k))
    ret = task.do(env={}, config=None)
    assert ret == i + j + k


def test_pass_kwargs():
    '''Test that keyword args are correctly passed to the function in the
    task.'''
    def sum_kwargs(*, i=None, j=None, k=None):
        return i + j + k
    i, j, k = 5, 6, 7
    kwargs = {'i': i, 'j': j, 'k': k}
    name = 'task'
    task = PythonTask(name, sum_kwargs, kwargs=kwargs)
    ret = task.do(env={}, config=None)
    assert ret == i + j + k


def test_pass_env():
    '''Test that the environment is correctly passed to the function in the
    task.'''
    def task_with_env(key, env):
        return env[key]
    key, value = 'tarapia', 'tapioco'
    name = 'task'
    task = PythonTask(name, task_with_env, args=(key,), env_kwarg='env')
    env = {key: value}
    ret = task.do(env=env, config=None)
    assert ret == value


def test_pass_config():
    '''Test that the configuration is correctly passed to the function in the
    task.'''
    def task_with_config(sec, opt, *, config):
        return config.get(sec, opt)
    sec, opt, val = 'tarapia', 'tapioco', 'antani'
    name = 'task'
    task = PythonTask(name, task_with_config, args=(sec, opt),
                      config_kwarg='config')
    config = Config(paths=[])
    config.add_section(sec)
    config.set(sec, opt, val)
    ret = task.do(env=None, config=config)
    assert ret == val


def test_modify_env_raises():
    '''Test that the function in the task is not allowed to modify the
    environment.'''
    def task_modify_env(env):
        env['tarapia'] = 'tapioco'
    task = PythonTask('task', task_modify_env, env_kwarg='env')
    with pytest.raises(TypeError):
        task.do(env={}, config=None)


def test_del_env_raises():
    '''Test that the function in the task is not allowed to delete keys from
    the environment.'''
    def task_del_env(env):
        del env['tarapia']
    task = PythonTask('task', task_del_env, env_kwarg='env')
    with pytest.raises(TypeError):
        task.do(env={'tarapia': 'tapioco'}, config=None)
