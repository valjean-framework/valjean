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

    Marks = enum.Enum('Marks', 'TEMP PERM')

    def __init__(self, dependencies):
        # self.nodes is the list of the graph nodes
        self.nodes = list(
            frozenset(dependencies.keys())
            | frozenset(v for vs in dependencies.values() for v in vs)
            )
        logger.debug('nodes: %s', self.nodes)

        # the self.index dictionary translated from node objects to integer
        # indices
        self.index = {x: i for i, x in enumerate(self.nodes)}
        logger.debug('index: %s', self.index)

        # translate the dependency dictionary elements to ints
        self.edges = {}
        for key, values in dependencies.items():
            new_key = self.index[key]
            new_values = list(map(lambda v: self.index[v], values))
            self.edges[new_key] = frozenset(new_values)
        logger.debug('incomplete graph: %s', self.edges)

        # finally, complete the dependency dictionary so that all values also
        # appear as keys, possibly with empty values
        self.edges = self.complete(self.edges)
        logger.debug('full graph: %s', self.edges)

    def __repr__(self):
        return str(self.edges)

    @staticmethod
    def complete(d):
        complete_d = copy.copy(d)
        for vs in d.values():
            for v in vs:
                if v not in complete_d:
                    complete_d[v] = frozenset()
        return complete_d

    def invert(self):
        inv_dict = {}
        for k, vs in self.edges.items():
            inv_dict.setdefault(k, [])
            for v in vs:
                inv_dict.setdefault(v, []).append(k)

        return DepGraph(inv_dict)

    def topological_sort(self):
        result = []
        marks = {}

        def visit(node):
            mark = marks.get(node, None)
            if mark == self.Marks.TEMP:
                raise DepGraphError('Dependency graph is cyclic!')
            if mark == self.Marks.PERM:
                return
            marks[node] = self.Marks.TEMP
            for target in self.edges.get(node, []):
                visit(target)
            marks[node] = self.Marks.PERM
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


if __name__ == '__main__':
    g = DepGraph({1: [2, 3], 5: [7, 4, 1, 2]})
    l = list(g.topological_sort())
    print(g)
    print(l)
