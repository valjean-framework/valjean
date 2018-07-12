'''Fixtures for the :mod:`~.valjean.cosette` tests.'''
# pylint: disable=redefined-outer-name

import os
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
requires_cmake, _CMAKE_VERSION = make_skip_marker(BuildTask.CMAKE,
                                                  r'^cmake version (.*)')
HAS_CMAKE = not requires_cmake.args[0]
requires_git, _ = make_skip_marker(CheckoutTask.GIT,
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

    check_call([CheckoutTask.GIT, 'init', project_dir],
               stdout=DEVNULL, stderr=DEVNULL)
    git_dir = os.path.join(project_dir, '.git')
    check_call([CheckoutTask.GIT, '--git-dir', git_dir,
                '--work-tree', project_dir, 'add', filename],
               stdout=DEVNULL, stderr=DEVNULL)
    check_call([CheckoutTask.GIT, '--git-dir', git_dir,
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


# pylint: disable=too-many-arguments
@composite
def dep_dicts(draw, elements=integers(0, 10), min_deps=0, max_deps=None,
              **kwargs):
    '''Composite Hypothesis strategy to generate acyclic dependency
    dictionaries.'''
    keys = draw(lists(elements, unique=True, **kwargs).map(sorted))
    dag = {}
    for i, key in enumerate(keys):
        vals = draw(sets(sampled_from(keys[i+1:]),
                         min_size=min_deps,
                         max_size=max_deps))
        dag[key] = vals
    return dag


#######################
#  depgraph fixtures  #
#######################

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

class DoNothingTask(Task):
    '''A task that does nothing.'''

    def do(self, _):
        '''What it says on the tin!'''
        pass


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


@pytest.fixture(scope='function', params=['json', 'pickle'])
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
    def do(self, env):
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
                min_size=None, max_size=None):
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
