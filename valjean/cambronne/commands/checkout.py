'''Module for the ``checkout`` subcommand.'''


from ..common import Command


class CheckoutCommand(Command):
    '''Command class for the ``checkout`` subcommand.'''

    NAME = 'checkout'

    FAMILY = 'checkout'

    HELP = 'checkout code'

    ALIASES = ('co',)
