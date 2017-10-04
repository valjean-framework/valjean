# -*- coding: utf-8 -*-
'''
'''

import enum
import copy
import logging

logging.basicConfig(format='%(levelname)s (%(name)s): %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class DepGraphError(Exception):
    pass


class DepGraph:
    '''Test docstring'''

    _Marks = enum.Enum('Marks', 'TEMP PERM')

    @classmethod
    def from_dependency_dictionary(cls, dependencies):
        # the list of the graph nodes
        nodes = list(
            frozenset(dependencies.keys())
            | frozenset(v for vs in dependencies.values() for v in vs)
            )

        # the index dictionary translates from node objects to integer indices
        index = {x: i for i, x in enumerate(nodes)}

        # translate the dependency dictionary elements to indices
        edges = {}
        for key, values in dependencies.items():
            new_key = index[key]
            new_values = list(map(lambda v: index[v], values))
            edges[new_key] = frozenset(new_values)

        return cls(nodes, edges, index)

    @staticmethod
    def _complete(d):
        '''Add singleton nodes to the dictionary.'''

        complete_d = copy.copy(d)
        for vs in d.values():
            for v in vs:
                if v not in complete_d:
                    complete_d[v] = frozenset()
        complete_d = {k: frozenset(v) for k, v in complete_d.items()}
        return complete_d

    def __init__(self, nodes, edges, index=None):
        # self.nodes is the list of the graph nodes
        self.nodes = list(nodes)
        logger.debug('nodes: %s', self.nodes)

        # the self.index dictionary translates from node objects to integer
        # indices
        if index is None:
            self.index = {x: i for i, x in enumerate(self.nodes)}
        else:
            # do a sanity check on index
            check = all(i == index[node] for i, node in enumerate(self.nodes))
            if not check:
                raise DepGraphError('index and nodes are inconsistent\n'
                                    'index = {index}\nnodes = {nodes}'
                                    .format(index=index, nodes=self.nodes))
            self.index = index
        logger.debug('index: %s', self.index)

        # finally, complete the edges dictionary so that all values also appear
        # as keys, possibly with empty values
        logger.debug('incomplete graph edges: %s', edges)
        self.edges = DepGraph._complete(edges)
        logger.debug('full graph edges: %s', self.edges)

    def __str__(self):

        assoc_list = [(self.nodes[k], map(lambda v: self.nodes[v], vs))
                      for k, vs in self.edges.items()]
        results = []
        for k, vs in sorted(assoc_list):
            result = str(k) + ': ['
            vs_str = [str(v) for v in sorted(vs)]
            result += ', '.join(vs_str) + ']'
            results.append(result)
        result = '{' + ', '.join(results) + '}'
        return result

    def invert(self):
        inv_edges = {}
        for k, vs in self.edges.items():
            inv_edges.setdefault(k, [])
            for v in vs:
                inv_edges.setdefault(v, []).append(k)

        return DepGraph(self.nodes, inv_edges, self.index)

    def topological_sort(self):
        result = []
        marks = {}

        def visit(node):
            mark = marks.get(node, None)
            if mark == self._Marks.TEMP:
                raise DepGraphError('Dependency graph is cyclic!')
            if mark == self._Marks.PERM:
                return
            marks[node] = self._Marks.TEMP
            index = self.index[node]
            for target in self.edges.get(index, []):
                visit(self.nodes[target])
            marks[node] = self._Marks.PERM
            result.append(node)

        for node in self.nodes:
            if node in marks:
                continue
            visit(node)

        return result

    def isomorphic_to(self, other):
        return self.edges == other.edges

    def dependencies(self, task):
        '''Return an iterable over the dependencies of the given task'''

        indices = self.edges.get(self.index[task], [])
        result = map(lambda i: self.nodes[i], indices)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('dependencies: %s -> %s', task, list(result))
        return result
