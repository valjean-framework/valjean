#!/usr/bin/env python3
# pylint: disable=no-value-for-parameter

'''Tests for the :mod:`depgraph` module.'''

from hypothesis import given, note, assume, event, settings
from hypothesis.strategies import (integers, sets, text, lists, composite,
                                   sampled_from, booleans)
import pytest

from ..context import valjean  # noqa: F401, pylint: disable=unused-import

# pylint: disable=wrong-import-order
import valjean.cosette.depgraph as depgraph


# pylint: disable=too-many-arguments
@composite
def dep_dicts(draw, elements=integers(0, 10), average_size=10, min_deps=0,
              max_deps=None, average_deps=2, **kwargs):
    '''Composite Hypothesis strategy to generate acyclic dependency
    dictionaries.'''
    keys = draw(lists(elements, average_size=average_size, unique=True,
                      **kwargs).map(sorted))
    dag = {}
    for i, key in enumerate(keys):
        vals = draw(sets(sampled_from(keys[i+1:]), min_size=min_deps,
                         average_size=average_deps, max_size=max_deps))
        dag[key] = vals
    return dag


# pylint: disable=too-many-arguments
@composite
def depgraphs(draw, elements=integers(0, 10), average_size=10, min_deps=0,
              max_deps=None, average_deps=2, **kwargs):
    '''Composite Hypothesis strategy to generate acyclic DepGraph objects.'''
    dag = draw(dep_dicts(elements, average_size=average_size,
                         min_deps=min_deps, average_deps=average_deps,
                         max_deps=max_deps, **kwargs))
    return depgraph.DepGraph.from_dependency_dictionary(dag)

######################
#  helper functions  #
######################


def is_complete(graph):
    '''Check that a graph is complete, i.e. that all nodes appear as keys.'''
    all_keys = set()
    all_values = set()
    for key, vals in graph:
        all_keys.add(key)
        for val in vals:
            all_values.add(val)
    note('keys: {}\nvalues: {}'.format(all_keys, all_values))
    return all_values <= all_keys


###########
#  tests  #
###########

@given(graph=depgraphs())
def test_complete(graph):
    '''Test that the generated edge dictionary is complete'''
    assert is_complete(graph)


@given(dag=dep_dicts(min_size=2))
def test_incomplete_is_completed(dag):
    '''Test that incomplete graph dictionaries are correctly completed.'''
    new_key = max(dag.keys()) + 1
    first_key = list(dag.keys())[0]
    dag[first_key].add(new_key)
    graph = depgraph.DepGraph.from_dependency_dictionary(dag)
    assert is_complete(graph)


@given(graph=depgraphs())
def test_topological_sort_int(graph):
    '''Test the topological sort invariant with integer dicts.'''
    do_test_topological_sort(graph)


@given(graph=depgraphs(elements=text(average_size=10)))
def test_topological_sort_str(graph):
    '''Test the topological sort invariant with string dicts.'''
    do_test_topological_sort(graph)


def do_test_topological_sort(graph):
    '''Test the topological sort invariant.

    Ensure that items appearing later in the list do not depend on any of
    the items appearing earlier.
    '''
    sorted_list = list(graph.topological_sort())
    note('topological sort: {}'.format(sorted_list))
    seen = set()
    for item in sorted_list:
        dependencies = graph.dependencies(item)
        success = all(x in seen for x in dependencies)
        if not success:
            assert False
        seen.add(item)


@given(graph=depgraphs())
def test_invert_roundtrip(graph):
    '''Test that DepGraph.invert() is idempotent.'''
    new_graph = graph.invert().invert()
    assert new_graph == graph


@given(graph=depgraphs())
def test_equivalent_constructors(graph):
    '''Test that incrementally and automatically generated graphs are
    isomorphic.'''
    graph_incr = depgraph.DepGraph()
    for key, vals in graph:
        graph_incr.add_node(key)
        for val in vals:
            graph_incr.add_node(val)
            graph_incr.add_dependency(key, val)

    note('graph: {!r}'.format(graph))
    note('graph_incr: {!r}'.format(graph_incr))
    assert graph.isomorphic_to(graph_incr)


@given(graph=depgraphs())
def test_self_isomorphism(graph):
    '''Test that each graph is isomorphic to itself.'''
    assert graph.isomorphic_to(graph)


@given(graph=depgraphs())
def test_add_node_breaks_iso(graph):
    '''Test that adding nodes breaks isomorphism.'''
    graph_copy = graph.copy()
    nodes = graph_copy.nodes()
    new_node = max(nodes) + 1 if nodes else 0
    graph_copy.add_node(new_node)
    assert not graph_copy.isomorphic_to(graph)


@given(graph=depgraphs(min_size=2))
def test_add_edge_breaks_iso(graph):
    '''Test that adding edges breaks isomorphism.'''
    nodes = graph.nodes()
    assume(not graph.depends(nodes[0], nodes[1]))
    graph_copy = graph.copy()
    graph_copy.add_dependency(nodes[0], nodes[1])
    assert not graph_copy.isomorphic_to(graph)


@given(graph=depgraphs())
def test_different_nodes_breaks_iso(graph):
    '''Test that having different nodes breaks isomorphism.'''
    graph2 = graph.copy()
    nodes = graph.nodes()
    new_node = max(nodes) + 1 if nodes else 0
    graph.add_node(new_node)
    graph2.add_node(new_node + 1)
    assert not graph2.isomorphic_to(graph)


@given(graph=depgraphs(min_size=2))
def test_add_remove_edge_roundtrip(graph):
    '''Test that adding + removing an edge is idempotent.'''
    graph_copy = graph.copy()
    nodes = graph.nodes()
    if graph.depends(nodes[0], nodes[1]):
        # edge exists, remove it first and add it back
        graph.remove_dependency(nodes[0], on=nodes[1])
        graph.add_dependency(nodes[0], on=nodes[1])
    else:
        # edge does not exist, add it first and remove it later
        graph.add_dependency(nodes[0], on=nodes[1])
        graph.remove_dependency(nodes[0], on=nodes[1])
    assert graph_copy.isomorphic_to(graph)


@given(graph=depgraphs())
def test_dict_roundtrip(graph):
    '''Test the graph -> dict -> graph roundtrip.'''
    roundtrip = depgraph.DepGraph.from_dependency_dictionary(dict(graph))
    assert graph == roundtrip


@settings(max_examples=10)
@given(graph=depgraphs())
def test_comparison_wrong_type(graph):
    '''Test that <= fails if the rhs is not a :class:`~.DepGraph`.'''
    assert not graph <= 42


@settings(max_examples=10)
@given(graph=depgraphs())
def test_isomorphism_wrong_type(graph):
    '''Test that :meth:`~.isomorphic_to` fails if the argument is not a
    :class:`~.DepGraph`.'''
    assert not graph.isomorphic_to(42)


@given(graph=depgraphs())
def test_subgraph_self(graph):
    '''Test that <= is reflexive.'''
    assert graph <= graph


@given(graph=depgraphs())
def test_merge_with_self(graph):
    '''Test that merging with `self` results in the identity.'''
    assert graph + graph == graph


@given(graph=depgraphs())
def test_merge_with_empty(graph):
    '''Test that merging with the empty graph results in the identity.'''
    assert graph + depgraph.DepGraph() == graph


@given(graph1=depgraphs(), graph2=depgraphs(), graph3=depgraphs())
def test_merge_associative(graph1, graph2, graph3):
    '''Test that merging graphs is associative.'''
    assert (graph1 + graph2) + graph3 == graph1 + (graph2 + graph3)


@given(graph1=depgraphs(), graph2=depgraphs())
def test_merge_commutative(graph1, graph2):
    '''Test that merging graphs is commutative.'''
    assert graph1 + graph2 == graph2 + graph1


@given(graph1=depgraphs(), graph2=depgraphs())
def test_merge_containment(graph1, graph2):
    '''Test that the merged graph contains both operands as subgraphs.'''
    graph = graph1 + graph2
    note('merged graph: {!r}'.format(graph))
    assert graph1 <= graph
    assert graph2 <= graph


@given(graph=depgraphs())
def test_trans_red_subgraph(graph):
    '''Test that transitive reduction results in a subgraph.'''
    graph_tr = graph.copy().transitive_reduction()
    note('reduced graph: {!r}'.format(graph_tr))
    assert graph_tr <= graph


@given(graph=depgraphs())
def test_trans_red_same_nodes(graph):
    '''Test that transitive reduction results in a graph over the same
    nodes.'''
    graph_tr = graph.copy().transitive_reduction()
    note('reduced graph: {!r}'.format(graph_tr))
    assert sorted(graph_tr.nodes()) == sorted(graph.nodes())


@given(graph=depgraphs())
def test_trans_red_reachability(graph):
    '''Test that transitive reduction results in a graph with the same
    reachability.'''
    graph_tr = graph.copy().transitive_reduction()
    for node in graph.nodes():
        all_deps = graph.dependencies(node, recurse=True)
        all_deps_tr = graph_tr.dependencies(node, recurse=True)
        assert sorted(all_deps) == sorted(all_deps_tr)


@given(graph=depgraphs())
def test_trans_red_idempotent(graph):
    '''Test that transitive reduction is idempotent.'''
    graph_tr = graph.copy().transitive_reduction()
    graph_tr2 = graph_tr.copy().transitive_reduction()
    assert graph_tr == graph_tr2


@given(graph=depgraphs())
def test_trans_closure_supergraph(graph):
    '''Test that transitive closure results in a supergraph.'''
    graph_cl = graph.copy().transitive_closure()
    note('closure graph: {!r}'.format(graph_cl))
    assert graph <= graph_cl


@given(graph=depgraphs())
def test_trans_closure_same_nodes(graph):
    '''Test that transitive closure results in a graph over the same
    nodes.'''
    graph_cl = graph.copy().transitive_closure()
    note('closure graph: {!r}'.format(graph_cl))
    assert sorted(graph_cl.nodes()) == sorted(graph.nodes())


@given(graph=depgraphs())
def test_trans_closure_reachability(graph):
    '''Test that transitive closure results in a graph with the same
    reachability.'''
    graph_cl = graph.copy().transitive_closure()
    for node in graph.nodes():
        all_deps = graph.dependencies(node, recurse=True)
        all_deps_cl = graph_cl.dependencies(node, recurse=True)
        assert sorted(all_deps) == sorted(all_deps_cl)


@given(graph=depgraphs())
def test_trans_closure_idempotent(graph):
    '''Test that transitive closure is idempotent.'''
    graph_cl = graph.copy().transitive_closure()
    graph_cl2 = graph_cl.copy().transitive_closure()
    assert graph_cl == graph_cl2


@given(graph=depgraphs())
def test_trans_closure_dependencies(graph):
    '''Test that indirect dependencies in a graph are converted into direct
    dependencies in the transitive closure.'''
    graph_cl = graph.copy().transitive_closure()
    for node in graph.nodes():
        assert (sorted(graph.dependencies(node, recurse=True)) ==
                sorted(graph_cl.dependencies(node, recurse=False)))


@given(graph=depgraphs(), recurse=booleans())
def test_depends(graph, recurse):
    '''Test that dependencies are correctly detected.'''
    nodes = set(graph.nodes())
    count_deps = 0
    count_no_deps = 0
    for node in nodes:
        deps = set(graph.dependencies(node, recurse))
        for dep in deps:
            assert graph.depends(node, dep, recurse)
            count_deps += 1
        for dep in nodes - deps:
            assert not graph.depends(node, dep, recurse)
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


@given(graph=depgraphs())
def test_terminal_no_edge(graph):
    '''Test that terminal nodes have no outgoing edge.'''
    terms = graph.terminal()
    for term in terms:
        assert not graph[term]


@given(graph=depgraphs())
def test_initial_terminal_invert(graph):
    '''Test that initial nodes are terminal nodes of the inverse graph.'''
    inits = graph.initial()
    graph_inv = graph.invert()
    terms_inv = graph_inv.terminal()
    assert sorted(inits) == sorted(terms_inv)


@given(graph=depgraphs())
def test_terminal_initial_invert(graph):
    '''Test that terminal nodes are initial nodes of the inverse graph.'''
    terms = graph.terminal()
    graph_inv = graph.invert()
    inits_inv = graph_inv.initial()
    assert sorted(inits_inv) == sorted(terms)


@given(graph=depgraphs(), new=integers())
def test_add_remove_is_identity(graph, new):
    '''Test that adding and removing a node results in the same graph.'''
    assume(new not in graph)
    graph_copy = graph.copy().add_node(new)
    n_nodes = len(graph)
    if n_nodes > 1:
        event("added incoming edge")
        old = graph.nodes()[1]
        graph_copy.add_dependency(old, on=new)
    elif n_nodes > 0:
        event("added incoming and outgoing edge")
        old = graph.nodes()[0]
        graph_copy.add_dependency(new, on=old)
    else:
        event("no edges added")
    graph_copy.remove_node(new)
    assert graph == graph_copy


@given(graph1=depgraphs(min_size=2), graph2=depgraphs())
def test_flatten_dependencies(graph1, graph2):
    '''Test that grafting one graph into another respects the dependency
    topology.
    '''
    # add graph2 into graph1; graph1 has at least two nodes
    nodes = graph1.nodes()
    node0 = nodes[0]
    node1 = nodes[0]
    graph1.add_dependency(node0, on=graph2)
    graph1.add_dependency(graph2, on=node1)
    graph1.flatten()
    for node in graph2.nodes():
        assert graph1.depends(node0, node, recurse=True)
        assert graph1.depends(node, node1, recurse=True)
    event('min_graph_size={}'.format(min(len(graph1), len(graph2))))


@given(graph1=depgraphs(min_size=2), graph2=depgraphs())
def test_flatten_size(graph1, graph2):
    '''Test that grafting one graph into another yields a graph with the
    correct size.
    '''
    expected_nodes = set(graph1.nodes()) | set(graph2.nodes())
    note('graph1: {!r}'.format(graph1))
    note('graph2: {!r}'.format(graph2))
    note('expected_nodes: {}'.format(expected_nodes))
    expected_n_nodes = len(expected_nodes)
    # add graph2 into graph1; graph1 has at least two nodes
    nodes = graph1.nodes()
    graph1.add_dependency(nodes[0], on=graph2)
    graph1.add_dependency(graph2, on=nodes[1])
    note('before flattening: {!r}'.format(graph1))
    graph1.flatten()
    note('after flattening: {!r}'.format(graph1))
    observed_n_nodes = len(graph1)
    event('min_graph_size={}'.format(min(len(graph1), len(graph2))))
    assert expected_n_nodes == observed_n_nodes


@given(graph1=depgraphs(min_size=2), graph2=depgraphs(min_size=2),
       graph3=depgraphs())
def test_flatten_size3(graph1, graph2, graph3):
    '''Test that grafting three nested graphs yields a graph with the
    correct size.
    '''
    expected_nodes = set(graph1.nodes()) | set(graph2.nodes())
    note('expected_nodes: {}'.format(expected_nodes))
    expected_n_nodes = len(expected_nodes) + 1
    # add g3 into graph2; graph2 has at least two nodes
    graph2.add_dependency(graph2.nodes()[0], on=graph3)
    graph2.add_dependency(graph3, on=graph2.nodes()[1])
    # add graph2 into graph1; graph1 has at least two nodes
    graph1.add_dependency(graph1.nodes()[0], on=graph2)
    graph1.add_dependency(graph2, on=graph1.nodes()[1])
    note('graph1: {!r}'.format(graph1))
    note('graph2: {!r}'.format(graph2))
    note('graph3: {!r}'.format(graph3))
    note('before flattening: {!r}'.format(graph1))
    graph1.flatten(recurse=False)
    note('after flattening: {!r}'.format(graph1))
    observed_n_nodes = len(graph1)
    event('min_graph_size={}'.format(min(len(graph1), len(graph2),
                                         len(graph3))))
    assert expected_n_nodes == observed_n_nodes


@given(graph1=depgraphs(min_size=2), graph2=depgraphs(min_size=2),
       graph3=depgraphs())
def test_recursive_flatten_size3(graph1, graph2, graph3):
    '''Test that grafting three nested graphs yields a graph with the
    correct size.
    '''
    nodes1 = graph1.nodes()
    nodes2 = graph2.nodes()
    nodes3 = graph3.nodes()
    expected_nodes = set(nodes1) | set(nodes2) | set(nodes3)
    note('expected_nodes: {}'.format(expected_nodes))
    expected_n_nodes = len(expected_nodes)
    # add graph3 into graph2; graph2 has at least two nodes
    graph2.add_dependency(nodes2[0], on=graph3)
    graph2.add_dependency(graph3, on=nodes2[1])
    # add graph2 into graph1; graph1 has at least two nodes
    graph1.add_dependency(nodes1[0], on=graph2)
    graph1.add_dependency(graph2, on=nodes1[1])
    note('graph1: {!r}'.format(graph1))
    note('graph2: {!r}'.format(graph2))
    note('graph3: {!r}'.format(graph3))
    note('before flattening: {!r}'.format(graph1))
    graph1.flatten()
    note('after flattening: {!r}'.format(graph1))
    observed_n_nodes = len(graph1)
    event('min_graph_size={}'.format(min(len(graph1), len(graph2),
                                         len(graph3))))
    assert expected_n_nodes == observed_n_nodes


@given(graph=depgraphs(min_size=1))
def test_dependees(graph):
    '''Test that dependees are correctly computed.'''
    node0 = graph.nodes()[0]
    dependees = graph.dependees(node0)
    for dep in dependees:
        assert node0 in graph[dep]


@given(graph=depgraphs(min_size=1))
def test_to_graphviz(graph):
    '''Test that DepGraph produces syntactically correct `dot` files.'''
    pydot = pytest.importorskip('pydot')
    gviz = graph.to_graphviz()
    pydot.graph_from_dot_data(gviz)


#######################################
#  tests that should raise exceptions #
#######################################

def test_cyclic_raises():
    '''Test that sorting a cyclic graph raises an exception.'''
    graph = depgraph.DepGraph.from_dependency_dictionary({0: [1], 1: [0]})
    with pytest.raises(depgraph.DepGraphError):
        graph.topological_sort()


@settings(max_examples=10)
@given(graph=depgraphs(max_deps=0, average_deps=0, min_size=2))
def test_remove_missing_edge_raises(graph):
    '''Test that removing a missing edge raises an exception.'''
    nodes = graph.nodes()
    assert not graph.depends(nodes[0], nodes[1])
    with pytest.raises(KeyError):
        graph.remove_dependency(nodes[0], on=nodes[1])
