'''Common utilities for :program:`valjean` commands.'''

import argparse

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
        LOGGER.info('hard_graph contains %s tasks', len(hard_graph))
        LOGGER.info('soft_graph contains %s tasks', len(soft_graph))
        LOGGER.info('will schedule up to %d tasks in parallel', args.workers)

        env = init_env(path=args.env_path, skip_read=args.env_skip_read,
                       fmt=args.env_format)
        new_env = schedule(hard_graph=hard_graph, soft_graph=soft_graph,
                           env=env, config=config, workers=args.workers)

        self.task_diagnostics(tasks=collected_tasks,
                              env=new_env, config=config)

        if not args.env_skip_write:
            write_env(env=env, path=args.env_path, fmt=args.env_format)
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
        from pathlib import Path
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


def init_env(*, path, skip_read, fmt):
    '''Create an initial environment for the given tasks, possibly merging a
    serialized environment.

    The environment will be created from the given tasks. If `skip_read` is
    `False`, the environment will be read from `path` and merged.

    If `path` is `None`, no de-serialization will take place.

    :param path: Path to the serialized environment. If `None`, no
                 de-serialzation will take place.
    :type path: str or None
    :param bool skip_read: If `True`, the environment will not be deserialized
                           from the given file.
    :param str fmt: Environment serialization format (only ``'pickle'`` is
                    supported at the moment).
    '''
    env = Env()
    if path is not None and not skip_read:
        LOGGER.info('deserializing %s environment from file %s',
                    fmt, path)
        persistent_env = Env.from_file(path, fmt)
        if persistent_env is not None:
            env.merge_done_tasks(persistent_env)
    LOGGER.debug('returning environment: %s', env)
    return env


def write_env(env, *, path, fmt):
    '''Serialize the environment to the given file. If `path` is `None`, no
    serialization will take place.

    :param Env env: The environment to serialize.
    :param path: Path to file to be written. If `None`, no serialzation will
                 take place.
    :type path: str or None
    :param str fmt: Environment serialization format (only ``'pickle'`` is
                    supported at the moment).
    '''
    if env is not None and path is not None:
        LOGGER.info('serializing %s environment to file %s',
                    fmt, path)
        env.to_file(path, fmt)
    else:
        LOGGER.debug('skipping environment serialization')


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
