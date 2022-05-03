import numpy as np
from time import time

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

class PriorityQueue:
    def __init__(self, tab=[]):
        self.tab = tab

    def is_empty(self):
        return self.tab == []

    def peak(self):
        if self.is_empty():
            print("Your queue is empty!")
            return
        return self.tab[0]

    def enqueue(self, priority, data):
        new_elem = Element(priority, data)
        if self.is_empty():
            self.tab.append(new_elem)
            return

        i = len(self.tab)
        self.tab.append(None)
        i_parent = (i - 1)//2

        while i > 0 and self.tab[i_parent] < new_elem:
            self.tab[i] = self.tab[i_parent]
            i = i_parent
            i_parent = (i - 1)//2
        self.tab[i] = new_elem

    def dequeue(self):
        if self.is_empty():
            print("Your queue is empty!")
            return None
        elem_to_return = self.tab[0]
        n = len(self.tab) - 1
        v = self.tab.pop()
        if self.is_empty():
            return elem_to_return
        i = 0
        j = 1
        while j < n:
            if j + 1 < n and self.tab[j + 1] > self.tab[j]:
                j += 1

            if v >= self.tab[j]:
                break

            self.tab[i] = self.tab[j]
            i = j
            j = 2*j + 1

        self.tab[i] = v
        return elem_to_return

    def print_heap(self):
        print("==============")
        self._print_heap(0, 0)
        print("==============")

    def _print_heap(self, i, lvl):
        if i < len(self.tab):
            self._print_heap(2*i + 2, lvl + 10)
            print()
            for j in range(10, lvl + 10):
                print(end=" ")
            print(self.tab[i])
            self._print_heap(2*i + 1, lvl + 10)

    def print_tab(self):
        for elem in self.tab:
            print(elem, end=",  ")
        print("\n")


    def heapify_helper(self, n, node=None):
        if node is None:
            node = self.tab[0]
        sub_root = node
        left = 2*node + 1
        right = 2*node + 2

        if left < n and self.tab[sub_root] < self.tab[left]:
            sub_root = left
        if right < n and self.tab[sub_root] < self.tab[right]:
            sub_root = right

        if sub_root != node:
            self.tab[node], self.tab[sub_root] = self.tab[sub_root], self.tab[node]
            self.heapify_helper(n, sub_root)

    def heapify(self):
        n = len(self.tab)
        for i in range(n//2-1, -1, -1):
            self.heapify_helper(n, i)

    def sort_heapify(self):
        n = len(self.tab)
        self.heapify()
        new_t = [None for _ in range(len(self.tab))]
        for i in range(n - 1, -1, -1):
            new_t[i] = self.dequeue()
        return new_t

    def print_sort_heapify(self):
        sorted_tab = self.sort_heapify()
        for i in range(len(sorted_tab)):
            print(sorted_tab[i], end=', ')
        print("\n")

    def sort_enq(self):
        n = len(self.tab)
        new_t = [None for _ in range(len(self.tab))]
        for i in range(n - 1, -1, -1):
            new_t[i] = self.dequeue()
        return new_t

    def print_sort_enq(self):
        sorted_tab = self.sort_enq()
        for i in range(len(sorted_tab)):
            print(sorted_tab[i], end=', ')
        print("\n")


class ShiftSwapTab:
    def __init__(self):
        self.tab = []

    def insert(self, key, data):
        self.tab.append(Element(key, data))

    def swap(self):
        size = len(self.tab)
        for i in range(size):
            temp = i

            for j in range(i+1, size):
                if self.tab[temp] > self.tab[j]:
                    temp = j

            self.tab[i], self.tab[temp] = self.tab[temp], self.tab[i]

    def shift(self):
        size = len(self.tab)
        for i in range(size):
            temp = self.tab[i]
            j = i - 1

            while j >= 0 and temp < self.tab[j]:
                self.tab[j + 1] = self.tab[j]
                j -= 1

            self.tab[j + 1] = temp

    def print_tab(self):
        size = len(self.tab)
        for i in range(size):
            print(self.tab[i], end=',  ')
        print("\n")


def main():
    priorities = [3,6,1,8,4,12,7,13,9,22,15,5,11,16,18,20,25,21,27,30]
    data = []
    for p in priorities:
        data.append(Element(p, p))
    tab = PriorityQueue(data)
    print("Tablica nieposortowana:")
    tab.print_tab()
    print("Drzewo:")
    tab.print_heap()
    print("Kopiec:")
    tab.heapify()
    tab.print_heap()
    print("Tablica posortowana (heapify):")
    tab.print_sort_heapify()

def main_time():
    data_to_time = np.random.randint(1001, size=10000).tolist()
    tab_enque = PriorityQueue()
    start_enq = time()
    for p in data_to_time:
        tab_enque.enqueue(p, p)
    tab_enque.sort_enq()
    stop_enq = time()

    start_h = time()
    tab_heapify = PriorityQueue(data_to_time)
    tab_heapify.heapify()
    tab_heapify.sort_heapify()
    stop_h = time()

    print("Czas dla enqueue:", stop_enq-start_enq)
    print("Czas dla heapify:", stop_h-start_h)
    t = (stop_enq-start_enq)/(stop_h-start_h)
    print("Heapify jest szybsze {0:5.1f} razy".format(t))

def main_shift_swap():
    data = [(5, 'A'), (5, 'B'), (7, 'C'), (2, 'D'), (5, 'E'), (1, 'F'), (7, 'G'), (5, 'H'), (1, 'I'), (2, 'J')]
    tab1 = ShiftSwapTab()
    tab2 = ShiftSwapTab()
    for key, d in data:
        tab1.insert(key, d)
        tab2.insert(key, d)
    print("Tablica przed sortowaniem:")
    tab1.print_tab()
    tab1.swap()
    print("Tablica po sortowaniu swap:")
    tab1.print_tab()
    tab2.shift()
    print("Tablica po sortowaniu shift:")
    tab2.print_tab() #dla shift zostaje zachowana wejściowa koejność elementów


main()
main_time()
main_shift_swap()