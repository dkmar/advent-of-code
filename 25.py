#!/usr/bin/env python3
from lib import *

# 23:11
infile = sys.argv[1] if len(sys.argv)>1 else '25.in'
f = open(infile, 'r') if infile != '-' else sys.stdin

lines = list(map(Input, f))
part1 = part2 = 0
'''
pxv: xtm lsh jgq
tgb: jqb rmh fzx
fnf: mpx lzb vnb sgd lhz
blx: xrj
zql: czm kqz gjt rxn
'''

class UnionFind:
    def __init__(self, n: int):
        self.root = list(range(n))
        self.size = [1] * n

    def find(self, u):
        if self.root[u] == u:
            # if u is its own root, just return.
            return u

        # find root of u and compress path along the way.
        self.root[u] = self.find(self.root[u])
        return self.root[u]

    def union(self, u, v) -> int | None:
        ''' returns root id if the union was performed, None otherwise '''
        ru, rv = self.find(u), self.find(v)
        if ru == rv:
            # already sharing a root.
            return None

        size = self.size
        # union under higher-rank root.
        if size[ru] >= size[rv]:
            self.root[rv] = ru
            size[ru] += size[rv]
            return ru
        else:
            self.root[ru] = rv
            size[rv] += size[ru]
            return rv


def find_bipartition(graph: dict, edges: list):
    '''
    return (# of edges unused), (size of component 1), (size of component 2)
    The unused edges are those bridging components 1 and 2.
    '''
    uf = UnionFind(N := len(graph))
    component_count = N

    random.shuffle(edges)
    edge_pool = iter(edges)
    for u,v in edge_pool:
        uv = uf.union(u,v)
        if uv is None:
            continue

        component_count -= 1
        if component_count == 2:
            bridges = sum(1 for u,v in edge_pool if uf.find(u) != uf.find(v))

            c1_size = uf.size[uv]
            c2_size = N - c1_size
            return bridges, c1_size, c2_size

    # unreachable
    raise RuntimeError('Failed to partition graph.')


def vertex_to_id(v) -> int:
    if (vid := vertex_id.get(v)) is not None:
        return vid
    vertex_id[v] = vid = len(vertices)
    vertices.append(v)
    return vid

vertices = []
vertex_id = {}
edges = []
graph = defaultdict(list)

for line in lines:
    nodes = line.drop(':').split()
    src, *dsts = map(vertex_to_id, nodes)

    for dst in dsts:
        graph[src].append(dst)
        graph[dst].append(src)
        edges.append((src, dst))

# something like Karger's Algorithm to find minimum cut.
while True:
    num_bridges, group1_size, group2_size = find_bipartition(graph, edges)
    if num_bridges == 3:
        part1 = group1_size * group2_size
        break

print(f'Part 1: {part1}')
print(f'Part 2: {part2}')
