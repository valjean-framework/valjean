'''Common utilities for :program:`valjean` commands.'''

import argparse

from ..cosette.depgraph import DepGraph
from ..cosette.env import Env
from ..cosette.scheduler import Scheduler
from .. import LOGGER


class UniqueAppendAction(argparse.Action):
    ''':mod:`argparse` action that stores option arguments in a set instead of
    a list (no duplicates).'''
    def __call__(self, parser, namespace, values, option_string=None):
        unique_values = set(values)
        setattr(namespace, self.dest, unique_values)


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

        LOGGER.debug('building graph for tasks: %s', collected_tasks)
        graph = build_graph(collected_tasks)
        LOGGER.debug('resulting graph: %s', graph)

        env = init_env(path=args.env_path, skip_read=args.env_skip_read,
                       fmt=args.env_format)
        new_env = schedule(graph, env=env, config=config)
        if not args.env_skip_write:
            write_env(env=env, path=args.env_path, fmt=args.env_format)
        return new_env


def build_graph(tasks):
    '''Build a dependency graph according to the CLI parameters and the
    configuration.'''

    graph = DepGraph()
    for task in tasks:
        graph.add_node(task)
        for dep in task.depends_on:
            graph.add_dependency(task, on=dep)

    return graph


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
        LOGGER.info('attempting to deserialize %s environment from file %s',
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


def schedule(graph, *, env, config=None):
    '''Schedule a graph for execution.

    '''
    scheduler = Scheduler(graph)
    new_env = scheduler.schedule(env=env, config=config)
    LOGGER.debug('resulting environment: %s', new_env)
    return new_env
