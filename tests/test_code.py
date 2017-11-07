#!/usr/bin/env python3

'''Test classes for the :mod:`~.task.code` module.'''

import pytest
import tempfile
import os

from .context import valjean  # noqa: F401
import valjean.task.code as code


SAMPLE_TEXT = 'spidiguda'


@pytest.fixture(scope='module')
def git_repo():
    '''Set up a temporary, empty git repository.'''

    from subprocess import check_call
    with tempfile.TemporaryDirectory() as repo_dir:
        check_call([code.GIT, 'init', repo_dir])
        filename = os.path.join(repo_dir, 'testfile')
        with open(filename, 'w+b') as f:
            f.write(SAMPLE_TEXT.encode('utf-8'))
        check_call([code.GIT, '-C', repo_dir, 'add', filename])
        check_call([code.GIT, '-C', repo_dir, 'commit', '-m', 'Test commit'])
        yield repo_dir


class TestCodeTasks:

    def test_checkout(self, git_repo):
        with tempfile.TemporaryDirectory() as tmpdir:
            t = code.CheckoutTask('test_checkout', git_repo, 'master', tmpdir,
                                  vcs='git')
            env = {}
            t.do(env)
            assert env['tasks']['test_checkout']['return_code'] == 0
            assert env['checkout']['test_checkout']['repository'] == git_repo
            assert env['checkout']['test_checkout']['checkout_dir'] == tmpdir

            filename = os.path.join(tmpdir, 'testfile')
            with open(filename) as f:
                content = f.read()
            assert content == SAMPLE_TEXT
