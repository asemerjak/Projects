import graf_mst
import numpy as np
import cv2
import matplotlib.pyplot as plt


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


def MST_Prim(G: ListGraph):
    MST = ListGraph()
    intree = {}
    distance = {}
    parent = {}

    for v in G.vertexes():
        MST.insert_vertex(v.data, v.colour)
        intree[v] = False
        distance[v] = np.inf
        parent[v] = -1
    suma = 0
    v = G.get_vertex(1)
    while not intree[v]:
        intree[v] = True
        for start, stop, weight in G.edges_of_vertex(v.data):
            if weight < distance[stop] and not intree[stop]:
                parent[stop] = start
                distance[stop] = weight

        min_val = np.inf
        umin = None
        for key, value in distance.items():
            if value < min_val and not intree[key]:
                min_val = value
                umin = key
        if umin is None:
            break
        v = umin
        MST.insert_edge(parent[v].data, v.data, distance[v])
        MST.insert_edge(v.data, parent[v].data, distance[v])
        suma += distance[v]

    return MST, suma


def colouring(G: ListGraph, start, stop):
    visited = {}
    for v in G.vertexes():
        visited[v] = False

    for s in [start, stop]:
        queue = [s]
        visited[s] = True
        if s == start:
            colour = 100
        else:
            colour = 200

        while queue:
            s = queue.pop(0)
            for v in G.neighbours(s.data):
                if v in visited.keys():
                    if not visited[v]:
                        queue.append(v)
                        visited[v] = True
                        v.colour = colour
    return G


def segmentation():
    I = cv2.imread('sample.png', cv2.IMREAD_GRAYSCALE)
    plt.imshow(I, cmap='gray', vmin=0, vmax=255)
    plt.xlabel([]), plt.ylabel([])
    plt.title("Obraz oryginalny")
    plt.show()

    X, Y = I.shape
    G = ListGraph()
    for i in range(0, X):
        for j in range(0, Y):
            G.insert_vertex(new_data=X*j + i, new_colour=I[i, j])

    for i in range(1, X-1):
        for j in range(1, Y-1):
            neighbours = [[j - 1, i], [j - 1, i - 1], [j, i - 1], [j + 1, i], [j + 1, i + 1], [j, i + 1], [j - 1, i + 1],
                          [j + 1, i - 1]]
            for n in neighbours:
                G.insert_edge(data_1=X*j + i, data_2=X*n[1] + n[0], weight=abs(I[i][j] - I[n[0], n[1]]))
                G.insert_edge(data_1=X * n[1] + n[0], data_2=X * j + i, weight=abs(I[i][j] - I[n[0], n[1]]))

    MST, sum_mst = MST_Prim(G)
    mst_edges = MST.edges()

    def myFunc(e):
        start, stop, weight = e
        return weight

    mst_edges.sort(key=myFunc)

    start, stop, weight = mst_edges[-1]
    MST.delete_edge(start.data, stop.data)
    MST.delete_edge(stop.data, start.data)

    MST = colouring(MST, start, stop)

    IS = np.zeros((X, Y), dtype='uint8')
    for i in range(1, X):
        for j in range(1, Y):
            for v in MST.vertexes():
                if v.data == X*j + i:
                    IS[i, j] = v.colour

    plt.imshow(IS, cmap='gray', vmin=0, vmax=256)
    plt.xlabel([]), plt.ylabel([])
    plt.title("Obraz po segmentacji")
    plt.show()


def main_mst():
    G = ListGraph()
    for start, stop, weight in graf_mst.graf:
        G.insert_vertex(start)
        G.insert_vertex(stop)
        G.insert_edge(start, stop, weight)
        G.insert_edge(stop, start, weight)
    print(G)

    mst, suma = MST_Prim(G)
    print("\nKrawędzie w MST:")
    print(mst)
    print("suma:", suma)


main_mst()
segmentation()
