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

        # filter only requested tasks
        if args.targets:
            tasks = [task for task in collected_tasks
                     if task.name in args.targets]
        else:
            tasks = collected_tasks
        LOGGER.debug('building graph for tasks: %s', tasks)
        graph = build_graph(tasks)

        env_mode = '' if args.env_skip_read else 'r'
        env_mode += '' if args.env_skip_write else 'w'
        return schedule(graph, env_path=args.env_path,
                        env_format=args.env_format, env_mode=env_mode,
                        config=config)


def build_graph(tasks):
    '''Build a dependency graph according to the CLI parameters and the
    configuration.'''

    graph = DepGraph()
    for task in tasks:
        graph.add_node(task)
        for dep in task.depends_on:
            graph.add_dependency(task, on=dep)

    return graph


def schedule(graph, *,
             env_path=None, env_format='json', env_mode='rw', config=None):
    '''Schedule a graph for execution.

    The additional parameters control the behaviour of the scheduler with
    respect to persistent execution environments. If `env_mode` contains
    ``'w'``, the environment will be written to the file specified by
    `env_path` at the end of the run, in the format specified by `env_format`
    (either ``'json'`` or ``'pickle'``).

    Also, if `env_mode` contains ``'r'``, the environment will be read from
    `env_path` at the beginning of the run.

    If `env_path` is `None`, no serialization/de-serialization will take place.

    :param env_path: Path to the serialized environment. If `None`, no
                     serialization/de-serialzation will take place.
    :type env_path: str or None
    :param str env_format: Environment serialization format (``'json'``,
                            ``'pickle'``).
    :param str env_mode: Possible values: ``'r'`` (read-only), ``'w'``
                         (write-only), ``'rw'`` (read and write).
    '''
    scheduler = Scheduler(graph)
    env = Env.from_graph(graph)

    if env_path is not None and 'r' in env_mode:
        LOGGER.info('deserializing %s environment from file %s',
                    env_format, env_path)
        persistent_env = Env.from_file(env_path, env_format)
        if persistent_env is not None:
            env.merge_done_tasks(persistent_env)
    else:
        LOGGER.debug('starting with an empty environment')

    new_env = scheduler.schedule(env=env, config=config)

    if new_env is not None and env_path is not None and 'w' in env_mode:
        LOGGER.info('serializing %s environment to file %s',
                    env_format, env_path)
        new_env.to_file(env_path, env_format)
    else:
        LOGGER.debug('skipping environment serialization')

    LOGGER.debug('resulting environment: %s', new_env)
    return new_env
