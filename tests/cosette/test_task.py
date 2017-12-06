#!/usr/bin/env python3

'''Test classes for the :mod:`~.task` module.'''

import pytest
import tempfile
import os

from ..context import valjean  # noqa: F401
import valjean.cosette.task.task as task
from valjean.cosette.task import TaskStatus


@pytest.fixture(scope='function')
def tempdir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


class TestExecuteTask:

    def test_echo(self, tempdir):
        filename = os.path.join(tempdir, 'testfile')
        with open(filename, 'w') as f_out:
            t = task.ExecuteTask('echo', ['echo', 'test'], stdout=f_out)
            env_up, status = t.do(dict())
        assert status == TaskStatus.DONE
        assert env_up['tasks']['echo']['return_code'] == 0

        with open(filename) as f_in:
            result = f_in.readline()
            assert result == 'test\n'


class TestShellTask:

    def test_shell(self, tempdir):
        script = r'''echo here
        echo there
        echo and everywhere
        '''

        filename = os.path.join(tempdir, 'testfile')
        with open(filename, 'w') as f_out:
            t = task.ShellTask('script', script, stdout=f_out)
            env_up, status = t.do(dict())
        assert status == TaskStatus.DONE
        assert env_up['tasks']['script']['return_code'] == 0

        with open(filename) as f_in:
            result = f_in.read()
            assert result == 'here\nthere\nand everywhere\n'
