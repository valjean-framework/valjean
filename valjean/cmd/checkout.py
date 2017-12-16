'''Module for the ``checkout`` subcommand.'''


from .common import Command, build_graph, UniqueAppendAction


class CheckoutCommand(Command):

    def register(self, parser):
        '''Register options for this command in the parser.'''
        parser.add_argument(
            'targets', metavar='TARGET', nargs='*',
            action=UniqueAppendAction,
            help='targets to checkout'
            )
        parser.set_defaults(func=self.execute)

    def execute(self, args, config):
        '''Execute the ``checkout`` command.'''
        return build_graph(args, config)
