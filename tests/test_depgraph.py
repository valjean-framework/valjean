#!/usr/bin/env python3

from hypothesis import given, note
from hypothesis.strategies import (integers, sets, text, lists, composite,
                                   sampled_from)
import copy
import pytest

from .context import valjean  # noqa: F401
import valjean.depgraph as depgraph


@composite
def depgraphs(draw, elements=integers(0, 10), average_size=10, average_deps=2):
    '''Composite Hypothesis strategy to generate acyclic DepGraph objects.'''
    ks = draw(lists(elements, average_size=average_size).map(sorted))
    dag = {}
    for i, k in enumerate(ks):
        vs = draw(sets(sampled_from(ks[i+1:])))
        dag[k] = vs
    return depgraph.DepGraph.from_dependency_dictionary(dag)


class TestDepGraph:

    @given(g=depgraphs())
    def test_complete(self, g):
        '''Test that the generated edge dictionary is complete'''
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

    @given(g=depgraphs())
    def test_topological_sort_int(self, g):
        '''Test the topological sort invariant with integer dicts.'''
        self.do_test_topological_sort(g)

    @given(g=depgraphs(elements=text(average_size=10)))
    def test_topological_sort_str(self, g):
        '''Test the topological sort invariant with string dicts.'''
        self.do_test_topological_sort(g)

    def do_test_topological_sort(self, g):
        '''Test the topological sort invariant.

        Ensure that items appearing later in the list do not depend on any of
        the items appearing earlier.
        '''

        l = list(g.topological_sort())
        note('topological sort: {}'.format(l))
        assert self.successful_topological_sort(g, l)

    def successful_topological_sort(self, graph, sorted_list):
        seen = set()
        for item in sorted_list:
            dependencies = graph.dependencies(item)
            ok = all(x in seen for x in dependencies)
            if not ok:
                return False
            seen.add(item)
        return True

    @given(g=depgraphs())
    def test_invert_roundtrip(self, g):
        '''Test that DepGraph.invert() is idempotent.'''

        new_g = g.invert().invert()
        assert new_g == g

    def test_cyclic_raises(self):
        g = depgraph.DepGraph.from_dependency_dictionary({0: [1], 1: [0]})
        with pytest.raises(depgraph.DepGraphError):
            g.topological_sort()

    @given(g=depgraphs())
    def test_equivalent_constructors(self, g):
        '''Test that incrementally and automatically generated graphs are
        isomorphic.'''

        g_incr = depgraph.DepGraph()
        for k, vs in g:
            g_incr.add_node(k)
            for v in vs:
                g_incr.add_node(v)
                g_incr.add_dependency(k, v)

        assert g.isomorphic_to(g_incr)

    @given(g=depgraphs())
    def test_self_isomorphism(self, g):
        '''Test that each graph is isomorphic to itself.'''
        assert g.isomorphic_to(g)

    @given(g=depgraphs())
    def test_dict_roundtrip(self, g):
        '''Test that each graph is isomorphic to itself.'''
        g_roundtrip = depgraph.DepGraph.from_dependency_dictionary(dict(g))
        assert g == g_roundtrip
