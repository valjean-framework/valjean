'''Module for the ``eval`` subcommand.'''


from ..common import Command
from ...gavroche.eval_test_task import EvalTestTask


class EvalCommand(Command):
    '''Command class for the ``eval`` subcommand.'''

    NAME = 'eval'

    ALIASES = ('evaluate', 'test')

    PRIORITY = EvalTestTask.PRIORITY

    HELP = 'evaluate the tests'
