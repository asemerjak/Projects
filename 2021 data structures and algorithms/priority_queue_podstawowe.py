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
    def __init__(self):
        self.tab = []

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



def main():
    my_q = PriorityQueue()
    keys = [4, 7, 2, 5, 7, 6, 2, 1]
    vals = "algorytm"

    for i in range(len(keys)):
        my_q.enqueue(keys[i], vals[i])

    print("Kolejka priorytetowa w formie kopca - etap początkowy")
    my_q.print_heap()

    print("Pierwsza dana (dequeue):", my_q.dequeue())
    print("Pierwsza dana (peak):", my_q.peak())

    print("\nKolejka priorytetowa w formie tablicy:")
    my_q.print_tab()
    while not my_q.is_empty():
        my_q.dequeue()

    print("Kolejka opróżniona:")
    my_q.print_heap()
    my_q.print_tab()
    print("Czy kolejka jest pusta?", my_q.is_empty())

main()








