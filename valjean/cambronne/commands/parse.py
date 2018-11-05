'''Module for the ``parse`` subcommand.'''


from ..common import Command
from ...eponine.parse_t4_task import ParseT4Task


class ParseCommand(Command):
    '''Command class for the ``parse`` subcommand.'''

    NAME = 'parse'

    PRIORITY = ParseT4Task.PRIORITY

    HELP = 'parse the result of a TRIPOLI-4 run'
