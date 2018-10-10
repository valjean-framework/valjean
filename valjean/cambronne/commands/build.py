'''Module for the ``build`` subcommand.'''


from ..common import Command
from ...cosette.code import BuildTask


class BuildCommand(Command):
    '''Command class for the ``build`` subcommand.'''

    NAME = 'build'

    PRIORITY = BuildTask.PRIORITY

    HELP = 'build code'
