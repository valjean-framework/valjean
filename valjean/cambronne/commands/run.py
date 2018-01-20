'''Module for the ``run`` subcommand.'''


from ..common import Command


class RunCommand(Command):
    '''Command class for the ``run`` subcommand.'''

    NAME = 'run'

    FAMILY = None

    HELP = 'run a task'
