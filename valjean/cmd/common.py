'''Common utilities for :program:`valjean` commands.'''

import argparse
from itertools import dropwhile

from ..cosette.task import RunTask
from ..cosette.code import CheckoutTask, BuildTask
from ..cosette.depgraph import DepGraph
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

    def register(self, parser):
        '''Register options for this command in the parser.'''
        parser.add_argument(
            'targets', metavar='TARGET', nargs='*',
            action=UniqueAppendAction,
            help='targets to process'
            )
        parser.set_defaults(func=self.execute)

    def execute(self, args, config):
        '''Execute this command.'''
        raise NotImplementedError('Command must be subclassed.')


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
    PHASES = [('checkout', CheckoutTask),
              ('build', BuildTask),
              ('run', RunTask)]

    def __init__(self, config, start_from, up_to):
        '''Initialize a factory.

        :param Config config: The configuration object.
        :param start_from: The start of the range of phases for which tasks
                           will be generated.
        :type start_from: str or None
        :param up_to: The end of the range of phases for which tasks
                      will be generated.
        :type up_to: str or None
        '''
        self.config = config
        if start_from is None:
            phases = self.PHASES
        else:
            phases = dropwhile(lambda elem: elem[0] != start_from,
                               self.PHASES)
        if not phases:
            raise ValueError('cannot find starting action {}'
                             .format(start_from))
        last = None
        for i, phase in enumerate(phases):
            if phase[0] == up_to:
                last = i + 1
                break
        self.phases = phases[:last]
        if not self.phases:
            raise ValueError('nothing to do between {!r} and {!r}'
                             .format(start_from, up_to))

    def make_tasks(self, targets):
        '''Generate a list of tasks.

        This method generates tasks based on a collection of task names
        (`targets`) which will be looked up in the configuration. So, for
        instance, if the factory has been configured to produce tasks in the
        range from ``'configure'`` to ``'build'``, and if `targets` contains
        ``'swallow'`` and ``'coconut'``, this method will search the
        configuration file for sections

            * ``[checkout swallow]``
            * ``[checkout coconut]``
            * ``[build swallow]``
            * ``[build coconut]``

        :param collection targets: A collection of strings.
        '''
        if targets:
            return [cls.from_config(target, self.config)
                    for _, cls in self.phases
                    for target in targets]
        else:
            return [cls.from_config(target, self.config)
                    for phase, cls in self.phases
                    for _, target in self.config.sections_by_family(phase)]


def build_graph(args, config):
    '''Build a dependency graph according to the CLI parameters and the
    configuration.'''

    graph = DepGraph()

    factory = TaskFactory(config, args.start_from, args.command_name)

    tasks = factory.make_tasks(args.targets)
    tasks_by_name = {}
    for task in tasks:
        tasks_by_name[task.name] = task
        graph.add_node(task)

    for task in tasks:
        for dep in task.depends_on:
            graph.add_dependency(task, on=tasks_by_name[dep])

    return graph


def schedule(graph):
    '''Schedule a graph for execution.'''
    scheduler = Scheduler(graph)
    env = scheduler.schedule()
    LOGGER.info(env)
    return env
