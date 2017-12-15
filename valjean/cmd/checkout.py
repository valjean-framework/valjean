'''Module for the ``checkout`` subcommand.'''


from .common import Action, TaskFactory
from ..cosette.code import CheckoutTask
from ..cosette.depgraph import DepGraph
from ..cosette.scheduler import Scheduler
from .. import LOGGER


class CheckoutAction(Action):

    def __init__(self):
        super().__init__()
        self.factory = TaskFactory('checkout', CheckoutTask)

    def register(self, parser):
        '''Register options for this command in the parser.'''
        parser.add_argument(
            'target', metavar='TARGET', nargs='*',
            help='targets to checkout'
            )
        parser.set_defaults(func=self.process)


    def process(self, args, config):
        '''Process the arguments to the ``config`` command.

        :param args: The arguments parsed by :mod:`argparse`.
        :param Config config: The configuration object.
        '''
        tasks = self.factory.make_tasks(config, set(args.target))

        graph = DepGraph()
        for task in tasks:
            graph.add_node(task)
        scheduler = Scheduler(graph)
        env = scheduler.schedule()
        LOGGER.info(env)
