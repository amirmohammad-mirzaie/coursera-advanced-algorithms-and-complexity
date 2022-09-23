# python3
from collections import OrderedDict


class Edge:
    """
    class used for creating edges
    """
    def __init__(self, u, v, capacity, flow) -> None:
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = flow


class Graph:
    """
    class used for creating a graph. I used the same procedure the coursera used for the first assignment (evacuation)
    """
    def __init__(self, adjacency_matrix) -> None:

        self.adj = adjacency_matrix

        self.n_crews = len(self.adj[0])
        self.n_flights = len(self.adj)

        self.starting_index_flights = self.n_crews
        self.node_start_index = self.n_crews + self.n_flights
        self.node_end_index = self.node_start_index + 1

        self.node_neighbors = [[] for _ in range(self.n_crews + self.n_flights + 2)]

        self.edges = []

    def get_edge(self, eid):
        return self.edges[eid]

    def create_edge_from_adjacency_matrix(self, ):

        for i in range(self.n_flights):
            for j in range(self.n_crews):

                if self.adj[i][j] == 1:
                    edge = Edge(u=j, v=self.starting_index_flights + i, capacity=1, flow=0)
                    self.node_neighbors[j].append(len(self.edges))
                    self.edges.append(edge)

                    backward_edge = Edge(u=self.starting_index_flights + i, v=j, capacity=1, flow=1)
                    self.node_neighbors[self.starting_index_flights + i].append(len(self.edges))
                    self.edges.append(backward_edge)

        for j in range(self.n_crews):
            edge = Edge(u=self.node_start_index, v=j, capacity=1, flow=0)
            self.node_neighbors[self.node_start_index].append(len(self.edges))
            self.edges.append(edge)

            backward_edge = Edge(u=j, v=self.node_start_index, capacity=1, flow=1)
            self.node_neighbors[j].append(len(self.edges))
            self.edges.append(backward_edge)

        for i in range(self.n_flights):
            edge = Edge(u=self.starting_index_flights + i, v=self.node_end_index, capacity=1, flow=0)
            self.node_neighbors[self.starting_index_flights + i].append(len(self.edges))
            self.edges.append(edge)

            backward_edge = Edge(u=self.node_end_index, v=self.starting_index_flights + i, capacity=1, flow=1)
            self.node_neighbors[self.node_end_index].append(len(self.edges))
            self.edges.append(backward_edge)


class MaxMatching:

    def read_data(self):
        n, m = map(int, input().split())
        adj_matrix = [list(map(int, input().split())) for i in range(n)]
        return adj_matrix

    def read_data_from_path(self, path):
        file1 = open(path, 'r')
        Lines = file1.readlines()

        n, m = map(int, Lines[0].split())

        adj_matrix = [list(map(int, Lines[i + 1].split())) for i in range(n)]
        return adj_matrix

    def write_response(self, matching):
        line = [str(-1 if x == -1 else x + 1) for x in matching]
        print(' '.join(line))

    def find_matching(self, adj_matrix):

        # Replace this code with an algorithm that finds the maximum
        # matching correctly in all cases.

        graph = Graph(adj_matrix)
        graph.create_edge_from_adjacency_matrix()

        from_index = graph.node_start_index
        to_index = graph.node_end_index

        calculations = Calculations()

        can_go_forward = True

        while can_go_forward:

            # it turns out that DFS is working much better than BFS for this problem
            path = calculations.dfs(graph, from_index, to_index)

            if path is None:
                can_go_forward = False

            else:
                calculations.update_direction(graph, path)

        return calculations.generate_proper_format_string(graph)

    def solve(self, ):
        max_matching = MaxMatching()
        adj_matrix = max_matching.read_data()
        graph = Graph(adj_matrix)
        graph.create_edge_from_adjacency_matrix()
        a = max_matching.find_matching(adj_matrix)
        print(a)

    def solve_from_path(self, path):
        max_matching = MaxMatching()
        adj_matrix = max_matching.read_data_from_path(path)
        graph = Graph(adj_matrix)
        graph.create_edge_from_adjacency_matrix()
        a = max_matching.find_matching(adj_matrix)
        print(a)


class Calculations:

    def bfs(self, graph, from_, to, ):
        '''implementing a BFS using a while loop
        '''
        directions = OrderedDict()
        visited = []

        remaining = []
        remaining.append(from_)

        while len(remaining):

            first = remaining.pop(0)

            if first == to:
                path = self.find_path(directions, to, from_, )
                return path

            visited.append(first)

            neighbors = [graph.edges[item].v for item in graph.node_neighbors[first]
                         if (graph.edges[item].v not in visited and
                             (graph.edges[item].capacity - graph.edges[item].flow > 0))]

            directions[first] = neighbors

            remaining.extend(neighbors)

        return None

    def dfs(self, graph, from_, to, ):
        '''implementing a DFS using a while loop
                '''
        directions = OrderedDict()
        visited = []

        remaining = []
        remaining.append(from_)

        while len(remaining):

            latest = remaining.pop()

            if latest == to:
                path = self.find_path(directions, to, from_, )
                return path

            visited.append(latest)

            neighbors = [graph.edges[item].v for item in graph.node_neighbors[latest]
                         if (graph.edges[item].v not in visited and
                             (graph.edges[item].capacity - graph.edges[item].flow > 0))]

            directions[latest] = neighbors

            remaining.extend(neighbors)

        return None

    def find_path(self, directions: OrderedDict, to, from_):
        """
        after we reach the desination we are looking for, we find the related path that joins different nodes
        together so that we can reach from the starting point the ending joint"""
        direction = []
        current_to = to

        for key, value in reversed(list(directions.items())):

            if key == from_:
                direction.append(current_to)
                direction.append(key)
                break

            if current_to in value:
                direction.append(current_to)
                current_to = key

        return direction[::-1]

    def update_direction(self, graph, direction):
        '''we update the direction along the selected path.'''
        for i in range(len(direction) - 1):

            u = direction[i]
            v = direction[i + 1]

            u_edges = graph.node_neighbors[u]

            # we can use other search methods for finding the edge we are looking for
            for index in u_edges:
                if graph.edges[index].v == v:
                    graph.edges[index].flow += 1  # each edge's capacity is 1
                    graph.edges[index ^ 1].flow -= 1

                    break

    def generate_proper_format_string(self, graph):

        final_string = ''

        node_flight_index_start = graph.starting_index_flights
        node_flight_index_end = graph.starting_index_flights + graph.n_flights
        node_end_index = graph.node_end_index
        flights_indices1 = {i: None for i in range(node_flight_index_start, node_flight_index_end)}

        for index in flights_indices1.keys():
            for neighbor_index in graph.node_neighbors[index]:
                if graph.edges[neighbor_index].flow == 0 and graph.edges[neighbor_index].v != node_end_index:
                    flights_indices1[index] = graph.edges[neighbor_index].v + 1
                    break

        for key in sorted(flights_indices1.keys()):

            if flights_indices1[key] != None:
                final_string += str(flights_indices1[key]) + ' '
            else:
                final_string += str(-1) + ' '

        final_string = final_string[:-1]
        return final_string


if __name__ == '__main__':
    max_matching = MaxMatching()
    max_matching.solve()
