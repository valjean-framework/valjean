'''Integration tests for the happy path of :command:`valjean` execution.'''

from shutil import rmtree
from pathlib import Path

import pytest

# pylint: disable=wrong-import-order
from ..context import valjean   # pylint: disable=unused-import
from valjean.cosette.task import TaskStatus

from ..cosette.conftest import requires_git, requires_cmake
from .conftest import call_valjean, run_valjean


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


def do_test_run(*args, job_config,  # pylint: disable=too-many-arguments
                config_tmp, env_filename, subdir, job_file,
                expected):
    '''Actually run the test for the `run` command.'''
    env = run_valjean(job_config=job_config, config=config_tmp,
                      env_filename=env_filename, job_file=job_file, *args)
    assert_task_done(env, 'checkout_cecho')
    assert_task_done(env, 'build_cecho')
    assert_cecho_exists(env, 'build_cecho', subdir)
    assert_task_done(env, 'pling.cecho')
    assert_task_done(env, 'plong.cecho')
    for prefix in ('pling', 'plong'):
        task = prefix + '.cecho'
        assert 'output_dir' in env[task]
        assert 'stdout' in env[task]
        assert 'result' in env[task]
        assert env[task]['stdout'] == env[task]['result']
        content = Path(env[task]['stdout']).read_text()
        assert content == prefix + expected


@requires_git
@requires_cmake
def test_run(job_config,  # pylint: disable=too-many-arguments
             config_tmp, env_filename, subdir, job_file):
    '''Test the `run` command.'''
    do_test_run(job_config=job_config, config_tmp=config_tmp,
                env_filename=env_filename, subdir=subdir, job_file=job_file,
                expected=' it\n')


@requires_git
@requires_cmake
def test_run_kwarg(job_config,  # pylint: disable=too-many-arguments
                   config_tmp, env_filename, subdir, job_file):
    '''Test the ``-k`` cli option.'''
    do_test_run('-k', 'what=the thing',
                job_config=job_config, config_tmp=config_tmp,
                env_filename=env_filename, subdir=subdir, job_file=job_file,
                expected=' the thing\n')


@requires_git
@requires_cmake
def test_resume(job_config, config_tmp, env_filename, subdir, job_file):
    '''Test that running twice does not rerun done tasks.'''
    env_1 = run_valjean(job_config=job_config, config=config_tmp,
                        env_filename=env_filename, job_file=job_file)
    assert_cecho_exists(env_1, 'build_cecho', subdir)
    for task_name in ('checkout_cecho', 'build_cecho', 'pling.cecho',
                      'plong.cecho'):
        assert_task_done(env_1, task_name)

    env_2 = run_valjean(job_config=job_config, config=config_tmp,
                        env_filename=env_filename, job_file=job_file)
    assert_cecho_exists(env_2, 'build_cecho', subdir)
    for task_name in ('checkout_cecho', 'build_cecho', 'pling.cecho',
                      'plong.cecho'):
        assert_task_done(env_2, task_name)
        env_1[task_name]['elapsed_time'] = env_2[task_name]['elapsed_time']
        env_1[task_name]['start_clock'] = env_2[task_name]['start_clock']
        env_1[task_name]['end_clock'] = env_2[task_name]['end_clock']


@requires_git
@requires_cmake
def test_resume_newer(job_config, config_tmp, env_filename, subdir, job_file):
    '''Test that running `checkout` followed by `build`, followed by a forced
    `checkout` again triggers a new `build` run.'''
    env = run_valjean(job_config=job_config, config=config_tmp,
                      env_filename=env_filename, job_file=job_file)
    assert_task_done(env, 'checkout_cecho')
    assert_task_done(env, 'build_cecho')
    assert 'start_clock' in env['build_cecho']
    assert 'end_clock' in env['build_cecho']
    start_clock = env['build_cecho']['start_clock']
    end_clock = env['build_cecho']['end_clock']

    # remove the checkout directory
    rmtree(env['checkout_cecho']['output_dir'])
    env = run_valjean(job_config=job_config, config=config_tmp,
                      env_filename=env_filename, job_file=job_file)
    assert_task_done(env, 'build_cecho')
    assert 'start_clock' in env['build_cecho']
    assert 'end_clock' in env['build_cecho']
    assert start_clock < env['build_cecho']['start_clock']
    assert end_clock < env['build_cecho']['end_clock']
    assert_cecho_exists(env, 'build_cecho', subdir)


@pytest.mark.parametrize('dependencies', [None, 'hard', 'soft', 'both'])
def test_graph(dependencies, job_file, capsys):
    '''Test that the `graph` command produces syntactically valid graphviz
    files.'''
    pydot = pytest.importorskip('pydot')
    args = ['graph', str(job_file)]
    if dependencies is not None:
        args.extend(('--dependencies', dependencies))
    call_valjean(*args)
    captured = capsys.readouterr()
    pydot.graph_from_dot_data(captured.out)


@pytest.mark.parametrize('dependencies', [None, 'hard', 'soft', 'both'])
def test_graph_on_file(dependencies, job_file, tmp_path):
    '''Test that the `graph` command produces syntactically valid graphviz
    files.'''
    pydot = pytest.importorskip('pydot')
    output_file = tmp_path / 'graph.dot'
    args = ['graph', str(job_file), '-o', str(output_file)]
    if dependencies is not None:
        args.extend(('--dependencies', dependencies))
    call_valjean(*args)
    graph = output_file.read_text()
    pydot.graph_from_dot_data(graph)


def test_env(job_config, config_tmp, env_filename, job_file, capsys):
    '''Test the `env` command.'''
    run_valjean(job_config=job_config, config=config_tmp,
                env_filename=env_filename, job_file=job_file)
    for name in ('checkout_cecho', 'build_cecho',
                 'pling.cecho', 'plong.cecho'):
        output_root = config_tmp.get('path', 'output-root')
        args = ['env', str(Path(output_root) / name / env_filename)]
        call_valjean(*args)
        captured = capsys.readouterr()
        assert captured.out.startswith('{{{!r}:'.format(name)), captured
        assert "'output_dir':" in captured.out
        assert "'status':" in captured.out
        assert "'start_clock':" in captured.out
        assert "'end_clock':" in captured.out
        assert "'elapsed_time':" in captured.out
