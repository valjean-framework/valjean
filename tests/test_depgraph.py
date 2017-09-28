from hypothesis import given
from hypothesis.strategies import dictionaries, integers, lists
import unittest
from copy import deepcopy

from context import depgraph


class TestDepGraph(unittest.TestCase):

    @given(d=dictionaries(integers(0, 10),
                          lists(integers(0, 10), average_size=2),
                          average_size=10))
    def test_topological_sort(self, d):
        # We need to avoid circular dependencies in the generated dictionary.
        # We do this by ensuring that, for each (key, [value_1, value2, ...])
        # pair, we always have value_i>key.
        dag = deepcopy(d)
        for k, vals in d.items():
            new_vals = dag[k]
            for i, val in enumerate(vals):
                if val <= k:
                    new_val = 2*k-val+1
                    new_vals[i] = new_val

        g = depgraph.DepGraph(dag)
        l = list(g.topological_sort())
        assert self.successful_topological_sort(g, l)

    def successful_topological_sort(self, graph, sorted_list):
        seen = set()
        for item in sorted_list:
            dependencies = graph.edges.get(item, [])
            ok = all(x in seen for x in dependencies)
            if not ok:
                return False
            seen.add(item)
        return True


if __name__ == '__main__':
    unittest.main()
