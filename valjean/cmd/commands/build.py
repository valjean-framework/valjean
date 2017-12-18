'''Module for the ``build`` subcommand.'''


from ..common import Command, build_graph, UniqueAppendAction


class BuildCommand(Command):

    NAME = 'build'

    HELP = 'build code'

    def register(self, parser):
        '''Register options for this command in the parser.'''
        parser.add_argument(
            'targets', metavar='TARGET', nargs='*',
            action=UniqueAppendAction,
            help='targets to build'
            )
        parser.set_defaults(func=self.execute)

    def execute(self, args, config):
        '''Execute the ``build`` command.'''
        return build_graph(args, config)
