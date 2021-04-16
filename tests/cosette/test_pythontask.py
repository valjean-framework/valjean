# Copyright French Alternative Energies and Atomic Energy Commission
# Contributors: Ève le Ménédeu, Davide Mancusi (2021)
# eve.le-menedeu@cea.fr, davide.mancusi@cea.fr
#
# This software is a computer program whose purpose is to analyze and
# post-process numerical simulation results.
#
# This software is governed by the CeCILL license under French law and abiding
# by the rules of distribution of free software. You can use, modify and/ or
# redistribute the software under the terms of the CeCILL license as circulated
# by CEA, CNRS and INRIA at the following URL: http://www.cecill.info.
#
# As a counterpart to the access to the source code and rights to copy, modify
# and redistribute granted by the license, users are provided only with a
# limited warranty and the software's author, the holder of the economic
# rights, and the successive licensors have only limited liability.
#
# In this respect, the user's attention is drawn to the risks associated with
# loading, using, modifying and/or developing or reproducing the software by
# the user in light of its specific status of free software, that may mean that
# it is complicated to manipulate, and that also therefore means that it is
# reserved for developers and experienced professionals having in-depth
# computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling
# the security of their systems and/or data to be ensured and, more generally,
# to use and operate it in the same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

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
        return config.query(sec, opt)
    sec, opt, val = 'tarapia', 'tapioco', 'antani'
    name = 'task'
    task = PythonTask(name, task_with_config, args=(sec, opt),
                      config_kwarg='config')
    config = Config()
    config[sec] = {}
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
