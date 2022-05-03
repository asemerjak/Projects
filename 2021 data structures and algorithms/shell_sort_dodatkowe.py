from time import time
import numpy as np


class Element:
    def __init__(self, priority, data):
        self.data = data
        self.priority = priority

    def __gt__(self, other):
        return self.priority > other.priority

    def __ge__(self, other):
        return self.priority >= other.priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __le__(self, other):
        return self.priority <= other.priority

    def __str__(self):
        return str(self.priority) + " : " + str(self.data)

class ShellMedianTab:
    def __init__(self):
        self.tab = []

    def insert(self, key, data):
        self.tab.append(Element(key, data))

    def print_tab(self):
        size = len(self.tab)
        for i in range(size):
            print(self.tab[i], end=',  ')
        print("\n")

    def shell_sort(self):
        size = len(self.tab)
        k = 0
        cnt = 0
        while (3**k - 1)/2 < size/3:
            k += 1
        h = int((3**k - 1)/2)
        while h > 0:
            for i in range(h, size):
                temp = self.tab[i]
                idx = i
                while idx >= h and self.tab[idx-h] > temp:
                    cnt += 1
                    self.tab[idx] = self.tab[idx-h]
                    idx -= h
                self.tab[idx] = temp
            h = int(h/3)
        return cnt

    def insertion_sort(self):
        size = len(self.tab)
        cnt = 0
        for i in range(size):
            temp = self.tab[i]
            j = i - 1
            while j >= 0 and temp < self.tab[j]:
                cnt += 1
                self.tab[j + 1] = self.tab[j]
                j -= 1
            self.tab[j + 1] = temp
        return cnt


def shell_main():
    data = np.random.randint(101, size=1000).tolist()
    tab1 = ShellMedianTab()
    tab2 = ShellMedianTab()
    for d in data:
        tab1.insert(d, " ")
        tab2.insert(d, " ")
    print("Tablica przed sortowaniem:")
    tab1.print_tab()
    start_shell = time()
    cnt1 = tab1.shell_sort()
    stop_shell = time()
    print("Tablica po sortowaniu shell:")
    tab1.print_tab()

    start_insertion = time()
    cnt2 = tab2.insertion_sort()
    stop_insertion = time()
    print("Czas wykonywania shell:", stop_shell - start_shell)
    print("Liczba przesunięć shell:", cnt1)

    print("\nCzas wykonywania insertion", stop_insertion - start_insertion)
    print("Liczba przesunięć insertion:", cnt2)

    t = (stop_insertion - start_insertion) / (stop_shell - start_shell)
    print("Shell jest szybsze {0:3.1f} razy".format(t))
    n = cnt2/cnt1
    print("Shell wykonuje {0:2.0f} razy mniej przesunięć".format(n))

shell_main()
