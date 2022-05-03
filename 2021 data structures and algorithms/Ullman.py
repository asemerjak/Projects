import numpy as np

class MatrixGraph:
    def __init__(self):
        self.G = [[None]] #pierwsza kolumna i pierwszy wiersz grafu to dane wierzchołków

    def get_matrix(self):
        matrix = [[self.G[r][c] for r in range(1, len(self.G))] for c in range(1, len(self.G[0]))]
        return np.array(matrix)

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


def is_isomorph(G, P, M):
    for i in range(M.shape[0]):
        if np.sum(M[i]) != 1:
            return False

    for c in range(M.shape[1]):
        summ = 0
        for r in range(M.shape[0]):
            summ += M[r, c]
        if summ > 1:
            return False

    G_mat = G.get_matrix()
    P_mat = P.get_matrix()

    if (M @ (M @ G_mat).T == P_mat).all():
        return True
    return False


def Ullman_1_0_helper(used_cols, curr_r, G, P, M, recur_counter, found_iso=[False]):
    recur_counter[0] += 1
    if curr_r == M.shape[0]:
        if is_isomorph(G, P, M):
            found_iso[0] = True
            print("\nMacierz M\n", M)
            return True, M, recur_counter
        else:
            return False, M, recur_counter

    M_copy = M.copy()
    cols = [i for i in range(M.shape[1])]

    for col in used_cols:
        if col in cols:
            cols.remove(col)

    if cols:
        for col in cols:
            used_cols.append(col)
            M_copy[curr_r] = [0 for _ in M_copy[curr_r]]
            M_copy[curr_r][col] = 1
            if not found_iso[0]:
                Ullman_1_0_helper(used_cols, curr_r + 1, G, P, M_copy, recur_counter)
            else:
                return True, M, recur_counter
            used_cols.remove(col)
    else:
        M_copy[curr_r] = [0 for _ in M_copy[curr_r]]
        if not found_iso[0]:
            Ullman_1_0_helper(used_cols, curr_r + 1, G, P, M_copy, recur_counter)
        else:
            return True, M, recur_counter


def Ullman_2_0_helper(used_cols, curr_r, G, P, M, recur_counter, found_iso=[False]):
    recur_counter[0] += 1
    if curr_r == M.shape[0]:
        if is_isomorph(G, P, M):
            found_iso[0] = True
            print("\nMacierz M\n", M)
            return True, M, recur_counter
        else:
            return False, M, recur_counter

    M_copy = M.copy()
    cols = [i for i in range(M.shape[1])]

    for col in used_cols:
        if col in cols:
            cols.remove(col)

    changed = True
    if cols:
        for col in cols:
            if M[curr_r][col] == 1:
                used_cols.append(col)
                M_copy[curr_r] = [0 for _ in M_copy[curr_r]]
                M_copy[curr_r][col] = 1
                if not found_iso[0]:
                    Ullman_2_0_helper(used_cols, curr_r + 1, G, P, M_copy, recur_counter, found_iso)
                else:
                    return True, M, recur_counter
                used_cols.remove(col)
                changed = True
            else:
                changed = False

    if not cols or not changed:
        M_copy[curr_r] = [0 for _ in M_copy[curr_r]]
        if not found_iso[0]:
            Ullman_2_0_helper(used_cols, curr_r + 1, G, P, M_copy, recur_counter, found_iso)
        else:
            return True, M, recur_counter


def prune(G, P, M):
    changed = True
    while changed:
        changed = False
        for r in range(M.shape[0]):
            for c in range(M.shape[1]):
                if M[r, c] == 1:
                    n = True
                    for i in range(M.shape[0]):
                        if P.get_matrix()[r][i] == 1:
                            for j in range(M.shape[1]):
                                if G.get_matrix()[c, j] == 1 and M[i, j] == 1:
                                    n = False
                    if n:
                        M[r, c] = 0
                        changed = True
    return M


def Ullman_3_0_helper(used_cols, curr_r, G, P, M, recur_counter, found_iso=[False]):
    recur_counter[0] += 1
    if curr_r == M.shape[0]:
        if is_isomorph(G, P, M):
            found_iso[0] = True
            print("\nMacierz M\n", M)
            return True, M, recur_counter
        else:
            return False, M, recur_counter

    M = prune(G, P, M)
    M_copy = M.copy()
    cols = [i for i in range(M.shape[1])]

    for col in used_cols:
        if col in cols:
            cols.remove(col)

    changed = True
    if cols:
        for col in cols:
            if M[curr_r][col] == 1:
                used_cols.append(col)
                M_copy[curr_r] = [0 for _ in M_copy[curr_r, :]]
                M_copy[curr_r, col] = 1
                if not found_iso[0]:
                    Ullman_3_0_helper(used_cols, curr_r + 1, G, P, M_copy, recur_counter, found_iso)
                else:
                    return True, M_copy, recur_counter
                used_cols.remove(col)
                changed = True
            else:
                changed = False

    if cols == [] or not changed:
        M_copy[curr_r] = [0 for _ in M_copy[curr_r]]
        if not found_iso[0]:
            Ullman_3_0_helper(used_cols, curr_r + 1, G, P, M_copy, recur_counter, found_iso)
        else:
            return True, M_copy, recur_counter


def Ullman_2_0(G, P):
    M = [[] for _ in range(P.order())]
    for r in range(P.order()):
        for c in range(G.order()):
            M[r].append(0)
    for r in range(len(M)):
        for c in range(len(M[r])):
            if np.sum(P.get_matrix()[r]) <= np.sum(G.get_matrix()[c]):
                M[r][c] = 1

    recur_counter = [1]
    print("===== Ullman 2.0 =====")
    print("Macierz G\n", G.get_matrix())
    print("\nMacierz P\n", P.get_matrix())
    is_isomorph_, M_new, cnt = Ullman_2_0_helper([], 0, G, P, np.array(M), recur_counter=recur_counter)
    print("\nCzy grafy są izomorficzne?", is_isomorph_)
    print("\nLiczba rekurencji:", cnt[0], "\n\n")


def Ullman_1_0(G, P):
    M = [[] for _ in range(P.order())]
    for r in range(P.order()):
        for c in range(G.order()):
            M[r].append(1)
    recur_counter = [1]
    print("\n===== Ullman 1.0 =====")
    print("Macierz G\n", G.get_matrix())
    print("\nMacierz P\n", P.get_matrix())
    is_isomorph_, M_new, cnt = Ullman_1_0_helper([], 0, G, P, np.array(M), recur_counter=recur_counter)
    print("\nCzy grafy są izomorficzne?", is_isomorph_)
    print("\nLiczba rekurencji:", cnt[0], "\n\n")


def Ullman_3_0(G, P):
    M = [[] for _ in range(P.order())]
    for r in range(P.order()):
        for c in range(G.order()):
            M[r].append(0)
    for r in range(len(M)):
        for c in range(len(M[r])):
            if np.sum(P.get_matrix()[r]) <= np.sum(G.get_matrix()[c]):
                M[r][c] = 1

    recur_counter = [0]
    print("===== Ullman 3.0 =====")
    print("Macierz G\n", G.get_matrix())
    print("\nMacierz P\n", P.get_matrix())
    is_isomorph_, M_new, cnt = Ullman_3_0_helper([], 0, G, P, np.array(M), recur_counter=recur_counter)
    print("\nCzy grafy są izomorficzne?", is_isomorph_)
    print("\nLiczba rekurencji:", cnt[0], "\n\n")

def main():
    data_G = [('A', 'B', 1), ('B', 'F', 1), ('B', 'C', 1), ('C', 'D', 1), ('C', 'E', 1), ('D', 'E', 1)]
    data_P = [('A', 'B', 1), ('B', 'C', 1), ('A', 'C', 1)]

    G = MatrixGraph()
    P = MatrixGraph()

    for start, stop, weight in data_G:
        G.insert_vertex(start)
        G.insert_vertex(stop)
        G.insert_edge(start, stop)
        G.insert_edge(stop, start)

    for start, stop, weight in data_P:
        P.insert_vertex(start)
        P.insert_vertex(stop)
        P.insert_edge(start, stop)
        P.insert_edge(stop, start)

    Ullman_1_0(G, P)
    Ullman_2_0(G, P)
    Ullman_3_0(G, P)

main()








