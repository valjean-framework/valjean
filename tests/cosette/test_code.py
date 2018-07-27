#!/usr/bin/env python3
# pylint: disable=redefined-outer-name

'''Tests for the :mod:`~.code` module.'''

import os
from configparser import NoOptionError
from subprocess import check_call, check_output, DEVNULL, CalledProcessError
import re

import pytest

from ..context import valjean  # noqa: F401, pylint: disable=unused-import

# pylint: disable=wrong-import-order
from valjean.cosette import code
from valjean.config import Config
from valjean.cosette.task import TaskStatus
from valjean.cosette.env import Env
from valjean import LOGGER


def make_skip_marker(command, regex):
    '''Create a :func:`pytest.mark.skipif` marker for a command.

    :param str command: the name of a command (an executable). If the command
                        is not available, the marker will flag the tests as
                        SKIPPED.
    :param str regex: a regex to extract the version number of the command from
                      the output of ``command --version``. The version number
                      must appear in the first capture group.
    '''
    import locale
    has = False
    try:
        encoding = locale.getpreferredencoding(False)
        version_str = check_output([command, '--version']).decode(encoding)
        match = re.match(regex, version_str)
        if match is None:
            version = ''
            reason = ('could not parse version string for ' + command +
                      ', needed for this test')
        else:
            version = match.group(1)
            has = True
            reason = ''
    except FileNotFoundError:
        version = ''
        reason = 'could not find ' + command + ', needed for this test'
    except CalledProcessError:
        version = ''
        reason = 'call to `' + command + ' --version` failed'

    marker = pytest.mark.skipif(not has, reason=reason)
    return marker, version


# pylint: disable=invalid-name
requires_cmake, _CMAKE_VERSION = make_skip_marker(code.BuildTask.CMAKE,
                                                  r'^cmake version (.*)')
HAS_CMAKE = not requires_cmake.args[0]
requires_git, _ = make_skip_marker(code.CheckoutTask.GIT,
                                   r'^git version (.*)$')
HAS_GIT = not requires_git.args[0]

CMAKELISTS = r'''project(TestCodeTasks C)
cmake_minimum_required(VERSION ''' + _CMAKE_VERSION + ''')
set(SOURCE_FILENAME "${PROJECT_BINARY_DIR}/test.c")
file(WRITE "${SOURCE_FILENAME}" "int main() { return 0; }")
add_executable(test_exe "${SOURCE_FILENAME}")
'''


@pytest.fixture(scope='function', params=['test', 'test with space'])
def task_name(request):
    '''Return possible names for tasks.'''
    return request.param

#####################################
#  fixture for project generation  ##
#####################################


def setup_project(project_dir):
    '''Set up a minimalist project for testing in the given directory.

    The project consists of a git repository containing a simple
    `CMakelists.txt` file.

    :param str project_dir: the path to an existing directory.
    '''
    LOGGER.debug('HAS_GIT: %s', HAS_GIT)
    LOGGER.debug('HAS_CMAKE: %s', HAS_CMAKE)

    filename = os.path.join(project_dir, 'CMakeLists.txt')

    with open(filename, 'w') as cmakelists_file:
        cmakelists_file.write(CMAKELISTS)

    if not HAS_GIT:
        return

    check_call([code.CheckoutTask.GIT, 'init', project_dir],
               stdout=DEVNULL, stderr=DEVNULL)
    git_dir = os.path.join(project_dir, '.git')
    check_call([code.CheckoutTask.GIT, '--git-dir', git_dir,
                '--work-tree', project_dir, 'add', filename],
               stdout=DEVNULL, stderr=DEVNULL)
    check_call([code.CheckoutTask.GIT, '--git-dir', git_dir,
                '--work-tree', project_dir, 'commit', '-m', 'Test commit'],
               stdout=DEVNULL, stderr=DEVNULL)


#################################
#  fixtures for Config objects  #
#################################

# git-related fixtures

@pytest.fixture(scope='function', params=['master', None])
def git_ref(request):
    '''Return possible values of the `ref` option for git checkout.'''
    return request.param


@pytest.fixture(scope='function', params=['--depth 1', None])
def git_flags(request):
    '''Return possible values of the `flags` option for git checkout.'''
    return request.param


@pytest.fixture(scope='function', params=['git', None])
def git_vcs(request):
    '''Return possible values of the `vcs` option for git checkout.'''
    return request.param


@pytest.fixture(scope='function')
def git_params(git_ref, git_flags, git_vcs):
    '''Collect the git-related fixtures in a tuple.'''
    return git_ref, git_flags, git_vcs


@pytest.fixture(scope='function', params=[True, False])
def checkout_core(request):
    '''Controls whether the checkout dir should be implicitly specified (in the
    core section) in generated config files.'''
    return request.param


def make_git_config(task_name, project_dir, log_dir, checkout_dir,
                    checkout_core, **kwargs):
    '''Set up a Config object for git repository testing.'''
    config = Config()
    config.set('core', 'log-root', log_dir)
    sec_name = 'checkout/' + task_name
    config.add_section(sec_name)
    config.set(sec_name, 'repository', project_dir)
    if checkout_core:
        config.set('core', 'checkout-root', checkout_dir)
    else:
        config.set(sec_name, 'checkout-dir', checkout_dir)
    git_vcs = kwargs.get('git_vcs', None)
    if git_vcs is not None:
        config.set(sec_name, 'vcs', git_vcs)
    git_ref = kwargs.get('git_ref', None)
    if git_ref is not None:
        config.set(sec_name, 'ref', git_ref)
    git_flags = kwargs.get('git_flags', None)
    if git_flags is not None:
        config.set(sec_name, 'flags', git_flags)
    return config


@pytest.fixture(scope='function')
def git_config(task_name, tmpdir_factory, checkout_core, git_params):
    '''Create a full configuration object for git checkout testing.'''
    git_ref, git_flags, git_vcs = git_params
    project_dir = str(tmpdir_factory.mktemp('project'))
    log_dir = str(tmpdir_factory.mktemp('log'))
    checkout_dir = str(tmpdir_factory.mktemp('checkout'))
    setup_project(project_dir)
    return make_git_config(task_name, project_dir, log_dir, checkout_dir,
                           checkout_core, git_ref=git_ref, git_flags=git_flags,
                           git_vcs=git_vcs)


@pytest.fixture(scope='function')
def simple_git_config(task_name, tmpdir_factory, checkout_core):
    '''Create a simplified configuration object for git checkout testing.'''
    project_dir = str(tmpdir_factory.mktemp('project'))
    log_dir = str(tmpdir_factory.mktemp('log'))
    checkout_dir = str(tmpdir_factory.mktemp('checkout'))
    setup_project(project_dir)
    return make_git_config(task_name, project_dir, log_dir, checkout_dir,
                           checkout_core)


# cmake-related fixtures

@pytest.fixture(scope='function', params=['-DCMAKE_BUILD_TYPE=Debug', None])
def cmake_conf_flags(request):
    '''Return possible values of the configuration flags for CMake builds.'''
    return request.param


@pytest.fixture(scope='function', params=['-- -j1', None])
def cmake_build_flags(request):
    '''Return possible values of the build flags for CMake builds.'''
    return request.param


@pytest.fixture(scope='function', params=['test_exe all', 'test_exe', None])
def cmake_targets(request):
    '''Return possible values of the target option for CMake builds.'''
    return request.param


@pytest.fixture(scope='function')
def cmake_params(cmake_conf_flags, cmake_build_flags, cmake_targets):
    '''Collect the cmake-related fixtures in a tuple.'''
    return cmake_conf_flags, cmake_build_flags, cmake_targets


@pytest.fixture(scope='function', params=[True, False])
def build_core(request):
    '''Controls whether the build dir should be implicitly specified (in the
    core section) in generated config files.'''
    return request.param


def make_cmake_config(task_name, project_dir, log_dir, build_dir, build_core,
                      **kwargs):
    '''Set up a Config object for CMake build testing.'''
    config = Config()
    config.set('core', 'log-root', log_dir)
    sec_name = 'build/' + task_name
    config.add_section(sec_name)
    config.set(sec_name, 'source-dir', project_dir)
    if build_core:
        config.set('core', 'build-root', build_dir)
    else:
        config.set(sec_name, 'build-dir', build_dir)
    cmake_conf_flags = kwargs.get('cmake_conf_flags', None)
    if cmake_conf_flags is not None:
        config.set(sec_name, 'configure-flags', cmake_conf_flags)
    cmake_build_flags = kwargs.get('cmake_build_flags', None)
    if cmake_build_flags is not None:
        config.set(sec_name, 'build-flags', cmake_build_flags)
    cmake_targets = kwargs.get('cmake_targets', None)
    if cmake_targets is not None:
        config.set(sec_name, 'build-targets', cmake_targets)
    return config


@pytest.fixture(scope='function')
def cmake_config(task_name, tmpdir_factory, build_core, cmake_params):
    '''Set up a full Config object for CMake build testing.'''
    cmake_conf_flags, cmake_build_flags, cmake_targets = cmake_params
    project_dir = str(tmpdir_factory.mktemp('project'))
    log_dir = str(tmpdir_factory.mktemp('log'))
    build_dir = str(tmpdir_factory.mktemp('build'))
    setup_project(project_dir)
    return make_cmake_config(task_name, project_dir, log_dir, build_dir,
                             build_core, cmake_conf_flags=cmake_conf_flags,
                             cmake_build_flags=cmake_build_flags,
                             cmake_targets=cmake_targets)


@pytest.fixture(scope='function')
def simple_cmake_config(task_name, tmpdir_factory, build_core):
    '''Set up a simplified Config object for CMake build testing.'''
    project_dir = str(tmpdir_factory.mktemp('project'))
    log_dir = str(tmpdir_factory.mktemp('log'))
    build_dir = str(tmpdir_factory.mktemp('build'))
    setup_project(project_dir)
    return make_cmake_config(task_name, project_dir, log_dir, build_dir,
                             build_core)


@pytest.fixture(scope='function', params=[True, False])
def with_source_dir(request):
    '''Return the unimplemented version-control systems.'''
    return request.param


@pytest.fixture(scope='function')
def git_cmake_config(simple_git_config, simple_cmake_config, with_source_dir):
    '''Set up a Config object for combined git checkout/CMake build testing.'''
    sec_name, _ = simple_cmake_config.section_by_family('build')
    simple_git_config.merge_section(simple_cmake_config, sec_name)

    if not with_source_dir:
        sec_name, _ = simple_git_config.section_by_family('build')
        _, name = simple_git_config.section_by_family('checkout')
        LOGGER.debug('modifying sections %s and %s',
                     sec_name, name)
        simple_git_config.remove_option(sec_name, 'source-dir')
        simple_git_config.set(sec_name, 'checkout', name)

    LOGGER.debug('git_cmake_config: %s', simple_git_config)
    return simple_git_config


@pytest.fixture(scope='function', params=['svn', 'cvs', 'copy'])
def notimpl_vcs(request):
    '''Return the unimplemented version-control systems.'''
    return request.param


@pytest.fixture(scope='function', params=['autoconf', 'configure'])
def notimpl_build(request):
    '''Return the unimplemented build systems.'''
    return request.param


################################
#  helper functions for tests  #
################################


def do_git_checkout(config, env=None):
    '''Actually perform the git checkout.'''
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
    full_name = 'checkout/' + name
    try:
        assert status == TaskStatus.DONE
        assert env_up[full_name]['return_code'] == 0
        assert env_up[full_name]['repository'] == git_repo
        assert env_up[full_name]['checkout_dir'] == checkout_dir
        filename = os.path.join(checkout_dir, 'CMakeLists.txt')
        with open(filename) as cmake_file:
            content = cmake_file.read()
        assert content == CMAKELISTS
    except AssertionError:
        with open(env_up[full_name]['checkout_log']) as c_f:
            code.LOGGER.debug('checkout_log:\n%s', c_f.read())
        raise

    env.apply(env_up)
    return env


def do_cmake_build(config, env=None):
    '''Actually perform the CMake build.'''
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
    full_name = 'build/' + name
    try:
        assert status == TaskStatus.DONE
        assert env_up[full_name]['return_code'] == 0
        configure_log_dir = os.path.dirname(env_up[full_name]['configure_log'])
        assert os.path.samefile(configure_log_dir, log_dir)
        build_log_dir = os.path.dirname(env_up[full_name]['build_log'])
        assert os.path.samefile(build_log_dir, log_dir)
    except AssertionError:
        with open(env_up[full_name]['configure_log']) as c_f:
            code.LOGGER.debug('configure_log:\n%s', c_f.read())
        with open(env_up[full_name]['build_log']) as build_f:
            code.LOGGER.debug('build_log:\n%s', build_f.read())
        raise

    assert check_call([os.path.join(build_dir, 'test_exe')]) == 0
    env.apply(env_up)
    return env


###########
#  tests  #
###########


@requires_git
def test_git_checkout(git_config):
    '''Test that git checkout works from a generated configuration.'''
    return do_git_checkout(git_config)


@requires_cmake
def test_cmake_build(cmake_config):
    '''Test that CMake build works from a generated configuration.'''
    return do_cmake_build(cmake_config)


@requires_git
@requires_cmake
def test_git_checkout_cmake_build(git_cmake_config):
    '''Test a git checkout followed by a CMake build.'''
    # extract the section name and the task name
    env = do_git_checkout(git_cmake_config)
    do_cmake_build(git_cmake_config, env)


########################################
#  tests that should raise exceptions  #
########################################

def test_missing_checkout_section(simple_git_config):
    '''Test that a missing checkout section raises an error on checkout.'''
    # extract the section name and the task name
    sec_name, name = simple_git_config.section_by_family('checkout')
    simple_git_config.remove_section(sec_name)
    with pytest.raises(NoOptionError):
        code.CheckoutTask.from_config(name, simple_git_config)


def test_notimpl_checkout(simple_git_config, notimpl_vcs):
    '''Test that unimplemented VCSs raise an error.'''
    # extract the section name and the task name
    sec_name, name = simple_git_config.section_by_family('checkout')
    simple_git_config.set(sec_name, 'vcs', notimpl_vcs)
    with pytest.raises(NotImplementedError):
        code.CheckoutTask.from_config(name, simple_git_config)


def test_unknown_checkout(simple_git_config):
    '''Test that an unknown VCS raises an error.'''
    # extract the section name and the task name
    sec_name, name = simple_git_config.section_by_family('checkout')
    simple_git_config.set(sec_name, 'vcs', 'antani')
    with pytest.raises(ValueError):
        code.CheckoutTask.from_config(name, simple_git_config)


def test_missing_build_section(simple_cmake_config):
    '''Test that a missing build section raises an error on build.'''
    with pytest.raises(NoOptionError):
        missing_build_section(simple_cmake_config)


def missing_build_section(simple_cmake_config):
    '''Actual test implementation for :func:`test_missing_build_section`.'''
    # extract the section name and the task name
    sec_name, name = simple_cmake_config.section_by_family('build')
    simple_cmake_config.remove_section(sec_name)
    code.BuildTask.from_config(name, simple_cmake_config)


def test_notimpl_build(simple_cmake_config, notimpl_build):
    '''Test that unimplemented build systems raise an error.'''
    # extract the section name and the task name
    sec_name, name = simple_cmake_config.section_by_family('build')
    simple_cmake_config.set(sec_name, 'build-system', notimpl_build)
    with pytest.raises(NotImplementedError):
        code.BuildTask.from_config(name, simple_cmake_config)


def test_unknown_build(simple_cmake_config):
    '''Test that an unknown build system raises an error.'''
    # extract the section name and the task name
    sec_name, name = simple_cmake_config.section_by_family('build')
    simple_cmake_config.set(sec_name, 'build-system', 'tarapio')
    with pytest.raises(ValueError):
        code.BuildTask.from_config(name, simple_cmake_config)
