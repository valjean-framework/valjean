'''Module for the ``run`` subcommand.'''


from ..common import Command, build_graph, schedule


class RunCommand(Command):
    '''Command class for the ``run`` subcommand.'''

    NAME = 'run'

    HELP = 'run a task'

    def execute(self, args, config):
        '''Execute the ``run`` command.'''
        graph = build_graph(args, config)
        return schedule(graph)
