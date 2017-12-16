'''Module for the ``build`` subcommand.'''


from .common import Command, build_graph


class BuildCommand(Command):

    def register(self, parser):
        '''Register options for this command in the parser.'''
        parser.add_argument(
            'targets', metavar='TARGET', nargs='*',
            help='targets to build'
            )
        parser.set_defaults(func=self.execute)

    def execute(self, args, config):
        '''Execute the ``build`` command.'''
        return build_graph(args, config)
