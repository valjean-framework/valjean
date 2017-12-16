'''Module for the ``build`` subcommand.'''


from .common import Action, TaskFactory
from ..cosette.code import BuildTask, CheckoutTask
from ..cosette.depgraph import DepGraph
from ..cosette.scheduler import Scheduler
from .. import LOGGER


class BuildAction(Action):

    def __init__(self):
        super().__init__()
        self.co_factory = TaskFactory('checkout', CheckoutTask)
        self.factory = TaskFactory('build', BuildTask)

    def register(self, parser):
        '''Register options for this command in the parser.'''
        parser.add_argument(
            'target', metavar='TARGET', nargs='*',
            help='targets to build'
            )
        parser.set_defaults(func=self.process)


    def process(self, args, config):
        '''Process the arguments to the ``config`` command.

        :param args: The arguments parsed by :mod:`argparse`.
        :param Config config: The configuration object.
        '''

        graph = DepGraph()
        for target in set(args.target):
            co_task = self.co_factory.make_task(config, target)
            task = self.factory.make_task(config, target)
            graph.add_dependency(task, on=co_task)
        scheduler = Scheduler(graph)
        env = scheduler.schedule()
        LOGGER.info(env)
