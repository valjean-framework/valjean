'''Module for the ``checkout`` subcommand.'''


from ..common import Command
from ...cosette.code import CheckoutTask


class CheckoutCommand(Command):
    '''Command class for the ``checkout`` subcommand.'''

    NAME = 'checkout'

    PRIORITY = CheckoutTask.PRIORITY

    HELP = 'checkout code'

    ALIASES = ('co',)
