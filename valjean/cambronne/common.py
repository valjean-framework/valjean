'''Common utilities for :program:`valjean` commands.'''

import argparse
from pathlib import Path

from ..cosette.depgraph import DepGraph
from ..cosette.env import Env
from ..cosette.scheduler import Scheduler
from ..cosette.backends.queue import QueueScheduling
from ..cosette.task import TaskStatus
from .. import LOGGER


class Command:
    '''Base class for all :program:`valjean` subcommands.'''

    ALIASES = ()

    def register(self, parser):
        '''Register options for this command in the parser.'''
        parser.add_argument('targets', metavar='TARGET', nargs='*',
                            action=UniqueAppendAction,
                            help='targets to process')
        parser.set_defaults(func=self.execute)

    # pylint: disable=no-self-use
    def execute(self, args, collected_tasks, config):
        '''Execute a generic command.'''

        LOGGER.debug('building graphs for tasks: %s', collected_tasks)
        hard_graph, soft_graph = build_graphs(collected_tasks)
        LOGGER.debug('resulting hard_graph: %s', hard_graph)
        LOGGER.debug('resulting soft_graph: %s', soft_graph)
        LOGGER.info('hard_graph contains %d tasks', len(hard_graph))
        LOGGER.info('soft_graph contains %d tasks', len(soft_graph))
        LOGGER.info('will schedule up to %d tasks in parallel', args.workers)

        output_root = config.get('path', 'output-root')
        task_names = [task.name for task in collected_tasks]
        env = read_env(root=output_root, names=task_names,
                       filename=args.env_filename, fmt=args.env_format)
        new_env = schedule(hard_graph=hard_graph, soft_graph=soft_graph,
                           env=env, config=config, workers=args.workers)

        self.task_diagnostics(tasks=collected_tasks,
                              env=new_env, config=config)

        if not args.env_skip_write:
            write_env(env, filename=args.env_filename, fmt=args.env_format)
        return new_env

    @classmethod
    def task_diagnostics(cls, *, tasks, env, config):
        '''Emit diagnostic messages about the status of the tasks. Count how
        many have succeeded, how many have failed, etc.  If any tasks have
        failed, this method writes their names in a file called 'failed_tasks'
        in the log directory.

        :param tasks: the tasks that have been scheduled.
        :type tasks: list(Task)
        :param Env env: the environment.
        :param Config config: the configuration object.
        '''
        from collections import Counter
        count_status = Counter()
        missing = []
        failed = []
        for task in tasks:
            task_name = task.name
            if task_name in env:
                status = env[task.name]['status']
                count_status[status] += 1
                if status == TaskStatus.FAILED:
                    failed.append(task_name)
            else:
                missing.append(task_name)

        if missing:
            LOGGER.warning('the following %s tasks are missing from the '
                           'environment: %s',
                           len(missing), '\n  '.join(missing))

        total_graph = len(tasks)
        msgs = ('{:>7}: {}/{} ({:5.1f}%)'
                .format(status.name, count, total_graph, 100*count/total_graph)
                for status, count in count_status.items())
        LOGGER.info('final environment statistics:\n  %s',
                    '\n  '.join(msgs))

        cls.write_failed_tasks(failed=failed, config=config)

    @classmethod
    def write_failed_tasks(cls, *, failed, config):
        '''Write the names of the failed tasks in the ``failed_tasks`` file.

        :param list(str) failed: the names of the failed tasks.
        :param Config config: the configuration object.
        '''
        if not failed:
            return
        log_root = config.get('path', 'log-root')
        failed_fname = Path(log_root, 'failed-tasks')
        with failed_fname.open('w') as failed_file:
            for task in failed:
                failed_file.write(task + '\n')


def build_graphs(tasks):
    '''Build the dependency graphs according to the CLI parameters and the
    configuration.'''

    hard_graph = DepGraph()
    soft_graph = DepGraph()
    for task in tasks:
        hard_graph.add_node(task)
        soft_graph.add_node(task)
        for dep in task.depends_on:
            hard_graph.add_dependency(task, on=dep)
        for dep in task.soft_depends_on:
            soft_graph.add_dependency(task, on=dep)

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


def schedule(*, hard_graph, soft_graph, env, config=None, workers=1):
    '''Schedule a graph for execution.

    '''
    scheduler = Scheduler(hard_graph=hard_graph, soft_graph=soft_graph,
                          backend=QueueScheduling(workers))
    new_env = scheduler.schedule(env=env, config=config)
    LOGGER.debug('resulting environment: %s', new_env)
    return new_env


class UniqueAppendAction(argparse.Action):
    ''':mod:`argparse` action that stores option arguments in a set instead of
    a list (no duplicates).'''
    def __call__(self, parser, namespace, values, option_string=None):
        unique_values = set(values)
        setattr(namespace, self.dest, unique_values)
