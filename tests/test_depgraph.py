#!/usr/bin/env python3

from hypothesis import given, note
from hypothesis.strategies import dictionaries, integers, frozensets, text
import copy
import pytest

import context  # noqa: F401
import velvet.depgraph as depgraph


def remove_cycles(d):
    '''Suppress cycles in a graph

    The graph d is expressed as an adjacency dictionary of integers.  We
    remove cycles by ensuring that, for each (key, [value_1, value2, ...])
    pair, we always have value_i>key.
    '''

    dag = copy.copy(d)
    for k, vals in d.items():
        new_vals = list(vals)
        for i, val in enumerate(vals):
            if val <= k:
                if isinstance(val, str):
                    new_val = k + val
                else:
                    new_val = 2*k-val+1
                new_vals[i] = new_val
        dag[k] = frozenset(new_vals)
    return dag


class TestDepGraph:

    @given(dag=dictionaries(integers(0, 10),
           frozensets(integers(0, 10), average_size=2), average_size=10))
    def test_complete(self, dag):
        '''Test that the generated edge dictionary is complete'''

        g = depgraph.DepGraph.from_dependency_dictionary(dag)
        assert self.edges_dict_is_complete(g)

    def edges_dict_is_complete(self, graph):
        keys = set()
        values = set()
        for k, vs in graph.edges.items():
            keys.add(k)
            for v in vs:
                values.add(v)
        note('keys: {}\nvalues: {}'.format(keys, values))
        return values <= keys

    @given(dag=dictionaries(integers(0, 10),
           frozensets(integers(0, 10), average_size=2), average_size=10)
           .map(remove_cycles))
    def test_topological_sort_int(self, dag):
        '''Test the topological sort invariant with integer dicts.'''

        self.do_test_topological_sort(dag)

    @given(dag=dictionaries(text(average_size=10),
           frozensets(text(average_size=10), average_size=2), average_size=10)
           .map(remove_cycles))
    def test_topological_sort_str(self, dag):
        '''Test the topological sort invariant with string dicts.'''

        self.do_test_topological_sort(dag)

    def do_test_topological_sort(self, dag):
        '''Test the topological sort invariant

        Ensure that items appearing later in the list do not depend on any of
        the items appearing earlier.
        '''

        g = depgraph.DepGraph.from_dependency_dictionary(dag)
        l = list(g.topological_sort())
        assert self.successful_topological_sort(g, l)

    def successful_topological_sort(self, graph, sorted_list):
        seen = set()
        for item in sorted_list:
            dependencies = graph.edges.get(item, frozenset())
            ok = all(x in seen for x in dependencies)
            if not ok:
                return False
            seen.add(item)
        return True

    @given(dag=dictionaries(integers(0, 10),
           frozensets(integers(0, 10), average_size=2), average_size=10))
    def test_invert_roundtrip(self, dag):
        '''Test that DepGraph.invert() is idempotent.'''

        g = depgraph.DepGraph.from_dependency_dictionary(dag)
        new_g = g.invert().invert()
        note('dag: {}\ng.edges: {}\nnew_g.edges: {}'
             .format(dag, g.edges, new_g.edges))
        assert new_g.isomorphic_to(g)

    def test_cyclic_raises(self):
        g = depgraph.DepGraph.from_dependency_dictionary({0: [1], 1: [0]})
        with pytest.raises(depgraph.DepGraphError):
            g.topological_sort()
