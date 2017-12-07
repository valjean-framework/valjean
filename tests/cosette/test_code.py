#!/usr/bin/env python3

'''Test classes for the :mod:`~.code` module.'''

import pytest
import tempfile
import os

from ..context import valjean  # noqa: F401
import valjean.cosette.code as code
from valjean.cosette.task import TaskStatus


SAMPLE_TEXT = 'spidiguda'


@pytest.fixture(scope='function')
def git_repo():
    '''Set up a minimalist git repository.'''

    from subprocess import check_call
    with tempfile.TemporaryDirectory() as repo_dir:
        check_call([code.GIT, 'init', repo_dir])
        filename = os.path.join(repo_dir, 'testfile')
        with open(filename, 'w+b') as f:
            f.write(SAMPLE_TEXT.encode('utf-8'))
        check_call([code.GIT, '-C', repo_dir, 'add', filename])
        check_call([code.GIT, '-C', repo_dir, 'commit', '-m', 'Test commit'])
        yield repo_dir


@pytest.fixture(scope='function')
def cmake_project():
    '''Set up a minimalist CMake project.'''

    cmakelists = r'''project(TestCodeTasks C)
set(SOURCE_FILENAME "${PROJECT_BINARY_DIR}/test.c")
file(WRITE "${SOURCE_FILENAME}" "int main() { return 0; }")
add_executable(test_exe "${SOURCE_FILENAME}")'''
    with tempfile.TemporaryDirectory() as cmake_dir:
        filename = os.path.join(cmake_dir, 'CMakeLists.txt')
        with open(filename, 'w+b') as f:
            f.write(cmakelists.encode('utf-8'))
        yield cmake_dir


class TestCodeTasks:

    def test_git_checkout(self, git_repo):
        return self.do_git_checkout(git_repo)

    def test_git_checkout_extra(self, git_repo):
        return self.do_git_checkout(git_repo, ref='master', flags='--depth 1')

    def do_git_checkout(self, git_repo, ref=None, flags=None):
        with tempfile.TemporaryDirectory() as tmpdir:
            with tempfile.TemporaryDirectory() as logdir:
                t = code.CheckoutTask(name='test_checkout',
                                      repository=git_repo,
                                      log_dir=logdir,
                                      checkout_dir=tmpdir,
                                      ref=ref,
                                      flags=flags,
                                      vcs='git')
                env_up, status = t.do(dict())
                assert status == TaskStatus.DONE
                assert env_up['tasks']['test_checkout']['return_code'] == 0
                assert (env_up['checkout']['test_checkout']['repository']
                        == git_repo)
                assert (env_up['checkout']['test_checkout']['checkout_dir']
                        == tmpdir)

                filename = os.path.join(tmpdir, 'testfile')
                with open(filename) as f:
                    content = f.read()
                assert content == SAMPLE_TEXT

    def test_cmake_build(self, cmake_project):
        return self.do_cmake_build(cmake_project)

    def test_cmake_build_extra(self, cmake_project):
        return self.do_cmake_build(cmake_project,
                                   configure_flags='-DCMAKE_BUILD_TYPE=Debug',
                                   build_targets=['test_exe', 'all'],
                                   build_flags='-- -j1')

    def do_cmake_build(self, cmake_project,
                       configure_flags=None,
                       build_flags=None,
                       build_targets=None):
        with tempfile.TemporaryDirectory() as tmpdir:
            t = code.BuildTask(name='test_build',
                               source_dir=cmake_project,
                               build_dir=tmpdir,
                               log_dir=tmpdir,
                               configure_flags=configure_flags,
                               build_flags=build_flags,
                               build_targets=build_targets,
                               build_system='cmake')
            env_up, status = t.do(dict())
            assert status == TaskStatus.DONE
            assert env_up['tasks']['test_build']['return_code'] == 0
            configure_log_dir = os.path.dirname(
                env_up['build']['test_build']['configure_log']
                )
            assert os.path.samefile(configure_log_dir, tmpdir)
            build_log_dir = os.path.dirname(
                env_up['build']['test_build']['build_log']
                )
            assert os.path.samefile(build_log_dir, tmpdir)

            exe_name = os.path.join(tmpdir, 'test_exe')
            from subprocess import check_call
            assert check_call([exe_name]) == 0
