'''Common utilities for :program:`valjean` commands.'''

from itertools import dropwhile

from ..cosette.code import CheckoutTask, BuildTask
from ..cosette.depgraph import DepGraph
from ..cosette.scheduler import Scheduler
from .. import LOGGER


class Command:

    def register(self, parser):
        '''Register options for this command in the parser.'''
        raise NotImplementedError('Command must be subclassed.')

    def execute(self, args, config):
        '''Execute this command.'''
        raise NotImplementedError('Command must be subclassed.')


class TaskFactory:

    PHASES = [('checkout', CheckoutTask),
              ('build', BuildTask)]

    def __init__(self, config, start_from, up_to):
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
        suffixes = [None] if targets is None else targets
        return [cls.from_config(name, self.config)
                for phase, cls in self.phases
                for suffix in suffixes
                for _, name in self.config.sections_by_prefix(phase, suffix)]


def build_graph(args, config):

    if args.targets:
        targets = set(args.targets)
    else:
        targets = None

    graph = DepGraph()

    factory = TaskFactory(config, args.start_from, args.command_name)

    tasks = factory.make_tasks(targets)
    tasks_by_name = {}
    for task in tasks:
        tasks_by_name[task.name] = task
        graph.add_node(task)

    for task in tasks:
        for dep in task.depends_on:
            graph.add_dependency(task, on=tasks_by_name[dep])

    scheduler = Scheduler(graph)
    env = scheduler.schedule()
    LOGGER.info(env)
    return env
