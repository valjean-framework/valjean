'''Integration tests for the happy path of :command:`valjean` execution.'''

import logging
from shutil import rmtree
from pathlib import Path

import pytest

# pylint: disable=wrong-import-order
from ..context import valjean   # pylint: disable=unused-import
from valjean import LOGGER
from valjean.cambronne.main import main
from valjean.cosette.env import Env
from valjean.cosette.task import TaskStatus

from ..cosette.conftest import (requires_git,  # pylint: disable=unused-import
                                requires_cmake, config_tmp)


def load_all_envs(output_root, filename, fmt):
    '''Load all environment files found in `output_root`.

    :param str output_root: path to the root directory
    :param str filename: name of the environment files
    :param str fmt: the environment format
    :returns: the merged environment
    '''
    env = Env()
    output_root = Path(output_root)
    for path in output_root.glob('**/' + filename):
        persisted_env = Env.from_file(path, fmt=fmt)
        if persisted_env is not None:
            env.update(persisted_env)
    return env


def run_valjean(*other_args, config, job_config, env_filename, job_file):
    '''Run :command:`valjean` using the specified arguments.'''
    args = ['-c', str(job_config), '--env-filename', str(env_filename),
            '-j', str(job_file)]
    if LOGGER.getEffectiveLevel() == logging.DEBUG:
        args.append('-v')
    args.extend(*other_args)
    LOGGER.info('******** Starting valjean run')
    LOGGER.info('******** with args: %s', args)
    main(args)
    LOGGER.info('******** End of the valjean run')
    output_root = config.get('path', 'output-root')
    env = load_all_envs(output_root=output_root, filename=env_filename,
                        fmt='pickle')
    return env


def assert_task_done(env, name):
    '''Assert that the task with the given name is present in the environment
    and has been successfully completed.'''
    assert name in env, '{} missing in env keys: {}'.format(name, list(env))
    assert 'status' in env[name], ("'status' missing in env[{!r}] = {}"
                                   .format(name, env[name]))
    assert env[name]['status'] == TaskStatus.DONE


def assert_cecho_exists(env, name, subdir):
    '''Assert that the cecho executable can be found in the subdir
    directory.'''
    assert name in env
    assert 'output_dir' in env[name]
    cecho_path = Path(env[name]['output_dir']) / subdir / 'cecho'
    assert cecho_path.exists()
    assert cecho_path.is_file()


@requires_git
@pytest.mark.parametrize('target', [None, 'checkout_cecho'],
                         ids=['no target', 'checkout_cecho'])
def test_checkout(job_config, config_tmp, target, env_filename, job_file):
    '''Test the `checkout` command.'''
    args = ['checkout']
    if target is not None:
        args.append(target)
    env = run_valjean(args, config=config_tmp, job_config=job_config,
                      env_filename=env_filename, job_file=job_file)
    assert_task_done(env, 'checkout_cecho')
    assert 'build_cecho' not in env


@requires_git
@requires_cmake
@pytest.mark.parametrize('target', [None, 'checkout_cecho', 'build_cecho'],
                         ids=['no target', 'checkout_cecho', 'build_cecho'])
def test_build(job_config,  # pylint: disable=too-many-arguments
               config_tmp, target, env_filename, subdir, job_file):
    '''Test the `build` command.'''
    args = ['build']
    if target is not None:
        args.append(target)
    env = run_valjean(args, config=config_tmp, job_config=job_config,
                      env_filename=env_filename, job_file=job_file)
    assert_task_done(env, 'checkout_cecho')
    if target != 'checkout_cecho':
        assert_task_done(env, 'build_cecho')
        assert_cecho_exists(env, 'build_cecho', subdir)
    else:
        assert 'build_cecho' not in env


@requires_git
@requires_cmake
def test_resume(job_config, config_tmp, env_filename, subdir, job_file):
    '''Test that running `checkout` followed by `build` does not rerun
    `checkout`.'''
    env = run_valjean(['checkout'], job_config=job_config, config=config_tmp,
                      env_filename=env_filename, job_file=job_file)
    assert_task_done(env, 'checkout_cecho')
    assert 'build_cecho' not in env
    assert 'start_clock' in env['checkout_cecho']
    assert 'end_clock' in env['checkout_cecho']
    assert 'elapsed_time' in env['checkout_cecho']
    elapsed = env['checkout_cecho']['elapsed_time']
    start_clock = env['checkout_cecho']['start_clock']
    end_clock = env['checkout_cecho']['end_clock']

    env = run_valjean(['build'], job_config=job_config, config=config_tmp,
                      env_filename=env_filename, job_file=job_file)
    assert_task_done(env, 'checkout_cecho')
    assert 'elapsed_time' in env['checkout_cecho']
    assert env['checkout_cecho']['elapsed_time'] == elapsed
    assert 'start_clock' in env['checkout_cecho']
    assert env['checkout_cecho']['start_clock'] == start_clock
    assert 'end_clock' in env['checkout_cecho']
    assert env['checkout_cecho']['end_clock'] == end_clock
    assert_task_done(env, 'build_cecho')
    assert_cecho_exists(env, 'build_cecho', subdir)


@requires_git
@requires_cmake
def test_resume_newer(job_config, config_tmp, env_filename, subdir, job_file):
    '''Test that running `checkout` followed by `build`, followed by a forced
    `checkout` again triggers a new `build` run.'''
    env = run_valjean(['checkout'], job_config=job_config, config=config_tmp,
                      env_filename=env_filename, job_file=job_file)
    assert_task_done(env, 'checkout_cecho')
    env = run_valjean(['build'], job_config=job_config, config=config_tmp,
                      env_filename=env_filename, job_file=job_file)
    assert_task_done(env, 'checkout_cecho')
    assert_task_done(env, 'build_cecho')
    assert 'start_clock' in env['build_cecho']
    assert 'end_clock' in env['build_cecho']
    start_clock = env['build_cecho']['start_clock']
    end_clock = env['build_cecho']['end_clock']

    # remove the checkout directory, too, otherwise the new checkout_cecho will
    # fail
    rmtree(env['checkout_cecho']['output_dir'])
    # remove checkout_echo from the env, so that it is rerun
    del env['checkout_cecho']
    env = run_valjean(['build'], job_config=job_config, config=config_tmp,
                      env_filename=env_filename, job_file=job_file)
    assert_task_done(env, 'build_cecho')
    assert 'start_clock' in env['build_cecho']
    assert 'end_clock' in env['build_cecho']
    assert start_clock < env['build_cecho']['start_clock']
    assert end_clock < env['build_cecho']['end_clock']
    assert_cecho_exists(env, 'build_cecho', subdir)


@requires_git
@requires_cmake
@pytest.mark.parametrize('target', [None, 'checkout_cecho', 'build_cecho',
                                    'pling.cecho', 'plong.cecho'],
                         ids=['no target', 'checkout_cecho', 'build_cecho',
                              'pling.cecho', 'plong.cecho'])
def test_run(job_config,  # pylint: disable=too-many-arguments
             config_tmp, target, env_filename, subdir, job_file):
    '''Test the `run` command.'''
    args = ['run']
    if target is not None:
        args.append(target)
    env = run_valjean(args, job_config=job_config, config=config_tmp,
                      env_filename=env_filename, job_file=job_file)
    assert_task_done(env, 'checkout_cecho')
    if target != 'checkout_cecho':
        assert_task_done(env, 'build_cecho')
        assert_cecho_exists(env, 'build_cecho', subdir)
    if target == 'pling.cecho':
        assert_task_done(env, 'pling.cecho')
        assert 'plong.cecho' not in env
    elif target == 'plong.cecho':
        assert_task_done(env, 'plong.cecho')
        assert 'pling.cecho' not in env
    elif target is None:
        assert_task_done(env, 'pling.cecho')
        assert_task_done(env, 'plong.cecho')


@pytest.mark.parametrize('target', [None, 'checkout_cecho', 'build_cecho'],
                         ids=['no target', 'checkout_cecho', 'build_cecho'])
@pytest.mark.parametrize('dependencies', [None, 'hard', 'soft', 'both'])
def test_graph(job_config, config_tmp,  # pylint: disable=too-many-arguments
               target, dependencies, env_filename, job_file, capsys):
    '''Test that the `graph` command produces syntactically valid graphviz
    files.'''
    pydot = pytest.importorskip('pydot')
    args = ['graph']
    if dependencies is not None:
        args.append('--dependencies')
        args.append(dependencies)
    if target is not None:
        args.append(target)
    run_valjean(args, job_config=job_config, config=config_tmp,
                env_filename=env_filename, job_file=job_file)
    captured = capsys.readouterr()
    pydot.graph_from_dot_data(captured.out)


@pytest.mark.parametrize('target', [None, 'checkout_cecho', 'build_cecho'],
                         ids=['no target', 'checkout_cecho', 'build_cecho'])
@pytest.mark.parametrize('dependencies', [None, 'hard', 'soft', 'both'])
def test_graph_on_file(job_config,  # pylint: disable=too-many-arguments
                       config_tmp, target, dependencies, env_filename,
                       job_file, tmpdir):
    '''Test that the `graph` command produces syntactically valid graphviz
    files.'''
    pydot = pytest.importorskip('pydot')
    output_file = tmpdir / 'graph.dot'
    args = ['graph', '-o', str(output_file)]
    if dependencies is not None:
        args.append('--dependencies')
        args.append(dependencies)
    if target is not None:
        args.append(target)
    run_valjean(args, job_config=job_config, config=config_tmp,
                env_filename=env_filename, job_file=job_file)
    graph = output_file.read()
    pydot.graph_from_dot_data(graph)


def test_env(job_config, config_tmp, env_filename, job_file, capsys):
    '''Test the `env` command.'''
    run_valjean(['run'], job_config=job_config, config=config_tmp,
                env_filename=env_filename, job_file=job_file)
    for name in ('checkout_cecho', 'build_cecho',
                 'pling.cecho', 'plong.cecho'):
        output_root = config_tmp.get('path', 'output-root')
        args = ['env', str(Path(output_root) / name / env_filename)]
        run_valjean(args, job_config=job_config, config=config_tmp,
                    env_filename=env_filename, job_file=job_file)
        captured = capsys.readouterr()
        assert captured.out.startswith('{{{!r}:'.format(name))
        assert "'output_dir':" in captured.out
        assert "'status':" in captured.out
        assert "'start_clock':" in captured.out
        assert "'end_clock':" in captured.out
        assert "'elapsed_time':" in captured.out
