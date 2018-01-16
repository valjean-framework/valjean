#!/usr/bin/env python3

'''Test classes for the :mod:`~.code` module.'''

import pytest
import tempfile
import os
from configparser import NoSectionError

from ..context import valjean  # noqa: F401
import valjean.cosette.code as code
from valjean.config import Config
from valjean.cosette.task import TaskStatus
from valjean.cosette.env import Env
from valjean import LOGGER


CMAKELISTS = r'''project(TestCodeTasks C)
set(SOURCE_FILENAME "${PROJECT_BINARY_DIR}/test.c")
file(WRITE "${SOURCE_FILENAME}" "int main() { return 0; }")
add_executable(test_exe "${SOURCE_FILENAME}")
'''


@pytest.fixture(scope='function', params=['test', 'test with space'])
def task_name(request):
    return request.param

#####################################
#  fixture for project generation  ##
#####################################


@pytest.fixture(scope='session')
def project():
    '''Set up a minimalist project for testing.'''
    from subprocess import check_call, DEVNULL

    with tempfile.TemporaryDirectory(prefix='project_') as proj_dir:
        check_call([code.CheckoutTask.GIT, 'init', proj_dir],
                   stdout=DEVNULL, stderr=DEVNULL)
        filename = os.path.join(proj_dir, 'CMakeLists.txt')
        with open(filename, 'wb') as f:
            f.write(CMAKELISTS.encode('utf-8'))
        git_dir = os.path.join(proj_dir, '.git')
        check_call([code.CheckoutTask.GIT, '--git-dir', git_dir,
                    '--work-tree', proj_dir, 'add', filename],
                   stdout=DEVNULL, stderr=DEVNULL)
        check_call([code.CheckoutTask.GIT, '--git-dir', git_dir,
                    '--work-tree', proj_dir, 'commit', '-m', 'Test commit'],
                   stdout=DEVNULL, stderr=DEVNULL)
        yield proj_dir


#################################
#  fixtures for Config objects  #
#################################


@pytest.fixture(scope='function')
def log_dir():
    with tempfile.TemporaryDirectory(prefix='log_') as log_dir:
        yield log_dir


@pytest.fixture(scope='function')
def checkout_dir():
    with tempfile.TemporaryDirectory(prefix='co_') as checkout_dir:
        yield checkout_dir


@pytest.fixture(scope='function', params=['master', None])
def git_ref(request):
    return request.param


@pytest.fixture(scope='function', params=['--depth 1', None])
def git_flags(request):
    return request.param


@pytest.fixture(scope='function', params=['git', None])
def git_vcs(request):
    return request.param


@pytest.fixture(scope='function', params=[True, False])
def checkout_core(request):
    return request.param


def _make_git_config(task_name, project, log_dir, checkout_dir, checkout_core,
                     git_ref=None, git_flags=None, git_vcs=None):
    '''Set up a Config object for git repository testing.'''
    config = Config()
    config.set('core', 'log-root', log_dir)
    sec_name = 'checkout/' + task_name
    config.add_section(sec_name)
    config.set(sec_name, 'repository', project)
    if checkout_core:
        config.set('core', 'checkout-root', checkout_dir)
    else:
        config.set(sec_name, 'checkout-dir', checkout_dir)
    if git_vcs is not None:
        config.set(sec_name, 'vcs', git_vcs)
    if git_ref is not None:
        config.set(sec_name, 'ref', git_ref)
    if git_flags is not None:
        config.set(sec_name, 'flags', git_flags)
    yield config


@pytest.fixture(scope='function')
def git_config(task_name, project, log_dir, checkout_dir, checkout_core,
               git_ref, git_flags, git_vcs):
    yield from _make_git_config(task_name, project, log_dir, checkout_dir,
                                checkout_core, git_ref, git_flags, git_vcs)


@pytest.fixture(scope='function')
def simple_git_config(task_name, project, log_dir, checkout_dir,
                      checkout_core):
    yield from _make_git_config(task_name, project, log_dir, checkout_dir,
                                checkout_core)


@pytest.fixture(scope='function', params=['-DCMAKE_BUILD_TYPE=Debug', None])
def cmake_conf_flags(request):
    return request.param


@pytest.fixture(scope='function', params=['-- -j1', None])
def cmake_build_flags(request):
    return request.param


@pytest.fixture(scope='function', params=['test_exe all', 'test_exe', None])
def cmake_targets(request):
    return request.param


@pytest.fixture(scope='function')
def build_dir():
    with tempfile.TemporaryDirectory(prefix='build_') as build_dir:
        yield build_dir


@pytest.fixture(scope='function', params=[True, False])
def build_core(request):
    return request.param


def _make_cmake_config(task_name, project, log_dir, build_dir, build_core,
                       cmake_conf_flags=None, cmake_build_flags=None,
                       cmake_targets=None):
    '''Set up a Config object for CMake build testing.'''
    config = Config()
    config.set('core', 'log-root', log_dir)
    sec_name = 'build/' + task_name
    config.add_section(sec_name)
    config.set(sec_name, 'source-dir', project)
    if build_core:
        config.set('core', 'build-root', build_dir)
    else:
        config.set(sec_name, 'build-dir', build_dir)
    if cmake_conf_flags is not None:
        config.set(sec_name, 'configure-flags', cmake_conf_flags)
    if cmake_build_flags is not None:
        config.set(sec_name, 'build-flags', cmake_build_flags)
    if cmake_targets is not None:
        config.set(sec_name, 'build-targets', cmake_targets)
    yield config


@pytest.fixture(scope='function')
def cmake_config(task_name, project, log_dir, build_dir, build_core,
                 cmake_conf_flags, cmake_build_flags, cmake_targets):
    '''Set up a Config object for CMake build testing.'''
    yield from _make_cmake_config(task_name, project, log_dir, build_dir,
                                  build_core, cmake_conf_flags,
                                  cmake_build_flags, cmake_targets)


@pytest.fixture(scope='function')
def simple_cmake_config(task_name, project, log_dir, build_dir, build_core):
    yield from _make_cmake_config(task_name, project, log_dir, build_dir,
                                  build_core)


@pytest.fixture(scope='function')
def git_cmake_config(task_name, project, log_dir,
                     simple_git_config, simple_cmake_config):
    '''Set up a Config object for combined git checkout/CMake build testing.'''
    sec_name, name = simple_cmake_config.section_by_family('build')
    simple_git_config.merge_section(simple_cmake_config, sec_name)
    simple_git_config.set('core', 'build-root',
                          simple_cmake_config.get('core', 'build-root'))
    yield simple_git_config


@pytest.fixture(scope='function', params=['svn', 'cvs', 'copy'])
def failing_vcs(request):
    return request.param


@pytest.fixture(scope='function', params=['autoconf', 'configure'])
def failing_build(request):
    return request.param


##################
#  test classes  #
##################


class TestCodeTasks:

    def test_git_checkout(self, git_config):
        return self.do_git_checkout(git_config)

    def do_git_checkout(self, config, env=None):
        # extract the section name and the task name
        sec_name, name = config.section_by_family('checkout')

        # extract the path to the git repository
        git_repo = config.get(sec_name, 'repository')

        # extract the path to the checkout directory
        checkout_dir = config.get(sec_name, 'checkout-dir')

        # create the task and run it
        task = code.CheckoutTask.from_config(name=name, config=config)
        if env is None:
            env = Env()
        env_up, status = task.do(env)
        LOGGER.debug('env_up = %s', env_up)

        # run some checks
        assert status == TaskStatus.DONE
        full_name = 'checkout/' + name
        assert env_up['tasks'][full_name]['return_code'] == 0
        assert env_up['checkout'][full_name]['repository'] == git_repo
        assert env_up['checkout'][full_name]['checkout_dir'] == checkout_dir
        filename = os.path.join(checkout_dir, 'CMakeLists.txt')
        with open(filename) as f:
            content = f.read()
        assert content == CMAKELISTS
        env.apply(env_up)
        return env

    def test_cmake_build(self, cmake_config):
        return self.do_cmake_build(cmake_config)

    def do_cmake_build(self, config, env=None):
        # extract the section name and the task name
        sec_name, name = config.section_by_family('build')

        # extract the path to the build directory
        build_dir = config.get(sec_name, 'build-dir')

        # extract the path to the log directory
        log_dir = config.get('core', 'log-root')

        # create the task and run it
        task = code.BuildTask.from_config(name=name, config=config)
        if env is None:
            env = Env()
        env_up, status = task.do(env)
        LOGGER.debug('env_up = %s', env_up)

        # run some checks
        try:
            assert status == TaskStatus.DONE
            full_name = 'build/' + name
            assert env_up['tasks'][full_name]['return_code'] == 0
            configure_log_dir = os.path.dirname(
                env_up['build'][full_name]['configure_log']
                )
            assert os.path.samefile(configure_log_dir, log_dir)
            build_log_dir = os.path.dirname(
                env_up['build'][full_name]['build_log']
                )
            assert os.path.samefile(build_log_dir, log_dir)
        except AssertionError:
            with open(env_up['build'][full_name]['configure_log']) as c_f:
                code.LOGGER.debug('configure_log:\n%s', c_f.read())
            with open(env_up['build'][full_name]['build_log']) as build_f:
                code.LOGGER.debug('build_log:\n%s', build_f.read())
            raise

        exe_name = os.path.join(build_dir, 'test_exe')
        from subprocess import check_call
        assert check_call([exe_name]) == 0
        env.apply(env_up)
        return env

    def test_git_checkout_cmake_build(self, git_cmake_config):
        # extract the section name and the task name
        sec_name, name = git_cmake_config.section_by_family('build')

        git_cmake_config.remove_option(sec_name, 'source-dir')
        env = self.do_git_checkout(git_cmake_config)
        self.do_cmake_build(git_cmake_config, env)


class TestFailingCodeTasks:

    def test_missing_checkout_section_raises(self, simple_git_config):
        # extract the section name and the task name
        sec_name, name = simple_git_config.section_by_family('checkout')
        simple_git_config.remove_section(sec_name)
        with pytest.raises(NoSectionError):
            code.CheckoutTask.from_config(name, simple_git_config)

    def test_notimpl_checkout_raises(self, simple_git_config, failing_vcs):
        # extract the section name and the task name
        sec_name, name = simple_git_config.section_by_family('checkout')
        simple_git_config.set(sec_name, 'vcs', failing_vcs)
        with pytest.raises(NotImplementedError):
            code.CheckoutTask.from_config(name, simple_git_config)

    def test_unknown_checkout_raises(self, simple_git_config):
        # extract the section name and the task name
        sec_name, name = simple_git_config.section_by_family('checkout')
        simple_git_config.set(sec_name, 'vcs', 'antani')
        with pytest.raises(ValueError):
            code.CheckoutTask.from_config(name, simple_git_config)

    def test_missing_build_section_raises(self, simple_cmake_config):
        # extract the section name and the task name
        sec_name, name = simple_cmake_config.section_by_family('build')
        simple_cmake_config.remove_section(sec_name)
        with pytest.raises(NoSectionError):
            code.BuildTask.from_config(name, simple_cmake_config)

    def test_notimpl_build_raises(self, simple_cmake_config, failing_build):
        # extract the section name and the task name
        sec_name, name = simple_cmake_config.section_by_family('build')
        simple_cmake_config.set(sec_name, 'build-system', failing_build)
        with pytest.raises(NotImplementedError):
            code.BuildTask.from_config(name, simple_cmake_config)

    def test_unknown_build_raises(self, simple_cmake_config):
        # extract the section name and the task name
        sec_name, name = simple_cmake_config.section_by_family('build')
        simple_cmake_config.set(sec_name, 'build-system', 'tarapio')
        with pytest.raises(ValueError):
            code.BuildTask.from_config(name, simple_cmake_config)
