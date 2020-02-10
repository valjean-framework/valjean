'''Tests for the :mod:`~cosette.run` module.'''

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
    output_dir = config.get('path', 'output-root')
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
    assert stderr == '$ echo ' + TEXT + '\n'


@requires_git
def test_factory_checkout(git_myecho_repo, config_tmp, subdir):
    '''Test that :class:`RunTaskFactory` produces working `:class:`RunTask`
    objects from a :class:`CheckoutTask`.
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
    '''Test that :class:`RunTaskFactory` produces working `:class:`RunTask`
    objects from a :class:`BuildTask`.
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
    '''Test that :class:`RunTaskFactory` produces working `:class:`RunTask`
    objects from an existing executable.
    '''
    factory = RunTaskFactory.from_executable('/bin/echo')
    task = factory.make(name='task',
                        extra_args=(TEXT,))
    stdout, stderr = do_test_task(task, {}, config_tmp)
    assert stdout == TEXT + '\n'
    assert stderr == '$ /bin/echo ' + TEXT + '\n'


def test_factory_exe_args(config_tmp):
    '''Test that :class:`RunTaskFactory` produces working `:class:`RunTask`
    objects from an existing executable.
    '''
    factory = RunTaskFactory.from_executable('/bin/echo',
                                             default_args=['{text}'])
    task = factory.make(name='task', text=TEXT)
    stdout, stderr = do_test_task(task, {}, config_tmp)
    assert stdout == TEXT + '\n'
    assert stderr == '$ /bin/echo ' + TEXT + '\n'


def test_factory_exe_raise_missing(config_tmp):
    '''Test that :class:`RunTaskFactory` raises if required run arguments are
    missing.
    '''
    factory = RunTaskFactory.from_executable('/bin/echo',
                                             default_args=['{text}'])
    task = factory.make(name='task')  # key 'text' intentionally omitted
    with pytest.raises(KeyError):
        do_test_task(task, {}, config_tmp)
