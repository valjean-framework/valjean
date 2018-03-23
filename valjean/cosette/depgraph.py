# -*- coding: utf-8 -*-
'''The :class:`DepGraph` class encapsulates a number of useful methods to deal
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


Building
--------

You can create a :class:`DepGraph` in of two ways. Either you pass a dictionary
representing the dependencies between items to the
:meth:`~DepGraph.from_dependency_dictionary()` class method:

.. testsetup:: depgraph

   from valjean.cosette.depgraph import DepGraph

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
   >>> g == h
   True

In these examples, `sausage` depends on `eggs` and `spam`, and `bacon` depends
on `spam`; `spam` and `eggs` have no dependencies. Note that the dependency
dictionary may be seen as a sparse representation of the graph adjacency
matrix.

You can recover the dependency dictionary by passing the graph to
:class:`dict() <dict>`:

.. doctest:: depgraph

   >>> pprint(dict(g))  # doctest: +SKIP
   {'bacon': {'spam'}, 'eggs': set(), 'sausage': {'eggs', 'spam'}, \
'spam': set()}

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
   >>> free == also_free
   True


Querying
--------

You can inspect the nodes of the graph:

.. doctest:: depgraph

   >>> sorted(g.nodes())
   ['bacon', 'eggs', 'sausage', 'spam']

or ask for the dependencies of a node:

.. doctest:: depgraph

   >>> sorted(g.dependencies('sausage'))
   ['eggs', 'spam']
   >>> sorted(g['sausage'])  # equivalent, shorter syntax
   ['eggs', 'spam']

or ask for the nodes that depend on another node (careful though, this
operation has `O(N)` time complexity, `N` being the number of nodes in the
graph):

.. doctest:: depgraph

   >>> sorted(g.dependees('spam'))
   ['bacon', 'sausage']

You can also iterate over graphs:

.. doctest:: depgraph

   >>> for k, vs in sorted(g):
   ...     for v in sorted(vs):
   ...         print("You can't have {} without {}!".format(k, v))
   You can't have bacon without spam!
   You can't have sausage without eggs!
   You can't have sausage without spam!

Finally, you can check if a graph is a subgraph of another one:

.. doctest:: depgraph

   >>> sub_g = DepGraph().add_dependency('bacon', on='spam') \\
   ...                   .add_dependency('sausage', on='eggs')
   >>> sub_g <= g
   True


Merging, sorting and other operations
-------------------------------------

Given two graphs, possibly sharing some nodes and edges, you can construct the
*union* `g12` as follows:

.. doctest:: depgraph

   >>> g1 = sub_g
   >>> g2 = DepGraph().add_dependency('sausage', on='spam')
   >>> g12 = g1 + g2
   >>> g12 == g
   True
   >>> _ = g2.merge(g1)  # in-place merge
   >>> g2 == g
   True
   >>> g2 += g1          # equivalent syntax
   >>> g2 == g
   True

It is also possible to compute the transitive reduction of the graph. Let `g`
be an acyclic graph. The transitive reduction `tr(g)` is the minimal (in the
number of edges), provably unique subgraph of `g` over the same vertices with
the following property: for each pair of nodes `A` and `B`, `A` is reachable
from `B` within `g` iff it is reachable within `tr(g)`.

.. doctest:: depgraph

   >>> g_redundant = DepGraph() \\
   ...     .add_dependency('eggs', on='bacon') \\
   ...     .add_dependency('bacon', on='spam') \\
   ...     .add_dependency('eggs', on='spam')  # this edge is redundant
   >>> g_tr = g_redundant.copy()
   >>> print(g_tr.transitive_reduction())
   [('bacon', ['spam']), ('eggs', ['bacon']), ('spam', [])]
   >>> 'spam' in g_tr.dependencies('eggs')
   False

You can also do a topological sort of the graph. The result is a list of the
graph nodes, with the property that each node is guaranteed to appear after all
the nodes it depends on. Note that in general there are several possible
topological sorts for a given graph.

.. doctest:: depgraph

   >>> g.topological_sort()  # doctest: +SKIP
   ['eggs', 'spam', 'bacon', 'sausage']


Grafting sub-graph nodes into the graph itself
----------------------------------------------

A nice feature of :class:`DepGraph` is that you can have graph nodes that are
themselves instances of :class:`DepGraph`! Consider the following graph:

.. digraph:: depgraph
   :align: center

   compound=true;
   "Spanish Inquisition" -> "surprise" [lhead=cluster1];
   subgraph cluster1 {
     label="chief weapons"
     "surprise" -> "fear";
     "surprise" -> "efficiency";
     "fear" -> "devotion";
     "efficiency" -> "devotion";
   }
   "devotion" -> "nice red uniforms" [ltail=cluster1];

Here is the code that generates it:

.. doctest:: depgraph

   >>> spanish_inq = 'Spanish Inquisition'
   >>> surprise, fear, efficiency = 'surprise', 'fear', 'efficiency'
   >>> devotion, uniforms = 'devotion', 'nice red uniforms'
   >>> chief_weapons = DepGraph.from_dependency_dictionary({
   ...    surprise: [fear, efficiency],
   ...    fear: [devotion],
   ...    efficiency: [devotion]
   ...    })
   >>> spanish = DepGraph() \\
   ...     .add_dependency(spanish_inq, on=chief_weapons) \\
   ...     .add_dependency(chief_weapons, on=uniforms)

Here `chief_weapons` is a :class:`DepGraph` itself, but it is also a node of
`spanish`. You can graft `chief_weapons` inside `spanish` like so:

.. doctest:: depgraph

   >>> spanish.graft(chief_weapons)
   DepGraph(...)

This yields the following graph

.. digraph:: depgraph
   :align: center

   compound=true;
   "Spanish Inquisition" -> "surprise";
   "surprise" -> "fear";
   "surprise" -> "efficiency";
   "fear" -> "devotion";
   "efficiency" -> "devotion";
   "devotion" -> "nice red uniforms";

as you can verify yourself:

.. doctest:: depgraph

   >>> full_graph = DepGraph.from_dependency_dictionary({
   ...    spanish_inq: [surprise],
   ...    surprise: [fear, efficiency],
   ...    fear: [devotion],
   ...    efficiency: [devotion],
   ...    devotion: [uniforms]
   ...    })
   >>> full_graph == spanish
   True

The nice thing about this feature is that it makes it easier (more modular) to
build complex graphs. Just build smaller subgraphs and assemble them together
as if they were nodes! The :meth:`.flatten` method will recursively graft all
graph nodes into the main graph.

(Fun fact: the :class:`DepGraph` type is a monad, with :meth:`.flatten`
playing the role of ``join``. If what I just wrote makes no sense to you, don't
worry.)


Caveats
-------

Some things you should be aware of when using :class:`DepGraph`:

* The type of the items in the graph is irrelevant, but if you want to use the
  :meth:`~.DepGraph.from_dependency_dictionary()` constructor they need to be
  stored in a dictionary, and therefore they must be *hashable*;
* You need to use a single-element list if you want to express a single
  dependency, as in the case of `bacon`. So this is wrong:

    >>> bad_deps = {0: 1, 7: [0, 42]}  # error, should be 0: [1]
    >>> bad = DepGraph.from_dependency_dictionary(deps)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
        [...]
    TypeError: 'int' object is not iterable

  Here ``1`` is not iterable, and the test crashed. However, if your graph
  nodes happen to be iterable, the :class:`DepGraph` constructor will not
  crash, but you will not get what you expect.
'''

import logging
from .rlist import RList

LOGGER = logging.getLogger('valjean')


class DepGraphError(Exception):
    '''An exception raised by :class:`DepGraph`.'''
    pass


class DepGraph:
    '''A dependency graph.

    There are two preferred ways to instantiate this class:

    * using the :meth:`from_dependency_dictionary()` class method;
    * constructing an empty graph and repeatedly calling
      :meth:`add_dependency()` and/or :meth:`add_node()`.

    Alternatively, you may also use the full form of the constructor; in this
    case, the graph `edges` are represented as a dictionary between integers,
    with the convention that each node is represented by its index in the
    `nodes` list.  So `nodes` can be seen as a mapping from integers to nodes.
    The inverse mapping is called `index` and may be passed to the constructor
    if it is available to the caller as a dictionary; if not, it will be
    constructed internally.
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

        # translate the dependency dictionary elements to indices
        edges = {}
        for key, values in dependencies.items():
            new_key = nodes.index(key)
            new_values = set(map(nodes.index, values))
            edges[new_key] = new_values

        return cls(nodes, edges)

    @staticmethod
    def _complete(dct):
        '''Add singleton nodes to the dictionary.'''

        import copy
        complete_dct = copy.copy(dct)
        for vals in dct.values():
            for val in vals:
                if val not in complete_dct:
                    complete_dct[val] = set()
        complete_dct = {k: set(v) for k, v in complete_dct.items()}
        return complete_dct

    def __init__(self, nodes=None, edges=None):
        '''Initialize the object from a list of nodes and an edge dictionary.

        :param iterable nodes: An iterable over the nodes of the graph, or
                              `None` for an empty graph.
        :param mapping edges: A mapping between integers representing the
                              nodes, or `None` for an empty graph.
        '''

        if nodes is None or edges is None:
            self._nodes = RList()
            self._edges = {}
            return

        # self._nodes is the list of the graph nodes
        self._nodes = RList(nodes)
        LOGGER.debug('nodes: %s', self._nodes)

        # finally, complete the edges dictionary so that all values also appear
        # as keys, possibly with empty values
        LOGGER.debug('incomplete graph edges: %s', edges)
        self._edges = DepGraph._complete(edges)
        LOGGER.debug('full graph edges: %s', self._edges)

    def __str__(self):
        assoc_list = sorted([(str(self._nodes[k]),
                              sorted(map(lambda v: str(self._nodes[v]), vs)))
                             for k, vs in self._edges.items()])
        return str(assoc_list)

    def __repr__(self):
        return 'DepGraph(nodes={nodes}, edges={edges})'.format(
            nodes=repr(self._nodes), edges=repr(self._edges)
            )

    def __iter__(self):
        for i, node in enumerate(self._nodes):
            values = map(lambda j: self._nodes[j], self._edges[i])
            yield (node, list(values))

    def __add__(self, other):
        '''Merge two graphs, return the result as a new graph.'''
        return self.copy().merge(other)

    __radd__ = __add__

    def __len__(self):
        '''Return the number of vertices in the graph.'''
        return len(self._nodes)

    def __contains__(self, node):
        '''Returns `True` if `x` is one of the nodes.'''
        return node in self._nodes

    def __le__(self, other):
        '''`g` <= `h` if `g` is a subgraph of `h`'''
        if not isinstance(other, DepGraph):
            return False
        # pylint: disable=protected-access
        return (all(node in other._nodes for node in self._nodes) and
                all(dep in other[node] for node in self._nodes
                    for dep in self[node]))

    def isomorphic_to(self, other):
        '''Returns `True` if this graph is isomorphic to `other`.'''

        if not isinstance(other, DepGraph):
            return False

        size = len(self)
        if size != len(other):
            return False
        i2o = [None] * size
        o2i = [None] * size
        for i, node in enumerate(self._nodes):
            # pylint: disable=W0212
            other_i = other._nodes.get_index(node, None)
            if other_i is None:
                LOGGER.debug('could not find node %s, not isomorphic', node)
                return False
            LOGGER.debug('node %s found: %d -> %d', node, i, other_i)
            i2o[i] = other_i
            o2i[other_i] = i
        if any(i is None for i in o2i):
            LOGGER.debug('some node is in other but not in self, '
                         'not isomorphic')
            return False
        for key, vals in self._edges.items():
            # pylint: disable=protected-access
            other_vals = set(o2i[o] for o in other._edges[i2o[key]])
            if set(vals) != set(other_vals):
                LOGGER.debug('node %d fails isomorphism check (%s != %s)',
                             key, vals, other_vals)
                return False
        LOGGER.debug('graphs are isomorphic')
        return True

    __eq__ = isomorphic_to

    def add_node(self, node):
        '''Add a new node to the graph.

        :param node: The new node.
        '''

        if node in self:
            LOGGER.info('Node %s already belongs to the graph', node)
            return

        new_index = len(self._nodes)
        self._nodes.append(node)
        self._edges[new_index] = set()
        return self

    def remove_node(self, node):
        '''Remove a node from the graph.

        Any edges going in and out of the node will be removed, too.

        :param node: The node to be removed.
        '''

        i = self._nodes.get_index(node, None)
        if i is None:
            LOGGER.warning('Cannot remove node %s: not in graph', node)
            return

        # first, we need to put the selected node at the end of the _nodes list
        last = len(self._nodes) - 1
        self._nodes.swap(i, last)
        # swap nodes in the _edges dictionary
        tmp = self._edges[i]
        self._edges[i] = self._edges[last]
        self._edges[last] = tmp

        def _swapper(k):
            if k == i:
                return last
            elif k == last:
                return i
            return k
        for k, vals in self._edges.items():
            self._edges[k] = set(map(_swapper, vals))
        # now we can remove the edges
        # remove edges from last
        del self._edges[last]
        # remove edges into last
        for k, vals in self._edges.items():
            self._edges[k] = set(n for n in vals if n != last)

        # finally, we can remove the node itself
        del self._nodes[last]

        return self

    def add_dependency(self, node, on):
        '''Add a new dependency to the graph.

        :param node: The node for which the dependency is specified.
        :param on: The node `node` depends on.
        '''

        self.add_node(node)
        self.add_node(on)
        i_node = self._nodes.index(node)
        i_on = self._nodes.index(on)
        self._edges[i_node].add(i_on)
        return self

    def remove_dependency(self, node, on):
        '''Remove a dependency from the graph.

        :param node: The node for which the dependency is specified.
        :param on: The node `node` depends on.
        '''

        i_node = self._nodes.index(node)
        i_on = self._nodes.index(on)
        try:
            self._edges[i_node].remove(i_on)
        except KeyError:
            raise KeyError('trying to remove missing edge {} -> {}'
                           .format(node, on))
        return self

    def invert(self):
        '''Invert the graph.

        :returns: A new graph having the same nodes but all edges inverted.
        '''

        inv_edges = {}
        for key, vals in self._edges.items():
            inv_edges.setdefault(key, [])
            for val in vals:
                inv_edges.setdefault(val, []).append(key)

        return DepGraph(self._nodes, inv_edges)

    def topological_sort(self):
        '''Perform a topological sort of the graph.

        :returns: The nodes of the graph, as a list, with the invariant that
                  each node appears in the list after all the nodes it depends
                  on.
        :raises DepGraphError: if the graph is cyclic.
                  '''

        result = []
        marks = {}

        def _visit(node):
            mark = marks.get(node, None)
            if mark == self._Marks.TEMP:
                raise DepGraphError('Dependency graph is cyclic!')
            if mark == self._Marks.PERM:
                return
            marks[node] = self._Marks.TEMP
            index = self._nodes.index(node)
            for target in self._edges.get(index, []):
                _visit(self._nodes[target])
            marks[node] = self._Marks.PERM
            result.append(node)

        for node in self._nodes:
            if node in marks:
                continue
            _visit(node)

        return result

    def copy(self):
        '''Return a copy of this graph. '''
        return DepGraph(self._nodes.copy(), self._edges.copy())

    def merge(self, other):
        '''Merge this graph in place with another one.

        :param DepGraph other: The graph to merge.
        '''

        for key, vals in other:
            self.add_node(key)
            for val in vals:
                self.add_dependency(key, on=val)
        return self

    __iadd__ = merge

    def nodes(self):
        '''Returns the graph nodes.'''
        return self._nodes

    def dependencies(self, node, recurse=False):
        '''Query the graph about the dependencies of `node`. If `recurse` is
        ``True``, also return indirect dependencies (the transitive closure of
        the specified node). With `recurse=False`, this operation is `O(1)`.

        :param bool recurse: If true, return indirect dependencies as well.
        :returns: A list containing the dependencies of `node`.
        '''

        from itertools import chain
        result = list(
            map(lambda i: self._nodes[i], self._edges[self._nodes.index(node)])
            )
        LOGGER.debug('dependencies: %s -> %s', node, result)
        if recurse:
            sub_deps = chain.from_iterable(self.dependencies(d, recurse)
                                           for d in result)
            return list(frozenset(sub_deps) | frozenset(result))
        return result

    __getitem__ = dependencies

    def dependees(self, node):
        '''Collect the nodes that depend on the given node. This operation is
        `O(N)`, where `N` is the number of nodes in the graph.

        :returns: A set containing the dependees of `node`.
        '''
        i = self._nodes.index(node)
        indices = set(n for n in range(len(self)) if i in self._edges[n])
        return list(self._nodes[i] for i in indices)

    def to_graphviz(self):
        '''Convert the graph to graphviz format.

        :returns: A string describing the file in graphviz format.
        '''

        gviz = [r'digraph {']
        for key, vals in self._edges.items():
            from_node = str(self._nodes[key])
            gviz.append(from_node + ';')
            for val in vals:
                to_node = str(self._nodes[val])
                gviz.append(from_node + ' -> ' + to_node)
        gviz.append(r'}')
        gviz.append('')
        return '\n'.join(gviz)

    def transitive_reduction(self):
        '''Perform a transitive reduction of the graph in place.'''

        def _visit(start_edges, current):
            current_edges = self._edges[current]
            LOGGER.debug('visiting: %s: %s, %s',
                         current, current_edges, start_edges)
            to_remove = set()
            for dest in current_edges:
                if dest in start_edges:
                    LOGGER.debug('  marking %s for removal', dest)
                    to_remove.add(dest)
                LOGGER.debug('  recursing into %s', dest)
                to_remove |= _visit(start_edges, dest)
            return to_remove

        LOGGER.debug(repr(self))
        for i_node in range(len(self)):
            to_remove = set()
            for j_node in self._edges[i_node]:
                to_remove |= _visit(self._edges[i_node], j_node)
            for j in to_remove:
                self._edges[i_node].remove(j)

        return self

    def transitive_closure(self):
        '''Perform a transitive closure of the graph in place.'''

        def _visit(start_edges, current):
            current_edges = self._edges[current]
            LOGGER.debug('visiting: %s: %s, %s',
                         current, current_edges, start_edges)
            to_add = set()
            for dest in current_edges:
                if dest not in start_edges:
                    LOGGER.debug('  marking %s for insertion', dest)
                    to_add.add(dest)
                LOGGER.debug('  recursing into %s', dest)
                to_add |= _visit(start_edges, dest)
            return to_add

        LOGGER.debug(repr(self))
        for i_node in range(len(self)):
            to_add = set()
            for j_node in self._edges[i_node]:
                to_add |= _visit(self._edges[i_node], j_node)
            for j in to_add:
                self._edges[i_node].add(j)

        return self

    def initial(self):
        '''Return the initial nodes of the graph.

        The initial nodes are the nodes that have no ingoing edge; i.e., no
        other node depends on them.

        :returns: The list of initial nodes.
        '''

        index_set = set(range(len(self)))
        itarget_set = set()
        for vals in self._edges.values():
            itarget_set |= set(vals)
        index_set.difference_update(itarget_set)
        return [self._nodes[i] for i in index_set]

    def terminal(self):
        '''Return the terminal nodes of the graph.

        The terminal nodes are the nodes that have no outgoing edge; i.e., they
        do not depend on any other node.

        :returns: The list of terminal nodes.
        '''

        return [n for n in self._nodes if len(self[n]) == 0]

    def graft(self, node):
        '''Graft the given node into the graph.

        :param DepGraph node: A DepGraph embedded as a graph node.
        '''

        # collect the incoming and outgoing edges
        deps = self[node]
        dependees = self.dependees(node)
        # remove the graph-node
        self.remove_node(node)
        # graft the graph-node by adding incoming edges into its initial nodes
        # and outgoing edges from its terminal nodes
        inits = node.initial()
        terms = node.terminal()
        LOGGER.debug('Initial nodes = %s', inits)
        LOGGER.debug('Terminal nodes = %s', terms)
        LOGGER.debug('Dependencies = %s', deps)
        LOGGER.debug('Dependees = %s', dependees)
        self += node  # merge
        LOGGER.debug('Merged graph = %r', self)
        for dep in deps:
            for term in terms:
                LOGGER.debug('Adding dependency of %s on %s',
                             term, dep)
                self.add_dependency(term, on=dep)
        for dependee in dependees:
            for init in inits:
                LOGGER.debug('Adding dependency of %s on %s',
                             dependee, init)
                self.add_dependency(dependee, on=init)
        LOGGER.debug('Grafted graph = %r', self)

        return self

    def flatten(self, recurse=True):
        '''Graft all DepGraph nodes into this graph.

        :param bool recurse: If true, recursively graft DepGraph nodes until
                             all nodes are flat.
        '''
        nodes = [n for n in self._nodes if isinstance(n, DepGraph)]
        while nodes:
            LOGGER.debug('flatten() will graft the following nodes: %s',
                         nodes)
            for node in nodes:
                self.graft(node)
            if not recurse:
                break
            nodes = [n for n in self._nodes if isinstance(n, DepGraph)]
        return self

    def depends(self, node1, node2, recurse=False):
        '''Return ``True`` if the node `node1` depends on `node2`.

        :param node1: The first node.
        :param node2: The second node.
        :param bool recurse: If true, look at indirect dependencies, too.
        :returns: ``True`` if `node1` directly (``recurse == False``) or
                  indirectly (``recurse == True``) depends on `node2`.
        '''

        import itertools
        ind1 = self._nodes.index(node1)
        ind2 = self._nodes.index(node2)
        deps1 = self._edges[ind1]
        depends = False
        while deps1:
            depends = ind2 in deps1
            if depends or not recurse:
                return depends
            deps1 = list(itertools.chain.from_iterable(self._edges[i]
                                                       for i in deps1))
        return depends
