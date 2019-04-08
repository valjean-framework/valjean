'''Fixtures for the :mod:`~.valjean.cosette` tests.'''
# pylint: disable=redefined-outer-name

import re
from subprocess import check_call, check_output, DEVNULL, CalledProcessError

import pytest
from hypothesis.strategies import (integers, sets, lists, composite,
                                   sampled_from, text, dictionaries, one_of,
                                   just, floats)

# pylint: disable=wrong-import-order
from ..context import valjean  # noqa: F401, pylint: disable=unused-import
from valjean.cosette.code import CheckoutTask, BuildTask
from valjean.cosette.depgraph import DepGraph
from valjean.cosette.task import Task, TaskStatus, DelayTask
from valjean.cosette.env import Env
from valjean.cosette.rlist import RList
from valjean.config import Config
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
            reason = ('could not parse version string for ' + command
                      + ', needed for this test')
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
requires_cmake, _CMAKE_VERSION = make_skip_marker(BuildTask.CMAKE,
                                                  r'^cmake version (.*)')
HAS_CMAKE = not requires_cmake.args[0]
requires_git, _ = make_skip_marker(CheckoutTask.GIT,
                                   r'^git version (.*)$')
HAS_GIT = not requires_git.args[0]


@pytest.fixture(scope='function', params=['test', 'test with space'])
def task_name(request):
    '''Return possible names for tasks.'''
    return request.param


#####################################
#  fixture for project generation  ##
#####################################

CMAKELISTS = r'''project(TestCodeTasks C)
cmake_minimum_required(VERSION ''' + _CMAKE_VERSION + ''')
set(SOURCE_FILENAME "${PROJECT_BINARY_DIR}/test.c")
file(WRITE "${SOURCE_FILENAME}" "int main(){return 0;}")
add_executable(test_exe "${SOURCE_FILENAME}")
'''


def setup_project(project_path):
    '''Set up a minimalist project for testing in the given directory.

    The project consists of a git repository containing a simple
    `CMakelists.txt` file.

    :param project_path: the path to an existing directory
    :type project_path: :class:`~py._path.local.LocalPath`
    '''
    LOGGER.debug('Setting up a git/CMake project in %s', project_path)
    LOGGER.debug('HAS_GIT: %s', HAS_GIT)
    LOGGER.debug('HAS_CMAKE: %s', HAS_CMAKE)

    filename = project_path / 'CMakeLists.txt'
    with filename.open('w') as cmakelists_file:
        cmakelists_file.write(CMAKELISTS)

    make_git_repo(project_path)


def make_git_repo(path):
    '''Turn path into a git repository.

    This function adds to the git repository all the files that are contained
    in `path`.
    '''
    if not HAS_GIT:
        return
    path_str = str(path)
    filenames = path.listdir()
    check_call([CheckoutTask.GIT, 'init', path_str],
               stdout=DEVNULL, stderr=DEVNULL)
    git_dir = str(path / '.git')
    for filename in filenames:
        check_call([CheckoutTask.GIT, '--git-dir', git_dir,
                    '--work-tree', path_str, 'add', str(filename)],
                   stdout=DEVNULL, stderr=DEVNULL)
    check_call([CheckoutTask.GIT, '--git-dir', git_dir,
                '--work-tree', path_str, 'commit', '-m', 'Test commit'],
               stdout=DEVNULL, stderr=DEVNULL)


#########################################
#  fixtures for CheckoutTask/BuildTask  #
#########################################

@pytest.fixture(scope='function')
def project(tmpdir_factory):
    '''Set up a git project with a CMake file.'''
    project_path = tmpdir_factory.mktemp('project')
    project_path.chmod(0o700)
    setup_project(project_path)
    project_path.chmod(0o500, rec=True)
    yield project_path
    project_path.chmod(0o700, rec=True)


# git-related fixtures

@pytest.fixture(scope='function', params=['master', None],
                ids=['master', 'no ref'])
def git_ref(request):
    '''Return possible values of the `ref` option for git checkout.'''
    return request.param


@pytest.fixture(scope='function', params=[['--depth', '1'], None],
                ids=['depth=1', 'no flags'])
def git_flags(request):
    '''Return possible values of the `flags` option for git checkout.'''
    return request.param


@pytest.fixture(scope='function')
def config_tmp(tmpdir_factory):
    '''Create a configuration object with the path options set to temporary
    directories.'''
    log_dir = str(tmpdir_factory.mktemp('log'))
    checkout_dir = str(tmpdir_factory.mktemp('checkout'))
    build_dir = str(tmpdir_factory.mktemp('build'))
    run_dir = str(tmpdir_factory.mktemp('run'))
    config = Config(paths=[])
    config.set('path', 'log-root', log_dir)
    config.set('path', 'checkout-root', checkout_dir)
    config.set('path', 'build-root', build_dir)
    config.set('path', 'run-root', run_dir)
    return config


@pytest.fixture(scope='function', params=['svn', 'cvs', 'copy'])
def notimpl_vcs(request):
    '''Return the unimplemented version-control systems.'''
    return request.param


# cmake-related fixtures

@pytest.fixture(scope='function', params=[['-DCMAKE_BUILD_TYPE=Debug'], None],
                ids=['with configure flags', 'without configure flags'])
def cmake_configure_flags(request):
    '''Return possible values of the configuration flags for CMake builds.'''
    return request.param


@pytest.fixture(scope='function', params=[['--', '-j1'], None],
                ids=['with build flags', 'without build flags'])
def cmake_build_flags(request):
    '''Return possible values of the build flags for CMake builds.'''
    return request.param


@pytest.fixture(scope='function', params=[['test_exe', 'all'], ['test_exe'],
                                          None],
                ids=['two targets', 'one target', 'no target'])
def cmake_targets(request):
    '''Return possible values of the target option for CMake builds.'''
    return request.param


@pytest.fixture(scope='function', params=['autoconf', 'configure'])
def notimpl_build(request):
    '''Return the unimplemented build systems.'''
    return request.param


#########################################
#  fixtures for RunTask/RunTaskFactory  #
#########################################

@pytest.fixture(scope='function',
                params=('', 'subdir'),
                ids=('without relative_path', 'with relative_path'))
def subdir(request):
    '''Return a name for a subdirectory, or an empty string for no subdir.

    This fixture is used to parametrize the :class:`~.RunTaskFactory` tests.
    '''
    return request.param


@pytest.fixture(scope='function')
def git_myecho_repo(tmpdir_factory, subdir):
    '''Set up a git project with the :command:`echo` command.'''
    import py
    project_path = tmpdir_factory.mktemp('project')
    project_path.chmod(0o700)
    myecho_dir = project_path / subdir
    myecho_dir.ensure(dir=True)
    myecho = myecho_dir / 'myecho'
    echo = py.path.local('/bin/echo')
    echo.copy(myecho, mode=True)
    make_git_repo(project_path)
    project_path.chmod(0o500, rec=True)
    yield project_path
    project_path.chmod(0o700, rec=True)


CECHO_CMAKE = r'''project(CEcho C)
cmake_minimum_required(VERSION ''' + _CMAKE_VERSION + ''')
add_executable(cecho "${{PROJECT_SOURCE_DIR}}/cecho.c")
set_target_properties(cecho PROPERTIES RUNTIME_OUTPUT_DIRECTORY
                      "${{PROJECT_BINARY_DIR}}{}")
'''
CECHO_C = r'''#include <stdio.h>
int main(int argc, char **argv)
{
  int i;
  for(i=1; i<argc-1; ++i) {
    printf("%s ", argv[i]);
  }
  printf("%s\n", argv[argc-1]);
  return 0;
}
'''


@pytest.fixture(scope='function')
def cmake_echo(tmpdir_factory, subdir):
    '''Set up a CMake project with a CMake file.'''
    project_path = tmpdir_factory.mktemp('project')
    project_path.chmod(0o700)
    cmakelists = project_path / 'CMakeLists.txt'
    if subdir:
        subdir = '/' + subdir
    cmakelists.ensure(file=True).write(CECHO_CMAKE.format(subdir))
    cecho = project_path / 'cecho.c'
    cecho.ensure(file=True).write(CECHO_C)
    make_git_repo(project_path)
    project_path.chmod(0o500, rec=True)
    yield project_path
    project_path.chmod(0o700, rec=True)


#######################
#  depgraph fixtures  #
#######################

# pylint: disable=too-many-arguments
@composite
def dep_dicts(draw, elements=integers(0, 10), min_deps=0, max_deps=None,
              **kwargs):
    '''Composite Hypothesis strategy to generate acyclic dependency
    dictionaries.'''
    keys = draw(lists(elements, unique=True, **kwargs).map(sorted))
    dag = {}
    for i, key in enumerate(keys):
        if i == len(keys) - 1:
            vals = set()
        else:
            vals = draw(sets(sampled_from(keys[i+1:]),
                             min_size=min_deps,
                             max_size=max_deps))
        dag[key] = vals
    return dag


class DoNothingTask(Task):
    '''A task that does nothing.'''
    def do(self, _env, _config):
        '''Do nothing!'''


@composite
def dep_tasks(draw, names=text(min_size=1), min_deps=0, max_deps=None,
              **kwargs):
    '''Composite Hypothesis strategy to generate a list of
    interdependent :class:`DoNothingTask` objects (no dependency cycles
    though!).'''
    dep_dict = draw(dep_dicts(elements=names, min_deps=min_deps,
                              max_deps=max_deps, **kwargs))

    def to_task(dep_dict, task_name, task_dict):
        if task_name in task_dict:
            return task_dict[task_name]
        deps = [to_task(dep_dict, name, task_dict)
                for name in dep_dict[task_name]]
        task = DoNothingTask(task_name, deps=deps)
        task_dict[task_name] = task
        return task

    task_dict = {}
    tasks = [to_task(dep_dict, task_name, task_dict)
             for task_name in dep_dict.keys()]
    return tasks


# pylint: disable=too-many-arguments
@composite
def depgraphs(draw, elements=integers(0, 10), min_deps=0, max_deps=None,
              **kwargs):
    '''Composite Hypothesis strategy to generate acyclic DepGraph objects.'''
    dag = draw(dep_dicts(elements,
                         min_deps=min_deps, max_deps=max_deps,
                         **kwargs))
    return DepGraph.from_dependency_dictionary(dag)


##################
#  env fixtures  #
##################

def env_names():
    '''Strategy to generate names for :class:`~.Env`.'''
    return text(min_size=1)


@composite
def env_keys(draw, from_keys=None, **kwargs):
    '''Generate keys for the :class:`~.Env` dictionary.'''
    # strategies to construct keys, values and status
    # sample the dictionary keys if necessary
    if from_keys is None:
        keys = draw(lists(env_names(), unique=True, **kwargs))
    else:
        keys = draw(lists(sampled_from(from_keys), unique=True, **kwargs))
    return keys


# pylint: disable=no-value-for-parameter
@composite
def envs(draw, keys=env_keys()):
    '''Generate an environment with some random information.'''
    # sample the dictionary keys
    the_keys = draw(keys)

    # strategies to construct keys, values and status
    values_strat = dictionaries(keys=env_names(), values=integers())
    status_strat = one_of(sampled_from(TaskStatus), just(TaskStatus.DONE))

    # sample the values and the status
    n_keys = len(the_keys)
    updates = draw(lists(values_strat, min_size=n_keys, max_size=n_keys))
    statuses = draw(lists(status_strat, min_size=n_keys, max_size=n_keys))

    # build the environment dictionary
    an_env = Env()
    for key, update, status in zip(the_keys, updates, statuses):
        update['status'] = status
        an_env[key] = update

    return an_env


@pytest.fixture(scope='function', params=['pickle'])
def persistence_format(request):
    '''Yield all the available persistence formats.'''
    return request.param


####################
#  rlist fixtures  #
####################

@composite
def reversible_lists(draw, elements=integers(0, 10), **kwargs):
    '''Composite Hypothesis strategy to generate RLists.'''
    lst = draw(lists(elements, **kwargs))
    return RList(lst)


########################
#  scheduler fixtures  #
########################


def make_graph(tasks, randoms, dep_frac):
    '''Create a :class:`.DepGraph` from a list of tasks and a list of random
    values.'''
    task_deps = {}
    all_tasks = []
    for task, random in zip(tasks, randoms):
        if dep_frac > 0.0:
            dependees = [t for t in all_tasks if random < dep_frac]
            task_deps[task] = dependees
        else:
            task_deps[task] = []
        all_tasks.append(task)
    graph = DepGraph.from_dependency_dictionary(task_deps)
    return graph


class FailingTask(Task):
    '''A failing task.'''
    def do(self, env, config):
        '''Raise an exception.'''
        raise Exception


@composite
def graphs(draw, task_strategy, dep_frac=0.0):
    '''Composite Hypothesis strategy to generate a :class:`.DepGraph`.

    :param task_strategy: A hypothesis strategy that generates tasks.
    '''
    tasks = draw(task_strategy)
    n_tasks = len(tasks)
    randoms = draw(lists(floats(min_value=0.0, max_value=1.0),
                         min_size=n_tasks, max_size=n_tasks))
    return make_graph(tasks, randoms, dep_frac)


# pylint: disable=too-many-arguments
@composite
def delay_tasks(draw, min_duration=1e-15, max_duration=1e-5,
                min_size=0, max_size=None):
    '''Composite Hypothesis strategy to generate a list of delay tasks.'''
    durations = draw(
        lists(floats(min_value=min_duration, max_value=max_duration),
              min_size=min_size, max_size=max_size))

    tasks = [DelayTask(str(i), dur) for i, dur in enumerate(durations)]
    return tasks


@composite
def failing_tasks(draw, min_size=1, max_size=20):
    '''Composite Hypothesis strategy to generate a list of failing tasks.'''
    n_tasks = draw(integers(min_value=min_size, max_value=max_size))
    tasks = [FailingTask('FailingTask {}'.format(i)) for i in range(n_tasks)]
    return tasks


@pytest.fixture(scope='function')
def quiet(caplog):
    '''This fixture will temporarily set the level of the ``valjean`` logger to
    CRITICAL, in order to silence any warning/error that may be produced.'''
    import logging
    with caplog.at_level(logging.CRITICAL, logger='valjean'):
        yield
