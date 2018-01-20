'''Module for the ``build`` subcommand.'''


from ..common import Command


class BuildCommand(Command):
    '''Command class for the ``build`` subcommand.'''

    NAME = 'build'

    FAMILY = 'build'

    HELP = 'build code'
