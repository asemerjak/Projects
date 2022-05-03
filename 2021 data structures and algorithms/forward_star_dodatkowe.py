import polska


class ForwardAndReverseStar:
    def __init__(self):
        self._vertexes = []
        self._edges = []

    def insert_vertex(self, data):
        already_exists = False
        for i in range(len(self._vertexes)):
            if self._vertexes[i][0] == data:
                already_exists = True
                break
        if not already_exists:
            self._vertexes.append([data, None])

    def insert_edge(self, data_1, data_2):
        self._edges.append([data_1, data_2])
        self.sort_edges()
        self.update_vertexes()

    def get_vertex_idx(self, data):
        for i in range(len(self._vertexes)):
            if self._vertexes[i][0] == data:
                return i

    def sort_edges(self):
        def idx(e):
            return self.get_vertex_idx(e[0])
        self._edges.sort(key=idx)

    def update_vertexes(self):
        for i in range(len(self._vertexes)):
            vertex = self._vertexes[i][0]
            for j in range(len(self._edges)):
                if self._edges[j][0] == vertex:
                    self._vertexes[i][1] = j
                    break
                if j == len(self._edges) - 1:
                    self._vertexes[i][1] = None

    def delete_vertex(self, data):
        idx = self.get_vertex_idx(data)
        self._vertexes.pop(idx)
        indexes_to_del = []
        for i in range(len(self._edges)):
            if self._edges[i][0] == data or self._edges[i][1] == data:
                indexes_to_del.append(i)
        for i in sorted(indexes_to_del, reverse=True):
            self._edges.pop(i)
        self.update_vertexes()

    def delete_edge(self, data_1, data_2):
        for i in range(len(self._edges)):
            if self._edges[i][0] == data_1 and self._edges[i][1] == data_2:
                self._edges.pop(i)
                break
        self.update_vertexes()

    def get_vertex(self, idx):
        return self._vertexes[idx][0]

    def neighbours(self, data):
        neighbours = []
        next_vertex = False
        for i in range(len(self._edges)):
            if self._edges[i][0] == data:
                neighbours.append(self._edges[i][1])
                next_vertex = True
            elif next_vertex:
                break

        return neighbours

    def order(self):
        return len(self._vertexes)

    def size(self):
        return len(self._edges)

    def edges(self):
        return [(edge[0], edge[1]) for edge in self._edges]

def main():
    G = ForwardAndReverseStar()
    for start, stop in polska.graf:
        G.insert_vertex(start)
        G.insert_vertex(stop)
        G.insert_edge(start, stop)
    G.delete_vertex('K')
    G.delete_edge('W', 'E')
    G.delete_edge('E', 'W')
    polska.draw_map(G.edges())

main()





