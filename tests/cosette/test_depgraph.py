#!/usr/bin/env python3

from hypothesis import given, note, assume, event
from hypothesis.strategies import (integers, sets, text, lists, composite,
                                   sampled_from, data, booleans)
import pytest

from ..context import valjean  # noqa: F401
import valjean.cosette.depgraph as depgraph


@composite
def depgraphs(draw, elements=integers(0, 10), average_size=10, average_deps=2,
              **kwargs):
    '''Composite Hypothesis strategy to generate acyclic DepGraph objects.'''
    ks = draw(lists(elements, average_size=average_size,
                    unique=True, **kwargs).map(sorted))
    dag = {}
    for i, k in enumerate(ks):
        vs = draw(sets(sampled_from(ks[i+1:]), average_size=average_deps))
        dag[k] = vs
    return depgraph.DepGraph.from_dependency_dictionary(dag)


class TestDepGraph:

    @given(g=depgraphs())
    def test_complete(self, g):
        '''Test that the generated edge dictionary is complete'''
        keys = set()
        values = set()
        for k, vs in g:
            keys.add(k)
            for v in vs:
                values.add(v)
        note('keys: {}\nvalues: {}'.format(keys, values))
        assert values <= keys

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

    @given(g=depgraphs())
    def test_subgraph_self(self, g):
        '''Test that merging with self results in the identity.'''
        assert g <= g

    @given(g=depgraphs())
    def test_merge_with_self_is_identity(self, g):
        '''Test that merging with self results in the identity.'''
        assert g + g == g

    @given(g=depgraphs())
    def test_merge_with_empty_is_identity(self, g):
        '''Test that merging with the empty graph results in the identity.'''
        assert g + depgraph.DepGraph() == g

    @given(g1=depgraphs(), g2=depgraphs(), g3=depgraphs())
    def test_merge_associative(self, g1, g2, g3):
        '''Test that merging graphs is associative.'''
        assert (g1 + g2) + g3 == g1 + (g2 + g3)

    @given(g1=depgraphs(), g2=depgraphs())
    def test_merge_commutative(self, g1, g2):
        '''Test that merging graphs is commutative.'''
        assert g1 + g2 == g2 + g1

    @given(g1=depgraphs(), g2=depgraphs())
    def test_merge_containment(self, g1, g2):
        '''Test that the merged graph contains both operands as subgraphs.'''
        g = g1 + g2
        note(repr(g))
        assert g1 <= g
        assert g2 <= g

    @given(g=depgraphs())
    def test_transitive_reduction_subgraph(self, g):
        '''Test that transitive reduction results in a subgraph.'''
        g_tr = g.copy().transitive_reduction()
        note('reduced graph: {}'.format(repr(g_tr)))
        assert g_tr <= g

    @given(g=depgraphs())
    def test_transitive_reduction_same_nodes(self, g):
        '''Test that transitive reduction results in a graph over the same
        nodes.'''
        g_tr = g.copy().transitive_reduction()
        note('reduced graph: {}'.format(repr(g_tr)))
        assert sorted(g_tr.nodes()) == sorted(g.nodes())

    @given(g=depgraphs())
    def test_transitive_reduction_same_reachability(self, g):
        '''Test that transitive reduction results in a graph with the same
        reachability.'''
        g_tr = g.copy().transitive_reduction()
        for node in g.nodes():
            all_deps = g.dependencies(node, recurse=True)
            all_deps_tr = g_tr.dependencies(node, recurse=True)
            assert sorted(all_deps) == sorted(all_deps_tr)

    @given(g=depgraphs())
    def test_transitive_reduction_idempotent(self, g):
        '''Test that transitive reduction is idempotent.'''
        g_tr = g.copy().transitive_reduction()
        g_tr2 = g_tr.copy().transitive_reduction()
        assert g_tr == g_tr2

    @given(g=depgraphs())
    def test_transitive_closure_supergraph(self, g):
        '''Test that transitive closure results in a supergraph.'''
        g_cl = g.copy().transitive_closure()
        note('closure graph: {}'.format(repr(g_cl)))
        assert g <= g_cl

    @given(g=depgraphs())
    def test_transitive_closure_same_nodes(self, g):
        '''Test that transitive closure results in a graph over the same
        nodes.'''
        g_cl = g.copy().transitive_closure()
        note('closure graph: {}'.format(repr(g_cl)))
        assert sorted(g_cl.nodes()) == sorted(g.nodes())

    @given(g=depgraphs())
    def test_transitive_closure_same_reachability(self, g):
        '''Test that transitive closure results in a graph with the same
        reachability.'''
        g_cl = g.copy().transitive_closure()
        for node in g.nodes():
            all_deps = g.dependencies(node, recurse=True)
            all_deps_cl = g_cl.dependencies(node, recurse=True)
            assert sorted(all_deps) == sorted(all_deps_cl)

    @given(g=depgraphs())
    def test_transitive_closure_idempotent(self, g):
        '''Test that transitive closure is idempotent.'''
        g_cl = g.copy().transitive_closure()
        g_cl2 = g_cl.copy().transitive_closure()
        assert g_cl == g_cl2

    @given(g=depgraphs())
    def test_transitive_closure_same_as_dependencies(self, g):
        '''Test that transitive closure is idempotent.'''
        g_cl = g.copy().transitive_closure()
        for node in g.nodes():
            assert (sorted(g.dependencies(node, recurse=True)) ==
                    sorted(g_cl.dependencies(node, recurse=False)))

    @given(g=depgraphs(), recurse=booleans())
    def test_depends(self, g, recurse):
        '''Test that dependencies are correctly detected.'''
        nodes = set(g.nodes())
        count_deps = 0
        count_no_deps = 0
        for n in nodes:
            deps = set(g.dependencies(n, recurse))
            for d in deps:
                assert g.depends(n, d, recurse)
                count_deps += 1
            for d in nodes - deps:
                assert not g.depends(n, d, recurse)
                count_no_deps += 1
        if count_deps < 5:
            event('count_deps = {}'.format(count_deps))
        else:
            event('count_deps > 5')
        if count_no_deps < 5:
            event('count_no_deps = {}'.format(count_no_deps))
        else:
            event('count_no_deps > 5')
        event('recurse = {}'.format(recurse))

    @given(g=depgraphs())
    def test_terminal_no_edge(self, g):
        '''Test that terminal nodes have no outgoing edge.'''
        terms = g.terminal()
        for term in terms:
            assert len(g[term]) == 0

    @given(g=depgraphs())
    def test_initial_terminal_invert(self, g):
        '''Test that initial nodes are terminal nodes of the inverse graph.'''
        inits = g.initial()
        g_inv = g.invert()
        terms_inv = g_inv.terminal()
        assert sorted(inits) == sorted(terms_inv)

    @given(g=depgraphs())
    def test_terminal_initial_invert(self, g):
        '''Test that terminal nodes are initial nodes of the inverse graph.'''
        terms = g.terminal()
        g_inv = g.invert()
        inits_inv = g_inv.initial()
        assert sorted(inits_inv) == sorted(terms)

    @given(g=depgraphs(), data=data())
    def test_swap_indices_isomorphism(self, g, data):
        '''Test that swapping two nodes results in an isomorphic graph.'''
        i = data.draw(sampled_from(range(len(g))))
        j = data.draw(sampled_from(range(len(g))))
        g_swapped = g.copy()._swap_indices(i, j)
        assert g.isomorphic_to(g_swapped)

    @given(g=depgraphs(), new=integers())
    def test_add_remove_is_identity(self, g, new):
        '''Test that adding and removing a node results in the same graph.'''
        assume(new not in g)
        g_copy = g.copy().add_node(new)
        if len(g) > 1:
            event("added incoming edge")
            old = g._nodes[1]
            g_copy.add_dependency(old, on=new)
        elif len(g) > 0:
            event("added incoming and outgoing edge")
            old = g._nodes[0]
            g_copy.add_dependency(new, on=old)
        else:
            event("no edges added")
        g_copy.remove_node(new)
        assert g == g_copy

    @given(g1=depgraphs(min_size=2), g2=depgraphs())
    def test_flatten_dependencies(self, g1, g2):
        '''Test that grafting one graph into another respects the dependency
        topology.
        '''
        # add g2 into g1; g1 has at least two nodes
        n0 = g1._nodes[0]
        n1 = g1._nodes[1]
        g1.add_dependency(n0, on=g2)
        g1.add_dependency(g2, on=n1)
        g1.flatten()
        for n in g2.nodes():
            assert g1.depends(n0, n, recurse=True)
            assert g1.depends(n, n1, recurse=True)
        event('min_graph_size={}'.format(min(len(g1), len(g2))))

    @given(g1=depgraphs(min_size=2), g2=depgraphs())
    def test_flatten_size(self, g1, g2):
        '''Test that grafting one graph into another yields a graph with the
        correct size.
        '''
        expected_nodes = set(g1.nodes()) | set(g2.nodes())
        note('g1: {}'.format(repr(g1)))
        note('g2: {}'.format(repr(g2)))
        note('expected_nodes: {}'.format(expected_nodes))
        expected_n_nodes = len(expected_nodes)
        # add g2 into g1; g1 has at least two nodes
        g1.add_dependency(g1._nodes[0], on=g2)
        g1.add_dependency(g2, on=g1._nodes[1])
        note('before flattening: {}'.format(repr(g1)))
        g1.flatten()
        note('after flattening: {}'.format(repr(g1)))
        observed_n_nodes = len(g1)
        event('min_graph_size={}'.format(min(len(g1), len(g2))))
        assert expected_n_nodes == observed_n_nodes

    @given(g1=depgraphs(min_size=2), g2=depgraphs(min_size=2), g3=depgraphs())
    def test_recursive_flatten_size(self, g1, g2, g3):
        '''Test that grafting three nested graphs yields a graph with the
        correct size.
        '''
        expected_nodes = set(g1.nodes()) | set(g2.nodes()) | set(g3.nodes())
        note('g1: {}'.format(repr(g1)))
        note('g2: {}'.format(repr(g2)))
        note('g3: {}'.format(repr(g3)))
        note('expected_nodes: {}'.format(expected_nodes))
        expected_n_nodes = len(expected_nodes)
        # add g3 into g2; g2 has at least two nodes
        g2.add_dependency(g2._nodes[0], on=g3)
        g2.add_dependency(g3, on=g2._nodes[1])
        # add g2 into g1; g1 has at least two nodes
        g1.add_dependency(g1._nodes[0], on=g2)
        g1.add_dependency(g2, on=g1._nodes[1])
        note('before flattening: {}'.format(repr(g1)))
        g1.flatten()
        note('after flattening: {}'.format(repr(g1)))
        observed_n_nodes = len(g1)
        event('min_graph_size={}'.format(min(len(g1), len(g2), len(g3))))
        assert expected_n_nodes == observed_n_nodes

    @given(g=depgraphs(min_size=1))
    def test_dependees(self, g):
        '''Test that dependees are correctly computed.'''
        n0 = g._nodes[0]
        dependees = g.dependees(n0)
        for d in dependees:
            assert n0 in g[d]
