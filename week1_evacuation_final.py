# python3
from collections import OrderedDict

class Edge:

    def __init__(self, u, v, capacity, flow):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = flow

# This class implements a bit unusual scheme for storing edges of the graph,
# in order to retrieve the backward edge for a given edge quickly.
class FlowGraph:

    def __init__(self, n):
        # List of all - forward and backward - edges
        self.edges = []
        # These adjacency lists store only indices of edges in the edges list
        self.graph = [[] for _ in range(n)]

    def add_edge(self, from_, to, capacity):
        # Note that we first append a forward edge and then a backward edge,
        # so all forward edges are stored at even indices (starting from 0),
        # whereas backward edges are stored at odd indices.
        forward_edge = Edge(from_, to, capacity, 0)
        backward_edge = Edge(to, from_, capacity, capacity)
        self.graph[from_].append(len(self.edges))
        self.edges.append(forward_edge)
        self.graph[to].append(len(self.edges))
        self.edges.append(backward_edge)

    def size(self):
        return len(self.graph)

    def get_ids(self, from_):
        return self.graph[from_]

    def get_edge(self, id):
        return self.edges[id]

    def add_flow(self, id, flow):
        # To get a backward edge for a true forward edge (i.e id is even), we should get id + 1
        # due to the described above scheme. On the other hand, when we have to get a "backward"
        # edge for a backward edge (i.e. get a forward edge for backward - id is odd), id - 1
        # should be taken.
        #
        # It turns out that id ^ 1 works for both cases. Think this through!
        self.edges[id].flow += flow
        self.edges[id ^ 1].flow -= flow

def read_data():
    vertex_count, edge_count = map(int, input().split())
    # print('vertices')

    us, vs, capacities = [], [], []

    graph = FlowGraph(vertex_count)

    for _ in range(edge_count):
        # print('edges')
        u, v, capacity = map(int, input().split())
        us.append(u)
        vs.append(v)
        capacities.append(capacity)


    if len(us) > 1:
        current_forward_ind = 0
        current_backward_ind = 1

        current_u, current_v, current_capacity = us[0], vs[0], capacities[0]

        if current_u != current_v:
            graph.add_edge(current_u - 1, current_v - 1, current_capacity)

        for ind, l in enumerate(us[1:]):
            u, v, capacity = us[ind+1], vs[ind+1], capacities[ind+1]

            if u != v:

                if current_u == u and current_v == v:

                    graph.get_edge(current_forward_ind).capacity += capacity
                    graph.get_edge(current_backward_ind).capacity += capacity
                    graph.get_edge(current_backward_ind).flow += capacity

                else:
                    graph.add_edge(u-1, v-1, capacity)
                    current_u = u
                    current_v = v
    else:

        for ind, l in enumerate(us):
            u, v, capacity = us[ind], vs[ind], capacities[ind]

            if u != v:
                graph.add_edge(u - 1, v - 1, capacity)

    return graph

def update_graph(direction, graph: FlowGraph):

    min_remaining = 1000000
    edge_indices = []
    for i, node in enumerate(direction[:-1]):
        # print('node:', node)
        indices = graph.get_ids(node)

        # can write a search algorithm for this
        for index in indices:
            # print('index, i+1', index, ' ', graph.get_edge(index).v, ' ', direction[i+1])
            if graph.get_edge(index).v == direction[i+1]: # we found the edge that connects our current node to the next node in the flow path
                edge_indices.append(index)

                remaining_capacity = graph.get_edge(index).capacity - graph.get_edge(index).flow
                # print('remaining capacity', remaining_capacity)
                if remaining_capacity < min_remaining:
                    min_remaining = remaining_capacity

                break


    for edge_index in edge_indices:
        graph.add_flow(edge_index, min_remaining)

def max_flow(graph, from_, to):
    flow = 0
    if len(graph.edges) > 0:

        there_is_direction = True

        while there_is_direction:

            direction = bfs(graph, from_, to)

            if direction is not None:
                # print('direction:', direction)
                update_graph(direction, graph)
            else:
                there_is_direction = False

        for first_neighbor in graph.get_ids(0):
            if first_neighbor%2 == 0:
                flow += graph.get_edge(first_neighbor).flow

    return flow

def calculate_direction(directions, to, from_):
    direction = []
    latest_node = to
    for (key, value) in reversed(list(directions.items())):
        if latest_node in value:
            direction.append(latest_node)
            latest_node = key

            if key == from_:
                direction.append(key)
                break
    # print('reversed:', direction)
    return direction[::-1]

def bfs(graph: FlowGraph, from_, to,):

    remaining = []
    visited = []
    directions = OrderedDict()

    remaining.append(from_)

    while len(remaining) > 0:
        # print('rema', remaining)
        current_node = remaining.pop(0)

        if current_node == to:

            direction = calculate_direction(directions, to=to, from_=from_)

            return direction

        if not current_node in visited:
            visited.append(current_node)

        edges = graph.get_ids(current_node)

        neighbors = [graph.get_edge(id_).v for id_ in edges if graph.get_edge(id_).v not in visited
                     and graph.get_edge(id_).v not in remaining
                     and (graph.get_edge(id_).capacity-graph.get_edge(id_).flow) > 0]

        directions[current_node] = neighbors

        remaining += neighbors
    return None

if __name__ == '__main__':

    graph = read_data()
    maxf = max_flow(graph, 0, graph.size() - 1)
    print(maxf)
