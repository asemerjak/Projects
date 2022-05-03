class Queue:
    def __init__(self):
        self.size = 5
        self.tab = [None for i in range(5)]
        self.i_write = 0
        self.i_read = 0

    def is_empty(self):
        return self.i_read == self.i_write

    def peek(self):
        return self.tab[self.i_read]

    def realloc(self):
        self.tab = [self.tab[i] if i < self.size else None for i in range(self.size*2)]
        self.size = self.size*2

    def dequeue(self):
        if self.is_empty():
            return None

        elem = self.tab[self.i_read]
        self.tab[self.i_read] = None
        self.i_read -= 1
        self.size -= 1
        return elem

    def enqueue(self, elem):
        if self.i_read + 1 >= self.size:
            self.realloc()
        i = self.i_read
        while i >= 0:
            self.tab[i + 1] = self.tab[i]
            i -= 1

        self.tab[self.i_write+1] = elem
        self.i_read += 1

    def print_tab(self):
        print(self.tab)

    def print_queue(self):
        if self.is_empty():
            print("Your queue is empty!")
            return
        for i in range(self.size):
            if self.tab[i]:
                print(self.tab[i], end = " ")
        print("\n")


def main():
    my_queue = Queue()
    print("Moja kolejka:", end=' ')
    my_queue.print_queue()
    print("Moja tablica:", end=" ")
    my_queue.print_tab()

    for i in range(4):
        my_queue.enqueue(i+1)

    print("Kolejka pod dodaniu kolejno 1, 2, 3, 4: ")
    my_queue.print_queue()
    print("Pierwsza wpisana dana:", my_queue.dequeue())
    print("Druga wpisana dana:", my_queue.peek())
    print("Aktualny stan kolejki:")
    my_queue.print_queue()

    for i in range(5, 9):
        my_queue.enqueue(i)

    print("Tablica po wstawieniu 4 kolejnych liczb:")
    my_queue.print_tab()

    print("Opróżnianie kolejki:")
    while not my_queue.is_empty():
        print(my_queue.dequeue())

    print("Czy kolejka jest pusta?", my_queue.is_empty())

main()







