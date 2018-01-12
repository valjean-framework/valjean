'''Module for the ``run`` subcommand.'''


from ..common import Command, build_graph, schedule


class RunCommand(Command):
    '''Command class for the ``run`` subcommand.'''

    NAME = 'run'

    HELP = 'run a task'

    def execute(self, args, config):
        '''Execute the ``run`` command.'''
        if args.targets:
            family_targets = [(None, target) for target in args.targets]
        else:
            family_targets = [(None, None)]
        graph = build_graph(family_targets, config)
        return schedule(graph)
