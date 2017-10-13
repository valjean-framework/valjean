# -*- coding: utf-8 -*-
'''Dependency graphs.

The :class:`DepGraph` class encapsulates a number of useful methods to deal
with interdependent items. It represents the workhorse for the scheduling
algorithms in the :mod:`~.scheduler` module.

A dependency graph is a directed acyclic graph which may be represented as
follows:

.. digraph:: depgraph
   :align: center

   "bacon" -> "spam";
   "sausage" -> "eggs", "spam";

The convention here is that if an edge goes from `A` to `B`, then `A` depends
on `B`.

You can create a :class:`DepGraph` in of two ways. Either you pass a dictionary
representing the dependencies between items to the
:meth:`~DepGraph.from_dependency_dictionary` class method:

.. testsetup:: depgraph

   from valjean.depgraph import DepGraph

.. doctest:: depgraph

   >>> from pprint import pprint
   >>> deps = {'bacon': ['spam'], 'sausage': ['eggs', 'spam']}
   >>> pprint(deps)
   {'bacon': ['spam'], 'sausage': ['eggs', 'spam']}
   >>> g = DepGraph.from_dependency_dictionary(deps)

or you create an empty graph and add nodes and dependencies by hand:

.. doctest:: depgraph

   >>> h = DepGraph().add_dependency('bacon', on='spam') \\
   ...               .add_dependency('sausage', on='eggs') \\
   ...               .add_dependency('sausage', on='spam')
   >>> print(g == h)
   True

In these examples, `sausage` depends on `eggs` and `spam`, and `bacon` depends
on `spam`; `spam` and `eggs` have no dependencies. Note that the dependency
dictionary may be seen as a sparse representation of the graph adjacency
matrix.

You can recover the dependency dictionary by passing the graph to
:func:`dict()`:

.. doctest:: depgraph

   >>> pprint(dict(g))  # doctest: +SKIP
   {'bacon': {'spam'}, 'eggs': set(), 'sausage': {'eggs', 'spam'}, \
'spam': set()}

and you can also iterate over graphs:

.. doctest:: depgraph

   >>> for k, vs in sorted(g):
   ...     for v in sorted(vs):
   ...         print("You can't have {} without {}!".format(k, v))
   You can't have bacon without spam!
   You can't have sausage without eggs!
   You can't have sausage without spam!

Some things you should be aware of when using :class:`DepGraph`:

* The type of the items in the graph is irrelevant, but since they need to be
  stored in a dictionary, they must be *hashable*;
* You need to use a single-element list if you want to express a single
  dependency, as in the case of `bacon`. So this is wrong:

    >>> bad_deps = {0: 1, 7: [0, 42]}  # error, should be [1]
    >>> bad = DepGraph.from_dependency_dictionary(deps)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
        [...]
    TypeError: 'int' object is not iterable

If you print the dictionary, you will notice that `spam` and `eggs` have been
added as nodes with no dependencies:

.. doctest:: depgraph

   >>> print(g)
   [('bacon', ['spam']), ('eggs', []), ('sausage', ['eggs', 'spam']), \
('spam', [])]

What if a node has no dependencies and no other node depends on it? Just add it
to the dictionary with the empty list as a value:

.. doctest:: depgraph

   >>> free = DepGraph.from_dependency_dictionary({'kazantzakis': []})

You can also add it after creating the graph:

.. doctest:: depgraph

   >>> also_free = DepGraph().add_node('kazantzakis')
   >>> print(free == also_free)
   True

You can inspect the nodes of the graph:

.. doctest:: depgraph

   >>> print(sorted(g.nodes()))
   ['bacon', 'eggs', 'sausage', 'spam']

or ask for the dependencies of a node:

.. doctest:: depgraph

   >>> print(sorted(list(g.dependencies('sausage'))))
   ['eggs', 'spam']

You can also do a topological sort of the graph. The result is a list of the
graph nodes, with the property that each node is guaranteed to appear after all
the nodes it depends on. Note that in general there are several possible
topological sorts for a given graph.

.. doctest:: depgraph

   >>> print(g.topological_sort())  # doctest: +SKIP
   ['eggs', 'spam', 'bacon', 'sausage']
'''

import logging

logging.basicConfig(format='%(levelname)s (%(name)s): %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class DepGraphError(Exception):
    pass


class DepGraph:
    '''A dependency graph.

    The preferred way to instantiate this class is to use the
    :meth:`from_dependency_dictionary` class method. Alternatively, you may use
    the direct constructor; in this case, the graph `edges` are represented as
    a dictionary between integers, with the convention that each node is
    represented by its index in the `nodes` list. So `nodes` can be seen as a
    mapping from integers to nodes. The inverse mapping is called `index` and
    may be passed to the constructor if it is available to the caller as a
    dictionary; if not, it will be constructed internally.

    :param list nodes: An iterable over the nodes of the graph, or `None` for
        an empty graph.
    :param mapping edges: A mapping between integers representing the nodes, or
        `None` for an empty graph.
    :param mapping index: The inverse mapping to `nodes`, or `None` if it is
        not available. The constructor checks that the following invariant
        holds::

            all(i == index[node] for i, node in enumerate(nodes))
    '''

    import enum
    _Marks = enum.Enum('Marks', 'TEMP PERM')

    @classmethod
    def from_dependency_dictionary(cls, dependencies):
        '''Generate a :class:`DepGraph` from a dependency dictionary.'''

        # the list of the graph nodes
        nodes = list(
            set(dependencies.keys())
            | set(v for vs in dependencies.values() for v in vs)
            )

        # the index dictionary translates from node objects to integer indices
        index = {x: i for i, x in enumerate(nodes)}

        # translate the dependency dictionary elements to indices
        edges = {}
        for key, values in dependencies.items():
            new_key = index[key]
            new_values = set(map(lambda v: index[v], values))
            edges[new_key] = new_values

        return cls(nodes, edges, index)

    @staticmethod
    def _complete(d):
        '''Add singleton nodes to the dictionary.'''

        import copy
        complete_d = copy.copy(d)
        for vs in d.values():
            for v in vs:
                if v not in complete_d:
                    complete_d[v] = set()
        complete_d = {k: set(v) for k, v in complete_d.items()}
        return complete_d

    def __init__(self, nodes=None, edges=None, index=None):

        if nodes is None or edges is None:
            self._nodes = {}
            self._index = {}
            self._edges = {}
            return

        # self._nodes is the list of the graph nodes
        self._nodes = {i: node for i, node in enumerate(nodes)}
        logger.debug('nodes: %s', self._nodes)

        # the self._index dictionary translates from node objects to integer
        # indices
        if index is None:
            self._index = {x: i for i, x in self._nodes.items()}
        else:
            # do a sanity check on index
            check = all(i == index[node] for i, node in self._nodes.items())
            if not check:
                raise DepGraphError('index and nodes are inconsistent\n'
                                    'index = {index}\nnodes = {nodes}'
                                    .format(index=index, nodes=self._nodes))
            self._index = index
        logger.debug('index: %s', self._index)

        # finally, complete the edges dictionary so that all values also appear
        # as keys, possibly with empty values
        logger.debug('incomplete graph edges: %s', edges)
        self._edges = DepGraph._complete(edges)
        logger.debug('full graph edges: %s', self._edges)

    def __str__(self):
        assoc_list = sorted([(str(self._nodes[k]),
                             sorted(map(lambda v: str(self._nodes[v]), vs)))
                             for k, vs in self._edges.items()])
        return str(assoc_list)

    def __repr__(self):
        return 'DepGraph(nodes={nodes}, edges={edges}, index={index})'\
               .format(nodes=self._nodes, edges=self._edges, index=self._index)

    def __eq__(self, other):
        return self.isomorphic_to(other)

    def __iter__(self):
        for i, node in self._nodes.items():
            values = map(lambda j: self._nodes[j], self._edges[i])
            yield (node, set(values))

    def isomorphic_to(self, other):
        return dict(self) == dict(other)

    def add_node(self, node):
        '''Add a new node to the graph.

        :param node: The new node.
        '''

        if node in self._index:
            logging.info('Node {} already belongs to the graph'.format(node))
            return

        new_index = len(self._nodes)
        self._nodes[new_index] = node
        self._index[node] = new_index
        self._edges[new_index] = set()
        return self

    def add_dependency(self, node, on):
        '''Add a new dependency to the graph.

        :param node: The node for which the dependency is specified.
        :param on: The node `node` depends on.
        '''

        self.add_node(node)
        self.add_node(on)
        i_node = self._index[node]
        i_on = self._index[on]
        self._edges[i_node].add(i_on)
        return self

    def invert(self):
        '''Invert the graph.

        :returns: A new graph having the same nodes but all edges inverted.
        '''

        inv_edges = {}
        for k, vs in self._edges.items():
            inv_edges.setdefault(k, [])
            for v in vs:
                inv_edges.setdefault(v, []).append(k)

        return DepGraph(self._nodes.values(), inv_edges, self._index)

    def topological_sort(self):
        '''Perform a topological sort of the graph.

        :returns: The nodes of the graph, as a list, with the invariant that
                  each node appears in the list after all the nodes it depends
                  on.
        :raises DepGraphError: if the graph is cyclic.
                  '''

        result = []
        marks = {}

        def visit(node):
            mark = marks.get(node, None)
            if mark == self._Marks.TEMP:
                raise DepGraphError('Dependency graph is cyclic!')
            if mark == self._Marks.PERM:
                return
            marks[node] = self._Marks.TEMP
            index = self._index[node]
            for target in self._edges.get(index, []):
                visit(self._nodes[target])
            marks[node] = self._Marks.PERM
            result.append(node)

        for node in self._nodes.values():
            if node in marks:
                continue
            visit(node)

        return result

    def nodes(self):
        return self._nodes.values()

    def dependencies(self, node):
        '''Query the graph about the dependencies of `node`.

        :returns: An iterable over the dependencies of `node`.'''

        indices = self._edges.get(self._index[node], [])
        result = map(lambda i: self._nodes[i], indices)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('dependencies: %s -> %s', node, list(result))
        return result
