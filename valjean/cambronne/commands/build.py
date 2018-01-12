'''Module for the ``build`` subcommand.'''


from ..common import Command, build_graph, schedule


class BuildCommand(Command):
    '''Command class for the ``build`` subcommand.'''

    NAME = 'build'

    HELP = 'build code'

    def execute(self, args, config):
        '''Execute the ``build`` command.'''
        if args.targets:
            family_targets = [('build', target) for target in args.targets]
        else:
            family_targets = [('build', None)]
        graph = build_graph(family_targets, config)
        return schedule(graph)
