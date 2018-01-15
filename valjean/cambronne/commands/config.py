'''Module for the ``config`` subcommand.'''


from ..common import Command


class ConfigCommand(Command):
    '''Command class for the ``config`` subcommand.'''

    NAME = 'config'

    HELP = 'inspect the configuration'

    def register(self, parser):
        '''Register options for this command in the parser.'''
        parser.add_argument(
            'section', metavar='SECTION',
            help='name of the configuration section'
            )
        parser.add_argument(
            'option', metavar='OPTION', help='name of the option', nargs='?'
            )
        parser.add_argument(
            '--raw', action='store_true',
            help='do not interpolate option values'
            )
        parser.set_defaults(func=self.execute)

    @staticmethod
    def execute(args, config):
        '''Execute the ``config`` command.'''
        raw = args.raw
        if args.option is None:
            for opt, val in config.items(args.section, raw=raw):
                print('{} = {}'.format(opt, val))
        else:
            value = config.get(args.section, args.option, raw=raw)
            print(value)
