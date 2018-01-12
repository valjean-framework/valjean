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
    PHASES = {'checkout': CheckoutTask,
              'build': BuildTask,
              'run': RunTask}

    def __init__(self, config):
        '''Initialize a factory.

        :param Config config: The configuration object.
        '''
        self.config = config

    # def make_tasks(self, targets):
    #     '''Generate a list of tasks.

    #     This method generates tasks based on a collection of task names
    #     (`targets`) which will be looked up in the configuration. So, for
    #     instance, if the factory has been configured to produce tasks in the
    #     range from ``'configure'`` to ``'build'``, and if `targets` contains
    #     ``'swallow'`` and ``'coconut'``, this method will search the
    #     configuration file for sections

    #         * ``[checkout swallow]``
    #         * ``[checkout coconut]``
    #         * ``[build swallow]``
    #         * ``[build coconut]``

    #     :param collection targets: A collection of strings.
    #     '''
    #     if targets:
    #         return [cls.from_config(target, self.config)
    #                 for _, cls in self.phases
    #                 for target in targets]
    #     else:
    #         return [cls.from_config(target, self.config)
    #                 for phase, cls in self.phases
    #                 for _, target in self.config.sections_by_family(phase)]

    def make_task(self, command, name):
        LOGGER.debug('making task for command %s, name %s', command, name)
        cls = self.PHASES.get(command, None)
        LOGGER.debug('task class is %s', cls)
        if cls is None:
            return None
        task = cls.from_config(name, self.config)
        return task

    def make_tasks(self, family_targets):
        tasks_by_name = {}
        for family, target in family_targets:
            LOGGER.debug('making tasks for family/targets %s', family_targets)
            task_name = '{}/{}'.format(family, target)
            if task_name in tasks_by_name:
                continue
            task = self.make_task(family, target)
            if task is None:
                continue
            try:
                assert task_name == task.name
            except AssertionError:
                LOGGER.fatal('%s != %s', task_name, task.name)
                raise
            tasks_by_name[task_name] = task
            for dep in task.depends_on:
                dep_family, dep_name = self.config.split_section(dep)
                dep_tasks = self.make_tasks([(dep_family, dep_name)])
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


def schedule(graph):
    '''Schedule a graph for execution.'''
    scheduler = Scheduler(graph)
    env = scheduler.schedule()
    LOGGER.info(env)
    return env
