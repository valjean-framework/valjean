'''Module for the ``checkout`` subcommand.'''


from ..common import Command, build_graph, schedule


class CheckoutCommand(Command):
    '''Command class for the ``checkout`` subcommand.'''

    NAME = 'checkout'

    HELP = 'checkout code'

    ALIASES = ('co',)

    def execute(self, args, config):
        '''Execute the ``checkout`` command.'''
        if args.targets:
            family_targets = [('checkout', target) for target in args.targets]
        else:
            family_targets = [('checkout', None)]
        graph = build_graph(family_targets, config)
        return schedule(graph)
