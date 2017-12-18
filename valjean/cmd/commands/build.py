'''Module for the ``build`` subcommand.'''


from ..common import Command, build_graph, schedule


class BuildCommand(Command):

    NAME = 'build'

    HELP = 'build code'

    def execute(self, args, config):
        '''Execute the ``build`` command.'''
        graph = build_graph(args, config)
        return schedule(graph)
