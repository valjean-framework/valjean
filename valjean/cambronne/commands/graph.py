# Copyright French Alternative Energies and Atomic Energy Commission
# Contributors: valjean developers
# valjean-support@cea.fr
#
# This software is a computer program whose purpose is to analyze and
# post-process numerical simulation results.
#
# This software is governed by the CeCILL license under French law and abiding
# by the rules of distribution of free software. You can use, modify and/ or
# redistribute the software under the terms of the CeCILL license as circulated
# by CEA, CNRS and INRIA at the following URL: http://www.cecill.info.
#
# As a counterpart to the access to the source code and rights to copy, modify
# and redistribute granted by the license, users are provided only with a
# limited warranty and the software's author, the holder of the economic
# rights, and the successive licensors have only limited liability.
#
# In this respect, the user's attention is drawn to the risks associated with
# loading, using, modifying and/or developing or reproducing the software by
# the user in light of its specific status of free software, that may mean that
# it is complicated to manipulate, and that also therefore means that it is
# reserved for developers and experienced professionals having in-depth
# computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling
# the security of their systems and/or data to be ensured and, more generally,
# to use and operate it in the same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

'''Module for the ``graph`` subcommand.'''

import os
import logging

from ..common import JobCommand, build_graphs


LOGGER = logging.getLogger(__name__)


class GraphCommand(JobCommand):
    '''Command class for the ``build`` subcommand.'''

    NAME = 'graph'

    HELP = 'Output the dependency graph in any format supported by Graphviz.'

    DESC = HELP

    def register(self, parser):
        '''Register options for this command in the parser.'''
        super().register(parser)
        parser.add_argument('--dependencies', action='store',
                            help='select which dependencies to draw (default: '
                            'both)', choices=['hard', 'soft', 'both'],
                            default='both')
        parser.add_argument('-o', '--output',
                            action='store', help='path to the output file')
        parser.set_defaults(func=self.execute)

    @staticmethod
    def execute(args, _config):
        '''Execute the ``graph`` command.'''
        hard_graph, soft_graph = build_graphs(args)
        if args.dependencies == 'hard':
            graph_str = hard_graph.to_graphviz()
        elif args.dependencies == 'soft':
            graph_str = soft_graph.to_graphviz()
        elif args.dependencies == 'both':
            hard_graph_str = hard_graph.to_graphviz()
            soft_graph_str = soft_graph.to_graphviz()
            graph_str = GraphCommand.merge_graph_str(hard_graph_str,
                                                     soft_graph_str)

        if args.output:
            _, ext = os.path.splitext(args.output)
            if ext:
                try:
                    from pydot import graph_from_dot_data
                except ImportError:
                    LOGGER.error('you need to install pydot to use the '
                                 '--output option.')
                    raise
                # pylint: disable-next=possibly-used-before-assignment
                graph_pydot = graph_from_dot_data(graph_str)[0]
                try:
                    writer = getattr(graph_pydot, 'write_' + ext[1:].lower())
                except AttributeError as aerr:
                    raise ValueError(f'graph output format {ext} is not '
                                     'supported') from aerr
                writer(args.output)
            else:
                with open(args.output, 'w', encoding='utf-8') as fout:
                    fout.write(graph_str)
        else:
            print(graph_str)

    @staticmethod
    def merge_graph_str(solid_graph, dashed_graph):
        r'''Merge two strings representing graphviz graphs into one graph. The
        graphs are merged in such a way that the edges of `solid_graph` and
        `dashed_graph` are respectively represented as solid and dashed.

        .. doctest:: merge_graph_str
            :hide:

            >>> solid_graph = ('digraph {\n  node1 -> node2;\n'
            ... '  node2 -> node3;\n}')
            >>> dashed_graph = 'digraph {\n  node1 -> node3;\n}'

        For example:

        >>> print(solid_graph)
        digraph {
          node1 -> node2;
          node2 -> node3;
        }
        >>> print(dashed_graph)
        digraph {
          node1 -> node3;
        }
        >>> print(GraphCommand.merge_graph_str(solid_graph, dashed_graph))
        digraph {
          subgraph G1 {
          node1 -> node2;
          node2 -> node3;
          }
          subgraph G2 {
          edge [style=dashed];
          node1 -> node3;
          }
        }

        :param str solid_graph: a graph, as produced by
            :meth:`~.DepGraph.to_graphviz`.
        :param str dashed_graph: another graph, as produced by
            :meth:`~.DepGraph.to_graphviz`.
        :returns: the merged graph.
        :rtype: str
        '''
        from itertools import chain
        lines_solid = solid_graph.split('\n')
        lines_dashed = dashed_graph.split('\n')
        lines = list(chain(('digraph {\n  subgraph G1 {',),
                           lines_solid[1:-1],
                           ('  }\n  subgraph G2 {\n  edge [style=dashed];',),
                           lines_dashed[1:-1],
                           ('  }\n}',)))
        return '\n'.join(lines)
