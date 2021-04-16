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

'''Tests for the :mod:`~valjean.cosette.run` module.'''

import shlex
from pathlib import Path
import pytest

# pylint: disable=wrong-import-order
from .conftest import requires_git, requires_cmake
from ..context import valjean  # pylint: disable=unused-import
from valjean import LOGGER
from valjean.cosette.task import TaskStatus
from valjean.cosette.code import CheckoutTask, BuildTask
from valjean.cosette.run import RunTask, RunTaskFactory


#: Some text used in the tests
TEXT = '''Une araignée sur le plancher se tricotait des bottes
Dans un flacon un limaçon enfilait sa culotte
J'ai vu dans le ciel une mouche à miel pinçant sa guitare
Des rats tout confus sonner l'angélus au son d'la fanfare
'''


def do_test_task(task, env, config):
    '''Run the task with the given config, check the status and return codes
    and return stdout and stderr as strings.'''
    env_up, status = task.do(env=env, config=config)
    assert status == TaskStatus.DONE
    assert env_up[task.name]['return_codes'] == [0]
    stdout = Path(env_up[task.name]['stdout'])
    stderr = Path(env_up[task.name]['stderr'])
    output_dir = config.query('path', 'output-root')
    stdout.relative_to(str(output_dir))  # raises ValueError if impossible
    stderr.relative_to(str(output_dir))  # raises ValueError if impossible
    with stdout.open() as f_out:
        stdout_content = f_out.read()
    with stderr.open() as f_out:
        stderr_content = f_out.read()
    return stdout_content, stderr_content


def test_echo(config_tmp):
    '''Test :class:`~.RunTask` with a simple echo command.'''
    runtask = RunTask.from_cli('echo', ['echo', TEXT])
    stdout, stderr = do_test_task(runtask, {}, config_tmp)
    assert stdout == TEXT + '\n'
    assert stderr == '$ echo ' + shlex.quote(TEXT) + '\n'


@requires_git
def test_factory_checkout(git_myecho_repo, config_tmp, subdir):
    '''Test that :class:`~.RunTaskFactory` produces working `:class:`~.RunTask`
    objects from a :class:`~.CheckoutTask`.
    '''
    checkout = CheckoutTask('checkout_myecho',
                            repository=str(git_myecho_repo))
    myecho_path = str(Path(subdir) / 'myecho')
    factory = RunTaskFactory.from_task(checkout, relative_path=myecho_path)
    env = {}
    env_up, status = checkout.do(env=env, config=config_tmp)
    assert status == TaskStatus.DONE
    env.update(env_up)
    LOGGER.debug('env after checkout: %s', env)
    task = factory.make(name='task', extra_args=(TEXT,))
    stdout, _ = do_test_task(task, env, config_tmp)
    assert stdout == TEXT + '\n'


@requires_cmake
def test_factory_build(cmake_echo, config_tmp, subdir):
    '''Test that :class:`~.RunTaskFactory` produces working `:class:`~.RunTask`
    objects from a :class:`~.BuildTask`.
    '''
    build = BuildTask('build_echo', source=str(cmake_echo))
    cecho_path = str(Path(subdir) / 'cecho')
    factory = RunTaskFactory.from_task(build, relative_path=cecho_path)
    env = {}
    env_up, status = build.do(env=env, config=config_tmp)
    assert status == TaskStatus.DONE
    env.update(env_up)
    LOGGER.debug('env after build: %s', env)
    task = factory.make(name='task', extra_args=(TEXT,))
    stdout, _ = do_test_task(task, env, config_tmp)
    assert stdout == TEXT + '\n'


def test_factory_exe(config_tmp):
    '''Test that :class:`~.RunTaskFactory` produces working `:class:`~.RunTask`
    objects from an existing executable.
    '''
    factory = RunTaskFactory.from_executable('/bin/echo')
    task = factory.make(name='task',
                        extra_args=(TEXT,))
    stdout, stderr = do_test_task(task, {}, config_tmp)
    assert stdout == TEXT + '\n'
    assert stderr == '$ /bin/echo ' + shlex.quote(TEXT) + '\n'


def test_factory_exe_args(config_tmp):
    '''Test that :class:`~.RunTaskFactory` produces working `:class:`~.RunTask`
    objects from an existing executable.
    '''
    factory = RunTaskFactory.from_executable('/bin/echo',
                                             default_args=['{text}'])
    task = factory.make(name='task', text=TEXT)
    stdout, stderr = do_test_task(task, {}, config_tmp)
    assert stdout == TEXT + '\n'
    assert stderr == '$ /bin/echo ' + shlex.quote(TEXT) + '\n'


def test_factory_exe_raise_missing(config_tmp):
    '''Test that :class:`~.RunTaskFactory` raises if required run arguments are
    missing.
    '''
    factory = RunTaskFactory.from_executable('/bin/echo',
                                             default_args=['{text}'])
    task = factory.make(name='task')  # key 'text' intentionally omitted
    with pytest.raises(KeyError):
        do_test_task(task, {}, config_tmp)
