import numpy as np


class Vertex:
    def __init__(self, data, colour=None):
        self.data = data
        self.colour = colour

    def __eq__(self, other):
        return self.data == other.data

    def __str__(self):
        return str(self.data)

    def __hash__(self):
        return hash(self.data)


class Edge:
    def __init__(self, start: Vertex, stop: Vertex, weight: int = 1):
        self.start = start
        self.stop = stop
        self.weight = weight

    def __eq__(self, other):
        return self.start == other.start and self.stop == other.stop and self.weight == other.weight

    def __hash__(self):
        return hash((self.start, self.stop, self.weight))

    def __str__(self):
        s = "(" + str(self.start) + " -> " + str(self.stop) + ", " + str(self.weight)


class ListGraph:
    def __init__(self):
        self.G = {}

    def insert_vertex(self, new_data, new_colour=None):
        new_vertex = Vertex(new_data, new_colour)
        if new_vertex not in self.G.keys():
            self.G[new_vertex] = []

    def insert_edge(self, data_1, data_2, weight):
        start_v = Vertex(data_1)
        end_v = Vertex(data_2)
        edge = Edge(start_v, end_v, weight)
        self.G[start_v].append(edge)

    def delete_vertex(self, data):
        v_to_del = Vertex(data)
        for neighbours in self.G.values():
            for edge in neighbours:
                if edge.stop == v_to_del:
                    neighbours.remove(edge)

        del self.G[v_to_del]

    def delete_edge(self, data_1, data_2, weight=1):
        start_v = Vertex(data_1)
        end_v = Vertex(data_2)
        edge_to_del = Edge(start_v, end_v, weight)
        self.G[start_v].remove(edge_to_del)

    def get_vertex_idx(self, data):
        num = 1
        for key in self.G.keys():
            if key == data:
                return num
            num += 1

    def get_vertex(self, idx):
        num = 1
        for key in self.G.keys():
            if idx == num:
                return key
            num += 1

    def neighbours(self, data):
        return self.G[Vertex(data)]

    def order(self):
        return len(self.G)

    def size(self):
        return len(self.edges())

    def edges(self):
        list_of_edges = []
        for vertex, neighbours in self.G.items():
            for edge in neighbours:
                list_of_edges.append(edge)
        return list_of_edges

    def edges_from_vertex(self, start):
        if start in self.G:
            list_of_edges = []
            for edge in self.G[start]:
                list_of_edges.append(edge)
            return list_of_edges

    def print_edges(self, v=None):
        if v is None:
            lst = self.edges()
        else:
            lst = self.edges_from_vertex(v)
        for edge in lst:
            print(edge, end=", ")
        print(" ")

    def __str__(self):
        s = "{\n"
        for v, neighbours in self.G.items():
            s += str(v.data) + ": ["
            for edge in neighbours:
                s += "(" + str(edge.stop) + ", " + str(edge.weight) + "), "
            s += "]\n"
        s += "}"
        return s

    def vertexes(self):
        return self.G.keys()

    def BFS(self, start, stop):
        visited = {v: False for v in self.vertexes()}
        parent = {v: None for v in self.vertexes()}
        s = start
        queue = [s]
        visited[s] = True
        while queue:
            s = queue.pop(0)
            for edge in self.edges_from_vertex(s):
                v = edge.stop
                if not visited[v] and edge.weight > 0:
                    if v == stop:
                        parent[v] = s
                        return True, parent
                    queue.append(v)
                    visited[v] = True
                    parent[v] = s
        return False, parent

    def edges_to_vertex(self, v: Vertex):
        list_of_edges = []
        for vertex, neighbours in self.G.items():
            for edge in neighbours:
                if edge.stop == v:
                    list_of_edges.append(edge)
        return list_of_edges

    def edge(self, start, stop):

        if start in self.G.keys():
            for edge in self.G[start]:
                if edge.stop == stop:
                    return edge

    def path_analyze(self, start: Vertex, stop: Vertex, parent):
        s = stop
        min_cap = np.inf
        if parent[s] is None:
            return 0

        while s != start:
            edge = self.edge(parent[s], s)
            if edge and edge.weight < min_cap:
                min_cap = edge.weight
            s = parent[s]
        return min_cap

    def aug(self, start: Vertex, stop: Vertex, parent, min_cap):
        s = stop
        if parent[s] is None:
            return 0

        while s != start:

            if self.edge(parent[s], s):
                self.edge(parent[s], s).weight -= min_cap
            if self.edge(s, parent[s]):
                self.edge(s, parent[s]).weight += min_cap
            s = parent[s]
        return min_cap

    def Ford_Fulkerson(self, start=Vertex('s'), stop=Vertex('t')):
        flow = 0
        is_path, parent = self.BFS(start, stop)
        while is_path:
            min_cap = self.path_analyze(start, stop, parent)
            self.aug(start, stop, parent, min_cap)
            flow += min_cap
            is_path, parent = self.BFS(start, stop)

        return flow


def main():
    graf_0 = [('s', 'u', 2), ('u', 't', 1), ('u', 'v', 3), ('s', 'v', 1), ('v', 't', 2)]

    G = ListGraph()
    for start, stop, weight in graf_0:
        G.insert_vertex(start)
        G.insert_vertex(stop)
        G.insert_edge(start, stop, weight)
    print("graf_0:", G.Ford_Fulkerson())


def main2():
    graf_1 = [('s', 'a', 16), ('s', 'c', 13), ('a', 'c', 10), ('c', 'a', 4), ('a', 'b', 12), ('b', 'c', 9),
              ('b', 't', 20), ('c', 'd', 14), ('d', 'b', 7), ('d', 't', 4)]
    G = ListGraph()
    for start, stop, weight in graf_1:
        G.insert_vertex(start)
        G.insert_vertex(stop)
        G.insert_edge(start, stop, weight)
    print("graf_1:", G.Ford_Fulkerson())


def main3():
    graf_2 = [ ('s', 'a', 3), ('s', 'c', 3), ('a', 'b', 4), ('b', 's', 3), ('b', 'c', 1), ('b', 'd', 2), ('c', 'e', 6), ('c', 'd', 2), ('d', 't', 1), ('e', 't', 9)]
    G = ListGraph()
    for start, stop, weight in graf_2:
        G.insert_vertex(start)
        G.insert_vertex(stop)
        G.insert_edge(start, stop, weight)
    print("graf_2:", G.Ford_Fulkerson())


def main4():
    graf_3 = [('s', 'a', 8), ('s', 'd', 3), ('a', 'b', 9), ('b', 'd', 7), ('b', 't', 2), ('c', 't', 5), ('d', 'b', 7),
              ('d', 'c', 4)]

    G = ListGraph()
    for start, stop, weight in graf_3:
        G.insert_vertex(start)
        G.insert_vertex(stop)
        G.insert_edge(start, stop, weight)
    print("graf_3:", G.Ford_Fulkerson())

main()
main2()
main3()
main4()



