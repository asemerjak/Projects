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

    def insert(self, d):
        self.tab.append(d)

    def print_tab(self):
        size = len(self.tab)
        for i in range(size):
            print(self.tab[i], end=',  ')
        print("\n")

    def median(self, tab):
        tab = sorted(tab)
        size = len(tab)
        idx = (size - 1) // 2
        if size % 2:
            return tab[idx]
        else:
            return (tab[idx] + tab[idx + 1])/2.0

    def median_of_medians(self, tab):
        temp = tab[:]
        while len(temp) > 5:
            size = len(temp)
            rest = size % 5

            sub_tabs = [temp[i: i+5] for i in range(0, size - rest, 5)]
            sub_tabs.append(temp[-rest:])
            print("podzbiory:", sub_tabs)
            sorted_sub_tabs = [sorted(sub_tab) for sub_tab in sub_tabs]
            temp = [sorted_sub_tab[2] for sorted_sub_tab in sorted_sub_tabs[0:-1]]
            temp[-1] = self.median(sorted_sub_tabs[-1])

        return self.median(temp)

    def median_of_medians_sort(self, start: int = 0, stop: int = None):
        if stop is None:
            stop = len(self.tab) - 1

        pivot: float = self.median_of_medians(self.tab[start: stop])
        print("\npivot:", pivot)
        i: int = start
        j: int = stop

        while i < j:
            while self.tab[i] < pivot:
                i = i + 1
            while self.tab[j] > pivot:
                j = j - 1
            if i <= j:
                a: float = self.tab[i]
                self.tab[i] = self.tab[j]
                self.tab[j] = a
                i = i + 1
                j = j - 1

        if start < j:
            self.median_of_medians_sort(start, j)

        if i < stop:
            self.median_of_medians_sort(i, stop)

def median_main():
    data = np.random.randint(101, size=64).tolist()
    tab1 = ShellMedianTab()

    for d in data:
        tab1.insert(d)
    print("Tablica przed sortowaniem:")
    tab1.print_tab()
    print("===============================")
    tab1.median_of_medians_sort()
    print("===============================")
    print("\nTablica po sortowaniu median:")
    tab1.print_tab()

median_main()