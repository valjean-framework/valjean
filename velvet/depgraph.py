from enum import Enum


class DepGraphError(Exception):
    pass


class DepGraph:
    Marks = Enum('Marks', 'TEMP PERM')

    def __init__(self, dictionary):
        self.edges = dictionary
        self.nodes = frozenset(dictionary.keys()) \
            | frozenset(x for l in dictionary.values() for x in l)

    def __repr__(self):
        return str(self.edges)

    def invert(self):
        inv_dict = {}
        for k, vs in self.edges.items():
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


if __name__ == '__main__':
    g = DepGraph({1: [2, 3], 5: [7, 4, 1, 2]})
    l = list(g.topological_sort())
    print(g)
    print(l)
