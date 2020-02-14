'''Module for the ``env`` subcommand.'''


from pprint import pprint

from ... import LOGGER
from ..common import Command
from ...cosette.env import Env


class EnvCommand(Command):
    '''Command class for the ``env`` subcommand.'''

    NAME = 'env'

    HELP = 'inspect the content of one or more serialized environment files'

    def register(self, parser):
        '''Register options for this command in the parser.'''
        parser.add_argument('names', metavar='NAME', nargs='+',
                            help='The name of the environment file to show.')
        parser.set_defaults(func=self.env)

    def env(self,  # pylint: disable=no-self-use
            args, _collected_tasks, _config):
        '''Execute the ``show-env`` command.'''
        # deserialize the environment
        for name in args.names:
            env = Env.from_file(name, fmt=args.env_format)
            if env is None:
                LOGGER.error('cannot show the environment for task %s', name)
            else:
                pprint(dict(env.items()))
