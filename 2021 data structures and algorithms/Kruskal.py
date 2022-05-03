import graf_mst
import string


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

class ListGraph:
    def __init__(self):
        self.G = {}

    def insert_vertex(self, new_data, new_colour=None):
        new_vertex = Vertex(new_data, new_colour)
        if new_vertex not in self.G:
            self.G[new_vertex] = []

    def insert_edge(self, data_1, data_2, weight):
        start_v = Vertex(data_1)
        end_v = Vertex(data_2)
        if (end_v, weight) not in self.G[start_v]:
            self.G[start_v].append((end_v, weight)) #krotka (wierzchołek końcowy, waga)

    def delete_vertex(self, data):
        v_to_del = Vertex(data)
        for neighbours in self.G.values():
            for neighbour, weight in neighbours:
                if neighbour == v_to_del:
                    neighbours.remove((neighbour, weight))

        del self.G[v_to_del]

    def delete_edge(self, data_1, data_2):
        start_v = Vertex(data_1)
        end_v = Vertex(data_2)
        for neighbour, weight in self.G[start_v]:
            if neighbour == end_v:
                self.G[start_v].remove((neighbour, weight))
                return

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
            for neighbour , weight in neighbours:
                list_of_edges.append((vertex, neighbour, weight))
        return list_of_edges

    def edges_of_vertex(self, data):
        start = Vertex(data)
        if start in self.G:
            list_of_edges = []
            for neighbour, weight in self.G[start]:
                list_of_edges.append((start, neighbour, weight))
            return list_of_edges

    def print_edges(self, v=None):
        if v is None:
            lst = self.edges()
        else:
            lst = self.edges_of_vertex(v)
        for start, stop, weight in lst:
            print("(" + str(start) + ", " + str(stop) + ", " + str(weight) + ")", end=", ")
        print(" ")

    def __str__(self):
        s = "{\n"
        for v, neighbours in self.G.items():
            s += str(v.data) + ": ["
            for neighbour, weight in neighbours:
                s += "(" + str(neighbour) + ", " + str(weight) + "), "
            s += "]\n"
        s += "}"
        return s

    def vertexes(self):
        return self.G.keys()


class UnionFind:
    def __init__(self, n):
        self.size = [0 for i in range(n)]
        self.parent = [i for i in range(n)]

    def find(self, v):
        root = self.parent[v]
        while root != v:
            v = root
            root = self.parent[v]
        return root

    def union_sets(self, v, u):
        root_v = self.find(v)
        root_u = self.find(u)
        if self.same_component(v, u):
            return
        else:
            if self.size[root_v] >= self.size[root_u]:
                self.parent[root_u] = root_v
                self.size[root_v] = max(self.size[root_u] + 1, self.size[root_v])
            else:
                self.parent[root_v] = root_u
                self.size[root_u] = max(self.size[root_v] + 1, self.size[root_u])

    def same_component(self, v, u):
        return self.find(v) == self.find(u)


def MST_Kruskal(G: ListGraph):
    def myFunc(e):
        start, stop, weight = e
        return weight

    edges = G.edges()
    edges.sort(key=myFunc)

    def idx(v):
        return string.ascii_uppercase.index(v.data)

    MST = ListGraph()
    num_of_v = G.order()
    uf = UnionFind(num_of_v)

    for v in G.vertexes():
        MST.insert_vertex(v.data, v.colour)

    cnt = 0
    suma = 0
    while cnt < num_of_v - 1:
        start, stop, weight = edges.pop(0)
        idx1 = idx(start)
        idx2 = idx(stop)
        if not uf.same_component(idx1, idx2):
            cnt += 1
            MST.insert_edge(start.data, stop.data, weight)
            MST.insert_edge(stop.data, start.data, weight)
            uf.union_sets(idx1, idx2)
            suma += weight

    return MST, suma


def main_mst():
    G = ListGraph()
    for start, stop, weight in graf_mst.graf:
        G.insert_vertex(start)
        G.insert_vertex(stop)
        G.insert_edge(start, stop, weight)
        G.insert_edge(stop, start, weight)
    print(G)

    mst, suma = MST_Kruskal(G)
    print("\nKrawędzie w MST:")
    print(mst)
    print("suma:", suma)


main_mst()