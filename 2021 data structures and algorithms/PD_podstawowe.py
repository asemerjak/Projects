import time
import numpy as np


def Fibonacci_recursive(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return Fibonacci_recursive(n - 1) + Fibonacci_recursive(n - 2)

def Fibonacci_cache(n):
    tab = [None for _ in range(n+1)]
    tab[0] = 0
    tab[1] = 1
    def fib_inside(n):
        if tab[n] is None:
            tab[n] = fib_inside(n - 1) + fib_inside(n - 2)
        return tab[n]

    return fib_inside(40)

def Fibonacci_PD(n):
    tab = [None for _ in range(n + 1)]
    tab[0] = 0
    tab[1] = 1

    for i in range(2, n + 1):
        tab[i] = tab[i - 1] + tab[i - 2]

    return tab[n]

def Fibonacci_PD_2_0(n):
    tab = [None for _ in range(3)]
    tab[0] = 0
    tab[1] = 1

    for i in range(2, n):
        tab[2] = tab[1] + tab[0]
        tab[0], tab[1] = tab[1], tab[2]

    return tab[1] + tab[0]

def match(c, d):
    if c == d:
        return 0
    else:
        return 1

def indel(c):
    return 1

def recursive_compare(s, t, i, j):
    MATCH = 0
    INSERT = 1
    DELETE = 2

    opt = [None for _ in range(3)]

    if i == 0:
        return j * indel(' ')
    if j == 0:
        return i * indel(' ')

    opt[MATCH] = recursive_compare(s, t, i - 1, j - 1) + match(s[i], t[j])
    opt[INSERT] = recursive_compare(s, t, i, j - 1) + indel(t[j])
    opt[DELETE] = recursive_compare(s, t, i - 1, j) + indel(s[i])

    lowest_cost = opt[MATCH]

    for k in range(INSERT, DELETE + 1):
        if opt[k] < lowest_cost:
            lowest_cost = opt[k]

    return lowest_cost

# ======= b) wariant PD =======
class Cell:
    cost = 0
    parent = -1

def PD_compare(s, t, return_m=False):
    MATCH = 0
    INSERT = 1
    DELETE = 2
    MAXLEN = 20
    m = np.array([[Cell() for x in range(MAXLEN + 1)] for y in range(MAXLEN + 1)])

    def row_init(i):
        m[0][i].cost = i
        if i > 0:
            m[0][i].parent = INSERT
        else:
            m[0][i].parent = -1

    def column_init(i):
        m[i][0].cost = i
        if i > 0:
            m[i][0].parent = DELETE
        else:
            m[i][0].parent = -1

    def goal_cell(s, t):
        i = len(s) - 1
        j = len(t) - 1
        return i, j

    for i in range(0, MAXLEN):
        row_init(i)
        column_init(i)

    opt = [None for _ in range(3)]

    for i in range(1, len(s)):
        for j in range(1, len(t)):
            opt[MATCH] = m[i - 1][j - 1].cost + match(s[i], t[j])
            opt[INSERT] = m[i][j - 1].cost + indel(t[j])
            opt[DELETE] = m[i - 1][j].cost + indel(s[i])

            m[i][j].cost = opt[MATCH]
            m[i][j].parent = MATCH

            for k in range(INSERT, DELETE + 1):
                if opt[k] < m[i][j].cost:
                    m[i][j].cost = opt[k]
                    m[i][j].parent = k

    i, j = goal_cell(s, t)
    if return_m:
        return m, m[i][j].cost

    return m[i][j].cost

# ======= c) odtwarzanie ścieżki =======
def match_out(s, t, i, j):
    if s[i] == t[j]:
        print('M', end='')
    else:
        print('S', end='')

def insert_out(t, j):
    print("I", end='')

def delete_out(s, i):
    print("D", end='')

def reconstruct_path(m, s, t, i, j, result=None):
    MATCH = 0
    INSERT = 1
    DELETE = 2

    if m[i][j].parent == -1:
        return result

    if m[i][j].parent == MATCH:
        reconstruct_path(m, s, t, i - 1, j - 1, result)
        match_out(s, t, i, j)
        if result is not None:
            result[0] += s[i]
        return

    if m[i][j].parent == INSERT:
        reconstruct_path(m, s, t, i, j - 1, result)
        insert_out(t, j)
        return

    if m[i][j].parent == DELETE:
        reconstruct_path(m, s, t, i - 1, j, result)
        delete_out(s, i)
        return

# ======= d) dopasowanie podciągów =======
def PD_compare2(s, t, return_m=False):
    MATCH = 0
    INSERT = 1
    DELETE = 2
    MAXLEN = 20
    m = np.array([[Cell() for x in range(MAXLEN + 1)] for y in range(MAXLEN + 1)])

    opt = [None for _ in range(3)]

    def row_init2(i):
        m[0][i].cost = 0
        m[0][i].parent = -1

    def goal_cell2(s, t):
        i = len(s) - 1
        j = 0
        for k in range(1, len(t)):
            if m[i][k].cost < m[i][j].cost:
                j = k
        return i, j

    def column_init(i):
        m[i][0].cost = i
        if i > 0:
            m[i][0].parent = DELETE
        else:
            m[i][0].parent = -1

    for i in range(MAXLEN):
        row_init2(i)
        column_init(i)

    for i in range(1, len(s)):
        for j in range(1, len(t)):
            opt[MATCH] = m[i - 1][j - 1].cost + match(s[i], t[j])
            opt[INSERT] = m[i][j - 1].cost + indel(t[j])
            opt[DELETE] = m[i - 1][j].cost + indel(s[i])

            m[i][j].cost = opt[MATCH]
            m[i][j].parent = MATCH

            for k in range(INSERT, DELETE + 1):
                if opt[k] < m[i][j].cost:
                    m[i][j].cost = opt[k]
                    m[i][j].parent = k

    i, j = goal_cell2(s, t)
    if return_m:
        return m, m[i][j].cost
    return m[i][j].cost

# ======= e) najdłuższy wspólny podciąg =======
def PD_compare3(s, t, return_m=False):
    MATCH = 0
    INSERT = 1
    DELETE = 2
    MAXLEN = 20
    m = np.array([[Cell() for x in range(MAXLEN + 1)] for y in range(MAXLEN + 1)])

    def match2(c, d):
        if c == d:
            return 0
        else:
            return MAXLEN

    def row_init(i):
        m[0][i].cost = i
        if i > 0:
            m[0][i].parent = INSERT
        else:
            m[0][i].parent = -1

    def column_init(i):
        m[i][0].cost = i
        if i > 0:
            m[i][0].parent = DELETE
        else:
            m[i][0].parent = -1

    def goal_cell(s, t):
        i = len(s) - 1
        j = len(t) - 1
        return i, j

    for i in range(0, MAXLEN):
        row_init(i)
        column_init(i)

    opt = [None for _ in range(3)]

    for i in range(1, len(s)):
        for j in range(1, len(t)):
            opt[MATCH] = m[i - 1][j - 1].cost + match2(s[i], t[j])
            opt[INSERT] = m[i][j - 1].cost + indel(t[j])
            opt[DELETE] = m[i - 1][j].cost + indel(s[i])

            m[i][j].cost = opt[MATCH]
            m[i][j].parent = MATCH

            for k in range(INSERT, DELETE + 1):
                if opt[k] < m[i][j].cost:
                    m[i][j].cost = opt[k]
                    m[i][j].parent = k

    i, j = goal_cell(s, t)
    if return_m:
        return m, m[i][j].cost

    return m[i][j].cost

def main1():
    start = time.time()
    recur = Fibonacci_recursive(40)
    stop = time.time()
    t = stop - start
    print("\n== Fibbonaci rekurencyjnie ==")
    print("40 liczba ciągu Fibbonaciego:", recur)
    print("Czas wykonywania:", t)

def main2():
    start = time.time()
    cache = Fibonacci_cache(40)
    stop = time.time()
    t = stop - start
    print("\n== Fibbonaci z pamięcią podręczną ==")
    print("40 liczba ciągu Fibbonaciego:", cache)
    print("Czas wykonywania:", t)

def main3():
    start = time.time()
    PD = Fibonacci_PD(40)
    stop = time.time()
    t = stop - start
    print("\n== Fibbonaci z PD ==")
    print("40 liczba ciągu Fibbonaciego:", PD)
    print("Czas wykonywania:", t)

def main4():
    start = time.time()
    PD2 = Fibonacci_PD_2_0(40)
    stop = time.time()
    t = stop - start
    print("\n== Fibbonaci z PD 2.0 ==")
    print("40 liczba ciągu Fibbonaciego:", PD2)
    print("Czas wykonywania:", t)

def main5():
    s1 = ' kot'
    t1 = ' kon'
    s2 = ' kot'
    t2 = ' pies'
    start1 = time.time()
    res1 = recursive_compare(s1, t1, len(s1) - 1, len(t1) - 1)
    stop1 = time.time()
    t_1 = stop1 - start1
    print("\n== Dopasowanie rekurencyjnie ==")
    print("wyrazy:", s1, t1)
    print("wynik:", res1)
    print("czas wykonywania:", t_1)

    start2 = time.time()
    res2 = recursive_compare(s2, t2, len(s2) - 1, len(t2) - 1)
    stop2 = time.time()
    t_2 = stop2 - start2

    print("\nwyrazy:", s2, t2)
    print("wynik:", res2)
    print("czas wykonywania:", t_2)

def main6():
    s1 = ' kot'
    t1 = ' kon'
    s2 = ' kot'
    t2 = ' pies'
    start1 = time.time()
    res1 = PD_compare(s1, t1)
    stop1 = time.time()
    t_1 = stop1 - start1
    print("\n== Dopasowanie PD ==")
    print("wyrazy:", s1, t1)
    print("wynik:", res1)
    print("czas wykonywania:", t_1)
    start2 = time.time()
    res2 = PD_compare(s2, t2)
    stop2 = time.time()
    t_2 = stop2 - start2
    print("\nwyrazy:", s2, t2)
    print("wynik:", res2)
    print("czas wykonywania:", t_2)

def main7():
    S = ' thou shalt not'
    T = ' you should not'

    print("\n== Rekonstrukcja ścieżki ==")
    print("Analizowane ciągi: -", S, "- oraz -", T)
    start = time.time()
    m, result = PD_compare(S, T, return_m=True)
    print("wynik:", result)
    print("Odtworzona ścieżka: ", end='')
    reconstruct_path(m, S, T, len(S) - 1, len(T) - 1)
    stop = time.time()
    t_1 = stop - start
    print("Czas wykonywania:", t_1)

def main8():
    T = ' ban'
    S = ' mokeyssbanana'

    print("\n== Dopasowanie podciągu ==")
    print("Analizowane ciągi: -", S, "- oraz -", T)
    start = time.time()
    m, result = PD_compare2(S, T, return_m=True)
    print("wynik:", result)
    print("Odtworzona ścieżka: ", end='')
    reconstruct_path(m, S, T, len(S) - 1, len(T) - 1)
    stop = time.time()
    t_1 = stop - start
    print("Czas wykonywania:", t_1)

def main9():
    S = ' democrat'
    T = ' republican'

    print("\n== Najdłuższy wspólny podciąg ==")
    print("Analizowane ciągi: -", S, "- oraz -", T)
    start = time.time()
    m, result = PD_compare3(S, T, return_m=True)
    print("wynik:", result)
    print("Odtworzona ścieżka: ", end='')
    r = ['']
    reconstruct_path(m, S, T, len(S) - 1, len(T) - 1, r)
    print("\nodtworzony wynik:", r[0])
    stop = time.time()
    t_1 = stop - start
    print("Czas wykonywania:", t_1)

def main10():
    T = '243517698'
    S = sorted(T)

    print("\n== Najdłuższy wspólny podciąg monotoniczny ==")
    print("Analizowane ciągi: -", S, "- oraz -", T)
    start = time.time()
    m, result = PD_compare3(S, T, return_m=True)
    print("wynik:", result)
    print("Odtworzona ścieżka: ", end='')
    r = ['']
    reconstruct_path(m, S, T, len(S) - 1, len(T) - 1, r)
    print("\nodtworzony wynik:", r[0])
    stop = time.time()
    t_1 = stop - start
    print("Czas wykonywania:", t_1)

def main11():
    T = 'mamma mia'
    S = sorted(T)

    print("\n== Najdłuższy wspólny podciąg monotoniczny ==")
    print("Analizowane ciągi: -", S, "- oraz -", T)
    start = time.time()
    m, result = PD_compare3(S, T, return_m=True)
    print("wynik:", result)
    print("Odtworzona ścieżka: ", end='')
    r = ['']
    reconstruct_path(m, S, T, len(S) - 1, len(T) - 1, r)
    print("\nodtworzony wynik:", r[0])
    stop = time.time()
    t_1 = stop - start
    print("Czas wykonywania:", t_1)

def main():
    main1()
    main2()
    main3()
    main4()
    main5()
    main6()
    main7()
    main8()
    main9()
    main10()
    main11()

main()