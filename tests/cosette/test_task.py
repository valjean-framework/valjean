#!/usr/bin/env python3

'''Tests for the :mod:`~.task` module.'''

from ..context import valjean  # noqa: F401, pylint: disable=unused-import

# pylint: disable=wrong-import-order
import valjean.cosette.task as task
from valjean.cosette.task import TaskStatus


def test_echo(tmpdir):
    '''Test :class:`~.RunTask` with a simple echo command.'''
    testfile = tmpdir.join('testfile')
    testfile.ensure()
    f_out = testfile.open(mode='w')
    runtask = task.RunTask('echo', ['echo', 'test'],
                           subprocess_args={'stdout': f_out})
    env_up, status = runtask.do(dict())
    assert status == TaskStatus.DONE
    assert env_up['tasks']['echo']['return_code'] == 0

    result = testfile.read()
    assert result == 'test\n'


def test_shell(tmpdir):
    '''Test :class:`~.ShellTask` with a simple shell script.'''
    script = r'''echo here
echo there
echo and everywhere
'''
    testfile = tmpdir.join('testfile')
    testfile.ensure()
    f_out = testfile.open(mode='w')
    shelltask = task.ShellTask('script', script,
                               subprocess_args={'stdout': f_out})
    env_up, status = shelltask.do(dict())
    assert status == TaskStatus.DONE
    assert env_up['tasks']['script']['return_code'] == 0

    result = testfile.read()
    assert result == 'here\nthere\nand everywhere\n'
