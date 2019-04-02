'''Integration tests for the happy path of :command:`valjean` execution.'''

import logging

import pytest

# pylint: disable=wrong-import-order
from ..context import valjean   # pylint: disable=unused-import
from valjean import LOGGER
from valjean.cambronne.main import main
from valjean.cosette.env import Env
from valjean.cosette.task import TaskStatus

from ..cosette.conftest import requires_git, requires_cmake


def run_valjean(*other_args, job_config, env_path):
    '''Run :command:`valjean` using the specified arguments.'''
    args = ['-c', str(job_config), '--env-path', str(env_path)]
    if LOGGER.getEffectiveLevel() == logging.DEBUG:
        args.append('-v')
    args.extend(*other_args)
    main(args)
    env = Env.from_file(str(env_path))
    return env


def assert_task_done(env, name):
    '''Assert that the task with the given name is present in the environment
    and has been successfully completed.'''
    assert name in env
    assert 'status' in env[name]
    assert env[name]['status'] == TaskStatus.DONE


@requires_git
@pytest.mark.parametrize('target', [None, 'checkout_cecho'],
                         ids=['no target', 'checkout_cecho'])
def test_checkout(job_config, target, env_path):
    '''Test the `checkout` command.'''
    args = ['checkout']
    if target is not None:
        args.append(target)
    env = run_valjean(args, job_config=job_config, env_path=env_path)
    assert_task_done(env, 'checkout_cecho')
    assert 'build_cecho' not in env


@requires_git
@requires_cmake
@pytest.mark.parametrize('target', [None, 'checkout_cecho', 'build_cecho'],
                         ids=['no target', 'checkout_cecho', 'build_cecho'])
def test_build(job_config, target, env_path):
    '''Test the `build` command.'''
    args = ['build']
    if target is not None:
        args.append(target)
    env = run_valjean(args, job_config=job_config, env_path=env_path)
    assert_task_done(env, 'checkout_cecho')
    if target != 'checkout_cecho':
        assert_task_done(env, 'build_cecho')
    else:
        assert 'build_cecho' not in env


@requires_git
@requires_cmake
def test_resume(job_config, env_path):
    '''Test that running `checkout` followed by `build` does not rerun
    `checkout`.'''
    env = run_valjean(['checkout'], job_config=job_config, env_path=env_path)
    assert_task_done(env, 'checkout_cecho')
    assert 'elapsed_time' in env['checkout_cecho']
    assert 'build_cecho' not in env
    elapsed = env['checkout_cecho']['elapsed_time']

    env = run_valjean(['build'], job_config=job_config, env_path=env_path)
    assert_task_done(env, 'checkout_cecho')
    assert 'elapsed_time' in env['checkout_cecho']
    assert env['checkout_cecho']['elapsed_time'] == elapsed
    assert_task_done(env, 'build_cecho')


@requires_git
@requires_cmake
@pytest.mark.parametrize('target', [None, 'checkout_cecho', 'build_cecho',
                                    'pling', 'plong'],
                         ids=['no target', 'checkout_cecho', 'build_cecho',
                              'pling', 'plong'])
def test_run(job_config, target, env_path):
    '''Test the `run` command.'''
    args = ['run']
    if target is not None:
        args.append(target)
    env = run_valjean(args, job_config=job_config, env_path=env_path)
    assert_task_done(env, 'checkout_cecho')
    if target != 'checkout_cecho':
        assert_task_done(env, 'build_cecho')
    if target == 'pling':
        assert_task_done(env, 'pling')
        assert 'plong' not in env
    elif target == 'plong':
        assert_task_done(env, 'plong')
        assert 'pling' not in env
    elif target is None:
        assert_task_done(env, 'pling')
        assert_task_done(env, 'plong')


@pytest.mark.parametrize('target', [None, 'checkout_cecho', 'build_cecho'],
                         ids=['no target', 'checkout_cecho', 'build_cecho'])
@pytest.mark.parametrize('dependencies', [None, 'hard', 'soft', 'both'])
def test_graph(job_config, target, dependencies, env_path, capsys):
    '''Test that the `graph` command produces syntactically valid graphviz
    files.'''
    pydot = pytest.importorskip('pydot')
    args = ['graph']
    if dependencies is not None:
        args.append('--dependencies')
        args.append(dependencies)
    if target is not None:
        args.append(target)
    run_valjean(args, job_config=job_config, env_path=env_path)
    captured = capsys.readouterr()
    pydot.graph_from_dot_data(captured.out)


@pytest.mark.parametrize('target', [None, 'checkout_cecho', 'build_cecho'],
                         ids=['no target', 'checkout_cecho', 'build_cecho'])
@pytest.mark.parametrize('dependencies', [None, 'hard', 'soft', 'both'])
def test_graph_on_file(job_config, target, dependencies, env_path, tmpdir):
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
    run_valjean(args, job_config=job_config, env_path=env_path)
    graph = output_file.read()
    pydot.graph_from_dot_data(graph)
