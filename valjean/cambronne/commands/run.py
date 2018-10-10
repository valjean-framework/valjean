'''Module for the ``run`` subcommand.'''


from ..common import Command
from ...cosette.run import RunTask


class RunCommand(Command):
    '''Command class for the ``run`` subcommand.'''

    NAME = 'run'

    PRIORITY = RunTask.PRIORITY

    HELP = 'run a task'
