import numpy as np
from time import time

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def dist(p1, p2):
    return np.sqrt((p1.x - p2.x)*(p1.x - p2.x) + (p1.y - p2.y)*(p1.y - p2.y))

def min_cost_recursive(p, i=0, j=None):
    if j is None:
        j = len(p) - 1
    if j < i + 2:
        return 0
    res = np.inf
    for k in range(i+1, j):
        cost = dist(p[i], p[j]) + dist(p[j], p[k]) + dist(p[k], p[i])
        res = min(res, (min_cost_recursive(p, i, k) + min_cost_recursive(p, k, j) + cost))
    return res

def min_cost_PD(p, n=None):
    if n is None:
        n = len(p)

    if n < 3:
        return 0

    m = [[None for _ in range(n)] for _ in range(n)]

    for g in range(n):
        i = 0
        for j in range(g, n):
            if j < i + 2:
                m[i][j] = 0
            else:
                m[i][j] = np.inf
                for k in range(i + 1, j):
                    cost = dist(p[i], p[j]) + dist(p[j], p[k]) + dist(p[k], p[i])
                    temp = m[i][k] + m[k][j] + cost
                    if m[i][j] > temp:
                        m[i][j] = temp
            i += 1

    return m[0][n-1]

def str_points(data):
    s = ""
    for p in data:
        s += "(" + str(p.x) + ', ' + str(p.y) + "), "
    return s[:-2]


def main():
    data1 = [Point(0, 0), Point(1, 0), Point(2, 1), Point(1, 2), Point(0, 2)]
    data2 = [Point(0, 0), Point(4, 0), Point(5, 4), Point(4, 5), Point(2, 5), Point(1, 4), Point(0, 3), Point(0, 2)]
    print("== Rekurencja ==")
    print("Dane:", str_points(data1))
    start1 = time()
    r = min_cost_recursive(data1)
    stop1 = time()
    print("Wynik:", r)
    print("Czas wykonywania:", stop1-start1)

    print("\nDane:", str_points(data2))
    start1 = time()
    r = min_cost_recursive(data2)
    stop1 = time()
    print("Wynik:", r)
    print("Czas wykonywania:", stop1 - start1) # czas działania wersji rekurencyjnej dla więkzgo zestawu danych jest zauważalnie dłuższy

    print("\n\n== PD ==")
    print("Dane:", str_points(data1))
    start1 = time()
    r = min_cost_PD(data1)
    stop1 = time()
    print("Wynik:", r)
    print("Czas wykonywania:", stop1-start1)

    print("\nDane:", str_points(data2))
    start1 = time()
    r = min_cost_PD(data2)
    stop1 = time()
    print("Wynik:", r)
    print("Czas wykonywania:", stop1 - start1)


main()