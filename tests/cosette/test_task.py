#!/usr/bin/env python3

'''Test classes for the :mod:`~.task` module.'''

import pytest

from ..context import valjean  # noqa: F401
import valjean.cosette.task as task
from valjean.cosette.task import TaskStatus


class TestRunTask:

    def test_echo(self, tmpdir):
        testfile = tmpdir.join('testfile')
        testfile.ensure()
        f_out = testfile.open(mode='w')
        t = task.RunTask('echo', ['echo', 'test'],
                         subprocess_args={'stdout': f_out})
        env_up, status = t.do(dict())
        assert status == TaskStatus.DONE
        assert env_up['tasks']['echo']['return_code'] == 0

        result = testfile.read()
        assert result == 'test\n'


class TestShellTask:

    def test_shell(self, tmpdir):
        script = r'''echo here
echo there
echo and everywhere
'''
        testfile = tmpdir.join('testfile')
        testfile.ensure()
        f_out = testfile.open(mode='w')
        t = task.ShellTask('script', script,
                            subprocess_args={'stdout': f_out})
        env_up, status = t.do(dict())
        assert status == TaskStatus.DONE
        assert env_up['tasks']['script']['return_code'] == 0

        result = testfile.read()
        assert result == 'here\nthere\nand everywhere\n'
