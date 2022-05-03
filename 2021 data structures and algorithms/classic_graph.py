import polska


class MatrixGraph:
    def __init__(self):
        self.G = [[None]] #pierwsza kolumna i pierwszy wiersz grafu to dane wierzchołków

    def insert_vertex(self, data):
        if data not in self.G[0]:
            self.G[0].append(data)
            self.G.append([data] + [0 for _ in range(len(self.G))])
            for i in range(1, len(self.G)-1):
                self.G[i].append(0)

    def insert_edge(self, data_1, data_2):
        index_1 = self.get_vertex_idx(data_1)
        index_2 = self.get_vertex_idx(data_2)
        self.G[index_1][index_2] = 1

    def delete_vertex(self, data):
        idx = self.get_vertex_idx(data)
        for i in range(len(self.G)):
            self.G[i].pop(idx)
        self.G.pop(idx)

    def delete_edge(self, data_1, data_2):
        index_1 = self.get_vertex_idx(data_1)
        index_2 = self.get_vertex_idx(data_2)
        self.G[index_1][index_2] = 0

    def get_vertex_idx(self, data):
        for idx in range(1, len(self.G[0])):
            if self.G[0][idx] == data:
                return idx

    def get_vertex(self, idx):
        return self.G[0][idx]

    def neighbours(self, data):
        list_of_neigh = []
        idx = self.get_vertex_idx(data)
        for i in range(1, len(self.G)):
            if self.G[idx][i] == 1:
                list_of_neigh.append(self.G[0][i])
        return list_of_neigh

    def order(self):
        return len(self.G) - 1

    def size(self):
        size = 0
        for i in range(1, len(self.G)):
            for j in range(1, len(self.G)):
                if self.G[i][j] == 1:
                    size += 1

    def edges(self):
        list_of_edges = []
        for i in range(1, len(self.G)):
            for j in range(1, len(self.G)):
                if self.G[i][j] == 1:
                    list_of_edges.append((self.G[0][i], self.G[0][j]))
        return list_of_edges


class ListGraph:
    def __init__(self):
        self.G = {}

    def insert_vertex(self, data):
        if data not in self.G:
            self.G[data] = []

    def insert_edge(self, data_1, data_2):
        self.G[data_1].append(data_2)

    def delete_vertex(self, data):
        for val in self.G.values():
            for elem in val:
                if elem == data:
                    val.remove(data)
        del self.G[data]

    def delete_edge(self, data_1, data_2):
        self.G[data_1].remove(data_2)

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
        return self.G[data]

    def order(self):
        return len(self.G)

    def size(self):
        return len(self.edges())

    def edges(self):
        list_of_edges = []
        for vertex, neighbours in self.G.items():
            for neighbour in neighbours:
                list_of_edges.append((vertex, neighbour))
        return list_of_edges


def coloring(G, traversal_way):
    visited = {G.get_vertex(i): False for i in range(1, G.order()+1)}
    forbidden_colors = {G.get_vertex(i): [] for i in range(1, G.order()+1)}
    colors = {G.get_vertex(i): [] for i in range(1, G.order()+1)}
    s = G.get_vertex(1)
    if traversal_way == 'BFS':
        queue = []
        queue.append(s)
        visited[s] = True
        while queue:
            s = queue.pop(0)

            color = 0
            while color in forbidden_colors[s]:
                color += 1
            colors[s] = color

            for v in G.neighbours(s):
                forbidden_colors[v].append(color)
                if not visited[v]:
                    queue.append(v)
                    visited[v] = True

    elif traversal_way == 'DFS':
        stack = []
        stack.append(s)
        while stack:
            s = stack.pop()
            if not visited[s]:

                color = 0
                while color in forbidden_colors[s]:
                    color += 1
                colors[s] = color

                visited[s] = True

            for v in G.neighbours(s):
                forbidden_colors[v].append(color)
                if not visited[v]:
                    stack.append(v)

    return colors


def dict_to_list(dict):
    return [(vertex, color) for vertex, color in dict.items()]


def main():
    G1 = MatrixGraph()
    G2 = ListGraph()
    graphs = [G1, G2]
    for G in graphs:
        for start, stop in polska.graf:
            G.insert_vertex(start)
            G.insert_vertex(stop)
            G.insert_edge(start, stop)
        G.delete_vertex('K')
        G.delete_edge('W', 'E')
        G.delete_edge('E', 'W')
        polska.draw_map(G.edges())


def main2():
    G1 = MatrixGraph()
    G2 = ListGraph()
    graphs = [G1, G2]
    for G in graphs:
        for start, stop in polska.graf:
            G.insert_vertex(start)
            G.insert_vertex(stop)
            G.insert_edge(start, stop)
        colors_DFS = coloring(G, 'DFS')
        colors_DFS = dict_to_list(colors_DFS)  # DFS potrzebuje 5 kolorów, gdzie BFS jedynie 4
        colors_BFS = coloring(G, 'BFS')
        colors_BFS = dict_to_list(colors_BFS)
        polska.draw_map(G.edges(), colors_DFS)
        polska.draw_map(G.edges(), colors_BFS)


main()
main2()


