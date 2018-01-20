'''Common utilities for :program:`valjean` commands.'''

import argparse

from ..cosette.task import RunTask
from ..cosette.code import CheckoutTask, BuildTask
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

    ALIASES = []

    FAMILY = None

    def register(self, parser):
        '''Register options for this command in the parser.'''
        parser.add_argument(
            'targets', metavar='TARGET', nargs='*',
            action=UniqueAppendAction,
            help='targets to process'
            )
        parser.set_defaults(func=self.execute)

    def execute(self, args, config):
        '''Execute a generic command.'''
        if args.targets:
            family_targets = [(self.FAMILY, target) for target in args.targets]
        else:
            family_targets = [(self.FAMILY, None)]
        graph = build_graph(family_targets, config)

        env_mode = '' if args.env_skip_read else 'r'
        env_mode += '' if args.env_skip_write else 'w'
        return schedule(graph, env_path=args.env_path,
                        env_format=args.env_format, env_mode=env_mode)


class TaskFactory:
    '''Factory class to generate tasks from a list of targets.

    A :program:`valjean` run proceeds in a number of phases (i.e. checkout,
    build, run, test...). The sequence of phases is stored in the `PHASES`
    class attribute as an association list of ``(phase_name, class)`` pairs. At
    construction, the factory can be configured to generate tasks from a given
    range of phases using the `start_from` and `up_to` parameters.
    '''

    #: Association list of execution phases. Each item is of the form
    #: ``(phase_name, class)``, where ``phase_name`` is the name of the phase,
    #: as a string, and ``class`` is the class of the tasks for the given
    #: phase.
    PHASES = {'checkout': CheckoutTask,
              'build': BuildTask,
              'run': RunTask}

    def __init__(self, config):
        '''Initialize a factory.

        :param Config config: The configuration object.
        '''
        self.config = config

    def make_task(self, command, name):
        '''Create a task given a command and a task name.

        :param str command: The name of the command for which the task should
                            be created. If the command is known to the factory
                            (i.e. if it appears as a key in the `PHASES`
                            dictionary), a suitable task will be created.
        :param str name: The name of the task.
        '''
        LOGGER.debug('making task for command %s, name %s', command, name)
        cls = self.PHASES.get(command, None)
        LOGGER.debug('task class is %s', cls)
        if cls is None:
            return None
        task = cls.from_config(name, self.config)
        return task

    def make_tasks(self, command_targets):
        '''Create tasks given a list of command/target pairs

        :param str command_targets: A list of pairs of the form ``(command,
                                    name)``.
        '''
        tasks_by_name = {}
        LOGGER.debug('making tasks for command/targets %s', command_targets)
        for command, target in command_targets:
            task_name = '/'.join((command, target))
            if task_name in tasks_by_name:
                continue
            task = self.make_task(command, target)
            if task is None:
                continue
            try:
                assert task_name == task.name
            except AssertionError:
                LOGGER.fatal('%s != %s', task_name, task.name)
                raise
            tasks_by_name[task_name] = task
            for dep in task.depends_on:
                dep_command, dep_name = self.config.split_section(dep)
                dep_tasks = self.make_tasks([(dep_command, dep_name)])
                tasks_by_name.update(dep_tasks)

        return tasks_by_name


def build_graph(family_targets, config):
    '''Build a dependency graph according to the CLI parameters and the
    configuration.'''

    graph = DepGraph()

    factory = TaskFactory(config)

    expanded_family_targets = []
    for fam, tar in family_targets:
        if fam is None and tar is None:
            LOGGER.debug('building graph for all family/targets')
            expanded_family_targets.extend(
                config.split_section(sec_name)
                for sec_name in config.sections()
                )
        elif tar is None:
            LOGGER.debug('implicit targets for family: %s', fam)
            expanded_family_targets.extend(
                (fam, t) for _, t in config.sections_by_family(fam)
                )
        elif fam is None:
            LOGGER.debug('implicit families for target: %s', tar)
            for sec_name in config.sections():
                sec_split = config.split_section(sec_name)
                if tar == sec_split[1]:
                    expanded_family_targets.append(sec_split)
        else:
            LOGGER.debug('explicit family/target pair: %s, %s',
                         fam, tar)
            expanded_family_targets.append(fam, tar)

    tasks_by_name = factory.make_tasks(expanded_family_targets)
    for task in tasks_by_name.values():
        graph.add_node(task)
        for dep in task.depends_on:
            if dep in tasks_by_name:
                graph.add_dependency(task, on=tasks_by_name[dep])

    return graph


def schedule(graph, env_path=None, env_format='json', env_mode='rw'):
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

    new_env = scheduler.schedule(env)

    if new_env is not None and env_path is not None and 'w' in env_mode:
        LOGGER.info('serializing %s environment to file %s',
                    env_format, env_path)
        new_env.to_file(env_path, env_format)
    else:
        LOGGER.debug('skipping environment serialization')

    LOGGER.info(new_env)
    return new_env
