'''Module for the ``checkout`` subcommand.'''


from ..common import Command, build_graph, schedule


class CheckoutCommand(Command):

    NAME = 'checkout'

    HELP = 'checkout code'

    ALIASES = ('co',)

    def execute(self, args, config):
        '''Execute the ``checkout`` command.'''
        graph = build_graph(args, config)
        return schedule(graph)
