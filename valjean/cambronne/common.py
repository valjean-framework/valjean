'''Common utilities for :program:`valjean` commands.'''

from pathlib import Path
import sys
import inspect

from ..cosette.env import Env
from ..cosette.depgraph import DepGraph
from ..cosette.task import close_dependency_graph
from .. import LOGGER


class Command:
    '''Base class for all :program:`valjean` subcommands.'''

    ALIASES = ()


class JobCommand(Command):
    '''Base class for all :program:`valjean` subcommands that take a job file
    and job arguments.'''

    @staticmethod
    def register(parser):
        '''Add the `job_file` and `job_args` positional arguments to the
        parser.'''
        parser.add_argument('job_file', action='store', metavar='JOB_FILE',
                            help='path to the job file')
        parser.add_argument('job_args', metavar='ARGUMENT', nargs='*',
                            help='arguments that will be passed to the job() '
                            'function; multiple arguments can be passed')


def run_job(job_file, job_args):
    '''Run the `job()` function from the specified job file and return its
    result.

    :param str job_file: the name of the file containing the `job()` function.
    :param list(str) job_args: the list of arguments to be passed to the
        `job()` function.
    :returns: whatever `job()` returns; expected to be a list of
        :class:`~.Task` objects.
    :rtype: list(Task)
    '''
    from ..dyn_import import dyn_import
    LOGGER.debug('importing job-file: %s', job_file)
    try:
        module = dyn_import(job_file)
    except FileNotFoundError:
        LOGGER.fatal('Cannot find job file %s', job_file)
        sys.exit(1)

    try:
        tasks = module.job(*job_args)
    except TypeError as err:
        if str(err).startswith('job()'):
            signature = inspect.getfullargspec(module.job)
            n_args = len(signature.args)
            new_msg = ('This valjean job expects exactly {} -a/--args '
                       'option(s)'.format(n_args))
            err = TypeError(new_msg)
        raise err
    LOGGER.debug('job tasks: %s', tasks)
    return tasks


def check_unique_task_names(tasks):
    '''Check that the tasks have unique names.

    :param list tasks: A list of tasks.
    :raises ValueError: if two or more tasks have the same name.
    '''
    names = set()
    dups = set()
    for task in tasks:
        if task.name in names:
            dups.add(task.name)
        names.add(task.name)
    if dups:
        dups_str = '\n  '.join(dups)
        err = ('Task names must be unique; the following task names appear '
               'more than once:\n  {}'.format(dups_str))
        raise ValueError(err)


def collect_tasks(job_file, job_args):
    '''Collect tasks from a job file, along with all their dependencies.

    :param str job_file: the name of the file containing the `job()` function.
    :param list(str) job_args: the list of arguments to be passed to the
        `job()` function.
    :returns: the collected tasks.
    :rtype: list(Task)
    '''
    # import the job file and run the job() function
    tasks = run_job(job_file, job_args)
    # compute the transitive closure of the dependency graph for the tasks
    # returned by job()
    tasks = close_dependency_graph(tasks)
    LOGGER.debug('collected tasks: %s', tasks)
    check_unique_task_names(tasks)
    return tasks


def build_graphs(args):
    '''Build the dependency graphs according to the CLI parameters.'''

    tasks = collect_tasks(args.job_file, args.job_args)
    LOGGER.debug('building graphs for tasks: %s', tasks)

    hard_graph = DepGraph()
    soft_graph = DepGraph()
    for task in tasks:
        hard_graph.add_node(task)
        soft_graph.add_node(task)
        for dep in task.depends_on:
            hard_graph.add_dependency(task, on=dep)
        for dep in task.soft_depends_on:
            soft_graph.add_dependency(task, on=dep)

    LOGGER.debug('resulting hard_graph: %s', hard_graph)
    LOGGER.debug('resulting soft_graph: %s', soft_graph)
    return hard_graph, soft_graph


def read_env(*, root, names, filename, fmt):
    '''Create an initial environment for the given task names, possibly merging
    a set of serialized environments.

    The environment will be created from the partial environments that were
    serialized for the given task names. Missing partial environments will be
    silently ignored.

    If `filename` is `None`, no de-serialization will take place and an empty
    environment will be returned.

    :param str root: path to the root directory containing all the
        environment files.
    :param list(str) names: the list of task names that will be deserialized.
    :param filename: Name of the file containing the serialized environment. If
        `None`, no de-serialzation will take place.
    :type filename: str or None
    :param str fmt: Environment serialization format (only ``'pickle'`` is
        supported at the moment).
    :returns: an environment.
    :rtype: Env
    '''
    env = Env()
    if filename is None:
        return env
    LOGGER.info('deserializing %s environment from %r files in %s',
                fmt, filename, root)
    for task_name in names:
        task_file = Path(root) / task_name / filename
        persisted_env = Env.from_file(task_file, fmt=fmt)
        if persisted_env is not None:
            env.merge_done_tasks(persisted_env)
    LOGGER.info('%d environment files found and deserialized', len(env))
    LOGGER.debug('deserialized environment: %s', env)
    return env


def write_env(env, *, filename, fmt):
    '''Serialize the environment to files.

    The environment will be written to one file per task (i.e. one per
    environment key). The name of the environment file is given by the
    `filename` parameter, and the directory is the output directory
    (``'output_dir'`` key) of the task. If the task does not have an
    ``'output_dir'`` key, serialization for that task will be skipped.

    If `filename` is `None`, no serialization will take place at all.

    :param filename: Name of the file containing the serialized environment. If
        `None`, no serialzation will take place.
    :type filename: str or None
    :param str fmt: Environment serialization format (only ``'pickle'`` is
        supported at the moment).
    '''
    if env is None or filename is None:
        LOGGER.debug('skipping environment serialization')
        return
    LOGGER.info('serializing %s environment to %r files', fmt, filename)
    LOGGER.debug('environment to serialize: %s', env)
    written_files = []
    for task_name, subenv in env.items():
        if 'output_dir' not in subenv:
            LOGGER.debug("skipping serialization of task %s because it does "
                         "not have any 'output_dir' key", task_name)
            continue
        task_file = Path(subenv['output_dir']) / filename
        env.to_file(task_file, task_name=task_name, fmt=fmt)
        written_files.append(str(task_file))
    LOGGER.info('%d environment files written', len(written_files))
    LOGGER.debug('list of written environment files: %s', written_files)
