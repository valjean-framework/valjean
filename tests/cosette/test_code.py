'''Tests for the :mod:`~.code` module.'''
# pylint: disable=redefined-outer-name

import os
from configparser import NoOptionError
from subprocess import check_call

import pytest

from ..context import valjean  # pylint: disable=unused-import
# pylint: disable=wrong-import-order
from valjean.cosette import code
from valjean.cosette.task import TaskStatus
from valjean.cosette.env import Env
from valjean import LOGGER


from .conftest import CMAKELISTS, requires_git, requires_cmake


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
