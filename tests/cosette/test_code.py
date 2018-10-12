'''Tests for the :mod:`~.code` module.'''
# pylint: disable=redefined-outer-name

import os
from subprocess import check_call

import pytest

from ..context import valjean  # pylint: disable=unused-import
# pylint: disable=wrong-import-order
from valjean import LOGGER
from valjean.cosette.task import TaskStatus
from valjean.cosette.code import CheckoutTask, BuildTask
from valjean.cosette.env import Env


from .conftest import CMAKELISTS, requires_git, requires_cmake


################################
#  helper functions for tests  #
################################


def do_git_checkout(name, config, project, *, env=None, ref, flags):
    '''Actually perform the git checkout.'''
    # create the task and run it
    task = CheckoutTask(name=name, repository=project, ref=ref,
                        flags=flags)
    if env is None:
        env = Env()
    env_up, status = task.do(env, config)
    LOGGER.debug('env_up = %s', env_up)

    # run some checks
    try:
        assert status == TaskStatus.DONE
        checkout_log_dir = os.path.dirname(env_up[name]['checkout_log'])
        assert os.path.samefile(checkout_log_dir,
                                config.get('path', 'log-root'))
        assert env_up[name]['repository'] == project
        checkout_dir = env_up[name]['checkout_dir']
        filename = os.path.join(checkout_dir, 'CMakeLists.txt')
        with open(filename) as cmake_file:
            content = cmake_file.read()
        assert content == CMAKELISTS
    except AssertionError:
        with open(env_up[name]['checkout_log']) as c_f:
            LOGGER.debug('checkout_log:\n%s', c_f.read())
        raise

    env.apply(env_up)
    return task, env


def do_cmake_build(name, config, source, *, env=None, configure_flags,
                   build_flags, targets):
    '''Actually perform the CMake build.'''
    # create the task and run it
    task = BuildTask(name, source,
                     configure_flags=configure_flags,
                     build_flags=build_flags,
                     targets=targets)

    if env is None:
        env = Env()
    env_up, status = task.do(env, config)
    LOGGER.debug('env_up = %s', env_up)

    # run some checks
    try:
        log_root = config.get('path', 'log-root')
        assert status == TaskStatus.DONE
        build_log_dir = os.path.dirname(env_up[name]['build_log'])
        assert os.path.samefile(build_log_dir, log_root)
    except AssertionError:
        with open(env_up[name]['build_log']) as build_f:
            LOGGER.debug('build_log:\n%s', build_f.read())
        raise

    build_dir = env_up[name]['build_dir']
    assert check_call([os.path.join(build_dir, 'test_exe')]) == 0
    env.apply(env_up)
    return env


###########
#  tests  #
###########


@requires_git
def test_git_checkout(task_name, config_paths, project, git_ref, git_flags):
    '''Test that git checkout works from a generated configuration.

    .. todo::
       Add some checks on the return values of :func:`do_git_checkout`.
    '''
    do_git_checkout(task_name, config_paths, project,
                    ref=git_ref, flags=git_flags)


# pylint: disable=too-many-arguments
@requires_cmake
def test_cmake_build(task_name, config_paths, project, cmake_configure_flags,
                     cmake_build_flags, cmake_targets):
    '''Test that CMake build works from a generated configuration.

    .. todo::
       Add some checks on the return values of :func:`do_cmake_build`.
    '''
    do_cmake_build(task_name, config_paths, project,
                   configure_flags=cmake_configure_flags,
                   build_flags=cmake_build_flags,
                   targets=cmake_targets)


@requires_git
@requires_cmake
def test_git_checkout_cmake_build(task_name, config_paths, project):
    '''Test a git checkout followed by a CMake build.

    .. todo::
       Add some checks on the return values of :func:`do_cmake_build`.
    '''
    # extract the section name and the task name
    task, env = do_git_checkout(task_name, config_paths, project,
                                ref=None, flags=None)
    do_cmake_build(task_name, config_paths, task, env=env,
                   configure_flags=None, build_flags=None, targets=None)


########################################
#  tests that should raise exceptions  #
########################################

def test_notimpl_checkout(project, notimpl_vcs):
    '''Test that unimplemented VCSs raise an error.'''
    with pytest.raises(NotImplementedError):
        CheckoutTask('checkout', repository=project, vcs=notimpl_vcs)


def test_unknown_checkout(project):
    '''Test that an unknown VCS raises an error.'''
    with pytest.raises(ValueError):
        CheckoutTask('checkout', repository=project, vcs='antani')


def test_notimpl_build(project, notimpl_build):
    '''Test that unimplemented build systems raise an error.'''
    with pytest.raises(NotImplementedError):
        BuildTask('build', project, build_system=notimpl_build)


def test_unknown_build(project):
    '''Test that an unknown build system raises an error.'''
    # extract the section name and the task name
    with pytest.raises(ValueError):
        BuildTask('build', project, build_system='antani')
