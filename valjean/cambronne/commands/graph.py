'''Module for the ``graph`` subcommand.'''

import os

from ..common import Command, build_graph
from ... import LOGGER


class GraphCommand(Command):
    '''Command class for the ``build`` subcommand.'''

    NAME = 'graph'

    HELP = 'output the dependency graph in graphviz format'

    def register(self, parser):
        '''Register options for this command in the parser.'''
        parser.add_argument(
            '-o', '--output',
            action='store',
            help='path to the output file'
            )
        parser.set_defaults(func=self.execute)

    def execute(self, args, config):
        '''Execute the ``graph`` command.'''
        family_targets = [(None, None)]
        graph = build_graph(family_targets, config)
        graph_str = graph.to_graphviz()
        if args.output:
            _, ext = os.path.splitext(args.output)
            if ext:
                try:
                    import pydot
                except ImportError:
                    LOGGER.critical('you need to install pydot to use the '
                                    '--display option.')
                    raise
                graph_pydot = pydot.graph_from_dot_data(graph_str)[0]
                low_ext = ext[1:].lower()
                try:
                    writer = getattr(graph_pydot, 'write_' + low_ext)
                except AttributeError:
                    raise ValueError('graph output format {} is not supported'
                                     .format(ext))
                writer(args.output)
            else:
                with open(args.output, 'w') as fout:
                    fout.write(graph_str)
        else:
            print(graph_str)
