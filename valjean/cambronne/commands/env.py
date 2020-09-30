'''Module for the ``env`` subcommand.'''


from pprint import pprint

from ... import LOGGER
from ..common import Command
from ...cosette.env import Env


class EnvCommand(Command):
    '''Command class for the ``env`` subcommand.'''

    NAME = 'env'

    HELP = 'Inspect the content of one or more serialized environment files.'

    DESC = HELP

    def register(self, parser):
        '''Register options for this command in the parser.'''
        parser.add_argument('--env-format', action='store',
                            choices=('pickle',), default='pickle',
                            help='environment persistency format')
        parser.add_argument('env_files', metavar='ENV_FILE', nargs='+',
                            help='The environment file to show.')
        parser.set_defaults(func=self.env)

    @staticmethod
    def env(args, _config):
        '''Execute the ``show-env`` command.'''
        # deserialize the environment
        for env_file in args.env_files:
            env = Env.from_file(env_file, fmt=args.env_format)
            if env is None:
                LOGGER.error('cannot show the environment for task %s',
                             env_file)
            else:
                pprint(dict(env.items()))
