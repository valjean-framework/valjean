#!/usr/bin/env python3

'''Tests for the :mod:`~cosette.run` module.'''

from pathlib import Path

from ..context import valjean  # pylint: disable=unused-import

# pylint: disable=wrong-import-order
from valjean.config import Config
from valjean.cosette.task import TaskStatus
from valjean.cosette.run import RunTask


def test_echo(tmpdir):
    '''Test :class:`~.RunTask` with a simple echo command.'''
    config = Config([])
    config.set('path', 'run-root', str(tmpdir))

    runtask = RunTask('echo', [['echo', 'test']])
    env_up, status = runtask.do(dict(), config)
    assert status == TaskStatus.DONE
    assert env_up['echo']['return_codes'] == [0]
    stdout = Path(env_up['echo']['stdout'])
    stderr = Path(env_up['echo']['stderr'])
    stdout.relative_to(str(tmpdir))  # raises ValueError if impossible
    stderr.relative_to(str(tmpdir))  # raises ValueError if impossible
    with stdout.open() as f_out:
        content = f_out.read()
        assert content == 'test\n'
